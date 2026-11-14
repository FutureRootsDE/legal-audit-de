"""Shared test helpers (HTTP fake, fixtures). Importing it puts scripts/ on sys.path."""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
FIXTURES = HERE / "fixtures"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def fixture_bytes(name: str) -> bytes:
    return (FIXTURES / f"{name}.json").read_bytes()



class FakeFetch:
    """Scripted HTTP layer. `responses` maps file number -> (status, body) or a
    list of such tuples (consumed in order, the last one repeats)."""

    def __init__(self, responses=None, default=None):
        self.responses = responses or {}
        self.default = default
        self.calls: list[str] = []

    def __call__(self, url: str, timeout: float):
        self.calls.append(url)
        query = parse_qs(urlparse(url).query)
        key = query.get("fileNumber", [""])[0]
        entry = self.responses.get(key, self.default)
        if entry is None:
            return 200, fixture_bytes("ris_rechtsprechung_kein_treffer")
        if isinstance(entry, list):
            idx = min(len(self.calls_for(key)) - 1, len(entry) - 1)
            entry = entry[idx]
        if isinstance(entry, Exception):
            raise entry
        return entry

    def calls_for(self, key: str) -> list[str]:
        return [u for u in self.calls if parse_qs(urlparse(u).query).get("fileNumber", [""])[0] == key]


OK_I_ZR_159 = (200, fixture_bytes("ris_rechtsprechung_i_zr_159_24"))
OK_VI_ZR_10 = (200, fixture_bytes("ris_rechtsprechung_vi_zr_10_24"))
OK_EMPTY = (200, fixture_bytes("ris_rechtsprechung_kein_treffer"))
ERR_422 = (422, fixture_bytes("ris_fehler_422"))

GOOD_ECLI = "ECLI:DE:BGH:2025:091025UIZR159.24.0"
GOOD_HIT = {"ecli": GOOD_ECLI, "date": "2025-10-09", "type": "Urteil",
            "document_number": "KORE726702025", "court": "BGH",
            "file_numbers": ["I ZR 159/24"], "headline": "BGH, Urteil"}
