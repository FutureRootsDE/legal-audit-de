"""Text rules for prose fields: forbidden phrases (RDG line, spec 6.8) and dash detection.

Only `prose` fields are checked; `verbatim` fields (evidence excerpts, URLs, curl commands,
snippets, expected output) are never passed in here.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Sequence

from .models import ValidationIssue

DEFAULT_PHRASES_PATH = Path(__file__).resolve().parents[2] / "templates" / "client-test" / "forbidden-phrases.json"
PHRASES_FILE_VERSION = 1

# Invisible characters that can split a word without changing how it looks.
INVISIBLE_RE = re.compile("[\u00ad\u180e\u200b-\u200d\u2060\ufeff]")
# Space variants that render like a normal space (NBSP, figure space, narrow NBSP).
SPACE_LIKE_RE = re.compile("[\u00a0\u2007\u202f]")
WHITESPACE_RE = re.compile(r"\s+")
# Hyphen characters removed for phrase matching, so "rechts-widrig" still matches.
HYPHENS_RE = re.compile("[-\u2010\u2011]")
PERCENT_RE = re.compile(r"\s*%\s*")
UMLAUT_FOLD = str.maketrans({"ä": "a", "ö": "o", "ü": "u"})
DIGRAPH_RE = re.compile("([aou])e")

# Dash characters that are never allowed in prose (figure dash to horizontal bar, two/three-em
# dashes, presentation forms) and hyphen-like characters used as a spaced pseudo dash.
DASH_CHAR_RE = re.compile("[\u2012-\u2015\u2e3a\u2e3b\ufe31\ufe32\ufe58]")
SPACED_HYPHEN_RE = re.compile("\\s[-\u2010\u2011\u2212\ufe63\uff0d]\\s")
DASH_CONTEXT = 20


def load_forbidden_phrases(path: Path | None = None) -> tuple[str, ...]:
    """Read the forbidden phrase list; the default lives next to the catalog, not in the cwd."""
    source = Path(path) if path is not None else DEFAULT_PHRASES_PATH
    data = json.loads(source.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or data.get("version") != PHRASES_FILE_VERSION:
        raise ValueError(f"{source}: expected an object with version {PHRASES_FILE_VERSION}")
    phrases = data.get("phrases")
    if not isinstance(phrases, list) or not phrases:
        raise ValueError(f"{source}: 'phrases' must be a non-empty list")
    if not all(isinstance(p, str) and normalize(p) for p in phrases):
        raise ValueError(f"{source}: every phrase must be a non-empty string")
    return tuple(phrases)


def _clean(text: str) -> str:
    """NFC, invisible characters removed, space look-alikes turned into plain spaces."""
    text = unicodedata.normalize("NFC", text)
    text = INVISIBLE_RE.sub("", text)
    return SPACE_LIKE_RE.sub(" ", text)


def normalize(text: str) -> str:
    """Matching form of a text: case and spelling variants (ß/ss, ö/oe/o) collapse to one form.

    Umlauts and their ae/oe/ue spellings both fold to the base vowel, so plural forms such as
    "Mängel" or "Verstöße" still contain the folded singular phrase.
    """
    text = _clean(text).casefold()
    text = HYPHENS_RE.sub("", text)
    text = PERCENT_RE.sub(" % ", text)
    text = text.translate(UMLAUT_FOLD)
    text = DIGRAPH_RE.sub(r"\1", text)
    return WHITESPACE_RE.sub(" ", text).strip()


def find_forbidden(text: str, phrases: Sequence[str]) -> list[str]:
    """Phrases (in list order, original spelling, each once) whose normalized form occurs in `text`."""
    haystack = normalize(text)
    found: list[str] = []
    for phrase in phrases:
        needle = normalize(phrase)
        if needle and needle in haystack and phrase not in found:
            found.append(phrase)
    return found


def _dash_matches(text: str) -> list[re.Match[str]]:
    cleaned = _clean(text)
    matches = list(DASH_CHAR_RE.finditer(cleaned)) + list(SPACED_HYPHEN_RE.finditer(cleaned))
    return sorted(matches, key=lambda m: m.start())


def find_dashes(text: str) -> list[str]:
    """Dash snippets found in `text`: dash characters and hyphens with whitespace on both sides."""
    return [m.group(0) for m in _dash_matches(text)]


def _describe_dash(match: re.Match[str]) -> str:
    char = match.group(0).strip()
    code = f"U+{ord(char):04X}"
    if match.group(0) != char:
        code += " mit Leerzeichen"
    before = match.string[max(0, match.start() - DASH_CONTEXT):match.start()]
    # keep the message itself dash-free when an earlier dash falls into the context
    before = SPACED_HYPHEN_RE.sub(" … ", DASH_CHAR_RE.sub("…", before)).strip()
    where = f" nach „{before}“" if before else " am Textanfang"
    return f"Gedankenstrich ({code}){where}; Ersatz: Komma, Doppelpunkt, „•“ oder „bis“"


def check_texts(items: Iterable[tuple[str, str]], phrases: Sequence[str]) -> list[ValidationIssue]:
    """Check (field path, text) pairs of prose fields; one issue per forbidden phrase and per dash."""
    issues: list[ValidationIssue] = []
    for path, text in items:
        value = str(text)
        for phrase in find_forbidden(value, phrases):
            issues.append(ValidationIssue(path, f"verbotene Wendung „{phrase}“"))
        for match in _dash_matches(value):
            issues.append(ValidationIssue(path, _describe_dash(match)))
    return issues
