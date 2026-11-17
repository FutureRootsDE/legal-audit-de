"""Shared value types and error classes of the client_report package."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import cached_property
from types import MappingProxyType
from typing import Iterable, Mapping, NamedTuple


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
