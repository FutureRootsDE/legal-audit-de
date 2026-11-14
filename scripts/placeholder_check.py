"""Shared placeholder detection for find-placeholders.py and legal-status.py.

The exact marker form is `<<VERIFIKATION AUSSTEHEND>>` (or `<<UNVERIFIZIERT>>`). Broken or deviating variants
(extra text, single closing bracket, marker split over two lines, unclosed marker) are reported as warnings so
they do not go unnoticed. Markers inside inline code (backticks) are never reported: change notes quote them.
"""
from __future__ import annotations

import re
from typing import NamedTuple

EXACT_RE = re.compile(r"<<\s*(VERIFIKATION\s+AUSSTEHEND|UNVERIFIZIERT)\s*>>", re.IGNORECASE)
_EXACT_FULL = re.compile(r"<<\s*(?:VERIFIKATION\s+AUSSTEHEND|UNVERIFIZIERT)\s*>>", re.IGNORECASE)
_KEYWORD = r"(?:VERIFIKATION|UNVERIFIZIERT)"
# A marker candidate: one or two "<", at most 80 characters without angle brackets around a keyword, one or two ">".
_CANDIDATE = re.compile(rf"(?<!<)<{{1,2}}[^<>]{{0,80}}?{_KEYWORD}[^<>]{{0,80}}?>{{1,2}}(?!>)", re.IGNORECASE)
_UNCLOSED = re.compile(rf"(?<!<)<{{1,2}}\s*{_KEYWORD}(?![^<>]*>)[^<>\n]{{0,80}}", re.IGNORECASE)
_INLINE_CODE = re.compile(r"`[^`\n]*`")


class Deviant(NamedTuple):
    line: int
    reason: str
    snippet: str


def _mask_inline_code(text: str) -> str:
    """Blank out inline code spans (same length, newlines kept) so quoted markers are ignored."""
    return _INLINE_CODE.sub(lambda m: " " * len(m.group(0)), text)


def _reason(candidate: str) -> str | None:
    """Why a candidate deviates from the exact form; None if it is exact on a single line."""
    if _EXACT_FULL.fullmatch(candidate):
        return "ueber mehrere Zeilen" if "\n" in candidate else None
    if not candidate.startswith("<<"):
        return "einfaches oeffnendes <"
    if not candidate.endswith(">>"):
        return "einfaches schliessendes >"
    if "\n" in candidate:
        return "ueber mehrere Zeilen"
    return "Zusatztext oder abweichende Schreibweise"


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def find_deviant(text: str) -> list[Deviant]:
    """Return all marker-like constructs that differ from the exact single-line form."""
    masked = _mask_inline_code(text)
    found: list[Deviant] = []
    for m in _CANDIDATE.finditer(masked):
        reason = _reason(m.group(0))
        if reason:
            found.append(Deviant(_line_of(text, m.start()), reason, " ".join(m.group(0).split())[:120]))
    for m in _UNCLOSED.finditer(masked):
        found.append(Deviant(_line_of(text, m.start()), "nicht geschlossen", " ".join(m.group(0).split())[:120]))
    return sorted(set(found))
