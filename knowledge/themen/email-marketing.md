---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/uwg_2004/__7.html
quellen-sekundaer:
  - https://www.bfdi.bund.de/DE/Buerger/Inhalte/DatenschutzAZ/Werbung/Werbung-node.html
  - https://www.datenschutzkonferenz-online.de/
verifiziert-am: 2026-11-14
teilverifiziert-am: 2026-11-15
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
   § 7 Abs. 2 Nr. 3 Buchst. c UWG).

## Schluesselparagraphen / Kernaussagen

### § 7 Abs. 2 Nr. 2 UWG — Einwilligungspflicht

Werbung per elektronischer Post (E-Mail, SMS, Messenger) benoetigt eine
**vorherige, ausdrueckliche, freiwillige, informierte, spezifische**
Einwilligung. Die Einwilligung muss in unmittelbarem Zusammenhang mit der
Werbemassnahme erfolgen und der Werbende muss sie nachweisen koennen
(Beweislast beim Versender).

**Konkrete Anforderungen (Double-Opt-In; zur Rechtsprechung BGH I ZR 164/09, 10.02.2011, "Double-opt-in-Verfahren", siehe unten):**

1. Formular-Eintrag (Single Opt-In) mit aktiver Handlung (leere Checkbox,
   die der Nutzer anhaken muss, oder expliziter "Anmelden"-Klick).
2. Versand einer **Bestaetigungs-Mail** an die angegebene Adresse mit einem
   **eindeutigen Bestaetigungslink**.
3. Klick auf den Link dokumentiert = Einwilligung.
4. **Logging** des Vorgangs: IP, User-Agent, Timestamp des Eintrags +
   Timestamp der Bestaetigung + genauer Einwilligungstext. Das Logging von IP
   und User-Agent ist Praxisempfehlung, keine Vorgabe des Urteils.

### § 7 Abs. 3 UWG — Bestandskundenausnahme

Vier kumulative Voraussetzungen:

1. E-Mail-Adresse **im Zusammenhang mit dem Verkauf** einer Ware/DL erhalten.
   Nach EuGH C-654/23 (Inteligo Media, 13.11.2025, Tenor 1) genuegt auch ein
   kostenloses Nutzerkonto, das Zugang zu Gratisinhalten und einem Newsletter
   gibt und zugleich kostenpflichtige Zusatzangebote eroeffnet. Eine reine
   Newsletter-Anmeldung ohne solchen Angebotsbezug oder ein Lead-Magnet-Download
   genuegen weiterhin nicht (§ 7 Abs. 3 Nr. 1 UWG richtlinienkonform auslegen).
2. Bewerbung nur fuer **aehnliche eigene** Waren/DL (z.B. Kaffeemaschine
   gekauft → Kaffeekapseln bewerben: OK; Kaffeemaschine gekauft → Waschmaschine
   bewerben: nicht OK).
3. Kunde **hat nicht widersprochen**.
4. Bei Adress-Erhebung UND bei **jeder Verwendung** klarer Hinweis auf
   Widerspruchsrecht (kein Aufwand ueber Basistarif).

### Art. 21 DSGVO — Widerspruchsrecht bei Direktwerbung

Jede betroffene Person hat das Recht, jederzeit der Verarbeitung
personenbezogener Daten zu Zwecken der Direktwerbung zu widersprechen
(Art. 21 Abs. 2, 3 DSGVO; unentgeltlich nach Art. 12 Abs. 5 DSGVO).
Praxisempfehlung (keine ausdrueckliche gesetzliche Vorgabe):
One-Click-Unsubscribe-Link im Footer jeder Werbemail.

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
- keine Verschleierung von Absender oder kommerziellem Charakter in Kopf- und
  Betreffzeile (§ 6 Abs. 1 DDG; Verstoss zugleich § 7 Abs. 2 Nr. 3 Buchst. a,
  b UWG)

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

1. **Single-Opt-In (nur Formular-Submit):** hohes Risiko. Die Einwilligung muss
   fuer jeden Empfaenger vollstaendig dokumentiert und nachweisbar sein (BGH
   I ZR 164/09, LS 2); ohne Bestaetigungsschritt (DOI) ist der Nachweis, dass
   der Adressinhaber selbst eingewilligt hat, praktisch kaum zu fuehren.
2. **Bestaetigungs-Mail = bereits Werbung:** Die Opt-In-Bestaetigungs-Mail
   darf KEINEN Werbe-Inhalt haben (OLG Muenchen 29 U 1563/20).
3. **Pre-checked Checkbox** bei Signup: nach Planet49 (EuGH C-673/17) unwirksam.
4. **Kopplung mit anderer Leistung** ("Erhalten Sie 10% Rabatt, wenn Sie
   unseren Newsletter abonnieren"): kann zulaessig sein, aber nicht an Vertrag
   koppeln (Art. 7 Abs. 4 DSGVO, sogenanntes Kopplungsverbot; nach dem
   Wortlaut ein Beruecksichtigungsgebot, kein absolutes Verbot).
5. **Forward-/Tell-a-Friend-Funktion:** Nachricht an Dritten ohne dessen
   Einwilligung → Direktwerbung des Versenders, abmahnfaehig (BGH, Urteil vom
   12.09.2013, I ZR 208/12, Empfehlungs-E-Mail).
6. **Logging luecken:** Kein Audit-Log → keine Einwilligung nachweisbar →
   Prozess verloren.
7. **Abmeldelink fuehrt zu 404 oder erfordert Login:** verstoesst gegen
   Art. 21 Abs. 2, 3 DSGVO / § 7 Abs. 2 Nr. 3 Buchst. c, Abs. 3 Nr. 4 UWG: Die
   Abmeldung muss jederzeit moeglich sein. Ein Abmeldelink mit einem Klick ist
   Praxisempfehlung, keine gesetzliche Pflicht.
8. **Transaktions-Mail mit Marketing:** "Ihre Rechnung + 'passende Produkte'"
   ist rechtlich Werbung, nicht Transaktion.
9. **Re-Engagement-Kampagnen an alte Listen:** Eine Einwilligung erlischt
   grundsaetzlich nicht allein durch Zeitablauf (BGH, Urt. v. 01.02.2018,
   III ZR 196/17, Rn. 31). Eine feste 24-Monats-Frist gibt es nicht. Die DSK
   haelt es aber fuer moeglich, dass sich Verantwortliche auf eine lange
   ungenutzte Einwilligung nicht mehr berufen koennen, und empfiehlt, bei
   laenger als zwei Jahre ungenutzten Einwilligungen vorsorglich die
   Information oder die Einwilligung zu erneuern (OH Direktwerbung, Februar
   2022, Ziff. 3.5).
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
- **BfDI (Bundesbeauftragter):** zustaendig fuer oeffentliche Stellen des
  Bundes und fuer Unternehmen, soweit sie Daten fuer geschaeftsmaessige
  Telekommunikationsdienste verarbeiten (§ 9 Abs. 1 BDSG, § 29 TDDDG) sowie
  spezialgesetzlich fuer Postdienste; fuer uebrige Unternehmen die
  Landesbehoerde am Sitz.
- **Konferenz der unabhaengigen Datenschutzaufsichtsbehoerden (DSK):**
  Orientierungshilfe der Aufsichtsbehoerden zur Verarbeitung von
  personenbezogenen Daten fuer Zwecke der Direktwerbung unter Geltung der
  DS-GVO (18.02.2022).

## Zitierbare Urteile

- **BGH I ZR 164/09** (10.02.2011, "Double-opt-in-Verfahren"): vollstaendige
  Dokumentation jeder Einwilligung erforderlich (LS 2); die DOI-Bestaetigung
  belegt keine Einwilligung in Telefonwerbung (LS 3); bei E-Mail-Werbung ist
  die Einwilligung nach bestaetigter Adresse grundsaetzlich hinreichend
  dokumentiert (Rn. 37), der Verbraucher traegt die Darlegungslast, wenn er
  sie bestreitet (LS 4). Logging von IP und User-Agent ist
  Praxisempfehlung, keine Vorgabe des Urteils.
- **BGH, Beschl. v. 20.05.2009, I ZR 218/07** ("E-Mail-Werbung II"): Werbung
  per E-Mail ohne vorherige ausdrueckliche Einwilligung ist stets unzumutbare
  Belaestigung (so zitiert in BGH VI ZR 225/17).
- **BGH, Urt. v. 16.07.2008, VIII ZR 348/06** (BGHZ 177, 253): Opt-Out-Loesungen
  nicht ausreichend. <<VERIFIKATION AUSSTEHEND>>
- **BGH I ZR 25/19** (13.01.2022, "Inbox-Werbung II"): Auch Inbox-Placements
  in Freemail-Postfaechern sind Werbung; Einwilligung muss konkrete
  Modalitaeten der Werbe-Einblendung umfassen. Siehe [[urteile/bgh-inbox-werbung]].
- **EuGH C-102/20** (25.11.2021): Inbox-Werbung ist Verwendung elektronischer
  Post fuer Direktwerbung (Tenor 1).
- **EuGH C-673/17** (01.10.2019, "Planet49"): Pre-ticked Checkboxen unwirksam.
- **EuGH C-654/23** (13.11.2025, "Inteligo Media"): E-Mail-Adresse "im
  Zusammenhang mit dem Verkauf eines Produkts oder einer Dienstleistung"
  erhalten, wenn der Nutzer ein kostenloses Konto mit Zugang zu einer
  begrenzten Zahl von Artikeln und einem taeglichen Newsletter einrichtet und
  gegen Bezahlung auf zusaetzliche Artikel zugreifen kann (Tenor 1).
- Die Urteile des BGH vom 09.09.2021 (I ZR 90/20 "Influencer I",
  I ZR 125/20 "Influencer II", I ZR 126/20) ergingen zu § 5a Abs. 6
  UWG a. F.; die Regelung steht seit dem 28.05.2022 in § 5a Abs. 4
  UWG. Das Merkmal der Gegenleistung leitete der BGH aus § 6 Abs. 1
  Nr. 1 TMG und § 22 Abs. 1 Satz 1 MStV ab, deren Wertung § 5a Abs. 6
  UWG a. F. nicht unterlaufen darf (I ZR 125/20, Leitsaetze 1 und 2);
  seit 28.05.2022 steht es in § 5a Abs. 4 Satz 2 UWG. Geltende
  Fassung: "Ein kommerzieller Zweck liegt bei einer Handlung zugunsten
  eines fremden Unternehmens nicht vor, wenn der Handelnde kein
  Entgelt oder keine aehnliche Gegenleistung fuer die Handlung von
  dem fremden Unternehmen erhaelt oder sich versprechen laesst. Der
  Erhalt oder das Versprechen einer Gegenleistung wird vermutet, es
  sei denn der Handelnde macht glaubhaft, dass er eine solche nicht
  erhalten hat." (§ 5a Abs. 4 Saetze 2 und 3 UWG). Nach den Urteilen
  vom 09.09.2021 war ein Beitrag ohne Gegenleistung nur bei
  werblichem Ueberschuss eine geschaeftliche Handlung zugunsten des
  fremden Unternehmens (I ZR 90/20, Leitsatz 4); nach § 5a Abs. 4
  Satz 2 UWG n. F. kommt es fuer die Kennzeichnungspflicht nach § 5a Abs. 4 UWG darauf nicht mehr an; eine Gegenleistung wird jedoch vermutet (Satz 3). Eigenwerbung ist
  regelmaessig eine geschaeftliche Handlung zugunsten des eigenen
  Unternehmens (I ZR 90/20, Leitsatz 2); das Merkmal der Gegenleistung gilt dafuer nicht
  (I ZR 125/20, Leitsatz 2). ECLI-Belege:
  ECLI:DE:BGH:2021:090921UIZR90.20.0,
  ECLI:DE:BGH:2021:090921UIZR125.20.0,
  ECLI:DE:BGH:2021:090921UIZR126.20.0,
  ECLI:DE:BGH:2022:130122UIZR35.21.0 (ueber die Rechtsinformations-API
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
  themen/werbekennzeichnung.md belegt). Zitat daher nicht uebernehmen.
- **BGH I ZR 218/07**: in Vorgaengerfassungen als Beleg fuer Tell-a-Friend-
  Werbung und mit Datum 10.02.2011 / "Payback" zitiert. Tatsaechlich: Beschluss
  vom 20.05.2009, "E-Mail-Werbung II". Beleg fuer Empfehlungs-E-Mails ist
  BGH I ZR 208/12 (12.09.2013).

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
- **2026-11-14 (Review-Korrekturlauf PR #17, Nachtrag)**: Normangabe
  zum Influencer-Trio richtig zugeordnet (§ 5a Abs. 6 UWG a. F. =
  § 5a Abs. 4 UWG n. F., Fassung seit 28.05.2022), Aussage am
  Gesetzeswortlaut von § 5a Abs. 4 Satz 2 und 3 UWG geschaerft; BGH
  I ZR 35/21 (13.01.2022, "Influencer III", ECLI:DE:BGH:2022:
  130122UIZR35.21.0) ergaenzt. Grundlage: § 5a UWG auf gesetze-im-
  internet.de/uwg_2004/__5a.html (abgerufen 2026-11-14) sowie
  Treffer der Rechtsinformations-API des Bundes.
- **2026-11-14 (Review-Korrekturlauf PR #17, Influencer-Absatz)**:
  Darstellung der BGH-Influencer-Rechtsprechung und von § 5a Abs. 4
  UWG wortgleich am Gesetzeswortlaut (§ 5a Abs. 4 Saetze 2 und 3 UWG)
  und an den Leitsaetzen von I ZR 90/20 (Leitsaetze 4 und 5) und
  I ZR 125/20 (Leitsaetze 1 und 2) ausgerichtet; Aussagen ohne
  Quellenbeleg entfernt.
- **2026-11-14 (Nachzug Review, Leitsatz-Zuordnung)**: Eigenwerbung-Beleg auf I ZR 90/20 Leitsatz 2 und I ZR 125/20 Leitsatz 2 getrennt, Vermutung der Gegenleistung auf § 5a Abs. 4 Satz 3 UWG gestellt (statt Satz 2), Formulierung am Gesetzeswortlaut ausgerichtet.
- **2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1)**:
  Abmeldeadresse auf § 7 Abs. 2 Nr. 3 Buchst. c UWG umgestellt; § 6 Abs. 2
  DDG ergaenzt; Tell-a-Friend auf BGH I ZR 208/12 umgestellt, I ZR 218/07
  richtig als E-Mail-Werbung II (20.05.2009) zugeordnet; VIII ZR 348/06 mit
  Verifikationsmarker; I ZR 164/09 und EuGH C-102/20 praezisiert; feste
  24-Monats-Frist fuer Einwilligungen gestrichen (BGH III ZR 196/17, Rn. 31);
  Art. 7 Abs. 4, Art. 21, Art. 12 Abs. 5 DSGVO praezisiert; DSK OH
  Direktwerbung (18.02.2022) zitiert.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2):
  Bestandskundenausnahme um EuGH C-654/23 (Tenor 1) ergaenzt; Single-Opt-In
  als hohes Risiko mit BGH I ZR 164/09, LS 2 statt "reicht nicht"; DSK-Hinweis
  zu lange ungenutzten Einwilligungen (OH Direktwerbung, Ziff. 3.5); BfDI-
  Zustaendigkeit praezisiert.
