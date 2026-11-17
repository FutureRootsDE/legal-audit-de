"""Checks for command files and generated platform adapters."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import support

ROOT = support.HERE.parent
# Plugin installation (verified) and direct `claude mcp add` installation.
RIGHT_PREFIX = "mcp__plugin_chrome-devtools-mcp_chrome-devtools__"
DIRECT_PREFIX = "mcp__chrome-devtools__"
WRONG_PREFIX = "mcp__plugin_chrome-devtools-mcp__"


def _load_sync_platforms():
    spec = importlib.util.spec_from_file_location(
        "sync_platforms", ROOT / "scripts" / "sync-platforms.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command_frontmatter(path: Path) -> dict[str, str]:
    parse = _load_sync_platforms().parse_frontmatter
    return parse(path.read_text(encoding="utf-8"))[0]


class ChromeDevtoolsToolNames(unittest.TestCase):
    def test_no_wrong_prefix_in_commands_or_adapters(self):
        files = (list((ROOT / ".claude/commands").glob("*.md"))
                 + list((ROOT / ".codex/prompts").glob("*.md"))
                 + list((ROOT / ".github/prompts").glob("*/PROMPT.md")))
        offenders = [str(p) for p in files
                     if WRONG_PREFIX in p.read_text(encoding="utf-8")]
        self.assertEqual(offenders, [])

    def test_live_audit_allowed_tools_cover_both_install_variants(self):
        raw = command_frontmatter(ROOT / ".claude/commands/legal-audit-live.md")["allowed-tools"]
        mcp = [t.strip() for t in raw.split(",") if t.strip().startswith("mcp__")]
        plugin = [t for t in mcp if t.startswith(RIGHT_PREFIX)]
        direct = [t for t in mcp if t.startswith(DIRECT_PREFIX)]
        self.assertEqual(len(plugin), 12)
        self.assertEqual(len(direct), 12)
        self.assertEqual(len(mcp), 24)
        self.assertEqual({t[len(RIGHT_PREFIX):] for t in plugin},
                         {t[len(DIRECT_PREFIX):] for t in direct})


if __name__ == "__main__":
    unittest.main()
