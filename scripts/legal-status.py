#!/usr/bin/env python3
"""
legal-audit-de Status-Report.

Zeigt:
  - KB-Dateienzahl + Aktualitaets-Status (YAML-Frontmatter aktualisiert:)
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


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
KB = ROOT / "knowledge"
AUDITS = ROOT / "audits"
HOOKS = ROOT / ".claude" / "hooks"


def kb_categories() -> dict[str, list[Path]]:
    cats = {}
    for sub in ["gesetze", "themen", "urteile", "behoerden", "checklisten", "anwaelte-tools"]:
        d = KB / sub
        cats[sub] = sorted(d.glob("*.md")) if d.exists() else []
    index = KB / "INDEX.md"
    cats["_index"] = [index] if index.exists() else []
    return cats


AKTUALISIERT_RE = re.compile(r"^aktualisiert:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"<<\s*(VERIFIKATION\s+AUSSTEHEND|UNVERIFIZIERT)\s*>>", re.IGNORECASE)


def age_days(aktualisiert_str: str, today: date) -> int:
    try:
        d = datetime.strptime(aktualisiert_str, "%Y-%m-%d").date()
        return (today - d).days
    except Exception:
        return -1


def scan_file(path: Path, today: date) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {"path": str(path), "error": "read-fail"}

    aktual_match = AKTUALISIERT_RE.search(text)
    aktual = aktual_match.group(1) if aktual_match else None
    age = age_days(aktual, today) if aktual else -1
    placeholders = PLACEHOLDER_RE.findall(text)

    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "aktualisiert": aktual,
        "age_days": age,
        "placeholders": len(placeholders),
        "placeholder_types": {
            "verifikation_ausstehend": sum(1 for p in placeholders if "VERIFIKATION" in p.upper()),
            "unverifiziert": sum(1 for p in placeholders if "UNVERIFIZIERT" in p.upper()),
        },
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


def build_report(verbose: bool) -> dict:
    today = date.today()
    cats = kb_categories()
    files: list[dict] = []
    for sub_files in cats.values():
        for path in sub_files:
            files.append(scan_file(path, today))

    fresh = [f for f in files if 0 <= f.get("age_days", -1) < 90]
    stale = [f for f in files if 90 <= f.get("age_days", -1) < 180]
    very_stale = [f for f in files if f.get("age_days", -1) >= 180]
    no_frontmatter = [f for f in files if f.get("age_days") == -1]

    total_placeholders = sum(f.get("placeholders", 0) for f in files)
    files_with_placeholders = [f for f in files if f.get("placeholders", 0) > 0]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "project_dir": str(ROOT),
        "kb": {
            "total": sum(len(v) for v in cats.values()),
            "by_category": {k: len(v) for k, v in cats.items()},
            "aktualitaet": {
                "fresh_under_90d": len(fresh),
                "stale_90_to_180d": len(stale),
                "very_stale_over_180d": len(very_stale),
                "no_frontmatter": len(no_frontmatter),
            },
        },
        "placeholders": {
            "total": total_placeholders,
            "affected_files": len(files_with_placeholders),
            "by_type": {
                "verifikation_ausstehend": sum(
                    f["placeholder_types"]["verifikation_ausstehend"] for f in files
                ),
                "unverifiziert": sum(
                    f["placeholder_types"]["unverifiziert"] for f in files
                ),
            },
        },
        "audits": audit_history(),
        "hooks": hook_status(),
    }

    if verbose:
        report["kb"]["stale_files"] = [{"path": f["path"], "age_days": f["age_days"]} for f in stale + very_stale]
        report["placeholders"]["files"] = [
            {"path": f["path"], "count": f["placeholders"]} for f in files_with_placeholders
        ]
        report["kb"]["no_frontmatter_files"] = [f["path"] for f in no_frontmatter]

    return report


def render_text(report: dict) -> str:
    kb = report["kb"]
    ph = report["placeholders"]
    lines = [
        "=== legal-audit-de Status ===",
        f"Generiert: {report['generated_at']}",
        f"Pfad: {report['project_dir']}",
        "",
        "Knowledge Base:",
        f"  Gesamt: {kb['total']} Dateien",
        f"  Kategorien: " + ", ".join(f"{k}={v}" for k, v in kb['by_category'].items()),
        f"  Aktualitaet:",
        f"    - Aktuell (<90 Tage):     {kb['aktualitaet']['fresh_under_90d']}",
        f"    - Stale (90-180 Tage):    {kb['aktualitaet']['stale_90_to_180d']}",
        f"    - Sehr Stale (>180 Tage): {kb['aktualitaet']['very_stale_over_180d']}",
        f"    - Ohne Frontmatter:       {kb['aktualitaet']['no_frontmatter']}",
        "",
        "Platzhalter (zu recherchieren):",
        f"  VERIFIKATION AUSSTEHEND: {ph['by_type']['verifikation_ausstehend']}",
        f"  UNVERIFIZIERT:           {ph['by_type']['unverifiziert']}",
        f"  Gesamt:                  {ph['total']}",
        f"  Betroffene Dateien:      {ph['affected_files']}",
    ]
    if ph["total"] > 0:
        lines.append(f"  Empfehlung: /legal-update --fix-pending")

    lines.extend(["", "Audit-Historie:"])
    if not report["audits"]:
        lines.append("  Keine Audits durchgefuehrt (noch).")
    else:
        lines.append(f"  Gesamt: {len(report['audits'])} Audits")
        for a in report["audits"][-3:]:
            meta = a.get("meta") or {}
            ts = meta.get("audit_timestamp", "?")
            sev = meta.get("severity_count", {})
            sev_str = " ".join(f"{k}:{v}" for k, v in sev.items()) if sev else ""
            lines.append(f"  - {a['name']} @ {ts} {sev_str}")

    lines.extend(["", "Hook-Status:"])
    for hook, info in report["hooks"].items():
        if hook == "trigger_patterns":
            lines.append(f"  Trigger-Patterns: {info}")
        else:
            ok = "OK" if info["exists"] else "FEHLT"
            lines.append(f"  {hook}: {ok} ({info['script']})")

    lines.extend(["", "Empfohlene Aktionen:"])
    if ph["total"] > 10:
        lines.append("  - /legal-update --fix-pending  (Platzhalter aufloesen)")
    if kb["aktualitaet"]["stale_90_to_180d"] + kb["aktualitaet"]["very_stale_over_180d"] > 0:
        lines.append("  - /legal-update --stale-only   (veraltete KB-Dateien)")
    if not report["audits"]:
        lines.append("  - /legal-audit <pfad>  (ersten Audit durchfuehren)")

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
            if report["placeholders"].get("files"):
                print("\nDateien mit Platzhaltern:")
                for f in report["placeholders"]["files"]:
                    print(f"  {f['path']}: {f['count']} Platzhalter")
            if report["kb"].get("no_frontmatter_files"):
                print("\nDateien ohne aktualisiert:-Frontmatter:")
                for p in report["kb"]["no_frontmatter_files"]:
                    print(f"  {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
