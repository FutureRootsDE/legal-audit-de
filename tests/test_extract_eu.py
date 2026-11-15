"""Offline tests: EU file numbers with suffixes, legacy numbers, name hints, short-form list dates."""
from __future__ import annotations

import unittest

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import extract, names

TODAY = "2026-11-14"


def found(text: str, rel: str = "knowledge/themen/x.md"):
    return extract.extract_citations(text, rel, today=TODAY)


def azs(text: str) -> list[str]:
    return [c.az for c in found(text)]


class EuFileNumbers(unittest.TestCase):
    def test_plain_and_hyphen_variants_are_normalised(self):
        for hyphen in "-‐‑‒–—−":
            self.assertEqual(azs(f"EuGH C{hyphen}311/18"), ["C-311/18"], hyphen)

    def test_suffixes_are_part_of_the_file_number(self):
        self.assertEqual(azs("EuGH C-703/25 P laeuft"), ["C-703/25 P"])
        self.assertEqual(azs("EuGH C-619/18 R Beschluss"), ["C-619/18 R"])
        self.assertEqual(azs("EuGH C-1/20 PPU Eilverfahren"), ["C-1/20 PPU"])
        self.assertEqual(azs("EuG T-553/23 R"), ["T-553/23 R"])

    def test_following_words_starting_with_p_or_r_are_no_suffix(self):
        self.assertEqual(azs("EuGH C-311/18 Pflicht"), ["C-311/18"])
        self.assertEqual(azs("EuGH C-311/18 Rn. 5"), ["C-311/18"])

    def test_joined_cases_give_one_citation_each(self):
        self.assertEqual(azs("EuGH, verb. Rs. C-293/12 und C-594/12"), ["C-293/12", "C-594/12"])
        self.assertEqual(azs("EuGH C-511/18, C-512/18 und C-520/18"), ["C-511/18", "C-512/18", "C-520/18"])

    def test_court_follows_the_register_letter(self):
        cites = {c.az: c.court for c in found("EuGH C-311/18 und EuG T-553/23")}
        self.assertEqual(cites, {"C-311/18": "EuGH", "T-553/23": "EuG"})

    def test_legacy_number_needs_a_court_and_a_case_marker(self):
        self.assertEqual(azs("EuGH, Rs. 26/62 (van Gend & Loos)"), ["C-26/62"])
        self.assertEqual(azs("EuG, Rechtssache 7/90"), ["T-7/90"])
        self.assertEqual(azs("Rs. 26/62 ohne Gericht"), [])
        self.assertEqual(azs("BGH Rs. 26/62"), [])

    def test_existing_citations_keep_their_covered_flag(self):
        self.assertFalse(found("EuGH C-311/18")[0].covered)


class NameCandidates(unittest.TestCase):
    def test_quotes_and_brackets_give_names(self):
        self.assertEqual(names.extract_names('EuGH C-311/18 "Schrems II" gilt'), ("Schrems II",))
        self.assertEqual(names.extract_names("EuGH C-673/17 (Planet49) vom"), ("Planet49",))
        self.assertEqual(names.extract_names("C-40/17 „Fashion ID“"), ("Fashion ID",))

    def test_dates_and_memo_words_are_no_names(self):
        self.assertEqual(names.extract_names("C-311/18 (16.07.2020)"), ())
        self.assertEqual(names.extract_names("C-311/18 (Urt. v. 16.07.2020, Rn. 5)"), ())
        self.assertEqual(names.extract_names("C-311/18 (Grosse Kammer)"), ())

    def test_name_hint_values(self):
        title = ["data", "protection", "commissioner", "facebook", "ireland", "schrems"]
        self.assertEqual(names.name_hint(("Schrems II",), title), "match")
        self.assertEqual(names.name_hint(("Planet49",), title), "no_match")
        self.assertEqual(names.name_hint((), title), "none")
        self.assertEqual(names.name_hint(("II",), title), "none")
        self.assertEqual(names.name_hint(("Schrems II",), []), "none")

    def test_names_attach_to_the_nearest_eu_citation(self):
        cite = found('EuGH C-311/18 "Schrems II" und C-673/17 (Planet49)')
        self.assertEqual({c.az: c.names for c in cite},
                         {"C-311/18": ("Schrems II",), "C-673/17": ("Planet49",)})


class ShortFormListDates(unittest.TestCase):
    def dates(self, text: str) -> dict[str, str | None]:
        return {c.az: c.date for c in found(text)}

    def test_date_after_the_list_binds_to_every_member(self):
        self.assertEqual(self.dates("I ZR 90/20, 125/20, 126/20 vom 09.09.2021"),
                         {"I ZR 90/20": "2021-09-09", "I ZR 125/20": "2021-09-09", "I ZR 126/20": "2021-09-09"})

    def test_date_before_the_list_binds_to_every_member(self):
        self.assertEqual(self.dates("Urteil vom 09.09.2021 I ZR 90/20, 125/20 und 126/20"),
                         {"I ZR 90/20": "2021-09-09", "I ZR 125/20": "2021-09-09", "I ZR 126/20": "2021-09-09"})

    def test_real_kb_lines(self):
        self.assertEqual(self.dates("BGH I ZR 90/20, I ZR 125/20 und I ZR 126/20 v. 09.09.2021"),
                         {"I ZR 90/20": None, "I ZR 125/20": None, "I ZR 126/20": "2021-09-09"})
        self.assertEqual(self.dates("(BGH I ZR 90/20, 125/20, 126/20 v. 09.09.2021)"),
                         {"I ZR 90/20": "2021-09-09", "I ZR 125/20": "2021-09-09", "I ZR 126/20": "2021-09-09"})

    def test_real_index_lines_with_bracket_dates(self):
        line = 'I ZR 90/20, 125/20, 126/20 (09.09.2021), I ZR 7/16 (28.05.2020, "Cookie-Einwilligung II")'
        self.assertEqual(self.dates(line), {"I ZR 90/20": "2021-09-09", "I ZR 125/20": "2021-09-09",
                                            "I ZR 126/20": "2021-09-09", "I ZR 7/16": "2020-05-28"})

    def test_a_date_between_members_ends_the_list(self):
        self.assertEqual(self.dates("BGH I ZR 1/20 vom 01.02.2020, 2/20"), {"I ZR 1/20": "2020-02-01"})

    def test_separate_azs_are_not_a_list(self):
        self.assertEqual(self.dates("BGH I ZR 90/20 und VI ZR 5/21 vom 09.09.2021"),
                         {"I ZR 90/20": None, "VI ZR 5/21": "2021-09-09"})


if __name__ == "__main__":
    unittest.main()
