"""Classification of citations against API lookups and result aggregation."""
from __future__ import annotations

import re
from dataclasses import asdict

from .api import ApiClient
from .models import API_BASE, STATUSES, Citation, LookupResult


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


def build_results(citations: list[Citation], client: ApiClient) -> list[dict]:
    lookups: dict[tuple[str, str], LookupResult] = {}
    results: list[dict] = []
    for citation in citations:
        lookup = None
        if citation.covered:
            key = (citation.court, citation.az)
            if key not in lookups:
                lookups[key] = client.lookup(*key)
            lookup = lookups[key]
        status = classify(citation, lookup)
        entry = asdict(citation)
        entry.update(status=status, hits=lookup.hits if lookup else [],
                     detail=lookup.detail if lookup and lookup.state != "ok" else "")
        note = _bgh_note(citation) if status == "NOT_IN_DATASET" else None
        if note:
            entry["note"] = note
        results.append(entry)
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
        "api_requests": client.requests_made,
        "offline": offline,
        "api_base": API_BASE,
    }
