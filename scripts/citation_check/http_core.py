"""Shared HTTP layer of all backends: bounded reads, same-host redirects, rate limit, backoff.

Every backend (Rechtsinformations-API, Cellar, gesetze-im-internet.de, recht.bund.de) talks
through the same hardened code path: https only, redirects only to https on the same host,
size and time limits, fixed error categories without any text taken from the remote side.
"""
from __future__ import annotations

import http.client
import socket
import ssl
import time
import urllib.error
import urllib.request
from email.utils import parsedate_to_datetime
from typing import Callable, NamedTuple
from urllib.parse import urlparse

USER_AGENT = "citation-check/1.0"
MAX_RESPONSE_BYTES = 5_000_000
READ_CHUNK = 8_192
SOCKET_TIMEOUT = 5.0  # upper bound for one socket operation; the total time is enforced per block
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})

FetchFn = Callable[[str, float], tuple]  # (status, body) or (status, body, headers)


class NonRetryableError(OSError):
    """Network-level failure that a retry cannot fix (redirect to elsewhere, size or time limit)."""


class ResponseTooLarge(NonRetryableError):
    pass


class RedirectBlocked(NonRetryableError):
    pass


class DeadlineExceeded(NonRetryableError, TimeoutError):
    pass


class SameHostHttpsRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects only to https on the same host and port; everything else is an error."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urlparse(req.full_url), urlparse(newurl)
        same_origin = (new.scheme == "https" and new.hostname == old.hostname
                       and (new.port or 443) == (old.port or 443))
        if not same_origin:
            raise RedirectBlocked(f"Weiterleitung auf {new.scheme}://{new.hostname} nicht erlaubt")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def build_request(url: str, accept: str = "application/json") -> urllib.request.Request:
    return urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})


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


def socket_timeout(timeout: float, limit: float = SOCKET_TIMEOUT) -> float:
    """Timeout of a single socket operation: small, so a stalled read overshoots the deadline only slightly.

    `limit` is raised only for endpoints that stay silent while they compute (SPARQL).
    """
    return min(timeout, limit)


def default_fetch(url: str, timeout: float, accept: str = "application/json",
                  limit: int = MAX_RESPONSE_BYTES, socket_limit: float = SOCKET_TIMEOUT) -> tuple[int, bytes, dict[str, str]]:
    """GET over https with a total time limit; returns (status, body, retry headers)."""
    if urlparse(url).scheme != "https":
        raise NonRetryableError("nur https erlaubt")
    deadline = time.monotonic() + timeout
    opener = urllib.request.build_opener(SameHostHttpsRedirect)
    try:
        with opener.open(build_request(url, accept), timeout=socket_timeout(timeout, socket_limit)) as resp:
            return resp.status, read_bounded(resp, deadline, limit=limit), _retry_headers(resp.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, read_bounded(exc, deadline, limit=limit), _retry_headers(exc.headers)


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


class Attempt(NamedTuple):
    status: int | None
    body: bytes
    headers: dict
    detail: str
    fatal: bool


class PoliteClient:
    """Rate limit, exponential backoff with cap, Retry-After; shared by all backends."""

    retry_timeouts = True  # a backend with long single requests (SPARQL) sets False: a timeout is final

    def __init__(self, fetch: FetchFn | None = None, rate: float = 2.0, timeout: float = 15.0,
                 max_retries: int = 4, max_backoff: float = 30.0,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.fetch = fetch or default_fetch
        self.min_interval = 1.0 / rate
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_backoff = max_backoff
        self.sleep = sleep
        self.clock = clock
        self.requests_made = 0
        self._last_request: float | None = None

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
            category = error_category(exc)
            fatal = not self.retry_timeouts and category == "Zeitueberschreitung"
            return Attempt(None, b"", {}, f"Netzwerkfehler: {category}", fatal)
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
