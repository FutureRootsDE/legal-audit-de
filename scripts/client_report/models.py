"""Shared value types and error classes of the client_report package."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import cached_property
from types import MappingProxyType
from typing import Any, Iterable, Mapping, NamedTuple

# Sort order of open results; same values as schema.SEVERITIES (not imported: schema imports models).
_SEVERITY_RANK = {"CRIT": 0, "HIGH": 1, "MED": 2, "LOW": 3}
_OPEN_STATUSES = ("notice", "defect")


class ValidationIssue(NamedTuple):
    """One blocking problem, located by a field path such as `results[3].client_text`."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


class ReportInputError(Exception):
    """Raised when findings.json (or derived data) violates a rule; carries every issue found."""

    def __init__(self, issues: Iterable[ValidationIssue]) -> None:
        self.issues: list[ValidationIssue] = list(issues)
        super().__init__("\n".join(str(issue) for issue in self.issues))


@dataclass(frozen=True)
class LegalBasis:
    """One provision a catalog test touches; `valid_from` is the day the duty starts to apply."""

    norm: str
    valid_from: date
    kb_ref: str


@dataclass(frozen=True)
class AreaInfo:
    """A test area (ID prefix) with its report heading and one introductory sentence."""

    prefix: str
    title: str
    intro: str


@dataclass(frozen=True)
class CatalogEntry:
    """One fixed test of the catalog; run data comes from findings.json, never from here."""

    id: str
    area: str
    title: str
    description: str
    legal_basis: tuple[LegalBasis, ...]
    applies_if: tuple[str, ...]
    always_run: bool
    basis: str
    max_status: str | None
    not_applicable_reason: str
    retest_default: str


@dataclass(frozen=True)
class Catalog:
    """The versioned test catalog in report order (areas, then entries)."""

    version: str
    areas: tuple[AreaInfo, ...]
    entries: tuple[CatalogEntry, ...]
    glossary: tuple[tuple[str, str], ...]

    @cached_property
    def by_id(self) -> Mapping[str, CatalogEntry]:
        """Read-only lookup of entries by test ID."""
        return MappingProxyType({entry.id: entry for entry in self.entries})


@dataclass(frozen=True)
class DerivedResult:
    """Result of one catalog test after applicability and downgrades (spec 6.9.2 steps 2 and 3).

    `status` and `severity` are the derived values; `severity_original` holds the input severity
    when the script downgraded a defect, else None. `notes` are fixed texts from texts.NOTE_*.
    `data` is the model's raw result row (read-only; empty when the script set the row itself).
    """

    entry: CatalogEntry
    status: str
    severity: str | None
    severity_original: str | None
    reason_kind: str | None
    reason: str | None
    notes: tuple[str, ...]
    data: Mapping[str, Any]


@dataclass(frozen=True)
class ReportModel:
    """Derived report data: one result per catalog entry in catalog order, counts per status."""

    findings: Mapping[str, Any]
    check_date: date
    results: tuple[DerivedResult, ...]
    counts: Mapping[str, int]

    def open_results(self) -> tuple[DerivedResult, ...]:
        """Results with status notice or defect, by severity (CRIT first), then catalog order."""
        open_rows = [r for r in self.results if r.status in _OPEN_STATUSES]
        # sorted() is stable, so equal severities keep catalog order.
        return tuple(sorted(open_rows, key=lambda r: _SEVERITY_RANK.get(r.severity or "", len(_SEVERITY_RANK))))
