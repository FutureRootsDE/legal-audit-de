"""HTTP access to the Rechtsinformations-API: pagination and hit validation on top of http_core."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Callable
from urllib.parse import quote, urlencode

from .cache import HitCache
from .hits import sanitize_hit
from .http_core import (  # noqa: F401  (re-exported: tests and callers use api.<name>)
    MAX_RESPONSE_BYTES, READ_CHUNK, RETRY_STATUSES, SOCKET_TIMEOUT, USER_AGENT, DeadlineExceeded, FetchFn,
    NonRetryableError, PoliteClient, RedirectBlocked, ResponseTooLarge, SameHostHttpsRedirect, build_request,
    default_fetch, error_category, parse_retry_after, read_bounded, socket_timeout)
from .models import API_BASE, DEFAULT_CACHE_TTL_DAYS, LookupResult
from .text import short

PAGE_SIZE = 50
MAX_PAGES = 3
ERROR_CODE_RE = re.compile(r"^[A-Za-z0-9_.-]{1,40}$")
MAX_ERROR_CODES = 3
CACHE_TTL_SECONDS = DEFAULT_CACHE_TTL_DAYS * 24 * 3600


class ResponseShapeError(ValueError):
    """The API answered with JSON of an unexpected structure."""


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


class ApiClient(PoliteClient):
    """Polite client: rate limit, exponential backoff, circuit breaker, JSON cache."""

    def __init__(self, fetch: FetchFn | None = None, cache_dir: Path | None = None,
                 rate: float = 2.0, timeout: float = 15.0, max_retries: int = 4,
                 max_backoff: float = 30.0, breaker_threshold: int = 5,
                 cache_ttl_seconds: float = CACHE_TTL_SECONDS, offline: bool = False,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> None:
        super().__init__(fetch, rate, timeout, max_retries, max_backoff, sleep, clock)
        self.breaker_threshold = breaker_threshold
        self.offline = offline
        self.warnings: list[str] = []
        self.cache = HitCache(cache_dir, cache_ttl_seconds, offline, self.warnings)
        self._consecutive_failures = 0

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
