"""Classification of citations against API lookups and result aggregation."""
from __future__ import annotations

import re

from .api import ApiClient
from .models import API_BASE, STATUSES, Citation, LookupResult
from .text import short

CORRECTION_NOTE = "Korrektur- oder Aenderungsvermerk in der Zeile, Datum nicht verglichen"
LookupMap = dict[tuple[str, str], LookupResult]


def classify(citation: Citation, lookup: LookupResult | None) -> str:
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


def _notes(citation: Citation, status: str) -> str:
    notes = [CORRECTION_NOTE] if citation.correction else []
    bgh = _bgh_note(citation) if status == "NOT_IN_DATASET" else None
    return "; ".join(notes + ([bgh] if bgh else []))


def _entry(citation: Citation, lookup: LookupResult | None) -> dict:
    status = classify(citation, lookup)
    entry = {
        "file": short(citation.file), "line": citation.line, "az": short(citation.az),
        "court": short(citation.court), "covered": citation.covered, "date": citation.date,
        "pending": citation.pending, "status": status, "source": _source(lookup),
        "hits": lookup.hits if lookup else [],
        "detail": short(lookup.detail) if lookup and lookup.state != "ok" else "",
    }
    note = _notes(citation, status)
    if note:
        entry["note"] = note
    return entry


def build_results(citations: list[Citation], client: ApiClient, fresh: bool = False,
                  lookups: LookupMap | None = None) -> list[dict]:
    """Classify all citations; each (court, az) is looked up once. `lookups` is shared with later steps."""
    lookups = lookups if lookups is not None else {}
    results: list[dict] = []
    for citation in citations:
        lookup = None
        if citation.covered:
            key = (citation.court, citation.az)
            if key not in lookups:
                lookups[key] = client.lookup(*key, fresh=fresh)
            lookup = lookups[key]
        results.append(_entry(citation, lookup))
    return results


def summarize(results: list[dict], client: ApiClient, offline: bool) -> dict:
    counts = {s: 0 for s in STATUSES}
    for r in results:
        counts[r["status"]] += 1
    return {
        "counts": counts,
        "citations": len(results),
        "unique_az": len({(r["court"], r["az"]) for r in results}),
        "pending_markers": sum(1 for r in results if r["pending"]),
        "cache_hits": sum(1 for r in results if r["source"] == "cache"),
        "api_requests": client.requests_made,
        "offline": offline,
        "api_base": API_BASE,
    }
