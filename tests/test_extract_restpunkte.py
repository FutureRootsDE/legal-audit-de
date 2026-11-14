"""Offline tests: paren-date binding, run day parameter, court fallback in judgment files, short-form lists."""
from __future__ import annotations

import unittest

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import extract

TODAY = "2026-11-14"
BVERWG_HEAD = "# BVerwG Testurteil\n\n**Gericht:** BVerwG\n\n"
BVERWG_FILE = "knowledge/urteile/bverwg-test.md"


def found(text: str, rel: str = "knowledge/themen/x.md", today: str = TODAY):
    return extract.extract_citations(text, rel, today=today)


def dates(text: str) -> dict[str, str | None]:
    return {c.az: c.date for c in found(text)}


class ParenDateBeforeNextAz(unittest.TestCase):
    def test_real_pangv_line_does_not_bind_the_date_to_the_next_az(self):
        line = '  = "OeKO-TEST I" (Unionsmarke, 12.12.2019), I ZR 143/19 = "Knuspermuesli II"'
        self.assertEqual(dates(line), {"I ZR 143/19": None})

    def test_date_in_paren_after_az_stays_with_the_left_az(self):
        self.assertEqual(dates("BGH I ZR 173/16 (Urt. v. 12.12.2019), I ZR 143/19 folgt"),
                         {"I ZR 173/16": "2019-12-12", "I ZR 143/19": None})

    def test_paren_date_with_text_before_the_closing_bracket(self):
        self.assertEqual(dates("I ZR 173/16 (Unionsmarke, 12.12.2019) und I ZR 143/19"),
                         {"I ZR 173/16": None, "I ZR 143/19": None})

    def test_closing_bracket_after_spaces_blocks_the_right_binding(self):
        self.assertEqual(dates("(Stand frueher, 12.12.2019 ) I ZR 143/19"), {"I ZR 143/19": None})

    def test_positive_cases_still_bind(self):
        self.assertEqual(dates("Urteil vom 18.11.2024 – VI ZR 10/24"), {"VI ZR 10/24": "2024-11-18"})
        self.assertEqual(dates("VI ZR 10/24 (Urt. v. 18.11.2024)"), {"VI ZR 10/24": "2024-11-18"})


class RunDayParameter(unittest.TestCase):
    def test_date_on_or_after_the_run_day_is_no_decision_date(self):
        text = "BGH I ZR 159/24 vom 14.11.2026"
        self.assertIsNone(found(text, today="2026-11-14")[0].date)
        self.assertEqual(found(text, today="2026-11-15")[0].date, "2026-11-14")

    def test_scan_and_line_level_functions_accept_the_parameter(self):
        citations, _ = extract.extract_with_notes("BGH I ZR 159/24 vom 01.01.2026\n", "f.md", today="2026-01-01")
        self.assertIsNone(citations[0].date)


class CourtFallbackInJudgmentFiles(unittest.TestCase):
    def cites(self, line: str):
        return [(c.az, c.court, c.covered) for c in found(BVERWG_HEAD + line + "\n", BVERWG_FILE)]

    def test_own_az_without_court_name_is_attributed(self):
        self.assertEqual(self.cites("Aktenzeichen 6 C 12.20 im Volltext"), [("6 C 12.20", "BVerwG", True)])

    def test_vorinstanz_az_is_not_attributed_to_the_file_court(self):
        for line in ("Vorinstanz: 4 A 123/19", "vorgehend 4 A 123/19", "nachgehend 4 A 123/19",
                     "Berufungsgericht 4 A 123/19", "Instanz OVG, 4 A 123/19", "EuGH-Vorlage 4 A 123/19"):
            self.assertFalse([c for c in self.cites(line) if c[2]], line)

    def test_signal_in_the_line_also_blocks_a_register_that_would_fit(self):
        (_, _, covered), = self.cites("Vorinstanz: 6 C 12.20")
        self.assertFalse(covered)

    def test_explicit_bverwg_name_still_wins_over_the_signal(self):
        self.assertEqual(self.cites("Vorinstanz OVG 4 A 123/19, danach BVerwG 6 C 12.20"),
                         [("4 A 123/19", "OVG", False), ("6 C 12.20", "BVerwG", True)])

    def test_register_that_does_not_fit_is_not_covered(self):
        (_, _, covered), = self.cites("Aktenzeichen 4 A 123/19 im Volltext")
        self.assertFalse(covered)

    def test_other_files_do_not_use_the_fallback(self):
        self.assertEqual(found("Aktenzeichen 6 C 12.20 im Volltext"), [])


class ShortFormLists(unittest.TestCase):
    def azs(self, text: str):
        return [(c.az, c.court, c.covered) for c in found(text)]

    def test_real_kb_line_comma_list(self):
        line = ("alle Pflicht-Normzitate bestaetigt; BGH-Aktenzeichen I ZR 90/20, 125/20, 126/20 "
                "(09.09.2021 — Influencer-Trilogie)")
        self.assertEqual(self.azs(line), [("I ZR 90/20", "BGH", True), ("I ZR 125/20", "BGH", True),
                                          ("I ZR 126/20", "BGH", True)])

    def test_mixed_full_and_short_form_with_und(self):
        self.assertEqual([a for a, *_ in self.azs("I ZR 90/20, I ZR 125/20 und 126/20")],
                         ["I ZR 90/20", "I ZR 125/20", "I ZR 126/20"])

    def test_sowie_connector(self):
        self.assertEqual([a for a, *_ in self.azs("BGH I ZR 90/20 sowie 125/20")], ["I ZR 90/20", "I ZR 125/20"])

    def test_other_register_and_court(self):
        self.assertEqual(self.azs("BFH VI R 1/20, 2/20"), [("VI R 1/20", "BFH", True), ("VI R 2/20", "BFH", True)])

    def test_no_follow_up_after_rn_or_norm_citations(self):
        self.assertEqual([a for a, *_ in self.azs("BGH I ZR 90/20, Rn. 12/13")], ["I ZR 90/20"])
        self.assertEqual([a for a, *_ in self.azs("BGH I ZR 90/20, Art. 6/26 DSGVO")], ["I ZR 90/20"])
        self.assertEqual([a for a, *_ in self.azs("BGH I ZR 90/20 und § 12/13 UWG")], ["I ZR 90/20"])

    def test_no_follow_up_for_longer_numbers_or_dates(self):
        self.assertEqual([a for a, *_ in self.azs("BGH I ZR 90/20, 5/2021")], ["I ZR 90/20"])
        self.assertEqual([a for a, *_ in self.azs("BGH I ZR 90/20, 12.05/21")], ["I ZR 90/20"])

    def test_date_after_the_list_binds_to_the_last_member_only(self):
        result = {c.az: c.date for c in found("BGH I ZR 90/20, 125/20 v. 09.09.2021")}
        self.assertEqual(result, {"I ZR 90/20": None, "I ZR 125/20": "2021-09-09"})


if __name__ == "__main__":
    unittest.main()
