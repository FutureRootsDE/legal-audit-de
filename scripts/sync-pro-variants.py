#!/usr/bin/env python3
"""
Generator fuer die Pro-Mode-Agent-Varianten.

Quelle:
  .claude/agents/legal-auditor.md
  .claude/agents/legal-researcher.md
  .claude/agents/legal-text-writer.md
  (alle mit `model: claude-opus-4-7[1m]`)

Ziel:
  .claude/agents/legal-auditor-pro.md
  .claude/agents/legal-researcher-pro.md
  .claude/agents/legal-text-writer-pro.md
  (alle mit `model: claude-opus-4-7`, plus Pro-Mode-Protokoll als Body-Praefix)

Der Generator pflegt damit den Prompt-Body an einer Stelle (1M-Variante);
die Pro-Variante ist deterministisch ableitbar.

Modi:
  --check   Pruefen, ob Pro-Varianten aktuell sind. Exit 1 bei Drift.
  --apply   Pro-Varianten schreiben/aktualisieren.
  --verbose Detail-Output

Ausfuehrung:
  python3 scripts/sync-pro-variants.py --check
  python3 scripts/sync-pro-variants.py --apply
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
AGENTS_DIR = ROOT / ".claude" / "agents"

SOURCE_NAMES = ["legal-auditor", "legal-researcher", "legal-text-writer"]

PRO_PROTOCOL_BLOCK = """<!-- AUTO-GENERATED from {source}. Do not edit manually. Re-run: python3 scripts/sync-pro-variants.py --apply -->

> **Pro-Mode-Protokoll (Standard-Kontext, ~200 K Tokens)**
>
> Du laeufst in der Pro-Variante des Agents, weil der User keinen Zugriff auf den
> 1M-Kontext hat (Claude-Pro-Abo statt Max/Team/Enterprise). Halte daher dein
> Kontextfenster aktiv schlank:
>
> - Lade **keine** kompletten Gesetzestexte vorsorglich. Nutze `knowledge/INDEX.md`
>   plus die Regex-Trigger aus `.claude/hooks/triggers.json`, um nur die KB-Chunks
>   zu ziehen, die fuer das konkrete Thema relevant sind.
> - Halte Code-Snippets aus der Audit-Codebase moeglichst kurz. Zitiere nur die
>   konkreten Zeilen, die ein Finding belegen.
> - Bei Codebases > ~150 KB Quellcode warne im Audit-Output:
>   `> Hinweis: Codebase ist gross — fuer Vollabdeckung empfohlen: /legal-audit --chunked (ab v1.4.0)`
> - Wenn ein Pass nicht in den Kontext passt, **brich nicht ab** — fasse die
>   Teil-Ergebnisse zusammen und lasse den Orchestrator entscheiden, ob ein
>   chunked Re-Run noetig ist.
>
> Das uebrige Audit-/Recherche-/Schreib-Protokoll ist identisch zur 1M-Variante.

---
"""


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("source file must start with '---' YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter terminator '---' not found")
    fm_block = text[4:end]
    body = text[end + 5 :]
    fm: dict = {}
    for line in fm_block.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm, body


def render_pro_variant(source_name: str, fm: dict, body: str) -> str:
    pro_fm = dict(fm)
    pro_fm["name"] = f"{source_name}-pro"
    pro_fm["model"] = "claude-opus-4-7"
    desc = pro_fm.get("description", "")
    if "[Pro-Mode]" not in desc:
        pro_fm["description"] = f"[Pro-Mode] {desc}".strip()
    fm_lines = ["---"]
    for key in ("name", "description", "tools", "model"):
        if key in pro_fm:
            fm_lines.append(f"{key}: {pro_fm[key]}")
    for key, value in pro_fm.items():
        if key in ("name", "description", "tools", "model"):
            continue
        fm_lines.append(f"{key}: {value}")
    fm_lines.append("---")
    protocol = PRO_PROTOCOL_BLOCK.format(source=f".claude/agents/{source_name}.md")
    return "\n".join(fm_lines) + "\n\n" + protocol + body.lstrip("\n")


def expected_pro_content(source_name: str) -> str:
    source = AGENTS_DIR / f"{source_name}.md"
    if not source.is_file():
        raise FileNotFoundError(f"missing source: {source}")
    text = source.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    return render_pro_variant(source_name, fm, body)


def cmd_check(verbose: bool) -> int:
    drift = []
    for name in SOURCE_NAMES:
        target = AGENTS_DIR / f"{name}-pro.md"
        try:
            expected = expected_pro_content(name)
        except Exception as exc:
            print(f"FEHLER: konnte Quelle fuer {name} nicht lesen: {exc}", file=sys.stderr)
            return 1
        if not target.is_file():
            drift.append((name, "missing"))
            continue
        actual = target.read_text(encoding="utf-8")
        if actual != expected:
            drift.append((name, "out-of-date"))
        elif verbose:
            print(f"  OK   {target.relative_to(ROOT)}")
    if drift:
        for name, reason in drift:
            print(f"DRIFT: {AGENTS_DIR / (name + '-pro.md')}: {reason}", file=sys.stderr)
        print("\nRun: python3 scripts/sync-pro-variants.py --apply", file=sys.stderr)
        return 1
    print(f"OK ({len(SOURCE_NAMES)} Pro-Varianten aktuell)")
    return 0


def cmd_apply(verbose: bool) -> int:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for name in SOURCE_NAMES:
        target = AGENTS_DIR / f"{name}-pro.md"
        expected = expected_pro_content(name)
        if target.is_file() and target.read_text(encoding="utf-8") == expected:
            if verbose:
                print(f"  SKIP  {target.relative_to(ROOT)} (unchanged)")
            continue
        target.write_text(expected, encoding="utf-8")
        written += 1
        print(f"  WROTE {target.relative_to(ROOT)}")
    print(f"Done ({written}/{len(SOURCE_NAMES)} Pro-Varianten aktualisiert)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Pruefen, exit 1 bei Drift")
    group.add_argument("--apply", action="store_true", help="Pro-Varianten schreiben")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.check:
        return cmd_check(args.verbose)
    return cmd_apply(args.verbose)


if __name__ == "__main__":
    sys.exit(main())
