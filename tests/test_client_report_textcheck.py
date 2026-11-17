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


class ForbiddenPhrasesFile(unittest.TestCase):
    def test_contains_spec_minimum_and_a1_words(self):
        for phrase in SPEC_MINIMUM + ("bestanden", "Mangel"):
            self.assertIn(phrase, PHRASES)

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
