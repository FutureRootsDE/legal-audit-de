"""Shared value types and error classes of the client_report package."""
from __future__ import annotations

from typing import Iterable, NamedTuple


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
