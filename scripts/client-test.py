#!/usr/bin/env python3
"""Website-CheckUp command line (thin entry point; logic lives in client_report/cli.py).

Usage:
  python scripts/client-test.py check
  python scripts/client-test.py init https://example.de/
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from client_report.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
