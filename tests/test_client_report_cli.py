"""Offline tests for the client-test command line (scripts/client_report/cli.py)."""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support
from client_report import cli
from client_report.catalog import APPLICABILITY_KEYS, load_catalog
from client_report.texts import START_HINT
from client_report_support import valid_findings, write_png

PROFILE = {
    "company": "Muster Webdesign GmbH",
    "contact": "Erika Muster",
    "address": ["Hauptstraße 1", "10115 Berlin"],
    "email": "info@muster-web.de",
}
JPG_BYTES = b"\xff\xd8\xff\xe0" + b"0" * 64


def run_cli(argv, stdin_tty=False):
    out, err = io.StringIO(), io.StringIO()
    stdin = mock.Mock()
    stdin.isatty.return_value = stdin_tty
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), mock.patch.object(sys, "stdin", stdin):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


class CliCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.home = self.tmp / "home"
        self.work = self.tmp / "work"
        self.work.mkdir()
        self._cwd = os.getcwd()
        os.chdir(self.work)
        patcher = mock.patch.dict(os.environ, {"LEGAL_AUDIT_CLIENT_TEST_HOME": str(self.home)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)
        self.addCleanup(os.chdir, self._cwd)

    def save_profile(self, logo_name="logo.png", extra=None, tty=False):
        logo = self.tmp / logo_name
        if logo_name.endswith(".png"):
            write_png(logo, (31, 78, 121))
        else:
            logo.write_bytes(JPG_BYTES)
        data = self.tmp / "profile.json"
        data.write_text(json.dumps(PROFILE), encoding="utf-8")
        argv = ["profile", "save", "--data", str(data), "--logo", str(logo)] + (extra or [])
        return run_cli(argv, stdin_tty=tty)

    def init_report(self):
        self.assertEqual(self.save_profile()[0], 0)
        code, out, _ = run_cli(["init", "https://www.Example.de:8443/", "--date", "2026-11-17"])
        self.assertEqual(code, 0)
        return Path(out.splitlines()[-1])

    def read(self, report_dir):
        return json.loads((report_dir / "findings.json").read_text(encoding="utf-8"))

    def write(self, report_dir, data):
        (report_dir / "findings.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def set_applicability(self, report_dir, **values):
        data = self.read(report_dir)
        for key in APPLICABILITY_KEYS:
            data["applicability"][key] = {"value": values.get(key, False), "source": "user"}
        self.write(report_dir, data)

    def valid_report(self):
        d = self.init_report()
        data = valid_findings(load_catalog())
        data["issuer"] = self.read(d)["issuer"]
        self.write(d, data)
        return d


class Check(CliCase):
    def test_check_prints_start_hint_first(self):
        code, out, _ = run_cli(["check"])
        self.assertEqual((code, out.splitlines()[0]), (0, START_HINT))
        self.assertIn("plugin_version:", out)

    def test_check_fails_with_exit_2_when_template_missing(self):
        with mock.patch.object(cli, "TEMPLATE_PATH", self.tmp / "missing.tmpl"):
            code, out, err = run_cli(["check"])
        self.assertEqual(code, 2)
        self.assertEqual(out.splitlines()[0], START_HINT)
        self.assertIn("missing.tmpl", err)


class Profile(CliCase):
    def test_show_without_profile_exits_3(self):
        code, out, err = run_cli(["profile", "show"])
        self.assertEqual(code, 3)
        self.assertIn("Kein Briefkopf-Profil gespeichert.", out + err)

    def test_save_and_show_json(self):
        code, out, _ = self.save_profile()
        self.assertEqual(code, 0)
        self.assertTrue(Path(out.strip().splitlines()[-1]).is_file())
        code, out, _ = run_cli(["profile", "show", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["company"], PROFILE["company"])

    def test_save_with_explicit_accent_is_contrast_adjusted(self):
        self.assertEqual(self.save_profile(extra=["--accent", "#FFFF00"])[0], 0)
        accent = json.loads(run_cli(["profile", "show", "--json"])[1])["accent_color"]
        self.assertNotEqual(accent.upper(), "#FFFF00")

    def test_save_accent_default(self):
        self.assertEqual(self.save_profile("logo.jpg", ["--accent", "default"])[0], 0)
        self.assertEqual(json.loads(run_cli(["profile", "show", "--json"])[1])["accent_color"], "#2F3E46")

    def test_save_accent_unknown_for_jpg_without_tty_does_not_hang(self):
        with mock.patch("builtins.input", side_effect=AssertionError("must not prompt")):
            code, out, _ = self.save_profile("logo.jpg")
        self.assertEqual(code, 5)
        self.assertIn("ACCENT_UNKNOWN", out)
        self.assertEqual(run_cli(["profile", "show"])[0], 3)

    def test_save_jpg_prompts_once_on_tty(self):
        with mock.patch("builtins.input", return_value="#1F4E79") as prompt:
            code, _, _ = self.save_profile("logo.jpg", tty=True)
        self.assertEqual(code, 0)
        self.assertEqual(prompt.call_count, 1)

    def test_save_jpg_empty_answer_on_tty_uses_default(self):
        with mock.patch("builtins.input", return_value=""):
            code, _, _ = self.save_profile("logo.jpg", tty=True)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(run_cli(["profile", "show", "--json"])[1])["accent_color"], "#2F3E46")

    def test_save_rejects_bad_accent(self):
        self.assertEqual(self.save_profile(extra=["--accent", "blau"])[0], 1)

    def test_save_rejects_invalid_profile_data(self):
        data = self.tmp / "bad.json"
        data.write_text(json.dumps({"company": "x"}), encoding="utf-8")
        logo = self.tmp / "l.png"
        write_png(logo, (1, 2, 3))
        code, _, err = run_cli(["profile", "save", "--data", str(data), "--logo", str(logo), "--accent", "default"])
        self.assertEqual(code, 1)
        self.assertIn("profile.", err)


class Init(CliCase):
    def test_init_without_profile_exits_3(self):
        self.assertEqual(run_cli(["init", "https://example.de/"])[0], 3)

    def test_init_creates_skeleton(self):
        d = self.init_report()
        self.assertEqual(d.name, "2026-11-17-example-de")
        data = self.read(d)
        self.assertEqual(data["results"], [])
        self.assertEqual(data["run"]["domain"], "example.de")
        self.assertEqual(data["issuer"]["logo_file"], "assets/logo.png")
        self.assertEqual(set(data["applicability"]), set(APPLICABILITY_KEYS))
        self.assertTrue((d / "assets" / "logo.png").is_file() and (d / "evidence").is_dir())
        self.assertTrue(d.is_relative_to(self.work / "client-reports"))

    def test_init_rejects_bad_url_and_date(self):
        self.assertEqual(self.save_profile()[0], 0)
        self.assertEqual(run_cli(["init", "ftp://example.de/"])[0], 1)
        self.assertEqual(run_cli(["init", "https://example.de/", "--date", "17.11.2026"])[0], 1)

    @unittest.skipUnless(shutil.which("git"), "git nicht installiert")
    def test_init_warns_when_reports_not_ignored(self):
        subprocess.run(["git", "init", "-q"], cwd=self.work, check=True)
        self.assertEqual(self.save_profile()[0], 0)
        code, out, _ = run_cli(["init", "https://example.de/", "--date", "2026-11-17"])
        self.assertEqual(code, 0)
        self.assertIn("nicht in .gitignore eingetragen", out)
        self.assertTrue(Path(out.splitlines()[-1]).is_dir())


class Plan(CliCase):
    def test_plan_lists_only_applicable_ids(self):
        d = self.init_report()
        self.set_applicability(d, b2c=True, subscription=None)
        code, out, _ = run_cli(["plan", str(d)])
        ids = [r["id"] for r in self.read(d)["results"]]
        self.assertEqual(code, 0)
        self.assertIn("A11Y-01", ids)
        self.assertIn("SHOP-05", ids)
        self.assertNotIn("SHOP-04", ids)
        self.assertNotIn("DSA-01", ids)
        self.assertIn("A11Y-01", out)

    def test_plan_requires_all_applicability_sources(self):
        d = self.init_report()
        self.set_applicability(d)
        data = self.read(d)
        data["applicability"]["shop"]["source"] = ""
        self.write(d, data)
        code, _, err = run_cli(["plan", str(d)])
        self.assertEqual(code, 1)
        self.assertIn("shop", err)

    def test_plan_requires_three_valued_value(self):
        d = self.init_report()
        self.set_applicability(d)
        data = self.read(d)
        data["applicability"]["bfsg"]["value"] = "ja"
        self.write(d, data)
        code, _, err = run_cli(["plan", str(d)])
        self.assertEqual(code, 1)
        self.assertIn("bfsg", err)

    def test_plan_keeps_existing_results(self):
        d = self.init_report()
        self.set_applicability(d)
        run_cli(["plan", str(d)])
        data = self.read(d)
        first = data["results"][0]["id"]
        data["results"][0]["status"] = "pass"
        self.write(d, data)
        run_cli(["plan", str(d)])
        rows = self.read(d)["results"]
        self.assertEqual((rows[0]["id"], rows[0]["status"]), (first, "pass"))
        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))


class Render(CliCase):
    def test_render_skeleton_fails_with_paths(self):
        d = self.init_report()
        self.set_applicability(d)
        run_cli(["plan", str(d)])
        code, _, err = run_cli(["render", str(d)])
        self.assertEqual(code, 1)
        self.assertIn("results[0].status", err)

    def test_render_valid_writes_html(self):
        d = self.valid_report()
        code, out, err = run_cli(["render", str(d)])
        self.assertEqual((code, err), (0, ""))
        self.assertTrue(Path(out.strip().splitlines()[-1]).is_file())

    def test_render_missing_folder_exits_1(self):
        self.assertEqual(run_cli(["render", str(self.tmp / "nope")])[0], 1)


class Pdf(CliCase):
    def test_pdf_without_html_exits_1(self):
        d = self.init_report()
        self.assertEqual(run_cli(["pdf", str(d)])[0], 1)

    def test_pdf_without_chrome_exits_4(self):
        d = self.valid_report()
        run_cli(["render", str(d)])
        with mock.patch.object(cli, "find_chrome", return_value=None):
            code, _, err = run_cli(["pdf", str(d)])
        self.assertEqual(code, 4)
        self.assertIn("Chrome oder Edge nicht gefunden. report.html bleibt das Ergebnis.", err)

    def test_pdf_error_exits_6(self):
        d = self.valid_report()
        run_cli(["render", str(d)])
        with mock.patch.object(cli, "find_chrome", return_value=Path("chrome")), \
                mock.patch.object(cli, "print_pdf", side_effect=cli.PdfError("kaputt")):
            code, _, err = run_cli(["pdf", str(d)])
        self.assertEqual(code, 6)
        self.assertIn("kaputt", err)

    def test_pdf_success_writes_named_copy(self):
        d = self.valid_report()
        run_cli(["render", str(d)])

        def fake_print(html, pdf, chrome=None, **_):
            Path(pdf).write_bytes(b"%PDF-1.4 fake")
            return Path(pdf)

        with mock.patch.object(cli, "find_chrome", return_value=Path("chrome")), \
                mock.patch.object(cli, "print_pdf", side_effect=fake_print):
            code, out, _ = run_cli(["pdf", str(d)])
        self.assertEqual(code, 0)
        self.assertTrue((d / "report.pdf").is_file())
        self.assertTrue((d / "Website-CheckUp-example-de-2026-11-17.pdf").is_file())
        self.assertIn("Website-CheckUp-example-de-2026-11-17.pdf", out)


class Entrypoint(unittest.TestCase):
    def test_entrypoint_runs_as_script_from_other_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, str(support.SCRIPTS / "client-test.py"), "check"],
                               capture_output=True, text=True, encoding="utf-8", cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.splitlines()[0], START_HINT)


if __name__ == "__main__":
    unittest.main()
