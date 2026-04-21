---
aktualisiert: 2026-04-19
quelle-primaer: https://curia.europa.eu/juris/liste.jsf?num=C-252/21
quellen-sekundaer:
  - https://curia.europa.eu/jcms/upload/docs/application/pdf/2023-07/cp230113de.pdf
  - https://www.bundeskartellamt.de/
  - https://www.datenschutzkonferenz-online.de/
verifiziert-am: 2026-04-19
geltungsbereich: [EU, DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# EuGH C-252/21 — Meta Platforms vs. Bundeskartellamt

## Kurz-Ueberblick

- **Gericht:** Europaeischer Gerichtshof (Grosse Kammer)
- **Aktenzeichen:** C-252/21
- **Datum:** **04.07.2023**
- **Verfahrensart:** Vorabentscheidung (Art. 267 AEUV)
- **Vorlegendes Gericht:** Oberlandesgericht Duesseldorf (Kartellsenat,
  Beschluss vom 24.03.2021)
- **Parteien:**
  - Klaegerin / Beschwerdefuehrerin: **Meta Platforms Inc.** (vormals
    Facebook Inc.), Meta Platforms Ireland Ltd., Facebook Deutschland GmbH
  - Beklagte: **Bundeskartellamt** (Deutsche Kartellbehoerde)

## Sachverhalt

Das Bundeskartellamt hatte mit Entscheidung vom **06.02.2019** Meta
(Facebook) missbraeuchliches Verhalten einer marktbeherrschenden Stellung
vorgeworfen (§§ 19, 32 GWB i.V.m. Art. 102 AEUV):

- Facebook verknuepfte Nutzerdaten aus dem Kernnetzwerk (facebook.com) mit
  Daten von **Instagram**, **WhatsApp**, **externen Webseiten** (ueber
  Facebook-Cookies, Pixel, Like-Buttons, Social Plugins) und **Drittanbieter-
  Apps** (Facebook Login).
- Die Nutzer hatten bei Anmeldung in Facebook einer **AGB-Klausel** zugestimmt,
  die diese Datenzusammenfuehrung ermoeglichte.
- Das BKartA sah darin einen **Ausbeutungsmissbrauch** in Form einer
  DSGVO-Verletzung (fehlende wirksame Einwilligung nach Art. 6, 9 DSGVO),
  die wegen Marktmacht "aufgezwungen" war.

Meta klagte gegen die BKartA-Entscheidung vor dem OLG Duesseldorf, das dem
EuGH Rechtsfragen vorlegte:

1. Darf eine **nationale Wettbewerbsbehoerde** im Rahmen einer kartellrecht-
   lichen Missbrauchs-Pruefung auch DSGVO-Verstoesse feststellen?
2. Wie sind die **Rechtsgrundlagen des Art. 6 DSGVO** (insb. berechtigtes
   Interesse, Vertragserfuellung) beim Verknuepfen von Nutzerdaten ueber
   Plattformgrenzen auszulegen?
3. Reicht die Einwilligung des Nutzers gegenueber einem **marktmaechtigen**
   Unternehmen "freiwillig" aus?

## Tenor (Kernaussagen)

Der EuGH entschied:

1. **Nationale Wettbewerbsbehoerde darf DSGVO-Verstoesse feststellen**, wenn
   diese im Rahmen einer kartellrechtlichen Missbrauchs-Pruefung relevant sind
   — jedoch **nur inzident**; die eigentliche DSGVO-Durchsetzung bleibt den
   Datenschutzaufsichtsbehoerden vorbehalten (Kohaerenzgebot, Art. 51 ff DSGVO).
   Konsultationspflicht mit der DSGVO-Lead-Behoerde.

2. **Art. 9 Abs. 1 DSGVO (sensible Daten):** Auch "offensichtlich
   oeffentlich gemachte" sensible Daten duerfen nicht ohne Weiteres
   verarbeitet werden; blosses Besuchen einer Website mit Like-Button ist
   KEINE bewusste Veroeffentlichung i.S.v. Art. 9 Abs. 2 lit. e DSGVO.

3. **Art. 6 Abs. 1 lit. b DSGVO (Vertragserfuellung):** Personalisierung der
   Werbung ist nicht zwingend "erforderlich" zur Erfuellung des Nutzungs-
   vertrags — eng auszulegen.

4. **Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse):** Weitreichende
   Datenzusammenfuehrung fuer personalisierte Werbung rechtfertigt sich in der
   Regel NICHT durch blosses berechtigtes Interesse. Konkrete Abwaegung
   erforderlich; Nutzererwartung und -interessen massgeblich.

5. **Einwilligung (Art. 6 Abs. 1 lit. a DSGVO):** Bei marktmaechtigen
   Anbietern ist die **Freiwilligkeit** der Einwilligung besonders kritisch
   zu pruefen. Marktmacht bedeutet nicht automatisch Unfreiwilligkeit, aber
   sie ist ein gewichtiger Faktor.

## Bedeutung fuer Codebases

1. **Cross-Service-Datenverknuepfung** (z.B. SaaS-Suite aus mehreren
   Produkten) braucht **separate, spezifische Einwilligungen** — keine
   blanket-AGB-Zustimmung.
2. **Social-Plugins (Like-Button, Share-Button, Facebook Login, Google
   Maps, YouTube Embed)** uebermitteln Daten an Drittanbieter — Einwilligung
   nach § 25 TTDSG / Art. 6 DSGVO erforderlich; Consent-Banner-Loesung Pflicht.
3. **Personalized Ads als "Vertragsleistung" ausweisen** ist unzureichend —
   Trennung Kernleistung / Werbung erforderlich.
4. **Berechtigtes Interesse als Fallback** bei Tracking: nach Meta-Urteil
   stark eingeschraenkt.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Consent-Management-Plattform (CMP) Pflicht; Cookie-Consent
  VOR Laden von Analytics/Ads-Scripts. Strikte Trennung: technisch-funktional
  (ohne Einwilligung) vs. Werbung/Tracking (mit Einwilligung).
- **Landingpage:** Google Fonts lokal hosten (LG Muenchen I 3 O 17493/20);
  YouTube nur "nocookie"-Modus ohne Consent.
- **n8n-Workflows:** Workflow-Integration zu Meta Ads API / Google Ads API
  braucht dokumentierte Nutzer-Einwilligung (Conversion-API, CAPI).
- **E-Commerce:** Personalisierte Kauf-Empfehlungen: Einwilligung nach
  Art. 6 Abs. 1 lit. a DSGVO empfehlenswert, nicht "berechtigtes Interesse".
- **Content/Blog:** Kommentar-Embeds (Disqus, Facebook Comments): opt-in
  gefordert.

## Follow-Up

- **BKartA-Entscheidung vom 06.02.2019** wurde durch EuGH-Urteil bestaetigt
  im Rahmen des Rechtsstreits.
- **OLG Duesseldorf**: Folge-Urteil nach EuGH-Vorabentscheidung
  (Verfahren fortgefuehrt 2023/2024).
- **DSGVO-Abaenderungen**: Sowohl DSK-Leitfaeden (2023) als auch EDPB-
  Guidelines wurden entsprechend angepasst (Art. 6 Abs. 1 lit. b enge
  Auslegung, Art. 9 sensible Daten online).

## Tenor (wesentliche Leitsaetze — sinngemaess)

> Art. 51 ff DSGVO stehen einer nationalen Wettbewerbsbehoerde nicht
> entgegen, im Rahmen der Pruefung eines Missbrauchs marktbeherrschender
> Stellung DSGVO-Verstoesse festzustellen, sofern die Kohaerenz mit den
> Entscheidungen der Datenschutzbehoerden gewahrt bleibt. Art. 9 Abs. 1 DSGVO
> ist weit auszulegen; Nutzer erlauben durch blosse Website-Nutzung keine
> sensible Datenverarbeitung. Art. 6 Abs. 1 lit. b DSGVO rechtfertigt
> personalisierte Werbung nur, wenn sie objektiv zur Vertragserfuellung
> erforderlich ist. Die Freiwilligkeit der Einwilligung nach Art. 6 Abs. 1
> lit. a DSGVO ist bei marktmaechtigen Unternehmen besonders zu pruefen.

## Siehe auch

- [[gesetze/uwg]]
- [[themen/email-marketing]]
- [[themen/werbekennzeichnung]]
- BKartA-Entscheidung B6-22/16 (06.02.2019)
