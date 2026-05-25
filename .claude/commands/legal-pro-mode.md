---
description: Aktiviert, deaktiviert oder prueft den Pro-Mode fuer Claude Pro-Abonnenten (Standard-Kontext statt 1M). Schaltet das Agenten-Routing zwischen 1M- und Standard-Varianten um.
argument-hint: enable | disable | status [--json]
allowed-tools: Bash, Read
---

# /legal-pro-mode

Steuert den **Pro-Mode** des legal-audit-de Plugins.

## Hintergrund

Das Plugin nutzt standardmaessig `claude-opus-4-7[1m]` (1M-Kontext) fuer alle drei
Agenten. Das erfordert ein **Max-Abonnement** (100 USD/Monat).

Der **Pro-Mode** schaltet auf `claude-opus-4-7` (Standard-Kontext ~200k) um und ist
kompatibel mit dem **Pro-Abonnement** (20 USD/Monat).

| | Standard | Pro-Mode |
|--|----------|----------|
| Abonnement | Max (100 USD/Mo) | Pro (20 USD/Mo) |
| Kontext-Fenster | 1M Tokens | ~200k Tokens |
| Codebases | bis ~700k Tokens | bis ~150k Tokens |
| Agenten | `legal-auditor` etc. | `legal-auditor-pro` etc. |

## Subcommands

### `/legal-pro-mode enable`
Aktiviert den Pro-Mode. Schreibt Marker nach `${CLAUDE_PLUGIN_DATA}/pro-mode.json`
(offizieller Plugin-Datenspeicher, ueberlebt Plugin-Updates).

```bash
python "${CLAUDE_PROJECT_DIR}/scripts/legal-audit-pro-mode.py" enable
```

### `/legal-pro-mode disable`
Deaktiviert den Pro-Mode. Loescht den Marker.

```bash
python "${CLAUDE_PROJECT_DIR}/scripts/legal-audit-pro-mode.py" disable
```

### `/legal-pro-mode status`
Zeigt den aktuellen Status.

```bash
python "${CLAUDE_PROJECT_DIR}/scripts/legal-audit-pro-mode.py" status
```

### `/legal-pro-mode status --json`
Maschinenlesbarer JSON-Output (fuer Skripte und CI).

```bash
python "${CLAUDE_PROJECT_DIR}/scripts/legal-audit-pro-mode.py" status --json
```

## Marker-Persistenz

Der Marker wird an zwei Orten gesucht (in Prioritaetsreihenfolge):

1. `${CLAUDE_PLUGIN_DATA}/pro-mode.json` — offizieller Plugin-Datenspeicher
   (ueberlebt `/plugin install` und Marketplace-Refreshes)
2. `~/.claude/legal-audit-de-pro-mode.json` — Fallback wenn `CLAUDE_PLUGIN_DATA`
   nicht gesetzt ist

## Wie es funktioniert

1. **`/legal-pro-mode enable`** schreibt `{"enabled": true, ...}` in den Marker.
2. Der **SessionStart-Hook** liest den Marker bei jedem Session-Start und injiziert
   einen Kontext-Block mit der Routing-Tabelle.
3. **Commands** (`/legal-audit`, `/legal-doc-check`, etc.) pruefen den Marker und
   dispatchen die `-pro`-Agent-Varianten statt der Standard-Agenten.

## Einschraenkungen im Pro-Mode

- Codebases > 150 KB koennen den Kontext ueberschreiten (200k-Fenster)
- In diesem Fall: der Pro-Agent priorisiert CRIT/HIGH und vermerkt den Abbruch
- Ab v1.4.0 wird ein `--chunked`-Flag mit Session-Logfiles ergaenzt

## Nach Abschluss

Ausgabe: Statusbestaetigung mit Marker-Pfad und aktivem Routing.
