"""Offline tests for client_report.schema: findings.json input validation (spec 6.3, 6.9.1, 6.9.2, 6.10)."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.catalog import APPLICABILITY_KEYS, load_catalog
from client_report.models import ReportInputError
from client_report.schema import (
    PROSE_PATHS,
    SCHEMA_VERSION,
    SEVERITIES,
    STATUSES,
    iter_prose,
    load_findings,
    validate_input,
)
from client_report_support import make_report_dir, open_result, valid_findings

CAT = load_catalog()


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.rd = make_report_dir(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def paths(self, findings):
        return [i.path for i in validate_input(findings, CAT, self.rd)]


class Constants(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(SCHEMA_VERSION, "1.0")
        self.assertEqual(STATUSES, ("pass", "notice", "defect", "none"))
        self.assertEqual(SEVERITIES, ("CRIT", "HIGH", "MED", "LOW"))
        self.assertIn("results[].client_action", PROSE_PATHS)
        self.assertNotIn("results[].evidence[].excerpt", PROSE_PATHS)


class LoadFindings(Base):
    def test_bom_file_loads(self):
        p = self.rd / "findings.json"
        p.write_bytes(b"\xef\xbb\xbf" + json.dumps(valid_findings(CAT)).encode("utf-8"))
        self.assertEqual(load_findings(p)["schema_version"], "1.0")

    def test_invalid_json_reports_line(self):
        p = self.rd / "findings.json"
        p.write_text('{\n  "schema_version": "1.0",\n  oops\n}', encoding="utf-8")
        with self.assertRaises(ReportInputError) as ctx:
            load_findings(p)
        self.assertIn("Zeile 3", str(ctx.exception))

    def test_non_object_and_missing_file(self):
        p = self.rd / "findings.json"
        p.write_text("[]", encoding="utf-8")
        with self.assertRaises(ReportInputError):
            load_findings(p)
        with self.assertRaises(ReportInputError):
            load_findings(self.rd / "missing.json")


class InputValidation(Base):
    def test_valid_findings_pass(self):
        self.assertEqual(validate_input(valid_findings(CAT), CAT, self.rd), [])

    def test_valid_open_results_pass(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "defect", "HIGH"), open_result("UWG-01", "notice", "LOW")])
        self.assertEqual(validate_input(f, CAT, self.rd), [])

    def test_defect_on_legal_judgment_is_error(self):
        f = valid_findings(CAT, results=[open_result("UWG-01", "defect", "HIGH")])
        issues = validate_input(f, CAT, self.rd)
        self.assertTrue(any(i.path.startswith("results[0].status") for i in issues))
        self.assertTrue(any("Prüffrage" in i.message for i in issues))

    def test_defect_with_max_status_notice_is_error(self):
        f = valid_findings(CAT, shop=True, results=[open_result("SHOP-07", "defect", "MED")])
        self.assertIn("results[0].status", self.paths(f))

    def test_not_applicable_from_model_is_error(self):
        none = {"id": "A11Y-02", "status": "none", "reason_kind": "not_applicable", "reason": "Kein Shop."}
        f = valid_findings(CAT, results=[none])
        self.assertIn("results[0].reason_kind", self.paths(f))

    def test_not_checkable_is_accepted_and_reason_kind_only_with_none(self):
        none = {"id": "SHOP-04", "status": "none", "reason_kind": "not_checkable",
                "reason": "Der Bestellbutton liegt hinter einer Eingabe."}
        self.assertEqual(self.paths(valid_findings(CAT, shop=True, results=[none])), [])
        odd = open_result("CK-03", "notice", "LOW") | {"reason_kind": "not_checkable"}
        self.assertIn("results[0].reason_kind", self.paths(valid_findings(CAT, results=[odd])))

    def test_severity_mapping(self):
        f = valid_findings(CAT, results=[
            open_result("CK-01", "defect", "LOW"),
            open_result("CK-02", "notice", "HIGH"),
            {"id": "CK-04", "status": "pass", "severity": "MED", "one_liner": "Nichts beobachtet."},
        ])
        self.assertEqual(self.paths(f), ["results[0].severity", "results[1].severity", "results[2].severity"])

    def test_severity_original_must_be_null(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "notice", "MED") | {"severity_original": "HIGH"}])
        self.assertEqual(self.paths(f), ["results[0].severity_original"])

    def test_unknown_status(self):
        f = valid_findings(CAT, results=[{"id": "CK-03", "status": "ok", "one_liner": "x"}])
        self.assertIn("results[0].status", self.paths(f))

    def test_unknown_and_duplicate_ids(self):
        f = valid_findings(CAT, results=[open_result("XX-99", "notice", "LOW"), open_result("CK-03", "notice", "LOW"),
                                         open_result("CK-03", "notice", "LOW")])
        self.assertEqual(self.paths(f), ["results[0].id", "results[2].id"])

    def test_unknown_result_field_rejected(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "notice", "LOW") | {"client_actoin": "x"}])
        self.assertEqual(self.paths(f), ["results[0].client_actoin"])

    def test_summary_needs_exactly_three_sentences(self):
        f = valid_findings(CAT, summary={"sentences": ["Eins.", "Zwei."], "top_actions": []})
        self.assertEqual(self.paths(f), ["summary.sentences"])

    def test_top_actions_must_name_known_ids(self):
        f = valid_findings(CAT, summary={"sentences": ["Eins.", "Zwei.", "Drei."], "top_actions": ["ZZ-01", 3]})
        self.assertEqual(self.paths(f), ["summary.top_actions[0]", "summary.top_actions[1]"])

    def test_more_than_25_pages_rejected(self):
        f = valid_findings(CAT)
        f["run"]["pages_visited"] = [f"https://www.example.de/p{i}" for i in range(26)]
        self.assertEqual(self.paths(f), ["run.pages_visited"])

    def test_run_rules(self):
        f = valid_findings(CAT)
        f["run"].update(started_utc="2026-11-17 09:12", finished_utc="2026-11-17T08:00:00Z",
                        target_url="ftp://example.de/", final_url="javascript:alert(1)")
        self.assertEqual(sorted(self.paths(f)), ["run.final_url", "run.started_utc", "run.target_url"])
        g = valid_findings(CAT)
        g["run"]["finished_utc"] = "2026-11-17T08:00:00Z"
        self.assertEqual(self.paths(g), ["run.finished_utc"])
        h = valid_findings(CAT)
        h["run"]["domain"] = "andere.de"
        self.assertEqual(self.paths(h), ["run.domain"])

    def test_applicability_shape(self):
        f = valid_findings(CAT)
        f["applicability"]["shop"] = {"value": "ja", "source": "user"}
        f["applicability"]["b2c"] = {"value": True, "source": ""}
        del f["applicability"]["ai_chat"]
        f["applicability"]["newsletter"] = {"value": False, "source": "user"}
        self.assertEqual(sorted(self.paths(f)), ["applicability.ai_chat", "applicability.b2c.source",
                                                 "applicability.newsletter", "applicability.shop.value"])

    def test_applicability_accepts_null_and_note(self):
        f = valid_findings(CAT, subscription=None)
        f["applicability"]["bfsg"]["note"] = "Kleinstunternehmen"
        self.assertEqual(self.paths(f), [])
        self.assertEqual(set(f["applicability"]), set(APPLICABILITY_KEYS))

    def test_issuer_and_client(self):
        f = valid_findings(CAT, client={"address": ["x"]})
        f["issuer"]["logo_file"] = "../logo.png"
        f["issuer"]["accent_color"] = "red"
        self.assertEqual(sorted(self.paths(f)), ["client", "issuer.accent_color", "issuer.logo_file"])

    def test_versions_must_match(self):
        f = valid_findings(CAT, schema_version="2.0", catalog_version="2025.01-1")
        self.assertEqual(sorted(self.paths(f)), ["catalog_version", "schema_version"])

    def test_missing_blocks_and_unknown_top_level(self):
        f = valid_findings(CAT)
        del f["run"], f["results"]
        f["extra"] = 1
        self.assertEqual(sorted(self.paths(f)), ["extra", "results", "run"])

    def test_reference_must_be_https(self):
        r = open_result("CK-03", "notice", "LOW") | {"references": ["javascript:alert(1)", "http://x.de/", "https://ok.de/a",
                                                                   "https://", 'https://x.de/"onmouseover=1']}
        self.assertEqual(self.paths(valid_findings(CAT, results=[r])),
                         ["results[0].references[0]", "results[0].references[1]", "results[0].references[3]",
                          "results[0].references[4]"])

    def test_evidence_rules(self):
        r = open_result("CK-03", "notice", "LOW")
        r["evidence"] = [
            {"kind": "screenshot", "file": "evidence/shot.png", "caption": "x"},       # alt missing
            {"kind": "screenshot", "file": "assets/logo.svg", "alt": "x"},            # wrong suffix (and missing)
            {"kind": "video", "excerpt": "x"},                                         # unknown kind
            {"kind": "network", "file": "..\\x.json"},                                 # traversal
            {"kind": "dom"},                                                           # neither file nor excerpt
        ]
        self.assertEqual(self.paths(valid_findings(CAT, results=[r])),
                         ["results[0].evidence[0].alt", "results[0].evidence[1].file", "results[0].evidence[2].kind",
                          "results[0].evidence[3].file", "results[0].evidence[4]"])

    def test_fix_effort_rules(self):
        r = open_result("CK-03", "notice", "LOW")
        r["fix"]["effort"] = {"level": "klein", "minutes": 0}
        r["fix"]["snippets"] = [{"target": "css", "lang": "css", "code": 5}]
        self.assertEqual(self.paths(valid_findings(CAT, results=[r])),
                         ["results[0].fix.snippets[0].code", "results[0].fix.effort.level", "results[0].fix.effort.minutes"])
        r2 = open_result("CK-03", "notice", "LOW")
        r2["fix"]["effort"]["minutes"] = True
        self.assertEqual(self.paths(valid_findings(CAT, results=[r2])), ["results[0].fix.effort.minutes"])

    def test_field_types(self):
        r = open_result("CK-03", "notice", "LOW") | {"client_text": ["x"], "checklist": "x", "retest": {"how": 1}}
        self.assertEqual(self.paths(valid_findings(CAT, results=[r])),
                         ["results[0].client_text", "results[0].retest.how", "results[0].checklist"])

    def test_forbidden_phrase_reports_field_path(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "defect", "HIGH") | {"client_text": "Das verstößt gegen § 25 TDDDG."}])
        self.assertIn("results[0].client_text", self.paths(f))

    def test_dash_in_prose_reported(self):
        r = open_result("CK-03", "notice", "LOW")
        r["fix"]["steps"] = ["Erst das – dann jenes."]
        r["evidence"][0]["caption"] = "Banner - Ansicht"
        self.assertEqual(self.paths(valid_findings(CAT, results=[r])),
                         ["results[0].fix.steps[0]", "results[0].evidence[0].caption"])

    def test_verbatim_fields_not_text_checked(self):
        r = open_result("CK-03", "notice", "LOW")
        r["evidence"][1]["excerpt"] = "a – b rechtswidrig"
        r["retest"]["command"] = "curl -sI https://x - y"
        r["retest"]["expected"] = "Verstoß — garantiert"
        r["fix"]["snippets"][0]["code"] = "/* illegal - zertifiziert */"
        self.assertEqual(validate_input(valid_findings(CAT, results=[r]), CAT, self.rd), [])

    def test_all_issues_collected(self):
        f = valid_findings(CAT, results=[open_result("UWG-01", "defect", "LOW") | {"client_text": "Das ist illegal."}])
        f["run"]["target_url"] = "ftp://x"
        self.assertGreaterEqual(len(validate_input(f, CAT, self.rd)), 4)

    def test_not_a_dict(self):
        self.assertEqual([i.path for i in validate_input([], CAT, self.rd)], ["findings"])  # type: ignore[arg-type]

    def test_input_not_mutated(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "defect", "HIGH")])
        before = copy.deepcopy(f)
        validate_input(f, CAT, self.rd)
        self.assertEqual(f, before)

    def test_messages_dash_free(self):
        f = valid_findings(CAT, results=[open_result("UWG-01", "defect", "LOW")], summary={})
        for issue in validate_input(f, CAT, self.rd):
            self.assertNotRegex(issue.message, "[–—]| - ", msg=issue)


class IterProse(unittest.TestCase):
    def test_concrete_paths(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "notice", "LOW")])
        paths = dict(iter_prose(f))
        self.assertIn("summary.sentences[2]", paths)
        self.assertIn("results[0].client_action", paths)
        self.assertIn("results[0].fix.steps[1]", paths)
        self.assertIn("results[0].evidence[0].alt", paths)
        self.assertIn("results[0].retest.how", paths)
        self.assertNotIn("results[0].retest.command", paths)
        self.assertNotIn("results[0].evidence[1].excerpt", paths)
        self.assertNotIn("run.target_url", paths)

    def test_tolerates_wrong_types(self):
        self.assertEqual(list(iter_prose({"results": "x", "summary": {"sentences": [1, None]}})), [])


if __name__ == "__main__":
    unittest.main()
