---
description: Aktiviert oder deaktiviert den Pro-Mode (Standard-Kontext statt 1M). Notwendig fuer Claude-Pro-Abonnenten, die keinen Zugriff auf 1M-Kontext haben.
argument-hint: enable | disable | status
allowed-tools: bash, view
---
<!--
  AUTO-GENERATED — DO NOT EDIT DIRECTLY.
  Source: .claude/commands/legal-pro-mode.md
  Regenerate via: python3 scripts/sync-platforms.py --apply
-->
# /legal-pro-mode

Schaltet die `legal-*`-Subagents zwischen Default (1M-Kontext, Max/Team/Enterprise-Plan) und
Pro-Mode (Standard-Kontext via `-pro`-Agent-Varianten) um.

## Wozu

Die drei Custom-Agents (`legal-auditor`, `legal-researcher`, `legal-text-writer`) sind per
Default auf `claude-opus-4-7[1m]` gepinnt. Claude-Pro-User (20 USD/mo) haben **keinen Zugriff**
auf 1M-Kontext — der erste Agent-Aufruf endet mit
`1M context requires usage credits or Max plan`. Pro-Mode loest das, indem Commands stattdessen
die `-pro`-Varianten der Agents dispatchen (gleicher Prompt, `model: claude-opus-4-7` statt
`[1m]`-Suffix).

## Subcommands

### `/legal-pro-mode enable`
Aktiviert Pro-Mode. Schreibt einen atomaren Marker:
- Claude Code: `${CLAUDE_PLUGIN_DATA}/pro-mode.json` (ueberlebt Plugin-Updates, per
  [plugins-reference](https://code.claude.com/docs/en/plugins-reference) dokumentiert)
- Fallback: `~/.claude/legal-audit-de-pro-mode.json`
- Wenn vorhanden: zusaetzlich `~/.codex/legal-audit-de-pro-mode.json` und
  `~/.copilot/legal-audit-de-pro-mode.json`

Bitte den User danach, die CLI-Session neu zu starten, damit der SessionStart-Hook den Marker
sieht und kuenftige Subagent-Dispatches auf `-pro` umlenkt.

### `/legal-pro-mode disable`
Entfernt den Marker auf allen erkannten Plattformen. Dispatches schalten beim naechsten
Session-Start zurueck auf die 1M-Varianten.

### `/legal-pro-mode status`
Reportet den aktuellen Marker-Zustand pro Plattform (siehe `--json` fuer maschinenlesbar).

## Ablauf

Rufe das Script mit dem entsprechenden Subcommand auf:

```bash
python3 "${GITHUB_WORKSPACE}/scripts/legal-audit-pro-mode.py" $ARGUMENTS
```

Wenn `$ARGUMENTS` leer ist, gib eine Hilfemeldung mit den drei Subcommands aus und fordere
zu einer Auswahl auf.

Bei `enable`/`disable`: zeige dem User die geschriebenen/entfernten Pfade.

Bei `status`: bei inkonsistentem State (Marker existiert auf einer Plattform, fehlt auf
anderer) den User informieren und `enable` oder `disable` zum Resynchronisieren empfehlen.

## Hinweise

- Pro-Mode laesst die `.claude/agents/*.md`-Dateien **unangetastet**. Es werden ausschliesslich
  Marker im user-scope Persistenz-Verzeichnis gesetzt.
- Der Marker ueberlebt `/plugin install` und Plugin-Updates (per offizieller Anthropic-Doku
  fuer `${CLAUDE_PLUGIN_DATA}`).
- Die `-pro`-Varianten der Agents werden via `scripts/sync-pro-variants.py` aus den
  1M-Varianten generiert. CI prueft die Konsistenz im `validate.yml`.
- Wer eine grosse Codebase auditieren will und auf Standard-Kontext laeuft, sollte zusaetzlich
  `--chunked` an `/legal-audit` haengen (verfuegbar ab v1.4.0).
