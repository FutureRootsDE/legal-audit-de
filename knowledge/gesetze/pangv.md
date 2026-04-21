---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/pangv_2022/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/pangv_2022/__11.html
  - https://www.bmwk.de/Redaktion/DE/Artikel/Wirtschaft/preisangabenverordnung.html
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

# PAngV 2022 — Preisangabenverordnung (Neufassung)

## Kurz-Ueberblick

Die Preisangabenverordnung (PAngV) regelt, wie Unternehmen gegenueber Verbrauchern
Preise auszuzeichnen haben. Die **Neufassung trat am 28.05.2022 in Kraft**
(Umsetzung der EU-Omnibus-Richtlinie 2019/2161). Wichtigste Neuerung: § 11
PAngV mit der **30-Tage-Streichpreis-Regel**.

Die PAngV konkretisiert § 1 UKlaG / §§ 3, 5, 5a UWG und ist ueber § 3a UWG
(Rechtsbruch) wettbewerbsrechtlich abmahnfaehig.

## Schluesselparagraphen / Kernaussagen

### § 1 PAngV — Anwendungsbereich, Grundsatz

Wer Verbrauchern Waren oder Dienstleistungen anbietet oder als Anbieter
adressiert Werbung unter Angabe von Preisen betreibt, muss Gesamtpreise angeben
(inkl. USt. und aller sonstigen Preisbestandteile).

### § 3 PAngV — Pflicht zur Angabe des Gesamtpreises

"Gesamtpreis" = Endpreis einschliesslich Umsatzsteuer und sonstiger
Preisbestandteile. Fuer Versandhandel: zusaetzlich Hinweis, ob Liefer- und
Versandkosten anfallen und in welcher Hoehe (§ 6 PAngV).

### § 4 PAngV — Grundpreisangabe

Wer Waren in Fertigpackungen, offenen Packungen oder als Verkaufseinheiten ohne
Umhuellung **nach Gewicht, Volumen, Laenge oder Flaeche** anbietet, muss
neben dem Gesamtpreis auch den **Grundpreis** (je 1 kg / 1 l / 1 m / 1 m²)
angeben.

Ausnahmen u.a. fuer:

- Waren, deren Nenngewicht/-volumen in §§ 4-6 MessEinhG-Anlage geregelt ist
  (z.B. Aerosol-Deodorants in Gramm)
- Waren < 10 g/10 ml
- Einzelportionen in Gastronomie

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

Preisangabe fuer Dienstleistungen (Handwerker, Friseur, Steuerberater etc.):
entweder Festpreis oder nach Preisverzeichnis / Stundensatz.

## Typische Fallstricke in Codebases

1. **Hardcoded Streichpreise ohne Audit-Trail:** Der "999 EUR statt 1999 EUR"-
   Rabatt muss als **UVP-Vergleich** (nicht § 11) ODER **Streichpreis aus
   30-Tage-Historie** (§ 11) klar gekennzeichnet werden. Ohne DB-Historie
   unmoeglich zu rechtfertigen.
2. **Black-Friday-Pseudo-Rabatte:** Preise kurz vor Aktion erhoehen, dann
   "reduzieren" ist klassischer Verstoss.
3. **Dynamic Pricing (A/B Test):** Wenn Preis B an einige User getestet wird,
   kann "niedrigster Preis der 30 Tage" aus B-Cohort resultieren — Streichpreis
   muss sich daran orientieren.
4. **Grundpreis fehlt in Produktkachel:** Suchergebnislisten, Kategorieseiten,
   Social-Ads muessen Grundpreis enthalten, wenn § 4 greift.
5. **Versandkosten-Hinweis zu spaet im Checkout:** Gesamtpreis inkl.
   Versandinfo muss **vor** Bestellabschluss sichtbar sein (§ 6 PAngV;
   flankiert von § 312j Abs. 2 BGB).
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
  widrigkeiten nach § 19 PAngV bis **100.000 EUR Bussgeld**.
- **Abmahnungen:** regelmaessig durch Wettbewerbszentrale, IDO, vzbv.

## Zitierbare Urteile

- **OLG Hamburg 3 U 37/22** zur 30-Tage-Regel und E-Commerce-Streichpreisen
  `<<VERIFIKATION AUSSTEHEND — Aktenzeichen / Datum bitte pruefen>>`
- **EuGH C-330/23** (26.09.2024, "Aldi Sued"): Klarstellung, dass der
  30-Tage-Referenzpreis auch in Werbung (Prospekte, Online-Ads) gelten muss,
  nicht nur am Regal.
- **BGH I ZR 173/16** (31.10.2018): Preisangabe muss fuer den Verbraucher
  "auf einen Blick" erkennbar sein.
- **BGH I ZR 143/19** (05.11.2020, "Sofort lieferbar"): Kopplung Lieferzeit +
  Preisangabe.

## Siehe auch

- [[themen/preisangaben]]
- [[gesetze/uwg]] — § 3a UWG Rechtsbruch
- [[gesetze/bgb-agb]] — § 312j BGB Button-Loesung
- [[themen/button-loesung]]
