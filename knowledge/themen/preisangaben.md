---
aktualisiert: 2026-11-14
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
Rabattbewerbung.

Dazu treten unveraendert:

- Gesamtpreis inkl. USt. (§ 3)
- Grundpreis (§ 4) je 1 kg / 1 l / 1 m / 1 m²
- Versandkosten-Hinweis (§ 6)

Verstoss = Bussgeld bis 100.000 EUR (§ 19 PAngV) + UWG-Abmahnung ueber § 3a UWG.

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

**Abs. 3:** Regel gilt entsprechend fuer Grundpreise.

**Abs. 4 (Ausnahmen):**

- Individuelle Rabatte (Kunden-Geburtstag, 1:1-Coupon)
- Verderbliche Ware bei drohendem Ablauf (wenn klar gekennzeichnet)

### § 3 PAngV — Gesamtpreis

- Endpreis **inkl. USt.** und sonstigen Preisbestandteilen
- Bei Online-Angeboten: neben dem Preis zusaetzliche Angabe, ob Liefer- und
  Versandkosten anfallen und in welcher Hoehe (§ 6)
- "ab X EUR" nur zulaessig, wenn "ab" deutlich erkennbar und Preisbereich
  realistisch

### § 4 PAngV — Grundpreis

Pflicht bei **Fertigpackungen**, offene Packungen, Verkaufseinheiten:

- Waren nach Gewicht: je 1 kg / 100 g (bei < 250 g)
- Fluessige: je 1 l / 100 ml
- Laenge: je 1 m
- Flaeche: je 1 m²

Ausnahmen:

- Gastronomie
- Waren unter 10 g/10 ml
- gleiche Nenn- und Fuellmengen (MessEinhG-Anlagen)

### § 6 PAngV — Versandkosten

Bei elektronischem Geschaeftsverkehr: Hinweis vor Vertragsabschluss, dass und
in welcher Hoehe zusaetzliche Kosten anfallen. Pflicht auch bei
Versand-Freigrenzen ("ab 50 EUR versandkostenfrei").

### § 12 PAngV — Dienstleistungen

Bei DL gelten entsprechende Pflichten: entweder Festpreis oder Preisliste
(Stundensatz + Pauschalen).

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
5. **"statt"-Preise bei neuen Produkten:** Neue Produkte ohne 30-Tage-Historie
   koennen keinen Streichpreis haben.
6. **Dynamic Pricing / A/B Tests:** Wenn unterschiedlichen Nutzergruppen
   unterschiedliche Preise angezeigt werden, muss die 30-Tage-Berechnung auf
   **alle** gezeigten Preise zurueckgreifen — nicht nur "der offizielle Preis".
7. **"Unser Preis" vs. "Mindestpreis 30 Tage":** Bei Kombination von UVP-
   Vergleich UND § 11-Angabe Transparenz gefordert (EuGH C-330/23 Aldi Sued,
   26.09.2024).
8. **Grundpreis bei Mengenrabatten:** Kauf 3 zahle 2 → Grundpreis je Stueck
   bleibt angegeben.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Abo-Preise meist keine "Waren" → § 4 nicht relevant; aber
  § 11 gilt auch fuer DL-Preisreduzierungen ("statt 99 EUR, jetzt 79 EUR") ueber
  § 12.
- **Landingpage:** Bei Aktion-Pricing "50 % statt 100 EUR" Price-Log-Endpoint
  (DB-Tabelle `price_history` mit timestamp, valid_from, valid_to) Pflicht.
- **n8n-Workflows:** Product-Sync-Workflows (Shopify/Shopware) sollten
  Preiseintraege in eine Archiv-Tabelle schreiben. Rabatt-Bestaetigung vor
  Marketing-Versand via DB-Query.
- **E-Commerce:** Shopify "compare_at_price" oder Shopware "listPrice" =
  rechtlich nur dann OK, wenn Preis tatsaechlich binnen 30 Tagen verlangt
  wurde. Plugin-Ecosystem (z.B. Trusted Shops PriceGuard) verfuegbar.
- **Content/Blog:** Deal-Portale muessen Vergleichspreis korrekt deklarieren,
  Quelle + Timestamp nennen; Haftung bei Affiliates eingeschraenkt, aber
  Mitwirken an Irrefuehrung moeglich.

## Behoerden-Hinweise

- **Gewerbeaufsicht / Marktueberwachung** der Bundeslaender: Ordnungs-
  widrigkeiten gemaess § 19 PAngV — bis 100.000 EUR.
- **Eichbehoerden** (Preis- und Grundpreis-Pruefungen).
- **Wettbewerbszentrale / vzbv / IDO** — haeufige Abmahner.

## Zitierbare Urteile

- **BGH I ZR 183/24** (09.10.2025, "Streichpreis-Werbung"): NEU — Werbung
  mit einer Preisermaessigung ist unlauter, wenn der niedrigste Gesamtpreis
  der letzten 30 Tage **nicht eindeutig, klar erkennbar und gut lesbar**
  angegeben wird. (Quelle: bundesgerichtshof.de Pressemitteilung 184/2025).
- **EuGH C-330/23** (26.09.2024, "Aldi Sued"): Der Referenzpreis nach § 11
  PAngV / Art. 6a UGP-Richtlinie muss sich auch in **Werbemassnahmen**
  (Prospekte, Online-Ads) auf den 30-Tage-Tiefstpreis beziehen, nicht nur am
  Regal.
- **OLG Hamm 4 U 85/22** (unzulaessiger Streichpreis ohne 30-Tage-Basis) <<VERIFIKATION AUSSTEHEND>>
- **BGH I ZR 85/21** (Angabe "inkl. MwSt." bei B2B-/Hybrid-Angeboten) <<VERIFIKATION AUSSTEHEND>>

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
  und § 6 (Versandkosten) bleiben unveraendert. Neu ist das eigenstaendige
  Preisangabengesetz (PAngG) mit Bussgeldrahmen bis 100.000 EUR, in das
  die bisher im WiStG geregelte Sanktionsnorm verlagert wird. Siehe
  [[gesetze/pangv]]. Quelle: recht.bund.de/bgbl/1/2026/314/VO.html.
