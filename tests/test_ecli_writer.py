"""Offline tests for --write-ecli."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import api, cache, cli
from support import FakeFetch, fixture_bytes, OK_I_ZR_159, OK_VI_ZR_10, GOOD_ECLI, GOOD_HIT


URTEIL_FRONT = (
    "---\n"
    "aktualisiert: 2026-05-08\n"
    "verifiziert-am: 2026-05-08\n"
    "geltungsbereich: [DE]\n"
    "---\n"
    "\n"
    "# BGH I ZR 159/24 — „Button“\n"
    "\n"
    "| Feld | Wert |\n"
    "|------|------|\n"
    "| **Aktenzeichen** | I ZR 159/24 |\n"
    "| **Datum** | 09.10.2025 |\n"
    "\n"
    "Text mit Umlauten äöü.\n"
)


class WriteEcliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "urteile").mkdir(parents=True)
        (self.kb / "themen").mkdir(parents=True)
        self.cache = self.tmp / "cache"
        self.fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159, "VI ZR 10/24": OK_VI_ZR_10})

    def write(self, rel: str, text: str, eol: str = "\n") -> Path:
        path = self.kb / rel
        path.write_bytes(text.replace("\n", eol).encode("utf-8"))
        return path

    def run_cli(self, *args, fetch=None):
        out = io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.cache), *args],
                       fetch=fetch or self.fetch, sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def test_inserts_exactly_one_line_lf(self):
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        code, _ = self.run_cli("--write-ecli")
        self.assertEqual(code, 0)
        after = path.read_bytes()
        expected = before.replace(
            b"geltungsbereich: [DE]\n---\n",
            b"geltungsbereich: [DE]\necli: ECLI:DE:BGH:2025:091025UIZR159.24.0\n---\n", 1)
        self.assertEqual(after, expected)
        self.assertEqual(after.count(b"\n"), before.count(b"\n") + 1)

    def test_crlf_preserved(self):
        path = self.write("urteile/a.md", URTEIL_FRONT, eol="\r\n")
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        after = path.read_bytes()
        self.assertIn(b"ecli: ECLI:DE:BGH:2025:091025UIZR159.24.0\r\n---\r\n", after)
        self.assertEqual(after.count(b"\n"), after.count(b"\r\n"))
        self.assertEqual(len(after), len(before) + len(b"ecli: ECLI:DE:BGH:2025:091025UIZR159.24.0\r\n"))

    def test_existing_ecli_untouched(self):
        text = URTEIL_FRONT.replace("geltungsbereich: [DE]\n", "geltungsbereich: [DE]\necli: ECLI:DE:BGH:1:2\n")
        path = self.write("urteile/a.md", text)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_dry_run_writes_nothing_and_lists_proposal(self):
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        code, text = self.run_cli("--write-ecli", "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(path.read_bytes(), before)
        self.assertIn("ECLI:DE:BGH:2025:091025UIZR159.24.0", text)
        self.assertIn("a.md", text)

    def test_default_never_writes(self):
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        self.run_cli()
        self.assertEqual(path.read_bytes(), before)

    def test_only_urteile_directory(self):
        path = self.write("themen/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_not_verified_is_skipped(self):
        path = self.write("urteile/a.md", URTEIL_FRONT.replace("09.10.2025", "10.10.2025"))
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_not_covered_court_is_skipped(self):
        text = URTEIL_FRONT.replace("BGH I ZR 159/24", "EuGH C-252/21").replace("| I ZR 159/24 |", "| C-252/21 |")
        path = self.write("urteile/a.md", text)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_ambiguous_without_date_is_skipped(self):
        text = (URTEIL_FRONT.replace("I ZR 159/24", "VI ZR 10/24")
                .replace("| **Datum** | 09.10.2025 |\n", ""))
        path = self.write("urteile/a.md", text)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_ambiguous_resolved_by_date(self):
        text = URTEIL_FRONT.replace("I ZR 159/24", "VI ZR 10/24").replace("09.10.2025", "31.10.2024")
        path = self.write("urteile/a.md", text)
        self.run_cli("--write-ecli")
        self.assertIn(b"ecli: ECLI:DE:BGH:2024:311024BVIZR10.24.0\n", path.read_bytes())

    def test_date_label_entscheidungstermin_is_understood(self):
        text = (URTEIL_FRONT.replace("I ZR 159/24", "VI ZR 10/24")
                .replace("| **Datum** | 09.10.2025 |", "- **Entscheidungstermin:** **31.10.2024**"))
        path = self.write("urteile/a.md", text)
        self.run_cli("--write-ecli")
        self.assertIn(b"ecli: ECLI:DE:BGH:2024:311024BVIZR10.24.0\n", path.read_bytes())

    def test_malformed_ecli_from_api_is_rejected(self):
        body = json.loads(fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
        body["member"][0]["item"]["ecli"] = "ECLI:DE:BGH:2025:1\ninjected: yes"
        fetch = FakeFetch({"I ZR 159/24": (200, json.dumps(body).encode("utf-8"))})
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        self.run_cli("--write-ecli", fetch=fetch)
        self.assertEqual(path.read_bytes(), before)

    def test_no_frontmatter_is_skipped(self):
        path = self.write("urteile/a.md", "# BGH I ZR 159/24\n| **Aktenzeichen** | I ZR 159/24 |\n")
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_no_temp_files_left_behind(self):
        self.write("urteile/a.md", URTEIL_FRONT)
        self.run_cli("--write-ecli")
        self.assertEqual(sorted(p.name for p in (self.kb / "urteile").iterdir()), ["a.md"])

    def test_json_reports_ecli_updates(self):
        self.write("urteile/a.md", URTEIL_FRONT)
        _, text = self.run_cli("--write-ecli", "--dry-run", "--json")
        data = json.loads(text)
        self.assertEqual(data["ecli_updates"][0]["ecli"], "ECLI:DE:BGH:2025:091025UIZR159.24.0")
        self.assertEqual(data["ecli_updates"][0]["written"], False)


class WriteEcliIgnoresCacheTests(unittest.TestCase):
    POISONED = "ECLI:DE:BGH:2025:999999UIZR159.24.0"

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "urteile").mkdir(parents=True)
        self.cache = self.tmp / "cache"
        self.cache.mkdir()
        self.file = self.kb / "urteile" / "a.md"
        self.file.write_bytes(URTEIL_FRONT.encode("utf-8"))
        self.fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})
        poisoned = dict(GOOD_HIT, ecli=self.POISONED)
        client = api.ApiClient(fetch=self.fetch, cache_dir=self.cache, sleep=lambda s: None)
        client.cache.write("BGH", "I ZR 159/24", [poisoned])

    def run_cli(self, *args, fetch=None):
        out = io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.cache), *args],
                       fetch=fetch or self.fetch, sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def test_write_uses_fresh_query_not_poisoned_cache(self):
        code, _ = self.run_cli("--write-ecli")
        self.assertEqual(code, 0)
        data = self.file.read_bytes()
        self.assertIn(f"ecli: {GOOD_ECLI}\n".encode(), data)
        self.assertNotIn(self.POISONED.encode(), data)
        self.assertGreaterEqual(len(self.fetch.calls_for("I ZR 159/24")), 1)

    def test_dry_run_may_use_cache_but_never_writes(self):
        before = self.file.read_bytes()
        _, text = self.run_cli("--write-ecli", "--dry-run")
        self.assertEqual(self.file.read_bytes(), before)
        self.assertIn(self.POISONED, text)

    def test_write_with_offline_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            self.run_cli("--write-ecli", "--offline")
        self.assertEqual(ctx.exception.code, 2)
        self.assertEqual(self.file.read_bytes(), URTEIL_FRONT.encode("utf-8"))

    def test_fresh_result_is_not_written_to_cache(self):
        self.run_cli("--write-ecli")
        entry = json.loads(next(self.cache.glob("*.json")).read_text(encoding="utf-8"))
        self.assertEqual(entry["hits"][0]["ecli"], self.POISONED)

    def test_ecli_outside_strict_pattern_is_not_written(self):
        for bad in ("ECLI:EU:C:2020:559", "ECLI:DE:BGH:2025:091025uizr159", "ECLI:DE:BGH:25:1",
                    "ECLI:DE:BGH:2025:AB-C", "ECLI:DE:BGH:2025:1 2"):
            body = json.loads(fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
            body["member"][0]["item"]["ecli"] = bad
            fetch = FakeFetch({"I ZR 159/24": (200, json.dumps(body).encode("utf-8"))})
            before = self.file.read_bytes()
            code, text = self.run_cli("--write-ecli", fetch=fetch)
            self.assertEqual(code, 0, bad)
            self.assertEqual(self.file.read_bytes(), before, bad)
            self.assertRegex(text, r"Uebersprungen: [1-9]")


if __name__ == "__main__":
    unittest.main()
