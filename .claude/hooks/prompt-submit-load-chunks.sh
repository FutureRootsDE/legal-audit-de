#!/usr/bin/env bash
# UserPromptSubmit-Hook fuer legal-audit-de.
# Delegiert an Python (robuster UTF-8-Support + stdin-Handling).
set -euo pipefail
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
python "${PROJECT_DIR}/.claude/hooks/prompt_submit.py"
