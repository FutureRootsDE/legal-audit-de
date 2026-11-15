---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/pangv_2022/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/pangv_2022/__11.html
  - https://www.bmwk.de/Redaktion/DE/Artikel/Wirtschaft/preisangabenverordnung.html
  - https://www.wettbewerbszentrale.de/de/themen/preisangaben/
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

# Preisangaben — PAngV 2022 in der Praxis

## Kurz-Ueberblick

Seit **28.05.2022** gilt die neu gefasste Preisangabenverordnung (PAngV).
Wichtigste Praxisaenderung: **§ 11 PAngV** verpflichtet zur Angabe des
**niedrigsten Preises der letzten 30 Tage** als Referenz bei jeder
Bekanntgabe einer Preisermaessigung fuer eine Ware gegenueber Verbrauchern
(nicht fuer Dienstleistungen und digitale Leistungen).

Dazu treten unveraendert:

- Gesamtpreis inkl. USt. (§ 3)
- Grundpreis (§ 4) mit Mengeneinheit nach § 5 Abs. 1 PAngV: je 1 kg / 1 l /
  1 m³ / 1 m / 1 m²
- Versandkosten-Hinweis (§ 6)

Verstoss = Ordnungswidrigkeit nach § 20 PAngV i. V. m. § 3 Abs. 1 Satz 1 Nr. 2
WiStG 1954; Bussgeld bis 31.12.2026 bis zu 25.000 EUR (§ 3 Abs. 2 WiStG
1954), ab 01.01.2027 bis
100.000 EUR (§ 3 Abs. 3 PAngG n. F., BGBl. 2026 I Nr. 314). Daneben
UWG-Abmahnung; bei Verstoessen gegen § 11 PAngV lauterkeitsrechtlich ueber
§§ 5a, 5b UWG, nicht ueber § 3a UWG (BGH I ZR 183/24, Leitsatz 2, zu § 11
PAngV; in Fortfuehrung von I ZR 69/21 zur Grundpreisangabe).

## Schluesselparagraphen / Kernaussagen

### § 11 PAngV — 30-Tage-Streichpreis

**Abs. 1 (Grundregel):** Bei jeder Bekanntgabe einer Preisermaessigung fuer
eine Ware muss der niedrigste Gesamtpreis angegeben werden, den der Haendler
in den **letzten 30 Tagen vor Beginn der Ermaessigung** von Verbrauchern
verlangt hat.

Beispiel:

- Regulaerer Preis: 100 EUR (Tag 1-60)
- Tag 45: Senkung auf 80 EUR fuer 5 Tage
- Tag 50: Zurueck auf 100 EUR
- Tag 65: neue Aktion "20 % Rabatt" → Referenzpreis ist **80 EUR**
  (niedrigster der letzten 30 Tage), nicht 100 EUR.

**Abs. 2 (Progressive Rabatte):** Bei lueckenlosen, schrittweisen
Ermaessigungen (z.B. "Letzte Woche 10 %, jetzt 20 %, bald 30 %") darf
durchgehend der Preis vor Beginn der ersten Ermaessigung als Vergleich genannt
werden.

**Abs. 3:** Regel gilt entsprechend, wenn nur ein Grundpreis anzugeben ist
(lose Ware, § 4 Abs. 2 PAngV).

**Abs. 4 (Ausnahmen):**

- Individuelle Rabatte (Kunden-Geburtstag, 1:1-Coupon)
- Verderbliche Ware bei drohendem Ablauf (wenn klar gekennzeichnet)

### § 3 PAngV — Gesamtpreis

- Endpreis **inkl. USt.** und sonstigen Preisbestandteilen
- Bei Online-Angeboten: neben dem Preis zusaetzliche Angabe, ob Liefer- und
  Versandkosten anfallen und in welcher Hoehe (§ 6)
- "ab X EUR" regelt § 3 PAngV nicht (Praxishinweis ohne Normbezug: "ab"
  deutlich erkennbar und Preisbereich realistisch)

### § 4 PAngV — Grundpreis

Pflicht bei **Fertigpackungen**, offene Packungen, Verkaufseinheiten:

- Mengeneinheit nach § 5 Abs. 1 PAngV: je 1 kg, 1 l, 1 m³, 1 m oder 1 m²
- 100 g oder 100 ml nur bei loser Ware (§ 5 Abs. 2 PAngV)

Ein gesonderter Grundpreis entfaellt, wenn er mit dem Gesamtpreis identisch
ist (§ 4 Abs. 1 Satz 2 PAngV).

Ausnahmen: abschliessend in § 4 Abs. 3 Nr. 1 bis 8 PAngV geregelt.

### § 6 PAngV — Versandkosten

Bei Angeboten zum Abschluss eines Fernabsatzvertrags: Angabe, dass die Preise
die Umsatzsteuer enthalten, und ob zusaetzlich Fracht-, Liefer- oder
Versandkosten anfallen; deren Hoehe, soweit im Voraus berechenbar (§ 6
Abs. 1, 2 PAngV). Pflicht auch bei Versand-Freigrenzen ("ab 50 EUR
versandkostenfrei").

### § 12 PAngV — Dienstleistungen

Preisverzeichnis ueber die wesentlichen Leistungen oder Verrechnungssaetze
am Ort des Leistungsangebots (§ 12 Abs. 1, 2 PAngV).

## Typische Fallstricke in Codebases

1. **Streichpreis ohne History:** Shopsysteme zeigen "UVP 199 EUR" → das ist
   **nicht** die Referenz aus § 11 PAngV. UVP und Streichpreis MUESSEN
   unterscheidbar benannt sein.
2. **Aktions-Kette ohne § 11 Abs. 2 Nachweis:** Ohne lueckenlose Kette darf
   NICHT der Ur-Preis als Vergleich genannt werden.
3. **Vor Black-Friday Preis erhoehen:** Klassisch rechtswidrig ("pseudo-
   Rabatt"). Price-History muss sauber gefuehrt werden.
4. **Grundpreis in Kategorielisten fehlt:** Auch Produktkarten in
   Suchergebnissen benoetigen Grundpreis.
5. **"statt"-Preise bei neuen Produkten:** § 11 Abs. 1 PAngV verbietet
   Streichpreise bei neuen Produkten nicht; wird die Ware seit weniger als
   30 Tagen angeboten, ist der niedrigste Gesamtpreis seit Angebotsbeginn
   anzugeben.
6. **Dynamic Pricing / A/B Tests:** Wenn unterschiedlichen Nutzergruppen
   unterschiedliche Preise angezeigt werden, muss die 30-Tage-Berechnung auf
   **alle** gezeigten Preise zurueckgreifen — nicht nur "der offizielle Preis".
7. **Rabatt-Prozentsatz und Vorteilshervorhebung:** Eine in Prozent oder als
   Werbeaussage bekannt gegebene Ermaessigung ist am 30-Tage-Preis zu
   bemessen (EuGH C-330/23 Aldi Sued, 26.09.2024).
8. **Grundpreis bei Mengenrabatten:** Der Grundpreis bezieht sich auf die
   Mengeneinheit nach § 5 Abs. 1 PAngV (1 kg, 1 l, 1 m³, 1 m, 1 m²), nicht
   auf das Stueck; er bleibt bei Mengenaktionen anzugeben.
9. **Angabe "inkl. MwSt." bei B2B-/Hybrid-Angeboten:** Hinweis zur Angabe bei
   Angeboten, die sich auch an Unternehmer richten. <<VERIFIKATION AUSSTEHEND>>

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Abo-Preise meist keine "Waren" → § 4 nicht relevant;
  § 11 PAngV gilt nur fuer Waren, nicht fuer Dienstleistungen und
  SaaS-Abos. Rabattwerbung fuer Leistungen ("statt 99 EUR, jetzt 79 EUR")
  an § 5 Abs. 2 Nr. 2, Abs. 5 UWG messen.
- **Landingpage:** Bei Aktionspreisen fuer Waren den niedrigsten
  30-Tage-Preis angeben (§ 11 Abs. 1 PAngV); eine Preis-Historie (z. B.
  DB-Tabelle `price_history` mit timestamp, valid_from, valid_to) ist als
  Nachweis dringend zu empfehlen (Beweislast, § 5 Abs. 5 Satz 2 UWG), aber
  keine gesetzliche Pflicht.
- **n8n-Workflows:** Product-Sync-Workflows (Shopify/Shopware) sollten
  Preiseintraege in eine Archiv-Tabelle schreiben. Rabatt-Bestaetigung vor
  Marketing-Versand via DB-Query.
- **E-Commerce:** Shopify "compare_at_price" / Shopware "listPrice" als
  Streichpreis einer Preisermaessigung nur zulaessig, wenn er den niedrigsten
  Gesamtpreis der letzten 30 Tage vor der Ermaessigung wiedergibt (§ 11
  Abs. 1 PAngV); dass der Preis irgendwann in diesen 30 Tagen verlangt
  wurde, genuegt nicht.
- **Content/Blog:** Deal-Portale: Preisvergleiche duerfen nicht irrefuehren
  (§ 5 UWG); Quelle und Zeitpunkt des Vergleichspreises anzugeben ist
  Empfehlung, keine Normpflicht. § 11 PAngV trifft nur, wer selbst zur
  Angabe des Gesamtpreises verpflichtet ist. Haftung bei Affiliates
  eingeschraenkt, aber Mitwirken an Irrefuehrung moeglich.

## Behoerden-Hinweise

- **Gewerbeaufsicht / Marktueberwachung** der Bundeslaender: Ordnungs-
  widrigkeiten nach § 20 PAngV (Bussgeldrahmen siehe Kurz-Ueberblick).
- **Eichbehoerden** (Preis- und Grundpreis-Pruefungen).
- **Wettbewerbszentrale / vzbv:** haeufige Abmahner. Wirtschaftsverbaende
  nur, wenn sie in der Liste nach § 8b UWG eingetragen sind (§ 8 Abs. 3 Nr. 2
  UWG), z. B. die Wettbewerbszentrale; Verbraucherverbaende wie der vzbv als
  qualifizierte Verbraucherverbaende (§ 8 Abs. 3 Nr. 3 UWG). Die aktuelle
  Liste nach § 8b UWG fuehrt das Bundesamt fuer Justiz.

## Zitierbare Urteile

- **BGH, Urteil vom 09.10.2025, I ZR 183/24** ("Jacobs Kroenung",
  ECLI:DE:BGH:2025:091025UIZR183.24.0): Bei Bekanntgabe einer
  Preisermaessigung fuer eine Ware ist der niedrigste Gesamtpreis der letzten
  30 Tage in einer fuer den angesprochenen Verbraucher **eindeutigen, klaren
  und verstaendlichen Weise** anzugeben (§ 11 Abs. 1 i. V. m. § 1 Abs. 3
  Satz 2 PAngV; Leitsatz 1). Verstoesse sind nach §§ 5a, 5b UWG zu
  beurteilen, nicht nach § 3a UWG (Leitsatz 2). (Hinweis, kein Beleg:
  Pressemitteilung des BGH 184/2025.)
- **EuGH C-330/23** (26.09.2024, "Aldi Sued"): Art. 6a Abs. 1, 2 der
  Preisangabenrichtlinie 98/6/EG (nicht UGP-Richtlinie) verlangt, dass eine
  in Prozent oder als Werbeaussage bekannt gegebene Ermaessigung auf
  Grundlage des vorherigen (30-Tage-)Preises berechnet wird.
- **BGH I ZR 49/24** (03.06.2026, "Bearbeitungspauschale II", nach EuGH
  C-62/25 vom 26.03.2026): Pauschale unterhalb eines Mindestbestellwerts
  nicht in den Gesamtpreis einzurechnen, sofern klar angegeben und
  Mindestbetrag die Zahlung nicht praktisch unvermeidbar macht.
- **BGH I ZR 135/20** (26.10.2023, "Flaschenpfand IV", nach EuGH C-543/21):
  Gesamtpreis enthaelt nicht den Pfandbetrag (§ 7 PAngV).
- **OLG Hamm 4 U 85/22** (unzulaessiger Streichpreis ohne 30-Tage-Basis) <<VERIFIKATION AUSSTEHEND>>

### Nicht zitieren — nachweislich falsch zugeordnete Aktenzeichen

- **BGH I ZR 173/16** — in Vorgaengerfassungen als Preisangaben-Entscheidung
  ("auf einen Blick") gefuehrt. Tatsaechlich: Urteil des I. Zivilsenats vom
  **12.12.2019** "ÖKO-TEST I" (Unionsmarken-Verletzung,
  ECLI:DE:BGH:2019:121219UIZR173.16.0). Aktenzeichen nachweislich falsch
  zugeordnet, nicht zitieren; die behauptete Aussage zu Preisangaben ist
  damit unbelegt.
- **BGH I ZR 143/19** — in Vorgaengerfassungen als "Sofort lieferbar"-
  Entscheidung zur Kopplung Lieferzeit/Preis gefuehrt. Tatsaechlich: Urteil
  des I. Zivilsenats vom **07.04.2022** "Knuspermüsli II" (Lebensmittel-
  informations-Pflichten nach LMIV,
  ECLI:DE:BGH:2022:070422UIZR143.19.0). Aktenzeichen nachweislich falsch
  zugeordnet, nicht zitieren; die behauptete Aussage zu Preisangaben ist
  damit unbelegt.
- **BGH I ZR 85/21**: in den amtlichen Datenbanken nicht auffindbar.

## Siehe auch

- [[gesetze/pangv]]
- [[gesetze/uwg]] — § 3a Rechtsbruch, § 5 Irrefuehrung
- [[themen/button-loesung]]

## Aenderungsvermerk 2026-11-14

- Frontmatter-Daten und Disclaimer-Stand auf 2026-11-14.
- Vier Marker-Varianten mit angehaengtem Grund auf das einzeilige
  Standardformat des Verifikationsmarkers normalisiert
  (BGH I ZR 173/16, I ZR 143/19, OLG Hamm 4 U 85/22, BGH I ZR 85/21).
- **2026-11-14 (Review-Korrekturlauf PR #14)**: BGH I ZR 173/16 und
  BGH I ZR 143/19 aus "Zitierbare Urteile" herausgenommen; beide
  Aktenzeichen sind der Preisangaben-Thematik nachweislich falsch
  zugeordnet (I ZR 173/16 = Marke "OeKO-TEST I" 12.12.2019;
  I ZR 143/19 = LMIV "Knuspermuesli II" 07.04.2022). Hinweisblock
  "Nicht zitieren" mit dem tatsaechlichen Verfahrensgegenstand ergaenzt.
  Spiegelbild in gesetze/pangv.md.
- EuGH C-330/23 Aldi Sued und BGH I ZR 183/24 (jeweils 2024/2025) unveraendert
  belassen; weitere Folgerechtsprechung zu § 11 PAngV nicht aufgefunden.
- **2026-11-14 (Task 12, API-Gegenprobe)**: BGH I ZR 173/16 und BGH I ZR 143/19
  ueber die Rechtsinformations-API des Bundes abgefragt. Treffer passen nicht
  zum hier zugeschriebenen Gegenstand (Preisangaben) — I ZR 173/16 =
  "OeKO-TEST I" (Unionsmarke, Urteil 12.12.2019,
  ECLI:DE:BGH:2019:121219UIZR173.16.0); I ZR 143/19 = "Knuspermuesli II"
  (LMIV, Urteil 07.04.2022, ECLI:DE:BGH:2022:070422UIZR143.19.0, dazu
  EuGH-Vorlagebeschluss vom 23.07.2020). Beide Zitate werden daher nicht mit
  Daten/ECLI gefuellt, sondern bleiben mit Verifikationsmarker belassen;
  die Abweichung ist in gesetze/pangv.md spiegelbildlich dokumentiert.
- **2026-11-14 (Abgleich)**: Hinweis auf das Gesetz zur Aenderung des
  Preisangabenrechts vom 19.10.2026 (BGBl. 2026 I Nr. 314, Inkrafttreten
  01.01.2027) ergaenzt. Die Aenderung betrifft die PAngV selbst nur in
  § 20 (Sanktionsverweis); § 11 (30-Tage-Streichpreis), § 4 (Grundpreis)
  und § 6 (Versandkosten) bleiben unveraendert. Das seit 1984 bestehende
  Preisangabengesetz erhaelt einen eigenen Bussgeldtatbestand (bis
  100.000 EUR); § 20 PAngV verweist ab 01.01.2027 darauf statt auf das
  WiStG (berichtigt 2026-11-15, zuvor "neu ... eigenstaendiges PAngG"). Siehe
  [[gesetze/pangv]]. Quelle: recht.bund.de/bgbl/1/2026/314/VO.html.
- **2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1)**:
  Sanktionsnorm § 20 PAngV (statt § 19) mit Bussgeldrahmen ab 01.01.2027
  nach § 3 Abs. 3 PAngG n. F.; Rahmen bis 31.12.2026 mit
  Verifikationsmarker; Lauterkeit bei § 11-Verstoessen ueber §§ 5a, 5b UWG
  (BGH I ZR 183/24, Leitsatz 2); § 11 nur fuer Waren gegenueber
  Verbrauchern (auch im SaaS-Abschnitt); Mengeneinheiten nach § 5 PAngV,
  250-g-Regel gestrichen; Grundpreis-Ausnahmen auf § 4 Abs. 3 PAngV
  verwiesen; § 6, § 11 Abs. 3 und § 12 praezisiert; BGH I ZR 183/24 mit
  Leitsatzwortlaut und ECLI; EuGH C-330/23 auf Art. 6a RL 98/6/EG
  umgestellt, Fallstrick 7 neu gefasst.
- **2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2)**:
  Bussgeldrahmen bis 31.12.2026 nach § 3 Abs. 2 WiStG 1954 (25.000 EUR,
  Marker entfernt); "ab X EUR" als Praxishinweis ohne Normbezug; Fallstricke
  5 und 8, Preis-Historie, compare_at_price und Deal-Portale neu gefasst;
  Plugin-Hinweis und "IDO" gestrichen; BGH I ZR 49/24 und I ZR 135/20
  aufgenommen; BGH I ZR 85/21 als nicht auffindbar nach "Nicht zitieren".
