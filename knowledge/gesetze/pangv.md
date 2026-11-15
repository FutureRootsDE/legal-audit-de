---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/pangv_2022/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/pangv_2022/__11.html
  - https://www.bmwk.de/Redaktion/DE/Artikel/Wirtschaft/preisangabenverordnung.html
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
>
> **Fassung:** Ausfertigung 12.11.2021 (BGBl. I S. 4921), in Kraft seit
> 28.05.2022. Letzte Aenderung durch **Art. 3 des Gesetzes zur Aenderung
> des Preisangabenrechts zur Sanktionierung von Verstoessen gegen
> nationale und europaeische Regelungen ueber Preisangaben vom 19.10.2026
> (BGBl. 2026 I Nr. 314, verkuendet 22.10.2026)**. Art. 3 aendert allein
> **§ 20 PAngV** (Verweis auf das geaenderte Preisangabengesetz (PAngG vom
> 03.12.1984; durch Art. 1 geaendert) statt auf
> § 3 Abs. 1 Satz 1 Nr. 2 WiStG 1954); die materiellen Vorschriften zu
> Gesamtpreis, Grundpreis, Versandkosten, 30-Tage-Referenzpreis (§ 11)
> und Dienstleistungen bleiben unveraendert. Inkrafttreten der Aenderung:
> **01.01.2027** (Art. 4). Quelle: recht.bund.de/bgbl/1/2026/314/VO.html,
> abgerufen 2026-11-14.

# PAngV 2022 — Preisangabenverordnung (Neufassung)

## Kurz-Ueberblick

Die Preisangabenverordnung (PAngV) regelt, wie Unternehmen gegenueber Verbrauchern
Preise auszuzeichnen haben. Die **Neufassung trat am 28.05.2022 in Kraft**
(Umsetzung der EU-Omnibus-Richtlinie 2019/2161). Wichtigste Neuerung: § 11
PAngV mit der **30-Tage-Streichpreis-Regel**.

Verstoesse gegen die PAngV sind wettbewerbsrechtlich abmahnfaehig. Fuer § 11
Abs. 1 PAngV beurteilt der BGH die Unlauterkeit nach §§ 5a, 5b UWG und nicht
nach § 3a UWG (BGH I ZR 183/24, LS 2); fuer andere PAngV-Pflichten im Einzelfall
pruefen.

## Schluesselparagraphen / Kernaussagen

### § 1 PAngV — Anwendungsbereich, Grundsatz

§ 1 PAngV regelt den Anwendungsbereich (Unternehmer gegenueber Verbrauchern)
sowie Preisklarheit und Preiswahrheit (Abs. 3); die Pflicht zur
Gesamtpreisangabe folgt aus § 3 Abs. 1.

### § 3 PAngV — Pflicht zur Angabe des Gesamtpreises

"Gesamtpreis" = Endpreis einschliesslich Umsatzsteuer und sonstiger
Preisbestandteile. Fuer Versandhandel: zusaetzlich Hinweis, ob Liefer- und
Versandkosten anfallen und in welcher Hoehe (§ 6 PAngV).

### § 4 PAngV — Grundpreisangabe

Wer Waren in Fertigpackungen, offenen Packungen oder als Verkaufseinheiten ohne
Umhuellung **nach Gewicht, Volumen, Laenge oder Flaeche** anbietet, muss
neben dem Gesamtpreis auch den **Grundpreis** (je 1 kg / 1 l / 1 m / 1 m²)
angeben.

Ausnahmen nach § 4 Abs. 3 Nrn. 1 bis 8 PAngV, u.a. fuer:

- Waren < 10 g/10 ml
- Waren, die im Rahmen einer Dienstleistung angeboten werden (§ 4 Abs. 3
  Nr. 4)

### § 11 PAngV — Streichpreis-Regel (30-Tage)

**Abs. 1:** "Wer zur Angabe eines Gesamtpreises verpflichtet ist, hat gegenueber
Verbrauchern bei jeder Bekanntgabe einer Preisermaessigung fuer eine Ware den
**niedrigsten Gesamtpreis** anzugeben, den er innerhalb der letzten **30 Tage**
vor der Anwendung der Preisermaessigung gegenueber Verbrauchern angewendet hat."

**Abs. 2 — Progressive Rabatte:** Bei einer schrittweise erhoehten Preis-
ermaessigung darf als Vergleichspreis derjenige Preis verwendet werden, der vor
Beginn der ersten Ermaessigung galt — vorausgesetzt, die Ermaessigungsstufen
folgen ohne Unterbrechung aufeinander.

**Abs. 3:** Fuer Anbieter, die nach § 4 nur Grundpreise angeben muessen, gilt
die Regel entsprechend.

**Abs. 4 — Ausnahmen:**

- individuelle, auf einen bestimmten Kunden bezogene Preisermaessigungen
- Preisherabsetzungen verderblicher Waren (bei drohendem Verderb / Ablauf),
  wenn die Herabsetzung eindeutig gekennzeichnet ist

### § 12 PAngV — Leistungen (DL)

§ 12 PAngV: Preisverzeichnis ueber die wesentlichen Leistungen oder ueber
Verrechnungssaetze; Ausnahmen nach Abs. 4 (u. a. Leistungen auf Grund
schriftlicher Einzelangebote).

## Typische Fallstricke in Codebases

1. **Hardcoded Streichpreise ohne Audit-Trail:** Der "999 EUR statt 1999 EUR"-
   Rabatt muss als **Vergleich mit der unverbindlichen Preisempfehlung des
   Herstellers**, klar als UVP gekennzeichnet, ODER als **Streichpreis aus
   30-Tage-Historie** (§ 11) klar gekennzeichnet werden. Ob § 11 PAngV beim
   UVP-Vergleich greift, haengt davon ab, ob die Darstellung als Ermaessigung
   des eigenen Preises verstanden wird; im Einzelfall pruefen. Ohne DB-Historie
   unmoeglich zu rechtfertigen.
2. **Black-Friday-Pseudo-Rabatte:** Preise kurz vor Aktion erhoehen, dann
   "reduzieren" ist klassischer Verstoss.
3. **Dynamic Pricing (A/B Test):** Wenn Preis B an einige User getestet wird,
   kann "niedrigster Preis der 30 Tage" aus B-Cohort resultieren — Streichpreis
   muss sich daran orientieren.
4. **Grundpreis fehlt in Produktkachel:** Suchergebnislisten, Kategorieseiten,
   Social-Ads muessen Grundpreis enthalten, wenn § 4 greift.
5. **Versandkosten-Hinweis zu spaet im Checkout:** Der Hinweis auf
   Umsatzsteuer und Versandkosten ist bereits beim Angebot zu geben (§ 6
   Abs. 1, 2 PAngV), nicht erst im Checkout; zusaetzlich unmittelbar vor der
   Bestellung nach § 312j Abs. 2 BGB.
6. **Abo-Preise / Aktions-Zeitraum:** Bei "erster Monat gratis, dann X EUR"
   muss der regulaere Preis klar erkennbar sein.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Preistabellen mit "Normal-/Aktionspreis" benoetigen einen
  Price-History-Service mit 30-Tage-Logik vor Angabe eines Streichpreises.
- **Landingpage:** Rabatt-Banner ("50% Off!") brauchen Nachweis des
  Originalpreises — speichere Preise inkl. Timestamps.
- **n8n-Workflows:** Produkt-Sync mit Shopify/Shopware → Preis-History-Tabelle
  fuehren; Workflows, die "aktuelle Rabatte" aus externen Feeds uebernehmen,
  muessen § 11 pruefen.
- **E-Commerce (Shopify/WooCommerce/Shopware):** Streichpreis-Feld
  (compare_at_price) muss datenschutzkonform und regel-konform gefuellt werden;
  ohne 30-Tage-Historie: leer lassen oder nur UVP zeigen.
- **Content/Blog:** Deal-Seiten, die fremde Shop-Preise bewerben, sollten
  Disclaimer + Timestamp-Angabe verwenden; Gefahr der Mithaftung reduziert.

## Behoerden-Hinweise

- **Zustaendige Behoerde:** Landes-Eichbehoerden / Gewerbeaufsicht; Ordnungs-
  widrigkeiten nach § 20 PAngV: bis 31.12.2026 Geldbusse bis **25.000 EUR**
  (§ 3 Abs. 2 WiStG 1954); ab 01.01.2027 bis **100.000 EUR** (§ 3 Abs. 3
  PAngG n. F., G v. 19.10.2026, BGBl. 2026 I Nr. 314).
- **Abmahnungen:** regelmaessig durch Wettbewerbszentrale, IDO, vzbv.

## Zitierbare Urteile

- **OLG Hamburg, Beschl. v. 12.12.2022 — 3 W 38/22**: Zu § 11 PAngV
  (30-Tage-Streichpreis-Regel). Klarstellung: Eine bloße Angabe des
  niedrigsten Referenzpreises (Streichpreis) genuegt; eine zusaetzliche
  Erlaeuterung des Vergleichszeitraums ist nicht erforderlich. Verbraucher
  duerfen davon ausgehen, dass es sich um den vorherigen Verkaufspreis handelt.
  (Hinweis: Vorgaengerfassung dieser KB nannte fehlerhaft "OLG Hamburg
  3 U 37/22" — diese Zitation war nicht gegen rechtsprechung-im-internet
  belegbar; korrigiert am 2026-05-08.)
- **EuGH C-330/23** (Urt. v. 26.09.2024, "Aldi Sued"): Wird eine
  Preisermaessigung als Prozentsatz oder mit einer Werbeaussage zur
  Vorteilhaftigkeit bekanntgegeben, muss sie auf Grundlage des "vorherigen
  Preises", d. h. des niedrigsten Preises der letzten 30 Tage, berechnet sein.

## Nicht zitieren: falsch zugeordnete Aktenzeichen

- **BGH I ZR 173/16** — in Vorgaengerfassungen dieser KB als Preisangabe-
  Entscheidung ("auf einen Blick", 31.10.2018) zitiert. Gegenprobe ueber die
  Rechtsinformations-API des Bundes am 2026-11-14 ergibt: unter diesem
  Aktenzeichen gibt es nur das Urteil des I. Zivilsenats vom **12.12.2019**
  ("OeKO-TEST I", ECLI:DE:BGH:2019:121219UIZR173.16.0) zur Verletzung einer
  Unionsmarke; eine Preisangaben-Entscheidung unter diesem Aktenzeichen ist
  dort nicht nachweisbar. Zitat daher nicht uebernehmen; Befund geklaert
  (siehe themen/preisangaben.md).
- **BGH I ZR 143/19** — in Vorgaengerfassungen dieser KB als "Sofort
  lieferbar"-Entscheidung (05.11.2020) zur Kopplung Lieferzeit + Preis zitiert.
  Gegenprobe ueber die Rechtsinformations-API des Bundes am 2026-11-14 ergibt:
  unter diesem Aktenzeichen sind nur das Urteil des I. Zivilsenats vom
  **07.04.2022** ("Knuspermuesli II", ECLI:DE:BGH:2022:070422UIZR143.19.0,
  Lebensmittelinformations-Pflichten) und der dazugehoerige Vorlagebeschluss
  vom 23.07.2020 (ECLI:DE:BGH:2020:230720BIZR143.19.0) gefuehrt; eine
  Preisangaben-Entscheidung unter diesem Aktenzeichen ist dort nicht
  nachweisbar. Zitat daher nicht uebernehmen; Befund geklaert (siehe
  themen/preisangaben.md).

## Siehe auch

- [[themen/preisangaben]]
- [[gesetze/uwg]] — § 3a UWG Rechtsbruch
- [[gesetze/bgb-agb]] — § 312j BGB Button-Loesung
- [[themen/button-loesung]]

## Aenderungsvermerk

- **2026-11-14**: Frontmatter-Datum, Disclaimer-Stand und Hinweis auf die
  letzte Aenderung der PAngV durch Gesetz vom 19.10.2026
  (BGBl. 2026 I Nr. 314) aktualisiert.
- **2026-11-14 (Abgleich)**: Aenderungsinhalt primaer verifiziert
  (recht.bund.de/bgbl/1/2026/314/VO.html). Art. 3 des Gesetzes aendert
  **ausschliesslich § 20 PAngV** (Sanktionsverweis); § 11 (30-Tage-
  Streichpreis), § 4 (Grundpreis), § 6 (Versandkosten) sowie Pfand- und
  Energieangaben sind nicht betroffen. Kern des Artikelgesetzes ist das
  geaenderte Preisangabengesetz (PAngG vom 03.12.1984; durch Art. 1
  geaendert) mit eigenem Bussgeldrahmen bis
  **100.000 EUR** (§ 3 Abs. 3 PAngG). Inkrafttreten 01.01.2027 (Art. 4).
  Vorheriger Hinweis "Betroffenheit einzelner Paragraphen nicht einzeln
  gegenverifiziert" damit aufgeloest.
- **2026-11-14 (Task 12, API-Gegenprobe)**: BGH I ZR 173/16 und BGH I ZR 143/19
  ueber die Rechtsinformations-API des Bundes abgefragt. Beide Treffer
  passen nicht zum hier zugeschriebenen Gegenstand (Preisangaben) — I ZR 173/16
  = "OeKO-TEST I" (Unionsmarke, 12.12.2019), I ZR 143/19 = "Knuspermuesli II"
  (LMIV, 07.04.2022). Zitate werden daher nicht mit Daten/ECLI gefuellt,
  sondern bleiben mit Verifikationsmarker belassen; die Abweichung ist im
  jeweiligen Eintrag dokumentiert.
- **2026-11-14 (Review-Korrekturlauf PR #14)**: Befund zu I ZR 173/16 und
  I ZR 143/19 abschliessend geklaert; Verifikationsmarker in beiden
  Eintraegen entfernt, Verweis auf themen/preisangaben.md (Hinweisblock
  "Nicht zitieren") ergaenzt. Gleichlaut mit preisangaben.md hergestellt.
- **2026-11-14 (Review-Korrekturlauf PR #14, Nachtrag)**: Hinweisblock zu
  den beiden Fehlzitaten unter eine eigene Ueberschrift
  ("Nicht zitieren: falsch zugeordnete Aktenzeichen") ausserhalb von
  "Zitierbare Urteile" verschoben; Inhalt unveraendert. Analog zur
  bestehenden Struktur in themen/preisangaben.md.
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  PAngG als geaendertes Gesetz von 1984; § 1 als Anwendungsbereich, Gesamtpreis
  aus § 3 Abs. 1; Grundpreis-Ausnahmen nach § 4 Abs. 3 (MessEinhG-Bullet und
  "Einzelportionen in Gastronomie" gestrichen); § 12 Preisverzeichnis; OWi nach
  § 20 PAngV mit 25.000 EUR bis 31.12.2026 und 100.000 EUR ab 01.01.2027;
  EuGH C-330/23 inhaltlich berichtigt; Versandkostenhinweis bereits beim
  Angebot (§ 6 PAngV).
- **2026-11-15**: Korrekturen aus doppelter unabhängiger Prüfung (Runde 2):
  Abmahnfaehigkeit ohne "konkretisiert § 1 UKlaG"; fuer § 11 Abs. 1 PAngV
  Beurteilung nach §§ 5a, 5b UWG (BGH I ZR 183/24, LS 2); UVP-Vergleich neutral
  gefasst, Gleichung "(nicht § 11)" gestrichen.
