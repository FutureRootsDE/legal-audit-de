# legal-audit-de

> Multi-Platform-Toolkit für **deutsche und EU-Rechts-Audits** von Codebases, Live-URLs und Rechtsdokumenten — verfügbar für **Claude Code**, **OpenAI Codex CLI** und **GitHub Copilot CLI**.
>
> **⚠️ This is NOT legal advice.** See [Disclaimer](#disclaimer) below.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Language](https://img.shields.io/badge/language-German-informational)](#sprache)
[![Scope](https://img.shields.io/badge/scope-DE%20%2F%20EU-blue)](#rechtsgebiete-scope)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-orange)](#installation)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-supported-black)](#codex-cli)
[![Copilot CLI](https://img.shields.io/badge/GitHub%20Copilot%20CLI-supported-181717)](#github-copilot-cli)

🇬🇧 [English README](README.en.md)

---

## Was ist `legal-audit-de`?

Ein Claude-Code-Plugin, das wie ein IT-/Datenschutz-Fachaudit agiert. Es analysiert Codebases, Live-Websites und einzelne Rechtsdokumente auf Verstöße gegen deutsches und EU-Recht und liefert:

- **`LegalAudit.md`** mit Findings klassifiziert nach Severity (CRIT / HIGH / MED / LOW)
- **Clean-Versionen** der beanstandeten Stellen — 1:1 übernehmbar in das Zielprojekt
- **Live-Browser-Checks** via `chrome-devtools-mcp` (Cookie-Banner-Blocking, Google-Fonts-Leaks, Pre-/Post-Consent-Verhalten)
- **Einzel-Dokument-Prüfungen** (AGB, DSE, Impressum, Widerrufsbelehrung, Cookie-Richtlinie)

## Features

### 🔎 Commands

| Command | Zweck |
|---------|-------|
| `/legal-audit <pfad>` | Vollständiger Rechts-Audit einer Codebase |
| `/legal-audit-live <url>` | Live-Browser-Check einer öffentlichen URL |
| `/legal-doc-check <datei>` | Einzel-Dokument-Prüfung (AGB/DSE/Impressum/Widerruf/Cookie) |
| `/legal-kb <slug>` | KB-Artikel gezielt in den Kontext laden |
| `/legal-verify <thema>` | Fachanwalts- und Tool-Empfehlungen |
| `/legal-update [--stale-only]` | KB gegen Primärquellen aktualisieren |
| `/legal-audit-de-update` | **NEU** — Plugin + KB gemeinsam aktualisieren (Marketplace-Refresh + Primärquellen-Verifikation) |
| `/legal-status` | Plugin-Gesundheit (KB-Alter, Platzhalter, Hook-Status) |

### 🤖 Agenten

Drei Custom-Agents (alle Claude Opus 4.7 [1M] — maximale Zitat-Genauigkeit):

- `legal-auditor` — scannt Codebase, klassifiziert Findings
- `legal-researcher` — verifiziert jedes Zitat gegen Primärquellen (Tier-1-Kaskade)
- `legal-text-writer` — erstellt Clean-Versionen inkl. Disclaimer-Injection

### 📚 Knowledge Base

63 kuratierte KB-Dateien mit Primärquellen-Links:

- **Gesetze**: DSGVO, BDSG, TDDDG, UWG, PAngV, BGB/AGB, DDG, DSA, DMA, AI Act, BFSG, UrhG, MarkenG, NIS2-BSIG
- **Themen**: Cookie-Consent, Tracking, Datenschutzerklärung, AGB, Widerruf, Drittland, AVV, DSFA, KI-Transparenz, Social Media, KUG, Siegel-Werbung, Zitatrecht, Tool-Katalog (80+ Tools)
- **Urteile**: EuGH Schrems II, Planet49, Fashion ID, Meta-Bundeskartellamt; BGH Cookie-Einwilligung, Inbox-Werbung; LG München I „Google Fonts"
- **Behörden**: DSK, EDSA, BfDI, Landesbeauftragte
- **Checklisten** für SaaS, Landingpage, E-Commerce, n8n, Content/Blog, Pre-Launch

### ⚡ Hook-basiertes Context-Management

Der Clou: die 63 KB-Dateien werden **nicht** komplett in jede Session geladen. Stattdessen:

- **SessionStart-Hook** lädt nur `knowledge/INDEX.md` (~1.000 Tokens)
- **UserPromptSubmit-Hook** matcht den Prompt gegen Regex-Patterns in `.claude/hooks/triggers.json` und lädt bis zu 3 passende KB-Chunks on-demand
- **PostToolUse-Hook** validiert Disclaimer-Injection in jeder geschriebenen Output-Datei

Damit bleibt dein Kontext schlank und aktuelles Rechtswissen trotzdem parat.

## Installation

### Voraussetzungen

- Python ≥ 3.10 (für Hook-Skripte und Sync-Tool)
- Eine der folgenden CLIs:
  - [Claude Code](https://claude.com/claude-code) ≥ 2.0 (vollständige Feature-Unterstützung)
  - [OpenAI Codex CLI](https://github.com/openai/codex) (eingeschränkt — siehe Limitationen)
  - [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) (eingeschränkt — siehe Limitationen)
- Optional: [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) für `/legal-audit-live`
- Optional: [Obsidian](https://obsidian.md/) für visuelle KB-Navigation (Graph-View, Backlinks)

### Claude Code (empfohlen — vollständige Hook-Architektur)

#### Marketplace

```bash
# In Claude Code — Marketplace hinzufügen, dann Plugin installieren
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

Updates später via:
```bash
/plugin marketplace update futureroots-legal
/legal-audit-de-update
```

#### Workspace-Clone

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
claude
```

Beim ersten Start lädt der SessionStart-Hook automatisch `knowledge/INDEX.md`. Danach kannst du sofort loslegen:

```
/legal-audit /pfad/zu/deinem/projekt
```

### Codex CLI

Voraussetzung: [OpenAI Codex CLI](https://github.com/openai/codex) installiert.

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
codex
```

Codex lädt automatisch `AGENTS.md` und `.codex/config.toml`. Slash-Prompts liegen unter `.codex/prompts/`. Aufruf:

```
/legal-audit ./mein-projekt
```

**Wichtige Unterschiede zu Claude Code:**
- Keine SessionStart-/UserPromptSubmit-Hooks → die Skills laden `knowledge/INDEX.md` selbst und ziehen passende KB-Chunks bei Bedarf (Auto-Routing).
- Kein `WebSearch`-Tool → Tier-1-Verifikation nutzt nur `http.get` auf der Whitelist-Domain-Liste in `.codex/config.toml`.
- Modell-Auswahl: das Plugin gibt `claude-opus-4-7[1m]` als Original-Modell an; Codex-User wählen ein äquivalentes Modell mit großem Kontext (z.B. `gpt-5`).

### GitHub Copilot CLI

Voraussetzung: `gh` CLI mit Copilot-Subscription, oder GitHub Copilot CLI Standalone installiert.

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
gh copilot suggest "Führe legal-audit auf das aktuelle Verzeichnis aus"
```

Copilot lädt automatisch `.github/copilot-instructions.md`. Slash-Prompts liegen unter `.github/prompts/<name>/PROMPT.md`.

**Wichtige Unterschiede zu Claude Code:**
- Keine Hook-API → analoges Auto-Routing wie bei Codex.
- Permissions werden über GitHub-App-Scopes gesteuert, nicht über Plugin-Config. Die Whitelist in `.github/copilot-instructions.md` ist eine Konvention, kein Enforcement.
- `model:`-Felder in Agents werden ignoriert; Copilot nutzt seinen eigenen Default.

### Maintainer-Workflow (Cross-Platform-Sync)

Wer in `.claude/` arbeitet (Source of Truth), muss vor jedem Commit den Sync laufen lassen:

```bash
python scripts/sync-platforms.py --apply   # generiert .codex/ und .github/prompts/
python scripts/sync-platforms.py --check   # CI-Modus: exit 1 bei Drift
```

Die GitHub-Action `validate.yml` blockiert PRs, wenn der Sync nicht durchgeführt wurde.

## Quick Start

### 1. Codebase-Audit

```
/legal-audit /path/to/your/nextjs-saas
```

Claude erkennt den Projekt-Typ (SaaS / Landingpage / E-Commerce / n8n / Content), wählt die passende Checkliste und dispatcht die drei Agenten für vollständige Analyse + Clean-Versionen + Zitat-Verifikation. Ergebnis landet unter `docs/legal-audit/` im Zielprojekt.

### 2. Live-Website-Check

```
/legal-audit-live https://your-website.com
```

Prüft per Browser-Automation, welche Drittanbieter-Requests VOR und NACH Cookie-Consent feuern. Deckt klassische Abmahngründe auf: Google Fonts Laufzeit-Leaks, Tracker vor Consent, Pixel ohne Einwilligung.

### 3. Dokument-Review

```
/legal-doc-check /path/to/your/agb.md
```

Einzelne Rechtstexte (AGB, DSE, Impressum, Widerrufsbelehrung, Cookie-Policy) werden gegen aktuelle Rechtslage geprüft. Liefert Finding-Tabelle + vollständige korrigierte Fassung.

## Rechtsgebiete (Scope)

**Aktiviert:** DSGVO · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · KUG · MarkenG · NIS2-BSIG

**Nicht im Scope:** Strafrecht · Arbeitsrecht · Steuerrecht (außer HGB § 257 Retention) · Gesellschaftsrecht · Rechtsordnungen außerhalb DE/EU

## Sprache

Alle Outputs, Findings und KB-Artikel sind auf **Deutsch**. Code-Kommentare und Metadaten nutzen Englisch.

Wenn du Claude in Englisch bevorzugst, funktioniert das Plugin weiterhin — die juristischen Inhalte bleiben aber deutschsprachig, weil die Gesetzes-Zitate und Paragraphen-Formulierungen in der Originalsprache bindend sind.

Für englischsprachige Nutzer (die in Deutschland arbeiten oder DE/EU-Recht verstehen müssen): siehe [README.en.md](README.en.md) und das [englische Wiki](https://github.com/FutureRootsDE/legal-audit-de/wiki/Home-English).

## Quellen-Hierarchie

Der `legal-researcher`-Agent verifiziert jedes Zitat gegen:

**Tier 1** (verbindlich): `eur-lex.europa.eu`, `gesetze-im-internet.de`, `rechtsprechung-im-internet.de`, `curia.europa.eu`, `bundesanzeiger.de`

**Tier 2** (amtliche Sekundärquellen): `bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, Landesbeauftragte, `bsi.bund.de`

**Tier 3** (nur zur Einordnung, nie als Zitatbeleg): Kanzlei-Blogs

Jede Zitat-Verifikation wird unter `.claude/logs/zitate-verifikation-<datum>.log` protokolliert.

## Architektur

Details in [CLAUDE.md](CLAUDE.md) (Claude-spezifisch) und [AGENTS.md](AGENTS.md) (plattform-übergreifend). Kurzfassung:

```
legal-audit-de/
├── AGENTS.md                       # Top-Level für Codex / generische Agent-CLIs
├── CLAUDE.md                       # Claude-Code-spezifische Anleitung
├── README.md / README.en.md        # User-Doku (DE / EN)
│
├── .claude-plugin/
│   ├── plugin.json                 # Claude-Code-Plugin-Manifest
│   └── marketplace.json            # Marketplace-Metadaten
│
├── .claude/                        # ★ SOURCE OF TRUTH ★
│   ├── commands/*.md               # 8 Slash-Commands
│   ├── agents/*.md                 # 3 Custom-Agents
│   ├── skills/*/SKILL.md           # 4 Skills
│   ├── hooks/*.py                  # 3 Hooks (SessionStart / PromptSubmit / PostToolUse)
│   └── settings.json               # Permissions, WebFetch-Whitelist
│
├── .codex/                         # ⚙ generiert von scripts/sync-platforms.py
│   ├── config.toml                 # Codex-Konfiguration
│   ├── prompts/*.md                # 8 Prompts
│   ├── agents/*.md                 # 3 Agents
│   └── skills/*/SKILL.md           # 4 Skills (mit Auto-Routing)
│
├── .github/
│   ├── copilot-instructions.md     # Top-Level für Copilot CLI
│   ├── workflows/                  # GitHub Actions (validate.yml, release.yml)
│   ├── prompts/<name>/PROMPT.md    # ⚙ 8 Prompts (generiert)
│   ├── agents/*.md                 # ⚙ 3 Agents (generiert)
│   └── skills/*/SKILL.md           # ⚙ 4 Skills (generiert)
│
├── knowledge/                      # 63 KB-Dateien (Gesetze, Themen, Urteile, Behörden, Checklisten)
│   └── INDEX.md                    # einzige immer-geladene Datei (Claude Code via Hook)
│
├── templates/                      # LegalAudit-, Clean-, Disclaimer-Templates
└── scripts/
    ├── sync-platforms.py           # Codex/Copilot-Adapter-Generator
    ├── legal-status.py             # Plugin-Health-Check
    ├── audit-compare.py            # Audit-Diff-Tool
    ├── find-placeholders.py        # Platzhalter-Scanner
    └── legal-audit-pdf.py          # PDF-Bundling
```

Verzeichnisse mit ⚙ werden automatisch aus `.claude/` generiert. Direkte Edits dort werden vom Sync-Tool überschrieben.

## Roadmap

- [x] **v1.3.0** Multi-Platform-Support: Codex CLI + GitHub Copilot CLI (zusätzlich zu Claude Code)
- [x] **v1.3.0** GitHub Actions: `validate.yml` (Sync-Check, Disclaimer-Check, Platzhalter-Scan) + `release.yml` (Bundle-Build und Auto-Release bei Tag)
- [x] **v1.2.0** Tier-1-KB-Update-Wave: 40+ Aktenzeichen-Korrekturen, Primärquellen-Verifikation
- [x] **v1.1.0** Marketplace-Struktur (`.claude-plugin/marketplace.json`) + `/legal-audit-de-update`
- [ ] Marketplace-Submission für die offizielle Claude-Code-Plugin-Registry
- [ ] Englische KB-Kurzübersicht in `knowledge/en/SUMMARY.md` (für nicht-deutschsprachige Nutzer)
- [ ] Zusätzliche Checklisten: Mobile Apps (iOS/Android BFSG), API-only Services
- [ ] Integration mit `trivy`, `bandit`, anderen Security-Scannern für kombinierte Audits
- [ ] CI-Integration: automatische KB-Aktualitätsprüfungen (alle 90 Tage gegen Tier-1-Quellen)

## Contributing

Beiträge willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details:
- Neue Checklisten
- Weitere KB-Artikel zu Spezial-Themen
- Übersetzung englischer Kurzfassungen
- Verifikation veralteter Zitate
- Bug-Reports bei falschen/veralteten Rechts-Informationen

## Disclaimer

> **⚠️ Dieses Plugin erzeugt keine Rechtsberatung im Sinne des § 2 RDG.**
>
> Alle Ausgaben (LegalAudit.md, Clean-Versionen, KB-Artikel, Command-Outputs) dienen der **technischen Vorbereitung** einer anwaltlichen Prüfung. Eine abschließende Prüfung durch einen zugelassenen Rechtsanwalt (Fachanwalt für IT-Recht oder spezialisierter Datenschutz-Experte) ist **zwingend erforderlich**, bevor Inhalte produktiv gesetzt werden.
>
> Gesetze und Rechtsprechung ändern sich — Aktualität stets verifizieren.
>
> Die Nutzung dieses Plugins erfolgt auf eigene Verantwortung. Die Autoren und Mitwirkenden übernehmen keine Haftung für Schäden, die aus der Nutzung oder dem Vertrauen auf die Ausgaben entstehen. Siehe [LICENSE](LICENSE) für den vollständigen Haftungsausschluss.

## Ethik und Verantwortung

Dieses Plugin soll:
- die **Vorbereitungszeit** für rechtliche Prüfungen reduzieren
- Standards **demokratisieren** (auch Solo-Gründer sollen compliant launchen können)
- Entwickler **sensibilisieren** für wichtige Rechtsthemen im DE/EU-Kontext

Dieses Plugin soll **nicht**:
- Anwältinnen oder Datenschutzbeauftragte ersetzen
- Produktiv-Entscheidungen ohne menschliche Prüfung legitimieren
- Fehlerhafte oder veraltete Auskünfte abdecken (dafür gibt es aktive Issues und PRs)

Wenn du das Plugin in professionellem Kontext nutzt, gib bitte an, dass es eine **Vor-Prüfung** ist und hole eine anwaltliche Freigabe ein.

## Security

Siehe [SECURITY.md](SECURITY.md) für die Vulnerability-Disclosure-Policy.

## License

[MIT](LICENSE) — frei für jeden Einsatzzweck. Alle Rechte an zitierten Gesetzestexten und Urteilen bleiben bei den jeweiligen Rechteinhabern (EU, Bundesrepublik Deutschland, Gerichten).

## Credits

Aufgebaut auf [Claude Code](https://claude.com/claude-code) von Anthropic.

Inspiriert von der Erkenntnis, dass DSGVO-Compliance für technische Teams ohne Rechtsabteilung unnötig schwer ist — und dass gutes Vorbereitungswerkzeug den Fachanwalts-Zugang für Solo-Gründer bezahlbar macht.

---

**Fragen? Issues? Beiträge?** → [GitHub Issues](https://github.com/FutureRootsDE/legal-audit-de/issues) · [Discussions](https://github.com/FutureRootsDE/legal-audit-de/discussions) · [Wiki](https://github.com/FutureRootsDE/legal-audit-de/wiki)
