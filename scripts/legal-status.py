#!/usr/bin/env python3
"""
legal-audit-de Status-Report.

Zeigt:
  - KB-Dateienzahl + Aktualitaets-Status (massgeblich ist verifiziert-am, ersatzweise aktualisiert;
    Dateien mit teilverifiziert-am gelten als eigener Zustand "teilverifiziert" und nie als frisch)
  - Dateien mit Frontmatter, aber ungueltigem oder zukuenftigem Datum: eigener Zustand "ungueltiges Datum"
  - Anzahl <<VERIFIKATION AUSSTEHEND>> / <<UNVERIFIZIERT>>-Platzhalter
  - Audit-Historie aus audits/
  - Hook-Konfigurations-Check

Flags:
  --verbose    detaillierte Listen pro Datei
  --json       nur JSON (fuer Skripte)
"""
import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from placeholder_check import EXACT_RE, find_deviant  # noqa: E402

STALE_DAYS = 90
VERY_STALE_DAYS = 180


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
KB = ROOT / "knowledge"
AUDITS = ROOT / "audits"
HOOKS = ROOT / ".claude" / "hooks"
AGENTS = ROOT / ".claude" / "agents"
PRO_MODE_FILENAME = "pro-mode.json"
FALLBACK_PRO_MODE_FILENAME = "legal-audit-de-pro-mode.json"


def kb_categories(kb: Path = KB) -> dict[str, list[Path]]:
    cats = {}
    for sub in ["gesetze", "themen", "urteile", "behoerden", "checklisten", "anwaelte-tools"]:
        d = kb / sub
        cats[sub] = sorted(d.glob("*.md")) if d.exists() else []
    index = kb / "INDEX.md"
    cats["_index"] = [index] if index.exists() else []
    return cats


FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
DATE_FIELD_RE = re.compile(r"^(aktualisiert|verifiziert-am|teilverifiziert-am):[ \t]*(.*?)[ \t]*$", re.MULTILINE)
PLACEHOLDER_RE = EXACT_RE


def parse_date(value: str) -> date | None:
    """ISO date of a frontmatter value; quotes around it are tolerated, anything else is not a date."""
    cleaned = re.sub(r"\s+#.*$", "", value).strip().strip("\"'")
    try:
        return datetime.strptime(cleaned, "%Y-%m-%d").date()
    except ValueError:
        return None


def age_days(aktualisiert_str: str, today: date) -> int:
    parsed = parse_date(aktualisiert_str)
    return (today - parsed).days if parsed else -1


def frontmatter_fields(text: str) -> dict[str, str]:
    """Date fields of the YAML frontmatter (empty dict without frontmatter); only the first block counts."""
    block = FRONTMATTER_RE.match(text)
    return {k: v for k, v in DATE_FIELD_RE.findall(block.group(1))} if block else {}


def usable_reference(fields: dict[str, str], today: date) -> date | None:
    """verifiziert-am if it is a valid, non-future date; else aktualisiert under the same conditions."""
    for key in ("verifiziert-am", "aktualisiert"):
        parsed = parse_date(fields.get(key, ""))
        if parsed is not None and parsed <= today:
            return parsed
    return None


def freshness_state(fields: dict[str, str], today: date) -> tuple[str, int]:
    """State and verification age: verifiziert-am decides, aktualisiert is the fallback.

    teilverifiziert-am marks a partly verified file: own state, never fresh. A frontmatter with date
    fields but without any usable (valid, not future) date is "invalid_date"; without date fields
    (or without frontmatter) it is "no_frontmatter".
    """
    reference = usable_reference(fields, today)
    age = (today - reference).days if reference else -1
    if "teilverifiziert-am" in fields:
        return "teilverifiziert", age
    if reference is None:
        return ("invalid_date" if fields else "no_frontmatter"), age
    if age < STALE_DAYS:
        return "fresh", age
    return ("stale" if age < VERY_STALE_DAYS else "very_stale"), age


def scan_file(path: Path, today: date, root: Path = ROOT) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {"path": str(path), "error": "read-fail", "state": "no_frontmatter"}

    fields = frontmatter_fields(text)
    aktual = fields.get("aktualisiert") or None
    state, verification_age = freshness_state(fields, today)
    placeholders = [m.group(1) for m in PLACEHOLDER_RE.finditer(text)]

    return {
        "path": str(path.relative_to(root)).replace("\\", "/"),
        "aktualisiert": aktual,
        "age_days": age_days(aktual, today) if aktual else -1,
        "verifiziert_am": fields.get("verifiziert-am") or None,
        "teilverifiziert_am": fields.get("teilverifiziert-am") or None,
        "verification_age_days": verification_age,
        "state": state,
        "placeholders": len(placeholders),
        "placeholder_types": {
            "verifikation_ausstehend": sum(1 for p in placeholders if "VERIFIKATION" in p.upper()),
            "unverifiziert": sum(1 for p in placeholders if "UNVERIFIZIERT" in p.upper()),
        },
        "deviant_placeholders": [d._asdict() for d in find_deviant(text)],
    }


def audit_history() -> list[dict]:
    if not AUDITS.exists():
        return []
    history = []
    for entry in sorted(AUDITS.iterdir()):
        if entry.is_dir():
            meta = entry / "META.json"
            info = {"name": entry.name, "path": str(entry.relative_to(ROOT)).replace("\\", "/")}
            if meta.exists():
                try:
                    info["meta"] = json.loads(meta.read_text(encoding="utf-8"))
                except Exception:
                    info["meta"] = None
            history.append(info)
    return history


def hook_status() -> dict:
    status = {}
    for hook_name, script in [
        ("SessionStart", "session_start.py"),
        ("UserPromptSubmit", "prompt_submit.py"),
        ("PostToolUse", "post_write.py"),
    ]:
        p = HOOKS / script
        status[hook_name] = {
            "script": script,
            "exists": p.exists(),
            "size": p.stat().st_size if p.exists() else 0,
        }
    triggers = HOOKS / "triggers.json"
    if triggers.exists():
        try:
            cfg = json.loads(triggers.read_text(encoding="utf-8"))
            status["trigger_patterns"] = len(cfg.get("triggers", []))
        except Exception:
            status["trigger_patterns"] = -1
    return status


def pro_mode_status() -> dict:
    candidates: list[tuple[str, Path]] = []
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if plugin_data:
        candidates.append(("claude_plugin_data", Path(plugin_data) / PRO_MODE_FILENAME))
    candidates.append(("claude_fallback", Path.home() / ".claude" / FALLBACK_PRO_MODE_FILENAME))
    codex_home = os.environ.get("CODEX_HOME") or (Path.home() / ".codex")
    candidates.append(("codex", Path(codex_home) / FALLBACK_PRO_MODE_FILENAME))
    copilot_home = os.environ.get("COPILOT_HOME") or (Path.home() / ".copilot")
    candidates.append(("copilot", Path(copilot_home) / FALLBACK_PRO_MODE_FILENAME))

    enabled = False
    marker: dict | None = None
    marker_path: str | None = None
    for _label, path in candidates:
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("enabled") is True:
            enabled = True
            marker = data
            marker_path = str(path)
            break

    pro_variants_expected = ["legal-auditor-pro", "legal-researcher-pro", "legal-text-writer-pro"]
    pro_variants_present = [
        name for name in pro_variants_expected if (AGENTS / f"{name}.md").is_file()
    ]

    return {
        "enabled": enabled,
        "marker_path": marker_path,
        "set_at": (marker or {}).get("set_at"),
        "version": (marker or {}).get("version"),
        "variants_expected": pro_variants_expected,
        "variants_present": pro_variants_present,
        "variants_complete": pro_variants_present == pro_variants_expected,
    }


def _scan_all(cats: dict[str, list[Path]], today: date, root: Path) -> list[dict]:
    return [scan_file(path, today, root) for sub_files in cats.values() for path in sub_files]


def _in_state(files: list[dict], name: str) -> list[dict]:
    return [f for f in files if f.get("state") == name]


def _kb_section(cats: dict[str, list[Path]], files: list[dict]) -> dict:
    return {
        "total": sum(len(v) for v in cats.values()),
        "by_category": {k: len(v) for k, v in cats.items()},
        "aktualitaet": {
            "fresh_under_90d": len(_in_state(files, "fresh")),
            "stale_90_to_180d": len(_in_state(files, "stale")),
            "very_stale_over_180d": len(_in_state(files, "very_stale")),
            "no_frontmatter": len(_in_state(files, "no_frontmatter")),
            "teilverifiziert": len(_in_state(files, "teilverifiziert")),
            "invalid_date": len(_in_state(files, "invalid_date")),
            "basis": "verifiziert-am (ersatzweise aktualisiert); teilverifiziert-am zaehlt nie als frisch",
        },
    }


def _placeholder_section(files: list[dict]) -> dict:
    with_deviant = [f for f in files if f.get("deviant_placeholders")]
    return {
        "deviant": {
            "total": sum(len(f["deviant_placeholders"]) for f in with_deviant),
            "affected_files": len(with_deviant),
        },
        "total": sum(f.get("placeholders", 0) for f in files),
        "affected_files": len([f for f in files if f.get("placeholders", 0) > 0]),
        "by_type": {
            "verifikation_ausstehend": sum(f["placeholder_types"]["verifikation_ausstehend"] for f in files),
            "unverifiziert": sum(f["placeholder_types"]["unverifiziert"] for f in files),
        },
    }


def _add_verbose(report: dict, files: list[dict]) -> None:
    stale = _in_state(files, "stale") + _in_state(files, "very_stale")
    with_deviant = [f for f in files if f.get("deviant_placeholders")]
    report["kb"]["stale_files"] = [{"path": f["path"], "age_days": f["verification_age_days"]} for f in stale]
    report["kb"]["teilverifiziert_files"] = [
        {"path": f["path"], "teilverifiziert_am": f["teilverifiziert_am"]} for f in _in_state(files, "teilverifiziert")]
    report["placeholders"]["deviant_files"] = [
        {"path": f["path"], "findings": f["deviant_placeholders"]} for f in with_deviant]
    report["placeholders"]["files"] = [
        {"path": f["path"], "count": f["placeholders"]} for f in files if f.get("placeholders", 0) > 0]
    report["kb"]["no_frontmatter_files"] = [f["path"] for f in _in_state(files, "no_frontmatter")]
    report["kb"]["invalid_date_files"] = [
        {"path": f["path"], "verifiziert_am": f["verifiziert_am"], "aktualisiert": f["aktualisiert"]}
        for f in _in_state(files, "invalid_date")]


def build_report(verbose: bool, today: date | None = None, root: Path = ROOT) -> dict:
    today = today or date.today()
    cats = kb_categories(root / "knowledge")
    files = _scan_all(cats, today, root)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "project_dir": str(ROOT),
        "kb": _kb_section(cats, files),
        "placeholders": _placeholder_section(files),
        "audits": audit_history(),
        "hooks": hook_status(),
        "pro_mode": pro_mode_status(),
    }
    if verbose:
        _add_verbose(report, files)
    return report


def _kb_lines(kb: dict) -> list[str]:
    lines = [
        "Knowledge Base:",
        f"  Gesamt: {kb['total']} Dateien",
        f"  Kategorien: " + ", ".join(f"{k}={v}" for k, v in kb['by_category'].items()),
        f"  Aktualitaet:",
        "    (Alter der Verifikation: verifiziert-am, ersatzweise aktualisiert)",
        f"    - Aktuell (<90 Tage):     {kb['aktualitaet']['fresh_under_90d']}",
        f"    - Stale (90-180 Tage):    {kb['aktualitaet']['stale_90_to_180d']}",
        f"    - Sehr Stale (>180 Tage): {kb['aktualitaet']['very_stale_over_180d']}",
        f"    - Teilverifiziert:        {kb['aktualitaet']['teilverifiziert']}",
        f"    - Ohne Frontmatter:       {kb['aktualitaet']['no_frontmatter']}",
    ]
    if kb["aktualitaet"].get("invalid_date", 0):
        lines.append(f"    - Ungueltiges Datum:      {kb['aktualitaet']['invalid_date']}")
    return lines


def _placeholder_lines(ph: dict) -> list[str]:
    lines = [
        "Platzhalter (zu recherchieren):",
        f"  VERIFIKATION AUSSTEHEND: {ph['by_type']['verifikation_ausstehend']}",
        f"  UNVERIFIZIERT:           {ph['by_type']['unverifiziert']}",
        f"  Gesamt:                  {ph['total']}",
        f"  Betroffene Dateien:      {ph['affected_files']}",
    ]
    if ph["deviant"]["total"] > 0:
        lines.append(f"  WARNUNG: {ph['deviant']['total']} abweichende Platzhalter-Formen in "
                     f"{ph['deviant']['affected_files']} Dateien (python scripts/find-placeholders.py zeigt sie)")
    if ph["total"] > 0:
        lines.append(f"  Empfehlung: /legal-update --fix-pending")
    return lines


def _audit_lines(audits: list[dict]) -> list[str]:
    lines = ["", "Audit-Historie:"]
    if not audits:
        return lines + ["  Keine Audits durchgefuehrt (noch)."]
    lines.append(f"  Gesamt: {len(audits)} Audits")
    for a in audits[-3:]:
        meta = a.get("meta") or {}
        ts = meta.get("audit_timestamp", "?")
        sev = meta.get("severity_count", {})
        sev_str = " ".join(f"{k}:{v}" for k, v in sev.items()) if sev else ""
        lines.append(f"  - {a['name']} @ {ts} {sev_str}")
    return lines


def _hook_lines(hooks: dict) -> list[str]:
    lines = ["", "Hook-Status:"]
    for hook, info in hooks.items():
        if hook == "trigger_patterns":
            lines.append(f"  Trigger-Patterns: {info}")
        else:
            ok = "OK" if info["exists"] else "FEHLT"
            lines.append(f"  {hook}: {ok} ({info['script']})")
    return lines


def _pro_mode_lines(pm: dict) -> list[str]:
    lines = ["", "Pro-Mode:", f"  Status:           {'AKTIV' if pm['enabled'] else 'deaktiviert'}"]
    if pm["enabled"]:
        lines.append(f"  Marker:           {pm['marker_path']}")
        lines.append(f"  Gesetzt:          {pm.get('set_at') or '?'}")
    variants = f"{len(pm['variants_present'])}/{len(pm['variants_expected'])}"
    lines.append(f"  Agent-Varianten:  {variants} ({'OK' if pm['variants_complete'] else 'INKOMPLETT'})")
    if not pm["variants_complete"]:
        missing = [n for n in pm["variants_expected"] if n not in pm["variants_present"]]
        lines.append(f"    fehlt: {', '.join(missing)} — Run: python3 scripts/sync-pro-variants.py --apply")
    return lines


def _action_lines(report: dict) -> list[str]:
    kb, ph = report["kb"], report["placeholders"]
    lines = ["", "Empfohlene Aktionen:"]
    if ph["total"] > 10:
        lines.append("  - /legal-update --fix-pending  (Platzhalter aufloesen)")
    if kb["aktualitaet"]["stale_90_to_180d"] + kb["aktualitaet"]["very_stale_over_180d"] > 0:
        lines.append("  - /legal-update --stale-only   (veraltete KB-Dateien)")
    if kb["aktualitaet"]["teilverifiziert"] > 0:
        lines.append("  - /legal-update <slug>         (teilverifizierte Dateien vollstaendig verifizieren)")
    if kb["aktualitaet"].get("invalid_date", 0):
        lines.append("  - Datum im Frontmatter korrigieren  (ungueltig oder in der Zukunft, siehe --verbose)")
    if not report["audits"]:
        lines.append("  - /legal-audit <pfad>  (ersten Audit durchfuehren)")
    return lines


def render_text(report: dict) -> str:
    lines = ["=== legal-audit-de Status ===", f"Generiert: {report['generated_at']}",
             f"Pfad: {report['project_dir']}", ""]
    lines += _kb_lines(report["kb"]) + [""] + _placeholder_lines(report["placeholders"])
    lines += _audit_lines(report["audits"]) + _hook_lines(report["hooks"])
    lines += _pro_mode_lines(report["pro_mode"]) + _action_lines(report)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Detaillierte Listen pro Datei")
    parser.add_argument("--json", action="store_true", help="Nur JSON-Output")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    report = build_report(verbose=args.verbose)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
        if args.verbose:
            print("\n--- Verbose-Details ---")
            if report["kb"].get("stale_files"):
                print("\nStale-Dateien:")
                for f in report["kb"]["stale_files"]:
                    print(f"  {f['path']} ({f['age_days']} Tage alt)")
            if report["kb"].get("teilverifiziert_files"):
                print("\nTeilverifizierte Dateien:")
                for f in report["kb"]["teilverifiziert_files"]:
                    print(f"  {f['path']} (teilverifiziert-am {f['teilverifiziert_am']})")
            for f in report["placeholders"].get("deviant_files", []):
                for d in f["findings"]:
                    print(f"  WARNUNG {f['path']}:{d['line']}: {d['reason']}: {d['snippet']}")
            if report["placeholders"].get("files"):
                print("\nDateien mit Platzhaltern:")
                for f in report["placeholders"]["files"]:
                    print(f"  {f['path']}: {f['count']} Platzhalter")
            if report["kb"].get("invalid_date_files"):
                print("\nDateien mit ungueltigem Datum im Frontmatter:")
                for f in report["kb"]["invalid_date_files"]:
                    print(f"  {f['path']} (verifiziert-am {f['verifiziert_am']}, aktualisiert {f['aktualisiert']})")
            if report["kb"].get("no_frontmatter_files"):
                print("\nDateien ohne aktualisiert:-Frontmatter:")
                for p in report["kb"]["no_frontmatter_files"]:
                    print(f"  {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
