---
title: Setup
layout: default
nav_order: 2
description: "Installation fuer Claude Code, Codex CLI und Copilot CLI, plus Pro-Mode und optionale MCP-Beschleunigung"
---

# Setup
{: .no_toc }

## Inhalt
{: .no_toc .text-delta }

1. TOC
{:toc}

---

{: .warning }
> **Disclaimer.** Die folgenden Anleitungen aktivieren ein Audit-Tool. Sie ersetzen weder Anwalt noch DSB. Jeder Output traegt den Pflicht-Hinweis nach Paragraph 2 RDG, dass keine Rechtsberatung vorliegt.

## Voraussetzungen

| Komponente | Mindestversion | Notiz |
|------------|----------------|-------|
| Python | 3.10 | Fuer Hook-Skripte und Sync-Tool |
| Eine CLI | siehe unten | Claude Code, Codex CLI oder Copilot CLI |

Optional:

- [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) — Voraussetzung fuer `/legal-audit-live`
- [Obsidian](https://obsidian.md/) — Visualisierung der Knowledge Base mit Backlinks und Graph
- [`wolfgangihloff/rechtsinformationen-bund-de-mcp`](https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp) — strukturierter ELI/ECLI-Zugriff, Details unter [MCP-Integration](mcp-integration)

## Claude Code (empfohlen — volle Hook-Architektur)

### Variante A: Marketplace

```text
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

Updates:

```text
/plugin marketplace update futureroots-legal
/legal-audit-de-update
```

### Variante B: Workspace-Clone

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
claude
```

Beim ersten Start laedt der SessionStart-Hook nur `knowledge/INDEX.md`. Danach:

```text
/legal-audit /pfad/zu/deinem-projekt
```

### Was Claude Code gegenueber Codex und Copilot exklusiv kann

- `SessionStart`-Hook fuer KB-Index-Loading
- `UserPromptSubmit`-Hook fuer automatisches KB-Routing nach Schlagwoertern
- `PostToolUse`-Hook fuer Disclaimer-Validierung
- Native `WebSearch` fuer Aktenzeichen-Recherche

## OpenAI Codex CLI

### Variante A: Codex-Marketplace

```bash
codex plugin marketplace add FutureRootsDE/legal-audit-de
```

Das Repo enthaelt:

- `.codex-plugin/plugin.json` als natives Codex-Manifest
- `.agents/plugins/marketplace.json` als Codex-Marketplace-Eintrag
- `.codex/skills/` mit den portierten Skills

### Variante B: Workspace-Clone

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
codex
```

### Unterschiede gegenueber Claude Code

- Kein `SessionStart`- und `UserPromptSubmit`-Hook. Skills uebernehmen das KB-Routing selbst.
- Kein `WebSearch`-Tool. Tier-1-Verifikation nur ueber `http.get` gegen die Whitelist in `.codex/config.toml`.
- Modell-Wahl: das Plugin notiert `claude-opus-4-7[1m]` als Original. Codex-User waehlen ein aequivalentes Large-Context-Modell, z. B. `gpt-5`.

## GitHub Copilot CLI

Erfordert `gh` CLI mit Copilot-Abo oder die Standalone-Copilot-CLI.

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
gh copilot
```

Die Copilot-Adapter liegen unter `.github/agents/`, `.github/prompts/`, `.github/skills/`. Auto-Routing ist analog zur Codex-Variante implementiert, weil Copilot ebenfalls keine SessionStart-Hooks hat.

## Pro-Mode fuer Claude-Pro-Abonnenten

Claude-Pro-Abos (20 USD/mo) haben **keinen** Zugriff auf den 1M-Kontext. Der Default-Dispatch der Agents auf `claude-opus-4-7[1m]` endet bei Pro-Usern mit `1M context requires usage credits or Max plan`.

Loesung: Pro-Mode aktivieren. Damit dispatchen die Commands die `-pro`-Agentenvarianten mit Standard-Kontext (~200 K Tokens).

```text
/legal-pro-mode enable
```

oder direkt per Skript:

```bash
python3 scripts/legal-audit-pro-mode.py enable
```

Status pruefen:

```text
/legal-pro-mode status
```

Der Marker liegt unter `${CLAUDE_PLUGIN_DATA}/pro-mode.json` und ueberlebt Plugin-Updates und Marketplace-Refreshs.

## Optional: chrome-devtools-mcp fuer Live-Browser-Checks

`/legal-audit-live <url>` braucht `chrome-devtools-mcp`. Setup:

```bash
claude mcp add --transport stdio chrome-devtools \
  -- npx -y chrome-devtools-mcp@latest
```

Damit kann der Auditor pruefen, welche Drittanbieter-Requests die Seite vor und nach Consent absetzt, ob Google Fonts trotz Self-Hosting nachgeladen wird, und ob der Cookie-Banner einen gleichwertigen Ablehnen-Button hat.

## Optional: Git-Hook im Zielprojekt

In Projekten, die haeufig rechts-relevante Aenderungen durchlaufen, lohnt ein Pre-Commit-Hook, der vor dem Commit warnt, wenn rechts-relevante Dateien ohne aktuellen Audit eingehen.

Template: `templates/git-hooks/pre-commit.sh`. Installation und `LEGAL_AUDIT_STRICT=1` als Hard-Block stehen in `templates/git-hooks/README.md`.

## Naechste Schritte

- [Commands](commands) durchschauen
- Erstes [Audit fahren](commands#legal-audit) auf einem kleinen Projekt
- Bei Pro-Abo den [Pro-Mode aktivieren](#pro-mode-fuer-claude-pro-abonnenten)
