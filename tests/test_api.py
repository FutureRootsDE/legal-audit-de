"""Offline tests for citation_check.api (HTTP client, backoff, pagination)."""
from __future__ import annotations

import shutil
import tempfile
import urllib.error
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import api, cache
from support import FakeFetch, OK_I_ZR_159, OK_VI_ZR_10, OK_EMPTY, ERR_422


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
        return api.ApiClient(fetch=fetch, cache_dir=self.tmp / "cache",
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
        req = api.build_request("https://example.invalid/x")
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
            client = api.ApiClient(fetch=fetch, cache_dir=self.tmp / f"cache{status}",
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
        self.assertEqual(res.detail, "HTTP 422 (invalid_parameter_value)")
        self.assertNotIn("pageIndex", res.detail)

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
        client.cache.now_epoch = lambda: 10_000_000_000.0  # far future
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


if __name__ == "__main__":
    unittest.main()
