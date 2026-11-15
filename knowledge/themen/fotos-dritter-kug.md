---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/kunsturhg/BJNR000070907.html
quellen-sekundaer:
  - https://www.rechtsprechung-im-internet.de/
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=LG+Frankfurt/Main&Datum=26.09.2019&Aktenzeichen=2-03+O+402/18
verifiziert-am: 2026-11-14
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
> **Stand:** 2026-11-14

# Fotos Dritter — Recht am eigenen Bild (KUG) und DSGVO

## Kurz-Ueberblick

Das **Recht am eigenen Bild** ist in Deutschland seit 1907 im Kunsturhebergesetz
(KUG, §§ 22, 23) geregelt. Es schuetzt die Abgebildeten davor, dass Fotos ohne
ihre Einwilligung **verbreitet oder oeffentlich zur Schau gestellt** werden.

Seit Geltungsbeginn der DSGVO (25.05.2018, Art. 99 Abs. 2 DSGVO) besteht Unsicherheit ueber das
Verhaeltnis von KUG zu DSGVO:

- **DSGVO gilt fuer das Erstellen** und die allgemeine Verarbeitung des Fotos
- **Fortgeltung des KUG fuer Verbreitung/Zurschaustellung** ist nur im
  journalistischen (sowie kuenstlerischen, wissenschaftlichen,
  literarischen) Bereich ueber Art. 85 DSGVO gesichert (OLG Koeln
  15 W 27/18, 15 U 110/18). Ausserhalb dieses Bereichs ist sie umstritten
  und ungeklaert; dort sind auch Art. 6, 7 und 13 DSGVO zu beachten.

Fuer **Codebase-Relevanz** heisst das: Fotos von Mitarbeitenden, Kunden,
Veranstaltungen, Team-Fotos, Testimonials, Social-Media-Posts — alle brauchen
vor der Online-Veroeffentlichung eine rechtliche Grundlage (Einwilligung oder
gesetzlicher Ausnahmetatbestand).

## Schluesselparagraphen / Kernaussagen

### § 22 KUG (Recht am eigenen Bild)

> "Bildnisse duerfen nur mit Einwilligung des Abgebildeten verbreitet oder
> oeffentlich zur Schau gestellt werden. Die Einwilligung gilt im Zweifel als
> erteilt, wenn der Abgebildete dafuer, dass er sich abbilden liess, eine
> Entlohnung erhielt. Nach dem Tode des Abgebildeten bedarf es bis zum Ablaufe
> von 10 Jahren der Einwilligung der Angehoerigen des Abgebildeten."

**Kernpunkte:**
- Geschuetzt ist das Bildnis (Erkennbarkeit, nicht nur Gesicht)
- Ausserhalb des Arbeitsverhaeltnisses ist die Einwilligung nach § 22 KUG
  **formfrei** (auch konkludent), aber aus Beweisgruenden stets
  schriftlich/elektronisch dokumentieren
- Fotos von Beschaeftigten: Einwilligung schriftlich oder elektronisch
  (§ 26 Abs. 2 Satz 3 BDSG; BAG 19.02.2015, 8 AZR 1011/13: Schriftform),
  dazu Aufklaerung in Textform (§ 26 Abs. 2 Satz 4 BDSG)
- Im Arbeitsverhaeltnis bedarf die Einwilligung nach § 22 KUG der
  Schriftform (BAG 8 AZR 1011/13, Rn. 25). Sie erlischt nicht automatisch
  mit dem Ende des Arbeitsverhaeltnisses (Rn. 32). Ein spaeterer Widerruf
  braucht eine plausible Begruendung (Rn. 37 f.); ohne sie darf der
  Arbeitgeber Aufnahmen, die nur der Illustration dienen, weiter nutzen.
- Hinweis: Das BAG-Urteil erging zum BDSG a. F.; das Verhaeltnis zu
  Art. 7 Abs. 3 DSGVO (jederzeitiger Widerruf) ist seither nicht
  hoechstrichterlich geklaert, anwaltlich pruefen.
- Postmortaler Schutz fuer 10 Jahre

### § 23 KUG (Ausnahmen)

> **(1) Ohne die nach § 22 erforderliche Einwilligung duerfen verbreitet und
> zur Schau gestellt werden:**
>
> 1. Bildnisse aus dem Bereiche der Zeitgeschichte;
> 2. Bilder, auf denen die Personen nur als Beiwerk neben einer Landschaft oder
>    sonstigen Oertlichkeit erscheinen;
> 3. Bilder von Versammlungen, Aufzuegen und aehnlichen Vorgaengen, an denen
>    die dargestellten Personen teilgenommen haben;
> 4. Bildnisse, die nicht auf Bestellung angefertigt sind, sofern die
>    Verbreitung oder Schaustellung einem hoeheren Interesse der Kunst dient.
>
> **(2)** Die Befugnis erstreckt sich jedoch nicht auf eine Verbreitung und
> Schaustellung, durch die ein berechtigtes Interesse des Abgebildeten oder,
> falls dieser verstorben ist, seiner Angehoerigen verletzt wird.

**Abgestuftes Schutzkonzept (BVerfG / BGH):** Bei Personen der Zeitgeschichte
ist stets eine **Einzelfall-Abwaegung** zwischen Informationsinteresse und
Persoenlichkeitsrecht vorzunehmen.

### Verhaeltnis KUG <-> DSGVO seit 2018

- Art. 6 Abs. 1 lit. a DSGVO — Einwilligung
- Art. 6 Abs. 1 lit. f DSGVO — berechtigte Interessen (mit Abwaegung)
- Art. 85 DSGVO — Oeffnungsklausel fuer Journalismus/Kunst/Wissenschaft

Gesichert ist die Fortgeltung des KUG nur im journalistischen Bereich
(OLG Koeln 15 W 27/18, 15 U 110/18). Ausserhalb dieses Bereichs ist sie
umstritten und ungeklaert; dort sind auch Art. 6, 7 und 13 DSGVO zu pruefen.

## Typische Fallstricke in Codebases / Webseiten

| Problem | Risiko | Fix |
|---|---|---|
| Team-Foto auf About-Seite ohne Einwilligung | § 22 KUG, Art. 6 DSGVO | Schriftliche Einwilligung **vor** Veroeffentlichung |
| Ehemaliger Mitarbeiter weiterhin im Impressum/Team | Einwilligung erlischt nicht mit dem Ausscheiden; Widerruf nur mit plausibler Begruendung (BAG 8 AZR 1011/13); Verhaeltnis zu Art. 7 Abs. 3 DSGVO ungeklaert | Widerruf auf plausible Begruendung pruefen; Verhaeltnis zu Art. 7 Abs. 3 DSGVO anwaltlich klaeren |
| Event-Fotos mit erkennbaren Gaesten | § 22 KUG | Einwilligung einholen oder § 23 Abs. 1 Nr. 3 KUG (Versammlungen, Aufzuege und aehnliche Vorgaenge) pruefen; Hinweisschilder und Opt-out dienen der Information (Art. 13 DSGVO), ersetzen die Einwilligung nicht |
| Kunden-Testimonial mit Foto | § 22 KUG + UWG (Authentizitaet) | Schriftliche, zweckgebundene Einwilligung |
| Stock-Foto mit Model-Release fehlend | § 22 KUG | Nur Stock-Anbieter mit Model-Release nutzen, Lizenz archivieren |
| KI-generierte Gesichter aehneln realen Personen | § 22 KUG analog + Persoenlichkeitsrecht | Sorgfaeltige Pruefung, siehe [[ki-content]] |
| Hintergrund-Personen auf Social-Media-Foto erkennbar | § 22 KUG | Unkenntlich machen oder § 23 Abs. 1 Nr. 2 KUG (Beiwerk neben einer Landschaft oder sonstigen Oertlichkeit) pruefen |

## Relevanz fuer Codebase-Typen

### Next.js SaaS / Landingpage

- About-/Team-Seite: Model-Release-Datenbank pflegen, Foto-Asset mit
  Einwilligungs-ID verknuepfen
- CI/CD-Check: Team-Seite vs. Active-Directory der Mitarbeitenden

### E-Commerce

- Kunden-Bewertungen mit Foto: Doppelte Einwilligung (Bewertung + Foto)
- Influencer-Kampagnen: Vertraegliche Bildrechte + Zweckbindung

### Content/Blog

- Journalistische Nutzung fuer Nachrichten: Art. 85 DSGVO + § 23 KUG pruefen
- Archiv-Artikel: "Recht auf Vergessenwerden" beachten (Art. 17 DSGVO)

### n8n

- Workflow-generierte Beitraege mit Personenbildern: automatischer
  Einwilligungs-Check vor Publishing-Schritt

## Behoerden-Hinweise / Gerichtspraxis

- **BfDI / LfDI**: Hinweispapiere zur DSGVO-Anwendung auf Fotografie (z.B.
  LfDI Rheinland-Pfalz, Orientierungshilfe 2018)
- **Hamburger Beauftragter fuer Datenschutz**: Pruefung von Unternehmens-Webseiten
  auf Team-Foto-Compliance
- **BVerfG**: Stuetzt die Einzelfall-Abwaegung bei Personen der Zeitgeschichte
  (Caroline-von-Monaco-Rechtsprechung, fortgefuehrt als "abgestuftes Schutzkonzept")

## Zitierbare Urteile

### OLG Koeln, 15 U 110/18, Beschluss vom 08.10.2018 (DSGVO + KUG, Fortgeltung KUG)

Verifiziert ueber dejure.org / aufrecht.de (Sekundaer-Tier-2, da
rechtsprechung-im-internet.de keine direkte Treffer-URL lieferte).
Kernaussage: Das KUG ist neben der DSGVO weiterhin anwendbar,
weil Art. 85 DSGVO als Oeffnungsklausel eine nationale Regelung ermoeglicht
— jedenfalls fuer journalistische Bildberichterstattung. Hinweis: Das KUG
regelt nur Verbreitung/Schaustellung, nicht das Erstellen der Fotos.

### LG Frankfurt a.M., 2-03 O 402/18, 26.09.2019 (Xing-Profilbild per E-Mail)

Der urspruenglich hier gelistete Verweis "2-03 O 234/20" liess sich gegen
Tier-1-Quellen nicht verifizieren und wurde im Update 2026-07-08 durch das
tatsaechlich einschlaegige, breit rezipierte LG-Frankfurt-Urteil ersetzt.

Sachverhalt: Der Beklagte hatte das Xing-Profilbild des Klaegers per E-Mail
an einen Dritten weitergeleitet, um die Identitaet zu verifizieren.

Kernaussage:
- Das Versenden eines Bildnisses per E-Mail ist ein Verbreiten i.S.d. §§ 22,
  23 KUG (auch bei nicht-koerperlicher Weitergabe in digitaler Form).
- Die Regelungen des KUG gelten ueber Art. 85 Abs. 2 DSGVO als nationale
  Sonderregelungen zum Datenschutz weiter.
- Das Einstellen eines Profilbilds bei Xing ist keine Einwilligung fuer
  jede beliebige weitere Nutzung.

Foto ohne Einwilligung → Unterlassungsanspruch + Schadensersatz (§ 823 BGB
i.V.m. § 22 KUG; Art. 82 DSGVO).

Sekundaerquellen: dejure.org, rechtambild.de, beckmannundnorda.de. LG
Frankfurt a. M. 2-03 O 402/18 nicht am Primaertext verifiziert (die
dejure-Verlinkung war bei der Stichprobe 2026-10-24 nicht abrufbar);
Aktenzeichen und Datum vor Verwendung in einem Audit gegen den Volltext
(z. B. Landesrecht Hessen) pruefen.

### BAG, Urt. v. 19.02.2015, 8 AZR 1011/13 (ECLI:DE:BAG:2015:190215.U.8AZR1011.13.0)

Sinngemaess (kein woertliches Zitat): Im Arbeitsverhaeltnis bedarf die
Einwilligung nach § 22 KUG der Schriftform (Rn. 24 bis 26). Sie erlischt
nicht automatisch mit dem Ende des Arbeitsverhaeltnisses (Rn. 32 bis 34).
Ein spaeterer Widerruf braucht eine plausible Begruendung (Rn. 37 f.).

Praxisfolge: Das blosse Ausscheiden genuegt fuer einen Widerruf nicht. Ohne
plausible Begruendung darf der Arbeitgeber Aufnahmen, die nur der
Illustration dienen, weiter nutzen. Hinweis: Das Urteil erging zum BDSG
a. F.; das Verhaeltnis zu Art. 7 Abs. 3 DSGVO (jederzeitiger Widerruf) ist
seither nicht hoechstrichterlich geklaert, anwaltlich pruefen.

### EuGH C-131/12 (Google Spain), 13.05.2014

Grundlage fuer "Recht auf Vergessenwerden" — Suchmaschinen-Pflicht zur
Delisting bei nicht mehr gerechtfertigter Verbreitung.

## Praxis-Check (Was Code-Reviewer konkret pruefen)

- [ ] Jedes Foto einer erkennbaren Person hat eine dokumentierte
      **Einwilligung** (Release-Form, Stock-Lizenz, Vertrag)
- [ ] Einwilligung nennt konkret: Medium (Web, Print, Social), Zweck,
      Dauer, Widerruflichkeit
- [ ] Prozess "Mitarbeiter scheidet aus" enthaelt Foto-Loeschung
      (Team-Seite, Impressum, About, Pressebereich, Social-Media-Posts,
      Backup/Archive)
- [ ] Gruppen-/Event-Fotos: Hinweisschild + Opt-out-Moeglichkeit
      dokumentiert
- [ ] Kein Stock-Foto ohne Model-Release-Attribut in der Lizenz
      (Adobe Stock, Shutterstock etc.)
- [ ] Bei KI-generierten Gesichtern: Pruefen, dass keine reale Person
      identifizierbar aehnelt; Kennzeichnung als KI-Bild (siehe [[ki-content]])
- [ ] CMS/Asset-Management traegt fuer jedes Bild: Urheber, Lizenz,
      Einwilligungsstatus, Ablaufdatum
- [ ] Journalistische/Redaktions-Fotos: Pruefung § 23 KUG + Art. 85 DSGVO

## Einsatzfertiger Einwilligungstext (Model-Release Kurzform)

> **Einwilligung zur Verwendung von Bildaufnahmen**
>
> Ich, [Name], willige ein, dass die von mir am [Datum] durch [Fotograf] im
> Zusammenhang mit [Zweck/Anlass] gefertigten Aufnahmen durch
> [Unternehmen] zu folgenden Zwecken verwendet werden:
>
> - [ ] Firmenwebsite (Team-/About-Seite)
> - [ ] Social-Media-Profile ([Plattformen benennen])
> - [ ] Printmaterial (Broschuere, Visitenkarten)
> - [ ] Pressearbeit
>
> Die Einwilligung erfolgt fuer [Dauer/unbefristet] und kann jederzeit
> formlos, z. B. per E-Mail an [Kontakt], mit Wirkung fuer die Zukunft
> widerrufen werden.
> Rechtsgrundlage: § 22 KUG, Art. 6 Abs. 1 lit. a DSGVO.

## Siehe auch

- [[datenschutzerklaerung]] — Foto-DSE-Passus
- [[urheber-stockfoto]] — Lizenzrecht bei Fotos
- [[ki-content]] — KI-generierte Bilder + Persoenlichkeitsrecht
- [[werbekennzeichnung]] — Testimonials + UWG
- [[social-media-datenschutz]] — Fotos auf Fanpages
- [[meldepflicht-datenpanne]] — Foto-Leak als Datenpanne

## Aenderungsvermerk 2026-11-14

- Frontmatter-Daten und Disclaimer-Stand auf 2026-11-14 vereinheitlicht
  (zuvor: `aktualisiert` 2026-10-24, `verifiziert-am` + Disclaimer-Stand
  2026-07-08).
- 2026-11-14: geprueft am Primaertext § 22 KUG
  (gesetze-im-internet.de/kunsturhg/__22.html) und § 23 KUG (dto.) sowie
  Art. 6 Abs. 1 Buchst. a und f DSGVO (eur-lex.europa.eu CELEX:32016R0679);
  Kernaussagen (Einwilligungserfordernis, Ausnahmen Bildnis der
  Zeitgeschichte / Beiwerk / Versammlungen / hoeheres Interesse der Kunst)
  bestaetigt.
- Zitate: LG Frankfurt a. M. 2-03 O 402/18 (26.09.2019) nicht am
  Primaertext verifiziert (berichtigt am 2026-11-15; die fruehere Angabe
  "ueber dejure.org bestaetigt" traf nicht zu); BAG 8 AZR 1011/13
  (19.02.2015) breit rezipiert.
- Keine neue BGH-/OLG-Rechtsprechung zu KUG/DSGVO-Verhaeltnis seit
  2026-07-08 identifiziert.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  KUG-Fortgeltung nur im journalistischen Bereich gesichert (OLG Koeln
  15 W 27/18, 15 U 110/18), ausserhalb ungeklaert; Form der Einwilligung
  bei Beschaeftigten (Schriftform, § 26 Abs. 2 Satz 3 und 4 BDSG);
  BAG 8 AZR 1011/13 berichtigt (kein Erloeschen mit Ausscheiden, Widerruf
  nur mit plausibler Begruendung, Randnummern, ECLI, Hinweis zu Art. 7
  Abs. 3 DSGVO); Abschnitt "BGH VI ZR 160/18" gestrichen (Aktenzeichen
  in der Rechtsinformations-API des Bundes nicht nachweisbar; das Urteil
  zum Recht auf Auslistung ist VI ZR 405/18 und traegt keine KUG-Aussage).
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2):
  Widerruf der Einwilligung im Mustertext formlos (Art. 7 Abs. 3 DSGVO);
  Event-Fotos: Hinweisschilder ersetzen die Einwilligung nicht, § 23 Abs. 1
  Nr. 3 KUG; Beiwerk als § 23 Abs. 1 Nr. 2 KUG; Geltungsbeginn der DSGVO
  mit Art. 99 Abs. 2 DSGVO.
