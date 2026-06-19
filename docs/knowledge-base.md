---
title: Knowledge Base
layout: default
nav_order: 4
description: "Aufbau der Knowledge Base, abgedeckte Gesetze, Urteile, Themen und Checklisten"
---

# Knowledge Base
{: .no_toc }

## Inhalt
{: .no_toc .text-delta }

1. TOC
{:toc}

---

{: .warning }
> **Disclaimer.** Saemtliche KB-Inhalte sind technische Vorarbeit fuer eine anwaltliche Pruefung. Keine Rechtsberatung im Sinne des Paragraph 2 RDG. Stand und Verifikationsdatum stehen im YAML-Frontmatter jeder Datei.

## Warum eine KB statt blossem LLM-Wissen

Sprachmodelle haben einen Trainings-Cutoff. Rechtsvorschriften aendern sich danach, und Trainingsdaten enthalten Fach-Einordnungen, die oft mit Primaerquellen kollidieren. Beispiel aus der eigenen Geschichte: die initiale KB des Plugins hatte sechs schwere Aktenzeichen-Fehler ("Inbox-Werbung II = I ZR 186/17" war falsch, korrekt ist I ZR 25/19) und einen erfundenen Paragraph 7 Absatz 4 UWG. Lehre: jede KI-generierte Rechts-KB muss gegen Tier-1-Primaerquellen re-verifiziert werden, bevor sie produktiv eingesetzt wird.

Die KB liegt deshalb als Markdown-Vault im Repo. Jede Datei hat YAML-Frontmatter mit Quelle, Aktualisierungsdatum und Verifikationsdatum. Der `legal-researcher`-Agent re-verifiziert auf Anforderung gegen Primaerquellen.

## Quellen-Hierarchie

Verbindlich fuer jede Zitat-Verifikation.

### Tier 1 — Primaerquellen

| Domain | Zustaendig fuer |
|--------|-----------------|
| `eur-lex.europa.eu` | EU-Primaerrecht, CELEX, konsolidierte Fassungen |
| `gesetze-im-internet.de` | DE-Gesetze, BMJ-offiziell |
| `rechtsprechung-im-internet.de` | DE-Rechtsprechung |
| `curia.europa.eu` | EuGH |
| `bundesanzeiger.de` | Verordnungen |

### Tier 2 — Amtliche Sekundaerquellen

`bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, Landesdatenschutz-Behoerden, `bsi.bund.de`.

### Tier 3 — Fach-Einordnungen (nie als Zitat-Grundlage)

`dr-schwenke.de`, `haerting.de`, `datenschutz-notizen.de`, `e-recht24.de`, `it-recht-kanzlei.de`. Diese Quellen liefern Kontext und Diskussion, aber jede Aussage muss ueber Tier 1 belegbar sein, bevor sie in einen Audit-Output uebernommen wird.

## Aufbau

```text
knowledge/
├── INDEX.md                # einzige immer-geladene Datei
├── gesetze/                # Vollabdeckung des Scope
├── themen/                 # quer-laufende Compliance-Themen
├── urteile/                # Schluessel-Rechtsprechung
├── behoerden/              # Aufsichts-Leitlinien
├── checklisten/            # Audit-Checklisten pro Codebase-Typ
└── anwaelte-tools/         # Verifikations-Empfehlungen
```

## Abgedeckte Gesetze

| Gesetz | Slug | Geltungsbereich |
|--------|------|-----------------|
| DSGVO | `gesetze/dsgvo` | EU |
| BDSG | `gesetze/bdsg` | DE |
| TDDDG | `gesetze/tdddg` | DE |
| UWG | `gesetze/uwg` | DE |
| PAngV | `gesetze/pangv` | DE |
| BGB/AGB | `gesetze/bgb-agb` | DE |
| DDG | `gesetze/ddg` | DE |
| DSA | `gesetze/dsa` | EU |
| DMA | `gesetze/dma` | EU |
| AI Act | `gesetze/ai-act` | EU |
| BFSG | `gesetze/bfsg` | DE |
| UrhG | `gesetze/urhg` | DE |
| MarkenG | `gesetze/markeng` | DE |
| NIS2-BSIG | `gesetze/nis2-bsig` | DE/EU |

## Themen-Cluster

Quer-laufende Compliance-Themen, die mehrere Gesetze beruehren:

- Cookie-Consent und Tracking
- Datenschutzerklaerung, Impressum, AGB
- Widerrufsbelehrung, Button-Loesung
- Newsletter und Inbox-Werbung
- Drittland-Transfer, AVV-Muster, Verarbeitungsverzeichnis, TOM
- DSFA, KI-Transparenz, KI-Content-Kennzeichnung
- Barrierefreiheit (BFSG), Werbekennzeichnung, Preisangaben
- Stockfoto, Fotos Dritter (KUG)
- Datenpannen-Meldepflicht, Social-Media-Datenschutz
- Siegel-Werbung, Zitatrecht, Tool-Katalog (80+ Tools)

## Schluessel-Urteile

EuGH:

- **Schrems II** (C-311/18) — Drittland-Transfer ohne Angemessenheits-Beschluss
- **Planet49** (C-673/17) — wirksame Cookie-Einwilligung
- **Fashion ID** (C-40/17) — gemeinsame Verantwortlichkeit fuer Social-Plugins
- **Meta gegen Bundeskartellamt** (C-252/21) — kartellrechtliche Datenschutz-Pruefung
- **IAB Europe / TCF** (C-604/22) — TCF-String als personenbezogenes Datum

BGH:

- **Cookie-Einwilligung I** (I ZR 7/16, fortgefuehrt nach Planet49)
- **Inbox-Werbung II** (I ZR 25/19)

LG Muenchen I:

- **Google Fonts** (3 O 17493/20)

## Behoerden-Material

- **DSK** (Datenschutzkonferenz) — Beschluesse und Kurzpapiere
- **EDSA** (European Data Protection Board) — Guidelines, Recommendations
- **BfDI** — Bundes-Aufsicht
- Landes-Datenschutzbeauftragte (Bayern, NRW, Berlin u. a.)

## Checklisten pro Codebase-Typ

| Marker im Projekt | Checkliste |
|-------------------|------------|
| `package.json` mit `next` | `checklisten/audit-saas` |
| `package.json` mit `astro`, reines HTML | `checklisten/audit-landingpage` |
| `*.workflow.json`, n8n-Export | `checklisten/audit-n8n` |
| `woocommerce`, `shopify`, Stripe-Checkout | `checklisten/audit-ecommerce` |
| ueberwiegend `.md` mit `content/` | `checklisten/audit-content-blog` |
| unklar | `checklisten/general-pre-launch` |

Der `legal-auditor`-Agent erkennt den Codebase-Typ ueber die Marker und laedt die passende Checkliste.

## Frontmatter-Konvention

Jede KB-Datei beginnt mit YAML-Frontmatter:

```yaml
---
aktualisiert: 2026-05-08
quelle-primaer: https://eur-lex.europa.eu/eli/reg/2016/679/oj
quellen-sekundaer:
  - https://www.edpb.europa.eu/...
verifiziert-am: 2026-05-08
geltungsbereich: [DE, EU]
# Optional, bevorzugt wenn verfuegbar — stabile Identifier nach
# ELI (European Legislation Identifier) und ECLI (European Case Law Identifier):
eli: http://data.europa.eu/eli/reg/2016/679/oj
ecli: ECLI:EU:C:2020:559
---
```

Die optionalen `eli`- und `ecli`-Felder ueberleben URL-Reshuffles der Portale und sind die bevorzugte Referenz, wenn der [MCP-Server](mcp-integration) `rechtsinformationen` aktiv ist.

## Kontext-Management

Die 63 KB-Dateien werden **nicht** in jede Claude-Session geladen. Stattdessen:

- `SessionStart`-Hook laedt nur `knowledge/INDEX.md` (ca. 1.000 Tokens)
- `UserPromptSubmit`-Hook matcht den User-Prompt gegen Regex-Trigger in `.claude/hooks/triggers.json` und laedt bis zu drei passende Chunks als `additionalContext`
- Codex und Copilot haben keine Hooks, dort uebernehmen die Skills das Routing per Auto-Routing-Block

Trigger-Beispiele:

| Schlagwort | geladene Chunks |
|------------|-----------------|
| `cookie`, `consent` | `themen/cookie-consent` |
| `drittland`, `schrems` | `themen/drittland-transfer`, `urteile/eugh-schrems-ii` |
| `ai.act`, `ki.vo` | `themen/ki-transparenz`, `gesetze/ai-act` |
| `impressum`, `tmg` | `themen/impressum`, `gesetze/ddg` |

Vollstaendiger Trigger-Katalog: `.claude/hooks/triggers.json`.

## KB-Wartung

Alle 90 Tage `/legal-update --stale-only` ausfuehren. Halbjaehrlich `/legal-update anwaelte-tools`, weil sich Fachanwalts-Profile und Tool-Landschaft langsamer aendern.

Wenn `aktualisiert` und `verifiziert-am` mehr als 180 Tage zurueckliegen, markiert `/legal-status` die Datei als "sehr stale" und schlaegt `/legal-update --fix-pending` vor.
