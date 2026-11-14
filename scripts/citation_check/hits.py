"""Validation of API hits: only canonical, type-checked fields survive."""
from __future__ import annotations

import re

ECLI_RE = re.compile(r"ECLI:[A-Z]{2}:[A-Za-z0-9]+:\d{4}:[A-Za-z0-9.\-]+")
DATE_FIELD_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _clean_text(value: object, pattern: re.Pattern[str] | None = None) -> str | None:
    if not isinstance(value, str) or len(value) > 500:
        return None
    if pattern is not None and not pattern.fullmatch(value):
        return None
    return value


def sanitize_hit(raw: dict) -> dict:
    """Canonical hit with validated field types; invalid fields become None."""
    numbers = raw.get("file_numbers")
    if not isinstance(numbers, list):
        numbers = []
    return {
        "ecli": _clean_text(raw.get("ecli"), ECLI_RE),
        "date": _clean_text(raw.get("date"), DATE_FIELD_RE),
        "type": _clean_text(raw.get("type")),
        "document_number": _clean_text(raw.get("document_number")),
        "court": _clean_text(raw.get("court")),
        "file_numbers": [n for n in numbers if _clean_text(n) is not None],
        "headline": _clean_text(raw.get("headline")),
    }
