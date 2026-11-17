"""Offline tests for client_report.catalog and templates/client-test/catalog.json (test catalog v1)."""
from __future__ import annotations

import copy
import json
import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.catalog import (
    APPLICABILITY_KEYS,
    AREA_ORDER,
    DEFAULT_CATALOG_PATH,
    evaluate,
    load_catalog,
    validate_catalog,
)
from client_report.models import Catalog, CatalogEntry, LegalBasis, ReportInputError
from client_report.textcheck import load_forbidden_phrases

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "templates" / "client-test" / "catalog.json"
KNOWLEDGE = ROOT / "knowledge"
PHRASES = load_forbidden_phrases()


def minimal_catalog(**entry_overrides) -> dict:
    """Smallest valid catalog: all areas, one entry, one glossary item."""
    entry = {
        "id": "CK-01",
        "area": "CK",
        "title": "Keine Analyse-Requests vor Einwilligung",
        "description": "Wir prüfen, ob vor der Einwilligung Analysedienste geladen werden.",
        "legal_basis": [{"norm": "§ 25 TDDDG", "valid_from": "2021-12-01", "kb_ref": "gesetze/tdddg.md:47"}],
        "applies_if": [],
        "always_run": False,
        "basis": "measurable",
        "max_status": None,
        "not_applicable_reason": "",
        "retest_default": "Seite im privaten Fenster öffnen und das Netzwerkprotokoll ansehen.",
    }
    entry.update(entry_overrides)
    return {
        "catalog_version": "2026.11-1",
        "areas": [{"prefix": p, "title": "Bereich", "intro": "Worum es hier geht."} for p in AREA_ORDER],
        "entries": [entry],
        "glossary": [{"term": "Header", "text": "Zusatzangaben, die der Server mit jeder Seite sendet."}],
    }


def issue_paths(raw: dict) -> list[str]:
    return [i.path for i in validate_catalog(raw, PHRASES)]


class CatalogFile(unittest.TestCase):
    def setUp(self):
        self.cat = load_catalog()

    def test_default_path_is_plugin_asset(self):
        self.assertEqual(DEFAULT_CATALOG_PATH.resolve(), CATALOG_PATH.resolve())

    def test_size_and_unique_ids(self):
        ids = [e.id for e in self.cat.entries]
        self.assertEqual(len(ids), 56)
        self.assertEqual(len(set(ids)), 56)

    def test_types(self):
        self.assertIsInstance(self.cat, Catalog)
        self.assertEqual(self.cat.version, "2026.11-1")
        for e in self.cat.entries:
            self.assertIsInstance(e, CatalogEntry)
            self.assertTrue(e.legal_basis)
            self.assertTrue(all(isinstance(b, LegalBasis) and isinstance(b.valid_from, date) for b in e.legal_basis))
            self.assertIsInstance(e.applies_if, tuple)

    def test_area_counts(self):
        counts = {a: sum(1 for e in self.cat.entries if e.area == a) for a in AREA_ORDER}
        self.assertEqual(counts, {"IMP": 3, "DSE": 2, "CK": 8, "DRT": 6, "SEC": 8, "FRM": 5,
                                  "A11Y": 7, "SHOP": 10, "UWG": 3, "KI": 2, "DSA": 2})

    def test_areas_follow_area_order(self):
        self.assertEqual(tuple(a.prefix for a in self.cat.areas), AREA_ORDER)
        order = [AREA_ORDER.index(e.area) for e in self.cat.entries]
        self.assertEqual(order, sorted(order))
        for e in self.cat.entries:
            self.assertTrue(e.id.startswith(e.area + "-"), e.id)

    def test_a11y_always_run_without_conditions(self):
        a11y = [e for e in self.cat.entries if e.area == "A11Y"]
        self.assertTrue(a11y and all(e.always_run and not e.applies_if for e in a11y))
        self.assertTrue(all(not e.always_run for e in self.cat.entries if e.area != "A11Y"))

    def test_basis_per_area(self):
        for area in ("UWG", "KI", "DSA"):
            self.assertTrue(all(e.basis == "legal_judgment" for e in self.cat.entries if e.area == area))
        self.assertTrue(all(e.basis == "measurable" for e in self.cat.entries if e.area in ("SEC", "A11Y")))

    def test_basis_of_mixed_areas(self):
        judgment = {e.id for e in self.cat.entries if e.basis == "legal_judgment"}
        expected_mixed = {"IMP-03", "DSE-02", "CK-07", "DRT-06", "FRM-04", "FRM-05",
                          "SHOP-01", "SHOP-03", "SHOP-06", "SHOP-08", "SHOP-09", "SHOP-10"}
        self.assertEqual(judgment - {e.id for e in self.cat.entries if e.area in ("UWG", "KI", "DSA")},
                         expected_mixed)

    def test_pinned_dates(self):
        by = self.cat.by_id
        self.assertEqual(by["SHOP-04"].legal_basis[0].valid_from, date(2026, 6, 19))
        self.assertEqual(by["SHOP-05"].legal_basis[0].valid_from, date(2022, 7, 1))
        self.assertEqual(by["SHOP-08"].legal_basis[0].valid_from, date(2026, 9, 27))
        self.assertEqual(by["SHOP-09"].applies_if, ("shop", "b2c", "durability_guarantee"))

    def test_future_obligations_dated_exactly(self):
        by = self.cat.by_id
        for entry_id in ("SHOP-08", "SHOP-09", "UWG-01", "UWG-02"):
            self.assertEqual({b.valid_from for b in by[entry_id].legal_basis}, {date(2026, 9, 27)}, entry_id)
        for entry_id in ("KI-01", "KI-02"):
            self.assertEqual(by[entry_id].legal_basis[0].valid_from, date(2026, 8, 2))
        self.assertEqual(by["SHOP-07"].legal_basis[0].valid_from, date(2025, 7, 20))
        self.assertTrue(all(b.valid_from == date(2025, 6, 28)
                            for e in self.cat.entries if e.area == "A11Y" for b in e.legal_basis))

    def test_applicability_conditions(self):
        by = self.cat.by_id
        self.assertEqual(by["SHOP-05"].applies_if, ("b2c", "subscription"))
        self.assertEqual(by["SHOP-10"].applies_if, ("b2c", "more_than_10_employees"))
        self.assertEqual(by["KI-01"].applies_if, ("ai_chat",))
        self.assertEqual(by["DSA-01"].applies_if, ("platform_features",))
        for entry_id in ("SHOP-01", "SHOP-02", "SHOP-03", "SHOP-04", "SHOP-06", "SHOP-07", "SHOP-08"):
            self.assertEqual(by[entry_id].applies_if, ("shop", "b2c"), entry_id)
        unconditional = [e.id for e in self.cat.entries if e.area in ("IMP", "DSE", "CK", "DRT", "SEC", "FRM", "UWG")]
        self.assertTrue(all(not by[i].applies_if for i in unconditional))

    def test_conditional_entries_explain_not_applicable(self):
        for e in self.cat.entries:
            if e.applies_if:
                self.assertTrue(e.not_applicable_reason, e.id)

    def test_max_status_only_for_os_platform_link(self):
        self.assertEqual({e.id for e in self.cat.entries if e.max_status}, {"SHOP-07"})
        self.assertEqual(self.cat.by_id["SHOP-07"].max_status, "notice")

    def test_ppwr_is_no_test_but_glossary_outlook(self):
        texts = " ".join(f"{e.title} {e.description}" for e in self.cat.entries)
        self.assertNotIn("PPWR", texts)
        ppwr = [text for term, text in self.cat.glossary if "PPWR" in term]
        self.assertEqual(len(ppwr), 1)
        self.assertIn("12.08.2026", ppwr[0])
        self.assertIn("12.08.2028", ppwr[0])

    def test_glossary_contains_required_terms(self):
        terms = " ".join(term for term, _ in self.cat.glossary)
        for term in ("Consent", "Header", "HSTS", "Drittland", "Content-Security-Policy", "Lighthouse"):
            self.assertIn(term, terms)

    def test_kb_refs_point_to_existing_lines(self):
        for e in self.cat.entries:
            for b in e.legal_basis:
                rel, _, lines = b.kb_ref.partition(":")
                path = KNOWLEDGE / rel
                self.assertTrue(path.is_file(), f"{e.id}: {b.kb_ref}")
                count = len(path.read_text(encoding="utf-8").splitlines())
                for line in filter(None, lines.split(",")):
                    self.assertLessEqual(int(line), count, f"{e.id}: {b.kb_ref}")

    def test_catalog_prose_passes_text_checks(self):
        self.assertEqual(validate_catalog(json.loads(CATALOG_PATH.read_text(encoding="utf-8")), load_forbidden_phrases()), [])

    def test_descriptions_are_neutral_questions_of_fact(self):
        for e in self.cat.entries:
            self.assertTrue(e.description.startswith("Wir "), e.id)


class CatalogValidation(unittest.TestCase):
    def test_minimal_catalog_is_valid(self):
        self.assertEqual(issue_paths(minimal_catalog()), [])

    def test_unknown_applicability_key_rejected(self):
        self.assertIn("entries[0].applies_if", issue_paths(minimal_catalog(applies_if=["shopp"])))

    def test_duplicate_id_rejected(self):
        raw = minimal_catalog()
        raw["entries"].append(copy.deepcopy(raw["entries"][0]))
        self.assertIn("entries[1].id", issue_paths(raw))

    def test_bad_id_format_rejected(self):
        for bad in ("CK-3", "XX-01", "ck-01", "CK-001"):
            self.assertIn("entries[0].id", issue_paths(minimal_catalog(id=bad)), bad)

    def test_area_must_match_id_prefix(self):
        self.assertIn("entries[0].area", issue_paths(minimal_catalog(area="SEC")))

    def test_forbidden_phrase_in_title_rejected(self):
        paths = issue_paths(minimal_catalog(title="Rechtssicherer Banner"))
        self.assertTrue(any(p.endswith(".title") for p in paths), paths)

    def test_dash_in_description_rejected(self):
        self.assertIn("entries[0].description", issue_paths(minimal_catalog(description="Wir prüfen das Banner – sofort.")))

    def test_basis_and_max_status_values(self):
        self.assertIn("entries[0].basis", issue_paths(minimal_catalog(basis="judgment")))
        self.assertIn("entries[0].max_status", issue_paths(minimal_catalog(max_status="defect")))

    def test_always_run_only_for_a11y(self):
        self.assertIn("entries[0].always_run", issue_paths(minimal_catalog(always_run=True)))
        a11y = minimal_catalog(id="A11Y-01", area="A11Y", always_run=False)
        self.assertIn("entries[0].always_run", issue_paths(a11y))
        a11y = minimal_catalog(id="A11Y-01", area="A11Y", always_run=True, applies_if=["bfsg"],
                               not_applicable_reason="Keine Pflicht.")
        self.assertIn("entries[0].applies_if", issue_paths(a11y))

    def test_valid_from_must_be_iso_date(self):
        for bad in ("01.12.2021", "2021-13-01", "", None):
            raw = minimal_catalog()
            raw["entries"][0]["legal_basis"][0]["valid_from"] = bad
            self.assertIn("entries[0].legal_basis[0].valid_from", issue_paths(raw), bad)

    def test_legal_basis_required_and_kb_ref_format(self):
        self.assertIn("entries[0].legal_basis", issue_paths(minimal_catalog(legal_basis=[])))
        raw = minimal_catalog()
        raw["entries"][0]["legal_basis"][0]["kb_ref"] = "../secret.md"
        self.assertIn("entries[0].legal_basis[0].kb_ref", issue_paths(raw))

    def test_conditional_entry_needs_not_applicable_reason(self):
        self.assertIn("entries[0].not_applicable_reason", issue_paths(minimal_catalog(applies_if=["shop"])))

    def test_unknown_field_rejected(self):
        self.assertIn("entries[0].severity", issue_paths(minimal_catalog(severity="HIGH")))

    def test_entries_out_of_order_rejected(self):
        raw = minimal_catalog()
        raw["entries"].insert(0, dict(copy.deepcopy(raw["entries"][0]), id="SEC-01", area="SEC"))
        self.assertIn("entries[1].id", issue_paths(raw))

    def test_areas_must_match_area_order(self):
        raw = minimal_catalog()
        raw["areas"].reverse()
        self.assertIn("areas", issue_paths(raw))

    def test_glossary_text_checked(self):
        raw = minimal_catalog()
        raw["glossary"][0]["text"] = "Garantiert sicher."
        self.assertIn("glossary[0].text", issue_paths(raw))

    def test_not_an_object_rejected(self):
        self.assertEqual(issue_paths([]), ["catalog"])  # type: ignore[arg-type]

    def test_load_catalog_raises_with_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_text(json.dumps(minimal_catalog(id="CK-3")), encoding="utf-8")
            with self.assertRaises(ReportInputError) as ctx:
                load_catalog(path)
            self.assertIn("entries[0].id", [i.path for i in ctx.exception.issues])
            path.write_text("{ kaputt", encoding="utf-8")
            with self.assertRaises(ReportInputError) as ctx:
                load_catalog(path)
            self.assertTrue(re.search(r"Zeile 1", str(ctx.exception)))

    def test_load_catalog_accepts_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_bytes(b"\xef\xbb\xbf" + json.dumps(minimal_catalog()).encode("utf-8"))
            self.assertEqual([e.id for e in load_catalog(path).entries], ["CK-01"])


class Evaluate(unittest.TestCase):
    def test_three_valued_and(self):
        self.assertIs(evaluate([], {}), True)
        self.assertIs(evaluate(["shop"], {"shop": False}), False)
        self.assertIs(evaluate(["shop", "b2c"], {"shop": None, "b2c": False}), False)
        self.assertIsNone(evaluate(["shop", "b2c"], {"shop": None, "b2c": True}))
        self.assertIs(evaluate(["shop"], {"shop": True}), True)
        self.assertIsNone(evaluate(["shop"], {}))

    def test_applicability_keys(self):
        self.assertEqual(APPLICABILITY_KEYS, ("b2c", "shop", "bfsg", "subscription", "more_than_10_employees",
                                              "platform_features", "ai_chat", "durability_guarantee"))


if __name__ == "__main__":
    unittest.main()
