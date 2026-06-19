---
title: Commands
layout: default
nav_order: 3
description: "Alle Slash-Befehle mit Optionen und Beispiel-Aufrufen"
---

# Commands
{: .no_toc }

## Inhalt
{: .no_toc .text-delta }

1. TOC
{:toc}

---

{: .note }
> Alle Commands sind in Claude Code als Slash-Befehle verfuegbar. Codex- und Copilot-Adapter liegen unter `.codex/prompts/` bzw. `.github/prompts/` und werden in den jeweiligen CLIs identisch aufgerufen.

## `/legal-audit`

Vollstaendiger Rechts-Audit einer Codebase. Erzeugt `docs/legal-audit/LegalAudit.md` mit klassifizierten Findings, `SUMMARY.md` als Management-Kurzfassung und einen `clean/`-Ordner mit lupenreinen Korrektur-Versionen pro Finding.

```text
/legal-audit /pfad/zum/projekt
```

Optionen:

| Flag | Wirkung |
|------|---------|
| `--compare` | Diff-Report gegen das letzte Audit aus dem `audits/`-Schatten-Archiv |
| `--pdf` | Erzeugt zusaetzlich `anwalts-briefing.html` und (falls `pandoc` vorhanden) PDF |

Output-Struktur im Zielprojekt:

```text
<zielprojekt>/docs/legal-audit/
├── LegalAudit.md
├── SUMMARY.md
├── clean/
│   └── F-NNN-<slug>.md
└── evidence/
```

Parallel landet eine Schatten-Kopie unter `${CLAUDE_PROJECT_DIR}/audits/<projekt>-<timestamp>/`. Begruendung: Nachweis-Kette fuer die DSGVO-Rechenschaftspflicht aus Artikel 5 Absatz 2.

## `/legal-audit-live`

Live-Browser-Check einer oeffentlichen URL. Pruefkriterien:

- Welche Drittanbieter-Requests laufen vor dem ersten Consent-Klick?
- Wird Google Fonts trotz Self-Hosting-Behauptung nachgeladen?
- Hat der Cookie-Banner einen gleichwertigen Ablehnen-Button (Stichwort BGH Planet49)?
- Welche Cookies werden ohne Consent gesetzt?

```text
/legal-audit-live https://deine-domain.de
```

Setzt `chrome-devtools-mcp` voraus. Setup unter [Setup](setup#optional-chrome-devtools-mcp-fuer-live-browser-checks).

## `/legal-doc-check`

Einzeldokument-Pruefung. Funktioniert ohne Codebase-Kontext, ideal fuer schnelle Rechtstext-Reviews.

```text
/legal-doc-check /pfad/zur/agb.md
```

Erkannte Dokumenttypen: AGB, Datenschutzerklaerung, Impressum, Widerrufsbelehrung, Cookie-Richtlinie, Social-Media-Bio.

Output: Finding-Liste plus Clean-Version mit Disclaimer-Block.

## `/legal-kb`

Laedt einen einzelnen KB-Artikel gezielt in den Kontext, um Folgefragen direkt damit beantworten zu lassen.

```text
/legal-kb cookie-consent
/legal-kb urteile/eugh-schrems-ii
/legal-kb gesetze/dsgvo
```

Die verfuegbaren Slugs stehen in `knowledge/INDEX.md`.

## `/legal-verify`

Empfiehlt Fachanwaelte, spezialisierte Kanzleien und Verifikations-Tools zu einem Thema.

```text
/legal-verify cookie-consent
/legal-verify ai-act
/legal-verify barrierefreiheit
```

Wichtig: das Plugin verifiziert die Empfehlungen halbjaehrlich gegen Primaerquellen (`/legal-update anwaelte-tools`), aber sie sind redaktionell, keine garantierte Eignung.

## `/legal-update`

Aktualisiert die Knowledge Base gegen Primaerquellen.

```text
/legal-update                     # interaktive Auswahl
/legal-update tdddg               # einzelnen Artikel updaten
/legal-update --stale-only        # nur KB-Dateien aelter als 90 Tage
/legal-update --all               # komplette Tier-1-Re-Verifikation
/legal-update --fix-pending       # Platzhalter <<VERIFIKATION AUSSTEHEND>> aufloesen
```

Der `legal-researcher`-Agent verifiziert dabei jedes Zitat gegen `eur-lex.europa.eu`, `gesetze-im-internet.de`, `rechtsprechung-im-internet.de` oder `curia.europa.eu`. Wenn der `rechtsinformationen`-MCP-Server registriert ist, bevorzugt der Agent dessen ELI/ECLI-Tools. Details unter [MCP-Integration](mcp-integration).

Log: `.claude/logs/zitate-verifikation-<YYYY-MM-DD>.log`.

## `/legal-audit-de-update`

Plugin und Knowledge Base gemeinsam aktualisieren.

```text
/legal-audit-de-update                # beide aktualisieren
/legal-audit-de-update --plugin-only  # nur Marketplace-Refresh
/legal-audit-de-update --kb-only      # nur Primaerquellen-Verifikation
/legal-audit-de-update --dry-run      # Vorschau, keine Aenderungen
```

## `/legal-status`

Plugin-Gesundheits-Report.

```text
/legal-status              # menschenlesbar
/legal-status --verbose    # Detail-Output
/legal-status --json       # maschinenlesbar
```

Liefert KB-Aktualitaet, Platzhalter-Zaehler, Hook-Status, Audit-Historie und den aktuellen Pro-Mode-Stand.

## `/legal-pro-mode`

Toggle fuer Claude-Pro-Abonnenten ohne 1M-Zugriff.

```text
/legal-pro-mode enable
/legal-pro-mode disable
/legal-pro-mode status
```

Details unter [Setup](setup#pro-mode-fuer-claude-pro-abonnenten).

## Severity-Matrix

Jedes Finding bekommt einen von vier Schweregraden:

| Level | Kriterium |
|-------|-----------|
| **CRIT** | Aktuelle Abmahnwelle, Bussgeld ueber 10 Kilo moeglich, strafrechtlich relevant |
| **HIGH** | Dokumentierte Abmahnfaelle, Unterlassungsanspruch |
| **MED** | Formale Pflichtverletzung, Einzelanspruch moeglich |
| **LOW** | Best-Practice-Verstoss |

Grundsatz: im Zweifel eine Stufe hoeher klassifizieren. Abmahnkosten sind asymmetrisch.

## Hilfsskripte unter `scripts/`

| Skript | Zweck |
|--------|-------|
| `legal-status.py` | Status-Report (Quelle fuer `/legal-status`) |
| `audit-compare.py` | Diff zwischen zwei Audits, `--auto <pfad>` findet das vorherige automatisch |
| `find-placeholders.py` | Listet alle `<<VERIFIKATION AUSSTEHEND>>`- und `<<UNVERIFIZIERT>>`-Stellen |
| `legal-audit-pdf.py` | HTML/PDF-Briefing aus einem Audit-Ordner |
| `legal-audit-pro-mode.py` | Pro-Mode-Marker setzen, loeschen, abfragen |
| `sync-pro-variants.py` | `-pro`-Agentenvarianten deterministisch aus den 1M-Varianten generieren |
| `sync-platforms.py` | Codex- und Copilot-Adapter aus `.claude/` portieren |
