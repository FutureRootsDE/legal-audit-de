---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/bgb/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/bgb/__305.html
  - https://www.gesetze-im-internet.de/bgb/__309.html
  - https://www.gesetze-im-internet.de/bgb/__312j.html
  - https://www.gesetze-im-internet.de/bgb/__355.html
  - https://www.gesetze-im-internet.de/bgb/__312g.html
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

# BGB — AGB-Recht, Button-Loesung, Widerruf

## Kurz-Ueberblick

Dieses Dokument behandelt die drei fuer Online-Codebases zentralen Bloecke des
Buergerlichen Gesetzbuchs:

1. **§§ 305-310 BGB** — AGB-Kontrolle (Einbeziehung, Inhalts-/Transparenzkontrolle)
2. **§ 312j BGB** — Fernabsatz-Informationspflichten + "Button-Loesung"
3. **§§ 355-361 BGB** — Widerrufsrecht (14-Tage-Frist, Muster, Rechtsfolgen)

Diese Normen ergaenzen die speziellen Anforderungen der PAngV, UWG und DSGVO.

## Schluesselparagraphen / Kernaussagen

### § 305 BGB — Einbeziehung von AGB

**Abs. 1:** AGB sind "alle fuer eine Vielzahl von Vertraegen vorformulierten
Vertragsbedingungen, die eine Vertragspartei (Verwender) der anderen
Vertragspartei bei Abschluss eines Vertrags stellt". Irrelevant, ob sie aeusserlich
getrennt oder Vertragsbestandteil sind.

Keine AGB, soweit die Bedingungen im Einzelnen **ausgehandelt** wurden.

**Abs. 2 — Einbeziehungsvoraussetzungen (B2C):**

1. Ausdruecklicher Hinweis des Verwenders auf die AGB oder deutlich sichtbarer
   Aushang am Ort des Vertragsschlusses.
2. Moeglichkeit der zumutbaren Kenntnisnahme (vor Vertragsschluss lesbar).
3. Einverstaendnis der anderen Partei mit der Geltung der AGB.

**Abs. 3:** Rahmenvereinbarungen fuer bestimmte Arten von Rechtsgeschaeften
zulaessig.

### § 305c BGB — Ueberraschungsklauseln

Bestimmungen, die "nach den Umstaenden, insbesondere nach dem aeusseren
Erscheinungsbild des Vertrags, so ungewoehnlich sind, dass der Vertragspartner
des Verwenders mit ihnen nicht zu rechnen braucht," werden **nicht Vertrags-
bestandteil**. Zweifel gehen zu Lasten des Verwenders.

### § 307 BGB — Inhaltskontrolle / Generalklausel

AGB sind unwirksam, wenn sie den Vertragspartner **entgegen Treu und Glauben
unangemessen benachteiligen**. Dazu gehoert insbesondere Intransparenz
(§ 307 Abs. 1 Satz 2 BGB).

### § 308 BGB — Klauselverbote **mit** Wertungsmoeglichkeit

Enthaelt u.a. Verbote von:

- uebermaessig langen Annahme-/Leistungsfristen (Nr. 1)
- einseitigen Leistungsaenderungsrechten ohne sachlichen Grund (Nr. 4)
- fingierten Erklaerungen (Nr. 5)
- kurzen Ruecksendefristen bei Ruecktritt

### § 309 BGB — Klauselverbote **ohne** Wertungsmoeglichkeit (HART)

Wichtigste fuer Codebases:

- **Nr. 1** — Preiserhoehungen binnen 4 Monaten nach Vertragsschluss unzulaessig.
- **Nr. 2** — Ausschluss von Leistungsverweigerungs-/Zurueckbehaltungsrechten.
- **Nr. 3** — Ausschluss des Aufrechnungsrechts bei unbestrittenen/
  rechtskraeftigen Forderungen.
- **Nr. 7** — Haftungsausschluss fuer Verletzung von Leben, Koerper,
  Gesundheit UND fuer grobe Fahrlaessigkeit/Vorsatz ist verboten.
- **Nr. 8b** — Beschraenkung von Maengelrechten (Gewaehrleistung) ist
  unzulaessig.
- **Nr. 9** — Vertragslaufzeit > 2 Jahre, automatische Verlaengerung > 1 Jahr,
  Kuendigungsfrist > 3 Monate bei Dauerschuldverhaeltnissen = unzulaessig.
  **Seit 01.03.2022** (Gesetz fuer faire Verbrauchervertraege) gilt zusaetzlich:
  Nach Ablauf der Erstlaufzeit duerfen Vertraege nur noch **auf unbestimmte
  Zeit** verlaengert werden, Kuendigungsfrist max. **1 Monat**.
- **Nr. 13** — Formerfordernisse strenger als Textform (z.B. Schriftform
  fuer Kuendigung) sind unzulaessig. **Seit 01.10.2016** ist fuer AGB nur
  Textform zulaessig.

### § 312j BGB — Pflichten bei Fernabsatz / "Button-Loesung"

**Abs. 2:** Im elektronischen Geschaeftsverkehr muss der Unternehmer dem
Verbraucher **unmittelbar bevor** dieser seine Bestellung abgibt, folgende
Infos klar und verstaendlich, hervorgehoben bereitstellen:

- wesentliche Merkmale der Ware/DL
- Gesamtpreis inkl. Steuern und Abgaben
- alle zusaetzlichen Kosten (Versand)
- ggf. Laufzeit / Mindestlaufzeit / Kuendigungsbedingungen

**Abs. 3 (Button-Loesung):** "Der Unternehmer hat die Bestellsituation so zu
gestalten, dass der Verbraucher mit seiner Bestellung **ausdruecklich bestaetigt**,
dass er sich zu einer **Zahlung verpflichtet**. Erfolgt die Bestellung ueber
eine Schaltflaeche, ist die Pflicht nur erfuellt, wenn diese Schaltflaeche gut
lesbar **mit nichts anderem als den Woertern 'zahlungspflichtig bestellen'**
oder mit einer entsprechenden eindeutigen Formulierung beschriftet ist."

**Abs. 4:** Verstoesst der Unternehmer gegen Abs. 3, **kommt KEIN Vertrag
zustande**. Der Verbraucher muss nicht zahlen.

Zulaessige Alternativen laut BGH: "zahlungspflichtigen Vertrag schliessen",
"kostenpflichtig bestellen", "kaufen". **Unzulaessig:** "Anmelden", "Weiter",
"Bestellung abschicken", "Jetzt buchen", "Bestellung abgeben" (BGH
VIII ZR 63/15).

### §§ 355-361 BGB — Widerrufsrecht

**§ 355 BGB — Widerruf allgemein:**

- **Abs. 1:** Widerruf erfolgt durch **eindeutige Erklaerung** des Widerrufswillens
  gegenueber dem Unternehmer. Keine Begruendung erforderlich. Rechtzeitige
  Absendung genuegt.
- **Abs. 2:** **Widerrufsfrist = 14 Tage**. Beginn: Vertragsschluss, soweit
  nichts anderes bestimmt.

**§ 356 BGB — Widerruf bei Fernabsatz:**

- Frist beginnt mit Erhalt der Ware (bei Warenkauf) bzw. Vertragsschluss (DL).
- Fehlt die Widerrufsbelehrung, verlaengert sich die Frist auf **12 Monate + 14 Tage**.

**§ 357 BGB — Rechtsfolgen:**

- Rueckgewaehr binnen 14 Tagen nach Widerruf (beiderseits).
- Unternehmer muss dasselbe Zahlungsmittel verwenden wie Verbraucher.
- Bei Waren: Unternehmer kann Rueckzahlung zurueckhalten, bis Ware zurueck.
- Verbraucher traegt Rueckversandkosten NUR, wenn darueber belehrt wurde.
- **Wertersatz** nur bei Wertverlust durch einen nicht zur Pruefung
  notwendigen Umgang mit der Ware.

**§ 312g BGB — Widerrufsrecht im Fernabsatz:**

**Abs. 1:** "Dem Verbraucher steht bei ausserhalb von Geschaeftsraeumen
geschlossenen Vertraegen und bei Fernabsatzvertraegen ein Widerrufsrecht
gemaess § 355 zu."

**Abs. 2 — Ausnahmen** (nicht erschoepfend):

1. Individuell nach Kundenwunsch angefertigte Waren (z.B. Konfigurator-Moebel).
2. Schnell verderbliche Waren.
3. Versiegelte Hygieneartikel nach Oeffnung.
4. Waren, die untrennbar mit anderen vermischt wurden.
5. Versiegelte Ton-/Video-/Software-Aufzeichnungen nach Oeffnung.
6. Zeitungen/Zeitschriften (ausser Abos).
7. Digitale Inhalte nicht auf koerperlichem Datentraeger: Widerrufsrecht
   erlischt nur bei vorheriger Zustimmung + Hinweis auf Erloeschen + Bestaetigung
   (§ 356 Abs. 5 BGB).
8. Dienstleistungen, die vollstaendig erbracht wurden (bei ausdruecklicher
   Zustimmung und Kenntnis).

**Anlage 1 EGBGB** enthaelt das verbindliche **Musterwiderrufsbelehrungs-Formular**,
das bei korrekter Verwendung eine **Schutzwirkung** (Gesetzlichkeitsfiktion)
entfaltet.

## Typische Fallstricke in Codebases

1. **AGB nur per Link im Footer:** Checkbox "Ich akzeptiere AGB" mit anklickbarem
   Link erforderlich — § 305 Abs. 2 BGB. Linktext "AGB" reicht nicht, besser:
   Checkbox mit Link zur PDF/Unterseite.
2. **Button mit "Anmelden" / "Weiter":** KLASSISCHER Verstoss gegen § 312j
   Abs. 3 BGB. Nur "zahlungspflichtig bestellen", "kaufen", "kostenpflichtig
   bestellen" sind gerichtsfest.
3. **Widerrufsbelehrung fehlerhaft oder fehlt:** Verlaengerte Widerrufsfrist
   12 Monate + 14 Tage → erheblicher Schaden.
4. **Pre-ticked Marketing-Consent:** Nicht nur DSGVO-, sondern auch AGB-
   widrig (§ 307 BGB Transparenz).
5. **Automatische Abo-Verlaengerung > 1 Monat:** Seit dem "Gesetz fuer faire
   Verbrauchervertraege" (01.03.2022) unzulaessig.
6. **Kuendigungs-Button fehlt:** § 312k BGB verpflichtet Anbieter von Online-
   Dauerschuldverhaeltnissen zu einem "Kuendigen-Button", der direkt zur
   Kuendigung fuehrt. Verstoss: fristlose Kuendigung jederzeit moeglich.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Subscription-Flow braucht sauberen Button "Jetzt
  kostenpflichtig abonnieren" + Widerrufsbelehrung + Kuendigen-Button-Route.
- **Landingpage:** Kein Kaufabschluss → § 312j irrelevant, aber AGB-Pflicht
  bei Anfrageformularen, wenn Vertragsschluss moeglich.
- **n8n-Workflows:** Automatische Vertragsbestaetigungs-E-Mails muessen
  Widerrufsbelehrung + AGB als PDF-Anhang enthalten; Trigger bei Order-Create.
- **E-Commerce:** Vollstaendige Implementation aller genannten Punkte
  Pflicht. Shopify/WooCommerce-Templates DE haeufig korrekt konfiguriert,
  Custom-Checkouts riskant.
- **Content/Blog:** Im Kommentarbereich und Newsletter-Opt-In keine AGB noetig,
  aber Datenschutzerklaerung + Impressum.

## Behoerden-Hinweise

- **Keine zentrale Aufsicht:** Zivilrechtsweg (Unterlassungsklage durch
  Verbraucherverbaende nach UKlaG) + Abmahnung durch Mitbewerber.
- **vzbv, Verbraucherzentralen:** typische Klaeger gegen unwirksame AGB.

## Zitierbare Urteile

- **BGH VIII ZR 63/15** (19.07.2017): Button-Beschriftung "Jetzt anmelden"
  reicht NICHT fuer § 312j Abs. 3.
- **BGH VIII ZR 21/19** (08.12.2020): Widerrufsbelehrung muss den Beginn der
  Frist eindeutig benennen.
- **EuGH C-543/19** "Amazon EU": Information zur Identitaet des Haendlers muss
  bei Marketplace-Verkaeufen gegeben sein.
- **BGH XI ZR 26/20** (03.11.2020): Unwirksamkeit einer Klausel zur
  automatischen Zustimmung zu AGB-Aenderungen.
- **EuGH C-649/17** (10.07.2019, "Amazon EU"): Kontaktmoeglichkeiten im
  Fernabsatz — Telefon nicht zwingend, aber gleichwertige Alternativen noetig.
- **LG Berlin 52 O 157/20** zu § 312k BGB Kuendigungs-Button.

## Siehe auch

- [[gesetze/pangv]] — Preisangaben im Bestellprozess
- [[gesetze/uwg]] — Wettbewerbsrechtliche Flankierung
- [[themen/agb-muster]]
- [[themen/widerrufsbelehrung]]
- [[themen/button-loesung]]
