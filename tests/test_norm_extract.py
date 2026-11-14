"""Offline tests: extraction of norm citations and BGBl. references."""
from __future__ import annotations

import unittest

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import norm_extract as ne


def refs(text: str) -> list[tuple]:
    out = ne.extract_text(text, "knowledge/themen/x.md")
    return [(r.law, r.kind, r.art, r.number, r.absaetze, r.saetze) for r in out.norms]


class ParagraphForms(unittest.TestCase):
    def test_simple_paragraph(self):
        self.assertEqual(refs("siehe § 356a BGB."), [("BGB", "§", None, "356a", (), ())])
        self.assertEqual(refs("§ 25 TDDDG"), [("TDDDG", "§", None, "25", (), ())])

    def test_absatz_and_satz(self):
        self.assertEqual(refs("§ 5a Abs. 4 Satz 2 UWG"), [("UWG", "§", None, "5a", (4,), (2,))])
        self.assertEqual(refs("§ 5a Abs. 4 S. 3 UWG"), [("UWG", "§", None, "5a", (4,), (3,))])
        self.assertEqual(refs("§ 312k Absatz 1 Satz 1 BGB"), [("BGB", "§", None, "312k", (1,), (1,))])

    def test_number_lettered_items_and_literals_are_skipped(self):
        self.assertEqual(refs("§ 3 Abs. 1 Nr. 2 lit. a UWG"), [("UWG", "§", None, "3", (1,), ())])

    def test_several_absaetze(self):
        self.assertEqual(refs("§ 7 Abs. 2 Nr. 2/Abs. 3 UWG"), [("UWG", "§", None, "7", (2, 3), ())])
        self.assertEqual(refs("§ 18 Abs. 2+3 MStV")[0][4], (2, 3))
        self.assertEqual(refs("§ 1 Abs. 1 und 3 UWG")[0][4], (1, 3))

    def test_paragraph_lists(self):
        self.assertEqual([r[3] for r in refs("§§ 312j, 312k BGB")], ["312j", "312k"])
        self.assertEqual([r[3] for r in refs("§§ 305 ff. BGB")], ["305"])
        self.assertEqual([r[3] for r in refs("§ 22/§ 23 KUG")], ["22", "23"])
        self.assertEqual([r[3] for r in refs("§ 14/§ 37 BFSG")], ["14", "37"])
        self.assertEqual([r[3] for r in refs("§§ 305–310 BGB")], ["305", "310"])

    def test_article_with_paragraph(self):
        self.assertEqual(refs("Art. 246a § 1 EGBGB"), [("EGBGB", "§", "246a", "1", (), ())])
        self.assertEqual(refs("Art. 246a § 1 Abs. 2 EGBGB"), [("EGBGB", "§", "246a", "1", (2,), ())])

    def test_german_article(self):
        self.assertEqual(refs("Art. 12 GG"), [("GG", "Art", None, "12", (), ())])

    def test_several_citations_in_one_line(self):
        text = "§ 5 DDG, § 18 MStV, § 38 BDSG, § 5a Abs. 4 UWG und § 312k BGB"
        self.assertEqual([r[0] for r in refs(text)], ["DDG", "MStV", "BDSG", "UWG", "BGB"])

    def test_iVm_separates_groups(self):
        self.assertEqual([r[:4] for r in refs("§ 3a UWG i.V.m. § 8 UWG")],
                         [("UWG", "§", None, "3a"), ("UWG", "§", None, "8")])
        self.assertEqual(refs("§ 5 Abs. 1 i.V.m. § 8 UWG"), [("UWG", "§", None, "8", (), ())])


class NoCitation(unittest.TestCase):
    def test_text_after_a_paragraph_is_no_law(self):
        for text in ("§ 5 regelt das", "nach § 5 Abs. 1 der Verordnung", "§ 5 (alt)", "ab § 12. Danach", "§ 5"):
            self.assertEqual(refs(text), [], text)

    def test_capitalised_nouns_are_no_laws(self):
        self.assertEqual(refs("§ 5 Impressum"), [])
        self.assertEqual(refs("§ 7 Verweist auf"), [])

    def test_old_version_is_flagged(self):
        out = ne.extract_text("§ 8 Abs. 1 UWG a. F. und § 8 UWG", "f.md")
        self.assertEqual([(r.number, r.old_version) for r in out.norms], [("8", True), ("8", False)])


class RealKbForms(unittest.TestCase):
    def test_bare_articles_before_a_paragraph_belong_to_another_law(self):
        self.assertEqual(refs("Art. 37-39, § 38 BDSG"), [("BDSG", "§", None, "38", (), ())])
        self.assertEqual(refs("Art. 6 Abs. 1 lit. f, § 4 BDSG"), [("BDSG", "§", None, "4", (), ())])
        self.assertEqual(refs("Art. 6 lit. a + § 25 TDDDG"), [("TDDDG", "§", None, "25", (), ())])

    def test_compound_words_are_no_law_abbreviations(self):
        for text in ("§ 5 Button-Loesung", "Art. 33 DSGVO-Meldeweg", "§ 12 Opt-Out", "§ 3 DDG-Verstoss"):
            self.assertEqual(refs(text), [], text)

    def test_hyphenated_all_caps_laws_are_kept(self):
        self.assertEqual(refs("§ 3 KI-MIG"), [("KI-MIG", "§", None, "3", (), ())])

    def test_eu_directives_and_ai_act_are_counted(self):
        out = ne.extract_text("Art. 50 AI Act, Art. 5 RL und Art. 3 VO", "f.md")
        self.assertEqual((out.norms, out.eu_counts), ([], {"AI": 1, "RL": 1, "VO": 1}))


class EuLaws(unittest.TestCase):
    def test_eu_articles_are_counted_not_listed(self):
        out = ne.extract_text("Art. 6 Abs. 1 lit. a DSGVO, Art. 30/32/33 DSGVO und Art. 50 KI-VO", "f.md")
        self.assertEqual(out.norms, [])
        self.assertEqual(out.eu_counts, {"DSGVO": 4, "KI-VO": 1})

    def test_mixed_line(self):
        out = ne.extract_text("§ 25 TDDDG und Art. 6 DSGVO", "f.md")
        self.assertEqual([r.law for r in out.norms], ["TDDDG"])
        self.assertEqual(out.eu_counts, {"DSGVO": 1})


class FileLevel(unittest.TestCase):
    def test_line_numbers_and_verification_date(self):
        text = "---\naktualisiert: 2026-01-01\nverifiziert-am: \"2026-05-08\"\n---\n\nText\n§ 5 UWG\n"
        out = ne.extract_text(text, "f.md")
        self.assertEqual((out.norms[0].line, out.norms[0].verified_on), (7, "2026-05-08"))

    def test_fallback_to_aktualisiert_and_none_without_frontmatter(self):
        self.assertEqual(ne.frontmatter_verified_on("---\naktualisiert: 2026-01-02\n---\n"), "2026-01-02")
        self.assertIsNone(ne.frontmatter_verified_on("# Titel\n"))
        self.assertIsNone(ne.frontmatter_verified_on("---\naktualisiert: kein-datum\n---\n"))

    def test_overlong_lines_are_skipped_and_noted(self):
        out = ne.extract_text("§ 5 UWG " + "x" * 6000, "f.md")
        self.assertEqual(out.norms, [])
        self.assertEqual(len(out.skipped), 1)


class BgblReferences(unittest.TestCase):
    def bgbl(self, text: str) -> list[tuple]:
        return [(b.part, b.year, b.number) for b in ne.extract_text(text, "f.md").bgbl]

    def test_forms(self):
        self.assertEqual(self.bgbl("BGBl. 2026 I Nr. 322"), [("I", 2026, 322)])
        self.assertEqual(self.bgbl("(BGBl. 2025 I Nr. 301)"), [("I", 2025, 301)])
        self.assertEqual(self.bgbl("BGBl. I Nr. 322/2026"), [("I", 2026, 322)])
        self.assertEqual(self.bgbl("BGBl. I 2026 Nr. 322"), [("I", 2026, 322)])

    def test_old_page_references_are_not_taken(self):
        self.assertEqual(self.bgbl("BGBl. I S. 1414"), [])


if __name__ == "__main__":
    unittest.main()
