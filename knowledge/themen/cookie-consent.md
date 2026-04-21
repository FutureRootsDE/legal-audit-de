---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/ttdsg/__25.html
quellen-sekundaer:
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en
  - https://www.datenschutzkonferenz-online.de/media/oh/OH_Digitale_Dienste.pdf
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

# Cookie-Consent — § 25 TDDDG + Art. 6 DSGVO

## Kurz-Überblick

Cookie-Consent ist doppelt reguliert: Zum einen verlangt § 25 TDDDG Einwilligung für jeden Zugriff auf oder Speicherung in Endgeräten (unabhängig davon, ob die gespeicherten Daten personenbezogen sind). Zum anderen gilt für die damit verbundene Datenverarbeitung zusätzlich Art. 6 DSGVO. In der Praxis wird beides im Consent Management Platform (CMP) gebündelt abgewickelt. Zentrale Urteile: EuGH Planet49 (C-673/17) und BGH Cookie II (I ZR 7/16).

## Kernaussagen

### Wann ist Einwilligung Pflicht?
Immer, wenn der Speichervorgang oder Zugriff **nicht unbedingt erforderlich** für einen vom Nutzer ausdrücklich gewünschten Dienst ist. Praxis-Einordnung:

| Cookie-Art | Einwilligung? | Rechtsgrundlage |
|------------|---------------|-----------------|
| Session-Cookie (Login, Warenkorb) | Nein | § 25 Abs. 2 Nr. 2 TDDDG |
| CSRF-Token | Nein | § 25 Abs. 2 Nr. 2 TDDDG |
| Load-Balancer | Nein | § 25 Abs. 2 Nr. 1 TDDDG |
| Cookie-Consent-State selbst | Nein | § 25 Abs. 2 Nr. 2 TDDDG (unbedingt erforderlich für Consent-Funktion) |
| Sprach-/Theme-Präferenz | Grauzone, eher ja bei Drittanbieter | § 25 Abs. 1 TDDDG |
| Analytics (GA4, Matomo, Plausible\*) | Ja (\*Plausible im Cookie-losen Modus: nein) | § 25 Abs. 1 TDDDG + Art. 6 Abs. 1 lit. a DSGVO |
| Marketing-Pixel (Meta, TikTok, LinkedIn) | Ja | dito |
| Retargeting (Google Ads, Criteo) | Ja | dito |
| A/B-Test (VWO, Optimizely) | Ja | dito |
| Support-Chat (Intercom, Zendesk) | Ja (bei Drittanbieter-Cookies) | dito |
| YouTube-/Vimeo-Embed | Ja | dito |

### Anforderungen an wirksame Einwilligung (EDSA 05/2020 + DSGVO Art. 4 Nr. 11 / Art. 7)

1. **Freiwillig** — keine Nachteile bei Ablehnung, gleichwertige Ablehnen-Möglichkeit auf erster Ebene
2. **Für bestimmten Fall** — granular pro Zweck / Anbieter-Kategorie
3. **Informiert** — vor Setzen der Einwilligung müssen die Infos aus Art. 13 DSGVO bereitstehen
4. **Unmissverständlich** — aktive Handlung: Klick auf „Akzeptieren", NICHT Scrollen, NICHT Weitersurfen, NICHT vorausgewählte Checkbox
5. **Nachweisbar** — Protokollierung (Zeitpunkt, Text-Version, Auswahl)
6. **Widerrufbar** — genauso einfach wie Erteilung (z. B. „Cookie-Einstellungen"-Link im Footer)

### CMP-Anforderungen (Mindestpflichten)

- Keine nicht-notwendigen Cookies/Scripts **vor** Einwilligung
- Ablehnen-Button **gleichwertig prominent** auf erster Ebene (LG Rostock 3 O 762/19; OVG NRW-orientierte Aufsichtsbehörden)
- Zwei-Klick-Modell für Einzelentscheidungen pro Kategorie
- Keine Dark Patterns (Farbgebung, Platzierung, Textmanipulation)
- Consent-Log serverseitig speicherbar
- Versionierung bei Änderungen der CMP-Konfiguration
- Speicherdauer Consent-Cookie: DSK empfiehlt ~12 Monate Max

### Problematische Pattern

- **„Akzeptieren" grün/groß vs. „Ablehnen" grau/klein** → Nudging-Problem (EDSA Opinion 08/2024)
- **„Nur essenzielle" nur im Zwei-Klick** während „Alle akzeptieren" im Ein-Klick → unausgewogen
- **Ablehnen nur über „Einstellungen"-Menü** → unzulässig (vgl. Noyb-Beschwerden, CNIL-Bußgelder gegen Google/Facebook 2022)
- **„Legitimes Interesse" als Vorauswahl** im TCF-Standard → EuGH C-252/21 (Meta): reicht nicht
- **Cookie-Wall** (Zugang nur bei Consent) → grundsätzlich unfreiwillig (EDSA 05/2020)

## Typische Fallstricke in Codebases

- **Google Tag Manager vor Consent geladen:** GTM selbst lädt Consent-abhängige Tags → muss hinter Consent Mode v2 gated sein.
- **Meta Pixel im `<Head>` direkt:** Next.js `<Script>`-Component mit `strategy="afterInteractive"` UND Consent-Guard verwenden.
- **Hotjar / Smartlook / Session-Recording:** Einwilligungspflichtig; deutsche Aufsichtsbehörden sehen Session-Recording kritisch (DSK-Hinweise zu Tracking).
- **Server-Side GTM mit First-Party-Cookie:** § 25 TDDDG bleibt anwendbar — Kernfrage ist nicht, wo der Server steht, sondern dass Infos auf Endgerät gespeichert werden.
- **Consent-Mode v2 ohne Basic/Advanced-Unterscheidung:** Google sendet auch ohne Consent pingbacks — prüfen, was tatsächlich gesendet wird.
- **A/B-Test vor Consent (Optimize, Varify):** DOM-Manipulation + clientseitiger Storage → einwilligungspflichtig.
- **LocalStorage als „Cookie-Bypass":** EuGH C-673/17 gilt technikneutral.

## Relevanz für Codebase-Typen

- **Next.js SaaS:** Consent-Kontext als React-Provider; Scripts in Layout mit `strategy="lazyOnload"` + Consent-Check. Beliebte Lösungen: `react-cookie-consent`, `@c15t/react`, Eigenbau mit Zustand.
- **Landingpage:** Cookiebot / Usercentrics / Borlabs / Klaro am verbreitetsten. Bei WP: Borlabs / Real Cookie Banner. Bei statischen Seiten: Orestbida/CookieConsent.
- **n8n:** Selbst keine Consent-Problematik (Backend-Tool); aber Workflows, die Tracking-Daten von Frontends einsammeln, sind vorgelagert Consent-pflichtig.
- **E-Commerce:** Shopify/Shopware/WooCommerce haben native oder Plugin-Lösungen. Besonders heikel: Conversion-Pixel im Checkout.
- **Content/Blog:** „Click to load"-Pattern für Embeds. Shariff Wrapper statt nativer Share-Buttons.

## Behörden-Hinweise

- **DSK Orientierungshilfe für Anbieter:innen digitaler Dienste (ehem. OH Telemedien)** — aktualisiert 2023
- **EDSA Leitlinien 05/2020 zur Einwilligung** (v1.1, Mai 2020) — Scrollen, Cookie-Walls, klares Opt-In
- **EDSA Opinion 08/2024** — „Consent or Pay"-Modelle
- **CNIL-Bußgelder gegen Google (150 Mio. €) und Facebook (60 Mio. €) 2022** — Paradefälle mangelhafter Ablehnungsmöglichkeit

## Zitierbare Urteile

- **EuGH C-673/17 (Planet49), 01.10.2019** — Keine wirksame Einwilligung durch vorausgewählte Checkbox
- **BGH I ZR 7/16 (Cookie II), 28.05.2020** — Umsetzung Planet49 in deutschem Recht
- **LG Rostock 3 O 762/19, 15.09.2020** — „Cookie-Einstellungen"-Button gleichwertig zu „Akzeptieren"
- **EuGH C-252/21 (Meta/Bundeskartellamt), 04.07.2023** — Personalisierte Werbung nicht auf „berechtigtes Interesse" stützbar
- **LG München I 3 O 17493/20, 20.01.2022** — Google Fonts als Beispiel für Drittanbieter-Tracking ohne Consent

## Siehe auch

- [[gesetze/tdddg]]
- [[gesetze/dsgvo]]
- [[themen/tracking-analytics]]
- [[urteile/eugh-planet49]]
- [[urteile/bgh-cookie-einwilligung]]
- [[urteile/bgh-google-fonts]]
