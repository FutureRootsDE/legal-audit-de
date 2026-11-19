"""Tests for client_report.chrome: browser discovery, argument list and real PDF printing."""
from __future__ import annotations

import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report import chrome as chrome_mod
from client_report.chrome import ChromeNotFound, PdfError, find_chrome, pdf_args, print_pdf

WIN_ENV = {
    "ProgramFiles": "C:/PF",
    "ProgramFiles(x86)": "C:/PF86",
    "LocalAppData": "C:/Local",
}


class FindChrome(unittest.TestCase):
    def test_env_override_wins(self):
        self.assertEqual(
            find_chrome({"LEGAL_AUDIT_CHROME": "C:/x/chrome.exe"}, "Windows", exists=lambda p: True),
            Path("C:/x/chrome.exe"),
        )

    def test_env_override_must_exist(self):
        with self.assertRaises(ChromeNotFound) as ctx:
            find_chrome({"LEGAL_AUDIT_CHROME": "C:/x/missing.exe"}, "Windows", exists=lambda p: False)
        self.assertIn("LEGAL_AUDIT_CHROME", str(ctx.exception))

    def test_linux_edge_stable_and_macos_user_apps(self):
        which = lambda name: "/usr/bin/microsoft-edge-stable" if name == "microsoft-edge-stable" else None
        self.assertEqual(find_chrome({}, "Linux", which=which), Path("/usr/bin/microsoft-edge-stable"))
        found = find_chrome({}, "Darwin", exists=lambda p: "Applications" in p.parts and "Users" in str(p) or str(p).startswith(str(Path.home())), which=lambda n: None)
        self.assertTrue(str(found).startswith(str(Path.home())))
        self.assertEqual(
            find_chrome({}, "Darwin", exists=lambda p: False, which=lambda n: "/opt/bin/chromium" if n == "chromium" else None),
            Path("/opt/bin/chromium"),
        )

    def test_windows_prefers_chrome_over_edge(self):
        found = find_chrome(WIN_ENV, "Windows", exists=lambda p: True)
        self.assertEqual(found, Path("C:/PF") / "Google" / "Chrome" / "Application" / "chrome.exe")

    def test_windows_falls_back_to_edge(self):
        found = find_chrome(WIN_ENV, "Windows", exists=lambda p: p.name == "msedge.exe")
        self.assertEqual(found.name, "msedge.exe")

    def test_macos_paths(self):
        found = find_chrome({}, "Darwin", exists=lambda p: "Chromium" in str(p))
        self.assertIn("Chromium", str(found))

    def test_linux_uses_which(self):
        which = lambda name: "/usr/bin/chromium" if name == "chromium" else None
        self.assertEqual(find_chrome({}, "Linux", which=which), Path("/usr/bin/chromium"))

    def test_none_when_nothing_found(self):
        self.assertIsNone(find_chrome({}, "Windows", which=lambda n: None, exists=lambda p: False))
        self.assertIsNone(find_chrome({}, "Linux", which=lambda n: None, exists=lambda p: False))


class PdfArgs(unittest.TestCase):
    def test_uri_encoding_and_isolated_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            args = pdf_args(Path("chrome"), tmp / "Kunde Müller" / "report.html", tmp / "out.pdf", tmp / "prof")
            uri = args[-1]
            self.assertTrue(uri.startswith("file:///"))
            self.assertIn("Kunde%20M%C3%BCller", uri)
            self.assertIn(f"--user-data-dir={tmp / 'prof'}", args)
            self.assertTrue(any(a.startswith("--print-to-pdf=") for a in args))
            self.assertIn("--generate-pdf-document-outline", args)
            self.assertIn("--no-pdf-header-footer", args)


class PrintPdfPolling(unittest.TestCase):
    """Edge style: the process ends first, the file shows up later."""

    def test_waits_for_late_file_and_cleans_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            html, pdf = tmp / "r.html", tmp / "r.pdf"
            html.write_text("<p>x</p>", encoding="utf-8")
            profiles: list[Path] = []

            def fake_run(args, timeout):
                flag = next(a for a in args if a.startswith("--user-data-dir="))
                profiles.append(Path(flag.split("=", 1)[1]))
                threading.Timer(0.5, lambda: pdf.write_bytes(b"%PDF-1.7 test")).start()
                return 0

            with mock.patch.object(chrome_mod, "_run_browser", fake_run):
                out = print_pdf(html, pdf, chrome=Path("edge"), wait=10, interval=0.05)
            self.assertEqual(out, pdf)
            self.assertFalse(profiles[0].exists())

    def test_timeout_raises_german_error_without_dash(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            html = tmp / "r.html"
            html.write_text("x", encoding="utf-8")
            run = lambda args, timeout: 0
            with mock.patch.object(chrome_mod, "_run_browser", run):
                with self.assertRaises(PdfError) as ctx:
                    print_pdf(html, tmp / "r.pdf", chrome=Path("edge"), wait=0.3, interval=0.05)
            message = str(ctx.exception)
            self.assertIn("nicht erzeugt", message)
            self.assertIn("prüfen", message)
            for dash in ("\u2014", "\u2013", " - "):
                self.assertNotIn(dash, message)

    def test_non_pdf_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            html, pdf = tmp / "r.html", tmp / "r.pdf"
            html.write_text("x", encoding="utf-8")

            def run(args, timeout):
                pdf.write_bytes(b"not a pdf")
                return 0

            with mock.patch.object(chrome_mod, "_run_browser", run):
                with self.assertRaises(PdfError):
                    print_pdf(html, pdf, chrome=Path("edge"), wait=0.3, interval=0.05)

    def test_process_timeout_raises(self):
        def run(args, timeout):
            raise subprocess.TimeoutExpired(args, timeout)

        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / "r.html"
            html.write_text("x", encoding="utf-8")
            with mock.patch.object(chrome_mod, "_run_browser", run):
                with self.assertRaises(PdfError):
                    print_pdf(html, Path(tmp) / "r.pdf", chrome=Path("c"), timeout=1)


FAKE_BROWSER = """import subprocess, sys, time
subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
time.sleep(60)
"""


class ProcessTree(unittest.TestCase):
    def test_timeout_returns_promptly_despite_grandchild(self):
        import os
        import stat
        import sys

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            script = tmp / "fake_browser.py"
            script.write_text(FAKE_BROWSER, encoding="utf-8")
            if os.name == "nt":
                browser = tmp / "fake_browser.cmd"
                browser.write_text(f'@"{sys.executable}" "{script}"\r\n', encoding="utf-8")
            else:
                browser = tmp / "fake_browser.sh"
                browser.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}"\n', encoding="utf-8")
                browser.chmod(browser.stat().st_mode | stat.S_IEXEC)
            html = tmp / "r.html"
            html.write_text("x", encoding="utf-8")
            start = time.monotonic()
            with self.assertRaises(PdfError) as ctx:
                print_pdf(html, tmp / "r.pdf", chrome=browser, timeout=2, wait=0.2, interval=0.05)
            self.assertLess(time.monotonic() - start, 15)
            self.assertIn("nicht geantwortet", str(ctx.exception))


def _installed_browsers() -> list[Path]:
    system, env = chrome_mod.platform.system(), chrome_mod.os.environ
    paths = [p for p in chrome_mod.candidate_paths(system, env) if p.is_file()]
    found = find_chrome()
    if found and found not in paths:
        paths.append(found)
    return paths


@unittest.skipUnless(find_chrome(), "Chrome/Edge nicht installiert")
class RealPdf(unittest.TestCase):
    def test_minimal_html_to_pdf_with_every_installed_browser(self):
        for browser in _installed_browsers():
            with self.subTest(browser=browser.name), tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                html = tmp / "Kunde Müller" / "report.html"
                html.parent.mkdir()
                html.write_text(
                    '<!doctype html><html lang="de"><meta charset="utf-8"><title>T</title><h1>Überschrift</h1>',
                    encoding="utf-8",
                )
                out = print_pdf(html, tmp / "out.pdf", chrome=browser)
                self.assertEqual(out.read_bytes()[:5], b"%PDF-")


if __name__ == "__main__":
    unittest.main()
