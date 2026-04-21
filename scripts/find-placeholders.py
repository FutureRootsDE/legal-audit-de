#!/usr/bin/env python3
"""
Findet alle <<VERIFIKATION AUSSTEHEND>> / <<UNVERIFIZIERT>>-Platzhalter in knowledge/
und gibt sie als strukturierte Liste aus (fuer /legal-update --fix-pending).

Output-Format (JSON):
[
  {
    "file": "knowledge/themen/preisangaben.md",
    "line": 47,
    "context": "OLG Hamburg 3 U 37/22 <<VERIFIKATION AUSSTEHEND>> Streichpreis-Urteil",
    "placeholder_type": "VERIFIKATION AUSSTEHEND"
  },
  ...
]
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
KB = ROOT / "knowledge"
PLACEHOLDER_RE = re.compile(r"<<\s*(VERIFIKATION\s+AUSSTEHEND|UNVERIFIZIERT)\s*>>", re.IGNORECASE)


def scan() -> list[dict]:
    results = []
    if not KB.exists():
        return results
    for md in sorted(KB.rglob("*.md")):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            for match in PLACEHOLDER_RE.finditer(line):
                placeholder_type = re.sub(r"\s+", " ", match.group(1).strip().upper())
                # Kontext: die Zeile selbst, mit Hervorhebung
                ctx = line.strip()
                # Versuche umliegende 2 Zeilen als zusaetzlichen Kontext
                prev_line = lines[i - 2].strip() if i > 1 else ""
                next_line = lines[i].strip() if i < len(lines) else ""
                results.append({
                    "file": str(md.relative_to(ROOT)).replace("\\", "/"),
                    "line": i,
                    "context": ctx,
                    "context_before": prev_line,
                    "context_after": next_line,
                    "placeholder_type": placeholder_type,
                })
    return results


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--group-by-file", action="store_true", help="Gruppiert Output nach Datei")
    args = p.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    placeholders = scan()

    if args.json:
        print(json.dumps(placeholders, ensure_ascii=False, indent=2))
        return 0

    if args.group_by_file:
        by_file: dict[str, list[dict]] = {}
        for p in placeholders:
            by_file.setdefault(p["file"], []).append(p)
        print(f"=== {len(placeholders)} Platzhalter in {len(by_file)} Dateien ===\n")
        for fn in sorted(by_file):
            entries = by_file[fn]
            print(f"{fn}  ({len(entries)} Platzhalter)")
            for e in entries:
                print(f"  L{e['line']} [{e['placeholder_type']}]: {e['context'][:120]}")
            print()
    else:
        print(f"=== {len(placeholders)} Platzhalter gesamt ===\n")
        for p in placeholders:
            print(f"{p['file']}:{p['line']} [{p['placeholder_type']}]")
            print(f"  {p['context'][:140]}")
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
