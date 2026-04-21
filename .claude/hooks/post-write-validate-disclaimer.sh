#!/usr/bin/env bash
# PostToolUse-Hook fuer legal-audit-de.
# Delegiert an Python.
set -euo pipefail
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
python "${PROJECT_DIR}/.claude/hooks/post_write.py"
