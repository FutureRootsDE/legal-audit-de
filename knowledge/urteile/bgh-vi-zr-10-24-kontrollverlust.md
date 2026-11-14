---
aktualisiert: 2026-11-14
quelle-primaer: https://testphase.rechtsinformationen.bund.de/v1/rechtsprechung/KORE710342024.html
ecli: ECLI:DE:BGH:2024:181124UVIZR10.24.0
quellen-sekundaer:
  - https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2024/2024218.html
  - https://curia.europa.eu/juris/liste.jsf?num=C-182/22
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

# BGH VI ZR 10/24 — Kontrollverlust als immaterieller Schaden (Facebook-Scraping)

## Kurz-Ueberblick

- **Gericht:** Bundesgerichtshof, 6. Zivilsenat
- **Aktenzeichen:** VI ZR 10/24
- **Entscheidungstermin:** 18.11.2024 (Urteil)
- **ECLI:** ECLI:DE:BGH:2024:181124UVIZR10.24.0
- **Vorinstanz:** OLG Koeln, 15. Zivilsenat, Urteil vom 07.12.2023
- **Verfahrenstyp:** Leitentscheidungsverfahren nach § 552b ZPO zum sog.
  **Facebook-Scraping-Komplex** (Vorfall April 2021, ca. 533 Mio.
  Nutzerdaten).

Der 6. Zivilsenat hat erstmals hoechstrichterlich klargestellt, dass bereits
der **kurzzeitige Kontrollverlust ueber eigene personenbezogene Daten**
infolge eines DSGVO-Verstosses ein immaterieller Schaden im Sinne von
**Art. 82 Abs. 1 DSGVO** sein kann — ohne dass eine konkrete missbraeuchliche
Verwendung der Daten oder sonstige spuerbare negative Folgen hinzutreten
muessten.

## Leitsatz (woertlich)

> "Immaterieller Schaden im Sinne des Art. 82 Abs. 1 DSGVO kann auch der
> blosse und kurzzeitige Verlust der Kontrolle ueber eigene personenbezogene
> Daten infolge eines Verstosses gegen die Datenschutz-Grundverordnung sein.
> Weder muss eine konkrete missbraeuchliche Verwendung dieser Daten zum
> Nachteil des Betroffenen erfolgt sein noch bedarf es sonstiger
> zusaetzlicher spuerbarer negativer Folgen."
> (BGH, Urt. v. 18.11.2024, VI ZR 10/24, Rn. 30 — Leitsatz)

## Kernaussagen (mit Randnummern)

- **Rn. 23 f.** — Der Scraping-Vorfall ist bereits dem Verarbeitungsbegriff
  des Art. 4 Nr. 2 DSGVO zu unterstellen (Speichern, Abfragen, Offenlegung
  durch Uebermittlung, Bereitstellung, Verknuepfung); der raeumliche und
  zeitliche Anwendungsbereich der DSGVO ist eroeffnet (Rn. 19 f.).
- **Rn. 30 (Leitsatz)** — Kontrollverlust als immaterieller Schaden i. S. v.
  Art. 82 Abs. 1 DSGVO. Die Auslegung folgt der Linie des EuGH
  (insb. C-300/21, C-340/21, C-687/21, C-456/22, NJW 2024, 1561).
- **Rn. 36** — Zu den **Darlegungsanforderungen**: Werden konkret
  erlebte Folgen vorgetragen (Flut unerwuenschter SMS/Anrufe, Zeit- und
  Muehe-Aufwand beim Umgang mit dem Scraping-Vorfall, Schutz vor
  kuenftigem Missbrauch), ueberspannt das Berufungsgericht die Anforderungen,
  wenn es diese als unsubstantiiert zurueckweist.
- **Rn. 100 f. (Bemessung)** — Der Senat haelt eine Festsetzung "in
  gegebenenfalls nur einstelliger Hoehe" fuer **zweifelhaft** mit Blick
  auf den Effektivitaetsgrundsatz; einen Groessenordnungs-Rahmen von
  **rund 100 EUR** fuer den Kontrollverlust als solchem (im Anschluss an
  OLG Hamm, GRUR-RS 2024, 16856 Rn. 40) haelt er grundsaetzlich fuer
  vertretbar. Bei zusaetzlich geltend gemachten psychischen Beeintraechtigungen
  ist das Tatgericht zu gesonderter Abwaegung aufgerufen (Rn. 101).
- **Rn. 17 ff.** — Streitgegenstand: Der Antrag auf Ersatz des immateriellen
  Schadens bildet einen **einheitlichen Streitgegenstand** rund um den
  Scraping-Vorfall; eine Aufspaltung in gesonderte Betraege fuer einzelne
  Datenschutzverstoesse scheidet aus.

## Tenor (zusammengefasst)

Die Revision des Klaegers hat teilweise Erfolg: Das Berufungsurteil des
OLG Koeln vom 07.12.2023 wird im Kostenpunkt und insoweit aufgehoben, als
die Berufung des Klaegers zu Antraegen auf (1) Ersatz immateriellen Schadens,
(2) Feststellung der Ersatzpflicht fuer kuenftige Schaeden, (3b) Unterlassung
der Verwendung der Telefonnummer ausserhalb der Einwilligung und (5)
vorgerichtliche Rechtsanwaltskosten zurueckgewiesen wurde. Insoweit wird die
Sache zur neuen Verhandlung an das Berufungsgericht zurueckverwiesen; im
Uebrigen wird die Revision zurueckgewiesen.

## Bedeutung fuer Audits

- **Scraping-/Datenleck-Faelle**: Bereits der Kontrollverlust kann einen
  Schadensersatzanspruch nach Art. 82 DSGVO tragen. Betreiber muessen bei
  Datenlecks mit **Massen-Schadensersatzforderungen in Groessenordnung
  rund 100 EUR pro betroffener Person** rechnen (zuzueglich moeglicher
  psychischer Beeintraechtigungen und Aufwands).
- **Scraping-Vorbeugung**: Standardeinstellungen zur Suchbarkeit nach
  Telefonnummer, Rate-Limits, Bot-Erkennung und Monitoring werden zu
  Audit-Kriterien bei Diensten mit grossen Nutzer-Verzeichnissen.
- **Breach-Dokumentation**: Fuer die Darlegungslast bedeutsam, dass konkret
  erlebte Folgen (SMS-Flut, Rufnummernwechsel) substantiiert vorgetragen
  werden koennen — bedingt Audit-Tauglichkeit der Breach-Response-Prozesse
  (siehe [[themen/meldepflicht-datenpanne]]).
- **Produktseitig**: Transparente **Benachrichtigungs- und
  Auskunftsprozesse** nach Art. 33/34/15 DSGVO (siehe Rn. 26 zur
  Kausalitaet).

## Abgrenzung

- **Keine Strafsanktion**: Der Senat betont (Rn. unter Bezugnahme auf EuGH
  C-340/21), dass Art. 82 DSGVO **ausschliesslich Ausgleichsfunktion** hat,
  keine Abschreckung oder Strafe. Schadensersatzhoehe folgt der
  Kompensationslogik, nicht der Bussgeldlogik.
- **Konkurrenz zum gesetzlichen Unterlassungsanspruch**: Zu Antrag 3a
  (Unterlassung unbefugter Offenlegung) weist der Senat auf die bislang
  offene unionsrechtliche Frage hin, ob die DSGVO einen Rueckgriff auf
  § 1004 BGB analog erlaubt (Rn. 56 ff.); Unterlassungsanspruch kann
  zudem aus dem Nutzungsvertrag folgen (§ 280 Abs. 1, § 241 Abs. 2 BGB).
- **Abgrenzung zur bloss abstrakten Gefahr**: Der Kontrollverlust muss
  tatsaechlich eingetreten sein; eine abstrakt-generelle Verletzungsangst
  genuegt nicht.

## Siehe auch

- [[gesetze/dsgvo]] — Art. 82 DSGVO
- [[themen/meldepflicht-datenpanne]]
- [[themen/tom]]
- [[urteile/eugh-schrems-ii]]
- [[urteile/eugh-c-654-25-google-fonts-vorlage]]

## Quellen

- BGH, Urteil vom 18.11.2024, VI ZR 10/24 — Volltext ueber die
  Rechtsinformations-API des Bundes
  (`https://testphase.rechtsinformationen.bund.de/v1/rechtsprechung/KORE710342024.html`).
  Am 2026-11-14 geprueft (ECLI, Datum, Dokumenttyp "Urteil" aus der
  API-Response; Leitsatz, Rn. 30 und Rn. 100 f. am Volltext belegt).
- Pressemitteilung Nr. 218/2024 des BGH (sekundaer).

## Aenderungsvermerk

- **2026-11-14**: Datei neu angelegt; Primaerbeleg ueber die
  Rechtsinformations-API des Bundes. Groessenordnung des Schadensersatzes
  (~100 EUR) und Darlegungsanforderungen (Rn. 36) direkt am Volltext
  (Rn. 100 f.) belegt.
