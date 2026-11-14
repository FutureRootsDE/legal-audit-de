"""Offline tests for the write path of --write-ecli: failures, lost updates, links, court codes."""
from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import api, cli, ecli_writer
from support import FakeFetch, GOOD_ECLI, OK_I_ZR_159, OK_VI_ZR_10, fixture_bytes

FRONT = (
    "---\naktualisiert: 2026-05-08\ngeltungsbereich: [DE]\n---\n\n# BGH {az}\n\n"
    "| **Aktenzeichen** | {az} |\n| **Datum** | {date} |\n\nText.\n"
)


def can_symlink(tmp: Path) -> bool:
    probe = tmp / "probe-link"
    try:
        probe.symlink_to(tmp, target_is_directory=True)
    except (OSError, NotImplementedError):
        return False
    probe.unlink()
    return True


class EcliBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "urteile").mkdir(parents=True)
        self.cache = self.tmp / "cache"
        self.fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159, "VI ZR 10/24": OK_VI_ZR_10})

    def write(self, name: str, az="I ZR 159/24", date="09.10.2025") -> Path:
        path = self.kb / "urteile" / name
        path.write_bytes(FRONT.format(az=az, date=date).encode("utf-8"))
        return path

    def run_cli(self, *args, fetch=None):
        out = io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.cache), *args],
                        fetch=fetch or self.fetch, sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def client(self, fetch=None):
        return api.ApiClient(fetch=fetch or self.fetch, cache_dir=None, sleep=lambda s: None)


class WriteFailureTests(EcliBase):
    def test_write_error_is_reported_and_other_files_are_still_processed(self):
        first = self.write("a.md")
        second = self.write("b.md", az="VI ZR 10/24", date="31.10.2024")
        real = ecli_writer.atomic_write

        def flaky(path, data):
            if path.name == "a.md":
                raise OSError("Platte voll")
            real(path, data)

        with mock.patch.object(ecli_writer, "atomic_write", flaky):
            code, text = self.run_cli("--write-ecli")
        self.assertEqual(code, 3)
        self.assertIn("a.md", text)
        self.assertIn("Platte voll", text)
        self.assertNotIn(b"ecli:", first.read_bytes())
        self.assertIn(b"ecli: ECLI:DE:BGH:2024:311024BVIZR10.24.0", second.read_bytes())

    def test_write_error_in_json(self):
        self.write("a.md")
        with mock.patch.object(ecli_writer, "atomic_write", side_effect=OSError("kein Zugriff")):
            code, text = self.run_cli("--write-ecli", "--json")
        data = json.loads(text)
        self.assertEqual(code, 3)
        self.assertEqual(data["ecli_failed"][0]["file"], "knowledge/urteile/a.md")
        self.assertFalse(data["ecli_updates"][0]["written"])

    def test_success_exit_code_stays_zero(self):
        self.write("a.md")
        self.assertEqual(self.run_cli("--write-ecli")[0], 0)


class LostUpdateTests(EcliBase):
    def test_file_changed_between_plan_and_write_is_skipped(self):
        path = self.write("a.md")
        updates, _ = ecli_writer.plan_ecli_updates(self.kb, self.client(), fresh=True)
        self.assertEqual(len(updates), 1)
        changed = path.read_bytes() + b"\nNachtrag eines Redakteurs\n"
        path.write_bytes(changed)
        result = ecli_writer.apply_updates(updates, self.kb)
        self.assertEqual((result.written, result.failed), ([], []))
        self.assertIn("geaendert", result.skipped[0]["reason"])
        self.assertEqual(path.read_bytes(), changed)

    def test_unchanged_file_is_written(self):
        path = self.write("a.md")
        updates, _ = ecli_writer.plan_ecli_updates(self.kb, self.client(), fresh=True)
        result = ecli_writer.apply_updates(updates, self.kb)
        self.assertEqual(len(result.written), 1)
        self.assertIn(f"ecli: {GOOD_ECLI}".encode(), path.read_bytes())


class SingleQueryTests(EcliBase):
    def test_write_mode_queries_each_az_once(self):
        self.write("a.md")
        (self.kb / "themen").mkdir()
        (self.kb / "themen" / "t.md").write_text("BGH I ZR 159/24\n", encoding="utf-8")
        self.run_cli("--write-ecli")
        self.assertEqual(len(self.fetch.calls_for("I ZR 159/24")), 1)

    def test_dry_run_without_cache_queries_each_az_once(self):
        self.write("a.md")
        self.run_cli("--write-ecli", "--dry-run", "--no-cache")
        self.assertEqual(len(self.fetch.calls_for("I ZR 159/24")), 1)


class LinkTests(EcliBase):
    def test_symlinked_file_is_rejected(self):
        if not can_symlink(self.tmp):
            self.skipTest("Symlinks nicht erstellbar")
        outside = self.tmp / "outside.md"
        outside.write_bytes(FRONT.format(az="I ZR 159/24", date="09.10.2025").encode("utf-8"))
        before = outside.read_bytes()
        (self.kb / "urteile" / "link.md").symlink_to(outside)
        code, text = self.run_cli("--write-ecli")
        self.assertEqual(code, 0)
        self.assertEqual(outside.read_bytes(), before)
        self.assertIn("Symlink", text)

    def test_symlinked_urteile_directory_is_rejected(self):
        if not can_symlink(self.tmp):
            self.skipTest("Symlinks nicht erstellbar")
        real = self.tmp / "real-urteile"
        real.mkdir()
        target = real / "a.md"
        target.write_bytes(FRONT.format(az="I ZR 159/24", date="09.10.2025").encode("utf-8"))
        before = target.read_bytes()
        shutil.rmtree(self.kb / "urteile")
        (self.kb / "urteile").symlink_to(real, target_is_directory=True)
        code, text = self.run_cli("--write-ecli")
        self.assertEqual(target.read_bytes(), before)
        self.assertIn("Symlink", text)

    def test_apply_refuses_path_outside_urteile(self):
        outside = self.tmp / "elsewhere.md"
        outside.write_bytes(b"x")
        update = ecli_writer.EcliUpdate("knowledge/urteile/x.md", outside, "I ZR 1/20", GOOD_ECLI, b"y",
                                        ecli_writer.digest_of(b"x"), False)
        result = ecli_writer.apply_updates([update], self.kb)
        self.assertEqual(result.written, [])
        self.assertEqual(outside.read_bytes(), b"x")


class CourtCodeTests(EcliBase):
    def other_court_fetch(self, ecli: str):
        body = json.loads(fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
        body["member"][0]["item"]["ecli"] = ecli
        return FakeFetch({"I ZR 159/24": (200, json.dumps(body).encode("utf-8"))})

    def test_ecli_of_another_court_is_not_written(self):
        path = self.write("a.md")
        before = path.read_bytes()
        code, text = self.run_cli("--write-ecli", fetch=self.other_court_fetch("ECLI:DE:BFH:2025:091025UIZR159.24.0"))
        self.assertEqual(code, 0)
        self.assertEqual(path.read_bytes(), before)
        self.assertIn("passt nicht zum Gericht", text)

    def test_matching_court_code_is_written(self):
        path = self.write("a.md")
        self.run_cli("--write-ecli")
        self.assertIn(b"ECLI:DE:BGH:", path.read_bytes())

    def test_court_code_table_covers_all_seven_courts(self):
        self.assertEqual(set(ecli_writer.ECLI_COURT_CODES),
                         {"BGH", "BFH", "BVerwG", "BAG", "BSG", "BVerfG", "BPatG"})


class FrontmatterTests(EcliBase):
    def test_unclosed_frontmatter_is_skipped(self):
        path = self.kb / "urteile" / "a.md"
        path.write_bytes(b"---\naktualisiert: 2026-05-08\n\n# BGH I ZR 159/24\n| **Aktenzeichen** | I ZR 159/24 |\n")
        before = path.read_bytes()
        code, text = self.run_cli("--write-ecli")
        self.assertEqual(code, 0)
        self.assertEqual(path.read_bytes(), before)
        self.assertIn("kein Frontmatter", text)

    def test_empty_file_is_skipped(self):
        path = self.kb / "urteile" / "leer.md"
        path.write_bytes(b"")
        code, _ = self.run_cli("--write-ecli")
        self.assertEqual((code, path.read_bytes()), (0, b""))

    def test_non_utf8_file_is_skipped(self):
        path = self.kb / "urteile" / "latin.md"
        path.write_bytes(b"---\n---\n\xff\xfe")
        self.assertEqual(self.run_cli("--write-ecli")[0], 0)


if __name__ == "__main__":
    unittest.main()
