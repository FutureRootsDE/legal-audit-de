"""Offline tests for client_report.embed, .render and .pipeline (spec 6.5, 6.6, 6.8, 6.9.2 step 5).

Security focus (plan, Review Focus 1): hostile website content in verbatim fields must appear
as escaped text, links only for https references, no external requests from the report.
"""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.accent import contrast_ratio
from client_report.catalog import load_catalog
from client_report.derive import derive
from client_report.embed import SIZE_BUDGET_BYTES, data_uri, find_external_refs
from client_report.models import ReportInputError
from client_report.pipeline import RenderResult, build_report
from client_report.render import CSS_PATH, PAGED_JS_ENABLED, TEMPLATE_PATH, render_html, template_text_items
from client_report.textcheck import check_texts, load_forbidden_phrases
from client_report.texts import (
    DISCLAIMER_FULL,
    DISCLAIMER_SHORT,
    FOOTER,
    LAWYER_SENTENCE,
    PAGE_OF_WORD,
    PAGE_WORD,
    PASS_ON_SENTENCE,
    STATUS_LABEL,
    STATUS_SHORT,
    TITLE,
)
from client_report_support import make_report_dir, open_result, valid_findings, write_png

CAT = load_catalog()
GOLDEN = Path(__file__).resolve().parent / "fixtures" / "client_test" / "golden_structure.json"
HOSTILE = '</p><script>alert(1)</script><img src=x onerror=alert(2)>"'
EVIL_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><script>alert(3)</script>'
            '<rect width="10" height="10" fill="#1F4E79"/></svg>')


# ---------------------------------------------------------------- fixtures

def none_result(test_id: str) -> dict:
    return {"id": test_id, "status": "none", "reason_kind": "not_checkable",
            "reason": "Die Seite war während der Prüfung nicht erreichbar."}


def all_status_mix() -> dict:
    """Every status: two defects, a measurable and a legal_judgment notice, a not_checkable, n/a rows."""
    return valid_findings(CAT, shop=False, results=[
        open_result("CK-03", "defect", "HIGH"),
        open_result("SEC-01", "defect", "MED"),
        open_result("UWG-03", "notice", "MED"),
        open_result("A11Y-02", "notice", "LOW"),
        none_result("IMP-03"),
    ])


def findings_with_defects(ids: list[str]) -> dict:
    return valid_findings(CAT, results=[open_result(i, "defect", "HIGH") for i in ids])


# ---------------------------------------------------------------- html helpers

class _Collector(HTMLParser):
    """Start tags with attributes, text nodes outside style/script, and the marker order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.texts: list[str] = []
        self.order: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if a.get("data-section"):
            self.order.append(f"section:{a['data-section']}")
        if a.get("data-id"):
            self.order.append(f"id:{a['data-id']}")
        if tag in ("style", "script"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.texts.append(data)


def parse(html: str) -> _Collector:
    c = _Collector()
    c.feed(html)
    c.close()
    return c


def structure(html: str) -> list[str]:
    """(data-section | data-id) markers in document order."""
    return parse(html).order


def section(html: str, name: str) -> str:
    """Markup from the element carrying data-section=name up to the next section marker."""
    start = html.index(f'data-section="{name}"')
    nxt = html.find("data-section=", start + 1)
    return html[start:nxt if nxt != -1 else len(html)]


def visible_text(html: str) -> str:
    return " ".join(parse(html).texts)


# ---------------------------------------------------------------- base

class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.rd = make_report_dir(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, findings: dict) -> None:
        (self.rd / "findings.json").write_text(json.dumps(findings, ensure_ascii=False), encoding="utf-8")

    def run_build(self, findings: dict) -> RenderResult:
        self.write(findings)
        return build_report(self.rd, CAT)

    def build(self, findings: dict) -> str:
        return self.run_build(findings).html_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- embed

class Embed(unittest.TestCase):
    def test_data_uri_mime_by_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "a.png"
            write_png(png, (1, 2, 3))
            self.assertTrue(data_uri(png).startswith("data:image/png;base64,iVBOR"))
            for name, mime in (("b.jpg", "image/jpeg"), ("c.JPEG", "image/jpeg"), ("d.webp", "image/webp"),
                               ("e.svg", "image/svg+xml"), ("f.woff2", "font/woff2")):
                p = Path(tmp) / name
                p.write_bytes(b"x")
                self.assertTrue(data_uri(p).startswith(f"data:{mime};base64,"), name)

    def test_data_uri_rejects_unknown_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.html"
            p.write_text("<script></script>", encoding="utf-8")
            with self.assertRaises(ValueError):
                data_uri(p)

    def test_find_external_refs_detects(self):
        self.assertEqual(len(find_external_refs(
            '<img src="https://x/y.png"><link href="//cdn/x.css"><style>a{background:url(http://t)}</style>')), 3)
        self.assertEqual(find_external_refs('<a href="https://gesetze-im-internet.de/">x</a>'), [])

    def test_find_external_refs_more_vectors(self):
        cases = ('<style>@import "x.css";</style>', '<div style="background:url(//t/x.png)"></div>',
                 '<img srcset="https://x/a.png 2x">', "<iframe src='//evil'></iframe>",
                 '<a href="javascript:alert(1)">x</a>', '<a href="http://plain">x</a>', '<base href="https://x/">')
        for html in cases:
            self.assertNotEqual(find_external_refs(html), [], html)

    def test_find_external_refs_ignores_text_and_data(self):
        html = ('<p>GET https://t.example/?src=https://x.example/ url(https://y)</p>'
                '<img src="data:image/png;base64,AAAA" alt=""><a href="#a-ck-03">CK-03</a>')
        self.assertEqual(find_external_refs(html), [])

    def test_anchor_scheme_check_is_case_insensitive(self):
        self.assertEqual(find_external_refs('<a href="HTTPS://www.bsi.bund.de/">x</a>'), [])
        self.assertNotEqual(find_external_refs('<a href="HTTP://plain/">x</a>'), [])
        self.assertNotEqual(find_external_refs('<a href="JavaScript:alert(1)">x</a>'), [])


# ---------------------------------------------------------------- render

class Render(Base):
    def test_paged_js_disabled_per_spike(self):
        self.assertFalse(PAGED_JS_ENABLED)

    def test_hostile_content_is_escaped(self):
        row = open_result("CK-03", "defect", "HIGH")
        row["one_liner"] = "Banner"
        row["client_text"] = HOSTILE
        row["evidence"][0]["alt"] = HOSTILE
        row["evidence"][0]["caption"] = HOSTILE
        row["evidence"][1]["excerpt"] = HOSTILE
        row["fix"]["snippets"][0]["code"] = HOSTILE
        row["retest"]["command"] = HOSTILE
        f = valid_findings(CAT, results=[row])
        f["client"]["name"] = HOSTILE
        f["issuer"]["company"] = HOSTILE
        f["run"]["user_agent"] = HOSTILE
        html = self.build(f)
        doc = parse(html)
        self.assertNotIn("<script>alert(1)", html)
        self.assertNotIn("script", [tag for tag, _ in doc.tags])
        for tag, attrs in doc.tags:
            self.assertFalse(any(k.startswith("on") for k in attrs), (tag, attrs))
            self.assertNotEqual(attrs.get("src"), "x")
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("&lt;img src=x onerror=alert(2)&gt;&quot;", html)
        alts = [a.get("alt") for t, a in doc.tags if t == "img" and a.get("alt")]
        self.assertIn(HOSTILE, alts)          # attribute value stays intact, no break-out
        self.assertIn("Logo " + HOSTILE, alts)

    def test_non_https_reference_is_text_not_link(self):
        # Bypasses input validation on purpose: the renderer must not trust it either.
        row = open_result("CK-03", "defect", "HIGH")
        row["references"] = ["javascript:alert(1)", "data:text/html,<b>x</b>", "http://x.example/",
                             "https://ok.example/a?b=1"]
        model, _ = derive(valid_findings(CAT, results=[row]), CAT)
        html = render_html(model, CAT, self.rd)
        hrefs = [a.get("href") for t, a in parse(html).tags if t == "a" and a.get("href", "").startswith(("http", "j", "d"))]
        self.assertEqual(hrefs, ["https://ok.example/a?b=1"])
        self.assertIn("javascript:alert(1)", visible_text(html))
        self.assertIn("data:text/html,&lt;b&gt;x&lt;/b&gt;", html)
        self.assertIn('rel="noreferrer"', html)

    def test_upper_case_https_reference_renders_with_lower_case_scheme(self):
        row = open_result("CK-03", "notice", "LOW") | {"references": ["HTTPS://www.bsi.bund.de/Pfad"]}
        html = self.build(valid_findings(CAT, results=[row]))   # full pipeline: validation passes it
        hrefs = [a.get("href") for t, a in parse(html).tags if t == "a" and "bsi" in a.get("href", "")]
        self.assertEqual(hrefs, ["https://www.bsi.bund.de/Pfad"])

    def test_reference_with_userinfo_is_text_not_link(self):
        row = open_result("CK-03", "defect", "HIGH")
        row["references"] = ["https://bank.de@evil.example/"]
        model, _ = derive(valid_findings(CAT, results=[row]), CAT)
        html = render_html(model, CAT, self.rd)
        self.assertFalse(any(a.get("href", "").startswith("https://bank") for t, a in parse(html).tags if t == "a"))

    def test_lawyer_sentence_twice_per_defect(self):
        html = self.build(findings_with_defects(["CK-01", "SEC-01"]))
        self.assertEqual(html.count(LAWYER_SENTENCE), 4)
        self.assertEqual(section(html, "part-a").count(LAWYER_SENTENCE), 2)
        self.assertEqual(section(html, "part-b").count(LAWYER_SENTENCE), 2)

    def test_page_counter_text_comes_from_texts_not_css_file(self):
        html = self.build(valid_findings(CAT))
        self.assertIn(f'@bottom-right {{ content: "{PAGE_WORD} " counter(page) " {PAGE_OF_WORD} " counter(pages); }}', html)
        self.assertNotIn(f'"{PAGE_WORD} "', CSS_PATH.read_text(encoding="utf-8"))

    def test_downgraded_defect_has_no_lawyer_sentence(self):
        f = valid_findings(CAT, shop=True, started="2026-06-01T08:00:00Z",
                           results=[open_result("SHOP-04", "defect", "CRIT")])
        html = self.build(f)
        self.assertEqual(html.count(LAWYER_SENTENCE), 0)
        self.assertIn("Pflicht gilt ab 19.06.2026.", section(html, "overview"))

    def test_pass_on_sentence_on_cover_and_disclaimers(self):
        html = self.build(all_status_mix())
        cover = section(html, "cover")
        self.assertIn(PASS_ON_SENTENCE, cover)
        self.assertIn(DISCLAIMER_SHORT, cover)
        self.assertIn("§ 2 RDG", cover)
        self.assertIn(TITLE.replace("&", "&amp;"), cover)
        self.assertIn(DISCLAIMER_FULL, section(html, "appendix-d"))
        self.assertIn(FOOTER, html)

    def test_no_bestanden_no_mangel(self):
        html = self.build(all_status_mix())
        doc = parse(html)
        attrs = " ".join(v for _, a in doc.tags for v in a.values() if v and not v.startswith("data:"))
        low = (visible_text(html) + " " + attrs).lower()
        self.assertNotIn("bestanden", low)
        self.assertNotIn("mangel", low)

    def test_no_external_refs_and_svg_logo_as_img(self):
        (self.rd / "assets" / "logo.svg").write_text(EVIL_SVG, encoding="utf-8")
        f = valid_findings(CAT)
        f["issuer"]["logo_file"] = "assets/logo.svg"
        html = self.build(f)
        self.assertEqual(find_external_refs(html), [])
        logos = [a for t, a in parse(html).tags if t == "img" and (a.get("class") or "") == "logo"]
        self.assertEqual(len(logos), 1)
        self.assertTrue(logos[0]["src"].startswith("data:image/svg+xml;base64,"))
        self.assertNotIn("<svg", html)
        self.assertNotIn("alert(3)", html)

    def test_csp_blocks_scripts_and_remote_loads(self):
        html = self.build(valid_findings(CAT))
        m = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)"', html)
        self.assertIsNotNone(m)
        csp = m.group(1)
        self.assertIn("default-src 'none'", csp)
        self.assertNotIn("script-src", csp)
        self.assertNotIn("http", csp)
        self.assertIn('<html lang="de">', html)

    def test_structure_matches_golden(self):
        html = self.build(all_status_mix())
        self.assertEqual(structure(html), json.loads(GOLDEN.read_text(encoding="utf-8")))

    def test_golden_order_and_one_overview_row_per_id(self):
        order = json.loads(GOLDEN.read_text(encoding="utf-8"))
        sections = [s.split(":", 1)[1] for s in order if s.startswith("section:")]
        self.assertEqual(sections, ["cover", "overview", "part-a", "part-b", "appendix-a", "appendix-b",
                                    "appendix-c", "appendix-d"])
        overview = order[order.index("section:overview") + 1:order.index("section:part-a")]
        self.assertEqual(overview, [f"id:{e.id}" for e in CAT.entries])
        part_a = order[order.index("section:part-a") + 1:order.index("section:part-b")]
        self.assertEqual(part_a, [f"id:{e.id}" for e in CAT.entries])
        part_b = order[order.index("section:part-b") + 1:order.index("section:appendix-a")]
        self.assertEqual(part_b, ["id:CK-03", "id:SEC-01", "id:UWG-03", "id:A11Y-02"])

    def test_render_is_deterministic(self):
        f = all_status_mix()
        self.assertEqual(self.build(f), self.build(f))

    def test_counts_shown_match_model(self):
        f = all_status_mix()
        html = self.build(f)
        model, _ = derive(f, CAT)
        shown = {k: int(v) for k, v in re.findall(r'data-count="(\w+)">(\d+)<', section(html, "overview"))}
        self.assertEqual(shown, dict(model.counts))
        for status, label in STATUS_LABEL.items():
            self.assertIn(label, section(html, "overview"), status)

    def test_status_labels_and_icons(self):
        html = self.build(all_status_mix())
        overview = section(html, "overview")
        for short in STATUS_SHORT.values():
            self.assertIn(short, overview)
        icons = [a for t, a in parse(html).tags if t == "img" and "status-icon" in (a.get("class") or "")]
        self.assertTrue(icons)
        for a in icons:
            self.assertEqual(a.get("alt"), "")
            self.assertEqual(a.get("aria-hidden"), "true")
            self.assertTrue(a["src"].startswith("data:image/svg+xml;base64,"))

    def test_na_rows_grey_but_a11y_never(self):
        f = valid_findings(CAT, shop=False, bfsg=False)
        html = self.build(f)
        rows = {a["data-id"]: (a.get("class") or "") for t, a in parse(section(html, "overview")).tags
                if t == "tr" and a.get("data-id")}
        self.assertIn("is-na", rows["SHOP-04"])
        for test_id, cls in rows.items():
            if test_id.startswith("A11Y-"):
                self.assertNotIn("is-na", cls, test_id)

    def test_ids_link_overview_part_a_part_b(self):
        html = self.build(all_status_mix())
        self.assertIn('href="#a-ck-03"', section(html, "overview"))
        self.assertIn('id="a-ck-03"', section(html, "part-a"))
        self.assertIn('href="#b-ck-03"', section(html, "part-a"))
        self.assertIn('id="b-ck-03"', section(html, "part-b"))

    def test_review_question_only_for_legal_judgment(self):
        html = self.build(all_status_mix())
        part_a = section(html, "part-a")
        uwg = part_a[part_a.index('id="a-uwg-03"'):part_a.index('id="a-uwg-03"') + 4000]
        self.assertIn("Prüffrage für Ihre Rechtsberatung", uwg)
        sec = part_a[part_a.index('id="a-sec-02"'):part_a.index('id="a-sec-03"')]
        self.assertNotIn("Prüffrage für Ihre Rechtsberatung", sec)

    def test_no_wall_clock_time(self):
        html = self.build(all_status_mix())
        self.assertIn("17.11.2026", section(html, "cover"))
        self.assertIn("17.11.2026, 09:12:03 UTC", section(html, "appendix-a"))

    def test_status_colors_contrast(self):
        css = CSS_PATH.read_text(encoding="utf-8")
        for name in ("pass", "notice", "defect", "none"):
            m = re.search(rf"--status-{name}:\s*(#[0-9A-Fa-f]{{6}})\s*;", css)
            self.assertIsNotNone(m, name)
            self.assertGreaterEqual(contrast_ratio(m.group(1)), 4.5, name)

    def test_accent_from_issuer_with_contrast(self):
        f = valid_findings(CAT)
        f["issuer"]["accent_color"] = "#FFD54F"   # too light, must be darkened
        html = self.build(f)
        m = re.search(r"--accent:\s*(#[0-9A-Fa-f]{6})", html)
        self.assertIsNotNone(m)
        self.assertGreaterEqual(contrast_ratio(m.group(1)), 4.5)

    def test_template_text_passes_checks(self):
        items = template_text_items()
        self.assertEqual(check_texts(items, load_forbidden_phrases()), [])
        self.assertTrue(TEMPLATE_PATH.is_file())

    def test_fonts_embedded(self):
        html = self.build(valid_findings(CAT))
        self.assertEqual(html.count("data:font/woff2;base64,"), 5)
        self.assertIn('font-family: "IBM Plex Sans"', html)


# ---------------------------------------------------------------- pipeline

class Pipeline(Base):
    def test_success_writes_report(self):
        result = self.run_build(all_status_mix())
        self.assertEqual(result.html_path, self.rd / "report.html")
        self.assertTrue(result.html_path.is_file())
        self.assertEqual(result.warnings, [])

    def test_invalid_input_raises_and_writes_nothing(self):
        f = valid_findings(CAT, results=[open_result("UWG-03", "defect", "HIGH")])   # legal_judgment
        with self.assertRaises(ReportInputError) as ctx:
            self.run_build(f)
        self.assertTrue(any(i.path == "results[0].status" for i in ctx.exception.issues))
        self.assertFalse((self.rd / "report.html").exists())

    def test_invariant_violation_raises(self):
        f = valid_findings(CAT, results=[open_result("CK-03", "notice", "LOW")], top_actions=[])
        with self.assertRaises(ReportInputError) as ctx:
            self.run_build(f)
        self.assertTrue(any(i.path == "summary.top_actions" for i in ctx.exception.issues))
        self.assertFalse((self.rd / "report.html").exists())

    def test_warnings_from_derive_are_passed_on(self):
        extra = open_result("SHOP-04", "notice", "LOW")
        result = self.run_build(valid_findings(CAT, shop=False, results_extra=[extra]))
        self.assertTrue(any("SHOP-04" in w for w in result.warnings))

    def test_size_budget_warning(self):
        big = self.rd / "evidence" / "big.png"
        big.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * (SIZE_BUDGET_BYTES + 1))
        row = open_result("CK-03", "defect", "HIGH")
        row["evidence"][0]["file"] = "evidence/big.png"
        result = self.run_build(valid_findings(CAT, results=[row]))
        self.assertIn("Hinweis: report.html ist größer als 10 MB.", result.warnings)
        self.assertTrue(result.html_path.is_file())

    def test_missing_findings_file(self):
        with self.assertRaises(ReportInputError):
            build_report(self.rd, CAT)

    def test_render_check_failure_becomes_input_error(self):
        from unittest import mock
        with mock.patch("client_report.pipeline.render_html",
                        side_effect=RuntimeError("report.html enthält externe Referenzen: <a href=x>")):
            with self.assertRaises(ReportInputError) as ctx:
                self.run_build(valid_findings(CAT))
        issue = ctx.exception.issues[0]
        self.assertEqual(issue.path, "report.html")
        self.assertIn("externe Referenzen", issue.message)
        self.assertNotRegex(issue.message, "[–—]| - ")
        self.assertFalse((self.rd / "report.html").exists())

    def test_pipeline_checks_catalog_completeness(self):
        from unittest import mock
        import client_report.pipeline as pipeline
        seen = {}

        def spy(model, catalog=None):
            seen["catalog"] = catalog
            return []
        with mock.patch.object(pipeline, "check_invariants", side_effect=spy):
            self.run_build(valid_findings(CAT))
        self.assertIs(seen["catalog"], CAT)


if __name__ == "__main__":
    unittest.main()
