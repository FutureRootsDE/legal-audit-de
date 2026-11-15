---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/ddg/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/ddg/__5.html
  - https://www.bmj.de/DE/themen/digitales/digitale_dienste/DDG/DDG_node.html
verifiziert-am: 2026-11-14
teilverifiziert-am: 2026-11-15
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

# DDG — Digitale-Dienste-Gesetz

## Kurz-Ueberblick

Das **Digitale-Dienste-Gesetz (DDG)** vom 06.05.2024 (BGBl. 2024 I Nr. 149,
verkuendet am 13.05.2024) ist am **14. Mai 2024** in Kraft getreten und loest
das bisherige Telemediengesetz (TMG) und Teile des Netzwerkdurchsetzungs-
gesetzes (NetzDG) ab. Es dient der Umsetzung und Durchfuehrung der
EU-Verordnung **Digital Services Act (DSA) 2022/2065**.

Fassung: zuletzt geaendert durch Art. 1 G v. 12.05.2026 (BGBl. 2026 I Nr. 138).

Fuer die Anbieter von Websites, Online-Shops, Apps und SaaS-Portalen ist vor
allem **§ 5 DDG** (Impressumspflicht) praxisrelevant — inhaltlich unveraendert
gegenueber dem frueheren § 5 TMG.

## Schluesselparagraphen / Kernaussagen

### § 5 DDG — Allgemeine Informationspflichten (Impressumspflicht)

Diensteanbieter muessen fuer geschaeftsmaessige, in der Regel gegen Entgelt
angebotene digitale Dienste folgende Informationen **leicht erkennbar, unmittelbar
erreichbar und staendig verfuegbar** halten:

**Abs. 1 Nr. 1 — Identitaet:**

- Name und Anschrift, unter der sie niedergelassen sind
- bei juristischen Personen: Rechtsform, Vertretungsberechtigter
- ggf. Angaben zum gezeichneten Kapital und noch ausstehenden Einlagen

**Abs. 1 Nr. 2 — Schnelle Kontaktaufnahme:**

- Angaben, die eine schnelle elektronische Kontaktaufnahme und unmittelbare
  Kommunikation ermoeglichen
- insbesondere **E-Mail-Adresse**
- zweiter Kommunikationsweg neben der E-Mail-Adresse (z.B. Telefon oder
  elektronisches Kontaktformular), abgeleitet aus EuGH C-298/07 (16.10.2008),
  nicht aus C-649/17

**Abs. 1 Nr. 3 — Behoerdliche Zulassung:**

- soweit erforderlich: Angaben zur zustaendigen Aufsichtsbehoerde
  (z.B. bei erlaubnispflichtigen Taetigkeiten: Makler, Versicherungsvermittler,
  Anwaelte, Steuerberater, Heilberufe)

**Abs. 1 Nr. 4 — Registereintrag:**

- Handelsregister, Vereinsregister, Partnerschaftsregister,
  Genossenschaftsregister + Registernummer

**Abs. 1 Nr. 5 — Berufsbezeichnung (reglementiert):**

- Kammer
- gesetzliche Berufsbezeichnung und Staat der Verleihung
- Bezeichnung der berufsrechtlichen Regelungen und Link / Fundstelle

**Abs. 1 Nr. 6 — Steuernummern:**

- Umsatzsteuer-Identifikationsnummer nach § 27a UStG, sofern vorhanden
- alternativ: Wirtschafts-Identifikationsnummer nach § 139c AO

**Abs. 1 Nr. 7 — Liquidations-/Abwicklungsstatus:**

- AG, KGaA, GmbH: Hinweis auf Abwicklung oder Liquidation

**Abs. 1 Nr. 8 — Audiovisuelle Mediendienste:**

- Sitzstaat
- zustaendige Regulierungs-/Aufsichtsbehoerde

### § 18 Medienstaatsvertrag (MStV) — Verantwortlicher i.S. Presserecht

Fuer journalistisch-redaktionell gestaltete Angebote (insbesondere solche, die
Inhalte periodischer Druckerzeugnisse wiedergeben; bei Blogs, News-Sites und
Podcasts im Einzelfall pruefen) ist zusaetzlich ein **Verantwortlicher nach
§ 18 Abs. 2 MStV** mit Namen und Anschrift zu benennen. Er muss den
staendigen Aufenthalt im Inland haben, unbeschraenkt geschaeftsfaehig und
strafrechtlich verfolgbar sein und darf die Faehigkeit zur Bekleidung
oeffentlicher Aemter nicht verloren haben. Bei mehreren Verantwortlichen ist
die Zustaendigkeit je Teil kenntlich zu machen.

### Weitere Normen im DDG

- **§ 7 DDG** — Die Haftungsprivilegien fuer reine Durchleitung, Caching
  und Hosting folgen unmittelbar aus Art. 4 bis 6 DSA, ergaenzt durch
  Art. 7 und 8 DSA; § 7 Abs. 1 DDG erstreckt Art. 4 bis 8 DSA auf alle
  Diensteanbieter.
- **§§ 12 bis 21 DDG** — zustaendige Behoerden und Koordinierungsstelle fuer
  digitale Dienste bei der Bundesnetzagentur; §§ 24 bis 32 DDG Befugnisse;
  § 33 DDG Bussgelder.
- Trusted Flagger (Art. 22 DSA) und internes Beschwerdemanagement
  (Art. 20 DSA) sind im DSA geregelt, nicht in §§ 17 ff. DDG.

## Typische Fallstricke in Codebases

1. **Impressum zu tief verlinkt:** Die Pflichtangaben muessen leicht erkennbar,
   unmittelbar erreichbar und staendig verfuegbar sein (§ 5 Abs. 1 DDG).
2. **Nur "impressum@..."-Mailto:** E-Mail-Adresse plus ein weiterer Weg, der
   eine schnelle Kontaktaufnahme und unmittelbare, effiziente Kommunikation
   ermoeglicht; eine Telefonnummer ist nicht zwingend, eine elektronische
   Anfragemaske kann genuegen (EuGH C-298/07, Tenor).
3. **Keine USt-IdNr trotz vorhandener:** Wenn eine USt-IdNr vorhanden ist, MUSS
   sie ins Impressum — "sofern vorhanden" heisst nicht "optional wenn egal".
4. **Kein Impressum auf Landingpage-Varianten:** Jede oeffentlich erreichbare
   Variante eines geschaeftsmaessigen Dienstes muss die Pflichtangaben leicht
   erkennbar, unmittelbar erreichbar und staendig verfuegbar halten
   (§ 5 Abs. 1 DDG); ein klar bezeichneter Link genuegt, eine ausgenommene
   "private" Sub-Route gibt es nicht.
5. **Social-Media-Profile ohne Impressum:** Instagram/TikTok/YouTube-Profile
   mit geschaeftlicher Nutzung brauchen Impressum — typisch: Link in Bio.
6. **Fehlender MStV-Verantwortlicher bei Blog:** Redaktionelle Beitraege ohne
   genannten "verantwortlich nach § 18 Abs. 2 MStV" sind abmahnfaehig.
7. **API-gesteuerte Impressumsdaten:** CMS-Feld "company_name" leer in
   Staging-/Preview-Builds → Impressum-Validator fehlt.
8. **Bussgeld:** Ein fehlendes, unrichtiges oder unvollstaendiges Impressum
   ist eine Ordnungswidrigkeit nach § 33 Abs. 2 Nr. 1 DDG, Geldbusse bis
   50.000 EUR (§ 33 Abs. 6 Nr. 3 DDG); daneben wettbewerbsrechtliches
   Abmahnrisiko.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** `/impressum`-Route mit Server-gerendertem Content,
  automatische Pflege aus zentraler "company"-Config; Footer-Link auf allen
  Seiten (inkl. Auth-Routes, 404).
- **Landingpage:** Impressum + Datenschutz MUSSEN vorhanden sein, auch bei
  Coming-Soon-Pages, sobald Business-Kontext erkennbar.
- **n8n-Workflows:** Falls Workflow eine oeffentliche Webhook-UI (Forms)
  bereitstellt, Impressum in Form-Footer einbauen.
- **E-Commerce:** Shop-Templates pflegen Impressum meist automatisch;
  dennoch Kategorie-, Produkt- und Checkout-Seiten pruefen.
- **Content/Blog:** Zusaetzlich MStV-Verantwortlicher; bei Gastautoren ggf.
  pro Artikel "Autor"-Angabe.

## Behoerden-Hinweise

- **Bundesnetzagentur (BNetzA)** — Koordinierungsstelle fuer digitale
  Dienste nach § 12 Abs. 1 DDG seit Inkrafttreten des DDG am 14.05.2024
  (der DSA gilt seit 17.02.2024), zustaendig fuer DSA-Durchsetzung.
- **Landesmedienanstalten:** Aufsicht nach dem MStV (§ 104 Abs. 1);
  Massnahmen (§ 109 Abs. 1) und Bussgeld (§ 115 Abs. 1 Satz 2 Nr. 1) bei
  Verstoessen gegen § 18 Abs. 1 MStV (Name und Anschrift). § 18 Abs. 2 MStV
  (Verantwortlicher bei journalistisch-redaktionellen Angeboten) ist von den
  Massnahmen nach § 109 Abs. 1 ausgenommen.
- **Landes-Datenschutzbehoerden** — nicht fuer Impressum, aber oft angrenzend
  (Datenschutzerklaerung).

## Zitierbare Urteile

- Aussage: Das Impressum muss leicht erkennbar, unmittelbar erreichbar und
  staendig verfuegbar sein (§ 5 Abs. 1 DDG). Ob ein Weg ueber zwei Klicks
  genuegt ("Zwei-Klick-Regel"), ist nicht primaer belegt. <<VERIFIKATION AUSSTEHEND>>
- **EuGH C-298/07** (16.10.2008, "deutsche internet versicherung AG"):
  Zweiter Kommunikationsweg neben E-Mail erforderlich.
- Aussage: Anforderung an verstaendliche, deutschsprachige Kontaktaufnahme
  im Impressum. <<VERIFIKATION AUSSTEHEND>> (vgl. Abschnitt "Nicht zitieren")
- **OLG Duesseldorf I-20 U 17/07** (18.12.2007,
  ECLI:DE:OLGD:2007:1218.I20U17.07.00): Auch wer eigene Angebotsseiten
  innerhalb eines fremden Portals betreibt, muss dort ein Impressum
  vorhalten; keine Aussage zu Mobilnummern.
- **BGH, Urt. v. 25.02.2016, I ZR 238/14, Mehrwertdienstenummer**
  (ECLI:DE:BGH:2016:250216UIZR238.14.0): Eine kostenpflichtige
  Mehrwertdienstenummer neben der E-Mail-Adresse ist kein ausreichender
  weiterer Kommunikationsweg i. S. d. § 5 Abs. 1 Nr. 2 TMG (jetzt DDG).
- **OLG Muenchen 29 U 3698/20** zur Impressumspflicht bei
  Instagram-Business-Profilen. <<VERIFIKATION AUSSTEHEND>>

## Nicht zitieren: falsch zugeordnete Aktenzeichen

- **BGH I ZR 228/14** — in Vorgaengerfassungen dieser KB als Impressum-
  Entscheidung "English alphabet" vom 07.07.2016 gefuehrt. Gegenprobe ueber
  die Rechtsinformations-API des Bundes am 2026-11-14: unter diesem
  Aktenzeichen ist nur das Urteil des I. Zivilsenats vom **17.09.2015**
  gefuehrt ("Ramses — Kabelweitersendung durch Uebertragung von mit einer
  Gemeinschaftsantenne der Wohnanlage empfangenen Fernseh- oder Hoerfunk-
  signalen", Urheberrecht). Eine Impressum-/Kontaktaufnahme-Entscheidung
  unter diesem Aktenzeichen ist dort nicht nachweisbar. Zitat daher nicht
  uebernehmen; die zugrundeliegende Aussage bleibt mit Verifikationsmarker.
- **BGH I ZR 151/02**: in Vorgaengerfassungen dieser KB als Entscheidung
  zur Anbieterkennzeichnung im Internet vom 20.07.2006 gefuehrt. Das gemeinte
  Urteil ist **BGH I ZR 228/03** vom 20.07.2006 (Anbieterkennzeichnung im
  Internet, GRUR 2007, 159).

## Siehe auch

- [[themen/impressum]]
- [[gesetze/uwg]] — Impressumsverletzung = UWG-Verstoss ueber § 3a UWG
- [[gesetze/bgb-agb]]

## Aenderungsvermerk

- **2026-11-14**: Frontmatter-Datum und Disclaimer-Stand aktualisiert.
  Fundstelle BGBl. 2024 I Nr. 149 (verkuendet 13.05.2024, Ausfertigung
  06.05.2024) ergaenzt. Materielle Inhalte (§ 5 DDG, §§ 7-16 DDG, § 18 MStV)
  gegen gesetze-im-internet.de/ddg abgeglichen. (Korrektur 2026-11-15: Der
  Vermerk "unveraendert" war nicht haltbar; das DDG ist zuletzt geaendert
  durch Art. 1 G v. 12.05.2026 (BGBl. 2026 I Nr. 138).)
- **2026-11-14 (Nachlauf PR, API-Gegenprobe)**: BGH I ZR 228/14 ueber die
  Rechtsinformations-API des Bundes abgefragt — Treffer: 17.09.2015
  "Ramses", Urheberrecht. Gegenstand passt nicht zu Impressum; Zitat aus
  "Zitierbare Urteile" entfernt und in Hinweisblock "Nicht zitieren"
  dokumentiert, Aussage mit Verifikationsmarker belassen.
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  "digitale Dienste" statt "Telemedien" in § 5; zweiter Kommunikationsweg
  aus EuGH C-298/07; Aufsichtsbehoerde ohne Anschriftspflicht; Normueberblick
  (§ 7, §§ 12 bis 21, 24 bis 33 DDG; Trusted Flagger und Beschwerdemanagement
  im DSA); BGH I ZR 228/03 statt I ZR 151/02 (in "Nicht zitieren"
  eingetragen); Zeile BGH I ZR 228/03 vom 14.07.2005 gestrichen; OLG
  Duesseldorf I-20 U 17/07 inhaltlich korrigiert; BNetzA seit 14.05.2024;
  Landesmedienanstalten (MStV); Fassungsangabe ergaenzt.
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2):
  BGH I ZR 238/14 (Mehrwertdienstenummer) aufgenommen; Kontaktweg nach
  EuGH C-298/07 ohne "Chat"; MStV-Verantwortlicher nach § 18 Abs. 2 MStV
  (Voraussetzungen, kein "ladungsfaehig, kein Postfach"); Bussgeld nach § 33
  DDG; Klick-Aussage ohne Aktenzeichen, Zwei-Klick-Aussage mit
  Verifikationsmarker.
