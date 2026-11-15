"""Project rules for the scripts: files up to 800 lines, functions up to 50 lines, no bare or silent excepts."""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

import support

MAX_FILE_LINES = 800
MAX_FUNCTION_LINES = 50
SOURCES = sorted((support.SCRIPTS / "citation_check").glob("*.py")) + [
    support.SCRIPTS / "legal-status.py", support.SCRIPTS / "verify-citations.py"]


def _functions(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


class CodeLimits(unittest.TestCase):
    def test_file_length(self):
        for path in SOURCES:
            lines = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(lines, MAX_FILE_LINES, f"{path.name}: {lines} Zeilen")

    def test_function_length(self):
        for path in SOURCES:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in _functions(tree):
                length = node.end_lineno - node.lineno + 1
                self.assertLessEqual(length, MAX_FUNCTION_LINES, f"{path.name}:{node.name} hat {length} Zeilen")

    def test_no_bare_or_silent_excepts(self):
        for path in SOURCES:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    where = f"{path.name}:{node.lineno}"
                    self.assertIsNotNone(node.type, f"nackter except in {where}")
                    silent = all(isinstance(stmt, ast.Pass) for stmt in node.body)
                    self.assertFalse(silent, f"stiller except in {where}")

    def test_no_debug_output_in_the_package(self):
        for path in (p for p in SOURCES if p.parent.name == "citation_check"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                    keywords = {k.arg for k in node.keywords}
                    self.assertIn("file", keywords, f"print ohne file= in {path.name}:{node.lineno}")


if __name__ == "__main__":
    unittest.main()
