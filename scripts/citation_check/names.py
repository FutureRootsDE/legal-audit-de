"""Short names near EU file numbers ("Schrems II", (Planet49)) and the informative name hint.

The hint compares a short name with the words of the official title. It never decides
anything: a mismatch only means that a person should look at the citation.
"""
from __future__ import annotations

import re

QUOTED = re.compile(r'"([^"\n]{2,40})"|„([^“”"\n]{2,40})[“”"]|“([^“”\n]{2,40})”|»([^«\n]{2,40})«')
BRACKETED = re.compile(r"\(([^()\n]{2,60})\)")
DATE_LIKE = re.compile(r"\b[0-9]{1,2}\.\s?[0-9]{1,2}\.\s?[0-9]{2,4}\b|\b(?:19|20)[0-9]{2}\b")
MEMO_START = re.compile(
    r"^(?:urt|urteil|beschl|beschluss|stand|rn|rdnr|leits|leitsatz|leitsaetze|vom|v\.|az|aktenzeichen|siehe|s\.|"
    r"gro(?:ss|ß)e|kammer|gerichtshof|eugh|eug|rs|rechtssache|vgl|ebenso|u\.a|ua|ecli|celex|anhaengig|anhängig|"
    r"abs|art|nr)\b", re.IGNORECASE)
WORD = re.compile(r"[a-z0-9äöüß]+")
STOP = frozenset({"und", "der", "die", "das", "gegen", "vom", "von", "des", "the", "and", "eugh", "eug"})
ROMAN = re.compile(r"^(?:i{1,3}|iv|v|vi{0,3}|ix|x)$")
MAX_NAMES = 4


def _clean(text: str) -> str | None:
    value = re.sub(r"\s+", " ", text).strip(" ,;.:-")
    if not (3 <= len(value) <= 40) or ":" in value or not re.search(r"[A-Za-zÄÖÜäöüß]", value):
        return None
    if DATE_LIKE.search(value) or MEMO_START.match(value) or not value[0].isupper():
        return None
    return value


def _bracket_parts(content: str) -> list[str]:
    return re.split(r"[;,/]", content)


def extract_names(segment: str) -> tuple[str, ...]:
    """Candidate short names in a line segment: quoted strings and bracketed words, deduplicated."""
    candidates: list[str] = []
    for match in QUOTED.finditer(segment):
        candidates.append(next(g for g in match.groups() if g))
    for match in BRACKETED.finditer(segment):
        candidates.extend(_bracket_parts(match.group(1)))
    found: list[str] = []
    for raw in candidates:
        value = _clean(raw)
        if value is not None and value not in found:
            found.append(value)
    return tuple(found[:MAX_NAMES])


def _significant(name: str) -> list[str]:
    return [w for w in WORD.findall(name.lower()) if len(w) >= 3 and w not in STOP and not ROMAN.match(w)]


def name_hint(candidates: tuple[str, ...], title_tokens: object) -> str:
    """match: all significant words of one name occur in the title; no_match; none: nothing to compare."""
    title = set(title_tokens) if title_tokens else set()
    usable = [w for w in (_significant(n) for n in candidates) if w]
    if not usable or not title:
        return "none"
    return "match" if any(all(w in title for w in words) for words in usable) else "no_match"
