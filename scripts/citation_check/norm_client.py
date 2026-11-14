"""gesetze-im-internet.de backend: one table of contents and one XML archive per cited law, cached per user."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .cache import DocCache
from .http_core import FetchFn, PoliteClient, default_fetch
from .models import DEFAULT_CACHE_TTL_DAYS
from .norm_laws import GII_BASE, SLUG_RE, TOC_URL, parse_toc
from .norm_xml import MAX_ZIP_BYTES, XmlRejected, parse_law_zip, validate_index

NORM_RATE = 1.0
NORM_TIMEOUT = 60.0
TOC_CACHE_NAME = "gii-toc"


def norm_fetch(url: str, timeout: float) -> tuple:
    return default_fetch(url, timeout, accept="*/*", limit=MAX_ZIP_BYTES)


@dataclass
class LawData:
    """Index of one law (validated) or the reason it is not available."""
    state: str  # ok | error
    index: dict | None = None
    detail: str = ""
    from_cache: bool = False


@dataclass
class TocData:
    slugs: set[str] = field(default_factory=set)
    state: str = "ok"
    detail: str = ""
    from_cache: bool = False


class NormClient(PoliteClient):
    """Loads the table of contents and the law archives; every law is requested at most once per run."""

    def __init__(self, fetch: FetchFn | None = None, cache_dir: Path | None = None, rate: float = NORM_RATE,
                 timeout: float = NORM_TIMEOUT, offline: bool = False,
                 cache_ttl_seconds: float = DEFAULT_CACHE_TTL_DAYS * 24 * 3600,
                 sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> None:
        super().__init__(fetch or norm_fetch, rate, timeout, 2, 30.0, sleep, clock)
        self.offline = offline
        self.warnings: list[str] = []
        self.cache = DocCache(cache_dir, cache_ttl_seconds, offline, self.warnings)
        self._toc: TocData | None = None
        self._laws: dict[str, LawData] = {}

    def toc(self) -> TocData:
        if self._toc is None:
            self._toc = self._load_toc()
        return self._toc

    def _load_toc(self) -> TocData:
        cached = self.cache.read(TOC_CACHE_NAME)
        if isinstance(cached, list) and all(isinstance(s, str) and SLUG_RE.match(s) for s in cached) and cached:
            return TocData(set(cached), from_cache=True)
        if self.offline:
            return TocData(state="error", detail="offline, kein Cache-Eintrag")
        status, body, detail = self._request(TOC_URL)
        if status != 200:
            return TocData(state="error", detail=detail or f"HTTP {status}")
        try:
            slugs = parse_toc(body)
        except ValueError:
            return TocData(state="error", detail="Inhaltsverzeichnis unerwartet")
        self.cache.write(TOC_CACHE_NAME, sorted(slugs))
        return TocData(slugs)

    def law(self, slug: str) -> LawData:
        if slug not in self._laws:
            self._laws[slug] = self._load_law(slug)
        return self._laws[slug]

    def _load_law(self, slug: str) -> LawData:
        cached = validate_index(self.cache.read(f"law:{slug}"))
        if cached is not None:
            return LawData("ok", cached, from_cache=True)
        if self.offline:
            return LawData("error", detail="offline, kein Cache-Eintrag")
        status, body, detail = self._request(f"{GII_BASE}/{slug}/xml.zip")
        if status != 200:
            return LawData("error", detail=detail or f"HTTP {status}")
        try:
            index = validate_index(parse_law_zip(body))
        except XmlRejected as exc:
            return LawData("error", detail=f"XML abgelehnt: {exc}")
        if index is None:
            return LawData("error", detail="Index ungueltig")
        self.cache.write(f"law:{slug}", index)
        return LawData("ok", index)
