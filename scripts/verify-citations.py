#!/usr/bin/env python3
"""
Sammelpruefung von Bundesgerichts-Aktenzeichen in knowledge/ gegen die
Rechtsinformations-API des Bundes (https://testphase.rechtsinformationen.bund.de).

Die API ist OPTIONALE Beschleunigung (Testphase, keine Stabilitaetszusage, keine
dokumentierte Datenlizenz). Sie deckt nur sieben Bundesgerichte ab (BGH ab etwa
2010, BFH, BVerwG, BPatG, BAG, BSG, BVerfG). "Kein Treffer" ist deshalb NIE ein
Gegenbeweis; nicht abgedeckte Gerichte (OLG/LG/OVG/VG/LAG, EuGH/EuG) werden nur
ausgewiesen, nicht abgefragt.

Klassifikation je Zitat:
  VERIFIED        Treffer, KB-Datum stimmt oder fehlt
  DATE_MISMATCH   Treffer, aber die KB nennt ein anderes Datum
  NOT_IN_DATASET  abgedecktes Gericht, kein Treffer (kein Gegenbeweis)
  NOT_COVERED     Gericht nicht im Bestand der API
  ERROR           API nicht erreichbar oder Fehlerantwort
  UNCHECKED       nur mit --offline: kein Cache-Eintrag vorhanden

Schreibt standardmaessig nie in KB-Dateien. Nur mit --write-ecli wird fuer
Dateien unter knowledge/urteile/ ohne `ecli:` genau diese eine Zeile ins
Frontmatter eingefuegt (Vorschau mit --dry-run). Marker entfernt das Skript nie.

Beispiele:
  python scripts/verify-citations.py
  python scripts/verify-citations.py --json --only-pending
  python scripts/verify-citations.py --offline
  python scripts/verify-citations.py --write-ecli --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable
from urllib.parse import quote, urlencode


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])

API_BASE = "https://testphase.rechtsinformationen.bund.de/v1"
USER_AGENT = "citation-check/1.0"
PAGE_SIZE = 50
MAX_PAGES = 3
MAX_RESPONSE_BYTES = 5_000_000
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
CACHE_TTL_SECONDS = 7 * 24 * 3600
MAX_RATE_PER_SECOND = 10.0
STATUSES = ("VERIFIED", "DATE_MISMATCH", "NOT_IN_DATASET", "NOT_COVERED", "ERROR", "UNCHECKED")

FetchFn = Callable[[str, float], "tuple[int, bytes]"]

# --------------------------------------------------------------- extraction

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
ECLI_RE = re.compile(r"ECLI:[A-Z]{2}:[A-Za-z0-9]+:\d{4}:[A-Za-z0-9.\-]+")


@dataclass(frozen=True)
class Citation:
    file: str
    line: int
    az: str
    court: str
    covered: bool
    date: str | None
    pending: bool
    context: str


@dataclass
class LookupResult:
    state: str  # ok | error | unchecked
    hits: list[dict] = field(default_factory=list)
    detail: str = ""
    from_cache: bool = False


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


# ---------------------------------------------------------------------- API

def build_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})


def default_fetch(url: str, timeout: float) -> tuple[int, bytes]:
    try:
        with urllib.request.urlopen(build_request(url), timeout=timeout) as resp:
            return resp.status, resp.read(MAX_RESPONSE_BYTES)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(MAX_RESPONSE_BYTES)


def _norm_file_number(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _error_detail(status: int, body: bytes) -> str:
    try:
        errors = json.loads(body.decode("utf-8", errors="replace")).get("errors") or []
        parts = [f"{e.get('parameter') or '-'}: {e.get('message') or e.get('code')}" for e in errors]
        if parts:
            return f"HTTP {status}: " + "; ".join(parts)
    except (ValueError, AttributeError):
        pass
    return f"HTTP {status}"


def _to_hit(item: dict) -> dict:
    return {
        "ecli": item.get("ecli"),
        "date": item.get("decisionDate"),
        "type": item.get("documentType"),
        "document_number": item.get("documentNumber"),
        "court": item.get("courtName"),
        "file_numbers": item.get("fileNumbers") or [],
        "headline": item.get("headline"),
    }


class ApiClient:
    """Polite client: rate limit, exponential backoff, circuit breaker, JSON cache."""

    def __init__(self, fetch: FetchFn | None = None, cache_dir: Path | None = None,
                 rate: float = 2.0, timeout: float = 15.0, max_retries: int = 4,
                 max_backoff: float = 30.0, breaker_threshold: int = 5,
                 cache_ttl_seconds: float = CACHE_TTL_SECONDS, offline: bool = False,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.fetch = fetch or default_fetch
        self.cache_dir = cache_dir
        self.min_interval = 1.0 / rate
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_backoff = max_backoff
        self.breaker_threshold = breaker_threshold
        self.cache_ttl_seconds = cache_ttl_seconds
        self.offline = offline
        self.sleep = sleep
        self.clock = clock
        self.warnings: list[str] = []
        self.requests_made = 0
        self._last_request: float | None = None
        self._consecutive_failures = 0

    def now_epoch(self) -> float:
        return time.time()

    # -- cache
    def _cache_path(self, court: str, az: str) -> Path | None:
        if self.cache_dir is None:
            return None
        digest = hashlib.sha256(f"{court}|{az}".encode("utf-8")).hexdigest()
        return self.cache_dir / f"{digest}.json"

    def _cache_read(self, court: str, az: str) -> list[dict] | None:
        path = self._cache_path(court, az)
        if path is None or not path.is_file():
            return None
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
            age = self.now_epoch() - float(entry["fetched_at"])
            if not self.offline and age > self.cache_ttl_seconds:
                return None
            return list(entry["hits"])
        except (OSError, ValueError, KeyError, TypeError):
            return None  # corrupt entry counts as miss and is overwritten

    def _cache_write(self, court: str, az: str, hits: list[dict]) -> None:
        path = self._cache_path(court, az)
        if path is None:
            return
        entry = {"court": court, "az": az, "fetched_at": self.now_epoch(), "hits": hits}
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(entry, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, path)
        except OSError as exc:
            self.warnings.append(f"Cache nicht schreibbar ({path.parent}): {exc}")

    # -- network
    def _throttle(self) -> None:
        if self._last_request is not None:
            wait = self._last_request + self.min_interval - self.clock()
            if wait > 0:
                self.sleep(wait)
        self._last_request = self.clock()

    def _request(self, url: str) -> tuple[int | None, bytes, str]:
        """GET with backoff. Returns (status or None, body, error detail)."""
        detail = ""
        for attempt in range(self.max_retries + 1):
            self._throttle()
            self.requests_made += 1
            try:
                status, body = self.fetch(url, self.timeout)
            except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
                status, body, detail = None, b"", f"Netzwerkfehler: {exc}"
            else:
                if status not in RETRY_STATUSES:
                    return status, body, ""
                detail = f"HTTP {status}"
            if attempt < self.max_retries:
                self.sleep(min(self.max_backoff, 1.0 * (2 ** attempt)))
        return None, b"", detail

    def _page_url(self, court: str, az: str, page: int) -> str:
        query = urlencode({"fileNumber": az, "court": court, "size": PAGE_SIZE, "pageIndex": page},
                          quote_via=quote)
        return f"{API_BASE}/rechtsprechung?{query}"

    def _query(self, court: str, az: str) -> LookupResult:
        wanted = _norm_file_number(az)
        hits: list[dict] = []
        for page in range(MAX_PAGES):
            status, body, detail = self._request(self._page_url(court, az, page))
            if status is None:
                self._consecutive_failures += 1
                return LookupResult("error", [], detail)
            if status == 404:
                break
            if status != 200:
                return LookupResult("error", [], _error_detail(status, body))
            try:
                data = json.loads(body.decode("utf-8"))
                members = data.get("member") or []
                total = int(data.get("totalItems") or 0)
            except (ValueError, AttributeError, TypeError):
                self._consecutive_failures += 1
                return LookupResult("error", [], "Antwort ist kein gueltiges JSON")
            for member in members:
                item = member.get("item") or {}
                if wanted in {_norm_file_number(n) for n in item.get("fileNumbers") or []}:
                    hits.append(_to_hit(item))
            if hits or (page + 1) * PAGE_SIZE >= total:
                break
        self._consecutive_failures = 0
        return LookupResult("ok", hits)

    def lookup(self, court: str, az: str) -> LookupResult:
        cached = self._cache_read(court, az)
        if cached is not None:
            return LookupResult("ok", cached, from_cache=True)
        if self.offline:
            return LookupResult("unchecked", [], "offline, kein Cache-Eintrag")
        if self._consecutive_failures >= self.breaker_threshold:
            return LookupResult("error", [], "API wiederholt nicht erreichbar, uebersprungen")
        result = self._query(court, az)
        if result.state == "ok":
            self._cache_write(court, az, result.hits)
        return result


# ----------------------------------------------------------- classification

def classify(citation: Citation, lookup: LookupResult | None) -> str:
    if not citation.covered:
        return "NOT_COVERED"
    if lookup is None or lookup.state == "unchecked":
        return "UNCHECKED"
    if lookup.state == "error":
        return "ERROR"
    if not lookup.hits:
        return "NOT_IN_DATASET"
    if citation.date is None or any(h.get("date") == citation.date for h in lookup.hits):
        return "VERIFIED"
    return "DATE_MISMATCH"


def _bgh_note(citation: Citation) -> str | None:
    match = re.search(r"/(\d{2})$", citation.az)
    if citation.court != "BGH" or not match:
        return None
    year = int(match.group(1))
    if year < 10 or year >= 30:  # two-digit year before 2010 (00-09) or 19xx (30-99)
        return "BGH-Bestand der API beginnt etwa 2010"
    return None


def build_results(citations: list[Citation], client: ApiClient) -> list[dict]:
    lookups: dict[tuple[str, str], LookupResult] = {}
    results: list[dict] = []
    for citation in citations:
        lookup = None
        if citation.covered:
            key = (citation.court, citation.az)
            if key not in lookups:
                lookups[key] = client.lookup(*key)
            lookup = lookups[key]
        status = classify(citation, lookup)
        entry = asdict(citation)
        entry.update(status=status, hits=lookup.hits if lookup else [],
                     detail=lookup.detail if lookup and lookup.state != "ok" else "")
        note = _bgh_note(citation) if status == "NOT_IN_DATASET" else None
        if note:
            entry["note"] = note
        results.append(entry)
    return results


def summarize(results: list[dict], client: ApiClient, offline: bool) -> dict:
    counts = {s: 0 for s in STATUSES}
    for r in results:
        counts[r["status"]] += 1
    return {
        "counts": counts,
        "citations": len(results),
        "unique_az": len({(r["court"], r["az"]) for r in results}),
        "pending_markers": sum(1 for r in results if r["pending"]),
        "api_requests": client.requests_made,
        "offline": offline,
        "api_base": API_BASE,
    }


# --------------------------------------------------------------- write-ecli

def _split_lines(text: str) -> list[str]:
    return [p for p in re.split(r"(?<=\n)", text) if p]


def _frontmatter_bounds(lines: list[str]) -> tuple[int, int] | None:
    if not lines or lines[0].strip("﻿\r\n ") != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip("\r\n ") == "---":
            return 0, idx
    return None


def _main_reference(lines: list[str], body_start: int) -> tuple[Citation | None, str | None]:
    """Main Aktenzeichen (and date) of a judgment file: Eckdaten row, else H1."""
    az_line = next((ln for ln in lines[body_start:] if "**Aktenzeichen" in ln), None)
    if az_line is None:
        az_line = next((ln for ln in lines[body_start:] if ln.startswith("# ")), None)
    if az_line is None:
        return None, None
    found = extract_citations(az_line, "")
    date_line = next((ln for ln in lines[body_start:]
                      if re.search(r"\*\*(?:Datum|Entscheidungstermin|Entscheidungsdatum)", ln)), None)
    dates = find_dates(date_line) if date_line else []
    return (found[0] if found else None), (dates[0][2] if dates else None)


def _unique_ecli(hits: list[dict], date: str | None) -> tuple[str | None, str]:
    candidates = [h for h in hits if date is None or h.get("date") == date]
    eclis = {h["ecli"] for h in candidates
             if isinstance(h.get("ecli"), str) and ECLI_RE.fullmatch(h["ecli"])}
    if len(eclis) == 1:
        return eclis.pop(), ""
    if not eclis:
        return None, "kein gueltiger ECLI im Treffer"
    return None, "mehrere Treffer, ohne eindeutiges Datum nicht entscheidbar"


def _atomic_write(path: Path, data: bytes) -> None:
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=".tmp-ecli-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.chmod(tmp_name, path.stat().st_mode & 0o777)
        except OSError:
            pass
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def plan_ecli_updates(kb_path: Path, client: ApiClient) -> tuple[list[dict], list[dict]]:
    """Return (updates, skipped). Updates carry the new file bytes, never written here."""
    updates: list[dict] = []
    skipped: list[dict] = []
    folder = kb_path / "urteile"
    for md in sorted(folder.glob("*.md")) if folder.is_dir() else []:
        rel = _rel(md, kb_path)

        def skip(reason: str) -> None:
            skipped.append({"file": rel, "reason": reason})

        try:
            text = md.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            skip(f"nicht lesbar: {exc}")
            continue
        lines = _split_lines(text)
        bounds = _frontmatter_bounds(lines)
        if bounds is None:
            skip("kein Frontmatter")
            continue
        if any(re.match(r"ecli\s*:", ln) for ln in lines[1:bounds[1]]):
            skip("ecli bereits vorhanden")
            continue
        citation, date = _main_reference(lines, bounds[1] + 1)
        if citation is None:
            skip("kein Haupt-Aktenzeichen erkannt")
            continue
        if not citation.covered:
            skip(f"{citation.court} nicht im Bestand der API")
            continue
        lookup = client.lookup(citation.court, citation.az)
        main = Citation(rel, 0, citation.az, citation.court, True, date, False, "")
        status = classify(main, lookup)
        if status != "VERIFIED":
            skip(f"{citation.az}: {status}")
            continue
        ecli, reason = _unique_ecli(lookup.hits, date)
        if ecli is None:
            skip(f"{citation.az}: {reason}")
            continue
        closing = lines[bounds[1]]
        eol = "\r\n" if closing.endswith("\r\n") else "\n"
        new_lines = lines[:bounds[1]] + [f"ecli: {ecli}{eol}"] + lines[bounds[1]:]
        updates.append({"file": rel, "path": md, "az": citation.az, "ecli": ecli,
                        "data": "".join(new_lines).encode("utf-8")})
    return updates, skipped


# ------------------------------------------------------------------- output

def _format_hit(hit: dict) -> str:
    return f"{hit.get('ecli') or '-'}  {hit.get('date') or '-'}  {hit.get('type') or '-'}"


def render_report(results: list[dict], summary: dict, warnings: list[str]) -> str:
    out = [f"=== Zitatpruefung gegen Rechtsinformations-API des Bundes (Testphase) ===",
           f"{summary['citations']} Zitate, {summary['unique_az']} eindeutige Aktenzeichen, "
           f"{summary['api_requests']} API-Anfragen"
           + (" (offline)" if summary["offline"] else ""), ""]
    out.append("Zusammenfassung: " + ", ".join(f"{k}={v}" for k, v in summary["counts"].items() if v or k in STATUSES[:5]))
    out.append("")
    labels = {
        "DATE_MISMATCH": "DATE_MISMATCH: Treffer, aber KB nennt anderes Datum",
        "VERIFIED": "VERIFIED: Treffer in der API (Primaerbeleg, Marker bleibt redaktionelle Entscheidung)",
        "NOT_IN_DATASET": "NOT_IN_DATASET: abgedecktes Gericht, kein Treffer (kein Gegenbeweis!)",
        "ERROR": "ERROR: API nicht erreichbar oder Fehlerantwort",
        "UNCHECKED": "UNCHECKED: offline, kein Cache-Eintrag",
        "NOT_COVERED": "NOT_COVERED: Gericht nicht im Bestand der API (nicht abgefragt)",
    }
    for status in ("DATE_MISMATCH", "VERIFIED", "NOT_IN_DATASET", "ERROR", "UNCHECKED", "NOT_COVERED"):
        group = [r for r in results if r["status"] == status]
        if not group:
            continue
        out.append(f"--- {labels[status]} ({len(group)}) ---")
        for r in group:
            marker = "Marker: ja" if r["pending"] else "Marker: nein"
            date = f"KB-Datum {r['date']}" if r["date"] else "KB-Datum -"
            out.append(f"{r['file']}:{r['line']}  {r['az']}  [{r['court']}]  {date}  {marker}")
            for hit in r["hits"]:
                out.append(f"    -> {_format_hit(hit)}")
            if r["detail"]:
                out.append(f"    ! {r['detail']}")
            if r.get("note"):
                out.append(f"    i {r['note']}")
        out.append("")
    if summary["counts"]["ERROR"]:
        out.append("Hinweis: API nicht erreichbar oder Fehler. Ergebnis fuer diese Zitate nicht aussagekraeftig; "
                   "weiter mit der Tier-1-Kaskade (rechtsprechung-im-internet.de).")
    out.append("Hinweis: NOT_IN_DATASET und NOT_COVERED sind kein Gegenbeweis. Die API deckt nur sieben "
               "Bundesgerichte ab (BGH ab etwa 2010) und ist eine Testphase ohne Stabilitaetszusage.")
    out.extend(f"Warnung: {w}" for w in warnings)
    return "\n".join(out)


def render_ecli(updates: list[dict], skipped: list[dict], dry_run: bool) -> str:
    head = "ECLI-Eintraege (Vorschau, es wird nichts geschrieben)" if dry_run else "ECLI-Eintraege (geschrieben)"
    out = ["", f"=== {head}: {len(updates)} ==="]
    out.extend(f"{u['file']}  {u['az']}  ecli: {u['ecli']}" for u in updates)
    out.append(f"Uebersprungen: {len(skipped)}")
    out.extend(f"  {s['file']}: {s['reason']}" for s in skipped)
    return "\n".join(out)


# --------------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Bundesgerichts-Aktenzeichen in knowledge/ gegen die "
                                            "Rechtsinformations-API des Bundes pruefen (optional).")
    p.add_argument("--path", default=str(ROOT / "knowledge"), help="KB-Verzeichnis (Standard: knowledge/)")
    p.add_argument("--json", action="store_true", help="JSON statt lesbarem Bericht")
    p.add_argument("--offline", action="store_true", help="nur Extraktion und Cache, keine Anfragen")
    p.add_argument("--only-pending", action="store_true",
                   help="nur Zitate mit <<VERIFIKATION AUSSTEHEND>> in derselben Zeile")
    p.add_argument("--rate", type=float, default=2.0, help="max. Anfragen pro Sekunde (Standard 2)")
    p.add_argument("--cache-dir", default=None,
                   help="Cache-Verzeichnis (Standard: System-Temp/citation-check-cache, nie im Repo)")
    p.add_argument("--timeout", type=float, default=15.0, help="Timeout je Anfrage in Sekunden")
    p.add_argument("--strict", action="store_true", help="Exit 1 bei DATE_MISMATCH")
    p.add_argument("--write-ecli", action="store_true",
                   help="ecli: in knowledge/urteile/*.md eintragen (nur eindeutig VERIFIED)")
    p.add_argument("--dry-run", action="store_true", help="mit --write-ecli: nur Vorschau")
    return p


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def main(argv: list[str] | None = None, fetch: FetchFn | None = None,
         sleep: Callable[[float], None] = time.sleep, stdout=None, stderr=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.dry_run and not args.write_ecli:
        parser.error("--dry-run ist nur zusammen mit --write-ecli sinnvoll")
    if not 0 < args.rate <= MAX_RATE_PER_SECOND:
        parser.error(f"--rate muss > 0 und <= {MAX_RATE_PER_SECOND:g} sein")
    if args.timeout <= 0:
        parser.error("--timeout muss > 0 sein")

    out = stdout or sys.stdout
    err = stderr or sys.stderr
    if stdout is None and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if stderr is None and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    cache_dir = Path(args.cache_dir) if args.cache_dir else Path(tempfile.gettempdir()) / "citation-check-cache"
    if _inside(cache_dir, ROOT):
        print(f"Fehler: --cache-dir darf nicht im Repo liegen ({cache_dir}).", file=err)
        return 2
    kb_path = Path(args.path)
    if not kb_path.is_dir():
        print(f"Fehler: KB-Verzeichnis nicht gefunden: {kb_path}", file=err)
        return 2

    client = ApiClient(fetch=fetch, cache_dir=cache_dir, rate=args.rate, timeout=args.timeout,
                       offline=args.offline, sleep=sleep)
    citations = scan_kb(kb_path)
    if args.only_pending:
        citations = [c for c in citations if c.pending]
    results = build_results(citations, client)
    summary = summarize(results, client, args.offline)

    updates: list[dict] = []
    skipped: list[dict] = []
    if args.write_ecli:
        updates, skipped = plan_ecli_updates(kb_path, client)
        if not args.dry_run:
            for update in updates:
                _atomic_write(update["path"], update["data"])
        summary["api_requests"] = client.requests_made

    if args.json:
        payload: dict = {"summary": summary, "citations": results, "warnings": client.warnings}
        if args.write_ecli:
            payload["ecli_updates"] = [{"file": u["file"], "az": u["az"], "ecli": u["ecli"],
                                        "written": not args.dry_run} for u in updates]
            payload["ecli_skipped"] = skipped
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=out)
    else:
        print(render_report(results, summary, client.warnings), file=out)
        if args.write_ecli:
            print(render_ecli(updates, skipped, args.dry_run), file=out)

    if args.strict and summary["counts"]["DATE_MISMATCH"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
