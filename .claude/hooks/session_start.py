#!/usr/bin/env python3
"""
SessionStart-Hook fuer legal-audit-de (Python-Implementierung fuer UTF-8-Korrektheit).

1. Liest knowledge/INDEX.md und gibt es als additionalContext zurueck.
2. Prueft Pro-Mode-Marker (Standard-Kontext statt 1M) und ergaenzt
   einen Reminder im additionalContext, damit der Orchestrator bei
   Subagent-Dispatches die `-pro`-Varianten waehlt.
"""
import json
import os
import sys
from pathlib import Path

PRO_MODE_FILENAME = "pro-mode.json"
FALLBACK_FILENAME = "legal-audit-de-pro-mode.json"


def load_pro_mode_marker() -> dict | None:
    """Return parsed marker dict if Pro-Mode is enabled, else None."""
    candidates: list[Path] = []
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if plugin_data:
        candidates.append(Path(plugin_data) / PRO_MODE_FILENAME)
    candidates.append(Path.home() / ".claude" / FALLBACK_FILENAME)
    for path in candidates:
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("enabled") is True:
            data.setdefault("_marker_path", str(path))
            return data
    return None


def pro_mode_reminder(marker: dict) -> str:
    set_at = marker.get("set_at", "?")
    marker_path = marker.get("_marker_path", "?")
    return (
        "\n\n"
        "================================================================\n"
        "PRO-MODE AKTIV (Standard-Kontext, kein 1M)\n"
        "================================================================\n"
        "Beim Dispatch von Subagents IMMER die `-pro`-Variante waehlen:\n"
        "  - `legal-auditor-pro`     (statt `legal-auditor`)\n"
        "  - `legal-researcher-pro`  (statt `legal-researcher`)\n"
        "  - `legal-text-writer-pro` (statt `legal-text-writer`)\n"
        "\n"
        "Grund: Marker {path} (gesetzt {set_at}).\n"
        "Deaktivieren: `python3 scripts/legal-audit-pro-mode.py disable`\n"
        "================================================================\n"
    ).format(path=marker_path, set_at=set_at)


def main() -> int:
    # Force UTF-8 for stdout on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    index_path = os.path.join(project_dir, "knowledge", "INDEX.md")

    pieces: list[str] = []

    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            content = None
        if content is not None:
            header = (
                "# legal-audit-de — Knowledge Base Index (via SessionStart-Hook geladen)\n\n"
                "Die vollstaendigen Inhalte der unten gelisteten KB-Dateien werden "
                "**on demand** per UserPromptSubmit-Hook geladen, wenn der Prompt "
                "relevante Schlagwoerter enthaelt (siehe `.claude/hooks/triggers.json`). "
                "Zum expliziten Laden: `/legal-kb <thema>`.\n\n---\n\n"
            )
            pieces.append(header + content)

    marker = load_pro_mode_marker()
    if marker is not None:
        pieces.append(pro_mode_reminder(marker))

    if not pieces:
        return 0

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "".join(pieces),
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
