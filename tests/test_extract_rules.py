"""Offline tests for date binding, court assignment and input limits of citation_check.extract."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import extract


def found(text: str):
    return extract.extract_citations(text, "knowledge/themen/x.md")


def dates(text: str) -> dict[str, str | None]:
    return {c.az: c.date for c in found(text)}


class DateBindingTests(unittest.TestCase):
    def test_vom_date_binds_to_the_az_on_its_left(self):
        self.assertEqual(dates("BFH VI R 1/20 vom 3.3.2021, X B 12/20"),
                         {"VI R 1/20": "2021-03-03", "X B 12/20": None})

    def test_date_before_az_binds_to_the_az_on_its_right(self):
        self.assertEqual(dates("Urteil vom 12.12.2019, I ZR 173/16"), {"I ZR 173/16": "2019-12-12"})
        self.assertEqual(dates("12.12.2019 – I ZR 173/16"), {"I ZR 173/16": "2019-12-12"})

    def test_date_does_not_bind_across_another_az(self):
        self.assertEqual(dates("BGH I ZR 5/20 und BFH VI R 1/20 vom 3.3.2021"),
                         {"I ZR 5/20": None, "VI R 1/20": "2021-03-03"})
        self.assertEqual(dates("3.3.2021: BGH I ZR 5/20, BFH VI R 1/20"),
                         {"I ZR 5/20": "2021-03-03", "VI R 1/20": None})

    def test_ambiguous_date_between_two_az_is_not_assigned(self):
        self.assertEqual(dates("I ZR 5/20, 3.3.2021, VI R 1/20"),
                         {"I ZR 5/20": None, "VI R 1/20": None})

    def test_each_az_keeps_its_own_date(self):
        self.assertEqual(dates("BGH I ZR 5/20 v. 01.02.2020 und BFH VI R 1/20 v. 03.03.2021"),
                         {"I ZR 5/20": "2020-02-01", "VI R 1/20": "2021-03-03"})

    def test_parenthesised_date_binds_left(self):
        self.assertEqual(dates("I ZR 1/20 (3.3.2021), X B 2/20"),
                         {"I ZR 1/20": "2021-03-03", "X B 2/20": None})

    def test_single_az_line_binds_an_adjacent_date_but_not_a_distant_one(self):
        # Adjacent (only court name and brackets in between): still bound. The "nearest date"
        # fallback now needs a gap of at most 30 characters and no memo word (see test_extract_memo_dates):
        # a wrong DATE_MISMATCH is worse than no date comparison at all.
        self.assertEqual(dates("Beschluss vom 5.5.2020 (BGH I ZR 1/20)"), {"I ZR 1/20": "2020-05-05"})
        far = "BGH I ZR 1/20 " + "Fuelltext " * 8 + "5.5.2020"
        self.assertEqual(dates(far), {"I ZR 1/20": None})

    def test_correction_line_yields_no_date_but_a_flag(self):
        (citation,) = found("BGH I ZR 159/24 vom 10.10.2025 (korrigiert, statt 09.10.2025)")
        self.assertIsNone(citation.date)
        self.assertTrue(citation.correction)
        for word in ("vormals", "fälschlich", "statt"):
            (c,) = found(f"BGH I ZR 159/24 vom 10.10.2025 {word} 09.10.2025")
            self.assertTrue(c.correction, word)
            self.assertIsNone(c.date, word)

    def test_normal_line_has_no_correction_flag(self):
        (citation,) = found("BGH I ZR 159/24 vom 09.10.2025")
        self.assertFalse(citation.correction)


class CourtAssignmentTests(unittest.TestCase):
    def test_vg_az_next_to_bverwg_is_not_bverwg(self):
        result = [(c.az, c.court, c.covered) for c in found("BVerwG 6 C 12.20 und VG Köln 6 K 123/20")]
        self.assertEqual(result, [("6 C 12.20", "BVerwG", True), ("6 K 123/20", "VG Köln", False)])

    def test_instance_court_register_signs_are_not_covered(self):
        for text in ("OVG NRW 12 A 123/20", "VG Köln 6 K 123/20", "LAG Hamm 3 Sa 45/20",
                     "OVG Münster 12 LB 5/20", "OVG Berlin 3 LA 7/20", "BVerwG und OVG Münster 12 A 5/20"):
            (c,) = found(text)
            self.assertFalse(c.covered, text)

    def test_bverwg_az_needs_an_immediately_preceding_bverwg(self):
        far = "Das BVerwG hat entschieden. " + "Weiterer Text " * 8 + "Aktenzeichen 6 C 12.20 war es."
        self.assertEqual(found(far), [])

    def test_bverwg_with_date_between_court_and_az(self):
        (c,) = found("BVerwG, Urteil vom 12.3.2020 – 6 C 12.20")
        self.assertEqual((c.court, c.covered, c.date), ("BVerwG", True, "2020-03-12"))

    def test_bgh_criminal_senate(self):
        (c,) = found("BGH 5 StR 12/20")
        self.assertEqual((c.az, c.court, c.covered), ("5 StR 12/20", "BGH", True))


class UnicodeAndLimitTests(unittest.TestCase):
    def test_non_ascii_digits_are_not_an_az(self):
        self.assertEqual(found("BGH I ZR １５９/24"), [])
        self.assertEqual(found("BGH I ZR ١٥٩/24"), [])

    def test_no_break_space_and_unicode_context_are_handled(self):
        (c,) = found("„BGH“ – Urt. v. 09.10.2025 – I ZR 159/24 – Überschätzung äöüß \U0001f600")
        self.assertEqual((c.az, c.date), ("I ZR 159/24", "2025-10-09"))

    def test_empty_text_and_empty_file(self):
        self.assertEqual(found(""), [])
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge"
            (kb / "themen").mkdir(parents=True)
            (kb / "themen" / "leer.md").write_bytes(b"")
            notes: list[str] = []
            self.assertEqual(extract.scan_kb(kb, notes), [])
            self.assertEqual(notes, [])

    def test_overlong_lines_are_skipped_and_reported(self):
        text = "BGH I ZR 159/24 " + "x" * (extract.MAX_LINE_CHARS + 10) + "\nBGH VI ZR 10/24\n"
        citations, skipped = extract.extract_with_notes(text, "f.md")
        self.assertEqual([c.az for c in citations], ["VI ZR 10/24"])
        self.assertEqual(skipped, 1)

    def test_oversized_file_is_skipped_and_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge"
            (kb / "themen").mkdir(parents=True)
            (kb / "themen" / "gross.md").write_bytes(b"BGH I ZR 159/24\n" + b"x" * extract.MAX_FILE_BYTES)
            (kb / "themen" / "klein.md").write_bytes(b"BGH VI ZR 10/24\n")
            notes: list[str] = []
            citations = extract.scan_kb(kb, notes)
            self.assertEqual([c.az for c in citations], ["VI ZR 10/24"])
            self.assertEqual(len(notes), 1)
            self.assertIn("gross.md", notes[0])

    def test_many_matches_in_one_line_stay_fast(self):
        line = " ".join(f"BGH I ZR {n}/20 v. 01.01.2020" for n in range(1, 120))
        self.assertLess(len(line), extract.MAX_LINE_CHARS)
        self.assertEqual(len(found(line)), 119)


if __name__ == "__main__":
    unittest.main()
