"""Shared constants and data types of the citation check."""
from __future__ import annotations

from dataclasses import dataclass, field

API_BASE = "https://testphase.rechtsinformationen.bund.de/v1"
DEFAULT_CACHE_TTL_DAYS = 7
STATUSES = ("VERIFIED", "DATE_MISMATCH", "NOT_IN_DATASET", "NOT_COVERED", "ERROR", "UNCHECKED")


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
