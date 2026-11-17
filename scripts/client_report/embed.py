"""Inline assets as data URIs and detect external references in rendered HTML (spec 6.6, anti-goal A7).

report.html must be self-contained: fonts, logo and screenshots are embedded, and the finished
document may not load anything from the network. `find_external_refs` parses tags and CSS, not
text, so a URL quoted in an escaped evidence excerpt is never mistaken for a reference.
"""
from __future__ import annotations

import base64
import re
from html.parser import HTMLParser
from pathlib import Path

SIZE_BUDGET_BYTES = 10 * 1024 * 1024

MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
}

# Attributes that make the browser fetch something on its own.
FETCH_ATTRS = ("src", "srcset", "data", "poster", "background", "action", "formaction", "xlink:href")
SAFE_ANCHOR_PREFIXES = ("https://", "#")
DATA_RE = re.compile(r"^\s*data:", re.IGNORECASE)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?\s*([^'\")\s]*)", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(r"@import\b", re.IGNORECASE)


def data_uri(path: Path) -> str:
    """Base64 data URI of a file; the MIME type follows the suffix, unknown suffixes are refused."""
    path = Path(path)
    mime = MIME_BY_SUFFIX.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"Dateityp nicht einbettbar: {path.suffix or path.name}")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def _is_remote(value: str) -> bool:
    """True for every non-empty fetch target except a data: URI or an in-page fragment.

    Relative paths count too: report.html is passed on alone, so nothing may live next to it.
    """
    value = value.strip()
    return bool(value) and not DATA_RE.match(value) and not value.startswith("#")


def _css_refs(css: str) -> list[str]:
    refs = [m.group(0) for m in CSS_IMPORT_RE.finditer(css)]
    refs += [f"url({m.group(1)})" for m in CSS_URL_RE.finditer(css) if _is_remote(m.group(1))]
    return refs


class _RefFinder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._check(tag, attrs)
        if tag == "style":
            self._in_style = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._check(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.refs += _css_refs(data)

    def _check(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "base":
            self.refs.append("<base>")
        for name, value in attrs:
            value = value or ""
            if name == "style":
                self.refs += _css_refs(value)
            elif name == "href" and tag == "a":
                if value and not value.startswith(SAFE_ANCHOR_PREFIXES):
                    self.refs.append(f"<a href={value}>")
            elif name == "href" or name in FETCH_ATTRS:
                parts = value.split(",") if name == "srcset" else [value]
                self.refs += [f"<{tag} {name}={p.strip()}>" for p in parts if _is_remote(p)]


def find_external_refs(html: str) -> list[str]:
    """References that would load or navigate outside the document; [] means self-contained.

    Flagged: any fetch attribute, `<link href>` or CSS `url()` that is not a data: URI (remote,
    protocol-relative or relative path), `@import`, `<base>`, and anchors other than https/#.
    Allowed: data: URIs, in-page anchors (`#…`) and `<a href="https://…">` text links.
    """
    finder = _RefFinder()
    finder.feed(html)
    finder.close()
    return finder.refs
