"""Render pipeline, spec 6.9.2 steps 1 to 5: validate, derive, check invariants, render, write.

Each step raises ReportInputError with every issue of that step; report.html is written only
when all steps passed, and atomically (temporary file, then replace), so a failed run never
leaves a half-written or stale-looking report behind.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .catalog import load_catalog
from .derive import derive
from .embed import SIZE_BUDGET_BYTES
from .invariants import check_invariants
from .models import Catalog, ReportInputError
from .render import render_html
from .schema import FINDINGS_PATH, load_findings, validate_input

REPORT_FILENAME = "report.html"
WARNING_SIZE = "Hinweis: report.html ist größer als 10 MB."


@dataclass(frozen=True)
class RenderResult:
    html_path: Path
    warnings: list[str] = field(default_factory=list)


def _atomic_write_text(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(prefix=".report-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def build_report(report_dir: Path, catalog: Catalog | None = None) -> RenderResult:
    """Run steps 1 to 5 for `report_dir/findings.json` and write `report_dir/report.html`."""
    report_dir = Path(report_dir)
    catalog = catalog if catalog is not None else load_catalog()
    findings = load_findings(report_dir / FINDINGS_PATH)
    issues = validate_input(findings, catalog, report_dir)                 # step 1
    if issues:
        raise ReportInputError(issues)
    model, warnings = derive(findings, catalog)                           # steps 2 and 3
    issues = check_invariants(model)                                      # step 4
    if issues:
        raise ReportInputError(issues)
    document = render_html(model, catalog, report_dir)                    # step 5
    if len(document.encode("utf-8")) > SIZE_BUDGET_BYTES:
        warnings.append(WARNING_SIZE)
    html_path = report_dir / REPORT_FILENAME
    _atomic_write_text(html_path, document)
    return RenderResult(html_path=html_path, warnings=warnings)
