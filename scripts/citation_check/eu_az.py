"""EU file numbers (C-311/18, T-553/23 P) and the CELEX numbers derived from them."""
from __future__ import annotations

import re
from dataclasses import dataclass

HYPHENS = "-‐‑‒–—−"
EU_AZ_RE = re.compile(rf"^([CT])\s?[{HYPHENS}]\s?([0-9]{{1,4}})/([0-9]{{2}})(?:\s?(PPU|P|R))?$")
LEGACY_AZ_RE = re.compile(r"^([0-9]{1,4})/([0-9]{2})$")
CELEX_RE = re.compile(r"^6[0-9]{4}[CT][A-Z][0-9]{4}(?:\([0-9]{2}\))?$")
ECLI_EU_RE = re.compile(r"^ECLI:EU:[CTF]:[0-9]{4}:[0-9]+$")
ORDER_SUFFIXES = ("", "(01)", "(02)", "(03)")

# CELEX type letters (second and third letter after the year) and their whitelisted German label
DOC_TYPES = {"CJ": "Urteil", "TJ": "Urteil", "CO": "Beschluss", "TO": "Beschluss",
             "CC": "Schlussantraege", "TC": "Schlussantraege", "CV": "Gutachten", "CN": "Mitteilung",
             "TN": "Mitteilung"}
TYPES_BY_COURT = {"C": ("CJ", "CO", "CC", "CV", "CN"), "T": ("TJ", "TO", "TC", "TN")}
COURT_NAMES = {"C": "EuGH", "T": "EuG"}
COURT_HINT_LETTER = {"EuGH": "C", "EuG": "T"}


@dataclass(frozen=True)
class EuCase:
    letter: str
    number: int
    year: int
    suffix: str = ""

    @property
    def court(self) -> str:
        return COURT_NAMES[self.letter]

    @property
    def az(self) -> str:
        tail = f" {self.suffix}" if self.suffix else ""
        return f"{self.letter}-{self.number}/{self.year % 100:02d}{tail}"


def full_year(two_digits: int) -> int:
    """Two-digit case year: up to 40 means 20xx, otherwise 19xx (the Court started in 1953)."""
    return 2000 + two_digits if two_digits <= 40 else 1900 + two_digits


def parse_eu_az(az: str, court: str | None = None) -> EuCase | None:
    """Parse an EU file number; legacy numbers without prefix only if `court` names EuGH or EuG."""
    text = re.sub(r"\s+", " ", az.strip())
    match = EU_AZ_RE.match(text)
    if match:
        letter, number, year, suffix = match.groups()
        return EuCase(letter, int(number), full_year(int(year)), suffix or "")
    legacy = LEGACY_AZ_RE.match(text)
    letter = COURT_HINT_LETTER.get(court or "")
    if legacy and letter:
        return EuCase(letter, int(legacy.group(1)), full_year(int(legacy.group(2))))
    return None


def celex_base(case: EuCase, doc_type: str) -> str:
    """CELEX scheme 6<year><type letters><4-digit number>, e.g. 62018CJ0311."""
    return f"6{case.year:04d}{doc_type}{case.number:04d}"


def celex_candidates(case: EuCase) -> list[str]:
    """All CELEX numbers a file number can have; orders may carry (01) to (03) for interim relief."""
    result: list[str] = []
    for doc_type in TYPES_BY_COURT[case.letter]:
        suffixes = ORDER_SUFFIXES if doc_type.endswith("O") else ("",)
        result.extend(celex_base(case, doc_type) + s for s in suffixes)
    return result


def doc_type_of(celex: str) -> str | None:
    """German document type of a CELEX number, or None if it is outside the whitelist."""
    if not CELEX_RE.match(celex):
        return None
    return DOC_TYPES.get(celex[5:7])
