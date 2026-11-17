"""Offline tests for client_report.textcheck, client_report.texts and client_report.models."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.models import ReportInputError, ValidationIssue
from client_report.textcheck import (
    check_texts,
    find_dashes,
    find_forbidden,
    load_forbidden_phrases,
    normalize,
)
from client_report.texts import (
    ALL_FIXED_STRINGS,
    CONFIDENTIAL,
    DISCLAIMER_FULL,
    DISCLAIMER_SHORT,
    FOOTER,
    LABEL_LEGAL_BASIS,
    LABEL_REVIEW_QUESTION,
    LABEL_RISK,
    LAWYER_SENTENCE,
    LINK_TO_PART_B,
    METHOD_TEXT,
    NOTE_VALID_FROM,
    PASS_ON_SENTENCE,
    SECTION_TITLES,
    START_HINT,
    STATUS_LABEL,
    STATUS_SHORT,
    STATUS_SYMBOL,
    SUBTITLE,
    TITLE,
)

PHRASES = load_forbidden_phrases()

# Minimum list from spec 6.8 (RDG adjustment 2026-11-17)
SPEC_MINIMUM = (
    "rechtssicher", "abmahnsicher", "100 % konform", "garantiert", "zertifiziert",
    "rechtswidrig", "Verstoß", "verstößt", "unzulässig", "illegal", "abmahnfähig",
)

# Review extension (RDG line, spec 6.8/6.10): words that state a legal verdict.
RDG_EXTENSION = (
    "konform", "widrig", "nicht zulässig", "nicht erlaubt", "verboten", "verletzt", "unwirksam",
    "nichtig", "rechtmäßig", "verstieß", "abmahnbar", "abmahngefährdet", "abmahnfest",
    "Abmahnung droht", "Bußgeld droht", "strafbar", "garantieren",
)


class ForbiddenPhrasesFile(unittest.TestCase):
    def test_contains_spec_minimum_and_a1_words(self):
        for phrase in SPEC_MINIMUM + ("bestanden", "Mangel"):
            self.assertIn(phrase, PHRASES)

    def test_contains_rdg_extension(self):
        for phrase in RDG_EXTENSION:
            self.assertIn(phrase, PHRASES)

    def test_verdict_words_in_sentences_are_found(self):
        cases = {
            "Die Seite ist DSGVO-konform.": "konform",
            "Das Banner ist widrig gestaltet.": "widrig",
            "Das Tracking ist nicht zulässig.": "nicht zulässig",
            "Das ist so nicht erlaubt.": "nicht erlaubt",
            "Das Einbinden ist verboten.": "verboten",
            "Damit wird die DSGVO verletzt.": "verletzt",
            "Die Klausel ist unwirksam.": "unwirksam",
            "Der Vertrag ist nichtig.": "nichtig",
            "Die Verarbeitung ist rechtmäßig.": "rechtmäßig",
            "Die Seite verstieß gegen Vorgaben.": "verstieß",
            "Das ist abmahnbar.": "abmahnbar",
            "Die Seite ist ABMAHNGEFÄHRDET.": "abmahngefährdet",
            "Danach ist die Seite abmahnfest.": "abmahnfest",
            "Eine Abmahnung droht.": "Abmahnung droht",
            "Ein Bussgeld droht.": "Bußgeld droht",
            "Das ist strafbar.": "strafbar",
            "Wir garantieren nichts.": "garantieren",
        }
        for text, phrase in cases.items():
            self.assertIn(phrase, find_forbidden(text, PHRASES), text)

    def test_shorter_phrase_inside_longer_one_is_reported_once(self):
        self.assertEqual(find_forbidden("Das ist rechtswidrig.", PHRASES), ["rechtswidrig"])
        self.assertEqual(find_forbidden("100 % konform", PHRASES), ["100 % konform"])
        # a separate occurrence of the shorter word is still reported
        self.assertEqual(find_forbidden("rechtswidrig und sonst widrig", PHRASES), ["rechtswidrig", "widrig"])
        self.assertEqual(find_forbidden("100 % konform, also konform", PHRASES), ["100 % konform", "konform"])

    def test_known_false_alarms_are_strict_on_purpose(self):
        # Substring matching is intentionally strict (documented in the textcheck docstring).
        self.assertIn("konform", find_forbidden("Konformitätserklärung", PHRASES))
        self.assertIn("widrig", find_forbidden("widrigenfalls", PHRASES))
        self.assertEqual(find_forbidden("Das wird berücksichtigt.", PHRASES), [])

    def test_default_path_does_not_depend_on_cwd(self):
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                self.assertEqual(load_forbidden_phrases(), PHRASES)
            finally:
                os.chdir(old)

    def test_explicit_path_with_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "phrases.json"
            path.write_bytes(b"\xef\xbb\xbf" + json.dumps({"version": 1, "phrases": ["foo"]}).encode())
            self.assertEqual(load_forbidden_phrases(path), ("foo",))

    def test_malformed_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "phrases.json"
            for payload in ({"version": 1}, {"version": 1, "phrases": ["ok", ""]},
                            {"version": 1, "phrases": "x"}, [], {"version": 2, "phrases": ["x"]}):
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(ValueError, msg=payload):
                    load_forbidden_phrases(path)


class Normalize(unittest.TestCase):
    def test_variants_of_forbidden_phrase_are_found(self):
        for text in ["Das VERSTÖSST gegen", "das verstoesst", "ein Verstoss", "Ver­stoß", "Ver​stoß"]:
            self.assertTrue(find_forbidden(text, PHRASES), text)

    def test_more_spelling_variants(self):
        for text in ["mehrere Verstöße", "zwei Mängel", "Maengel", "UNZULAESSIG", "rechts-widrig",
                     "abmahn‑sicher", "Ver‌stoß", "Ver‍stoß", "﻿illegal", "100%konform",
                     "Ab­mahn­fähig"]:
            self.assertTrue(find_forbidden(text, PHRASES), text)

    def test_percent_with_nbsp_matches(self):
        self.assertEqual(find_forbidden("100 %  konform", PHRASES), ["100 % konform"])

    def test_narrow_nbsp_matches(self):
        self.assertEqual(find_forbidden("100 % konform", PHRASES), ["100 % konform"])

    def test_returns_original_phrase_once(self):
        self.assertEqual(find_forbidden("rechtswidrig und RECHTSWIDRIG", PHRASES), ["rechtswidrig"])

    def test_harmless_words_pass(self):
        self.assertEqual(find_forbidden("Ist die Aussage zulässig gestaltet? Keine Garantie.", PHRASES), [])

    def test_normalize_is_casefolded_and_transliterated(self):
        self.assertEqual(normalize("Straße  ÄRGER x"), normalize("strasse aerger x"))


class Bypasses(unittest.TestCase):
    """Review findings: invisible characters, compatibility forms, minus signs, homoglyphs."""

    def test_invisible_format_and_filler_characters_are_removed(self):
        invisible = [
            "‎", "‏", "‪", "‮", "⁡", "⁤", "⁦", "⁩",
            "؜", "\U000e0041", "\U000e0001", "᠎", "­", "͏", "ᅟ",
            "ᅠ", "ㅤ", "︀", "️", "﻿", "​",
        ]
        for ch in invisible:
            text = f"Das ist ver{ch}boten und Ver{ch}stoß und il{ch}legal."
            found = find_forbidden(text, PHRASES)
            for phrase in ("verboten", "Verstoß", "illegal"):
                self.assertIn(phrase, found, f"U+{ord(ch):04X}")

    def test_fullwidth_letters_are_recognised(self):
        self.assertIn("illegal", find_forbidden("Das ist ｉｌｌｅｇａｌ.", PHRASES))
        self.assertIn("rechtssicher", find_forbidden("ＲＥＣＨＴＳＳＩＣＨＥＲ", PHRASES))

    def test_minus_like_characters_inside_word_count_as_hyphen(self):
        for ch in ("−", "－", "﹣"):
            self.assertIn("rechtswidrig", find_forbidden(f"rechts{ch}widrig", PHRASES), f"U+{ord(ch):04X}")
            self.assertIn("unzulässig", find_forbidden(f"un{ch}zulässig", PHRASES), f"U+{ord(ch):04X}")

    def test_homoglyphs_of_latin_letters_are_folded(self):
        cases = {
            "Vеrstoß": "Verstoß",            # Cyrillic e
            "іllegal": "illegal",                  # Cyrillic i
            "ıllegal": "illegal",                  # dotless i
            "gаrantiert": "garantiert",            # Cyrillic a
            "reсhtssiсher": "rechtssicher",   # Cyrillic c
            "verbоten": "verboten",                # Cyrillic o
            "ΑBMAHNFÄHIG": "abmahnfähig",     # Greek capital alpha
            "ILLΕGAL": "illegal",                  # Greek capital epsilon
            "ΜΑΝGEL": "Mangel",          # Greek capitals mu, alpha, nu
            "VERSTΟẞ": "Verstoß",             # Greek omicron, capital sharp s
            "abmahnfähig р": "abmahnfähig",        # Cyrillic er (looks like p) does not break
            "aрр strаfbаr": "strafbar",
            "Χ garantіeren": "garantieren",   # Greek capital chi, Cyrillic i
        }
        for text, phrase in cases.items():
            self.assertIn(phrase, find_forbidden(text, PHRASES), text)

    def test_line_break_inside_word_is_not_joined(self):
        # Joining lines would merge separate words and cause false alarms (decision in the review).
        self.assertNotIn("Verstoß", find_forbidden("Ver\nstoß", PHRASES))


class Dashes(unittest.TestCase):
    def test_em_en_and_spaced_hyphen(self):
        self.assertEqual(len(find_dashes("A — B")), 1)
        self.assertEqual(len(find_dashes("A – B")), 1)
        self.assertEqual(len(find_dashes("A - B")), 1)
        self.assertEqual(len(find_dashes("A - B")), 1)

    def test_dash_range_and_unspaced_dashes(self):
        for ch in ("‒", "–", "—", "―"):
            self.assertEqual(len(find_dashes(f"A{ch}B")), 1, hex(ord(ch)))

    def test_zero_width_around_spaced_hyphen(self):
        self.assertEqual(len(find_dashes("A ​- B")), 1)
        self.assertEqual(len(find_dashes("A - B")), 1)

    def test_compound_hyphen_allowed(self):
        self.assertEqual(find_dashes("Cookie-Banner, E-Mail, Website-CheckUp"), [])

    def test_double_and_triple_hyphen_as_dash(self):
        for text in ("A -- B", "A --- B", "A--B", "Banner--fehlt", "Banner---fehlt", "A ‐‐ B",
                     "A −− B", "A －－ B", "A ﹣ B", "A ---- B", "Banner​--fehlt", "Banner -- fehlt."):
            self.assertEqual(len(find_dashes(text)), 1, repr(text))

    def test_each_spaced_hyphen_counts(self):
        self.assertEqual(len(find_dashes("A - B - C")), 2)

    def test_no_false_alarm_for_compounds_and_ranges(self):
        for text in ("E-Mail", "DSGVO-Hinweis", "01.01.2026-31.12.2026", "Cookie-Banner-Text",
                     "Seiten 3-5", "Hinweis (z. B. Opt-in)"):
            self.assertEqual(find_dashes(text), [], text)

    def test_double_hyphen_message_is_dash_free(self):
        issues = check_texts([("x", "Banner--fehlt und A --- B")], PHRASES)
        self.assertEqual(len(issues), 2)
        for issue in issues:
            self.assertEqual(find_dashes(issue.message), [], issue.message)
            self.assertIn("U+002D", issue.message)

    def test_bullet_allowed(self):
        self.assertEqual(find_dashes(TITLE), [])


class CheckTexts(unittest.TestCase):
    def test_issue_carries_field_path(self):
        issues = check_texts([("results[3].client_text", "Das ist rechtswidrig.")], PHRASES)
        self.assertEqual(issues[0].path, "results[3].client_text")

    def test_dash_issue_and_clean_text(self):
        issues = check_texts([("summary.sentences[0]", "Banner — fehlt"), ("risk", "Alles ruhig.")], PHRASES)
        self.assertEqual([i.path for i in issues], ["summary.sentences[0]"])

    def test_both_kinds_reported(self):
        issues = check_texts([("x", "Verstoß — klar")], PHRASES)
        self.assertEqual(len(issues), 2)

    def test_issue_messages_are_dash_free(self):
        issues = check_texts([("x", "Verstoß — klar")], PHRASES)
        for issue in issues:
            self.assertEqual(find_dashes(issue.message.replace("—", "")), [])


class Models(unittest.TestCase):
    def test_validation_issue_str(self):
        self.assertEqual(str(ValidationIssue("results[0].id", "fehlt")), "results[0].id: fehlt")

    def test_report_input_error_keeps_issues(self):
        issues = [ValidationIssue("a", "b"), ValidationIssue("c", "d")]
        err = ReportInputError(issues)
        self.assertEqual(err.issues, issues)
        self.assertIn("a: b", str(err))
        self.assertIn("c: d", str(err))


class FixedStrings(unittest.TestCase):
    def test_fixed_strings_pass_own_checks(self):
        for s in ALL_FIXED_STRINGS:
            self.assertEqual(find_forbidden(s, PHRASES), [], s)
            self.assertEqual(find_dashes(s.replace(STATUS_SYMBOL["none"], "")), [], s)

    def test_fixed_strings_pass_full_list_and_dash_check(self):
        # Only documented exception: the status symbol "–" for "Nicht prüfbar / nicht anwendbar".
        # It is a stand-alone template element, never part of a sentence.
        self.assertEqual(find_dashes(STATUS_SYMBOL["none"]), ["–"])
        for s in ALL_FIXED_STRINGS:
            self.assertEqual(find_forbidden(s, PHRASES), [], s)
            if s != STATUS_SYMBOL["none"]:
                self.assertEqual(find_dashes(s), [], s)
        for word in RDG_EXTENSION:
            self.assertIn(word, PHRASES)

    def test_disclaimers_contain_required_parts(self):
        for s in (DISCLAIMER_SHORT, DISCLAIMER_FULL):
            self.assertIn("§ 2 RDG", s)
            self.assertIn("keine rechtsberatung", s.lower())
        self.assertIn("keine rechtsberatung", FOOTER.lower())

    def test_exact_texts_from_spec(self):
        self.assertEqual(TITLE, "Website-CheckUp • Technik, Datenschutz & Sicherheit")
        self.assertEqual(SUBTITLE, "KI-gestützte technische Ersteinschätzung")
        self.assertEqual(PASS_ON_SENTENCE, "Technische Ersteinschätzung, keine Rechtsberatung. "
                                           "Dieser Bericht ersetzt keine anwaltliche Prüfung.")
        self.assertEqual(LAWYER_SENTENCE, "Wir empfehlen, die rechtliche Bewertung dieses Punktes durch eine "
                                          "Rechtsanwältin oder einen Rechtsanwalt vornehmen zu lassen.")
        self.assertEqual(FOOTER, "KI-gestützte technische Ersteinschätzung. Kann Fehler enthalten. "
                                 "Keine Rechtsberatung, keine Garantie.")
        self.assertEqual(START_HINT, "Hinweis: Nutzen Sie den Website-CheckUp für eigene Kunden im Rahmen "
                                     "Ihrer Webleistung. Bieten oder bewerben Sie ihn nicht als eigenständigen "
                                     "Rechtscheck (§ 5 RDG).")
        self.assertEqual(CONFIDENTIAL, "Vertraulich")
        self.assertEqual(LABEL_LEGAL_BASIS, "Betroffene Vorschrift (zur Prüfung)")
        self.assertEqual(LABEL_RISK, "Warum das wichtig sein kann")
        self.assertEqual(LABEL_REVIEW_QUESTION, "Prüffrage für Ihre Rechtsberatung")

    def test_status_labels(self):
        self.assertEqual(STATUS_SYMBOL, {"pass": "✓", "notice": "▲", "defect": "✕", "none": "–"})
        self.assertEqual(STATUS_LABEL, {"pass": "Kein Befund im geprüften Umfang", "notice": "Hinweis",
                                        "defect": "Auffällig", "none": "Nicht prüfbar / nicht anwendbar"})
        self.assertEqual(STATUS_SHORT, {"pass": "Kein Befund", "notice": "Hinweis",
                                        "defect": "Auffällig", "none": "Nicht prüfbar / nicht anwendbar"})

    def test_no_bestanden_or_mangel_anywhere(self):
        for s in ALL_FIXED_STRINGS:
            low = s.lower()
            self.assertNotIn("bestanden", low, s)
            self.assertNotIn("mangel", low, s)
            self.assertNotIn("mängel", low, s)

    def test_section_titles_and_templates(self):
        self.assertEqual(set(SECTION_TITLES), {"overview", "part_a", "part_b", "appendix_a", "appendix_b",
                                               "appendix_c", "appendix_d", "top_actions", "summary"})
        self.assertEqual(SECTION_TITLES["part_a"], "Teil A • Für Sie als Inhaberin oder Inhaber")
        self.assertEqual(LINK_TO_PART_B.format(id="CK-03"), "Details für Ihre Technik: Teil B, CK-03")
        self.assertEqual(NOTE_VALID_FROM.format(date="28.06.2025"), "Pflicht gilt ab 28.06.2025.")

    def test_method_text_has_four_to_six_sentences(self):
        self.assertTrue(4 <= METHOD_TEXT.count(". ") + 1 <= 6, METHOD_TEXT)
        for part in ("passiv", "Stichprobe", "WCAG", "Momentaufnahme", "Logins", "keine rechtliche Bewertung"):
            self.assertIn(part, METHOD_TEXT)

    def test_all_fixed_strings_complete(self):
        for s in (TITLE, SUBTITLE, PASS_ON_SENTENCE, LAWYER_SENTENCE, DISCLAIMER_SHORT, DISCLAIMER_FULL,
                  FOOTER, START_HINT, CONFIDENTIAL, METHOD_TEXT, *STATUS_LABEL.values(),
                  *STATUS_SHORT.values(), *STATUS_SYMBOL.values(), *SECTION_TITLES.values()):
            self.assertIn(s, ALL_FIXED_STRINGS)


if __name__ == "__main__":
    unittest.main()
