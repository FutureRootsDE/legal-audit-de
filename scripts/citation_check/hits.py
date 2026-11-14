"""Validation of API hits: only canonical, pattern-checked structured fields survive.

Free texts (headline, Leitsatz) are deliberately dropped: the JSON output is read
by agents and must not carry text that originates from a third-party service.
"""
from __future__ import annotations

import re

ECLI_RE = re.compile(r"ECLI:[A-Z]{2}:[A-Za-z0-9]+:[0-9]{4}:[A-Za-z0-9.\-]+")
DATE_FIELD_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
LETTERS = "A-Za-zÄÖÜäöüß"
TYPE_RE = re.compile(rf"[{LETTERS}][{LETTERS} \-]{{0,39}}")
COURT_RE = re.compile(rf"[{LETTERS}0-9][{LETTERS}0-9 .()\-]{{0,59}}")
DOCUMENT_NUMBER_RE = re.compile(r"[A-Za-z0-9]{6,30}")
FILE_NUMBER_RE = re.compile(rf"[{LETTERS}0-9][{LETTERS}0-9 ./()\-]{{0,39}}")
MAX_FILE_NUMBERS = 10


def _clean_text(value: object, pattern: re.Pattern[str]) -> str | None:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        return None
    return value


def sanitize_hit(raw: dict) -> dict:
    """Canonical hit with validated field types; invalid fields become None."""
    numbers = raw.get("file_numbers")
    if not isinstance(numbers, list):
        numbers = []
    valid = [n for n in numbers if _clean_text(n, FILE_NUMBER_RE) is not None]
    return {
        "ecli": _clean_text(raw.get("ecli"), ECLI_RE),
        "date": _clean_text(raw.get("date"), DATE_FIELD_RE),
        "type": _clean_text(raw.get("type"), TYPE_RE),
        "document_number": _clean_text(raw.get("document_number"), DOCUMENT_NUMBER_RE),
        "court": _clean_text(raw.get("court"), COURT_RE),
        "file_numbers": valid[:MAX_FILE_NUMBERS],
    }
