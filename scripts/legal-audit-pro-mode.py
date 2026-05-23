#!/usr/bin/env python3
"""legal-audit-pro-mode.py — Toggle zwischen 1M-Kontext-Default und Pro-Mode (Standard-Kontext).

Hintergrund
-----------
Standard laeuft das Plugin auf `claude-opus-4-7[1m]` (1M-Kontext-Variante). Pro-
Abonnenten ohne aktivierte 1M-Usage-Credits werden damit beim Plugin-Load
gesperrt (`API Error: Usage credits required for 1M context`). Pro-Mode loest
das, indem:

  1) das `model:`-Frontmatter in allen drei Agents auf `claude-opus-4-7`
     (Standard-Kontext, ca. 200K Tokens) umgestellt wird, und
  2) ein Marker-File `.claude/.pro-mode` angelegt wird. Der `/legal-audit`-
     Command erkennt den Marker und faehrt den Audit in mehreren 200K-
     Subagent-Sessions (eine pro Pass), mit deterministischem Execution-
     Logfile im Zielprojekt.

Aufruf
------
  python3 scripts/legal-audit-pro-mode.py enable
  python3 scripts/legal-audit-pro-mode.py disable
  python3 scripts/legal-audit-pro-mode.py status

Disclaimer: Outputs sind keine Rechtsberatung im Sinne von Paragraph 2 RDG.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_FILES = [
    REPO_ROOT / ".claude" / "agents" / "legal-auditor.md",
    REPO_ROOT / ".claude" / "agents" / "legal-researcher.md",
    REPO_ROOT / ".claude" / "agents" / "legal-text-writer.md",
]
MARKER_FILE = REPO_ROOT / ".claude" / ".pro-mode"

MODEL_1M = "model: claude-opus-4-7[1m]"
MODEL_STD = "model: claude-opus-4-7"
MODEL_LINE_RE = re.compile(r"^model: claude-opus-4-7(\[1m\])?$", re.MULTILINE)


def detect_mode() -> str:
    """Returns 'pro', 'default', or 'inconsistent'."""
    found_models = set()
    for f in AGENT_FILES:
        if not f.exists():
            continue
        match = MODEL_LINE_RE.search(f.read_text(encoding="utf-8"))
        if match:
            found_models.add(match.group(0))
    if len(found_models) > 1:
        return "inconsistent"
    if not found_models:
        return "unknown"
    only = next(iter(found_models))
    return "pro" if only == MODEL_STD else "default"


def swap_model(target: str) -> int:
    """Swap the model line in every agent file. Returns count of changed files."""
    if target not in (MODEL_1M, MODEL_STD):
        raise ValueError(f"Unsupported target: {target}")
    changed = 0
    for f in AGENT_FILES:
        if not f.exists():
            print(f"WARN  missing: {f.relative_to(REPO_ROOT)}", file=sys.stderr)
            continue
        text = f.read_text(encoding="utf-8")
        new_text, n = MODEL_LINE_RE.subn(target, text)
        if n == 0:
            print(f"WARN  no model line in {f.relative_to(REPO_ROOT)}", file=sys.stderr)
            continue
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"OK    {f.relative_to(REPO_ROOT)} -> {target.split(': ', 1)[1]}")
    return changed


def cmd_enable() -> int:
    changed = swap_model(MODEL_STD)
    MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    MARKER_FILE.write_text(
        "Pro-Mode aktiv. Das /legal-audit-Command laeuft jetzt in chunked\n"
        "Sub-Session-Execution (eine Subagent-Session pro Audit-Pass, Standard-\n"
        "Kontext 200K). Execution-Log: <zielprojekt>/docs/legal-audit/\n"
        "audit-execution-<timestamp>.log\n\n"
        "Disable: python3 scripts/legal-audit-pro-mode.py disable\n",
        encoding="utf-8",
    )
    print()
    print(f"Pro-Mode AKTIV ({changed} Agent-Datei(en) auf claude-opus-4-7 umgestellt).")
    print(f"Marker: {MARKER_FILE.relative_to(REPO_ROOT)}")
    print()
    print("Hinweis: Plattform-Adapter regenerieren mit:")
    print("  python3 scripts/sync-platforms.py --apply")
    return 0


def cmd_disable() -> int:
    changed = swap_model(MODEL_1M)
    if MARKER_FILE.exists():
        MARKER_FILE.unlink()
    print()
    print(f"Pro-Mode DEAKTIVIERT ({changed} Agent-Datei(en) auf claude-opus-4-7[1m] zurueckgesetzt).")
    print()
    print("Hinweis: Plattform-Adapter regenerieren mit:")
    print("  python3 scripts/sync-platforms.py --apply")
    return 0


def cmd_status() -> int:
    mode = detect_mode()
    marker = "vorhanden" if MARKER_FILE.exists() else "nicht vorhanden"
    print(f"Modus laut Agent-Frontmatter: {mode}")
    print(f"Marker {MARKER_FILE.relative_to(REPO_ROOT)}: {marker}")
    if mode == "pro" and not MARKER_FILE.exists():
        print("WARN  Inkonsistent: Frontmatter ist Pro-Mode, aber Marker fehlt.", file=sys.stderr)
        return 1
    if mode == "default" and MARKER_FILE.exists():
        print("WARN  Inkonsistent: Marker vorhanden, aber Frontmatter ist Default (1M).", file=sys.stderr)
        return 1
    if mode == "inconsistent":
        print("WARN  Agent-Frontmatter inkonsistent (unterschiedliche Modelle).", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("action", choices=["enable", "disable", "status"])
    args = parser.parse_args()
    return {"enable": cmd_enable, "disable": cmd_disable, "status": cmd_status}[args.action]()


if __name__ == "__main__":
    sys.exit(main())
