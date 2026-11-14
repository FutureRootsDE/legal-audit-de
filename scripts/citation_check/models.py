"""Shared constants and data types of the citation check."""
from __future__ import annotations

from dataclasses import dataclass, field

API_BASE = "https://testphase.rechtsinformationen.bund.de/v1"
EU_BASE = "https://publications.europa.eu/webapi/rdf/sparql"
DEFAULT_CACHE_TTL_DAYS = 7
STATUSES = ("VERIFIED", "DATE_MISMATCH", "NOT_IN_DATASET", "NOT_COVERED", "ERROR", "UNCHECKED", "PENDING")


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
    correction: bool = False
    names: tuple = ()  # quoted or bracketed short names near an EU file number (informative name hint)


@dataclass
class LookupResult:
    state: str  # ok | error | unchecked
    hits: list[dict] = field(default_factory=list)
    detail: str = ""
    from_cache: bool = False
    backend: str = "ris"  # ris (Rechtsinformations-API) | cellar (EU)
    tokens: tuple = ()  # cellar only: lowercase title words for the informative name hint
