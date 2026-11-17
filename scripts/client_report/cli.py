"""Command line of the website check-up: check, profile, init, plan, render and pdf (spec 6.9).

Exit codes: 0 ok, 1 input error, 2 broken plugin installation, 3 no letterhead profile,
4 Chrome or Edge not found, 5 accent color unknown (profile save), 6 PDF creation failed.
All plugin assets are resolved relative to this file, never to the working directory.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Sequence

from .accent import DEFAULT_ACCENT, derive_accent, ensure_contrast
from .catalog import APPLICABILITY_KEYS, evaluate, load_catalog
from .chrome import ChromeNotFound, PdfError, find_chrome, print_pdf
from .derive import check_date
from .models import ReportInputError
from .paths import domain_from_url, domain_slug, new_report_dir
from .pipeline import REPORT_FILENAME, build_report
from .profile import ACCENT_RE, ensure_writable_dir, load_profile, logo_path, profile_dir, save_profile
from .render import CSS_PATH, FONT_FACES, FONTS_DIR, PAGED_JS_ENABLED, TEMPLATE_PATH
from .schema import FINDINGS_PATH, SCHEMA_VERSION, UTC_FORMAT, load_findings
from .texts import START_HINT
from .textcheck import DEFAULT_PHRASES_PATH, load_forbidden_phrases

EXIT_OK, EXIT_INPUT, EXIT_BROKEN, EXIT_NO_PROFILE, EXIT_NO_CHROME, EXIT_ACCENT, EXIT_PDF = 0, 1, 2, 3, 4, 5, 6
PLUGIN_JSON = Path(__file__).resolve().parents[2] / ".claude-plugin" / "plugin.json"
DEFAULT_BASE = "client-reports"
GITIGNORE_HINT = "Hinweis: Der Ordner client-reports/ ist nicht in .gitignore eingetragen. Er enthält Kundendaten."
NO_PROFILE_MESSAGE = "Kein Briefkopf-Profil gespeichert."
NO_CHROME_MESSAGE = "Chrome oder Edge nicht gefunden. report.html bleibt das Ergebnis."
ACCENT_UNKNOWN = "ACCENT_UNKNOWN"
PDF_PROFILE_KEYS = ("contact", "phone", "email", "website")


def _err(message: str) -> None:
    print(message, file=sys.stderr)


def _plugin_version() -> str:
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8-sig"))
    version = data.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("version fehlt in plugin.json")
    return version


def _write_json_atomic(path: Path, data: object) -> None:
    ensure_writable_dir(path.parent)
    fd, tmp = tempfile.mkstemp(prefix=".findings-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _report_issues(exc: ReportInputError) -> int:
    for issue in exc.issues:
        _err(str(issue))
    return EXIT_INPUT


# ---------------------------------------------------------------- check

def _check_items() -> list[tuple[str, object]]:
    return [
        ("Prüfkatalog", lambda: f"Version {load_catalog().version}"),
        ("Vorlage", lambda: _exists(TEMPLATE_PATH)),
        ("Stylesheet", lambda: _exists(CSS_PATH)),
        ("Schriften", lambda: _fonts()),
        ("Sperrliste", lambda: f"{len(load_forbidden_phrases())} Wendungen ({DEFAULT_PHRASES_PATH.name})"),
        ("Paged.js", lambda: "nicht aktiv" if not PAGED_JS_ENABLED else "aktiv"),
    ]


def _exists(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return path.name


def _fonts() -> str:
    for _family, name, _weight, _style in FONT_FACES:
        _exists(FONTS_DIR / name)
    return f"{len(FONT_FACES)} Dateien"


def cmd_check(_args: argparse.Namespace) -> int:
    print(START_HINT)
    failed = False
    for label, probe in _check_items():
        try:
            print(f"OK {label}: {probe()}")  # type: ignore[operator]
        except (OSError, ValueError, ReportInputError) as exc:
            failed = True
            _err(f"FEHLER {label}: {exc}")
    try:
        print(f"plugin_version: {_plugin_version()}")
    except (OSError, ValueError) as exc:
        failed = True
        _err(f"FEHLER plugin.json: {exc}")
    return EXIT_BROKEN if failed else EXIT_OK


# ---------------------------------------------------------------- profile

def _ask_accent() -> str | None:
    """One prompt on a terminal: a hex value, "" for Enter (default), None when unknown.

    End of input, an unreadable stdin and an invalid value all give None, never the default.
    """
    try:
        answer = input("Akzentfarbe als Hex-Wert (z. B. #1F4E79), Enter für Standard: ").strip()
    except (EOFError, OSError, ValueError):
        return None
    if answer and not ACCENT_RE.fullmatch(answer):
        _err("Ungültiger Hex-Wert. Erwartet wird zum Beispiel #1F4E79.")
        return None
    return answer


def _resolve_accent(option: str | None, logo: Path) -> str | None:
    if option == "default":
        return DEFAULT_ACCENT
    if option is not None:
        if not ACCENT_RE.fullmatch(option):
            raise ValueError("--accent muss ein Hex-Wert wie #1F4E79 oder default sein")
        return ensure_contrast(option)
    derived = derive_accent(logo)
    if derived is not None:
        return derived
    if sys.stdin.isatty():
        asked = _ask_accent()
        if asked is None:
            return None
        return ensure_contrast(asked) if asked else DEFAULT_ACCENT
    return None


def cmd_profile_show(args: argparse.Namespace) -> int:
    profile = load_profile()
    if profile is None:
        _err(NO_PROFILE_MESSAGE)
        return EXIT_NO_PROFILE
    if args.json:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
        return EXIT_OK
    for key, value in profile.items():
        print(f"{key}: {', '.join(value) if isinstance(value, list) else value}")
    print(f"Ordner: {profile_dir()}")
    return EXIT_OK


def cmd_profile_save(args: argparse.Namespace) -> int:
    try:
        data = json.loads(Path(args.data).read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("--data muss ein JSON-Objekt enthalten")
        accent = _resolve_accent(args.accent, Path(args.logo))
        if accent is None:
            print(f"{ACCENT_UNKNOWN}: Aus dem Logo lässt sich keine Akzentfarbe ableiten. "
                  "Bitte mit --accent <hex> oder --accent default erneut aufrufen.")
            return EXIT_ACCENT
        record = {k: v for k, v in data.items() if k not in ("logo_file", "accent_color")}
        record["accent_color"] = accent
        target = save_profile(record, Path(args.logo))
    except ReportInputError as exc:
        return _report_issues(exc)
    except (OSError, ValueError) as exc:
        _err(f"Profil nicht gespeichert: {exc}")
        return EXIT_INPUT
    print(f"Profil gespeichert (Akzentfarbe {accent}):")
    print(target)
    return EXIT_OK


# ---------------------------------------------------------------- init

def _reports_not_ignored(base: Path) -> bool:
    """True when the cwd is in a git repository and `base` is not ignored there."""
    try:
        inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, timeout=15)
        if inside.returncode != 0:
            return False
        ignored = subprocess.run(["git", "check-ignore", "-q", str(base)], capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return ignored.returncode == 1


def _skeleton(url: str, domain: str, started: str, profile: dict, logo_rel: str, catalog_version: str) -> dict:
    issuer = {"company": profile["company"], "address": list(profile["address"]),
              "logo_file": logo_rel, "accent_color": profile["accent_color"]}
    issuer.update({k: profile[k] for k in PDF_PROFILE_KEYS if k in profile})
    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_version": catalog_version,
        "plugin_version": _plugin_version(),
        "run": {"started_utc": started, "target_url": url, "domain": domain},
        "issuer": issuer,
        "client": {"name": "", "company": "", "address": []},
        "applicability": {key: {"value": None, "source": ""} for key in APPLICABILITY_KEYS},
        "summary": {"sentences": [], "top_actions": []},
        "results": [],
    }


def _parse_day(value: str | None) -> date:
    if not value:
        return datetime.now(timezone.utc).date()
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("--date muss ein gültiges Datum im Format JJJJ-MM-TT sein") from None


def cmd_init(args: argparse.Namespace) -> int:
    profile = load_profile()
    if profile is None:
        _err(NO_PROFILE_MESSAGE)
        return EXIT_NO_PROFILE
    try:
        domain = domain_from_url(args.url)
        day = _parse_day(args.date)
        started = (datetime.now(timezone.utc).strftime(UTC_FORMAT) if not args.date
                   else f"{day.isoformat()}T00:00:00Z")
        base = Path(args.out or DEFAULT_BASE)
        catalog = load_catalog()
        report_dir = new_report_dir(base, day, domain)
        ensure_writable_dir(report_dir)
        logo_src = logo_path(profile)
        logo_rel = f"assets/logo{logo_src.suffix.lower()}"
        shutil.copyfile(logo_src, report_dir / logo_rel)
        _write_json_atomic(report_dir / FINDINGS_PATH,
                           _skeleton(args.url.strip(), domain, started, profile, logo_rel, catalog.version))
    except ReportInputError as exc:
        return _report_issues(exc)
    except (OSError, ValueError) as exc:
        _err(f"init fehlgeschlagen: {exc}")
        return EXIT_INPUT
    if _reports_not_ignored(base):
        print(GITIGNORE_HINT)
    print(report_dir.resolve())
    return EXIT_OK


# ---------------------------------------------------------------- plan

def _intake_values(findings: dict) -> dict[str, bool | None]:
    """Intake answers with every key present, three-valued, and a non-empty source."""
    section = findings.get("applicability")
    if not isinstance(section, dict):
        raise ValueError("applicability fehlt")
    values: dict[str, bool | None] = {}
    for key in APPLICABILITY_KEYS:
        entry = section.get(key)
        if not isinstance(entry, dict) or "value" not in entry:
            raise ValueError(f"Anwendbarkeitsangabe fehlt: {key}")
        if entry["value"] is not None and not isinstance(entry["value"], bool):
            raise ValueError(f"Anwendbarkeitsangabe {key}: value muss true, false oder null sein")
        source = entry.get("source")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"Anwendbarkeitsangabe {key}: source fehlt")
        values[key] = entry["value"]
    return values


def cmd_plan(args: argparse.Namespace) -> int:
    report_dir = Path(args.folder)
    try:
        findings = load_findings(report_dir / FINDINGS_PATH)
        values = _intake_values(findings)
        catalog = load_catalog()
    except ReportInputError as exc:
        return _report_issues(exc)
    except ValueError as exc:
        _err(str(exc))
        return EXIT_INPUT
    rows = findings.get("results")
    rows = list(rows) if isinstance(rows, list) else []
    known = {r["id"] for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str)}
    planned = [e for e in catalog.entries if e.always_run or evaluate(e.applies_if, values) is not False]
    for entry in planned:
        if entry.id not in known:
            rows.append({"id": entry.id, "status": ""})
    findings["results"] = rows
    try:
        _write_json_atomic(report_dir / FINDINGS_PATH, findings)
    except OSError as exc:
        _err(f"{FINDINGS_PATH} konnte nicht geschrieben werden: {exc.strerror or type(exc).__name__}")
        return EXIT_INPUT
    titles = {a.prefix: a.title for a in catalog.areas}
    current = None
    for entry in planned:
        if entry.area != current:
            current = entry.area
            print(f"{current} {titles.get(current, '')}".rstrip())
        print(f"  {entry.id} {entry.title}")
    return EXIT_OK


# ---------------------------------------------------------------- render and pdf

def cmd_render(args: argparse.Namespace) -> int:
    try:
        ensure_writable_dir(Path(args.folder))
        result = build_report(Path(args.folder))
    except ReportInputError as exc:
        return _report_issues(exc)
    except (OSError, RuntimeError) as exc:
        _err(f"render fehlgeschlagen: {exc}")
        return EXIT_INPUT
    for warning in result.warnings:
        _err(warning)
    print(result.html_path.resolve())
    return EXIT_OK


def cmd_pdf(args: argparse.Namespace) -> int:
    report_dir = Path(args.folder)
    html = report_dir / REPORT_FILENAME
    if not html.is_file():
        _err(f"{REPORT_FILENAME} fehlt. Zuerst render ausführen.")
        return EXIT_INPUT
    try:
        findings = load_findings(report_dir / FINDINGS_PATH)
        named = f"Website-CheckUp-{domain_slug(findings['run']['domain'])}-{check_date(findings).isoformat()}.pdf"
    except (ReportInputError, KeyError, TypeError, ValueError) as exc:
        _err(f"findings.json nicht lesbar: {exc}")
        return EXIT_INPUT
    try:
        chrome = find_chrome()
    except ChromeNotFound as exc:
        _err(f"{exc} {NO_CHROME_MESSAGE}")
        return EXIT_NO_CHROME
    if chrome is None:
        _err(NO_CHROME_MESSAGE)
        return EXIT_NO_CHROME
    pdf = report_dir / "report.pdf"
    try:
        ensure_writable_dir(report_dir)
        print_pdf(html, pdf, chrome)
        shutil.copyfile(pdf, report_dir / named)
    except ChromeNotFound:
        _err(NO_CHROME_MESSAGE)
        return EXIT_NO_CHROME
    except (PdfError, OSError, RuntimeError) as exc:
        _err(f"PDF nicht erzeugt: {exc}")
        return EXIT_PDF
    print((report_dir / named).resolve())
    return EXIT_OK


# ---------------------------------------------------------------- entry

USAGE_ERRORS = (
    ("the following arguments are required", "Pflichtangabe fehlt"),
    ("unrecognized arguments", "Unbekannte Angabe"),
    ("invalid choice", "Unbekannter Befehl"),
    ("expected one argument", "Dem Schalter fehlt ein Wert"),
    ("ignored explicit argument", "Dem Schalter darf kein Wert folgen"),
    ("not allowed with argument", "Diese Angaben schließen sich aus"),
)
DEBUG_ENV = "LEGAL_AUDIT_DEBUG"
EXIT_INTERRUPTED = 130


class _GermanHelpFormatter(argparse.HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):  # type: ignore[no-untyped-def]
        return super()._format_usage(usage, actions, groups, "Aufruf: " if prefix is None else prefix)


class _GermanParser(argparse.ArgumentParser):
    """ArgumentParser with German headings and errors that exit with 1 (2 means broken install)."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        kwargs.setdefault("formatter_class", _GermanHelpFormatter)
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)
        self._positionals.title = "Angaben"
        self._optionals.title = "Optionen"
        self.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")

    def error(self, message: str) -> None:  # type: ignore[override]
        detail = next((f"{de}: {message.split(':', 1)[-1].strip()}" for key, de in USAGE_ERRORS
                       if key in message), "Ungültiger Aufruf")
        self.print_usage(sys.stderr)
        self.exit(EXIT_INPUT, f"{self.prog}: {detail}. Hilfe mit --help.\n")


def _parser() -> argparse.ArgumentParser:
    parser = _GermanParser(prog="client-test.py", description="Website-CheckUp")
    sub = parser.add_subparsers(dest="command", required=True, title="Befehle", metavar="BEFEHL")
    sub.add_parser("check", help="Installation prüfen").set_defaults(func=cmd_check)
    profile = sub.add_parser("profile", help="Briefkopf-Profil")
    psub = profile.add_subparsers(dest="profile_command", required=True, title="Befehle", metavar="BEFEHL")
    show = psub.add_parser("show", help="Gespeichertes Profil anzeigen")
    show.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    show.set_defaults(func=cmd_profile_show)
    save = psub.add_parser("save", help="Profil und Logo speichern")
    save.add_argument("--data", required=True, help="JSON-Datei mit den Absenderdaten")
    save.add_argument("--logo", required=True, help="Logo als PNG, JPG oder SVG")
    save.add_argument("--accent", help="Akzentfarbe als Hex-Wert (#1F4E79) oder default")
    save.set_defaults(func=cmd_profile_save)
    init = sub.add_parser("init", help="Report-Ordner anlegen")
    init.add_argument("url", help="Adresse der geprüften Website")
    init.add_argument("--out", help="Basisordner für Reports (Standard: client-reports)")
    init.add_argument("--date", help="Prüfdatum als JJJJ-MM-TT (Standard: heute)")
    init.set_defaults(func=cmd_init)
    for name, func, text in (("plan", cmd_plan, "Prüfplan festlegen"), ("render", cmd_render, "report.html erzeugen"),
                             ("pdf", cmd_pdf, "report.pdf erzeugen")):
        sp = sub.add_parser(name, help=text)
        sp.add_argument("folder", help="Report-Ordner")
        sp.set_defaults(func=func)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        args = _parser().parse_args(argv)
        return args.func(args)
    except KeyboardInterrupt:
        _err("Abgebrochen.")
        return EXIT_INTERRUPTED
    except Exception as exc:  # last resort: a German message instead of a traceback with local paths
        if os.environ.get(DEBUG_ENV):
            traceback.print_exc()
        _err(f"Unerwarteter Fehler: {type(exc).__name__}. Bitte Ausgabe melden.")
        return EXIT_INPUT
