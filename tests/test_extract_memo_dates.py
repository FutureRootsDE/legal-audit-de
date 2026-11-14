"""Offline tests: dates in memo context (Stand, geprueft, eingelegt, ...) are never decision dates."""
from __future__ import annotations

import unittest
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import extract

RUN_DAY = "2026-11-14"


def dates(text: str, rel: str = "knowledge/themen/x.md") -> dict[str, str | None]:
    with mock.patch.object(extract, "run_day", return_value=RUN_DAY):
        return {c.az: c.date for c in extract.extract_citations(text, rel)}


class RealKbLines(unittest.TestCase):
    """Lines taken from the knowledge base that produced false DATE_MISMATCH reports."""

    def test_changelog_entry_with_run_day_before_az(self):
        line = "- **2026-11-14 (Review-Korrekturlauf PR #14)**: Befund zu I ZR 173/16 und"
        self.assertEqual(dates(line), {"I ZR 173/16": None})
        line = "- **2026-11-14 (Review-Korrekturlauf PR #14)**: BGH I ZR 173/16 und"
        self.assertEqual(dates(line), {"I ZR 173/16": None})

    def test_stand_date_after_pending_revision(self):
        line = "**Revision — BGH, anhaengig: I ZR 281/25** (Stand 2026-10-24 kein Endurteil)."
        self.assertEqual(dates(line), {"I ZR 281/25": None})

    def test_check_date_at_line_start(self):
        line = "- 2026-11-14: geprueft am Volltext des EuGH-Urteils C-673/17 ueber"
        self.assertEqual(dates(line), {"C-673/17": None})

    def test_appeal_filing_date_is_not_a_decision_date(self):
        line = ("- **Rechtsmittel C-703/25 P (Latombe/Kommission), eingelegt am 31.10.2025**: "
                "Latombe hat Rechtsmittel eingelegt")
        self.assertEqual(dates(line), {"C-703/25 P": None})
        line = "- **2026-11-14 (Abgleich)**: Rechtsmittel **C-703/25 P (Latombe/Kommission)**"
        self.assertEqual(dates(line), {"C-703/25 P": None})


class MemoWords(unittest.TestCase):
    def test_every_memo_word_blocks_the_date(self):
        words = ["Stand", "Stand:", "geprüft", "geprüft am", "verifiziert am", "abgerufen am", "Abruf",
                 "aktualisiert", "zuletzt geändert", "eingelegt am", "anhängig seit", "in Kraft seit",
                 "gilt ab", "anzuwenden ab", "veröffentlicht am", "BGBl. I Nr. 5 vom"]
        for word in words:
            self.assertEqual(dates(f"BGH I ZR 1/20 ({word} 03.03.2021)"), {"I ZR 1/20": None}, word)

    def test_memo_word_in_gap_blocks_the_fallback(self):
        text = "BGH I ZR 1/20 geprüft und bestätigt, 5.5.2020"
        self.assertEqual(dates(text), {"I ZR 1/20": None})

    def test_dates_on_or_after_run_day_are_never_decision_dates(self):
        self.assertEqual(dates("BGH I ZR 1/20 vom 14.11.2026"), {"I ZR 1/20": None})
        self.assertEqual(dates("BGH I ZR 1/20 vom 15.11.2026"), {"I ZR 1/20": None})
        self.assertEqual(dates("BGH I ZR 1/20 vom 13.11.2026"), {"I ZR 1/20": "2026-11-13"})

    def test_real_decision_dates_are_kept(self):
        self.assertEqual(dates("BGH, Urteil vom 12.12.2019 – I ZR 173/16"), {"I ZR 173/16": "2019-12-12"})
        self.assertEqual(dates("I ZR 1/20 vom 3.3.2021"), {"I ZR 1/20": "2021-03-03"})


class NearestDateFallback(unittest.TestCase):
    def test_single_az_line_binds_only_a_close_date(self):
        # adjacent date (court name in between) still binds
        self.assertEqual(dates("Beschluss vom 5.5.2020 (BGH I ZR 1/20)"), {"I ZR 1/20": "2020-05-05"})
        # short non-adjacent gap (at most 30 characters, no memo word) binds as before
        self.assertEqual(dates("Das Urteil des BGH I ZR 1/20 wurde am 5.5.2020 erlassen"),
                         {"I ZR 1/20": "2020-05-05"})

    def test_distant_date_is_not_bound(self):
        text = "BGH I ZR 1/20 " + "wird in der Praxis oft zitiert " * 2 + "5.5.2020"
        self.assertEqual(dates(text), {"I ZR 1/20": None})


class BverwgFileFallback(unittest.TestCase):
    ROW = "| **Aktenzeichen** | 6 C 12.20 |\n"

    def cites(self, text: str, rel: str):
        with mock.patch.object(extract, "run_day", return_value=RUN_DAY):
            return [(c.az, c.court, c.covered) for c in extract.extract_citations(text, rel)]

    def test_gericht_row_in_a_judgment_file_gives_the_court(self):
        text = "# Cookies\n\n| **Gericht** | BVerwG |\n" + self.ROW
        self.assertEqual(self.cites(text, "knowledge/urteile/x.md"), [("6 C 12.20", "BVerwG", True)])

    def test_frontmatter_and_file_name_give_the_court(self):
        self.assertEqual(self.cites("---\ngericht: BVerwG\n---\n\n" + self.ROW, "knowledge/urteile/x.md"),
                         [("6 C 12.20", "BVerwG", True)])
        self.assertEqual(self.cites(self.ROW, "knowledge/urteile/bverwg-cookies.md"),
                         [("6 C 12.20", "BVerwG", True)])

    def test_fallback_is_limited_to_judgment_files_and_bverwg(self):
        text = "| **Gericht** | BVerwG |\n" + self.ROW
        self.assertEqual(self.cites(text, "knowledge/themen/x.md"), [])
        self.assertEqual(self.cites("| **Gericht** | OVG Münster |\n" + self.ROW, "knowledge/urteile/x.md"), [])

    def test_court_named_in_the_line_wins(self):
        text = "| **Gericht** | BVerwG |\nVG Köln 6 K 123/20 und " + self.ROW
        self.assertEqual(self.cites(text, "knowledge/urteile/x.md"),
                         [("6 K 123/20", "VG Köln", False)])  # a named VG owns the following 6 C 12.20


if __name__ == "__main__":
    unittest.main()
