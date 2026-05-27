---
description: Startet einen vollstaendigen Rechts-Audit auf einer Codebase (DE/EU-Scope). Erzeugt LegalAudit.md + clean/*.md im Zielprojekt.
argument-hint: <pfad> [--compare] [--pdf]
allowed-tools: bash, view, grep, glob, create, edit, web_fetch, task
---
<!--
  AUTO-GENERATED — DO NOT EDIT DIRECTLY.
  Source: .claude/commands/legal-audit.md
  Regenerate via: python3 scripts/sync-platforms.py --apply
-->
# /legal-audit

Fuehre einen strukturierten Rechts-Audit auf der unter `$ARGUMENTS` uebergebenen Codebase durch.

## Flags

### `/legal-audit <pfad>` (Standard)
Vollstaendiger Audit wie unten beschrieben.

### `/legal-audit <pfad> --compare`
Nach dem Audit: vergleicht mit letztem Audit desselben Projekts aus `legal-audit-de/audits/`. Liefert Diff-Report (neue/behobene/geaenderte Findings).
Implementierung:
```bash
python "${GITHUB_WORKSPACE}/scripts/audit-compare.py" --auto <pfad>
```

### `/legal-audit <pfad> --pdf`
Nach dem Audit: generiert `anwalts-briefing.html` (+ PDF falls pandoc installiert) aus allen Output-Dateien fuer Anwalts-Uebergabe.
Implementierung:
```bash
python "${GITHUB_WORKSPACE}/scripts/legal-audit-pdf.py" <pfad>/docs/legal-audit
```

Beide Flags kombinierbar.

## Pro-Mode-Awareness (vor jedem Subagent-Dispatch beachten)

Wenn der SessionStart-Hook einen "PRO-MODE AKTIV"-Block eingespielt hat oder
`scripts/legal-audit-pro-mode.py status --json` `any_enabled: true` zeigt, dann
**ersetze beim Dispatch jeden Agent-Namen durch die `-pro`-Variante** (siehe
Marker-Liste am Ende dieser Datei). Der Default bleibt die 1M-Variante.

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

3. **Dispatch `legal-auditor`-Agent** (Opus 4.7 [1M] — bei Pro-Mode siehe SessionStart-Reminder: `legal-auditor-pro`) mit der Codebase:
   - Der Agent scannt systematisch nach rechtlich relevanten Artefakten
   - Klassifiziert Findings nach Severity-Matrix (CRIT/HIGH/MED/LOW)
   - Nutzt Checklisten aus `knowledge/checklisten/audit-<codebase-typ>.md`

4. **Pro Finding dispatch `legal-text-writer`-Agent** (Opus 4.7 [1M] — bei Pro-Mode: `legal-text-writer-pro`) zur Erstellung der Clean-Version unter `docs/legal-audit/clean/F-NNN-<slug>.md`.

5. **Zitat-Verifikation:** Jeder im Audit zitierte Paragraph / jedes Aktenzeichen muss der `legal-researcher`-Agent (Pro-Mode: `legal-researcher-pro`) gegen die Primaerquelle verifizieren (eur-lex / gesetze-im-internet / rechtsprechung-im-internet). Das Log landet in `.claude/logs/zitate-verifikation-<timestamp>.log`.

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
- [ ] Parallel-Kopie nach `${GITHUB_WORKSPACE}/audits/<projektname>-<timestamp>/` (Schatten-Archiv)

## Nach Abschluss

Gib dem User eine Zusammenfassung:
- Anzahl Findings pro Severity
- Top-3 CRIT/HIGH mit 1-Zeilen-Beschreibung
- Geschaetzter Korrekturaufwand
- Empfohlene naechste Schritte (insb. Anwalts-Pruefung fuer CRIT-Findings)

## Agent-Marker (Default-Modus vs. Pro-Mode)

| Default (1M-Kontext, Max/Team/Enterprise) | Pro-Mode (Standard-Kontext, Claude-Pro-Abo) |
|---|---|
| `legal-auditor`     | `legal-auditor-pro`     |
| `legal-text-writer` | `legal-text-writer-pro` |
| `legal-researcher`  | `legal-researcher-pro`  |

Pro-Mode wird via `python3 scripts/legal-audit-pro-mode.py enable` aktiviert und
ueberlebt Plugin-Updates (Marker liegt in `${CLAUDE_PLUGIN_DATA}`).
