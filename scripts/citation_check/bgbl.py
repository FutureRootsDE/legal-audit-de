"""Existence check of BGBl. references on recht.bund.de, only as far as robots.txt allows and slowly.

robots.txt of recht.bund.de asks for a crawl delay of 30 seconds and leaves /bgbl/ open. The check
reads robots.txt on every run, honours Disallow and Crawl-delay, and never exceeds the number of
requests the caller allows (--max-bgbl).
"""
from __future__ import annotations

import re
import time
import urllib.robotparser
from dataclasses import dataclass
from typing import Callable

from .http_core import FetchFn, PoliteClient, default_fetch
from .norm_extract import BgblRef

BGBL_HOST = "https://www.recht.bund.de"
ROBOTS_URL = f"{BGBL_HOST}/robots.txt"
ROBOTS_AGENT = "citation-check"
DEFAULT_DELAY = 30.0
MAX_DELAY = 120.0
DEFAULT_MAX_BGBL = 20
TITLE_RE = re.compile(rb"<title>(.*?)</title>", re.DOTALL)
OK_TITLE = re.compile(rb"^\s*Bundesgesetzblatt Teil I")
PART_PATH = {"I": "1"}  # the URL pattern was verified for Part I only
MIN_YEAR = 2023


def bgbl_fetch(url: str, timeout: float) -> tuple:
    return default_fetch(url, timeout, accept="text/html,*/*", limit=1_000_000)


def page_url(ref: BgblRef) -> str:
    return f"{BGBL_HOST}/bgbl/{PART_PATH[ref.part]}/{ref.year}/{ref.number}/VO.html"


@dataclass(frozen=True)
class RobotsRules:
    allowed: bool
    delay: float
    detail: str = ""


class BgblChecker(PoliteClient):
    """Checks unique references one by one with the crawl delay of robots.txt in between."""

    def __init__(self, fetch: FetchFn | None = None, timeout: float = 30.0, max_checks: int = DEFAULT_MAX_BGBL,
                 offline: bool = False, sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic,
                 progress: Callable[[str], None] | None = None) -> None:
        super().__init__(fetch or bgbl_fetch, 1.0 / DEFAULT_DELAY, timeout, 1, 30.0, sleep, clock)
        self.max_checks = max_checks
        self.offline = offline
        self.progress = progress or (lambda message: None)
        self.checked = 0

    def robots(self) -> RobotsRules:
        status, body, detail = self._request(ROBOTS_URL)
        if status != 200:
            return RobotsRules(False, DEFAULT_DELAY, "robots.txt nicht lesbar: " + (detail or f"HTTP {status}"))
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(body.decode("utf-8", errors="replace").splitlines())
        sample = f"{BGBL_HOST}/bgbl/1/2026/1/VO.html"
        if not parser.can_fetch(ROBOTS_AGENT, sample):
            return RobotsRules(False, DEFAULT_DELAY, "robots.txt untersagt den Abruf")
        delay = parser.crawl_delay(ROBOTS_AGENT)
        wait = DEFAULT_DELAY if delay is None else min(float(delay), MAX_DELAY)
        return RobotsRules(True, wait)

    def check_all(self, refs: list[BgblRef]) -> tuple[list[dict], dict]:
        """One result per unique reference; returns (results, summary info)."""
        unique: dict[tuple[str, int, int], list[BgblRef]] = {}
        for ref in refs:
            unique.setdefault((ref.part, ref.year, ref.number), []).append(ref)
        if self.offline or self.max_checks <= 0 or not unique:
            reason = "offline" if self.offline else "--max-bgbl 0" if self.max_checks <= 0 else ""
            return self._all_unchecked(unique, reason), {"robots": None}
        rules = self.robots()
        if not rules.allowed:
            return self._all_unchecked(unique, rules.detail), {"robots": rules.detail}
        self.min_interval = rules.delay
        return self._check_unique(unique, rules), {"robots": "erlaubt", "crawl_delay": rules.delay}

    def _all_unchecked(self, unique: dict, reason: str) -> list[dict]:
        return [self._row(key, places, "BGBL_UNCHECKED", reason or "nicht geprueft")
                for key, places in unique.items()]

    def _check_unique(self, unique: dict, rules: RobotsRules) -> list[dict]:
        results: list[dict] = []
        keys = sorted(unique)
        budget = min(self.max_checks, len(keys))
        for key, places in ((k, unique[k]) for k in keys):
            part, year, number = key
            if part not in PART_PATH or year < MIN_YEAR:
                results.append(self._row(key, places, "BGBL_UNCHECKED", "Teil oder Jahr nicht pruefbar"))
            elif self.checked >= budget:
                results.append(self._row(key, places, "BGBL_UNCHECKED", "Begrenzung --max-bgbl erreicht"))
            else:
                self.checked += 1
                self.progress(f"BGBl. {year} {part} Nr. {number} ({self.checked}/{budget}, "
                              f"{rules.delay:.0f} s Abstand laut robots.txt)")
                results.append(self._check_one(key, places))
        return results

    def _check_one(self, key: tuple[str, int, int], places: list[BgblRef]) -> dict:
        part, year, number = key
        status, body, detail = self._request(page_url(places[0]))
        if status == 404:
            return self._row(key, places, "BGBL_MISSING", "Seite nicht vorhanden (HTTP 404)")
        if status != 200:
            return self._row(key, places, "ERROR", detail or f"HTTP {status}")
        title = TITLE_RE.search(body)
        if title and OK_TITLE.match(title.group(1)):
            return self._row(key, places, "BGBL_OK", "")
        return self._row(key, places, "ERROR", "unerwartete Seite")

    @staticmethod
    def _row(key: tuple[str, int, int], places: list[BgblRef], status: str, detail: str) -> dict:
        part, year, number = key
        return {"ref": f"BGBl. {year} {part} Nr. {number}", "status": status, "detail": detail,
                "places": [f"{p.file}:{p.line}" for p in places]}
