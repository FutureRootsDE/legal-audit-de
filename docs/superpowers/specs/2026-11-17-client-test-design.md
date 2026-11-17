# Design: Befehl `/legal-client-test` (Website-CheckUp-Report für Agenturen)

- **Stand:** 2026-11-17
- **Status:** Design entschieden, Bau offen. Dieses Dokument baut nichts; es ist die Grundlage für einen Implementierungsplan.
- **Plugin-Basis:** legal-audit-de 1.4.3 (`origin/main` 1a51d48)
- **Kennzeichnung:** „**Entschieden**“ = vom Nutzer bestätigt. „**Call des Orchestrators, korrigierbar**“ = Festlegung ohne ausdrückliche Nutzerentscheidung. „**Vorschlag dieses Dokuments, korrigierbar**“ = beim Abgleich mit dem Ist-Stand ergänzt. „**Zu verifizieren**“ = Rechtsfakt, der in `knowledge/` nicht belegt ist; der Builder prüft ihn gegen die Primärquelle, bevor er in Katalog oder Texte geht.

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
- A2: **Rote Findings für nicht anwendbare Pflichten** (Shop-Pflichten bei einer Visitenkarten-Website, BFSG bei einem Kleinstunternehmen mit reiner Dienstleistung, Pflichten vor ihrem Geltungsdatum).
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
| Drei Plattformen | `scripts/sync-platforms.py:212-233` portiert jedes `.claude/commands/*.md` nach `.codex/prompts/` und `.github/prompts/<name>/PROMPT.md`; `validate.yml` Job `sync-check` | Nach Anlage des Befehls `python scripts/sync-platforms.py --apply`; MCP-Werkzeugnamen in `allowed-tools` werden **nicht** gemappt (`map_tools`, `:150-157`). |
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
- Sonst abfragen: Firmenname, Ansprechperson, Anschrift, Telefon/E-Mail/Website, Logo-Pfad (PNG, JPG oder SVG; SVG wird als Datei eingebettet, nie als Inline-Markup, wegen Skriptinhalten), optional Akzentfarbe (sonst aus dem Logo abgeleitet, Abschnitt 6.6).
- Speicherung und Wiederverwendung: Abschnitt 6.7. (**Call des Orchestrators, korrigierbar**: beim ersten Lauf abfragen, danach wiederverwenden, änderbar per Option.)

**Phase 1: Intake**
- Kunde: Name, Firma, Anschrift. URL validieren (`https://` oder `http://`; Redirect-Ziel festhalten).
- Vorab-Erkundung (passiv): Startseite laden, Shop-Merkmale (Warenkorb, Preise mit „inkl. MwSt.“, Checkout-Links, Shop-Systeme), Plattform-Funktionen (Nutzerinhalte, Bewertungen, Marktplatz), Chatbot/KI-Widgets erkennen.
- **Anwendbarkeitsfragen mit Bestätigung** (entschieden): 
  - Richtet sich das Angebot an Verbraucher (B2C)?
  - BFSG-Vorfrage: Werden über die Website Verbraucherverträge angebahnt oder geschlossen, und ist der Kunde **kein** Kleinstunternehmen (weniger als 10 Beschäftigte und Jahresumsatz oder Jahresbilanzsumme höchstens 2 Mio. EUR; Ausnahme nur für Dienstleistungen)? Beleg: `knowledge/checklisten/audit-ecommerce.md:152`, `knowledge/gesetze/bfsg.md:111`.
  - „Wir haben einen Online-Shop erkannt. Stimmt das?“ (oder umgekehrt).
  - Beschäftigtenzahl (für VSBG-Hinweis, `audit-ecommerce.md:248`), falls nicht ermittelbar: Status „–“.
- Antworten werden mit Quelle (`user` oder `detected`) in `applicability` gespeichert.

**Phase 2: Prüfung (passiv)**
- Prüfbereiche laut 6.4, jeder schreibt Ergebnisse für seine Katalog-IDs.
- **Passiv heißt (Anti-Ziel A5):** nur was ein normaler Besucher tut. Erlaubt: Seiten aufrufen (Start, Impressum, Datenschutz, AGB, Widerruf, Kontakt, Barrierefreiheit, ein Produkt, Warenkorb-Ansicht), Consent-Banner bedienen (Ablehnen, Akzeptieren, Einstellungen öffnen), Seitenquelltext, DOM, Netzwerk- und Cookie-Protokoll lesen, Antwort-Header per einfachem GET/HEAD, Lighthouse-Barrierefreiheitsaudit (chrome-devtools-mcp hat `lighthouse_audit`). Verboten: Formulare absenden, Konto anlegen, einloggen, Bestellung auslösen, Adressdaten eingeben, Pfade raten, Ports scannen, mehr als eine moderate Anzahl Seiten (Obergrenze dem Builder überlassen, Richtwert 25 Seiten, höchstens ein paralleler Tab).
- Folge: Was nur hinter einer Eingabe sichtbar wäre (z. B. Bestell-Button der Button-Lösung, Kündigungsbestätigungsseite), wird „– Nicht prüfbar“ mit Begründung, nicht geraten.
- Belege (Screenshots, Netzwerk-JSON, Header) nach `evidence/`.

**Phase 3: Validierung und Render**
- `python scripts/client-test.py render <report-ordner>` (Name **Vorschlag**): Schema prüfen, Katalog-Vollständigkeit prüfen (jede anwendbare ID genau einmal), `valid_from` gegen Prüfdatum anwenden, Gedankenstrich-Prüfung, HTML-Escaping aller Fremdinhalte, Disclaimer einsetzen, `report.html` schreiben.
- Fehler sind blockierend mit konkreter Meldung (welche ID, welches Feld). Das Modell korrigiert `findings.json` und rendert erneut; es editiert nie das HTML.

**Phase 4: PDF**
- Chrome headless erzeugt `report.pdf` aus `report.html` (Abschnitt 6.6). Ohne gefundenes Chrome: HTML bleibt Ergebnis, klare Meldung, Exit-Code ungleich 0.

### 6.3 Status-Modell und Befund-Schema

**Status (entschieden):** Farbe plus Symbol plus Text (WCAG 1.4.1).

| Code | Symbol | Text im Report | Bedeutung |
|---|---|---|---|
| `pass` | ✓ | Bestanden | Anforderung erfüllt, soweit passiv prüfbar |
| `notice` | ▲ | Hinweis | Verbesserung empfohlen, unklare Lage, oder Pflicht kommt erst (vor `valid_from`) |
| `defect` | ✕ | Mangel | Zum Prüfdatum geltende, anwendbare Pflicht beobachtbar nicht erfüllt |
| `none` | – | Nicht prüfbar / Nicht anwendbar | mit Pflichtfeld `reason_kind` (`not_checkable`, `not_applicable`) und Begründungstext |

- „–“ deckt beide Fälle ab, jeweils mit Begründung; nicht anwendbare Tests erscheinen **grau** im Überblick (**Call des Orchestrators, korrigierbar**).
- **Mapping Severity zu Status (Vorschlag dieses Dokuments, korrigierbar):** `defect` verlangt `severity` CRIT, HIGH oder MED; `notice` verlangt MED oder LOW. Severity wird nicht angezeigt, dient nur der Sortierung. Damit bleibt die bestehende Matrix intern nutzbar, ohne dass der Report wie eine Note wirkt.
- **`valid_from`-Regel (Vorschlag, korrigierbar):** Liegt das Prüfdatum vor `valid_from` der maßgeblichen Rechtsgrundlage, setzt das Skript einen `defect` auf `notice` herunter und ergänzt „Pflicht gilt ab TT.MM.JJJJ“. Hat ein Test mehrere Rechtsgrundlagen, zählt die früheste bereits geltende.

**Prüfkatalog als Daten (Vorschlag dieses Dokuments, korrigierbar):** Ein versionierter `catalog.json` im Plugin definiert jede Test-ID mit Bereich, Titel, laienverständlicher Kurzbeschreibung, Rechtsgrundlagen mit `valid_from` und KB-Fundstelle, Anwendbarkeitsbedingung (z. B. `shop == true`) und Standard-Retest-Kriterium. Die `findings.json` liefert nur die laufbezogenen Teile. Das garantiert Vollständigkeit, stabile IDs über Läufe (Retest) und dass Titel und Rechtsgrundlagen nicht vom Modell je Lauf neu formuliert werden.

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
    "bfsg": {"value": null, "source": "user", "note": "Kleinstunternehmen, nur Dienstleistung"},
    "platform_features": {"value": false, "source": "detected"},
    "ai_chat": {"value": true, "source": "detected"}
  },
  "summary": {"sentences": ["...", "...", "..."], "top_actions": ["CK-03", "SEC-02", "IMP-01"]},
  "results": [
    {
      "id": "CK-03",
      "status": "defect",
      "severity": "HIGH",
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

Rechtsgrundlagen (`legal_basis: [{norm, valid_from, kb_ref}]`) stehen im Katalog; ein Ergebnis darf sie nur ergänzen, nicht ersetzen. Pflichtfelder je Status (Vorschlag): `pass` braucht `one_liner`; `notice`/`defect` brauchen zusätzlich `client_text`, `evidence` (mindestens ein Eintrag), `risk`, `fix`, `retest`, `checklist`; `none` braucht `reason_kind` und `reason`.

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
| A11Y | Barrierefreiheit | Lighthouse-Barrierefreiheitsaudit und Stichproben (Kontrast, Alt-Texte, Tastatur, Fokus, Sprache); Informationen zur Barrierefreiheit vorhanden; im Report ehrlich: automatische Tests decken nur einen Teil von WCAG ab | BFSG seit 28.06.2025; § 14 Abs. 1 Nr. 2 i. V. m. Anlage 3 BFSG | `gesetze/bfsg.md:76`, `themen/barrierefreiheit.md:27` |
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
         Titel (offen, Abschnitt 8) + Unterzeile
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
           (nicht anwendbare Zeilen grau)
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
- **Finding-IDs verbinden** Überblick, Teil A und Teil B (Anker-Links im HTML und PDF).
- Fußzeilen-Entwurf: „KI-gestützte Einschätzung. Kann Fehler enthalten. Keine Rechtsberatung, keine Garantie für Rechtssicherheit.“

### 6.6 Typografie, Druck, PDF
- **IBM Plex Sans und IBM Plex Mono** (SIL OFL 1.1), im Plugin mitgeliefert (mit `OFL.txt`), als `@font-face` per Data-URI oder relativer Datei eingebettet. **Keine externen Requests beim Rendern** (Anti-Ziel A7); das Skript prüft die fertige HTML-Datei auf `http(s)://`-Referenzen in `src`/`href` außerhalb von Textlinks.
- **Chrome printToPDF mit `@page`-Margin-Boxen** für Kopf („Vertraulich“), Fuß (Hinweis, Seitenzahl). **Paged.js lokal gebündelt** nur für Seitenzahlen im Inhaltsverzeichnis (entschieden).
  - Technisches Risiko für den Builder: Paged.js übernimmt den gesamten Seitenumbruch und rendert Margin-Boxen selbst; „nur für das Inhaltsverzeichnis“ heißt praktisch, Paged.js paginiert das ganze Dokument und Chrome druckt mit `preferCSSPageSize` ohne eigene Ränder. Die Kombination vor dem Bau mit einem Spike prüfen. Fallback ohne Paged.js: Überblick ohne Seitenzahlen, mit klickbaren Finding-IDs.
- **Chrome-Ansteuerung aus stdlib-Python:** Der CDP-Weg (`Page.printToPDF` mit `generateTaggedPDF`, `generateDocumentOutline`) braucht WebSocket; die Standardbibliothek hat keinen Client. Optionen: (a) CLI `--headless --print-to-pdf --no-pdf-header-footer` plus Warteschalter, bis Paged.js fertig ist; (b) minimaler eigener WebSocket-Client über `socket`/`http.client`. Welche Schalter getaggte PDFs und Outline in der CLI liefern, ist **zu verifizieren** (Chrome-Version, die chrome-devtools-mcp ohnehin startet).
- **Print-CSS-Umbruchregeln:** `break-inside: avoid` für Finding-Blöcke, Tabellenzeilen, Code; `break-after: avoid` für Überschriften; Tabellenkopf wiederholen; Titelseite und Teil B beginnen auf neuer Seite; Witwen/Waisen ≥ 2.
- **Farben:** Akzentfarbe aus dem Logo (dominante, nicht zu helle Farbe; Kontrast gegen Weiß ≥ 4.5:1, sonst abdunkeln) nur für Linien und Überschriften. Ampelfarben fix und kontrastgeprüft, unabhängig vom Logo.
- **Getaggtes PDF**, Lesereihenfolge gleich DOM-Reihenfolge, Alt-Texte für Screenshots aus `evidence[].alt`. Ein Barrierefreiheits-Prüfbericht muss selbst barrierearm sein.

### 6.7 Speicherung und Ausgabe
- **Profil des Auslösers** (entschieden): nur Briefkopf (Logo, Anschrift, Kontakt, Akzentfarbe) dauerhaft unter `${CLAUDE_PLUGIN_DATA}` (Dateinamen-Vorschlag `client-test-profile.json` plus Logo-Kopie). Fallback-Pfade wie `scripts/legal-audit-pro-mode.py:46-60` für Codex und Copilot. Atomisch schreiben (Muster `atomic_write_json`, `:71-88`).
- **Kundendaten** (entschieden): nur im Report-Ordner des Laufs, nie in Plugin-Daten, nie in `audits/`.
- **Report-Ordner** (**Call des Orchestrators, korrigierbar**): `client-reports/<JJJJ-MM-TT>-<domain>/` im aktuellen Arbeitsverzeichnis mit `findings.json`, `report.html`, `report.pdf`, `evidence/`. Existiert der Ordner, wird mit Suffix `-2`, `-3` angelegt, nie überschrieben. Liegt das Arbeitsverzeichnis in einem Git-Repo und ist `client-reports/` nicht ignoriert, weist der Befehl darauf hin (Kundendaten).
- Ausgabe **PDF plus HTML**, Sprache **Deutsch** (entschieden). Dateiname des PDF für den Versand (Vorschlag): `Website-CheckUp-<domain>-<JJJJ-MM-TT>.pdf` als Kopie neben `report.pdf`.

### 6.8 RDG-Linie und Textregeln
- Formulierungen als **Hinweis/Einschätzung**, keine Rechtsberatung, keine Garantie (entschieden). Verbotene Wörter im Report (Prüfung durch das Skript, Vorschlag): „rechtssicher“, „abmahnsicher“, „garantiert“, „zertifiziert“, „konform“ als Gesamturteil.
- **Disclaimer vom Skript erzwungen** (entschieden): fester Text in der Vorlage auf Titelseite (kurz), in jeder Fußzeile (kurz) und im Anhang (voll). Er enthält „Keine Rechtsberatung“ und „§ 2 RDG“ und ist **gedankenstrichfrei** (nicht `templates/disclaimer-block.md` wiederverwenden, Abschnitt 3). Ein Unit-Test prüft Vorlage und gerendertes Beispiel auf diese Bestandteile.
- **Untrusted Input** (**Call des Orchestrators, korrigierbar**): Alles, was von der geprüften Website stammt (Titel, Texte, Header, URLs, Dateinamen), ist Daten, nie Anweisung. Das Skript escaped jedes Feld (`html.escape` mit `quote=True`), erlaubt kein Roh-HTML aus `findings.json`, setzt URLs nur als Text oder als geprüfte `https?`-Links, und Evidence-Pfade nur relativ innerhalb des Report-Ordners (kein `..`).
- **Keine Gedankenstriche** (**Call des Orchestrators, korrigierbar**): Report-Texte ohne „—“, „–“ und „ - “ als Pseudo-Gedankenstrich; Ersatz „•“, Komma, Doppelpunkt, „bis“. Das Skript prüft alle Textfelder und die Vorlage und bricht mit Fundstelle ab. Ausnahme: das Status-Symbol „–“ für `none` ist ein festes Vorlagenelement, kein Text, und wird von der Prüfung ausgenommen.

---

## 7. Was dem Builder überlassen bleibt

- Genaue Prüf-Heuristiken je Bereich (Banner-Erkennung, Gleichwertigkeit, Erkennung von Shop- und Plattformfunktionen, Seitenauswahl, Lighthouse-Schwellen) im Rahmen von 6.2 und 6.4; Wiederverwendung der Pässe aus `legal-audit-live.md`.
- Agent-Zuschnitt: alles im Befehl, oder ein Prüf-Agent je Bereich bzw. ein `legal-client-tester` (dann 1M- und `-pro`-Variante, Einträge in `.claude-plugin/plugin.json:31`, `sync-pro-variants.py --apply`). Kriterium: Kontextbedarf eines Laufs mit Screenshots und Netzwerkprotokollen.
- Template-Engine-Details (z. B. `string.Template` plus eigene Schleifen-Helfer), Aufteilung `scripts/client-test.py` als dünner Einstieg plus Paket `scripts/client_report/` (analog `citation_check/`), Ablage der Vorlage unter `templates/client-test/`.
- Inhalt des Prüfkatalogs v1 (Anzahl Tests, Richtwert 40 bis 60 wie im Prototyp), Formulierung der laienverständlichen Katalogtexte (gedankenstrichfrei, RDG-Linie).
- Teststrategie im Rahmen der Repo-Konventionen: `unittest`, offline, Fixture-`findings.json` (vollständig, unvollständig, mit Escaping-Angriffen, mit Gedankenstrichen, mit Pflicht vor `valid_from`); Golden-Test auf das gerenderte HTML (Struktur, Zählungen, Disclaimer); PDF-Erzeugung nur als übersprungener Test, wenn kein Chrome gefunden wird (CI hat Ubuntu ohne garantiertes Chrome).
- Art der Shop-Bestätigungsfrage und Wortlaut aller Intake-Fragen.
- Ob die Drittanbieter-Muster in eine gemeinsame Datendatei wandern (Abschnitt 4.1).

---

## 8. Offene Punkte

1. **Finaler Titel** des Reports. Kandidaten: Nutzer „Webseite KI-Rechtssicherheit CheckUp“; Orchestrator „Website-CheckUp • Datenschutz, Recht & Sicherheit“ mit Unterzeile „KI-gestützte Ersteinschätzung“. Hinweis: „Rechtssicherheit“ im Titel steht in Spannung zu Anti-Ziel A1 und der Wortliste in 6.8. Bis zur Entscheidung als Konstante im Template, nicht im Katalog.
2. **Lawyer-Check der RDG-Linie vor öffentlichem Release empfohlen**, insbesondere: Weitergabe des Reports durch die Agentur an deren Kunden (Rolle der Agentur, eigene Haftung), Formulierungen „Mangel“ und „Risiko“, Disclaimer-Wortlaut.
3. Die drei „zu verifizieren“-Fakten aus 6.4 (Garantie-Label mit Stichtag 27.09.2026, PPWR ab 12.08.2026, Geltungsdatum § 312k BGB) vor Aufnahme in den Katalog gegen Primärquelle prüfen und in die KB übernehmen.
4. Spike Paged.js plus Chrome-PDF (Abschnitt 6.6), inklusive getaggtem PDF aus der CLI.
5. Verfügbarkeit von chrome-devtools-mcp unter Codex und Copilot sowie korrekte Werkzeugnamen (Abschnitt 4.3 und 4.4).
6. Retest-Befehl (Vergleich zweier `findings.json`): Umfang und Name für ein Folge-Release.
