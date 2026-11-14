"""Mapping of law abbreviations to their path on gesetze-im-internet.de.

gii-toc.xml lists title and link of every law but no abbreviation, and many slugs are
historical (UWG = uwg_2004, TDDDG = ttdsg, EGBGB = bgbeg). The mapping below is maintained by
hand and checked against the live table of contents on every run: a slug that is missing there
marks the law as unknown instead of guessing.
"""
from __future__ import annotations

import re

GII_BASE = "https://www.gesetze-im-internet.de"
TOC_URL = f"{GII_BASE}/gii-toc.xml"
SLUG_RE = re.compile(r"^[a-z0-9_.\-]{1,60}$")
TOC_LINK = re.compile(r"<link>https?://www\.gesetze-im-internet\.de/([a-z0-9_.\-]{1,60})/xml\.zip</link>")

LAW_SLUGS: dict[str, str] = {
    "BGB": "bgb", "EGBGB": "bgbeg", "UWG": "uwg_2004", "UrhG": "urhg", "RDG": "rdg", "DDG": "ddg",
    "TDDDG": "ttdsg", "TTDSG": "ttdsg", "PAngV": "pangv_2022", "BFSG": "bfsg", "BDSG": "bdsg_2018",
    "KUG": "kunsturhg", "KunstUrhG": "kunsturhg", "AO": "ao_1977", "HGB": "hgb", "VSBG": "vsbg",
    "UStG": "ustg_1980", "MarkenG": "markeng", "ZPO": "zpo", "TKG": "tkg_2021", "BetrVG": "betrvg",
    "BSIG": "bsig_2025", "UKlaG": "uklag", "MessEinhG": "me_einhg", "BRAO": "brao", "GG": "gg",
    "StGB": "stgb", "StPO": "stpo",
}
# Abbreviations that are the old name of a law under the same slug (reported as a note).
RENAMED = {"TTDSG": "TDDDG"}


def parse_toc(body: bytes) -> set[str]:
    """All law slugs of gii-toc.xml; raises ValueError if the document is not a table of contents."""
    text = body.decode("utf-8", errors="replace")
    if "<items>" not in text:
        raise ValueError("kein Inhaltsverzeichnis")
    slugs = set(TOC_LINK.findall(text))
    if len(slugs) < 100:
        raise ValueError("Inhaltsverzeichnis unvollstaendig")
    return slugs


def resolve(abbreviation: str, toc: set[str]) -> tuple[str | None, str]:
    """(slug, note) of a law abbreviation; slug None if the abbreviation is unmapped or gone from the toc."""
    slug = LAW_SLUGS.get(abbreviation)
    if slug is None:
        return None, "Kuerzel nicht zugeordnet"
    if slug not in toc:
        return None, "Gesetz nicht im Inhaltsverzeichnis (aufgehoben oder umbenannt)"
    return slug, (f"Altname von {RENAMED[abbreviation]}" if abbreviation in RENAMED else "")
