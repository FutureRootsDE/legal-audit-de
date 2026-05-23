---
description: Startet einen vollstaendigen Rechts-Audit auf einer Codebase (DE/EU-Scope). Erzeugt LegalAudit.md + clean/*.md im Zielprojekt.
argument-hint: <pfad> [--compare] [--pdf] [--pro-mode]
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

### `/legal-audit <pfad> --pro-mode`
Pro-Mode-Audit fuer Claude-Pro-Abonnenten ohne aktivierte 1M-Usage-Credits. Alle
Subagent-Sessions laufen auf `claude-opus-4-7` (Standard-Kontext, ca. 200K Tokens
statt 1M). Damit der Audit trotzdem vollstaendig durchlaufen kann, wird er in
**acht sequentielle Sub-Sessions** aufgeteilt (eine pro Audit-Pass). Jeder Pass
laeuft in einem frischen 200K-Kontext, persistiert seine Findings auf Disk und
gibt nur eine kurze Zusammenfassung an den Orchestrator zurueck — so passt selbst
ein grosser Codebase-Audit in Standard-Kontext.

Auto-Aktivierung: das Flag ist implizit gesetzt, wenn die Datei
`.claude/.pro-mode` existiert (anlegen via `python3 scripts/legal-audit-pro-mode.py enable`).

**Execution-Logfile:** `<zielprojekt>/docs/legal-audit/audit-execution-<ISO-timestamp>.log`
mit einer Zeile pro Pass:
```
[2026-05-23T14:00:00Z] mode=pro pass=1/8 (PII-Identifikation) target=<pfad> agent=legal-auditor model=claude-opus-4-7
[2026-05-23T14:05:23Z] pass=1 done findings=3 files_scanned=42 duration_s=323
```
Letzte Zeile: `mode=pro complete passes=8 findings_total=<N> duration_s=<T>`.

Implementierungs-Skelett (im Command auszufuehren):
```bash
# Pro-Mode aktiv? Marker oder Flag setzen?
if [ -f "${GITHUB_WORKSPACE}/.claude/.pro-mode" ] || [ "$1" = "--pro-mode" ] || [ "$2" = "--pro-mode" ]; then
  PRO_MODE=1
fi

# Logfile vorbereiten
TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)
LOG="<pfad>/docs/legal-audit/audit-execution-${TS}.log"
mkdir -p "<pfad>/docs/legal-audit/passes"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] mode=pro start target=<pfad>" >> "$LOG"
```

Pro-Mode + `--compare`/`--pdf` sind kombinierbar.

Beide normalen Flags kombinierbar.

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

3. **Dispatch `legal-auditor`-Agent** mit der Codebase:
   - **Default-Mode (Opus 4.7 [1M]):** ein einziger Subagent-Lauf scannt alle 8 Passes in einem 1M-Kontextfenster.
   - **Pro-Mode (Opus 4.7 Standard, 200K):** acht sequentielle `Task`-Aufrufe an `legal-auditor`, jeder mit der Anweisung "Fuehre ausschliesslich Pass <N> aus, lade nur die fuer diesen Pass relevanten KB-Chunks, persistiere Findings nach `docs/legal-audit/passes/pass-<N>.json`, gib eine kurze JSON-Zusammenfassung zurueck (findings_count, files_scanned, dauer_sek)". Vor jedem Pass und nach jedem Pass eine Zeile ins Execution-Logfile schreiben (siehe Format oben).
   - In beiden Modi: Klassifizierung nach Severity-Matrix (CRIT/HIGH/MED/LOW), Checklisten aus `knowledge/checklisten/audit-<codebase-typ>.md`.

4. **Pro Finding dispatch `legal-text-writer`-Agent** zur Erstellung der Clean-Version unter `docs/legal-audit/clean/F-NNN-<slug>.md`. (Im Pro-Mode auch hier Standard-Kontext — Clean-Versionen sind klein genug, kein Chunking noetig.)

4a. **Pro-Mode Aggregation:** nach Abschluss aller acht Passes liest der Orchestrator die acht `passes/pass-<N>.json`-Dateien, vergibt fortlaufende Finding-IDs (F-001, F-002, ...) und schreibt das konsolidierte `LegalAudit.md`. Zeile "complete" ins Logfile.

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
- [ ] Parallel-Kopie nach `${GITHUB_WORKSPACE}/audits/<projektname>-<timestamp>/` (Schatten-Archiv)
- [ ] **Pro-Mode zusaetzlich:** `audit-execution-<ts>.log` mit acht Pass-Eintraegen + `complete`-Zeile, plus acht `passes/pass-<N>.json` mit Roh-Findings vor Konsolidierung.

## Nach Abschluss

Gib dem User eine Zusammenfassung:
- Anzahl Findings pro Severity
- Top-3 CRIT/HIGH mit 1-Zeilen-Beschreibung
- Geschaetzter Korrekturaufwand
- Empfohlene naechste Schritte (insb. Anwalts-Pruefung fuer CRIT-Findings)
