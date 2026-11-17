"""Render invariants on the *derived* model (spec 6.3, 6.9.2 step 4, 6.10).

Checked after the downgrades, so a defect that became a notice is judged by the notice rules.
Paths point to the input row (`results[3].client_action`) where one exists; rows the script set
itself (not applicable, missing) are reported under `results` with the test ID in the message.
"""
from __future__ import annotations

from typing import Any, Mapping

from .derive import STATUS_MISSING
from .models import DerivedResult, ReportModel, ValidationIssue
from .schema import DEFECT_NOT_ALLOWED, SEVERITY_BY_STATUS, STATUSES

OPEN_STATUSES = ("notice", "defect")
TOP_ACTIONS_MAX = 3
REASON_KINDS = ("not_checkable", "not_applicable")
# Required authored fields of the result row per derived status: (dotted path, kind).
OPEN_REQUIRED = (
    ("one_liner", "text"), ("client_text", "text"), ("client_action", "text"), ("risk", "text"),
    ("evidence", "list"), ("fix.steps", "list"), ("fix.effort", "object"), ("retest.how", "text"),
    ("checklist", "list"),
)
REQUIRED_BY_STATUS = {"pass": (("one_liner", "text"),), "notice": OPEN_REQUIRED, "defect": OPEN_REQUIRED, "none": ()}


def _get(data: Mapping[str, Any], dotted: str) -> Any:
    node: Any = data
    for part in dotted.split("."):
        if not isinstance(node, Mapping):
            return None
        node = node.get(part)
    return node


def _present(value: Any, kind: str) -> bool:
    if kind == "text":
        return isinstance(value, str) and bool(value.strip())
    if kind == "list":
        return isinstance(value, list) and len(value) > 0
    return isinstance(value, Mapping) and bool(value)


def _input_index(findings: Mapping[str, Any]) -> dict[str, int]:
    results = findings.get("results")
    index: dict[str, int] = {}
    for i, row in enumerate(results if isinstance(results, list) else ()):
        if isinstance(row, Mapping) and isinstance(row.get("id"), str):
            index.setdefault(row["id"], i)
    return index


def _required_issues(r: DerivedResult, prefix: str) -> list[ValidationIssue]:
    test_id = r.entry.id
    fields = REQUIRED_BY_STATUS.get(r.status, ())
    if r.status == "notice" and r.entry.basis == "legal_judgment":
        fields = fields + (("review_question", "text"),)
    issues = [ValidationIssue(f"{prefix}.{name}", f"{test_id}: Pflichtfeld bei Status {r.status} fehlt")
              for name, kind in fields if not _present(_get(r.data, name), kind)]
    if r.status == "none":
        if r.reason_kind not in REASON_KINDS:
            issues.append(ValidationIssue(f"{prefix}.reason_kind", f"{test_id}: Pflichtfeld bei Status none fehlt"))
        if not _present(r.reason, "text"):
            issues.append(ValidationIssue(f"{prefix}.reason", f"{test_id}: Pflichtfeld bei Status none fehlt"))
    return issues


def _status_issues(r: DerivedResult, prefix: str, bfsg: Any) -> list[ValidationIssue]:
    test_id = r.entry.id
    issues: list[ValidationIssue] = []
    allowed = SEVERITY_BY_STATUS.get(r.status)
    if (allowed and r.severity not in allowed) or (not allowed and r.severity is not None):
        issues.append(ValidationIssue(f"{prefix}.severity", f"{test_id}: Severity {r.severity} passt nicht zu Status {r.status}"))
    if r.severity_original is not None and r.status != "notice":
        issues.append(ValidationIssue(f"{prefix}.severity_original", f"{test_id}: nur bei herabgestuftem Befund"))
    if r.status == "defect" and (r.entry.basis == "legal_judgment" or r.entry.max_status == "notice"):
        issues.append(ValidationIssue(f"{prefix}.status", f"{test_id}: {DEFECT_NOT_ALLOWED}"))
    if r.entry.always_run and r.status == "defect" and bfsg is not True:
        issues.append(ValidationIssue(f"{prefix}.status", f"{test_id}: Barrierefreiheit ohne BFSG-Pflicht nie Auffällig"))
    if r.entry.always_run and r.reason_kind == "not_applicable":
        issues.append(ValidationIssue(f"{prefix}.reason_kind", f"{test_id}: Barrierefreiheit ist immer anwendbar"))
    return issues


def _result_issues(model: ReportModel) -> list[ValidationIssue]:
    index = _input_index(model.findings)
    app = model.findings.get("applicability")
    bfsg = _get(app, "bfsg.value") if isinstance(app, Mapping) else None
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for r in model.results:
        test_id = r.entry.id
        if test_id in seen:
            issues.append(ValidationIssue("results", f"{test_id} mehrfach"))
            continue
        seen.add(test_id)
        prefix = f"results[{index[test_id]}]" if test_id in index else "results"
        if r.status == STATUS_MISSING:
            issues.append(ValidationIssue("results", f"{test_id} fehlt"))
        elif r.status not in STATUSES:
            issues.append(ValidationIssue(f"{prefix}.status", f"{test_id}: unbekannter Status"))
        else:
            issues += _status_issues(r, prefix, bfsg) + _required_issues(r, prefix)
    return issues


def _count_issues(model: ReportModel) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if set(model.counts) != set(STATUSES):
        issues.append(ValidationIssue("counts", f"Zählung braucht genau die Status {', '.join(STATUSES)}"))
    for status in STATUSES:
        actual = sum(1 for r in model.results if r.status == status)
        if model.counts.get(status) != actual:
            issues.append(ValidationIssue("counts", f"Zählung {status}: {model.counts.get(status)} statt {actual}"))
    return issues


def _top_action_issues(model: ReportModel) -> list[ValidationIssue]:
    top = _get(model.findings, "summary.top_actions")
    if not isinstance(top, list):
        return [ValidationIssue("summary.top_actions", "muss eine Liste von Test-IDs sein")]
    open_rows = model.open_results()
    open_ids = {r.entry.id for r in open_rows}
    issues: list[ValidationIssue] = []
    for i, item in enumerate(top):
        if item in top[:i]:
            issues.append(ValidationIssue(f"summary.top_actions[{i}]", f"doppelte ID {item}"))
        elif item not in open_ids:
            issues.append(ValidationIssue(f"summary.top_actions[{i}]", f"{item} ist kein offener Befund (Hinweis oder Auffällig)"))
    expected = min(TOP_ACTIONS_MAX, len(open_rows))
    if len(top) != expected:
        issues.append(ValidationIssue("summary.top_actions", f"genau {expected} IDs nötig (offene Befunde: {len(open_rows)})"))
    return issues


def check_invariants(model: ReportModel) -> list[ValidationIssue]:
    """Every invariant violation of the derived model; an empty list means step 4 passed."""
    return _result_issues(model) + _count_issues(model) + _top_action_issues(model)
