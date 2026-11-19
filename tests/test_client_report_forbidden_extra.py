"""Second legal review (RDG, 2026-11-17): extra stems in the forbidden phrase list.

The stem "abmahn" covers every form of "Abmahnung" (inflection, compounds such as "Abmahnrisiko");
"bußgeld" covers "Bußgelder", "Bussgeld" and compounds. Prose in the shipped catalog and in the
fixture run must stay free of all of them.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.catalog import validate_catalog
from client_report.schema import iter_prose
from client_report.textcheck import check_texts, find_forbidden, load_forbidden_phrases

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "templates" / "client-test" / "catalog.json"
FIXTURE = ROOT / "tests" / "fixtures" / "client_test" / "findings_full.json"
PHRASES = load_forbidden_phrases()
NEW_STEMS = ("abmahn", "abgemahnt", "bußgeld", "unbedenklich", "ordnungsgemäß", "erfüllt die Anforderungen")


def hits(text: str) -> list[str]:
    return find_forbidden(text, PHRASES)


class ExtraStems(unittest.TestCase):
    def test_new_stems_are_listed(self):
        for stem in NEW_STEMS:
            self.assertIn(stem, PHRASES)

    def test_earlier_entries_are_kept(self):
        for phrase in ("abmahnsicher", "abmahnfähig", "abmahnbar", "abmahngefährdet", "abmahnfest",
                       "Abmahnung droht", "Bußgeld droht"):
            self.assertIn(phrase, PHRASES)

    def test_inflected_and_compound_forms_are_found(self):
        cases = {
            "Abmahnungen drohen.": "abmahn",
            "Hier besteht ein Abmahnrisiko.": "abmahn",
            "Das kann eine ABMAHNUNG auslösen.": "abmahn",
            "Mitbewerber mahnen das häufig ab, man könnte abgemahnt werden.": "abgemahnt",
            "Bußgelder drohen.": "bußgeld",
            "Ein Bussgeldverfahren ist möglich.": "bußgeld",
            "Die Einbindung ist unbedenklich.": "unbedenklich",
            "Das Impressum ist ordnungsgemäss.": "ordnungsgemäß",
            "Die ordnungsgemäße Kennzeichnung fehlt.": "ordnungsgemäß",
            "Das Banner erfüllt die Anforderungen.": "erfüllt die Anforderungen",
            "Das Banner erfuellt die Anforderungen.": "erfüllt die Anforderungen",
        }
        for text, phrase in cases.items():
            self.assertIn(phrase, hits(text), text)

    def test_longer_existing_entry_wins_over_stem(self):
        self.assertEqual(hits("Eine Abmahnung droht."), ["Abmahnung droht"])
        self.assertEqual(hits("Ein Bußgeld droht."), ["Bußgeld droht"])
        self.assertEqual(hits("Die Seite ist abmahnsicher."), ["abmahnsicher"])

    def test_neutral_wording_is_not_hit(self):
        for text in ("Das kann Rückfragen von Aufsichtsbehörden auslösen.",
                     "Die Anforderungen an Einwilligungen sind ein häufiger Prüfpunkt.",
                     "Die Schaltfläche fehlt auf der ersten Ebene."):
            self.assertEqual(hits(text), [], text)


class ShippedProseIsClean(unittest.TestCase):
    def test_catalog_prose(self):
        raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(validate_catalog(raw, PHRASES), [])

    def test_fixture_prose(self):
        findings = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(check_texts(iter_prose(findings), PHRASES), [])


if __name__ == "__main__":
    unittest.main()
