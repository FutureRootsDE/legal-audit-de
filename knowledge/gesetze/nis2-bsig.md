---
aktualisiert: 2026-04-19
quelle-primaer: https://www.bundesregierung.de/breg-de/aktuelles/nis-2-richtlinie-deutschland-2373174
quellen-sekundaer:
  - https://www.bundestag.de/dokumente/textarchiv/2025/kw46-de-nis-2-1123138
  - https://www.openkritis.de/it-sicherheitsgesetz/nis2-umsetzung-gesetz-cybersicherheit.html
  - https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Regulierte-Wirtschaft/NIS-2/nis-2_node.html
  - https://eur-lex.europa.eu/eli/dir/2022/2555/oj
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

# BSIG / NIS-2-Umsetzungsgesetz (NIS2UmsuCG)

## Kurz-Ueberblick

Die **NIS-2-Richtlinie (EU) 2022/2555** loest die NIS-1-Richtlinie ab und setzt deutlich erweiterte Anforderungen an die **Cybersicherheit von Unternehmen und oeffentlichen Stellen** in der EU. Umsetzungsfrist war **17.10.2024**.

**Deutschland** hat verzoegert umgesetzt: Das **NIS-2-Umsetzungs- und Cybersicherheitsstaerkungsgesetz (NIS2UmsuCG)** wurde
- am **13.11.2025** vom Bundestag beschlossen
- am **21.11.2025** vom Bundesrat gebilligt
- am **05./06.12.2025** im Bundesgesetzblatt verkuendet und **unmittelbar in Kraft getreten** (ohne Uebergangsfrist)

Quellen: Bundesregierung, Bundestag-Pressearchiv (2025-11), BGBl. (Dezember 2025)

Das NIS2UmsuCG **novelliert das BSI-Gesetz (BSIG)** erheblich. Der gelaeufige Ausdruck "BSIG 2.0" bezeichnet diese novellierte Fassung.

## Schluesselparagraphen / Kernaussagen

### Betroffenenkreis (stark erweitert vs. NIS-1)

Zwei Kategorien:

**1. Besonders wichtige Einrichtungen (bwE)** / "essential entities":
- **Grossunternehmen** (>= 250 Beschaeftigte ODER > 50 Mio. EUR Jahresumsatz UND > 43 Mio. EUR Bilanzsumme)
- Aus Sektoren nach **Anhang I NIS-2**: Energie, Verkehr, Bankwesen, Finanzmarktinfrastruktur, Gesundheit, Trinkwasser, Abwasser, Digitale Infrastruktur (DNS, TLD-Registries, Cloud-, Rechenzentrums-, CDN-Anbieter), IKT-Dienste, oeffentliche Verwaltung, Raumfahrt
- **Proaktive BSI-Aufsicht**, 3-jaehrlicher Nachweis
- Bussgelder bis **10 Mio. EUR oder 2 %** weltweitem Jahresumsatz

**2. Wichtige Einrichtungen (wE)** / "important entities":
- **Mittelgrosse Unternehmen** (>= 50 Beschaeftigte ODER > 10 Mio. EUR Umsatz UND > 10 Mio. EUR Bilanzsumme)
- Aus Sektoren nach **Anhang II NIS-2**: Post-/Kurierdienste, Abfallwirtschaft, Chemie, Lebensmittel, Verarbeitendes Gewerbe (Medizinprodukte, Elektronik, Maschinenbau, Fahrzeuge), Digitale Dienstleister (Online-Marktplaetze, Online-Suchmaschinen, Plattformen fuer Soziale Netze), Forschung
- **Reaktive Aufsicht** (anlassbezogen)
- Bussgelder bis **7 Mio. EUR oder 1,4 %** weltweitem Jahresumsatz

**Schaetzung**: ca. **30.000 Einrichtungen** in DE erfasst (gegenueber ~4.500 unter NIS-1 / altem BSIG).

### Kernpflichten (nach BSIG n.F. / NIS-2-Art. 21)

**Risikomanagement-Massnahmen** (mindestens):
1. Konzepte und Verfahren **Risikoanalyse und Informationssicherheit**
2. **Incident Handling**
3. **Business Continuity / Backup / Krisenmanagement**
4. **Supply-Chain-Security** (Lieferkette)
5. Sicherheit in Netz- und Informationssystemen (Beschaffung, Entwicklung, Wartung)
6. **Wirksamkeitsbewertung** der Risikomanagement-Massnahmen
7. Grundlegende **Cyberhygiene** und Schulungen
8. **Kryptografie** und ggf. Verschluesselung
9. Personalsicherheit, Zugangskontrolle, Asset Management
10. **MFA / kontinuierliche Authentifizierung**, gesicherte Sprach-/Video-/Textkommunikation, gesicherte Notfallkommunikation

### Meldepflichten (nach NIS-2-Art. 23)

Bei **erheblichen Sicherheitsvorfaellen**:
- **24 Stunden**: Erstmeldung (Fruehwarnung)
- **72 Stunden**: Vorfallsmeldung (mit Erstbewertung, Indicators of Compromise)
- **1 Monat**: Abschlussbericht

Meldung an das **BSI** (zentral in DE ueber NIS-2-Meldeportal).

### Leitungshaftung (neu, Art. 20 NIS-2)

Geschaeftsleitungen (Geschaeftsfuehrer, Vorstand) haften **persoenlich** fuer:
- Umsetzung der Cybersicherheits-Risikomassnahmen
- **Pflichtschulungen** zu Cybersicherheit
- Bussgelder und Entzug von Managementverantwortung bei schweren Verstoessen moeglich

### Registrierungspflicht

Betroffene Einrichtungen muessen sich **beim BSI registrieren** (3-Monats-Frist nach Feststellung der Betroffenheit; fuer digitale Infrastruktur-Anbieter teilweise bereits beim Markteintritt).

## Typische Fallstricke in Codebases

- **Supply-Chain-Security ignoriert**: Dependencies ohne CVE-Monitoring, keine SBOM (Software Bill of Materials)
- **Kein Incident-Response-Playbook**
- **Unverschluesselte Backups**
- **Keine MFA** fuer Admin-Zugaenge
- **Secrets in Git** (klassischer Fall; auch DSGVO-Risiko)
- **Container-Images** ohne Vulnerability Scanning
- **Logs unverschluesselt / nicht persistent**: 72h-Meldepflicht kaum erfuellbar
- **Third-Party-SaaS ohne Datenverarbeitungsvertrag + Sicherheitsnachweis**
- **Keine Leitungsschulung** dokumentiert
- **Nicht registriert** beim BSI trotz Betroffenheit

## Relevanz fuer Codebase-Typen

**Bitte beachten: NIS-2-Pflicht haengt an UNTERNEHMENSGROESSE + SEKTOR, nicht am Codebase-Typ.**

- **Next.js SaaS als digitaler Dienstleister**: Wenn Online-Marktplatz, Online-Suchmaschine oder Plattform fuer soziale Netze → Anhang II (wichtige Einrichtung), wenn Schwellen erfuellt. Klassischer SaaS (z. B. B2B-Tool) ist oft NICHT sektoral erfasst — aber pruefen!
- **Landingpage**: Nicht NIS-2-verpflichtet als solche.
- **n8n-Automation fuer interne Prozesse**: Keine direkte Pflicht. Wenn n8n-Server der Bundesbehoerde betrieben wird: andere Regelungen fuer oeffentliche Verwaltung (Anhang I Ziff. 8).
- **E-Commerce als Online-Marktplatz** (B2C Plattform mit Drittanbietern): Anhang II wichtige Einrichtung bei Schwellen.
- **Content/Blog**: Nicht erfasst.
- **Cloud-, DNS-, CDN-, Rechenzentrums-Anbieter**: Anhang I besonders wichtige Einrichtung, **schon bei mittelgrosser Groesse** (keine Sektor-Befreiung fuer KMU-Schwellen bei kritischen Digitalen Infrastrukturen).

**Wichtig**: Auch wenn NIS-2 formal nicht greift, sind die Massnahmen **Good Practice**. Zudem strahlen sie ueber **Supply-Chain-Security-Anforderungen** auf KMU-Zulieferer aus (bwE-Unternehmen verlangen Nachweise von Dienstleistern).

## Behoerden-Hinweise

- **BSI (Bundesamt fuer Sicherheit in der Informationstechnik)**: https://www.bsi.bund.de/ — zentrale Aufsichtsbehoerde und Meldestelle
- **BSI NIS-2-Informationsseite**: https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Regulierte-Wirtschaft/NIS-2/nis-2_node.html
- **BMI** (Bundesinnenministerium): Gesetzgebungsverantwortlich
- **Praxisleitfaden**: BSI IT-Grundschutz + BSI-Mindeststandards als Orientierung

## Zitierbare Urteile

**Kaum bestehende Rechtsprechung** — das NIS2UmsuCG ist erst seit Dezember 2025 in Kraft.

Indirekt relevant aus NIS-1-Ära / IT-Sicherheitsgesetz:
- **VG Koeln, Urt. v. 11.10.2019 — 1 L 861/19** (zu KRITIS-Einstufungsbescheiden)
- **BGH, Urt. v. 16.03.2021 — VI ZR 260/20** (Haftungsmassstab bei Datenpannen, DSGVO-nahe Anwendung)

`<<VERIFIKATION AUSSTEHEND>>` — erste BSI-Bussgeldbescheide unter NIS2UmsuCG sind fuer 2026 zu erwarten; beim naechsten Update pruefen.

## Siehe auch

- [[dsa]] — ueberschneidende Kontaktstelle (Art. 11/12 DSA); Security-Anforderungen an Hosting
- [[ai-act]] — Cybersicherheitsaspekte bei Hochrisiko-KI (Art. 15)
