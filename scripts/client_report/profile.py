"""Issuer letterhead profile: company, contact, address, logo copy and accent color.

Only the issuer is stored here. Client data never goes into the profile (spec A4).
"""
from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Mapping

from .models import ReportInputError, ValidationIssue

PROFILE_FILENAME = "client-test-profile.json"
FALLBACK_DIRNAME = "legal-audit-de-client-test"
HOME_OVERRIDE_ENV = "LEGAL_AUDIT_CLIENT_TEST_HOME"
LOGO_BASENAME = "client-test-logo"
LOGO_EXTENSIONS = ("png", "jpg", "jpeg", "svg")
MAX_LOGO_BYTES = 5 * 1024 * 1024
MAX_FIELD_CHARS = 300
MAX_ADDRESS_LINES = 8

REQUIRED_KEYS = ("company", "contact", "address", "logo_file", "accent_color")
OPTIONAL_KEYS = ("phone", "website", "email")
ACCENT_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
LOGO_FILE_RE = re.compile(rf"^{LOGO_BASENAME}\.(?:{'|'.join(LOGO_EXTENSIONS)})$")
SVG_START_RE = re.compile(rb"<svg[\s>]", re.IGNORECASE)


def profile_dir(env: Mapping[str, str] | None = None) -> Path:
    """Directory of the profile: test override, plugin data, Codex, Copilot, else ~/.claude."""
    env = os.environ if env is None else env
    if env.get(HOME_OVERRIDE_ENV):
        return Path(env[HOME_OVERRIDE_ENV])
    if env.get("CLAUDE_PLUGIN_DATA"):
        return Path(env["CLAUDE_PLUGIN_DATA"])
    if env.get("CODEX_HOME"):
        return Path(env["CODEX_HOME"]) / FALLBACK_DIRNAME
    if env.get("COPILOT_HOME"):
        return Path(env["COPILOT_HOME"]) / FALLBACK_DIRNAME
    return Path.home() / ".claude" / FALLBACK_DIRNAME


def _text_issue(path: str, value: object) -> ValidationIssue | None:
    if not isinstance(value, str) or not value.strip():
        return ValidationIssue(path, "muss ein nicht leerer Text sein")
    if len(value) > MAX_FIELD_CHARS:
        return ValidationIssue(path, f"zu lang (höchstens {MAX_FIELD_CHARS} Zeichen)")
    return None


def validate_profile(data: Mapping) -> list[ValidationIssue]:
    """Blocking problems of a profile; unknown keys (for example client data) are rejected."""
    if not isinstance(data, Mapping):
        return [ValidationIssue("profile", "muss ein Objekt sein")]
    issues: list[ValidationIssue] = []
    allowed = set(REQUIRED_KEYS) | set(OPTIONAL_KEYS)
    for key in data:
        if key not in allowed:
            issues.append(ValidationIssue(f"profile.{key}", "unbekanntes Feld (nur Absenderdaten erlaubt)"))
    for key in REQUIRED_KEYS:
        if key not in data:
            issues.append(ValidationIssue(f"profile.{key}", "Pflichtfeld fehlt"))
    for key in ("company", "contact") + OPTIONAL_KEYS:
        if key in data:
            issue = _text_issue(f"profile.{key}", data[key])
            if issue:
                issues.append(issue)
    if "address" in data:
        address = data["address"]
        if not isinstance(address, list) or not address or len(address) > MAX_ADDRESS_LINES:
            issues.append(
                ValidationIssue("profile.address", f"muss eine Liste mit 1 bis {MAX_ADDRESS_LINES} Zeilen sein")
            )
        else:
            for i, line in enumerate(address):
                issue = _text_issue(f"profile.address[{i}]", line)
                if issue:
                    issues.append(issue)
    if not any(data.get(k) for k in OPTIONAL_KEYS):
        issues.append(ValidationIssue("profile", "mindestens eines von email, phone, website ist nötig"))
    if "logo_file" in data:
        logo = data["logo_file"]
        if not (isinstance(logo, str) and LOGO_FILE_RE.match(logo)):
            issues.append(
                ValidationIssue(
                    "profile.logo_file",
                    f"muss ein Dateiname {LOGO_BASENAME}.<png|jpg|jpeg|svg> ohne Pfad sein",
                )
            )
    if "accent_color" in data:
        accent = data["accent_color"]
        if not (isinstance(accent, str) and ACCENT_RE.match(accent)):
            issues.append(ValidationIssue("profile.accent_color", "muss ein Hex-Wert wie #1F4E79 sein"))
    return issues


def load_profile(env: Mapping[str, str] | None = None) -> dict | None:
    """The stored profile, or None when missing, unreadable, invalid or without its logo file."""
    base = profile_dir(env)
    try:
        data = json.loads((base / PROFILE_FILENAME).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or validate_profile(data):
        return None
    if not (base / data["logo_file"]).is_file():
        return None
    return data


def logo_path(profile: Mapping, env: Mapping[str, str] | None = None) -> Path:
    """Absolute path of the stored logo copy of a validated profile."""
    return profile_dir(env) / profile["logo_file"]


def _logo_kind_matches(ext: str, head: bytes) -> bool:
    if ext == "png":
        return head.startswith(b"\x89PNG\r\n\x1a\n")
    if ext in ("jpg", "jpeg"):
        return head.startswith(b"\xff\xd8\xff")
    return bool(SVG_START_RE.search(head))


def _read_logo(logo_src: Path) -> tuple[bytes, str]:
    """Read a user-supplied logo: regular file, known extension, size cap, matching content."""
    src = Path(logo_src)
    ext = src.suffix.lower().lstrip(".")
    if ext not in LOGO_EXTENSIONS:
        raise ValueError(f"Logo-Format nicht unterstützt: .{ext} (erlaubt: png, jpg, jpeg, svg)")
    if not src.is_file():
        raise ValueError("Logo ist keine Datei")
    if src.stat().st_size > MAX_LOGO_BYTES:
        raise ValueError(f"Logo ist größer als {MAX_LOGO_BYTES // (1024 * 1024)} MB")
    content = src.read_bytes()
    if not _logo_kind_matches(ext, content[:2048]):
        raise ValueError("Logo-Inhalt passt nicht zur Dateiendung")
    return content, ext


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def save_profile(data: Mapping, logo_src: Path, env: Mapping[str, str] | None = None) -> Path:
    """Validate, copy the logo as client-test-logo.<ext> and write the profile atomically."""
    content, ext = _read_logo(logo_src)
    record = dict(data)
    record["logo_file"] = f"{LOGO_BASENAME}.{ext}"
    issues = validate_profile(record)
    if issues:
        raise ReportInputError(issues)
    base = profile_dir(env)
    base.mkdir(parents=True, exist_ok=True)
    for old in LOGO_EXTENSIONS:
        stale = base / f"{LOGO_BASENAME}.{old}"
        if old != ext and stale.is_file():
            stale.unlink()
    _atomic_write_bytes(base / record["logo_file"], content)
    text = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    target = base / PROFILE_FILENAME
    _atomic_write_bytes(target, text.encode("utf-8"))
    return target
