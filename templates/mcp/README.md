# Optionale MCP-Integration: `rechtsinformationen-bund-de-mcp`

> **TL;DR:** Wenn du das Plugin produktiv fuer Zitat-Verifikation nutzt, kannst du
> zusaetzlich den MCP-Server `wolfgangihloff/rechtsinformationen-bund-de-mcp`
> registrieren. Der `legal-researcher`-Agent erkennt ihn automatisch und nutzt
> strukturierte ELI/ECLI-Calls statt HTML-Scraping per WebFetch. **Opt-in, kein
> Auto-Load.** Das Plugin funktioniert ohne den Server vollwertig weiter.

---

## Warum optional?

Der MCP-Server ist ein eigenstaendiges Node.js-Projekt, das nicht zum Plugin
gehoert. Wir bundlen ihn nicht aus drei Gruenden:

1. **Eigenes Lifecycle:** Der Server wird vom Drittautor (`wolfgangihloff`)
   gepflegt. Wir wollen seinen Update-Pfad nicht in unseren forken.
2. **Test-API:** Die zugrundeliegende API
   `https://testphase.rechtsinformationen.bund.de/v1` ist explizit als
   "Trial service — may be subject to changes" markiert. Breaking-Changes
   moeglich.
3. **Lokaler Build noetig:** Der Server ist auf npm nur als Drittanbieter-Wrapper
   verfuegbar (`@iflow-mcp/wolfgangihloff-rechtsinformationen`); der offizielle
   Weg ist `git clone` + `npm install` + `npm run build`. Das soll der User
   bewusst entscheiden.

## Was du davon hast

Mit aktivem MCP-Server bevorzugt `legal-researcher`:

- `mcp__rechtsinformationen__semantische_rechtssuche` statt WebFetch + HTML-Parse
- `mcp__rechtsinformationen__gesetz_per_eli_abrufen` mit kanonischer ELI-URI
- `mcp__rechtsinformationen__rechtsprechung_suchen` mit `court`-Filter (BGH,
  BVerfG, BAG, BFH, BSG, BVerwG)
- `mcp__rechtsinformationen__dokument_details_abrufen` fuer Volltext

Konkrete Vorteile:

- **ELI/ECLI** statt fragiler URL: Identifier sind stabil ueber Re-Releases
  des Portals hinweg.
- **JSON-Response** statt HTML: weniger Parse-Fehler.
- **Eine semantische Suche** statt mehrerer URL-Konstruktionen.

Ohne MCP-Server faellt `legal-researcher` automatisch auf `WebFetch` gegen
`gesetze-im-internet.de`, `eur-lex.europa.eu`, `rechtsprechung-im-internet.de`
und `curia.europa.eu` zurueck — also die bisherige Logik.

## Installation (drei Optionen)

### Option A — Upstream Git-Repo (empfohlen)

```bash
# Irgendwo lokal auschecken (NICHT in dein Audit-Projekt)
cd ~/tools
git clone https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp.git
cd rechtsinformationen-bund-de-mcp
npm install
npm run build

# Pruefe, dass dist/index.js entstanden ist
ls dist/index.js
```

### Option B — Third-Party npm Wrapper

Es existiert ein Drittanbieter-Wrapper auf npm
(`@iflow-mcp/wolfgangihloff-rechtsinformationen`). Aktuell sehr geringe
Verbreitung (Stand 2026-06: ca. 23 monatliche Downloads), Single-Maintainer.
**Supply-Chain-Risiko abschaetzen**, bevor du das nutzt.

Wenn du dich dafuer entscheidest:

```bash
npx -y @iflow-mcp/wolfgangihloff-rechtsinformationen
```

Beispiel `.mcp.json`-Eintrag:

```json
{
  "mcpServers": {
    "rechtsinformationen": {
      "command": "npx",
      "args": ["-y", "@iflow-mcp/wolfgangihloff-rechtsinformationen"]
    }
  }
}
```

### Option C — Gar nicht

Funktioniert weiter wie vorher. `legal-researcher` macht `WebFetch` auf die
Tier-1-Quellen. Keine Aktion noetig.

## Registrierung (drei Scopes)

Du hast drei Scopes zur Wahl. Reihenfolge nach Empfehlung:

### 1. Pro Projekt (`.mcp.json` im Audit-Projekt)

Pruefst du nur **dieses eine Projekt** mit MCP-Beschleunigung? Dann in das
Audit-Ziel-Repo:

```bash
cp /pfad/zu/legal-audit-de/templates/mcp/rechtsinformationen.mcp.json.example \
   /pfad/zu/deinem-audit-ziel/.mcp.json
# Pfad in der Datei anpassen (siehe unten)
```

Claude Code fragt beim naechsten Start nach `Approve project MCP server?`.

### 2. User-weit (`~/.claude.json`)

Willst du den Server fuer **alle** Projekte? Eintrag in `~/.claude.json` unter
`mcpServers`. Einfacher per CLI:

```bash
claude mcp add --transport stdio rechtsinformationen \
  -- node /ABSOLUTER/PFAD/zu/rechtsinformationen-bund-de-mcp/dist/index.js
```

### 3. Direkt im Plugin (`.mcp.json` im Plugin-Root)

**Nicht empfohlen.** Wir koennten `.mcp.json` direkt in dieses Plugin legen,
dann wuerde Claude Code den Server beim Plugin-Enable starten. Das wuerde aber
fuer alle User fehlschlagen, die den Upstream-Server nicht installiert haben.
Daher ist der Plugin-Root bewusst MCP-frei.

## Pfad-Anpassung

Im Template steht `/ABSOLUTER/PFAD/zu/rechtsinformationen-bund-de-mcp/dist/index.js`.
Ersetze das mit dem realen Pfad. Beispiel auf macOS:

```json
{
  "mcpServers": {
    "rechtsinformationen": {
      "command": "node",
      "args": ["/Users/du/tools/rechtsinformationen-bund-de-mcp/dist/index.js"]
    }
  }
}
```

Relative Pfade funktionieren in stdio-Configs unzuverlaessig. Nimm absolute.

## Pruefen, dass es laeuft

In Claude Code:

```
/mcp
```

Du solltest `rechtsinformationen` mit der Anzahl seiner Tools (sechs) sehen.
Im Status `connected`. Bei `pending approval` bestaetige einmalig in der
naechsten interaktiven Session.

Schneller Funktionstest:

```
Frage: "Verifiziere § 7 Abs. 2 Nr. 2 UWG via MCP."
```

Der Agent sollte `mcp__rechtsinformationen__semantische_rechtssuche` aufrufen
statt `WebFetch` auf `gesetze-im-internet.de`.

## Bekannte Limitationen

Direkt aus der Upstream-Doku des MCP-Servers:

- **Test-Phase-API:** Antwortstrukturen koennen sich aendern.
- **Aenderungsgesetze schwach indexiert:** Bei aelteren Aenderungs-Aktenzeichen
  ist die semantische Suche manchmal unscharf.
- **Historische Fassungen nur teilweise:** Aktuelle konsolidierte Fassungen
  sind primaer abrufbar; aeltere Versionen nicht durchgaengig.

Fuer historische Fassungen oder Aenderungsgesetze faellt der Agent
explizit auf WebFetch gegen `gesetze-im-internet.de` und `eur-lex.europa.eu`
zurueck. Die Tier-1-Hierarchie bleibt unveraendert verbindlich.

## Wenn etwas schief geht

| Symptom | Vermutung | Loesung |
|---------|-----------|---------|
| `/mcp` zeigt `Failed` | Pfad zu `dist/index.js` falsch | absoluten Pfad pruefen |
| `/mcp` zeigt `Pending approval` | erste Verwendung | interaktive Session starten, "Approve" |
| Agent ruft trotzdem WebFetch auf | Tool nicht im Agent-Toolset | normal — siehe naechster Punkt |
| Tool-Liste in Agent unbekannt | Subagent-Tool-Liste ist statisch | der Agent prueft den Toolset zur Laufzeit; ohne MCP-Match laeuft der Fallback |

## Quellen

- Upstream Server: <https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp>
- API-Doku: <https://docs.rechtsinformationen.bund.de>
- ELI-Standard: <http://publications.europa.eu/eli>
- ECLI-Standard: <https://e-justice.europa.eu/ecli>
- Claude Code MCP-Doku: <https://code.claude.com/docs/en/mcp>
