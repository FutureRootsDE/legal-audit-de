---
aktualisiert: 2026-11-15
quellen-sekundaer:
  - https://usercentrics.com/de/
  - https://www.cookiebot.com/de/
  - https://klaro.org/
  - https://www.osano.com/
  - https://borlabs.io/borlabs-cookie/
  - https://complianz.io/
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung / keine Empfehlung**
>
> Die genannten Consent-Management-Platforms (CMP) sind oeffentlich verfuegbare
> Tools. Ihre **korrekte Konfiguration** liegt beim Nutzer. Auch eine
> "zertifizierte" CMP kann durch falsche Konfiguration DSGVO-widrig sein
> (z.B. Dark Patterns, Pre-Tick, fehlender Ablehnen-Button).
>
> **Stand:** 2026-11-14

# Consent-Management-Platforms (CMP)

## Kategorie-Ueberblick

Eine CMP managt die Einwilligung fuer nicht-notwendige Cookies / Tracking. Sie
erfuellt dabei zwei Pflichten gleichzeitig:
- **§ 25 TDDDG** — Speicherung/Abruf von Informationen in Endgeraeten nur nach Einwilligung
- **DSGVO Art. 6 Abs. 1 lit. a i. V. m. Art. 7** — Einwilligung als Rechtsgrundlage fuer die anschliessende Verarbeitung personenbezogener Daten (Nachweispflicht Art. 7 Abs. 1)
- **§ 26 TDDDG / EinwV** — anerkannte Dienste zur Einwilligungsverwaltung (Einwilligungsverwaltungsverordnung vom 6. Februar 2025, BGBl. 2025 I Nr. 32, in Kraft seit 01.04.2025); Einbindung fuer Website-Betreiber freiwillig

Wer Tracking, Analytics, Marketing-Pixel oder Embeds mit Tracking (YouTube,
Vimeo ohne Nocookie, Maps) einsetzt, muss die Einwilligung (§ 25 Abs. 1 TDDDG)
vorab einholen und nachweisen koennen. Eine CMP ist dafuer das uebliche Mittel,
aber nicht gesetzlich vorgeschrieben. Fonts von Drittanbietern lassen sich
durch Selbst-Hosten ohne Einwilligung einbinden.

## Tier 1: Enterprise-CMPs

### Usercentrics CMP

| Feld | Wert |
|------|------|
| URL | https://usercentrics.com/de/ |
| Sitz | Muenchen, Deutschland |
| Zielgruppe | KMUs bis Enterprise; Publisher, E-Commerce, Mobile App, Connected TV |
| TCF-Unterstuetzung | IAB TCF laut Anbieter; unterstuetzte Version und Zertifizierungsstatus in der IAB-CMP-Liste pruefen |
| Reichweite | 2.4 Mio Websites/Apps, 195 Laender, 8.8 Mrd. Consents/Monat |
| Pricing Web CMP (Stand 2026-05-08) | **Free** (bis 1.000 Sitzungen/Monat, 1 Domain) / **Essential** 7 EUR/Monat (bis 1.500 Sessions) / **Plus** 15 EUR/Monat (bis 3.000) / **Pro** 30 EUR/Monat (bis 15.000) / **Business** 50 EUR/Monat (bis 50.000) / **Corporate** auf Anfrage (ab 1 Mio Sessions). App-CMP: ab 50 EUR/Monat. Quelle: usercentrics.com/de/preise/ |
| Besonderheit | IAB TCF: keine gesetzliche Pflicht; ggf. von Werbeplattformen gefordert |
| Google Consent Mode v2 | volle Unterstuetzung |
| Integrationen | 1000+ vordefinierte Services |

### Cookiebot

| Feld | Wert |
|------|------|
| URL | https://www.cookiebot.com/de/ |
| Hersteller | Usercentrics A/S (Cookiebot ist Marke von Usercentrics) |
| Sitz | Daenemark (HR-Nr. 34624607) |
| TCF-Unterstuetzung | **IAB TCF 2.3** + **IAB-zertifiziert** (verifiziert 2026-04-19) |
| Pricing (Cookiebot Core, Stand 2026-05-08) | **Core Free** unbegrenzt nutzbar (bis 50 Unterseiten, 1 Domain) / **Premium Lite** 7 EUR/Monat (bis 50 Subpages, 1 Domain) / **Premium Small** 15 EUR/Monat (bis 350 Subpages, 4+ Domains) / **Premium Medium** 30 EUR/Monat (bis 3.500) / **Premium Large** 50 EUR/Monat (bis 7.000) / **Premium Extra Large** 90 EUR/Monat (> 7.000). Quelle: cookiebot.com/de/pricing/ |
| Besonderheit | automatischer Cookie-Scan; generiert DSE-Abschnitt |
| Beliebt bei | Corporate Websites, Publishing |

### Osano

| Feld | Wert |
|------|------|
| URL | https://www.osano.com/ |
| Sitz | USA (Osano, Inc., Public Benefit Corp); zusaetzliche Gesellschaften "Osano International Compliance Services LTD" und "Osano UK Compliance LTD". Konkrete Stadt-Adresse auf osano.com/plans am 2026-11-14 nicht oeffentlich ausgewiesen. |
| Drittland-Thema | US-Anbieter — DPF-Status pruefen |
| Zielgruppe | Mid-Market bis Enterprise |
| Features | CMP + DSAR-Workflow-Automatisierung + Vendor-Risk-Management |
| Pricing (Stand 2026-05-08) | Self-Service-Plaene + Enterprise auf Anfrage; 30-Tage-Trial. Konkrete Preisstaffeln werden auf der Pricing-Seite nicht oeffentlich gelistet (osano.com/plans). |
| Beachten | als US-Anbieter Drittland-Pruefung; alternativ EU-CMP bevorzugen |

## Tier 2: Open-Source / Kleinere CMPs

### Klaro

| Feld | Wert |
|------|------|
| URL | https://klaro.org/ |
| Lizenz | BSD-3 (frei fuer kommerzielle Nutzung) — verifiziert 2026-05-08 |
| Hersteller/Maintainer | KIProtect (Unternehmen) |
| Hosting | Self-Hosted (Open-Source) oder als gehosteter Service mit Server-Funktionalitaet, Integrations-Beratung, Priority Support, Continuous Monitoring |
| Features | Privacy by Design, 23 Sprachen, responsive, ~50 KB komprimiert, unterstuetzt 99.9%+ Browser inkl. IE9-11 |
| Zielgruppe | Entwickler mit Fokus auf Datenschutz-Design und Flexibilitaet |
| Besonders gut | eigene Website-/SaaS-Kontrolle, ohne Drittanbieter-Abhaengigkeit |
| TCF-Unterstuetzung | Nicht primaer als TCF-Provider ausgerichtet; Klaro unterstuetzt Google Consent Mode v2; eine offizielle IAB-TCF-Zertifizierung ist auf klaro.org nicht ausgewiesen (Stand 2026-05-08). |
| Pricing | Open-Source-Edition kostenlos; Cloud-Service: Tarife oeffentlich unter klaro.org/pricing |

## Tier 3: WordPress-spezifische CMPs

### Borlabs Cookie

| Feld | Wert |
|------|------|
| URL | https://borlabs.io/borlabs-cookie/ |
| Produktname | Borlabs Cookie(R) 3.0 |
| Hersteller | Borlabs GmbH (Deutschland) |
| Plattform | WordPress-Plugin (Premium, lizenzpflichtig) |
| Aktuelle Version | Aktuelle Versionsnummer laut Changelog des Herstellers (borlabs.io/borlabs-cookie/changelog/) |
| Pricing | Jahreslizenzen in sechs Stufen (49 / 79 / 109 / 179 / 229 / 499 EUR/Jahr, netto), inklusive 1 Jahr Updates und Support; Staffel und Leistungsumfang laut Anbieterseite borlabs.io/borlabs-cookie/prices/ |
| Besonders gut bei | WordPress-Sites mit komplexem Content (Videos, Maps, externe Widgets) |
| Geo-Blocking | unterstuetzt IAB TCF 2.4 laut Hersteller |

### Complianz

| Feld | Wert |
|------|------|
| URL | https://complianz.io/ |
| Hersteller | Complianz BV (Teil von iubenda, verifiziert 2026-11-14) |
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

Keine gesetzliche Pflicht, sondern Vorgabe von Google fuer Google-Tags im EWR; Einzelheiten laut Google-Hilfe zum Einwilligungsmodus pruefen. Die CMP muss die Signale uebergeben koennen.

### Consent-O-Matic

- URL: https://consentomatic.au.dk/
- Browser-Erweiterung der Uni Aarhus (Forschungsprojekt)
- **Kein CMP-Ersatz** — Automatisiert das ABLEHNEN von Consent-Bannern fuer **den Endnutzer**
- Interessant fuer Tester / Auditoren, nicht fuer Website-Betreiber

## Auswahl-Kriterien

- [ ] **Plattform**: WordPress → Borlabs/Complianz; Headless/SaaS → Usercentrics/Cookiebot/Klaro
- [ ] **TCF-Zertifizierung noetig?** (wenn programmatische Werbung ueber TCF-Vendoren) → Usercentrics, Cookiebot, Borlabs (Zertifizierungsstatus jeweils in der IAB-CMP-Liste pruefen)
- [ ] **Open-Source-Praeferenz** → Klaro (selbst hosten)
- [ ] **DPF/Drittland-Problematik minimieren** → Anbieter mit EU-Sitz (Usercentrics, Cookiebot, Klaro, Complianz, Borlabs) als Ausgangspunkt; Unterauftragsverarbeiter und Hosting im AVV pruefen, ein EU-Sitz schliesst Drittlanduebermittlungen nicht aus. Self-Hosting (Klaro, Borlabs) vermeidet den Auftragsverarbeiter ganz.
- [ ] **Traffic-Volumen** — kleine Sites profitieren von Free-Tiers (Cookiebot, Complianz Free)
- [ ] **Sprachen** — Internationale Websites brauchen i18n (Usercentrics, Klaro gut)
- [ ] **Consent-Log-Speicherung** — Nachweis-Pflicht Art. 7 Abs. 1 DSGVO
- [ ] **A/B-Testing** des Banners fuer Opt-In-Quote (Usercentrics bietet das)

## Typische Konfigurations-Fehler

### CRIT (macht die gesamte CMP wertlos)

- **Pre-Tick** bei Marketing-Kategorien → EuGH Planet49 C-673/17 verletzt
- **Kein gleichwertiger Ablehnen-Weg auf der ersten Ebene**: Risiko fuer die Freiwilligkeit der Einwilligung (Art. 4 Nr. 11, Art. 7 DSGVO i. V. m. § 25 Abs. 1 TDDDG). BGH I ZR 7/16 betrifft das voreingestellte Haekchen und traegt diese Aussage nicht.
- **Tracking-Scripts im `<head>` vor CMP-Init** (GA4 laedt vor Consent-Check)
- **Widerruf schwieriger als Einwilligung** (Button versteckt)

### HIGH

- **Cookie-Kategorien zu grob** ("Marketing-Cookies" ohne Erklaerung welcher Anbieter)
- **Third-Party-Embeds vor Consent** (z. B. YouTube-iframe ohne Zwei-Klick- bzw. Vorschau-Loesung; der Nocookie-Modus allein genuegt nicht)
- **Google Fonts direkt** (LG Muenchen I 3 O 17493/20, Endurteil vom 20.01.2022)
- **Fonts von Drittservern ohne Rechtsgrundlage geladen** (unabhaengig vom Google Consent Mode)

### MED

- Einwilligungsnachweis nicht gesichert (Art. 7 Abs. 1, Art. 5 Abs. 2 DSGVO), z. B. Consent-Log nur clientseitig und Einwilligungsprozess nicht dokumentiert
- Cookie-Banner verdeckt Impressum oder Datenschutzerklaerung (leichte Erkennbarkeit und Erreichbarkeit der Pflichtangaben beeintraechtigt)
- Geo-Targeting (Banner nur fuer EU-Nutzer): nur vertretbar, wenn weder die DSGVO noch § 25 TDDDG auf die uebrigen Nutzer anwendbar ist. Bei Niederlassung in der EU gilt die DSGVO unabhaengig vom Aufenthaltsort der Nutzer (Art. 3 Abs. 1 DSGVO).
- **Consent Mode nicht aktiviert** trotz Google-Diensten: fuer sich kein Verstoss gegen § 25 Abs. 1 TDDDG oder die DSGVO, sondern Verstoss gegen Vorgaben von Google (Vertragsrisiko)

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

## Aenderungsvermerk

- **2026-11-14** (Batch E3, Live-Pruefung): Jeden CMP-Eintrag live abgerufen. Usercentrics-Preisstaffel (Free / 7 / 15 / 30 / 50 EUR + Corporate) gegen usercentrics.com/de/preise/ bestaetigt. Cookiebot-Staffel (Free / 7 / 15 / 30 / 50 / 90 EUR, Premium Small aufwaerts je Domain) gegen cookiebot.com/de/pricing/ bestaetigt; Zugehoerigkeit zu Usercentrics A/S erneut bestaetigt. Osano-Sitz prazisiert: osano.com/plans nennt nur "Osano, Inc., Public Benefit Corp" plus UK- und International-Compliance-Gesellschaft, keine Stadt mehr (alte Angabe "Austin, Texas" entfernt). Klaro (klaro.org): BSD-3-Lizenz, Maintainer KIProtect, keine IAB-TCF-Zertifizierung bestaetigt. Borlabs-Produktseite zeigt aktuell weder konkrete Version noch die Jahres-Staffel, nur "ab 49 EUR" — Markierung als VERIFIKATION AUSSTEHEND gesetzt. Complianz (complianz.io): Firmensitz Groningen bestaetigt, neu Zugehoerigkeit zu iubenda eingetragen. Consent-O-Matic (consentomatic.au.dk): erreichbar, Aarhus-University-Entwicklung bestaetigt.
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1): CMP als uebliches Mittel statt Pflicht (§ 25 Abs. 1 TDDDG); Klaro-Tarife oeffentlich; Borlabs unterstuetzt IAB TCF 2.4 laut Hersteller und ist in der TCF-Auswahl ergaenzt; Borlabs-Versionsnummer durch Verweis auf den Changelog ersetzt, Preisstaffel auf sechs Stufen netto, beide Verifikationsmarker entfernt; Usercentrics-TCF-Version durch Verweis auf die IAB-CMP-Liste ersetzt; Ablehnen-Button nicht mehr BGH I ZR 7/16 zugeordnet; Datum zu LG Muenchen I 3 O 17493/20 ergaenzt.
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2): Art. 7 und § 26 TDDDG / EinwV ergaenzt; TCF als branchenueblich statt gesetzliche Pflicht gefasst; Consent Mode als Vorgabe von Google ohne gesetzliche Pflicht, Jahr und Reichweite entfernt, Einstufung CRIT aufgehoben (jetzt MED); Embeds, Fonts, Geo-Targeting, Einwilligungsnachweis und Cookie-Banner auf Impressum/Datenschutzerklaerung norm- bzw. wortnah gefasst; Hinweis zu EU-Sitz und Unterauftragsverarbeitern ergaenzt.
