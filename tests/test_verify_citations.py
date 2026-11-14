#!/usr/bin/env python3
"""Offline tests for scripts/verify-citations.py (no network access).

Run: python -m unittest discover -s tests -v
HTTP is replaced by an injectable fetch function; fixtures under tests/fixtures
mirror real (shortened) responses of the Rechtsinformations-API des Bundes.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "verify-citations.py"
FIXTURES = HERE / "fixtures"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_citations", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["verify_citations"] = module
    spec.loader.exec_module(module)
    return module


vc = load_module()


def fixture_bytes(name: str) -> bytes:
    return (FIXTURES / f"{name}.json").read_bytes()


class FakeFetch:
    """Scripted HTTP layer. `responses` maps file number -> (status, body) or a
    list of such tuples (consumed in order, the last one repeats)."""

    def __init__(self, responses=None, default=None):
        self.responses = responses or {}
        self.default = default
        self.calls: list[str] = []

    def __call__(self, url: str, timeout: float):
        self.calls.append(url)
        query = parse_qs(urlparse(url).query)
        key = query.get("fileNumber", [""])[0]
        entry = self.responses.get(key, self.default)
        if entry is None:
            return 200, fixture_bytes("ris_rechtsprechung_kein_treffer")
        if isinstance(entry, list):
            idx = min(len(self.calls_for(key)) - 1, len(entry) - 1)
            entry = entry[idx]
        if isinstance(entry, Exception):
            raise entry
        return entry

    def calls_for(self, key: str) -> list[str]:
        return [u for u in self.calls if parse_qs(urlparse(u).query).get("fileNumber", [""])[0] == key]


OK_I_ZR_159 = (200, fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
OK_VI_ZR_10 = (200, fixture_bytes("ris_rechtsprechung_vi_zr_10_24"))
OK_EMPTY = (200, fixture_bytes("ris_rechtsprechung_kein_treffer"))
ERR_422 = (422, fixture_bytes("ris_fehler_422"))


# ---------------------------------------------------------------- extraction
class ExtractionTests(unittest.TestCase):
    def extract(self, text: str):
        return vc.extract_citations(text, "knowledge/themen/x.md")

    def one(self, text: str):
        found = self.extract(text)
        self.assertEqual(len(found), 1, found)
        return found[0]

    def test_bgh_civil_senate_numbers(self):
        for az in ("I ZR 159/24", "VIII ZR 63/15", "VI ZR 10/24", "XI ZR 26/20"):
            c = self.one(f"Siehe BGH {az} zur Sache.")
            self.assertEqual((c.az, c.court, c.covered), (az, "BGH", True), az)

    def test_other_federal_courts(self):
        cases = {
            "BVerfG 1 BvR 1234/20": ("1 BvR 1234/20", "BVerfG"),
            "BAG 8 AZR 209/21": ("8 AZR 209/21", "BAG"),
            "BFH VII R 12/20": ("VII R 12/20", "BFH"),
            "BSG B 1 KR 5/19 R": ("B 1 KR 5/19 R", "BSG"),
            "BPatG 35 W (pat) 12/20": ("35 W (pat) 12/20", "BPatG"),
            "BVerwG 6 C 12.20": ("6 C 12.20", "BVerwG"),
        }
        for text, (az, court) in cases.items():
            c = self.one(text)
            self.assertEqual((c.az, c.court, c.covered), (az, court, True), text)

    def test_bverwg_pattern_needs_court_context(self):
        self.assertEqual(self.extract("Ein Verfahren 6 C 12.20 lief."), [])

    def test_lower_courts_flagged_not_covered(self):
        c = self.one("OLG Hamburg, 5 U 104/24 zum Streichpreis")
        self.assertFalse(c.covered)
        self.assertEqual(c.court, "OLG Hamburg")
        c = self.one("LG München I, Urteil 3 O 17493/20")
        self.assertFalse(c.covered)
        self.assertTrue(c.court.startswith("LG München"))

    def test_eu_courts_flagged_not_covered(self):
        for az in ("C-252/21", "T-557/20", "C‑673/17", "C–311/18"):
            c = self.one(f"EuGH {az} Meta")
            self.assertFalse(c.covered, az)
            self.assertEqual(c.court, "EuGH")
            self.assertEqual(c.az[0], "C" if az[0] == "C" else "T")

    def test_no_false_positives(self):
        text = "Art. 82 DSGVO, § 7 Abs. 2 UWG, Version 2.4/3, 24/7 Support, EUR 19/24."
        self.assertEqual(self.extract(text), [])

    def test_date_numeric_and_written(self):
        self.assertEqual(self.one("BGH, Urt. v. 09.10.2025 - I ZR 159/24").date, "2025-10-09")
        self.assertEqual(self.one("I ZR 159/24 (BGH, 9. Oktober 2025)").date, "2025-10-09")
        self.assertIsNone(self.one("BGH I ZR 159/24 ohne Datum").date)

    def test_date_only_from_same_line(self):
        found = vc.extract_citations("Urteil vom 01.01.2020\nBGH I ZR 159/24\n", "f.md")
        self.assertIsNone(found[0].date)

    def test_pending_marker_same_line_only(self):
        found = vc.extract_citations(
            "BGH I ZR 159/24 <<VERIFIKATION AUSSTEHEND>>\nBGH VI ZR 10/24\n", "f.md")
        self.assertEqual([c.pending for c in found], [True, False])

    def test_pending_marker_with_extra_text_and_spaces(self):
        c = self.one("BGH I ZR 159/24 `<<VERIFIKATION  AUSSTEHEND — Text>>`")
        self.assertTrue(c.pending)

    def test_file_line_reference(self):
        found = vc.extract_citations("a\nb\nBGH I ZR 159/24\n", "knowledge/themen/x.md")
        self.assertEqual((found[0].file, found[0].line), ("knowledge/themen/x.md", 3))

    def test_multiple_per_line(self):
        found = self.extract("BGH I ZR 25/19 und BGH VI ZR 10/24")
        self.assertEqual([c.az for c in found], ["I ZR 25/19", "VI ZR 10/24"])

    def test_crlf_file_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge"
            (kb / "themen").mkdir(parents=True)
            (kb / "themen" / "a.md").write_bytes(b"x\r\nBGH I ZR 159/24 (09.10.2025)\r\n")
            found = vc.scan_kb(kb)
            self.assertEqual(len(found), 1)
            self.assertEqual((found[0].line, found[0].date), (2, "2025-10-09"))
            self.assertEqual(found[0].file, "knowledge/themen/a.md")


# -------------------------------------------------------------------- client
class ClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.sleeps: list[float] = []
        self.now = 0.0

    def sleep(self, seconds: float):
        self.sleeps.append(seconds)
        self.now += seconds

    def clock(self) -> float:
        return self.now

    def client(self, fetch, **kw):
        kw.setdefault("rate", 2.0)
        return vc.ApiClient(fetch=fetch, cache_dir=self.tmp / "cache",
                            sleep=self.sleep, clock=self.clock, **kw)

    def test_hit_returns_ecli_date_type(self):
        res = self.client(FakeFetch({"I ZR 159/24": OK_I_ZR_159})).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "ok")
        self.assertEqual(len(res.hits), 1)
        hit = res.hits[0]
        self.assertEqual(hit["ecli"], "ECLI:DE:BGH:2025:091025UIZR159.24.0")
        self.assertEqual((hit["date"], hit["type"]), ("2025-10-09", "Urteil"))

    def test_multiple_hits_kept(self):
        res = self.client(FakeFetch({"VI ZR 10/24": OK_VI_ZR_10})).lookup("BGH", "VI ZR 10/24")
        self.assertEqual({h["type"] for h in res.hits}, {"Urteil", "Beschluss"})

    def test_empty_result(self):
        res = self.client(FakeFetch({"I ZR 999/99": OK_EMPTY})).lookup("BGH", "I ZR 999/99")
        self.assertEqual((res.state, res.hits), ("ok", []))

    def test_fuzzy_hits_without_exact_file_number_are_dropped(self):
        res = self.client(FakeFetch({"I ZR 160/24": OK_I_ZR_159})).lookup("BGH", "I ZR 160/24")
        self.assertEqual((res.state, res.hits), ("ok", []))

    def test_request_url_is_encoded_and_filtered_by_court(self):
        fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})
        self.client(fetch).lookup("BGH", "I ZR 159/24")
        url = fetch.calls[0]
        self.assertTrue(url.startswith("https://testphase.rechtsinformationen.bund.de/v1/rechtsprechung?"))
        self.assertIn("court=BGH", url)
        self.assertNotIn(" ", url)
        self.assertEqual(parse_qs(urlparse(url).query)["fileNumber"], ["I ZR 159/24"])

    def test_generic_user_agent(self):
        req = vc.build_request("https://example.invalid/x")
        self.assertEqual(req.get_header("User-agent"), "citation-check/1.0")

    def test_backoff_on_503_then_success(self):
        fetch = FakeFetch({"I ZR 159/24": [(503, b""), (503, b""), OK_I_ZR_159]})
        res = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "ok")
        self.assertEqual(len(fetch.calls), 3)
        waits = [s for s in self.sleeps if s >= 1.0]
        self.assertEqual(waits, [1.0, 2.0])

    def test_backoff_is_capped_and_gives_up(self):
        fetch = FakeFetch({"I ZR 159/24": (503, b"")})
        res = self.client(fetch, max_retries=6, max_backoff=4.0).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "error")
        self.assertEqual(len(fetch.calls), 7)
        self.assertLessEqual(max(self.sleeps), 4.0)

    def test_backoff_on_429_and_500(self):
        for status in (429, 500):
            fetch = FakeFetch({"I ZR 159/24": [(status, b""), OK_I_ZR_159]})
            client = vc.ApiClient(fetch=fetch, cache_dir=self.tmp / f"cache{status}",
                                  sleep=self.sleep, clock=self.clock)
            res = client.lookup("BGH", "I ZR 159/24")
            self.assertEqual((res.state, len(fetch.calls)), ("ok", 2), status)

    def test_network_error_is_error_not_exception(self):
        fetch = FakeFetch({"I ZR 159/24": urllib.error.URLError("offline")})
        res = self.client(fetch, max_retries=1).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "error")
        self.assertIn("offline", res.detail)

    def test_422_is_error_without_retry_and_reports_message(self):
        fetch = FakeFetch({"I ZR 159/24": ERR_422})
        res = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual((res.state, len(fetch.calls)), ("error", 1))
        self.assertIn("pageIndex", res.detail)

    def test_404_empty_body_means_no_hit(self):
        res = self.client(FakeFetch({"I ZR 159/24": (404, b"")})).lookup("BGH", "I ZR 159/24")
        self.assertEqual((res.state, res.hits), ("ok", []))

    def test_invalid_json_is_error(self):
        res = self.client(FakeFetch({"I ZR 159/24": (200, b"<html>")})).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "error")

    def test_cache_hit_avoids_second_request_across_clients(self):
        fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})
        first = self.client(fetch).lookup("BGH", "I ZR 159/24")
        second = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual(len(fetch.calls), 1)
        self.assertTrue(second.from_cache)
        self.assertFalse(first.from_cache)
        self.assertEqual(first.hits, second.hits)

    def test_empty_result_is_cached_errors_are_not(self):
        fetch = FakeFetch({"A": OK_EMPTY, "B": (503, b"")})
        client = self.client(fetch, max_retries=0)
        client.lookup("BGH", "A")
        client.lookup("BGH", "A")
        client.lookup("BGH", "B")
        client.lookup("BGH", "B")
        self.assertEqual((len(fetch.calls_for("A")), len(fetch.calls_for("B"))), (1, 2))

    def test_expired_cache_entry_is_refetched(self):
        fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})
        client = self.client(fetch, cache_ttl_seconds=10)
        client.lookup("BGH", "I ZR 159/24")
        client.now_epoch = lambda: 10_000_000_000.0  # far future
        client.lookup("BGH", "I ZR 159/24")
        self.assertEqual(len(fetch.calls), 2)

    def test_offline_uses_cache_only(self):
        fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159})
        self.client(fetch).lookup("BGH", "I ZR 159/24")
        offline = self.client(fetch, offline=True)
        self.assertEqual(offline.lookup("BGH", "I ZR 159/24").state, "ok")
        self.assertEqual(offline.lookup("BGH", "VI ZR 10/24").state, "unchecked")
        self.assertEqual(len(fetch.calls), 1)

    def test_rate_limit_spaces_requests(self):
        fetch = FakeFetch({})
        client = self.client(fetch, rate=2.0)
        client.lookup("BGH", "A")
        client.lookup("BGH", "B")
        client.lookup("BGH", "C")
        self.assertGreaterEqual(sum(self.sleeps), 1.0 - 1e-9)

    def test_circuit_breaker_stops_hammering_dead_api(self):
        fetch = FakeFetch(default=(503, b""))
        client = self.client(fetch, max_retries=0, breaker_threshold=3)
        states = [client.lookup("BGH", f"I ZR {n}/24").state for n in range(1, 9)]
        self.assertEqual(set(states), {"error"})
        self.assertEqual(len(fetch.calls), 3)


# ------------------------------------------------------------ classification
def make_citation(az="I ZR 159/24", court="BGH", covered=True, date=None, pending=False):
    return vc.Citation(file="knowledge/themen/x.md", line=1, az=az, court=court,
                       covered=covered, date=date, pending=pending, context="")


def lookup_ok(*hits):
    return vc.LookupResult(state="ok", hits=list(hits))


HIT = {"ecli": "ECLI:DE:BGH:2025:091025UIZR159.24.0", "date": "2025-10-09",
       "type": "Urteil", "document_number": "KORE726702025"}


class ClassificationTests(unittest.TestCase):
    def test_verified_when_date_matches(self):
        self.assertEqual(vc.classify(make_citation(date="2025-10-09"), lookup_ok(HIT)), "VERIFIED")

    def test_verified_when_kb_has_no_date(self):
        self.assertEqual(vc.classify(make_citation(), lookup_ok(HIT)), "VERIFIED")

    def test_date_mismatch(self):
        self.assertEqual(vc.classify(make_citation(date="2025-10-10"), lookup_ok(HIT)), "DATE_MISMATCH")

    def test_verified_if_date_matches_any_of_several_hits(self):
        beschluss = dict(HIT, date="2024-10-31", type="Beschluss", ecli="ECLI:X")
        self.assertEqual(
            vc.classify(make_citation(date="2024-10-31"), lookup_ok(HIT, beschluss)), "VERIFIED")

    def test_not_in_dataset(self):
        self.assertEqual(vc.classify(make_citation(), lookup_ok()), "NOT_IN_DATASET")

    def test_not_covered_never_needs_lookup(self):
        self.assertEqual(vc.classify(make_citation(court="OLG Hamburg", covered=False), None),
                         "NOT_COVERED")

    def test_error(self):
        res = vc.LookupResult(state="error", hits=[], detail="HTTP 503")
        self.assertEqual(vc.classify(make_citation(), res), "ERROR")

    def test_unchecked_offline(self):
        res = vc.LookupResult(state="unchecked", hits=[])
        self.assertEqual(vc.classify(make_citation(), res), "UNCHECKED")


# ----------------------------------------------------------------------- CLI
KB_TEXT_LF = (
    "# Thema\n"
    "BGH, Urt. v. 09.10.2025 - I ZR 159/24\n"
    "BGH VI ZR 10/24 v. 18.11.2024 <<VERIFIKATION AUSSTEHEND>>\n"
    "BGH I ZR 999/99 erfunden\n"
    "OLG Hamburg 5 U 104/24\n"
    "EuGH C-252/21\n"
    "BGH I ZR 25/19 v. 01.01.2022\n"
)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "themen").mkdir(parents=True)
        (self.kb / "themen" / "t.md").write_text(KB_TEXT_LF, encoding="utf-8", newline="")
        self.cache = self.tmp / "cache"
        self.fetch = FakeFetch({
            "I ZR 159/24": OK_I_ZR_159,
            "VI ZR 10/24": OK_VI_ZR_10,
            "I ZR 999/99": OK_EMPTY,
            "I ZR 25/19": OK_I_ZR_159,  # fuzzy, filtered out -> NOT_IN_DATASET
        })

    def run_cli(self, *args, fetch=None):
        out = io.StringIO()
        code = vc.main(["--path", str(self.kb), "--cache-dir", str(self.cache), *args],
                       fetch=fetch or self.fetch, sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def test_json_report_counts_and_fields(self):
        code, text = self.run_cli("--json")
        self.assertEqual(code, 0)
        data = json.loads(text)
        counts = data["summary"]["counts"]
        self.assertEqual(counts["VERIFIED"], 2)
        self.assertEqual(counts["NOT_IN_DATASET"], 2)
        self.assertEqual(counts["NOT_COVERED"], 2)
        self.assertEqual(counts["DATE_MISMATCH"], 0)
        by_az = {c["az"]: c for c in data["citations"]}
        self.assertEqual(by_az["VI ZR 10/24"]["pending"], True)
        self.assertEqual(len(by_az["VI ZR 10/24"]["hits"]), 2)
        self.assertEqual(by_az["I ZR 159/24"]["file"], "knowledge/themen/t.md")
        self.assertEqual(by_az["I ZR 159/24"]["line"], 2)

    def test_date_mismatch_and_strict_exit_code(self):
        (self.kb / "themen" / "t.md").write_text("BGH I ZR 159/24 v. 10.10.2025\n", encoding="utf-8")
        code, text = self.run_cli("--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(text)["summary"]["counts"]["DATE_MISMATCH"], 1)
        code, _ = self.run_cli("--json", "--strict")
        self.assertEqual(code, 1)

    def test_strict_without_mismatch_is_zero(self):
        code, _ = self.run_cli("--strict")
        self.assertEqual(code, 0)

    def test_api_down_exit_zero_with_hint(self):
        down = FakeFetch(default=urllib.error.URLError("no route"))
        code, text = self.run_cli(fetch=down)
        self.assertEqual(code, 0)
        self.assertIn("ERROR", text)
        self.assertIn("nicht erreichbar", text)

    def test_only_pending(self):
        code, text = self.run_cli("--json", "--only-pending")
        data = json.loads(text)
        self.assertEqual([c["az"] for c in data["citations"]], ["VI ZR 10/24"])

    def test_unique_az_queried_once(self):
        (self.kb / "themen" / "u.md").write_text("Nochmals BGH I ZR 159/24\n", encoding="utf-8")
        self.run_cli("--json")
        self.assertEqual(len(self.fetch.calls_for("I ZR 159/24")), 1)

    def test_not_covered_is_not_queried(self):
        self.run_cli("--json")
        queried = {parse_qs(urlparse(u).query)["fileNumber"][0] for u in self.fetch.calls}
        self.assertNotIn("5 U 104/24", queried)
        self.assertNotIn("C-252/21", queried)

    def test_offline_makes_no_requests_and_marks_unchecked(self):
        code, text = self.run_cli("--json", "--offline")
        self.assertEqual(code, 0)
        self.assertEqual(self.fetch.calls, [])
        counts = json.loads(text)["summary"]["counts"]
        self.assertEqual(counts["UNCHECKED"], 4)
        self.assertEqual(counts["NOT_COVERED"], 2)

    def test_offline_after_online_run_uses_cache(self):
        self.run_cli("--json")
        calls_before = len(self.fetch.calls)
        _, text = self.run_cli("--json", "--offline")
        self.assertEqual(len(self.fetch.calls), calls_before)
        self.assertEqual(json.loads(text)["summary"]["counts"]["VERIFIED"], 2)

    def test_human_report_is_readable_and_german(self):
        code, text = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("VERIFIED", text)
        self.assertIn("knowledge/themen/t.md:2", text)
        self.assertIn("kein Gegenbeweis", text)
        self.assertIn("ECLI:DE:BGH:2025:091025UIZR159.24.0", text)

    def test_cache_dir_inside_repo_is_rejected(self):
        out = io.StringIO()
        err = io.StringIO()
        target = vc.ROOT / "tests" / "_must_not_exist_cache"
        code = vc.main(["--path", str(self.kb), "--cache-dir", str(target)],
                       fetch=self.fetch, sleep=lambda s: None, stdout=out, stderr=err)
        self.assertEqual(code, 2)
        self.assertFalse(target.exists())

    def test_dry_run_requires_write_ecli(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            self.run_cli("--dry-run")
        self.assertEqual(ctx.exception.code, 2)


# ---------------------------------------------------------------- write-ecli
URTEIL_FRONT = (
    "---\n"
    "aktualisiert: 2026-05-08\n"
    "verifiziert-am: 2026-05-08\n"
    "geltungsbereich: [DE]\n"
    "---\n"
    "\n"
    "# BGH I ZR 159/24 — „Button“\n"
    "\n"
    "| Feld | Wert |\n"
    "|------|------|\n"
    "| **Aktenzeichen** | I ZR 159/24 |\n"
    "| **Datum** | 09.10.2025 |\n"
    "\n"
    "Text mit Umlauten äöü.\n"
)


class WriteEcliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "urteile").mkdir(parents=True)
        (self.kb / "themen").mkdir(parents=True)
        self.cache = self.tmp / "cache"
        self.fetch = FakeFetch({"I ZR 159/24": OK_I_ZR_159, "VI ZR 10/24": OK_VI_ZR_10})

    def write(self, rel: str, text: str, eol: str = "\n") -> Path:
        path = self.kb / rel
        path.write_bytes(text.replace("\n", eol).encode("utf-8"))
        return path

    def run_cli(self, *args, fetch=None):
        out = io.StringIO()
        code = vc.main(["--path", str(self.kb), "--cache-dir", str(self.cache), *args],
                       fetch=fetch or self.fetch, sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def test_inserts_exactly_one_line_lf(self):
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        code, _ = self.run_cli("--write-ecli")
        self.assertEqual(code, 0)
        after = path.read_bytes()
        expected = before.replace(
            b"geltungsbereich: [DE]\n---\n",
            b"geltungsbereich: [DE]\necli: ECLI:DE:BGH:2025:091025UIZR159.24.0\n---\n", 1)
        self.assertEqual(after, expected)
        self.assertEqual(after.count(b"\n"), before.count(b"\n") + 1)

    def test_crlf_preserved(self):
        path = self.write("urteile/a.md", URTEIL_FRONT, eol="\r\n")
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        after = path.read_bytes()
        self.assertIn(b"ecli: ECLI:DE:BGH:2025:091025UIZR159.24.0\r\n---\r\n", after)
        self.assertEqual(after.count(b"\n"), after.count(b"\r\n"))
        self.assertEqual(len(after), len(before) + len(b"ecli: ECLI:DE:BGH:2025:091025UIZR159.24.0\r\n"))

    def test_existing_ecli_untouched(self):
        text = URTEIL_FRONT.replace("geltungsbereich: [DE]\n", "geltungsbereich: [DE]\necli: ECLI:DE:BGH:1:2\n")
        path = self.write("urteile/a.md", text)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_dry_run_writes_nothing_and_lists_proposal(self):
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        code, text = self.run_cli("--write-ecli", "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(path.read_bytes(), before)
        self.assertIn("ECLI:DE:BGH:2025:091025UIZR159.24.0", text)
        self.assertIn("a.md", text)

    def test_default_never_writes(self):
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        self.run_cli()
        self.assertEqual(path.read_bytes(), before)

    def test_only_urteile_directory(self):
        path = self.write("themen/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_not_verified_is_skipped(self):
        path = self.write("urteile/a.md", URTEIL_FRONT.replace("09.10.2025", "10.10.2025"))
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_not_covered_court_is_skipped(self):
        text = URTEIL_FRONT.replace("BGH I ZR 159/24", "EuGH C-252/21").replace("| I ZR 159/24 |", "| C-252/21 |")
        path = self.write("urteile/a.md", text)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_ambiguous_without_date_is_skipped(self):
        text = (URTEIL_FRONT.replace("I ZR 159/24", "VI ZR 10/24")
                .replace("| **Datum** | 09.10.2025 |\n", ""))
        path = self.write("urteile/a.md", text)
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_ambiguous_resolved_by_date(self):
        text = URTEIL_FRONT.replace("I ZR 159/24", "VI ZR 10/24").replace("09.10.2025", "31.10.2024")
        path = self.write("urteile/a.md", text)
        self.run_cli("--write-ecli")
        self.assertIn(b"ecli: ECLI:DE:BGH:2024:311024BVIZR10.24.0\n", path.read_bytes())

    def test_date_label_entscheidungstermin_is_understood(self):
        text = (URTEIL_FRONT.replace("I ZR 159/24", "VI ZR 10/24")
                .replace("| **Datum** | 09.10.2025 |", "- **Entscheidungstermin:** **31.10.2024**"))
        path = self.write("urteile/a.md", text)
        self.run_cli("--write-ecli")
        self.assertIn(b"ecli: ECLI:DE:BGH:2024:311024BVIZR10.24.0\n", path.read_bytes())

    def test_malformed_ecli_from_api_is_rejected(self):
        body = json.loads(fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
        body["member"][0]["item"]["ecli"] = "ECLI:DE:BGH:2025:1\ninjected: yes"
        fetch = FakeFetch({"I ZR 159/24": (200, json.dumps(body).encode("utf-8"))})
        path = self.write("urteile/a.md", URTEIL_FRONT)
        before = path.read_bytes()
        self.run_cli("--write-ecli", fetch=fetch)
        self.assertEqual(path.read_bytes(), before)

    def test_no_frontmatter_is_skipped(self):
        path = self.write("urteile/a.md", "# BGH I ZR 159/24\n| **Aktenzeichen** | I ZR 159/24 |\n")
        before = path.read_bytes()
        self.run_cli("--write-ecli")
        self.assertEqual(path.read_bytes(), before)

    def test_no_temp_files_left_behind(self):
        self.write("urteile/a.md", URTEIL_FRONT)
        self.run_cli("--write-ecli")
        self.assertEqual(sorted(p.name for p in (self.kb / "urteile").iterdir()), ["a.md"])

    def test_json_reports_ecli_updates(self):
        self.write("urteile/a.md", URTEIL_FRONT)
        _, text = self.run_cli("--write-ecli", "--dry-run", "--json")
        data = json.loads(text)
        self.assertEqual(data["ecli_updates"][0]["ecli"], "ECLI:DE:BGH:2025:091025UIZR159.24.0")
        self.assertEqual(data["ecli_updates"][0]["written"], False)


if __name__ == "__main__":
    unittest.main()
