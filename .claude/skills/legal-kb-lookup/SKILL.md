---
name: legal-kb-lookup
description: Laedt gezielt Knowledge-Base-Chunks zu einem rechtlichen Thema. Nutze diese Skill wenn /legal-kb aufgerufen wird ODER wenn der User eine spezifische Rechtsinformation braucht (z.B. "Erklaer mir Cookie-Consent", "Was sagt Art. 30 DSGVO?", "Welche Urteile gibt es zu Google Fonts?").
---

# Knowledge-Base Lookup

On-Demand-Zugriff auf die Rechts-Knowledge-Base.

## Wann nutzen

- Expliziter Aufruf: `/legal-kb <slug>`
- User fragt nach spezifischem Rechtsgebiet, Urteil, Behoerden-Leitlinie
- Wenn UserPromptSubmit-Hook zwar Schlagwort erkannt hat, aber der User explizit "mehr Details" oder "die ganze Datei" moechte

## Funktion

Die KB ist unter `knowledge/` organisiert:

```
knowledge/
├── INDEX.md                    # Inhaltsverzeichnis (alle Slugs)
├── gesetze/<slug>.md           # Gesetzestexte + Kommentierung
├── themen/<slug>.md            # Themen-Dossiers (Cookie, AGB, etc.)
├── urteile/<slug>.md           # Urteile mit Leitsaetzen
├── behoerden/<slug>.md         # DSK, EDSA, BfDI etc.
├── checklisten/<slug>.md       # Audit-Checklisten
└── anwaelte-tools/<slug>.md    # Verifizierungs-Empfehlungen
```

## Suchlogik

1. **Exakter Slug-Match** (Prio-Reihenfolge: themen → gesetze → urteile → checklisten → behoerden → anwaelte-tools)
2. **Fuzzy-Match** via `Glob("knowledge/**/*<slug>*.md")` wenn kein exakter Treffer
3. **Fallback:** Liste aus `INDEX.md` zeigen + User nach exakter Auswahl fragen

## Kontext-Budget

- Max **3 KB-Dateien** pro Lookup in den Kontext laden
- Bei mehr Treffern: Liste anzeigen, User-Interaktion fuer Feinselection
- Grund: Kontextfenster schonen, damit andere Work-Items Platz haben

## Cross-Refs

Jede KB-Datei hat am Ende einen `## Siehe auch`-Block mit Obsidian-Links `[[cross-ref]]`. Wenn der User sichtbar an einem Thema weiterarbeitet, proaktiv Cross-Refs anbieten (aber nicht automatisch laden).

## Missing-Datei-Handling

Wenn die angefragte Datei noch nicht existiert:
1. Zeige aehnliche Slugs aus INDEX.md
2. Frage: "Soll ich `/legal-update <slug>` ausfuehren, um diesen Artikel zu erstellen?"
3. Log in `.claude/logs/missing-kb-requests.log`
