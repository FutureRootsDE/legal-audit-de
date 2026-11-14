"""Offline tests for pagination, response shapes, Retry-After, redirects and bounded reads."""
from __future__ import annotations

import json
import socket
import urllib.error
import unittest
import urllib.request

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import api
from support import FakeFetch, OK_I_ZR_159, fixture_bytes


def page_body(members, total):
    return (200, json.dumps({"member": members, "totalItems": total}).encode("utf-8"))


def filler(n):
    return [{"item": {"fileNumbers": [f"I ZR {i}/20"], "ecli": "ECLI:DE:BGH:2020:1"}} for i in range(n)]


class ClientBase(unittest.TestCase):
    def setUp(self):
        self.sleeps: list[float] = []
        self.now = 0.0

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds

    def client(self, fetch, **kw):
        return api.ApiClient(fetch=fetch, cache_dir=None, sleep=self.sleep, clock=lambda: self.now, **kw)


class PaginationTests(ClientBase):
    def test_hit_on_second_page_is_found(self):
        hit_page = json.loads(fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
        second = (200, json.dumps(hit_page).encode("utf-8"))
        fetch = FakeFetch({"I ZR 159/24": [page_body(filler(api.PAGE_SIZE), 120), second]})
        res = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual((res.state, len(res.hits)), ("ok", 1))
        self.assertEqual(len(fetch.calls), 2)

    def test_stops_after_max_pages(self):
        fetch = FakeFetch({"I ZR 159/24": page_body(filler(api.PAGE_SIZE), 10_000)})
        res = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual((res.state, res.hits, len(fetch.calls)), ("ok", [], api.MAX_PAGES))


class TimeoutTests(ClientBase):
    def test_socket_timeout_is_error_not_exception(self):
        fetch = FakeFetch({"I ZR 159/24": socket.timeout("timed out")})
        res = self.client(fetch, max_retries=1).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "error")
        self.assertEqual(res.detail, "Netzwerkfehler: Zeitueberschreitung")

    def test_total_deadline_stops_trickling_response(self):
        class Trickle:
            def read(self, n):
                return b"x"

        ticks = iter(range(0, 1000))
        with self.assertRaises(api.NonRetryableError):
            api.read_bounded(Trickle(), deadline=5, clock=lambda: next(ticks))

    def test_oversized_response_is_rejected_not_truncated(self):
        class Endless:
            def read(self, n):
                return b"x" * n

        with self.assertRaises(api.ResponseTooLarge):
            api.read_bounded(Endless(), deadline=1e12, clock=lambda: 0, limit=1000)

    def test_exact_limit_is_accepted(self):
        class Once:
            def __init__(self):
                self.data = b"x" * 1000

            def read(self, n):
                chunk, self.data = self.data[:n], self.data[n:]
                return chunk

        self.assertEqual(len(api.read_bounded(Once(), deadline=1e12, clock=lambda: 0, limit=1000)), 1000)

    def test_non_retryable_error_is_not_retried(self):
        fetch = FakeFetch({"I ZR 159/24": api.ResponseTooLarge("zu gross")})
        res = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual((res.state, len(fetch.calls)), ("error", 1))


class RetryAfterTests(ClientBase):
    def test_retry_after_seconds_is_respected_and_capped(self):
        fetch = FakeFetch({"I ZR 159/24": [(429, b"", {"Retry-After": "7"}), OK_I_ZR_159]})
        res = self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual(res.state, "ok")
        self.assertIn(7.0, self.sleeps)
        fetch = FakeFetch({"I ZR 159/24": [(503, b"", {"retry-after": "9999"}), OK_I_ZR_159]})
        self.sleeps.clear()
        self.client(fetch, max_backoff=4.0).lookup("BGH", "I ZR 159/24")
        self.assertLessEqual(max(self.sleeps), 4.0)
        self.assertIn(4.0, self.sleeps)

    def test_without_header_exponential_backoff_stays(self):
        fetch = FakeFetch({"I ZR 159/24": [(503, b""), (503, b""), OK_I_ZR_159]})
        self.client(fetch).lookup("BGH", "I ZR 159/24")
        self.assertEqual([s for s in self.sleeps if s >= 1.0], [1.0, 2.0])

    def test_parse_retry_after_variants(self):
        self.assertEqual(api.parse_retry_after("5", now=0), 5.0)
        self.assertIsNone(api.parse_retry_after("-3", now=0))
        self.assertIsNone(api.parse_retry_after("soon", now=0))
        self.assertIsNone(api.parse_retry_after(None, now=0))
        self.assertAlmostEqual(api.parse_retry_after("Thu, 01 Jan 1970 00:00:10 GMT", now=0), 10.0)


class ResponseShapeTests(ClientBase):
    def lookup(self, payload):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        return self.client(FakeFetch({"I ZR 159/24": (200, body)})).lookup("BGH", "I ZR 159/24")

    def test_unexpected_types_are_an_error_not_a_crash(self):
        cases = [
            {"member": "text", "totalItems": 1},
            {"member": {"a": 1}, "totalItems": 1},
            {"member": ["x"], "totalItems": 1},
            {"member": [1], "totalItems": 1},
            {"member": [{"item": "x"}], "totalItems": 1},
            {"member": [{"item": {"fileNumbers": "I ZR 159/24"}}], "totalItems": 1},
            {"member": [{"item": {"fileNumbers": [1, None]}}], "totalItems": 1},
            {"member": [], "totalItems": "viele"},
            [1, 2, 3],
            "just a string",
            None,
        ]
        for case in cases:
            with self.subTest(case=str(case)[:50]):
                res = self.lookup(case)
                self.assertEqual(res.state, "error")
                self.assertTrue(res.detail)

    def test_missing_optional_parts_are_still_fine(self):
        self.assertEqual(self.lookup({"totalItems": 0}).state, "ok")
        self.assertEqual(self.lookup({"member": [{}], "totalItems": 1}).state, "ok")


class RedirectTests(unittest.TestCase):
    def follow(self, target, origin="https://testphase.rechtsinformationen.bund.de/v1/x"):
        handler = api.SameHostHttpsRedirect()
        req = urllib.request.Request(origin)
        return handler.redirect_request(req, None, 302, "Found", {}, target)

    def test_same_host_https_is_allowed(self):
        new = self.follow("https://testphase.rechtsinformationen.bund.de/v1/y")
        self.assertEqual(new.full_url, "https://testphase.rechtsinformationen.bund.de/v1/y")

    def test_other_host_scheme_or_port_is_blocked(self):
        for target in ("https://evil.example/v1", "http://testphase.rechtsinformationen.bund.de/v1",
                       "https://testphase.rechtsinformationen.bund.de:8443/v1", "file:///etc/passwd",
                       "ftp://testphase.rechtsinformationen.bund.de/x"):
            with self.subTest(target=target), self.assertRaises(api.RedirectBlocked):
                self.follow(target)

    def test_redirect_block_is_error_without_retry(self):
        fetch = FakeFetch({"I ZR 159/24": api.RedirectBlocked("weg")})
        client = api.ApiClient(fetch=fetch, cache_dir=None, sleep=lambda s: None)
        res = client.lookup("BGH", "I ZR 159/24")
        self.assertEqual((res.state, len(fetch.calls)), ("error", 1))

    def test_default_fetch_refuses_plain_http(self):
        with self.assertRaises(api.NonRetryableError):
            api.default_fetch("http://testphase.rechtsinformationen.bund.de/v1/x", 1.0)


class HeaderTupleTests(ClientBase):
    def test_fetch_may_return_two_or_three_values(self):
        for ret in ((200, fixture_bytes("ris_rechtsprechung_kein_treffer")),
                    (200, fixture_bytes("ris_rechtsprechung_kein_treffer"), {})):
            res = self.client(FakeFetch({"A": ret})).lookup("BGH", "A")
            self.assertEqual(res.state, "ok")


if __name__ == "__main__":
    unittest.main()
