"""Extraction of Aktenzeichen, dates and pending markers from knowledge/*.md."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from .models import Citation


ROMAN = r"(?:XIII|XII|XI|IX|X|VIII|VII|VI|IV|V|III|II|I)"
HYPHEN = "-‐‑‒–—−"

# (regex, court, needs "BVerwG" in line). Order = priority on overlapping spans.
FEDERAL_PATTERNS: list[tuple[re.Pattern[str], str, bool]] = [
    (re.compile(rf"\b{ROMAN}a?\s+(?:ZR|ZB|ZA|StR|KZR|KVR|KRB|EnZR|EnVR|AnwZ|NotZ|StB|ARZ|AR)\s+\d{{1,4}}/\d{{2}}\b"),
     "BGH", False),
    (re.compile(r"\b\d{1,2}\s+Bv[RFLEQC]\s+\d{1,4}/\d{2}\b"), "BVerfG", False),
    (re.compile(r"\b\d{1,2}\s+(?:AZR|AZB|AZN|ABR|ABN)\s+\d{1,4}/\d{2}\b"), "BAG", False),
    (re.compile(r"\bB\s+\d{1,2}\s+[A-Z]{1,3}\s+\d{1,4}/\d{2}(?:\s+[A-Z])?\b"), "BSG", False),
    (re.compile(r"\b\d{1,2}\s+W\s*\(pat\)\s+\d{1,4}/\d{2}\b"), "BPatG", False),
    (re.compile(r"\b\d{1,2}\s+Ni\s+\d{1,4}/\d{2}\b"), "BPatG", False),
    (re.compile(rf"\b{ROMAN}\s+(?:R|B|S|K|E)\s+\d{{1,4}}/\d{{2}}\b"), "BFH", False),
    (re.compile(r"\b\d{1,2}\s+(?:A|B|C|D|F|K|P|S|WD|WB|CN|CE|AV|VR)\s+\d{1,4}[./]\d{2}\b"), "BVerwG", True),
]
BVERWG_HINT = re.compile(r"\bBVerwG\b")
EU_PATTERN = re.compile(rf"(?<![\w/])([CT])\s?[{HYPHEN}]\s?(\d{{1,4}})/(\d{{2}})\b")
EU_HINT = re.compile(r"\b(EuGH|EuG|EGMR)\b")
LOWER_PATTERN = re.compile(
    r"\b\d{1,3}\s+(?:U|O|S|W|Ca|Sa|Ws|C|F|K|Ss|Cs|Js|Qs|Ns|Ds|AR|Wx)\s+\d{1,5}/\d{2}\b")
LOWER_UNAMBIGUOUS = re.compile(r"\b\d{1,3}\s+(?:U|O|Ca|Sa)\s+\d{1,5}/\d{2}\b")
LOWER_HINT = re.compile(
    r"\b(?:OLG|LG|AG|OVG|VGH|VG|LAG|KG|FG|SG|LSG|ArbG|BayObLG)"
    r"(?:\s+[A-ZÄÖÜ][\wäöüß.\-]+(?:\s+(?:am\s+Main|I{1,3}))?)?")
HINT_WINDOW = 60

MONTHS = {m: i for i, m in enumerate(
    ["januar", "februar", "märz", "april", "mai", "juni", "juli", "august",
     "september", "oktober", "november", "dezember"], start=1)}
DATE_NUMERIC = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")
DATE_WRITTEN = re.compile(
    r"\b(\d{1,2})\.\s*(Januar|Februar|M(?:ä|ae)rz|April|Mai|Juni|Juli|August|September|"
    r"Oktober|November|Dezember)\s+(\d{4})\b", re.IGNORECASE)
DATE_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
DATE_MAX_DISTANCE = 120
PENDING_RE = re.compile(r"<<\s*VERIFIKATION\s+AUSSTEHEND", re.IGNORECASE)



def _iso(year: int, month: int, day: int) -> str | None:
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return None
    return f"{year:04d}-{month:02d}-{day:02d}"


def find_dates(line: str) -> list[tuple[int, int, str]]:
    """Return (start, end, iso) for every date in a line."""
    found: list[tuple[int, int, str]] = []
    for m in DATE_NUMERIC.finditer(line):
        iso = _iso(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        if iso:
            found.append((m.start(), m.end(), iso))
    for m in DATE_WRITTEN.finditer(line):
        month = MONTHS[m.group(2).lower().replace("ae", "ä")]
        iso = _iso(int(m.group(3)), month, int(m.group(1)))
        if iso:
            found.append((m.start(), m.end(), iso))
    for m in DATE_ISO.finditer(line):
        iso = _iso(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if iso:
            found.append((m.start(), m.end(), iso))
    return found


def _normalize_az(raw: str) -> str:
    return re.sub(r"\s+", " ", raw.strip())


def _last_hint(line: str, start: int, pattern: re.Pattern[str]) -> str | None:
    window = line[max(0, start - HINT_WINDOW):start]
    matches = list(pattern.finditer(window))
    return re.sub(r"\s+", " ", matches[-1].group(0)).strip() if matches else None


def _line_matches(line: str) -> list[tuple[int, int, str, str, bool]]:
    """Find all Aktenzeichen in one line: (start, end, az, court, covered)."""
    spans: list[tuple[int, int, str, str, bool]] = []

    def free(start: int, end: int) -> bool:
        return all(end <= s or start >= e for s, e, *_ in spans)

    for pattern, court, needs_hint in FEDERAL_PATTERNS:
        if needs_hint and not BVERWG_HINT.search(line):
            continue
        for m in pattern.finditer(line):
            if free(m.start(), m.end()):
                spans.append((m.start(), m.end(), _normalize_az(m.group(0)), court, True))
    for m in EU_PATTERN.finditer(line):
        if free(m.start(), m.end()):
            az = f"{m.group(1)}-{m.group(2)}/{m.group(3)}"
            court = _last_hint(line, m.start(), EU_HINT) or ("EuGH" if m.group(1) == "C" else "EuG")
            spans.append((m.start(), m.end(), az, court, False))
    for m in LOWER_PATTERN.finditer(line):
        if not free(m.start(), m.end()):
            continue
        hint = _last_hint(line, m.start(), LOWER_HINT)
        if hint or LOWER_UNAMBIGUOUS.fullmatch(m.group(0)):
            spans.append((m.start(), m.end(), _normalize_az(m.group(0)), hint or "Land-/Oberlandesgericht", False))
    return sorted(spans)


def _assign_dates(line: str, spans: list[tuple[int, int, str, str, bool]]) -> list[str | None]:
    """Give each date to its nearest Aktenzeichen, then pick the nearest per AZ."""
    dates = find_dates(line)
    best: list[tuple[int, str] | None] = [None] * len(spans)
    for d_start, d_end, iso in dates:
        distances = [max(s - d_end, d_start - e, 0) for s, e, *_ in spans]
        if not distances:
            continue
        owner = min(range(len(spans)), key=lambda i: distances[i])
        if distances[owner] <= DATE_MAX_DISTANCE and (best[owner] is None or distances[owner] < best[owner][0]):
            best[owner] = (distances[owner], iso)
    return [b[1] if b else None for b in best]


def extract_citations(text: str, rel_path: str) -> list[Citation]:
    """Extract Aktenzeichen with file:line, nearby date and pending marker."""
    citations: list[Citation] = []
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.rstrip("\r")
        spans = _line_matches(line)
        if not spans:
            continue
        pending = bool(PENDING_RE.search(line))
        context = line.strip()[:160]
        for (_, _, az, court, covered), date in zip(spans, _assign_dates(line, spans)):
            citations.append(Citation(rel_path, lineno, az, court, covered, date, pending, context))
    return citations


def _rel(path: Path, kb_path: Path) -> str:
    return path.relative_to(kb_path.parent).as_posix()


def scan_kb(kb_path: Path) -> list[Citation]:
    citations: list[Citation] = []
    if not kb_path.exists():
        return citations
    for md in sorted(kb_path.rglob("*.md")):
        try:
            text = md.read_bytes().decode("utf-8", errors="replace")
        except OSError as exc:
            print(f"Warnung: {md} nicht lesbar: {exc}", file=sys.stderr)
            continue
        citations.extend(extract_citations(text, _rel(md, kb_path)))
    return citations
