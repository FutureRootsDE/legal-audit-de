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

## `/legal-client-test`

Website-CheckUp fuer Agenturen und Freelancer. Prueft eine oeffentliche Website passiv und erzeugt einen Report mit dem eigenen Briefkopf.

```text
/legal-client-test https://kunde.example [--edit-profile] [--out=<ordner>] [--no-pdf]
```

Ablauf:

1. **Briefkopf-Profil:** Beim ersten Aufruf werden Name, Anschrift und Kontakt der Agentur erfasst und lokal gespeichert (`--edit-profile` erfasst neu).
2. **Intake:** Kurze Fragen zur Website (Angebot an Verbraucherinnen und Verbraucher, Pflicht nach dem Barrierefreiheitsstaerkungsgesetz, Online-Shop, Abo- oder Mitgliedschaftsvertraege, mehr als zehn Beschaeftigte, Haltbarkeitsgarantie des Herstellers ueber mehr als 2 Jahre, Funktionen fuer Inhalte von Nutzern, Chat), danach legt das Skript fest, welche Tests anwendbar sind.
3. **Passive Pruefung** ueber chrome-devtools-mcp: Consent und Cookiebanner, Drittanbieter vor Einwilligung, Sicherheitsheader, Barrierefreiheit, Pflichtangaben. Nicht geprueft werden Speed, SEO und GEO.
4. **Report:** `report.html` als eigenstaendige Datei plus getaggtes PDF ueber headless Chrome oder Edge (`--no-pdf` laesst das PDF aus).

**Skriptaufrufe:** Der Befehl gibt die Shell nicht vorab frei. Claude Code fragt vor jedem Skriptaufruf nach; erlaube nur Aufrufe von client-test.py. Unter Codex CLI und GitHub Copilot CLI gibt es kein vorab freigegebenes Shell-Werkzeug mehr; wie sich der Befehl dort verhaelt, ist ungeprueft.

Ausgabe: ein Unterordner von `client-reports/` im Arbeitsverzeichnis (oder von `--out`) mit `findings.json`, `report.html`, PDF samt Kopie fuer den Versand und `evidence/`.

Die Pruefkriterien stehen im Katalog `templates/client-test/catalog.json` (Version 1, 56 Tests). Rechtsgrundlagen stammen ausschliesslich aus diesem Katalog. Jeder Befund nennt Tatsachen und die betroffene Vorschrift zur Pruefung; bei jedem nicht bestandenen Test steht der Hinweis auf eine anwaltliche Pruefung, der Report enthaelt einen Weitergabe-Satz und einen Start-Hinweis.

**Kundendaten:** Der Ordner `client-reports/` enthaelt Daten Dritter (Screenshots, Netzwerk-Logs). Nicht committen und nur an die Auftraggeberin oder den Auftraggeber weitergeben; `init` weist darauf hin, wenn `client-reports/` nicht in `.gitignore` steht.

**Keine Rechtsberatung:** Der Report ist eine KI-gestuetzte technische Ersteinschaetzung und keine Rechtsberatung im Sinne des § 2 RDG. Eine abschliessende Pruefung durch eine zugelassene Fachanwaeltin oder einen zugelassenen Fachanwalt fuer IT-Recht ist erforderlich.

Voraussetzungen und Grenzen: `chrome-devtools-mcp` (Werkzeugpraefix `mcp__plugin_chrome-devtools-mcp_chrome-devtools__*` oder `mcp__chrome-devtools__*`); PDF nur mit installiertem Chrome oder Edge; keine Seitenzahlen im Inhaltsverzeichnis (Spike-Ergebnis: kein Paged.js); unter Copilot laeuft der Befehl nur, wenn das Plugin-Repo selbst der Workspace ist (`${CLAUDE_PLUGIN_ROOT}` wird dort auf `${GITHUB_WORKSPACE}` abgebildet).

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
/legal-update --stale-only        # nur KB-Dateien, deren Verifikation (verifiziert-am, ersatzweise aktualisiert) 90 Tage oder aelter ist
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
| `legal-status.py` | Status-Report (Quelle fuer `/legal-status`; `--verbose`, `--json`); Frische nach `verifiziert-am` (ersatzweise `aktualisiert`), `teilverifiziert-am` als eigener Zustand |
| `audit-compare.py` | Diff zwischen zwei Audits, `--auto <pfad>` findet das vorherige automatisch |
| `find-placeholders.py` | (`--json`, `--group-by-file`) Listet alle `<<VERIFIKATION AUSSTEHEND>>`- und `<<UNVERIFIZIERT>>`-Stellen; abweichende oder defekte Marker werden als WARNUNG auf stderr gemeldet (Exit 0) |
| `legal-audit-pdf.py` | HTML/PDF-Briefing aus einem Audit-Ordner |
| `legal-audit-pro-mode.py` | Pro-Mode-Marker setzen, loeschen, abfragen |
| `verify-citations.py` | Prueft Aktenzeichen der KB: Bundesgerichte gegen die Rechtsinformations-API des Bundes, EuGH/EuG gegen den Cellar des Amts fuer Veroeffentlichungen (Status `PENDING` fuer anhaengige Verfahren, `name_hint` nur als Hinweis; `--no-eu` schaltet ab). Eigener Modus `--check-norms`: Normzitate gegen gesetze-im-internet.de (Paragraph, Ueberschrift, Absatz, Stand) und BGBl.-Fundstellen gegen recht.bund.de (`--max-bgbl N`, 30 Sekunden Abstand laut robots.txt). Je Zitat zeigen `checked`/`unchecked` (JSON) bzw. `[nicht geprueft: ...]` (Text), was verglichen wurde; Grenzen: Nr. und lit. werden nie geprueft, Saetze nur bei eindeutiger Zuordnung zur Absatzmarke, Absaetze mit Buchstaben (2a) nur gegen vorhandene Absatzmarken. Gesetzesdaten aus dem Cache sind als "Quelle: Cache (ungeprueft)" gekennzeichnet; `--strict` gibt Exit 1 bei DATE_MISMATCH, mit `--check-norms` bei NORM_MISSING, ABSATZ_MISSING oder BGBL_MISSING. Optional, nur Standardbibliothek; `--path`, `--only-pending`, `--json`, `--offline`, `--today YYYY-MM-DD`, `--write-ecli --dry-run` (auch EU-ECLI). Tempo und Cache: `--rate`, `--eu-rate`, `--norm-rate` (Anfragen pro Sekunde), `--timeout`, `--no-cache`, `--cache-dir`, `--cache-ttl-days` (Standard 7) |
| `sync-pro-variants.py` | `-pro`-Agentenvarianten deterministisch aus den 1M-Varianten generieren |
| `client-test.py` | Einstieg fuer `/legal-client-test` (Unterbefehle `check`, `profile`, `tempfile`, `init`, `plan`, `render`, `pdf`; `tempfile` gibt einen Pfad im Temp-Ordner des Plugins fuer die Profildaten aus, `profile save --consume` loescht die Datei danach; Bibliothek `client_report/`, nur Standardbibliothek) |
| `sync-platforms.py` | Codex- und Copilot-Adapter aus `.claude/` portieren |
