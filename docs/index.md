---
title: Startseite
layout: default
nav_order: 1
description: "Multi-Plattform-Toolkit fuer DSGVO/TDDDG/UWG/AI-Act-Audits in Claude Code, Codex CLI und Copilot CLI"
permalink: /
---

# legal-audit-de
{: .fs-9 }

Multi-Plattform-Toolkit fuer **deutsche und EU-Rechts-Audits** von Codebases, Live-URLs und Rechtsdokumenten. Laeuft in **Claude Code**, **OpenAI Codex CLI** und **GitHub Copilot CLI**.
{: .fs-6 .fw-300 }

[Schnellstart fuer Claude Code](#schnellstart-claude-code){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHub](https://github.com/FutureRootsDE/legal-audit-de){: .btn .fs-5 .mb-4 .mb-md-0 }

---

{: .warning }
> **Keine Rechtsberatung.** Dieses Plugin erzeugt keine Rechtsberatung im Sinne des Paragraph 2 RDG. Alle Ausgaben dienen der technischen Vorbereitung einer anwaltlichen Pruefung. Eine abschliessende Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend erforderlich, bevor Inhalte produktiv gesetzt werden.

## Was es tut

`legal-audit-de` agiert wie ein IT- und Datenschutz-Fachaudit. Es analysiert Codebases, Live-Websites und einzelne Rechtsdokumente auf Verstoesse gegen deutsches und EU-Recht und liefert:

- **`LegalAudit.md`** mit Findings nach Severity (CRIT, HIGH, MED, LOW)
- **Clean-Versionen** der beanstandeten Passagen zum 1-zu-1-Einbau
- **Live-Browser-Checks** ueber `chrome-devtools-mcp` (Cookie-Banner, Google-Fonts-Leak, Pre-Consent-Tracker)
- **Einzeldokument-Reviews** (AGB, Datenschutzerklaerung, Impressum, Widerruf, Cookie-Richtlinie)

## Fuer wen es gemacht ist

Solo-Gruender, Indie-Hacker und kleine Teams, die im deutschen oder europaeischen Markt operieren und

- keine eigene Rechtsabteilung haben,
- vor der anwaltlichen Erstpruefung schon eine saubere Vorlage liefern wollen,
- die Abrechnung der Kanzlei auf das Wesentliche reduzieren wollen,
- mit KI-Tooling arbeiten und ein Werkzeug brauchen, das DE/EU-Spezifika kennt.

## Scope

In Scope: DSGVO, BDSG, TDDDG, UWG, PAngV, BGB/AGB, DDG, DSA, DMA, AI Act, BFSG, UrhG, MarkenG, NIS2-BSIG.

Out of Scope: Strafrecht, Arbeitsrecht, Steuerrecht (ausser HGB Paragraph 257 Retention), Gesellschaftsrecht, nicht-EU-Rechtsordnungen.

## Schnellstart Claude Code

```text
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

Dann im Workspace deines Zielprojekts:

```text
/legal-audit /pfad/zu/deinem-projekt
```

Du bekommst eine vollstaendige Audit-Mappe unter `docs/legal-audit/` mit Findings, Clean-Versionen und einem Anwalts-Briefing.

Codex CLI und Copilot CLI sind ebenfalls unterstuetzt. Details unter [Setup](setup).

## Architektur in einem Satz

Eine Knowledge Base mit 63 kuratierten Artikeln (Gesetze, Themen, Urteile, Behoerden-Leitlinien, Checklisten) wird **nicht** vollstaendig in die Session geladen, sondern ueber Hooks oder Auto-Routing nur dann gezogen, wenn die Aufgabe sie wirklich braucht. Damit bleibt das Kontextfenster schlank und das Rechtswissen trotzdem zur Hand.

## Naechste Schritte

- [Setup](setup) — Installation fuer alle drei CLIs, Vorraussetzungen, Pro-Mode-Toggle
- [Commands](commands) — alle Slash-Befehle mit Optionen und Beispielen
- [Knowledge Base](knowledge-base) — was die KB abdeckt und wie sie aufgebaut ist
- [MCP-Integration](mcp-integration) — optionaler `rechtsinformationen-bund-de-mcp`-Server fuer ELI/ECLI-Zugriff
- [Changelog](https://github.com/FutureRootsDE/legal-audit-de/blob/main/CHANGELOG.md) — alle Releases mit Begruendung

## Lizenz

MIT. Forks, kommerzielle Nutzung und Weiterentwicklung sind ausdruecklich erwuenscht.
