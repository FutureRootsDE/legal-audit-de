"""Classification of EU citations against Cellar hits (VERIFIED, DATE_MISMATCH, PENDING, ...)."""
from __future__ import annotations

from .eu_az import parse_eu_az
from .models import Citation, LookupResult
from .names import name_hint

DECISION_TYPES = ("Urteil", "Gutachten", "Beschluss")
PENDING_NOTE = "Verfahren anhaengig oder nur Schlussantraege/Mitteilung vorhanden, keine Entscheidung im Bestand"
JOINED_NOTE = "verbundene Rechtssache: Entscheidung unter der CELEX-Nummer des Leitverfahrens"
OTHER_DATE_NOTE = "KB-Datum entspricht dem Datum von {kind} (nicht dem massgeblichen Entscheidungsdatum)"


def _suffix(citation: Citation) -> str:
    case = parse_eu_az(citation.az, citation.court)
    return case.suffix if case else ""


def decision_hits(citation: Citation, hits: list[dict]) -> list[dict]:
    """The hits that count for the date comparison: judgment first, order as fallback (interim relief: order)."""
    judgments = [h for h in hits if h.get("type") in ("Urteil", "Gutachten")]
    orders = [h for h in hits if h.get("type") == "Beschluss"]
    ordered = (orders or judgments) if _suffix(citation) == "R" else (judgments or orders)
    return [h for h in ordered if h.get("date")]


def classify_eu(citation: Citation, lookup: LookupResult | None) -> str:
    if lookup is None or lookup.state == "unchecked":
        return "UNCHECKED"
    if lookup.state == "error":
        return "ERROR"
    if not lookup.hits:
        return "NOT_IN_DATASET"
    decisions = decision_hits(citation, lookup.hits)
    if not decisions:
        return "PENDING"
    if citation.date is None or any(h["date"] == citation.date for h in decisions):
        return "VERIFIED"
    return "DATE_MISMATCH"


def eu_notes(citation: Citation, lookup: LookupResult, status: str) -> list[str]:
    """Informative remarks; none of them changes the status."""
    notes: list[str] = []
    if status == "PENDING":
        notes.append(PENDING_NOTE)
    if any(h.get("joined") for h in lookup.hits):
        notes.append(JOINED_NOTE)
    if status == "DATE_MISMATCH":
        notes.extend(_other_date_notes(citation, lookup.hits))
    return notes


def _other_date_notes(citation: Citation, hits: list[dict]) -> list[str]:
    kinds = sorted({h["type"] for h in hits if h.get("date") == citation.date and h.get("type")})
    return [OTHER_DATE_NOTE.format(kind="/".join(kinds))] if kinds else []


def eu_name_hint(citation: Citation, lookup: LookupResult | None) -> str:
    """Informative only: never part of a verdict."""
    if lookup is None or lookup.state != "ok":
        return "none"
    return name_hint(citation.names, lookup.tokens)
