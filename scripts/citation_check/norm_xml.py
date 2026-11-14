"""Reduction of a gesetze-im-internet.de XML (xml.zip) to a small, validated index.

The XML is third-party input: size limits for the archive and the unpacked document, no entity
declarations, only the known DOCTYPE, and every value that reaches the index (or the cache) is
validated against a strict pattern. Free text never leaves this module except the short official
heading of a paragraph (pattern-checked, 160 characters at most).
"""
from __future__ import annotations

import io
import re
import xml.etree.ElementTree as ET  # input is size-limited, entity-free and has a fixed DOCTYPE (checked below)
import zipfile
from datetime import date

MAX_ZIP_BYTES = 12_000_000
MAX_XML_BYTES = 40_000_000
MAX_NORMS = 20_000
MAX_JURABK = 6
HEADING_RE = re.compile(r"^[A-Za-zÄÖÜäöüß0-9 .,;:()\-/„“\"'&+–§*]{1,160}$")
JURABK_RE = re.compile(r"^[A-Za-zÄÖÜäöüß0-9 \-]{1,30}$")
KEY_RE = re.compile(r"^(?:Art [0-9]{1,4}[a-z]{0,2}\|)?(?:§|Art) [0-9]{1,4}[a-z]{0,2}$")
BGBL_FUND_RE = re.compile(r"^BGBl\. [0-9]{4} I Nr\. [0-9]{1,4}$")
DOCTYPE_OK = re.compile(rb'<!DOCTYPE dokumente SYSTEM "https?://www\.gesetze-im-internet\.de/dtd/[0-9.]+/gii-norm\.dtd">')
ENBEZ_SINGLE = re.compile(r"^(?:\(XXXX\)\s*)?(§|Art)\s+([0-9]{1,4})([a-z]{0,2})$")
ENBEZ_RANGE = re.compile(r"^(?:\(XXXX\)\s*)?(?:§§|Art)\s+([0-9]{1,4})([a-z]{0,2})\s+bis\s+([0-9]{1,4})([a-z]{0,2})$")
ABSATZ_MARK = re.compile(r"^\(([0-9]{1,3})([a-z]?)\)\s")
STAND_RE = re.compile(r"\b[A-Za-zÄÖÜäöü]{1,4} v\. ([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})(?: I Nr\. ([0-9]{1,4}))?")
RISKY_ABBREV = re.compile(
    r"\b(?:Nr|Nrn|Abs|Art|S|bzw|vgl|ggf|etc|v|lit|Buchst|Alt|Var|Hs|ff?|Rn|Anh|u|z|d|i|B|h|a|m)\.|[0-9]\.")
SENTENCE_END = re.compile(r"[.!?][\"“”)]?(?=\s+[A-ZÄÖÜ„\"(]|\s*$)")
GONE = "(weggefallen)"


class XmlRejected(ValueError):
    """The archive or document does not meet the safety or shape requirements."""


def _unzip(data: bytes) -> bytes:
    if len(data) > MAX_ZIP_BYTES:
        raise XmlRejected("Archiv zu gross")
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise XmlRejected("kein gueltiges Archiv") from None
    members = [i for i in archive.infolist() if i.filename.lower().endswith(".xml")]
    if len(members) != 1 or members[0].file_size > MAX_XML_BYTES:
        raise XmlRejected("unerwartete Archivstruktur")
    with archive.open(members[0]) as handle:
        raw = handle.read(MAX_XML_BYTES + 1)
    if len(raw) > MAX_XML_BYTES:
        raise XmlRejected("XML zu gross")
    return raw


def _checked_root(raw: bytes) -> ET.Element:
    head = raw[:2000]
    if b"<!ENTITY" in raw or b"<!ELEMENT" in raw or b"<!ATTLIST" in raw:
        raise XmlRejected("Entity- oder DTD-Deklaration nicht erlaubt")
    if b"<!DOCTYPE" in head and not DOCTYPE_OK.search(head):
        raise XmlRejected("unbekannter DOCTYPE")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        raise XmlRejected("XML nicht lesbar") from None
    if root.tag != "dokumente":
        raise XmlRejected("Wurzelelement unerwartet")
    return root


def count_sentences(text: str) -> int | None:
    """Number of sentences, or None if the text contains abbreviations or numbering that make it unreliable."""
    body = ABSATZ_MARK.sub("", text.strip() + " ", count=1).strip()
    if not body or RISKY_ABBREV.search(body) or not re.search(r"[.!?][\"“”)]?$", body):
        return None
    return len(SENTENCE_END.findall(body))


def _heading(norm: ET.Element) -> str | None:
    title = re.sub(r"\s+", " ", (norm.findtext("metadaten/titel") or "")).strip()
    return title[:160] if HEADING_RE.match(title[:160]) else None


def _absatz_info(norm: ET.Element) -> tuple[int, list[int | None]]:
    """Number of Absaetze and the (reliable or None) sentence count per Absatz."""
    paragraphs = [p for p in norm.findall("textdaten/text/Content/P") if "".join(p.itertext()).strip()]
    marks = [m for m in (ABSATZ_MARK.match("".join(p.itertext()).strip() + " ") for p in paragraphs) if m]
    count = max((int(m.group(1)) for m in marks), default=1 if paragraphs else 0)
    sentences: list[int | None] = []
    for p in paragraphs:
        plain = not list(p)
        sentences.append(count_sentences("".join(p.itertext())) if plain else None)
    return count, sentences[:count]


def _norm_key(norm: ET.Element) -> tuple[str, str] | None:
    enbez = re.sub(r"\s+", " ", (norm.findtext("metadaten/enbez") or "").replace("\xa0", " ")).strip()
    single = ENBEZ_SINGLE.match(enbez)
    if not single:
        return None
    glied = (norm.findtext("metadaten/gliederungseinheit/gliederungsbez") or "").replace("\xa0", " ").strip()
    article = glied if re.fullmatch(r"Art [0-9]{1,4}[a-z]{0,2}", glied) and single.group(1) == "§" else None
    key = f"{article}|" if article else ""
    return key + f"{single.group(1)} {single.group(2)}{single.group(3)}", enbez


def _range_of(norm: ET.Element) -> list | None:
    enbez = re.sub(r"\s+", " ", (norm.findtext("metadaten/enbez") or "").replace("\xa0", " ")).strip()
    match = ENBEZ_RANGE.match(enbez)
    if not match or (norm.findtext("metadaten/titel") or "").strip() != GONE:
        return None
    kind = "Art" if "Art" in enbez else "§"
    return [kind, int(match.group(1)), match.group(2), int(match.group(3)), match.group(4)]


def _stand(root: ET.Element) -> tuple[str | None, str | None]:
    for angabe in root.iter("standangabe"):
        if (angabe.findtext("standtyp") or "").strip() != "Stand":
            continue
        match = STAND_RE.search(angabe.findtext("standkommentar") or "")
        if match:
            return _stand_fields(match)
    return None, None


def _stand_fields(match: re.Match[str]) -> tuple[str | None, str | None]:
    day, month, year, number = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)
    try:
        iso = date(year, month, day).isoformat()
    except ValueError:
        return None, None
    return iso, (f"BGBl. {year} I Nr. {int(number)}" if number else None)


def _jurabk(root: ET.Element) -> list[str]:
    first = root.find("norm")
    values = [(e.text or "").strip() for e in (first.iter("jurabk") if first is not None else [])]
    return [v for v in values if JURABK_RE.match(v)][:MAX_JURABK]


def parse_law_xml(raw: bytes) -> dict:
    """Index of one law: norms (heading, number of Absaetze, sentence counts, 'weggefallen'), ranges, Stand."""
    root = _checked_root(raw)
    norms: dict[str, dict] = {}
    ranges: list[list] = []
    arts: set[str] = set()
    for norm in root.findall("norm"):
        glied = (norm.findtext("metadaten/gliederungseinheit/gliederungsbez") or "").replace("\xa0", " ").strip()
        if re.fullmatch(r"Art [0-9]{1,4}[a-z]{0,2}", glied):
            arts.add(glied)
        span = _range_of(norm)
        if span:
            ranges.append(span)
        keyed = _norm_key(norm)
        if keyed is None or len(norms) >= MAX_NORMS:
            continue
        count, sentences = _absatz_info(norm)
        gone = (norm.findtext("metadaten/titel") or "").strip() == GONE
        norms[keyed[0]] = {"t": _heading(norm), "a": count, "g": gone, "s": sentences}
    stand_date, stand_bgbl = _stand(root)
    return {"jurabk": _jurabk(root), "builddate": (root.get("builddate") or "")[:8], "stand_date": stand_date,
            "stand_bgbl": stand_bgbl, "norms": norms, "ranges": ranges, "arts": sorted(arts)}


def parse_law_zip(data: bytes) -> dict:
    return parse_law_xml(_unzip(data))


def validate_index(obj: object) -> dict | None:
    """Canonical index of an untrusted (cached) object, or None if anything is off."""
    if not isinstance(obj, dict) or set(obj) != {"jurabk", "builddate", "stand_date", "stand_bgbl", "norms",
                                                  "ranges", "arts"}:
        return None
    try:
        return _validated(obj)
    except (TypeError, ValueError, KeyError):
        return None


def _valid_norm(key: object, value: object) -> bool:
    if not isinstance(key, str) or not KEY_RE.match(key) or not isinstance(value, dict):
        return False
    heading, count, gone, sat = value.get("t"), value.get("a"), value.get("g"), value.get("s")
    if set(value) != {"t", "a", "g", "s"} or not isinstance(gone, bool):
        return False
    if not (heading is None or (isinstance(heading, str) and HEADING_RE.match(heading))):
        return False
    if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= 200:
        return False
    return isinstance(sat, list) and len(sat) <= 200 and all(
        s is None or (isinstance(s, int) and not isinstance(s, bool) and 0 <= s <= 200) for s in sat)


def _validated(obj: dict) -> dict | None:
    if len(obj["norms"]) > MAX_NORMS or not all(_valid_norm(k, v) for k, v in obj["norms"].items()):
        return None
    if not all(isinstance(v, str) and JURABK_RE.match(v) for v in obj["jurabk"]) or len(obj["jurabk"]) > MAX_JURABK:
        return None
    stand_date, stand_bgbl = obj["stand_date"], obj["stand_bgbl"]
    if stand_date is not None:
        date.fromisoformat(stand_date)
    if stand_bgbl is not None and not BGBL_FUND_RE.match(stand_bgbl):
        return None
    if not re.fullmatch(r"[0-9]{0,8}", obj["builddate"]):
        return None
    ranges = [r for r in obj["ranges"] if _valid_range(r)]
    arts = [a for a in obj["arts"] if isinstance(a, str) and re.fullmatch(r"Art [0-9]{1,4}[a-z]{0,2}", a)]
    if len(ranges) != len(obj["ranges"]) or len(arts) != len(obj["arts"]):
        return None
    return dict(obj)


def _valid_range(span: object) -> bool:
    return (isinstance(span, list) and len(span) == 5 and span[0] in ("§", "Art")
            and isinstance(span[1], int) and isinstance(span[3], int)
            and isinstance(span[2], str) and isinstance(span[4], str)
            and re.fullmatch(r"[a-z]{0,2}", span[2]) is not None and re.fullmatch(r"[a-z]{0,2}", span[4]) is not None)
