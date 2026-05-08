---
aktualisiert: 2026-05-08
gilt-fuer: generische Pre-Launch-Pruefung (jedes Web-Projekt in DE/EU)
verifiziert-am: 2026-05-08
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Diese Generalist-Checkliste
> ersetzt nicht die Pruefung durch einen Fachanwalt vor Launch.
>
> **Stand:** 2026-05-08

# Generische Pre-Launch-Checkliste

## Kurz-Ueberblick

Diese Liste ist die **Meta-Checkliste** — sie entscheidet, welche spezifischen
Audits noetig sind. Fuer Detail-Pruefungen siehe:

- `audit-saas.md` bei Web-Apps / SaaS
- `audit-landingpage.md` bei Marketing-Sites
- `audit-ecommerce.md` bei Shops
- `audit-n8n.md` bei Workflow-Orchestrierung
- `audit-content-blog.md` bei redaktionellen Angeboten

## 0. Projekt-Klassifikation

Zuerst klar bestimmen **was** gelauncht wird — das entscheidet ueber den
Pflichtenkatalog.

- [ ] **Projekt-Typ**: SaaS / Landingpage / E-Commerce / Content-Site / API / Mobile App / n8n / Mixed
- [ ] **Zielgruppe**: B2B / B2C / Mixed
- [ ] **Marktgebiete**: DE / EU / weltweit
- [ ] **Unternehmensgroesse**: Kleinstunternehmen (< 10 MA und < 2 Mio EUR) / Mittel / Gross
- [ ] **Rechtsform**: Einzelunternehmer / GbR / GmbH / UG / AG / Verein
- [ ] **USt-pflichtig**: ja / nein (Kleinunternehmer-Regelung § 19 UStG)
- [ ] **Branche mit Sonder-Compliance**: Finanz / Gesundheit / Kinder / Glueck / Recht

## 1. Rechtstraeger + Impressum

- [ ] Rechtstraeger gegruendet + Handelsregister-Eintrag
- [ ] USt-ID beantragt (bei Pflicht)
- [ ] Geschaeftsadresse **ladungsfaehig** (kein Postfach, Co-Working nur mit Vertrag)
- [ ] Impressum nach § 5 DDG fertig und verlinkt — [[themen/impressum]]
- [ ] Bei journalistischen Angeboten: § 18 MStV verantwortliche Person benannt
- [ ] Aufsichtsbehoerde bei regulierten Berufen genannt
- [ ] [[gesetze/ddg]]

## 2. Datenschutz-Grundpaket

- [ ] **Verarbeitungsverzeichnis** (Art. 30 DSGVO) erstellt — [[themen/verarbeitungsverzeichnis]]
- [ ] **TOM-Dokument** (Art. 32 DSGVO) erstellt — [[themen/tom]]
- [ ] **AVVs** fuer alle aktiven Drittanbieter unterschrieben — [[themen/avv-muster]]
- [ ] **Datenschutzerklaerung** nach Art. 13 DSGVO fertig — [[themen/datenschutzerklaerung]]
- [ ] **DSB** benannt falls Pflicht (§ 38 BDSG: > 20 Personen mit PII-Arbeit ODER Kerngeschaeft Scoring/Profiling/Artikel-9-Daten) — siehe [[anwaelte-tools/datenschutzbeauftragte]]
- [ ] **DSFA** fuer risikoreiche Verarbeitungen (Art. 35) — [[themen/dsfa]]
- [ ] **Drittland-Pruefung** fuer jeden US-/Nicht-EU-Provider — [[themen/drittland-transfer]]
- [ ] **Melde-Prozess** fuer Datenpannen (Art. 33 / 34) definiert — [[themen/meldepflicht-datenpanne]]

## 3. Cookies / Tracking / Consent

- [ ] Alle Cookies/LocalStorage/SessionStorage inventarisiert
- [ ] Kategorisierung: notwendig / praeferenz / statistik / marketing
- [ ] Consent-Banner DSGVO- + BGH-konform (Planet49, Cookie-Einwilligung I/II)
- [ ] Ablehnen-Button gleichrangig zu Akzeptieren
- [ ] Widerruf jederzeit moeglich
- [ ] Consent-Log persistent (Server oder clientseitig mit TTL)
- [ ] Keine Fonts/Maps/Embeds von Drittanbietern ohne Consent
- [ ] [[themen/cookie-consent]], [[themen/tracking-analytics]]

## 4. Vertragstexte

- [ ] **AGB** (falls Leistungsabgabe) mit Einbeziehungs-Mechanismus, AGB-Kontrolle §§ 305-309 BGB — [[themen/agb-muster]]
- [ ] **Widerrufsbelehrung** bei B2C nach § 355 BGB + Art. 246a EGBGB — [[themen/widerrufsbelehrung]]
- [ ] **Button-Loesung** (§ 312j Abs. 3 BGB) bei entgeltlichen Services — Pflichtwortlaut auf finalem Button (BGH I ZR 159/24 v. 09.10.2025) — [[themen/button-loesung]]
- [ ] **Preisangaben** transparent (PAngV; § 11 PAngV: 30-Tage-Tiefstpreis bei Reduzierungen; BGH I ZR 183/22) — [[themen/preisangaben]]
- [ ] **VSBG-Hinweis** bei Online-Verkauf (§ 36 VSBG) — ODR-Plattform-Pflicht **entfaellt seit 20.07.2025** (VO (EU) 2024/3228 — ODR-Plattform abgeschaltet)
- [ ] **SLA** bei B2B-Services (optional, aber empfohlen)

## 5. Marketing / Kommunikation

- [ ] **Newsletter** mit Double-Opt-In — [[themen/email-marketing]]
- [ ] **Werbemails** nur mit Einwilligung (§ 7 Abs. 2 Nr. 2 UWG; Bestandskunden-Ausnahme § 7 Abs. 3 UWG) — [[urteile/bgh-inbox-werbung]] (BGH I ZR 25/19 v. 13.01.2022 "Inbox-Werbung II")
- [ ] **Telefon-Werbung** an Verbraucher nur mit ausdruecklicher (vorheriger) Einwilligung — § 7 Abs. 2 Nr. 1 UWG
- [ ] **SMS / Push** als "elektronische Post" — Opt-In noetig (§ 7 Abs. 2 Nr. 2 UWG)
- [ ] **Kennzeichnung bezahlter Inhalte** (§ 5a Abs. 4 UWG) — [[themen/werbekennzeichnung]]
- [ ] **Influencer-Kooperationen** mit klarer Werbe-Kennzeichnung (BGH I ZR 90/20, 125/20, 126/20 v. 09.09.2021)
- [ ] **Bewertungen-Echtheit** (§ 5b Abs. 3 UWG) — bei Aggregat-Anzeigen Methode der Verifikation transparent

## 6. Geistiges Eigentum

- [ ] **Marken-Recherche** fuer Produktname + Logo (DPMA, EUIPO)
- [ ] **Domain-Check** auf Markenverletzungen
- [ ] **Lizenzen** aller eingesetzten Bilder/Icons/Fonts dokumentiert
- [ ] **Eigene Marken** ggf. anmelden (ab 290 EUR national, 850 EUR EU)
- [ ] **Open-Source-Lizenzen** im Stack kompatibel (MIT/Apache OK, GPL/AGPL vorsichtig)

## 7. Branche-spezifische Sonder-Compliance

Je nach Branche weitere Pflichten:

- [ ] **Finanzdienstleistungen**: BaFin-Erlaubnis, WpIG, KWG
- [ ] **Gesundheit**: HWG, MPDG, Patientendaten-Schutz
- [ ] **Glueckspiel**: GlueStV, Laender-Erlaubnis
- [ ] **Minderjaehrige**: JMStV, Altersverifikation
- [ ] **Arzneimittel**: AMG, HWG
- [ ] **Immobilien**: WoVermRG, MaBV
- [ ] **Telekommunikation**: TKG, BNetzA-Meldung
- [ ] **Kritische Infrastruktur (KRITIS)**: BSI-Meldung, NIS2 — [[gesetze/nis2-bsig]]

## 8. KI / AI Act (Verordnung (EU) 2024/1689)

Anwendbarkeits-Stufung: Verbotene Praktiken (Art. 5) seit **02.02.2025**, **KI-Kompetenz** (Art. 4) seit **02.02.2025**, GPAI-Pflichten seit **02.08.2025**, Vollanwendung ab **02.08.2026**, High-Risk Anhang II ab 02.08.2027.

- [ ] **Verbotene Praktiken** (Art. 5) ausgeschlossen
- [ ] **KI-Kompetenz** Mitarbeiter (Art. 4) — Schulung dokumentiert
- [ ] KI-Komponenten klassifiziert (Verboten / Hoch / Begrenzt / Minimal)
- [ ] Transparenzpflichten erfuellt (Art. 50 AI Act); ab 02.08.2026 Wasserzeichen-Pflicht
- [ ] High-Risk: Konformitaetsbewertung eingeleitet
- [ ] GPAI-Provider-Compliance bei verwendeten Modellen
- [ ] [[gesetze/ai-act]], [[themen/ki-transparenz]], [[themen/ki-content]]

## 9. Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist **seit 28.06.2025 in Anwendung**. Pflicht-Pruefung fuer B2C-Online-Dienstleistungen.

- [ ] Pruefen ob BFSG-pflichtig (B2C-Online-Dienstleistung; Kleinstunternehmen-Ausnahme: < 10 MA UND < 2 Mio EUR)
- [ ] WCAG 2.1 AA eingehalten (BFSGV § 3 setzt EN 301 549 um)
- [ ] **Barrierefreiheitserklaerung** veroeffentlicht (§ 14 BFSG)
- [ ] **Feedback-Kanal** fuer Barrieren
- [ ] Bussgeldrahmen bis 100.000 EUR (§ 37 BFSG)
- [ ] [[gesetze/bfsg]], [[themen/barrierefreiheit]]

## 10. IT-Sicherheit

- [ ] HTTPS / HSTS / TLS 1.2+ aktiviert
- [ ] Admin-Bereiche mit 2FA
- [ ] Passwoerter gehasht (bcrypt/argon2)
- [ ] Backup-Strategie + Disaster Recovery getestet
- [ ] Incident-Response-Plan (wer macht was bei Panne?)
- [ ] Bei KRITIS-/wichtigen-Einrichtungen: NIS2-Compliance

## 11. Finanz-/Steuer-Setup (organisatorisch)

- [ ] Buchhaltungs-System eingerichtet (DATEV, Lexoffice, sevDesk)
- [ ] Rechnungs-Template nach § 14 UStG
- [ ] Archivierung 10 Jahre (§ 257 HGB, § 147 AO)
- [ ] GoBD-konforme Speicherung

## 12. Rechtsanwalt-/DSB-Review

- [ ] Fachanwalt fuer IT-Recht gebucht (Budget 500-1.500 EUR Review, Liste in [[anwaelte-tools/fachanwaelte-it-recht]] und [[anwaelte-tools/kanzleien-saas-spezialisiert]])
- [ ] DSB extern oder intern (falls Pflicht) — [[anwaelte-tools/datenschutzbeauftragte]]
- [ ] Review-Protokoll als PDF archiviert (Beweis der Sorgfalt)

## 13. Live-Browser-Check (vor Go-Live zwingend)

Code-Analyse alleine deckt NICHT auf, was der Browser tatsaechlich laedt. Vor Go-Live zusaetzlich `/legal-audit-live <url>` ausfuehren:

- [ ] Pre-Consent-Pass: keine Requests an `fonts.googleapis.com`, Analytics, Pixel
- [ ] Post-Reject-Pass: nach "Ablehnen" keine Tracker
- [ ] Post-Accept-Pass: nur Tools laden, die in DSE stehen
- [ ] Tool-Liste cross-pruefen mit [[themen/tool-katalog]]
- [ ] Mobile-Emulation: Banner + Buttons erreichbar

## 14. Social-Media / Off-Site-Praesenz

- [ ] Impressum-Link in jedem aktiven Social-Profil (LinkedIn, Instagram, TikTok, X, YouTube, Pinterest)
- [ ] DSE-Link ebenfalls verlinkt
- [ ] Joint-Controller-Addendum mit Meta fuer Facebook-Page akzeptiert
- [ ] Automatisiertes Crossposting (n8n, Zapier): Kennzeichnung nach § 18 Abs. 3 MStV
- [ ] Details: [[themen/social-media-datenschutz]]

## 15. Trust-Signale / Werbung mit Siegeln

- [ ] Alle Siegel/Logos/Testsieger-Hinweise: aktuell, nachpruefbar, lizensiert — [[themen/siegel-werbung]]
- [ ] Pressezitate: § 51 UrhG-konform — [[themen/zitatrecht]]
- [ ] Team-/Kunden-/Testimonial-Fotos: KUG-Einwilligung + Art. 6 DSGVO — [[themen/fotos-dritter-kug]]

## Minimaler Pre-Launch Go-Live-Block (falls Zeit knapp)

Wenn alles andere zurueckgestellt werden muss, aber **ohne diese sechs Punkte NICHT gelauncht werden**:

1. Impressum
2. Datenschutzerklaerung (mit allen aktiven Providern)
3. Cookie-Banner (ohne Pre-Tick, mit Ablehnen)
4. AVVs mit allen Drittanbietern
5. Verarbeitungsverzeichnis (intern)
6. Widerrufsbelehrung + Button-Loesung (bei B2C-Verkauf)

Alles andere ist stark empfehlenswert, aber der Minimum-Satz reduziert
das Abmahn-Risiko auf ein beherrschbares Niveau.

## Post-Launch (erste 30 Tage)

- [ ] Google Search Console + Lighthouse-A11y-Scan
- [ ] Erste Executions in der Datenbank auf PII-Leak gepruft
- [ ] Erste Support-Anfragen: wurden Daten richtig verarbeitet?
- [ ] Consent-Rate monitoren (auffaellige Werte deuten auf fehlerhaftes Banner hin)
- [ ] Sentry/Error-Tracking live
- [ ] Security-Scan (https://observatory.mozilla.org/, https://webbkoll.5july.net/)

## Siehe auch

- [[checklisten/audit-saas]]
- [[checklisten/audit-landingpage]]
- [[checklisten/audit-ecommerce]]
- [[checklisten/audit-n8n]]
- [[checklisten/audit-content-blog]]
- [[gesetze/ai-act]]
- [[gesetze/bfsg]]
- [[gesetze/uwg]]
- [[gesetze/bgb-agb]]
- [[urteile/bgh-cookie-einwilligung]]
- [[urteile/bgh-google-fonts]]
- [[urteile/bgh-inbox-werbung]]
- [[anwaelte-tools/fachanwaelte-it-recht]]
- [[anwaelte-tools/datenschutzbeauftragte]]
- [[anwaelte-tools/tools-generatoren]]
