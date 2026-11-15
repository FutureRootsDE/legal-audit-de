"""Fixed SPARQL template for the Cellar endpoint and strict validation of its answer.

The query text is assembled from constants and CELEX numbers that are built from integers
and checked against CELEX_RE: raw text of a citation never reaches the query (no injection).
Titles of the answer are reduced to lowercase word tokens for the informative name hint and
are never passed on as free text.
"""
from __future__ import annotations

import json
import re
from urllib.parse import urlencode

from .eu_az import CELEX_RE, ECLI_EU_RE, DOC_TYPES, EuCase, celex_candidates, doc_type_of

SPARQL_BASE = "https://publications.europa.eu/webapi/rdf/sparql"
JOIN_URI = "http://publications.europa.eu/resource/case/celex%3A"
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
TOKEN_RE = re.compile(r"[a-z0-9äöüß]+")
TOKEN_OK = re.compile(r"^[a-z0-9äöüß]{3,40}$")
MAX_TOKENS = 200
MAX_ROWS = 60
MAX_BINDINGS = 500
COURTS = ("EuGH", "EuG")
DOC_LABELS = frozenset(DOC_TYPES.values())

QUERY_TEMPLATE = (
    "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>\n"
    "SELECT DISTINCT ?celex ?ecli ?date ?title ?joins WHERE {{\n"
    "  {{ ?w cdm:resource_legal_id_celex ?celex . FILTER(STR(?celex) IN ({celexes})) }}\n"
    "  UNION\n"
    "  {{ ?w cdm:case-law_joins_case_court ?joins . VALUES ?joins {{ {joined} }}\n"
    "     ?w cdm:resource_legal_id_celex ?celex . }}\n"
    "  OPTIONAL {{ ?w cdm:case-law_ecli ?ecli }}\n"
    "  OPTIONAL {{ ?w cdm:work_date_document ?date }}\n"
    "  OPTIONAL {{ ?e cdm:expression_belongs_to_work ?w ; cdm:expression_title ?title ;\n"
    "     cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/DEU> }}\n"
    "}} LIMIT {limit}\n")


class EuShapeError(ValueError):
    """The endpoint answered with JSON of an unexpected structure."""


# Interim relief: German title wording, or a file number with suffix R ("C-204/21 R", "T-1/20 P R");
# the trailing word boundary keeps RENV, REC and rev out.
INTERIM_TITLE = re.compile(r"vorl(?:ä|ae)ufige[rn]? rechtsschutz|einstweilige[rn]? anordnung"
                           r"|(?:\brechtssache\s+)?\b[ct]-[0-9]+/[0-9]+(?:\s?p)?\s?r\b")


def build_query(case: EuCase) -> str:
    celexes = celex_candidates(case)
    if not all(CELEX_RE.match(c) for c in celexes):
        raise ValueError("ungueltige CELEX-Nummer")
    literal = ", ".join(f'"{c}"' for c in celexes)
    joined = " ".join(f"<{JOIN_URI}{c}>" for c in celexes)
    return QUERY_TEMPLATE.format(celexes=literal, joined=joined, limit=MAX_ROWS)


def build_url(case: EuCase) -> str:
    params = {"query": build_query(case), "format": "application/sparql-results+json"}
    return f"{SPARQL_BASE}?{urlencode(params)}"


def sanitize_eu_hit(raw: dict) -> dict:
    """Canonical EU hit; invalid fields become None (so cache validation compares equal only for clean hits)."""
    celex, ecli, date = raw.get("celex"), raw.get("ecli"), raw.get("date")
    kind, court, joined = raw.get("type"), raw.get("court"), raw.get("joined")
    interim = raw.get("interim")
    return {
        "celex": celex if isinstance(celex, str) and CELEX_RE.match(celex) else None,
        "ecli": ecli if isinstance(ecli, str) and ECLI_EU_RE.match(ecli) else None,
        "date": date if isinstance(date, str) and DATE_RE.match(date) else None,
        "type": kind if kind in DOC_LABELS else None,
        "court": court if court in COURTS else None,
        "joined": joined if isinstance(joined, bool) else None,
        "interim": interim if isinstance(interim, bool) else None,
    }


def sanitize_tokens(raw: object) -> list[str] | None:
    """Validated token list for the cache, or None if it is malformed."""
    if not isinstance(raw, list) or len(raw) > MAX_TOKENS:
        return None
    if not all(isinstance(t, str) and TOKEN_OK.match(t) for t in raw):
        return None
    return list(raw)


def _bindings(body: bytes) -> list[dict]:
    try:
        data = json.loads(body.decode("utf-8"))
    except ValueError:
        raise EuShapeError("Antwort ist kein gueltiges JSON") from None
    results = data.get("results") if isinstance(data, dict) else None
    rows = results.get("bindings") if isinstance(results, dict) else None
    if not isinstance(rows, list) or len(rows) > MAX_BINDINGS:
        raise EuShapeError("Antwortstruktur unerwartet")
    if not all(isinstance(r, dict) for r in rows):
        raise EuShapeError("Zeile ist kein Objekt")
    return rows


def _value(row: dict, key: str) -> str | None:
    cell = row.get(key)
    value = cell.get("value") if isinstance(cell, dict) else None
    return value if isinstance(value, str) else None


def _row_hit(row: dict) -> dict | None:
    celex = _value(row, "celex")
    kind = doc_type_of(celex) if celex else None
    if kind is None:
        return None
    return sanitize_eu_hit({"celex": celex, "ecli": _value(row, "ecli"), "date": _value(row, "date"),
                            "type": kind, "court": "EuGH" if celex[5] == "C" else "EuG",
                            "joined": _value(row, "joins") is not None,
                            "interim": is_interim_title(_value(row, "title"))})


def is_interim_title(title: str | None) -> bool:
    """True for titles of interim relief orders (vorlaeufiger Rechtsschutz, file number with suffix R)."""
    text = (title or "").lower()
    return bool(INTERIM_TITLE.search(text))


def _title_tokens(title: str | None) -> set[str]:
    return {t for t in TOKEN_RE.findall((title or "").lower()) if TOKEN_OK.match(t)}


def parse_response(body: bytes) -> tuple[list[dict], list[str]]:
    """Hits (deduplicated per CELEX, a direct hit wins over a joined one) and title tokens."""
    hits: dict[str, dict] = {}
    tokens: set[str] = set()
    for row in _bindings(body):
        hit = _row_hit(row)
        if hit is None or hit["celex"] is None:
            continue
        tokens |= _title_tokens(_value(row, "title"))
        known = hits.get(hit["celex"])
        winner = hit if known is None or (known["joined"] and not hit["joined"]) else known
        # duplicate rows often lack the title: any interim row marks the whole CELEX
        interim = bool(hit["interim"] or (known and known["interim"]))
        hits[hit["celex"]] = {**winner, "interim": True} if interim else winner
    ordered = sorted(hits.values(), key=lambda h: (h["date"] or "", h["celex"]))
    return ordered, sorted(tokens)[:MAX_TOKENS]
