---
aktualisiert: 2026-04-19
quellen-sekundaer:
  - https://usercentrics.com/de/
  - https://www.cookiebot.com/de/
  - https://klaro.org/
  - https://www.osano.com/
  - https://borlabs.io/borlabs-cookie/
  - https://complianz.io/
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung / keine Empfehlung**
>
> Die genannten Consent-Management-Platforms (CMP) sind oeffentlich verfuegbare
> Tools. Ihre **korrekte Konfiguration** liegt beim Nutzer. Auch eine
> "zertifizierte" CMP kann durch falsche Konfiguration DSGVO-widrig sein
> (z.B. Dark Patterns, Pre-Tick, fehlender Ablehnen-Button).
>
> **Stand:** 2026-04-19

# Consent-Management-Platforms (CMP)

## Kategorie-Ueberblick

Eine CMP managt die Einwilligung fuer nicht-notwendige Cookies / Tracking. Sie
erfuellt dabei zwei Pflichten gleichzeitig:
- **§ 25 TDDDG** — Speicherung/Abruf von Informationen in Endgeraeten nur nach Einwilligung
- **DSGVO Art. 6 Abs. 1 lit. a** — Einwilligung fuer PII-Verarbeitung

Eine CMP ist **Pflicht** bei jeder Website, die Tracking, Analytics, Marketing-
Pixel, Embeds mit Tracking (YouTube, Vimeo ohne Nocookie, Maps) oder Fonts
von Drittanbietern einsetzt.

## Tier 1: Enterprise-CMPs

### Usercentrics CMP

| Feld | Wert |
|------|------|
| URL | https://usercentrics.com/de/ |
| Sitz | Muenchen, Deutschland |
| Zielgruppe | KMUs bis Enterprise; Publisher, E-Commerce, Mobile App, Connected TV |
| TCF-Unterstuetzung | **IAB TCF 2.3** (verifiziert 2026-04-19) |
| Reichweite | 2.4 Mio Websites/Apps, 195 Laender, 8.8 Mrd. Consents/Monat |
| Pricing | abgestuft nach Pageviews/Features, ab ca. 15-30 EUR/Monat Basis <<UNVERIFIZIERT>> — Enterprise verhandelt |
| Besonderheit | **TCF-v2.2/v2.3-zertifiziert** — Pflicht bei Ausspielung programmatischer Werbung |
| Google Consent Mode v2 | volle Unterstuetzung |
| Integrationen | 1000+ vordefinierte Services |

### Cookiebot

| Feld | Wert |
|------|------|
| URL | https://www.cookiebot.com/de/ |
| Hersteller | Usercentrics A/S (Cookiebot ist Marke von Usercentrics) |
| Sitz | Daenemark (HR-Nr. 34624607) |
| TCF-Unterstuetzung | **IAB TCF 2.3** + **IAB-zertifiziert** (verifiziert 2026-04-19) |
| Pricing | gestaffelt nach Seiten; kostenloser Tier fuer kleine Websites <<UNVERIFIZIERT exakter Preis>> |
| Besonderheit | automatischer Cookie-Scan; generiert DSE-Abschnitt |
| Beliebt bei | Corporate Websites, Publishing |

### Osano

| Feld | Wert |
|------|------|
| URL | https://www.osano.com/ |
| Sitz | USA (Austin, Texas) |
| Drittland-Thema | US-Anbieter — DPF-Status pruefen |
| Zielgruppe | Mid-Market bis Enterprise |
| Features | CMP + DSAR-Workflow-Automatisierung + Vendor-Risk-Management |
| Pricing | Enterprise, auf Anfrage |
| Beachten | als US-Anbieter Drittland-Pruefung; alternativ EU-CMP bevorzugen |

## Tier 2: Open-Source / Kleinere CMPs

### Klaro

| Feld | Wert |
|------|------|
| URL | https://klaro.org/ |
| Lizenz | BSD-3 (frei fuer kommerzielle Nutzung) |
| Hersteller/Maintainer | KIProtect (Unternehmen) |
| Hosting | Self-Hosted oder als Cloud-Service |
| Features | Privacy by Design, 23 Sprachen, responsive, ~50 KB komprimiert, unterstuetzt 99.9%+ Browser inkl. IE9-11 |
| Zielgruppe | Entwickler mit Fokus auf Datenschutz-Design und Flexibilitaet |
| Besonders gut | eigene Website-/SaaS-Kontrolle, ohne Drittanbieter-Abhaengigkeit |
| TCF-Unterstuetzung | <<NEIN/BEGRENZT — VERIFIKATION AUSSTEHEND>> — nicht primaer als TCF-Provider ausgerichtet |

## Tier 3: WordPress-spezifische CMPs

### Borlabs Cookie

| Feld | Wert |
|------|------|
| URL | https://borlabs.io/borlabs-cookie/ |
| Produktname | Borlabs Cookie(R) 3.0 |
| Hersteller | Borlabs GmbH (Deutschland) |
| Plattform | WordPress-Plugin (Premium, lizenzpflichtig) |
| Aktuelle Version | 3.4 (veroeffentlicht 2026-02-06, verifiziert 2026-04-19) |
| Pricing | Jahreslizenz pro Domain, ab ca. 39-99 EUR/Jahr <<UNVERIFIZIERT>> |
| Besonders gut bei | WordPress-Sites mit komplexem Content (Videos, Maps, externe Widgets) |
| Geo-Blocking | kein TCF-Provider, fuer Small-/Mid-Market ausreichend |

### Complianz

| Feld | Wert |
|------|------|
| URL | https://complianz.io/ |
| Hersteller | Complianz BV |
| Sitz | Kalmarweg 14-5, 9723 JG Groningen, Niederlande |
| Plattform | WordPress-Plugin (Free + Premium), Shopify-App |
| Nutzer | > 1 Mio, Bewertung 4.8/5 (> 1500 Bewertungen) |
| Besonders gut bei | Small Business / Mittelstand mit WordPress |
| Features | Setup-Assistent, weltweite Regelwerke (nicht nur DSGVO), 30-Tage-Geld-zurueck-Garantie |

## Ergaenzende Tools (keine CMPs, aber relevant)

### Google Consent Mode v2

Google Consent Mode **ist keine CMP**, sondern ein Schnittstellen-Standard,
mit dem eine CMP den Consent-Status an Google-Services (GA4, Google Ads)
uebergibt. Zwei Modi:
- **Basic**: Tags laden bei Consent-Denied nicht
- **Advanced**: Tags laden immer, aber uebermitteln cookie-freie Pings, die modelliert werden

Pflicht seit 2024 fuer Google Ads in Europa. Muss mit jeder CMP zusammenarbeiten.

### Consent-O-Matic

- URL: https://consentomatic.au.dk/
- Browser-Erweiterung der Uni Aarhus (Forschungsprojekt)
- **Kein CMP-Ersatz** — Automatisiert das ABLEHNEN von Consent-Bannern fuer **den Endnutzer**
- Interessant fuer Tester / Auditoren, nicht fuer Website-Betreiber

## Auswahl-Kriterien

- [ ] **Plattform**: WordPress → Borlabs/Complianz; Headless/SaaS → Usercentrics/Cookiebot/Klaro
- [ ] **TCF-Zertifizierung noetig?** (wenn programmatische Werbung ueber TCF-Vendoren) → Usercentrics, Cookiebot
- [ ] **Open-Source-Praeferenz** → Klaro (selbst hosten)
- [ ] **DPF/Drittland-Problematik minimieren** → EU-Anbieter bevorzugen (Usercentrics, Cookiebot, Klaro, Complianz, Borlabs)
- [ ] **Traffic-Volumen** — kleine Sites profitieren von Free-Tiers (Cookiebot, Complianz Free)
- [ ] **Sprachen** — Internationale Websites brauchen i18n (Usercentrics, Klaro gut)
- [ ] **Consent-Log-Speicherung** — Nachweis-Pflicht Art. 7 Abs. 1 DSGVO
- [ ] **A/B-Testing** des Banners fuer Opt-In-Quote (Usercentrics bietet das)

## Typische Konfigurations-Fehler

### CRIT (macht die gesamte CMP wertlos)

- **Pre-Tick** bei Marketing-Kategorien → EuGH Planet49 C-673/17 verletzt
- **Kein Ablehnen-Button** oder nur im Untermenue → BGH Cookie-Einwilligung verletzt
- **Tracking-Scripts im `<head>` vor CMP-Init** (GA4 laedt vor Consent-Check)
- **Consent-Mode nicht aktiviert** trotz Google-Services
- **Widerruf schwieriger als Einwilligung** (Button versteckt)

### HIGH

- **Cookie-Kategorien zu grob** ("Marketing-Cookies" ohne Erklaerung welcher Anbieter)
- **Third-Party-Embeds vor Consent** (YouTube-iframe ohne Nocookie)
- **Google Fonts direkt** (LG Muenchen I 3 O 17493/20)
- **Fonts per CDN geladen** (selbst wenn Google Consent Mode aktiv)

### MED

- Consent-Log nur clientseitig (LocalStorage ohne Server-Backup)
- Cookie-Banner erscheint auf Legal-Pages (Impressum, DSE) — sollte i.d.R. nicht consent-pflichtig sein
- Geo-Targeting: EU-User bekommen Banner, US-User nicht (das ist ok, wenn nur EU-DSGVO anwendbar)

## Migration zwischen CMPs

Wenn ein Wechsel ansteht:
1. Alte Consent-Logs exportieren (DSAR-Relevanz)
2. Cookie-Inventar uebernehmen
3. Testphase mit Canary-Deploy (1% Traffic)
4. Datenschutzerklaerung aktualisieren (neue CMP nennen)
5. Alte Scripts entfernen (kein Zombie-Code)

## Siehe auch

- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[gesetze/tdddg]] — § 25
- [[gesetze/dsgvo]] — Art. 6, 7, 13
- [[urteile/eugh-planet49]]
- [[urteile/bgh-cookie-einwilligung]]
- [[urteile/bgh-google-fonts]]
- [[anwaelte-tools/tools-scanner]]
- [[anwaelte-tools/tools-generatoren]]
