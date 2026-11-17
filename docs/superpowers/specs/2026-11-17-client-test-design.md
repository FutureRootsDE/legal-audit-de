# Design: Befehl `/legal-client-test` (Website-CheckUp-Report für Agenturen)

- **Stand:** 2026-11-17
- **Status:** Design entschieden, Bau offen. Dieses Dokument baut nichts; es ist die Grundlage für einen Implementierungsplan. Builder-Check vom 2026-11-17 eingearbeitet (Abschnitte 6.9 und 9).
- **Plugin-Basis:** legal-audit-de 1.4.3 (`origin/main` 1a51d48)
- **Kennzeichnung:** „**Entschieden**“ = vom Nutzer bestätigt; „**entschieden durch Nutzer, 2026-11-17**“ = am Tag des Builder-Checks (Abschnitt 9) entschieden. „**Call des Orchestrators, korrigierbar**“ = Festlegung ohne ausdrückliche Nutzerentscheidung. „**Vorschlag dieses Dokuments, korrigierbar**“ = beim Abgleich mit dem Ist-Stand ergänzt. „**Zu verifizieren**“ = Rechtsfakt, der in `knowledge/` nicht belegt ist; der Builder prüft ihn gegen die Primärquelle, bevor er in Katalog oder Texte geht.

> Internes Design-Dokument. Die hier skizzierten Report-Texte sind Entwürfe; jede Rechtsaussage im späteren Report ist eine KI-gestützte Einschätzung und keine Rechtsberatung im Sinne des § 2 RDG.

---

## 1. Intent und Warum

Ein neuer Befehl „Client Test“. Ausgelöst wird er von einer **Agentur oder einem Freelancer**. Der Report geht zuerst an diese Person und wird meist an deren **Kunden** weitergegeben. Eingaben:

1. Eigenes Firmenlogo und Anschrift als **Briefkopf** (für spätere Läufe gespeichert),
2. Name, Firma und Anschrift des **Kunden**,
3. die zu prüfende **Website**.

Danach folgt eine vollständige **passive** Prüfung der öffentlichen Website und ein professioneller Report:

1. Seite 1: ansprechende, professionelle Titelseite.
2. Überblick wie ein Inhaltsverzeichnis: jeder Testtitel mit einzeiligem Ampel-Ergebnis.
3. Die Tests: kurz und laienverständlich beschrieben, mit Befund oder „bestanden“.
4. Ein Teil für den WebAdmin „mit allen wichtigen detaillierten Infos, die er braucht, um die offenen Findings zu beheben oder zu prüfen, mit Checkliste und ggf. einfachen HowTo-Guides“.

**Warum ein eigener Befehl:** `/legal-audit-live` (`.claude/commands/legal-audit-live.md`) liefert ein internes `LiveAudit.md` mit Severity-Tabelle für Fachleute. Es fehlen: Briefkopf, Kundenadressat, laienverständlicher Kundenteil, Behebungsteil für den WebAdmin, Anwendbarkeitslogik (Shop, BFSG) und ein festes, reproduzierbares Layout. Der optische Prototyp (Eigentümer-Report für eine Werkstatt-Website, HTML plus PDF über headless Chrome, 52-Punkte-Katalog) zeigte, dass das Format trägt, aber per Hand-HTML je Lauf nicht stabil reproduzierbar ist (siehe Abschnitt 5, Variante B).

**Scope (entschieden):** alles, was ansatzweise rechtliche Relevanz hat, ausdrücklich auch Barrierefreiheit und Cookiebanner. **Nicht:** Website-Geschwindigkeit, SEO, GEO.

---

## 2. Ziele, Nicht-Ziele, Anti-Ziele

### Ziele
- G1: Ein Lauf erzeugt aus URL plus Intake-Antworten einen vollständigen Report (PDF und HTML) mit identischem Layout bei jedem Lauf.
- G2: Jeder Test aus dem Prüfkatalog erscheint genau einmal mit genau einem Status; Zählung und Ampel sind maschinell korrekt.
- G3: Der Kundenteil ist ohne Fachwissen lesbar; der WebAdmin-Teil reicht aus, um jeden offenen Punkt zu beheben und selbst nachzuprüfen.
- G4: Pflichten, die zum Prüfdatum nicht gelten oder auf den Kunden nicht anwendbar sind, erzeugen keinen Mangel.
- G5: Briefkopf einmal erfassen, danach wiederverwenden.
- G6: Funktioniert auf Claude Code, Codex CLI und Copilot CLI im Rahmen dessen, was die Plattform an Browser-Werkzeugen bietet (Abschnitt 4).

### Nicht-Ziele (v1)
- Geschwindigkeit/Performance, SEO, GEO, Ranking, Inhaltsqualität.
- Prüfung von Code, Server-Konfiguration oder Verträgen hinter der Website (das bleibt `/legal-audit` und `/legal-doc-check`).
- Automatischer Retest-Diff-Report. Das Schema wird retest-fähig gebaut (stabile Test-IDs, Retest-Kriterium je Finding), der Vergleichsbefehl folgt später.
- Englische Reports, Mehrsprachigkeit.
- Versand des Reports, Kundenverwaltung, Abrechnung.

### Anti-Ziele (das darf das Ergebnis nie sein oder tun)
- A1: Der Report **wirkt wie ein Rechtsgutachten oder eine Garantie** („rechtssicher“, „abmahnsicher“, „DSGVO-konform zertifiziert“, Siegel, Gesamtnote).
- A2: **Rote Findings für nicht anwendbare Pflichten** (Shop-Pflichten bei einer Visitenkarten-Website, Pflichten vor ihrem Geltungsdatum). Barrierefreiheitsmängel ohne BFSG-Pflicht sind nie ✕, sondern ▲ mit dem Zusatz „keine gesetzliche Pflicht, empfohlen“ (Abschnitt 6.3, entschieden durch Nutzer, 2026-11-17).
- A3: **Layout schwankt** zwischen Läufen; Abschnitte fehlen; Zählung stimmt nicht mit den Einzelergebnissen überein.
- A4: **Kundendaten landen in Plugin-Daten** (`${CLAUDE_PLUGIN_DATA}`) oder im Schatten-Archiv `audits/` des Plugins.
- A5: Die Prüfung geht **über normales Browsen hinaus**: keine Formularabsendungen, keine Logins, keine Bestellungen, kein Fuzzing, keine Port- oder Verzeichnis-Scans, keine Last.
- A6: Inhalte der geprüften Website werden **unescaped** in den Report übernommen oder als Anweisung behandelt.
- A7: Externe Requests beim Rendern des Reports (Fonts, CDNs, Tracking im Report selbst).

---

## 3. Constraints

| Constraint | Quelle im Ist-Stand | Folge für den Bau |
|---|---|---|
| Python nur Standardbibliothek | Konvention aller Skripte, z. B. Paket `scripts/citation_check/` (CLAUDE.md, Abschnitt Hilfs-Skripte) | Kein Jinja2, kein `markdown`, kein `jsonschema`, kein WebSocket-Client. Template-Ersetzung und Schema-Prüfung von Hand. |
| Kein pandoc, kein WeasyPrint | `scripts/legal-audit-pdf.py:119-136` hängt an pandoc/wkhtmltopdf, Fallback ist ein `<pre>`-Block (`:53-61`) | PDF ausschließlich über Chrome/Chromium. |
| Windows primär, macOS/Linux mit Chrome-Erkennung | Nutzerumgebung Windows 11 | Chrome-Pfade: `%ProgramFiles%`, `%ProgramFiles(x86)%`, `%LocalAppData%\Google\Chrome\Application\chrome.exe`, Edge als Fallback; macOS `/Applications/Google Chrome.app/...`; Linux `shutil.which` für `google-chrome`, `chromium`, `chromium-browser`. Umgebungsvariable als Override (Name dem Builder überlassen). |
| Drei Plattformen | `scripts/sync-platforms.py:212-233` portiert jedes `.claude/commands/*.md` nach `.codex/prompts/` und `.github/prompts/<name>/PROMPT.md`; `validate.yml` Job `sync-check` | Nach Anlage des Befehls `python scripts/sync-platforms.py --apply`; MCP-Werkzeugnamen in `allowed-tools` werden **nicht** gemappt (`map_tools`, `:150-157`). Die Abbildung `${CLAUDE_PLUGIN_ROOT}` → `${GITHUB_WORKSPACE}` für Copilot (`:71`) ist im Plan zu korrigieren oder als Einschränkung zu dokumentieren (Abschnitt 6.9.3). |
| Agents manuell im Manifest | `.claude-plugin/plugin.json:31` (`agents` ist ein Array einzelner `.md`-Pfade) | Ein neuer Agent braucht zwei Einträge (1M und `-pro`), `-pro` per `scripts/sync-pro-variants.py --apply`. |
| Versionsbump und CHANGELOG | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json:9,19`; Codex-Manifest übernimmt die Version (`sync-platforms.py:311`) | Neuer Befehl = Minor-Release (1.5.0), Eintrag unter `[Unreleased]` in `CHANGELOG.md`; `CLAUDE.md`-Befehlstabelle, `README.md`/`README.en.md`, `docs/commands.md` nachziehen. |
| CI `validate.yml` | Jobs sync-check, Unit-Tests (`python -m unittest discover -s tests`), pro-variants-check, disclaimer-check (`:74-102`) | Neue Tests laufen automatisch mit. Der disclaimer-check greift nur `*.md` unter `templates/` (`:91`), eine HTML-Vorlage ist nicht abgedeckt: Disclaimer-Prüfung für die Vorlage als Unit-Test ergänzen. |
| RDG | CLAUDE.md, Haftungsausschluss; `templates/disclaimer-block.md` | Disclaimer im Report fest im Skript eingesetzt, nicht vom Modell formuliert. |
| Keine Gedankenstriche in Report-Texten | Nutzerregel (global) | Gilt für alle Strings im PDF/HTML. Kollision: `templates/disclaimer-block.md:1,8` enthält selbst Gedankenstriche; der Report braucht einen **eigenen**, gedankenstrichfreien Disclaimer-Text (Abschnitt 6.8). |

---

## 4. Ist-Stand, der die Entscheidungen berührt

1. **`/legal-audit-live` ist die Prüfgrundlage.** Pässe 1 bis 8 (`legal-audit-live.md:63-158`) und die Drittanbieter-Muster (`:160-192`) werden für die Prüfbereiche Consent, Drittanbieter und Sicherheit wiederverwendet, nicht dupliziert. Empfehlung: die Muster in eine gemeinsame Datendatei auslagern (z. B. JSON unter `templates/client-test/` oder `knowledge/`), die beide Befehle lesen. Der Builder entscheidet, ob er `legal-audit-live.md` dafür anfasst.
2. **Severity-Modell weicht ab.** Bestehend: CRIT/HIGH/MED/LOW mit „im Zweifel eine Stufe höher“ (CLAUDE.md, Severity-Matrix) und Regeln wie „Google Fonts immer CRIT“ (`legal-audit-live.md:133,180`). Der Client-Report zeigt **keine** Severity, sondern vier Status. Die Severity bleibt als internes Feld für die Sortierung (Top-3, Reihenfolge im WebAdmin-Teil) erhalten (Abschnitt 6.3).
3. **Werkzeugnamen in `legal-audit-live.md:4`** lauten `mcp__plugin_chrome-devtools-mcp__chrome-devtools__*`. In der aktuellen Claude-Code-Umgebung heißen die Werkzeuge `mcp__plugin_chrome-devtools-mcp_chrome-devtools__*` (einfacher Unterstrich vor `chrome-devtools`). Builder: die tatsächlichen Namen prüfen, bevor er `allowed-tools` für den neuen Befehl abschreibt; der bestehende Befehl ist vermutlich mit betroffen (eigenes Issue).
4. **Codex/Copilot:** `sync-platforms.py` reicht MCP-Namen unverändert durch. Ob chrome-devtools-mcp dort mit gleichen Namen verfügbar ist, ist offen. v1-Anforderung: Befehl wird portiert; ohne Browser-Werkzeug bricht er mit klarer Meldung ab, statt einen unvollständigen Report zu erzeugen.
5. **`post_write.py` prüft nur `.md`** unter `docs/legal-audit/`, `knowledge/`, `templates/`, `audits/` (`.claude/hooks/post_write.py:19-24`). Report-Dateien unter `client-reports/` sind nicht erfasst: Die Disclaimer-Erzwingung liegt beim Render-Skript, nicht beim Hook.
6. **Plugin-Daten-Pfad:** Muster aus `scripts/legal-audit-pro-mode.py:46-60` (`CLAUDE_PLUGIN_DATA`, sonst `~/.claude/`, für Codex `CODEX_HOME`, für Copilot `COPILOT_HOME`). Das Profil folgt demselben Muster.
7. **Testkonvention:** `unittest`, offline, `tests/support.py` legt `scripts/` auf `sys.path`; Skripte mit Bindestrich werden per `importlib` geladen (z. B. `tests/test_legal_status.py`). Das Render-Skript braucht dieselbe Behandlung.

---

## 5. Approaches

### A. Gemeinsame `findings.json` plus festes HTML-Template plus Chrome-PDF (**gewählt, entschieden**)
Jeder Prüfbereich schreibt seine Ergebnisse in eine gemeinsame `findings.json` mit festem Schema. Ein Python-Skript (nur Standardbibliothek) validiert sie und füllt eine feste HTML-Vorlage (Titelseite, Überblick, Kundenteil, WebAdmin-Teil, Anhang). Headless Chrome erzeugt das PDF.
- **Pro:** gleiches Layout bei jedem Lauf; Zählung und Ampel garantiert korrekt; Disclaimer fest eingesetzt; testbar mit Fixtures; eine Datenquelle für Kunden- und WebAdmin-Teil; `valid_from` im Befund lässt das Skript zum Prüfdatum entscheiden, ob eine Pflicht schon galt; ein späterer Retest vergleicht zwei `findings.json`.
- **Contra:** Schema und Prüfkatalog müssen gepflegt werden; Modellfreiheit bei Texten ist auf Felder begrenzt (gewollt).

### B. KI schreibt das HTML je Lauf (**verworfen**)
So entstand der Prototyp. Layout schwankt, mehrere Korrekturrunden waren nötig, Vollständigkeit und Zählung sind nicht garantiert, kaum testbar.

### C. `scripts/legal-audit-pdf.py` ausbauen (**verworfen**)
Der Ist-Stand rendert Markdown über das optionale Paket `markdown` oder escaped in `<pre>` und erzeugt PDF nur mit pandoc. Titelseite, zweiteiliger Aufbau und Checklisten sind damit nicht tragbar; faktisch ein Neuschreiben plus pandoc-Abhängigkeit.

### D. WeasyPrint als PDF-Engine (**verworfen**)
Unter Windows sind GTK-Bibliotheken nötig; Installationshürde für Agenturen.

---

## 6. Entschiedene Teile

### 6.1 Befehl und Aufruf
- Name: `/legal-client-test` (**Call des Orchestrators, korrigierbar**; passt zu den `/legal-*`-Befehlen).
- Argumente (**Vorschlag dieses Dokuments**): `<url> [--edit-profile] [--out=<ordner>] [--no-pdf]`. Flags englisch wie bei `--compare`, `--pdf`, `--consent`, `--out`.
- Pro-Mode-Awareness-Abschnitt und Agent-Marker-Tabelle wie in `legal-audit.md:32-37,99-108`, falls ein Agent dispatcht wird.

### 6.2 Ablauf in Phasen

**Phase 0: Briefkopf-Profil**
- Profil vorhanden und nicht `--edit-profile`: kurz anzeigen (Firma, Ort) und weiter.
- Sonst abfragen: Firmenname, Ansprechperson, Anschrift, Telefon/E-Mail/Website, Logo-Pfad (PNG, JPG oder SVG; SVG wird als Datei eingebettet, nie als Inline-Markup, wegen Skriptinhalten), optional Akzentfarbe `accent_color` (Hex; sonst Ableitung beim ersten Lauf, Abschnitt 6.6).
- Speicherung und Wiederverwendung: Abschnitt 6.7. (**Call des Orchestrators, korrigierbar**: beim ersten Lauf abfragen, danach wiederverwenden, änderbar per Option.)

**Phase 1: Intake**
- Kunde: Name, Firma, Anschrift. URL validieren (`https://` oder `http://`; Redirect-Ziel festhalten).
- Vorab-Erkundung (passiv): Startseite laden, Shop-Merkmale (Warenkorb, Preise mit „inkl. MwSt.“, Checkout-Links, Shop-Systeme), Plattform-Funktionen (Nutzerinhalte, Bewertungen, Marktplatz), Chatbot/KI-Widgets erkennen.
- **Anwendbarkeitsfragen mit Bestätigung** (entschieden): 
  - Richtet sich das Angebot an Verbraucher (B2C)?
  - BFSG-Vorfrage (steuert nur die Einstufung der A11Y-Ergebnisse, nicht ob die A11Y-Tests laufen, Abschnitt 6.3): Werden über die Website Verbraucherverträge angebahnt oder geschlossen, und ist der Kunde **kein** Kleinstunternehmen (weniger als 10 Beschäftigte und Jahresumsatz oder Jahresbilanzsumme höchstens 2 Mio. EUR; Ausnahme nur für Dienstleistungen)? Beleg: `knowledge/checklisten/audit-ecommerce.md:152`, `knowledge/gesetze/bfsg.md:111`.
  - „Wir haben einen Online-Shop erkannt. Stimmt das?“ (oder umgekehrt).
  - Beschäftigtenzahl (für VSBG-Hinweis, `audit-ecommerce.md:248`), falls nicht ermittelbar: Status „–“.
- Antworten werden mit Quelle (`user` oder `detected`) in `applicability` gespeichert und sind **dreiwertig**: `true`, `false` oder `null` (unbekannt). Bei `null` fragt der Befehl nach; die Folgen stehen in Abschnitt 6.9.1 (**Call des Orchestrators, korrigierbar**).

**Phase 2: Prüfung (passiv)**
- Prüfbereiche laut 6.4, jeder schreibt Ergebnisse für seine Katalog-IDs.
- **Passiv heißt (Anti-Ziel A5):** nur was ein normaler Besucher tut. Erlaubt: Seiten aufrufen (Start, Impressum, Datenschutz, AGB, Widerruf, Kontakt, Barrierefreiheit, ein Produkt, Warenkorb-Ansicht), Consent-Banner bedienen (Ablehnen, Akzeptieren, Einstellungen öffnen), Seitenquelltext, DOM, Netzwerk- und Cookie-Protokoll lesen, Antwort-Header per einfachem GET/HEAD, Lighthouse-Barrierefreiheitsaudit (chrome-devtools-mcp hat `lighthouse_audit`). Verboten: Formulare absenden, Konto anlegen, einloggen, Bestellung auslösen, Adressdaten eingeben, Pfade raten, Ports scannen, mehr als eine moderate Anzahl Seiten (Obergrenze dem Builder überlassen, Richtwert 25 Seiten, höchstens ein paralleler Tab).
- Folge: Was nur hinter einer Eingabe sichtbar wäre (z. B. Bestell-Button der Button-Lösung, Kündigungsbestätigungsseite), wird „– Nicht prüfbar“ mit Begründung, nicht geraten.
- Belege (Screenshots, Netzwerk-JSON, Header) nach `evidence/`.

**Phase 3: Validierung und Render**
- `python scripts/client-test.py render <report-ordner>` (Name **Vorschlag**): in dieser Reihenfolge (Begründung und Details in 6.9.2, **Call des Orchestrators, korrigierbar**): (1) eingelesene `findings.json` gegen das Schema validieren; (2) Katalog-Vollständigkeit prüfen und Anwendbarkeit aus `applies_if` ableiten; (3) Herabstufungen anwenden (`valid_from`, ungeklärte Anwendbarkeit); (4) Render-Invarianten auf dem abgeleiteten Modell prüfen (Zählung, Pflichtfelder je abgeleitetem Status); (5) Textprüfung der Prosa-Felder, HTML-Escaping aller Fremdinhalte, Disclaimer einsetzen, `report.html` schreiben.
- Fehler sind blockierend mit konkreter Meldung (welche ID, welches Feld). Das Modell korrigiert `findings.json` und rendert erneut; es editiert nie das HTML.

**Phase 4: PDF**
- Chrome headless erzeugt `report.pdf` aus `report.html` (Abschnitt 6.6). Ohne gefundenes Chrome: HTML bleibt Ergebnis, klare Meldung, Exit-Code ungleich 0.

### 6.3 Status-Modell und Befund-Schema

**Status (entschieden):** Farbe plus Symbol plus Text (WCAG 1.4.1).

| Code | Symbol | Text im Report | Bedeutung |
|---|---|---|---|
| `pass` | ✓ | Bestanden | Anforderung erfüllt, soweit passiv prüfbar |
| `notice` | ▲ | Hinweis | Verbesserung empfohlen, unklare Lage, Pflicht kommt erst (vor `valid_from`), Anwendbarkeit ungeklärt, oder A11Y-Mangel ohne gesetzliche Pflicht |
| `defect` | ✕ | Mangel | Zum Prüfdatum geltende, anwendbare Pflicht beobachtbar nicht erfüllt |
| `none` | – | Nicht prüfbar / Nicht anwendbar | mit Pflichtfeld `reason_kind` (`not_checkable`, `not_applicable`) und Begründungstext |

- „–“ deckt beide Fälle ab, jeweils mit Begründung; nicht anwendbare Tests erscheinen **grau** im Überblick (**Call des Orchestrators, korrigierbar**). **Ausnahme A11Y**, siehe nächster Punkt.
- **Barrierefreiheit ohne BFSG-Pflicht (entschieden durch Nutzer, 2026-11-17):** Die A11Y-Tests laufen immer (Katalogflag `always_run`), unabhängig von der BFSG-Antwort. Ein Mangel erscheint dann als ▲ Hinweis mit dem Zusatz „keine gesetzliche Pflicht, empfohlen“, **nie** als ✕. „–“ ist für A11Y nur zulässig, wenn ein Test technisch nicht prüfbar war (`reason_kind: not_checkable`); `not_applicable` ist für A11Y-IDs unzulässig und wird vom Skript abgelehnt. Damit entfällt der Widerspruch zu „nicht anwendbare Tests grau“: A11Y wird nie wegen Anwendbarkeit grau. Lesart dieses Dokuments (**Call des Orchestrators, korrigierbar**): Besteht eine BFSG-Pflicht (`bfsg == true`), gilt für A11Y die normale Regel inklusive `defect` und `valid_from` 28.06.2025; bei `bfsg == false` greift die Entscheidung oben; bei `bfsg == null` ist das Ergebnis ▲ mit Vermerk „Anwendbarkeit ungeklärt“ (6.9.1).
- **Mapping Severity zu Status (Vorschlag dieses Dokuments, korrigierbar):** `defect` verlangt `severity` CRIT, HIGH oder MED; `notice` verlangt MED oder LOW. Severity wird nicht angezeigt, dient nur der Sortierung. Damit bleibt die bestehende Matrix intern nutzbar, ohne dass der Report wie eine Note wirkt.
- **`valid_from`-Regel (Vorschlag, korrigierbar; Reihenfolge Call des Orchestrators, korrigierbar):** Liegt das Prüfdatum vor `valid_from` der maßgeblichen Rechtsgrundlage, setzt das Skript einen `defect` auf `notice` herunter, begrenzt die Severity auf höchstens MED, hält das Original in `severity_original` fest und ergänzt „Pflicht gilt ab TT.MM.JJJJ“. Hat ein Test mehrere Rechtsgrundlagen, zählt die früheste bereits geltende. Die Herabstufung geschieht **nach** der Schema-Validierung der Eingabe und **vor** den Render-Invarianten (6.9.2).

**Prüfkatalog als Daten (Vorschlag dieses Dokuments, korrigierbar):** Ein versionierter `catalog.json` im Plugin definiert jede Test-ID mit Bereich, Titel, laienverständlicher Kurzbeschreibung, Rechtsgrundlagen mit `valid_from` und KB-Fundstelle, Anwendbarkeitsbedingung `applies_if` (z. B. `shop == true`, auswertbar gegen die dreiwertigen Intake-Antworten, 6.9.1), Flag `always_run` (für A11Y, 6.3) und Standard-Retest-Kriterium. Die `findings.json` liefert nur die laufbezogenen Teile. Das garantiert Vollständigkeit, stabile IDs über Läufe (Retest) und dass Titel und Rechtsgrundlagen nicht vom Modell je Lauf neu formuliert werden.

**ID-Präfixe (CK-, SEC-, A11Y- entschieden; Rest Vorschlag):** `IMP-` Impressum, `DSE-` Datenschutzerklärung, `CK-` Cookie/Consent, `DRT-` Drittanbieter und Drittland, `SEC-` Sicherheit, `FRM-` Formulare, `A11Y-` Barrierefreiheit, `SHOP-` Verbraucher- und Shop-Pflichten, `UWG-` Werbung, Umweltaussagen, Bewertungen, `KI-` KI-Transparenz, `DSA-` Plattform-Funktionen. Format `CK-03`, zweistellig, nie wiederverwendet.

**Schema-Skizze `findings.json`** (Feldnamen englisch, Inhalte deutsch):

```json
{
  "schema_version": "1.0",
  "catalog_version": "2026.11-1",
  "plugin_version": "1.5.0",
  "run": {
    "started_utc": "2026-11-17T09:12:03Z",
    "finished_utc": "2026-11-17T09:31:40Z",
    "target_url": "https://example.de/",
    "final_url": "https://www.example.de/",
    "domain": "example.de",
    "user_agent": "...",
    "viewports": ["1920x1080", "390x844 (mobil)"],
    "tools": {"chrome": "...", "chrome_devtools_mcp": "...", "lighthouse": "..."},
    "pages_visited": ["https://www.example.de/", "https://www.example.de/impressum"]
  },
  "issuer": {"company": "...", "contact": "...", "address": ["..."], "email": "...",
             "logo_file": "assets/logo.png", "accent_color": "#1F4E79"},
  "client": {"name": "...", "company": "...", "address": ["..."]},
  "applicability": {
    "b2c": {"value": true, "source": "user"},
    "shop": {"value": false, "source": "detected+confirmed"},
    "bfsg": {"value": false, "source": "user", "note": "Kleinstunternehmen, nur Dienstleistung"},
    "platform_features": {"value": false, "source": "detected"},
    "ai_chat": {"value": true, "source": "detected"}
  },
  "summary": {"sentences": ["...", "...", "..."], "top_actions": ["CK-03", "SEC-02", "IMP-01"]},
  "results": [
    {
      "id": "CK-03",
      "status": "defect",
      "severity": "HIGH",
      "severity_original": null,
      "reason_kind": null,
      "reason": null,
      "one_liner": "Ablehnen ist im Banner nur über einen Zusatzschritt erreichbar.",
      "client_text": "Laienverständliche Erklärung in 2 bis 4 Sätzen.",
      "evidence": [
        {"kind": "screenshot", "file": "evidence/ck-03-banner.png", "caption": "...", "alt": "..."},
        {"kind": "network", "file": "evidence/network-pre-consent.json", "excerpt": "..."}
      ],
      "risk": "Wozu das führen kann, ohne Drohkulisse.",
      "fix": {
        "steps": ["...", "..."],
        "snippets": [{"target": "wordpress", "lang": "text", "code": "..."}],
        "effort": {"level": "gering", "minutes": 30}
      },
      "retest": {"how": "Seite im privaten Fenster öffnen ...", "command": "curl -sI https://www.example.de/",
                 "expected": "Strict-Transport-Security: max-age=..."},
      "references": ["https://www.gesetze-im-internet.de/..."],
      "checklist": ["...", "..."]
    }
  ]
}
```

Rechtsgrundlagen (`legal_basis: [{norm, valid_from, kb_ref}]`) stehen im Katalog; ein Ergebnis darf sie nur ergänzen, nicht ersetzen. Pflichtfelder je Status (Vorschlag): `pass` braucht `one_liner`; `notice`/`defect` brauchen zusätzlich `client_text`, `evidence` (mindestens ein Eintrag), `risk`, `fix`, `retest`, `checklist`; `none` braucht `reason_kind` und `reason`. Die Pflichtfelder gelten für den **abgeleiteten** Status (6.9.2); `severity_original` und der Vermerk werden vom Skript gesetzt, nie vom Modell. `applicability.*.value` ist `true`, `false` oder `null`. **Feldklassen (Call des Orchestrators, korrigierbar):** Das Schema markiert jedes String-Feld als `prose` (selbst verfasster Text: `one_liner`, `client_text`, `risk`, `summary.sentences`, `fix.steps`, `checklist`, `reason`, Titel) oder `verbatim` (Fremd- oder Maschinentext: `evidence[].excerpt`, zitierte Seitentitel und Header, URLs, `retest.command`, `retest.expected`, `fix.snippets[].code`); die Textprüfung in 6.8 liest nur `prose`.

### 6.4 Prüfbereiche und rechtlicher Prüfumfang

Grundlage für den Katalog. Spalte „KB“ zeigt, ob der Fakt in `knowledge/` belegt ist; „zu verifizieren“ heißt: vom Builder gegen Primärquelle zu prüfen, bevor er in den Katalog geht.

| Präfix | Bereich | Kernprüfungen (passiv) | Rechtsgrundlage, `valid_from` | KB |
|---|---|---|---|---|
| IMP | Impressum | erreichbar mit einem Klick von jeder Seite, Pflichtangaben vorhanden | § 5 DDG (seit 14.05.2024) | `gesetze/ddg.md:39`, `gesetze/dsa.md:29` |
| DSE | Datenschutzerklärung | vorhanden, erreichbar; beobachtete Dienste und Cookies in der Erklärung genannt (Abgleich mit Netzwerkprotokoll) | Art. 13 DSGVO | `themen/datenschutzerklaerung.md` |
| CK | Consent | Leaks vor Einwilligung; Ablehnen auf erster Ebene, wenn das Banner Inhalte versperrt oder eine Interaktion erzwingt; keine vorangekreuzten Boxen; Widerruf jederzeit erreichbar; Verhalten nach Ablehnen gleich Erstbesuch | § 25 TDDDG, DSGVO; DSK OH Digitale Dienste Rn. 124 f. | `gesetze/tdddg.md:47`, `themen/cookie-consent.md:59` |
| DRT | Drittanbieter | Google Fonts, Embeds (YouTube, Maps, Vimeo, Social), Analytics, Pixel, CDN; US-Transfer und DPF-Zertifizierung als Hinweis; Rechtsmittel C-703/25 P anhängig | Art. 44 ff. DSGVO, § 25 TDDDG | `themen/drittland-transfer.md:52,112` |
| SEC | Sicherheit (nur passiv) | HTTPS erzwungen, HSTS, Sicherheits-Header (CSP, frame-ancestors/X-Frame-Options, Referrer-Policy, X-Content-Type-Options), Mixed Content, Cookie-Flags (Secure, HttpOnly, SameSite) | Art. 32 DSGVO, § 19 Abs. 4 TDDDG | `checklisten/audit-ecommerce.md:27` |
| FRM | Formulare | Transportverschlüsselung, Pflichtfelder sparsam, Datenschutzhinweis am Formular, Newsletter-Einwilligung nicht vorangekreuzt, Double-Opt-in nur als Hinweis (nicht absendbar prüfbar) | Art. 5, 6, 7, 13 DSGVO; § 7 UWG | `themen/email-marketing.md` |
| A11Y | Barrierefreiheit | läuft immer, Mängel ohne BFSG-Pflicht nur als ▲ „keine gesetzliche Pflicht, empfohlen“ (6.3); Lighthouse-Barrierefreiheitsaudit und Stichproben (Kontrast, Alt-Texte, Tastatur, Fokus, Sprache); Informationen zur Barrierefreiheit vorhanden; im Report ehrlich: automatische Tests decken nur einen Teil von WCAG ab | BFSG seit 28.06.2025; § 14 Abs. 1 Nr. 2 i. V. m. Anlage 3 BFSG | `gesetze/bfsg.md:76`, `themen/barrierefreiheit.md:27` |
| SHOP | nur bei Shop | Preisangaben (PAngV), Button-Lösung (meist „–“, Abschnitt 6.2), Widerrufsbelehrung, Widerrufsfunktion, Kündigungsbutton bei Abos, GPSR-Angaben am Produkt, Gewährleistungsmitteilung, kein OS-Plattform-Link mehr nötig, Garantie-Label, Verpackungsregister | siehe Zeilen unten | siehe unten |
| UWG | Werbung | Umweltaussagen/Green Claims, Bewertungen (Hinweis nach § 5b Abs. 3 UWG), irreführende Angaben | §§ 5, 5a, 5b UWG; EmpCo-Umsetzung seit 27.09.2026 | `checklisten/audit-ecommerce.md:136,147` |
| KI | KI-Transparenz | Chatbot als KI gekennzeichnet; KI-Inhalte (Deepfakes) | Art. 50 AI Act, anwendbar seit 02.08.2026 | `gesetze/ai-act.md:147`, `checklisten/general-pre-launch.md:123` |
| DSA | Plattform-Funktionen | Kontaktstellen, Melde- und Abhilfeverfahren, nur wenn Nutzerinhalte gehostet werden | Art. 11, 12, 16 DSA | `gesetze/dsa.md:39,43,58` |

Shop-Einzelpunkte:

| Pflicht | `valid_from` | KB |
|---|---|---|
| Widerrufsfunktion § 356a BGB | 19.06.2026 | `checklisten/audit-ecommerce.md:100,302` |
| Kündigungsbutton § 312k BGB | KB nennt kein Datum; **zu verifizieren** (Geltung seit 01.07.2022) | `audit-ecommerce.md:111` |
| GPSR VO (EU) 2023/988 Art. 19 | 13.12.2024 | `audit-ecommerce.md:131` |
| OS-Plattform-Link entfällt (Plattform eingestellt) | 20.07.2025 | `audit-ecommerce.md:119` |
| Harmonisierte Gewährleistungsmitteilung DVO (EU) 2025/1960 | KB ohne Datum | `general-pre-launch.md:84` |
| Garantie-Label (Haltbarkeitsgarantie) DVO (EU) 2025/1960, ab 27.09.2026 | **zu verifizieren** (KB belegt nur die Mitteilung, nicht Label und Stichtag) | nicht belegt |
| PPWR VO (EU) 2025/40, ab 12.08.2026 (Verpackungsregister) | **zu verifizieren** (nicht in der KB) | nicht belegt |
| BFSG-Kleinstunternehmen-Ausnahme | 28.06.2025 | `audit-ecommerce.md:152` |

**Digital Omnibus:** Der Vorschlag zur Änderung von DSGVO/ePrivacy (`knowledge/gesetze/dsgvo.md:24`, `themen/drittland-transfer.md:129`) ist Entwurf und wird **nicht** verwendet; geprüft wird gegen den geltenden § 25 TDDDG. Achtung, Abgrenzung: Die KB führt den KI-Omnibus als erlassene VO (EU) 2026/1744 (`general-pre-launch.md:123`); er bestimmt die Art.-50-Daten (Altbestand-Markierung bis 02.12.2026). Der Builder verwendet die Art.-50-Daten so, wie die KB sie belegt.

### 6.5 Report-Gliederung (Text-Skizze)

Alle hier in Anführungszeichen gezeigten Report-Strings sind gedankenstrichfrei.

```
Seite 1  Titelseite
         Logo und Briefkopf des Auslösers (oben)
         Titel "Website-CheckUp • Datenschutz, Recht & Sicherheit" + Unterzeile "KI-gestützte Ersteinschätzung" (entschieden durch Nutzer, 2026-11-17)
         Geprüfte Website: domain
         Erstellt für: Kunde Name, Firma, Anschrift
         Prüfdatum, Report-Kennung (Datum + Domain)
         Erstellt von: Firma des Auslösers, Kontakt
         Kurzhinweis: "KI-gestützte Einschätzung. Keine Rechtsberatung, keine Garantie."
         "Vertraulich"
Seite 2  Überblick
         Vier Zähler: ✓ Bestanden n • ▲ Hinweis n • ✕ Mangel n • – Nicht prüfbar/anwendbar n
         Zusammenfassung: genau 3 Sätze
         Die 3 wichtigsten Maßnahmen (aus summary.top_actions, mit Finding-ID)
         Tabelle aller Tests, gruppiert nach Bereich:
           ID | Testtitel | Symbol + Statustext | Einzeiler | Seite
           (nicht anwendbare Zeilen grau, A11Y nie wegen Anwendbarkeit)
Teil A   Für Sie als Inhaberin oder Inhaber (Kundenteil)
         je Bereich: ein Satz, worum es geht
         je Test: Was wir geprüft haben | Ergebnis | bei ▲/✕: Was das bedeutet,
         was zu tun ist (1 bis 2 Sätze), Verweis "Details für Ihre Technik: Teil B, CK-03"
Teil B   Für Ihre Webbetreuung (WebAdmin-Teil)
         Prioritätenliste: alle offenen IDs als ☐-Checkliste, sortiert nach Severity, mit Aufwand
         je offenem Finding:
           Befund | Beleg (Screenshot, Netzwerk- oder Header-Auszug)
           Risiko | So beheben Sie es (Schritte; Snippets nginx, Apache, WordPress wo sinnvoll)
           So prüfen Sie es nach (curl-Befehl + erwartete Ausgabe, oder Browser-Schritte)
           Referenzen | ☐-Checkliste | Aufwand und Zeitschätzung
Anhang   A Prüfprotokoll (Tool-Versionen, UTC-Zeiten, User-Agent, Viewports, besuchte Seiten)
         B Methodik und Grenzen (passiv, Stichprobe, automatische WCAG-Tests nur Teilabdeckung,
           Momentaufnahme, keine Prüfung hinter Logins oder Formularen)
         C Glossar (Consent, Header, HSTS, Drittland, ...)
         D Vollständiger Haftungsausschluss
Jede Seite: Kopf "Vertraulich"; Fuß mit Kurzhinweis und "Seite x von y"
```

- **Keine Gesamtnote, kein Score**, nur Zählungen je Status (entschieden).
- **Titel (entschieden durch Nutzer, 2026-11-17):** „Website-CheckUp • Datenschutz, Recht & Sicherheit“, Unterzeile „KI-gestützte Ersteinschätzung“. Grund: „Rechtssicherheit“ im Titel suggeriert eine Garantie (Anti-Ziel A1). Der Titel ist eine Konstante im Template, nicht im Katalog. Das „&“ wird wie jeder Text escaped.
- **Finding-IDs verbinden** Überblick, Teil A und Teil B (Anker-Links im HTML und PDF).
- Fußzeilen-Entwurf: „KI-gestützte Einschätzung. Kann Fehler enthalten. Keine Rechtsberatung, keine Garantie für Rechtssicherheit.“

### 6.6 Typografie, Druck, PDF
- **IBM Plex Sans und IBM Plex Mono** (SIL OFL 1.1), im Plugin mitgeliefert (mit `OFL.txt`), als `@font-face` per Data-URI eingebettet. **`report.html` ist eigenständig weitergebbar** (**Call des Orchestrators, korrigierbar**): Fonts, Logo und Screenshots stehen als Data-URI im Dokument. Screenshots werden verkleinert und komprimiert; Größenbudget etwa 10 MB, darüber gibt das Skript eine Warnung aus (kein Abbruch). **Keine externen Requests beim Rendern** (Anti-Ziel A7); das Skript prüft die fertige HTML-Datei auf `http(s)://`-Referenzen in `src`/`href` außerhalb von Textlinks (`data:` ist erlaubt).
- **Chrome printToPDF mit `@page`-Margin-Boxen** für Kopf („Vertraulich“), Fuß (Hinweis, Seitenzahl). **Paged.js lokal gebündelt** nur für Seitenzahlen im Inhaltsverzeichnis (entschieden).
  - Technisches Risiko für den Builder: Paged.js übernimmt den gesamten Seitenumbruch und rendert Margin-Boxen selbst; „nur für das Inhaltsverzeichnis“ heißt praktisch, Paged.js paginiert das ganze Dokument und Chrome druckt mit `preferCSSPageSize` ohne eigene Ränder. Die Kombination vor dem Bau mit einem Spike prüfen. Fallback ohne Paged.js: Überblick ohne Seitenzahlen, mit klickbaren Finding-IDs.
- **Chrome-Ansteuerung aus stdlib-Python:** Der CDP-Weg (`Page.printToPDF` mit `generateTaggedPDF`, `generateDocumentOutline`) braucht WebSocket; die Standardbibliothek hat keinen Client. Optionen: (a) CLI `--headless --print-to-pdf --no-pdf-header-footer` plus Warteschalter, bis Paged.js fertig ist; (b) minimaler eigener WebSocket-Client über `socket`/`http.client`. Welche Schalter getaggte PDFs und Outline in der CLI liefern, ist **zu verifizieren** (Chrome-Version, die chrome-devtools-mcp ohnehin startet).
- **Print-CSS-Umbruchregeln:** `break-inside: avoid` für Finding-Blöcke, Tabellenzeilen, Code; `break-after: avoid` für Überschriften; Tabellenkopf wiederholen; Titelseite und Teil B beginnen auf neuer Seite; Witwen/Waisen ≥ 2.
- **Farben:** Akzentfarbe nur für Linien und Überschriften. Ampelfarben fix und kontrastgeprüft, unabhängig vom Logo. **Akzentfarbe (Call des Orchestrators, korrigierbar):** optionales Profilfeld `accent_color` (Hex). Beim ersten Lauf ohne Angabe: bei PNG Extraktion der dominanten, nicht zu hellen Farbe per `zlib` (Standardbibliothek), bei SVG aus den Füllfarben; bei JPG oder bei Fehlschlag einmal nach einem Hex-Wert fragen, sonst neutrale Standardfarbe (dunkles Schiefergrau). Das Ergebnis wird im Profil gespeichert. Kontrast gegen Weiß mindestens 4.5:1, sonst abdunkeln.
- **Getaggtes PDF**, Lesereihenfolge gleich DOM-Reihenfolge, Alt-Texte für Screenshots aus `evidence[].alt`. Ein Barrierefreiheits-Prüfbericht muss selbst barrierearm sein.

### 6.7 Speicherung und Ausgabe
- **Profil des Auslösers** (entschieden): nur Briefkopf (Logo, Anschrift, Kontakt, Akzentfarbe) dauerhaft unter `${CLAUDE_PLUGIN_DATA}` (Dateinamen-Vorschlag `client-test-profile.json` plus Logo-Kopie). Fallback-Pfade wie `scripts/legal-audit-pro-mode.py:46-60` für Codex und Copilot. Atomisch schreiben (Muster `atomic_write_json`, `:71-88`).
- **Kundendaten** (entschieden): nur im Report-Ordner des Laufs, nie in Plugin-Daten, nie in `audits/`.
- **Report-Ordner** (**Call des Orchestrators, korrigierbar**): `client-reports/<JJJJ-MM-TT>-<domain>/` im aktuellen Arbeitsverzeichnis mit `findings.json`, `report.html`, `report.pdf`, `evidence/`. Existiert der Ordner, wird mit Suffix `-2`, `-3` angelegt, nie überschrieben. Liegt das Arbeitsverzeichnis in einem Git-Repo und ist `client-reports/` nicht ignoriert, weist der Befehl darauf hin (Kundendaten).
- Ausgabe **PDF plus HTML**, Sprache **Deutsch** (entschieden). Dateiname des PDF für den Versand (Vorschlag): `Website-CheckUp-<domain>-<JJJJ-MM-TT>.pdf` als Kopie neben `report.pdf`.

### 6.8 RDG-Linie und Textregeln
- Formulierungen als **Hinweis/Einschätzung**, keine Rechtsberatung, keine Garantie (entschieden). **Verbotene Wendungen (Call des Orchestrators, korrigierbar):** Das Skript erkennt kein „Gesamturteil konform“ semantisch, sondern prüft eine Liste verbotener Wendungen (Datendatei neben dem Katalog, Beispiele: „rechtssicher“, „abmahnsicher“, „100 % konform“, „garantiert“, „zertifiziert“) in den `prose`-Feldern, ohne Beachtung von Groß- und Kleinschreibung und mit normalisierten Leerzeichen. Bei einem Treffer bricht es mit dem Feldpfad ab (z. B. `results[3].client_text`). `verbatim`-Felder sind ausgenommen.
- **Disclaimer vom Skript erzwungen** (entschieden): fester Text in der Vorlage auf Titelseite (kurz), in jeder Fußzeile (kurz) und im Anhang (voll). Er enthält „Keine Rechtsberatung“ und „§ 2 RDG“ und ist **gedankenstrichfrei** (nicht `templates/disclaimer-block.md` wiederverwenden, Abschnitt 3). Ein Unit-Test prüft Vorlage und gerendertes Beispiel auf diese Bestandteile.
- **Untrusted Input** (**Call des Orchestrators, korrigierbar**): Alles, was von der geprüften Website stammt (Titel, Texte, Header, URLs, Dateinamen), ist Daten, nie Anweisung. Das Skript escaped jedes Feld (`html.escape` mit `quote=True`), erlaubt kein Roh-HTML aus `findings.json`, setzt URLs nur als Text oder als geprüfte `https?`-Links, und Evidence-Pfade nur relativ innerhalb des Report-Ordners (kein `..`).
- **Keine Gedankenstriche** (**Call des Orchestrators, korrigierbar**): Report-Texte ohne „—“, „–“ und „ - “ als Pseudo-Gedankenstrich; Ersatz „•“, Komma, Doppelpunkt, „bis“. Das Skript prüft alle selbst verfassten Prosa-Felder (Titel, Zusammenfassung, Kundentext, Risiko, Fix-Beschreibung, Checklistenpunkte, Begründungen) und die Vorlage und bricht mit Fundstelle ab. **Ausgenommen** sind Evidence-Auszüge, zitierte Seitentitel und Header, URLs, curl-Befehle, Code-Snippets und erwartete Ausgaben; das Schema markiert diese Felder als `verbatim` (**Call des Orchestrators, korrigierbar**; interne Doku wie dieses Dokument darf Gedankenstriche im Fließtext verwenden, zitierte Report-Strings nicht). Ausnahme: das Status-Symbol „–“ für `none` ist ein festes Vorlagenelement, kein Text, und wird von der Prüfung ausgenommen.

### 6.9 Ableitungslogik, Reihenfolge, Pfade (Calls des Orchestrators, korrigierbar, 2026-11-17)

**6.9.1 Anwendbarkeit**
- Intake-Antworten sind dreiwertig: `true`, `false`, `null` (unbekannt).
- Das Skript leitet die Anwendbarkeit **deterministisch** aus den Katalogbedingungen (`applies_if`) und den Intake-Antworten ab. Das Modell setzt „nicht anwendbar“ nie selbst; ein `none` mit `reason_kind: not_applicable` in der Eingabe ist ein Validierungsfehler, das Skript trägt solche Zeilen selbst ein.
- Bei `null` fragt der Befehl nach. Bleibt es unbekannt, gilt der Test als anwendbar; ein `defect` wird zu `notice` mit dem Vermerk „Anwendbarkeit ungeklärt“ (gleiche Mechanik wie die `valid_from`-Herabstufung, Severity höchstens MED, Original in `severity_original`).
- Shop-Tests ohne Shop (`shop == false`): „–“ nicht anwendbar, grau, mit Begründung aus dem Katalog.
- Ausnahme A11Y: siehe 6.3 (`always_run`).

**6.9.2 Verarbeitungsreihenfolge im Render-Skript**
1. Eingelesene `findings.json` gegen das Schema validieren (Roheingabe, Statuscodes, Severity-Mapping aus 6.3, Feldklassen).
2. Katalog-Vollständigkeit prüfen und Anwendbarkeit ableiten (6.9.1).
3. Herabstufung: `valid_from` (6.3) und ungeklärte Anwendbarkeit; `defect` wird `notice`, Severity höchstens MED, `severity_original` bleibt erhalten, Vermerk „Pflicht gilt ab TT.MM.JJJJ“ bzw. „Anwendbarkeit ungeklärt“.
4. Render-Invarianten auf dem **abgeleiteten** Modell prüfen: Zählung gleich Summe der Zeilen, Pflichtfelder je abgeleitetem Status, `top_actions` verweisen auf offene IDs.
5. Textprüfung (6.8), Escaping, Disclaimer, Einbettung (6.6), HTML schreiben.

Begründung: Auf dem Rohmodell würden die Invarianten herabgestufte Befunde falsch bewerten (ein `defect` vor `valid_from` braucht die Pflichtfelder von `notice`, nicht die Severity-Spanne von `defect`). Fixtures decken beide Stufen ab: Eingabe-Validierung und Herabstufung.

**6.9.3 Pfade und Plattformen**
- Plugin-Assets (Skript, Katalog, Vorlage, Fonts, Paged.js) werden über `${CLAUDE_PLUGIN_ROOT}` adressiert; das Skript löst seine Assets relativ zu `__file__` auf, **nie** relativ zum Arbeitsverzeichnis. Nur der Report-Ordner liegt im Arbeitsverzeichnis (6.7); das Profil bleibt unter `${CLAUDE_PLUGIN_DATA}`.
- Claude Code ist Primärziel. Die Abbildung `${CLAUDE_PLUGIN_ROOT}` → `${GITHUB_WORKSPACE}` für Copilot (`scripts/sync-platforms.py:71`) trifft Plugin-Assets nicht, weil sie im Arbeitsbereich des Zielprojekts nicht liegen. Der Plan korrigiert die Abbildung **oder** führt die Einschränkung (Copilot: Assets nur bei Plugin-Kopie im Workspace) als dokumentierte Einschränkung.

---

## 7. Was dem Builder überlassen bleibt

- Genaue Prüf-Heuristiken je Bereich (Banner-Erkennung, Gleichwertigkeit, Erkennung von Shop- und Plattformfunktionen, Seitenauswahl, Lighthouse-Schwellen) im Rahmen von 6.2 und 6.4; Wiederverwendung der Pässe aus `legal-audit-live.md`.
- Agent-Zuschnitt: alles im Befehl, oder ein Prüf-Agent je Bereich bzw. ein `legal-client-tester` (dann 1M- und `-pro`-Variante, Einträge in `.claude-plugin/plugin.json:31`, `sync-pro-variants.py --apply`). Kriterium: Kontextbedarf eines Laufs mit Screenshots und Netzwerkprotokollen.
- Template-Engine-Details (z. B. `string.Template` plus eigene Schleifen-Helfer), Aufteilung `scripts/client-test.py` als dünner Einstieg plus Paket `scripts/client_report/` (analog `citation_check/`), Ablage der Vorlage unter `templates/client-test/`.
- Inhalt des Prüfkatalogs v1 (Anzahl Tests, Richtwert 40 bis 60 wie im Prototyp), Formulierung der laienverständlichen Katalogtexte (gedankenstrichfrei, RDG-Linie).
- Teststrategie im Rahmen der Repo-Konventionen: `unittest`, offline, Fixture-`findings.json` (vollständig, unvollständig, mit Escaping-Angriffen, mit Gedankenstrichen, mit Pflicht vor `valid_from`); Golden-Test auf das gerenderte HTML (Struktur, Zählungen, Disclaimer); PDF-Erzeugung nur als übersprungener Test, wenn kein Chrome gefunden wird (CI hat Ubuntu ohne garantiertes Chrome).
- Art der Shop-Bestätigungsfrage und Wortlaut aller Intake-Fragen.
- Ob die Drittanbieter-Muster in eine gemeinsame Datendatei wandern (Abschnitt 4.1).
- Spike Paged.js plus Chrome-PDF inklusive getaggtem PDF aus der CLI (Abschnitt 6.6), vor dem eigentlichen Bau.
- Verfügbarkeit von chrome-devtools-mcp unter Codex und Copilot sowie korrekte Werkzeugnamen (Abschnitt 4.3 und 4.4).
- Retest-Befehl (Vergleich zweier `findings.json`): Umfang und Name für ein Folge-Release.

---

## 8. Offene Punkte

1. **Lawyer-Check der RDG-Linie vor öffentlichem Release empfohlen**, insbesondere: Weitergabe des Reports durch die Agentur an deren Kunden (Rolle der Agentur, eigene Haftung), Formulierungen „Mangel“ und „Risiko“, Disclaimer-Wortlaut.
2. Die drei „zu verifizieren“-Fakten aus 6.4 vor Aufnahme in den Katalog gegen Primärquelle prüfen und in die KB übernehmen: Garantie-Label mit Stichtag 27.09.2026, PPWR ab 12.08.2026, Geltung § 312k BGB.

Randnotiz (nicht Teil dieses Vorhabens): Die falschen Werkzeugnamen in `.claude/commands/legal-audit-live.md:4` (Abschnitt 4.3) sind in einem separaten Fix zu korrigieren.

Entschieden und aus dieser Liste entfernt: Titel (6.5), Spike Paged.js, Werkzeug-Verfügbarkeit unter Codex und Copilot sowie Retest-Befehl wanderten als Builder-Aufgaben nach Abschnitt 7.

---

## 9. Builder-Check 2026-11-17

Sechs Fragen aus dem Builder-Check und ihre Beantwortung (Calls des Orchestrators, korrigierbar):

1. Wie wird Anwendbarkeit bei unbekannten Intake-Antworten bestimmt, ohne dass das Modell sie rät? Beantwortet in 6.9.1 (dreiwertig, deterministisch aus `applies_if`, ▲ mit „Anwendbarkeit ungeklärt“), Schema in 6.3, Intake in 6.2 Phase 1.
2. Wie läuft die Textprüfung, ohne Evidence und Code zu treffen und ohne ein Gesamturteil zu erraten? Beantwortet in 6.8 (nur `prose`-Felder, Liste verbotener Wendungen, Abbruch mit Feldpfad) und Feldklassen in 6.3.
3. Wo liegen Plugin-Assets, wo der Report-Ordner? Beantwortet in 6.9.3 (`${CLAUDE_PLUGIN_ROOT}`, Auflösung über `__file__`, Copilot-Abbildung korrigieren oder dokumentieren), Constraints in Abschnitt 3.
4. Ist `report.html` eigenständig weitergebbar? Beantwortet in 6.6 (Data-URI für Fonts, Logo, Screenshots, Budget etwa 10 MB mit Warnung).
5. Woher kommt die Akzentfarbe? Beantwortet in 6.6 (`accent_color`, PNG per zlib, SVG-Füllfarben, Rückfrage, Schiefergrau, Kontrast 4.5:1) und Profil in 6.2 Phase 0.
6. In welcher Reihenfolge laufen Schema-Prüfung, `valid_from`-Herabstufung und Render-Invarianten? Beantwortet in 6.9.2 und 6.2 Phase 3 sowie in der `valid_from`-Regel in 6.3.

Zusätzlich vom Nutzer entschieden (entschieden durch Nutzer, 2026-11-17): Titel „Website-CheckUp • Datenschutz, Recht & Sicherheit“ mit Unterzeile „KI-gestützte Ersteinschätzung“ (6.5); Barrierefreiheit läuft ohne BFSG-Pflicht als ▲ „keine gesetzliche Pflicht, empfohlen“, nie als ✕ (6.3, 6.4, Abschnitt 2 Anti-Ziel A2).
