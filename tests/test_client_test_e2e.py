"""End-to-end smoke test of the website check-up: the whole CLI chain against a fixture run.

Chain: check, profile save (temporary profile home), init, plan, fill in the fixture results,
render, pdf. Everything is written to temporary folders; nothing is left in the repository.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support
from client_report import cli
from client_report.chrome import find_chrome
from client_report.embed import SIZE_BUDGET_BYTES, find_external_refs
from client_report.texts import FOOTER, LAWYER_SENTENCE, PASS_ON_SENTENCE, TITLE
from client_report_support import SHOT_FILE, write_png

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "client_test" / "findings_full.json"
ENTRY = REPO_ROOT / "scripts" / "client-test.py"
FIXTURE_DATE = "2026-11-17"
PDF_NAME = f"Website-CheckUp-127-0-0-1-{FIXTURE_DATE}.pdf"
FORBIDDEN_LABELS = ("Bestanden", "Mangel")
PROFILE = {
    "company": "Muster Webdesign GmbH",
    "contact": "Erika Muster",
    "address": ["Hauptstraße 1", "10115 Berlin"],
    "email": "info@muster-web.de",
}


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    stdin = mock.Mock()
    stdin.isatty.return_value = False
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), mock.patch.object(sys, "stdin", stdin):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


class EndToEndCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.work = self.tmp / "work"
        self.work.mkdir()
        self._cwd = os.getcwd()
        os.chdir(self.work)
        patcher = mock.patch.dict(os.environ, {"LEGAL_AUDIT_CLIENT_TEST_HOME": str(self.tmp / "home")})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)
        self.addCleanup(os.chdir, self._cwd)

    def init_from_fixture(self) -> Path:
        """Profile save, init, plan and fixture results: the state after the browser phase."""
        logo = self.tmp / "logo.png"
        write_png(logo, (31, 78, 121))
        data = self.tmp / "profile.json"
        data.write_text(json.dumps(PROFILE), encoding="utf-8")
        code, _, err = run_cli(["profile", "save", "--data", str(data), "--logo", str(logo)])
        self.assertEqual(code, 0, err)
        code, out, err = run_cli(["init", "http://127.0.0.1:8765/", "--out", str(self.tmp / "reports"),
                                  "--date", FIXTURE_DATE])
        self.assertEqual(code, 0, err)
        report_dir = Path(out.splitlines()[-1])
        findings = json.loads(FIXTURE.read_text(encoding="utf-8"))
        findings["issuer"] = json.loads((report_dir / "findings.json").read_text(encoding="utf-8"))["issuer"]
        (report_dir / "findings.json").write_text(json.dumps(findings, ensure_ascii=False), encoding="utf-8")
        write_png(report_dir / SHOT_FILE, (200, 200, 200))
        return report_dir

    @staticmethod
    def count_status(report_dir: Path, status: str) -> int:
        rows = json.loads((report_dir / "findings.json").read_text(encoding="utf-8"))["results"]
        return sum(1 for row in rows if row["status"] == status)


class EndToEnd(EndToEndCase):
    def test_check_runs_through_real_entry_point(self):
        done = subprocess.run([sys.executable, str(ENTRY), "check"], capture_output=True, text=True,
                              encoding="utf-8", timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("plugin_version:", done.stdout)

    def test_fixture_run_renders_html(self):
        report_dir = self.init_from_fixture()
        code, out, err = run_cli(["plan", str(report_dir)])
        self.assertEqual(code, 0, err)
        self.assertNotIn("SHOP-05", out)
        self.assertNotIn("SHOP-10", out)
        code, _, err = run_cli(["render", str(report_dir)])
        self.assertEqual(code, 0, err)
        html = (report_dir / "report.html").read_text(encoding="utf-8")
        defects = self.count_status(report_dir, "defect")
        self.assertEqual(defects, 3)
        self.assertEqual(html.count(LAWYER_SENTENCE), 2 * defects)
        self.assertIn(TITLE.replace("&", "&amp;"), html)
        self.assertIn(PASS_ON_SENTENCE, html)
        self.assertIn(FOOTER, html)
        self.assertIn("Prüffrage für Ihre Rechtsberatung", html)
        self.assertIn("Anwendbarkeit ungeklärt", html)
        for label in FORBIDDEN_LABELS:
            self.assertNotIn(label, html)
        self.assertEqual(find_external_refs(html), [])
        self.assertLess(len(html.encode("utf-8")), SIZE_BUDGET_BYTES)

    def test_forbidden_phrase_in_prose_blocks_render(self):
        report_dir = self.init_from_fixture()
        path = report_dir / "findings.json"
        findings = json.loads(path.read_text(encoding="utf-8"))
        index = next(i for i, row in enumerate(findings["results"]) if row["id"] == "CK-01")
        findings["results"][index]["client_text"] = "Die Seite verstößt gegen geltendes Recht."
        path.write_text(json.dumps(findings, ensure_ascii=False), encoding="utf-8")
        code, _, err = run_cli(["render", str(report_dir)])
        self.assertEqual(code, 1)
        self.assertIn(f"results[{index}].client_text", err)
        self.assertFalse((report_dir / "report.html").exists())

    def test_missing_result_blocks_render(self):
        report_dir = self.init_from_fixture()
        path = report_dir / "findings.json"
        findings = json.loads(path.read_text(encoding="utf-8"))
        findings["results"] = [row for row in findings["results"] if row["id"] != "IMP-01"]
        path.write_text(json.dumps(findings, ensure_ascii=False), encoding="utf-8")
        code, _, err = run_cli(["render", str(report_dir)])
        self.assertEqual(code, 1)
        self.assertIn("IMP-01 fehlt", err)

    @unittest.skipUnless(find_chrome(), "Chrome/Edge nicht installiert")
    def test_fixture_run_prints_pdf(self):
        report_dir = self.init_from_fixture()
        self.assertEqual(run_cli(["render", str(report_dir)])[0], 0)
        code, out, err = run_cli(["pdf", str(report_dir)])
        self.assertEqual(code, 0, err)
        pdf = (report_dir / "report.pdf").read_bytes()
        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertIn(b"/StructTreeRoot", pdf)
        named = report_dir / PDF_NAME
        self.assertTrue(named.is_file())
        self.assertEqual(named.read_bytes(), pdf)
        self.assertEqual(Path(out.strip().splitlines()[-1]).name, PDF_NAME)
        self.assertRegex(PDF_NAME, re.compile(r"^Website-CheckUp-[a-z0-9-]+-\d{4}-\d{2}-\d{2}\.pdf$"))

    def test_run_leaves_repository_clean(self):
        self.init_from_fixture()
        self.assertFalse((REPO_ROOT / "client-reports").exists())


if __name__ == "__main__":
    unittest.main()
