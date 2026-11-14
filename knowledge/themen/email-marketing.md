---
aktualisiert: 2026-11-14
quelle-primaer: https://www.gesetze-im-internet.de/uwg_2004/__7.html
quellen-sekundaer:
  - https://www.bfdi.bund.de/DE/Buerger/Inhalte/DatenschutzAZ/Werbung/Werbung-node.html
  - https://www.datenschutzkonferenz-online.de/
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

# E-Mail-Marketing — Rechtliche Anforderungen

## Kurz-Ueberblick

E-Mail-Werbung an Verbraucher (B2C) und auch an Geschaeftskunden (B2B) ist in
Deutschland ohne **vorherige ausdrueckliche Einwilligung** (§ 7 Abs. 2 Nr. 2 UWG)
rechtswidrig. Zusaetzlich greifen die DSGVO (Art. 6 Abs. 1 lit. a) und — bei
Kopplung mit Tracking — § 25 TDDDG (das TTDSG wurde am 14.05.2024 durch das
TDDDG abgeloest, materiell inhaltsgleich).

Drei Saeulen der Compliance:

1. **Double-Opt-In** — zweistufige Einwilligung als Beweisstandard.
2. **Bestandskundenausnahme** — § 7 Abs. 3 UWG fuer bestehende Kundenbeziehungen.
3. **Abmelde-/Widerspruchslink** — in jeder einzelnen Werbemail (Art. 21 DSGVO,
   § 7 Abs. 2 Nr. 4 UWG).

## Schluesselparagraphen / Kernaussagen

### § 7 Abs. 2 Nr. 2 UWG — Einwilligungspflicht

Werbung per elektronischer Post (E-Mail, SMS, Messenger) benoetigt eine
**vorherige, ausdrueckliche, freiwillige, informierte, spezifische**
Einwilligung. Die Einwilligung muss in unmittelbarem Zusammenhang mit der
Werbemassnahme erfolgen und der Werbende muss sie nachweisen koennen
(Beweislast beim Versender).

**Konkrete Anforderungen (Double-Opt-In laut BGH I ZR 164/09, 10.02.2011 — "Double-opt-in-Verfahren"):**

1. Formular-Eintrag (Single Opt-In) mit aktiver Handlung (leere Checkbox,
   die der Nutzer anhaken muss, oder expliziter "Anmelden"-Klick).
2. Versand einer **Bestaetigungs-Mail** an die angegebene Adresse mit einem
   **eindeutigen Bestaetigungslink**.
3. Klick auf den Link dokumentiert = Einwilligung.
4. **Logging** des Vorgangs: IP, User-Agent, Timestamp des Eintrags +
   Timestamp der Bestaetigung + genauer Einwilligungstext.

### § 7 Abs. 3 UWG — Bestandskundenausnahme

Vier kumulative Voraussetzungen:

1. E-Mail-Adresse **im Zusammenhang mit dem Verkauf** einer Ware/DL erhalten
   (nicht: nur Newsletter-Anmeldung, nicht: Lead-Magnet-Download).
2. Bewerbung nur fuer **aehnliche eigene** Waren/DL (z.B. Kaffeemaschine
   gekauft → Kaffeekapseln bewerben: OK; Kaffeemaschine gekauft → Waschmaschine
   bewerben: nicht OK).
3. Kunde **hat nicht widersprochen**.
4. Bei Adress-Erhebung UND bei **jeder Verwendung** klarer Hinweis auf
   Widerspruchsrecht (kein Aufwand ueber Basistarif).

### Art. 21 DSGVO — Widerspruchsrecht bei Direktwerbung

Jede betroffene Person hat das Recht, jederzeit der Verarbeitung
personenbezogener Daten zu Zwecken der Direktwerbung zu widersprechen. Der
Widerspruch muss **einfach und kostenfrei** moeglich sein — praktische
Umsetzung: One-Click-Unsubscribe-Link im Footer jeder Werbemail.

### § 6 DDG / § 5 DDG — Identitaet & Kennzeichnung

§ 7 UWG kennt nur die Absaetze 1 bis 3 (Stand 2026-05-08, verifiziert auf
gesetze-im-internet.de/uwg_2004/__7.html). Die Identitaets-/Kennzeichnungs-
pflicht fuer kommerzielle Kommunikation ergibt sich daher aus **§ 6 DDG**
(frueher § 6 TMG) und **§ 5 DDG** (Impressum). Pflichtangaben in der Mail:

- korrekter Absender-Name (kommerzielle Kommunikation klar erkennbar, § 6 DDG)
- gueltige Reply-Adresse
- Impressum / Link zum Impressum (§ 5 DDG)
- bei Werbe-Mails zusaetzlich: Kennzeichnungspflicht nach § 6 DDG, Auftraggeber
  identifizierbar

### Art. 13 DSGVO — Informationspflichten beim Opt-In

Beim Erheben der E-Mail-Adresse muss informiert werden:

- Identitaet des Verantwortlichen
- Zweck (E-Mail-Marketing)
- Rechtsgrundlage (Einwilligung Art. 6 Abs. 1 lit. a DSGVO)
- Empfaenger (insb. externer Newsletter-Provider → **Auftragsverarbeitung
  Art. 28 DSGVO**)
- Speicherdauer
- Rechte (Widerruf, Auskunft, Loeschung)
- ggf. Drittlandtransfer (z.B. Mailchimp → USA → DPF / SCC)

## Typische Fallstricke in Codebases

1. **Single-Opt-In (nur Formular-Submit):** Reicht NICHT, selbst wenn
   DSGVO-Checkbox dabei. Beweislast kann nicht erfuellt werden.
2. **Bestaetigungs-Mail = bereits Werbung:** Die Opt-In-Bestaetigungs-Mail
   darf KEINEN Werbe-Inhalt haben (OLG Muenchen 29 U 1563/20).
3. **Pre-checked Checkbox** bei Signup: nach Planet49 (EuGH C-673/17) unwirksam.
4. **Kopplung mit anderer Leistung** ("Erhalten Sie 10% Rabatt, wenn Sie
   unseren Newsletter abonnieren"): kann zulaessig sein, aber nicht an Vertrag
   koppeln (Art. 7 Abs. 4 DSGVO Kopplungsverbot).
5. **Forward-/Tell-a-Friend-Funktion:** Nachricht an Dritten ohne dessen
   Einwilligung → Direktwerbung des Versenders, abmahnfaehig (BGH I ZR 218/07).
6. **Logging luecken:** Kein Audit-Log → keine Einwilligung nachweisbar →
   Prozess verloren.
7. **Abmeldelink fuehrt zu 404 oder erfordert Login:** verstoesst gegen
   Art. 21 DSGVO / § 7 Abs. 2 Nr. 4 UWG; ein-Klick-Abmeldung Pflicht.
8. **Transaktions-Mail mit Marketing:** "Ihre Rechnung + 'passende Produkte'"
   ist rechtlich Werbung, nicht Transaktion.
9. **Re-Engagement-Kampagnen an alte Listen:** Opt-In > 24 Monate alt? Gefahr,
   dass Einwilligung verfristet / nicht mehr zeitgemaess ist (str., Tendenz
   Aufsicht: ja).
10. **Purchased Lists / Lead-Boersen:** Nahezu immer rechtswidrig (keine
    direkte Einwilligung gegenueber dem Werbenden).

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Signup-Form darf Newsletter-Opt-In NICHT mit ToS-Acceptance
  koppeln. Separate Checkbox "Ich moechte den Newsletter erhalten" (leer).
  Verwendung von react-hook-form + audit-log-Endpunkt.
- **Landingpage:** Lead-Magnet-Download mit Double-Opt-In Kaskade; erste Mail
  enthaelt Lead-Magnet + Opt-In-Bestaetigung gekoppelt → unsauber, besser:
  Bestaetigungs-Mail (nur DOI-Link), dann Lead-Magnet nach Bestaetigung.
- **n8n-Workflows:** Pre-Send-Filter gegen Abmelde-Liste (PostgreSQL-Table
  `unsubscribed_at IS NOT NULL`). Bei Kampagnen: letzten 30 Tage Bounce-Rate
  + Opt-In-Alter als Gating-Kriterium.
- **E-Commerce:** Bestandskundenausnahme § 7 Abs. 3 nutzen: Filter
  "last_order_at > NOW() - INTERVAL 2 YEARS" plus nur fuer "aehnliche
  Produkte" (gleiche Kategorie).
- **Content/Blog:** RSS-to-Email-Automation nur nach DOI; Gastautoren-Kommentar-
  Notifies nur bei Opt-In.

## Behoerden-Hinweise

- **Landes-Datenschutzbehoerden:** zustaendig fuer DSGVO-Verstoesse; Bussgelder
  bis 20 Mio. EUR / 4 % Jahresumsatz.
- **Wettbewerbszentrale, IDO, vzbv:** klassische UWG-Abmahner.
- **BfDI (Bundesbeauftragter):** nur fuer Telekom-/Post-Unternehmen und
  Bundesbehoerden zustaendig.
- **Konferenz der unabhaengigen Datenschutzaufsichtsbehoerden (DSK):**
  Orientierungshilfen: "Werbung" (2022), "Direktwerbung" (FAQ).

## Zitierbare Urteile

- **BGH I ZR 164/09** (10.02.2011 / Folgeurteil 2012, "Double-Opt-In"):
  Anerkennung des DOI-Standards.
- **BGH I ZR 218/07** (10.02.2011, "Payback"): Einwilligung muss bewusst und
  eindeutig sein; Opt-Out-Loesungen nicht ausreichend.
- **BGH I ZR 25/19** (13.01.2022, "Inbox-Werbung II"): Auch Inbox-Placements
  in Freemail-Postfaechern sind Werbung; Einwilligung muss konkrete
  Modalitaeten der Werbe-Einblendung umfassen. Siehe [[urteile/bgh-inbox-werbung]].
- **EuGH C-102/20** (25.11.2021): Vorabentscheidung zum Begriff "elektronische
  Post" — breit auszulegen.
- **EuGH C-673/17** (01.10.2019, "Planet49"): Pre-ticked Checkboxen unwirksam.
- **BGH I ZR 90/20, I ZR 125/20 und I ZR 126/20** (jeweils 09.09.2021,
  "Influencer I/II/III"): Kommerzielle Kommunikation in sozialen Medien
  ist als geschaeftliche Handlung zu kennzeichnen; werblicher Ueberschuss
  begruendet Kennzeichnungspflicht nach § 5a Abs. 4 UWG a. F. / § 5a
  Abs. 6 UWG n. F. (ECLI:DE:BGH:2021:090921UIZR90.20.0,
  ECLI:DE:BGH:2021:090921UIZR125.20.0,
  ECLI:DE:BGH:2021:090921UIZR126.20.0; ueber die Rechtsinformations-API
  des Bundes am 2026-11-14 primaer bestaetigt). Vertiefung in
  [[themen/werbekennzeichnung]].
- **OLG Muenchen 29 U 1563/20**: Bestaetigungs-Mail darf keine Werbung
  enthalten.

## Nicht zitieren: falsch zugeordnete Aktenzeichen

- **BGH I ZR 61/20** — in Vorgaengerfassungen als Teil der Influencer-
  Rechtsprechung vom 09.09.2021 zitiert. Gegenprobe ueber die
  Rechtsinformations-API des Bundes am 2026-11-14: unter diesem Aktenzeichen
  ist nur das Urteil des I. Zivilsenats vom **06.05.2021** gefuehrt
  ("Markenverletzungsstreit: Zurechnungszusammenhang; Die Filsbacher",
  ECLI:DE:BGH:2021:060521UIZR61.20.0). Keine Influencer-Entscheidung unter
  diesem Aktenzeichen nachweisbar; das Influencer-Trio vom 09.09.2021 ist
  I ZR 90/20, I ZR 125/20 und I ZR 126/20 (bereits in
  themen/werbekennzeichnung.md belegt). Zitat daher nicht uebernehmen;
  Aussage bleibt mit Verifikationsmarker.

## Siehe auch

- [[gesetze/uwg]] — § 7 UWG
- [[themen/werbekennzeichnung]]
- [[urteile/bgh-inbox-werbung]]

## Aenderungsvermerk 2026-11-14

- TTDSG-Referenz auf TDDDG (seit 14.05.2024) aktualisiert.
- Tier-3-Quelle (dr-schwenke.de) aus Frontmatter entfernt; war nicht zitierfaehig.
- § 7 UWG gegen gesetze-im-internet.de verifiziert.
- Stand/verifiziert-am auf 2026-11-14 vereinheitlicht.
- **2026-11-14 (Nachlauf PR, API-Gegenprobe)**: BGH I ZR 61/20 ueber die
  Rechtsinformations-API des Bundes abgefragt — Treffer: 06.05.2021
  "Die Filsbacher" (Markenrecht). Gegenstand passt nicht zum Influencer-
  Trio; Zitat aus "Zitierbare Urteile" entfernt und in Hinweisblock
  "Nicht zitieren" dokumentiert. Aussage mit Verifikationsmarker belassen;
  Verweis auf das bereits belegte Trio in themen/werbekennzeichnung.md.
- **2026-11-14 (Review-Korrekturlauf PR #17)**: Influencer-Trio (BGH
  I ZR 90/20, I ZR 125/20, I ZR 126/20 vom 09.09.2021) per Rechts-
  informations-API primaer bestaetigt (ECLI-Ketten
  090921UIZR90.20.0 / 125.20.0 / 126.20.0); Aussage in "Zitierbare
  Urteile" mit Belegen versehen, Verifikationsmarker dort entfernt.
  Hinweisblock zu BGH I ZR 61/20 ("Die Filsbacher", Markenrecht) bleibt
  bestehen.
