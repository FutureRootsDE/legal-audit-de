---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/ttdsg/__25.html
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/media/oh/OH_Digitale_Dienste.pdf
  - https://www.edpb.europa.eu/
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# Tracking & Analytics — GA4, Meta Pixel, Server-Side-Tracking

## Kurz-Überblick

Web-Tracking ist unter DSGVO + TDDDG nur mit wirksamer Einwilligung zulässig. Betroffen sind insbesondere Google Analytics 4 (GA4), Meta/Facebook Pixel, TikTok Pixel, LinkedIn Insight Tag, Pinterest Tag, Microsoft Clarity, Hotjar sowie Server-Side-Tracking (sGTM). Trotz EU-US Data Privacy Framework (seit 10.07.2023) bleibt die Consent-Pflicht nach § 25 TDDDG bestehen — das DPF ersetzt nur den Drittland-Nachweis, nicht die Rechtsgrundlage.

## Kernaussagen

### Google Analytics 4 (GA4)

- **Einwilligung nach § 25 Abs. 1 TDDDG erforderlich** (Client-ID wird im LocalStorage gesetzt)
- **Drittland:** Google LLC (USA) — unter DPF **selbstzertifiziert**; Übertragung legal, wenn DPF-Listung geprüft und Transparenz in Datenschutzerklärung
- **Consent Mode v2:** Pflicht ab März 2024 für Ads-Features; technischer Mechanismus, ersetzt keine Einwilligung
- **IP-Anonymisierung:** in GA4 Standard (nicht mehr abschaltbar), aber allein nicht ausreichend für Consent-Verzicht
- **Aufsichtsbehörden-Einschätzung:** CNIL (FR), Garante (IT), DSB (AT) haben GA Universal als unvereinbar mit SCCs erklärt (vor DPF); seit DPF entspannte Lage — aber granulare Einwilligung weiter Pflicht

### Meta Pixel (Facebook Pixel)

- **Einwilligung zwingend** — gemeinsam Verantwortlichkeit (EuGH C-40/17 Fashion ID analog)
- **Joint-Controller-Agreement (JCA)** mit Meta: Controller Addendum seit 2018 standard
- **Advanced Matching (Hashed E-Mail):** zusätzlich heikel; auch gehashte E-Mail = personenbezogenes Datum (OLG Frankfurt, Hamburger DPA-Position)
- **Conversions-API (CAPI) / Server-Side:** ersetzt NICHT die Consent-Pflicht; Cookie-basiertes Matching bleibt einwilligungspflichtig

### Server-Side-Tracking (sGTM, Segment, RudderStack)

- **Endgeräte-Cookie bleibt Einwilligungs-Trigger**: Server-Container schickt weiter First-Party-Cookie an Browser → § 25 TDDDG greift
- **Vorteil:** bessere Kontrolle über Datenfluss, Drittland-Minimierung, Filterung vor Weitergabe
- **Nachteil:** kein Consent-Bypass; Aufsichtsbehörden betonen, dass rechtlich entscheidend ist, was am Endgerät passiert, nicht wo der Server steht (DSK Stellungnahme 2023)

### Cookieless Analytics (Plausible, Fathom, SimpleAnalytics)

- Werben mit „kein Consent nötig", technisch oft zutreffend (keine Cookies, aggregierte Daten)
- **Aber:** Wenn IP temporär verarbeitet wird, bleibt DSGVO anwendbar → **Datenschutzerklärung ja**, **Consent nein** (Art. 6 Abs. 1 lit. f DSGVO)
- Rechtlich sicher, wenn tatsächlich: keine Fingerprints, IP nur flüchtig, keine Cookies/LocalStorage, keine Drittland-Übertragung oder EU-Hosting

### Microsoft Clarity / Hotjar / Session Recording

- **Besonders einwilligungspflichtig** — nicht nur § 25 TDDDG, auch Art. 6 DSGVO
- Aufsichtsbehörden sehen Session-Recording als eingriffsintensiv (DSFA-pflichtig bei breitem Einsatz)
- Zwingend: Maskierung von Formularfeldern, PII, Zahlungsdaten

## Typische Fallstricke in Codebases

- **GTM im `<head>` geladen ohne Consent Mode v2:** sendet Pings auch ohne Consent.
- **Fehlende `dataLayer`-Flags:** `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization` müssen vor GTM-Load gesetzt sein.
- **Meta Pixel via Plugin (z. B. Yoast / Rank Math):** direktes Einbinden ohne Consent-Wrapper.
- **Facebook CAPI ohne Match-Event-Filter:** hashed E-Mail/Telefon wird auch ohne Consent gesendet.
- **Hotjar Tracking-Code im Layout** vor Consent-State.
- **A/B-Testing (VWO, Google Optimize Nachfolger):** oft ohne Consent — DSGVO + TDDDG anwendbar, Dark Pattern.
- **UTM-Parameter in Datenbank** verknüpft mit User-ID ohne Rechtsgrundlage.
- **Logging von `document.referrer`** + IP in App-Server-Logs langfristig gespeichert — Datenminimierung verletzt.

## Relevanz für Codebase-Typen

- **Next.js SaaS:**
  - `next/script` mit `strategy="afterInteractive"` und Consent-Guard
  - GA4 nur via GTM Container geladen nach Consent-Event
  - Server-Side: bei Vercel/Cloudflare Edge-Functions prüfen, ob IP gespeichert wird
- **Landingpage:**
  - Standardstack: GTM + GA4 + Meta Pixel + Google Ads Tag + LinkedIn Insight
  - Alle über CMP (Cookiebot/Usercentrics) gated
  - **Fallback-Analytics:** Plausible/Fathom ohne Consent als Ergänzung für Basis-Metriken
- **n8n:** Oft Empfänger von Tracking-Events via Webhook — auf Quellseite ist Consent zu prüfen.
- **E-Commerce:** Conversion-Tracking im Checkout — granulare Ereignis-Flags (purchase, add_to_cart); Enhanced E-Commerce nur mit Consent.
- **Content/Blog:** Meist weniger aggressiv; oft reichen Plausible + Search Console.

## Behörden-Hinweise

- **DSK Orientierungshilfe Digitale Dienste** (2023, ehem. OH Telemedien)
- **EDSA Leitlinien 05/2020** zur Einwilligung
- **CNIL (FR)** Sanktion 150 Mio. € gegen Google (2022) wegen Cookie-Banner
- **Garante (IT) Bescheid 09.06.2022** — Google Analytics (Universal) rechtswidrig (vor DPF)
- **DSB Österreich 22.04.2022** — analog GA Universal unvereinbar
- **Hamburgische DPA: Leitfaden „Einsatz von Analyse-Tools"** (jährlich aktualisiert)

## Zitierbare Urteile

- **EuGH C-40/17 (Fashion ID), 29.07.2019** — Betreiber mit Social-Plugin ist Mitverantwortlicher
- **LG München I 3 O 17493/20, 20.01.2022** — Google Fonts dynamisch = 100 EUR Schadenersatz
- **EuGH C-252/21 (Meta/Bundeskartellamt), 04.07.2023** — Personalisierte Werbung nur mit Einwilligung
- **EuGH C-604/22 (IAB Europe), 07.03.2024** — TC-String ist personenbezogenes Datum; IAB ist (Mit-)Verantwortlicher für TCF

## Siehe auch

- [[gesetze/tdddg]]
- [[gesetze/dsgvo]]
- [[themen/cookie-consent]]
- [[themen/drittland-transfer]]
- [[urteile/bgh-google-fonts]]
