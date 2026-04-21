---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/bgb/__312j.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/bgb/__312k.html
  - https://www.bmj.de/DE/themen/verbraucherrecht/faire_vertraege/
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# Button-Loesung — § 312j Abs. 3/4 BGB

## Kurz-Ueberblick

Seit dem **01.08.2012** gilt die **Button-Loesung**: Wer Verbrauchern online
entgeltliche Bestellungen ermoeglicht, muss den finalen "Kaufen"-Button
**ausdruecklich und eindeutig** als zahlungspflichtigen Schritt kennzeichnen.

**Gesetzestext § 312j Abs. 3 BGB:** Die Schaltflaeche muss "gut lesbar mit
nichts anderem als den Woertern '**zahlungspflichtig bestellen**' oder mit
einer entsprechenden eindeutigen Formulierung beschriftet" sein.

**Rechtsfolge bei Verstoss (§ 312j Abs. 4 BGB):** Es **kommt kein Vertrag
zustande**. Der Verbraucher muss nicht zahlen und kann Leistung dennoch
verlangen (str.), jedenfalls erhaelt er keine Pflicht zur Gegenleistung.

## Schluesselparagraphen / Kernaussagen

### § 312j Abs. 2 BGB — Transparenzpflichten VOR dem Button

Unmittelbar bevor der Verbraucher seine Bestellung abgibt, muss der
Unternehmer klar und verstaendlich **hervorgehoben** bereitstellen:

- wesentliche Merkmale der Ware/Dienstleistung
- Gesamtpreis inkl. Steuern und Abgaben
- ggf. Liefer- und Versandkosten
- Laufzeit / Mindestlaufzeit / Kuendigungsbedingungen

Diese "Kontroll-Seite" / "Bestellzusammenfassung" muss zwingend VOR dem
Button kommen.

### § 312j Abs. 3 BGB — Button-Beschriftung

"Erfolgt die Bestellung ueber eine Schaltflaeche, ist die Pflicht des
Unternehmers aus Satz 1 nur erfuellt, wenn diese Schaltflaeche gut lesbar mit
nichts anderem als den Woertern **'zahlungspflichtig bestellen'** oder mit
einer entsprechenden eindeutigen Formulierung beschriftet ist."

**Zulaessige Alternativen (laut Rechtsprechung / Literatur):**

- "zahlungspflichtig bestellen" (gesetzeswortlaut)
- "kostenpflichtig bestellen"
- "kaufen" (BGH VIII ZR 63/15 2017, wenn Gesamtkontext unmissverstaendlich)
- "zahlungspflichtigen Vertrag schliessen"
- "Jetzt kaufen" (Tendenz: OK)
- "Kostenpflichtig bestellen"

**Unzulaessig** (laut Rechtsprechung):

- "Anmelden"
- "Weiter"
- "Weiter zur Bezahlung"
- "Bestellung abschicken"
- "Bestellung abgeben" (umstritten, Tendenz: unzulaessig)
- "Jetzt anmelden" (BGH VIII ZR 63/15)
- "Bestellen" (alleine)
- "Buchen"
- "Auftrag erteilen"

### § 312j Abs. 4 BGB — Rechtsfolge

"Ein Vertrag [...] kommt nur zustande, wenn der Unternehmer seine Pflicht aus
Absatz 3 erfuellt." → **Vertrag unwirksam**, Verbraucher zahlt nicht, hat aber
Anspruch auf Ausgleich erhaltener Leistungen (§ 812 BGB Bereicherungsrecht).

### § 312k BGB — Kuendigungs-Button (seit 01.07.2022)

Analog zur Button-Loesung fuer Vertragsabschluss **muessen Anbieter von
Dauerschuldverhaeltnissen** (Abos, SaaS, Telko, Streaming) einen **"Vertrage
hier kuendigen"-Button** gut sichtbar einbauen. Der Button fuehrt zu einer
Bestaetigungsseite mit allen Pflichtangaben; nach Klick wird die Kuendigung
sofort bestaetigt (Textform).

Verstoss → Verbraucher kann **jederzeit fristlos** kuendigen (§ 312k Abs. 6).

## Typische Fallstricke in Codebases

1. **"Anmelden" / "Registrieren" als Finaler-Button** bei SaaS-Paid-Plans:
   klassischer Verstoss. Must be: "Kostenpflichtig abonnieren" /
   "zahlungspflichtig bestellen".
2. **Stripe-Checkout-Default-Button** "Pay" / "Bezahlen": gerichtsfest
   meistens OK; dennoch pruefen, ob deutscher Kontext konfiguriert ist.
3. **Icons ohne Text** ("Shopping-Cart"-Icon): nicht gut lesbar → Verstoss.
4. **Zusaetzliche Woerter neben Button** ("Jetzt zahlungspflichtig bestellen
   und Bonus sichern"): "nichts anderes als" → Verstoss.
5. **Bestellzusammenfassung nach Button:** Fatal. Abs. 2 verlangt Summary
   VOR Button.
6. **Upsell-Flow**: Jeder zusaetzliche Kauf braucht eigenen
   Button-Loesung-konformen Schritt.
7. **Mobile-Viewport** Button abgeschnitten oder verdeckt durch Sticky-
   Footer: nicht "gut lesbar".
8. **Double-Submit-Prevention:** Klick soll nicht mehrfach auswerten; aber
   technisches Detail, rechtlich irrelevant.
9. **Kuendigungs-Button nach Login versteckt** (§ 312k): Button muss
   unmittelbar aufrufbar sein, Authentifizierung ist zulaessig, muss aber
   niedrigschwellig bleiben.
10. **SaaS-Upgrades innerhalb App:** Jeder kostenpflichtige Upgrade-Button
    braucht seine eigene Button-Loesung.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Checkout-Page muss Summary-Section + Final-Button
  "Kostenpflichtig abonnieren" als primary Button. Kuendigen-Button auf
  Account-Settings-Page prominent.
- **Landingpage:** Nur relevant, wenn Verkauf direkt ohne separaten Checkout
  stattfindet (One-Click-Buy).
- **n8n-Workflows:** n8n-Forms werden **nicht** direkt fuer B2C-Verkaufs-
  abschluss verwendet — aber wenn Embedded in Shop, muss Integration-Flow
  die Button-Pflicht erfuellen.
- **E-Commerce:** Kernfunktion; alle gaengigen Shop-Systeme DE-konfiguriert
  korrekt. Custom-Checkouts pruefen.
- **Content/Blog:** Relevant bei kostenpflichtigem Content-Zugang (Paywall).

## Behoerden-Hinweise

- Keine zentrale Aufsicht; Abmahnung durch Wettbewerbsverbaende.
- Verbraucher koennen Zahlungen zurueckverlangen / nicht zahlen und auf
  § 312j Abs. 4 berufen.

## Zitierbare Urteile

- **BGH VIII ZR 63/15** (19.07.2017): "Jetzt anmelden" nicht ausreichend.
- **BGH VIII ZR 99/19** (04.11.2020): "Buchen" ebenfalls nicht ausreichend,
  wenn unklar bleibt, ob entgeltlich.
- **OLG Koeln 6 U 102/12** (10.05.2013): Fruehe Praezisierung zu
  Button-Labels.
- **EuGH C-249/21** (07.04.2022, "Fuhrmann-2"): Der Button-Text muss "aus
  sich heraus" die Zahlungsverpflichtung erkennbar machen; Gesamtumstaende
  reichen nicht.
- **LG Berlin 52 O 157/20** zu § 312k (Kuendigungs-Button)
  `<<VERIFIKATION AUSSTEHEND — Aktenzeichen/Datum pruefen>>`.

## Siehe auch

- [[gesetze/bgb-agb]] — § 312j BGB Text
- [[themen/widerrufsbelehrung]]
- [[themen/agb-muster]]
- [[themen/preisangaben]]
