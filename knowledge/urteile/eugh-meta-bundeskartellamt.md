---
aktualisiert: 2026-11-14
quelle-primaer: https://curia.europa.eu/juris/liste.jsf?num=C-252/21
quellen-sekundaer:
  - https://curia.europa.eu/jcms/upload/docs/application/pdf/2023-07/cp230113de.pdf
  - https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:62021CJ0252
  - https://www.bundeskartellamt.de/SharedDocs/Meldung/DE/Pressemitteilungen/2024/10_10_2024_Facebook.html
  - https://www.datenschutzkonferenz-online.de/
verifiziert-am: 2026-11-14
geltungsbereich: [EU, DE]
ecli: ECLI:EU:C:2023:537
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

# EuGH C-252/21 — Meta Platforms vs. Bundeskartellamt

## Kurz-Ueberblick

- **Gericht:** Europaeischer Gerichtshof (Grosse Kammer)
- **Aktenzeichen:** C-252/21
- **ECLI:** ECLI:EU:C:2023:537
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
- **Verfahrensende OLG Duesseldorf (10.10.2024):** Meta hat seine Beschwerde
  gegen die BKartA-Entscheidung **zurueckgenommen**. Das BKartA-Verfahren ist
  damit bestandskraeftig abgeschlossen. Quelle: BKartA-Pressemitteilung vom
  10.10.2024 (https://www.bundeskartellamt.de/SharedDocs/Meldung/DE/Pressemitteilungen/2024/10_10_2024_Facebook.html).
- **EuGH C-446/21 (Schrems/Meta, 04.10.2024):** Grundsatz der Datenminimierung
  (Art. 5 Abs. 1 lit. c DSGVO) begrenzt die Aggregation personenbezogener Daten
  fuer personalisierte Werbung auch bei erteilter Einwilligung zeitlich und
  sachlich; zudem Praezisierung zu Art. 9 DSGVO (Hinweis auf sexuelle
  Orientierung durch Nutzer macht nicht alle Daten zu „offensichtlich oeffentlich
  gemacht"). Verfahren war nach Vorlage des Bundeskartellamt-Verfahrens
  ausgesetzt. Beleg: curia.europa.eu, Rechtssache C-446/21.
- **EDSA-Opinion 08/2024 vom 17.04.2024 („Consent or Pay")**: Auf gemeinsame
  Anfrage NL/NO/HmbBfDI; Kernaussage: „Consent or Pay"-Modelle grosser Online-
  Plattformen koennen in der Regel keine freiwillige Einwilligung i.S.v.
  Art. 4 Nr. 11, Art. 7 DSGVO erzeugen; eine gleichwertige Alternative ohne
  Entgelt ist regelmaessig erforderlich. Beleg: edpb.europa.eu, Opinion
  202408_consentorpay. Eigenstaendige „Consent or Pay"-Guidelines standen zum
  2026-11-14 weiterhin im EDSA-Arbeitsprogramm 2026-2027 und waren nicht final
  verabschiedet.
- **DMA-Entscheidung der EU-Kommission vom 23.04.2025 gegen Meta** wegen
  „Pay or Consent"-Werbemodell: Verstoss gegen Art. 5 Abs. 2 DMA (Verknuepfung
  personenbezogener Daten ueber Dienste ohne wirksame Einwilligung); Geldbusse
  **200 Mio. EUR**, erste Nichtkonformitaets-Entscheidung unter dem DMA
  ueberhaupt. Meta hat Nichtigkeitsklage vor dem EuG erhoben (Rechtssache
  T-435/25, Anhaengigkeit laut Amtsblatt-Veroeffentlichung). <<VERIFIKATION AUSSTEHEND>>
  (Press-corner-IP-Nummer im Direkt-Abruf nicht geladen; Beleg ueber
  Sekundaer-Zusammenfassungen, eur-lex-Amtsblatt T-435/25 zu pruefen).
- **DSGVO-Abaenderungen**: Sowohl DSK-Leitfaeden (2023/2024) als auch EDSA-
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

## Aenderungsvermerk

- 2026-11-14: Frontmatter und Disclaimer-Stand auf 2026-11-14 aktualisiert.
  ECLI (ECLI:EU:C:2023:537) in Frontmatter und Kurz-Ueberblick ergaenzt
  (bestaetigt ueber curia.europa.eu / FRA-Caselaw und WebSearch). Grosse Kammer
  und Urteilsdatum 04.07.2023 gegengeprueft. Follow-Up erweitert um EuGH
  C-446/21 (Schrems/Meta, 04.10.2024, Datenminimierung), EDSA-Opinion 08/2024
  „Consent or Pay" (17.04.2024), DMA-Entscheidung der EU-Kommission vom
  23.04.2025 gegen Meta (200 Mio. EUR, Art. 5 Abs. 2 DMA, Klage T-435/25).
  Marker fuer die DMA-Entscheidung gesetzt, weil die Kommissions-Press-Corner-
  URL (IP/25/1085) im Abruf nicht den Volltext lieferte und der genaue Fundstellen-
  Anker der Klage T-435/25 im eur-lex-Amtsblatt noch zu verifizieren ist.
