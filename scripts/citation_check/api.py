"""HTTP access to the Rechtsinformations-API: rate limit, backoff, pagination."""
from __future__ import annotations

import http.client
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable
from urllib.parse import quote, urlencode

from .cache import HitCache
from .hits import sanitize_hit
from .models import API_BASE, DEFAULT_CACHE_TTL_DAYS, LookupResult

USER_AGENT = "citation-check/1.0"
PAGE_SIZE = 50
MAX_PAGES = 3
MAX_RESPONSE_BYTES = 5_000_000
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
CACHE_TTL_SECONDS = DEFAULT_CACHE_TTL_DAYS * 24 * 3600

FetchFn = Callable[[str, float], "tuple[int, bytes]"]


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
    return sanitize_hit({
        "ecli": item.get("ecli"),
        "date": item.get("decisionDate"),
        "type": item.get("documentType"),
        "document_number": item.get("documentNumber"),
        "court": item.get("courtName"),
        "file_numbers": item.get("fileNumbers") or [],
        "headline": item.get("headline"),
    })


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
