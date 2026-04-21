---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/ttdsg/
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/media/oh/OH_Digitale_Dienste.pdf
  - https://www.bfdi.bund.de/
verifiziert-am: 2026-04-19
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# TDDDG — Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz

## Kurz-Überblick

Das TDDDG (vormals TTDSG, umbenannt im Mai 2024 im Rahmen des Digitale-Dienste-Gesetzes) setzt die ePrivacy-Richtlinie 2002/58/EG in nationales Recht um. Es regelt Fernmeldegeheimnis, Verkehrs- und Standortdaten sowie insbesondere die Einwilligung beim Zugriff auf Endgeräte-Informationen (§ 25 — „Cookie-Paragraf"). Der bisherige § 25 TTDSG gilt inhaltlich unverändert als § 25 TDDDG weiter.

## Schlüsselparagraphen

### § 1 — Anwendungsbereich
Gilt für Anbieter von Telekommunikationsdiensten und Anbieter digitaler Dienste (vorher „Telemedien"). Geltungsbereich folgt Marktortprinzip analog DSGVO.

### § 2 — Begriffsbestimmungen
Verweis auf TKG / DDG; „Endeinrichtung" = jedes Gerät mit Verbindung zu öffentlichem TK-Netz (Laptop, Smartphone, Smart-TV, IoT).

### § 3 — Fernmeldegeheimnis
Inhalte und nähere Umstände der TK unterliegen dem Fernmeldegeheimnis. Verletzung kann strafbar nach § 27 TDDDG sein.

### § 19 — Technische und organisatorische Vorkehrungen
Anbieter digitaler Dienste müssen geeignete TOM treffen (ergänzt Art. 32 DSGVO für Kommunikations-Kontext).

### § 25 — Schutz der Privatsphäre bei Endeinrichtungen (zentrale Norm)

**Abs. 1 (Wortlaut):**
> „Die Speicherung von Informationen in der Endeinrichtung des Endnutzers oder der Zugriff auf Informationen, die bereits in der Endeinrichtung gespeichert sind, sind nur zulässig, wenn der Endnutzer auf der Grundlage von klaren und umfassenden Informationen eingewilligt hat."

Die Einwilligung muss **den Anforderungen der DSGVO** genügen (Art. 4 Nr. 11, Art. 7 DSGVO).

**Abs. 2 — Ausnahmen (kumulativ oder alternativ zu prüfen):**
- **Nr. 1:** Alleiniger Zweck ist die **Durchführung der Übermittlung einer Nachricht** über ein öffentliches TK-Netz (z. B. Load-Balancer-Cookie während Verbindungsaufbau).
- **Nr. 2:** Speicherung/Zugriff ist **unbedingt erforderlich**, damit der Anbieter einen vom Nutzer **ausdrücklich gewünschten Dienst** bereitstellen kann (z. B. Session-Cookie für Login, Warenkorb-Cookie).

**Nicht ausnahmefähig** (Einwilligung zwingend):
- Analytics (z. B. Google Analytics, Matomo ohne spezielle Konfiguration)
- Werbe-/Tracking-Cookies (Meta Pixel, TikTok Pixel, LinkedIn Insight)
- Personalisierungs-Cookies ohne explizite Nutzeranforderung
- A/B-Test-Cookies ohne Einwilligung
- Chatbots/Support-Widgets (Intercom, Zendesk) mit Drittanbieter-Cookies

### § 26 — Anerkannte Dienste zur Einwilligungsverwaltung (PIMS)
Seit 2022/2024 Rechtsgrundlage für zentrale Consent-Management-Dienste. Verordnungsermächtigung noch nicht voll ausgeschöpft.

### § 27 — Strafvorschriften
Bis zu **2 Jahre Freiheitsstrafe** bei Verletzung des Fernmeldegeheimnisses.

### § 28 — Bußgeldvorschriften
Bis zu **300.000 EUR** bei Verstoß gegen § 25 (parallele Zuständigkeit zur Bußgeldmacht der DSGVO-Aufsicht!).

### § 29 — Zuständigkeit BfDI
Der Bundesbeauftragte für den Datenschutz überwacht § 25 TDDDG.

## Typische Fallstricke in Codebases

- **Cookie-Banner lädt Tracking-Skripte VOR Consent:** Ganz klassischer Fehler — Tags müssen gated sein (Google Tag Manager Consent Mode v2, Cookiebot, Usercentrics).
- **„Nur notwendige" / „Alle akzeptieren" ungleich groß/prominent:** verstößt gegen Freiwilligkeit (vgl. EDSA Leitlinie 05/2020, nudging).
- **LocalStorage/SessionStorage-Fingerprinting ohne Consent:** § 25 TDDDG gilt technikneutral — nicht nur für HTTP-Cookies.
- **Server-Side-Tracking mit Client-ID-Cookie:** Client-seitige Speicherung bleibt einwilligungspflichtig, auch wenn Data-Transfer serverseitig erfolgt.
- **Page-Reload leert Consent-Status:** Consent muss persistent und widerrufbar sein.
- **Cookie-Wall (Zugang nur bei Einwilligung):** EDSA sieht das überwiegend als unfreiwillig; Alternativen prüfen (Pur-Abo nach EDSA Opinion 08/2024, aber mit Auflagen).
- **Länger als 12 Monate gespeicherte Consent-Cookies:** DSK Orientierungshilfe sieht ~12 Monate als Grenze.

## Relevanz für Codebase-Typen

- **Next.js SaaS:** `next/script` mit Strategy `afterInteractive` für Tracking-Scripts **nur** nach Consent laden. Empfehlung: Dynamic Import gated durch Consent-State (z. B. via Zustand/Context).
- **Landingpage:** Absolut zentral — fast jede Landingpage hat Marketing-Pixel. Consent-Tool (Cookiebot, Usercentrics, Borlabs, Klaro) Pflicht.
- **n8n:** Selbst kaum betroffen. Betroffen wenn Webhooks von Marketing-Tools Daten einsammeln — dann ist Quell-Seite verantwortlich.
- **E-Commerce:** Warenkorb-Cookie = unbedingt erforderlich (§ 25 Abs. 2 Nr. 2). Conversion-Tracking = einwilligungspflichtig.
- **Content/Blog:** YouTube/Vimeo-Embeds mit Cookies = einwilligungspflichtig; Lösung: „Click to load"-Pattern oder youtube-nocookie.com (trotzdem prüfen).

## Behörden-Hinweise

- **DSK Orientierungshilfe für Anbieter:innen von Telemedien ab dem 1.12.2021** (OH Telemedien, aktualisiert 2023 als „OH Digitale Dienste")
- **EDSA Leitlinien 05/2020** zur Einwilligung (Scrolling, Cookie-Walls)
- **EDSA Opinion 08/2024** — „Consent or Pay"-Modelle für Large Online Platforms
- **BfDI** ist nationale Aufsichtsbehörde für § 25 TDDDG

## Zitierbare Urteile

- **EuGH C-673/17 (Planet49), 01.10.2019** — Vorangekreuzte Checkbox ungültig
- **BGH I ZR 7/16 (Cookie II), 28.05.2020** — Umsetzung Planet49 in deutsches Recht
- **EuGH C-252/21 (Meta Platforms / Bundeskartellamt), 04.07.2023** — Personalisierte Werbung braucht Einwilligung, nicht nur „berechtigtes Interesse"

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[urteile/eugh-planet49]]
- [[urteile/bgh-cookie-einwilligung]]
