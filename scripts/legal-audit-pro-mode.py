#!/usr/bin/env python3
"""
legal-audit-de Pro-Mode Toggle.

Schaltet die Plugin-Agents zwischen 1M-Kontext-Default (Max/Team/Enterprise)
und Standard-Kontext-Pro-Mode (Pro-Abo) um, ohne dabei Agent-Files zu
mutieren. Toggle setzt ausschliesslich einen Marker im user-scope
Persistenz-Verzeichnis der jeweiligen Plattform:

  Claude Code: ${CLAUDE_PLUGIN_DATA}/pro-mode.json
               (= ~/.claude/plugins/data/<plugin-id>/pro-mode.json)
               Fallback wenn CLAUDE_PLUGIN_DATA unset:
               ~/.claude/legal-audit-de-pro-mode.json
  Codex CLI:   ~/.codex/legal-audit-de-pro-mode.json
  Copilot CLI: ~/.copilot/legal-audit-de-pro-mode.json

Diese Pfade ueberleben Plugin-Updates (per offizieller Anthropic-Doku
fuer ${CLAUDE_PLUGIN_DATA} und per Konvention fuer ~/.codex/, ~/.copilot/).

Subcommands:
  enable    Marker an allen verfuegbaren Plattformen atomar setzen
  disable   Marker an allen Plattformen entfernen
  status    Aktuellen Marker-Status reportieren

Flags (status):
  --json    JSON-Output statt menschenlesbar

Exit codes:
  0  Erfolg, oder Status konsistent
  2  Status inkonsistent (Marker existiert auf einer Plattform, nicht auf anderer)
  1  Fehler (I/O, JSON-Parsing)
"""
import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MARKER_VERSION = "1.3.2"
MARKER_FILENAME = "pro-mode.json"
FALLBACK_FILENAME = "legal-audit-de-pro-mode.json"


def claude_marker_path() -> Path:
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if plugin_data:
        return Path(plugin_data) / MARKER_FILENAME
    return Path.home() / ".claude" / FALLBACK_FILENAME


def codex_marker_path() -> Path:
    codex_home = os.environ.get("CODEX_HOME") or (Path.home() / ".codex")
    return Path(codex_home) / FALLBACK_FILENAME


def copilot_marker_path() -> Path:
    copilot_home = os.environ.get("COPILOT_HOME") or (Path.home() / ".copilot")
    return Path(copilot_home) / FALLBACK_FILENAME


def platform_paths() -> dict[str, Path]:
    return {
        "claude": claude_marker_path(),
        "codex": codex_marker_path(),
        "copilot": copilot_marker_path(),
    }


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def read_marker(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"_corrupt": True, "path": str(path)}
    if not isinstance(data, dict):
        return {"_corrupt": True, "path": str(path)}
    return data


def detect_platforms() -> list[str]:
    """Return platforms whose home directory already exists; toggle writes only there."""
    available = []
    for name, path in platform_paths().items():
        parent_root = path.parent
        # Climb to the platform root (~/.claude, ~/.codex, ~/.copilot or the CLAUDE_PLUGIN_DATA root)
        if name == "claude":
            root = Path(os.environ.get("CLAUDE_PLUGIN_DATA")) if os.environ.get("CLAUDE_PLUGIN_DATA") else Path.home() / ".claude"
        elif name == "codex":
            root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
        else:
            root = Path(os.environ.get("COPILOT_HOME") or Path.home() / ".copilot")
        if root.exists() or parent_root.exists():
            available.append(name)
    return available


def cmd_enable(args) -> int:
    payload = {
        "enabled": True,
        "version": MARKER_VERSION,
        "set_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "set_by": "scripts/legal-audit-pro-mode.py",
    }
    paths = platform_paths()
    detected = detect_platforms()
    if not detected:
        # No platform home detected → still write the Claude fallback so the user has something to disable later.
        detected = ["claude"]
    written: list[str] = []
    errors: list[tuple[str, str]] = []
    for name in detected:
        target = paths[name]
        try:
            atomic_write_json(target, payload)
            written.append(name)
        except OSError as exc:
            errors.append((name, str(exc)))
    if errors:
        for name, msg in errors:
            print(f"FEHLER: {name} marker write failed: {msg}", file=sys.stderr)
    print("Pro-Mode AKTIVIERT.")
    for name in written:
        print(f"  {name}: {paths[name]}")
    if errors:
        return 1
    print("\nHinweis: starte deine CLI-Session neu, damit der SessionStart-Hook")
    print("den Marker liest und kuenftige Dispatches auf die -pro-Varianten umlenkt.")
    return 0


def cmd_disable(args) -> int:
    paths = platform_paths()
    removed: list[str] = []
    missing: list[str] = []
    errors: list[tuple[str, str]] = []
    for name, target in paths.items():
        if target.is_file():
            try:
                target.unlink()
                removed.append(name)
            except OSError as exc:
                errors.append((name, str(exc)))
        else:
            missing.append(name)
    if errors:
        for name, msg in errors:
            print(f"FEHLER: {name} marker delete failed: {msg}", file=sys.stderr)
        return 1
    if not removed:
        print("Pro-Mode war bereits deaktiviert (kein Marker gefunden).")
        return 0
    print("Pro-Mode DEAKTIVIERT.")
    for name in removed:
        print(f"  {name}: {paths[name]} entfernt")
    return 0


def build_status_report() -> tuple[dict, int]:
    paths = platform_paths()
    per_platform: dict[str, dict] = {}
    enabled_states: list[bool] = []
    for name, target in paths.items():
        marker = read_marker(target)
        if marker is None:
            per_platform[name] = {"present": False, "path": str(target)}
        elif marker.get("_corrupt"):
            per_platform[name] = {
                "present": True,
                "path": str(target),
                "corrupt": True,
            }
            enabled_states.append(False)
        else:
            per_platform[name] = {
                "present": True,
                "path": str(target),
                "enabled": bool(marker.get("enabled")),
                "version": marker.get("version"),
                "set_at": marker.get("set_at"),
            }
            enabled_states.append(bool(marker.get("enabled")))

    detected = detect_platforms()
    relevant_states = [
        per_platform[name].get("enabled", False)
        for name in detected
        if per_platform[name].get("present")
    ]
    if not relevant_states:
        consistent = True
        any_enabled = False
    else:
        consistent = all(relevant_states) or not any(relevant_states)
        any_enabled = any(relevant_states)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "any_enabled": any_enabled,
        "consistent_across_platforms": consistent,
        "detected_platforms": detected,
        "platforms": per_platform,
    }
    exit_code = 0 if consistent else 2
    return report, exit_code


def cmd_status(args) -> int:
    report, exit_code = build_status_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return exit_code
    print("=== legal-audit-de Pro-Mode Status ===")
    print(f"Generiert: {report['generated_at']}")
    state = "AKTIV" if report["any_enabled"] else "deaktiviert"
    print(f"Gesamt:    {state}")
    print(f"Konsistent: {'ja' if report['consistent_across_platforms'] else 'NEIN (siehe unten)'}")
    print(f"Erkannte Plattform-Homes: {', '.join(report['detected_platforms']) or '(keine)'}")
    print()
    for name, info in report["platforms"].items():
        if not info.get("present"):
            print(f"  [{name}] kein Marker  ({info['path']})")
        elif info.get("corrupt"):
            print(f"  [{name}] KORRUPT       ({info['path']})")
        else:
            tag = "enabled" if info.get("enabled") else "disabled"
            ver = info.get("version") or "?"
            ts = info.get("set_at") or "?"
            print(f"  [{name}] {tag} v{ver} @ {ts}  ({info['path']})")
    if not report["consistent_across_platforms"]:
        print()
        print("WARNUNG: Marker zwischen Plattformen inkonsistent.")
        print("Empfehlung: 'enable' oder 'disable' erneut ausfuehren, um zu re-synchronisieren.")
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="legal-audit-pro-mode",
        description="Toggle Pro-Mode (Standard-Kontext statt 1M) fuer legal-audit-de.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("enable", help="Pro-Mode aktivieren (Marker setzen)")
    sub.add_parser("disable", help="Pro-Mode deaktivieren (Marker entfernen)")
    p_status = sub.add_parser("status", help="Marker-Status reportieren")
    p_status.add_argument("--json", action="store_true", help="JSON-Output")

    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.cmd == "enable":
        return cmd_enable(args)
    if args.cmd == "disable":
        return cmd_disable(args)
    if args.cmd == "status":
        return cmd_status(args)
    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
