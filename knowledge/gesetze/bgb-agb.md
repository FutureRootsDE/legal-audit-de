---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/bgb/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/bgb/__305.html
  - https://www.gesetze-im-internet.de/bgb/__309.html
  - https://www.gesetze-im-internet.de/bgb/__312j.html
  - https://www.gesetze-im-internet.de/bgb/__312k.html
  - https://www.gesetze-im-internet.de/bgb/__355.html
  - https://www.gesetze-im-internet.de/bgb/__312g.html
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=LG+Berlin&Datum=16.03.2023&Aktenzeichen=52+O+333%2F22
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=BGH&Datum=09.10.2025&Aktenzeichen=I+ZR+159/24
  - https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2021/2021088.html
verifiziert-am: 2026-10-24
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
> **Stand:** 2026-10-24

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
- einseitigen Leistungsaenderungsvorbehalten, die fuer den anderen
  Vertragsteil nicht zumutbar sind (Nr. 4)
- fingierten Erklaerungen (Nr. 5)
- unangemessen hoher Verguetung oder Aufwendungsersatz bei Ruecktritt oder
  Kuendigung (Nr. 7)

### § 309 BGB — Klauselverbote **ohne** Wertungsmoeglichkeit (HART)

Wichtigste fuer Codebases:

- **Nr. 1** — Preiserhoehungen fuer Leistungen, die binnen vier Monaten nach
  Vertragsschluss zu erbringen sind; gilt nicht fuer Dauerschuldverhaeltnisse
  (z. B. Abos/SaaS; dort Kontrolle nach § 307).
- **Nr. 2** — Ausschluss von Leistungsverweigerungs-/Zurueckbehaltungsrechten.
- **Nr. 3** — Ausschluss des Aufrechnungsrechts bei unbestrittenen/
  rechtskraeftigen Forderungen.
- **Nr. 7** — Haftungsausschluss fuer Verletzung von Leben, Koerper,
  Gesundheit UND fuer grobe Fahrlaessigkeit/Vorsatz ist verboten.
- **Nr. 8 Buchst. b** — bestimmte Beschraenkungen der Maengelrechte bei
  Vertraegen ueber neu hergestellte Sachen und Werkleistungen (aa bis ff).
- **Nr. 9** (fuer ab 01.03.2022 entstandene Schuldverhaeltnisse, Art. 229 § 60
  EGBGB; Gesetz fuer faire Verbrauchervertraege): a) Erstlaufzeit hoechstens
  **zwei Jahre**; b) stillschweigende Verlaengerung nur **auf unbestimmte Zeit**
  mit jederzeitigem Kuendigungsrecht (Frist hoechstens **ein Monat**);
  c) Kuendigungsfrist zum Ende der Erstlaufzeit hoechstens **ein Monat**.
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

**Abs. 3 (Button-Loesung):** "Der Unternehmer hat die Bestellsituation bei einem
Vertrag nach Absatz 2 so zu gestalten, dass der Verbraucher mit seiner Bestellung
**ausdruecklich bestaetigt**, dass er sich zu einer **Zahlung verpflichtet**.
Erfolgt die Bestellung ueber eine Schaltflaeche, ist die Pflicht des Unternehmers
aus Satz 1 nur erfuellt, wenn diese Schaltflaeche gut
lesbar **mit nichts anderem als den Woertern 'zahlungspflichtig bestellen'**
oder mit einer entsprechenden eindeutigen Formulierung beschriftet ist."

**Abs. 4 (Wortlaut, gesetze-im-internet.de):** "Ein Vertrag nach Absatz 2 kommt
nur zustande, wenn der Unternehmer seine Pflicht aus Absatz 3 erfuellt." — Bei
Verstoss gegen Abs. 3 kommt also **kein Vertrag** zustande; der Verbraucher
muss nicht zahlen.

Zulaessige Alternativen laut Gesetzesbegruendung / Rechtsprechung:
"zahlungspflichtigen Vertrag schliessen", "kostenpflichtig bestellen", "kaufen".
**Unzulaessig** sind Beschriftungen, die fuer sich genommen keine Zahlungspflicht
ausdruecken, etwa "Anmelden", "Weiter", "Senden", "Bestellung abschicken" oder
"Bestellung abgeben"; bei Formulierungen wie "Jetzt buchen" kommt es allein auf
die Worte der Schaltflaeche an (EuGH, Urt. v. 07.04.2022, C-249/21), es ist von
hohem Risiko auszugehen. Aktuell
bestaetigt durch **BGH I ZR 159/24, Urt. v. 09.10.2025** (Online-Maklervertrag
ohne "zahlungspflichtig bestellen"-Button ist nach § 312j Abs. 4 BGB endgueltig
unwirksam; ein Neuabschluss durch einseitige Bestaetigung des Verbrauchers
(§ 141 Abs. 1 BGB) ist moeglich, setzt aber selbst die ausdrueckliche
Bestaetigung der Zahlungspflicht nach § 312j Abs. 3 BGB voraus).

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
  notwendigen Umgang mit der Ware (§ 357a Abs. 1 BGB).

**§ 312g BGB — Widerrufsrecht im Fernabsatz:**

**Abs. 1:** "Dem Verbraucher steht bei ausserhalb von Geschaeftsraeumen
geschlossenen Vertraegen und bei Fernabsatzvertraegen ein Widerrufsrecht
gemaess § 355 zu."

**Abs. 2 — Ausnahmen** (Auswahl, mit gesetzlicher Nummerierung):

- **Nr. 1:** Individuell nach Kundenwunsch angefertigte Waren (z.B.
  Konfigurator-Moebel).
- **Nr. 2:** Schnell verderbliche Waren.
- **Nr. 3:** Versiegelte Hygieneartikel nach Oeffnung.
- **Nr. 4:** Waren, die untrennbar mit anderen vermischt wurden.
- **Nr. 6:** Versiegelte Ton-/Video-/Software-Aufzeichnungen nach Oeffnung.
- **Nr. 7:** Zeitungen/Zeitschriften (ausser Abos).

**Erloeschen des Widerrufsrechts (keine Ausnahme nach § 312g Abs. 2):**

- Digitale Inhalte nicht auf koerperlichem Datentraeger: Widerrufsrecht
  erlischt nur bei vorheriger Zustimmung + Hinweis auf Erloeschen + Bestaetigung
  (§ 356 Abs. 6 BGB).
- Dienstleistungen, die vollstaendig erbracht wurden (bei ausdruecklicher
  Zustimmung und Kenntnis; § 356 Abs. 5 BGB).

### § 356a BGB: Widerrufsfunktion (seit 19.06.2026)

Bei ueber eine Online-Benutzeroberflaeche geschlossenen Fernabsatzvertraegen
muss der Unternehmer eine Widerrufsfunktion bereitstellen, gut lesbar mit
**"Vertrag widerrufen"** beschriftet und waehrend der Widerrufsfrist staendig
verfuegbar (Abs. 1). Abzufragen sind Name, Identifikation des Vertrags und
Kommunikationsweg (Abs. 2); es folgt eine Bestaetigungsfunktion **"Widerruf
bestaetigen"** (Abs. 3). Der Unternehmer muss den Eingang unverzueglich auf
einem dauerhaften Datentraeger bestaetigen (Abs. 4).

**Anlage 1 EGBGB** enthaelt das Muster fuer die Widerrufsbelehrung; seine
Verwendung ist freiwillig ("kann", Art. 246a § 1 Abs. 2 Satz 2 EGBGB), erfuellt
bei zutreffender Ausfuellung aber die Informationspflicht. Das
Muster-Widerrufsformular steht in Anlage 2. Seit 19.06.2026 enthaelt Anlage 1 den
Gestaltungshinweis 3 zur Widerrufsfunktion nach § 356a BGB.

Art. 246a § 1 Abs. 2 Nr. 1 EGBGB verlangt jetzt auch Information ueber "das
Bestehen und die Platzierung der Widerrufsfunktion nach § 356a".

## Typische Fallstricke in Codebases

1. **AGB nur per Link im Footer:** § 305 Abs. 2 BGB verlangt einen
   ausdruecklichen Hinweis bei Vertragsschluss, die zumutbare Moeglichkeit der
   Kenntnisnahme und das Einverstaendnis; eine Checkbox ist nicht gesetzlich
   vorgeschrieben, aber ein gaengiges Nachweismittel.
2. **Button mit "Anmelden" / "Weiter":** KLASSISCHER Verstoss gegen § 312j
   Abs. 3 BGB. Nur "zahlungspflichtig bestellen", "kaufen", "kostenpflichtig
   bestellen" sind gerichtsfest.
3. **Widerrufsbelehrung fehlerhaft oder fehlt:** Verlaengerte Widerrufsfrist
   12 Monate + 14 Tage → erheblicher Schaden.
4. **Pre-ticked Marketing-Consent:** Nicht nur DSGVO-, sondern auch AGB-
   widrig: unangemessene Benachteiligung nach § 307 Abs. 1 Satz 1, Abs. 2 Nr. 1
   BGB wegen Abweichung vom gesetzlichen Einwilligungserfordernis (BGH, Urt.
   v. 28.05.2020, I ZR 7/16, Cookie-Einwilligung II).
5. **Automatische Abo-Verlaengerung:** Stillschweigende Verlaengerung nur auf
   unbestimmte Zeit mit Kuendigungsfrist von hoechstens einem Monat (§ 309
   Nr. 9 Buchst. b BGB, fuer ab 01.03.2022 geschlossene Vertraege).
6. **Kuendigungs-Button fehlt:** § 312k Abs. 2 BGB (seit 01.07.2022, auch fuer
   vorher geschlossene Vertraege, Art. 229 § 60 Satz 3 EGBGB) verpflichtet
   Anbieter von Online-Dauerschuldverhaeltnissen zu einem zweistufigen Ablauf: eine
   Kuendigungsschaltflaeche "Vertraege hier kuendigen" fuehrt den Verbraucher
   unmittelbar zu einer Bestaetigungsseite mit den Angaben nach Abs. 2 Satz 3
   Nr. 1 und einer Bestaetigungsschaltflaeche "jetzt kuendigen"; beide staendig
   verfuegbar sowie unmittelbar und leicht zugaenglich. Ausgenommen sind
   Vertraege, deren Kuendigung gesetzlich eine strengere Form als Textform
   verlangt, sowie Webseiten und Vertraege ueber Finanzdienstleistungen (§ 312k
   Abs. 1 Satz 2 BGB). Verstoss: fristlose Kuendigung jederzeit moeglich.
7. **Widerrufsfunktion fehlt:** Seit 19.06.2026 muss bei online geschlossenen
   Fernabsatzvertraegen die Widerrufsfunktion "Vertrag widerrufen" nach § 356a
   BGB bereitstehen.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Subscription-Flow braucht sauberen Button "Jetzt
  kostenpflichtig abonnieren" + Widerrufsbelehrung + Widerrufsfunktion (§ 356a
  BGB, seit 19.06.2026) + Kuendigen-Button-Route.
- **Landingpage:** Ohne Bestellabschluss greift § 312j Abs. 2 bis 4 nicht.
  Eine AGB-Pflicht gibt es nicht; werden AGB verwendet und kommt ueber das
  Formular ein Vertrag zustande, sind sie nach § 305 Abs. 2 BGB einzubeziehen
  und nach § 312i Abs. 1 Satz 1 Nr. 4 BGB abruf- und speicherbar zu machen; bei
  Vertraegen mit Verbrauchern gelten die vorvertraglichen Informationspflichten
  (§ 312d BGB, Art. 246a EGBGB).
- **n8n-Workflows:** Automatische Vertragsbestaetigungs-E-Mails: Bestaetigung
  auf dauerhaftem Datentraeger (E-Mail genuegt, PDF ueblich, nicht
  vorgeschrieben) mit Vertragsinhalt und Angaben nach Art. 246a EGBGB
  einschliesslich Widerrufsbelehrung, soweit nicht schon vorher auf dauerhaftem
  Datentraeger erteilt (§ 312f Abs. 2 BGB); Trigger bei Order-Create.
- **E-Commerce:** Vollstaendige Implementation aller genannten Punkte
  Pflicht. Shopify/WooCommerce-Templates DE haeufig korrekt konfiguriert,
  Custom-Checkouts riskant.
- **Content/Blog:** Im Kommentarbereich und Newsletter-Opt-In keine AGB noetig,
  aber Datenschutzerklaerung + Impressum, soweit das Angebot geschaeftsmaessig
  ist (§ 5 Abs. 1 DDG).

## Behoerden-Hinweise

- **Keine zentrale Aufsicht:** Zivilrechtsweg (Unterlassungsklage durch
  Verbraucherverbaende nach UKlaG) + Abmahnung durch Mitbewerber.
- **vzbv, Verbraucherzentralen:** typische Klaeger gegen unwirksame AGB.

## Zitierbare Urteile

- **BGH, Urt. v. 09.10.2025 — I ZR 159/24**: Ein im elektronischen
  Geschaeftsverkehr geschlossener Maklervertrag ohne ausdrueckliche
  Bestaetigung der Zahlungspflicht ("zahlungspflichtig bestellen"-Schaltflaeche)
  kommt nach § 312j Abs. 3, 4 BGB nicht zustande; auch eine nachtraegliche
  einseitige Bestaetigung fuehrt nicht ohne Weiteres zu einem wirksamen
  Neuabschluss. Wegweisend fuer alle Online-Bestellprozesse mit
  Verbraucherbeteiligung.
- **EuGH, Urt. v. 30.05.2024, C-400/22** ("Conny"): Die Button-Pflicht (Art. 8
  Abs. 2 RL 2011/83/EU, § 312j Abs. 3 BGB) gilt auch, wenn die Zahlungspflicht
  erst bei Eintritt einer weiteren Bedingung entsteht (z. B. erfolgsabhaengiges
  Honorar).
- **BGH, Urt. v. 27.04.2021 — XI ZR 26/20** (PM 88/2021): Klauseln in
  Banken-AGB, die eine fiktive Zustimmung des Kunden zu AGB-Aenderungen ohne
  inhaltliche Begrenzung vorsehen, sind nach § 307 Abs. 1 und 2 BGB
  unwirksam.
- **EuGH, Urt. v. 10.07.2019 — C-649/17** ("Bundesverband / Amazon EU"):
  Onlinehaendler muessen keine Telefonnummer bereitstellen; ausreichend sind
  andere direkte und effiziente Kommunikationsmittel (z. B. Kontaktformular,
  Chat, Rueckrufsystem).
- **LG Berlin 52 O 333/22** (16.03.2023): Auch fuer online bestellte Lebens-
  mittel-Abos/Kochboxen (Marley Spoon) besteht die gesetzliche Pflicht zum
  Kuendigungsbutton nach § 312k BGB; Verstoss loest UWG-Unterlassungsanspruch
  von Verbraucherverbaenden aus. Verifiziert ueber dejure.org und
  vzbv.de/urteile/zum-kuendigungsbutton-bei-marley-spoon.
- Hinweis zur Zitat-Bereinigung (Stand 2026-07-08): Die folgenden Aktenzeichen
  aus einer aelteren Vorgaengerfassung wurden im Update 2026-07-08 entfernt,
  weil sie gegen Tier-1-Quellen nicht verifizierbar waren bzw. thematisch
  nicht passten: "BGH VIII ZR 63/15 (Button 'Jetzt anmelden')" — nicht
  auffindbar; "BGH VIII ZR 21/19 (Widerrufsbelehrung)" — Az. existiert
  (09.10.2019), betrifft aber Mieterhoehung nach Modernisierung, nicht die
  Widerrufsbelehrung; "EuGH C-543/19 Amazon EU" — Az. existiert
  (Urt. v. 15.10.2020, Jebsen & Jessen, Vorlage FG Hamburg, Zoll-/
  Antidumpingrecht), betrifft nicht Amazon; einschlaegig ist EuGH C-649/17
  (10.07.2019);
  "LG Berlin 52 O 157/20 (Kuendigungsbutton)" — Az. so nicht auffindbar
  (das verwandte 52 O 157/21 betrifft Netflix-Preisanpassung, kein
  Kuendigungsbutton). Ersatz siehe LG Berlin 52 O 333/22.

## Siehe auch

- [[gesetze/pangv]] — Preisangaben im Bestellprozess
- [[gesetze/uwg]] — Wettbewerbsrechtliche Flankierung
- [[themen/agb-muster]]
- [[themen/widerrufsbelehrung]]
- [[themen/button-loesung]]
