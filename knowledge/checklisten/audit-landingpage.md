---
aktualisiert: 2026-05-08
gilt-fuer: statische Marketing-Sites (Astro, Next.js-SSG, HTML, WordPress, Jekyll, Hugo)
verifiziert-am: 2026-05-08
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Vor Live-Gang Pruefung durch
> einen Fachanwalt fuer IT-Recht bzw. einen Datenschutzbeauftragten.
>
> **Stand:** 2026-05-08

# Audit-Checkliste: Landingpage / Marketing-Website

## Kurz-Ueberblick

Eine "Landingpage" im Rechts-Sinne ist **jede oeffentlich erreichbare Website**, die Diensteanbieter-Informationspflichten (DDG) und Datenschutz-Pflichten (DSGVO, TDDDG) unterliegt — auch reine Marketing-/Coming-Soon-Seiten. Typische Architekturen: Astro, Next.js-SSG, WordPress, Jekyll/Hugo, Webflow, Wix.

Im Vergleich zu SaaS: Weniger Backend-PII, aber **gleichzeitig hoeheres Tracking-/Werbekennzeichnungs-Risiko** wegen Analytics/Conversion-Pixel/Retargeting.

## Pass 1: PII-Identifikation

- [ ] Kontaktformular vorhanden? Welche Felder (Name, E-Mail, Telefon, Nachricht, Firma)?
- [ ] Newsletter-Anmeldung? Double-Opt-In korrekt (§ 7 Abs. 2 Nr. 2 UWG; BGH "Double-Opt-In II" I ZR 218/07 v. 10.02.2011 zur Bestaetigungs-Mail; vgl. BGH "Inbox-Werbung II" I ZR 25/19 v. 13.01.2022)?
- [ ] Webinar-/Event-Registrierung?
- [ ] Chat-Tool (Intercom, Tawk.to, Crisp)?
- [ ] Cookie-basiertes Tracking (GA4, GTM, Meta Pixel, TikTok Pixel, LinkedIn Insight)?
- [ ] Logs beim Hoster (IP-Retention dokumentiert?)
- [ ] Leadgen-Tools (Calendly, Typeform) mit Datenabfluss an US-Anbieter?

## Pass 2: Drittland-/Drittanbieter-Transfers

Landingpages sind der **Haupt-Angriffspunkt** in DSGVO-Abmahnungen, weil sie typisch viele Third-Party-Scripts laden.

- [ ] **Google Analytics 4** — Einwilligung zwingend; IP-Anonymisierung; Consent Mode v2; DPF-zertifiziert (Google LLC)
- [ ] **Google Tag Manager** — selbst i.d.R. einwilligungsfrei fuer reinen GTM-Load, aber getriggerte Tags natuerlich consent-pflichtig
- [ ] **Meta Pixel / Conversion API** — Einwilligung; gemeinsame Verantwortlichkeit mit Meta (Art. 26 DSGVO) — **Joint Controller Agreement** (JCA) noetig
- [ ] **Google Ads Conversion** — ueber Consent Mode v2 konfigurieren
- [ ] **LinkedIn Insight Tag** — Einwilligung
- [ ] **YouTube Embed** — nano-cookie-free via youtube-nocookie.com; oder Consent
- [ ] **Google Fonts** — lokal self-hosted (LG Muenchen I 3 O 17493/20)
- [ ] **reCAPTCHA** — Einwilligung oder Wechsel zu hCaptcha (EU-Anbieter) / Cloudflare Turnstile
- [ ] **Calendly / Typeform** — AVV (beide US, Calendly DPF-zertifiziert pruefen)
- [ ] **Mailchimp / ConvertKit** (Newsletter) — AVV + SCC + DPF-Pruefung
- [ ] Hoster in EU? (Hetzner, Netlify-EU-Region, Vercel mit EU-Edge)

## Pass 3: Cookie-/Consent-Analyse

Landingpages stehen im Fokus der Aufsichtsbehoerden wegen **Cookie-Banner-Mustern**.

- [ ] **Ohne Interaktion kein Tracking** (Cookie-Banner laedt NICHTS ausser sich selbst und essentielle Scripts)
- [ ] "Ablehnen" **gleichrangig** zu "Akzeptieren" (gleiche Farbe, gleiche Position-Prominenz)
- [ ] Kein "Alle akzeptieren" ohne Gegen-Button auf oberster Ebene
- [ ] Kategorien: Notwendig / Statistik / Marketing / Funktional (keine Pre-Tick)
- [ ] Widerruf per Fingertip wieder erreichbar (Floating-Button / Footer-Link "Cookie-Einstellungen")
- [ ] **Consent-Log** persistiert (Server oder IndexedDB mit TTL)
- [ ] Technisch: Banner rendert **vor** Tracking-Scripts (kein GA4 in `<head>` vor Consent)
- [ ] Mehr Details in [[themen/cookie-consent]] und [[urteile/eugh-planet49]]

## Pass 4: Pflicht-Texte

Landingpages sind hier typisch schlampig — teuerster Abmahn-Vektor.

- [ ] **Impressum** nach § 5 DDG (geaendert 14.05.2024 — DDG ersetzt TMG) + § 18 MStV: Firma/Name, ladungsfaehige Anschrift (KEIN Postfach), Kontakt (Telefon + E-Mail), Vertretungsberechtigte, Registergericht + HRB, USt-ID, Aufsichtsbehoerde bei regulierten Berufen, journalistisch-redaktionelle Verantwortliche (bei Blog)
- [ ] **Datenschutzerklaerung** nach Art. 13 DSGVO: jede Drittanbieter-Kategorie genannt, Rechtsgrundlagen, Speicherdauer, Betroffenenrechte, Beschwerderecht an Aufsichtsbehoerde
- [ ] **Werbekennzeichnung** § 5a Abs. 4 UWG bei kommerziellen Inhalten ohne klare Werbe-Indizes
- [ ] **Barrierefreiheitserklaerung** falls B2C-Online-Dienstleistung im Anwendungsbereich des BFSG (seit 28.06.2025 anwendbar)
- [ ] Kein AGB-Pflicht bei reiner Marketing-Landingpage ohne Kaufoption

## Pass 5: KI-Spezifisch (AI Act-Stufung)

Anwendbarkeit: Verbotene Praktiken (Art. 5) seit **02.02.2025**, KI-Kompetenz (Art. 4) seit **02.02.2025**, GPAI-Pflichten seit **02.08.2025**, Vollanwendung ab **02.08.2026**.

- [ ] **KI-Kompetenz** Art. 4 AI Act: Schulungs-/Sensibilisierungsnachweis fuer Mitarbeiter mit KI-Beruehrung
- [ ] KI-Chatbot eingebunden? → Art. 50 Abs. 1 AI Act Transparenzpflicht ("Sie interagieren mit einer KI")
- [ ] KI-Text-/Bild-Generierung im Content (Blog)? → Kennzeichnung als KI-Content (Art. 50 Abs. 2; ab 02.08.2026 Wasserzeichen-Pflicht) — siehe [[themen/ki-content]] und [[themen/ki-transparenz]]
- [ ] KI-gesteuerter Produktempfehlungs-Widget? → DSFA pruefen bei Personalisierung
- [ ] [[gesetze/ai-act]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist seit **28.06.2025 in Anwendung**. Gilt fuer B2C-Online-Dienstleistungen ueber Kleinstunternehmen-Grenze (>= 10 MA ODER >= 2 Mio EUR Jahresumsatz/Bilanzsumme).

- [ ] **Anwendungsbereich** (§ 1 BFSG): B2C-Online-Dienstleistung? Kleinstunternehmen-Ausnahme dokumentiert?
- [ ] WCAG 2.1 AA als Standard (BFSGV § 3 setzt EN 301 549 um)
- [ ] Farbkontrast, Alt-Texte, Keyboard-Navigation, Screen-Reader (NVDA/JAWS/VoiceOver)
- [ ] **Barrierefreiheitserklaerung** veroeffentlicht (§ 14 BFSG)
- [ ] Feedback-Kanal fuer Barrieren
- [ ] Marktueberwachung Bundeslaender — Bussgeldrahmen bis 100.000 EUR (§ 37 BFSG)
- [ ] [[gesetze/bfsg]], [[themen/barrierefreiheit]]

## Pass 7: Urheber / Marken

- [ ] Alle Hero-Images: Lizenz dokumentiert (Shutterstock / Unsplash / Eigenproduktion)
- [ ] Icons (Font Awesome Pro / Heroicons / custom): Lizenzbedingungen im LICENSES.md
- [ ] Fonts: Webfont-Lizenz (nicht Google Fonts CDN — lokal via @font-face)
- [ ] Logos verwendeter Tools/Partner: Nutzungsrecht geklaert (explizite Erlaubnis oder Press-Kit)
- [ ] Testimonials/Kundenzitate: schriftliche Freigabe vorhanden
- [ ] Wettbewerber in Texten genannt? Vergleichende Werbung nach § 6 UWG zulaessig, aber Grenzen (keine Verunglimpfung)
- [ ] [[themen/urheber-stockfoto]], [[gesetze/urhg]], [[gesetze/markeng]]

## Pass 8: Logs / Retention

- [ ] Hoster-Access-Logs max. 7-14 Tage
- [ ] Form-Submissions in Admin-Panel mit Retention-Regel
- [ ] Newsletter-Double-Opt-In-Bestaetigungs-Mail min. 2 Jahre archivieren (Nachweis fuer Abmahnschutz!)

## Pass 9: Social-Media / Plugins / Embeds

Landingpages sind der haeufigste Plugin-Fundort — hier passiert Fashion-ID-Risiko (EuGH C-40/17) in Reinkultur. Details siehe [[themen/social-media-datenschutz]].

- [ ] Facebook-/Instagram-/LinkedIn-/X-Icons: **nur** statische Links (kein Facebook-SDK, keine Twitter-Widgets, keine LinkedIn-Plugins)
- [ ] Falls Social-Sharing: **Shariff**-Loesung oder 2-Klick-Aktivierung
- [ ] YouTube-Embed: `youtube-nocookie.com` + Consent-Gate
- [ ] Vimeo-Embed: `?dnt=1` + Consent
- [ ] Instagram-Feed-Widget: serverseitiger Proxy oder Consent-Gate (Live-Embed blockt vor Consent)
- [ ] Twitter-Blockquote-Embed via `platform.twitter.com` → Consent-pflichtig
- [ ] "Linktree"-aehnliche Bio-Profile auf Social: Impressum + DSE verlinkt
- [ ] Meta-Pixel / LinkedIn Insight Tag / TikTok Pixel auf LP nur nach Consent (siehe Pass 2)

## Pass 10: Fotos / Testimonials / Persoenlichkeitsrechte

Auf Landingpages stehen Team-, Kunden- und Testimonial-Fotos im Mittelpunkt — hohes Abmahnrisiko. Siehe [[themen/fotos-dritter-kug]].

- [ ] **Team-Fotos**: schriftliche Einwilligung jedes Mitarbeiters (Art. 6 DSGVO lit. a + § 22 KUG, bei Beschaeftigten auch § 26 BDSG)
- [ ] **Ausgeschiedene Mitarbeiter**: nach Austritt Foto entfernt (Widerruf der Einwilligung)
- [ ] **Kundenzitate mit Foto**: separate Freigabe fuer Foto + Zitat, idealerweise mit Verwendungs-Scope (Website / Print / Social)
- [ ] **Stock-Testimonials** (gekaufte Fotos mit anderem Text beschriftet): Model-Release pruefen — viele Stock-Lizenzen verbieten "endorsement"-Kontext
- [ ] **Team-Schnappschuesse** mit Passanten im Hintergrund: Beiwerk-Ausnahme § 23 Abs. 1 Nr. 2 KUG pruefen
- [ ] Personen der Zeitgeschichte (Gast-Speaker, Keynotes): § 23 Abs. 1 Nr. 1 KUG — Ausnahme dennoch eng auslegen

## Pass 11: Trust-Badges / Siegel / Auszeichnungen

Gerade B2C-LPs werben stark mit Siegeln — haeufig abmahnbar. Siehe [[themen/siegel-werbung]].

- [ ] "TUeV-geprueft" / "DEKRA-zertifiziert" / "ISO 27001": Siegel **aktuell** (nicht abgelaufen), pruefbare Zertifikat-Nummer verlinkt
- [ ] "Testsieger Stiftung Warentest 03/2024": Jahr + Heft angegeben, Vergleichstest-Feld erkennbar (BGH I ZR 163/19)
- [ ] Trusted Shops / eKomi / Trustpilot: Widget laedt **vor** Consent? → Finding; nach Consent erlaubt
- [ ] Branchen-Siegel / "Ausgezeichnet.org" / "ProvenExpert": Verlinkung auf Zertifizierungsseite Pflicht
- [ ] Selbst erstellte "Premium"-/"Top"-Siegel ohne externe Pruefung: irrefuehrende Werbung (§ 5 UWG)

## Pass 12: Zitate / Pressestimmen

Landingpages blenden gern "Wie in der Presse" ein — § 51 UrhG + Markenrecht kritisch. Siehe [[themen/zitatrecht]].

- [ ] Presse-Logos (FAZ, Handelsblatt, TechCrunch) mit Genehmigung oder nur als Namenszug (kein Markenlogo ohne Erlaubnis)
- [ ] Pressezitate: Quellenangabe Pflicht (Autor, Medium, Datum)
- [ ] Umfang der Zitate nicht ueber das fuer Auseinandersetzung Noetige hinaus
- [ ] "Als vom X. beraten"-Hinweis nur mit schriftlicher Freigabe der genannten Partner

## Pass 13: Live-Browser-Verhalten

`/legal-audit-live <url>` ist fuer Landingpages PFLICHT vor Live-Gang, nicht nur Code-Scan:

- [ ] Pre-Consent-Pass: keine Requests an bekannte Tracker (Liste siehe [[themen/tool-katalog]])
- [ ] Google Fonts direkt via `fonts.googleapis.com`? → CRIT
- [ ] Post-Reject-Pass: nach "Ablehnen" tatsaechlich keine Analytics/Pixel-Requests
- [ ] Post-Accept-Pass: nur Tools laden, die in DSE genannt sind
- [ ] Mobile-Viewport: Banner + Ablehnen-Button weiterhin erreichbar

## Typ-spezifische Besonderheiten

- **Coming-Soon-Page mit Newsletter-Collect**: Minimal-Impressum + Minimal-DSE + Double-Opt-In reicht
- **Multi-Page-Marketing-Site**: Cookie-Banner auf allen Seiten identisch; Consent-Status cross-page persistent
- **WordPress-Landingpage**: Plugin-Ecosystem pruefen (Yoast SEO sendet optional Telemetrie, Elementor ebenso)
- **Jamstack / Static**: Meistens wenig Backend, aber Form-Provider (Netlify Forms, Formspree) = Drittland-Pruefung!
- **Headless CMS** (Contentful, Sanity, Storyblok): AVV pruefen, Admin-Zugang absichern

## Typische Findings

### CRIT

- Google Fonts direkt via fonts.googleapis.com (ohne Consent, ohne Self-Hosting; LG Muenchen I 3 O 17493/20)
- GA4 oder Meta Pixel laden vor Consent (BGH I ZR 91/21 "Cookie-Einwilligung II")
- Impressum fehlt oder hat Postfach statt Anschrift (§ 5 DDG)
- Meta Pixel ohne Joint Controller Agreement mit Meta Platforms Ireland (Art. 26 DSGVO; EuGH C-40/17 Fashion ID)
- Newsletter ohne Double-Opt-In — Verstoss gegen § 7 Abs. 2 Nr. 2 UWG
- BFSG-Pflichten komplett ignoriert bei B2C-Angebot mit > 10 MA (seit 28.06.2025 anwendbar)

### HIGH

- Cookie-Banner ohne Ablehnen-Button auf oberster Ebene
- Datenschutzerklaerung erwaehnt Provider nicht konkret (nur "ggf. Dritte")
- YouTube-Embed ohne Consent oder ohne Nocookie-Domain
- reCAPTCHA v3 ohne Consent (laedt Google-Scripts)
- Formular-Daten gehen per HTTP POST ueber US-Service ohne AVV

### MED

- Alt-Texte fehlen (BFSG bei B2C HIGH, sonst MED)
- Kontaktformular sendet Plaintext-Mail (Verschluesselung empfohlen)
- Keine Double-Opt-In-Bestaetigungsmail archiviert

### LOW

- Impressum-Link nicht im sichtbaren Bereich der Haupt-Navigation
- DSE-Sprache veraltet (zitiert BDSG-alt statt BDSG-neu)

## Siehe auch

- [[gesetze/dsgvo]]
- [[gesetze/tdddg]] — § 25 Cookies
- [[gesetze/ddg]] — § 5 Impressum (DDG ersetzt TMG seit 14.05.2024)
- [[gesetze/uwg]] — § 7 Direktmarketing, § 5a Werbekennzeichnung
- [[gesetze/bfsg]] — seit 28.06.2025 anwendbar
- [[gesetze/ai-act]]
- [[themen/impressum]]
- [[themen/barrierefreiheit]]
- [[themen/ki-transparenz]]
- [[urteile/bgh-cookie-einwilligung]]
- [[themen/datenschutzerklaerung]]
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[themen/email-marketing]]
- [[themen/werbekennzeichnung]]
- [[themen/social-media-datenschutz]]
- [[themen/fotos-dritter-kug]]
- [[themen/siegel-werbung]]
- [[themen/zitatrecht]]
- [[themen/tool-katalog]]
- [[urteile/bgh-google-fonts]]
- [[urteile/eugh-planet49]]
- [[urteile/bgh-inbox-werbung]]
