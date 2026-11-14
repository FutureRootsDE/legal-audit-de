"""Report of the norm mode (--check-norms): counts, problem lists, law status, JSON payload."""
from __future__ import annotations

from .norm_check import NORM_STATUSES
from .text import clean_structure, strip_controls

BGBL_STATUSES = ("BGBL_OK", "BGBL_MISSING", "BGBL_UNCHECKED", "ERROR")
PROBLEMS = ("NORM_MISSING", "ABSATZ_MISSING", "NORM_UNKNOWN_LAW", "ERROR", "NORM_OLD_VERSION")
LABELS = {
    "NORM_MISSING": "NORM_MISSING: Paragraph nicht vorhanden oder weggefallen",
    "ABSATZ_MISSING": "ABSATZ_MISSING: Absatz oder Satz nicht vorhanden",
    "NORM_UNKNOWN_LAW": "NORM_UNKNOWN_LAW: Gesetz nicht zugeordnet oder nicht (mehr) im Inhaltsverzeichnis",
    "ERROR": "ERROR: Quelle nicht erreichbar oder Antwort unbrauchbar",
    "NORM_OLD_VERSION": "NORM_OLD_VERSION: alte Fassung (a. F.), nicht geprueft",
}


def _counts(rows: list[dict], statuses: tuple[str, ...]) -> dict[str, int]:
    counts = {s: 0 for s in statuses}
    for row in rows:
        counts[row["status"]] += 1
    return counts


def build_summary(norms: list[dict], laws: dict, eu_counts: dict, bgbl: list[dict], norm_requests: int,
                  bgbl_requests: int, skipped: int) -> dict:
    return {
        "citations": len(norms),
        "unique_refs": len({(n["law"], n["ref"]) for n in norms}),
        "counts": _counts(norms, NORM_STATUSES),
        "laws": len(laws),
        "eu_counts": dict(sorted(eu_counts.items())),
        "eu_note": "EU-Verordnungen werden in diesem Modus nur gezaehlt, nicht geprueft",
        "bgbl_refs": len(bgbl),
        "bgbl_counts": _counts(bgbl, BGBL_STATUSES),
        "norm_requests": norm_requests,
        "bgbl_requests": bgbl_requests,
        "skipped_inputs": skipped,
        "source": "https://www.gesetze-im-internet.de",
    }


def json_payload(norms: list[dict], laws: dict, changed: list[dict], bgbl: list[dict], bgbl_info: dict,
                 summary: dict, warnings: list[str]) -> dict:
    return clean_structure({"mode": "norms", "summary": summary, "norms": norms,
                            "laws": sorted(laws.values(), key=lambda law: law["law"]),
                            "changed_after_verification": changed, "bgbl": bgbl, "bgbl_info": bgbl_info,
                            "warnings": warnings})


def _lines_of(norms: list[dict], status: str) -> list[str]:
    out = []
    for n in (r for r in norms if r["status"] == status):
        detail = f"  ({n['detail']})" if n["detail"] else ""
        out.append(f"{n['file']}:{n['line']}  {n['ref']}{detail}")
    return out


def _law_lines(laws: dict) -> list[str]:
    out = ["--- Gesetze und Stand ---"]
    for law in sorted(laws.values(), key=lambda item: item["law"]):
        stand = f"{law['stand_date']} {law['stand_bgbl'] or ''}".strip() if law["stand_date"] else "-"
        slug = law["slug"] or "-"
        note = f"  ({law['note']})" if law["note"] else ""
        out.append(f"{law['law']}  [{slug}]  {law['state']}  Stand: {stand}{note}")
    return out


def render_text(payload: dict) -> str:
    summary = payload["summary"]
    out = ["=== Normpruefung gegen gesetze-im-internet.de ===",
           f"{summary['citations']} Normzitate, {summary['unique_refs']} eindeutige, {summary['laws']} Gesetze, "
           f"{summary['norm_requests']} Anfragen",
           "Zusammenfassung: " + ", ".join(f"{k}={v}" for k, v in summary["counts"].items() if v or k == "NORM_OK"),
           "EU-Verordnungen (nur gezaehlt): " + (", ".join(f"{k}={v}" for k, v in summary["eu_counts"].items())
                                                  or "keine"), ""]
    for status in PROBLEMS:
        lines = _lines_of(payload["norms"], status)
        if lines:
            out.extend([f"--- {LABELS[status]} ({len(lines)}) ---", *lines, ""])
    out.extend(_law_lines({law["law"]: law for law in payload["laws"]}))
    out.extend(_changed_lines(payload["changed_after_verification"]))
    out.extend(_bgbl_lines(payload["bgbl"], summary))
    out.extend(f"Warnung: {w}" for w in payload["warnings"])
    return "\n".join(strip_controls(line) for line in out)


def _changed_lines(changed: list[dict]) -> list[str]:
    out = ["", f"--- Gesetz nach verifiziert-am der zitierenden Datei geaendert ({len(changed)}, Hinweis, kein Fehler) ---"]
    for item in changed:
        lines = ",".join(str(n) for n in item["lines"][:8])
        out.append(f"{item['file']}  {item['law']}  verifiziert-am {item['verified_on']}  "
                   f"Aenderung vom {item['stand_date']} {item['stand_bgbl'] or ''}  Zeilen {lines}".rstrip())
    return out


def _bgbl_lines(bgbl: list[dict], summary: dict) -> list[str]:
    counts = ", ".join(f"{k}={v}" for k, v in summary["bgbl_counts"].items() if v)
    out = ["", f"--- BGBl.-Fundstellen ({len(bgbl)}): {counts or 'keine'} ---"]
    out.extend(f"{b['ref']}  {b['status']}  {b['places'][0]}" + (f"  ({b['detail']})" if b["detail"] else "")
               for b in bgbl if b["status"] != "BGBL_UNCHECKED")
    return out
