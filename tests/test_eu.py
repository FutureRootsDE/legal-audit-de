"""Offline tests of the EU backend (Cellar): file numbers, query, parsing, client, classification, CLI."""
from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
import urllib.error
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import cli, eu_az, eu_classify, eu_sparql
from citation_check.eu_client import EuClient
from citation_check.models import Citation, LookupResult
from support import EuFakeFetch, FakeFetch, cellar_fixture

ECLI_SCHREMS = "ECLI:EU:C:2020:559"


def cite(az: str, date: str | None = None, court: str = "EuGH", names: tuple = ()) -> Citation:
    return Citation("knowledge/themen/x.md", 1, az, court, False, date, False, "", False, names)


class FileNumbers(unittest.TestCase):
    def test_forms_are_parsed(self):
        cases = {"C-311/18": ("C", 311, 2018, ""), "C‑311/18": ("C", 311, 2018, ""),
                 "T-553/23": ("T", 553, 2023, ""), "C-703/25 P": ("C", 703, 2025, "P"),
                 "C-1/20 PPU": ("C", 1, 2020, "PPU"), "C-619/18 R": ("C", 619, 2018, "R"),
                 "C-26/62": ("C", 26, 1962, ""), "T-7/90": ("T", 7, 1990, "")}
        for az, expected in cases.items():
            case = eu_az.parse_eu_az(az)
            self.assertEqual((case.letter, case.number, case.year, case.suffix), expected, az)

    def test_legacy_number_needs_the_court(self):
        self.assertIsNone(eu_az.parse_eu_az("26/62"))
        self.assertEqual(eu_az.parse_eu_az("26/62", "EuGH").az, "C-26/62")
        self.assertEqual(eu_az.parse_eu_az("7/90", "EuG").az, "T-7/90")
        self.assertIsNone(eu_az.parse_eu_az("26/62", "BGH"))

    def test_garbage_is_rejected(self):
        for text in ('C-1/18"} UNION {?s ?p ?o', "C-1/18; DROP", "X-1/18", "C-12345/18", "C-1/2018", ""):
            self.assertIsNone(eu_az.parse_eu_az(text), text)

    def test_celex_candidates(self):
        celex = eu_az.celex_candidates(eu_az.parse_eu_az("C-311/18"))
        self.assertIn("62018CJ0311", celex)
        self.assertIn("62018CC0311", celex)
        self.assertIn("62018CN0311", celex)
        self.assertIn("62018CO0311(01)", celex)
        self.assertEqual(eu_az.celex_candidates(eu_az.parse_eu_az("T-553/23"))[0], "62023TJ0553")
        self.assertTrue(all(eu_az.CELEX_RE.match(c) for c in celex))

    def test_document_types_come_from_a_whitelist(self):
        self.assertEqual(eu_az.doc_type_of("62018CJ0311"), "Urteil")
        self.assertEqual(eu_az.doc_type_of("62018CO0619(01)"), "Beschluss")
        self.assertEqual(eu_az.doc_type_of("62018CC0311"), "Schlussantraege")
        self.assertEqual(eu_az.doc_type_of("62025CN0703"), "Mitteilung")
        self.assertIsNone(eu_az.doc_type_of("62018XX0311"))
        self.assertIsNone(eu_az.doc_type_of("evil"))


class QueryTemplate(unittest.TestCase):
    def test_query_contains_only_derived_celex_numbers(self):
        query = eu_sparql.build_query(eu_az.parse_eu_az("C-311/18"))
        self.assertIn('"62018CJ0311"', query)
        self.assertIn("celex%3A62018CC0311>", query)
        self.assertIn("LIMIT 60", query)
        self.assertEqual(query.count('"'), 2 * len(eu_az.celex_candidates(eu_az.parse_eu_az("C-311/18"))))

    def test_url_uses_the_fixed_endpoint_and_json_format(self):
        url = eu_sparql.build_url(eu_az.parse_eu_az("T-553/23"))
        parsed = urlparse(url)
        self.assertEqual(f"{parsed.scheme}://{parsed.netloc}{parsed.path}", eu_sparql.SPARQL_BASE)
        self.assertEqual(parse_qs(parsed.query)["format"], ["application/sparql-results+json"])

    def test_invalid_celex_never_reaches_a_query(self):
        original = eu_az.celex_candidates
        try:
            eu_sparql.celex_candidates = lambda case: ['62018CJ0311"} DROP']
            with self.assertRaises(ValueError):
                eu_sparql.build_query(eu_az.parse_eu_az("C-311/18"))
        finally:
            eu_sparql.celex_candidates = original


class Parsing(unittest.TestCase):
    def parse(self, name: str):
        return eu_sparql.parse_response(cellar_fixture(name)[1])

    def test_judgment_opinion_and_notice_of_one_case(self):
        hits, tokens = self.parse("c_311_18")
        by_type = {h["type"]: h for h in hits}
        self.assertEqual(set(by_type), {"Urteil", "Schlussantraege", "Mitteilung"})
        self.assertEqual((by_type["Urteil"]["ecli"], by_type["Urteil"]["date"]), (ECLI_SCHREMS, "2020-07-16"))
        self.assertEqual(by_type["Schlussantraege"]["date"], "2019-12-19")
        self.assertIsNone(by_type["Mitteilung"]["ecli"])
        self.assertIn("schrems", tokens)

    def test_hits_carry_only_whitelisted_fields(self):
        hits, _ = self.parse("t_553_23")
        for hit in hits:
            self.assertEqual(set(hit), {"celex", "ecli", "date", "type", "court", "joined", "interim"})
            self.assertEqual(hit["court"], "EuG")
            self.assertEqual(hit, eu_sparql.sanitize_eu_hit(hit))

    def test_general_court_judgment_and_order(self):
        hits, _ = self.parse("t_553_23")
        self.assertEqual({(h["type"], h["date"]) for h in hits},
                         {("Urteil", "2025-09-03"), ("Beschluss", "2023-10-12"), ("Mitteilung", "2023-09-06")})

    def test_pending_case_has_only_a_notice(self):
        hits, _ = self.parse("c_703_25_p")
        self.assertEqual([(h["type"], h["date"]) for h in hits], [("Mitteilung", "2025-10-31")])

    def test_joined_case_is_found_under_the_leading_celex(self):
        hits, _ = self.parse("c_594_12_joined")
        joined = [h for h in hits if h["type"] == "Urteil"]
        self.assertEqual([(h["celex"], h["joined"]) for h in joined], [("62012CJ0293", True)])

    def test_interim_orders_with_suffix_are_found(self):
        hits, _ = self.parse("c_619_18_r")
        orders = sorted(h["celex"] for h in hits if h["type"] == "Beschluss")
        self.assertEqual(orders, ["62018CO0619(01)", "62018CO0619(02)", "62018CO0619(03)"])

    def test_empty_answer(self):
        self.assertEqual(self.parse("leer"), ([], []))

    def test_unexpected_shapes_raise_a_shape_error(self):
        for body in (b"not json", b"[]", b'{"results": []}', b'{"results": {"bindings": {}}}',
                     b'{"results": {"bindings": [1]}}'):
            with self.assertRaises(eu_sparql.EuShapeError, msg=body):
                eu_sparql.parse_response(body)

    def test_invalid_values_are_dropped_not_passed_on(self):
        body = json.dumps({"results": {"bindings": [
            {"celex": {"value": "62018CJ0311"}, "ecli": {"value": "ECLI:EU:C:2020:559\x1b[31m"},
             "date": {"value": "gestern"}},
            {"celex": {"value": "evil"}, "date": {"value": "2020-01-01"}},
            {"celex": {"value": 5}}]}}).encode()
        hits, _ = eu_sparql.parse_response(body)
        self.assertEqual(len(hits), 1)
        self.assertEqual((hits[0]["ecli"], hits[0]["date"]), (None, None))

    def test_titles_are_never_part_of_the_hits(self):
        hits, _ = self.parse("c_311_18")
        self.assertNotIn("Facebook", json.dumps(hits))


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.sleeps: list[float] = []
        self.now = 0.0

    def sleep(self, seconds: float):
        self.sleeps.append(seconds)
        self.now += seconds

    def client(self, fetch, **kw):
        return EuClient(fetch=fetch, cache_dir=self.tmp / "cache", sleep=self.sleep,
                        clock=lambda: self.now, **kw)

    def test_lookup_and_cache_roundtrip_keeps_tokens(self):
        fetch = EuFakeFetch({"62018CJ0311": cellar_fixture("c_311_18")})
        first = self.client(fetch).lookup("EuGH", "C-311/18")
        self.assertEqual((first.state, first.backend, first.from_cache), ("ok", "cellar", False))
        second = self.client(fetch).lookup("EuGH", "C-311/18")
        self.assertTrue(second.from_cache)
        self.assertEqual((second.hits, second.tokens), (first.hits, first.tokens))
        self.assertEqual(len(fetch.calls), 1)

    def test_fresh_bypasses_the_cache(self):
        fetch = EuFakeFetch({"62018CJ0311": cellar_fixture("c_311_18")})
        client = self.client(fetch)
        client.lookup("EuGH", "C-311/18")
        client.lookup("EuGH", "C-311/18", fresh=True)
        self.assertEqual(len(fetch.calls), 2)

    def test_poisoned_cache_entry_is_ignored(self):
        fetch = EuFakeFetch({"62018CJ0311": cellar_fixture("c_311_18")})
        client = self.client(fetch)
        client.lookup("EuGH", "C-311/18")
        path = client.cache.path("EuGH", "C-311/18")
        entry = json.loads(path.read_text(encoding="utf-8"))
        entry["hits"][0]["ecli"] = "ECLI:EU:C:2020:559\nInjected"
        path.write_text(json.dumps(entry), encoding="utf-8")
        again = self.client(fetch).lookup("EuGH", "C-311/18")
        self.assertFalse(again.from_cache)

    def test_requests_are_throttled_to_one_per_second(self):
        client = self.client(EuFakeFetch())
        client.lookup("EuGH", "C-1/18")
        client.lookup("EuGH", "C-2/18")
        self.assertTrue(any(abs(s - 1.0) < 1e-6 for s in self.sleeps))

    def test_server_error_is_retried_with_a_bounded_backoff_then_reported(self):
        fetch = EuFakeFetch(default=(503, b"<html>kaputt \x1b[31m</html>"))
        result = self.client(fetch).lookup("EuGH", "C-311/18")
        self.assertEqual((result.state, result.detail), ("error", "HTTP 503"))
        self.assertEqual(len(fetch.calls), 3)
        self.assertTrue(all(s <= 30.0 for s in self.sleeps))

    def test_retry_after_is_honoured(self):
        replies = iter([(429, b"", {"Retry-After": "7"}), cellar_fixture("c_311_18")])
        client = self.client(lambda url, timeout: next(replies))
        self.assertEqual(client.lookup("EuGH", "C-311/18").state, "ok")
        self.assertIn(7.0, self.sleeps)

    def test_network_error_has_a_fixed_category(self):
        def boom(url, timeout):
            raise urllib.error.URLError(ConnectionRefusedError("secret host details"))
        result = self.client(boom).lookup("EuGH", "C-311/18")
        self.assertEqual(result.state, "error")
        self.assertNotIn("secret", result.detail)

    def test_unexpected_answer_is_an_error_not_a_crash(self):
        fetch = EuFakeFetch(default=(200, b'{"foo": 1}'))
        result = self.client(fetch).lookup("EuGH", "C-311/18")
        self.assertEqual(result.state, "error")

    def test_unparsable_file_number_is_an_error_without_a_request(self):
        fetch = EuFakeFetch()
        result = self.client(fetch).lookup("EuGH", "kaputt")
        self.assertEqual(result.state, "error")
        self.assertEqual(fetch.calls, [])

    def test_offline_never_requests(self):
        fetch = EuFakeFetch()
        client = self.client(fetch, offline=True)
        self.assertEqual(client.lookup("EuGH", "C-311/18").state, "unchecked")
        self.assertEqual(client.lookup("EuGH", "C-311/18", fresh=True).state, "unchecked")
        self.assertEqual(fetch.calls, [])

    def test_circuit_breaker_stops_requests_after_repeated_failures(self):
        fetch = EuFakeFetch(default=(500, b""))
        client = self.client(fetch, breaker_threshold=2)
        for number in range(1, 5):
            client.lookup("EuGH", f"C-{number}/18")
        self.assertEqual(len(fetch.calls), 2 * 3)


class Classification(unittest.TestCase):
    def lookup(self, name: str, **extra) -> LookupResult:
        hits, tokens = eu_sparql.parse_response(cellar_fixture(name)[1])
        return LookupResult("ok", hits, backend="cellar", tokens=tuple(tokens), **extra)

    def status(self, az: str, name: str, date: str | None, court: str = "EuGH") -> str:
        return eu_classify.classify_eu(cite(az, date, court), self.lookup(name))

    def test_verified_with_matching_or_missing_date(self):
        self.assertEqual(self.status("C-311/18", "c_311_18", "2020-07-16"), "VERIFIED")
        self.assertEqual(self.status("C-311/18", "c_311_18", None), "VERIFIED")

    def test_date_mismatch_and_opinion_date_is_never_the_decision_date(self):
        self.assertEqual(self.status("C-311/18", "c_311_18", "2020-07-17"), "DATE_MISMATCH")
        citation = cite("C-311/18", "2019-12-19")
        lookup = self.lookup("c_311_18")
        self.assertEqual(eu_classify.classify_eu(citation, lookup), "DATE_MISMATCH")
        self.assertIn("Schlussantraege", "; ".join(eu_classify.eu_notes(citation, lookup, "DATE_MISMATCH")))

    def test_judgment_counts_before_order(self):
        self.assertEqual(self.status("T-553/23", "t_553_23", "2025-09-03", "EuG"), "VERIFIED")
        self.assertEqual(self.status("T-553/23", "t_553_23", "2023-10-12", "EuG"), "DATE_MISMATCH")

    def test_interim_relief_compares_with_the_order(self):
        self.assertEqual(self.status("C-619/18 R", "c_619_18_r", "2018-11-15"), "VERIFIED")
        self.assertEqual(self.status("C-619/18 R", "c_619_18_r", "2019-06-24"), "DATE_MISMATCH")
        self.assertEqual(self.status("C-619/18", "c_619_18_r", "2019-06-24"), "VERIFIED")

    def test_pending_without_decision(self):
        self.assertEqual(self.status("C-703/25 P", "c_703_25_p", "2025-10-31"), "PENDING")
        self.assertEqual(self.status("C-627/24 P", "c_627_24_p", None), "PENDING")

    def test_joined_case_is_verified_with_a_note(self):
        lookup = self.lookup("c_594_12_joined")
        citation = cite("C-594/12", "2014-04-08")
        self.assertEqual(eu_classify.classify_eu(citation, lookup), "VERIFIED")
        self.assertIn("verbunden", "; ".join(eu_classify.eu_notes(citation, lookup, "VERIFIED")))

    def test_empty_unchecked_and_error(self):
        self.assertEqual(eu_classify.classify_eu(cite("C-999/99"), self.lookup("leer")), "NOT_IN_DATASET")
        self.assertEqual(eu_classify.classify_eu(cite("C-1/18"), None), "UNCHECKED")
        self.assertEqual(eu_classify.classify_eu(cite("C-1/18"), LookupResult("error", backend="cellar")), "ERROR")

    def test_name_hint_is_informative_only(self):
        lookup = self.lookup("c_311_18")
        match = cite("C-311/18", "2020-07-16", names=("Schrems II",))
        wrong = cite("C-311/18", "2020-07-16", names=("Planet49",))
        self.assertEqual(eu_classify.eu_name_hint(match, lookup), "match")
        self.assertEqual(eu_classify.eu_name_hint(wrong, lookup), "no_match")
        self.assertEqual(eu_classify.classify_eu(wrong, lookup), "VERIFIED")


class Router:
    def __init__(self, ris, eu):
        self.ris, self.eu = ris, eu

    def __call__(self, url, timeout):
        return (self.eu if "publications.europa.eu" in url else self.ris)(url, timeout)


KB_EU = (
    "# EU\n"
    'EuGH C-311/18 vom 16.07.2020 "Schrems II"\n'
    "EuGH C-703/25 P eingelegt am 31.10.2025 (Planet49)\n"
    "EuG T-553/23 vom 04.09.2025\n"
    "EuGH C-999/99 erfunden\n"
    "EuGH, verb. Rs. C-293/12 und C-594/12\n"
)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "themen").mkdir(parents=True)
        (self.kb / "themen" / "t.md").write_text(KB_EU, encoding="utf-8")
        self.eu = EuFakeFetch({"62018CJ0311": cellar_fixture("c_311_18"),
                               "62025CJ0703": cellar_fixture("c_703_25_p"),
                               "62023TJ0553": cellar_fixture("t_553_23"),
                               "62012CJ0293": cellar_fixture("c_293_12"),
                               "62012CJ0594": cellar_fixture("c_594_12_joined")})

    def run_cli(self, *args):
        out = io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.tmp / "cache"), *args],
                        fetch=Router(FakeFetch(), self.eu), sleep=lambda s: None, stdout=out)
        return code, out.getvalue()

    def entries(self, *args):
        _, text = self.run_cli("--json", *args)
        data = json.loads(text)
        return data, {c["az"]: c for c in data["citations"]}

    def test_statuses_hints_and_backend_fields(self):
        data, by_az = self.entries()
        self.assertEqual(by_az["C-311/18"]["status"], "VERIFIED")
        self.assertEqual(by_az["C-311/18"]["backend"], "cellar")
        self.assertEqual(by_az["C-311/18"]["name_hint"], "match")
        self.assertEqual(by_az["C-703/25 P"]["status"], "PENDING")
        self.assertEqual(by_az["C-703/25 P"]["name_hint"], "no_match")  # Planet49 is not in that title
        self.assertEqual(by_az["T-553/23"]["status"], "DATE_MISMATCH")
        self.assertEqual(by_az["C-999/99"]["status"], "NOT_IN_DATASET")
        self.assertEqual(by_az["C-594/12"]["status"], "VERIFIED")
        counts = data["summary"]["counts"]
        self.assertEqual((counts["PENDING"], counts["DATE_MISMATCH"], counts["NOT_IN_DATASET"]), (1, 1, 1))
        self.assertTrue(data["summary"]["eu_enabled"])
        self.assertEqual(data["summary"]["eu_requests"], len(self.eu.calls))

    def test_json_has_no_free_text_from_the_source(self):
        text = self.run_cli("--json")[1]
        self.assertNotIn("Facebook", text)
        self.assertNotIn("Gerichtshof", text)

    def test_no_eu_restores_not_covered_and_sends_no_request(self):
        data, by_az = self.entries("--no-eu")
        self.assertEqual(by_az["C-311/18"]["status"], "NOT_COVERED")
        self.assertEqual(by_az["C-311/18"]["backend"], "none")
        self.assertEqual(self.eu.calls, [])
        self.assertFalse(data["summary"]["eu_enabled"])

    def test_second_run_comes_from_the_cache(self):
        self.run_cli("--json")
        calls = len(self.eu.calls)
        _, by_az = self.entries()
        self.assertEqual(len(self.eu.calls), calls)
        self.assertEqual(by_az["C-311/18"]["source"], "cache")

    def test_human_report_names_pending_and_hint(self):
        _, text = self.run_cli()
        self.assertIn("PENDING", text)
        self.assertIn("knowledge/themen/t.md:2", text)
        self.assertIn("Namenshinweis", text)

    def test_cellar_down_gives_error_and_exit_zero(self):
        self.eu = EuFakeFetch(default=(503, b""))
        code, text = self.run_cli("--json")
        self.assertEqual(code, 0)
        self.assertGreaterEqual(json.loads(text)["summary"]["counts"]["ERROR"], 1)


URTEIL_EU = (
    "---\n"
    "aktualisiert: 2026-05-08\n"
    "verifiziert-am: 2026-05-08\n"
    "---\n"
    "\n"
    "# EuGH C-311/18 (Schrems II)\n"
    "\n"
    "| **Aktenzeichen** | C-311/18 |\n"
    "| **Datum** | 16.07.2020 |\n"
)


class WriteEcliEu(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "urteile").mkdir(parents=True)
        self.path = self.kb / "urteile" / "eugh.md"
        self.path.write_bytes(URTEIL_EU.encode("utf-8"))
        self.eu = EuFakeFetch({"62018CJ0311": cellar_fixture("c_311_18")})

    def run_cli(self, *args):
        out = io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.tmp / "cache"), "--json", *args],
                        fetch=Router(FakeFetch(), self.eu), sleep=lambda s: None, stdout=out)
        return code, json.loads(out.getvalue())

    def test_dry_run_proposes_the_eu_ecli_and_writes_nothing(self):
        before = self.path.read_bytes()
        _, data = self.run_cli("--write-ecli", "--dry-run")
        self.assertEqual([(u["az"], u["ecli"]) for u in data["ecli_updates"]], [("C-311/18", ECLI_SCHREMS)])
        self.assertEqual(self.path.read_bytes(), before)

    def test_write_inserts_exactly_one_line(self):
        _, data = self.run_cli("--write-ecli")
        text = self.path.read_text(encoding="utf-8")
        self.assertIn(f"ecli: {ECLI_SCHREMS}\n---\n", text)
        self.assertEqual(text.count("ecli:"), 1)
        self.assertTrue(data["ecli_updates"][0]["written"])

    def test_wrong_date_or_pending_case_is_not_written(self):
        self.path.write_bytes(URTEIL_EU.replace("16.07.2020", "17.07.2020").encode("utf-8"))
        _, data = self.run_cli("--write-ecli", "--dry-run")
        self.assertEqual(data["ecli_updates"], [])
        self.assertIn("DATE_MISMATCH", json.dumps(data["ecli_skipped"]))

    def test_no_eu_skips_eu_files(self):
        _, data = self.run_cli("--write-ecli", "--dry-run", "--no-eu")
        self.assertEqual(data["ecli_updates"], [])
        self.assertEqual(self.eu.calls, [])


if __name__ == "__main__":
    unittest.main()
