---
aktualisiert: 2026-11-15
gilt-fuer: generische Pre-Launch-Pruefung (jedes Web-Projekt in DE/EU)
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Diese Generalist-Checkliste
> ersetzt nicht die Pruefung durch einen Fachanwalt vor Launch.
>
> **Stand:** 2026-11-14

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
- [ ] **Unternehmensgroesse**: Kleinstunternehmen (weniger als 10 Beschaeftigte und Jahresumsatz oder Jahresbilanzsumme hoechstens 2 Mio EUR, § 2 Nr. 17 BFSG; BFSG-Ausnahme nur fuer Dienstleistungen, § 3 Abs. 3 BFSG) / Mittel / Gross
- [ ] **Rechtsform**: Einzelunternehmer / GbR / GmbH / UG / AG / Verein
- [ ] **USt-pflichtig**: ja / nein (Kleinunternehmer-Regelung § 19 UStG)
- [ ] **Branche mit Sonder-Compliance**: Finanz / Gesundheit / Kinder / Glueck / Recht
- [ ] **Hosting-/Vermittlungsdienst (DSA)**: Speichert oder vermittelt das Projekt Nutzerinhalte (Art. 3 lit. g DSA)?
- [ ] **Datenverarbeitungsdienst (Data Act)**: Wird Kunden ein skalierbarer Cloud-Dienst bereitgestellt (Art. 2 Nr. 8)?
- [ ] **NIS2**: Einrichtungsart nach Anlage 1/2 BSIG und Schwellen nach § 28 BSIG?

## 1. Rechtstraeger + Impressum

- [ ] Rechtstraeger gegruendet + Handelsregister-Eintrag
- [ ] USt-ID beantragt (bei Pflicht)
- [ ] Anschrift der Niederlassung angegeben (§ 5 Abs. 1 Nr. 1 DDG), kein Postfach; bei Co-Working muss dort tatsaechlich eine Niederlassung bestehen
- [ ] Impressum nach § 5 DDG fertig und verlinkt — [[themen/impressum]]
- [ ] Bei journalistischen Angeboten: § 18 MStV verantwortliche Person benannt
- [ ] Aufsichtsbehoerde bei regulierten Berufen genannt
- [ ] [[gesetze/ddg]]

## 2. Datenschutz-Grundpaket

- [ ] **Verarbeitungsverzeichnis** (Art. 30 DSGVO) erstellt — [[themen/verarbeitungsverzeichnis]]
- [ ] **TOM-Dokument** erstellt (Massnahmen nach Art. 32 DSGVO; Beschreibung im Verarbeitungsverzeichnis nach Art. 30 Abs. 1 Satz 2 lit. g; Nachweis nach Art. 5 Abs. 2 DSGVO) — [[themen/tom]]
- [ ] **AVVs** fuer alle aktiven Drittanbieter unterschrieben — [[themen/avv-muster]]
- [ ] **Datenschutzerklaerung** nach Art. 13 DSGVO fertig — [[themen/datenschutzerklaerung]]
- [ ] **DSB** benannt falls Pflicht (§ 38 Abs. 1 Satz 1 BDSG: in der Regel mindestens 20 Personen staendig mit automatisierter Verarbeitung personenbezogener Daten beschaeftigt; Satz 2: unabhaengig davon bei DSFA-pflichtiger Verarbeitung; ODER Kerntaetigkeit Scoring/Profiling/Artikel-9-Daten nach Art. 37 Abs. 1 lit. b, c DSGVO) — siehe [[anwaelte-tools/datenschutzbeauftragte]]
- [ ] **DSFA** fuer risikoreiche Verarbeitungen (Art. 35) — [[themen/dsfa]]
- [ ] **Drittland-Pruefung** fuer jeden US-/Nicht-EU-Provider — [[themen/drittland-transfer]]
- [ ] **Melde-Prozess** fuer Datenpannen (Art. 33 / 34) definiert — [[themen/meldepflicht-datenpanne]]

## 3. Cookies / Tracking / Consent

- [ ] Alle Cookies/LocalStorage/SessionStorage inventarisiert
- [ ] Kategorisierung: notwendig / praeferenz / statistik / marketing
- [ ] Consent-Banner DSGVO- + BGH-konform (Planet49, Cookie-Einwilligung I/II)
- [ ] Ablehnen-Moeglichkeit auf erster Ebene, wenn das Banner Inhalte versperrt oder eine Interaktion erzwingt (DSK, OH Digitale Dienste, Rn. 124 f.; in der Praxis meist der Fall); Ablehnen als gleichwertige Alternative erkennbar, in Groesse, Farbe, Kontrast und Schriftbild vergleichbar (Rn. 135)
- [ ] Widerruf jederzeit moeglich
- [ ] Consent-Log persistent (Server oder clientseitig mit TTL)
- [ ] Keine Fonts/Maps/Embeds von Drittanbietern ohne Consent
- [ ] [[themen/cookie-consent]], [[themen/tracking-analytics]]

## 4. Vertragstexte

- [ ] **AGB** (falls Leistungsabgabe) mit Einbeziehungs-Mechanismus, AGB-Kontrolle §§ 305-309 BGB — [[themen/agb-muster]]
- [ ] **Widerrufsbelehrung** bei B2C nach § 355 BGB + Art. 246a EGBGB — [[themen/widerrufsbelehrung]]
- [ ] **Button-Loesung** (§ 312j Abs. 3 BGB) bei entgeltlichen Services: Pflichtwortlaut nach § 312j Abs. 3 Satz 2 BGB; bei Verstoss ist der Vertrag endgueltig unwirksam (§ 312j Abs. 4 BGB; BGH, Urt. v. 09.10.2025, I ZR 159/24) — [[themen/button-loesung]]
- [ ] **Kuendigungsbutton § 312k BGB** bei entgeltlichen Dauerschuldverhaeltnissen mit Verbrauchern: Schaltflaeche "Vertraege hier kuendigen" + Bestaetigungsseite mit "jetzt kuendigen", staendig verfuegbar; Folge bei Verstoss: fristlose Kuendigung jederzeit (§ 312k Abs. 6 BGB) — Severity CRIT
- [ ] **Elektronische Widerrufsfunktion / "Widerrufsbutton" nach § 356a BGB** (gesetze-im-internet.de/bgb/__356a.html) bei **allen** Fernabsatzvertraegen, die ueber eine Online-Benutzeroberflaeche geschlossen werden (nicht nur Finanzdienstleistungen): Schaltflaeche "Vertrag widerrufen" (oder eine andere gleichbedeutende eindeutige Formulierung), waehrend der gesamten Widerrufsfrist erreichbar, mit Bestaetigungsschaltflaeche "Widerruf bestaetigen" (oder eine andere gleichbedeutende eindeutige Formulierung) und Eingangsbestaetigung auf dauerhaftem Datentraeger inkl. Datum und Uhrzeit (§ 356a Abs. 1 bis 4 BGB); anzuwenden seit **19.06.2026** (Umsetzung der RL (EU) 2023/2673, CELEX:32023L2673 — Umsetzung bis 19.12.2025, Anwendung ab 19.06.2026) — Severity CRIT
- [ ] **Harmonisierte Mitteilung zum gesetzlichen Gewaehrleistungsrecht** bei Fernabsatz-Warenkauf mit Verbrauchern (Art. 246a § 1 Abs. 1 Satz 1 Nr. 11 EGBGB i. V. m. Anhang I DVO (EU) 2025/1960); bei Haltbarkeitsgarantie ggf. Nr. 11a
- [ ] **Preisangaben** transparent (PAngV; § 11 PAngV: 30-Tage-Tiefstpreis bei Preisermaessigungen fuer **Waren** (gilt nicht fuer Dienstleistungen); EuGH, Urt. v. 26.09.2024, C-330/23 (Aldi Sued); BGH, Urt. v. 09.10.2025, I ZR 183/24 (Jacobs Kroenung)) — [[themen/preisangaben]]
- [ ] **VSBG-Hinweis** bei Online-Verkauf (§ 36 VSBG; Ausnahme fuer die Hinweispflicht nach § 36 Abs. 1 Nr. 1 bei hoechstens zehn Beschaeftigten am 31.12. des Vorjahres, § 36 Abs. 3 VSBG; darunter Hinweispflicht nur bei Teilnahmepflicht, § 36 Abs. 1 Nr. 2 VSBG); die **Pflicht zur Verlinkung der EU-OS-Plattform** nach Art. 14 Abs. 1 VO (EU) 524/2013 ist mit Wirkung vom **20.07.2025** entfallen — Aufhebung durch **VO (EU) 2024/3228** vom 19.12.2024, Art. 1 (CELEX 32024R3228; verifiziert am Cellar-Volltext 2026-11-14). Die OS-Plattform wurde eingestellt; vorhandene Hinweise/Links auf https://ec.europa.eu/consumers/odr/ entfernen.
- [ ] **SLA** bei B2B-Services (optional, aber empfohlen)

## 5. Marketing / Kommunikation

- [ ] **Newsletter** mit Double-Opt-In — [[themen/email-marketing]]
- [ ] **Werbemails** nur mit Einwilligung (§ 7 Abs. 2 Nr. 2 UWG; Bestandskunden-Ausnahme § 7 Abs. 3 UWG) — [[urteile/bgh-inbox-werbung]] (BGH I ZR 25/19 v. 13.01.2022 "Inbox-Werbung II")
- [ ] **Telefon-Werbung** an Verbraucher nur mit ausdruecklicher (vorheriger) Einwilligung — § 7 Abs. 2 Nr. 1 UWG
- [ ] **SMS / Push** als "elektronische Post" — Opt-In noetig (§ 7 Abs. 2 Nr. 2 UWG)
- [ ] **Kennzeichnung bezahlter Inhalte** (§ 5a Abs. 4 UWG) — [[themen/werbekennzeichnung]]
- [ ] **Influencer-Kooperationen**: kommerziellen Zweck kenntlich machen, wenn der Handelnde fuer die Handlung zugunsten eines fremden Unternehmens ein Entgelt oder eine aehnliche Gegenleistung erhaelt oder sich versprechen laesst; die Gegenleistung wird vermutet, es sei denn, er macht glaubhaft, dass er keine erhalten hat (§ 5a Abs. 4 Saetze 2 und 3 UWG), ferner bei eigenem kommerziellen Zweck (Eigenwerbung). Die BGH-Urteile vom 09.09.2021 (I ZR 90/20, 125/20, 126/20) ergingen zu § 5a Abs. 6 UWG a. F.; siehe [[themen/werbekennzeichnung]]
- [ ] **Bewertungen-Echtheit** (§ 5b Abs. 3 UWG) — bei Aggregat-Anzeigen Methode der Verifikation transparent
- [ ] **Umweltaussagen / Nachhaltigkeitssiegel** — EmpCo-Richtlinie (EU) 2024/825 (CELEX:32024L0825): Mitgliedstaaten erlassen bis 27.03.2026, Anwendung ab **27.09.2026** (per Cellar verifiziert); umgesetzt durch G v. 12.02.2026 (BGBl. 2026 I Nr. 43, Drittes UWG-Aenderungsgesetz), in Kraft seit 27.09.2026; Uebergangsvorschrift § 15b UWG (Art. 5 G v. 22.10.2026, BGBl. 2026 I Nr. 322) (siehe [[gesetze/uwg]]): Verbot vager/pauschaler Umweltaussagen (§ 5 Abs. 2 Nr. 1, Abs. 3 Nr. 3/4 UWG), Einschraenkungen bei nicht-zertifizierten Nachhaltigkeitssiegeln (Anhang Nrn. 2a, 4a-4c, 10a, 23d), ergaenzte Informationspflichten § 5b Abs. 3a UWG — Severity HIGH

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
- [ ] **NIS2/BSIG**: nicht nur KRITIS. Betroffenheit nach § 28 BSIG pruefen: Einrichtungsart nach Anlage 1 oder 2 (u. a. Cloud-Computing, Rechenzentrum) ab 50 Beschaeftigten oder Jahresumsatz und Jahresbilanzsumme jeweils ueber 10 Mio. EUR; Pflichten: Risikomanagement (§ 30), Meldepflichten (§ 32), Registrierung (§ 33); siehe [[gesetze/nis2-bsig]]

## 8. KI / AI Act (Verordnung (EU) 2024/1689)

Anwendbarkeit (Stand 2026-11-14, inkl. VO (EU) 2026/1744 Digital Omnibus on AI): Verbotene Praktiken (Art. 5) seit **02.02.2025** (neue NCII/CSAM-Verbote ab 02.12.2026); **KI-Kompetenz** (Art. 4) seit **02.02.2025**, seit 27.07.2026 Verhaltenspflicht; GPAI-Pflichten seit **02.08.2025**; **Art. 50 Transparenz seit 02.08.2026 anwendbar** (Altbestand-Markierung bis 02.12.2026, Art. 111 Abs. 4); Hochrisiko Anhang III **verschoben auf 02.12.2027**, Anhang I **verschoben auf 02.08.2028**.

- [ ] **Verbotene Praktiken** (Art. 5) ausgeschlossen (inkl. NCII/CSAM-Generatoren ab 02.12.2026)
- [ ] **KI-Kompetenz** Art. 4 KI-VO n. F. (seit 27.07.2026 i. d. F. VO (EU) 2026/1744): Anbieter und Betreiber ergreifen **Massnahmen zur Unterstuetzung** der KI-Kompetenz; **keine Pflicht**, ein bestimmtes Kompetenzniveau zu **garantieren** (Art. 4 Abs. 1 Satz 2 n. F.) — Foerdermassnahmen und Schulungsnachweise dennoch dokumentieren
- [ ] KI-Komponenten klassifiziert (Verboten / Hoch / Begrenzt / Minimal)
- [ ] Transparenzpflichten erfuellt (Art. 50 AI Act), getrennt nach Rolle: maschinenlesbare Markierung nach Art. 50 Abs. 2 seit 02.08.2026 (Altbestand bis 02.12.2026) ist Pflicht des Anbieters; Betreiber treffen die Pflichten nach Art. 50 Abs. 4 (Deepfakes; Texte zu Angelegenheiten von oeffentlichem Interesse ohne menschliche Ueberpruefung und redaktionelle Verantwortung)
- [ ] High-Risk: Konformitaetsbewertung eingeleitet
- [ ] GPAI-Provider-Compliance bei verwendeten Modellen
- [ ] [[gesetze/ai-act]], [[themen/ki-transparenz]], [[themen/ki-content]]

## 9. Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist **seit 28.06.2025 in Anwendung**. Pflicht-Pruefung fuer B2C-Online-Dienstleistungen.

- [ ] Pruefen ob BFSG-pflichtig (B2C-Online-Dienstleistung; Kleinstunternehmen-Ausnahme: weniger als 10 Beschaeftigte und Jahresumsatz oder Jahresbilanzsumme hoechstens 2 Mio EUR, § 2 Nr. 17 BFSG; BFSG-Ausnahme nur fuer Dienstleistungen, § 3 Abs. 3 BFSG)
- [ ] WCAG 2.1 AA als Pruefraster: § 3 BFSGV verweist auf den Stand der Technik; Konformitaetsvermutung nach § 4 BFSG, EN 301 549 / WCAG 2.1 AA nur darueber; Anforderungen §§ 12, 19 BFSGV
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
- [ ] Archivierung: Rechnungen/Buchungsbelege 8 Jahre (§ 257 Abs. 1 Nr. 4, Abs. 4 HGB; § 147 Abs. 1 Nr. 4, Abs. 3 AO; § 14b Abs. 1 UStG); Buecher, Inventare, Abschluesse 10 Jahre; Handels- und Geschaeftsbriefe 6 Jahre; Ausnahme 10 Jahre fuer Kredit-, Versicherungs- und Wertpapierinstitute (§ 257 Abs. 4 Satz 2 HGB)
- [ ] GoBD-konforme Speicherung

## 12. Rechtsanwalt-/DSB-Review

- [ ] Fachanwalt fuer IT-Recht gebucht (Kosten vorab erfragen, Liste in [[anwaelte-tools/fachanwaelte-it-recht]] und [[anwaelte-tools/kanzleien-saas-spezialisiert]])
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
- [ ] Automatisiertes Crossposting (n8n, Zapier): Kennzeichnung nach § 18 Abs. 3 MStV, wenn das Nutzerkonto seinem aeusseren Erscheinungsbild nach fuer die Nutzung durch natuerliche Personen bereitgestellt wurde
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
6. Widerrufsbelehrung + Button-Loesung, elektronische Widerrufsfunktion (§ 356a BGB) und Kuendigungsbutton bei entgeltlichen Dauerschuldverhaeltnissen (§ 312k BGB) (bei B2C-Verkauf)

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

---

## Aenderungsvermerk (2026-11-14, Batch F stale-only)

- Frontmatter und Disclaimer-Stand auf 2026-11-14 aktualisiert.
- Abschnitt 4 (Vertragstexte) um Kuendigungsbutton § 312k BGB erweitert; Tier-1-belegt gegen gesetze-im-internet.de/bgb/__312k.html.
- **Abschnitt 4 (Korrektur):** Elektronische Widerrufsfunktion nach § 356a BGB gilt NICHT nur fuer Fernabsatz-Finanzdienstleistungsvertraege, sondern fuer **alle** Fernabsatzvertraege, die ueber eine Online-Benutzeroberflaeche geschlossen werden. Pflichtschaltflaechen "Vertrag widerrufen" und "Widerruf bestaetigen", Eingangsbestaetigung mit Datum/Uhrzeit, anzuwenden seit 19.06.2026. Tier-1-Beleg: gesetze-im-internet.de/bgb/__356a.html; RL (EU) 2023/2673 (CELEX:32023L2673) per Cellar verifiziert (Umsetzung bis 19.12.2025, Anwendung ab 19.06.2026). Marker aufgeloest.
- Abschnitt 4 (VSBG/ODR): Marker am 2026-11-14 aufgeloest. Primaerbeleg VO (EU) 2024/3228 vom 19.12.2024, Art. 1 (CELEX 32024R3228, Cellar-Volltext): Aufhebung der VO (EU) 524/2013 mit Wirkung 20.07.2025, Einstellung der OS-Plattform.
- Abschnitt 5 um EmpCo-RL (EU) 2024/825 (ab 27.09.2026) ergaenzt; nun Cellar-verifiziert (CELEX:32024L0825, Mitgliedstaaten erlassen bis 27.03.2026, Anwendung ab 27.09.2026). Deutsche Umsetzung Tier-1-belegt via knowledge/gesetze/uwg.md (Art. 6 Gesetz vom 22.10.2026, BGBl. 2026 I Nr. 322, § 15b UWG). Marker aufgeloest.
- Bestandspruefung (11 Pflicht-Normzitate ausserhalb Abschnitt 8): alle bestaetigt — § 5 DDG, § 18 MStV, Art. 30/32/33/35/5/13/17 DSGVO, § 38 BDSG, § 7 Abs. 2 Nr. 2/Abs. 3 UWG, § 5a Abs. 4 UWG, § 5b Abs. 3 UWG, § 312j Abs. 3 BGB, § 312k BGB, § 11 PAngV, § 51 UrhG, § 22 KUG, § 14/§ 37 BFSG, § 257 HGB, § 147 AO. BGH-Aktenzeichen I ZR 159/24 (09.10.2025), I ZR 25/19 (13.01.2022), I ZR 90/20, 125/20, 126/20 (09.09.2021), I ZR 7/16 (28.05.2020, "Cookie-Einwilligung II"), EuGH C-673/17 (Planet49), C-40/17 (Fashion ID) — konsistent zu KB.
- Abschnitt 8 (KI) wurde am selben Tag von einem anderen Agent aktualisiert; hier nicht angetastet.

## Aenderungsvermerk (2026-11-15)

- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1): Kleinstunternehmen-Definition (§ 2 Nr. 17 BFSG) und BFSGV § 3 berichtigt; DSB-Pflicht nach § 38 Abs. 1 BDSG und Art. 37 Abs. 1 lit. b, c DSGVO; I ZR 159/24 nur fuer die endgueltige Unwirksamkeit nach § 312j Abs. 4 BGB; 30-Tage-Tiefstpreis mit EuGH C-330/23 und BGH I ZR 183/24 statt I ZR 183/22; VSBG-Ausnahme § 36 Abs. 3; Influencer-Kennzeichnung nur bei Gegenleistung bzw. eigenem kommerziellen Zweck; EmpCo-Umsetzung durch G v. 12.02.2026 (BGBl. 2026 I Nr. 43), § 15b UWG nur Uebergangsvorschrift (berichtigt den EmpCo-Vermerk oben); Art. 50 KI-VO nach Anbieter und Betreiber getrennt; Aufbewahrungsfristen 8/10/6 Jahre; Crossposting-Hinweis nur bei personenaehnlichen Konten. Die Bestandspruefung oben ("alle bestaetigt", "konsistent zu KB") traf insoweit nicht zu.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2): Projekt-Klassifikation um DSA, Data Act und NIS2 ergaenzt; Anschrift der Niederlassung (§ 5 Abs. 1 Nr. 1 DDG); TOM-Dokument mit Art. 32, Art. 30 Abs. 1 Satz 2 lit. g, Art. 5 Abs. 2; Ablehnoption einheitlich nach DSK, OH Digitale Dienste, Rn. 124, 125, 135; Widerrufsfunktion § 356a BGB auf CRIT; neuer Punkt harmonisierte Gewaehrleistungsmitteilung (DVO (EU) 2025/1960); 30-Tage-Tiefstpreis nur fuer Waren; NIS2/BSIG nach § 28 BSIG statt nur KRITIS; Kuendigungsbutton und Widerrufsfunktion im Go-Live-Block; Anwaltsbudget gestrichen.
