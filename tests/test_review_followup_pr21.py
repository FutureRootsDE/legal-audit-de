"""Regression tests for the review findings of PR #21 (norm mode, EU check, cache, legal-status)."""
from __future__ import annotations

import io
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
import urllib.error
import zipfile
from pathlib import Path
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import bgbl, cache, cli, eu_classify, eu_sparql, norm_check, norm_extract, norm_xml
from citation_check.eu_client import EuClient
from citation_check.models import Citation, LookupResult
from citation_check.norm_client import NormClient
from citation_check.norm_extract import NormRef
from test_legal_status import STATUS
from test_norms import TOC_URL, UrlFake, zip_of

FIX = support.FIXTURES
HEAD = (b'<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE dokumente SYSTEM '
        b'"https://www.gesetze-im-internet.de/dtd/1.01/gii-norm.dtd">\n')


def law_xml(*paragraphs: str, enbez: str = "§ 9") -> bytes:
    body = "".join(f"<P>{p}</P>" for p in paragraphs)
    return HEAD + (f'<dokumente builddate="20261101"><norm><metadaten><jurabk>XG</jurabk><enbez>{enbez}</enbez>'
                   f"<titel>Titel</titel></metadaten><textdaten><text><Content>{body}</Content></text></textdaten>"
                   "</norm></dokumente>").encode("utf-8")


def ref(number: str = "9", absaetze=(), saetze=(), others=()) -> NormRef:
    return NormRef("knowledge/themen/x.md", 1, "XG", "§", number, None, tuple(absaetze), tuple(saetze), False, None,
                   tuple(others))


INSERTED = law_xml("(1) Erster Satz.", "(1a) Eins. Zwei. Drei.", "(2) Nur ein Satz.")


class AbsatzMarks(unittest.TestCase):
    """Findings 1 and 2: sentences are keyed by the Absatz mark, lettered Absaetze are checked against the marks."""

    def check(self, raw: bytes, norm: NormRef):
        return norm_check.check_norm(norm, norm_xml.parse_law_xml(raw))

    def test_inserted_absatz_does_not_shift_the_sentence_counts(self):
        self.assertEqual(self.check(INSERTED, ref(absaetze=("2",), saetze=(3,)))[0], "ABSATZ_MISSING")
        self.assertEqual(self.check(INSERTED, ref(absaetze=("2",), saetze=(1,)))[0], "NORM_OK")
        self.assertEqual(self.check(INSERTED, ref(absaetze=("1a",), saetze=(3,)))[0], "NORM_OK")
        self.assertEqual(self.check(INSERTED, ref(absaetze=("1a",), saetze=(4,)))[0], "ABSATZ_MISSING")

    def test_ambiguous_assignment_leaves_the_satz_unchecked(self):
        raw = law_xml("(1) Erster Satz.", "Fortsetzung ohne Marke. Noch einer.", "(2) Zweiter.")
        status, _, _, coverage = self.check(raw, ref(absaetze=("1",), saetze=(5,)))
        self.assertEqual(status, "NORM_OK")
        self.assertIn("satz", coverage["unchecked"])
        self.assertNotIn("satz", coverage["checked"])

    def test_lettered_absatz_is_checked_against_the_marks(self):
        self.assertEqual(norm_extract.extract_text("§ 5a Abs. 2a UWG", "x.md").norms[0].absaetze, ("2a",))
        status, detail, _, coverage = self.check(INSERTED, ref(absaetze=("2a",)))
        self.assertEqual(status, "ABSATZ_MISSING")
        self.assertIn("2a", detail)
        status, _, _, coverage = self.check(INSERTED, ref(absaetze=("1a",)))
        self.assertEqual((status, coverage["checked"]), ("NORM_OK", ["paragraph", "absatz"]))

    def test_lettered_absatz_without_marks_is_not_checked(self):
        raw = law_xml("Ein Satz ohne Absatzmarke.")
        status, _, _, coverage = self.check(raw, ref(absaetze=("2a",)))
        self.assertEqual(status, "NORM_OK")
        self.assertIn("absatz", coverage["unchecked"])

    def test_index_keeps_marks_and_validates(self):
        index = norm_xml.parse_law_xml(INSERTED)
        self.assertEqual(index["norms"]["§ 9"]["m"], ["1", "1a", "2"])
        self.assertEqual(index["norms"]["§ 9"]["s"], {"1": 1, "1a": 3, "2": 1})
        self.assertEqual(norm_xml.validate_index(json.loads(json.dumps(index))), index)


def _patched(data: bytes, local: int | None = None, central: int | None = None, value: bytes = b"") -> bytes:
    out = bytearray(data)
    if local is not None:
        out[local:local + len(value)] = value
    if central is not None:
        start = data.rfind(b"PK\x01\x02")
        out[start + central:start + central + len(value)] = value
    return bytes(out)


class BrokenArchives(unittest.TestCase):
    """Finding 3: any decompression error becomes XmlRejected, the run continues."""

    def broken(self) -> dict[str, bytes]:
        good = zip_of("gii_bgb")
        name_len = int.from_bytes(good[26:28], "little")
        extra_len = int.from_bytes(good[28:30], "little")
        data_start = 30 + name_len + extra_len
        garbage = bytearray(good)
        garbage[data_start:data_start + 64] = b"\xff" * 64
        return {
            "deflate": bytes(garbage),
            "encrypted": _patched(_patched(good, local=6, value=b"\x01\x00"), central=8, value=b"\x01\x00"),
            "method": _patched(_patched(good, local=8, value=b"\x63\x00"), central=10, value=b"\x63\x00"),
            "truncated-stream": _patched(good, local=data_start, value=b"\x00"),
        }

    def test_every_broken_archive_is_rejected(self):
        for label, data in self.broken().items():
            with self.subTest(label), self.assertRaises(norm_xml.XmlRejected):
                norm_xml.parse_law_zip(data)

    def test_client_reports_a_fixed_category_and_keeps_going(self):
        for label, data in self.broken().items():
            fake = UrlFake({"https://www.gesetze-im-internet.de/bgb/xml.zip": (200, data)})
            client = NormClient(fetch=fake, sleep=lambda s: None)
            with self.subTest(label):
                result = client.law("bgb")
                self.assertEqual(result.state, "error")
                self.assertTrue(result.detail.startswith("XML abgelehnt"))
                self.assertEqual(client.law("uwg_2004").state, "ok")


class RegexBounds(unittest.TestCase):
    """Findings 4 and 5: no quadratic regex on hostile input."""

    def test_frontmatter_line_with_many_spaces(self):
        text = "---\naktualisiert:" + " " * 200_000 + "x\n---\n"
        start = time.perf_counter()
        STATUS.frontmatter_fields(text)
        self.assertLess(time.perf_counter() - start, 1.0)

    def test_frontmatter_value_is_still_stripped(self):
        self.assertEqual(STATUS.frontmatter_fields("---\naktualisiert:   2026-01-02  \n---\n"),
                         {"aktualisiert": "2026-01-02"})

    def test_title_search_with_many_open_tags(self):
        body = b"<title>" * 150_000
        start = time.perf_counter()
        self.assertIsNone(bgbl.page_title(body))
        self.assertLess(time.perf_counter() - start, 1.0)
        self.assertEqual(bgbl.page_title(b"<html><title>Bundesgesetzblatt Teil I</title>"),
                         b"Bundesgesetzblatt Teil I")


class XmlHardening(unittest.TestCase):
    """Findings 6 and 7."""

    def test_entity_declaration_in_utf16_is_rejected(self):
        doc = ('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE dokumente [<!ENTITY a "aaaa">]>'
               "<dokumente>&a;</dokumente>").encode("utf-16")
        with self.assertRaises(norm_xml.XmlRejected):
            norm_xml.parse_law_xml(doc)

    def test_internal_subset_without_entities_is_rejected(self):
        doc = '<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE dokumente [ ]><dokumente/>'.encode("utf-16")
        with self.assertRaises(norm_xml.XmlRejected):
            norm_xml.parse_law_xml(doc)

    def test_real_document_still_parses(self):
        self.assertIn("§ 356a", norm_xml.parse_law_xml((FIX / "gii_bgb.xml").read_bytes())["norms"])

    def test_wrong_container_types_in_cache_are_rejected(self):
        index = json.loads(json.dumps(norm_xml.parse_law_xml((FIX / "gii_bgb.xml").read_bytes())))
        for key, value in (("norms", []), ("jurabk", "BGB"), ("ranges", {}), ("arts", 5), ("builddate", 7)):
            broken = dict(index, **{key: value})
            with self.subTest(key):
                self.assertIsNone(norm_xml.validate_index(broken))


class KbReading(unittest.TestCase):
    """Finding 8: link check and bounded read shared with extract.py."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "themen").mkdir(parents=True)
        (self.kb / "themen" / "a.md").write_text("Nach § 356a BGB.\n", encoding="utf-8")

    def test_whole_file_is_never_read_unbounded(self):
        with mock.patch.object(Path, "read_bytes", side_effect=AssertionError("unbounded read")):
            out = norm_extract.scan_kb_norms(self.kb)
        self.assertEqual([n.number for n in out.norms], ["356a"])

    def test_link_like_files_are_skipped(self):
        with mock.patch("citation_check.extract.is_link_like", side_effect=lambda p: p.name == "a.md"):
            out = norm_extract.scan_kb_norms(self.kb)
        self.assertEqual(out.norms, [])
        self.assertTrue(any("a.md" in s for s in out.skipped))

    @unittest.skipUnless(os.name == "nt", "Windows junction")
    def test_files_below_a_junction_are_skipped(self):
        outside = self.tmp / "outside"
        outside.mkdir()
        (outside / "b.md").write_text("Nach § 312j BGB.\n", encoding="utf-8")
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.kb / "link"), str(outside)],
                              capture_output=True, check=False)
        if made.returncode != 0:
            self.skipTest("junction not creatable")
        out = norm_extract.scan_kb_norms(self.kb)
        self.assertEqual([n.number for n in out.norms], ["356a"])


KB_TEXT = "---\nverifiziert-am: 2026-01-01\n---\nNach § 356a BGB und § 3 Abs. 1 Nr. 2 lit. a BGB, § 999 BGB.\n"


class NormCli(unittest.TestCase):
    """Findings 9, 12 and 14."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "themen").mkdir(parents=True)
        (self.kb / "themen" / "t.md").write_text(KB_TEXT, encoding="utf-8")
        self.timeouts: list[float] = []
        fake = UrlFake()

        def fetch(url, timeout):
            self.timeouts.append(timeout)
            return fake(url, timeout)
        self.fetch = fetch

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.tmp / "cache"), "--check-norms", *args],
                        fetch=self.fetch, sleep=lambda s: None, stdout=out, stderr=err)
        return code, out.getvalue()

    def test_text_report_marks_cached_law_data(self):
        _, first = self.run_cli()
        self.assertIn("Quelle: gesetze-im-internet.de", first)
        _, second = self.run_cli()
        self.assertIn("Quelle: Cache (ungeprueft)", second)

    def test_strict_exits_one_on_problems(self):
        self.assertEqual(self.run_cli()[0], 0)
        self.assertEqual(self.run_cli("--strict")[0], 1)

    def test_timeout_is_used_for_the_norm_requests(self):
        self.run_cli("--timeout", "7")
        self.assertTrue(self.timeouts)
        self.assertEqual(set(self.timeouts), {7.0})

    def test_checked_and_unchecked_parts_per_citation(self):
        data = json.loads(self.run_cli("--json")[1])
        by_ref = {n["ref"]: n for n in data["norms"]}
        ok = by_ref["§ 356a BGB"]
        self.assertEqual((ok["checked"], ok["unchecked"]), (["paragraph"], []))
        nummer = next(n for n in data["norms"] if n["ref"].startswith("§ 3 "))
        self.assertIn("nummer", nummer["unchecked"])
        self.assertIn("lit", nummer["unchecked"])
        _, text = self.run_cli()
        self.assertIn("nummer, lit]", text)


class CacheWarnings(unittest.TestCase):
    """Finding 10: no absolute paths or exception texts in warnings."""

    def test_unwritable_cache_warning_is_anonymous(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "datei"
            blocker.write_text("x", encoding="utf-8")
            warnings: list[str] = []
            cache.write_json_atomic(blocker / "sub", blocker / "sub" / "e.json", {"a": 1}, warnings)
        self.assertTrue(warnings)
        for warning in warnings:
            self.assertNotIn(tmp, warning)
            self.assertNotIn("Errno", warning)
            self.assertNotIn("WinError", warning)

    def test_prepare_and_vet_warnings_are_anonymous(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "datei"
            blocker.write_text("x", encoding="utf-8")
            _, prepared = cache.prepare_cache_dir(blocker)
            _, vetted = cache.vet_default_dir(Path(tmp) / "x", Path(tmp) / "home", enforce=True)
        for warning in (prepared, vetted):
            self.assertIsNotNone(warning)
            self.assertNotIn(tmp, warning)
            self.assertNotIn("Errno", warning)
            self.assertNotIn("WinError", warning)


def cite(az: str, date: str | None) -> Citation:
    return Citation("knowledge/urteile/x.md", 1, az, "EuG", False, date, False, "")


class InterimOrders(unittest.TestCase):
    """Finding 11: interim relief orders only count for file numbers with suffix R."""

    def lookup_without_judgment(self) -> LookupResult:
        data = json.loads((FIX / "cellar_t_553_23.json").read_text(encoding="utf-8"))
        data["results"]["bindings"] = [b for b in data["results"]["bindings"] if "TJ" not in b["celex"]["value"]]
        hits, tokens = eu_sparql.parse_response(json.dumps(data).encode("utf-8"))
        return LookupResult("ok", hits, backend="cellar", tokens=tuple(tokens))

    def test_only_interim_orders_mean_pending(self):
        lookup = self.lookup_without_judgment()
        self.assertTrue(any(h["interim"] for h in lookup.hits))
        self.assertEqual(eu_classify.classify_eu(cite("T-553/23", "2023-10-12"), lookup), "PENDING")

    def test_suffix_r_still_uses_the_interim_order(self):
        lookup = self.lookup_without_judgment()
        self.assertEqual(eu_classify.classify_eu(cite("T-553/23 R", "2023-10-12"), lookup), "VERIFIED")


class SparqlTimeout(unittest.TestCase):
    """Finding 13: a SPARQL timeout is not retried."""

    def test_timeout_is_not_retried(self):
        for exc in (TimeoutError("t"), socket.timeout("t"), urllib.error.URLError(TimeoutError("t"))):
            calls: list[str] = []

            def fetch(url, timeout, exc=exc):
                calls.append(url)
                raise exc
            client = EuClient(fetch=fetch, sleep=lambda s: None)
            with self.subTest(type(exc).__name__):
                result = client.lookup("EuGH", "C-311/18")
                self.assertEqual(result.state, "error")
                self.assertEqual(len(calls), 1)


class Docs(unittest.TestCase):
    """Findings 14 and 15."""

    def test_claude_md_sentence_and_limits(self):
        text = (support.HERE.parent / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertNotIn("Ausnahme EU-Rechtsprechung", text)
        self.assertIn("Nr. und lit.", text)


if __name__ == "__main__":
    unittest.main()
