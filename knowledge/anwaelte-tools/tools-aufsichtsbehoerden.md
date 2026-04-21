---
aktualisiert: 2026-04-19
quellen-sekundaer:
  - https://formulare.bfdi.bund.de/
  - https://www.lda.bayern.de/de/datenpanne.html
  - https://www.ldi.nrw.de/kontakt/meldepflicht-fuer-verantwortliche-verletzungen-des-schutzes-personenbezogener-daten
verifiziert-am: 2026-04-19
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
> **Stand:** 2026-04-19

# Meldewege an Aufsichtsbehoerden — Portale und Prozesse

## Kategorie-Ueberblick

Meldungen nach Art. 33 DSGVO (Datenpanne) und Art. 34 DSGVO (Benachrichtigung
Betroffene) sind **fristgebunden** und **formgebunden**. Alle deutschen
Aufsichtsbehoerden haben dafuer eigene Online-Formulare eingerichtet — deren
Nutzung ist in der Regel die **erste Wahl** gegenueber E-Mail/Post.

## Zustaendigkeits-Bestimmung (Schritt 0)

**Bevor Du meldest:** Welche Behoerde ist zustaendig?

- **Nicht-oeffentliche Stelle** (Unternehmen) → LDA des Bundeslandes Hauptsitz
  - In Bayern: **BayLDA** (nicht BayLfD!) — haeufige Verwechslung
- **Oeffentliche Stelle Land** → Landesbeauftragter
- **Oeffentliche Stelle Bund / TK / Post** → **BfDI**
- **Grenzueberschreitend** → federfuehrende Behoerde nach Art. 56 DSGVO (One-Stop-Shop)
- **Kirchliche Stelle** → KDSA / DSG-EKD

Volle Liste in [[behoerden/landesbeauftragte-kontakte]].

## Online-Formulare (verifiziert 2026-04-19)

### BfDI (Bund)

- **URL**: https://formulare.bfdi.bund.de/
- **Formular**: "Meldung Datenschutzverstoss durch Verantwortliche"
- **Authentifizierung**: kein Login noetig
- **Speicherung**: digital, offizieller Eingangsnachweis
- **Rueckmeldung**: i.d.R. binnen weniger Werktage

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

**VERIFIKATION AUSSTEHEND** fuer konkrete direkte Deep-Links pro Bundesland —
pruefen durch `site:lda.brandenburg.de datenpanne` oder aehnliche Google-
Suchanfrage.

## Pflicht-Inhalte der Meldung (Art. 33 Abs. 3)

Alle Online-Formulare fragen diese Felder ab:

- [ ] **Art der Verletzung** (Was ist passiert? Einbruch / Fehlversand / Fehlkonfiguration / Malware / Human Error)
- [ ] **Zeitpunkt** der Verletzung (Begin und ggf. Ende)
- [ ] **Zeitpunkt der Kenntnisnahme** (Start der 72-h-Frist)
- [ ] **Kategorien betroffener Daten** (Identitaet, Kontakt, Finanzen, Gesundheit, Artikel-9-Daten etc.)
- [ ] **Anzahl betroffener Personen** (ungefaehr)
- [ ] **Anzahl betroffener Datensaetze** (ungefaehr)
- [ ] **Wahrscheinliche Folgen** (Identitaetsdiebstahl, Spam, finanzielle Schaeden, Ruf-Schaden)
- [ ] **Ergriffene Massnahmen** (Sofort-Massnahmen und geplante)
- [ ] **Kontakt DSB** / Verantwortlicher mit Name, E-Mail, Telefon
- [ ] **Wurde benachrichtigt** (Art. 34 — wenn hohes Risiko)?

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
- Empfehlungen fuer Betroffene (z.B. "Aendere Dein Passwort sofort")

### Ausnahmen von der Benachrichtigungspflicht (Art. 34 Abs. 3)

- Daten waren verschluesselt (und Schluessel nicht kompromittiert)
- Nachfolgende Massnahmen reduzierten das Risiko auf niedrig
- Benachrichtigung waere **unverhaeltnismaessig aufwendig** → oeffentliche Bekanntmachung

## Bussgeld-Risiko bei verspaeteter / fehlender Meldung

Art. 83 Abs. 4 lit. a DSGVO: bis **10 Mio EUR oder 2% weltweiter Jahresumsatz**.

In der Praxis werden Bussgelder bei verspaeteter Meldung nur dann massiv, wenn
- die Panne selbst durch Nachlaessigkeit entstanden ist
- interne Dokumentation fehlt (Art. 33 Abs. 5)
- oder die Benachrichtigung der Betroffenen unterlassen wurde

Die DSK hat 2019 ein **Bussgeld-Modell** veroeffentlicht (Konzept basiert auf
Umsatz-Klassifizierung und Tages-Saetzen).

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

## Siehe auch

- [[behoerden/landesbeauftragte-kontakte]] — komplette Liste mit Detail-Kontakten
- [[behoerden/dsk-beschluesse]] — Kurzpapier 18 (Risikomodell), Kurzpapier 19 (Datenpannen)
- [[behoerden/bfdi-leitfaeden]]
- [[themen/meldepflicht-datenpanne]] — Pflichten, Fristen, Mustertexte
- [[gesetze/dsgvo]] — Art. 33, 34, 83 (Bussgelder)
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]]
- [[themen/dsfa]]
