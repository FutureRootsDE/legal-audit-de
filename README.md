# legal-audit-de

> Claude Code plugin for systematic **German and EU legal audits** of codebases, live URLs, and legal documents.
>
> **⚠️ This is NOT legal advice.** See [Disclaimer](#disclaimer) below.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Language](https://img.shields.io/badge/language-German-informational)](#sprache)
[![Scope](https://img.shields.io/badge/scope-DE%20%2F%20EU-blue)](#rechtsgebiete)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-orange)](#installation)

---

## Was ist `legal-audit-de`?

Ein Claude-Code-Plugin, das wie ein IT-/Datenschutz-Fachaudit agiert. Es analysiert Codebases, Live-Websites und einzelne Rechtsdokumente auf Verstoesse gegen deutsches und EU-Recht und liefert:

- **`LegalAudit.md`** mit Findings klassifiziert nach Severity (CRIT / HIGH / MED / LOW)
- **Clean-Versionen** der beanstandeten Stellen — 1:1 uebernehmbar in das Zielprojekt
- **Live-Browser-Checks** via `chrome-devtools-mcp` (Cookie-Banner-Blocking, Google-Fonts-Leaks, Pre-/Post-Consent-Verhalten)
- **Einzel-Dokument-Pruefungen** (AGB, DSE, Impressum, Widerrufsbelehrung, Cookie-Richtlinie)

## Features

### 🔎 Commands

| Command | Zweck |
|---------|-------|
| `/legal-audit <pfad>` | Vollstaendiger Rechts-Audit einer Codebase |
| `/legal-audit-live <url>` | Live-Browser-Check einer oeffentlichen URL |
| `/legal-doc-check <datei>` | Einzel-Dokument-Pruefung (AGB/DSE/Impressum/Widerruf/Cookie) |
| `/legal-kb <slug>` | KB-Artikel gezielt in den Kontext laden |
| `/legal-verify <thema>` | Fachanwalts- und Tool-Empfehlungen |
| `/legal-update [--stale-only]` | KB gegen Primaerquellen aktualisieren |
| `/legal-status` | Plugin-Gesundheit (KB-Alter, Platzhalter, Hook-Status) |

### 🤖 Agenten

Drei Custom-Agents (alle Claude Opus 4.7 [1M] — maximale Zitat-Genauigkeit):

- `legal-auditor` — scant Codebase, klassifiziert Findings
- `legal-researcher` — verifiziert jedes Zitat gegen Primaerquellen (Tier-1-Kaskade)
- `legal-text-writer` — erstellt Clean-Versionen inkl. Disclaimer-Injection

### 📚 Knowledge Base

63 kuratierte KB-Dateien mit Primaerquellen-Links:

- **Gesetze**: DSGVO, BDSG, TDDDG, UWG, PAngV, BGB/AGB, DDG, DSA, DMA, AI Act, BFSG, UrhG, MarkenG, NIS2-BSIG
- **Themen**: Cookie-Consent, Tracking, Datenschutzerklaerung, AGB, Widerruf, Drittland, AVV, DSFA, KI-Transparenz, Social Media, KUG, Siegel-Werbung, Zitatrecht, Tool-Katalog (80+ Tools)
- **Urteile**: EuGH Schrems II, Planet49, Fashion ID, Meta-Bundeskartellamt; BGH Cookie-Einwilligung, Inbox-Werbung; LG Muenchen I "Google Fonts"
- **Behoerden**: DSK, EDSA, BfDI, Landesbeauftragte
- **Checklisten** fuer SaaS, Landingpage, E-Commerce, n8n, Content/Blog, Pre-Launch

### ⚡ Hook-basiertes Context-Management

Der Clou: die 63 KB-Dateien werden **nicht** komplett in jede Session geladen. Stattdessen:

- **SessionStart-Hook** laedt nur `knowledge/INDEX.md` (~1.000 Tokens)
- **UserPromptSubmit-Hook** matcht den Prompt gegen Regex-Patterns in `.claude/hooks/triggers.json` und laedt bis zu 3 passende KB-Chunks on-demand
- **PostToolUse-Hook** validiert Disclaimer-Injection in jeder geschriebenen Output-Datei

Damit bleibt dein Kontext schlank und aktuelles Rechtswissen trotzdem parat.

## Installation

### Voraussetzungen

- [Claude Code](https://claude.com/claude-code) >= 2.0
- Python >= 3.10 (fuer Hook-Skripte)
- Optional: [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) fuer `/legal-audit-live`
- Optional: [Obsidian](https://obsidian.md/) fuer visuelle KB-Navigation (Graph-View, Backlinks)

### Installation als Plugin

```bash
# In Claude Code
/plugin install FutureRootsDE/legal-audit-de
```

### Installation als Workspace-Clone

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
claude
```

Beim ersten Start laedt der SessionStart-Hook automatisch `knowledge/INDEX.md`. Danach kannst du sofort loslegen:

```
/legal-audit /pfad/zu/deinem/projekt
```

## Quick Start

### 1. Codebase-Audit

```
/legal-audit /path/to/your/nextjs-saas
```

Claude erkennt den Projekt-Typ (SaaS / Landingpage / E-Commerce / n8n / Content), waehlt die passende Checkliste und dispatcht die drei Agenten fuer vollstaendige Analyse + Clean-Versionen + Zitat-Verifikation. Ergebnis landet unter `docs/legal-audit/` im Zielprojekt.

### 2. Live-Website-Check

```
/legal-audit-live https://your-website.com
```

Prueft per Browser-Automation, welche Drittanbieter-Requests VOR und NACH Cookie-Consent feuern. Deckt klassische Abmahngruende auf: Google Fonts Laufzeit-Leaks, Tracker vor Consent, Pixel ohne Einwilligung.

### 3. Dokument-Review

```
/legal-doc-check /path/to/your/agb.md
```

Einzelne Rechtstexte (AGB, DSE, Impressum, Widerrufsbelehrung, Cookie-Policy) werden gegen aktuelle Rechtslage geprueft. Liefert Finding-Tabelle + vollstaendige korrigierte Fassung.

## Rechtsgebiete (Scope)

**Aktiviert:** DSGVO · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · MarkenG · NIS2-BSIG

**Nicht im Scope:** Strafrecht · Arbeitsrecht · Steuerrecht (ausser HGB § 257 Retention) · Gesellschaftsrecht · Rechtsordnungen ausserhalb DE/EU

## Sprache

Alle Outputs, Findings und KB-Artikel sind auf **Deutsch**. Code-Kommentare und Metadaten nutzen Englisch.

Wenn du Claude in Englisch bevorzugst, funktioniert das Plugin weiterhin — die juristischen Inhalte bleiben aber deutschsprachig, weil die Gesetzes-Zitate und Paragraphen-Formulierungen in der Originalsprache bindend sind.

## Quellen-Hierarchie

Der `legal-researcher`-Agent verifiziert jedes Zitat gegen:

**Tier 1** (verbindlich): `eur-lex.europa.eu`, `gesetze-im-internet.de`, `rechtsprechung-im-internet.de`, `curia.europa.eu`, `bundesanzeiger.de`

**Tier 2** (amtliche Sekundaerquellen): `bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, Landesbeauftragte, `bsi.bund.de`

**Tier 3** (nur zur Einordnung, nie als Zitatbeleg): Kanzlei-Blogs

Jede Zitat-Verifikation wird unter `.claude/logs/zitate-verifikation-<datum>.log` protokolliert.

## Architektur

Details in [CLAUDE.md](CLAUDE.md). Kurzfassung:

```
legal-audit-de/
├── plugin.json                 # Plugin-Manifest
├── CLAUDE.md                   # Claude-Orientierung
├── .claude/
│   ├── commands/*.md           # 7 Slash-Commands
│   ├── agents/*.md             # 3 Custom-Agents
│   ├── skills/*/SKILL.md       # 4 Skills
│   ├── hooks/*.py              # 3 Hooks (SessionStart / PromptSubmit / PostToolUse)
│   └── settings.json           # Hook-Registrierung
├── knowledge/                  # 63 KB-Dateien (Gesetze, Themen, Urteile, Behoerden, Checklisten, Anwaelte-Tools)
│   └── INDEX.md                # einzige immer-geladene Datei
├── templates/                  # LegalAudit-, Clean-, Disclaimer-Templates
└── scripts/                    # Python-Hilfsskripte
```

## Roadmap

- [ ] Marketplace-Submission fuer Claude-Code-Plugin-Registry
- [ ] Englische KB-Kurzuebersicht in `knowledge/en/SUMMARY.md` (fuer nicht-deutschsprachige Nutzer)
- [ ] Zusaetzliche Checklisten: Mobile Apps (iOS/Android BFSG), API-only Services
- [ ] Integration mit `trivy`, `bandit`, anderen Security-Scannern fuer kombinierte Audits
- [ ] CI-Integration: GitHub Action fuer automatische KB-Aktualitaetspruefungen

## Contributing

Beitraege willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) fuer Details:
- Neue Checklisten
- Weitere KB-Artikel zu Spezial-Themen
- Uebersetzung englischer Kurzfassungen
- Verifikation veralteter Zitate
- Bug-Reports bei falschen/veralteten Rechts-Informationen

## Disclaimer

> **⚠️ Dieses Plugin erzeugt keine Rechtsberatung im Sinne des § 2 RDG.**
>
> Alle Ausgaben (LegalAudit.md, Clean-Versionen, KB-Artikel, Command-Outputs) dienen der **technischen Vorbereitung** einer anwaltlichen Pruefung. Eine abschliessende Pruefung durch einen zugelassenen Rechtsanwalt (Fachanwalt fuer IT-Recht oder spezialisierter Datenschutz-Experte) ist **zwingend erforderlich**, bevor Inhalte produktiv gesetzt werden.
>
> Gesetze und Rechtsprechung aendern sich — Aktualitaet stets verifizieren.
>
> Die Nutzung dieses Plugins erfolgt auf eigene Verantwortung. Die Autoren und Mitwirkenden uebernehmen keine Haftung fuer Schaeden, die aus der Nutzung oder dem Vertrauen auf die Ausgaben entstehen. Siehe [LICENSE](LICENSE) fuer den vollstaendigen Haftungsausschluss.

## Ethik und Verantwortung

Dieses Plugin soll:
- die **Vorbereitungszeit** fuer rechtliche Pruefungen reduzieren
- Standards **demokratisieren** (auch Solo-Gruender sollen compliant launchen koennen)
- Entwickler **sensibilisieren** fuer wichtige Rechtsthemen im DE/EU-Kontext

Dieses Plugin soll **nicht**:
- Anwaeltinnen oder Datenschutzbeauftragte ersetzen
- Produktiv-Entscheidungen ohne menschliche Pruefung legitimieren
- Fehlerhafte oder veraltete Auskuenfte abdecken (dafuer gibt es aktive Issues und PRs)

Wenn du das Plugin in professionellem Kontext nutzt, gib bitte an, dass es eine **Vor-Pruefung** ist und hole eine anwaltliche Freigabe ein.

## Security

Siehe [SECURITY.md](SECURITY.md) fuer die Vulnerability-Disclosure-Policy.

## License

[MIT](LICENSE) — frei fuer jeden Einsatzzweck. Alle Rechte an zitierten Gesetzestexten und Urteilen bleiben bei den jeweiligen Rechteinhabern (EU, Bundesrepublik Deutschland, Gerichten).

## Credits

Aufgebaut auf [Claude Code](https://claude.com/claude-code) von Anthropic.

Inspiriert von der Erkenntnis, dass DSGVO-Compliance fuer technische Teams ohne Rechtsabteilung unnoetig schwer ist — und dass gutes Vorbereitungswerkzeug den Fachanwalts-Zugang fuer Solo-Gruender bezahlbar macht.

---

**Questions? Issues? Contributions?** → [GitHub Issues](https://github.com/FutureRootsDE/legal-audit-de/issues)
