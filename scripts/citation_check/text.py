"""Cleaning of texts that originate from the API or from files before they are printed."""
from __future__ import annotations

import re

CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
DEFAULT_LIMIT = 200


def strip_controls(value: str) -> str:
    """Remove C0, DEL and C1 control characters (no exceptions, newlines included)."""
    return CONTROL_RE.sub("", value)


def short(value: object, limit: int = DEFAULT_LIMIT) -> str:
    """Control-free text of at most `limit` characters."""
    cleaned = strip_controls(str(value))
    return cleaned if len(cleaned) <= limit else cleaned[:limit - 3] + "..."


def clean_structure(data: object) -> object:
    """Recursively strip control characters from every string (keys and values)."""
    if isinstance(data, str):
        return strip_controls(data)
    if isinstance(data, list):
        return [clean_structure(item) for item in data]
    if isinstance(data, dict):
        return {clean_structure(key): clean_structure(value) for key, value in data.items()}
    return data
