"""Classification of citations against API lookups and result aggregation."""
from __future__ import annotations

import re

import dataclasses

from .api import ApiClient
from .eu_az import parse_eu_az
from .eu_classify import classify_eu, eu_name_hint, eu_notes
from .eu_client import EuClient
from .models import API_BASE, EU_BASE, STATUSES, Citation, LookupResult
from .text import short

CORRECTION_NOTE = "Korrektur- oder Aenderungsvermerk in der Zeile, Datum nicht verglichen"
LookupMap = dict[tuple[str, str], LookupResult]


def is_eu_citation(citation: Citation) -> bool:
    """An EU file number of EuGH or EuG that the Cellar backend can look up."""
    return (not citation.covered and citation.court in ("EuGH", "EuG")
            and parse_eu_az(citation.az, citation.court) is not None)


def classify(citation: Citation, lookup: LookupResult | None) -> str:
    if lookup is not None and lookup.backend == "cellar":
        return classify_eu(citation, lookup)
    if not citation.covered:
        return "NOT_COVERED"
    if lookup is None or lookup.state == "unchecked":
        return "UNCHECKED"
    if lookup.state == "error":
        return "ERROR"
    if not lookup.hits:
        return "NOT_IN_DATASET"
    if citation.date is None or any(h.get("date") == citation.date for h in lookup.hits):
        return "VERIFIED"
    return "DATE_MISMATCH"


def _bgh_note(citation: Citation) -> str | None:
    match = re.search(r"/(\d{2})$", citation.az)
    if citation.court != "BGH" or not match:
        return None
    year = int(match.group(1))
    if year < 10 or year >= 30:  # two-digit year before 2010 (00-09) or 19xx (30-99)
        return "BGH-Bestand der API beginnt etwa 2010"
    return None


def _source(lookup: LookupResult | None) -> str:
    """Provenance of a result: api (fresh query), cache (local file, not authenticated) or none."""
    if lookup is None or lookup.state == "unchecked":
        return "none"
    return "cache" if lookup.from_cache else "api"


def _notes(citation: Citation, status: str, lookup: LookupResult | None = None) -> str:
    notes = [CORRECTION_NOTE] if citation.correction else []
    bgh = _bgh_note(citation) if status == "NOT_IN_DATASET" else None
    eu = eu_notes(citation, lookup, status) if lookup is not None and lookup.backend == "cellar" else []
    return "; ".join(notes + ([bgh] if bgh else []) + eu)


def _backend_of(citation: Citation, lookup: LookupResult | None) -> str:
    if lookup is not None and lookup.backend == "cellar":
        return "cellar"
    return "ris" if citation.covered else "none"


def _entry(citation: Citation, lookup: LookupResult | None) -> dict:
    status = classify(citation, lookup)
    entry = {
        "file": short(citation.file), "line": citation.line, "az": short(citation.az),
        "court": short(citation.court), "covered": citation.covered, "date": citation.date,
        "pending": citation.pending, "status": status, "source": _source(lookup),
        "hits": lookup.hits if lookup else [],
        "detail": short(lookup.detail) if lookup and lookup.state != "ok" else "",
        "backend": _backend_of(citation, lookup),
    }
    if entry["backend"] == "cellar":
        entry["name_hint"] = eu_name_hint(citation, lookup)
    note = _notes(citation, status, lookup)
    if note:
        entry["note"] = note
    return entry


def lookup_citation(citation: Citation, client: ApiClient, eu: EuClient | None, fresh: bool,
                    lookups: LookupMap) -> tuple[Citation, LookupResult | None]:
    """Route a citation to its backend (once per (court, az)); returns the citation as covered or as is."""
    if citation.covered:
        backend = client
    elif eu is not None and is_eu_citation(citation):
        backend, citation = eu, dataclasses.replace(citation, covered=True)
    else:
        return citation, None
    key = (citation.court, citation.az)
    if key not in lookups:
        lookups[key] = backend.lookup(*key, fresh=fresh)
    return citation, lookups[key]


def build_results(citations: list[Citation], client: ApiClient, fresh: bool = False,
                  lookups: LookupMap | None = None, eu: EuClient | None = None) -> list[dict]:
    """Classify all citations; each (court, az) is looked up once. `lookups` is shared with later steps."""
    lookups = lookups if lookups is not None else {}
    return [_entry(*lookup_citation(c, client, eu, fresh, lookups)) for c in citations]


def _name_hint_counts(results: list[dict]) -> dict:
    counts = {"match": 0, "no_match": 0, "none": 0}
    for r in results:
        if "name_hint" in r:
            counts[r["name_hint"]] += 1
    return counts


def summarize(results: list[dict], client: ApiClient, offline: bool, eu: EuClient | None = None) -> dict:
    counts = {s: 0 for s in STATUSES}
    for r in results:
        counts[r["status"]] += 1
    return {
        "eu_enabled": eu is not None,
        "eu_requests": eu.requests_made if eu is not None else 0,
        "eu_base": EU_BASE,
        "eu_name_hints": _name_hint_counts(results),
        "counts": counts,
        "citations": len(results),
        "unique_az": len({(r["court"], r["az"]) for r in results}),
        "pending_markers": sum(1 for r in results if r["pending"]),
        "cache_hits": sum(1 for r in results if r["source"] == "cache"),
        "api_requests": client.requests_made,
        "offline": offline,
        "api_base": API_BASE,
    }
