---
aktualisiert: 2026-11-15
quellen-sekundaer:
  - https://www.bfdi.bund.de/DE/Service/Formulare/Formulare_node.html
  - https://www.lda.bayern.de/de/datenpanne.html
  - https://www.ldi.nrw.de/kontakt/meldepflicht-fuer-verantwortliche-verletzungen-des-schutzes-personenbezogener-daten
verifiziert-am: 2026-11-14
teilverifiziert-am: 2026-11-15
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument beschreibt technische Meldewege fuer Datenpannen (Art. 33
> DSGVO). Bei einer konkreten Panne ist **unverzueglich** ein Fachanwalt oder
> ein externer DSB einzubeziehen — die 72-Stunden-Frist laeuft ab Kenntnis.
> Falsch adressierte oder unvollstaendige Meldungen werden mit Bussgeldern
> geahndet.
>
> **Stand:** 2026-11-14

# Meldewege an Aufsichtsbehoerden — Portale und Prozesse

## Kategorie-Ueberblick

Meldungen nach Art. 33 DSGVO (Datenpanne) und Art. 34 DSGVO (Benachrichtigung
Betroffene) sind **fristgebunden**. Eine bestimmte Form schreibt die DSGVO
nicht vor, wohl aber einen gesetzlichen Mindestinhalt (Art. 33 Abs. 3 DSGVO). Erfolgt die Meldung nicht binnen 72
Stunden, ist eine Begruendung fuer die Verzoegerung beizufuegen (Art. 33
Abs. 1 Satz 2 DSGVO). Auftragsverarbeiter melden Verletzungen unverzueglich
dem Verantwortlichen (Art. 33 Abs. 2 DSGVO).
Alle deutschen Aufsichtsbehoerden haben dafuer eigene Online-Formulare eingerichtet — deren
Nutzung ist in der Regel die **erste Wahl** gegenueber E-Mail/Post.

## Zustaendigkeits-Bestimmung (Schritt 0)

**Bevor Du meldest:** Welche Behoerde ist zustaendig?

- **Nicht-oeffentliche Stelle** (Unternehmen) → LDA des Bundeslandes Hauptsitz
  - In Bayern: **BayLDA** (nicht BayLfD!) — haeufige Verwechslung
- **Oeffentliche Stelle Land** → Landesbeauftragter
- **Oeffentliche Stelle Bund / TK / Post** → **BfDI**
- **Grenzueberschreitend** → federfuehrende Behoerde nach Art. 56 DSGVO (One-Stop-Shop)
- **Kirchliche Stelle** → eigene kirchliche Datenschutzaufsicht (Art. 91 Abs. 2 DSGVO): evangelisch die Datenschutzaufsicht nach dem DSG-EKD, katholisch die zustaendige Dioezesan-Datenschutzaufsicht nach dem KDG

Volle Liste in [[behoerden/landesbeauftragte-kontakte]].

## Online-Formulare (verifiziert 2026-11-14)

### BfDI (Bund)

- **Einstieg**: Formularuebersicht des BfDI, https://www.bfdi.bund.de/DE/Service/Formulare/Formulare_node.html (die Stammadresse des Formularportals ist kein eigenstaendiger Meldeweg)
- **Formular**: "Meldung Datenschutzverstoss durch Verantwortliche"
- **Authentifizierung**: kein Login noetig
- **Hinweis Stand 2026-11-14**: Die Online-Anwendung meldete beim Live-Abruf "Die Anwendung steht aktuell nicht zur Verfuegung." Im Panne-Fall vorsorglich ergaenzend per E-Mail/Post an die BfDI melden und Terminverfuegbarkeit der Anwendung pruefen.

### BayLDA (Bayern nicht-oeffentlich)

- **URL**: https://www.lda.bayern.de/de/datenpanne.html
- **Formular**: Online-Meldeformular "Datenpanne"
- Telefon-Rueckfragen: +49 (0) 981 180093-0 (Mo-Fr 08:00-12:00)
- **Alternative**: Kontaktseite /de/kontakt.html + PGP-verschluesselte E-Mail

### LDI NRW (Nordrhein-Westfalen)

- **URL**: https://www.ldi.nrw.de/kontakt/meldepflicht-fuer-verantwortliche-verletzungen-des-schutzes-personenbezogener-daten
- Web-basiertes Formular, PGP-Verschluesselung optional

### Weitere Laender (Konstruktions-Muster)

Muster-URL-Strukturen (fuer direkte Navigation — bei Bedarf auf Behoerden-
Site nach "Datenpanne" / "Meldung Art. 33" / "Verantwortliche" suchen):

| Bundesland | URL-Startpunkt |
|------------|----------------|
| Baden-Wuerttemberg | https://www.baden-wuerttemberg.datenschutz.de/ |
| Berlin | https://www.datenschutz-berlin.de/ → Kontakt → Meldeformular |
| Brandenburg | https://www.lda.brandenburg.de/ |
| Bremen | https://www.datenschutz.bremen.de/ |
| Hamburg | https://datenschutz-hamburg.de/ |
| Hessen | https://datenschutz.hessen.de/ |
| Mecklenburg-Vorpommern | https://www.datenschutz-mv.de/ |
| Niedersachsen | https://lfd.niedersachsen.de/ |
| Rheinland-Pfalz | https://www.datenschutz.rlp.de/ |
| Saarland | https://datenschutz.saarland.de/ |
| Sachsen | https://www.saechsdsb.de/ |
| Sachsen-Anhalt | https://datenschutz.sachsen-anhalt.de/ |
| Schleswig-Holstein | https://www.datenschutzzentrum.de/ |
| Thueringen | https://www.tlfdi.de/ |

Konkrete direkte Deep-Links pro Bundesland pruefen durch
`site:lda.brandenburg.de datenpanne` oder aehnliche Google-Suchanfrage.
<<VERIFIKATION AUSSTEHEND>>

## Inhalte der Meldung

Die Formulare orientieren sich am gesetzlichen Mindestinhalt nach Art. 33 Abs. 3
lit. a bis d DSGVO und fragen darueber hinaus regelmaessig Zeitpunkte und den
Stand der Benachrichtigung nach Art. 34 ab.

Pflichtinhalte (Art. 33 Abs. 3 lit. a bis d):

- [ ] **Art der Verletzung** (Was ist passiert? Einbruch / Fehlversand / Fehlkonfiguration / Malware / Human Error), lit. a
- [ ] **Kategorien betroffener Daten** (Identitaet, Kontakt, Finanzen, Gesundheit, Artikel-9-Daten etc.), lit. a
- [ ] **Anzahl betroffener Personen** (ungefaehr), lit. a
- [ ] **Anzahl betroffener Datensaetze** (ungefaehr), lit. a
- [ ] **Kontakt DSB** oder sonstige Anlaufstelle mit Name, E-Mail, Telefon, lit. b
- [ ] **Wahrscheinliche Folgen** (Identitaetsdiebstahl, Spam, finanzielle Schaeden, Ruf-Schaden), lit. c
- [ ] **Ergriffene Massnahmen** (Sofort-Massnahmen und geplante), lit. d

Uebliche Zusatzfelder der Formulare (nicht Teil von Art. 33 Abs. 3):

- [ ] **Zeitpunkt** der Verletzung (Begin und ggf. Ende)
- [ ] **Zeitpunkt der Kenntnisnahme** (Start der 72-h-Frist)
- [ ] **Wurde benachrichtigt** (Art. 34, wenn hohes Risiko)?

## Vorab: Incident-Package bereithalten

Damit die 72-h-Meldung zeitlich machbar bleibt, sollte VOR einer Panne
bereitstehen:

- [ ] **Incident-Response-Plan** (Flowchart: Who-does-what-when)
- [ ] **Kontakt-Liste** DSB, externer Anwalt, Hoster-Support
- [ ] **Verarbeitungsverzeichnis** (fuer schnelle Ableitung "welche Kategorien betroffen")
- [ ] **Provider-Kontakte** (wenn Panne bei Sub-Prozessor entstand)
- [ ] **Muster-Benachrichtigung** fuer betroffene Personen (vorbereitet, lueckenhaft)
- [ ] **Kommunikations-Kanaele**: Server-Logs sichern, Git-Diff, DB-Snapshot

## Nachmeldung / Ergaenzung

Wenn initial nicht alle Informationen vorliegen (oft der Fall), kann
**schrittweise nachgemeldet** werden (Art. 33 Abs. 4 DSGVO). Das ist besser
als die 72-h-Frist reissen zu lassen.

## Art. 34: Benachrichtigung der Betroffenen

Zusaetzlich zur Meldung an die Aufsichtsbehoerde ist bei **hohem Risiko** fuer
Rechte und Freiheiten der Betroffenen eine **direkte Benachrichtigung** an
die Betroffenen noetig.

### Wann "hohes Risiko"?

- Abfluss von Kontodaten / Kreditkartendaten
- Abfluss von Login-Credentials (Passwoerter im Klartext)
- Abfluss von Artikel-9-Daten (Gesundheit, Ethnie, Religion, Sexualitaet)
- Abfluss von Daten, die zu Diskriminierung fuehren koennen
- Siehe DSK-Kurzpapier 18 (Risikomodell)

### Pflicht-Inhalte der Benachrichtigung

- Beschreibung der Verletzung in **klarer, einfacher Sprache**
- Kontakt-Moeglichkeit (Name/E-Mail DSB)
- Beschreibung der wahrscheinlichen Folgen
- Ergriffene / beabsichtigte Abhilfe-Massnahmen
- Massnahmen zur Abmilderung moeglicher nachteiliger Auswirkungen (Art. 33 Abs. 3 lit. d), sinnvollerweise mit Handlungsempfehlungen fuer Betroffene (z.B. "Aendere Dein Passwort sofort")

### Ausnahmen von der Benachrichtigungspflicht (Art. 34 Abs. 3)

- Daten fuer Unbefugte unzugaenglich gemacht, etwa durch Verschluesselung mit nicht kompromittiertem Schluessel (Art. 34 Abs. 3 lit. a DSGVO)
- Nachfolgende Massnahmen stellen sicher, dass das hohe Risiko aller Wahrscheinlichkeit nach nicht mehr besteht (Art. 34 Abs. 3 lit. b)
- Benachrichtigung waere **unverhaeltnismaessig aufwendig** → oeffentliche Bekanntmachung

## Bussgeld-Risiko bei verspaeteter / fehlender Meldung

Art. 83 Abs. 4 lit. a DSGVO: bis **10 Mio EUR oder 2% weltweiter Jahresumsatz**.

In der Praxis werden Bussgelder bei verspaeteter Meldung nur dann massiv, wenn
- die Panne selbst durch Nachlaessigkeit entstanden ist
- interne Dokumentation fehlt (Art. 33 Abs. 5)
- oder die Benachrichtigung der Betroffenen unterlassen wurde

Die DSK hat 2019 ein **Bussgeld-Modell** veroeffentlicht (Konzept basiert auf
Umsatz-Klassifizierung und Tages-Saetzen). Massgeblich fuer die Zumessung sind
inzwischen die EDSA-Leitlinien 04/2022 fuer die Berechnung von Geldbussen; zum
Verfahren siehe die DSK-Musterrichtlinien (MRiDaVG) vom 16.06.2025. <<VERIFIKATION AUSSTEHEND>>

## Checkliste fuer den Panne-Tag

### Stunde 0-2 (Incident Detection)

- [ ] Logs sichern (sofort, nicht erst nach Analyse)
- [ ] Systeme isolieren (wenn Malware/Einbruch) — aber **keine Beweise zerstoeren**
- [ ] Incident-Team alarmieren (DSB, externer Anwalt, Hoster-Support)
- [ ] Zeitstempel "Kenntnisnahme" exakt dokumentieren (Email-Eingang, Log-Alert)

### Stunde 2-12 (Triage)

- [ ] Umfang bestimmen (welche Datensaetze / Kategorien / Anzahl)
- [ ] Risiko-Einschaetzung nach DSK Kurzpapier 18
- [ ] Entscheidung: Meldepflicht ja/nein (bei Zweifel → melden)
- [ ] Entscheidung: Benachrichtigungs-Pflicht ja/nein

### Stunde 12-48 (Meldung vorbereiten)

- [ ] Online-Formular-Felder ausfuellen
- [ ] Juristischer Review durch Anwalt / DSB
- [ ] Kommunikations-Entwurf an Betroffene (falls Art. 34)

### Stunde 48-72 (Meldung einreichen)

- [ ] Online-Formular einreichen, Einreichungs-PDF speichern
- [ ] Interne Dokumentation (Art. 33 Abs. 5)
- [ ] Wenn Art. 34: Benachrichtigung versenden (parallel oder kurz darauf)

### Stunde 72+ (Aufarbeitung)

- [ ] Forensik-Bericht
- [ ] Root-Cause-Analyse
- [ ] Technische Korrekturen (Patch, Config, Training)
- [ ] Prozess-Update (wie verhindern wir das kuenftig?)
- [ ] Nachmeldung bei Behoerde, falls neue Erkenntnisse
- [ ] Abschluss-Kommunikation Betroffene (wenn Art. 34)

## Kommunikations-Stil in der Meldung

- **Sachlich** — keine Schuld-Verteilung
- **Vollstaendig** — lieber zuviel als zuwenig (Aufsichtsbehoerde schaetzt Transparenz)
- **Selbstkritisch-aber-nicht-panisch** — "Wir haben folgendes festgestellt und bereits unternommen"
- **Realistische Massnahmen-Plaene** — keine Versprechungen, die nicht gehalten werden koennen
- **Referenz auf Verarbeitungsverzeichnis** — beweist, dass Datenschutz-Governance existiert

## Hinweis: ODR-Plattform abgeschaltet (2025-07-20)

Die EU-**Online-Streitbeilegungsplattform (ODR/OS)** unter `ec.europa.eu/consumers/odr` ist seit dem **20.07.2025** eingestellt; die Rechtsgrundlage (VO (EU) 524/2013) wurde durch **VO (EU) 2024/3228** vom 19.12.2024, Art. 1 aufgehoben (CELEX 32024R3228; am 2026-11-14 am Cellar-Volltext verifiziert). Pflichten zur Verlinkung aus AGB / Impressum / Footer sind damit weggefallen. Verbraucherstreitbeilegung erfolgt seither ueber nationale Schlichtungsstellen (z.B. Universalschlichtungsstelle des Bundes / Allgemeine Verbraucherschlichtungsstelle des Zentrums fuer Schlichtung e.V., Kehl). Unberuehrt bleibt die Informationspflicht nach § 36 Abs. 1 VSBG (Angabe, ob der Unternehmer zur Teilnahme an einem Verfahren vor einer Verbraucherschlichtungsstelle bereit oder verpflichtet ist); ausgenommen sind Unternehmer mit zehn oder weniger Beschaeftigten (§ 36 Abs. 3 VSBG). Hinweis hier nur fuer Cross-Ref — ODR betrifft UWG/E-Commerce-Pflichten, **nicht** den Art.-33/34-DSGVO-Meldeweg, der hier dokumentiert ist.

## Siehe auch

- [[behoerden/landesbeauftragte-kontakte]] — komplette Liste mit Detail-Kontakten (in Wave-1 aktualisiert)
- [[behoerden/dsk-beschluesse]] — Kurzpapier 18 (Risiko fuer die Rechte und Freiheiten natuerlicher Personen)
- [[behoerden/bfdi-leitfaeden]]
- [[themen/meldepflicht-datenpanne]] — Pflichten, Fristen, Mustertexte
- [[gesetze/dsgvo]] — Art. 33, 34, 83 (Bussgelder)
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]]
- [[themen/dsfa]]

## Aenderungsvermerk

- **2026-11-14** (Batch E, stale-only): Freitext-Marker fuer die Deep-Link-Tabelle der 14 Landesaufsichtsbehoerden auf die einheitliche Form des Verifikationsmarkers (einzeilig, am Ende des Hinweises) normiert. Normative Aussagen gegen Tier-1 bestaetigt: 72-Stunden-Frist (Art. 33 Abs. 1 DSGVO), Benachrichtigungspflicht (Art. 34 DSGVO), Bussgeldrahmen 10 Mio EUR / 2 % (Art. 83 Abs. 4 lit. a DSGVO).
- **2026-11-14** (Batch E3, Live-Pruefung): Portale aktiv abgerufen. BfDI-Formular-Portal `formulare.bfdi.bund.de` erreichbar, aber Anwendung meldete "aktuell nicht zur Verfuegung" — Hinweis in Eintrag ergaenzt. BayLDA-Datenpanne-Seite (`lda.bayern.de/de/datenpanne.html`) und LDI-NRW-Meldeseite erreichbar und Formular-Links aktiv (LDI-Formular jetzt unter `ldi-fms.nrw.de/lip/action/invoke.do?id=Datenschutzverletzung`). ODR-Abschaltung 20.07.2025 gegen `consumer-redress.ec.europa.eu/site-relocation_en` bestaetigt (Rechtsgrundlage VO (EU) 2024/3228). `verifiziert-am` auf 2026-11-14 aktualisiert. Deep-Links der Landesaufsichtsbehoerden-Tabelle bleiben nicht einzeln reverifiziert und tragen weiterhin den Sammel-Marker.
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1): keine Formbindung, aber Mindestinhalt nach Art. 33 Abs. 3; Abschnitt "Inhalte der Meldung" trennt Pflichtinhalte nach lit. a bis d von Formular-Zusatzfeldern; Benachrichtigungsinhalt an Art. 33 Abs. 3 lit. d angeglichen; Ausnahme Art. 34 Abs. 3 lit. b wortnah gefasst; Kurzpapier 18 statt 19; BfDI-Einstieg ueber die Formularuebersicht, unbelegte Angaben zu Speicherung und Rueckmeldung entfernt; Hinweis auf EDSA-Leitlinien 04/2022 und DSK-Musterrichtlinien ergaenzt (Daten mit Verifikationsmarker, Nachpruefung offen).
- **2026-11-15**: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2): Begruendungspflicht bei verspaeteter Meldung (Art. 33 Abs. 1 Satz 2) und Meldung des Auftragsverarbeiters (Art. 33 Abs. 2) ergaenzt; kirchliche Aufsicht nach Art. 91 Abs. 2 DSGVO gefasst; Ausnahme Art. 34 Abs. 3 lit. a wortnah; Hinweis auf § 36 VSBG beim ODR-Wegfall ergaenzt.
