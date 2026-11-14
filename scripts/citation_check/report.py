"""Human-readable and JSON output of the citation check."""
from __future__ import annotations

from .models import STATUSES

LABELS = {
    "DATE_MISMATCH": "DATE_MISMATCH: Treffer, aber KB nennt anderes Datum",
    "VERIFIED": "VERIFIED: Treffer in der API (Primaerbeleg, Marker bleibt redaktionelle Entscheidung)",
    "NOT_IN_DATASET": "NOT_IN_DATASET: abgedecktes Gericht, kein Treffer (kein Gegenbeweis!)",
    "ERROR": "ERROR: API nicht erreichbar oder Fehlerantwort",
    "UNCHECKED": "UNCHECKED: offline, kein Cache-Eintrag",
    "NOT_COVERED": "NOT_COVERED: Gericht nicht im Bestand der API (nicht abgefragt)",
}
GROUP_ORDER = ("DATE_MISMATCH", "VERIFIED", "NOT_IN_DATASET", "ERROR", "UNCHECKED", "NOT_COVERED")


def _format_hit(hit: dict) -> str:
    return f"{hit.get('ecli') or '-'}  {hit.get('date') or '-'}  {hit.get('type') or '-'}"


def _render_entry(r: dict) -> list[str]:
    marker = "Marker: ja" if r["pending"] else "Marker: nein"
    date = f"KB-Datum {r['date']}" if r["date"] else "KB-Datum -"
    out = [f"{r['file']}:{r['line']}  {r['az']}  [{r['court']}]  {date}  {marker}"]
    out.extend(f"    -> {_format_hit(hit)}" for hit in r["hits"])
    if r["detail"]:
        out.append(f"    ! {r['detail']}")
    if r.get("note"):
        out.append(f"    i {r['note']}")
    return out


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
    out.append("Hinweis: NOT_IN_DATASET und NOT_COVERED sind kein Gegenbeweis. Die API deckt nur sieben "
               "Bundesgerichte ab (BGH ab etwa 2010) und ist eine Testphase ohne Stabilitaetszusage.")
    out.extend(f"Warnung: {w}" for w in warnings)
    return "\n".join(out)


def render_ecli(updates: list[dict], skipped: list[dict], dry_run: bool) -> str:
    head = "ECLI-Eintraege (Vorschau, es wird nichts geschrieben)" if dry_run else "ECLI-Eintraege (geschrieben)"
    out = ["", f"=== {head}: {len(updates)} ==="]
    out.extend(f"{u['file']}  {u['az']}  ecli: {u['ecli']}" for u in updates)
    out.append(f"Uebersprungen: {len(skipped)}")
    out.extend(f"  {s['file']}: {s['reason']}" for s in skipped)
    return "\n".join(out)


def json_payload(results: list[dict], summary: dict, warnings: list[str],
                 updates: list[dict] | None, skipped: list[dict], dry_run: bool) -> dict:
    payload: dict = {"summary": summary, "citations": results, "warnings": warnings}
    if updates is not None:
        payload["ecli_updates"] = [{"file": u["file"], "az": u["az"], "ecli": u["ecli"],
                                    "written": not dry_run} for u in updates]
        payload["ecli_skipped"] = skipped
    return payload
