#!/usr/bin/env python3
"""
SessionStart-Hook fuer legal-audit-de (Python-Implementierung fuer UTF-8-Korrektheit).
Liest knowledge/INDEX.md und optionalen Pro-Mode-Marker, gibt beides als
additionalContext zurueck.
"""
import json
import os
import sys
from pathlib import Path


PRO_MODE_FILENAME = "pro-mode.json"
FALLBACK_FILENAME = "legal-audit-de-pro-mode.json"


def load_pro_mode_marker() -> dict | None:
    """
    Sucht den Pro-Mode-Marker in den bekannten Speicherorten.
    Gibt None zurueck wenn nicht aktiv.
    """
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
    """Baut den Kontext-Block fuer den Pro-Mode zurueck."""
    set_at = marker.get("set_at", "unbekannt")
    marker_path = marker.get("_marker_path", "unbekannt")
    return (
        "# legal-audit-de — Pro-Mode AKTIV\n\n"
        f"> Marker: `{marker_path}` | Aktiviert: {set_at}\n\n"
        "**Agenten-Routing fuer diese Session:**\n\n"
        "| Standard-Agent | Pro-Mode-Agent | Modell |\n"
        "|----------------|----------------|--------|\n"
        "| `legal-auditor` | `legal-auditor-pro` | claude-opus-4-7 |\n"
        "| `legal-researcher` | `legal-researcher-pro` | claude-opus-4-7 |\n"
        "| `legal-text-writer` | `legal-text-writer-pro` | claude-opus-4-7 |\n\n"
        "Alle `/legal-*`-Commands nutzen automatisch die `-pro`-Varianten. "
        "Standard-Kontext (~200k) statt 1M-Fenster — Kontext-Management-Regeln "
        "sind in jedem Pro-Agenten dokumentiert.\n\n"
        "Zum Deaktivieren: `python scripts/legal-audit-pro-mode.py disable`\n\n"
        "---\n\n"
    )


def main() -> int:
    # Force UTF-8 for stdout on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    index_path = os.path.join(project_dir, "knowledge", "INDEX.md")

    index_content = ""
    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                index_content = f.read()
        except Exception:
            pass

    # Build context parts
    parts: list[str] = []

    # 1. Pro-Mode-Reminder (falls aktiv)
    marker = load_pro_mode_marker()
    if marker:
        parts.append(pro_mode_reminder(marker))

    # 2. KB-Index
    if index_content:
        header = (
            "# legal-audit-de — Knowledge Base Index (via SessionStart-Hook geladen)\n\n"
            "Die vollstaendigen Inhalte der unten gelisteten KB-Dateien werden "
            "**on demand** per UserPromptSubmit-Hook geladen, wenn der Prompt "
            "relevante Schlagwoerter enthaelt (siehe `.claude/hooks/triggers.json`). "
            "Zum expliziten Laden: `/legal-kb <thema>`.\n\n---\n\n"
        )
        parts.append(header + index_content)

    if not parts:
        return 0

    additional_context = "\n\n".join(parts)

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
