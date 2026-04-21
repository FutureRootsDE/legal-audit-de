---
description: Live-Rechts-Check einer oeffentlichen Website via chrome-devtools-mcp — testet Cookie-Banner-Blocking, Drittanbieter-Leaks VOR Consent, Google-Fonts-Leak, Embed-Verhalten, tatsaechlich gesetzte Cookies. Ergaenzt /legal-audit um die Verhaltens-Dimension.
argument-hint: <url> [--consent=accept|reject|ignore] [--out=<zielordner>]
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, WebFetch, Task, mcp__plugin_chrome-devtools-mcp__chrome-devtools__navigate_page, mcp__plugin_chrome-devtools-mcp__chrome-devtools__new_page, mcp__plugin_chrome-devtools-mcp__chrome-devtools__close_page, mcp__plugin_chrome-devtools-mcp__chrome-devtools__list_network_requests, mcp__plugin_chrome-devtools-mcp__chrome-devtools__get_network_request, mcp__plugin_chrome-devtools-mcp__chrome-devtools__take_screenshot, mcp__plugin_chrome-devtools-mcp__chrome-devtools__take_snapshot, mcp__plugin_chrome-devtools-mcp__chrome-devtools__evaluate_script, mcp__plugin_chrome-devtools-mcp__chrome-devtools__click, mcp__plugin_chrome-devtools-mcp__chrome-devtools__wait_for, mcp__plugin_chrome-devtools-mcp__chrome-devtools__list_console_messages, mcp__plugin_chrome-devtools-mcp__chrome-devtools__emulate
---

# /legal-audit-live

Fuehrt einen **Live-Browser-Check** einer oeffentlichen URL durch. Ergaenzt `/legal-audit` (der nur Code liest) um die **Verhaltens-Dimension**: was laedt die Website **tatsaechlich** im Browser — bevor und nachdem der User den Cookie-Banner bedient?

Typische Findings, die nur dieser Command aufdeckt:
- Google Fonts via `fonts.googleapis.com` trotz Code-Vermerk "self-hosted"
- Analytics-Requests VOR Consent-Banner-Klick
- Meta-Pixel / Google Tag Manager, der beim Laden sofort feuert
- YouTube-Embed ohne `youtube-nocookie.com`
- Cookie-Banner ohne gleichrangigen Ablehnen-Button (visuelle Pruefung)

## Voraussetzungen

- MCP-Server `chrome-devtools` aktiv (`mcp__plugin_chrome-devtools-mcp__*`-Tools verfuegbar).
- Chrome / Chromium installiert (vom MCP-Server selbst gestartet).

## Flags

### `/legal-audit-live <url>`
Standard — 3 Pass-Durchlaeufe:
1. **Erstbesuch ohne Interaktion** — was laedt VOR Consent?
2. **Banner ablehnen** — was laedt NACH "Alle ablehnen"?
3. **Banner akzeptieren** — was laedt NACH "Alle akzeptieren"?

### `/legal-audit-live <url> --consent=accept`
Nur ein Pass mit Akzeptieren. Fuer Tests, die nur den Accept-Zustand brauchen.

### `/legal-audit-live <url> --consent=reject`
Nur ein Pass mit Ablehnen. Haeufigste Variante fuer Abmahn-Risiko-Pruefung.

### `/legal-audit-live <url> --consent=ignore`
Nur ein Pass ohne Banner-Interaktion (reines "Seitenladen"). Oft deckt das die groessten Leaks auf.

### `/legal-audit-live <url> --out=<zielordner>`
Alternativer Output-Ordner. Default: `<cwd>/legal-audit-live/<hostname>-<timestamp>/`.

## Pflichtablauf

### Pass 0 — Vorbereitung

1. URL validieren (muss `https://` oder `http://` sein).
2. Zielordner anlegen:
   ```
   <out>/
   ├── LiveAudit.md         # Finding-Tabelle
   ├── screenshots/
   │   ├── 01-initial.png   # Erstbesuch, vor Interaktion
   │   ├── 02-banner.png    # Cookie-Banner-Screenshot
   │   ├── 03-rejected.png  # Nach "Ablehnen"
   │   └── 04-accepted.png  # Nach "Akzeptieren"
   └── network/
       ├── 01-pre-consent.json
       ├── 02-post-reject.json
       └── 03-post-accept.json
   ```

### Pass 1 — Pre-Consent-Check

1. `mcp__plugin_chrome-devtools-mcp__chrome-devtools__new_page` — neuer, isolierter Browser-Kontext (keine Vor-Cookies).
2. `mcp__plugin_chrome-devtools-mcp__chrome-devtools__navigate_page` → URL.
3. `mcp__plugin_chrome-devtools-mcp__chrome-devtools__wait_for` auf `networkidle` (oder 3s Fallback).
4. `take_screenshot` → `01-initial.png`.
5. `list_network_requests` → als `01-pre-consent.json` speichern.
6. `evaluate_script`:
   ```js
   ({
     cookies: document.cookie,
     localStorage: Object.entries(localStorage),
     sessionStorage: Object.entries(sessionStorage),
     thirdPartyScripts: Array.from(document.querySelectorAll('script[src]'))
       .map(s => s.src)
       .filter(src => !src.includes(location.hostname))
   })
   ```
7. **Analyse:** gab es Requests an bekannte Drittanbieter (siehe Liste unten) VOR Consent? → CRIT.

### Pass 2 — Banner-Analyse

1. `take_snapshot` — DOM-Struktur des Banners extrahieren (uid-Referenzen fuer Klicks).
2. Heuristik zur Button-Erkennung (via `evaluate_script`):
   ```js
   Array.from(document.querySelectorAll('button, a[role="button"]'))
     .map(b => ({
       text: b.innerText.trim(),
       rect: b.getBoundingClientRect(),
       style: {
         bg: getComputedStyle(b).backgroundColor,
         color: getComputedStyle(b).color,
         size: getComputedStyle(b).fontSize
       }
     }))
     .filter(b => b.text.length < 50)
   ```
3. Pruefe **Gleichrangigkeit** von Akzeptieren vs. Ablehnen:
   - Beide Buttons sichtbar auf **first screen** (ohne Scroll)?
   - Aehnliche Groesse, Farbe, Position?
   - Ablehnen NICHT nur als "Einstellungen"-Link versteckt?
   - → Wenn nicht gleichrangig: HIGH-Finding (Planet49, BGH I ZR 7/16).

4. `take_screenshot` mit fokussiertem Banner → `02-banner.png`.

### Pass 3 — Reject-Pfad

1. Falls Banner erkannt: `click` auf "Alle ablehnen"-Button (via uid).
2. `wait_for networkidle`.
3. `take_screenshot` → `03-rejected.png`.
4. `list_network_requests` nach Klick → `02-post-reject.json`.
5. `evaluate_script` (wie Pass 1 fuer Cookies/Storage).
6. **Analyse:** werden NACH Ablehnen weiterhin Drittanbieter-Requests erzeugt? → CRIT.

### Pass 4 — Accept-Pfad

1. `new_page` (frische Session).
2. Navigate + Banner → click "Alle akzeptieren".
3. `wait_for networkidle` + Screenshot + Network-Log → `03-post-accept.json`.
4. Pruefung: nur erwartbare Tools geladen? Oder laufen Tools, die **nicht** in der Datenschutzerklaerung stehen?

### Pass 5 — Google-Fonts-Check

Spezial-Test, da haeufigster Abmahnpunkt (LG Muenchen I 3 O 17493/20):

1. Netzwerk-Log aus Pass 1 (pre-consent) filtern auf:
   ```
   fonts.googleapis.com
   fonts.gstatic.com
   ```
2. Wenn Treffer → **CRIT-Finding**, unabhaengig davon, ob Consent existiert.

### Pass 6 — Embed-Check

1. Im DOM nach `<iframe>` suchen (`evaluate_script`).
2. Pro iframe:
   - `youtube.com/embed` ohne `-nocookie`? → HIGH
   - `player.vimeo.com` ohne dnt=1? → MED
   - `maps.googleapis.com` / `google.com/maps/embed`? → HIGH
   - `twitter.com/intent` / `platform.twitter.com`? → HIGH
   - `instagram.com/embed`? → HIGH

### Pass 7 — Response-Header-Check

1. Home-Response aus Pass 1 extrahieren (`get_network_request` mit uid der Root-Document-Request).
2. Pruefen:
   - `Content-Security-Policy` vorhanden? (LOW falls fehlt)
   - `Strict-Transport-Security`? (MED falls fehlt)
   - `X-Frame-Options` / `frame-ancestors`? (LOW)
   - `Referrer-Policy`? (LOW)

### Pass 8 — Mobile-Emulation

1. `emulate` → iPhone 14 Pro.
2. Navigate neu. Screenshot.
3. Pruefen: Banner touch-freundlich, "Ablehnen" noch sichtbar auf Mobile-Viewport?

## Drittanbieter-Muster (Erkennung in Network-Log)

Der Analyse-Schritt matcht Request-URLs gegen diese Liste. **Voll-Liste** siehe `knowledge/themen/tool-katalog.md`.

### Analytics (Einwilligung erforderlich)
- `google-analytics.com`, `googletagmanager.com`, `g.doubleclick.net`
- `www.googleadservices.com`, `stats.g.doubleclick.net`
- `matomo.*` (falls nicht selbst gehostet + anonymisiert)
- `hotjar.com`, `mouseflow.com`, `clarity.ms`, `inspectlet.com`
- `posthog.com`, `mixpanel.com`, `amplitude.com`, `heap.io`
- `fullstory.com`, `logrocket.com`, `smartlook.com`

### Marketing / Ads
- `facebook.com/tr`, `connect.facebook.net` (Meta Pixel)
- `px.ads.linkedin.com`, `snap.licdn.com` (LinkedIn Insight Tag)
- `analytics.tiktok.com`, `business-api.tiktok.com`
- `pinimg.com`, `ct.pinterest.com`
- `t.co`, `static.ads-twitter.com`

### CDN-Fonts (oft uebersehen)
- `fonts.googleapis.com`, `fonts.gstatic.com` → **immer CRIT**
- `use.typekit.net`, `p.typekit.net` (Adobe Fonts — meist OK wenn AVV)
- `cdn.jsdelivr.net`, `unpkg.com` mit Font-Pfad

### Maps / Embeds
- `maps.googleapis.com`, `maps.gstatic.com`
- `api.mapbox.com` (EU-Region pruefen)
- `www.youtube.com/embed` (statt `-nocookie`)
- `player.vimeo.com` ohne `dnt=1`

### Consent-Management (OK, selbst Pflicht)
- `consent.cookiebot.com`, `app.usercentrics.eu`, `cdn.cookielaw.org` (OneTrust)
- `consent.cookiefirst.com`, `cdn.klaro.org`

## Output: LiveAudit.md Struktur

```markdown
# Live-Audit: <hostname>

**URL:** <url>
**Geprueft am:** <timestamp>
**User-Agent:** <ua>
**Viewport:** 1920x1080 (Desktop) / iPhone 14 Pro (Mobile)

## Findings

| ID | Severity | Kategorie | Beschreibung | Evidence |
|----|----------|-----------|--------------|----------|
| LF-001 | CRIT | Google Fonts | Direkter fonts.googleapis.com-Request bei Seitenlade | network/01-pre-consent.json Zeile 47 |
| ... |

## Netzwerk-Verhalten

### Pre-Consent (ohne Interaktion)
- X Requests total, davon Y an Dritt-Domains
- Bekannte Trackers aktiv: [Liste]

### Nach Ablehnen
- X Requests, davon Y an Dritt-Domains
- **Erwartung:** 0 Tracker
- **Realitaet:** <Liste>

### Nach Akzeptieren
- X Requests, davon Y an Dritt-Domains
- Alle in DSE deklariert? <Liste>

## Cookie-Banner-Bewertung

- Banner erkannt: ja/nein
- Ablehnen gleichrangig: ja/nein
- Pre-ticked Boxes: ja/nein
- Einstellungen-Dialog granular: ja/nein

## Screenshots

- [Initial](screenshots/01-initial.png)
- [Banner](screenshots/02-banner.png)
- [Rejected](screenshots/03-rejected.png)
- [Accepted](screenshots/04-accepted.png)
```

## Nach Abschluss

Gib dem User eine Kurz-Zusammenfassung:
- Anzahl Findings pro Severity (CRIT/HIGH/MED/LOW)
- Top-3 CRIT mit 1-Zeilen-Beschreibung + Pfad zum Evidence
- Vergleich: Pre-Consent vs. Post-Reject (sollte identisch sein bei compliant Seiten)
- Direkter Verweis auf `knowledge/themen/cookie-consent.md` und `knowledge/urteile/eugh-planet49.md`

## Integration mit /legal-audit

Wenn vorher `/legal-audit <pfad>` gelaufen ist:
- Finde die URL in `docs/legal-audit/LegalAudit.md` (Feld "Live-URL") oder frage nach.
- Cross-Reference Pre-Consent-Leaks mit den statischen Findings aus der Codebase.
- Wenn Code selbst-gehostete Fonts suggeriert, Browser aber fonts.googleapis.com laedt → **Finding-Verstaerkung** im Haupt-Audit.

## Disclaimer-Injection

`LiveAudit.md` beginnt mit Disclaimer-Block aus `templates/disclaimer-block.md`. Der `PostToolUse`-Hook validiert das.
