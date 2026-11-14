"""Entry point, CI permissions, per-user cache location and function length limits."""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support
from citation_check import cache, cli

REPO = support.HERE.parent
SCRIPT = REPO / "scripts" / "verify-citations.py"
PACKAGE = REPO / "scripts" / "citation_check"
MAX_FILE_LINES = 800
MAX_FUNCTION_LINES = 50


class EntryPointTests(unittest.TestCase):
    def run_script(self, cwd: Path, *args: str):
        return subprocess.run([sys.executable, "-I", str(SCRIPT), *args], cwd=cwd, capture_output=True,
                              text=True, encoding="utf-8", timeout=60)

    def test_help_works_from_repo_root_and_from_elsewhere(self):
        for cwd in (REPO, Path(tempfile.gettempdir())):
            result = self.run_script(cwd, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--write-ecli", result.stdout)

    def test_offline_run_against_the_repo_kb_needs_no_network(self):
        result = self.run_script(REPO, "--offline", "--no-cache", "--json", "--path", str(REPO / "knowledge"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"UNCHECKED"', result.stdout)


class WorkflowTests(unittest.TestCase):
    def test_validate_workflow_has_read_only_top_level_permissions(self):
        text = (REPO / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^permissions:\n  contents: read\n")
        self.assertNotRegex(text, r"(?m)^\s+(contents|pull-requests|issues|actions): write")

    def test_ci_discovers_all_unit_tests(self):
        text = (REPO / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        self.assertIn("unittest discover -s tests", text)


class CacheLocationTests(unittest.TestCase):
    def test_default_dir_outside_the_user_profile_disables_the_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            home.mkdir()
            inside = home / "AppData" / "Local" / "citation-check" / "cache"
            outside = Path(tmp) / "elsewhere" / "citation-check" / "cache"
            self.assertEqual(cache.vet_default_dir(inside, home, enforce=True), (inside, None))
            path, warning = cache.vet_default_dir(outside, home, enforce=True)
            self.assertIsNone(path)
            self.assertIn("Nutzerprofil", warning)

    def test_vetting_is_not_enforced_when_not_requested(self):
        self.assertEqual(cache.vet_default_dir(Path("/somewhere/else"), Path("/home/x"), enforce=False),
                         (Path("/somewhere/else"), None))

    @unittest.skipUnless(os.name == "nt", "Windows-specific default location")
    def test_windows_default_with_manipulated_localappdata_runs_without_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp) / "home"
            fake_home.mkdir()
            with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(Path(tmp) / "fremd")}), \
                    mock.patch.object(cache, "user_home", lambda: fake_home):
                path, warning = cache.default_cache_dir_vetted()
            self.assertIsNone(path)
            self.assertIn("Nutzerprofil", warning)


class SizeLimitTests(unittest.TestCase):
    def python_files(self):
        return [SCRIPT, *sorted(PACKAGE.glob("*.py")), *sorted((REPO / "tests").glob("*.py"))]

    def test_no_file_over_800_lines(self):
        for path in self.python_files():
            lines = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(lines, MAX_FILE_LINES, f"{path.name}: {lines} Zeilen")

    def test_no_function_over_50_lines_in_the_package(self):
        for path in [SCRIPT, *sorted(PACKAGE.glob("*.py"))]:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    length = node.end_lineno - node.lineno + 1
                    self.assertLessEqual(length, MAX_FUNCTION_LINES, f"{path.name}:{node.name} {length} Zeilen")

    def test_no_pycache_or_cache_dirs_are_tracked(self):
        result = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            self.skipTest("kein Git-Repository")
        tracked = result.stdout.splitlines()
        self.assertEqual([f for f in tracked if "__pycache__" in f or f.endswith(".pyc")], [])
        self.assertEqual([f for f in tracked if re.search(r"(^|/)citation-check/", f)], [])


if __name__ == "__main__":
    unittest.main()
