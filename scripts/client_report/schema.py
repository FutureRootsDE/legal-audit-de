"""Input validation of findings.json (spec 6.3, 6.9.1, 6.9.2 step 1, 6.10).

This is step 1 of the render pipeline: it checks the raw input exactly as the model wrote it.
Required fields per *derived* status are checked later on the derived model (invariants).
Every problem is collected as a ValidationIssue with its field path; nothing stops at the first.

Field classes: the paths in PROSE_PATHS are authored text and go through the text rules
(forbidden phrases, dashes). Every other string is `verbatim` (website content, URLs,
commands, snippets) and is never text-checked; the renderer escapes all of it.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterator, Sequence
from urllib.parse import urlsplit

from .catalog import APPLICABILITY_KEYS
from .models import Catalog, CatalogEntry, ReportInputError, ValidationIssue
from .paths import domain_from_url, safe_evidence_path
from .textcheck import check_texts, load_forbidden_phrases

SCHEMA_VERSION = "1.0"
STATUSES = ("pass", "notice", "defect", "none")
SEVERITIES = ("CRIT", "HIGH", "MED", "LOW")
SEVERITY_BY_STATUS = {"defect": ("CRIT", "HIGH", "MED"), "notice": ("MED", "LOW")}
INPUT_REASON_KINDS = ("not_checkable",)
EVIDENCE_KINDS = ("screenshot", "network", "header", "dom")
SCREENSHOT_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")
LOGO_SUFFIXES = (".png", ".jpg", ".jpeg", ".svg")
EFFORT_LEVELS = ("gering", "mittel", "hoch")
MAX_PAGES = 25
MAX_FINDINGS_BYTES = 20 * 1024 * 1024
UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ACCENT_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
# Characters that never belong in a reference link (attribute break-out, whitespace, controls).
UNSAFE_LINK_RE = re.compile(r"[\s\x00-\x1f\x7f\"'<>`\\]")
DEFECT_NOT_ALLOWED = "defect nicht zulässig: Befund als Tatsache oder Prüffrage fassen"
FINDINGS_PATH = "findings.json"

PROSE_PATHS: tuple[str, ...] = (
    "summary.sentences[]",
    "results[].one_liner",
    "results[].client_text",
    "results[].client_action",
    "results[].review_question",
    "results[].risk",
    "results[].reason",
    "results[].fix.steps[]",
    "results[].checklist[]",
    "results[].evidence[].caption",
    "results[].evidence[].alt",
    "results[].retest.how",
)

TOP_REQUIRED = ("schema_version", "catalog_version", "run", "issuer", "client", "applicability", "summary", "results")
TOP_OPTIONAL = ("plugin_version",)
RUN_KEYS = ("started_utc", "finished_utc", "target_url", "final_url", "domain", "user_agent", "viewports", "tools",
            "pages_visited")
ISSUER_REQUIRED = ("company", "address", "logo_file")
ISSUER_OPTIONAL = ("contact", "phone", "email", "website", "accent_color")
RESULT_TEXT_KEYS = ("one_liner", "client_text", "client_action", "review_question", "risk", "reason")
RESULT_OPTIONAL = ("severity", "severity_original", "reason_kind", "reason", "one_liner", "client_text",
                   "client_action", "review_question", "evidence", "risk", "fix", "retest", "references", "checklist")


# ---------------------------------------------------------------- generic helpers

def _join(path: str, key: str) -> str:
    return f"{path}.{key}" if path else key


def _shape(obj: Any, path: str, required: Sequence[str], optional: Sequence[str]) -> tuple[list[ValidationIssue], bool]:
    """Object check: missing required and unknown keys are issues; second value: is it an object."""
    if not isinstance(obj, dict):
        return [ValidationIssue(path or "findings", "muss ein Objekt sein")], False
    allowed = set(required) | set(optional)
    issues = [ValidationIssue(_join(path, k), "Pflichtfeld fehlt") for k in required if k not in obj]
    issues += [ValidationIssue(_join(path, str(k)), "unbekanntes Feld") for k in obj if k not in allowed]
    return issues, True


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text(obj: dict, key: str, path: str) -> list[ValidationIssue]:
    """Non-empty string, checked only when the key is present (missing keys are reported by _shape)."""
    if key in obj and not _non_empty(obj[key]):
        return [ValidationIssue(_join(path, key), "muss ein nicht leerer Text sein")]
    return []


def _optional_text(obj: dict, key: str, path: str) -> list[ValidationIssue]:
    if key in obj and obj[key] is not None and not isinstance(obj[key], str):
        return [ValidationIssue(_join(path, key), "muss ein Text oder null sein")]
    return []


def _text_list(value: Any, path: str, min_items: int = 0) -> list[ValidationIssue]:
    if not isinstance(value, list) or len(value) < min_items:
        need = f" mit mindestens {min_items} Eintrag" if min_items else ""
        return [ValidationIssue(path, f"muss eine Liste von Texten sein{need}")]
    return [ValidationIssue(f"{path}[{i}]", "muss ein nicht leerer Text sein")
            for i, item in enumerate(value) if not _non_empty(item)]


def _parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not UTC_RE.match(value):
        return None
    try:
        return datetime.strptime(value, UTC_FORMAT)
    except ValueError:
        return None


def _url_issue(value: Any, path: str) -> tuple[list[ValidationIssue], str | None]:
    """Issue for a non-http(s) URL; second value: its normalised domain when valid."""
    try:
        return [], domain_from_url(value)
    except ValueError as exc:
        return [ValidationIssue(path, f"keine gültige http- oder https-URL ({exc})")], None


def _is_https_link(value: Any) -> bool:
    if not isinstance(value, str) or UNSAFE_LINK_RE.search(value):
        return False
    parts = urlsplit(value)
    return parts.scheme == "https" and bool(parts.hostname)


def _file_issues(rel: Any, path: str, report_dir: Path, suffixes: Sequence[str] | None) -> list[ValidationIssue]:
    if not isinstance(rel, str):
        return [ValidationIssue(path, "muss ein Pfad als Text sein")]
    if suffixes and PurePosixPath(rel).suffix.lower() not in suffixes:
        return [ValidationIssue(path, f"Dateiendung erlaubt: {', '.join(suffixes)}")]
    try:
        safe_evidence_path(report_dir, rel)
    except ValueError as exc:
        return [ValidationIssue(path, str(exc))]
    return []


# ---------------------------------------------------------------- prose fields and loading

def _tokens(pattern: str) -> list[str]:
    tokens: list[str] = []
    for part in pattern.split("."):
        if part.endswith("[]"):
            tokens += [part[:-2], "[]"]
        else:
            tokens.append(part)
    return tokens


def _walk(node: Any, tokens: list[str], path: str) -> Iterator[tuple[str, str]]:
    if not tokens:
        if isinstance(node, str):
            yield path, node
        return
    head, rest = tokens[0], tokens[1:]
    if head == "[]":
        if isinstance(node, list):
            for i, item in enumerate(node):
                yield from _walk(item, rest, f"{path}[{i}]")
    elif isinstance(node, dict) and head in node:
        yield from _walk(node[head], rest, _join(path, head))


def iter_prose(findings: dict) -> Iterator[tuple[str, str]]:
    """(concrete field path, text) of every prose string, e.g. ("results[3].client_text", "...")."""
    for pattern in PROSE_PATHS:
        yield from _walk(findings, _tokens(pattern), "")


def _reject_constant(name: str) -> Any:
    raise ValueError(f"{name} ist kein gültiger JSON-Wert")


def load_findings(path: Path) -> dict:
    """Read findings.json (UTF-8 with or without BOM, as PowerShell writes it)."""
    path = Path(path)

    def fail(message: str) -> ReportInputError:
        return ReportInputError([ValidationIssue(FINDINGS_PATH, message)])

    try:
        if path.stat().st_size > MAX_FINDINGS_BYTES:
            raise fail(f"Datei größer als {MAX_FINDINGS_BYTES // (1024 * 1024)} MB")
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise fail("keine gültige UTF-8-Datei") from exc
    except OSError as exc:
        raise fail(f"Datei nicht lesbar: {path.name}") from exc
    try:
        data = json.loads(text, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        raise fail(f"kein gültiges JSON (Zeile {exc.lineno}, Spalte {exc.colno})") from exc
    except ValueError as exc:
        raise fail(f"kein gültiges JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise fail("muss ein JSON-Objekt sein")
    return data


# ---------------------------------------------------------------- blocks

def _validate_run_times(run: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    times = {}
    for key in ("started_utc", "finished_utc"):
        times[key] = _parse_utc(run.get(key))
        if key in run and times[key] is None:
            issues.append(ValidationIssue(f"run.{key}", "Format JJJJ-MM-TTThh:mm:ssZ (UTC)"))
    if times["started_utc"] and times["finished_utc"] and times["finished_utc"] < times["started_utc"]:
        issues.append(ValidationIssue("run.finished_utc", "liegt vor started_utc"))
    return issues


def _validate_run_urls(run: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    target_domain = None
    for key in ("target_url", "final_url"):
        if key in run:
            url_issues, domain = _url_issue(run[key], f"run.{key}")
            issues += url_issues
            target_domain = domain if key == "target_url" else target_domain
    if "domain" in run:
        if not _non_empty(run["domain"]):
            issues.append(ValidationIssue("run.domain", "muss ein nicht leerer Text sein"))
        elif target_domain is not None and run["domain"] != target_domain:
            issues.append(ValidationIssue("run.domain", f"muss {target_domain} sein (abgeleitet aus target_url)"))
    pages = run.get("pages_visited")
    if "pages_visited" in run:
        if not isinstance(pages, list):
            issues.append(ValidationIssue("run.pages_visited", "muss eine Liste von URLs sein"))
        elif len(pages) > MAX_PAGES:
            issues.append(ValidationIssue("run.pages_visited", f"höchstens {MAX_PAGES} Seiten (passive Prüfung)"))
        else:
            for i, page in enumerate(pages):
                issues += _url_issue(page, f"run.pages_visited[{i}]")[0]
    return issues


def _validate_run(run: Any) -> list[ValidationIssue]:
    issues, ok = _shape(run, "run", RUN_KEYS, ())
    if not ok:
        return issues
    issues += _validate_run_times(run) + _validate_run_urls(run) + _text(run, "user_agent", "run")
    if "viewports" in run:
        issues += _text_list(run["viewports"], "run.viewports", min_items=1)
    tools = run.get("tools")
    if "tools" in run and not (isinstance(tools, dict) and all(isinstance(v, str) for v in tools.values())):
        issues.append(ValidationIssue("run.tools", "muss ein Objekt mit Versionstexten sein"))
    return issues


def _validate_issuer(issuer: Any, report_dir: Path) -> list[ValidationIssue]:
    issues, ok = _shape(issuer, "issuer", ISSUER_REQUIRED, ISSUER_OPTIONAL)
    if not ok:
        return issues
    for key in ("company", "contact", "phone", "email", "website"):
        issues += _text(issuer, key, "issuer")
    if "address" in issuer:
        issues += _text_list(issuer["address"], "issuer.address", min_items=1)
    if "logo_file" in issuer:
        issues += _file_issues(issuer["logo_file"], "issuer.logo_file", report_dir, LOGO_SUFFIXES)
    accent = issuer.get("accent_color")
    if accent is not None and not (isinstance(accent, str) and ACCENT_RE.match(accent)):
        issues.append(ValidationIssue("issuer.accent_color", "muss eine Hexfarbe #RRGGBB oder null sein"))
    return issues


def _validate_client(client: Any) -> list[ValidationIssue]:
    issues, ok = _shape(client, "client", ("address",), ("name", "company"))
    if not ok:
        return issues
    issues += _optional_text(client, "name", "client") + _optional_text(client, "company", "client")
    if not (_non_empty(client.get("name")) or _non_empty(client.get("company"))):
        issues.append(ValidationIssue("client", "Name oder Firma des Kunden fehlt"))
    if "address" in client:
        issues += _text_list(client["address"], "client.address", min_items=1)
    return issues


def _validate_applicability(app: Any) -> list[ValidationIssue]:
    issues, ok = _shape(app, "applicability", APPLICABILITY_KEYS, ())
    if not ok:
        return issues
    for key in APPLICABILITY_KEYS:
        path = f"applicability.{key}"
        entry_issues, entry_ok = _shape(app.get(key), path, ("value", "source"), ("note",)) if key in app else ([], False)
        issues += entry_issues
        if not entry_ok:
            continue
        value = app[key].get("value")
        if "value" in app[key] and not (value is None or isinstance(value, bool)):
            issues.append(ValidationIssue(f"{path}.value", "muss true, false oder null sein"))
        issues += _text(app[key], "source", path) + _optional_text(app[key], "note", path)
    return issues


def _validate_summary(summary: Any, catalog: Catalog) -> list[ValidationIssue]:
    issues, ok = _shape(summary, "summary", ("sentences", "top_actions"), ())
    if not ok:
        return issues
    sentences = summary.get("sentences")
    if "sentences" in summary:
        if not isinstance(sentences, list) or len(sentences) != 3:
            issues.append(ValidationIssue("summary.sentences", "genau 3 Sätze nötig"))
        else:
            issues += _text_list(sentences, "summary.sentences")
    top = summary.get("top_actions")
    if "top_actions" in summary:
        if not isinstance(top, list):
            issues.append(ValidationIssue("summary.top_actions", "muss eine Liste von Test-IDs sein"))
        else:
            issues += [ValidationIssue(f"summary.top_actions[{i}]", "unbekannte Test-ID")
                       for i, item in enumerate(top) if not (isinstance(item, str) and item in catalog.by_id)]
    return issues


# ---------------------------------------------------------------- results

def _check_id(result: dict, path: str, catalog: Catalog, seen: set[str]) -> tuple[list[ValidationIssue], CatalogEntry | None]:
    test_id = result.get("id")
    if "id" not in result:
        return [], None
    if not isinstance(test_id, str) or test_id not in catalog.by_id:
        return [ValidationIssue(f"{path}.id", "unbekannte Test-ID")], None
    if test_id in seen:
        return [ValidationIssue(f"{path}.id", f"doppelte ID {test_id}")], catalog.by_id[test_id]
    seen.add(test_id)
    return [], catalog.by_id[test_id]


def _status_rules(result: dict, path: str, status: str, entry: CatalogEntry | None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    allowed = SEVERITY_BY_STATUS.get(status)
    severity = result.get("severity")
    if allowed and severity not in allowed:
        issues.append(ValidationIssue(f"{path}.severity", f"{status} verlangt {', '.join(allowed[:-1])} oder {allowed[-1]}"))
    elif not allowed and severity is not None:
        issues.append(ValidationIssue(f"{path}.severity", f"bei Status {status} keine Severity angeben"))
    if result.get("severity_original") is not None:
        issues.append(ValidationIssue(f"{path}.severity_original", "setzt nur das Skript, muss null sein"))
    kind = result.get("reason_kind")
    if kind == "not_applicable":
        issues.append(ValidationIssue(f"{path}.reason_kind", "not_applicable setzt nur das Skript aus der Anwendbarkeit"))
    elif kind is not None and kind not in INPUT_REASON_KINDS:
        issues.append(ValidationIssue(f"{path}.reason_kind", "erlaubt: null oder not_checkable"))
    elif kind is not None and status != "none":
        issues.append(ValidationIssue(f"{path}.reason_kind", "nur bei Status none"))
    if status == "defect" and entry is not None and (entry.basis == "legal_judgment" or entry.max_status == "notice"):
        issues.append(ValidationIssue(f"{path}.status", DEFECT_NOT_ALLOWED))
    return issues


def _validate_evidence_item(item: Any, path: str, report_dir: Path) -> list[ValidationIssue]:
    issues, ok = _shape(item, path, ("kind",), ("file", "caption", "alt", "excerpt"))
    if not ok:
        return issues
    kind = item.get("kind")
    if "kind" in item and kind not in EVIDENCE_KINDS:
        issues.append(ValidationIssue(f"{path}.kind", f"erlaubt: {', '.join(EVIDENCE_KINDS)}"))
    for key in ("caption", "alt", "excerpt"):
        issues += _optional_text(item, key, path)
    file = item.get("file")
    if file is not None:
        issues += _file_issues(file, f"{path}.file", report_dir, SCREENSHOT_SUFFIXES if kind == "screenshot" else None)
    if kind == "screenshot":
        if file is None:
            issues.append(ValidationIssue(f"{path}.file", "Pflicht bei screenshot"))
        alt = item.get("alt")
        if alt is None or (isinstance(alt, str) and not alt.strip()):
            issues.append(ValidationIssue(f"{path}.alt", "Pflicht bei screenshot (Alternativtext)"))
    elif file is None and not _non_empty(item.get("excerpt")):
        issues.append(ValidationIssue(path, "Datei oder Auszug nötig"))
    return issues


def _validate_fix(fix: Any, path: str) -> list[ValidationIssue]:
    if fix is None:
        return []
    issues, ok = _shape(fix, path, (), ("steps", "snippets", "effort"))
    if not ok:
        return issues
    if "steps" in fix:
        issues += _text_list(fix["steps"], f"{path}.steps")
    snippets = fix.get("snippets")
    if "snippets" in fix and not isinstance(snippets, list):
        issues.append(ValidationIssue(f"{path}.snippets", "muss eine Liste sein"))
    for i, snippet in enumerate(snippets if isinstance(snippets, list) else []):
        snippet_path = f"{path}.snippets[{i}]"
        snippet_issues, snippet_ok = _shape(snippet, snippet_path, ("code",), ("target", "lang"))
        issues += snippet_issues
        if snippet_ok:
            issues += [ValidationIssue(f"{snippet_path}.{k}", "muss ein Text sein")
                       for k in ("code", "target", "lang") if k in snippet and not isinstance(snippet[k], str)]
    if "effort" in fix:
        issues += _validate_effort(fix["effort"], f"{path}.effort")
    return issues


def _validate_effort(effort: Any, path: str) -> list[ValidationIssue]:
    issues, ok = _shape(effort, path, ("level", "minutes"), ())
    if not ok:
        return issues
    if "level" in effort and effort["level"] not in EFFORT_LEVELS:
        issues.append(ValidationIssue(f"{path}.level", f"erlaubt: {', '.join(EFFORT_LEVELS)}"))
    minutes = effort.get("minutes")
    if "minutes" in effort and not (isinstance(minutes, int) and not isinstance(minutes, bool) and minutes > 0):
        issues.append(ValidationIssue(f"{path}.minutes", "muss eine positive ganze Zahl sein"))
    return issues


def _validate_result_parts(result: dict, path: str, report_dir: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for key in RESULT_TEXT_KEYS:
        issues += _optional_text(result, key, path)
    evidence = result.get("evidence")
    if evidence is not None and not isinstance(evidence, list):
        issues.append(ValidationIssue(f"{path}.evidence", "muss eine Liste sein"))
    for j, item in enumerate(evidence if isinstance(evidence, list) else []):
        issues += _validate_evidence_item(item, f"{path}.evidence[{j}]", report_dir)
    issues += _validate_fix(result.get("fix"), f"{path}.fix")
    retest = result.get("retest")
    if retest is not None:
        retest_issues, retest_ok = _shape(retest, f"{path}.retest", (), ("how", "command", "expected"))
        issues += retest_issues
        if retest_ok:
            for key in ("how", "command", "expected"):
                issues += _optional_text(retest, key, f"{path}.retest")
    references = result.get("references")
    if references is not None and not isinstance(references, list):
        issues.append(ValidationIssue(f"{path}.references", "muss eine Liste sein"))
    for j, ref in enumerate(references if isinstance(references, list) else []):
        if not _is_https_link(ref):
            issues.append(ValidationIssue(f"{path}.references[{j}]", "nur https-Links ohne Leer- oder Sonderzeichen"))
    if result.get("checklist") is not None:
        issues += _text_list(result["checklist"], f"{path}.checklist")
    return issues


def _validate_results(results: Any, catalog: Catalog, report_dir: Path) -> list[ValidationIssue]:
    if not isinstance(results, list):
        return [ValidationIssue("results", "muss eine Liste sein")]
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for i, result in enumerate(results):
        path = f"results[{i}]"
        shape_issues, ok = _shape(result, path, ("id", "status"), RESULT_OPTIONAL)
        issues += shape_issues
        if not ok:
            continue
        id_issues, entry = _check_id(result, path, catalog, seen)
        issues += id_issues
        status = result.get("status")
        if "status" in result and status not in STATUSES:
            issues.append(ValidationIssue(f"{path}.status", f"erlaubt: {', '.join(STATUSES)}"))
        elif status in STATUSES:
            issues += _status_rules(result, path, status, entry)
        issues += _validate_result_parts(result, path, report_dir)
    return issues


# ---------------------------------------------------------------- entry point

def validate_input(findings: dict, catalog: Catalog, report_dir: Path, *,
                   phrases: Sequence[str] | None = None) -> list[ValidationIssue]:
    """Every rule violation of the raw findings.json; an empty list means step 1 passed."""
    if not isinstance(findings, dict):
        return [ValidationIssue("findings", "muss ein JSON-Objekt sein")]
    issues, _ = _shape(findings, "", TOP_REQUIRED, TOP_OPTIONAL)
    if "schema_version" in findings and findings["schema_version"] != SCHEMA_VERSION:
        issues.append(ValidationIssue("schema_version", f"erwartet {SCHEMA_VERSION}"))
    if "catalog_version" in findings and findings["catalog_version"] != catalog.version:
        issues.append(ValidationIssue("catalog_version", f"erwartet {catalog.version} (Version des Prüfkatalogs)"))
    issues += _text(findings, "plugin_version", "")
    report_dir = Path(report_dir)
    checks = (
        ("run", lambda v: _validate_run(v)),
        ("issuer", lambda v: _validate_issuer(v, report_dir)),
        ("client", lambda v: _validate_client(v)),
        ("applicability", lambda v: _validate_applicability(v)),
        ("summary", lambda v: _validate_summary(v, catalog)),
        ("results", lambda v: _validate_results(v, catalog, report_dir)),
    )
    for key, check in checks:
        if key in findings:
            issues += check(findings[key])
    issues += check_texts(iter_prose(findings), phrases if phrases is not None else load_forbidden_phrases())
    return issues
