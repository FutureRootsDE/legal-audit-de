---
name: legal-update-sources
description: Aktualisiert KB-Artikel gegen Primaerquellen. Nutze diese Skill wenn /legal-update aufgerufen wird ODER wenn ein KB-Artikel aelter als 90 Tage ist und im aktuellen Arbeitskontext verwendet wird.
---

# Knowledge-Base Aktualitaets-Workflow

Haelt die Rechts-KB aktuell gegen Primaerquellen.

## Trigger

- Expliziter Aufruf: `/legal-update <slug>` oder `/legal-update --stale-only`
- Hook-Trigger: wenn UserPromptSubmit-Hook eine KB-Datei laedt, die `aktualisiert:`-Datum > 90 Tage hat, warnt Claude den User: "KB-Datei X ist 120 Tage alt — empfehle `/legal-update X`".

## Delegation

Die Recherche- und Verifikations-Arbeit uebernimmt der `legal-researcher`-Agent (sonnet). Diese Skill ist der Orchestrator:

```
1. Ermittle Zieldatei(en) aus Argument oder --stale-only-Scan
2. Pro Datei: dispatch legal-researcher mit:
   - aktuelle YAML-Frontmatter-Felder
   - Aktueller Datei-Inhalt
   - Auftrag: "Pruefe gegen Primaerquelle, liefere Diff"
3. User-Review bei CRIT-relevanten Diffs
4. Edit anwenden, Frontmatter updaten (aktualisiert:, verifiziert-am:)
5. Log in .claude/logs/kb-updates.log
```

## Stale-Detection

Ein KB-Artikel gilt als "stale", wenn:
- `aktualisiert:` > 90 Tage alt, ODER
- `verifiziert-am:` > 180 Tage alt, ODER
- Ein verlinktes Urteil/Gesetz zwischenzeitlich geaendert wurde (manuell per Trigger)

## Zitat-Preservation

Beim Update:
- **Niemals** Primaer-Paragraphen-Zitate aendern, ohne Primaerquelle zu re-fetchen
- Sekundaer-Einordnungen (Dr. Schwenke etc.) duerfen aktualisiert werden
- Geloeschte Zitate werden ins Log geschrieben mit Grund

## Output

Dem User nach Abschluss:
- Anzahl geprueft / aktualisiert / unveraendert
- Liste CRIT-Aenderungen (z.B. neue Paragraphen, aufgehobene Urteile)
- Verweis auf Log-Datei
