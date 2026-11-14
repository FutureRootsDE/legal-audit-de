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


def _absatz_problem(ref: NormRef, entry: dict) -> str | None:
    if ref.absaetze and max(ref.absaetze) > entry["a"]:
        return f"Absatz {max(ref.absaetze)} zitiert, Norm hat {entry['a']}"
    target = _satz_target(ref, entry)
    if target is not None and ref.saetze and max(ref.saetze) > target:
        return f"Satz {max(ref.saetze)} zitiert, Absatz hat {target}"
    return None


def _satz_target(ref: NormRef, entry: dict) -> int | None:
    """Reliable sentence count of the cited Absatz, or None (not evaluated)."""
    sentences = entry["s"]
    if len(ref.absaetze) == 1 and ref.absaetze[0] <= len(sentences):
        return sentences[ref.absaetze[0] - 1]
    if not ref.absaetze and entry["a"] == 1 and sentences:
        return sentences[0]
    return None


def _exists_as_article(ref: NormRef, index: dict) -> bool:
    return ref.kind == "Art" and f"Art {ref.number}" in index["arts"]


def check_norm(ref: NormRef, index: dict) -> tuple[str, str, dict | None]:
    """(status, detail, index entry) of one citation against its law index."""
    if ref.old_version:
        return "NORM_OLD_VERSION", "alte Fassung (a. F.), nicht gegen die geltende Fassung geprueft", None
    entry = index["norms"].get(_key(ref))
    if entry is None:
        if _exists_as_article(ref, index):
            return "NORM_OK", "", None
        gone = _in_gone_range(ref, index["ranges"])
        return "NORM_MISSING", "weggefallen (Bereich)" if gone else "nicht vorhanden", None
    if entry["g"]:
        return "NORM_MISSING", "weggefallen", entry
    problem = _absatz_problem(ref, entry)
    return ("ABSATZ_MISSING", problem, entry) if problem else ("NORM_OK", "", entry)


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
            "absaetze": None}
    if law["state"] == "unknown":
        return {**base, "status": "NORM_UNKNOWN_LAW", "detail": law["note"]}
    if law["state"] == "error":
        return {**base, "status": "ERROR", "detail": law["note"]}
    status, detail, entry = check_norm(ref, client.law(law["slug"]).index)
    if entry is not None:
        base = {**base, "heading": entry["t"], "absaetze": entry["a"]}
    return {**base, "status": status, "detail": detail}


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
