"""Offline tests for client_report.derive and .invariants (spec 6.3, 6.9.1, 6.9.2 steps 2 to 4, 6.10)."""
from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.catalog import load_catalog
from client_report.derive import check_date, derive
from client_report.invariants import check_invariants
from client_report.models import ReportInputError, ReportModel
from client_report.schema import SEVERITIES, STATUSES, validate_input
from client_report.texts import NOTE_A11Y_VOLUNTARY, NOTE_APPLICABILITY_UNCLEAR
from client_report_support import make_report_dir, open_result, pass_result, valid_findings

CAT = load_catalog()


def by_id(model: ReportModel, test_id: str):
    return next(r for r in model.results if r.entry.id == test_id)


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.rd = make_report_dir(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def derive_valid(self, findings):
        """Derive from findings that must pass step 1 (input validation) first."""
        self.assertEqual(validate_input(findings, CAT, self.rd), [])
        return derive(findings, CAT)


def berlin_day(started_utc: str) -> date:
    return check_date({"run": {"started_utc": started_utc}})


class CheckDate(unittest.TestCase):
    """Check date = calendar day in Europe/Berlin (CET/CEST), computed without tzdata."""

    def test_summer_time_evening_is_next_day(self):
        self.assertEqual(berlin_day("2026-06-18T21:59:59Z"), date(2026, 6, 18))
        self.assertEqual(berlin_day("2026-06-18T22:30:00Z"), date(2026, 6, 19))
        self.assertEqual(berlin_day("2026-06-18T23:59:59Z"), date(2026, 6, 19))

    def test_winter_time_uses_utc_plus_one(self):
        self.assertEqual(berlin_day("2026-11-17T22:59:59Z"), date(2026, 11, 17))
        self.assertEqual(berlin_day("2026-11-17T23:00:00Z"), date(2026, 11, 18))
        self.assertEqual(berlin_day("2026-12-31T23:30:00Z"), date(2027, 1, 1))

    def test_switch_days(self):
        # 2026: CEST from 29.03. 01:00 UTC to 25.10. 01:00 UTC
        self.assertEqual(berlin_day("2026-03-28T23:00:00Z"), date(2026, 3, 29))   # 00:00 CET
        self.assertEqual(berlin_day("2026-03-28T22:59:59Z"), date(2026, 3, 28))
        self.assertEqual(berlin_day("2026-03-29T00:59:59Z"), date(2026, 3, 29))   # 01:59:59 CET
        self.assertEqual(berlin_day("2026-03-29T22:00:00Z"), date(2026, 3, 30))   # 00:00 CEST
        self.assertEqual(berlin_day("2026-10-24T21:59:59Z"), date(2026, 10, 24))
        self.assertEqual(berlin_day("2026-10-24T22:00:00Z"), date(2026, 10, 25))   # 00:00 CEST
        self.assertEqual(berlin_day("2026-10-25T00:30:00Z"), date(2026, 10, 25))   # 02:30 CEST
        self.assertEqual(berlin_day("2026-10-25T22:59:59Z"), date(2026, 10, 25))   # 23:59:59 CET
        self.assertEqual(berlin_day("2026-10-25T23:00:00Z"), date(2026, 10, 26))

    def test_matches_zoneinfo_when_tzdata_is_available(self):
        from datetime import datetime, timedelta, timezone
        try:
            from zoneinfo import ZoneInfo
            berlin = ZoneInfo("Europe/Berlin")
        except Exception:  # noqa: BLE001  (no tzdata on this machine, e.g. Windows)
            self.skipTest("tzdata für Europe/Berlin nicht verfügbar")
        moment = datetime(2024, 1, 1, 0, 30, tzinfo=timezone.utc)
        while moment.year < 2029:
            stamp = moment.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.assertEqual(berlin_day(stamp), moment.astimezone(berlin).date(), msg=stamp)
            moment += timedelta(hours=1)

    def test_invalid_started_utc_raises_input_error(self):
        with self.assertRaises(ReportInputError) as ctx:
            check_date({"run": {"started_utc": "18.06.2026"}})
        self.assertEqual(ctx.exception.issues[0].path, "run.started_utc")


class Derive(Base):
    def test_shop_tests_not_applicable_without_shop(self):
        m, _ = self.derive_valid(valid_findings(CAT))  # shop False
        r = by_id(m, "SHOP-04")
        self.assertEqual((r.status, r.reason_kind, r.severity), ("none", "not_applicable", None))
        self.assertEqual(r.reason, r.entry.not_applicable_reason)

    def test_result_for_inapplicable_test_is_dropped_with_warning(self):
        m, warnings = self.derive_valid(valid_findings(CAT, results_extra=[open_result("SHOP-04", "defect", "CRIT")]))
        r = by_id(m, "SHOP-04")
        self.assertEqual((r.status, r.severity, dict(r.data)), ("none", None, {}))
        self.assertIn("SHOP-04: Ergebnis verworfen, Test nicht anwendbar", warnings)
        self.assertEqual(check_invariants(m), [])

    def test_defect_before_valid_from_becomes_notice(self):
        f = valid_findings(CAT, shop=True, started="2026-06-01T08:00:00Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        r = by_id(self.derive_valid(f)[0], "SHOP-04")
        self.assertEqual((r.status, r.severity, r.severity_original), ("notice", "MED", "CRIT"))
        self.assertIn("Pflicht gilt ab 19.06.2026.", r.notes)

    def test_defect_on_or_after_valid_from_stays(self):
        f = valid_findings(CAT, shop=True, started="2026-06-19T00:00:00Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        r = by_id(self.derive_valid(f)[0], "SHOP-04")
        self.assertEqual((r.status, r.severity, r.severity_original, r.notes), ("defect", "CRIT", None, ()))

    def test_med_defect_before_valid_from_keeps_med(self):
        f = valid_findings(CAT, shop=True, started="2026-06-01T08:00:00Z",
                           results=[open_result("SHOP-04", "defect", "MED")])
        r = by_id(self.derive_valid(f)[0], "SHOP-04")
        self.assertEqual((r.status, r.severity, r.severity_original), ("notice", "MED", "MED"))

    def test_notice_before_valid_from_gets_note_only(self):
        f = valid_findings(CAT, shop=True, started="2026-06-01T08:00:00Z",
                           results=[open_result("SHOP-03", "notice", "LOW")])
        r = by_id(self.derive_valid(f)[0], "SHOP-03")
        self.assertEqual((r.status, r.severity, r.severity_original), ("notice", "LOW", None))
        self.assertEqual(r.notes, ("Pflicht gilt ab 19.06.2026.",))

    def test_earliest_valid_from_counts_with_several_bases(self):
        # DRT-01 has bases from 2018-05-25 and 2021-12-01: one already applies, no downgrade.
        f = valid_findings(CAT, started="2020-01-01T08:00:00Z", results=[open_result("DRT-01", "defect", "HIGH")])
        r = by_id(self.derive_valid(f)[0], "DRT-01")
        self.assertEqual((r.status, r.notes), ("defect", ()))

    def test_unknown_applicability_downgrades_defect(self):
        f = valid_findings(CAT, shop=True, b2c=None, results=[open_result("SHOP-02", "defect", "HIGH")])
        r = by_id(self.derive_valid(f)[0], "SHOP-02")
        self.assertEqual((r.status, r.severity, r.severity_original), ("notice", "MED", "HIGH"))
        self.assertEqual(r.notes, (NOTE_APPLICABILITY_UNCLEAR,))

    def test_valid_from_compares_with_berlin_day(self):
        # SHOP-04 applies from 19.06.2026; 22:30 UTC on 18.06. is already 00:30 on 19.06. in Berlin.
        f = valid_findings(CAT, shop=True, started="2026-06-18T22:30:00Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        m, _ = self.derive_valid(f)
        self.assertEqual(m.check_date, date(2026, 6, 19))
        self.assertEqual((by_id(m, "SHOP-04").status, by_id(m, "SHOP-04").notes), ("defect", ()))
        g = valid_findings(CAT, shop=True, started="2026-06-18T21:59:59Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        self.assertEqual(by_id(self.derive_valid(g)[0], "SHOP-04").status, "notice")

    def test_unknown_applicability_keeps_test_applicable(self):
        m, _ = self.derive_valid(valid_findings(CAT, shop=True, b2c=None))
        self.assertEqual(by_id(m, "SHOP-02").status, "pass")
        self.assertEqual(by_id(m, "SHOP-02").notes, ())

    def test_a11y_without_bfsg_never_defect(self):
        f = valid_findings(CAT, bfsg=False, results=[open_result("A11Y-02", "defect", "HIGH")])
        r = by_id(self.derive_valid(f)[0], "A11Y-02")
        self.assertEqual((r.status, r.severity, r.severity_original), ("notice", "MED", "HIGH"))
        self.assertEqual(r.notes, (NOTE_A11Y_VOLUNTARY,))

    def test_a11y_unknown_bfsg_is_unclear(self):
        f = valid_findings(CAT, bfsg=None, results=[open_result("A11Y-02", "defect", "CRIT")])
        r = by_id(self.derive_valid(f)[0], "A11Y-02")
        self.assertEqual((r.status, r.severity, r.notes), ("notice", "MED", (NOTE_APPLICABILITY_UNCLEAR,)))

    def test_a11y_with_bfsg_stays_defect(self):
        f = valid_findings(CAT, bfsg=True, results=[open_result("A11Y-02", "defect", "HIGH")])
        r = by_id(self.derive_valid(f)[0], "A11Y-02")
        self.assertEqual((r.status, r.severity, r.severity_original, r.notes), ("defect", "HIGH", None, ()))

    def test_a11y_never_not_applicable(self):
        values = dict.fromkeys(("b2c", "shop", "bfsg", "subscription", "more_than_10_employees",
                                "platform_features", "ai_chat", "durability_guarantee"), False)
        m, _ = self.derive_valid(valid_findings(CAT, **values))
        a11y = [r for r in m.results if r.entry.area == "A11Y"]
        self.assertEqual(len(a11y), 7)
        self.assertFalse(any(r.reason_kind == "not_applicable" for r in a11y))

    def test_not_checkable_from_model_is_kept(self):
        row = {"id": "SEC-02", "status": "none", "reason_kind": "not_checkable", "reason": "Server antwortete nicht."}
        r = by_id(self.derive_valid(valid_findings(CAT, results=[row]))[0], "SEC-02")
        self.assertEqual((r.status, r.reason_kind, r.reason), ("none", "not_checkable", "Server antwortete nicht."))

    def test_counts_sum_to_catalog(self):
        m, _ = self.derive_valid(valid_findings(CAT))
        self.assertEqual(sum(m.counts.values()), 56)
        self.assertEqual(set(m.counts), set(STATUSES))
        self.assertEqual([r.entry.id for r in m.results], [e.id for e in CAT.entries])

    def test_input_is_not_mutated(self):
        f = valid_findings(CAT, shop=True, started="2026-06-01T08:00:00Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        before = repr(f)
        derive(f, CAT)
        self.assertEqual(repr(f), before)

    def test_open_results_sorted_by_severity_then_catalog(self):
        f = valid_findings(CAT, results=[open_result("SEC-02", "notice", "LOW"), open_result("CK-03", "defect", "MED"),
                                         open_result("IMP-01", "defect", "MED"), open_result("DRT-01", "defect", "CRIT")])
        m, _ = self.derive_valid(f)
        self.assertEqual([r.entry.id for r in m.open_results()], ["DRT-01", "IMP-01", "CK-03", "SEC-02"])

    def test_severity_order_matches_schema(self):
        from client_report import models
        self.assertEqual(tuple(models._SEVERITY_RANK), SEVERITIES)


class Invariants(Base):
    def issues(self, findings):
        model, _ = derive(findings, CAT)
        return check_invariants(model)

    def test_valid_model_has_no_issues(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "defect", "HIGH"), open_result("UWG-01", "notice", "MED")])
        self.assertEqual(self.issues(f), [])

    def test_downgraded_defect_needs_notice_fields_not_defect_severity(self):
        f = valid_findings(CAT, shop=True, started="2026-06-01T08:00:00Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        self.assertEqual(validate_input(f, CAT, self.rd), [])
        self.assertEqual(self.issues(f), [])

    def test_missing_required_field_reports_id(self):
        row = open_result("CK-03", "notice", "MED")
        del row["client_action"]
        issues = self.issues(valid_findings(CAT, results=[row]))
        self.assertIn("results[0].client_action", [i.path for i in issues])
        self.assertTrue(any("CK-03" in i.message for i in issues))

    def test_open_needs_evidence_fix_and_checklist(self):
        row = open_result("CK-03", "defect", "HIGH") | {"evidence": [], "checklist": []}
        row["fix"] = {"steps": [], "effort": None}
        paths = [i.path for i in self.issues(valid_findings(CAT, results=[row]))]
        for field in ("evidence", "checklist", "fix.steps", "fix.effort"):
            self.assertIn(f"results[0].{field}", paths)

    def test_pass_needs_one_liner(self):
        paths = [i.path for i in self.issues(valid_findings(CAT, results=[{"id": "IMP-01", "status": "pass"}]))]
        self.assertEqual(paths, ["results[0].one_liner"])

    def test_none_needs_reason(self):
        row = {"id": "SEC-02", "status": "none", "reason_kind": "not_checkable"}
        self.assertIn("results[0].reason", [i.path for i in self.issues(valid_findings(CAT, results=[row]))])

    def test_legal_judgment_notice_needs_review_question(self):
        row = open_result("UWG-01", "notice", "MED") | {"review_question": None}
        self.assertIn("results[0].review_question", [i.path for i in self.issues(valid_findings(CAT, results=[row]))])

    def test_measurable_notice_needs_no_review_question(self):
        row = open_result("CK-03", "notice", "MED") | {"review_question": None}
        self.assertEqual(self.issues(valid_findings(CAT, results=[row])), [])

    def test_top_actions_must_match_open_count(self):
        rows = [open_result(i, "notice", "MED") for i in ("CK-03", "SEC-02", "IMP-01", "DRT-01")]
        paths = [i.path for i in self.issues(valid_findings(CAT, results=rows, top_actions=["CK-03", "SEC-02"]))]
        self.assertIn("summary.top_actions", paths)
        paths = [i.path for i in self.issues(valid_findings(CAT, results=rows, top_actions=["CK-03", "SEC-02", "IMP-02"]))]
        self.assertIn("summary.top_actions[2]", paths)

    def test_top_actions_without_duplicates(self):
        rows = [open_result(i, "notice", "MED") for i in ("CK-03", "SEC-02", "IMP-01")]
        paths = [i.path for i in self.issues(valid_findings(CAT, results=rows, top_actions=["CK-03", "SEC-02", "CK-03"]))]
        self.assertIn("summary.top_actions[2]", paths)

    def test_top_actions_may_not_name_dropped_result(self):
        f = valid_findings(CAT, results_extra=[open_result("SHOP-04", "defect", "CRIT")], top_actions=["SHOP-04"])
        self.assertIn("summary.top_actions[0]", [i.path for i in self.issues(f)])

    def test_missing_applicable_id_reported(self):
        f = valid_findings(CAT)
        f = f | {"results": [r for r in f["results"] if r["id"] != "SEC-02"]}
        issues = self.issues(f)
        self.assertIn(("results", "SEC-02 fehlt"), [(i.path, i.message) for i in issues])

    def test_tampered_model_is_caught(self):
        m, _ = derive(valid_findings(CAT, results=[open_result("UWG-01", "notice", "MED")]), CAT)
        rows = tuple(r if r.entry.id != "UWG-01" else type(r)(**{**r.__dict__, "status": "defect", "severity": "HIGH"})
                     for r in m.results)
        bad = ReportModel(m.findings, m.check_date, rows, m.counts)
        messages = " ".join(i.message for i in check_invariants(bad))
        self.assertIn("UWG-01", messages)
        self.assertIn("Zählung", messages)


class LegalBasisOnlyFromCatalog(Base):
    """Orchestrator decision (spec 8): v1 results carry no own legal_basis; norms come from the catalog."""

    def test_result_with_legal_basis_is_rejected(self):
        row = pass_result("IMP-01") | {"legal_basis": [{"norm": "§ 1 XYZ", "valid_from": "2020-01-01", "kb_ref": "x/y.md"}]}
        paths = [i.path for i in validate_input(valid_findings(CAT, results=[row]), CAT, self.rd)]
        self.assertIn("results[0].legal_basis", paths)


if __name__ == "__main__":
    unittest.main()
