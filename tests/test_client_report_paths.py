"""Offline tests for client_report.paths: domain normalisation, report folders, safe evidence paths."""
from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.paths import domain_from_url, domain_slug, new_report_dir, safe_evidence_path
from client_report_support import make_report_dir, write_png


class DomainFromUrl(unittest.TestCase):
    def test_domain_normalisation(self):
        self.assertEqual(domain_from_url("https://WWW.Example.DE.:8443/x"), "example.de")
        self.assertEqual(domain_from_url("https://bücher.de/"), "xn--bcher-kva.de")
        self.assertEqual(domain_slug("example.de"), "example-de")

    def test_userinfo_query_and_http_are_handled(self):
        self.assertEqual(domain_from_url("http://user:pw@www.shop.example.de/a?b=c#d"), "shop.example.de")
        self.assertEqual(domain_from_url("  https://Example.de  "), "example.de")

    def test_rejected_urls(self):
        for url in ["javascript:alert(1)", "ftp://example.de/", "file:///C:/x", "https://", "example.de",
                    "https://exa mple.de/", "https://evil.de\\@example.de/", "https://[::1]/",
                    "https://example.de:99999/", "https://exa%6dple.de/", "https://a..de/", 42]:
            with self.assertRaises(ValueError, msg=repr(url)):
                domain_from_url(url)  # type: ignore[arg-type]


class DomainSlug(unittest.TestCase):
    def test_slug_keeps_punycode_and_is_bounded(self):
        self.assertEqual(domain_slug("xn--bcher-kva.de"), "xn--bcher-kva-de")
        long_slug = domain_slug("a" * 60 + "." + "b" * 40 + ".de")
        self.assertLessEqual(len(long_slug), 63)
        self.assertFalse(long_slug.endswith("-"))

    def test_slug_only_safe_characters(self):
        slug = domain_slug("Ex:ample/..\\Shop.DE")
        self.assertRegex(slug, r"^[a-z0-9-]+$")
        self.assertNotIn("..", slug)

    def test_windows_reserved_names_avoided(self):
        for name in ["con", "NUL", "com1", "lpt9", "aux", "prn"]:
            self.assertNotEqual(domain_slug(name).upper(), name.upper(), msg=name)

    def test_empty_slug_rejected(self):
        for bad in ["", "...", "::", "ä"]:
            with self.assertRaises(ValueError, msg=bad):
                domain_slug(bad)


class ReportDir(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_report_dir_never_overwrites(self):
        a = new_report_dir(self.tmp, date(2026, 11, 17), "example.de")
        b = new_report_dir(self.tmp, date(2026, 11, 17), "example.de")
        self.assertEqual((a.name, b.name), ("2026-11-17-example-de", "2026-11-17-example-de-2"))
        self.assertEqual(new_report_dir(self.tmp, date(2026, 11, 17), "example.de").name, "2026-11-17-example-de-3")

    def test_existing_file_with_same_name_is_skipped(self):
        (self.tmp / "2026-11-17-example-de").write_text("x", encoding="utf-8")
        self.assertEqual(new_report_dir(self.tmp, date(2026, 11, 17), "example.de").name, "2026-11-17-example-de-2")

    def test_report_dir_layout_and_base_created(self):
        base = self.tmp / "Kunden Berichte ä" / "client-reports"
        d = new_report_dir(base, date(2026, 1, 5), "Example.DE")
        self.assertEqual(d.name, "2026-01-05-example-de")
        self.assertTrue((d / "evidence").is_dir() and (d / "assets").is_dir())
        self.assertEqual(d.resolve().parent, base.resolve())


class EvidencePath(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.report_dir = make_report_dir(self.tmp)
        write_png(self.tmp / "outside.png", (1, 2, 3))

    def tearDown(self):
        self._tmp.cleanup()

    def test_valid_relative_path(self):
        p = safe_evidence_path(self.report_dir, "evidence/shot.png")
        self.assertEqual(p, (self.report_dir / "evidence" / "shot.png").resolve())

    def test_evidence_path_attacks_rejected(self):
        for rel in ["../x.png", "/etc/passwd", "C:\\x.png", "evidence\\..\\..\\x.png", "", "evidence/missing.png",
                    "evidence/../../outside.png", "../outside.png", "C:x.png", "c:/x.png", "\\\\server\\share\\x.png",
                    "//server/share/x.png", "evidence/shot.png:stream", "evidence/CON.png", "evidence/nul",
                    "evidence/shot.png.", "evidence/shot.png ", "./evidence/shot.png", "evidence//shot.png",
                    "evidence", "evidence/sh\x00ot.png", "   ", None, 5]:
            with self.assertRaises(ValueError, msg=repr(rel)):
                safe_evidence_path(self.report_dir, rel)  # type: ignore[arg-type]

    def test_symlink_escape_rejected(self):
        link = self.report_dir / "evidence" / "link.png"
        try:
            os.symlink(self.tmp / "outside.png", link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlinks not permitted here: {exc}")
        with self.assertRaises(ValueError):
            safe_evidence_path(self.report_dir, "evidence/link.png")

    def test_directory_link_escape_rejected(self):
        outside_dir = self.tmp / "outside"
        write_png(outside_dir / "x.png", (1, 2, 3))
        link = self.report_dir / "evidence" / "dirlink"
        try:
            if os.name == "nt":
                import _winapi  # junctions need no privilege on Windows
                _winapi.CreateJunction(str(outside_dir), str(link))
            else:
                os.symlink(outside_dir, link, target_is_directory=True)
        except (ImportError, AttributeError, OSError, NotImplementedError) as exc:
            self.skipTest(f"directory links not available: {exc}")
        with self.assertRaises(ValueError) as ctx:
            safe_evidence_path(self.report_dir, "evidence/dirlink/x.png")
        self.assertIn("außerhalb", str(ctx.exception))

    def test_error_messages_are_german_and_dash_free(self):
        for rel in ["../x.png", "/etc/x.png", "evidence/missing.png"]:
            with self.assertRaises(ValueError) as ctx:
                safe_evidence_path(self.report_dir, rel)
            self.assertNotRegex(str(ctx.exception), "[\u2013\u2014]| - ")
        self.assertIn("Report-Ordner", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
