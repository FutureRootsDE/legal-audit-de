"""Applicability and downgrades on validated findings.json (spec 6.3, 6.9.1, 6.9.2 steps 2 and 3).

Runs after input validation (schema.validate_input) and before the render invariants
(invariants.check_invariants). Everything here is deterministic: the model never decides
applicability, downgrades, `severity_original` or the notes; the script does.

Rules per catalog entry, in this order:
1. Applicability `evaluate(applies_if, intake)`. False: status `none` with `not_applicable`
   and the catalog reason; a result the model wrote for that ID is dropped with a warning.
   A11Y entries have no condition and are never `not_applicable`.
2. No result for an applicable entry: status STATUS_MISSING, reported by the invariants.
3. `valid_from`: no legal basis applies yet on the check date -> note with the earliest date.
4. Applicability unknown (`None`) -> note "Anwendbarkeit ungeklärt".
5. A11Y follows the BFSG answer: False -> note "keine gesetzliche Pflicht", None -> as rule 4,
   True -> normal rules.
Rules 3 to 5 only touch open results (notice, defect). Any of them turns a `defect` into a
`notice` with severity at most MED and keeps the input severity in `severity_original`.
"""
from __future__ import annotations

import copy
from datetime import date, datetime, time, timedelta
from types import MappingProxyType
from typing import Any, Mapping

from .catalog import evaluate
from .models import Catalog, CatalogEntry, DerivedResult, ReportInputError, ReportModel, ValidationIssue
from .schema import STATUSES, UTC_FORMAT, UTC_RE
from .texts import NOTE_A11Y_VOLUNTARY, NOTE_APPLICABILITY_UNCLEAR, NOTE_VALID_FROM

STATUS_MISSING = "missing"
OPEN_STATUSES = ("notice", "defect")
DOWNGRADE_CAP = {"CRIT": "MED", "HIGH": "MED"}
NOTE_DATE_FORMAT = "%d.%m.%Y"
WARNING_DROPPED = "{id}: Ergebnis verworfen, Test nicht anwendbar"
EMPTY: Mapping[str, Any] = MappingProxyType({})
CET = timedelta(hours=1)
CEST = timedelta(hours=2)
DST_SWITCH_UTC = time(1, 0)
SUNDAY = 6


def _last_sunday(year: int, month: int) -> date:
    """Last Sunday of a month with 31 days (March, October)."""
    last = date(year, month, 31)
    return last - timedelta(days=(last.weekday() - SUNDAY) % 7)


def _berlin_offset(utc: datetime) -> timedelta:
    """UTC offset of Europe/Berlin at a naive UTC moment: CEST (UTC+2) or CET (UTC+1).

    EU rule since 1996: summer time from the last Sunday of March, 01:00 UTC, to the last
    Sunday of October, 01:00 UTC.
    """
    start = datetime.combine(_last_sunday(utc.year, 3), DST_SWITCH_UTC)
    end = datetime.combine(_last_sunday(utc.year, 10), DST_SWITCH_UTC)
    return CEST if start <= utc < end else CET


def check_date(findings: Mapping[str, Any]) -> date:
    """Check date of the run: the calendar day of `run.started_utc` in Europe/Berlin.

    Decision (orchestrator, 2026-11-17): the report is for German clients, so the check date
    (note "Pflicht gilt ab", valid_from comparison, PDF file name) is the German local day,
    not the UTC day; a run started at 00:30 local time belongs to that day. Standard library
    only and without zoneinfo, because Windows ships no tzdata: the CET/CEST rule is computed
    in _berlin_offset (valid for the current EU rule, i.e. every date from 1996 on).
    """
    run = findings.get("run")
    value = run.get("started_utc") if isinstance(run, Mapping) else None
    try:
        if not (isinstance(value, str) and UTC_RE.fullmatch(value)):
            raise ValueError("not a UTC timestamp")
        utc = datetime.strptime(value, UTC_FORMAT)
        return (utc + _berlin_offset(utc)).date()
    except (TypeError, ValueError) as exc:
        raise ReportInputError([ValidationIssue("run.started_utc", "Format JJJJ-MM-TTThh:mm:ssZ (UTC)")]) from exc


def _intake(findings: Mapping[str, Any]) -> dict[str, bool | None]:
    """Three-valued intake answers; anything but true/false counts as unknown."""
    app = findings.get("applicability")
    values: dict[str, bool | None] = {}
    for key, item in (app.items() if isinstance(app, Mapping) else ()):
        value = item.get("value") if isinstance(item, Mapping) else None
        values[key] = value if isinstance(value, bool) else None
    return values


def _rows_by_id(findings: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """First result row per test ID (validation has already rejected duplicates)."""
    rows: dict[str, Mapping[str, Any]] = {}
    results = findings.get("results")
    for row in results if isinstance(results, list) else ():
        if isinstance(row, Mapping) and isinstance(row.get("id"), str):
            rows.setdefault(row["id"], row)
    return rows


def _frozen(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(copy.deepcopy(dict(row)))


def _open_notes(entry: CatalogEntry, applicable: bool | None, bfsg: bool | None, day: date) -> tuple[str, ...]:
    """Notes of rules 3 to 5 for an open result; any note means a defect is downgraded."""
    voluntary = entry.always_run and bfsg is False
    notes: list[str] = []
    earliest = min(basis.valid_from for basis in entry.legal_basis)
    if not voluntary and day < earliest:
        notes.append(NOTE_VALID_FROM.format(date=earliest.strftime(NOTE_DATE_FORMAT)))
    unclear = bfsg is None if entry.always_run else applicable is None
    if unclear:
        notes.append(NOTE_APPLICABILITY_UNCLEAR)
    if voluntary:
        notes.append(NOTE_A11Y_VOLUNTARY)
    return tuple(notes)


def _not_applicable(entry: CatalogEntry) -> DerivedResult:
    return DerivedResult(entry=entry, status="none", severity=None, severity_original=None,
                         reason_kind="not_applicable", reason=entry.not_applicable_reason, notes=(), data=EMPTY)


def _from_row(entry: CatalogEntry, row: Mapping[str, Any], applicable: bool | None,
              bfsg: bool | None, day: date) -> DerivedResult:
    status = row.get("status")
    severity = row.get("severity")
    severity_original = None
    notes: tuple[str, ...] = ()
    if status in OPEN_STATUSES:
        notes = _open_notes(entry, applicable, bfsg, day)
        if notes and status == "defect":
            status, severity_original = "notice", severity
            severity = DOWNGRADE_CAP.get(severity, severity)
    is_none = status == "none"
    return DerivedResult(
        entry=entry, status=status, severity=severity, severity_original=severity_original,
        reason_kind=row.get("reason_kind") if is_none else None,
        reason=row.get("reason") if is_none else None,
        notes=notes, data=_frozen(row),
    )


def derive(findings: Mapping[str, Any], catalog: Catalog) -> tuple[ReportModel, list[str]]:
    """Derived model with one result per catalog entry (catalog order) plus warnings."""
    day = check_date(findings)
    intake = _intake(findings)
    rows = _rows_by_id(findings)
    warnings: list[str] = []
    results: list[DerivedResult] = []
    for entry in catalog.entries:
        applicable = evaluate(entry.applies_if, intake)
        row = rows.get(entry.id)
        if applicable is False:
            if row is not None:
                warnings.append(WARNING_DROPPED.format(id=entry.id))
            results.append(_not_applicable(entry))
        elif row is None:
            results.append(DerivedResult(entry=entry, status=STATUS_MISSING, severity=None, severity_original=None,
                                         reason_kind=None, reason=None, notes=(), data=EMPTY))
        else:
            results.append(_from_row(entry, row, applicable, intake.get("bfsg"), day))
    counts = {status: sum(1 for r in results if r.status == status) for status in STATUSES}
    model = ReportModel(findings=MappingProxyType(copy.deepcopy(dict(findings))), check_date=day,
                        results=tuple(results), counts=MappingProxyType(counts))
    return model, warnings
