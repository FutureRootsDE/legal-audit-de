---
description: Aktualisiert einen KB-Artikel oder die gesamte Knowledge Base (Primaerquellen-Recherche, YAML-Frontmatter-Update).
argument-hint: [thema-slug | --all | --stale-only | --fix-pending]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task
---

# /legal-update

Aktualisiere Rechts-KB-Inhalte gegen Primaerquellen.

## Modi

### `/legal-update <slug>`
Aktualisiere genau eine KB-Datei (z.B. `/legal-update tdddg`).

### `/legal-update --stale-only`
Finde alle Dateien mit `aktualisiert:`-Datum aelter als 90 Tage, aktualisiere alle.

### `/legal-update --all`
Aktualisiere alle KB-Dateien (nur bewusst nutzen — toolintensiv).

### `/legal-update --fix-pending` (empfohlen fuer Routine-Wartung)
Scant die KB nach `<<VERIFIKATION AUSSTEHEND>>`- und `<<UNVERIFIZIERT>>`-Platzhaltern und dispatcht den `legal-researcher`-Agent gezielt auf jeden Fund. Loest damit die beim initialen KB-Befuellen markierten Recherche-Luecken auf.

**Ablauf:**
1. Liste aller Platzhalter ermitteln:
   ```bash
   python "${CLAUDE_PROJECT_DIR}/scripts/find-placeholders.py" --json
   ```
2. Dispatch `legal-researcher`-Agent (Opus 4.7 [1M]) mit der Platzhalter-Liste als Input.
3. Agent recherchiert jeden Platzhalter gegen Tier-1-Primaerquelle und ersetzt ihn durch das verifizierte Zitat (oder bestaetigt Ausstehend-Status mit Begruendung).
4. Frontmatter-Updates pro Datei, Log-Eintrag in `.claude/logs/kb-updates.log`.

**User-Bestaetigung:** Vor jedem Edit zeigt der Agent den konkreten Diff und bittet um OK. Das schuetzt vor versehentlichen Massenaenderungen.

## Ablauf pro Datei

1. **Dispatch `legal-researcher`-Agent** (Opus 4.7 [1M]) mit:
   - Zielthema / Gesetzestext / Urteil
   - Aktuelle YAML-Frontmatter-Felder (quelle-primaer, verifiziert-am)
   - Auftrag: "Pruefe die unten stehende Datei gegen die Primaerquelle. Liste alle Abweichungen (Paragraphen-Aenderungen, neue Urteile, Aufhebungen, Behoerden-Beschluesse)."

2. **Quellen-Kaskade** (immer in dieser Reihenfolge):
   1. `eur-lex.europa.eu` fuer EU-Recht (konsolidierte Fassung)
   2. `gesetze-im-internet.de` fuer DE-Recht
   3. `datenschutzkonferenz-online.de` + `edpb.europa.eu` fuer Behoerden-Leitlinien
   4. `curia.europa.eu` + `rechtsprechung-im-internet.de` fuer Rechtsprechung
   5. Sekundaere (Schwenke, Haerting, e-recht24) nur zur Einordnung, nicht als Primaerquelle

3. **Diff-Report erstellen:**
   ```
   AENDERUNGEN <slug>.md (Stand: <alt> → <neu>):
   - § 7 UWG Absatz 3 Nr. 2 neu (Opt-In-Verschaerfung)
   - Neues Urteil: BGH VI ZR 225/24 vom 12.03.2026
   - ...
   ```

4. **Edit-Anwendung** mit expliziter User-Bestaetigung (wenn CRIT-relevante Aenderung). Bei rein additiven Aenderungen (neue Urteile, neue Leitlinien) ohne Rueckfrage anwenden.

5. **YAML-Frontmatter aktualisieren:**
   ```yaml
   aktualisiert: <heute>
   verifiziert-am: <heute>
   quelle-primaer: <URL falls veraendert>
   ```

6. **Log-Eintrag** in `.claude/logs/kb-updates.log`:
   ```
   2026-04-19T10:30:00Z update tdddg: § 24 Abs. 2 neu, 2 Urteile ergaenzt
   ```

## Zitat-Verifikation

Alle in der geupdateten Datei zitierten Paragraphen / Aktenzeichen muessen vom `legal-researcher` gegen eine Primaerquelle aufloesbar sein (HTTP 200 + Text-Match). Halluzinierte Zitate werden geloescht.
