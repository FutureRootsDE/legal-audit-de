"""Offline tests: network errors are reduced to fixed categories, no exception text reaches the output."""
from __future__ import annotations

import contextlib
import http.client
import io
import json
import socket
import ssl
import tempfile
import unittest
import urllib.error
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import api, cli
from support import FakeFetch

SECRET = "evil.example.org 503 Service Unavailable"


def detail_for(exc: Exception) -> str:
    fetch = FakeFetch({"I ZR 159/24": exc})
    client = api.ApiClient(fetch=fetch, cache_dir=None, sleep=lambda s: None, max_retries=0)
    return client.lookup("BGH", "I ZR 159/24").detail


class ErrorCategories(unittest.TestCase):
    def test_fixed_categories(self):
        cases = [
            (socket.timeout(SECRET), "Zeitueberschreitung"),
            (api.DeadlineExceeded(SECRET), "Zeitueberschreitung"),
            (urllib.error.URLError(socket.timeout(SECRET)), "Zeitueberschreitung"),
            (ConnectionRefusedError(SECRET), "Verbindung abgelehnt"),
            (urllib.error.URLError(ConnectionRefusedError(SECRET)), "Verbindung abgelehnt"),
            (ssl.SSLError(SECRET), "TLS-Fehler"),
            (urllib.error.URLError(ssl.SSLCertVerificationError(SECRET)), "TLS-Fehler"),
            (api.RedirectBlocked(SECRET), "unzulaessige Weiterleitung"),
            (api.ResponseTooLarge(SECRET), "Antwort zu gross"),
            (http.client.IncompleteRead(b"x"), "ungueltige Antwort"),
            (http.client.BadStatusLine(SECRET), "ungueltige Antwort"),
            (OSError(SECRET), "OSError"),
            (urllib.error.URLError(SECRET), "URLError"),
            (api.NonRetryableError(SECRET), "NonRetryableError"),
        ]
        for exc, category in cases:
            with self.subTest(exc=type(exc).__name__):
                self.assertEqual(detail_for(exc), f"Netzwerkfehler: {category}")

    def test_no_exception_text_in_cli_report_or_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge"
            (kb / "themen").mkdir(parents=True)
            (kb / "themen" / "t.md").write_text("BGH I ZR 159/24\n", encoding="utf-8")
            fetch = FakeFetch({"I ZR 159/24": urllib.error.URLError(SECRET)})
            for extra in (["--json"], []):
                out = io.StringIO()
                cli.main(["--path", str(kb), "--no-cache", "--rate", "10", *extra],
                         fetch=fetch, sleep=lambda s: None, stdout=out)
                self.assertNotIn("evil.example.org", out.getvalue())
                self.assertNotIn("Service Unavailable", out.getvalue())


class TodayOption(unittest.TestCase):
    def run_cli(self, *args: str) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge"
            (kb / "themen").mkdir(parents=True)
            (kb / "themen" / "t.md").write_text("BGH I ZR 159/24 vom 09.10.2025\n", encoding="utf-8")
            out = io.StringIO()
            cli.main(["--path", str(kb), "--no-cache", "--offline", "--json", *args], stdout=out)
            return json.loads(out.getvalue())["citations"][0]

    def test_today_controls_the_run_day_rule(self):
        self.assertEqual(self.run_cli("--today", "2026-01-01")["date"], "2025-10-09")
        self.assertIsNone(self.run_cli("--today", "2025-10-09")["date"])

    def test_invalid_value_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            cli.main(["--today", "14.11.2026"], stdout=io.StringIO())
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
