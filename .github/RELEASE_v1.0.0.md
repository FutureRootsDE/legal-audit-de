# legal-audit-de v1.0.0 — Initial Open-Source Release

Erstes oeffentliches Release des Claude-Code-Plugins fuer systematische **deutsche und EU-Rechts-Audits** auf Codebases, Live-URLs und einzelnen Rechtsdokumenten.

## ⚠️ Wichtig zuerst

Dieses Plugin erzeugt **keine Rechtsberatung** im Sinne des § 2 RDG. Alle Ausgaben dienen der **technischen Vorbereitung** einer anwaltlichen Pruefung. Eine abschliessende Freigabe durch einen zugelassenen Rechtsanwalt (Fachanwalt fuer IT-Recht oder spezialisierter Datenschutz-Experte) ist zwingend erforderlich, bevor Inhalte produktiv gesetzt werden.

## Was ist `legal-audit-de`?

Ein Claude-Code-Plugin, das wie ein IT-/Datenschutz-Fachaudit-Prozess agiert. Es scannt Codebases, prueft Live-Websites im Browser und reviewed einzelne Rechtsdokumente — jeweils gegen den aktuellen Stand von deutschem und EU-Recht.

Der Wertbeitrag: **Reduziere die Vor-Arbeit fuer Fachanwalts-Reviews um 80-90 %**. Statt der Anwaeltin einen rohen Codebase-Link zu geben, uebergibst du eine saubere Finding-Liste mit Severity-Einstufung, Clean-Versionen und primaerquellen-verifizierten Zitaten. Das spart Honorar-Stunden und macht professionelle Rechts-Reviews fuer Solo-Gruender und kleine Teams bezahlbar.

## Scope (v1.0.0)

### Abgedeckte Rechtsgebiete
- **DSGVO / BDSG** — Datenschutz, inkl. Betroffenenrechte, AVV, VVT, TOM, DSFA, Drittlandtransfer
- **TDDDG** — § 25 Cookie-Consent (neuer Name des TTDSG seit 14.05.2024)
- **UWG** — Wettbewerbsrecht, Werbekennzeichnung, E-Mail-Marketing, Siegel-Werbung
- **PAngV** — Preisangabenverordnung (30-Tage-Tiefstpreis, Grundpreis etc.)
- **BGB / AGB** — §§ 305-310 AGB-Recht, Widerrufsbelehrung, Button-Loesung § 312j
- **DDG** — Diensteanbieterpflichten § 5 Impressum (neuer Name des TMG seit 14.05.2024)
- **DSA / DMA** — Digital Services Act, Digital Markets Act
- **AI Act** (VO 2024/1689) — Transparenzpflichten Art. 50, High-Risk-Klassifikation
- **BFSG** — Barrierefreiheitsstaerkungsgesetz (B2C ab 28.06.2025)
- **UrhG** — Urheberrecht, inkl. Zitatrecht § 51, Stockfoto-Lizenzierung
- **KUG** — Bildnisschutz §§ 22, 23 (Fotos erkennbarer Personen)
- **MarkenG** — Markenrecht
- **NIS2-BSIG** — IT-Sicherheit fuer Kritische Infrastruktur

### Nicht abgedeckt
Strafrecht · Arbeitsrecht · Steuerrecht (ausser HGB § 257 Retention) · Gesellschaftsrecht · Rechtsordnungen ausserhalb DE/EU

## Funktionen

### 7 Slash-Commands

| Command | Zweck |
|---------|-------|
| `/legal-audit <pfad>` | Vollstaendiger Rechts-Audit einer Codebase |
| `/legal-audit-live <url>` | Live-Browser-Check via chrome-devtools-mcp |
| `/legal-doc-check <datei>` | Einzel-Dokument-Pruefung (AGB, DSE, Impressum, Widerruf, Cookie, Social-Bio) |
| `/legal-kb <slug>` | KB-Artikel gezielt in Kontext laden |
| `/legal-verify <thema>` | Fachanwalts-/Tool-Empfehlungen |
| `/legal-update [--stale-only]` | KB gegen Primaerquellen aktualisieren |
| `/legal-status` | Plugin-Gesundheit |

### 3 Custom-Agents auf Claude Opus 4.7 [1M]

- `legal-auditor` — scannt, klassifiziert Findings nach CRIT/HIGH/MED/LOW
- `legal-researcher` — verifiziert jedes Zitat gegen Tier-1-Primaerquelle
- `legal-text-writer` — erstellt Clean-Versionen mit automatischer Disclaimer-Injection

### 63 Knowledge-Base-Dateien

- **14 Gesetze** mit Primaerquellen-Links (eur-lex, gesetze-im-internet, curia)
- **25 Themen** (Cookie-Consent, Tracking, DSE, AGB, Drittland, AVV, DSFA, KI-Transparenz, Social Media, KUG, Siegel-Werbung, Zitatrecht, Tool-Katalog mit 80+ Tools)
- **6 Urteile** (EuGH Schrems II, Planet49, Fashion ID, Meta-Bundeskartellamt; BGH Cookie-Einwilligung, Inbox-Werbung; LG Muenchen I "Google Fonts")
- **4 Behoerden-Uebersichten** (DSK, EDSA, BfDI, Landesbeauftragte)
- **6 Audit-Checklisten** (SaaS, Landingpage, E-Commerce, n8n, Content/Blog, Pre-Launch)
- **7 Anwaelte-/Tool-Empfehlungen**

### Hook-basiertes Context-Management (Kern-Innovation)

Statt die 63 KB-Dateien bei jeder Session vollstaendig zu laden:

- **SessionStart-Hook** laedt nur `knowledge/INDEX.md` (~1.000 Tokens)
- **UserPromptSubmit-Hook** matcht den Prompt gegen Regex-Patterns in `.claude/hooks/triggers.json` und laedt bis zu 3 passende KB-Chunks on-demand
- **PostToolUse-Hook** validiert Disclaimer-Injection in jeder geschriebenen Output-Datei

Damit bleibt der Kontext schlank (< 2 k Tokens initial) und aktuelles Rechtswissen trotzdem parat.

### Quellen-Hierarchie

Jedes Zitat wird gegen eine Tier-1-Primaerquelle verifiziert:

- **Tier 1** (verbindlich): `eur-lex.europa.eu`, `gesetze-im-internet.de`, `rechtsprechung-im-internet.de`, `curia.europa.eu`, `bundesanzeiger.de`
- **Tier 2** (amtliche Sekundaerquellen): `bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, Landesbeauftragte
- **Tier 3** (nur zur Einordnung, nie als Zitatbeleg): Kanzlei-Blogs wie Schwenke, Haerting, eRecht24

Jede Verifikation wird unter `.claude/logs/zitate-verifikation-<datum>.log` protokolliert.

## Installation

### Als Plugin in Claude Code

```
/plugin install FutureRootsDE/legal-audit-de
```

### Als Workspace-Clone

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
claude
```

Beim ersten Start laedt der SessionStart-Hook automatisch `knowledge/INDEX.md`.

### Voraussetzungen

- Claude Code >= 2.0
- Python >= 3.10 (fuer Hook-Skripte)
- Optional: `chrome-devtools-mcp` fuer `/legal-audit-live`
- Optional: Obsidian fuer visuelle KB-Navigation

## Quick Start

```
# Codebase-Audit
/legal-audit /path/to/your/nextjs-saas

# Live-Browser-Check (deckt Google Fonts Leaks, Tracker vor Consent)
/legal-audit-live https://your-website.com

# Einzel-Dokument-Review
/legal-doc-check /path/to/your/agb.md

# Gezielt ein KB-Thema laden
/legal-kb cookie-consent
```

## Was ist in diesem Release neu?

Da dies das **Initial Release** ist: alles! Zusammenfassend:

- Plugin-Manifest `plugin.json` (Claude-Code-Plugin-Format)
- 7 Commands, 3 Agents, 4 Skills, 3 Hooks
- 63 KB-Dateien mit verifizierten Primaerquellen
- Haftungs-Disclaimer in LICENSE + jedem Output
- MIT-Lizenz
- README auf Deutsch mit Quick-Start-Beispielen
- CONTRIBUTING-Guidelines fuer Rechts-Aenderungen (Primaerquellen-Pflicht)
- Issue-Templates fuer Bug-Report, Feature-Request, KB-Update
- Pull-Request-Template mit Checkliste fuer Rechts-Aktualisierungen
- Security-Policy + Code of Conduct (Contributor Covenant 2.1)

## Roadmap

- **v1.1** — Englische KB-Kurzuebersicht in `knowledge/en/SUMMARY.md`
- **v1.2** — Mobile-App-Checkliste (iOS/Android BFSG)
- **v1.3** — API-only-Services Checkliste
- **v1.x** — Integration mit Security-Scannern (trivy, bandit) fuer kombinierte Audits
- **v2.0** — Marketplace-Submission fuer Claude-Code-Plugin-Registry

## Dank und Motivation

Dieses Plugin ist entstanden aus der Beobachtung, dass DSGVO-Compliance fuer technische Teams ohne Rechtsabteilung unnoetig schwer ist. Der Zugang zu qualifizierten Fachanwaelten sollte nicht davon abhaengen, wieviel Vorbereitungszeit du mit manueller Recherche verbringen kannst.

Ich hoffe, dieses Plugin hilft Solo-Gruendern, Indie-Hackern und kleinen Teams dabei, rechtssicher zu launchen, ohne die ersten 5.000 Euro ihres Startups in eine Kanzlei zu investieren, bevor sie die erste Zeile produktiven Code schreiben.

## Contributing

Beitraege willkommen — insbesondere:
- Korrekturen veralteter Rechts-Zitate (mit Link zu aktueller Primaerquelle)
- Neue KB-Artikel zu Spezial-Themen
- Weitere Audit-Checklisten (Mobile Apps, Embedded Systems, etc.)
- Bug-Reports bei falschen Aussagen

Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Feedback

- [GitHub Issues](https://github.com/FutureRootsDE/legal-audit-de/issues)
- [GitHub Discussions](https://github.com/FutureRootsDE/legal-audit-de/discussions)
- [GitHub Wiki](https://github.com/FutureRootsDE/legal-audit-de/wiki)

## Lizenz

[MIT License](LICENSE) — mit Haftungs-Disclaimer (siehe LICENSE-Datei).
