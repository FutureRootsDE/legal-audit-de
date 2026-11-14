"""Offline tests for citation_check.extract."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import extract


class ExtractionTests(unittest.TestCase):
    def extract(self, text: str):
        return extract.extract_citations(text, "knowledge/themen/x.md")

    def one(self, text: str):
        found = self.extract(text)
        self.assertEqual(len(found), 1, found)
        return found[0]

    def test_bgh_civil_senate_numbers(self):
        for az in ("I ZR 159/24", "VIII ZR 63/15", "VI ZR 10/24", "XI ZR 26/20"):
            c = self.one(f"Siehe BGH {az} zur Sache.")
            self.assertEqual((c.az, c.court, c.covered), (az, "BGH", True), az)

    def test_other_federal_courts(self):
        cases = {
            "BVerfG 1 BvR 1234/20": ("1 BvR 1234/20", "BVerfG"),
            "BAG 8 AZR 209/21": ("8 AZR 209/21", "BAG"),
            "BFH VII R 12/20": ("VII R 12/20", "BFH"),
            "BSG B 1 KR 5/19 R": ("B 1 KR 5/19 R", "BSG"),
            "BPatG 35 W (pat) 12/20": ("35 W (pat) 12/20", "BPatG"),
            "BVerwG 6 C 12.20": ("6 C 12.20", "BVerwG"),
        }
        for text, (az, court) in cases.items():
            c = self.one(text)
            self.assertEqual((c.az, c.court, c.covered), (az, court, True), text)

    def test_bverwg_pattern_needs_court_context(self):
        self.assertEqual(self.extract("Ein Verfahren 6 C 12.20 lief."), [])

    def test_lower_courts_flagged_not_covered(self):
        c = self.one("OLG Hamburg, 5 U 104/24 zum Streichpreis")
        self.assertFalse(c.covered)
        self.assertEqual(c.court, "OLG Hamburg")
        c = self.one("LG München I, Urteil 3 O 17493/20")
        self.assertFalse(c.covered)
        self.assertTrue(c.court.startswith("LG München"))

    def test_eu_courts_flagged_not_covered(self):
        for az in ("C-252/21", "T-557/20", "C‑673/17", "C–311/18"):
            c = self.one(f"EuGH {az} Meta")
            self.assertFalse(c.covered, az)
            self.assertEqual(c.court, "EuGH")
            self.assertEqual(c.az[0], "C" if az[0] == "C" else "T")

    def test_no_false_positives(self):
        text = "Art. 82 DSGVO, § 7 Abs. 2 UWG, Version 2.4/3, 24/7 Support, EUR 19/24."
        self.assertEqual(self.extract(text), [])

    def test_date_numeric_and_written(self):
        self.assertEqual(self.one("BGH, Urt. v. 09.10.2025 - I ZR 159/24").date, "2025-10-09")
        self.assertEqual(self.one("I ZR 159/24 (BGH, 9. Oktober 2025)").date, "2025-10-09")
        self.assertIsNone(self.one("BGH I ZR 159/24 ohne Datum").date)

    def test_date_only_from_same_line(self):
        found = extract.extract_citations("Urteil vom 01.01.2020\nBGH I ZR 159/24\n", "f.md")
        self.assertIsNone(found[0].date)

    def test_pending_marker_same_line_only(self):
        found = extract.extract_citations(
            "BGH I ZR 159/24 <<VERIFIKATION AUSSTEHEND>>\nBGH VI ZR 10/24\n", "f.md")
        self.assertEqual([c.pending for c in found], [True, False])

    def test_pending_marker_with_extra_text_and_spaces(self):
        c = self.one("BGH I ZR 159/24 `<<VERIFIKATION  AUSSTEHEND — Text>>`")
        self.assertTrue(c.pending)

    def test_file_line_reference(self):
        found = extract.extract_citations("a\nb\nBGH I ZR 159/24\n", "knowledge/themen/x.md")
        self.assertEqual((found[0].file, found[0].line), ("knowledge/themen/x.md", 3))

    def test_multiple_per_line(self):
        found = self.extract("BGH I ZR 25/19 und BGH VI ZR 10/24")
        self.assertEqual([c.az for c in found], ["I ZR 25/19", "VI ZR 10/24"])

    def test_crlf_file_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge"
            (kb / "themen").mkdir(parents=True)
            (kb / "themen" / "a.md").write_bytes(b"x\r\nBGH I ZR 159/24 (09.10.2025)\r\n")
            found = extract.scan_kb(kb)
            self.assertEqual(len(found), 1)
            self.assertEqual((found[0].line, found[0].date), (2, "2025-10-09"))
            self.assertEqual(found[0].file, "knowledge/themen/a.md")


if __name__ == "__main__":
    unittest.main()
