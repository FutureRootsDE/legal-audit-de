#!/usr/bin/env python3
"""
legal-audit-de Pro-Mode Toggle.

Subcommands:
  enable         Aktiviert Pro-Mode (schreibt Marker-Datei)
  disable        Deaktiviert Pro-Mode (loescht Marker-Datei)
  status         Zeigt aktuellen Status (menschenlesbar)
  status --json  Gibt JSON-Bericht aus

Marker-Speicherorte (in Prioritaetsreihenfolge):
  1. ${CLAUDE_PLUGIN_DATA}/pro-mode.json  (offizieller persistenter Plugin-Speicher)
  2. ~/.claude/legal-audit-de-pro-mode.json  (Fallback)

Exit-Codes:
  0  OK
  1  Fehler (Schreibfehler, ungueltige Argumente)
  2  Inkonsistenter Marker-Zustand (fuer Monitoring-Pipelines)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PRO_MODE_FILENAME = "pro-mode.json"
FALLBACK_FILENAME = "legal-audit-de-pro-mode.json"
SCHEMA_VERSION = "1.2.0"


# ---------------------------------------------------------------------------
# Marker-Pfad-Aufloesung
# ---------------------------------------------------------------------------

def resolve_marker_paths() -> list[Path]:
    """Gibt alle moeglichen Marker-Pfade in Prioritaetsreihenfolge zurueck."""
    candidates: list[Path] = []
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if plugin_data:
        candidates.append(Path(plugin_data) / PRO_MODE_FILENAME)
    candidates.append(Path.home() / ".claude" / FALLBACK_FILENAME)
    return candidates


def primary_write_path() -> Path:
    """
    Gibt den bevorzugten Schreibpfad zurueck.
    Bevorzugt ${CLAUDE_PLUGIN_DATA} wenn gesetzt, sonst ~/.claude/Fallback.
    """
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if plugin_data:
        return Path(plugin_data) / PRO_MODE_FILENAME
    return Path.home() / ".claude" / FALLBACK_FILENAME


# ---------------------------------------------------------------------------
# Atomares Schreiben
# ---------------------------------------------------------------------------

def atomic_write_json(path: Path, payload: dict) -> None:
    """
    Schreibt payload als JSON atomar (tempfile + os.replace).
    Erstellt uebergeordnete Verzeichnisse automatisch.
    Setzt Berechtigungen 0o600 (nur Eigentuemerlesbar).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, prefix=".tmp-pro-mode-", suffix=".json"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.chmod(tmp_path, 0o600)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Marker lesen
# ---------------------------------------------------------------------------

def load_marker() -> dict | None:
    """
    Sucht in allen Marker-Pfaden und gibt den ersten gueltigen zurueck.
    Gibt None zurueck wenn kein aktiver Marker gefunden wird.
    """
    for path in resolve_marker_paths():
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("enabled") is True:
            data.setdefault("_marker_path", str(path))
            return data
    return None


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_enable(args: argparse.Namespace) -> int:
    write_path = primary_write_path()
    payload = {
        "enabled": True,
        "version": SCHEMA_VERSION,
        "set_at": datetime.now(timezone.utc).isoformat(),
        "set_by": f"legal-audit-pro-mode.py enable (PID {os.getpid()})",
    }
    try:
        atomic_write_json(write_path, payload)
    except Exception as exc:
        print(f"[FEHLER] Marker konnte nicht geschrieben werden: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Pro-Mode AKTIVIERT.")
    print(f"     Marker: {write_path}")
    print()
    print("     Agenten-Routing:")
    print("       legal-auditor     -> legal-auditor-pro     (claude-opus-4-7)")
    print("       legal-researcher  -> legal-researcher-pro  (claude-opus-4-7)")
    print("       legal-text-writer -> legal-text-writer-pro (claude-opus-4-7)")
    print()
    print("     Hinweis: Grosse Codebases (>150 KB) koennen den Kontext")
    print("     ueberschreiten. In v1.4 wird --chunked-Modus ergaenzt.")
    return 0


def cmd_disable(args: argparse.Namespace) -> int:
    removed: list[str] = []
    errors: list[str] = []

    for path in resolve_marker_paths():
        if not path.is_file():
            continue
        try:
            path.unlink()
            removed.append(str(path))
        except OSError as exc:
            errors.append(f"{path}: {exc}")

    if errors:
        for e in errors:
            print(f"[WARNUNG] Konnte nicht loeschen: {e}", file=sys.stderr)

    if removed:
        print("[OK] Pro-Mode DEAKTIVIERT.")
        for r in removed:
            print(f"     Marker geloescht: {r}")
    else:
        print("[INFO] Pro-Mode war nicht aktiv (kein Marker gefunden).")

    return 1 if errors else 0


def cmd_status(args: argparse.Namespace) -> int:
    marker = load_marker()
    enabled = marker is not None

    # Check for consistency: multiple markers?
    existing_paths = [p for p in resolve_marker_paths() if p.is_file()]
    inconsistent = len(existing_paths) > 1

    if args.json:
        out = {
            "enabled": enabled,
            "marker_path": marker.get("_marker_path") if marker else None,
            "set_at": marker.get("set_at") if marker else None,
            "version": marker.get("version") if marker else None,
            "inconsistent": inconsistent,
            "all_marker_paths": [str(p) for p in existing_paths],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 2 if inconsistent else 0

    # Human-readable
    status_str = "AKTIV" if enabled else "INAKTIV"
    print(f"Pro-Mode: {status_str}")
    if marker:
        print(f"  Marker: {marker.get('_marker_path', 'unbekannt')}")
        print(f"  Aktiviert am: {marker.get('set_at', 'unbekannt')}")
        print(f"  Schema-Version: {marker.get('version', 'unbekannt')}")
        print()
        print("  Aktives Agenten-Routing:")
        print("    legal-auditor     -> legal-auditor-pro")
        print("    legal-researcher  -> legal-researcher-pro")
        print("    legal-text-writer -> legal-text-writer-pro")
    else:
        print()
        print("  Agenten-Routing: Standard (Opus 4.7 [1M])")
        print("  Zum Aktivieren: python scripts/legal-audit-pro-mode.py enable")

    if inconsistent:
        print()
        print("[WARNUNG] Mehrere Marker-Dateien gefunden — Inkonsistenz:")
        for p in existing_paths:
            print(f"  {p}")
        print("  Empfehlung: 'disable' ausfuehren, dann 'enable'")

    return 2 if inconsistent else 0


# ---------------------------------------------------------------------------
# CLI-Einstieg
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="legal-audit-pro-mode.py",
        description="legal-audit-de Pro-Mode Toggle — steuert das Agenten-Routing.",
    )
    sub = parser.add_subparsers(dest="command", metavar="SUBCOMMAND")

    sub.add_parser("enable", help="Pro-Mode aktivieren")
    sub.add_parser("disable", help="Pro-Mode deaktivieren")

    status_p = sub.add_parser("status", help="Aktuellen Pro-Mode-Status anzeigen")
    status_p.add_argument(
        "--json", action="store_true", help="Maschinenlesbarer JSON-Output"
    )

    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "enable":
        return cmd_enable(args)
    elif args.command == "disable":
        return cmd_disable(args)
    elif args.command == "status":
        return cmd_status(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
