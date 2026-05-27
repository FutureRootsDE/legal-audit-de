---
name: legal-update-sources
description: Aktualisiert KB-Artikel gegen Primaerquellen. Nutze diese Skill wenn /legal-update aufgerufen wird ODER wenn ein KB-Artikel aelter als 90 Tage ist und im aktuellen Arbeitskontext verwendet wird.
---
<!--
  AUTO-GENERATED — DO NOT EDIT DIRECTLY.
  Source: .claude/skills/legal-update-sources/SKILL.md
  Regenerate via: python3 scripts/sync-platforms.py --apply
-->
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

## Auto-Routing (Plattform-Fallback fuer Hookless-CLIs)

Diese Plattform (Codex/Copilot) hat keine SessionStart-/UserPromptSubmit-Hooks. Das Skill uebernimmt das KB-Routing daher selbst:

1. **Lies `knowledge/INDEX.md`** zu Beginn jeder Session, falls noch nicht geladen.
2. **Matche Task-Schlagwoerter** (cookie, drittland, ai-act, newsletter, barrierefreiheit, ...) gegen die KB-Kategorien aus dem INDEX.
3. **Lies bis zu 3 passende Chunks** via Read/view aus `knowledge/themen/`, `knowledge/urteile/`, `knowledge/gesetze/`, `knowledge/checklisten/`.
4. **Merke geladene Slugs**, um Doppel-Reads zu vermeiden.

Triggers: siehe `.claude/hooks/triggers.json` (gleiche Schlagwort-Map gilt fuer Codex/Copilot).

## Pro-Mode-Erkennung (Hookless-CLI-Fallback)

Da Codex und Copilot keinen SessionStart-Hook haben, der den Pro-Mode-Marker liest,
muss das Skill den Marker vor dem Dispatch eines `legal-*`-Subagents selbst pruefen:

1. **Pruefe** in dieser Reihenfolge auf `enabled: true`:
   - `~/.codex/legal-audit-de-pro-mode.json` (auf Codex)
   - `~/.copilot/legal-audit-de-pro-mode.json` (auf Copilot)
   - Fallback `~/.claude/legal-audit-de-pro-mode.json`
2. **Wenn aktiv,** dispatche die `-pro`-Variante:
   - `legal-auditor-pro`     statt `legal-auditor`
   - `legal-researcher-pro`  statt `legal-researcher`
   - `legal-text-writer-pro` statt `legal-text-writer`
3. **Sonst** dispatche die Default-1M-Variante.

Aktivieren via: `python3 scripts/legal-audit-pro-mode.py enable`.
