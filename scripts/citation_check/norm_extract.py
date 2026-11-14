"""Extraction of norm citations (§ 356a BGB, Art. 246a § 1 EGBGB, Art. 6 DSGVO) and BGBl. references.

A small token scanner instead of one giant regex: it reads paragraph numbers, the qualifiers
(Abs., Satz, Nr., lit.) and finally the law abbreviation. A group without a law abbreviation
is dropped. EU laws (DSGVO, KI-VO, ...) are only counted, never checked.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .text import short

MAX_FILE_BYTES = 2_000_000
MAX_LINE_CHARS = 5000
TOKEN = re.compile(
    r"(?P<para>§§?)|(?P<art>\bArt\.|\bArtikel\b)"
    r"|(?P<q>\b(?:Abs\.?|Absatz|S\.|Satz|Nrn?\.?|Nummer|lit\.|Buchst\.|Buchstabe|Alt\.|Var\.|UAbs\.|Hs\.|Halbs\.|Halbsatz)(?![A-Za-zÄÖÜäöüß]))"
    r"|(?P<ivm>\bi\.\s?V\.\s?m\.|\biVm\b)"
    r"|(?P<num>\d+[a-z]?(?![A-Za-zÄÖÜäöüß0-9]))"
    r"|(?P<ff>\bff?\.)"
    r"|(?P<conn>\bund\b|\boder\b|\bsowie\b|\bbis\b|[,/+–—-])"
    r"|(?P<word>[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß0-9]*(?:-[A-Za-zÄÖÜäöüß0-9]+)*)"
    r"|(?P<other>\S)")
ABBR = re.compile(r"^[A-ZÄÖÜ][A-Za-zÄÖÜäöüß0-9]*(?:-[A-ZÄÖÜ][A-Za-zÄÖÜäöüß0-9]*)*$")
OLD_VERSION = re.compile(r"\s*(?:a\.\s?F\.|alter\s+Fassung|alte\s+Fassung)")
EU_LAWS = frozenset({"DSGVO", "DS-GVO", "KI-VO", "DSA", "DMA", "GRCh", "AEUV", "EUV", "ePrivacy-RL", "DSM-RL",
                     "NIS2-RL", "Data-Act", "AI-Act", "EMRK", "UGP-RL", "VRRL", "e-Commerce-RL"})
MEMO_FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
FRONT_DATE = re.compile(r"^(verifiziert-am|aktualisiert):[ \t]*[\"']?([0-9]{4}-[0-9]{2}-[0-9]{2})", re.MULTILINE)
BGBL = re.compile(
    r"BGBl\.?\s*(?:(?P<teil1>I{1,2})\s+)?(?P<y1>[0-9]{4})\s+(?P<teil2>I{1,2})\s+Nr\.\s*(?P<n1>[0-9]{1,4})"
    r"|BGBl\.?\s*(?P<teil3>I{1,2})\s+Nr\.\s*(?P<n2>[0-9]{1,4})\s*/\s*(?P<y2>[0-9]{4})"
    r"|BGBl\.?\s*(?P<teil4>I{1,2})\s+(?P<y3>[0-9]{4})\s+Nr\.\s*(?P<n3>[0-9]{1,4})")
MIN_BGBL_YEAR = 2023  # numbered issues (Nr.) exist on recht.bund.de since the electronic Bundesgesetzblatt


@dataclass(frozen=True)
class NormRef:
    file: str
    line: int
    law: str
    kind: str  # "§" or "Art"
    number: str  # paragraph or article number, e.g. "356a"
    art: str | None = None  # article of a paragraph below an article ("Art. 246a § 1 EGBGB")
    absaetze: tuple[int, ...] = ()
    saetze: tuple[int, ...] = ()
    old_version: bool = False
    verified_on: str | None = None


@dataclass(frozen=True)
class BgblRef:
    file: str
    line: int
    year: int
    number: int
    part: str
    verified_on: str | None = None


@dataclass
class _Item:
    kind: str
    number: str
    art: str | None = None
    absaetze: list[int] = field(default_factory=list)
    saetze: list[int] = field(default_factory=list)


@dataclass
class Extraction:
    norms: list[NormRef] = field(default_factory=list)
    eu_counts: dict[str, int] = field(default_factory=dict)
    bgbl: list[BgblRef] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def _is_law(word: str) -> bool:
    return word in EU_LAWS or (bool(ABBR.match(word)) and sum(c.isupper() for c in word) >= 2)


class _Scanner:
    """Collects items until a law abbreviation closes the group (feed returns it), else drops the group."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.items: list[_Item] = []
        self.mode = "none"  # none | para | art | sub | qual
        self.qual = ""
        self.conn = False  # the previous token was a connector (, / + und ...)
        self.num = False  # the previous token was a number

    def feed(self, kind: str, text: str) -> str | None:
        """Process one token; returns a law abbreviation when it closes the group."""
        law = getattr(self, f"_on_{kind}")(text)
        if kind not in ("conn", "ff"):
            self.conn = False
        if kind != "num":
            self.num = False
        return law

    def _on_para(self, text: str) -> None:
        under_article = bool(self.items) and self.items[-1].kind == "Art" and self.num and not self.conn
        if under_article:
            self.mode = "sub"
            return
        if not (self.items and self.conn):
            self.reset()
        self.mode = "para"

    def _on_art(self, text: str) -> None:
        if not (self.items and self.conn):
            self.reset()
        self.mode = "art"

    def _on_q(self, text: str) -> None:
        if not self.items:
            return
        label = text.lower().rstrip(".")
        self.mode = "qual"
        self.qual = "abs" if label.startswith(("abs", "uabs")) else "satz" if label in ("s", "satz") else "other"

    def _on_ivm(self, text: str) -> None:
        self.reset()

    def _on_ff(self, text: str) -> None:
        return None

    def _on_conn(self, text: str) -> None:
        self.conn = bool(self.items)

    def _on_num(self, text: str) -> None:
        if self.mode == "qual":
            self._qualifier(text)
        elif self.mode == "sub":
            last = self.items[-1]
            self.items[-1] = _Item("§", text, last.number)
            self.mode = "para"
        elif self.mode in ("para", "art") and not (self.num and not self.conn):
            self.items.append(_Item("Art" if self.mode == "art" else "§", text))
        self.num = True

    def _qualifier(self, text: str) -> None:
        value = int(re.match(r"\d+", text).group(0))
        target = self.items[-1]
        if self.qual == "abs":
            target.absaetze.append(value)
        elif self.qual == "satz":
            target.saetze.append(value)

    def _on_word(self, text: str) -> str | None:
        if self.items and self.mode == "qual" and len(text) == 1 and text.islower():
            return None  # "lit. a", "Buchstabe b"
        if self.items and _is_law(text):
            return text
        self.reset()
        return None

    def _on_other(self, text: str) -> None:
        self.reset()


def scan_line(line: str, rel: str, lineno: int, verified_on: str | None, out: Extraction) -> None:
    scanner = _Scanner()
    for match in TOKEN.finditer(line):
        kind = match.lastgroup or "other"
        law = scanner.feed(kind, match.group(0))
        if law is None:
            continue
        old = bool(OLD_VERSION.match(line, match.end()))
        _emit(scanner.items, law, old, rel, lineno, verified_on, out)
        scanner.reset()


def _emit(items: list[_Item], law: str, old: bool, rel: str, lineno: int, verified_on: str | None,
          out: Extraction) -> None:
    for item in items:
        if law in EU_LAWS:
            out.eu_counts[law] = out.eu_counts.get(law, 0) + 1
            continue
        out.norms.append(NormRef(rel, lineno, law, item.kind, item.number, item.art, tuple(item.absaetze),
                                 tuple(item.saetze), old, verified_on))


def frontmatter_verified_on(text: str) -> str | None:
    """verifiziert-am of the frontmatter, else aktualisiert; quotes tolerated; None if neither is a date."""
    block = MEMO_FRONT.match(text)
    if not block:
        return None
    found = {key: value for key, value in FRONT_DATE.findall(block.group(1))}
    return found.get("verifiziert-am") or found.get("aktualisiert")


def scan_bgbl(line: str, rel: str, lineno: int, verified_on: str | None, out: Extraction) -> None:
    for match in BGBL.finditer(line):
        groups = match.groupdict()
        part = groups["teil2"] or groups["teil3"] or groups["teil4"]
        year = groups["y1"] or groups["y2"] or groups["y3"]
        number = groups["n1"] or groups["n2"] or groups["n3"]
        out.bgbl.append(BgblRef(rel, lineno, int(year), int(number), part, verified_on))


def extract_text(text: str, rel: str, out: Extraction | None = None) -> Extraction:
    """Norm citations and BGBl. references of one file."""
    out = out if out is not None else Extraction()
    verified_on = frontmatter_verified_on(text)
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.rstrip("\r")
        if len(line) > MAX_LINE_CHARS:
            out.skipped.append(short(f"{rel}:{lineno}: Zeile zu lang uebersprungen", 300))
            continue
        scan_line(line, rel, lineno, verified_on, out)
        scan_bgbl(line, rel, lineno, verified_on, out)
    return out


def scan_kb_norms(kb_path: Path) -> Extraction:
    """All *.md files below the knowledge directory (symlinks and oversized files are skipped, noted)."""
    out = Extraction()
    for md in sorted(kb_path.rglob("*.md")):
        rel = md.relative_to(kb_path.parent).as_posix()
        if md.is_symlink():
            out.skipped.append(short(f"{rel}: Symlink uebersprungen", 300))
            continue
        try:
            data = md.read_bytes()
        except OSError as exc:
            out.skipped.append(short(f"{rel}: nicht lesbar ({exc})", 300))
            continue
        if len(data) > MAX_FILE_BYTES:
            out.skipped.append(short(f"{rel}: Datei zu gross uebersprungen", 300))
            continue
        extract_text(data.decode("utf-8", errors="replace"), rel, out)
    return out
