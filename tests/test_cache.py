"""Offline tests for citation_check.cache."""
from __future__ import annotations

import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import api, cache, cli
from support import FakeFetch, GOOD_HIT, OK_I_ZR_159, OK_EMPTY


def can_symlink(tmp: Path) -> bool:
    probe = tmp / "probe-link"
    try:
        probe.symlink_to(tmp, target_is_directory=True)
    except (OSError, NotImplementedError):
        return False
    probe.unlink()
    return True


class CacheDirTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_default_dir_is_per_user_and_not_system_temp(self):
        env = {"LOCALAPPDATA": str(self.tmp / "local"), "XDG_CACHE_HOME": str(self.tmp / "xdg")}
        with mock.patch.dict(os.environ, env):
            default = cache.default_cache_dir()
        if os.name == "nt":
            self.assertEqual(default, self.tmp / "local" / "citation-check" / "cache")
        else:
            self.assertEqual(default, self.tmp / "xdg" / "citation-check")
        self.assertNotEqual(default, Path(tempfile.gettempdir()) / "citation-check-cache")

    @unittest.skipIf(os.name == "nt", "POSIX permission bits")
    def test_created_with_mode_700(self):
        target = self.tmp / "a" / "cache"
        path, warning = cache.prepare_cache_dir(target)
        self.assertEqual((path, warning), (target, None))
        self.assertEqual(os.stat(target).st_mode & 0o777, 0o700)

    def test_symlink_disables_cache(self):
        if not can_symlink(self.tmp):
            self.skipTest("Symlinks nicht erstellbar")
        real = self.tmp / "real"
        real.mkdir()
        link = self.tmp / "link"
        link.symlink_to(real, target_is_directory=True)
        path, warning = cache.prepare_cache_dir(link)
        self.assertIsNone(path)
        self.assertIn("Symlink", warning)

    @unittest.skipIf(os.name == "nt", "POSIX permission bits")
    def test_group_writable_disables_cache(self):
        target = self.tmp / "shared"
        target.mkdir()
        os.chmod(target, 0o770)
        path, warning = cache.prepare_cache_dir(target)
        self.assertIsNone(path)
        self.assertIn("schreibbar", warning)

    @unittest.skipIf(os.name == "nt", "POSIX ownership")
    def test_foreign_owner_disables_cache(self):
        target = self.tmp / "foreign"
        target.mkdir(mode=0o700)
        with mock.patch.object(cache, "_current_uid", lambda: os.getuid() + 1):
            path, warning = cache.prepare_cache_dir(target)
        self.assertIsNone(path)
        self.assertIn("anderen Nutzer", warning)

    def test_unsafe_cache_dir_in_cli_warns_and_runs_without_cache(self):
        if not can_symlink(self.tmp):
            self.skipTest("Symlinks nicht erstellbar")
        real = self.tmp / "real"
        real.mkdir()
        link = self.tmp / "link"
        link.symlink_to(real, target_is_directory=True)
        kb = self.tmp / "knowledge" / "themen"
        kb.mkdir(parents=True)
        (kb / "t.md").write_text("BGH I ZR 159/24\n", encoding="utf-8")
        fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})
        out, err = io.StringIO(), io.StringIO()
        code = cli.main(["--path", str(self.tmp / "knowledge"), "--cache-dir", str(link)],
                       fetch=fetch, sleep=lambda s: None, stdout=out, stderr=err)
        self.assertEqual(code, 0)
        self.assertIn("WARNUNG", err.getvalue())
        self.assertEqual(list(real.iterdir()), [])
        self.assertEqual(len(fetch.calls), 1)


class CacheTamperingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.cache = self.tmp / "cache"
        self.cache.mkdir()
        self.fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})

    def client(self, **kw):
        return api.ApiClient(fetch=self.fetch, cache_dir=self.cache, sleep=lambda s: None, **kw)

    def plant(self, entry, court="BGH", az="I ZR 159/24"):
        path = self.client().cache.path(court, az)
        path.write_text(entry if isinstance(entry, str) else json.dumps(entry), encoding="utf-8")

    def entry(self, **over):
        base = {"court": "BGH", "az": "I ZR 159/24", "fetched_at": 1_000.0, "hits": [dict(GOOD_HIT)]}
        base.update(over)
        return base

    def assert_discarded(self, entry):
        self.fetch.calls.clear()
        self.plant(entry)
        client = self.client()
        client.cache.now_epoch = lambda: 1_000.0 + 60
        res = client.lookup("BGH", "I ZR 159/24")
        self.assertEqual(len(self.fetch.calls), 1, entry)
        self.assertFalse(res.from_cache)

    def test_valid_entry_is_used(self):
        self.plant(self.entry())
        client = self.client()
        client.cache.now_epoch = lambda: 1_060.0
        res = client.lookup("BGH", "I ZR 159/24")
        self.assertTrue(res.from_cache)
        self.assertEqual(self.fetch.calls, [])

    def test_manipulated_entries_are_discarded(self):
        bad_hit = dict(GOOD_HIT, ecli="ECLI:DE:BGH:2025:1\ninjected: yes")
        cases = [
            "not json {",
            "[]",
            self.entry(az="I ZR 160/24"),
            self.entry(court="BFH"),
            self.entry(hits="oops"),
            self.entry(hits=["x"]),
            self.entry(hits=[bad_hit]),
            self.entry(hits=[dict(GOOD_HIT, date="gestern")]),
            self.entry(hits=[dict(GOOD_HIT, file_numbers="I ZR 159/24")]),
            self.entry(fetched_at="1000"),
            self.entry(fetched_at=True),
            self.entry(extra="field"),
            {k: v for k, v in self.entry().items() if k != "hits"},
        ]
        for case in cases:
            with self.subTest(case=str(case)[:60]):
                self.assert_discarded(case)

    def test_stale_and_future_entries_are_discarded(self):
        self.assert_discarded(self.entry(fetched_at=1_000.0 - 8 * 24 * 3600))
        self.assert_discarded(self.entry(fetched_at=1_000.0 + 10 * 24 * 3600))

    def test_ttl_is_configurable(self):
        self.plant(self.entry())
        client = self.client(cache_ttl_seconds=10)
        client.cache.now_epoch = lambda: 1_100.0
        client.lookup("BGH", "I ZR 159/24")
        self.assertEqual(len(self.fetch.calls), 1)

    def test_cache_file_names_are_hashes_never_input(self):
        evil = "../../evil I ZR 1/24"
        self.fetch.responses[evil] = OK_EMPTY
        self.client().lookup("BGH", evil)
        names = [p.name for p in self.cache.iterdir()]
        self.assertEqual(len(names), 1)
        self.assertRegex(names[0], r"^[0-9a-f]{64}\.json$")

    def test_no_temp_leftovers_when_replace_fails(self):
        client = self.client()
        with mock.patch.object(os, "replace", side_effect=OSError("boom")):
            client.lookup("BGH", "I ZR 159/24")
        self.assertEqual(list(self.cache.iterdir()), [])
        self.assertTrue(any("Cache nicht schreibbar" in w for w in client.warnings))

    def test_written_entry_passes_own_validation(self):
        self.client().lookup("BGH", "I ZR 159/24")
        self.fetch.calls.clear()
        self.assertTrue(self.client().lookup("BGH", "I ZR 159/24").from_cache)
        self.assertEqual(self.fetch.calls, [])

    def test_no_cache_option_never_touches_disk(self):
        kb = self.tmp / "knowledge" / "themen"
        kb.mkdir(parents=True)
        (kb / "t.md").write_text("BGH I ZR 159/24\n", encoding="utf-8")
        target = self.tmp / "nocache"
        for _ in range(2):
            cli.main(["--path", str(self.tmp / "knowledge"), "--cache-dir", str(target), "--no-cache"],
                    fetch=self.fetch, sleep=lambda s: None, stdout=io.StringIO())
        self.assertFalse(target.exists())
        self.assertEqual(len(self.fetch.calls), 2)


if __name__ == "__main__":
    unittest.main()
