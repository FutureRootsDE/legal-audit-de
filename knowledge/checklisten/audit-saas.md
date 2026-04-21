---
aktualisiert: 2026-04-19
gilt-fuer: SaaS-Anwendungen (Next.js/React, Node/Python-Backend, PostgreSQL, Cloud-Hosting)
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Eine Pruefung durch einen
> zugelassenen Rechtsanwalt ist zwingend, bevor ein SaaS-Produkt live geht.
>
> **Stand:** 2026-04-19

# Audit-Checkliste: SaaS-Anwendung (Next.js/React)

## Kurz-Ueberblick

Diese Checkliste pruefst Du **vor jedem Production-Launch** und wiederholst sie
mindestens **halbjaehrlich**.

### Kurz-Scope

- [ ] Multi-Tenant oder Single-Tenant? (Multi-Tenant = striktere Isolierung)
- [ ] B2C, B2B oder Mixed? (BFSG gilt nur bei B2C ab 2025-06-28)
- [ ] Welche Drittlaender? (USA/UK/CH/IN — je mehr, desto komplexer)
- [ ] KI-Komponenten? (AI Act Risk-Class — Limited Risk i.d.R. = Transparenzpflicht)

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
- [ ] **Button-Loesung** "zahlungspflichtig bestellen" (§ 312j BGB) bei kostenpflichtigen Services — siehe [[themen/button-loesung]]
- [ ] **Preisangaben-Transparenz** (PAngV — Gesamtpreis inkl. USt, monatlich/jaehrlich)
- [ ] **Widerrufsrecht bei digitalen Inhalten** — Hinweis auf Verzicht moeglich (§ 356 Abs. 5 BGB)

## Pass 5: KI-Spezifisch (AI Act)

Falls das SaaS KI-Komponenten enthaelt (LLM-Integration, Klassifikation, Empfehlungen, Generierung):

- [ ] **Risiko-Klasse** bestimmt (Verboten / Hoch / Begrenzt / Minimal)
- [ ] Bei **Limited Risk** (Chatbot, generative KI-Outputs): **Transparenzpflicht** Art. 50 AI Act
  - Nutzer-Hinweis "Sie interagieren mit einer KI"
  - Generierte Bilder/Texte als KI-Output kennzeichnen (Watermark/Label)
- [ ] Bei **High Risk** (z.B. CV-Screening, Kredit-Scoring): volle Konformitaetsbewertung, Risk Management System, Logs, menschliche Aufsicht
- [ ] **Training-Daten-Rechtmaessigkeit** falls Fine-Tuning mit Nutzerdaten (explizite Einwilligung noetig)
- [ ] **Output-Verantwortlichkeit** (Halluzinationen, Bias, Diskriminierung) mit Haftungsausschluss + menschlichem Review
- [ ] **Datenschutz-Folgenabschaetzung (DSFA)** bei systematischer Bewertung von Personen (Art. 35 Abs. 3 lit. a) — siehe [[themen/dsfa]]
- [ ] Kennzeichnung von KI-generiertem Content — siehe [[themen/ki-transparenz]] und [[themen/ki-content]]

## Pass 6: Barrierefreiheit (BFSG — nur B2C ab 2025-06-28)

Falls B2C-Angebot mit > 10 MA oder > 2 Mio EUR Umsatz:

- [ ] **WCAG 2.1 Level AA** als Minimum
- [ ] Automatisierter Scan (axe-core, Lighthouse A11y) — kein rotes Issue
- [ ] Manueller Test: Tastatur-Navigation, Screen-Reader (NVDA/VoiceOver)
- [ ] **Barrierefreiheitserklaerung** auf der Website (Pflicht nach BFSG)
- [ ] **Feedback-Mechanismus** fuer Barrieren (Kontaktformular / E-Mail)
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
- [ ] **Automatisierte Loesch-Jobs** (Cron/Scheduler) mit Fehler-Alert — "stille" Cron-Fehler gefaehrden Art. 5 Abs. 1 lit. f DSGVO (Integritaet) und Art. 17 Abs. 1 (Loeschpflicht)

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
- **KI-Klassifikation** auf Kunden-Inhalten: **DSFA zwingend** (Art. 35 Abs. 3 lit. a DSGVO), da systematische automatisierte Bewertung personenbezogener Aspekte

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
- Keine Fachanwalt-Pruefung vor Launch (empfohlenes Budget 500-1.500 EUR fuer ein Review-Paket)
- Sub-Prozessor-Liste im AVV nicht aktuell

### MED

- Impressum fehlt USt-ID obwohl Firma ust-pflichtig
- Cookie-Kategorie-Beschreibungen zu generisch ("Marketing-Cookies" statt konkret)
- Retention-Zeiten nicht dokumentiert (Art. 13 Abs. 2 lit. a DSGVO)
- DSB nicht benannt obwohl > 20 Personen regelmaessig mit PII arbeiten (§ 38 BDSG)
- Keine Admin-Benachrichtigung bei Cron-Job-Fehlern ("stille Cron-Fehler" gefaehrden Datenintegritaet + Loeschpflicht)

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

Budget-Range (oeffentlich kommunizierte Marktpreise, <<UNVERIFIZIERT>> fuer konkreten Fall):
- Review eines fertigen Pakets: 500-1.500 EUR
- Vollstaendige Erstellung: 1.500-5.000 EUR
- Laufende DSB-Funktion extern: 150-500 EUR/Monat abhaengig vom Umfang

Siehe [[anwaelte-tools/fachanwaelte-it-recht]] und [[anwaelte-tools/kanzleien-saas-spezialisiert]].

## Siehe auch

- [[gesetze/dsgvo]] — Art. 6, 13, 28, 30, 32, 33, 35
- [[gesetze/bdsg]] — § 38 DSB-Pflicht
- [[gesetze/tdddg]] — § 25 Cookie-Consent
- [[gesetze/ai-act]] — Risiko-Klassen
- [[gesetze/bfsg]] — Barrierefreiheit
- [[themen/verarbeitungsverzeichnis]]
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
