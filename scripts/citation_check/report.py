"""Human-readable and JSON output of the citation check.

Everything printed passes through text.strip_controls / clean_structure: texts from
the API or from files must not carry terminal escape sequences or hidden line breaks.
"""
from __future__ import annotations

from .ecli_writer import EcliOutcome
from .models import STATUSES
from .text import clean_structure, strip_controls

LABELS = {
    "DATE_MISMATCH": "DATE_MISMATCH: Treffer, aber KB nennt anderes Datum",
    "VERIFIED": "VERIFIED: Treffer in der API (Primaerbeleg, Marker bleibt redaktionelle Entscheidung)",
    "NOT_IN_DATASET": "NOT_IN_DATASET: abgedecktes Gericht, kein Treffer (kein Gegenbeweis!)",
    "ERROR": "ERROR: API nicht erreichbar oder Fehlerantwort",
    "UNCHECKED": "UNCHECKED: offline, kein Cache-Eintrag",
    "NOT_COVERED": "NOT_COVERED: Gericht nicht im Bestand der API (nicht abgefragt)",
}
GROUP_ORDER = ("DATE_MISMATCH", "VERIFIED", "NOT_IN_DATASET", "ERROR", "UNCHECKED", "NOT_COVERED")
CACHE_HINT = ("Hinweis: {n} Ergebnis(se) stammen aus dem lokalen Cache (Quelle: Cache). Die Echtheit lokaler "
              "Cache-Dateien ist nicht authentisch pruefbar; fuer einen Beleg mit --no-cache frisch abfragen.")


def _format_hit(hit: dict) -> str:
    return f"{hit.get('ecli') or '-'}  {hit.get('date') or '-'}  {hit.get('type') or '-'}"


def _render_entry(r: dict) -> list[str]:
    marker = "Marker: ja" if r["pending"] else "Marker: nein"
    date = f"KB-Datum {r['date']}" if r["date"] else "KB-Datum -"
    source = "  Quelle: Cache" if r["source"] == "cache" else ""
    out = [f"{r['file']}:{r['line']}  {r['az']}  [{r['court']}]  {date}  {marker}{source}"]
    out.extend(f"    -> {_format_hit(hit)}" for hit in r["hits"])
    if r["detail"]:
        out.append(f"    ! {r['detail']}")
    if r.get("note"):
        out.append(f"    i {r['note']}")
    return out


def _clean(lines: list[str]) -> str:
    return "\n".join(strip_controls(line) for line in lines)


def render_report(results: list[dict], summary: dict, warnings: list[str]) -> str:
    out = ["=== Zitatpruefung gegen Rechtsinformations-API des Bundes (Testphase) ===",
           f"{summary['citations']} Zitate, {summary['unique_az']} eindeutige Aktenzeichen, "
           f"{summary['api_requests']} API-Anfragen"
           + (" (offline)" if summary["offline"] else ""), ""]
    out.append("Zusammenfassung: " + ", ".join(f"{k}={v}" for k, v in summary["counts"].items() if v or k in STATUSES[:5]))
    out.append("")
    for status in GROUP_ORDER:
        group = [r for r in results if r["status"] == status]
        if not group:
            continue
        out.append(f"--- {LABELS[status]} ({len(group)}) ---")
        for r in group:
            out.extend(_render_entry(r))
        out.append("")
    if summary["counts"]["ERROR"]:
        out.append("Hinweis: API nicht erreichbar oder Fehler. Ergebnis fuer diese Zitate nicht aussagekraeftig; "
                   "weiter mit der Tier-1-Kaskade (rechtsprechung-im-internet.de).")
    if summary["cache_hits"]:
        out.append(CACHE_HINT.format(n=summary["cache_hits"]))
    out.append("Hinweis: NOT_IN_DATASET und NOT_COVERED sind kein Gegenbeweis. Die API deckt nur sieben "
               "Bundesgerichte ab (BGH ab etwa 2010) und ist eine Testphase ohne Stabilitaetszusage.")
    out.extend(f"Warnung: {w}" for w in warnings)
    return _clean(out)


def render_ecli(outcome: EcliOutcome) -> str:
    if outcome.dry_run:
        head, shown = "ECLI-Eintraege (Vorschau, es wird nichts geschrieben)", outcome.updates
    else:
        head, shown = "ECLI-Eintraege (geschrieben)", outcome.written
    out = ["", f"=== {head}: {len(shown)} ==="]
    for u in shown:
        flag = "  (aus Cache, UNGEPRUEFT)" if u.from_cache else ""
        out.append(f"{u.file}  {u.az}  ecli: {u.ecli}{flag}")
    out.append(f"Uebersprungen: {len(outcome.skipped)}")
    out.extend(f"  {s['file']}: {s['reason']}" for s in outcome.skipped)
    if outcome.failed:
        out.append(f"Schreibfehler: {len(outcome.failed)}")
        out.extend(f"  {f['file']}: {f['error']}" for f in outcome.failed)
    return _clean(out)


def json_payload(results: list[dict], summary: dict, warnings: list[str],
                 ecli: EcliOutcome | None) -> dict:
    """Structured, validated fields only; cleaned of control characters."""
    payload: dict = {"summary": summary, "citations": results, "warnings": warnings}
    if ecli is not None:
        written = {u.file for u in ecli.written}
        payload["ecli_updates"] = [
            {"file": u.file, "az": u.az, "ecli": u.ecli, "written": u.file in written,
             "source": "cache" if u.from_cache else "api"} for u in ecli.updates]
        payload["ecli_skipped"] = ecli.skipped
        payload["ecli_failed"] = ecli.failed
    return clean_structure(payload)
