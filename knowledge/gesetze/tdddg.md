---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/ttdsg/
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/media/oh/OH_Digitale_Dienste.pdf
  - https://www.bfdi.bund.de/
verifiziert-am: 2026-11-14
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14
>
> **Hinweis zur URL:** Das Gesetz wurde 2024 in TDDDG umbenannt. Der URL-Pfad
> auf gesetze-im-internet.de bleibt jedoch `/ttdsg/`; der Pfad `/tdddg/` liefert
> HTTP 404 (geprueft am 2026-11-14). Letzte Aenderung des TDDDG laut Fussnote
> gesetze-im-internet.de: Art. 3 G v. 10.03.2026 (BGBl. 2026 I Nr. 64); §§ 25
> und 26 TDDDG dadurch unveraendert.

# TDDDG — Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz

## Kurz-Überblick

Das TDDDG (vormals TTDSG, umbenannt im Mai 2024 im Rahmen des Digitale-Dienste-Gesetzes) setzt die ePrivacy-Richtlinie 2002/58/EG in nationales Recht um. Es regelt Fernmeldegeheimnis, Verkehrs- und Standortdaten sowie insbesondere die Einwilligung beim Zugriff auf Endgeräte-Informationen (§ 25 — „Cookie-Paragraf"). Der bisherige § 25 TTDSG gilt inhaltlich unverändert als § 25 TDDDG weiter.

## Schlüsselparagraphen

### § 1 — Anwendungsbereich
Gilt für Anbieter von Telekommunikationsdiensten und Anbieter digitaler Dienste (vorher „Telemedien"). Geltungsbereich folgt Marktortprinzip analog DSGVO.

### § 2 — Begriffsbestimmungen
Verweis auf TKG / DDG; „Endeinrichtung" = jedes Gerät mit Verbindung zu öffentlichem TK-Netz (Laptop, Smartphone, Smart-TV, IoT).

### § 3 — Fernmeldegeheimnis
Inhalte und nähere Umstände der TK unterliegen dem Fernmeldegeheimnis. § 3 ist in § 27 TDDDG nicht genannt; § 27 stellt Verstöße gegen das Abhörverbot (§ 5) und gegen § 8 (getarnte Sendeanlagen) unter Strafe.

### § 19 — Technische und organisatorische Vorkehrungen
Anbieter digitaler Dienste haben ihre Pflichten nach § 19 Abs. 1 durch technische und organisatorische Vorkehrungen sicherzustellen; nach Abs. 2 ist die anonyme oder pseudonyme Nutzung zu ermöglichen, soweit dies technisch möglich und zumutbar ist (ergänzt Art. 32 DSGVO für Kommunikations-Kontext).

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
Rechtsgrundlage für zentrale Consent-Management-Dienste. Die
**Einwilligungsverwaltungsverordnung (EinwV)** wurde am 06.02.2025 erlassen
(BGBl. 2025 I Nr. 32, in Kraft seit 01.04.2025) und konkretisiert die
Anforderungen an anerkannte Dienste. Die Teilnahme ist fuer Websitebetreiber
freiwillig. Der BfDI fuehrt das Register anerkannter Dienste; der erste
anerkannte Dienst ("Consenter", Law & Innovation Technology GmbH) wurde am
**17.10.2025** registriert <<VERIFIKATION AUSSTEHEND>>

### § 27 — Strafvorschriften
Bis zu **2 Jahre Freiheitsstrafe** für Verstöße gegen das Abhörverbot (§ 5) und gegen § 8 (getarnte Sendeanlagen); § 3 ist in § 27 nicht genannt.

### § 28 — Bußgeldvorschriften
Bis zu **300.000 EUR** bei Verstoß gegen § 25 (parallele Zuständigkeit zur Bußgeldmacht der DSGVO-Aufsicht!).

### § 29 — Zuständigkeit BfDI
Nach § 29 Abs. 2 ist der BfDI nur bei Anbietern von TK-Diensten und öffentlichen Stellen des Bundes zuständig. Für private Anbieter digitaler Dienste (Websites, Apps, SaaS) überwachen die Landesdatenschutzbehörden § 25 TDDDG (§ 1 Abs. 1 Nr. 8 TDDDG, § 40 BDSG).

## Typische Fallstricke in Codebases

- **Cookie-Banner lädt Tracking-Skripte VOR Consent:** Ganz klassischer Fehler; Tags dürfen erst nach Einwilligung laden (Blockierung über die CMP, z. B. Cookiebot, Usercentrics, oder Google Consent Mode v2 im Basic-Modus; der Advanced-Modus lädt Google-Tags schon vor der Einwilligung und sendet cookielose Pings, er ist kein Gating).
- **„Nur notwendige"/„Alle akzeptieren" ungleich prominent:** kann die Freiwilligkeit/Unmissverständlichkeit der Einwilligung (Art. 4 Nr. 11, Art. 7 DSGVO i. V. m. § 25 Abs. 1 TDDDG) entfallen lassen; Prüfung im Einzelfall (vgl. EDSA Cookie Banner Taskforce Report vom 18.01.2023, Nr. 15 bis 17).
- **LocalStorage/SessionStorage-Fingerprinting ohne Consent:** § 25 TDDDG gilt technikneutral — nicht nur für HTTP-Cookies.
- **Server-Side-Tracking mit Client-ID-Cookie:** Client-seitige Speicherung bleibt einwilligungspflichtig, auch wenn Data-Transfer serverseitig erfolgt.
- **Page-Reload leert Consent-Status:** Einwilligung muss nachweisbar (Art. 7 Abs. 1 DSGVO) und so einfach widerrufbar sein wie erteilt (Art. 7 Abs. 3 DSGVO); geht der Status verloren, darf ohne erneute Einwilligung nichts Einwilligungspflichtiges gesetzt werden. Eine Persistenzpflicht als solche gibt es nicht.
- **Cookie-Wall (Zugang nur bei Einwilligung):** EDSA sieht das überwiegend als unfreiwillig; Alternativen prüfen (Pur-Abo nach EDSA Opinion 08/2024, aber mit Auflagen).
- **Länger als 12 Monate gespeicherte Consent-Cookies:** Die DSK OH Digitale Dienste nennt keine 12-Monats-Grenze; die Angabe ist ein nicht behördlich belegter Praxiswert.

## Relevanz für Codebase-Typen

- **Next.js SaaS:** `next/script` mit Strategy `afterInteractive` für Tracking-Scripts **nur** nach Consent laden. Empfehlung: Dynamic Import gated durch Consent-State (z. B. via Zustand/Context).
- **Landingpage:** Absolut zentral, fast jede Landingpage hat Marketing-Pixel. Werden nicht unbedingt erforderliche Cookies/Pixel eingesetzt, ist vorher eine Einwilligung nach § 25 Abs. 1 TDDDG einzuholen (praktisch über ein Consent-Tool wie Cookiebot, Usercentrics, Borlabs, Klaro); ohne solche Vorgänge besteht keine Tool-Pflicht.
- **n8n:** § 25 TDDDG trifft die Quell-Seite (Speicherung/Zugriff im Endgerät). Wer die Daten per Webhook im Workflow weiterverarbeitet, bleibt dafür nach DSGVO selbst Verantwortlicher oder Auftragsverarbeiter (Art. 6, 28 DSGVO).
- **E-Commerce:** Warenkorb-Cookie = unbedingt erforderlich (§ 25 Abs. 2 Nr. 2). Conversion-Tracking = einwilligungspflichtig.
- **Content/Blog:** YouTube/Vimeo-Embeds mit Cookies = einwilligungspflichtig; Lösung: „Click to load"-Pattern oder youtube-nocookie.com (trotzdem prüfen).

## Behörden-Hinweise

- **DSK Orientierungshilfe Digitale Dienste** (OH Digitale Dienste), Version 1.2, Stand November 2024; Vorgänger: OH Telemedien vom 20.12.2021, Version 1.1 vom 30.11.2022
- **EDSA Leitlinien 05/2020** zur Einwilligung (Scrolling, Cookie-Walls)
- **EDSA Opinion 08/2024** — „Consent or Pay"-Modelle für Large Online Platforms
- **Aufsicht über § 25 TDDDG:** Landesdatenschutzbehörden bei privaten Anbietern digitaler Dienste; BfDI nur für TK-Anbieter und öffentliche Stellen des Bundes (§ 29 Abs. 2)

## Zitierbare Urteile

- **EuGH C-673/17 (Planet49), 01.10.2019** — Vorangekreuzte Checkbox ungültig
- **BGH I ZR 7/16 (Cookie II), 28.05.2020** — Umsetzung Planet49 in deutsches Recht
- **EuGH C-252/21 (Meta Platforms / Bundeskartellamt), 04.07.2023** — Eine marktbeherrschende Stellung schließt eine wirksame Einwilligung nicht aus, ist aber ein wichtiger Aspekt bei der Beurteilung der Freiwilligkeit; die Beweislast liegt beim Betreiber (Tenor 8)

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[urteile/eugh-planet49]]
- [[urteile/bgh-cookie-einwilligung]]

## Aenderungsvermerk

- **2026-11-14**: Hinweis auf letzte Aenderung des TDDDG durch Gesetz vom
  10.03.2026 (BGBl. 2026 I Nr. 64, §§ 25/26 unveraendert) ergaenzt; § 26
  TDDDG um Hinweis auf die Einwilligungsverwaltungsverordnung (EinwV) vom
  06.02.2025 (BGBl. 2025 I Nr. 32, in Kraft seit 01.04.2025) ergaenzt.
  Anerkennung des ersten Dienstes "Consenter" am 17.10.2025 mit
  Verifikationsmarker versehen, da bislang nur ueber Sekundaerquellen
  belegt (BfDI-Register nicht direkt abgerufen).
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  § 27 (nur §§ 5, 8, nicht § 3), § 19 nach Wortlaut, Aufsicht ueber § 25
  bei Landesdatenschutzbehoerden (§ 29 Abs. 2), 12-Monats-Grenze nicht aus
  der DSK-OH, OH Digitale Dienste Version 1.2, EuGH C-252/21 auf Tenor 8
  beschraenkt, Fallstricke (Consent Mode, Button-Gestaltung, Reload,
  Landingpage, n8n) praezisiert.
