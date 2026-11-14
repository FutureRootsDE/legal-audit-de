"""Extraction of Aktenzeichen, dates and pending markers from knowledge/*.md."""
from __future__ import annotations

import re
from pathlib import Path

from .models import Citation

MAX_FILE_BYTES = 2_000_000
MAX_LINE_CHARS = 5000

ROMAN = r"(?:XIII|XII|XI|IX|X|VIII|VII|VI|IV|V|III|II|I)"
HYPHEN = "-‐‑‒–—−"
FEDERAL_COURTS = "BGH|BFH|BVerwG|BAG|BSG|BVerfG|BPatG"

# (regex, court, needs a directly preceding "BVerwG"). Order = priority on overlapping spans.
FEDERAL_PATTERNS: list[tuple[re.Pattern[str], str, bool]] = [
    (re.compile(rf"\b{ROMAN}a?\s+(?:ZR|ZB|ZA|StR|KZR|KVR|KRB|EnZR|EnVR|AnwZ|NotZ|StB|ARZ|AR)\s+[0-9]{{1,4}}/[0-9]{{2}}\b"),
     "BGH", False),
    (re.compile(r"\b[1-6]\s+(?:StR|StB)\s+[0-9]{1,4}/[0-9]{2}\b"), "BGH", False),
    (re.compile(r"\b[0-9]{1,2}\s+Bv[RFLEQC]\s+[0-9]{1,4}/[0-9]{2}\b"), "BVerfG", False),
    (re.compile(r"\b[0-9]{1,2}\s+(?:AZR|AZB|AZN|ABR|ABN)\s+[0-9]{1,4}/[0-9]{2}\b"), "BAG", False),
    (re.compile(r"\bB\s+[0-9]{1,2}\s+[A-Z]{1,3}\s+[0-9]{1,4}/[0-9]{2}(?:\s+[A-Z])?\b"), "BSG", False),
    (re.compile(r"\b[0-9]{1,2}\s+W\s*\(pat\)\s+[0-9]{1,4}/[0-9]{2}\b"), "BPatG", False),
    (re.compile(r"\b[0-9]{1,2}\s+Ni\s+[0-9]{1,4}/[0-9]{2}\b"), "BPatG", False),
    (re.compile(rf"\b{ROMAN}\s+(?:R|B|S|K|E)\s+[0-9]{{1,4}}/[0-9]{{2}}\b"), "BFH", False),
    (re.compile(r"\b[0-9]{1,2}\s+(?:A|B|C|D|F|K|P|S|WD|WB|CN|CE|AV|VR)\s+[0-9]{1,4}[./][0-9]{2}\b"), "BVerwG", True),
]
EU_PATTERN = re.compile(rf"(?<![\w/])([CT])\s?[{HYPHEN}]\s?([0-9]{{1,4}})/([0-9]{{2}})\b")
EU_HINT = re.compile(r"\b(EuGH|EuG|EGMR)\b")
LOWER_PATTERN = re.compile(
    r"\b[0-9]{1,3}\s+(?:U|O|S|W|Ca|Sa|Ws|C|F|K|Ss|Cs|Js|Qs|Ns|Ds|AR|Wx|LA|LB|A)\s+[0-9]{1,5}/[0-9]{2}\b")
LOWER_UNAMBIGUOUS = re.compile(r"\b[0-9]{1,3}\s+(?:U|O|Ca|Sa)\s+[0-9]{1,5}/[0-9]{2}\b")
LOWER_HINT = re.compile(
    r"\b(?:OLG|LG|AG|OVG|VGH|VG|LAG|KG|FG|SG|LSG|ArbG|BayObLG)"
    r"(?:\s+[A-ZÄÖÜ][\wäöüß.\-]+(?:\s+(?:am\s+Main|I{1,3}))?)?")
# Any court name (federal, EU, instance) incl. an optional place: the last one before an AZ owns it.
COURT_MENTION = re.compile(
    rf"\b(?:{FEDERAL_COURTS}|EuGH|EuG|EGMR|OLG|LG|AG|OVG|VGH|VG|LAG|KG|FG|SG|LSG|ArbG|BayObLG)\b"
    r"(?:\s+[A-ZÄÖÜ][\wäöüß.\-]+(?:\s+(?:am\s+Main|I{1,3}))?)?")
HINT_WINDOW = 60

MONTHS = {m: i for i, m in enumerate(
    ["januar", "februar", "märz", "april", "mai", "juni", "juli", "august",
     "september", "oktober", "november", "dezember"], start=1)}
DATE_NUMERIC = re.compile(r"\b([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})\b")
DATE_WRITTEN = re.compile(
    r"\b([0-9]{1,2})\.\s*(Januar|Februar|M(?:ä|ae)rz|April|Mai|Juni|Juli|August|September|"
    r"Oktober|November|Dezember)\s+([0-9]{4})\b", re.IGNORECASE)
DATE_ISO = re.compile(r"\b([0-9]{4})-([0-9]{2})-([0-9]{2})\b")
DATE_MAX_DISTANCE = 120
PENDING_RE = re.compile(r"<<\s*VERIFIKATION\s+AUSSTEHEND", re.IGNORECASE)
CORRECTION_RE = re.compile(r"\b(?:korrigiert|statt|vormals|fälschlich(?:erweise)?|berichtigt)\b", re.IGNORECASE)

_SEP = rf"[\s,;:()\[\]/{re.escape(HYPHEN)}]*"
_COURT_WORDS = rf"(?:(?:{FEDERAL_COURTS}|EuGH|EuG)\b[\s,.:{re.escape(HYPHEN)}]*)?"
_INTRO = r"(?:(?:Urteil|Urt\.|Beschluss|Beschl\.|Entscheidung|Gerichtsbescheid)\s*)?(?:vom|v\.)"
INTRO_LEFT = re.compile(rf"{_SEP}{_COURT_WORDS}{_INTRO}\s*")
LEFT_ADJACENT = re.compile(rf"{_SEP}{_COURT_WORDS}(?:{_INTRO}\s*)?")
RIGHT_ADJACENT = re.compile(rf"{_SEP}{_COURT_WORDS}")
PAREN_OPEN = re.compile(r"\(\s*[A-Za-z.,\s]*$")

Span = tuple[int, int, str, str, bool]  # start, end, az, court, covered


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


def _bverwg_precedes(line: str, start: int) -> bool:
    """True if the nearest court name before `start` is the BVerwG."""
    court = _last_hint(line, start, COURT_MENTION)
    return court is not None and court.startswith("BVerwG")


def _is_free(spans: list[Span], start: int, end: int) -> bool:
    return all(end <= s or start >= e for s, e, *_ in spans)


def _federal_spans(line: str, spans: list[Span]) -> None:
    for pattern, court, needs_bverwg in FEDERAL_PATTERNS:
        for m in pattern.finditer(line):
            if not _is_free(spans, m.start(), m.end()):
                continue
            if needs_bverwg and not _bverwg_precedes(line, m.start()):
                continue
            spans.append((m.start(), m.end(), _normalize_az(m.group(0)), court, True))


def _eu_spans(line: str, spans: list[Span]) -> None:
    for m in EU_PATTERN.finditer(line):
        if _is_free(spans, m.start(), m.end()):
            az = f"{m.group(1)}-{m.group(2)}/{m.group(3)}"
            court = _last_hint(line, m.start(), EU_HINT) or ("EuGH" if m.group(1) == "C" else "EuG")
            spans.append((m.start(), m.end(), az, court, False))


def _lower_spans(line: str, spans: list[Span]) -> None:
    for m in LOWER_PATTERN.finditer(line):
        if not _is_free(spans, m.start(), m.end()):
            continue
        hint = _last_hint(line, m.start(), LOWER_HINT)
        if hint or LOWER_UNAMBIGUOUS.fullmatch(m.group(0)):
            spans.append((m.start(), m.end(), _normalize_az(m.group(0)), hint or "Land-/Oberlandesgericht", False))


def _line_matches(line: str) -> list[Span]:
    """Find all Aktenzeichen in one line: (start, end, az, court, covered)."""
    spans: list[Span] = []
    _federal_spans(line, spans)
    _eu_spans(line, spans)
    _lower_spans(line, spans)
    return sorted(spans)


def _neighbours(line: str, spans: list[Span], d_start: int, d_end: int) -> tuple[tuple[int, str] | None,
                                                                                 tuple[int, str] | None]:
    """Nearest AZ on the left and right of a date, each as (index, text between), or None if too far."""
    left = max((i for i, s in enumerate(spans) if s[1] <= d_start), default=None)
    right = min((i for i, s in enumerate(spans) if s[0] >= d_end), default=None)
    left_gap = (left, line[spans[left][1]:d_start]) if left is not None else None
    right_gap = (right, line[d_end:spans[right][0]]) if right is not None else None
    if left_gap and len(left_gap[1]) > DATE_MAX_DISTANCE:
        left_gap = None
    if right_gap and len(right_gap[1]) > DATE_MAX_DISTANCE:
        right_gap = None
    return left_gap, right_gap


def _date_owner(line: str, spans: list[Span], d_start: int, d_end: int) -> tuple[int, int] | None:
    """Index of the AZ a date belongs to and the gap length; None if unclear.

    A date introduced by vom/v./Urt. v./Beschl. v. binds to the AZ directly on its left;
    a date in front of an AZ binds to the AZ on its right; no binding across another AZ.
    """
    left, right = _neighbours(line, spans, d_start, d_end)
    if left and INTRO_LEFT.fullmatch(left[1]):
        return left[0], len(left[1])
    if left and PAREN_OPEN.search(left[1]) and line[d_end:d_end + 1] == ")" and LEFT_ADJACENT.fullmatch(left[1]):
        return left[0], len(left[1])
    left_ok = bool(left and LEFT_ADJACENT.fullmatch(left[1]))
    right_ok = bool(right and RIGHT_ADJACENT.fullmatch(right[1]))
    if left_ok != right_ok:
        owner = left if left_ok else right
        return owner[0], len(owner[1])
    if not left_ok and len(spans) == 1:
        near = left or right
        return (near[0], len(near[1])) if near else None
    return None


def _assign_dates(line: str, spans: list[Span]) -> list[str | None]:
    """Bind every date to at most one AZ; per AZ the closest date wins."""
    best: list[tuple[int, str] | None] = [None] * len(spans)
    for d_start, d_end, iso in find_dates(line):
        owner = _date_owner(line, spans, d_start, d_end)
        if owner is None:
            continue
        index, distance = owner
        if best[index] is None or distance < best[index][0]:
            best[index] = (distance, iso)
    return [b[1] if b else None for b in best]


def _line_citations(line: str, lineno: int, rel_path: str) -> list[Citation]:
    spans = _line_matches(line)
    if not spans:
        return []
    pending = bool(PENDING_RE.search(line))
    correction = bool(CORRECTION_RE.search(line))
    dates = [None] * len(spans) if correction else _assign_dates(line, spans)
    context = line.strip()[:160]
    return [Citation(rel_path, lineno, az, court, covered, date, pending, context, correction)
            for (_, _, az, court, covered), date in zip(spans, dates)]


def extract_with_notes(text: str, rel_path: str) -> tuple[list[Citation], int]:
    """Extract citations; lines above MAX_LINE_CHARS are skipped and counted."""
    citations: list[Citation] = []
    skipped = 0
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.rstrip("\r")
        if len(line) > MAX_LINE_CHARS:
            skipped += 1
            continue
        citations.extend(_line_citations(line, lineno, rel_path))
    return citations, skipped


def extract_citations(text: str, rel_path: str) -> list[Citation]:
    """Extract Aktenzeichen with file:line, nearby date and pending marker."""
    return extract_with_notes(text, rel_path)[0]


def _rel(path: Path, kb_path: Path) -> str:
    return path.relative_to(kb_path.parent).as_posix()


def _read_limited(md: Path, rel: str, notes: list[str]) -> str | None:
    if md.is_symlink():
        notes.append(f"{rel}: Symlink uebersprungen")
        return None
    try:
        with md.open("rb") as handle:
            data = handle.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        notes.append(f"{rel}: nicht lesbar ({exc})")
        return None
    if len(data) > MAX_FILE_BYTES:
        notes.append(f"{rel}: Datei groesser als {MAX_FILE_BYTES} Bytes uebersprungen")
        return None
    return data.decode("utf-8", errors="replace")


def scan_kb(kb_path: Path, notes: list[str] | None = None) -> list[Citation]:
    """Scan all *.md files; skipped inputs (too large, too long lines, unreadable) go to `notes`."""
    notes = notes if notes is not None else []
    citations: list[Citation] = []
    if not kb_path.exists():
        return citations
    for md in sorted(kb_path.rglob("*.md")):
        rel = _rel(md, kb_path)
        text = _read_limited(md, rel, notes)
        if text is None:
            continue
        found, skipped = extract_with_notes(text, rel)
        citations.extend(found)
        if skipped:
            notes.append(f"{rel}: {skipped} Zeilen laenger als {MAX_LINE_CHARS} Zeichen uebersprungen")
    return citations
