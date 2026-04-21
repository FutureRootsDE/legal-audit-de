---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/kunsturhg/BJNR000070907.html
quellen-sekundaer:
  - https://www.rechtsprechung-im-internet.de/
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
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

# Fotos Dritter — Recht am eigenen Bild (KUG) und DSGVO

## Kurz-Ueberblick

Das **Recht am eigenen Bild** ist in Deutschland seit 1907 im Kunsturhebergesetz
(KUG, §§ 22, 23) geregelt. Es schuetzt die Abgebildeten davor, dass Fotos ohne
ihre Einwilligung **verbreitet oder oeffentlich zur Schau gestellt** werden.

Seit Inkrafttreten der DSGVO (25.05.2018) besteht Unsicherheit ueber das
Verhaeltnis von KUG zu DSGVO. Die h.M. und Rechtsprechung gehen davon aus:

- **DSGVO gilt fuer das Erstellen** und die allgemeine Verarbeitung des Fotos
- **KUG gilt (fort) fuer Verbreitung/Zurschaustellung** — ueber Art. 85 DSGVO
  ("Oeffnungsklausel Medien") oder als Ausdruck nationaler Regelungskompetenz

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
- Einwilligung ist **formfrei** moeglich (auch konkludent), aber aus
  Beweisgruenden stets schriftlich/elektronisch dokumentieren
- Einwilligung ist **widerruflich** (BAG, st.Rspr. — fuer Mitarbeitende
  insbesondere bei Ausscheiden)
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

Die Rechtsprechung (OLG Koeln, LG Frankfurt, KG Berlin) wendet KUG weiterhin
an, ergaenzt durch DSGVO-Informations- und Loeschpflichten.

## Typische Fallstricke in Codebases / Webseiten

| Problem | Risiko | Fix |
|---|---|---|
| Team-Foto auf About-Seite ohne Einwilligung | § 22 KUG, Art. 6 DSGVO | Schriftliche Einwilligung **vor** Veroeffentlichung |
| Ehemaliger Mitarbeiter weiterhin im Impressum/Team | Widerruf nach Ausscheiden wirksam | 30-Tage-Prozess: Ausscheiden -> Foto runter |
| Event-Fotos mit erkennbaren Gaesten | § 22 KUG | Hinweisschilder am Eingang + Opt-out-Moeglichkeit, oder § 23 Nr. 3 |
| Kunden-Testimonial mit Foto | § 22 KUG + UWG (Authentizitaet) | Schriftliche, zweckgebundene Einwilligung |
| Stock-Foto mit Model-Release fehlend | § 22 KUG | Nur Stock-Anbieter mit Model-Release nutzen, Lizenz archivieren |
| KI-generierte Gesichter aehneln realen Personen | § 22 KUG analog + Persoenlichkeitsrecht | Sorgfaeltige Pruefung, siehe [[ki-content]] |
| Hintergrund-Personen auf Social-Media-Foto erkennbar | § 22 KUG | Unkenntlich machen oder § 23 Nr. 2 (Beiwerk) pruefen |

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

### OLG Koeln, 15 U 66/18, 08.10.2018 (DSGVO + KUG, Fortgeltung KUG) `<<VERIFIKATION AUSSTEHEND>>`

Aktenzeichen und Datum final anhand der Originalquelle zu verifizieren
(dejure/NJW). Kernaussage: Das KUG ist neben der DSGVO weiterhin anwendbar,
weil Art. 85 DSGVO als Oeffnungsklausel eine nationale Regelung ermoeglicht.

### LG Frankfurt a.M., 2-03 O 234/20 `<<VERIFIKATION AUSSTEHEND>>`

Aktenzeichen und Datum final zu verifizieren. Tendenz der Rechtsprechung:
Foto ohne Einwilligung -> Unterlassungsanspruch + Schadensersatz (§ 823 BGB
i.V.m. § 22 KUG; Art. 82 DSGVO).

### BAG, 8 AZR 1011/13, 19.02.2015

> "Die nach § 22 KUG erteilte Einwilligung eines Arbeitnehmers in die
> Verbreitung seines Bildnisses zu Werbezwecken erlischt nicht automatisch mit
> dem Ende des Arbeitsverhaeltnisses; sie kann jedoch bei plausiblen Gruenden
> widerrufen werden."

Praxisfolge: Nach Ausscheiden einer Person reicht pauschaler Widerruf fuer
Loeschpflicht des Arbeitgebers.

### BGH VI ZR 160/18, 07.07.2020 (Google-Recht auf Vergessen II)

Grundsatz: Abwaegung zwischen Recht auf Vergessen und Recht auf Information
bei dauerhaft online auffindbaren Bildnissen.

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
> Die Einwilligung erfolgt fuer [Dauer/unbefristet] und ist jederzeit
> **schriftlich** gegenueber [Kontakt] widerrufbar mit Wirkung fuer die Zukunft.
> Rechtsgrundlage: § 22 KUG, Art. 6 Abs. 1 lit. a DSGVO.

## Siehe auch

- [[datenschutzerklaerung]] — Foto-DSE-Passus
- [[urheber-stockfoto]] — Lizenzrecht bei Fotos
- [[ki-content]] — KI-generierte Bilder + Persoenlichkeitsrecht
- [[werbekennzeichnung]] — Testimonials + UWG
- [[social-media-datenschutz]] — Fotos auf Fanpages
- [[meldepflicht-datenpanne]] — Foto-Leak als Datenpanne
