---
aktualisiert: 2026-11-15
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/kurzpapiere.html
  - https://www.datenschutz-hamburg.de/fileadmin/user_upload/HmbBfDI/Datenschutz/Informationen/DSFA_Muss-Liste_fuer_den_nicht-oeffentlicher_Bereich_-_Stand_17.10.2018.pdf
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
„Der Verantwortliche holt gegebenenfalls den Standpunkt der betroffenen Personen oder ihrer Vertreter […] ein" (z. B. über Interessenvertretungen, Betriebsrat).

### Art. 36 — Vorherige Konsultation
Bleibt trotz Maßnahmen ein hohes Restrisiko: vorherige Konsultation der Aufsichtsbehörde **vor** Verarbeitungsbeginn (Antwort bis zu acht Wochen, verlängerbar um sechs Wochen (Art. 36 Abs. 2)).

## DSK-Muss-Liste (Kurzfassung der 17 Fallgruppen für nichtöffentliche Stellen, Version 1.1)

Kurztitel; maßgeblich ist der Wortlaut der DSK-Muss-Liste V1.1.

1. **Biometrische Daten** (umfangreiche Verarbeitung)
2. **Genetische Daten** (umfangreiche Verarbeitung)
3. **Daten, die einem Sozial-, Berufs- oder Amtsgeheimnis unterliegen**
4. **Aufenthaltsdaten**
5. **Zusammenführung von Daten** (z. B. Fraud-Prevention, Scoring)
6. **Mobile optisch-elektronische Erfassung öffentlicher Bereiche**
7. **Bewertungsportale / Inkasso**
8. **Verhalten von Beschäftigten**
9. **Profile zu Interessen und Beziehungen**
10. **Big-Data-Analysen**
11. **Einsatz von Künstlicher Intelligenz**
12. **Auswertung von Mobilfunk-Sensoren und Funksignalen**
13. **Automatisierte Auswertung von Video- oder Audio-Aufnahmen zur Bewertung der Persönlichkeit**
14. **Profile zum Bewegungs- und Kaufverhalten**
15. **Anonymisierung** besonderer Kategorien
16. **Telemedizin** (Art.-9-Daten mit Sensoren oder mobilen Anwendungen)
17. **Art.-9-Daten aus Sensoren mit zentraler Speicherung** (z. B. Daten aus Fitnessarmbändern)

## Typische Fallstricke in Codebases

- **SaaS mit KI-gestütztem Scoring / Automation:** AI-Features oft DSFA-pflichtig (Art. 35 Abs. 3 lit. a). Zusatzpflichten aus der KI-VO greifen stufenweise: Art. 50 KI-VO (Transparenz von Chatbots, synthetischen Medien, Deepfakes) ist seit **02.08.2026** anwendbar; für vor dem 02.08.2026 in Verkehr gebrachte generative Systeme gilt Art. 50 Abs. 2 erst ab **02.12.2026** (Art. 111 Abs. 4 KI-VO n. F.); die Hochrisiko-Pflichten nach **Anhang III ab 02.12.2027** und nach **Anhang I ab 02.08.2028** (Art. 113 Abs. 3 Buchst. c KI-VO i. d. F. des Art. 1 Nr. 40 Buchst. b VO (EU) 2026/1744). Die **Grundrechte-Folgenabschätzung nach Art. 27 KI-VO** betrifft nur Hochrisiko-KI-Systeme nach Art. 6 Abs. 2 (Anhang III), ausgenommen den Bereich Anhang III Nr. 2; verpflichtet sind Betreiber, die Einrichtungen des öffentlichen Rechts sind oder private Einrichtungen, die öffentliche Dienste erbringen, sowie Betreiber von Systemen nach Anhang III Nr. 5 Buchst. b und c (Kreditwürdigkeitsprüfung sowie Risikobewertung und Preisbildung bei Lebens- und Krankenversicherung); für Anhang-I-Systeme gilt Art. 27 nicht. Zeitlich greift die Pflicht mit der Anwendbarkeit der Anhang-III-Hochrisiko-Pflichten (02.12.2027 nach Art. 113 Abs. 3 n. F.). Abgrenzung zur DSFA nach Art. 35 DSGVO beachten.
- **Tracking-heavy Landingpage:** bei breitem Drittland-Transfer + umfassendem Profiling (TCF-String-Fall, EuGH C-604/22): DSFA empfohlen.
- **HR-Tool mit Analytics / People-Analytics:** Mustertyp für DSFA-Pflicht (Nr. 8 DSK-Muss-Liste).
- **Fitness-Tracker / Health-Apps:** Art. 9 + Nr. 16 und 17 der Muss-Liste.
- **CCTV / Smart-Camera im Ladengeschäft:** Art. 35 Abs. 3 lit. c DSGVO; Muss-Liste Nr. 13 bei automatisierter Videoauswertung zur Bewertung der Persönlichkeit, Nr. 12 nur bei Offline-Tracking über Funksignale. Nr. 6 betrifft mobile Erfassung im öffentlichen Bereich.
- **Unternehmens-Chatbot mit Konversationsanalyse:** je nach Umfang Profiling (Nr. 11 DSK-Muss-Liste).
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
- **CNIL PIA-Software** (kostenlos, Open Source)
- **BSI PIA-Leitfaden**

## Zitierbare Urteile

- **EuGH C-634/21 (SCHUFA, Scoring), 07.12.2023**: Scoring ist automatisierte Entscheidung im Einzelfall nach Art. 22 Abs. 1 DSGVO, sofern der Wert für die Entscheidung des Dritten maßgeblich ist
- **EuGH C-26/22 und C-64/22 (SCHUFA), 07.12.2023**: Speicherdauer von Informationen über eine Restschuldbefreiung bei Auskunfteien über das öffentliche Register hinaus; volle gerichtliche Überprüfbarkeit der Beschlüsse der Aufsichtsbehörde
- **OVG NRW 16 A 2805/20, 07.05.2024** — Aufsichtsbehörden-Anordnung bei fehlender DSFA <<VERIFIKATION AUSSTEHEND>>
- **VG Wiesbaden 6 K 1164/21.WI, 19.01.2022** — Keylogger-Einsatz DSFA-pflichtig <<VERIFIKATION AUSSTEHEND>>

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]]
- [[themen/meldepflicht-datenpanne]]

## Aenderungsvermerk 2026-11-14

- EuGH C-26/22 und C-634/21 (SCHUFA, 07.12.2023) gegen curia.europa.eu
  verifiziert; Aussage bleibt korrekt.
- OVG NRW 16 A 2805/20 und VG Wiesbaden 6 K 1164/21.WI konnten nicht direkt
  gegen rechtsprechung-im-internet.de verifiziert werden; Aktenzeichen bleiben
  stehen mit Verifikationsmarker.
- AI-Act: Stufenweise Anwendbarkeit ergaenzt — Art. 5 (verbotene Praktiken)
  seit 02.02.2025 (die durch VO (EU) 2026/1744 neu eingefuegten Verbote,
  Art. 5 Abs. 1 UAbs. 1 lit. ba, bb, Abs. 1a, 1b, erst ab 02.12.2026),
  GPAI-Governance seit 02.08.2025, Art. 50 (Transparenz)
  anwendbar seit 02.08.2026; Pflichten fuer Hochrisiko-KI nach Anhang III ab
  **02.12.2027**, nach Anhang I ab **02.08.2028** (Art. 113 Abs. 3 Buchst. c
  KI-VO n. F., verschoben durch Art. 1 Nr. 40 Buchst. b der VO (EU) 2026/1744
  ("Digital Omnibus on AI"), verkuendet 24.07.2026, in Kraft seit 27.07.2026;
  Primaerquelle: Cellar-Volltext CELEX:32026R1744). Der am 19.11.2025 von der
  Kommission vorgelegte **Digital-Omnibus-Vorschlag zur DSGVO**
  (COM(2025) 837 final) befindet sich dagegen noch im ordentlichen
  Gesetzgebungsverfahren und ist Stand 2026-11-14 nicht verkuendet.
- Stand/verifiziert-am auf 2026-11-14 vereinheitlicht.
- **2026-11-14 (Review-Korrekturlauf PR #14)**: Fliesstext bei
  "SaaS mit KI-gestuetztem Scoring" konkretisiert — pauschales
  "ab 2026 stufenweise" durch die stufenweise Anwendbarkeit der KI-VO
  (Art. 50 seit 02.08.2026; Hochrisiko Anhang III ab 02.12.2027,
  Anhang I ab 02.08.2028) sowie den Hinweis auf Art. 27 KI-VO
  (Grundrechte-Folgenabschaetzung, erst mit den Hochrisiko-Pflichten)
  ersetzt. Beleg: Art. 27 Abs. 1 KI-VO (Cellar-Volltext
  CELEX:32024R1689); die Omnibus-Verordnung (EU) 2026/1744 aendert
  Art. 27 nur in Abs. 4 und Abs. 5 (Querverweis auf Abschnitte einer
  DSFA bzw. Fragebogenmuster), nicht den Anwendungsbereich in Abs. 1.
- **2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1)**:
  Liste der 17 Fallgruppen durch Kurzfassung der DSK-Muss-Liste V1.1
  ersetzt und Verweise darauf korrigiert (HR Nr. 8, KI-Chatbot Nr. 11,
  Fitness Nr. 16 und 17, CCTV Art. 35 Abs. 3 lit. c und Nr. 12/13);
  Scoring-Aussage (Art. 22) EuGH C-634/21 zugeordnet, C-26/22 und C-64/22
  betreffen die Restschuldbefreiung; Uebergangsfrist Art. 50 Abs. 2 KI-VO
  (Art. 111 Abs. 4 n. F.) ergaenzt; Omnibus-Aktenzeichen COM(2025) 837;
  Art. 35 Abs. 9 und Art. 36 Abs. 2 am Wortlaut ausgerichtet. Der obige
  Vermerk, die Aussage zu C-26/22 bleibe korrekt, ist damit ueberholt.
- 2026-11-15: Korrekturen aus doppelter unabhängiger Prüfung (Runde 2):
  Verbote nach VO (EU) 2026/1744 (Art. 5 Abs. 1 UAbs. 1 lit. ba, bb,
  Abs. 1a, 1b) erst ab 02.12.2026; CNIL PIA-Software ohne Sprachangabe.
