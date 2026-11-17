"""Fixed report strings (spec 6.3, 6.5, 6.8). The model never writes these; templates use them verbatim.

All strings are dash-free (no em dash, en dash or spaced hyphen); the only exception is the
status symbol for `none`, which is a fixed template element and not text.
"""
from __future__ import annotations

TITLE = "Website-CheckUp • Technik, Datenschutz & Sicherheit"
SUBTITLE = "KI-gestützte technische Ersteinschätzung"

PASS_ON_SENTENCE = "Technische Ersteinschätzung, keine Rechtsberatung. Dieser Bericht ersetzt keine anwaltliche Prüfung."
LAWYER_SENTENCE = (
    "Wir empfehlen, die rechtliche Bewertung dieses Punktes durch eine Rechtsanwältin "
    "oder einen Rechtsanwalt vornehmen zu lassen."
)
DISCLAIMER_SHORT = (
    "Keine Rechtsberatung im Sinne des § 2 RDG. Momentaufnahme der öffentlich erreichbaren "
    "Website zum Prüfdatum, passiv geprüft."
)
FOOTER = "KI-gestützte technische Ersteinschätzung. Kann Fehler enthalten. Keine Rechtsberatung, keine Garantie."
DISCLAIMER_FULL = (
    "Dieser Bericht ist eine KI-gestützte technische Ersteinschätzung der öffentlich erreichbaren "
    "Website zum Prüfdatum. Er ist keine Rechtsberatung im Sinne des § 2 RDG und keine rechtliche "
    "Bewertung des Einzelfalls. Er benennt beobachtete Tatsachen und Vorschriften, deren Prüfung wir "
    "empfehlen. Die Prüfung war passiv: Es wurden keine Formulare abgesendet, keine Konten angelegt "
    "und keine Bestellungen ausgelöst. Automatische Tests erfassen nur einen Teil der Anforderungen, "
    "insbesondere bei der Barrierefreiheit. Der Status „Kein Befund im geprüften Umfang“ bedeutet "
    "nicht, dass eine Anforderung erfüllt ist. Inhalte und Rechtslage können sich nach dem Prüfdatum "
    "ändern. Für eine rechtliche Bewertung wenden Sie sich an eine Rechtsanwältin oder einen "
    "Rechtsanwalt."
)
# Terminal hint of the command before phase 0 (spec 6.1); never part of the report.
START_HINT = (
    "Hinweis: Nutzen Sie den Website-CheckUp für eigene Kunden im Rahmen Ihrer Webleistung. "
    "Bieten oder bewerben Sie ihn nicht als eigenständigen Rechtscheck (§ 5 RDG)."
)
CONFIDENTIAL = "Vertraulich"

STATUS_SYMBOL = {"pass": "✓", "notice": "▲", "defect": "✕", "none": "–"}
STATUS_LABEL = {
    "pass": "Kein Befund im geprüften Umfang",
    "notice": "Hinweis",
    "defect": "Auffällig",
    "none": "Nicht prüfbar / nicht anwendbar",
}
STATUS_SHORT = {
    "pass": "Kein Befund",
    "notice": "Hinweis",
    "defect": "Auffällig",
    "none": "Nicht prüfbar / nicht anwendbar",
}

LABEL_LEGAL_BASIS = "Betroffene Vorschrift (zur Prüfung)"
LABEL_RISK = "Warum das wichtig sein kann"
LABEL_REVIEW_QUESTION = "Prüffrage für Ihre Rechtsberatung"
LABEL_CHECKED = "Was wir geprüft haben"
LABEL_OBSERVED = "Was wir beobachtet haben"
LABEL_CLIENT_ACTION = "Was Sie tun können"
LABEL_FIX = "So beheben Sie es"
LABEL_RETEST = "So prüfen Sie es nach"
LABEL_REFERENCES = "Referenzen"
LABEL_EFFORT = "Aufwand"
LABEL_EVIDENCE = "Beleg"
LINK_TO_PART_B = "Details für Ihre Technik: Teil B, {id}"

NOTE_VALID_FROM = "Pflicht gilt ab {date}."  # date as TT.MM.JJJJ
NOTE_APPLICABILITY_UNCLEAR = "Anwendbarkeit ungeklärt."
NOTE_A11Y_VOLUNTARY = "Keine gesetzliche Pflicht, empfohlen."

SECTION_TITLES = {
    "overview": "Überblick",
    "part_a": "Teil A • Für Sie als Inhaberin oder Inhaber",
    "part_b": "Teil B • Für Ihre Webbetreuung",
    "appendix_a": "Anhang A • Prüfprotokoll",
    "appendix_b": "Anhang B • Methodik und Grenzen",
    "appendix_c": "Anhang C • Glossar",
    "appendix_d": "Anhang D • Haftungsausschluss",
    "top_actions": "Die 3 wichtigsten Maßnahmen",
    "summary": "Zusammenfassung",
}

# Appendix B (spec 6.5): passive, sample, partial WCAG coverage, snapshot, no logins or forms,
# no legal assessment.
METHOD_TEXT = (
    "Die Prüfung war passiv: Wir haben die öffentlich erreichbare Website wie ein normaler Besucher "
    "aufgerufen und keine Formulare abgesendet, keine Konten angelegt und keine Bestellungen ausgelöst. "
    "Geprüft wurde eine Stichprobe von Seiten, nicht jede einzelne Unterseite. "
    "Bereiche hinter Logins oder Formularen haben wir nicht geprüft. "
    "Automatische Tests zur Barrierefreiheit nach WCAG decken nur einen Teil der Anforderungen ab. "
    "Der Bericht ist eine Momentaufnahme zum Prüfdatum und enthält keine rechtliche Bewertung des Einzelfalls."
)

# Further fixed labels of the rendered report (Task 8): cover, overview table, part B, appendix A.
LABEL_SITE = "Geprüfte Website"
LABEL_CLIENT = "Erstellt für"
LABEL_CHECK_DATE = "Prüfdatum"
LABEL_REPORT_ID = "Report-Kennung"
LABEL_ISSUER = "Erstellt von"
LABEL_COUNTS = "Ergebnisse nach Status"
LOGO_ALT = "Logo {company}"
COLUMN_ID = "ID"
COLUMN_TEST = "Test"
COLUMN_STATUS = "Status"
COLUMN_RESULT = "Ergebnis"
LABEL_PRIORITIES = "Prioritätenliste"
LABEL_CHECKLIST = "Checkliste"
LABEL_SNIPPETS = "Beispielcode"
LABEL_COMMAND = "Befehl"
LABEL_EXPECTED = "Erwartete Ausgabe"
EFFORT_FORMAT = "{level}, etwa {minutes} Minuten"
PROTOCOL_LABELS = {
    "target_url": "Aufgerufene Adresse",
    "final_url": "Adresse nach Weiterleitung",
    "started_utc": "Beginn",
    "finished_utc": "Ende",
    "user_agent": "User-Agent",
    "viewports": "Ansichten",
    "tools": "Werkzeuge und Versionen",
    "pages_visited": "Besuchte Seiten",
    "catalog_version": "Version des Prüfkatalogs",
    "plugin_version": "Version des Plugins",
}
UTC_DISPLAY_FORMAT = "%d.%m.%Y, %H:%M:%S UTC"

ALL_FIXED_STRINGS: tuple[str, ...] = (
    TITLE,
    SUBTITLE,
    PASS_ON_SENTENCE,
    LAWYER_SENTENCE,
    DISCLAIMER_SHORT,
    FOOTER,
    DISCLAIMER_FULL,
    START_HINT,
    CONFIDENTIAL,
    *STATUS_SYMBOL.values(),
    *STATUS_LABEL.values(),
    *STATUS_SHORT.values(),
    LABEL_LEGAL_BASIS,
    LABEL_RISK,
    LABEL_REVIEW_QUESTION,
    LABEL_CHECKED,
    LABEL_OBSERVED,
    LABEL_CLIENT_ACTION,
    LABEL_FIX,
    LABEL_RETEST,
    LABEL_REFERENCES,
    LABEL_EFFORT,
    LABEL_EVIDENCE,
    LINK_TO_PART_B,
    NOTE_VALID_FROM,
    NOTE_APPLICABILITY_UNCLEAR,
    NOTE_A11Y_VOLUNTARY,
    *SECTION_TITLES.values(),
    METHOD_TEXT,
    LABEL_SITE,
    LABEL_CLIENT,
    LABEL_CHECK_DATE,
    LABEL_REPORT_ID,
    LABEL_ISSUER,
    LABEL_COUNTS,
    LOGO_ALT,
    COLUMN_ID,
    COLUMN_TEST,
    COLUMN_STATUS,
    COLUMN_RESULT,
    LABEL_PRIORITIES,
    LABEL_CHECKLIST,
    LABEL_SNIPPETS,
    LABEL_COMMAND,
    LABEL_EXPECTED,
    EFFORT_FORMAT,
    *PROTOCOL_LABELS.values(),
)
