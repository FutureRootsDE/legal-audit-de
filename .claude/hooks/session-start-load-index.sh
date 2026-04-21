#!/usr/bin/env bash
# SessionStart-Hook fuer legal-audit-de.
# Laedt INDEX.md der Rechts-Knowledge-Base als additionalContext.
# Implementierung in Python (robuster UTF-8-Support als Bash unter Windows).
set -euo pipefail
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
python "${PROJECT_DIR}/.claude/hooks/session_start.py"
