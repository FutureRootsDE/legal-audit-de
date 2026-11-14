"""HTTP access to the Rechtsinformations-API: rate limit, backoff, pagination, bounded reads."""
from __future__ import annotations

import http.client
import json
import re
import socket
import ssl
import time
import urllib.error
import urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Callable, NamedTuple
from urllib.parse import quote, urlencode, urlparse

from .cache import HitCache
from .hits import sanitize_hit
from .models import API_BASE, DEFAULT_CACHE_TTL_DAYS, LookupResult
from .text import short

USER_AGENT = "citation-check/1.0"
PAGE_SIZE = 50
MAX_PAGES = 3
MAX_RESPONSE_BYTES = 5_000_000
READ_CHUNK = 8_192
SOCKET_TIMEOUT = 5.0  # upper bound for one socket operation; the total time is enforced per block
ERROR_CODE_RE = re.compile(r"^[A-Za-z0-9_.-]{1,40}$")
MAX_ERROR_CODES = 3
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
CACHE_TTL_SECONDS = DEFAULT_CACHE_TTL_DAYS * 24 * 3600

FetchFn = Callable[[str, float], tuple]  # (status, body) or (status, body, headers)


class NonRetryableError(OSError):
    """Network-level failure that a retry cannot fix (redirect to elsewhere, size or time limit)."""


class ResponseTooLarge(NonRetryableError):
    pass


class RedirectBlocked(NonRetryableError):
    pass


class DeadlineExceeded(NonRetryableError, TimeoutError):
    pass


class ResponseShapeError(ValueError):
    """The API answered with JSON of an unexpected structure."""


class SameHostHttpsRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects only to https on the same host and port; everything else is an error."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urlparse(req.full_url), urlparse(newurl)
        same_origin = (new.scheme == "https" and new.hostname == old.hostname
                       and (new.port or 443) == (old.port or 443))
        if not same_origin:
            raise RedirectBlocked(f"Weiterleitung auf {new.scheme}://{new.hostname} nicht erlaubt")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def build_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})


def read_bounded(resp, deadline: float, clock: Callable[[], float] = time.monotonic,
                 limit: int = MAX_RESPONSE_BYTES) -> bytes:
    """Read a response body in chunks: at most `limit` bytes and until `deadline` (clock value)."""
    parts: list[bytes] = []
    total = 0
    read = getattr(resp, "read1", None) or resp.read  # read1 returns after one socket read: no long block
    while True:
        if clock() > deadline:
            raise DeadlineExceeded("Gesamtzeit je Anfrage ueberschritten")
        chunk = read(min(READ_CHUNK, limit + 1 - total))
        if not chunk:
            return b"".join(parts)
        total += len(chunk)
        if total > limit:
            raise ResponseTooLarge(f"Antwort groesser als {limit} Bytes")
        parts.append(chunk)


def _retry_headers(headers) -> dict[str, str]:
    value = headers.get("Retry-After") if headers is not None else None
    return {"retry-after": str(value)} if value is not None else {}


def socket_timeout(timeout: float) -> float:
    """Timeout of a single socket operation: small, so a stalled read overshoots the deadline only slightly."""
    return min(timeout, SOCKET_TIMEOUT)


def default_fetch(url: str, timeout: float) -> tuple[int, bytes, dict[str, str]]:
    """GET over https with a total time limit; returns (status, body, retry headers)."""
    if urlparse(url).scheme != "https":
        raise NonRetryableError("nur https erlaubt")
    deadline = time.monotonic() + timeout
    opener = urllib.request.build_opener(SameHostHttpsRedirect)
    try:
        with opener.open(build_request(url), timeout=socket_timeout(timeout)) as resp:
            return resp.status, read_bounded(resp, deadline), _retry_headers(resp.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, read_bounded(exc, deadline), _retry_headers(exc.headers)


def parse_retry_after(value: str | None, now: float) -> float | None:
    """Seconds to wait from a Retry-After header (delta seconds or HTTP date); None if unusable."""
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return float(value)
    try:
        seconds = parsedate_to_datetime(value).timestamp() - now
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    return seconds if seconds >= 0 else None


def error_category(exc: BaseException) -> str:
    """Fixed category of a network error; never any text taken from the exception message."""
    reason = exc.reason if isinstance(exc, urllib.error.URLError) and isinstance(exc.reason, BaseException) else exc
    if isinstance(reason, RedirectBlocked):
        return "unzulaessige Weiterleitung"
    if isinstance(reason, ResponseTooLarge):
        return "Antwort zu gross"
    if isinstance(reason, (TimeoutError, socket.timeout)):
        return "Zeitueberschreitung"
    if isinstance(reason, ConnectionRefusedError):
        return "Verbindung abgelehnt"
    if isinstance(reason, ssl.SSLError):
        return "TLS-Fehler"
    if isinstance(reason, http.client.HTTPException):
        return "ungueltige Antwort"
    return type(reason).__name__


def _norm_file_number(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _error_detail(status: int, body: bytes) -> str:
    """Fixed format `HTTP <status>` plus at most MAX_ERROR_CODES API error codes of a strict pattern.

    No free text of the response is ever passed on (agents read this output).
    """
    try:
        errors = json.loads(body.decode("utf-8", errors="replace")).get("errors") or []
        codes = [e["code"] for e in errors if isinstance(e, dict) and isinstance(e.get("code"), str)
                 and ERROR_CODE_RE.fullmatch(e["code"])]
    except (ValueError, AttributeError, TypeError):
        codes = []
    return f"HTTP {status} ({', '.join(codes[:MAX_ERROR_CODES])})" if codes else f"HTTP {status}"


def parse_page(body: bytes) -> tuple[list[dict], int]:
    """Validate one result page: returns (items, totalItems) or raises ResponseShapeError."""
    try:
        data = json.loads(body.decode("utf-8"))
    except ValueError:
        raise ResponseShapeError("Antwort ist kein gueltiges JSON") from None
    if not isinstance(data, dict):
        raise ResponseShapeError("Antwort ist kein JSON-Objekt")
    members = data.get("member") or []
    if not isinstance(members, list):
        raise ResponseShapeError("member ist kein Array")
    try:
        total = int(data.get("totalItems") or 0)
    except (ValueError, TypeError):
        raise ResponseShapeError("totalItems ist keine Zahl") from None
    return [_item_of(member) for member in members], total


def _item_of(member: object) -> dict:
    if not isinstance(member, dict):
        raise ResponseShapeError("member-Eintrag ist kein Objekt")
    item = member.get("item") or {}
    if not isinstance(item, dict):
        raise ResponseShapeError("item ist kein Objekt")
    numbers = item.get("fileNumbers") or []
    if not isinstance(numbers, list) or not all(isinstance(n, str) for n in numbers):
        raise ResponseShapeError("fileNumbers ist keine Liste von Texten")
    return item


def _to_hit(item: dict) -> dict:
    return sanitize_hit({
        "ecli": item.get("ecli"),
        "date": item.get("decisionDate"),
        "type": item.get("documentType"),
        "document_number": item.get("documentNumber"),
        "court": item.get("courtName"),
        "file_numbers": item.get("fileNumbers") or [],
    })


class Attempt(NamedTuple):
    status: int | None
    body: bytes
    headers: dict
    detail: str
    fatal: bool


class ApiClient:
    """Polite client: rate limit, exponential backoff, circuit breaker, JSON cache."""

    def __init__(self, fetch: FetchFn | None = None, cache_dir: Path | None = None,
                 rate: float = 2.0, timeout: float = 15.0, max_retries: int = 4,
                 max_backoff: float = 30.0, breaker_threshold: int = 5,
                 cache_ttl_seconds: float = CACHE_TTL_SECONDS, offline: bool = False,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.fetch = fetch or default_fetch
        self.min_interval = 1.0 / rate
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_backoff = max_backoff
        self.breaker_threshold = breaker_threshold
        self.offline = offline
        self.sleep = sleep
        self.clock = clock
        self.warnings: list[str] = []
        self.cache = HitCache(cache_dir, cache_ttl_seconds, offline, self.warnings)
        self.requests_made = 0
        self._last_request: float | None = None
        self._consecutive_failures = 0

    def _throttle(self) -> None:
        if self._last_request is not None:
            wait = self._last_request + self.min_interval - self.clock()
            if wait > 0:
                self.sleep(wait)
        self._last_request = self.clock()

    def _attempt(self, url: str) -> Attempt:
        try:
            result = self.fetch(url, self.timeout)
        except NonRetryableError as exc:
            return Attempt(None, b"", {}, f"Netzwerkfehler: {error_category(exc)}", True)
        except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
            return Attempt(None, b"", {}, f"Netzwerkfehler: {error_category(exc)}", False)
        status, body, *rest = result
        headers = {str(k).lower(): v for k, v in (rest[0] if rest else {}).items()}
        return Attempt(status, body, headers, f"HTTP {status}" if status in RETRY_STATUSES else "", False)

    def _backoff(self, attempt: int, headers: dict) -> float:
        wait = parse_retry_after(headers.get("retry-after"), time.time())
        return min(self.max_backoff, 1.0 * (2 ** attempt) if wait is None else wait)

    def _request(self, url: str) -> tuple[int | None, bytes, str]:
        """GET with backoff. Returns (status or None, body, error detail)."""
        detail = ""
        for attempt in range(self.max_retries + 1):
            self._throttle()
            self.requests_made += 1
            outcome = self._attempt(url)
            detail = outcome.detail
            if outcome.fatal:
                return None, b"", detail
            if outcome.status is not None and outcome.status not in RETRY_STATUSES:
                return outcome.status, outcome.body, ""
            if attempt < self.max_retries:
                self.sleep(self._backoff(attempt, outcome.headers))
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
                items, total = parse_page(body)
            except ResponseShapeError as exc:
                self._consecutive_failures += 1
                return LookupResult("error", [], short(str(exc)))
            hits.extend(_to_hit(i) for i in items if wanted in {_norm_file_number(n) for n in i.get("fileNumbers") or []})
            if hits or (page + 1) * PAGE_SIZE >= total:
                break
        self._consecutive_failures = 0
        return LookupResult("ok", hits)

    def lookup(self, court: str, az: str, fresh: bool = False) -> LookupResult:
        """Look up one Aktenzeichen. fresh=True bypasses the cache (read and write)."""
        if fresh and self.offline:
            return LookupResult("unchecked", [], "offline, frische Abfrage nicht moeglich")
        cached = None if fresh else self.cache.read(court, az)
        if cached is not None:
            return LookupResult("ok", cached, from_cache=True)
        if self.offline:
            return LookupResult("unchecked", [], "offline, kein Cache-Eintrag")
        if self._consecutive_failures >= self.breaker_threshold:
            return LookupResult("error", [], "API wiederholt nicht erreichbar, uebersprungen")
        result = self._query(court, az)
        if result.state == "ok" and not fresh:
            self.cache.write(court, az, result.hits)
        return result
