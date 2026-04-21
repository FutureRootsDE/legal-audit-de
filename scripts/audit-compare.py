#!/usr/bin/env python3
"""
Audit-Compare: Vergleicht zwei LegalAudit.md-Dateien (aktueller Lauf vs. letzter Lauf).

Output:
  - Neue Findings (im aktuellen, nicht im alten)
  - Behobene Findings (im alten, nicht im aktuellen)
  - Geaenderte Findings (Severity- oder Titel-Change)
  - Identische Findings (beide enthalten, unveraendert)

Usage:
  python audit-compare.py <aktuelles-LegalAudit.md> <altes-LegalAudit.md>
  python audit-compare.py --auto <projektname>
     → findet letztes Audit im Schatten-Archiv und vergleicht mit docs/legal-audit/LegalAudit.md
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
AUDITS = ROOT / "audits"

FINDING_RE = re.compile(
    r"^## Finding (F-\d{3}):\s*(.+?)$\n"
    r"(?:\n|.)*?"
    r"\*\*Severity:\*\*\s*(CRIT|HIGH|MED|LOW)",
    re.MULTILINE,
)


def parse_findings(path: Path) -> dict[str, dict]:
    """Liest LegalAudit.md und extrahiert Findings in ein Dict {F-NNN: {titel, severity}}."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    findings = {}
    for match in FINDING_RE.finditer(text):
        fid, titel, severity = match.group(1), match.group(2).strip(), match.group(3)
        findings[fid] = {"titel": titel, "severity": severity}
    return findings


def find_previous_audit(projekt: str) -> Path | None:
    """Sucht das letzte Audit-Verzeichnis im audits/-Archiv."""
    if not AUDITS.exists():
        return None
    candidates = sorted(
        [d for d in AUDITS.iterdir() if d.is_dir() and d.name.startswith(projekt)],
        reverse=True,
    )
    for c in candidates:
        la = c / "LegalAudit.md"
        if la.exists():
            return la
    return None


def diff(current: dict, previous: dict) -> dict:
    cur_ids = set(current.keys())
    prev_ids = set(previous.keys())

    neu = sorted(cur_ids - prev_ids)
    behoben = sorted(prev_ids - cur_ids)
    gemeinsam = sorted(cur_ids & prev_ids)

    geaendert = []
    identisch = []
    for fid in gemeinsam:
        if current[fid] != previous[fid]:
            geaendert.append(
                {
                    "id": fid,
                    "vorher": previous[fid],
                    "jetzt": current[fid],
                }
            )
        else:
            identisch.append(fid)

    return {
        "neu": [{"id": f, **current[f]} for f in neu],
        "behoben": [{"id": f, **previous[f]} for f in behoben],
        "geaendert": geaendert,
        "identisch": identisch,
        "summary": {
            "aktuell_gesamt": len(current),
            "vorher_gesamt": len(previous),
            "neu": len(neu),
            "behoben": len(behoben),
            "geaendert": len(geaendert),
            "identisch": len(identisch),
        },
    }


def render(result: dict, current_path: Path, previous_path: Path) -> str:
    s = result["summary"]
    lines = [
        "=== Audit-Compare ===",
        f"Aktuell:  {current_path}",
        f"Vorher:   {previous_path}",
        "",
        f"Summary: {s['aktuell_gesamt']} aktuell vs. {s['vorher_gesamt']} vorher",
        f"  Neu:        {s['neu']}",
        f"  Behoben:    {s['behoben']}",
        f"  Geaendert:  {s['geaendert']}",
        f"  Identisch:  {s['identisch']}",
        "",
    ]
    if result["neu"]:
        lines.append("--- NEUE Findings (Regression oder neu entdeckt) ---")
        for f in result["neu"]:
            lines.append(f"  [{f['severity']}] {f['id']}: {f['titel']}")
        lines.append("")
    if result["behoben"]:
        lines.append("--- BEHOBENE Findings (im vorherigen, nicht mehr da) ---")
        for f in result["behoben"]:
            lines.append(f"  [{f['severity']}] {f['id']}: {f['titel']}")
        lines.append("")
    if result["geaendert"]:
        lines.append("--- GEAENDERTE Findings (Severity oder Titel) ---")
        for f in result["geaendert"]:
            v, j = f["vorher"], f["jetzt"]
            lines.append(
                f"  {f['id']}: [{v['severity']}→{j['severity']}] "
                f"\"{v['titel']}\" → \"{j['titel']}\""
            )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("current", nargs="?", help="Aktuelles LegalAudit.md")
    p.add_argument("previous", nargs="?", help="Altes LegalAudit.md")
    p.add_argument("--auto", metavar="PROJEKT", help="Automatisch letztes Audit im audits/-Archiv finden")
    p.add_argument("--json", action="store_true", help="JSON-Output")
    args = p.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.auto:
        projekt_dir = Path(args.auto).expanduser().resolve()
        current = projekt_dir / "docs" / "legal-audit" / "LegalAudit.md"
        previous = find_previous_audit(projekt_dir.name)
        if not current.exists():
            print(f"FEHLER: Aktuelles Audit nicht gefunden: {current}", file=sys.stderr)
            return 1
        if not previous:
            print(f"HINWEIS: Kein vorheriges Audit im Archiv fuer '{projekt_dir.name}'. Nichts zu vergleichen.")
            return 0
    else:
        if not args.current or not args.previous:
            p.error("current und previous Pfade benoetigt (oder --auto <projekt>)")
        current = Path(args.current)
        previous = Path(args.previous)

    cur_findings = parse_findings(current)
    prev_findings = parse_findings(previous)
    result = diff(cur_findings, prev_findings)

    if args.json:
        print(json.dumps({"current": str(current), "previous": str(previous), "diff": result}, ensure_ascii=False, indent=2))
    else:
        print(render(result, current, previous))

    return 0


if __name__ == "__main__":
    sys.exit(main())
