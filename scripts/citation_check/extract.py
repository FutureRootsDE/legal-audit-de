"""Extraction of Aktenzeichen, dates and pending markers from knowledge/*.md."""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from .fsutil import is_link_like
from .models import Citation
from .names import extract_names
from .text import short

MAX_FILE_BYTES = 2_000_000
MAX_LINE_CHARS = 5000
NOTE_LIMIT = 300

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
EU_PATTERN = re.compile(rf"(?<![\w/])([CT])\s?[{HYPHEN}]\s?([0-9]{{1,4}})/([0-9]{{2}})\b(?:\s?(PPU|P|R)(?!\w))?")
# Old file numbers without register letter ("Rs. 26/62") count only next to a named EuGH or EuG.
EU_LEGACY = re.compile(r"\b(?:Rs\.|Rechtssachen?)\s+([0-9]{1,4})/([0-9]{2})\b")
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
# Signals that an AZ in a judgment file belongs to another instance or proceeding, not to the file's court.
FOREIGN_SIGNAL = re.compile(
    r"\b(?:Vorinstanz\w*|vorgehend\w*|nachgehend\w*|Berufungsgericht\w*|Ausgangsverfahren|Vorverfahren|"
    r"LG|OLG|VG|OVG|VGH|AG|KG|FG|SG|LSG|LAG|ArbG|BayObLG|EuGH|EuG|EGMR)\b")
# BVerwG registers accepted by the file-court fallback, written in the official dotted form (6 C 12.20);
# A and K with a slash are register signs of the Oberverwaltungsgerichte and Verwaltungsgerichte.
BVERWG_FALLBACK_AZ = re.compile(r"^[0-9]{1,2}\s+(?:B|C|D|F|P|S|WD|WB|CN|CE|AV|VR|A)\s+[0-9]{1,4}\.[0-9]{2}$")
BVERWG_FALLBACK_SLASH = re.compile(r"^[0-9]{1,2}\s+(?:B|C)\s+[0-9]{1,4}/[0-9]{2}$")
# Short-form list member: ", 125/20", " und 126/20", " sowie 126/20" directly after an AZ.
SHORT_FORM = re.compile(r"\s*(?:,|\bund\b|\bsowie\b)\s*([0-9]{1,4})/([0-9]{2})(?![0-9/.\w])")
AZ_PARTS = re.compile(r"^(.+\s)[0-9]{1,4}/[0-9]{2}$")

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

FALLBACK_MAX_GAP = 30  # characters between AZ and a non-adjacent date for the nearest-date fallback
_MEMO_WORDS = (r"stand|gepr(?:ü|ue)ft|verifiziert|abgerufen|abruf|aktualisiert|zuletzt\s+ge(?:ä|ae)ndert|"
               r"eingelegt|anh(?:ä|ae)ngig\s+seit|in\s+kraft(?:\s+getreten)?|gilt\s+ab|anzuwenden\s+ab|"
               r"ver(?:ö|oe)ffentlicht|bgbl\.?")
_MEMO_PREP = r"(?:\s+(?:am|vom|seit|ab|zum|per|im))?"
# A date directly preceded by a memo word (Stand, geprueft, eingelegt am, ...) is no decision date.
MEMO_BEFORE = re.compile(rf"\b(?:{_MEMO_WORDS}){_MEMO_PREP}\W*$", re.IGNORECASE)
MEMO_BGBL = re.compile(r"\bBGBl\b[^;]{0,40}$", re.IGNORECASE)
MEMO_VERKUENDET = re.compile(r"\b(?:Gesetz|BGBl)\b.{0,40}verk(?:ü|ue)ndet(?:\s+\w+)?\W*$", re.IGNORECASE)
MEMO_ANY = re.compile(rf"\b(?:{_MEMO_WORDS})(?!\w)", re.IGNORECASE)
MEMO_TAIL = 45
GERICHT_ROW = re.compile(r"^\W*(?:\*\*Gericht:?\*\*|gericht\s*:)\W*([^|\n]*)", re.IGNORECASE)
HEAD_LINES = 60

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


def run_day() -> str:
    """ISO date of today; dates on or after it cannot be decision dates."""
    return date.today().isoformat()


def _is_memo_date(line: str, d_start: int, iso: str, today: str) -> bool:
    if iso >= today:
        return True
    tail = line[max(0, d_start - MEMO_TAIL):d_start]
    return bool(MEMO_BEFORE.search(tail) or MEMO_BGBL.search(tail) or MEMO_VERKUENDET.search(tail))


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


def _fallback_fits(line: str, az: str) -> bool:
    """File-court fallback: no foreign-instance signal in the line and a BVerwG-typical register."""
    if FOREIGN_SIGNAL.search(line):
        return False
    return bool(BVERWG_FALLBACK_AZ.fullmatch(az) or BVERWG_FALLBACK_SLASH.fullmatch(az))


def _bverwg_court(line: str, start: int, az: str, file_is_bverwg: bool) -> str | None:
    """Court for a BVerwG-style AZ: BVerwG, "unbekannt" (uncovered, doubtful), or None (named other court)."""
    if _bverwg_precedes(line, start):
        return "BVerwG"
    if not file_is_bverwg or _last_hint(line, start, COURT_MENTION) is not None:
        return None
    return "BVerwG" if _fallback_fits(line, az) else "unbekannt"


def _federal_spans(line: str, spans: list[Span], file_is_bverwg: bool = False) -> None:
    for pattern, court, needs_bverwg in FEDERAL_PATTERNS:
        for m in pattern.finditer(line):
            if not _is_free(spans, m.start(), m.end()):
                continue
            az = _normalize_az(m.group(0))
            if needs_bverwg:
                court = _bverwg_court(line, m.start(), az, file_is_bverwg)
                if court is None:
                    continue
            spans.append((m.start(), m.end(), az, court, court != "unbekannt"))


def _short_form_spans(line: str, spans: list[Span]) -> list[list[Span]]:
    """Add list members written without senate/register ("I ZR 90/20, 125/20 und 126/20").

    Returns the lists as groups of spans (head first): a date binds to the whole group.
    """
    groups: list[list[Span]] = []
    for head in list(spans):
        start, end, az, court, covered = head
        parts = AZ_PARTS.match(az)
        if not covered or not parts or court == "BVerwG":
            continue
        group, pos = [head], end
        while (m := SHORT_FORM.match(line, pos)):
            if not _is_free(spans, m.start(1), m.end()):
                break
            member = (m.start(1), m.end(), f"{parts.group(1)}{m.group(1)}/{m.group(2)}", court, True)
            spans.append(member)
            group.append(member)
            pos = m.end()
        if len(group) > 1:
            groups.append(group)
    return groups


def _eu_spans(line: str, spans: list[Span]) -> None:
    for m in EU_PATTERN.finditer(line):
        if _is_free(spans, m.start(), m.end()):
            az = f"{m.group(1)}-{m.group(2)}/{m.group(3)}" + (f" {m.group(4)}" if m.group(4) else "")
            court = _last_hint(line, m.start(), EU_HINT) or ("EuGH" if m.group(1) == "C" else "EuG")
            spans.append((m.start(), m.end(), az, court, False))
    for m in EU_LEGACY.finditer(line):
        court = _last_hint(line, m.start(), EU_HINT)
        if court in ("EuGH", "EuG") and _is_free(spans, m.start(), m.end()):
            letter = "C" if court == "EuGH" else "T"
            spans.append((m.start(), m.end(), f"{letter}-{m.group(1)}/{m.group(2)}", court, False))


def _lower_spans(line: str, spans: list[Span]) -> None:
    for m in LOWER_PATTERN.finditer(line):
        if not _is_free(spans, m.start(), m.end()):
            continue
        hint = _last_hint(line, m.start(), LOWER_HINT)
        if hint or LOWER_UNAMBIGUOUS.fullmatch(m.group(0)):
            spans.append((m.start(), m.end(), _normalize_az(m.group(0)), hint or "Land-/Oberlandesgericht", False))


def _line_matches(line: str, file_is_bverwg: bool = False) -> tuple[list[Span], list[list[Span]]]:
    """Find all Aktenzeichen in one line: ((start, end, az, court, covered) sorted, short-form list groups)."""
    spans: list[Span] = []
    _federal_spans(line, spans, file_is_bverwg)
    groups = _short_form_spans(line, spans)
    _eu_spans(line, spans)
    _lower_spans(line, spans)
    return sorted(spans), groups


def _spread_list_dates(spans: list[Span], groups: list[list[Span]], dates: list[str | None]) -> list[str | None]:
    """A date found for one member of a short-form list holds for all members that have none."""
    result = list(dates)
    for group in groups:
        indices = [spans.index(member) for member in group]
        known = {dates[i] for i in indices if dates[i] is not None}
        if len(known) == 1:
            value = known.pop()
            for i in indices:
                result[i] = result[i] or value
    return result


def _span_names(line: str, spans: list[Span], index: int) -> tuple[str, ...]:
    """Short names within 80 characters of an EU citation: text between two citations belongs to the first."""
    start, end = spans[index][0], spans[index][1]
    after = spans[index + 1][0] if index + 1 < len(spans) else len(line)
    lower = max(0, start - 80) if index == 0 else end
    return extract_names(line[lower:min(after, end + 80)])


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
    if right_gap and right_gap[1].lstrip().startswith(")"):
        right_gap = None  # a date inside a bracket belongs to the AZ before it, never to the one after it
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
        close = [g for g in (left, right) if g and len(g[1]) <= FALLBACK_MAX_GAP and not MEMO_ANY.search(g[1])]
        best = min(close, key=lambda g: len(g[1]), default=None)
        return (best[0], len(best[1])) if best else None
    return None


def _assign_dates(line: str, spans: list[Span], today: str) -> list[str | None]:
    """Bind every date to at most one AZ; per AZ the closest date wins."""
    best: list[tuple[int, str] | None] = [None] * len(spans)
    for d_start, d_end, iso in find_dates(line):
        if _is_memo_date(line, d_start, iso, today):
            continue
        owner = _date_owner(line, spans, d_start, d_end)
        if owner is None:
            continue
        index, distance = owner
        if best[index] is None or distance < best[index][0]:
            best[index] = (distance, iso)
    return [b[1] if b else None for b in best]


def _line_citations(line: str, lineno: int, rel_path: str, file_is_bverwg: bool = False,
                    today: str | None = None) -> list[Citation]:
    spans, groups = _line_matches(line, file_is_bverwg)
    if not spans:
        return []
    pending = bool(PENDING_RE.search(line))
    correction = bool(CORRECTION_RE.search(line))
    dates = [None] * len(spans) if correction else _spread_list_dates(
        spans, groups, _assign_dates(line, spans, today or run_day()))
    context = line.strip()[:160]
    return [Citation(rel_path, lineno, az, court, covered, date, pending, context, correction,
                     _span_names(line, spans, i) if az[:2] in ("C-", "T-") else ())
            for i, ((_, _, az, court, covered), date) in enumerate(zip(spans, dates))]


def is_bverwg_file(text: str, rel_path: str) -> bool:
    """Court fallback for judgment files: Gericht row/frontmatter, else file name or H1 names the BVerwG."""
    if "/urteile/" not in f"/{rel_path}":
        return False
    head = text.split("\n", HEAD_LINES)[:HEAD_LINES]
    for raw in head:
        row = GERICHT_ROW.match(raw.strip())
        if row:
            return row.group(1).strip().startswith("BVerwG")
    first_h1 = next((ln for ln in head if ln.startswith("# ")), "")
    return Path(rel_path).stem.lower().startswith("bverwg") or "BVerwG" in first_h1


def extract_with_notes(text: str, rel_path: str, today: str | None = None) -> tuple[list[Citation], int]:
    """Extract citations; lines above MAX_LINE_CHARS are skipped and counted. `today`: ISO run day."""
    citations: list[Citation] = []
    skipped = 0
    file_is_bverwg = is_bverwg_file(text, rel_path)
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.rstrip("\r")
        if len(line) > MAX_LINE_CHARS:
            skipped += 1
            continue
        citations.extend(_line_citations(line, lineno, rel_path, file_is_bverwg, today))
    return citations, skipped


def extract_citations(text: str, rel_path: str, today: str | None = None) -> list[Citation]:
    """Extract Aktenzeichen with file:line, nearby date and pending marker."""
    return extract_with_notes(text, rel_path, today)[0]


def _rel(path: Path, kb_path: Path) -> str:
    return path.relative_to(kb_path.parent).as_posix()


def _note(notes: list[str], message: str) -> None:
    notes.append(short(message, NOTE_LIMIT))


def _linked(md: Path, base: Path | None) -> bool:
    """True if the file or a directory between `base` and the file is a symlink or junction."""
    if is_link_like(md):
        return True
    if base is None:
        return False
    try:
        parents = md.relative_to(base).parents
    except ValueError:
        return True
    return any(is_link_like(base / parent) for parent in parents if parent != Path("."))


def read_limited(md: Path, rel: str, notes: list[str], base: Path | None = None) -> str | None:
    """Text of one KB file, read at most MAX_FILE_BYTES + 1 bytes; links and junctions are skipped (noted)."""
    if _linked(md, base):
        _note(notes, f"{rel}: Symlink oder Verzeichnis-Link uebersprungen")
        return None
    try:
        with md.open("rb") as handle:
            data = handle.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        _note(notes, f"{rel}: nicht lesbar ({type(exc).__name__})")
        return None
    if len(data) > MAX_FILE_BYTES:
        _note(notes, f"{rel}: Datei groesser als {MAX_FILE_BYTES} Bytes uebersprungen")
        return None
    return data.decode("utf-8", errors="replace")


def scan_kb(kb_path: Path, notes: list[str] | None = None, today: str | None = None) -> list[Citation]:
    """Scan all *.md files; skipped inputs (too large, too long lines, unreadable) go to `notes`."""
    notes = notes if notes is not None else []
    citations: list[Citation] = []
    if not kb_path.exists():
        return citations
    for md in sorted(kb_path.rglob("*.md")):
        rel = _rel(md, kb_path)
        text = read_limited(md, rel, notes, base=kb_path)
        if text is None:
            continue
        found, skipped = extract_with_notes(text, rel, today)
        citations.extend(found)
        if skipped:
            _note(notes, f"{rel}: {skipped} Zeilen laenger als {MAX_LINE_CHARS} Zeichen uebersprungen")
    return citations
