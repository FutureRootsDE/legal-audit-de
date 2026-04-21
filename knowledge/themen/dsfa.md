---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/kurzpapiere.html
  - https://www.datenschutz-hamburg.de/fileadmin/user_upload/HmbBfDI/Datenschutz/Informationen/DSFA_Muss-Liste_fuer_den_nicht-oeffentlicher_Bereich_-_Stand_17.10.2018.pdf
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

# DSFA — Datenschutz-Folgenabschätzung (Art. 35 DSGVO)

## Kurz-Überblick

Die Datenschutz-Folgenabschätzung (DSFA, Data Protection Impact Assessment / DPIA) ist nach Art. 35 DSGVO verpflichtend, wenn eine Verarbeitung voraussichtlich **ein hohes Risiko** für die Rechte und Freiheiten natürlicher Personen zur Folge hat. Sie ist **vor** der Verarbeitung durchzuführen. Die deutsche Datenschutzkonferenz (DSK) hat eine sogenannte Muss-Liste (Blacklist) mit ~17 typischen DSFA-pflichtigen Fällen veröffentlicht.

## Kernaussagen — Art. 35 DSGVO

### Abs. 1 — Grundsatz
DSFA-Pflicht bei „voraussichtlich hohem Risiko". Wesentliche Indikatoren: neue Technologien, Art/Umfang/Umstände der Verarbeitung.

### Abs. 3 — Regelbeispiele (automatisch DSFA-pflichtig)
- (a) Systematische und umfassende Bewertung persönlicher Aspekte durch automatisierte Entscheidung (Scoring, Profiling)
- (b) Umfangreiche Verarbeitung besonderer Datenkategorien (Art. 9) oder Strafdaten (Art. 10)
- (c) Systematische umfangreiche Überwachung öffentlich zugänglicher Bereiche

### Abs. 4 — Positivliste der Aufsichtsbehörden (Muss-Liste)
Jede Aufsichtsbehörde veröffentlicht Liste von Verarbeitungen, die zwingend DSFA erfordern. Deutsche Liste (DSK, Stand 17.10.2018, Version 1.1) für nichtöffentliche Stellen. Auch für KMU verbindlich.

### Abs. 5 — Negativliste
Optional — Verarbeitungen, bei denen DSFA **nicht** erforderlich ist.

### Abs. 7 — Mindestinhalt der DSFA
- (a) Systematische Beschreibung der Verarbeitung + Zwecke + berechtigte Interessen
- (b) Bewertung der Notwendigkeit und Verhältnismäßigkeit
- (c) Risiken für Betroffene
- (d) Abhilfemaßnahmen (TOM, Garantien, Schutzmechanismen)

### Abs. 9 — Einholen der Ansichten der Betroffenen
Soweit möglich sollten Meinungen Betroffener eingeholt werden (z. B. über Interessenvertretungen, Betriebsrat).

### Art. 36 — Vorherige Konsultation
Bleibt trotz Maßnahmen ein hohes Restrisiko: vorherige Konsultation der Aufsichtsbehörde **vor** Verarbeitungsbeginn (Antwort innerhalb 8 Wochen).

## DSK-Muss-Liste (Auszug — 17 Fallgruppen für nichtöffentliche Stellen)

1. **Umfangreiche Verarbeitung biometrischer Daten** zum Zweck der Identifikation
2. **Umfangreiche Verarbeitung genetischer Daten**
3. **Verarbeitung öffentlich zugänglicher Daten in erheblichem Umfang mit AI**
4. **KI-/Big-Data-gestützte Analyse von Bewerber-/Mitarbeiter-Profilen**
5. **Anonymisierungsverfahren** besonderer Kategorien in großem Umfang
6. **Automatisiertes Scoring** für Kreditwürdigkeit / Versicherungstarife
7. **Umfangreiches Tracking** in Ladengeschäften (z. B. durch WLAN-Scanner)
8. **Erstellung umfassender Profile zum Bewegungsverhalten**
9. **Zusammenführung** von Daten aus mehreren Quellen mit Profilbildung
10. **Massenhafte Verarbeitung mit Portalen** zur E-Mobility, Smart-Metering
11. **Umfangreiche Fernsteuerung von Endgeräten**, Smart-Home / IoT-Plattformen
12. **Kameras, Drohnen** mit Gesichtserkennung / Verhaltenserkennung
13. **Telematik-Systeme** mit Geolokalisierung von Fahrzeugen
14. **Lernanalyse-Software (Learning Analytics)** mit Leistungsprofilen
15. **Mobile Apps mit Sensorik** zu Gesundheits- / Bewegungsdaten
16. **Videoüberwachung großer Publikumsbereiche** (Flughäfen, Stadien)
17. **Automatisierte Entscheidungen im Einstellungsverfahren**

## Typische Fallstricke in Codebases

- **SaaS mit KI-gestütztem Scoring / Automation:** AI-Features oft DSFA-pflichtig (Abs. 3 lit. a). Neue Pflichten durch EU-AI-Act (ab 2026 stufenweise).
- **Tracking-heavy Landingpage:** bei breitem Drittland-Transfer + umfassendem Profiling (TCF-String-Fall, EuGH C-604/22): DSFA empfohlen.
- **HR-Tool mit Analytics / People-Analytics:** Mustertyp für DSFA-Pflicht (Punkt 4 DSK-Liste).
- **Fitness-Tracker / Health-Apps:** Art. 9 + Punkt 15 Muss-Liste.
- **CCTV / Smart-Camera in Ladengeschäft:** Punkt 7, 12, 16.
- **Unternehmens-Chatbot mit Konversationsanalyse:** je nach Umfang Profiling (Punkt 4, 8).
- **Produkt-Experimentation-Plattformen** (A/B mit Kohorten-Analyse + PII): Grenzfall, Prüfung empfohlen.
- **DSFA als einmaliges Dokument:** muss bei relevanten Änderungen aktualisiert werden (Art. 35 Abs. 11).

## Relevanz für Codebase-Typen

- **Next.js SaaS:** Bei KI-Features (Scoring, Empfehlungen, Personalisierung), Video-Call-Features (Recording), Analytics mit User-Level-Tracking → DSFA.
- **Landingpage:** In der Regel keine DSFA, wenn „nur" Standard-Tracking. Bei Lead-Scoring / CRM-Automation schon.
- **n8n:** Workflows mit KI-Integration (OpenAI, Claude) und HR-/Kundendaten können DSFA-pflichtig sein. Besonders bei automatisierten Entscheidungen.
- **E-Commerce:** Dynamic Pricing / Preis-Personalisierung, Bonitätsprüfung im Checkout → DSFA.
- **Content/Blog:** Selten DSFA-pflichtig.

## DSFA-Vorgehen (pragmatisch)

1. **Schwellenwertanalyse** — triggert DSFA-Pflicht?
2. **Systematische Beschreibung** der Verarbeitung (Datenflüsse, Beteiligte, Zwecke)
3. **Notwendigkeits-/Verhältnismäßigkeits-Prüfung**
4. **Risiko-Analyse** (Eintrittswahrscheinlichkeit × Schwere)
5. **Maßnahmen-Katalog** (TOM, Garantien)
6. **Restrisiko-Bewertung**
7. **Ggf. Konsultation Aufsichtsbehörde (Art. 36)**
8. **Dokumentation + regelmäßige Überprüfung**

Tools: BSI PIA-Tool (kostenlos), CNIL PIA-Tool (kostenlos), OneTrust, Activemind.

## Behörden-Hinweise

- **DSK Kurzpapier Nr. 5** — Datenschutz-Folgenabschätzung
- **DSK Kurzpapier Nr. 18** — Risiko für Rechte und Freiheiten natürlicher Personen
- **Art.-29-Gruppe WP 248 rev.01** — Leitlinien zur DSFA (vom EDSA übernommen)
- **Muss-Liste DSK v1.1, 17.10.2018** — 17 Fallgruppen
- **CNIL PIA-Software** (kostenlos, auch deutschsprachig)
- **BSI PIA-Leitfaden**

## Zitierbare Urteile

- **EuGH C-26/22, C-64/22 (SCHUFA), 07.12.2023** — Scoring ist automatisierte Entscheidung nach Art. 22 DSGVO
- **EuGH C-634/21 (SCHUFA), 07.12.2023** — Weitere Präzisierung Scoring
- **OVG NRW 16 A 2805/20, 07.05.2024** — Aufsichtsbehörden-Anordnung bei fehlender DSFA
- **VG Wiesbaden 6 K 1164/21.WI, 19.01.2022** — Keylogger-Einsatz DSFA-pflichtig

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]]
- [[themen/meldepflicht-datenpanne]]
