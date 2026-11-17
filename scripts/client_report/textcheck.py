"""Text rules for prose fields: forbidden phrases (RDG line, spec 6.8) and dash detection.

Only `prose` fields are checked; `verbatim` fields (evidence excerpts, URLs, curl commands,
snippets, expected output) are never passed in here.

Matching is a deliberately strict substring match on a normalized form (NFKC, invisible
characters removed, common Cyrillic/Greek look-alikes folded to Latin, case and umlaut
spelling folded, hyphens inside words removed). It hits word parts as well, so these
known false alarms are accepted on purpose and must be reworded in prose:

- "Konformitätserklärung", "Konformität" (contains "konform")
- "widrigenfalls", "Widrigkeit" (contain "widrig")
- "unverletzt" (contains "verletzt"), "unverboten" (contains "verboten")
- "garantieren" also matches "garantierend"; "nichtig" also matches "Nichtigkeit"

Not hits (checked): "berücksichtigt", "Benachrichtigung", "berichtigt",
"Datenschutzverletzung" (no "verletzt"), "Gewährleistung".

A line break inside a word is not joined, because joining lines would merge separate
words and produce false alarms.
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

# Invisible characters that are not category Cf but still render as nothing: combining
# grapheme joiner, Hangul fillers, Khmer inherent vowels, variation selectors.
EXTRA_INVISIBLE = frozenset(
    "͏ᅟᅠ឴឵ㅤﾠ" + "".join(chr(c) for c in range(0xFE00, 0xFE10))
)
# Space variants that render like a normal space (NBSP, figure space, narrow NBSP).
SPACE_LIKE_RE = re.compile("[   ]")
WHITESPACE_RE = re.compile(r"\s+")
# Hyphen and minus characters, used both inside words and in the dash rules.
HYPHEN_CHARS = "-‐‑−﹣－"
# Hyphens removed for phrase matching, so "rechts-widrig" or "rechts−widrig" still match.
HYPHENS_RE = re.compile(f"[{HYPHEN_CHARS}]")
PERCENT_RE = re.compile(r"\s*%\s*")
UMLAUT_FOLD = str.maketrans({"ä": "a", "ö": "o", "ü": "u"})
DIGRAPH_RE = re.compile("([aou])e")
# Frequent Cyrillic and Greek look-alikes of Latin letters (applied before casefolding,
# so capitals such as Greek Nu are mapped to their Latin look-alike, not their own lowercase).
HOMOGLYPHS = str.maketrans({
    # Cyrillic lowercase
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i",
    "ј": "j", "ѕ": "s", "һ": "h", "ԁ": "d", "ԛ": "q", "ԝ": "w", "ӏ": "l",
    # Cyrillic capitals
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P",
    "С": "C", "Т": "T", "Х": "X", "У": "Y", "І": "I", "Ј": "J", "Ѕ": "S", "Ԛ": "Q",
    "Ԝ": "W", "Ӏ": "I",
    # Greek capitals
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K", "Μ": "M",
    "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X",
    # Greek lowercase
    "α": "a", "ι": "i", "κ": "k", "ν": "v", "ο": "o", "ρ": "p", "υ": "u", "χ": "x",
    # Latin variants
    "ı": "i", "İ": "I",
})

# Dash characters that are never allowed in prose (figure dash to horizontal bar, two/three-em
# dashes, presentation forms) and hyphen-like characters used as a pseudo dash: spaced
# ("A - B", "A -- B") or doubled between words ("A--B").
DASH_CHAR_RE = re.compile("[‒-―⸺⸻︱︲﹘]")
# The trailing space is a lookahead so that "A - B - C" yields two matches.
SPACED_HYPHEN_RE = re.compile(f"\\s[{HYPHEN_CHARS}]+(?=\\s)")
DOUBLE_HYPHEN_RE = re.compile(f"(?<=\\w)[{HYPHEN_CHARS}]{{2,}}(?=\\w)")
DASH_PATTERNS = (DASH_CHAR_RE, SPACED_HYPHEN_RE, DOUBLE_HYPHEN_RE)
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


def _is_invisible(char: str) -> bool:
    return char in EXTRA_INVISIBLE or unicodedata.category(char) == "Cf"


def _clean(text: str) -> str:
    """NFKC, invisible characters removed, space look-alikes turned into plain spaces.

    NFKC runs again after the removal, because a removed character may have separated a
    letter from its combining mark.
    """
    text = unicodedata.normalize("NFKC", text)
    text = "".join(c for c in text if not _is_invisible(c))
    text = unicodedata.normalize("NFKC", text)
    return SPACE_LIKE_RE.sub(" ", text)


def normalize(text: str) -> str:
    """Matching form of a text: case and spelling variants (ß/ss, ö/oe/o) collapse to one form.

    Umlauts and their ae/oe/ue spellings both fold to the base vowel, so plural forms such as
    "Mängel" or "Verstöße" still contain the folded singular phrase.
    """
    text = _clean(text).translate(HOMOGLYPHS).casefold()
    text = HYPHENS_RE.sub("", text)
    text = PERCENT_RE.sub(" % ", text)
    text = text.translate(UMLAUT_FOLD)
    text = DIGRAPH_RE.sub(r"\1", text)
    return WHITESPACE_RE.sub(" ", text).strip()


def _occurrences(haystack: str, needle: str) -> list[tuple[int, int]]:
    """(start, end) of every occurrence of `needle`, overlapping ones included."""
    spans: list[tuple[int, int]] = []
    start = haystack.find(needle)
    while start != -1:
        spans.append((start, start + len(needle)))
        start = haystack.find(needle, start + 1)
    return spans


def find_forbidden(text: str, phrases: Sequence[str]) -> list[str]:
    """Phrases (in list order, original spelling, each once) whose normalized form occurs in `text`.

    A phrase whose every occurrence lies inside an occurrence of a longer listed phrase is left
    out, so "rechtswidrig" yields "rechtswidrig" only and not also "widrig".
    """
    haystack = normalize(text)
    spans: dict[str, list[tuple[int, int]]] = {}
    for phrase in phrases:
        needle = normalize(phrase)
        if needle and phrase not in spans:
            occurrences = _occurrences(haystack, needle)
            if occurrences:
                spans[phrase] = occurrences

    def covered(span: tuple[int, int], phrase: str) -> bool:
        return any(other != phrase and s <= span[0] and span[1] <= e and (e - s) > (span[1] - span[0])
                   for other, others in spans.items() for s, e in others)

    return [phrase for phrase, occurrences in spans.items()
            if not all(covered(span, phrase) for span in occurrences)]


def _dash_matches(text: str) -> list[re.Match[str]]:
    cleaned = _clean(text)
    matches = [m for pattern in DASH_PATTERNS for m in pattern.finditer(cleaned)]
    return sorted(matches, key=lambda m: m.start())


def find_dashes(text: str) -> list[str]:
    """Dash snippets found in `text`: dash characters, spaced hyphens and doubled hyphens."""
    return [m.group(0) for m in _dash_matches(text)]


def _strip_dashes(text: str) -> str:
    """Replace every dash match by an ellipsis so a message quoting `text` stays dash-free."""
    for pattern in DASH_PATTERNS:
        text = pattern.sub(" … ", text)
    return WHITESPACE_RE.sub(" ", text)


def _describe_dash(match: re.Match[str]) -> str:
    chars = match.group(0).strip()
    code = " ".join(f"U+{ord(c):04X}" for c in chars)
    if match.group(0) != chars:
        code += " mit Leerzeichen"
    before = match.string[max(0, match.start() - DASH_CONTEXT):match.start()]
    # keep the message itself dash-free when an earlier dash falls into the context
    before = _strip_dashes(before).strip()
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
