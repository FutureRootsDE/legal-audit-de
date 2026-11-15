---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/ttdsg/__25.html
quellen-sekundaer:
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en
  - https://www.datenschutzkonferenz-online.de/media/oh/OH_Digitale_Dienste.pdf
  - https://www.gesetze-im-internet.de/einwv/
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

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
| Load-Balancer | Nein, nur ohne langfristig gespeicherte eindeutige ID (DSK, OH Digitale Dienste) | § 25 Abs. 2 Nr. 1 TDDDG |
| Cookie-Consent-State selbst | Nein | § 25 Abs. 2 Nr. 2 TDDDG (unbedingt erforderlich für Consent-Funktion) |
| Sprach-/Theme-Präferenz | Nein, wenn nur ein nicht identifizierender Wert gespeichert wird (z. B. „language: de“) und erst nach Nutzerwahl; Ja bei UID oder Drittanbieter | § 25 Abs. 2 Nr. 2 TDDDG; DSK OH Digitale Dienste Rn. 81 |
| Analytics (GA4, Matomo, Plausible\*) | Ja (\*cookielose Tools: nur einwilligungsfrei, wenn weder gespeichert noch per Skript auf Endgeräteeigenschaften zugegriffen wird; Einzelfallprüfung) | § 25 Abs. 1 TDDDG + Art. 6 Abs. 1 lit. a DSGVO |
| Marketing-Pixel (Meta, TikTok, LinkedIn) | Ja | dito |
| Retargeting (Google Ads, Criteo) | Ja | dito |
| A/B-Test (VWO, Optimizely) | Ja | dito |
| Support-Chat (Intercom, Zendesk) | Ja (bei Drittanbieter-Cookies) | dito |
| YouTube-/Vimeo-Embed | Ja | dito |

### Anforderungen an wirksame Einwilligung (EDSA 05/2020 + DSGVO Art. 4 Nr. 11 / Art. 7)

1. **Freiwillig** — keine Nachteile bei Ablehnung; Ablehnen-Möglichkeit auf erster Ebene, wenn das Banner Inhalte versperrt oder eine Interaktion erzwingt (DSK, OH Digitale Dienste, Rn. 124 f.); Ablehnen darf nicht aufwendiger sein als Zustimmen
2. **Für bestimmten Fall** — granular pro Zweck / Anbieter-Kategorie
3. **Informiert**: vor Erteilung mindestens Identität des Verantwortlichen, Zweck jedes Vorgangs, Art der Daten, Widerrufsrecht, ggf. automatisierte Entscheidung und Drittlandrisiken (EDSA Leitlinien 05/2020 Rn. 64); die vollständigen Art.-13-Informationen zusätzlich leicht erreichbar
4. **Unmissverständlich** — aktive Handlung: Klick auf „Akzeptieren", NICHT Scrollen, NICHT Weitersurfen, NICHT vorausgewählte Checkbox
5. **Nachweisbar** — Protokollierung (Zeitpunkt, Text-Version, Auswahl)
6. **Widerrufbar** — genauso einfach wie Erteilung (z. B. „Cookie-Einstellungen"-Link im Footer)

### CMP-Anforderungen (Mindestpflichten)

- Keine nicht-notwendigen Cookies/Scripts **vor** Einwilligung
- Ablehnen-Möglichkeit auf erster Ebene, wenn das Banner Inhalte versperrt oder eine Interaktion erzwingt (DSK, OH Digitale Dienste V1.2, Rn. 124 f.; in der Praxis meist der Fall); Ablehnen darf nicht schwerer sein als Zustimmen. LG Rostock 3 O 762/19 <<VERIFIKATION AUSSTEHEND>>
- Zwei-Klick-Modell für Einzelentscheidungen pro Kategorie
- Keine Dark Patterns (Farbgebung, Platzierung, Textmanipulation)
- Consent-Log serverseitig speicherbar
- Versionierung bei Änderungen der CMP-Konfiguration
- Speicherdauer Consent-Cookie: Die DSK nennt keine feste Höchstdauer; Laufzeit begrenzt nach dem Grundsatz der Speicherbegrenzung (Art. 5 Abs. 1 lit. e DSGVO; DSK OH Digitale Dienste, Version 1.2)

### Problematische Pattern

- **„Akzeptieren" grün/groß vs. „Ablehnen" grau/klein** → Nudging-Problem
- **„Nur essenzielle" nur im Zwei-Klick** während „Alle akzeptieren" im Ein-Klick → unausgewogen
- **Ablehnen nur über „Einstellungen"-Menü** → unzulässig (vgl. Noyb-Beschwerden, CNIL-Bußgelder gegen Google/Facebook 2022)
- **„Legitimes Interesse" als Vorauswahl** im TCF-Standard → EuGH C-252/21 (Meta Platforms/Bundeskartellamt), 04.07.2023: Art. 6 Abs. 1 lit. f DSGVO trägt die Zusammenführung von Off-Site- und Konzerndaten nur unter engen Voraussetzungen (Tenor 5); für die Personalisierung von Werbung durch den Betreiber eines sozialen Netzwerks überwiegen die Interessen der Nutzer (Rn. 117). Das TCF war nicht Gegenstand; dazu EuGH C-604/22.
- **Cookie-Wall** (Zugang nur bei Consent) → grundsätzlich unfreiwillig (EDSA 05/2020)

## Typische Fallstricke in Codebases

- **Google Tag Manager vor Consent geladen:** GTM selbst lädt Consent-abhängige Tags → muss hinter Consent Mode v2 gated sein.
- **Meta Pixel im `<Head>` direkt:** Next.js `<Script>`-Component mit `strategy="afterInteractive"` UND Consent-Guard verwenden.
- **Hotjar / Smartlook / Session-Recording:** Einwilligungspflichtig; deutsche Aufsichtsbehörden sehen Session-Recording kritisch (DSK-Hinweise zu Tracking).
- **Server-Side GTM mit First-Party-Cookie:** § 25 TDDDG bleibt anwendbar — Kernfrage ist nicht, wo der Server steht, sondern dass Infos auf Endgerät gespeichert werden.
- **Consent-Mode v2 ohne Basic/Advanced-Unterscheidung:** Google sendet auch ohne Consent pingbacks — prüfen, was tatsächlich gesendet wird.
- **A/B-Test vor Consent (Optimize, Varify):** DOM-Manipulation + clientseitiger Storage → einwilligungspflichtig.
- **LocalStorage als „Cookie-Bypass":** § 25 Abs. 1 TDDDG erfasst jede Speicherung von Informationen in der Endeinrichtung, auch Web-Storage (so auch DSK OH Digitale Dienste).

## Relevanz für Codebase-Typen

- **Next.js SaaS:** Consent-Kontext als React-Provider; Scripts in Layout mit `strategy="lazyOnload"` + Consent-Check. Beliebte Lösungen: `react-cookie-consent`, `@c15t/react`, Eigenbau mit Zustand.
- **Landingpage:** Cookiebot / Usercentrics / Borlabs / Klaro am verbreitetsten. Bei WP: Borlabs / Real Cookie Banner. Bei statischen Seiten: Orestbida/CookieConsent.
- **n8n:** Selbst keine Consent-Problematik (Backend-Tool); aber Workflows, die Tracking-Daten von Frontends einsammeln, sind vorgelagert Consent-pflichtig.
- **E-Commerce:** Shopify/Shopware/WooCommerce haben native oder Plugin-Lösungen. Besonders heikel: Conversion-Pixel im Checkout.
- **Content/Blog:** „Click to load"-Pattern für Embeds. Shariff Wrapper statt nativer Share-Buttons.

## Behörden-Hinweise

- **DSK Orientierungshilfe für Anbieter:innen von digitalen Diensten (OH Digitale Dienste), Version 1.2, Stand November 2024**
- **EDSA Leitlinien 05/2020 zur Einwilligung** (v1.1, Mai 2020) — Scrollen, Cookie-Walls, klares Opt-In
- **EDSA Stellungnahme 08/2024 vom 17.04.2024** zu „Consent or Pay"-Modellen großer Online-Plattformen
- **CNIL-Bußgelder gegen Google (150 Mio. €) und Facebook (60 Mio. €) 2022** — Paradefälle mangelhafter Ablehnungsmöglichkeit

## Zitierbare Urteile

- **EuGH C-673/17 (Planet49), 01.10.2019** — Keine wirksame Einwilligung durch vorausgewählte Checkbox
- **BGH I ZR 7/16 (Cookie II), 28.05.2020** — Umsetzung Planet49 in deutschem Recht
- **LG Rostock 3 O 762/19, 15.09.2020** — „Cookie-Einstellungen"-Button gleichwertig zu „Akzeptieren"
- **EuGH C-252/21 (Meta Platforms/Bundeskartellamt), 04.07.2023**: Art. 6 Abs. 1 lit. f DSGVO trägt die Zusammenführung von Off-Site- und Konzerndaten nur unter engen Voraussetzungen (Tenor 5); für die Personalisierung von Werbung durch den Betreiber eines sozialen Netzwerks überwiegen die Interessen der Nutzer (Rn. 117). Das TCF war nicht Gegenstand; dazu EuGH C-604/22.
- **EuGH C-604/22 (IAB Europe), 07.03.2024**: TC-String ist personenbezogenes Datum, soweit er mit vertretbarem Aufwand einer Kennung (insbesondere der IP-Adresse) zugeordnet werden kann; IAB Europe ist unter den Voraussetzungen des Tenors 2 gemeinsam Verantwortlicher, nicht automatisch für die Weiterverarbeitung durch Dritte
- **LG München I 3 O 17493/20, 20.01.2022** — Google Fonts als Beispiel für Drittanbieter-Tracking ohne Consent

## Einwilligungsverwaltungsverordnung (EinwV) — seit 01.04.2025

Die auf § 26 TDDDG gestuetzte Einwilligungsverwaltungsverordnung (EinwV, BGBl.
2025 I Nr. 32 vom 06.02.2025, in Kraft seit 01.04.2025) regelt anerkannte
Dienste zur zentralen Einwilligungsverwaltung (Personal Information Management
Systems/PIMS). Teilnahme ist fuer Websitebetreiber **freiwillig**; ein Verzicht
auf die eigene Cookie-Banner-Logik ist damit nicht verbunden. Zustaendig fuer
die Anerkennung von Diensten ist der BfDI. Die EinwV aendert die materiellen
Anforderungen an die Einwilligung nach § 25 TDDDG und Art. 7 DSGVO nicht; sie
schafft lediglich einen zusaetzlichen Weg, Einwilligungen plattformuebergreifend
zu verwalten.

## Aenderungsvermerk 2026-11-14

- EinwV-Abschnitt ergaenzt (Quelle: BGBl. 2025 I Nr. 32, § 26 TDDDG auf
  gesetze-im-internet.de). Teilnahme bleibt freiwillig; keine Pflicht fuer
  Audit-Scope.
- Hinweis zum Digital-Omnibus-Vorschlag (COM(2025) 837 final vom 19.11.2025): Der
  Entwurf ist bislang **Kommissionsvorschlag** im ordentlichen
  Gesetzgebungsverfahren, **noch nicht verkuendet**. Bis zur Verkuendung
  gelten § 25 TDDDG und Art. 6/7 DSGVO unveraendert fort.
- Datum und Verifizierung auf 2026-11-14 vereinheitlicht.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  keine feste DSK-Hoechstdauer fuer das Consent-Cookie; Fehlbeleg EDSA
  Opinion 08/2024 beim Nudging entfernt; OH Digitale Dienste Version 1.2
  (November 2024); Omnibus-Aktenzeichen COM(2025) 837; C-252/21 und
  C-604/22 praezisiert; Technikneutralitaet auf § 25 Abs. 1 TDDDG gestuetzt;
  Load-Balancer-Vorbehalt, Sprach-/Theme-Praeferenz und Informationspflicht
  vor Einwilligung praezisiert.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2):
  Ablehnen-Moeglichkeit auf erster Ebene nach DSK OH Digitale Dienste V1.2
  (Rn. 124 f.) statt pauschaler Pflicht, Halbsatz ohne Beleg gestrichen,
  LG Rostock mit Marker; cookielose Tools nur bei fehlendem Endgeraetezugriff
  einwilligungsfrei.

## Siehe auch

- [[gesetze/tdddg]]
- [[gesetze/dsgvo]]
- [[themen/tracking-analytics]]
- [[urteile/eugh-planet49]]
- [[urteile/bgh-cookie-einwilligung]]
- [[urteile/bgh-google-fonts]]
