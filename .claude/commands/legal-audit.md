---
description: Startet einen vollstaendigen Rechts-Audit auf einer Codebase (DE/EU-Scope). Erzeugt LegalAudit.md + clean/*.md im Zielprojekt.
argument-hint: <pfad> [--compare] [--pdf]
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, WebFetch, Task
---

# /legal-audit

Fuehre einen strukturierten Rechts-Audit auf der unter `$ARGUMENTS` uebergebenen Codebase durch.

## Flags

### `/legal-audit <pfad>` (Standard)
Vollstaendiger Audit wie unten beschrieben.

### `/legal-audit <pfad> --compare`
Nach dem Audit: vergleicht mit letztem Audit desselben Projekts aus `legal-audit-de/audits/`. Liefert Diff-Report (neue/behobene/geaenderte Findings).
Implementierung:
```bash
python "${CLAUDE_PROJECT_DIR}/scripts/audit-compare.py" --auto <pfad>
```

### `/legal-audit <pfad> --pdf`
Nach dem Audit: generiert `anwalts-briefing.html` (+ PDF falls pandoc installiert) aus allen Output-Dateien fuer Anwalts-Uebergabe.
Implementierung:
```bash
python "${CLAUDE_PROJECT_DIR}/scripts/legal-audit-pdf.py" <pfad>/docs/legal-audit
```

Beide Flags kombinierbar.

## Pflichtablauf

1. **Validiere den Pfad.** Pruefe, dass `$ARGUMENTS` ein existierendes Verzeichnis ist. Wenn nicht, frage nach.

2. **Erstelle Output-Struktur** im Zielprojekt:
   ```
   <zielprojekt>/docs/legal-audit/
   ├── LegalAudit.md
   ├── SUMMARY.md
   ├── clean/
   └── evidence/
   ```

3. **Dispatch `legal-auditor`-Agent** (Opus 4.7 [1M]) mit der Codebase:
   - Der Agent scannt systematisch nach rechtlich relevanten Artefakten
   - Klassifiziert Findings nach Severity-Matrix (CRIT/HIGH/MED/LOW)
   - Nutzt Checklisten aus `knowledge/checklisten/audit-<codebase-typ>.md`

4. **Pro Finding dispatch `legal-text-writer`-Agent** (Opus 4.7 [1M]) zur Erstellung der Clean-Version unter `docs/legal-audit/clean/F-NNN-<slug>.md`.

5. **Zitat-Verifikation:** Jeder im Audit zitierte Paragraph / jedes Aktenzeichen muss der `legal-researcher`-Agent gegen die Primaerquelle verifizieren (eur-lex / gesetze-im-internet / rechtsprechung-im-internet). Das Log landet in `.claude/logs/zitate-verifikation-<timestamp>.log`.

6. **SUMMARY.md erzeugen:** Management-Zusammenfassung mit Top-5-CRIT/HIGH, Gesamt-Severity-Count und empfohlenen Sofortmassnahmen.

7. **Disclaimer-Injection:** Jede Output-Datei wird vom `legal-text-writer` mit dem Disclaimer-Block aus `templates/disclaimer-block.md` eingeleitet. Der `PostToolUse`-Hook validiert das.

## Codebase-Typ-Erkennung

Klassifiziere die Codebase anhand von Markern:
- `package.json` mit `next` → Next.js SaaS → `checklisten/audit-saas.md`
- `package.json` mit `astro` / `wordpress`-Marker / nur HTML → Landingpage → `checklisten/audit-landingpage.md`
- `*.workflow.json` / n8n-Export → `checklisten/audit-n8n.md`
- `package.json` mit `woocommerce` / `shopify` / Stripe + Checkout → E-Commerce → `checklisten/audit-ecommerce.md`
- vorwiegend `.md` + `content/` + Blog-Frontmatter → Content → `checklisten/audit-content-blog.md`

Wenn unklar: frage den User.

## Rechtsgebiete-Scope

DSGVO · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · MarkenG · NIS2-BSIG.

**Nicht im Scope:** Strafrecht, Arbeitsrecht, Steuerrecht (ausser HGB §§ 257 Retention), Gesellschaftsrecht, Rechtsordnungen ausserhalb DE/EU. Das Audit deklariert diese Bereiche explizit als **nicht geprueft**.

## Output-Verifikation

Am Ende muss jede Anforderung erfuellt sein:
- [ ] `docs/legal-audit/LegalAudit.md` mit Disclaimer + Finding-Tabelle existiert
- [ ] Pro Finding eine `clean/F-NNN-*.md`-Datei
- [ ] `SUMMARY.md` existiert
- [ ] Zitat-Verifikations-Log unter `.claude/logs/`
- [ ] Parallel-Kopie nach `${CLAUDE_PROJECT_DIR}/audits/<projektname>-<timestamp>/` (Schatten-Archiv)

## Nach Abschluss

Gib dem User eine Zusammenfassung:
- Anzahl Findings pro Severity
- Top-3 CRIT/HIGH mit 1-Zeilen-Beschreibung
- Geschaetzter Korrekturaufwand
- Empfohlene naechste Schritte (insb. Anwalts-Pruefung fuer CRIT-Findings)
