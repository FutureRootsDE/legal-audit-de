#!/usr/bin/env python3
"""
UserPromptSubmit-Hook fuer legal-audit-de (Python-Implementierung).

Input:   JSON auf stdin mit Feld .prompt (vom Claude-Code-Hook-Runtime)
Output:  JSON auf stdout mit hookSpecificOutput.additionalContext
Verhalten:
  - Liest knowledge/.claude/hooks/triggers.json
  - Matcht jeden Regex (case-insensitive via (?i) in patterns) gegen den Prompt
  - Sammelt deduplizierte Datei-Pfade unter knowledge/
  - Liest die Dateien, baut einen additionalContext-Block mit klaren Separatoren
  - Bei keinem Match: still exit 0 (kein Context-Inject)
"""
import json
import os
import re
import sys


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    triggers_path = os.path.join(project_dir, ".claude", "hooks", "triggers.json")
    kb_dir = os.path.join(project_dir, "knowledge")

    if not os.path.isfile(triggers_path):
        return 0

    # Read prompt from stdin (JSON).
    prompt = ""
    try:
        raw = sys.stdin.read()
        if raw.strip():
            data = json.loads(raw)
            prompt = data.get("prompt", "") or ""
    except Exception:
        # No valid stdin — nothing to do.
        return 0

    if not prompt:
        return 0

    try:
        with open(triggers_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        return 0

    matched_files: list[str] = []
    seen: set[str] = set()

    for trigger in cfg.get("triggers", []):
        pattern = trigger.get("pattern", "")
        if not pattern:
            continue
        try:
            if re.search(pattern, prompt):
                for rel in trigger.get("files", []):
                    if rel not in seen:
                        seen.add(rel)
                        matched_files.append(rel)
        except re.error:
            continue

    if not matched_files:
        return 0

    blocks: list[str] = []
    for rel in matched_files:
        full = os.path.join(kb_dir, rel.replace("/", os.sep))
        if not os.path.isfile(full):
            slug = os.path.splitext(os.path.basename(rel))[0]
            blocks.append(
                f"### {rel}\n\n"
                f"> [Hinweis] Datei noch nicht befuellt. "
                f"`/legal-update {slug}` triggert Recherche.\n"
            )
            continue
        try:
            with open(full, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"> [Lese-Fehler] {e}"
        blocks.append(f"### {rel}\n\n{content}\n")

    header = (
        "# legal-audit-de — Relevante Rechts-KB-Chunks (via UserPromptSubmit-Hook)\n\n"
        f"Der Hook erkannte Schlagwoerter in deiner Nachricht und hat folgende "
        f"{len(matched_files)} KB-Datei(en) geladen. Nutze sie als Primaer-Referenz; "
        "wenn Luecken bestehen, ruf `/legal-update <thema>` auf.\n\n---\n\n"
    )

    additional = header + "\n\n---\n\n".join(blocks)

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional,
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
