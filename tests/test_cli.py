"""Offline tests for the command line interface."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import urllib.error
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import cli
from support import FakeFetch, OK_I_ZR_159, OK_VI_ZR_10, OK_EMPTY


KB_TEXT_LF = (
    "# Thema\n"
    "BGH, Urt. v. 09.10.2025 - I ZR 159/24\n"
    "BGH VI ZR 10/24 v. 18.11.2024 <<VERIFIKATION AUSSTEHEND>>\n"
    "BGH I ZR 999/99 erfunden\n"
    "OLG Hamburg 5 U 104/24\n"
    "EuGH C-252/21\n"
    "BGH I ZR 25/19 v. 01.01.2022\n"
)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "themen").mkdir(parents=True)
        (self.kb / "themen" / "t.md").write_text(KB_TEXT_LF, encoding="utf-8", newline="")
        self.cache = self.tmp / "cache"
        self.fetch = FakeFetch({
            "I ZR 159/24": OK_I_ZR_159,
            "VI ZR 10/24": OK_VI_ZR_10,
            "I ZR 999/99": OK_EMPTY,
            "I ZR 25/19": OK_I_ZR_159,  # fuzzy, filtered out -> NOT_IN_DATASET
        })

    def run_cli(self, *args, fetch=None):
        out = io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.cache), "--no-eu", *args],
                       fetch=fetch or self.fetch, sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def test_json_report_counts_and_fields(self):
        code, text = self.run_cli("--json")
        self.assertEqual(code, 0)
        data = json.loads(text)
        counts = data["summary"]["counts"]
        self.assertEqual(counts["VERIFIED"], 2)
        self.assertEqual(counts["NOT_IN_DATASET"], 2)
        self.assertEqual(counts["NOT_COVERED"], 2)
        self.assertEqual(counts["DATE_MISMATCH"], 0)
        by_az = {c["az"]: c for c in data["citations"]}
        self.assertEqual(by_az["VI ZR 10/24"]["pending"], True)
        self.assertEqual(len(by_az["VI ZR 10/24"]["hits"]), 2)
        self.assertEqual(by_az["I ZR 159/24"]["file"], "knowledge/themen/t.md")
        self.assertEqual(by_az["I ZR 159/24"]["line"], 2)

    def test_date_mismatch_and_strict_exit_code(self):
        (self.kb / "themen" / "t.md").write_text("BGH I ZR 159/24 v. 10.10.2025\n", encoding="utf-8")
        code, text = self.run_cli("--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(text)["summary"]["counts"]["DATE_MISMATCH"], 1)
        code, _ = self.run_cli("--json", "--strict")
        self.assertEqual(code, 1)

    def test_strict_without_mismatch_is_zero(self):
        code, _ = self.run_cli("--strict")
        self.assertEqual(code, 0)

    def test_api_down_exit_zero_with_hint(self):
        down = FakeFetch(default=urllib.error.URLError("no route"))
        code, text = self.run_cli(fetch=down)
        self.assertEqual(code, 0)
        self.assertIn("ERROR", text)
        self.assertIn("nicht erreichbar", text)

    def test_only_pending(self):
        code, text = self.run_cli("--json", "--only-pending")
        data = json.loads(text)
        self.assertEqual([c["az"] for c in data["citations"]], ["VI ZR 10/24"])

    def test_unique_az_queried_once(self):
        (self.kb / "themen" / "u.md").write_text("Nochmals BGH I ZR 159/24\n", encoding="utf-8")
        self.run_cli("--json")
        self.assertEqual(len(self.fetch.calls_for("I ZR 159/24")), 1)

    def test_not_covered_is_not_queried(self):
        self.run_cli("--json")
        queried = {parse_qs(urlparse(u).query)["fileNumber"][0] for u in self.fetch.calls}
        self.assertNotIn("5 U 104/24", queried)
        self.assertNotIn("C-252/21", queried)

    def test_offline_makes_no_requests_and_marks_unchecked(self):
        code, text = self.run_cli("--json", "--offline")
        self.assertEqual(code, 0)
        self.assertEqual(self.fetch.calls, [])
        counts = json.loads(text)["summary"]["counts"]
        self.assertEqual(counts["UNCHECKED"], 4)
        self.assertEqual(counts["NOT_COVERED"], 2)

    def test_offline_after_online_run_uses_cache(self):
        self.run_cli("--json")
        calls_before = len(self.fetch.calls)
        _, text = self.run_cli("--json", "--offline")
        self.assertEqual(len(self.fetch.calls), calls_before)
        self.assertEqual(json.loads(text)["summary"]["counts"]["VERIFIED"], 2)

    def test_human_report_is_readable_and_german(self):
        code, text = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("VERIFIED", text)
        self.assertIn("knowledge/themen/t.md:2", text)
        self.assertIn("kein Gegenbeweis", text)
        self.assertIn("ECLI:DE:BGH:2025:091025UIZR159.24.0", text)

    def test_cache_dir_inside_repo_is_rejected(self):
        out = io.StringIO()
        err = io.StringIO()
        target = cli.ROOT / "tests" / "_must_not_exist_cache"
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(target)],
                       fetch=self.fetch, sleep=lambda s: None, stdout=out, stderr=err)
        self.assertEqual(code, 2)
        self.assertFalse(target.exists())

    def test_dry_run_requires_write_ecli(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            self.run_cli("--dry-run")
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
