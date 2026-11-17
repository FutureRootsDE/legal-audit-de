"""Test helpers for client_report: PNG writer, report folder and findings.json builders."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path
from typing import Any

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.catalog import APPLICABILITY_KEYS, evaluate
from client_report.models import Catalog

DEFAULT_STARTED = "2026-11-17T09:12:03Z"
DEFAULT_FINISHED = "2026-11-17T09:31:40Z"
LOGO_FILE = "assets/logo.png"
SHOT_FILE = "evidence/shot.png"
OPEN_STATUSES = ("notice", "defect")


def write_png(path: Path, rgb: tuple[int, int, int], size: tuple[int, int] = (4, 4)) -> None:
    """Write a solid-color 8-bit RGB PNG (no filter) using only zlib and struct."""
    width, height = size
    row = b"\x00" + bytes(rgb) * width
    raw = row * height

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    payload = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def make_report_dir(tmp: Path) -> Path:
    """Report folder with assets/logo.png and evidence/shot.png, as `init` and the browser phase leave it."""
    report_dir = Path(tmp) / "2026-11-17-example-de"
    write_png(report_dir / LOGO_FILE, (31, 78, 121))
    write_png(report_dir / SHOT_FILE, (200, 200, 200))
    return report_dir


def pass_result(test_id: str) -> dict[str, Any]:
    return {"id": test_id, "status": "pass", "one_liner": "Im geprüften Umfang nichts beobachtet."}


def open_result(test_id: str, status: str, severity: str) -> dict[str, Any]:
    """Complete notice/defect result with every field a derived open status needs."""
    return {
        "id": test_id,
        "status": status,
        "severity": severity,
        "severity_original": None,
        "reason_kind": None,
        "reason": None,
        "one_liner": "Beim ersten Aufruf lädt die Seite Schriften von einem fremden Server.",
        "client_text": "Beim ersten Aufruf lädt die Seite Schriften von fonts.googleapis.com, bevor eine Einwilligung erteilt ist.",
        "client_action": "Bitten Sie Ihre Webagentur, die Schriften lokal einzubinden.",
        "review_question": "Ist die Einbindung in dieser Form mit Ihrer Rechtsberatung abgestimmt?",
        "evidence": [
            {"kind": "screenshot", "file": SHOT_FILE, "caption": "Startseite beim ersten Aufruf",
             "alt": "Startseite mit Cookie-Banner"},
            {"kind": "network", "excerpt": "GET https://fonts.googleapis.com/css2?family=Roboto 200"},
        ],
        "risk": "Datenübermittlungen ohne Einwilligung können Rückfragen von Aufsichtsbehörden auslösen.",
        "fix": {
            "steps": ["Schriftdateien herunterladen.", "Schriften aus dem eigenen Server laden."],
            "snippets": [{"target": "css", "lang": "css", "code": "@font-face { font-family: Roboto; }"}],
            "effort": {"level": "gering", "minutes": 30},
        },
        "retest": {"how": "Seite im privaten Fenster öffnen und das Netzwerkprotokoll prüfen.",
                   "command": "curl -sI https://www.example.de/", "expected": "HTTP/2 200"},
        "references": ["https://www.gesetze-im-internet.de/ttdsg/__25.html"],
        "checklist": ["Netzwerkprotokoll ohne Anfragen an fonts.googleapis.com"],
    }


def valid_findings(catalog: Catalog, **overrides: Any) -> dict[str, Any]:
    """Valid findings.json: every applicable ID `pass`, intake all false except b2c and bfsg.

    Overrides: any applicability key (value True/False/None), `started` (run.started_utc),
    `results` (replace the pass rows of these IDs, placed first), `results_extra` (appended
    as given), `top_actions` (default: open IDs among `results`, at most 3), or any top-level
    key of findings.json (replaces that block).
    """
    overrides = dict(overrides)
    values: dict[str, bool | None] = {key: key in ("b2c", "bfsg") for key in APPLICABILITY_KEYS}
    for key in APPLICABILITY_KEYS:
        if key in overrides:
            values[key] = overrides.pop(key)
    started = overrides.pop("started", DEFAULT_STARTED)
    given = list(overrides.pop("results", []))
    extra = list(overrides.pop("results_extra", []))
    top_actions = overrides.pop("top_actions", None)
    given_ids = {r.get("id") for r in given}
    passes = [pass_result(e.id) for e in catalog.entries
              if e.id not in given_ids and evaluate(e.applies_if, values) is not False]
    if top_actions is None:
        open_ids = [r.get("id") for r in given if r.get("status") in OPEN_STATUSES and r.get("id") in catalog.by_id]
        top_actions = list(dict.fromkeys(open_ids))[:3]
    findings: dict[str, Any] = {
        "schema_version": "1.0",
        "catalog_version": catalog.version,
        "plugin_version": "1.5.0",
        "run": {
            "started_utc": started,
            "finished_utc": DEFAULT_FINISHED if started == DEFAULT_STARTED else started,
            "target_url": "https://example.de/",
            "final_url": "https://www.example.de/",
            "domain": "example.de",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0",
            "viewports": ["1920x1080", "390x844 (mobil)"],
            "tools": {"chrome": "131.0", "chrome_devtools_mcp": "0.10.0"},
            "pages_visited": ["https://www.example.de/", "https://www.example.de/impressum"],
        },
        "issuer": {"company": "Muster Webdesign GmbH", "contact": "Erika Muster",
                   "address": ["Hauptstraße 1", "10115 Berlin"], "email": "info@muster-web.de",
                   "logo_file": LOGO_FILE, "accent_color": "#1F4E79"},
        "client": {"name": "Max Kunde", "company": "Kunde GmbH", "address": ["Marktplatz 2", "50667 Köln"]},
        "applicability": {key: {"value": value, "source": "user"} for key, value in values.items()},
        "summary": {"sentences": ["Satz eins.", "Satz zwei.", "Satz drei."], "top_actions": top_actions},
        "results": given + passes + extra,
    }
    for key, value in overrides.items():
        if key not in findings:
            raise TypeError(f"unknown override: {key}")
        findings[key] = value
    return findings
