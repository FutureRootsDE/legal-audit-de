#!/usr/bin/env python3
"""
PostToolUse-Hook fuer legal-audit-de.

Prueft nach Write/Edit auf Dateien unterhalb docs/legal-audit/, knowledge/, audits/, templates/:
  1. Disclaimer-Block ist am Dateianfang vorhanden (Haftungsausschluss + Keine Rechtsberatung)
  2. Finding-IDs (F-NNN) sind eindeutig (nur fuer LegalAudit.md-Dateien)

Output:
  - Warnung via stderr wenn Disclaimer fehlt (non-blocking).
  - Exit 2 (blocking) bei doppelten Finding-IDs.
"""
import json
import os
import re
import sys


RELEVANT_PATH_PATTERNS = [
    re.compile(r"docs[\\/]legal-audit[\\/].+\.md$"),
    re.compile(r"knowledge[\\/].+\.md$"),
    re.compile(r"templates[\\/].+\.md$"),
    re.compile(r"audits[\\/].+\.md$"),
]

DISCLAIMER_HEAD = re.compile(r"Haftungsausschluss", re.IGNORECASE)
DISCLAIMER_BODY = re.compile(r"Keine\s+Rechtsberatung", re.IGNORECASE)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0

    file_path = (data.get("tool_input") or {}).get("file_path") or ""
    if not file_path or not os.path.isfile(file_path):
        return 0

    normalized = file_path.replace("\\", "/")
    if not any(p.search(normalized) for p in RELEVANT_PATH_PATTERNS):
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            first_lines = "".join(f.readlines()[:40])
    except Exception:
        return 0

    # Check 1: Disclaimer-Block
    if not DISCLAIMER_HEAD.search(first_lines) or not DISCLAIMER_BODY.search(first_lines):
        print(
            f"[legal-audit-de] WARNUNG: {file_path} fehlt der verpflichtende "
            f"Disclaimer-Block (Haftungsausschluss + Keine Rechtsberatung) "
            f"in den ersten 40 Zeilen.",
            file=sys.stderr,
        )
        print(
            "[legal-audit-de] Template: templates/disclaimer-block.md",
            file=sys.stderr,
        )
        # Non-blocking warning.

    # Check 2: Finding-ID-Uniqueness (nur LegalAudit.md)
    if file_path.endswith("LegalAudit.md"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            return 0

        ids = re.findall(r"^## Finding (F-\d{3})", text, flags=re.MULTILINE)
        seen = set()
        dupes = set()
        for fid in ids:
            if fid in seen:
                dupes.add(fid)
            seen.add(fid)

        if dupes:
            print(
                f"[legal-audit-de] FEHLER: {file_path} enthaelt doppelte "
                f"Finding-IDs: {sorted(dupes)}",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
