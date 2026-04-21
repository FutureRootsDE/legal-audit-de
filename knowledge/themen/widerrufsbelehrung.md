---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/egbgb/anlage_1.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/bgb/__355.html
  - https://www.gesetze-im-internet.de/bgb/__312g.html
  - https://www.gesetze-im-internet.de/bgb/__356.html
  - https://www.gesetze-im-internet.de/bgb/__357.html
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

# Widerrufsbelehrung — 14-Tage-Frist, Muster, Ausnahmen

## Kurz-Ueberblick

Verbraucher haben bei **Fernabsatzvertraegen** (Online-Shops, Apps, SaaS) und
bei **ausserhalb von Geschaeftsraeumen geschlossenen Vertraegen** ein
**14-taegiges Widerrufsrecht** (§§ 312g, 355 BGB).

Die Widerrufsbelehrung muss den gesetzlichen Anforderungen entsprechen —
sicherster Weg: **Muster-Widerrufsbelehrung nach Anlage 1 EGBGB** + Muster-
Widerrufsformular nach Anlage 2 EGBGB ("Gesetzlichkeitsfiktion").

Fehlt die Belehrung → Widerrufsfrist verlaengert sich auf **12 Monate + 14 Tage**
(§ 356 Abs. 3 BGB).

## Schluesselparagraphen / Kernaussagen

### § 355 BGB — Widerrufsrecht allgemein

**Abs. 1:** Widerruf durch **eindeutige Erklaerung** des Willens. Keine
Begruendung. Rechtzeitige **Absendung** genuegt zur Fristwahrung.

**Abs. 2:** **14 Tage** Frist, Beginn mit Vertragsschluss (soweit nichts
anderes gilt).

### § 356 BGB — Besondere Fristregelung fuer Fernabsatz

- **Abs. 2 Nr. 1:** Beim Warenkauf beginnt die Frist erst, wenn der
  Verbraucher die Ware erhalten hat.
- **Abs. 2 Nr. 2:** Bei mehreren Waren, Teillieferungen, wiederkehrender
  Lieferung gelten abweichende Startzeitpunkte.
- **Abs. 3:** Frist beginnt erst mit **ordnungsgemaesser Belehrung**. Ohne
  Belehrung erlischt Widerrufsrecht spaetestens **12 Monate + 14 Tage** nach
  Fristbeginn.

### § 312g Abs. 2 BGB — Ausnahmen vom Widerrufsrecht

Kein Widerrufsrecht u.a. bei:

1. **individuell angefertigten Waren** (Konfigurator, personalisiert)
2. schnell verderblichen Waren
3. **versiegelten Hygieneartikeln** nach Oeffnung (Masken, Kosmetik)
4. untrennbar mit anderen Waren vermischt
5. **versiegelter Software / DVD / Musik** nach Oeffnung
6. Zeitungen / Zeitschriften (ausser Abos)
7. **digitale Inhalte** ohne koerperlichen Traeger — Widerrufsrecht erlischt
   bei Zustimmung + Hinweis + Bestaetigung (§ 356 Abs. 5)
8. Dienstleistungen, die vollstaendig erbracht wurden (bei ausdruecklicher
   Zustimmung)
9. Beherbergung / Befoerderung / Mietwagen / Verpflegung / Freizeit mit
   festem Termin
10. Notariell beurkundete Vertraege

### § 357 BGB — Rechtsfolgen des Widerrufs

- **Abs. 1:** Rueckgewaehr empfangener Leistungen binnen **14 Tagen**.
- **Abs. 3:** Unternehmer muss **dasselbe Zahlungsmittel** verwenden.
- **Abs. 4:** Unternehmer kann Rueckzahlung **zurueckhalten, bis Ware
  zurueck** oder Nachweis des Versands.
- **Abs. 6:** Rueckversandkosten zu Lasten des Verbrauchers NUR bei
  ordnungsgemaesser Belehrung.
- **Abs. 7:** Wertersatz nur bei Wertverlust durch nicht zur Pruefung
  notwendigen Umgang (z.B. Benutzung).

### Anlage 1 EGBGB — Muster-Widerrufsbelehrung

Platzhalter:

- Name/Anschrift/Kontakt des Unternehmers
- Frist-Beginn (Warenkauf / Dienstleistung / digitaler Inhalt)
- Art und Weise des Widerrufs
- Folgen (Rueckerstattung, Rueckversandkosten, Wertersatz)

Gestaltungshinweise (in Anlage 1 enthalten) erlaeutern, welche Varianten fuer
welchen Vertragstyp einzusetzen sind. Bei sachgerechter Verwendung:
**Gesetzlichkeitsfiktion** — Belehrung gilt als ordnungsgemaess.

### Anlage 2 EGBGB — Muster-Widerrufsformular

Muss dem Verbraucher zur Verfuegung gestellt werden (Pflicht der Zurverfuegung-
stellung, § 312d Abs. 1 BGB iVm Art. 246a § 1 Abs. 2 Nr. 1 EGBGB).

## Typische Fallstricke in Codebases

1. **Widerrufsbelehrung nur als Text auf /widerruf-Seite**, nicht im
   Bestellprozess / nicht per E-Mail nach Bestellung: Verstoss gegen
   § 312f BGB (Bestaetigung in Textform PFLICHT).
2. **Platzhalter im Template nicht ersetzt** ("[Firma einfuegen]"): sofortige
   Unwirksamkeit, Frist verlaengert sich.
3. **Fristberechnung falsch** in Code ("14 Werktage" statt "14 Kalendertage"):
   materieller Rechtsverlust-Risiko.
4. **Digitale Inhalte ohne Verzichtserklaerung + Bestaetigung:** Widerrufsrecht
   bleibt bestehen; Checkbox "Ich verzichte auf mein Widerrufsrecht, wenn
   Download beginnt" + Bestaetigungs-Mail erforderlich.
5. **Widerrufs-Button nicht implementiert:** Unternehmen sind zwar NICHT
   verpflichtet, einen Widerrufs-Button anzubieten (anders: Kuendigungs-
   Button § 312k BGB), muessen aber Widerrufsformular zur Verfuegung stellen.
6. **Rueckversand-Tracking + 14-Tage-Rueckzahlungsfrist:** Oft laeuft Frist
   bei Haendlern aus, bevor Ware zurueck ist — § 357 Abs. 4 erlaubt
   Zurueckbehaltung, aber Prozess muss konfiguriert sein.
7. **Dienstleistung vor Fristablauf begonnen:** ohne ausdruecklichen
   Wunsch + Belehrung: Wertersatz entfaellt trotz Leistung.
8. **Belehrung nur im PDF-Anhang der Bestaetigungsmail:** E-Mail-Inline-
   Fassung plus Anhang sicherer.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Bei SaaS mit Verbrauchernutzung: Widerrufsverzicht bei
  sofortiger Nutzung im Signup-Flow erforderlich. Abo vs. Einmalkauf trennen.
  Klasse `WithdrawalInfo` im Checkout + Copy aus Template.
- **Landingpage:** Reine Lead-Generation → kein Widerruf relevant; bei
  verbindlicher Buchung (Kalender/Booking-Tool) wieder Pflicht.
- **n8n-Workflows:** Post-Order-Workflow sendet Bestellbestaetigung +
  Widerrufsbelehrung (PDF + Inline); Template-Versioning Pflicht
  (Belehrung alt vs. neu).
- **E-Commerce:** Shopify Germany / Shopware liefern Belehrung standardmaessig;
  Custom-Shops muessen Muster aus Anlage 1 EGBGB einbauen.
- **Content/Blog:** Nur relevant bei kostenpflichtigen Mitgliedschaften.

## Behoerden-Hinweise

- Keine zentrale Aufsicht; Wettbewerbszentrale / IDO / vzbv mahnen ab.
- Haftungsrisiko: bei fehlender Belehrung 12 Monate + 14 Tage Widerrufs-
  fenster → erhebliche Rueckabwicklungsrisiken.

## Zitierbare Urteile

- **EuGH C-649/17** (10.07.2019, "Amazon EU"): Informationen zur
  Widerrufsmoeglichkeit muessen leicht zugaenglich sein.
- **BGH VIII ZR 21/19** (08.12.2020): Widerrufsbelehrung muss Fristbeginn
  eindeutig bezeichnen.
- **BGH I ZR 123/16** (15.11.2017): Fehlende/fehlerhafte Belehrung ist
  wettbewerbsrechtlich relevant.
- **EuGH C-641/19** (03.09.2020): Wertersatz bei Widerruf von
  Dienstleistungen.
- **BGH VIII ZR 242/20** (27.04.2022): Belehrung im Video-Commerce.
- **EuGH C-529/19** (21.10.2020, "Moebel Kraft"): Ausnahme "individuelle
  Anfertigung" eng auszulegen.

## Siehe auch

- [[gesetze/bgb-agb]]
- [[themen/button-loesung]]
- [[themen/agb-muster]]
