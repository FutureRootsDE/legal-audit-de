"""Check of norm citations against the law indexes: NORM_OK, NORM_MISSING, ABSATZ_MISSING, ..."""
from __future__ import annotations

from .norm_client import NormClient
from .norm_extract import NormRef
from .norm_laws import resolve

NORM_STATUSES = ("NORM_OK", "NORM_MISSING", "ABSATZ_MISSING", "NORM_UNKNOWN_LAW", "NORM_OLD_VERSION", "ERROR")


def ref_text(ref: NormRef) -> str:
    """Readable citation, e.g. "Art. 246a § 1 Abs. 2 EGBGB"."""
    if ref.art:
        head = f"Art. {ref.art} § {ref.number}"
    else:
        head = f"§ {ref.number}" if ref.kind == "§" else f"Art. {ref.number}"
    parts = [head]
    if ref.absaetze:
        parts.append("Abs. " + "+".join(str(a) for a in ref.absaetze))
    if ref.saetze:
        parts.append("Satz " + "+".join(str(s) for s in ref.saetze))
    return " ".join(parts + [ref.law])


def _key(ref: NormRef) -> str:
    if ref.art:
        return f"Art {ref.art}|§ {ref.number}"
    return f"{'§' if ref.kind == '§' else 'Art'} {ref.number}"


def _number_parts(number: str) -> tuple[int, str]:
    digits = "".join(c for c in number if c.isdigit())
    return int(digits), number[len(digits):]


def _in_gone_range(ref: NormRef, ranges: list) -> bool:
    kind = "§" if ref.kind == "§" else "Art"
    value = _number_parts(ref.number)
    return any(span[0] == kind and (span[1], span[2]) <= value <= (span[3], span[4]) for span in ranges)


class Coverage:
    """Which parts of one citation were actually compared with the law text."""

    def __init__(self) -> None:
        self.checked: list[str] = []
        self.unchecked: list[str] = []

    def mark(self, part: str, checked: bool) -> None:
        target = self.checked if checked else self.unchecked
        if part not in target:
            target.append(part)

    def as_dict(self) -> dict[str, list[str]]:
        return {"checked": list(self.checked), "unchecked": [p for p in self.unchecked if p not in self.checked]}


def _mark_parts(label: object) -> tuple[int, str]:
    text = str(label)
    digits = "".join(c for c in text if c.isdigit())
    return int(digits), text[len(digits):]


def _absatz_check(ref: NormRef, entry: dict, cover: Coverage) -> str | None:
    """Problem text for a missing Absatz; lettered Absaetze are compared with the marks, else left unchecked."""
    evaluated = True
    for label in ref.absaetze:
        number, letter = _mark_parts(label)
        if not letter:
            if number > entry["a"]:
                cover.mark("absatz", True)
                return f"Absatz {number} zitiert, Norm hat {entry['a']}"
        elif entry["m"]:
            if f"{number}{letter}" not in entry["m"]:
                cover.mark("absatz", True)
                return f"Absatz {number}{letter} zitiert, nicht vorhanden"
        else:
            evaluated = False
    if ref.absaetze:
        cover.mark("absatz", evaluated)
    return None


def _absatz_problem(ref: NormRef, entry: dict, cover: Coverage | None = None) -> str | None:
    cover = cover if cover is not None else Coverage()
    problem = _absatz_check(ref, entry, cover)
    if problem or not ref.saetze:
        return problem
    target = _satz_target(ref, entry)
    cover.mark("satz", target is not None)
    if target is not None and max(ref.saetze) > target:
        return f"Satz {max(ref.saetze)} zitiert, Absatz hat {target}"
    return None


def _satz_target(ref: NormRef, entry: dict) -> int | None:
    """Reliable sentence count of the cited Absatz (looked up by its mark), or None (not evaluated)."""
    sentences = entry["s"]
    if len(ref.absaetze) == 1:
        return sentences.get(str(ref.absaetze[0]))
    if not ref.absaetze and entry["a"] == 1 and len(sentences) == 1:
        return next(iter(sentences.values()))
    return None


def _unchecked_rest(ref: NormRef, cover: Coverage) -> None:
    if ref.absaetze:
        cover.mark("absatz", False)
    if ref.saetze:
        cover.mark("satz", False)
    for part in ref.others:
        cover.mark(part, False)


def _exists_as_article(ref: NormRef, index: dict) -> bool:
    return ref.kind == "Art" and f"Art {ref.number}" in index["arts"]


def check_norm(ref: NormRef, index: dict) -> tuple[str, str, dict | None, dict[str, list[str]]]:
    """(status, detail, index entry, coverage) of one citation against its law index.

    coverage lists the checked parts (paragraph, absatz, satz) and the parts that were not compared
    (Absatz/Satz without a reliable assignment; Nr., lit. and other qualifiers are never checked).
    """
    cover = Coverage()
    if ref.old_version:
        cover.mark("paragraph", False)
        _unchecked_rest(ref, cover)
        detail = "alte Fassung (a. F.), nicht gegen die geltende Fassung geprueft"
        return "NORM_OLD_VERSION", detail, None, cover.as_dict()
    cover.mark("paragraph", True)
    entry = index["norms"].get(_key(ref))
    if entry is None:
        _unchecked_rest(ref, cover)
        if _exists_as_article(ref, index):
            return "NORM_OK", "", None, cover.as_dict()
        gone = _in_gone_range(ref, index["ranges"])
        return "NORM_MISSING", "weggefallen (Bereich)" if gone else "nicht vorhanden", None, cover.as_dict()
    if entry["g"]:
        _unchecked_rest(ref, cover)
        return "NORM_MISSING", "weggefallen", entry, cover.as_dict()
    problem = _absatz_problem(ref, entry, cover)
    _unchecked_rest(ref, cover)
    return ("ABSATZ_MISSING" if problem else "NORM_OK"), problem or "", entry, cover.as_dict()


def _law_record(abbr: str, slug: str | None, note: str, client: NormClient) -> dict:
    record = {"law": abbr, "slug": slug, "note": note, "state": "unknown", "jurabk": [], "stand_date": None,
              "stand_bgbl": None, "builddate": None, "source": "none"}
    if slug is None:
        return record
    data = client.law(slug)
    if data.state != "ok":
        return {**record, "state": "error", "note": data.detail}
    index = data.index
    return {**record, "state": "ok", "jurabk": index["jurabk"], "stand_date": index["stand_date"],
            "stand_bgbl": index["stand_bgbl"], "builddate": index["builddate"],
            "source": "cache" if data.from_cache else "gii"}


def check_all(refs: list[NormRef], client: NormClient) -> tuple[list[dict], dict[str, dict]]:
    """Results per citation and one record per law abbreviation."""
    toc = client.toc()
    laws: dict[str, dict] = {}
    results: list[dict] = []
    for ref in refs:
        if ref.law not in laws:
            slug, note = resolve(ref.law, toc.slugs) if toc.state == "ok" else (None, toc.detail)
            laws[ref.law] = _law_record(ref.law, slug, note, client)
            if toc.state != "ok":
                laws[ref.law]["state"] = "error"
        results.append(_result(ref, laws[ref.law], client))
    return results, laws


def _result(ref: NormRef, law: dict, client: NormClient) -> dict:
    base = {"file": ref.file, "line": ref.line, "law": ref.law, "ref": ref_text(ref), "heading": None,
            "absaetze": None, "source": law["source"]}
    if law["state"] in ("unknown", "error"):
        cover = Coverage()
        cover.mark("paragraph", False)
        _unchecked_rest(ref, cover)
        status = "NORM_UNKNOWN_LAW" if law["state"] == "unknown" else "ERROR"
        return {**base, "status": status, "detail": law["note"], **cover.as_dict()}
    status, detail, entry, coverage = check_norm(ref, client.law(law["slug"]).index)
    if entry is not None:
        base = {**base, "heading": entry["t"], "absaetze": entry["a"]}
    return {**base, "status": status, "detail": detail, **coverage}


def changed_after_verification(refs: list[NormRef], laws: dict[str, dict]) -> list[dict]:
    """Laws whose last amending act is dated after the verification date of a citing file (a hint, no error)."""
    found: dict[tuple[str, str], dict] = {}
    for ref in refs:
        law = laws.get(ref.law)
        if not law or not law.get("stand_date") or not ref.verified_on or ref.verified_on >= law["stand_date"]:
            continue
        entry = found.setdefault((ref.law, ref.file), {
            "law": ref.law, "file": ref.file, "verified_on": ref.verified_on, "stand_date": law["stand_date"],
            "stand_bgbl": law["stand_bgbl"], "lines": []})
        if ref.line not in entry["lines"]:
            entry["lines"].append(ref.line)
    return sorted(found.values(), key=lambda e: (e["law"], e["file"]))
