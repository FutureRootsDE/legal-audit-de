---
name: legal-update-sources
description: Aktualisiert KB-Artikel gegen Primaerquellen. Nutze diese Skill wenn /legal-update aufgerufen wird ODER wenn die Verifikation eines KB-Artikels 90 Tage oder aelter ist und im aktuellen Arbeitskontext verwendet wird.
---

# Knowledge-Base Aktualitaets-Workflow

Haelt die Rechts-KB aktuell gegen Primaerquellen.

## Trigger

- Expliziter Aufruf: `/legal-update <slug>` oder `/legal-update --stale-only`
- Hook-Trigger: wenn UserPromptSubmit-Hook eine KB-Datei laedt, deren `verifiziert-am:` (ersatzweise `aktualisiert:`) 90 Tage oder aelter ist, warnt Claude den User: "KB-Datei X ist 120 Tage alt — empfehle `/legal-update X`".

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

## Optionaler Vorab-Schritt: API-Sammelpruefung

`python scripts/verify-citations.py [--only-pending]` fragt Bundesgerichts-Aktenzeichen der KB gegen die Rechtsinformations-API des Bundes ab (optional, Testphase, nur sieben Bundesgerichte, gecacht und gedrosselt). Treffer mit ECLI und Datum gelten als Primaerbeleg; NOT_IN_DATASET und NOT_COVERED sind kein Gegenbeweis und fuehren zurueck auf die Tier-1-Kaskade. Das Skript schreibt nie in die KB (ausser explizit mit `--write-ecli`) und entfernt keine Marker.

## Stale-Detection

Ein KB-Artikel gilt als "stale", wenn `verifiziert-am:` 90 Tage oder aelter ist (massgeblich ist die Verifikation, nicht die letzte Bearbeitung). Fehlt `verifiziert-am:`, zaehlt `aktualisiert:`. `scripts/legal-status.py` weist 90 bis 180 Tage als "stale" und ab 180 Tagen als "sehr stale" aus.

Dateien mit `teilverifiziert-am:` sind ein eigener Zustand ("teilverifiziert"): sie gelten nie als frisch und werden einzeln per `/legal-update <slug>` vollstaendig verifiziert.

Unabhaengig davon kann ein manueller Trigger (ein verlinktes Urteil oder Gesetz hat sich zwischenzeitlich geaendert) eine Pruefung anstossen; das aendert nicht die Stale-Definition.

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
