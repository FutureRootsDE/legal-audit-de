---
aktualisiert: 2026-11-15
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-072020-concepts-controller-and-processor-gdpr_en
  - https://www.datenschutzkonferenz-online.de/kurzpapiere.html
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32021D0915
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

# AVV — Auftragsverarbeitungsvertrag (Art. 28 DSGVO)

## Kurz-Überblick

Der Auftragsverarbeitungsvertrag (AVV, englisch: Data Processing Agreement, DPA) regelt nach Art. 28 DSGVO das Verhältnis zwischen Verantwortlichem und Auftragsverarbeiter. Er ist Pflicht, sobald ein Dienstleister personenbezogene Daten im Auftrag verarbeitet (Hosting, Mail, CRM, Analytics-Tools, Cloud-Speicher, HR-Tools etc.). Ein fehlender oder mangelhafter AVV ist eigener Bußgeldtatbestand nach Art. 83 Abs. 4 lit. a DSGVO (bis 10 Mio. EUR / 2 % Umsatz).

## Kernaussagen — Pflichtinhalte nach Art. 28 Abs. 3 DSGVO

### Formale Anforderungen (Art. 28 Abs. 9)
AVV muss **schriftlich oder in elektronischer Form** abgeschlossen werden (elektronische Form ausreichend — digitaler Versand / Klick-Zustimmung genügt bei klarer Dokumentation).

### Pflicht-Regelungspunkte

1. **Gegenstand und Dauer** der Verarbeitung
2. **Art und Zweck** der Verarbeitung
3. **Art der personenbezogenen Daten** (z. B. Kontaktdaten, Bestelldaten)
4. **Kategorien betroffener Personen** (Kunden, Mitarbeiter, Interessenten)
5. **Rechte und Pflichten des Verantwortlichen**
6. **Weisungsgebundenheit** des Auftragsverarbeiters (Art. 28 Abs. 3 lit. a)
7. **Vertraulichkeitsverpflichtung** der Mitarbeiter (lit. b)
8. **TOM** nach Art. 32 DSGVO (lit. c)
9. **Sub-Auftragsverarbeiter** nur mit vorheriger schriftlicher (allgemein oder spezifisch) Genehmigung (lit. d, Abs. 2)
10. **Unterstützung** bei Betroffenenrechten (lit. e)
11. **Unterstützung** bei Meldepflichten, DSFA, Aufsichtsbehörden-Anfragen (lit. f)
12. **Rückgabe / Löschung** nach Ende der Verarbeitung, nach Wahl des Verantwortlichen (lit. g)
13. **Nachweis- und Kontrollpflichten** (lit. h) — inkl. Audit-Rechte

### EU-Standardvertrag (Art. 28 Abs. 7/8)

EU-Kommission hat Standardvertragsklauseln für AVV erlassen: **Durchführungsbeschluss (EU) 2021/915 vom 04.06.2021** (ABl. L 199 vom 7.6.2021, S. 18). Die Klauseln erfüllen nach Art. 1 des Beschlusses die Anforderungen des Art. 28 Abs. 3 und 4 DSGVO und können ganz oder teilweise Grundlage des Vertrags sein (Art. 28 Abs. 6, 7 DSGVO); eine aufsichtsbehördliche Genehmigung ist für AVV ohnehin nicht vorgesehen.

### Sub-Auftragsverarbeiter (Art. 28 Abs. 2, 4)

- **Allgemeine Genehmigung:** Auftragsverarbeiter darf neue Sub-Prozessoren einsetzen, muss aber vorab informieren und Einspruchsmöglichkeit geben
- **Spezifische Genehmigung:** jeder neue Sub-Prozessor einzeln zustimmungspflichtig
- Sub-Prozessor muss **gleiche vertragliche Pflichten** erfüllen wie Haupt-Auftragsverarbeiter
- **Haftung:** Auftragsverarbeiter haftet für Fehler des Sub-Prozessors wie für eigene

### Abgrenzung: Wer ist Auftragsverarbeiter?

**In der Regel Auftragsverarbeitung (AVV nach Art. 28 Abs. 3 DSGVO), sofern der Anbieter nur weisungsgebunden verarbeitet; Rolle je Dienst prüfen:**
- Hosting (AWS, Hetzner, IONOS, Vercel); Ausnahme nach BayLDA: Hosting rein statischer Websites ohne Datenfluss zum Betreiber und ohne Tracking ist keine Auftragsverarbeitung
- Mail-Versand (Postmark, SendGrid, Resend, Mailchimp)
- CRM (HubSpot, Salesforce, Pipedrive)
- Analytics (Google Analytics, Matomo)
- Cloud-Speicher (Dropbox, Google Drive, OneDrive)
- Video-Conferencing (Zoom, Teams)
- HR-Tools (Personio, BambooHR)
- Error-Monitoring (Sentry, Datadog)
- Customer Support (Intercom, Zendesk)

**Nein — kein AVV (sondern eigene Rechtsgrundlage / Controller-Controller):**
- Banken, Steuerberater, Wirtschaftsprüfer (eigene Berufs-/Geheimhaltungspflichten)
- Paketdienstleister (teils)
- Behörden

**Zahlungsdienstleister:** häufig (auch) eigene Verantwortliche; Rollenverteilung dem Vertrag und der Datenschutzvereinbarung des Anbieters entnehmen.

### Gemeinsame Verantwortung (Art. 26 DSGVO, Joint Controller)

Wenn beide Parteien Zwecke und Mittel gemeinsam festlegen (z. B. Fashion ID / Facebook Like-Button, Meta Pixel): **Joint Controller Agreement (JCA)** statt AVV. Die Wesensmerkmale sind in transparenter Form offenzulegen (Abs. 2).

## Typische Fallstricke in Codebases

- **Fehlender AVV mit GitHub (Copilot / Enterprise Logs):** GitHub speichert Repository-Inhalte, Nutzungsdaten → AVV über Microsoft Data Protection Agreement.
- **OpenAI / Anthropic / Google Gemini API:** Enterprise-Accounts haben Zero-Data-Retention möglich; API-DPA separat abschließen. Bei personenbezogenen Daten in Prompts: AVV zwingend.
- **Free-Tier SaaS ohne DPA-Option:** häufig problematisch — manche Anbieter bieten DPA erst ab Paid-Plan.
- **Keine aktualisierte Sub-Prozessor-Liste:** Vertragspflicht, bei großen Cloud-Anbietern dynamisch (AWS-Sub-Prozessoren ändern sich).
- **Fehlender Widerspruch gegen neuen Sub-Prozessor:** Wenn nicht aktiv überwacht, implizite Zustimmung.
- **Audit-Rechte praktisch nicht durchführbar:** Standard ist Verweis auf SOC 2 / ISO 27001 Reports — muss im AVV explizit geregelt sein.
- **`.env`-Files mit PII in Git:** indirekter AVV-Verstoß, weil unautorisierter Zugriff ermöglicht.
- **ChatGPT in Entwickler-Workflow:** Wenn PII in Prompts gelangt, Datentransfer außerhalb AVV.

## Relevanz für Codebase-Typen

- **Next.js SaaS:**
  - Hosting (Vercel/Netlify/AWS): AVV + Sub-Prozessor-Liste checken
  - Datenbank (Supabase/Neon): DPA + Region
  - Auth (Clerk/Auth0): DPA, besonders bei Magic-Links
  - Analytics: AVV + Consent
  - Mail: AVV zwingend
  - Als SaaS-Anbieter: eigenes AVV-Template für Kunden bereitstellen
- **Landingpage:** Meist nur wenige AVVs (Hosting + Mail + Analytics + Marketing).
- **n8n (self-hosted):** Workflows mit externen APIs lösen AVV-Anforderungen aus (bei jedem Datenfluss prüfen). n8n-Cloud: AVV mit n8n GmbH.
- **E-Commerce:** Typischerweise 15–30 AVVs (Shop-Plattform, Payment, Versand, Newsletter, Reviews, Chat, Retargeting, Fraud-Detection).
- **Content/Blog:** Hosting + CDN + Kommentar-System + Analytics.

## Behörden-Hinweise

- **DSK Kurzpapier Nr. 13** — Auftragsverarbeitung
- **EDSA Leitlinie 07/2020** — Konzepte Verantwortlicher / Auftragsverarbeiter
- **EU-Kommission Durchführungsbeschluss 2021/915** — Standard-AVV
- **BayLDA Formulierungshilfe für einen Vertrag zur Auftragsverarbeitung** und **Abgrenzungshilfe Auftragsverarbeitung/Verantwortlichkeit** (https://www.lda.bayern.de/de/thema_auftragsverarbeitung.html)

## Zitierbare Urteile

- **EuGH C-683/21 (Nacionalinis visuomenės sveikatos centras), 05.12.2023** — Controller-Status setzt keine eigenen Verarbeitungsvorgänge voraus (Tenor 1); Bußgeld nach Art. 83 DSGVO nur bei Vorsatz oder Fahrlässigkeit, kann aber gegen den Verantwortlichen auch für Verarbeitungen seines Auftragsverarbeiters verhängt werden, außer der Auftragsverarbeiter hat für eigene Zwecke oder außerhalb des vom Verantwortlichen festgelegten Rahmens verarbeitet (Tenor 4)
- **EuGH C-40/17 (Fashion ID), 29.07.2019** — Joint-Controller-Definition
- **EuGH C-210/16 (Wirtschaftsakademie), 05.06.2018** — Facebook-Seiten-Betreiber als Mitverantwortliche
- **OLG Frankfurt 6 U 119/23, 30.11.2023** — AVV-Mängel als Wettbewerbsverstoß (streitig) <<VERIFIKATION AUSSTEHEND>>
- **EuGH C-21/23 (Lindenapotheke), 04.10.2024** — Mitbewerber koennen DSGVO-Verstoesse nach UWG verfolgen (relevant fuer Abmahnrisiko bei AVV-Luecken)

## Aenderungsvermerk 2026-11-14

- OLG Frankfurt 6 U 119/23 mit Verifikationsmarker versehen (Aktenzeichen in
  Tier-1-Datenbanken nicht direkt auffindbar).
- EuGH C-21/23 (Lindenapotheke) ergaenzt: bestaetigt die Mitbewerber-
  Klagebefugnis bei DSGVO-Verstoessen, damit auch bei fehlendem/mangelhaftem AVV
  potenziell abmahnbar.
- Standard-AVV (Durchfuehrungsbeschluss 2021/915/EU vom 04.06.2021) gegen
  eur-lex.europa.eu verifiziert (CELEX 32021D0915).
- Stand/verifiziert-am auf 2026-11-14 vereinheitlicht.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  Abgrenzungsliste als Regelfall mit Rollenpruefung je Dienst formuliert,
  BayLDA-Ausnahme fuer rein statisches Hosting ergaenzt; nicht existente
  "BayLDA Checkliste AVV" durch BayLDA Formulierungshilfe und
  Abgrenzungshilfe ersetzt.
- 2026-11-15: Korrekturen aus doppelter unabhängiger Prüfung (Runde 2):
  Genehmigungssatz zum Standard-AVV ersetzt (Art. 1 des Beschlusses,
  Art. 28 Abs. 6, 7 DSGVO, ABl.-Fundstelle); EuGH C-683/21 um Tenor 1 und
  Tenor 4 praezisiert; Zahlungsdienstleister als eigene Zeile statt in Ja-
  und Nein-Liste.

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/drittland-transfer]]
- [[themen/tom]]
- [[themen/verarbeitungsverzeichnis]]
