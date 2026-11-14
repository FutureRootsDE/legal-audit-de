"""Offline tests of the norm mode: law XML index, checks, client, BGBl. references, CLI."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import bgbl, cli, norm_check, norm_extract, norm_laws, norm_xml
from citation_check.norm_client import NormClient
from citation_check.norm_extract import NormRef

FIX = support.FIXTURES


def zip_of(name: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{name}.xml", (FIX / f"{name}.xml").read_bytes())
    return buffer.getvalue()


TOC_URL = "https://www.gesetze-im-internet.de/gii-toc.xml"
ROBOTS_URL = "https://www.recht.bund.de/robots.txt"
ROBOTS_OK = b"User-agent: *\nDisallow: /SiteGlobals/\nCrawl-delay: 30\n"


class UrlFake:
    """Scripted HTTP layer for gii and recht.bund.de: url -> (status, body) or an exception."""

    def __init__(self, extra: dict | None = None):
        self.table = {
            TOC_URL: (200, (FIX / "gii_toc.xml").read_bytes()),
            "https://www.gesetze-im-internet.de/bgb/xml.zip": (200, zip_of("gii_bgb")),
            "https://www.gesetze-im-internet.de/uwg_2004/xml.zip": (200, zip_of("gii_uwg")),
            "https://www.gesetze-im-internet.de/bgbeg/xml.zip": (200, zip_of("gii_egbgb")),
            ROBOTS_URL: (200, ROBOTS_OK),
            "https://www.recht.bund.de/bgbl/1/2026/322/VO.html": (200, (FIX / "bgbl_ok.html").read_bytes()),
            "https://www.recht.bund.de/bgbl/1/2026/9999/VO.html": (404, (FIX / "bgbl_404.html").read_bytes()),
        }
        self.table.update(extra or {})
        self.calls: list[str] = []

    def __call__(self, url: str, timeout: float):
        self.calls.append(url)
        entry = self.table.get(url, (404, b""))
        if isinstance(entry, Exception):
            raise entry
        return entry


def ref(law: str, number: str, absaetze=(), saetze=(), kind="§", art=None, old=False) -> NormRef:
    return NormRef("knowledge/themen/x.md", 1, law, kind, number, art, tuple(absaetze), tuple(saetze), old, None)


class LawIndex(unittest.TestCase):
    def index(self, name: str) -> dict:
        return norm_xml.parse_law_xml((FIX / f"{name}.xml").read_bytes())

    def test_paragraph_heading_and_absatz_count(self):
        entry = self.index("gii_bgb")["norms"]["§ 356a"]
        self.assertEqual((entry["t"], entry["a"], entry["g"]), ("Elektronische Widerrufsfunktion bei Fernabsatzverträgen", 5, False))

    def test_sentence_counts_only_where_reliable(self):
        norms = self.index("gii_uwg")["norms"]
        self.assertEqual(norms["§ 5a"]["s"][3], 3)
        self.assertIsNone(norms["§ 5a"]["s"][0])  # truncated list text without a final period: not reliable

    def test_stand_is_date_and_bgbl_reference(self):
        uwg, bgb = self.index("gii_uwg"), self.index("gii_bgb")
        self.assertEqual((uwg["stand_date"], uwg["stand_bgbl"]), ("2026-10-22", "BGBl. 2026 I Nr. 322"))
        self.assertEqual((bgb["stand_date"], bgb["stand_bgbl"]), ("2026-07-23", "BGBl. 2026 I Nr. 226"))

    def test_range_of_dropped_paragraphs(self):
        self.assertEqual(self.index("gii_bgb")["ranges"], [["§", 3, "", 6, ""]])

    def test_articles_and_paragraphs_below_them(self):
        index = self.index("gii_egbgb")
        self.assertIn("Art 246a|§ 1", index["norms"])
        self.assertEqual(index["arts"], ["Art 246a", "Art 247"])

    def test_index_is_canonical_and_json_serialisable(self):
        index = self.index("gii_bgb")
        self.assertEqual(norm_xml.validate_index(json.loads(json.dumps(index))), index)

    def test_tampered_index_is_rejected(self):
        index = json.loads(json.dumps(self.index("gii_bgb")))
        index["norms"]["§ 1"]["t"] = "Boese\x1b[31m"
        self.assertIsNone(norm_xml.validate_index(index))
        index = json.loads(json.dumps(self.index("gii_bgb")))
        index["stand_bgbl"] = "kaputt"
        self.assertIsNone(norm_xml.validate_index(index))
        index = json.loads(json.dumps(self.index("gii_bgb")))
        index["norms"]["../../etc"] = index["norms"]["§ 1"]
        self.assertIsNone(norm_xml.validate_index(index))
        self.assertIsNone(norm_xml.validate_index([]))

    def test_entity_declarations_and_foreign_doctypes_are_rejected(self):
        bomb = b'<?xml version="1.0"?><!DOCTYPE dokumente [<!ENTITY a "aaaa">]><dokumente>&a;</dokumente>'
        for raw in (bomb, b'<!DOCTYPE dokumente SYSTEM "http://evil.example/x.dtd"><dokumente/>', b"<kaputt"):
            with self.assertRaises(norm_xml.XmlRejected):
                norm_xml.parse_law_xml(raw)

    def test_plain_http_doctype_of_the_real_files_is_accepted(self):
        raw = (b'<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE dokumente SYSTEM '
               b'"http://www.gesetze-im-internet.de/dtd/1.01/gii-norm.dtd">\n<dokumente builddate="20260101"/>')
        self.assertEqual(norm_xml.parse_law_xml(raw)["norms"], {})

    def test_archive_limits(self):
        with self.assertRaises(norm_xml.XmlRejected):
            norm_xml.parse_law_zip(b"kein zip")
        many = io.BytesIO()
        with zipfile.ZipFile(many, "w") as archive:
            archive.writestr("a.xml", "<dokumente/>")
            archive.writestr("b.xml", "<dokumente/>")
        with self.assertRaises(norm_xml.XmlRejected):
            norm_xml.parse_law_zip(many.getvalue())

    def test_sentence_counter(self):
        self.assertEqual(norm_xml.count_sentences("(1) Erster Satz. Zweiter Satz."), 2)
        self.assertEqual(norm_xml.count_sentences("Ein Satz; mit Strichpunkt: und Doppelpunkt."), 1)
        for text in ("(1) Siehe Nr. 2 und danach. Weiter.", "Ein Satz mit z. B. Abkuerzung.", "Ohne Punkt am Ende",
                     "Endet mit Zahl 5.", "Frist 3.2010 beachten."):
            self.assertIsNone(norm_xml.count_sentences(text), text)


class Checks(unittest.TestCase):
    def check(self, norm: NormRef, name: str = "gii_bgb"):
        index = norm_xml.parse_law_xml((FIX / f"{name}.xml").read_bytes())
        return norm_check.check_norm(norm, index)[:2]

    def test_existing_paragraph(self):
        self.assertEqual(self.check(ref("BGB", "356a")), ("NORM_OK", ""))
        self.assertEqual(self.check(ref("BGB", "356a", absaetze=(5,))), ("NORM_OK", ""))

    def test_missing_absatz(self):
        status, detail = self.check(ref("BGB", "356a", absaetze=(6,)))
        self.assertEqual(status, "ABSATZ_MISSING")
        self.assertIn("Absatz 6", detail)

    def test_satz_is_checked_only_when_countable(self):
        self.assertEqual(self.check(ref("UWG", "5a", (4,), (3,)), "gii_uwg"), ("NORM_OK", ""))
        status, detail = self.check(ref("UWG", "5a", (4,), (4,)), "gii_uwg")
        self.assertEqual(status, "ABSATZ_MISSING")
        self.assertIn("Satz 4", detail)
        self.assertEqual(self.check(ref("UWG", "5a", (1,), (9,)), "gii_uwg"), ("NORM_OK", ""))  # not countable
        self.assertEqual(self.check(ref("UWG", "5a", (), (9,)), "gii_uwg"), ("NORM_OK", ""))  # Absatz unknown

    def test_single_absatz_norm_takes_the_satz_without_absatz(self):
        self.assertEqual(self.check(ref("BGB", "1", (), (1,)))[0], "NORM_OK")
        self.assertEqual(self.check(ref("BGB", "1", (), (2,)))[0], "ABSATZ_MISSING")

    def test_dropped_range_and_unknown_paragraph(self):
        self.assertEqual(self.check(ref("BGB", "4")), ("NORM_MISSING", "weggefallen (Bereich)"))
        self.assertEqual(self.check(ref("BGB", "999")), ("NORM_MISSING", "nicht vorhanden"))
        self.assertEqual(self.check(ref("BGB", "7")), ("NORM_OK", ""))

    def test_article_with_paragraph_and_bare_article(self):
        self.assertEqual(self.check(ref("EGBGB", "1", kind="§", art="246a"), "gii_egbgb"), ("NORM_OK", ""))
        self.assertEqual(self.check(ref("EGBGB", "9", kind="§", art="246a"), "gii_egbgb")[0], "NORM_MISSING")
        self.assertEqual(self.check(ref("EGBGB", "246a", kind="Art"), "gii_egbgb"), ("NORM_OK", ""))
        self.assertEqual(self.check(ref("EGBGB", "999", kind="Art"), "gii_egbgb")[0], "NORM_MISSING")

    def test_old_version_is_not_checked(self):
        self.assertEqual(self.check(ref("BGB", "999", old=True))[0], "NORM_OLD_VERSION")

    def test_reference_text(self):
        self.assertEqual(norm_check.ref_text(ref("UWG", "5a", (4,), (2,))), "§ 5a Abs. 4 Satz 2 UWG")
        self.assertEqual(norm_check.ref_text(ref("EGBGB", "1", kind="§", art="246a")), "Art. 246a § 1 EGBGB")
        self.assertEqual(norm_check.ref_text(ref("GG", "12", kind="Art")), "Art. 12 GG")


class LawMapping(unittest.TestCase):
    def test_toc_and_resolution(self):
        slugs = norm_laws.parse_toc((FIX / "gii_toc.xml").read_bytes())
        self.assertEqual(norm_laws.resolve("UWG", slugs), ("uwg_2004", ""))
        self.assertEqual(norm_laws.resolve("EGBGB", slugs), ("bgbeg", ""))
        self.assertEqual(norm_laws.resolve("TTDSG", slugs)[1], "Altname von TDDDG")
        self.assertEqual(norm_laws.resolve("MStV", slugs)[0], None)
        self.assertIn("nicht im Inhaltsverzeichnis", norm_laws.resolve("PAngV", slugs)[1])

    def test_unusable_toc_raises(self):
        for body in (b"<html>nein</html>", b"<items><item><link>http://www.gesetze-im-internet.de/bgb/xml.zip</link></item></items>"):
            with self.assertRaises(ValueError):
                norm_laws.parse_toc(body)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def client(self, fake, **kw):
        return NormClient(fetch=fake, cache_dir=self.tmp / "cache", sleep=lambda s: None, **kw)

    def test_each_law_is_requested_once_and_cached_for_the_next_run(self):
        fake = UrlFake()
        client = self.client(fake)
        client.toc()
        client.law("bgb")
        client.law("bgb")
        self.assertEqual(len(fake.calls), 2)
        again = self.client(fake)
        self.assertTrue(again.toc().from_cache)
        self.assertTrue(again.law("bgb").from_cache)
        self.assertEqual(len(fake.calls), 2)

    def test_errors_do_not_crash(self):
        for entry in ((404, b""), (503, b"x"), (200, b"kein zip"), (200, b"")):
            fake = UrlFake({"https://www.gesetze-im-internet.de/bgb/xml.zip": entry})
            data = self.client(fake).law("bgb")
            self.assertEqual(data.state, "error", entry)
            self.assertNotIn("\x1b", data.detail)

    def test_offline_without_cache(self):
        fake = UrlFake()
        client = self.client(fake, offline=True)
        self.assertEqual(client.toc().state, "error")
        self.assertEqual(client.law("bgb").state, "error")
        self.assertEqual(fake.calls, [])

    def test_unusable_toc(self):
        fake = UrlFake({TOC_URL: (200, b"<html/>")})
        self.assertEqual(self.client(fake).toc().state, "error")


class WholeCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def results(self, refs, fake=None):
        client = NormClient(fetch=fake or UrlFake(), cache_dir=None, sleep=lambda s: None)
        return norm_check.check_all(refs, client)

    def test_statuses_per_law(self):
        refs = [ref("BGB", "356a"), ref("MStV", "18"), ref("PAngV", "11"), ref("UWG", "5a", (4,), (3,))]
        results, laws = self.results(refs)
        self.assertEqual([r["status"] for r in results], ["NORM_OK", "NORM_UNKNOWN_LAW", "NORM_UNKNOWN_LAW", "NORM_OK"])
        self.assertEqual(laws["BGB"]["stand_date"], "2026-07-23")
        self.assertEqual(laws["UWG"]["stand_bgbl"], "BGBl. 2026 I Nr. 322")
        self.assertEqual(results[0]["heading"], "Elektronische Widerrufsfunktion bei Fernabsatzverträgen")

    def test_unreachable_law_gives_error_only_for_that_law(self):
        fake = UrlFake({"https://www.gesetze-im-internet.de/bgb/xml.zip": (503, b"")})
        results, _ = self.results([ref("BGB", "1"), ref("UWG", "5a")], fake)
        self.assertEqual([r["status"] for r in results], ["ERROR", "NORM_OK"])

    def test_unreachable_toc_gives_error(self):
        fake = UrlFake({TOC_URL: (503, b"")})
        results, _ = self.results([ref("BGB", "1")], fake)
        self.assertEqual(results[0]["status"], "ERROR")

    def test_changed_after_verification(self):
        refs = [NormRef("knowledge/a.md", 3, "UWG", "§", "5", verified_on="2026-05-08"),
                NormRef("knowledge/a.md", 9, "UWG", "§", "5a", verified_on="2026-05-08"),
                NormRef("knowledge/b.md", 4, "UWG", "§", "5", verified_on="2026-11-01"),
                NormRef("knowledge/c.md", 4, "BGB", "§", "1", verified_on=None)]
        _, laws = self.results(refs)
        changed = norm_check.changed_after_verification(refs, laws)
        self.assertEqual([(c["law"], c["file"], c["lines"], c["stand_date"]) for c in changed],
                         [("UWG", "knowledge/a.md", [3, 9], "2026-10-22")])


class BgblTests(unittest.TestCase):
    def checker(self, fake, **kw):
        self.sleeps: list[float] = []
        self.progress: list[str] = []
        kw.setdefault("max_checks", 10)
        return bgbl.BgblChecker(fetch=fake, sleep=self.sleeps.append, clock=lambda: 0.0,
                                progress=self.progress.append, **kw)

    def refs(self, *numbers, year=2026, part="I"):
        return [norm_extract.BgblRef("knowledge/x.md", i + 1, year, n, part) for i, n in enumerate(numbers)]

    def test_ok_and_missing_with_the_crawl_delay(self):
        fake = UrlFake()
        rows, info = self.checker(fake).check_all(self.refs(322, 9999))
        self.assertEqual([(r["ref"], r["status"]) for r in rows],
                         [("BGBl. 2026 I Nr. 322", "BGBL_OK"), ("BGBl. 2026 I Nr. 9999", "BGBL_MISSING")])
        self.assertEqual(info["crawl_delay"], 30.0)
        self.assertTrue(all(abs(s - 30.0) < 1e-6 for s in self.sleeps if s > 1))
        self.assertGreaterEqual(len(self.progress), 2)

    def test_max_checks_limits_requests(self):
        fake = UrlFake()
        rows, _ = self.checker(fake, max_checks=1).check_all(self.refs(322, 9999))
        self.assertEqual([r["status"] for r in rows], ["BGBL_OK", "BGBL_UNCHECKED"])
        self.assertEqual(len([c for c in fake.calls if "/bgbl/" in c]), 1)

    def test_zero_budget_never_touches_the_network(self):
        fake = UrlFake()
        rows, _ = self.checker(fake, max_checks=0).check_all(self.refs(322))
        self.assertEqual(rows[0]["status"], "BGBL_UNCHECKED")
        self.assertEqual(fake.calls, [])

    def test_robots_disallow_stops_everything(self):
        fake = UrlFake({ROBOTS_URL: (200, b"User-agent: *\nDisallow: /\n")})
        rows, info = self.checker(fake).check_all(self.refs(322))
        self.assertEqual(rows[0]["status"], "BGBL_UNCHECKED")
        self.assertIn("untersagt", info["robots"])
        self.assertEqual([c for c in fake.calls if "/bgbl/" in c], [])

    def test_unreadable_robots_stops_everything(self):
        fake = UrlFake({ROBOTS_URL: (503, b"")})
        rows, _ = self.checker(fake).check_all(self.refs(322))
        self.assertEqual(rows[0]["status"], "BGBL_UNCHECKED")

    def test_unexpected_page_and_server_error(self):
        fake = UrlFake({"https://www.recht.bund.de/bgbl/1/2026/322/VO.html": (200, b"<title>Wartung</title>"),
                        "https://www.recht.bund.de/bgbl/1/2026/9999/VO.html": (500, b"")})
        rows, _ = self.checker(fake).check_all(self.refs(322, 9999))
        self.assertEqual([r["status"] for r in rows], ["ERROR", "ERROR"])

    def test_old_years_and_other_parts_are_not_checked(self):
        fake = UrlFake()
        rows, _ = self.checker(fake).check_all(self.refs(5, year=2019) + self.refs(5, part="II"))
        self.assertEqual({r["status"] for r in rows}, {"BGBL_UNCHECKED"})
        self.assertEqual([c for c in fake.calls if "/bgbl/" in c], [])

    def test_duplicates_are_checked_once_and_keep_all_places(self):
        fake = UrlFake()
        rows, _ = self.checker(fake).check_all(self.refs(322, 322))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["places"], ["knowledge/x.md:1", "knowledge/x.md:2"])

    def test_offline_never_requests(self):
        fake = UrlFake()
        rows, _ = self.checker(fake, offline=True).check_all(self.refs(322))
        self.assertEqual((rows[0]["status"], fake.calls), ("BGBL_UNCHECKED", []))


KB_TEXT = (
    "---\naktualisiert: 2026-05-08\nverifiziert-am: 2026-05-08\n---\n"
    "# Thema\n"
    "Pflicht nach § 356a BGB und § 5a Abs. 4 Satz 3 UWG.\n"
    "Weggefallen laut § 4 BGB, falsch § 356a Abs. 9 BGB.\n"
    "Art. 6 DSGVO und § 18 MStV sowie BGBl. 2026 I Nr. 322 und BGBl. 2026 I Nr. 9999.\n"
)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.kb = self.tmp / "knowledge"
        (self.kb / "themen").mkdir(parents=True)
        self.file = self.kb / "themen" / "t.md"
        self.file.write_text(KB_TEXT, encoding="utf-8")
        self.fake = UrlFake()

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        code = cli.main(["--path", str(self.kb), "--cache-dir", str(self.tmp / "cache"), "--check-norms", *args],
                        fetch=self.fake, sleep=lambda s: None, stdout=out, stderr=err)
        return code, out.getvalue(), err.getvalue()

    def test_json_counts_lists_and_laws(self):
        code, text, err = self.run_cli("--json", "--max-bgbl", "5")
        self.assertEqual(code, 0)
        data = json.loads(text)
        self.assertEqual(data["mode"], "norms")
        counts = data["summary"]["counts"]
        self.assertEqual((counts["NORM_OK"], counts["NORM_MISSING"], counts["ABSATZ_MISSING"],
                          counts["NORM_UNKNOWN_LAW"]), (2, 1, 1, 1))
        by_ref = {n["ref"]: n for n in data["norms"]}
        self.assertEqual(by_ref["§ 4 BGB"]["status"], "NORM_MISSING")
        self.assertEqual((by_ref["§ 4 BGB"]["file"], by_ref["§ 4 BGB"]["line"]), ("knowledge/themen/t.md", 7))
        self.assertEqual(data["summary"]["eu_counts"], {"DSGVO": 1})
        self.assertEqual({law["law"] for law in data["laws"]}, {"BGB", "UWG", "MStV"})
        self.assertEqual([b["status"] for b in data["bgbl"]], ["BGBL_OK", "BGBL_MISSING"])
        self.assertIn("BGBl. 2026 I Nr. 322", err)
        self.assertEqual([(c["law"], c["stand_date"]) for c in data["changed_after_verification"]],
                         [("BGB", "2026-07-23"), ("UWG", "2026-10-22")])

    def test_it_never_writes_into_the_knowledge_base(self):
        before = self.file.read_bytes()
        self.run_cli("--json", "--max-bgbl", "0")
        self.assertEqual(self.file.read_bytes(), before)
        self.assertEqual([p.name for p in self.kb.rglob("*") if p.is_file()], ["t.md"])

    def test_bgbl_check_is_opt_in(self):
        _, text, _ = self.run_cli("--json")
        self.assertEqual([c for c in self.fake.calls if "recht.bund.de" in c], [])
        self.assertEqual({b["status"] for b in json.loads(text)["bgbl"]}, {"BGBL_UNCHECKED"})

    def test_max_bgbl_zero_sends_no_bgbl_request(self):
        self.run_cli("--json", "--max-bgbl", "0")
        self.assertEqual([c for c in self.fake.calls if "recht.bund.de" in c], [])

    def test_human_report(self):
        _, text, _ = self.run_cli("--max-bgbl", "0")
        self.assertIn("NORM_MISSING", text)
        self.assertIn("knowledge/themen/t.md:7", text)
        self.assertIn("Hinweis, kein Fehler", text)

    def test_default_mode_does_not_check_norms(self):
        out = io.StringIO()
        cli.main(["--path", str(self.kb), "--cache-dir", str(self.tmp / "cache"), "--json", "--no-eu"],
                 fetch=self.fake, sleep=lambda s: None, stdout=out)
        self.assertNotIn("norms", json.loads(out.getvalue()))
        self.assertFalse([c for c in self.fake.calls if "gesetze-im-internet" in c])

    def test_incompatible_options_are_rejected(self):
        for extra in ("--write-ecli", "--only-pending"):
            with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
                self.run_cli(extra)
            self.assertEqual(ctx.exception.code, 2)

    def test_gii_down_gives_errors_and_exit_zero(self):
        self.fake = UrlFake({TOC_URL: (503, b"")})
        code, text, _ = self.run_cli("--json", "--max-bgbl", "0")
        self.assertEqual(code, 0)
        self.assertGreaterEqual(json.loads(text)["summary"]["counts"]["ERROR"], 1)


if __name__ == "__main__":
    unittest.main()
