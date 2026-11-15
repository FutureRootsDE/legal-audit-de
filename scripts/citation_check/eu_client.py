"""Cellar backend: one SPARQL request per EU file number, cached per user."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from .cache import HitCache
from .eu_az import parse_eu_az
from .eu_sparql import EuShapeError, build_url, parse_response, sanitize_eu_hit, sanitize_tokens
from .http_core import FetchFn, PoliteClient, default_fetch
from .models import DEFAULT_CACHE_TTL_DAYS, LookupResult
from .text import short

EU_RATE = 1.0  # at most one SPARQL request per second
EU_TIMEOUT = 60.0  # a cold query can take more than ten seconds
EU_MAX_RETRIES = 2
MAX_EU_RESPONSE_BYTES = 2_000_000


def eu_fetch(url: str, timeout: float) -> tuple:
    return default_fetch(url, timeout, accept="application/sparql-results+json", limit=MAX_EU_RESPONSE_BYTES,
                         socket_limit=EU_TIMEOUT)


def _error_detail(status: int) -> str:
    return f"HTTP {status}"


class EuClient(PoliteClient):
    """Looks up EU file numbers; hits carry only validated, pattern-checked fields."""

    retry_timeouts = False  # up to 60 s per query: a timeout is not repeated

    def __init__(self, fetch: FetchFn | None = None, cache_dir: Path | None = None,
                 rate: float = EU_RATE, timeout: float = EU_TIMEOUT, offline: bool = False,
                 cache_ttl_seconds: float = DEFAULT_CACHE_TTL_DAYS * 24 * 3600,
                 breaker_threshold: int = 5,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> None:
        super().__init__(fetch or eu_fetch, rate, timeout, EU_MAX_RETRIES, 30.0, sleep, clock)
        self.offline = offline
        self.breaker_threshold = breaker_threshold
        self.warnings: list[str] = []
        self.cache = HitCache(cache_dir, cache_ttl_seconds, offline, self.warnings,
                              sanitize=sanitize_eu_hit, token_sanitizer=sanitize_tokens)
        self._consecutive_failures = 0

    def _query(self, az: str, court: str) -> LookupResult:
        case = parse_eu_az(az, court)
        if case is None:
            return LookupResult("error", [], "Aktenzeichen nicht auswertbar", backend="cellar")
        status, body, detail = self._request(build_url(case))
        if status is None:
            self._consecutive_failures += 1
            return LookupResult("error", [], detail, backend="cellar")
        if status != 200:
            self._consecutive_failures += 1
            return LookupResult("error", [], _error_detail(status), backend="cellar")
        try:
            hits, tokens = parse_response(body)
        except EuShapeError as exc:
            self._consecutive_failures += 1
            return LookupResult("error", [], short(str(exc)), backend="cellar")
        self._consecutive_failures = 0
        return LookupResult("ok", hits, backend="cellar", tokens=tuple(tokens))

    def lookup(self, court: str, az: str, fresh: bool = False) -> LookupResult:
        """Look up one EU file number. fresh=True bypasses the cache (read and write)."""
        if fresh and self.offline:
            return LookupResult("unchecked", [], "offline, frische Abfrage nicht moeglich", backend="cellar")
        cached = None if fresh else self.cache.read_entry(court, az)
        if cached is not None:
            return LookupResult("ok", cached[0], from_cache=True, backend="cellar", tokens=tuple(cached[1]))
        if self.offline:
            return LookupResult("unchecked", [], "offline, kein Cache-Eintrag", backend="cellar")
        if self._consecutive_failures >= self.breaker_threshold:
            return LookupResult("error", [], "Cellar wiederholt nicht erreichbar, uebersprungen", backend="cellar")
        result = self._query(az, court)
        if result.state == "ok" and not fresh:
            self.cache.write(court, az, result.hits, list(result.tokens))
        return result
