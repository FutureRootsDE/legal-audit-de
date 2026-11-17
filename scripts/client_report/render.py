"""Render the derived report model into one self-contained report.html (spec 6.5, 6.6, 6.8, 6.9.2 step 5).

Security rules (spec 6.8 "Untrusted Input"): every value from findings.json goes through
`html.escape(..., quote=True)`; there is no raw HTML from the input; only `references[]` that
are plain https URLs become links (rel="noreferrer"), everything else is text; images come
only from the report folder via `safe_evidence_path` and are embedded as data URIs; an SVG
logo is only ever used through `<img>`, never inlined. Fixed sentences come from texts.py.

Spike result (docs/superpowers/spikes/2026-11-17-pagedjs-chrome-pdf.md): no Paged.js, so the
overview has no page column; finding IDs are anchor links. Status symbols are not in the
embedded font subset and are drawn as small SVG images, always with the text label next to them.
"""
from __future__ import annotations

import base64
import html
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from string import Template
from typing import Any, Iterable, Iterator, Mapping
from urllib.parse import urlsplit

from . import texts as T
from .accent import DEFAULT_ACCENT, ensure_contrast
from .embed import data_uri, find_external_refs
from .models import Catalog, DerivedResult, ReportModel
from .paths import domain_slug, safe_evidence_path
from .schema import STATUSES, UTC_FORMAT
from .textcheck import check_texts, load_forbidden_phrases

PAGED_JS_ENABLED = False  # Task 3 spike: unstable page count with the CLI print route

ASSETS_DIR = Path(__file__).resolve().parents[2] / "templates" / "client-test"
TEMPLATE_PATH = ASSETS_DIR / "report.html.tmpl"
CSS_PATH = ASSETS_DIR / "report.css"
FONTS_DIR = ASSETS_DIR / "fonts"
FONT_FACES = (
    ("IBM Plex Sans", "IBMPlexSans-Regular.woff2", 400, "normal"),
    ("IBM Plex Sans", "IBMPlexSans-Italic.woff2", 400, "italic"),
    ("IBM Plex Sans", "IBMPlexSans-SemiBold.woff2", 600, "normal"),
    ("IBM Plex Sans", "IBMPlexSans-Bold.woff2", 700, "normal"),
    ("IBM Plex Mono", "IBMPlexMono-Regular.woff2", 400, "normal"),
)
OPEN_STATUSES = ("notice", "defect")
DATE_FORMAT = "%d.%m.%Y"
STATUS_COLOR_RE = re.compile(r"--status-(pass|notice|defect|none):\s*(#[0-9A-Fa-f]{6})\s*;")
UNSAFE_LINK_RE = re.compile(r"[\s\x00-\x1f\x7f\"'<>`\\]")
HTTPS_PREFIX = "https://"
PLACEHOLDER_RE = re.compile(r"\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})")
# 16x16 status glyphs; {c} is the fixed status color from report.css.
ICON_SHAPES = {
    "pass": '<path d="M3 8.6l3.2 3.2L13 4.6" fill="none" stroke="{c}" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
    "notice": '<path d="M8 1.8L15.2 14.4H0.8Z" fill="{c}"/>',
    "defect": '<path d="M3.5 3.5l9 9M12.5 3.5l-9 9" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>',
    "none": '<path d="M3 8h10" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>',
}
SVG_WRAP = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">{body}</svg>'


# ---------------------------------------------------------------- small helpers

def _e(value: Any) -> str:
    """Escape any value for HTML text and attribute positions."""
    return html.escape("" if value is None else str(value), quote=True)


def _get(data: Any, dotted: str) -> Any:
    node = data
    for part in dotted.split("."):
        if not isinstance(node, Mapping):
            return None
        node = node.get(part)
    return node


def _texts(value: Any) -> list[str]:
    """Non-empty strings of a list value; anything else gives []."""
    return [v for v in value if isinstance(v, str) and v.strip()] if isinstance(value, list) else []


def _css_string(value: str) -> str:
    """Double-quoted CSS string literal; `<` is escaped so the value cannot close the style element."""
    out = value.replace("\\", "\\\\").replace('"', '\\"').replace("<", "\\3C ")
    return '"' + re.sub(r"[\r\n\f]", lambda _: "\\A ", out) + '"'


def _is_https_link(value: Any) -> bool:
    if not isinstance(value, str) or UNSAFE_LINK_RE.search(value):
        return False
    parts = urlsplit(value)
    return (value.lower().startswith(HTTPS_PREFIX) and parts.scheme == "https" and bool(parts.hostname)
            and "@" not in parts.netloc)


def _link_or_text(value: Any) -> str:
    """https reference as link, anything else as text. The scheme in href is normalised to lower
    case (`HTTPS://` is valid input), matching the case-insensitive anchor check in embed."""
    if _is_https_link(value):
        href = HTTPS_PREFIX + value[len(HTTPS_PREFIX):]
        return f'<a href="{_e(href)}" rel="noreferrer">{_e(value)}</a>'
    return _e(value)


def _utc_display(value: Any) -> str:
    try:
        return datetime.strptime(value, UTC_FORMAT).strftime(T.UTC_DISPLAY_FORMAT)
    except (TypeError, ValueError):
        return "" if value is None else str(value)


def _anchor(prefix: str, test_id: str) -> str:
    return f"{prefix}-{test_id.lower()}"


# ---------------------------------------------------------------- status

def _status_colors(css: str) -> dict[str, str]:
    colors = dict(STATUS_COLOR_RE.findall(css))
    missing = [s for s in STATUSES if s not in colors]
    if missing:
        raise RuntimeError(f"report.css: Statusfarbe fehlt für {', '.join(missing)}")
    return colors


def _status_icons(colors: Mapping[str, str]) -> dict[str, str]:
    icons = {}
    for status, shape in ICON_SHAPES.items():
        svg = SVG_WRAP.format(body=shape.format(c=colors[status]))
        icons[status] = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return icons


class _Ctx:
    """Render context shared by the section builders."""

    def __init__(self, model: ReportModel, catalog: Catalog, report_dir: Path, icons: Mapping[str, str]) -> None:
        self.model = model
        self.catalog = catalog
        self.report_dir = report_dir
        self.icons = icons
        self.findings = model.findings

    def status(self, status: str, short: bool = False) -> str:
        label = (T.STATUS_SHORT if short else T.STATUS_LABEL).get(status, status)
        return (f'<span class="status status-{_e(status)}"><img class="status-icon" src="{self.icons[status]}" '
                f'alt="" aria-hidden="true" width="12" height="12">{_e(label)}</span>')


def _notes(r: DerivedResult) -> str:
    if not r.notes:
        return ""
    return '<ul class="notes">' + "".join(f"<li>{_e(n)}</li>" for n in r.notes) + "</ul>"


def _norms(r: DerivedResult) -> str:
    return _e("; ".join(b.norm for b in r.entry.legal_basis))


def _effort(r: DerivedResult) -> str:
    effort = _get(r.data, "fix.effort")
    if not isinstance(effort, Mapping):
        return ""
    return _e(T.EFFORT_FORMAT.format(level=effort.get("level", ""), minutes=effort.get("minutes", "")))


def _by_area(model: ReportModel, catalog: Catalog) -> Iterator[tuple[Any, list[DerivedResult]]]:
    for area in catalog.areas:
        yield area, [r for r in model.results if r.entry.area == area.prefix]


# ---------------------------------------------------------------- cover

def _issuer_block(ctx: _Ctx) -> str:
    issuer = ctx.findings.get("issuer") or {}
    logo = safe_evidence_path(ctx.report_dir, issuer.get("logo_file"))
    alt = T.LOGO_ALT.format(company=issuer.get("company", ""))
    lines = [issuer.get("company"), *_texts(issuer.get("address"))]
    lines += [issuer.get(k) for k in ("contact", "phone", "email", "website")]
    address = "<br>".join(_e(line) for line in lines if isinstance(line, str) and line.strip())
    return (f'<header class="letterhead"><img class="logo" src="{data_uri(logo)}" alt="{_e(alt)}">'
            f'<address class="issuer-address">{address}</address></header>')


def _client_lines(client: Mapping[str, Any]) -> str:
    lines = [client.get("name"), client.get("company"), *_texts(client.get("address"))]
    return "<br>".join(_e(line) for line in lines if isinstance(line, str) and line.strip())


def _cover(ctx: _Ctx) -> str:
    run = ctx.findings.get("run") or {}
    issuer = ctx.findings.get("issuer") or {}
    domain = run.get("domain", "")
    by = ", ".join(v for v in (issuer.get("company"), issuer.get("contact")) if isinstance(v, str) and v.strip())
    facts = (
        (T.LABEL_SITE, _e(domain)),
        (T.LABEL_CLIENT, _client_lines(ctx.findings.get("client") or {})),
        (T.LABEL_CHECK_DATE, _e(ctx.model.check_date.strftime(DATE_FORMAT))),
        (T.LABEL_REPORT_ID, _e(f"{ctx.model.check_date.isoformat()}-{domain_slug(domain)}")),
        (T.LABEL_ISSUER, _e(by)),
    )
    rows = "".join(f"<dt>{_e(label)}</dt><dd>{value}</dd>" for label, value in facts)
    return (_issuer_block(ctx)
            + f'<div class="cover-title"><h1 id="cover-title">{_e(T.TITLE)}</h1>'
            + f'<p class="subtitle">{_e(T.SUBTITLE)}</p></div>'
            + f'<dl class="facts">{rows}</dl>'
            + f'<div class="cover-notice"><p><strong>{_e(T.PASS_ON_SENTENCE)}</strong></p>'
            + f"<p>{_e(T.DISCLAIMER_SHORT)}</p></div>")


# ---------------------------------------------------------------- overview

def _counts(ctx: _Ctx) -> str:
    items = "".join(f'<li>{ctx.status(s)}<span class="num" data-count="{s}">{int(ctx.model.counts.get(s, 0))}</span></li>'
                    for s in STATUSES)
    return f'<ul class="counts" aria-label="{_e(T.LABEL_COUNTS)}">{items}</ul>'


def _top_actions(ctx: _Ctx) -> str:
    ids = [i for i in _texts(_get(ctx.findings, "summary.top_actions")) if i in ctx.catalog.by_id]
    if not ids:
        return ""
    items = "".join(f'<li><a href="#{_anchor("a", i)}">{_e(i)}</a> {_e(ctx.catalog.by_id[i].title)}</li>'
                    for i in ids)
    return f'<h2>{_e(T.SECTION_TITLES["top_actions"])}</h2><ol class="top-actions">{items}</ol>'


def _result_line(r: DerivedResult) -> str:
    return _e(r.reason if r.status == "none" else _get(r.data, "one_liner"))


def _overview_row(ctx: _Ctx, r: DerivedResult) -> str:
    cls = ' class="is-na"' if r.reason_kind == "not_applicable" else ""
    return (f'<tr data-id="{_e(r.entry.id)}"{cls}><td class="col-id"><a href="#{_anchor("a", r.entry.id)}">'
            f'{_e(r.entry.id)}</a></td><td>{_e(r.entry.title)}</td><td class="col-status">'
            f"{ctx.status(r.status, short=True)}</td><td>{_result_line(r)}{_notes(r)}</td></tr>")


def _overview_table(ctx: _Ctx, title: str, rows: list[DerivedResult]) -> str:
    head = "".join(f'<th scope="col"{cls}>{_e(label)}</th>' for label, cls in (
        (T.COLUMN_ID, ' class="col-id"'), (T.COLUMN_TEST, ""), (T.COLUMN_STATUS, ' class="col-status"'),
        (T.COLUMN_RESULT, ' class="col-result"')))
    body = "".join(_overview_row(ctx, r) for r in rows)
    return f"<table><caption>{_e(title)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _overview(ctx: _Ctx) -> str:
    sentences = "".join(f"<p>{_e(s)}</p>" for s in _texts(_get(ctx.findings, "summary.sentences")))
    tables = "".join(_overview_table(ctx, area.title, rows) for area, rows in _by_area(ctx.model, ctx.catalog) if rows)
    return (f'<h1 id="overview-title">{_e(T.SECTION_TITLES["overview"])}</h1>{_counts(ctx)}'
            f'<h2>{_e(T.SECTION_TITLES["summary"])}</h2><div class="summary">{sentences}</div>'
            f"{_top_actions(ctx)}{tables}")


# ---------------------------------------------------------------- part A

def _fields(pairs: Iterable[tuple[str, str]]) -> str:
    return '<dl class="fields">' + "".join(f"<dt>{_e(k)}</dt><dd>{v}</dd>" for k, v in pairs if v) + "</dl>"


def _review_question(r: DerivedResult) -> str:
    if r.entry.basis != "legal_judgment":
        return ""
    return _e(_get(r.data, "review_question") or "")


def _lawyer(r: DerivedResult) -> str:
    return f'<p class="lawyer">{_e(T.LAWYER_SENTENCE)}</p>' if r.status == "defect" else ""


def _observed(r: DerivedResult) -> str:
    if r.status == "none":
        text = r.reason
    elif r.status in OPEN_STATUSES:
        text = _get(r.data, "client_text")
    else:
        text = _get(r.data, "one_liner")
    return f"<p>{_e(text)}</p>{_notes(r)}"


def _part_a_item(ctx: _Ctx, r: DerivedResult) -> str:
    is_open = r.status in OPEN_STATUSES
    pairs = [(T.LABEL_CHECKED, f"<p>{_e(r.entry.description)}</p>"), (T.LABEL_OBSERVED, _observed(r)),
             (T.COLUMN_STATUS, ctx.status(r.status))]
    link = ""
    if is_open:
        pairs += [(T.LABEL_LEGAL_BASIS, _norms(r)), (T.LABEL_RISK, _e(_get(r.data, "risk"))),
                  (T.LABEL_REVIEW_QUESTION, _review_question(r)),
                  (T.LABEL_CLIENT_ACTION, _e(_get(r.data, "client_action")))]
        link = (f'<p class="to-part-b"><a href="#{_anchor("b", r.entry.id)}">'
                f"{_e(T.LINK_TO_PART_B.format(id=r.entry.id))}</a></p>")
    cls = "finding is-open" if is_open else "finding"
    return (f'<article class="{cls}" id="{_anchor("a", r.entry.id)}" data-id="{_e(r.entry.id)}">'
            f'<h3><span class="fid">{_e(r.entry.id)}</span>{_e(r.entry.title)}</h3>'
            f"{_fields(pairs)}{link}{_lawyer(r)}</article>")


def _part_a(ctx: _Ctx) -> str:
    out = [f'<h1 id="part-a-title">{_e(T.SECTION_TITLES["part_a"])}</h1>']
    for area, rows in _by_area(ctx.model, ctx.catalog):
        if rows:
            out.append(f'<h2>{_e(area.title)}</h2><p class="area-intro">{_e(area.intro)}</p>')
            out += [_part_a_item(ctx, r) for r in rows]
    return "".join(out)


# ---------------------------------------------------------------- part B

def _evidence_item(ctx: _Ctx, item: Any) -> str:
    if not isinstance(item, Mapping):
        return ""
    caption = item.get("caption")
    if item.get("kind") == "screenshot":
        path = safe_evidence_path(ctx.report_dir, item.get("file"))
        cap = f"<figcaption>{_e(caption)}</figcaption>" if caption else ""
        return f'<figure><img src="{data_uri(path)}" alt="{_e(item.get("alt"))}">{cap}</figure>'
    parts = [f"<p>{_e(caption)}</p>" if caption else ""]
    if isinstance(item.get("excerpt"), str) and item["excerpt"]:
        parts.append(f"<pre><code>{_e(item['excerpt'])}</code></pre>")
    if isinstance(item.get("file"), str):
        parts.append(f'<p class="file">{_e(item["file"])}</p>')
    return "".join(parts)


def _evidence(ctx: _Ctx, r: DerivedResult) -> str:
    items = _get(r.data, "evidence")
    return "".join(_evidence_item(ctx, i) for i in items) if isinstance(items, list) else ""


def _fix(r: DerivedResult) -> str:
    steps = "".join(f"<li>{_e(s)}</li>" for s in _texts(_get(r.data, "fix.steps")))
    out = f'<ol class="steps">{steps}</ol>' if steps else ""
    snippets = _get(r.data, "fix.snippets")
    for s in snippets if isinstance(snippets, list) else ():
        if isinstance(s, Mapping) and isinstance(s.get("code"), str):
            label = " • ".join(_e(s[k]) for k in ("target", "lang") if isinstance(s.get(k), str) and s[k])
            cap = f"<figcaption>{_e(T.LABEL_SNIPPETS)}{': ' + label if label else ''}</figcaption>"
            out += f'<figure class="snippet">{cap}<pre><code>{_e(s["code"])}</code></pre></figure>'
    return out


def _retest(r: DerivedResult) -> str:
    retest = _get(r.data, "retest")
    if not isinstance(retest, Mapping):
        return ""
    out = f"<p>{_e(retest.get('how'))}</p>" if retest.get("how") else ""
    for key, label in (("command", T.LABEL_COMMAND), ("expected", T.LABEL_EXPECTED)):
        if isinstance(retest.get(key), str) and retest[key]:
            out += f'<figure class="snippet"><figcaption>{_e(label)}</figcaption><pre><code>{_e(retest[key])}</code></pre></figure>'
    return out


def _list(items: Iterable[str], cls: str) -> str:
    body = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="{cls}">{body}</ul>' if body else ""


def _part_b_item(ctx: _Ctx, r: DerivedResult) -> str:
    refs = _get(r.data, "references")
    pairs = [
        (T.LABEL_OBSERVED, _observed(r)),
        (T.LABEL_EVIDENCE, _evidence(ctx, r)),
        (T.LABEL_LEGAL_BASIS, _norms(r)),
        (T.LABEL_RISK, _e(_get(r.data, "risk"))),
        (T.LABEL_REVIEW_QUESTION, _review_question(r)),
        (T.LABEL_FIX, _fix(r)),
        (T.LABEL_RETEST, _retest(r)),
        (T.LABEL_REFERENCES, _list((_link_or_text(u) for u in (refs if isinstance(refs, list) else [])), "refs")),
        (T.LABEL_CHECKLIST, _list((_e(c) for c in _texts(_get(r.data, "checklist"))), "checklist")),
        (T.LABEL_EFFORT, _effort(r)),
    ]
    return (f'<article class="finding is-open" id="{_anchor("b", r.entry.id)}" data-id="{_e(r.entry.id)}">'
            f'<h2><span class="fid">{_e(r.entry.id)}</span>{_e(r.entry.title)}</h2>'
            f"<p>{ctx.status(r.status)}</p>{_fields(pairs)}{_lawyer(r)}</article>")


def _part_b(ctx: _Ctx) -> str:
    open_rows = ctx.model.open_results()
    prio = "".join(f'<li><a href="#{_anchor("b", r.entry.id)}">{_e(r.entry.id)}</a><span>{_e(r.entry.title)}</span>'
                   f'<span class="effort">{_effort(r)}</span></li>' for r in open_rows)
    head = f'<h1 id="part-b-title">{_e(T.SECTION_TITLES["part_b"])}</h1>'
    if prio:
        head += f'<h2>{_e(T.LABEL_PRIORITIES)}</h2><ul class="checklist priorities">{prio}</ul>'
    return head + "".join(_part_b_item(ctx, r) for r in open_rows)


# ---------------------------------------------------------------- appendices

def _protocol_value(key: str, value: Any) -> str:
    if key in ("started_utc", "finished_utc"):
        return _e(_utc_display(value))
    if key == "tools" and isinstance(value, Mapping):
        return _list((f"{_e(k)}: {_e(v)}" for k, v in value.items()), "plain")
    if isinstance(value, list):
        return _list((_e(v) for v in value), "plain")
    return _e(value)


def _appendix_a(ctx: _Ctx) -> str:
    run = ctx.findings.get("run") or {}
    source = {**run, "catalog_version": ctx.findings.get("catalog_version"),
              "plugin_version": ctx.findings.get("plugin_version")}
    rows = "".join(f'<tr><th scope="row">{_e(label)}</th><td>{_protocol_value(key, source[key])}</td></tr>'
                   for key, label in T.PROTOCOL_LABELS.items() if source.get(key) not in (None, "", [], {}))
    return (f'<h1 id="appendix-a-title">{_e(T.SECTION_TITLES["appendix_a"])}</h1>'
            f'<table class="protocol"><tbody>{rows}</tbody></table>')


def _appendix_b() -> str:
    return f'<h1 id="appendix-b-title">{_e(T.SECTION_TITLES["appendix_b"])}</h1><p>{_e(T.METHOD_TEXT)}</p>'


def _appendix_c(catalog: Catalog) -> str:
    items = "".join(f"<dt>{_e(term)}</dt><dd>{_e(text)}</dd>" for term, text in catalog.glossary)
    return f'<h1 id="appendix-c-title">{_e(T.SECTION_TITLES["appendix_c"])}</h1><dl class="glossary">{items}</dl>'


def _appendix_d() -> str:
    return (f'<h1 id="appendix-d-title">{_e(T.SECTION_TITLES["appendix_d"])}</h1>'
            f'<div class="disclaimer"><p>{_e(T.DISCLAIMER_FULL)}</p></div>')


# ---------------------------------------------------------------- css, template checks, entry point

def _fonts_css() -> str:
    return "\n".join(
        f'@font-face {{ font-family: "{family}"; src: url({data_uri(FONTS_DIR / name)}) format("woff2"); '
        f"font-weight: {weight}; font-style: {style}; font-display: block; }}"
        for family, name, weight, style in FONT_FACES)


def _css(model: ReportModel, base_css: str) -> str:
    accent = _get(model.findings, "issuer.accent_color")
    accent = ensure_contrast(accent if isinstance(accent, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", accent)
                             else DEFAULT_ACCENT)
    page = (f"@page {{ @top-center {{ content: {_css_string(T.CONFIDENTIAL)}; }} "
            f"@bottom-left {{ content: {_css_string(T.FOOTER)}; }} }}")
    return f":root {{ --accent: {accent}; }}\n{base_css}\n{page}"


class _TemplateText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[tuple[str, str]] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._skip += tag in ("style", "script")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        text = PLACEHOLDER_RE.sub(" ", data).strip()
        if text and not self._skip:
            self.items.append((f"{TEMPLATE_PATH.name}:{self.getpos()[0]}", text))


def template_text_items(path: Path = TEMPLATE_PATH) -> list[tuple[str, str]]:
    """(location, text) of the template's own text nodes, placeholders removed (spec 6.8)."""
    parser = _TemplateText()
    parser.feed(Path(path).read_text(encoding="utf-8"))
    parser.close()
    return parser.items


def _post_checks(document: str, model: ReportModel) -> None:
    refs = find_external_refs(document)
    if refs:
        raise RuntimeError(f"report.html enthält externe Referenzen: {', '.join(refs[:5])}")
    expected = 2 * model.counts.get("defect", 0)
    found = document.count(T.LAWYER_SENTENCE)
    if found != expected:
        raise RuntimeError(f"Anwaltsempfehlung {found}-mal statt {expected}-mal (zweimal je Auffällig)")
    issues = check_texts(template_text_items(), load_forbidden_phrases())
    if issues:
        raise RuntimeError("Vorlage verletzt Textregeln: " + "; ".join(str(i) for i in issues))


def render_html(model: ReportModel, catalog: Catalog, report_dir: Path) -> str:
    """Full report.html as text; raises RuntimeError when a post-render check fails."""
    base_css = CSS_PATH.read_text(encoding="utf-8")
    ctx = _Ctx(model, catalog, Path(report_dir), _status_icons(_status_colors(base_css)))
    domain = _get(model.findings, "run.domain") or ""
    values = {
        "title": _e(f"{T.TITLE} • {domain}" if domain else T.TITLE),
        "subtitle": _e(T.SUBTITLE),
        "fonts_css": _fonts_css(),
        "css": _css(model, base_css),
        "paged_script": "",  # PAGED_JS_ENABLED is False (spike); nothing is bundled
        "cover": _cover(ctx),
        "overview": _overview(ctx),
        "part_a": _part_a(ctx),
        "part_b": _part_b(ctx),
        "appendix_a": _appendix_a(ctx),
        "appendix_b": _appendix_b(),
        "appendix_c": _appendix_c(catalog),
        "appendix_d": _appendix_d(),
        "footer": _e(T.FOOTER),
        "confidential": _e(T.CONFIDENTIAL),
    }
    document = Template(TEMPLATE_PATH.read_text(encoding="utf-8")).substitute(values)
    _post_checks(document, model)
    return document
