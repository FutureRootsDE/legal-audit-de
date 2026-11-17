"""Checks for command files and generated platform adapters."""
from __future__ import annotations

import importlib.util
import re
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


CLIENT_TEST_TOOLS = {
    "new_page", "navigate_page", "select_page", "list_pages", "close_page", "wait_for",
    "take_screenshot", "take_snapshot", "evaluate_script", "list_network_requests",
    "get_network_request", "list_console_messages", "click", "hover", "press_key",
    "emulate", "resize_page", "lighthouse_audit",
}
# Tools that enter data, confirm dialogs or profile the browser: never allowed (passive check).
CLIENT_TEST_FORBIDDEN = ("fill", "fill_form", "type_text", "upload_file", "handle_dialog", "drag",
                         "performance_start_trace", "performance_stop_trace",
                         "performance_analyze_insight", "take_heapsnapshot")
QUOTE_RE = re.compile("„([^“”]*)“")


class ClientTestCommand(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / ".claude/commands/legal-client-test.md"
        self.text = self.path.read_text(encoding="utf-8")
        self.fm = command_frontmatter(self.path)
        self.tools = [t.strip() for t in self.fm["allowed-tools"].split(",") if t.strip()]

    def test_uses_both_prefix_variants_and_lighthouse(self):
        mcp = [t for t in self.tools if t.startswith("mcp__")]
        plugin = {t[len(RIGHT_PREFIX):] for t in mcp if t.startswith(RIGHT_PREFIX)}
        direct = {t[len(DIRECT_PREFIX):] for t in mcp if t.startswith(DIRECT_PREFIX)}
        self.assertEqual(len(mcp), 36)
        self.assertEqual(plugin, CLIENT_TEST_TOOLS)
        self.assertEqual(direct, CLIENT_TEST_TOOLS)
        self.assertIn(RIGHT_PREFIX + "lighthouse_audit", mcp)

    def test_no_input_tools(self):
        for name in CLIENT_TEST_FORBIDDEN:
            self.assertNotIn(RIGHT_PREFIX + name, self.tools)
            self.assertNotIn(DIRECT_PREFIX + name, self.tools)

    def test_core_tools_exact(self):
        core = [t for t in self.tools if not t.startswith("mcp__")]
        self.assertEqual(core, ["Bash(python:*)", "Bash(python3:*)", "Bash(py:*)", "Bash(curl -sI:*)",
                                "Read", "Write", "Glob", "Grep"])
        self.assertNotIn("Bash", core)

    def test_scripts_addressed_via_plugin_root(self):
        self.assertIn('python "${CLAUDE_PLUGIN_ROOT}/scripts/client-test.py"', self.text)
        self.assertNotIn("${CLAUDE_PROJECT_DIR}/scripts/client-test.py", self.text)

    def test_user_facing_quotes_dash_free(self):
        from client_report.textcheck import find_dashes, find_forbidden, load_forbidden_phrases
        phrases = load_forbidden_phrases()
        quotes = QUOTE_RE.findall(self.text)
        self.assertGreater(len(quotes), 10)
        offenders = [(q, find_dashes(q), find_forbidden(q, phrases)) for q in quotes
                     if find_dashes(q) or find_forbidden(q, phrases)]
        self.assertEqual(offenders, [])

    def test_body_has_no_dashes(self):
        body = self.text.split("\n---\n", 1)[1]
        self.assertNotIn("—", body)
        self.assertNotIn("–", body)

    def test_adapters_exist(self):
        codex = ROOT / ".codex/prompts/legal-client-test.md"
        copilot = ROOT / ".github/prompts/legal-client-test/PROMPT.md"
        self.assertTrue(codex.is_file())
        self.assertTrue(copilot.is_file())
        self.assertIn("${GITHUB_WORKSPACE}/scripts/client-test.py", copilot.read_text(encoding="utf-8"))


class BashPatternMapping(unittest.TestCase):
    """Restricted Bash(<pattern>) entries must never silently become full shell access."""
    TOOLS = "Bash(python:*), Bash(curl -sI:*), Read"

    def setUp(self):
        self.sp = _load_sync_platforms()

    def test_map_tools_collapses_patterns_to_shell_tool(self):
        self.assertEqual(self.sp.map_tools(self.TOOLS, "codex"), "shell.exec, file.read")
        self.assertEqual(self.sp.map_tools(self.TOOLS, "copilot"), "bash, view")

    def test_bare_bash_unchanged(self):
        self.assertEqual(self.sp.map_tools("Bash, Read", "codex"), "shell.exec, file.read")

    def test_extract_patterns(self):
        self.assertEqual(self.sp.extract_bash_patterns(self.TOOLS + ", Bash"),
                         ["python:*", "curl -sI:*"])

    def test_notice_lists_patterns_without_dashes(self):
        notice = self.sp.restriction_notice(["python:*", "curl -sI:*"])
        self.assertIn("Erlaubte Shell-Befehle: nur", notice)
        self.assertIn("`python:*`", notice)
        self.assertIn("`curl -sI:*`", notice)
        for bad in ("—", "–", " - "):
            self.assertNotIn(bad, notice)

    def test_generated_adapters_keep_restriction(self):
        for path in (ROOT / ".codex/prompts/legal-client-test.md",
                     ROOT / ".github/prompts/legal-client-test/PROMPT.md"):
            text = path.read_text(encoding="utf-8")
            fm_line = next(l for l in text.splitlines() if l.startswith("allowed-tools:"))
            self.assertNotIn("Bash(", fm_line)
            self.assertIn("Erlaubte Shell-Befehle: nur", text)
            self.assertIn("`curl -sI:*`", text)


if __name__ == "__main__":
    unittest.main()
