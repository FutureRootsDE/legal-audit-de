#!/usr/bin/env python3
"""
SessionStart-Hook fuer legal-audit-de (Python-Implementierung fuer UTF-8-Korrektheit).
Liest knowledge/INDEX.md und gibt es als additionalContext zurueck.
"""
import json
import os
import sys


def main() -> int:
    # Force UTF-8 for stdout on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    index_path = os.path.join(project_dir, "knowledge", "INDEX.md")

    if not os.path.isfile(index_path):
        # Still exit — no context to inject.
        return 0

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0

    header = (
        "# legal-audit-de — Knowledge Base Index (via SessionStart-Hook geladen)\n\n"
        "Die vollstaendigen Inhalte der unten gelisteten KB-Dateien werden "
        "**on demand** per UserPromptSubmit-Hook geladen, wenn der Prompt "
        "relevante Schlagwoerter enthaelt (siehe `.claude/hooks/triggers.json`). "
        "Zum expliziten Laden: `/legal-kb <thema>`.\n\n---\n\n"
    )

    additional_context = header + content

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
