#!/usr/bin/env python3
"""
sync-pro-variants.py — Generiert Pro-Mode-Agenten-Varianten aus den Standard-Agenten.

Liest: .claude/agents/legal-{auditor,researcher,text-writer}.md
Schreibt: .claude/agents/legal-{auditor,researcher,text-writer}-pro.md

Transformationen:
  - Frontmatter: model  claude-opus-4-7[1m] -> claude-opus-4-7
  - Frontmatter: name   <name>              -> <name>-pro
  - Frontmatter: description  <text>        -> "[Pro-Mode] <text>"
  - Body: PRO_PROTOCOL_BLOCK wird vorne eingefuegt

Flags:
  --check   Prueft ob Varianten aktuell sind (exit 1 wenn Drift)
  --apply   Schreibt / aktualisiert alle Varianten (Standard wenn kein Flag)
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
AGENTS_DIR = ROOT / ".claude" / "agents"

# Mapping: source -> target
AGENT_PAIRS: list[tuple[str, str]] = [
    ("legal-auditor.md", "legal-auditor-pro.md"),
    ("legal-researcher.md", "legal-researcher-pro.md"),
    ("legal-text-writer.md", "legal-text-writer-pro.md"),
]

MODEL_1M = "claude-opus-4-7[1m]"
MODEL_PRO = "claude-opus-4-7"

# ---------------------------------------------------------------------------
# Pro-Mode-Protokoll-Block (wird an den Anfang jedes Pro-Agenten eingefuegt)
# ---------------------------------------------------------------------------

PRO_PROTOCOL_BLOCK = textwrap.dedent("""\
    ## Pro-Mode-Protokoll (Standard-Kontext ~200k)

    Du laeuft im **Pro-Mode** — Standard-Kontext statt 1M-Fenster.

    ### Kontext-Management-Regeln

    1. **Groessen-Check vor Scan:** Pruefe Codebase-Groesse mit `Bash du -sh <pfad>`.
       - ≤ 100 KB: Vollscan moeglich, kein besonderes Protokoll noetig.
       - 100-200 KB: Vollscan moeglich, aber komprimierte Ausgabe (keine vollstaendigen
         Code-Zitate in LegalAudit.md — nur Datei:Zeile-Referenzen).
       - > 200 KB: Scanne in Prioritaets-Phasen (CRIT/HIGH zuerst). Dokumentiere
         welche Teile gescannt wurden und welche ausgelassen. Vermerke in SUMMARY.md:
         "**Hinweis:** Codebase ueberschreitet optimale Pro-Mode-Groesse. Fuer vollstaendige
         Abdeckung: Standard-Mode empfohlen (max. Kontext)."

    2. **Komprimierte Zwischenergebnisse:** Halte keine langen Code-Bloecke im Kontext.
       Schreibe Findings sofort in LegalAudit.md, statt sie im Gedaechtnis zu halten.

    3. **Chunked-Modus (v1.4.0):** Fuer Codebases > 200 KB wird in v1.4 ein
       `--chunked`-Flag mit Logfile-Tracking eingefuehrt. Bis dahin: Priorisierung.

    ---

""")


# ---------------------------------------------------------------------------
# Frontmatter-Parser (minimalistisch, kein YAML-Parser benoetigt)
# ---------------------------------------------------------------------------

# CRLF-robust: matches both \n (Unix) and \r\n (Windows/autocrlf) line endings
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?\r?\n)---\r?\n(.*)", re.DOTALL)


def split_frontmatter(content: str) -> tuple[str, str]:
    """Gibt (frontmatter_raw, body) zurueck. frontmatter_raw ohne --- Delimiter."""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return "", content
    return m.group(1), m.group(2)


def replace_frontmatter_field(fm: str, key: str, new_value: str) -> str:
    """
    Ersetzt den ERSTEN Frontmatter-Schluessel mit neuem Wert (Zeile-fuer-Zeile).
    Nur die erste Zeile wird ersetzt — schuetzt vor doppelten Schluessel-Eintraegen
    die sonst zu dauerhaftem --check-Drift fuehren wuerden.
    """
    lines = fm.splitlines(keepends=True)
    result = []
    replaced = False
    for line in lines:
        if not replaced and line.startswith(f"{key}:"):
            result.append(f"{key}: {new_value}\n")
            replaced = True
        else:
            result.append(line)
    return "".join(result)


def get_frontmatter_field(fm: str, key: str) -> str | None:
    """Liest Wert eines Frontmatter-Schluessels."""
    for line in fm.splitlines():
        if line.startswith(f"{key}:"):
            return line[len(key) + 1:].strip()
    return None


# ---------------------------------------------------------------------------
# Pro-Variante rendern
# ---------------------------------------------------------------------------

def render_pro_variant(source_content: str) -> str:
    """Erstellt Pro-Mode-Variante aus Source-Content."""
    fm_raw, body = split_frontmatter(source_content)

    # Sicherstellen dass Model korrekt ist
    current_model = get_frontmatter_field(fm_raw, "model")
    if current_model != MODEL_1M:
        # Falls Source kein 1M-Modell hat, trotzdem auf Standard setzen
        if "model:" in fm_raw:
            fm_raw = replace_frontmatter_field(fm_raw, "model", MODEL_PRO)
        else:
            fm_raw += f"model: {MODEL_PRO}\n"
    else:
        fm_raw = replace_frontmatter_field(fm_raw, "model", MODEL_PRO)

    # Name: Suffix -pro hinzufuegen
    current_name = get_frontmatter_field(fm_raw, "name") or ""
    if not current_name.endswith("-pro"):
        fm_raw = replace_frontmatter_field(fm_raw, "name", f"{current_name}-pro")

    # Description: [Pro-Mode] Prefix
    current_desc = get_frontmatter_field(fm_raw, "description") or ""
    if not current_desc.startswith("[Pro-Mode]"):
        fm_raw = replace_frontmatter_field(
            fm_raw, "description", f"[Pro-Mode] {current_desc}"
        )

    # Body: Pro-Protokoll-Block vorne einfuegen
    if PRO_PROTOCOL_BLOCK not in body:
        body = PRO_PROTOCOL_BLOCK + body

    return f"---\n{fm_raw}---\n{body}"


# ---------------------------------------------------------------------------
# Check / Apply
# ---------------------------------------------------------------------------

def check_pair(source_path: Path, target_path: Path) -> bool:
    """
    Prueft ob target aktuell ist.
    Gibt True zurueck wenn OK, False wenn Drift.
    """
    if not source_path.is_file():
        print(f"[FEHLER] Source fehlt: {source_path}", file=sys.stderr)
        return False

    expected = render_pro_variant(source_path.read_text(encoding="utf-8"))

    if not target_path.is_file():
        print(f"[DRIFT] Target fehlt: {target_path}")
        return False

    actual = target_path.read_text(encoding="utf-8")
    if actual != expected:
        print(f"[DRIFT] Inhalt veraltet: {target_path}")
        return False

    print(f"[OK]    {target_path.name}")
    return True


def atomic_write_text(path: Path, content: str) -> None:
    """
    Schreibt content atomar via tempfile + os.replace.
    Verhindert korrupte Zieldateien bei Disk-Full oder PermissionError.
    Tempfile liegt immer im selben Verzeichnis wie Ziel (kein Cross-Device-Problem).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, prefix=".tmp-sync-pro-", suffix=".md"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def apply_pair(source_path: Path, target_path: Path) -> bool:
    """
    Schreibt/aktualisiert Pro-Variante atomar.
    Gibt True zurueck wenn OK.
    """
    if not source_path.is_file():
        print(f"[FEHLER] Source fehlt: {source_path}", file=sys.stderr)
        return False

    content = render_pro_variant(source_path.read_text(encoding="utf-8"))
    try:
        atomic_write_text(target_path, content)
    except Exception as exc:
        print(f"[FEHLER] Schreiben fehlgeschlagen ({target_path.name}): {exc}", file=sys.stderr)
        return False
    print(f"[WRITTEN] {target_path.name}")
    return True


def run_check() -> int:
    all_ok = True
    for src_name, tgt_name in AGENT_PAIRS:
        ok = check_pair(AGENTS_DIR / src_name, AGENTS_DIR / tgt_name)
        if not ok:
            all_ok = False
    if all_ok:
        print("\nAlle Pro-Varianten aktuell.")
        return 0
    else:
        print("\nDrift erkannt. Ausfuehren: python scripts/sync-pro-variants.py --apply")
        return 1


def run_apply() -> int:
    all_ok = True
    for src_name, tgt_name in AGENT_PAIRS:
        ok = apply_pair(AGENTS_DIR / src_name, AGENTS_DIR / tgt_name)
        if not ok:
            all_ok = False
    if all_ok:
        print("\nAlle Pro-Varianten generiert.")
        return 0
    return 1


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    mode = "--apply"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == "--check":
        return run_check()
    elif mode in ("--apply", ""):
        return run_apply()
    else:
        print(f"Unbekanntes Flag: {mode}. Verwende --check oder --apply.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
