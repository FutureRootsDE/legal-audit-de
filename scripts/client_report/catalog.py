"""Test catalog v1: load, validate and evaluate applicability conditions (spec 6.3, 6.4, 6.9.1, 6.10).

The catalog is a plugin asset (templates/client-test/catalog.json, resolved relative to this
file, never to the working directory). It fixes IDs, titles, legal bases with `valid_from`,
applicability conditions and the kind of test (`basis`); findings.json only adds run data.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from .models import AreaInfo, Catalog, CatalogEntry, LegalBasis, ReportInputError, ValidationIssue
from .textcheck import check_texts, load_forbidden_phrases

DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[2] / "templates" / "client-test" / "catalog.json"

APPLICABILITY_KEYS = ("b2c", "shop", "bfsg", "subscription", "more_than_10_employees",
                      "platform_features", "ai_chat", "durability_guarantee")
AREA_ORDER = ("IMP", "DSE", "CK", "DRT", "SEC", "FRM", "A11Y", "SHOP", "UWG", "KI", "DSA")
BASIS_VALUES = ("measurable", "legal_judgment")
MAX_STATUS_VALUES = ("notice",)
ALWAYS_RUN_AREA = "A11Y"

ID_RE = re.compile(r"^(" + "|".join(AREA_ORDER) + r")-(\d{2})$")
VERSION_RE = re.compile(r"^\d{4}\.\d{2}-\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Path inside knowledge/ (one folder level, lower-case slug), optional line numbers "md:12,40".
KB_REF_RE = re.compile(r"^[a-z0-9-]+/[a-z0-9-]+\.md(:\d+(,\d+)*)?$")

TOP_KEYS = ("catalog_version", "areas", "entries", "glossary")
AREA_KEYS = ("prefix", "title", "intro")
ENTRY_KEYS = ("id", "area", "title", "description", "legal_basis", "applies_if", "always_run",
              "basis", "max_status", "not_applicable_reason", "retest_default")
BASIS_KEYS = ("norm", "valid_from", "kb_ref")
GLOSSARY_KEYS = ("term", "text")
ENTRY_PROSE = ("title", "description", "not_applicable_reason", "retest_default")


def _keys_issues(obj: Any, path: str, keys: Sequence[str]) -> list[ValidationIssue]:
    """Object check: must be a dict with exactly `keys` (missing and unknown fields are issues)."""
    if not isinstance(obj, dict):
        return [ValidationIssue(path, "muss ein Objekt sein")]
    issues = [ValidationIssue(f"{path}.{k}", "Pflichtfeld fehlt") for k in keys if k not in obj]
    issues += [ValidationIssue(f"{path}.{k}", "unbekanntes Feld") for k in obj if k not in keys]
    return issues


def _text_issue(obj: dict, key: str, path: str, allow_empty: bool = False) -> list[ValidationIssue]:
    value = obj.get(key)
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        return [ValidationIssue(f"{path}.{key}", "muss ein nicht leerer Text sein" if not allow_empty
                                else "muss ein Text sein")]
    return []


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str) or not DATE_RE.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _validate_areas(areas: Any) -> list[ValidationIssue]:
    if not isinstance(areas, list):
        return [ValidationIssue("areas", "muss eine Liste sein")]
    issues: list[ValidationIssue] = []
    for i, area in enumerate(areas):
        path = f"areas[{i}]"
        issues += _keys_issues(area, path, AREA_KEYS)
        if isinstance(area, dict):
            for key in AREA_KEYS:
                issues += _text_issue(area, key, path)
    prefixes = tuple(a.get("prefix") for a in areas if isinstance(a, dict))
    if prefixes != AREA_ORDER:
        issues.append(ValidationIssue("areas", f"Bereiche müssen genau {', '.join(AREA_ORDER)} in dieser Reihenfolge sein"))
    return issues


def _validate_legal_basis(items: Any, path: str) -> list[ValidationIssue]:
    if not isinstance(items, list) or not items:
        return [ValidationIssue(path, "mindestens eine Rechtsgrundlage nötig")]
    issues: list[ValidationIssue] = []
    for j, item in enumerate(items):
        item_path = f"{path}[{j}]"
        issues += _keys_issues(item, item_path, BASIS_KEYS)
        if not isinstance(item, dict):
            continue
        issues += _text_issue(item, "norm", item_path)
        if "valid_from" in item and _parse_date(item["valid_from"]) is None:
            issues.append(ValidationIssue(f"{item_path}.valid_from", "muss ein ISO-Datum JJJJ-MM-TT sein"))
        kb_ref = item.get("kb_ref")
        if "kb_ref" in item and not (isinstance(kb_ref, str) and KB_REF_RE.match(kb_ref)):
            issues.append(ValidationIssue(f"{item_path}.kb_ref", "Format „ordner/datei.md:zeile“ innerhalb von knowledge/"))
    return issues


def _validate_flags(entry: dict, path: str, area: str | None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    applies_if = entry.get("applies_if")
    if not isinstance(applies_if, list) or not all(isinstance(k, str) for k in applies_if):
        issues.append(ValidationIssue(f"{path}.applies_if", "muss eine Liste von Schlüsseln sein"))
        applies_if = []
    elif any(k not in APPLICABILITY_KEYS for k in applies_if) or len(set(applies_if)) != len(applies_if):
        issues.append(ValidationIssue(f"{path}.applies_if", f"nur eindeutige Schlüssel aus {', '.join(APPLICABILITY_KEYS)}"))
    always_run = entry.get("always_run")
    if not isinstance(always_run, bool) or always_run != (area == ALWAYS_RUN_AREA):
        issues.append(ValidationIssue(f"{path}.always_run", f"true genau bei Bereich {ALWAYS_RUN_AREA}"))
    if area == ALWAYS_RUN_AREA and applies_if:
        issues.append(ValidationIssue(f"{path}.applies_if", f"muss bei Bereich {ALWAYS_RUN_AREA} leer sein"))
    if entry.get("basis") not in BASIS_VALUES:
        issues.append(ValidationIssue(f"{path}.basis", f"erlaubt: {', '.join(BASIS_VALUES)}"))
    if entry.get("max_status") is not None and entry.get("max_status") not in MAX_STATUS_VALUES:
        issues.append(ValidationIssue(f"{path}.max_status", "erlaubt: null oder notice"))
    if applies_if and isinstance(entry.get("not_applicable_reason"), str) and not entry["not_applicable_reason"].strip():
        issues.append(ValidationIssue(f"{path}.not_applicable_reason", "Pflicht bei Anwendbarkeitsbedingung"))
    return issues


def _validate_entry(entry: Any, path: str) -> tuple[list[ValidationIssue], tuple[int, int] | None]:
    """Issues of one entry plus its sort key (area index, number) when the ID is well formed."""
    issues = _keys_issues(entry, path, ENTRY_KEYS)
    if not isinstance(entry, dict):
        return issues, None
    match = ID_RE.match(entry["id"]) if isinstance(entry.get("id"), str) else None
    if match is None:
        issues.append(ValidationIssue(f"{path}.id", "Format BEREICH-NN mit bekanntem Bereich"))
    elif entry.get("area") != match.group(1):
        issues.append(ValidationIssue(f"{path}.area", f"muss zum ID-Präfix {match.group(1)} passen"))
    for key in ENTRY_PROSE:
        issues += _text_issue(entry, key, path, allow_empty=key == "not_applicable_reason")
    issues += _validate_legal_basis(entry.get("legal_basis"), f"{path}.legal_basis")
    issues += _validate_flags(entry, path, match.group(1) if match else None)
    key = (AREA_ORDER.index(match.group(1)), int(match.group(2))) if match else None
    return issues, key


def _validate_entries(entries: Any) -> list[ValidationIssue]:
    if not isinstance(entries, list) or not entries:
        return [ValidationIssue("entries", "muss eine nicht leere Liste sein")]
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    last_key: tuple[int, int] | None = None
    for i, entry in enumerate(entries):
        path = f"entries[{i}]"
        entry_issues, key = _validate_entry(entry, path)
        issues += entry_issues
        entry_id = entry.get("id") if isinstance(entry, dict) else None
        if isinstance(entry_id, str) and entry_id in seen:
            issues.append(ValidationIssue(f"{path}.id", f"doppelte ID {entry_id}"))
        elif key is not None and last_key is not None and key < last_key:
            issues.append(ValidationIssue(f"{path}.id", "Reihenfolge: Bereiche wie AREA_ORDER, Nummern aufsteigend"))
        if isinstance(entry_id, str):
            seen.add(entry_id)
        last_key = key if key is not None else last_key
    return issues


def _validate_glossary(glossary: Any) -> list[ValidationIssue]:
    if not isinstance(glossary, list) or not glossary:
        return [ValidationIssue("glossary", "muss eine nicht leere Liste sein")]
    issues: list[ValidationIssue] = []
    terms: set[str] = set()
    for i, item in enumerate(glossary):
        path = f"glossary[{i}]"
        issues += _keys_issues(item, path, GLOSSARY_KEYS)
        if not isinstance(item, dict):
            continue
        for key in GLOSSARY_KEYS:
            issues += _text_issue(item, key, path)
        if item.get("term") in terms:
            issues.append(ValidationIssue(f"{path}.term", "doppelter Begriff"))
        terms.add(item.get("term"))
    return issues


def _iter_prose(raw: dict) -> Iterator[tuple[str, str]]:
    """(field path, text) of every catalog field that appears as authored text in the report."""
    for i, area in enumerate(raw.get("areas") or []):
        if isinstance(area, dict):
            for key in ("title", "intro"):
                if isinstance(area.get(key), str):
                    yield f"areas[{i}].{key}", area[key]
    for i, entry in enumerate(raw.get("entries") or []):
        if not isinstance(entry, dict):
            continue
        for key in ENTRY_PROSE:
            if isinstance(entry.get(key), str):
                yield f"entries[{i}].{key}", entry[key]
        for j, item in enumerate(entry.get("legal_basis") or []):
            if isinstance(item, dict) and isinstance(item.get("norm"), str):
                yield f"entries[{i}].legal_basis[{j}].norm", item["norm"]
    for i, item in enumerate(raw.get("glossary") or []):
        if isinstance(item, dict):
            for key in GLOSSARY_KEYS:
                if isinstance(item.get(key), str):
                    yield f"glossary[{i}].{key}", item[key]


def validate_catalog(raw: dict, phrases: Sequence[str]) -> list[ValidationIssue]:
    """All rule violations of a parsed catalog (structure, IDs, flags, dates, text rules)."""
    if not isinstance(raw, dict):
        return [ValidationIssue("catalog", "muss ein JSON-Objekt sein")]
    issues = _keys_issues(raw, "catalog", TOP_KEYS)
    version = raw.get("catalog_version")
    if not (isinstance(version, str) and VERSION_RE.match(version)):
        issues.append(ValidationIssue("catalog_version", "Format JJJJ.MM-N"))
    issues += _validate_areas(raw.get("areas"))
    issues += _validate_entries(raw.get("entries"))
    issues += _validate_glossary(raw.get("glossary"))
    issues += check_texts(_iter_prose(raw), phrases)
    return issues


def _build(raw: dict) -> Catalog:
    entries = tuple(
        CatalogEntry(
            id=e["id"], area=e["area"], title=e["title"], description=e["description"],
            legal_basis=tuple(LegalBasis(b["norm"], date.fromisoformat(b["valid_from"]), b["kb_ref"])
                              for b in e["legal_basis"]),
            applies_if=tuple(e["applies_if"]), always_run=e["always_run"], basis=e["basis"],
            max_status=e["max_status"], not_applicable_reason=e["not_applicable_reason"],
            retest_default=e["retest_default"],
        )
        for e in raw["entries"]
    )
    return Catalog(
        version=raw["catalog_version"],
        areas=tuple(AreaInfo(a["prefix"], a["title"], a["intro"]) for a in raw["areas"]),
        entries=entries,
        glossary=tuple((g["term"], g["text"]) for g in raw["glossary"]),
    )


def load_catalog(path: Path | None = None) -> Catalog:
    """Read and validate the catalog; raises ReportInputError listing every issue."""
    source = Path(path) if path is not None else DEFAULT_CATALOG_PATH
    try:
        raw = json.loads(source.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ReportInputError([ValidationIssue("catalog", f"kein gültiges JSON (Zeile {exc.lineno}, Spalte {exc.colno})")]) from exc
    issues = validate_catalog(raw, load_forbidden_phrases())
    if issues:
        raise ReportInputError(issues)
    return _build(raw)


def evaluate(applies_if: Sequence[str], applicability: Mapping[str, bool | None]) -> bool | None:
    """Three-valued AND over the conditions: any False wins, else any unknown gives None, else True."""
    result: bool | None = True
    for key in applies_if:
        value = applicability.get(key)
        if value is False:
            return False
        if value is not True:
            result = None
    return result
