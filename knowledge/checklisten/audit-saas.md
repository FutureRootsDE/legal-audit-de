---
aktualisiert: 2026-11-14
gilt-fuer: SaaS-Anwendungen (Next.js/React, Node/Python-Backend, PostgreSQL, Cloud-Hosting)
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Eine Pruefung durch einen
> zugelassenen Rechtsanwalt ist zwingend, bevor ein SaaS-Produkt live geht.
>
> **Stand:** 2026-11-14

# Audit-Checkliste: SaaS-Anwendung (Next.js/React)

## Kurz-Ueberblick

Diese Checkliste pruefst Du **vor jedem Production-Launch** und wiederholst sie
mindestens **halbjaehrlich**. Sie ist generisch — fuer ein konkretes ausgearbeitetes Beispiel mit Thompson-Sampling-Schwierigkeit siehe:

> **Referenz-Implementierung:** `C:\Users\Philip\SaaS_Project\projects\ksk-automation\.planning\plans\10-kind-quokka.md` — Gray Areas GA-1 bis GA-8 enthalten reichhaltige AVV-, Retention- und DSFA-Beispiele fuer KI-basiertes SaaS mit Stripe/Mistral/Brevo/Vercel/Hetzner.

### Kurz-Scope

- [ ] Multi-Tenant oder Single-Tenant? (Multi-Tenant = striktere Isolierung)
- [ ] B2C, B2B oder Mixed? (BFSG seit 28.06.2025 anwendbar — bei B2C zwingend pruefen)
- [ ] Welche Drittlaender? (USA/UK/CH/IN — je mehr, desto komplexer)
- [ ] KI-Komponenten? (AI Act Risk-Class — Limited Risk i.d.R. = Transparenzpflicht; verbotene Praktiken seit 02.02.2025; GPAI-Pflichten seit 02.08.2025; Art. 50 Transparenz seit 02.08.2026; Hochrisiko Anhang III seit Digital Omnibus VO (EU) 2026/1744 verschoben auf 02.12.2027)
- [ ] **KI-Kompetenz** Art. 4 KI-VO gilt seit 02.02.2025; seit 27.07.2026 in der Fassung der VO (EU) 2026/1744: Anbieter und Betreiber ergreifen **Massnahmen zur Unterstuetzung der KI-Kompetenz** ihres Personals und der in ihrem Auftrag mit KI befassten Personen — **ausdruecklich keine Pflicht**, ein bestimmtes Kompetenzniveau zu **garantieren** (Art. 4 Abs. 1 Satz 2 KI-VO n. F.); Schulungs- und Sensibilisierungsnachweise trotzdem dokumentieren (Nachweis-Obliegenheit).

## Pass 1: PII-Identifikation

Ziel: vollstaendiges Verzeichnis aller personenbezogenen Daten im System.

- [ ] Datenbank-Schema gescannt — alle Tabellen mit `email`, `name`, `ip`, `user_agent`, `address`, `phone`
- [ ] Log-Dateien (Backend, Nginx, PostgreSQL, Redis) — welche PII werden geloggt?
- [ ] Third-Party-SDKs im Frontend (Sentry, PostHog, Mixpanel, GA4) — Daten-Abfluss identifiziert
- [ ] File-Uploads (S3, R2, lokales FS) — welche User-Inhalte werden gespeichert?
- [ ] E-Mail-Inhalte (Transactional, Marketing) — Zwischenspeicherung in Brevo/Mailgun/Resend
- [ ] Session/Cookie-Namen erfasst und Zweck dokumentiert
- [ ] WebSockets / Server-Sent Events — Payload-Inhalte
- [ ] Payment-Daten (PCI-DSS Scope pruefen — Stripe Elements = Scope 1, Server-side Card = Scope 4)
- [ ] Backup-Strategie und -Retention fuer DB-Dumps
- [ ] Ergebnis: Verarbeitungsverzeichnis nach Art. 30 DSGVO vollstaendig? (siehe [[themen/verarbeitungsverzeichnis]])

## Pass 2: Drittland-/Drittanbieter-Transfers

Ziel: jeder ausgehende API-Call rechtlich abgesichert.

- [ ] Provider-Liste vollstaendig (inkl. Sub-Prozessoren!)
- [ ] Fuer jeden Provider: **AVV vorhanden** und unterzeichnet?
- [ ] Fuer jeden USA-Provider: **DPF-Zertifizierung** pruefen (dataprivacyframework.gov) — falls ja, zusaetzlich SCC als Fallback
- [ ] Fuer jeden Nicht-EU-Provider ohne DPF: **SCC Modul 2 (C2P) oder Modul 3 (P2P)** + TIA (Transfer Impact Assessment)
- [ ] Schrems-II-Konformitaet: **Zusatz-Massnahmen** dokumentiert? (Verschluesselung at rest/in transit, Pseudonymisierung, technische Zugriffs-Sperren)
- [ ] Informationspflicht nach Art. 13 Abs. 1 lit. f DSGVO in der Datenschutzerklaerung erfuellt?
- [ ] Sub-Prozessor-Liste des Providers gepflegt und **Veraenderungs-Benachrichtigungs-Klausel** im AVV?
- [ ] Differenzierung: **Auftragsverarbeitung** (Art. 28) vs. **gemeinsame Verantwortlichkeit** (Art. 26) vs. **getrennte Verantwortlichkeit**

### Typische SaaS-Provider-Kategorisierung

| Kategorie | Beispiel | Art der Verarbeitung | Rechtsgrundlage |
|-----------|----------|---------------------|-----------------|
| Hosting (EU) | Hetzner, Scaleway | AVV (Art. 28) | Art. 6 Abs. 1 lit. b/f |
| Hosting (US mit EU-Region) | Vercel, AWS-Frankfurt | AVV + SCC + DPF (falls zertifiziert) | siehe oben |
| Payment | Stripe | **Getrennte Verantwortlichkeit** (PCI-DSS-Zone + aufsichtsrechtliche Pflichten) | Art. 6 Abs. 1 lit. b/c |
| Transactional Mail | Brevo (FR), Postmark (US) | AVV (Art. 28) | lit. b/f |
| Marketing Mail | Mailchimp (US) | AVV + Opt-In-Nachweise | lit. a (Einwilligung) |
| KI-API | Mistral (FR, EU), OpenAI (US), Anthropic (US) | AVV + SCC (falls US) + DPF-Pruefung | lit. b/f + ggf. Art. 9 bei besonderen Kategorien |
| Analytics | PostHog self-hosted, Plausible | meist AVV Art. 28; Plausible cookie-frei | lit. f |
| Error-Tracking | Sentry SaaS | AVV + PII-Minimisierung (Masking!) | lit. f |

## Pass 3: Cookie-/Consent-Analyse

Ziel: § 25 TDDDG + DSGVO sauber umgesetzt.

- [ ] **Technisch notwendige** Cookies/Storage identifiziert (Session, CSRF, Language-Pref) — **kein Consent** noetig
- [ ] **Nicht-notwendige** Cookies/Scripts (Analytics, Marketing, Pixel) — ausschliesslich **nach Einwilligung**
- [ ] **Consent-Banner** vorhanden, **ablehnen gleichrangig zu akzeptieren** (Planet49, BGH I ZR 7/16)
- [ ] **Granulare Kategorien** statt "Alle oder nichts" (kein Dark Pattern)
- [ ] **Pre-ticked Boxes** VERBOTEN (Planet49 EuGH C-673/17)
- [ ] **Widerruf genauso einfach** wie Einwilligung (Art. 7 Abs. 3 DSGVO)
- [ ] Consent-Log mit Zeitstempel, Version, Wahl pro Kategorie — 2-Jahres-Aufbewahrung ueblich
- [ ] **Google Consent Mode v2** korrekt eingebunden (falls Google-Services)
- [ ] Fonts lokal self-hosted (nicht via fonts.googleapis.com — LG Muenchen I 3 O 17493/20 "Google Fonts")
- [ ] Embeds (YouTube, Vimeo, Maps, Twitter/X) nur mit 2-Klick-Loesung oder Consent
- [ ] Siehe [[themen/cookie-consent]] und [[themen/tracking-analytics]]

## Pass 4: Pflicht-Texte (Impressum / DSE / AGB)

- [ ] **Impressum** nach § 5 DDG + § 18 MStV — Vor- und Nachname oder Firma, Anschrift, Vertretungsberechtigte, Kontakt, Registernummer, USt-ID, Berufsrechtliche Angaben (bei regulierten Berufen) — siehe [[themen/impressum]]
- [ ] **Datenschutzerklaerung** nach Art. 13 DSGVO — Verantwortlicher, DSB, Zwecke, Rechtsgrundlagen, Empfaenger, Drittland, Speicherdauer, Betroffenenrechte, Beschwerderecht, automatisierte Entscheidungen — siehe [[themen/datenschutzerklaerung]]
- [ ] **AGB** (falls vorhanden) mit wirksamer Einbeziehung (§§ 305 ff. BGB), inbesondere AGB-rechtliche Klauselkontrolle
- [ ] **Widerrufsbelehrung** (bei B2C) — siehe [[themen/widerrufsbelehrung]]
- [ ] **Button-Loesung** "zahlungspflichtig bestellen" (§ 312j Abs. 3 BGB) bei kostenpflichtigen Services — Pflicht-Wortlaut (oder gleichbedeutend); BGH I ZR 159/24 (09.10.2025) bestaetigt: bei mehrstufigen Bestell-Flows muss Pflichtwortlaut auf finalem Button stehen — siehe [[themen/button-loesung]]
- [ ] **Kuendigungsbutton § 312k BGB** bei Abo-/SaaS-Vertraegen mit Verbrauchern: Schaltflaeche "Vertraege hier kuendigen" (oder gleichwertig) + Bestaetigungsseite mit Button "jetzt kuendigen", staendig verfuegbar und leicht zugaenglich (§ 312k Abs. 2 BGB); Bestaetigung unverzueglich in Textform (§ 312k Abs. 4 BGB); Folge bei Verstoss: jederzeitige fristlose Kuendigung durch Verbraucher moeglich (§ 312k Abs. 6 BGB) — Severity CRIT
- [ ] **Preisangaben-Transparenz** (PAngV — Gesamtpreis inkl. USt, monatlich/jaehrlich)
- [ ] **Widerrufsrecht bei digitalen Inhalten** — Hinweis auf Verzicht moeglich (§ 356 Abs. 5 BGB)
- [ ] **Elektronische Widerrufsfunktion nach § 356a BGB** bei B2C-Vertraegen, die ueber eine Online-Benutzeroberflaeche geschlossen werden (nicht auf Finanzdienstleistungen beschraenkt): Pflichtschaltflaeche "Vertrag widerrufen" (oder eine andere gleichbedeutende eindeutige Formulierung) waehrend der gesamten Widerrufsfrist erreichbar + Bestaetigungsschaltflaeche "Widerruf bestaetigen" (oder eine andere gleichbedeutende eindeutige Formulierung) + Eingangsbestaetigung auf dauerhaftem Datentraeger mit Datum und Uhrzeit (§ 356a Abs. 1-4 BGB; gesetze-im-internet.de/bgb/__356a.html); anzuwenden seit **19.06.2026** (Umsetzung RL (EU) 2023/2673, CELEX:32023L2673) — Severity HIGH

## Pass 5: KI-Spezifisch (AI Act — Verordnung (EU) 2024/1689)

Anwendbarkeit (Stand 2026-11-14, inkl. Digital Omnibus on AI VO (EU) 2026/1744): Verbotene Praktiken (Art. 5) seit **02.02.2025** (zwei neue Verbote NCII/CSAM ab **02.12.2026**); KI-Kompetenz (Art. 4) seit **02.02.2025**, seit 27.07.2026 Verhaltenspflicht ("Massnahmen ergreifen"); GPAI-Pflichten Art. 51 ff. seit **02.08.2025**; **Art. 50 Transparenzpflichten seit 02.08.2026 anwendbar** (Altbestand-Nachruestung Markierung Art. 50 Abs. 2 bis **02.12.2026** gem. Art. 111 Abs. 4); Hochrisiko Anhang III **verschoben auf 02.12.2027**, Anhang I **verschoben auf 02.08.2028**.

Falls das SaaS KI-Komponenten enthaelt (LLM-Integration, Klassifikation, Empfehlungen, Generierung):

- [ ] **Verbotene Praktiken** (Art. 5) ausgeschlossen? (Social Scoring, biometrische Echtzeit-Identifizierung, manipulative Subliminal-Techniken, Emotion-Recognition am Arbeitsplatz/Bildung)
- [ ] **KI-Kompetenz** Art. 4 KI-VO n. F.: "Massnahmen ergreifen" statt Erfolgspflicht — Schulungs-/Sensibilisierungsnachweis fuer alle Mitarbeiter mit KI-Beruehrung dokumentieren (Nachweispflicht im Streitfall)
- [ ] **Risiko-Klasse** bestimmt (Verboten / Hoch / Begrenzt / Minimal)
- [ ] Bei **Limited Risk** (Chatbot, generative KI-Outputs): **Transparenzpflicht** Art. 50 AI Act
  - Nutzer-Hinweis "Sie interagieren mit einer KI" (Art. 50 Abs. 1)
  - Generierte/manipulierte Bilder, Audio, Video als KI-Output kennzeichnen — maschinenlesbares Wasserzeichen seit 02.08.2026 Pflicht (Art. 50 Abs. 2); Altbestand vor 02.08.2026 bis 02.12.2026 nachzuruesten (Art. 111 Abs. 4 i.d.F. VO (EU) 2026/1744)
  - Deepfakes klar als kuenstlich erzeugt kennzeichnen (Art. 50 Abs. 4)
- [ ] Bei **High Risk** (Anhang III: CV-Screening, Kredit-Scoring, Bildungs-Bewertung, etc., Pflichten seit Digital Omnibus erst ab **02.12.2027**; Anhang I ab **02.08.2028**): volle Konformitaetsbewertung, Risk Management System (Art. 9), Logs (Art. 12), menschliche Aufsicht (Art. 14), Daten-Governance (Art. 10) — Aufbau JETZT beginnen, nicht bis zum Geltungsdatum warten
- [ ] **GPAI-Modelle** integriert (z.B. Claude, GPT-4): Provider-Compliance-Dokumentation einholen (technische Dokumentation, Trainings-Daten-Summary)
- [ ] **Training-Daten-Rechtmaessigkeit** falls Fine-Tuning mit Nutzerdaten (explizite Einwilligung noetig)
- [ ] **Output-Verantwortlichkeit** (Halluzinationen, Bias, Diskriminierung) mit Haftungsausschluss + menschlichem Review
- [ ] **Datenschutz-Folgenabschaetzung (DSFA)** bei systematischer Bewertung von Personen (Art. 35 Abs. 3 lit. a DSGVO) — siehe [[themen/dsfa]]
- [ ] Kennzeichnung von KI-generiertem Content — siehe [[themen/ki-transparenz]] und [[themen/ki-content]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist seit **28.06.2025 in Anwendung**. Pflicht-Pruefung fuer B2C-Angebote (Online-Dienstleistungen B2C, Banking-Apps, E-Commerce, E-Books, Personenbefoerderungs-Apps, Telefondienste) sofern nicht Kleinstunternehmen-Ausnahme greift (< 10 MA UND < 2 Mio EUR Jahresumsatz/Bilanz).

- [ ] **Anwendungsbereich** geprueft (§ 1 BFSG): B2C-Online-Dienstleistung? Kleinstunternehmen-Ausnahme dokumentiert?
- [ ] **WCAG 2.1 Level AA** als Minimum (BFSGV § 3 setzt EN 301 549 um — verweist auf WCAG 2.1 AA)
- [ ] **Vier Prinzipien** wahrnehmbar / bedienbar / verstaendlich / robust (§ 4 BFSG)
- [ ] Automatisierter Scan (axe-core, Lighthouse A11y, Pa11y) — kein rotes Issue
- [ ] Manueller Test: Tastatur-Navigation, Screen-Reader (NVDA/VoiceOver/JAWS)
- [ ] **Barrierefreiheitserklaerung** auf der Website (§ 14 BFSG i.V.m. BFSGV)
- [ ] **Feedback-Mechanismus** fuer Barrieren (Kontaktformular / E-Mail)
- [ ] **Marktueberwachung** durch Bundeslaender — Verstoss kann Bussgelder bis 100.000 EUR bedeuten (§ 37 BFSG)
- [ ] Siehe [[gesetze/bfsg]] und [[themen/barrierefreiheit]]

## Pass 7: Urheber / Marken

- [ ] Alle verwendeten Bilder / Icons / Fonts mit Lizenznachweis (S3/Dropbox-Ordner "licenses/")
- [ ] Stock-Bilder: Shutterstock / Adobe Stock / Unsplash — Lizenzbedingungen eingehalten? (Unsplash erlaubt kommerziell, aber keine trademarked faces)
- [ ] **KI-generierte Bilder** (Midjourney, DALL-E, Flux) — Copyright-Frage (oft keine Schutzfaehigkeit, aber Trainingsdaten-Klagen laufen)
- [ ] Marken-Recherche fuer Produktname (DPMA, EUIPO) — siehe [[gesetze/markeng]]
- [ ] Code-Lizenzen: MIT/Apache okay; **GPL-Komponenten** beim SaaS (nur Backend) meist kein Problem, bei AGPL kritisch (Netzwerk-Freigabe-Pflicht)

## Pass 8: Logs / Retention / Loeschkonzept

- [ ] **Access Logs** — Retention max. 7-14 Tage bei IP-Logging ohne Einwilligung (Art. 6 Abs. 1 lit. f + Erwaegungsgrund 49)
- [ ] **Application Logs** — PII minimieren (IDs statt Emails), Retention max. 30-90 Tage
- [ ] **DB-Backups** — Retention max. 30 Tage (laenger nur bei begruendetem Zweck)
- [ ] **Account-Loeschung**: Klarer Ablauf nach § 35 BDSG + Art. 17 DSGVO
  - Sofort-Loeschung: Profildaten, Inhalte ohne rechtliche Aufbewahrungspflicht
  - **Anonymisierung** statt Loeschung bei Daten mit Aufbewahrungspflicht
  - **10-Jahres-Retention** fuer Rechnungs-/Handelsdaten nach § 257 HGB + § 147 AO (Rechnungen, Buchungs-Belege, Steuer-relevante Mails)
- [ ] **Retention-Tabelle** im Verarbeitungsverzeichnis dokumentiert (fuer jede Kategorie)
- [ ] **Automatisierte Loesch-Jobs** (Cron/Scheduler) mit Fehler-Alert (siehe OPS-01 Anti-Pattern in ksk-automation)
- [ ] **Data Act (EU) 2023/2854** — zeitliche Staffelung pruefen (Art. 50 i. d. F. der konsolidierten Fassung, per Cellar CELEX:32023R2854 verifiziert):
  - **Kapitel VI** (Art. 23 ff., Wechsel zwischen Datenverarbeitungsdiensten) **gilt seit 12.09.2025**. SaaS-/Cloud-Vertraege auf Pflichten zum erleichterten Anbieterwechsel pruefen (Portabilitaet, Kuendigungs- und Uebergangsfristen).
  - **Art. 29** (schrittweise Abschaffung der Wechselentgelte): vom 11.01.2024 bis **12.01.2027** nur ermaessigte Wechselentgelte (max. Selbstkosten); **ab 12.01.2027** sind Wechselentgelte vollstaendig verboten.
  - **Kapitel IV** (Art. 13, missbraeuchliche Vertragsklauseln in B2B-Datenvertraegen): gilt fuer Vertraege, die **nach dem 12. September 2025** geschlossen wurden, unmittelbar; fuer Altvertraege, die am oder vor dem 12. September 2025 geschlossen wurden, gilt Kapitel IV **ab 12. September 2027** unter der in Art. 50 genannten Voraussetzung, dass der Vertrag unbefristet ist oder seine Geltungsdauer fruehestens zehn Jahre nach dem 11. Januar 2024 endet.
  - Severity MED

## Pass 9: Social-Media & Drittinhalte

Fast jedes SaaS-Produkt hat Marketing-Teile mit Social-Media-Icons, Embeds oder Testimonials. Separat auditieren — siehe [[themen/social-media-datenschutz]].

- [ ] Social-Media-Icons im Footer / Header — **nur** als statische Links ohne Plugin-Scripts (kein Facebook-SDK, keine Twitter-Widgets)
- [ ] YouTube-/Vimeo-Embeds auf Landing / Docs nur via `youtube-nocookie.com` bzw. `?dnt=1`, alternativ hinter Consent-Gate
- [ ] LinkedIn Insight Tag / Meta Pixel / TikTok Pixel auf Marketing-Seiten mit Consent? (siehe [[themen/tracking-analytics]])
- [ ] Unternehmens-Profile (LinkedIn, X, Instagram): Impressum-Link + DSE-Link in Bio gesetzt
- [ ] Joint-Controller-Agreement mit Meta fuer Page-Insights dokumentiert

## Pass 10: Werbung mit Siegeln / Trust-Badges / Zitaten

- [ ] "Testsieger"- / "TUeV-geprueft"-Badges auf Landing: nur mit nachpruefbarem, aktuellem Siegel (OLG Frankfurt 6 U 184/13, BGH I ZR 163/19) — siehe [[themen/siegel-werbung]]
- [ ] Zitate aus Presse / Analysten-Reports: § 51 UrhG-Konformitaet (Zweck, Umfang, Quelle) — siehe [[themen/zitatrecht]]
- [ ] Kundenfotos / Mitarbeiterfotos auf Team-Seite: KUG-Einwilligung + Art. 6 DSGVO — siehe [[themen/fotos-dritter-kug]]
- [ ] Testimonial-Texte: Freigabe dokumentiert, Person tatsaechlich existierend (keine Fake-Testimonials)

## Pass 11: Live-Browser-Verhalten (Ergaenzung zum Code-Audit)

Code allein reicht nicht — laufe zusaetzlich `/legal-audit-live <production-url>` und vergleiche:

- [ ] Pre-Consent: keine Requests an `fonts.googleapis.com`, `google-analytics.com`, `facebook.com/tr`, `connect.facebook.net`, etc.
- [ ] Post-Reject: tatsaechlich KEINE Tracker (oft Bug: Banner blockt Consent-Flag, aber Scripts laden trotzdem)
- [ ] Cookie-Banner: Ablehnen gleichrangig zu Akzeptieren (visuelle Pruefung)
- [ ] Mobile-Viewport: Banner und Buttons weiterhin bedienbar
- [ ] Tool-Liste aus DSE cross-pruefen gegen tatsaechlich geladene Third-Party-Hosts — Liste siehe [[themen/tool-katalog]]

## Typ-spezifische Besonderheiten (SaaS vs. Landingpage)

- **Mehrmandanten** (Multi-Tenant): Datentrennung pro Tenant kryptografisch absichern (Row-Level Security, Schema-Isolation, Encryption-Keys)
- **Admin-Dashboards**: Access-Log wer hat auf welche Kunden-Daten zugegriffen — Art. 32 DSGVO "Integritaet und Vertraulichkeit"
- **API-Keys / Webhooks**: Geheimhaltungspflicht, Rotation, kein Logging im Klartext
- **Betroffenen-Rechte-Portal**: Self-Service fuer Auskunft (Art. 15), Loeschung (Art. 17), Datenuebertragbarkeit (Art. 20)
- **Impersonate-Feature** (Admin loggt sich als Kunde ein): Sonder-Log, Einwilligung, Missbrauchs-Sperren
- **KI-Klassifikation** auf Kunden-Inhalten (siehe ksk-automation GA-5): **DSFA zwingend**, da systematische automatisierte Bewertung

## Typische Findings (Erwartungswerte bei SaaS-Audit)

### CRIT

- AVV fehlt fuer einen oder mehrere aktive Provider
- Google Fonts / Google Maps ohne Consent im Frontend geladen (LG Muenchen I)
- Session-Cookie als "notwendig" deklariert, aber enthaelt Tracking-ID
- Account-Loeschung loescht 10-Jahre-relevante Belege (HGB-Verstoss) ODER behaelt Profildaten trotz Loesch-Anfrage
- Admin-Dashboard ohne 2FA und ohne Access-Log
- Klartext-Passwoerter in Backup oder Log

### HIGH

- Consent-Banner ohne gleichrangigen Ablehnen-Button
- Datenschutzerklaerung nennt nicht alle Drittanbieter
- PII im Sentry-Stacktrace (User-E-Mail im Breadcrumb)
- Keine DSFA bei KI-gestuetzter Nutzer-Klassifikation
- Keine Fachanwalt-Pruefung vor Launch (empfohlenes Budget 500-1.500 EUR, siehe ksk-automation GA-6)
- Sub-Prozessor-Liste im AVV nicht aktuell

### MED

- Impressum fehlt USt-ID obwohl Firma ust-pflichtig
- Cookie-Kategorie-Beschreibungen zu generisch ("Marketing-Cookies" statt konkret)
- Retention-Zeiten nicht dokumentiert (Art. 13 Abs. 2 lit. a DSGVO)
- DSB nicht benannt obwohl > 20 Personen regelmaessig mit PII arbeiten (§ 38 BDSG)
- Keine Admin-Benachrichtigung bei Cron-Job-Fehlern (OPS-01 aus ksk-automation)

### LOW

- Cookie-Icon im Footer statt oben sichtbar
- Datenschutz-Kontakt nicht als mailto-Link
- Keine separate Sprach-Versionen der DSE fuer internationale Kunden

## Referenz: Fachanwalts-Briefing

Bei Mandatierung folgendes liefern lassen:

1. **Verarbeitungsverzeichnis** (Art. 30) als Excel/Doc
2. **TOM-Dokument** (Art. 32)
3. **Alle AVVs** als PDF-Sammlung
4. **Entwurf der Datenschutzerklaerung**
5. **Entwurf der AGB**
6. **Architektur-Skizze** (Provider, Dataflows, Drittland-Marker)
7. **DSFA-Entwurf** falls KI-Kernkomponente

Budget-Range (grobe, oeffentlich kommunizierte Marktspannen; Tier-3-Marktinfo, keine belastbare Kanzlei-Preisstatistik; unverbindliche ca.-Angaben, immer individuell einholen):
- Review eines fertigen Pakets: ca. 500-1.500 EUR
- Vollstaendige Erstellung: ca. 1.500-5.000 EUR
- Laufende DSB-Funktion extern: ca. 150-500 EUR/Monat abhaengig vom Umfang

Siehe [[anwaelte-tools/fachanwaelte-it-recht]] und [[anwaelte-tools/kanzleien-saas-spezialisiert]].

## Siehe auch

- [[gesetze/dsgvo]] — Art. 6, 13, 28, 30, 32, 33, 35
- [[gesetze/bdsg]] — § 38 DSB-Pflicht
- [[gesetze/tdddg]] — § 25 Cookie-Consent
- [[gesetze/ai-act]] — Risiko-Klassen
- [[gesetze/bfsg]] — Barrierefreiheit (seit 28.06.2025 anwendbar)
- [[gesetze/bgb-agb]] — § 312j Button-Loesung
- [[gesetze/uwg]] — § 7 Direktwerbung, § 5a Werbekennzeichnung
- [[themen/verarbeitungsverzeichnis]]
- [[themen/barrierefreiheit]]
- [[themen/button-loesung]]
- [[themen/email-marketing]]
- [[themen/meldepflicht-datenpanne]]
- [[themen/tom]]
- [[themen/drittland-transfer]]
- [[themen/dsfa]]
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[themen/social-media-datenschutz]]
- [[themen/fotos-dritter-kug]]
- [[themen/siegel-werbung]]
- [[themen/zitatrecht]]
- [[themen/tool-katalog]]
- [[urteile/bgh-google-fonts]]
- [[urteile/eugh-planet49]]
- [[urteile/eugh-schrems-ii]]
- [[anwaelte-tools/fachanwaelte-it-recht]]
- [[anwaelte-tools/kanzleien-saas-spezialisiert]]

---

## Aenderungsvermerk (2026-11-14, Batch F stale-only)

- Frontmatter und Disclaimer-Stand auf 2026-11-14 aktualisiert.
- Pass 4 um Kuendigungsbutton § 312k BGB erweitert (Tier-1-belegt gegen gesetze-im-internet.de/bgb/__312k.html).
- **Pass 4 neu:** Elektronische Widerrufsfunktion nach § 356a BGB fuer B2C-Vertragsschluss ueber Online-Benutzeroberflaeche (gesetze-im-internet.de/bgb/__356a.html; RL (EU) 2023/2673 per Cellar CELEX:32023L2673 verifiziert; Anwendung ab 19.06.2026).
- Pass 8 (Data Act): Darstellung an Art. 50 VO (EU) 2023/2854 (Cellar-Volltext CELEX:32023R2854, am 2026-11-14 geprueft) angeglichen — Kapitel VI (Anbieterwechsel) gilt seit 12.09.2025, Art. 29 (Wechselentgelte) bis 12.01.2027 reduziert und danach verboten, Kapitel IV (B2B-Vertragsklauseln) fuer Neuvertraege seit 12.09.2025 und fuer Altvertraege (unbefristet oder Laufzeitende fruehestens zehn Jahre nach dem 11.01.2024) ab 12.09.2027. Die zuvor Kapitel VI pauschal zugewiesene Altvertrags-Frist war falsch zugeordnet.
- Bestandspruefung (ausserhalb Pass 5): alle Pflicht-Normzitate gegen gesetze-im-internet.de und gesetzliche Fundstellen bestaetigt — Art. 5/6/13/26/28/30/32/33/35 DSGVO, § 25 TDDDG, § 5 DDG, § 18 MStV, § 312j Abs. 2/3, § 312k, § 355, § 356 Abs. 5 BGB, §§ 305-309 BGB, § 11 PAngV, § 38 BDSG, § 51 UrhG, § 22/§ 23 KUG, § 14/§ 37 BFSG, § 257 HGB, § 147 AO, § 7 Abs. 2 Nr. 2 UWG, § 5a Abs. 4, § 5b Abs. 3 UWG. BGH I ZR 159/24 (09.10.2025), I ZR 183/22 (10.10.2024), I ZR 25/19 (13.01.2022), I ZR 91/21, I ZR 7/16, I ZR 163/19; EuGH C-673/17, C-40/17, Schrems II (C-311/18); LG Muenchen I 3 O 17493/20 — konsistent zu KB.
- Pass 5 (KI) wurde am selben Tag von einem anderen Agent aktualisiert; hier nicht angetastet.
