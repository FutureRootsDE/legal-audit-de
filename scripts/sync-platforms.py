#!/usr/bin/env python3
"""
sync-platforms.py — Generator fuer Multi-Platform-Adapter.

Source of Truth: .claude/
Targets:
  - .codex/        (OpenAI Codex CLI)
  - .github/       (GitHub Copilot CLI: prompts/, agents/, skills/)

Modes:
  --check     Diff only, exit 1 wenn out-of-sync (CI).
  --apply     Schreibt/ueberschreibt Targets aus Source.
  --verbose   Listet jede Datei.

Tool-Mapping ist Konvention. Bei API-Aenderungen: TOOL_MAP_* anpassen.

Disclaimer: Outputs sind keine Rechtsberatung im Sinne von Paragraph 2 RDG.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / ".claude"
CODEX_DIR = REPO_ROOT / ".codex"
CODEX_PLUGIN_DIR = REPO_ROOT / ".codex-plugin"
CODEX_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
COPILOT_DIR = REPO_ROOT / ".github"

# --- Tool-Mappings ---
# Claude Code Tool -> Codex CLI Tool (Konvention; bei API-Drift hier anpassen)
TOOL_MAP_CODEX: Dict[str, str] = {
    "Read": "file.read",
    "Write": "file.write",
    "Edit": "file.edit",
    "Bash": "shell.exec",
    "Grep": "search.grep",
    "Glob": "file.glob",
    "Task": "spawn_agent",
    "WebFetch": "http.get",
    "WebSearch": "http.get",  # WebSearch fehlt -> Fallback http.get
    "TodoWrite": "update_plan",
}

# Claude Code Tool -> GitHub Copilot CLI Tool
TOOL_MAP_COPILOT: Dict[str, str] = {
    "Read": "view",
    "Write": "create",
    "Edit": "edit",
    "Bash": "bash",
    "Grep": "grep",
    "Glob": "glob",
    "Task": "task",
    "WebFetch": "web_fetch",
    "WebSearch": "web_fetch",  # WebSearch fehlt -> Fallback web_fetch
    "TodoWrite": "sql",
}

# Pfad-Variablen-Mapping
PATH_VARS_CODEX: Dict[str, str] = {
    "${CLAUDE_PROJECT_DIR}": "${CODEX_PROJECT_DIR}",
    "${CLAUDE_PLUGIN_ROOT}": "${CODEX_PLUGIN_ROOT}",
}
PATH_VARS_COPILOT: Dict[str, str] = {
    "${CLAUDE_PROJECT_DIR}": "${GITHUB_WORKSPACE}",
    "${CLAUDE_PLUGIN_ROOT}": "${GITHUB_WORKSPACE}",
}

# Auto-Routing-Block, der in Skills (Codex/Copilot) injiziert wird,
# weil dort keine SessionStart/UserPromptSubmit-Hooks existieren.
AUTO_ROUTING_BLOCK_DE = """
## Auto-Routing (Plattform-Fallback fuer Hookless-CLIs)

Diese Plattform (Codex/Copilot) hat keine SessionStart-/UserPromptSubmit-Hooks. Das Skill uebernimmt das KB-Routing daher selbst:

1. **Lies `knowledge/INDEX.md`** zu Beginn jeder Session, falls noch nicht geladen.
2. **Matche Task-Schlagwoerter** (cookie, drittland, ai-act, newsletter, barrierefreiheit, ...) gegen die KB-Kategorien aus dem INDEX.
3. **Lies bis zu 3 passende Chunks** via Read/view aus `knowledge/themen/`, `knowledge/urteile/`, `knowledge/gesetze/`, `knowledge/checklisten/`.
4. **Merke geladene Slugs**, um Doppel-Reads zu vermeiden.

Triggers: siehe `.claude/hooks/triggers.json` (gleiche Schlagwort-Map gilt fuer Codex/Copilot).
"""

PORT_HEADER = """<!--
  AUTO-GENERATED — DO NOT EDIT DIRECTLY.
  Source: .claude/{source_rel}
  Regenerate via: python3 scripts/sync-platforms.py --apply
-->
"""


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Minimaler YAML-Frontmatter-Parser (key: value, ohne Listen)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    block = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    fm: Dict[str, str] = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip()
    return fm, body


def render_frontmatter(fm: Dict[str, str]) -> str:
    """Rendert Frontmatter zurueck zu YAML-Block."""
    if not fm:
        return ""
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def map_tools(tools_str: str, target: str) -> str:
    """Mappt Tool-Namen aus Frontmatter `allowed-tools` oder `tools`."""
    if not tools_str:
        return tools_str
    table = TOOL_MAP_CODEX if target == "codex" else TOOL_MAP_COPILOT
    parts = [p.strip() for p in tools_str.split(",") if p.strip()]
    mapped = [table.get(p, p) for p in parts]
    return ", ".join(mapped)


def replace_path_vars(content: str, target: str) -> str:
    """Ersetzt Claude-spezifische Pfad-Variablen."""
    table = PATH_VARS_CODEX if target == "codex" else PATH_VARS_COPILOT
    for src, dst in table.items():
        content = content.replace(src, dst)
    return content


def port_command(source: Path, target_platform: str) -> str:
    """Portiert einen Slash-Command aus .claude/commands/."""
    raw = source.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)

    if "allowed-tools" in fm:
        fm["allowed-tools"] = map_tools(fm["allowed-tools"], target_platform)

    body = replace_path_vars(body, target_platform)
    source_rel = source.relative_to(SOURCE_DIR).as_posix()

    out = PORT_HEADER.format(source_rel=source_rel)
    out += render_frontmatter(fm)
    out += body
    return out


def port_agent(source: Path, target_platform: str) -> str:
    """Portiert einen Custom-Agent aus .claude/agents/."""
    raw = source.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)

    if "tools" in fm:
        fm["tools"] = map_tools(fm["tools"], target_platform)

    if target_platform == "codex":
        if "model" in fm and "claude" in fm["model"].lower():
            fm["model_note"] = "Original Claude-Modell; Codex-User waehlt aequivalentes Modell"
    elif target_platform == "copilot":
        original_model = fm.pop("model", None)
        if original_model:
            fm["original-model"] = original_model

    body = replace_path_vars(body, target_platform)
    source_rel = source.relative_to(SOURCE_DIR).as_posix()

    out = PORT_HEADER.format(source_rel=source_rel)
    out += render_frontmatter(fm)
    out += body
    return out


def port_skill(source: Path, target_platform: str) -> str:
    """Portiert ein Skill aus .claude/skills/<name>/SKILL.md."""
    raw = source.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    body = replace_path_vars(body, target_platform)

    if "Auto-Routing" not in body:
        body = body.rstrip() + "\n" + AUTO_ROUTING_BLOCK_DE

    source_rel = source.relative_to(SOURCE_DIR).as_posix()
    out = PORT_HEADER.format(source_rel=source_rel)
    out += render_frontmatter(fm)
    out += body
    return out


def collect_actions() -> List[Tuple[Path, Path, str]]:
    """Sammelt alle (source, target, kind)-Tupel."""
    actions: List[Tuple[Path, Path, str]] = []

    for cmd in (SOURCE_DIR / "commands").glob("*.md"):
        actions.append((cmd, CODEX_DIR / "prompts" / cmd.name, "command-codex"))
        actions.append((cmd, COPILOT_DIR / "prompts" / cmd.stem / "PROMPT.md", "command-copilot"))

    for agent in (SOURCE_DIR / "agents").glob("*.md"):
        actions.append((agent, CODEX_DIR / "agents" / agent.name, "agent-codex"))
        actions.append((agent, COPILOT_DIR / "agents" / agent.name, "agent-copilot"))

    for skill in (SOURCE_DIR / "skills").iterdir():
        if not skill.is_dir():
            continue
        skill_md = skill / "SKILL.md"
        if not skill_md.exists():
            continue
        actions.append((skill_md, CODEX_DIR / "skills" / skill.name / "SKILL.md", "skill-codex"))
        actions.append((skill_md, COPILOT_DIR / "skills" / skill.name / "SKILL.md", "skill-copilot"))

    return actions


def render_for_action(source: Path, kind: str) -> str:
    """Erzeugt den portierten Content fuer eine Action."""
    if kind == "command-codex":
        return port_command(source, "codex")
    if kind == "command-copilot":
        return port_command(source, "copilot")
    if kind == "agent-codex":
        return port_agent(source, "codex")
    if kind == "agent-copilot":
        return port_agent(source, "copilot")
    if kind == "skill-codex":
        return port_skill(source, "codex")
    if kind == "skill-copilot":
        return port_skill(source, "copilot")
    raise ValueError(f"Unbekannter kind: {kind}")


def write_codex_config() -> str:
    """Erzeugt .codex/config.toml aus .claude/settings.json."""
    settings = json.loads((SOURCE_DIR / "settings.json").read_text(encoding="utf-8"))
    permissions = settings.get("permissions", {}).get("allow", [])

    web_domains: List[str] = []
    bash_patterns: List[str] = []
    for p in permissions:
        if p.startswith("WebFetch(domain:") and p.endswith(")"):
            web_domains.append(p[len("WebFetch(domain:"):-1])
        elif p.startswith("Bash("):
            bash_patterns.append(p[len("Bash("):-1])

    lines = [
        "# Auto-generated from .claude/settings.json by scripts/sync-platforms.py",
        "# DO NOT EDIT DIRECTLY",
        "",
        "[plugin]",
        'name = "legal-audit-de"',
        'description = "DE/EU legal audit workspace (DSGVO, TDDDG, UWG, AI Act, etc.). NOT legal advice."',
        "",
        "[features]",
        "multi_agent = true",
        "",
        "[permissions]",
        "# WebFetch-Whitelist: Tier-1-Primaerquellen (DE/EU-Recht)",
        f"web_fetch_domains = {json.dumps(sorted(web_domains))}",
        "",
        "# Erlaubte Bash-Patterns",
        f"bash_patterns = {json.dumps(bash_patterns)}",
        "",
        "[language]",
        'response = "de"',
        'comments = "en"',
        "",
        "[disclaimer]",
        "always_inject = true",
        'text = "Outputs sind keine Rechtsberatung im Sinne von Paragraph 2 RDG. Eine abschliessende Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend erforderlich."',
    ]
    return "\n".join(lines) + "\n"


def write_codex_plugin_manifest() -> str:
    """Erzeugt das native Codex-Plugin-Manifest."""
    claude_manifest = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    manifest = {
        "name": claude_manifest.get("name", "legal-audit-de"),
        "version": claude_manifest.get("version", "0.0.0"),
        "description": claude_manifest.get("description", "DE/EU legal audit workspace. NOT legal advice."),
        "author": {
            "name": claude_manifest.get("author", {}).get("name", "FutureRoots DE"),
            "email": "noreply@futureroots.de",
            "url": claude_manifest.get("author", {}).get("url", "https://github.com/FutureRootsDE"),
        },
        "homepage": claude_manifest.get("homepage", "https://github.com/FutureRootsDE/legal-audit-de"),
        "repository": claude_manifest.get("repository", "https://github.com/FutureRootsDE/legal-audit-de"),
        "license": claude_manifest.get("license", "MIT"),
        "keywords": claude_manifest.get("keywords", []),
        "skills": "./.codex/skills/",
        "interface": {
            "displayName": "legal-audit-de",
            "shortDescription": "DE/EU legal audits for codebases, live URLs, and legal documents.",
            "longDescription": (
                "Specialized German/EU legal audit workspace for technical pre-checks of codebases, "
                "websites, and legal documents. Produces severity-classified findings and clean "
                "draft corrections. Outputs are not legal advice."
            ),
            "developerName": "FutureRoots DE",
            "category": "Compliance",
            "capabilities": ["Interactive", "Write"],
            "websiteURL": claude_manifest.get("homepage", "https://github.com/FutureRootsDE/legal-audit-de"),
            "defaultPrompt": [
                "Audit this project for DE/EU legal issues.",
                "Check this privacy policy for DSGVO issues.",
                "Load legal KB for cookie consent.",
            ],
            "brandColor": "#1F2937",
        },
    }
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def write_codex_marketplace() -> str:
    """Erzeugt eine Codex-Marketplace-Datei fuer dieses Repo als Plugin-Root."""
    marketplace = {
        "name": "futureroots-legal",
        "interface": {
            "displayName": "FutureRoots Legal",
        },
        "plugins": [
            {
                "name": "legal-audit-de",
                "source": {
                    "source": "local",
                    "path": "./",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Compliance",
            }
        ],
    }
    return json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n"


def sync(actions: List[Tuple[Path, Path, str]], apply: bool, verbose: bool) -> int:
    """Vergleicht / schreibt Targets. Returns drift count."""
    drift = 0
    for source, target, kind in actions:
        content = render_for_action(source, kind)
        if target.exists():
            current = target.read_text(encoding="utf-8")
            if current == content:
                if verbose:
                    print(f"OK   {target.relative_to(REPO_ROOT).as_posix()}")
                continue
            drift += 1
            if verbose or not apply:
                print(f"DIFF {target.relative_to(REPO_ROOT).as_posix()}")
        else:
            drift += 1
            if verbose or not apply:
                print(f"MISS {target.relative_to(REPO_ROOT).as_posix()}")

        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            if verbose:
                print(f"WROTE {target.relative_to(REPO_ROOT).as_posix()}")

    codex_config_path = CODEX_DIR / "config.toml"
    codex_config = write_codex_config()
    if codex_config_path.exists() and codex_config_path.read_text(encoding="utf-8") == codex_config:
        if verbose:
            print(f"OK   {codex_config_path.relative_to(REPO_ROOT).as_posix()}")
    else:
        drift += 1
        if verbose or not apply:
            label = "DIFF" if codex_config_path.exists() else "MISS"
            print(f"{label} {codex_config_path.relative_to(REPO_ROOT).as_posix()}")
        if apply:
            codex_config_path.parent.mkdir(parents=True, exist_ok=True)
            codex_config_path.write_text(codex_config, encoding="utf-8")

    codex_plugin_path = CODEX_PLUGIN_DIR / "plugin.json"
    codex_plugin = write_codex_plugin_manifest()
    if codex_plugin_path.exists() and codex_plugin_path.read_text(encoding="utf-8") == codex_plugin:
        if verbose:
            print(f"OK   {codex_plugin_path.relative_to(REPO_ROOT).as_posix()}")
    else:
        drift += 1
        if verbose or not apply:
            label = "DIFF" if codex_plugin_path.exists() else "MISS"
            print(f"{label} {codex_plugin_path.relative_to(REPO_ROOT).as_posix()}")
        if apply:
            codex_plugin_path.parent.mkdir(parents=True, exist_ok=True)
            codex_plugin_path.write_text(codex_plugin, encoding="utf-8")

    codex_marketplace = write_codex_marketplace()
    if CODEX_MARKETPLACE.exists() and CODEX_MARKETPLACE.read_text(encoding="utf-8") == codex_marketplace:
        if verbose:
            print(f"OK   {CODEX_MARKETPLACE.relative_to(REPO_ROOT).as_posix()}")
    else:
        drift += 1
        if verbose or not apply:
            label = "DIFF" if CODEX_MARKETPLACE.exists() else "MISS"
            print(f"{label} {CODEX_MARKETPLACE.relative_to(REPO_ROOT).as_posix()}")
        if apply:
            CODEX_MARKETPLACE.parent.mkdir(parents=True, exist_ok=True)
            CODEX_MARKETPLACE.write_text(codex_marketplace, encoding="utf-8")

    return drift


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Claude -> Codex/Copilot adapters")
    parser.add_argument("--check", action="store_true", help="Diff only, exit 1 if drift")
    parser.add_argument("--apply", action="store_true", help="Write/overwrite targets")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose listing")
    args = parser.parse_args()

    if not args.check and not args.apply:
        parser.print_help()
        return 2

    actions = collect_actions()
    drift = sync(actions, apply=args.apply, verbose=args.verbose)

    if args.check and drift > 0:
        print(f"\nFAIL: {drift} files out of sync. Run: python3 scripts/sync-platforms.py --apply", file=sys.stderr)
        return 1
    if args.apply:
        print(f"OK: {drift} files written/updated")
    elif args.check:
        print("OK: all platform adapters in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
