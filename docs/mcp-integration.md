---
title: MCP-Integration
layout: default
nav_order: 5
description: "Optionaler rechtsinformationen-bund-de-mcp-Server fuer strukturierten ELI/ECLI-Zugriff statt HTML-Scraping"
---

# MCP-Integration
{: .no_toc }

## Inhalt
{: .no_toc .text-delta }

1. TOC
{:toc}

---

{: .note }
> **Optional, kein Pflicht-Setup.** Das Plugin funktioniert ohne den hier beschriebenen MCP-Server vollwertig. Wer ihn registriert, bekommt strukturierten Zugriff auf das offizielle Bundes-Rechtsportal mit kanonischen ELI/ECLI-Identifiern statt HTML-Scraping ueber `WebFetch`.

## Worum es geht

Der `legal-researcher`-Agent verifiziert jedes Zitat gegen eine Tier-1-Primaerquelle. Standardmaessig macht er das per `WebFetch` gegen `gesetze-im-internet.de`, `eur-lex.europa.eu`, `rechtsprechung-im-internet.de` und `curia.europa.eu`.

Mit dem MCP-Server [`wolfgangihloff/rechtsinformationen-bund-de-mcp`](https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp) bekommt der Agent zusaetzlich strukturierten Zugriff auf das offizielle Portal `rechtsinformationen.bund.de` (NeuRIS) mit:

- semantischer Volltext-Suche ueber DE-Gesetze und DE-Rechtsprechung,
- kanonischen Identifiern nach ELI (European Legislation Identifier) und ECLI (European Case Law Identifier),
- JSON-Response statt HTML-Parse.

Bei verbundenem Server taucht in seinem Toolset der Praefix `mcp__rechtsinformationen__*` auf. Der Agent erkennt das und bevorzugt diese Tools fuer DE-Recht. Fehlt der Server, laeuft der bisherige Workflow unveraendert.

## Warum kein Auto-Install

Drei Gruende:

1. **Eigenes Lifecycle.** Der Server wird vom Drittautor `wolfgangihloff` gepflegt. Wir wollen seinen Update-Pfad nicht in unseren forken.
2. **Test-API.** Die zugrundeliegende API `https://testphase.rechtsinformationen.bund.de/v1` ist explizit als "Trial service — may be subject to changes" markiert. Breaking Changes moeglich.
3. **Lokaler Build noetig.** Der Server liegt nicht offiziell auf npm. Auf npm existiert ein Drittanbieter-Wrapper `@iflow-mcp/wolfgangihloff-rechtsinformationen`, der aber Single-Maintainer mit ca. 23 monatlichen Downloads ist. Supply-Chain-Risiko nicht zumutbar in einem rechts-relevanten Tooling-Stack.

Konsequenz: das Plugin liefert nur ein Template plus Dokumentation. Die Entscheidung, den Server zu installieren und zu registrieren, liegt bei dir.

## Installation

### Variante A — Upstream-Build (empfohlen)

```bash
cd ~/tools                      # irgendwo lokal, NICHT in deinem Audit-Projekt
git clone https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp.git
cd rechtsinformationen-bund-de-mcp
npm install
npm run build
ls dist/index.js                # muss vorhanden sein
```

Voraussetzung: Node.js ab Version 18.

### Variante B — npm-Wrapper (mit Vorbehalt)

```bash
npx -y @iflow-mcp/wolfgangihloff-rechtsinformationen
```

Pruefe vorher, ob dir der Drittautor und die Download-Zahlen ausreichen. Bei Zweifel Variante A.

### Variante C — gar nicht

Plugin funktioniert weiter, `legal-researcher` macht WebFetch wie gehabt.

## Registrierung

### Projekt-Scope (empfohlen fuer einzelne Audits)

```bash
cp $(claude config plugin-root legal-audit-de)/templates/mcp/rechtsinformationen.mcp.json.example \
   /pfad/zu/deinem-audit-ziel/.mcp.json
```

Anschliessend in der Datei den Platzhalter-Pfad durch den realen `dist/index.js`-Pfad ersetzen.

Claude Code fragt beim naechsten Start nach `Approve project MCP server?`.

### User-weit (alle Projekte)

```bash
claude mcp add --transport stdio rechtsinformationen \
  -- node /absoluter/pfad/zu/rechtsinformationen-bund-de-mcp/dist/index.js
```

### Plugin-weit

**Nicht empfohlen.** Wuerde fuer jeden User fehlschlagen, der den Upstream-Server nicht installiert hat. Daher liegt das Template bewusst nur unter `templates/mcp/` und nicht als `.mcp.json` im Plugin-Root.

## Wie der Agent es nutzt

Beim Verifikations-Protokoll praeferiert `legal-researcher` MCP-Tools nach dieser Tabelle:

| Vorgang | Mit MCP (bevorzugt) | Fallback (ohne MCP) |
|---------|---------------------|---------------------|
| Paragraphen-Suche | `mcp__rechtsinformationen__semantische_rechtssuche` | WebFetch auf `gesetze-im-internet.de` |
| Volltext per ELI | `mcp__rechtsinformationen__gesetz_per_eli_abrufen` | WebFetch auf `eur-lex.europa.eu` |
| Aktenzeichen-Suche | `mcp__rechtsinformationen__rechtsprechung_suchen` mit `court`-Filter | WebSearch `"<AZ>" site:rechtsprechung-im-internet.de` |
| Volltext-Urteil | `mcp__rechtsinformationen__dokument_details_abrufen` | WebFetch auf Entscheidungs-URL |

Anti-Fallen:

- Bei **historischen Fassungen** und **Aenderungsgesetzen** (z. B. TMG zu DDG, TTDSG zu TDDDG) ist der MCP-Index schwach. Der Agent prueft zusaetzlich per WebFetch gegen `gesetze-im-internet.de`.
- Bei **leerer oder Schema-inkonsistenter Response** faellt der Agent automatisch auf WebFetch zurueck. Kein harter Fehler.
- Jeder MCP-Treffer muss `eli` oder `ecli` im Response-Objekt liefern. Ohne diesen Identifier gilt der Treffer als unzureichend belegt und der Agent macht eine zweite Verifikation per Tier-1-WebFetch.

## Funktionspruefung

In Claude Code:

```text
/mcp
```

Du solltest `rechtsinformationen` mit sechs Tools im Status `connected` sehen. Bei `pending approval` einmalig in einer interaktiven Session bestaetigen.

Schneller Funktionstest:

```text
Verifiziere Paragraph 7 Absatz 2 Nummer 2 UWG via MCP.
```

Der Agent ruft dann `mcp__rechtsinformationen__semantische_rechtssuche` auf statt WebFetch.

## ELI/ECLI im KB-Frontmatter

Seit der MCP-Integration unterstuetzt das KB-Frontmatter zwei optionale Felder:

```yaml
---
aktualisiert: 2026-06-19
quelle-primaer: https://eur-lex.europa.eu/eli/reg/2016/679/oj
verifiziert-am: 2026-06-19
geltungsbereich: [DE, EU]
eli: http://data.europa.eu/eli/reg/2016/679/oj
ecli: ECLI:EU:C:2020:559
---
```

Beide Felder sind nicht verpflichtend, aber bei Verfuegbarkeit bevorzugt — sie sind stabiler als URLs allein und werden vom MCP-Server kanonisch geliefert.

## Bekannte Limitationen

Aus der Upstream-Doku:

- Test-Phase-API: Antwortstrukturen koennen sich aendern.
- Aenderungsgesetze schwach indexiert.
- Historische Fassungen nur teilweise abrufbar.

Fuer diese drei Faelle laeuft der WebFetch-Fallback weiterhin verbindlich.

## Troubleshooting

| Symptom | Vermutung | Loesung |
|---------|-----------|---------|
| `/mcp` zeigt `Failed` | Pfad zu `dist/index.js` falsch | absoluten Pfad pruefen, neu starten |
| `/mcp` zeigt `Pending approval` | erste Verwendung | interaktive Session starten und freigeben |
| Agent ruft trotzdem WebFetch auf | Tool nicht im Subagent-Toolset | normal — der Agent prueft Verfuegbarkeit zur Laufzeit |
| `Cannot find module 'dist/index.js'` | Build nicht durchgelaufen | `npm install && npm run build` im Upstream-Repo wiederholen |
| Antwort enthaelt kein `eli`/`ecli` | testphase-API noch nicht stabil | Agent macht automatisch Tier-1-Fallback |

## Quellen

- [`wolfgangihloff/rechtsinformationen-bund-de-mcp`](https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp) — Upstream-Server
- [`rechtsinformationen.bund.de`](https://docs.rechtsinformationen.bund.de) — API-Dokumentation
- [ELI-Standard](http://publications.europa.eu/eli)
- [ECLI-Standard](https://e-justice.europa.eu/ecli)
- [Claude Code MCP-Doku](https://code.claude.com/docs/en/mcp)
- Setup-Template im Repo: [`templates/mcp/README.md`](https://github.com/FutureRootsDE/legal-audit-de/blob/main/templates/mcp/README.md)
