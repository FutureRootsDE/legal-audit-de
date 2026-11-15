---
aktualisiert: 2026-11-15
gilt-fuer: statische Marketing-Sites (Astro, Next.js-SSG, HTML, WordPress, Jekyll, Hugo)
verifiziert-am: 2026-11-14
teilverifiziert-am: 2026-11-15
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Vor Live-Gang Pruefung durch
> einen Fachanwalt fuer IT-Recht bzw. einen Datenschutzbeauftragten.
>
> **Stand:** 2026-11-14

# Audit-Checkliste: Landingpage / Marketing-Website

## Kurz-Ueberblick

Eine "Landingpage" im Rechts-Sinne ist eine oeffentlich erreichbare Website; sie unterliegt § 5 DDG, wenn geschaeftsmaessig angeboten, bzw. § 18 Abs. 1 MStV, wenn nicht ausschliesslich persoenlichen oder familiaeren Zwecken dienend, sowie bei Verarbeitung personenbezogener Daten DSGVO/TDDDG; nicht jede oeffentlich erreichbare Website ist erfasst. Typische Architekturen: Astro, Next.js-SSG, WordPress, Jekyll/Hugo, Webflow, Wix.

Im Vergleich zu SaaS: Weniger Backend-PII, aber **gleichzeitig hoeheres Tracking-/Werbekennzeichnungs-Risiko** wegen Analytics/Conversion-Pixel/Retargeting.

## Pass 1: PII-Identifikation

- [ ] Kontaktformular vorhanden? Welche Felder (Name, E-Mail, Telefon, Nachricht, Firma)?
- [ ] Newsletter-Anmeldung? Double-Opt-In korrekt (§ 7 Abs. 2 Nr. 2 UWG; BGH, Urt. v. 10.02.2011, I ZR 164/09 (Double-opt-in-Verfahren))?
- [ ] Webinar-/Event-Registrierung?
- [ ] Chat-Tool (Intercom, Tawk.to, Crisp)?
- [ ] Cookie-basiertes Tracking (GA4, GTM, Meta Pixel, TikTok Pixel, LinkedIn Insight)?
- [ ] Logs beim Hoster (IP-Retention dokumentiert?)
- [ ] Leadgen-Tools (Calendly, Typeform) mit Datenabfluss an US-Anbieter?

## Pass 2: Drittland-/Drittanbieter-Transfers

Landingpages sind der **Haupt-Angriffspunkt** in DSGVO-Abmahnungen, weil sie typisch viele Third-Party-Scripts laden.

- [ ] **Google Analytics 4** — Einwilligung zwingend (§ 25 Abs. 1 TDDDG); DPF-Status am Audittag in der DPF-Liste (dataprivacyframework.gov) pruefen
- [ ] **Google Tag Manager**: Bereits das Laden des Skripts von Google-Servern uebermittelt die IP-Adresse an Google. Rechtsgrundlage nach Art. 6 Abs. 1 DSGVO und § 25 TDDDG pruefen; im Zweifel erst nach Einwilligung oder serverseitig laden (vgl. LG Muenchen I, Endurteil vom 20.01.2022, 3 O 17493/20 (zu Google Fonts)). Ausgeloeste Tags nur nach Einwilligung
- [ ] **Meta Pixel / Conversion API** — Einwilligung; gemeinsame Verantwortlichkeit mit Meta (Art. 26 DSGVO) — **Joint Controller Agreement** (JCA) noetig
- [ ] **Google Ads Conversion**: nur nach Einwilligung (§ 25 Abs. 1 TDDDG; Art. 6 Abs. 1 lit. a DSGVO); Consent Mode v2 ist ein Google-Werkzeug zur Signaluebermittlung, keine Rechtsgrundlage
- [ ] **LinkedIn Insight Tag** — Einwilligung
- [ ] **YouTube Embed** — YouTube-Einbindung erst nach Einwilligung laden (z. B. Zwei-Klick-Loesung); der Nocookie-Modus allein genuegt nicht; Einbindung vor Einwilligung technisch pruefen
- [ ] **Google Fonts** — lokal self-hosted (LG Muenchen I 3 O 17493/20)
- [ ] **reCAPTCHA** — Einwilligung oder Wechsel zu hCaptcha (laut Anbieter US-Unternehmen Intuition Machines, Inc., Stand 2026-11-14; Drittlandtransfer pruefen) / Cloudflare Turnstile
- [ ] **Calendly / Typeform** — AVV (beide US, Calendly DPF-zertifiziert pruefen)
- [ ] **Mailchimp / ConvertKit** (Newsletter) — AVV + SCC + DPF-Pruefung
- [ ] Hoster in EU? (Hetzner, Netlify-EU-Region, Vercel mit EU-Edge)

## Pass 3: Cookie-/Consent-Analyse

Landingpages stehen im Fokus der Aufsichtsbehoerden wegen **Cookie-Banner-Mustern**.

- [ ] **Ohne Interaktion kein Tracking** (Cookie-Banner laedt NICHTS ausser sich selbst und essentielle Scripts)
- [ ] Ablehnen-Moeglichkeit auf erster Ebene, wenn das Banner Inhalte versperrt oder eine Interaktion erzwingt (DSK, OH Digitale Dienste, Rn. 124 f.; in der Praxis meist der Fall); Ablehnen als gleichwertige Alternative erkennbar, in Groesse, Farbe, Kontrast und Schriftbild vergleichbar (Rn. 135)
- [ ] Kategorien: Notwendig / Statistik / Marketing / Funktional (keine Pre-Tick)
- [ ] Widerruf per Fingertip wieder erreichbar (Floating-Button / Footer-Link "Cookie-Einstellungen")
- [ ] Einwilligung nachweisbar (Art. 7 Abs. 1 DSGVO): Consent-Log persistiert, Einwilligungsprozess und Banner-Fassungen dokumentiert
- [ ] Technisch: Banner rendert **vor** Tracking-Scripts (kein GA4 in `<head>` vor Consent)
- [ ] Mehr Details in [[themen/cookie-consent]] und [[urteile/eugh-planet49]]

## Pass 4: Pflicht-Texte

Landingpages sind hier typisch schlampig — teuerster Abmahn-Vektor.

- [ ] **Impressum** nach § 5 DDG (DDG in Kraft seit 14.05.2024, ersetzt das TMG) + § 18 MStV: Firma/Name, ladungsfaehige Anschrift (KEIN Postfach), E-Mail-Adresse und ein weiterer Weg zur schnellen unmittelbaren Kommunikation (z. B. Telefon), § 5 Abs. 1 Nr. 2 DDG, Vertretungsberechtigte, Registergericht + HRB, USt-ID, Aufsichtsbehoerde bei regulierten Berufen, journalistisch-redaktionelle Verantwortliche (bei Blog)
- [ ] **Datenschutzerklaerung** nach Art. 13 DSGVO: jede Drittanbieter-Kategorie genannt, Rechtsgrundlagen, Speicherdauer, Betroffenenrechte, Beschwerderecht an Aufsichtsbehoerde
- [ ] **Werbekennzeichnung** § 5a Abs. 4 UWG bei kommerziellen Inhalten ohne klare Werbe-Indizes
- [ ] **Barrierefreiheitserklaerung** falls B2C-Online-Dienstleistung im Anwendungsbereich des BFSG (seit 28.06.2025 anwendbar)
- [ ] **Kuendigungsbutton § 312k BGB** falls die Landingpage den Abschluss eines entgeltlichen Dauerschuldverhaeltnisses mit Verbrauchern ermoeglicht (Abo, Mitgliedschaft, SaaS-Plan): Schaltflaeche "Vertraege hier kuendigen" + Bestaetigungsseite mit "jetzt kuendigen", staendig verfuegbar; Folge bei Verstoss: jederzeitige fristlose Kuendigung (§ 312k Abs. 6 BGB) — Severity CRIT
- [ ] **Elektronische Widerrufsfunktion nach § 356a BGB** falls die Landingpage einen Verbraucher-Fernabsatzvertrag ueber eine Online-Benutzeroberflaeche ermoeglicht (nicht nur Finanzdienstleistungen): Pflichtschaltflaeche "Vertrag widerrufen" (oder eine andere gleichbedeutende eindeutige Formulierung) + Bestaetigungsschaltflaeche "Widerruf bestaetigen" (oder eine andere gleichbedeutende eindeutige Formulierung) + Eingangsbestaetigung auf dauerhaftem Datentraeger mit Datum und Uhrzeit (§ 356a Abs. 1-4 BGB; gesetze-im-internet.de/bgb/__356a.html); anzuwenden seit **19.06.2026** (Umsetzung RL (EU) 2023/2673, CELEX:32023L2673) — Severity CRIT
- [ ] Kein AGB-Pflicht bei reiner Marketing-Landingpage ohne Kaufoption

## Pass 5: KI-Spezifisch (AI Act-Stufung)

Anwendbarkeit (Stand 2026-11-14, inkl. VO (EU) 2026/1744 Digital Omnibus on AI): Verbotene Praktiken (Art. 5) seit **02.02.2025** (neue NCII/CSAM-Verbote ab 02.12.2026), KI-Kompetenz (Art. 4) seit **02.02.2025** (seit 27.07.2026 Verhaltenspflicht), GPAI-Pflichten seit **02.08.2025**, **Art. 50 Transparenz seit 02.08.2026 anwendbar** (Altbestand-Markierung bis 02.12.2026, Art. 111 Abs. 4).

- [ ] **KI-Kompetenz** Art. 4 KI-VO n. F. (seit 27.07.2026 i. d. F. VO (EU) 2026/1744): "Massnahmen ergreifen" zur Unterstuetzung der KI-Kompetenz; **keine Pflicht** zur **Garantie** eines bestimmten Niveaus (Art. 4 Abs. 1 Satz 2 n. F.) — Nachweis geeigneter Foerdermassnahmen fuer Mitarbeiter mit KI-Beruehrung dennoch dokumentieren
- [ ] KI-Chatbot eingebunden? → Art. 50 Abs. 1 AI Act Transparenzpflicht gilt seit 02.08.2026 ("Sie interagieren mit einer KI")
- [ ] KI-Text-/Bild-Generierung im Content (Blog)? → Als Betreiber Offenlegung nur bei Deepfakes (Art. 50 Abs. 4 UAbs. 1) und bei KI-Texten zu Angelegenheiten von oeffentlichem Interesse ohne menschliche Ueberpruefung und redaktionelle Verantwortung (Art. 50 Abs. 4 UAbs. 2); die Markierung nach Art. 50 Abs. 2 und Art. 111 Abs. 4 trifft den Anbieter des KI-Systems. Siehe [[themen/ki-content]] und [[themen/ki-transparenz]]
- [ ] KI-gesteuerter Produktempfehlungs-Widget? → DSFA pruefen bei Personalisierung
- [ ] [[gesetze/ai-act]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist seit **28.06.2025 in Anwendung**. Gilt fuer B2C-Online-Dienstleistungen ueber Kleinstunternehmen-Grenze (ab 10 Beschaeftigten oder Jahresumsatz und Bilanzsumme jeweils ueber 2 Mio EUR).

- [ ] **Anwendungsbereich** (§ 1 BFSG): B2C-Online-Dienstleistung? Kleinstunternehmen-Ausnahme dokumentiert?
- [ ] WCAG 2.1 AA als Pruefraster: § 3 BFSGV verweist auf den Stand der Technik; Konformitaetsvermutung nach § 4 BFSG, EN 301 549 / WCAG 2.1 AA nur darueber; Anforderungen §§ 12, 19 BFSGV
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

- [ ] Hoster-Access-Logs: Speicherdauer nach Erforderlichkeit festlegen und begruenden (Art. 5 Abs. 1 lit. e DSGVO); 7 bis 14 Tage als Praxiswert
- [ ] Form-Submissions in Admin-Panel mit Retention-Regel
- [ ] Double-Opt-In-Nachweis aufbewahren, solange die Einwilligung genutzt wird, und danach bis zum Ablauf moeglicher Anspruchsfristen (Art. 7 Abs. 1 DSGVO); keine gesetzliche Zweijahresfrist

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

- [ ] **Team-Fotos**: Einwilligung jedes Mitarbeiters (§ 22 KUG; Art. 6 Abs. 1 lit. a DSGVO); bei Beschaeftigten § 26 BDSG, Tragfaehigkeit nach EuGH C-34/21 offen
- [ ] **Ausgeschiedene Mitarbeiter**: nach Austritt Foto entfernt (Widerruf der Einwilligung)
- [ ] **Kundenzitate mit Foto**: separate Freigabe fuer Foto + Zitat, idealerweise mit Verwendungs-Scope (Website / Print / Social)
- [ ] **Stock-Testimonials** (gekaufte Fotos mit anderem Text beschriftet): Lizenzbedingungen des Bildanbieters zur Nutzung in Testimonials pruefen; Einwilligung des Abgebildeten (§ 22 KUG)
- [ ] **Team-Schnappschuesse** mit Passanten im Hintergrund: Beiwerk-Ausnahme § 23 Abs. 1 Nr. 2 KUG pruefen
- [ ] Personen der Zeitgeschichte (Gast-Speaker, Keynotes): § 23 Abs. 1 Nr. 1 KUG — Ausnahme dennoch eng auslegen

## Pass 11: Trust-Badges / Siegel / Auszeichnungen

Gerade B2C-LPs werben stark mit Siegeln — haeufig abmahnbar. Siehe [[themen/siegel-werbung]].

- [ ] "TUeV-geprueft" / "DEKRA-zertifiziert" / "ISO 27001": Siegel nur mit gueltigem, aktuellem Zertifikat; eine Pflicht, die Zertifikatsnummer zu verlinken, besteht nicht
- [ ] "Testsieger Stiftung Warentest 03/2024": Jahr + Heft angegeben, Vergleichstest-Feld erkennbar <<VERIFIKATION AUSSTEHEND>>
- [ ] Trusted Shops / eKomi / Trustpilot: Widget laedt **vor** Consent? → Finding; nach Consent erlaubt
- [ ] Branchen-Siegel / "Ausgezeichnet.org" / "ProvenExpert": Verlinkung auf Zertifizierungsseite Pflicht
- [ ] Selbst erstellte "Premium"-/"Top"-Siegel ohne externe Pruefung: irrefuehrende Werbung (§ 5 UWG)

## Pass 12: Zitate / Pressestimmen

Landingpages blenden gern "Wie in der Presse" ein — § 51 UrhG + Markenrecht kritisch. Siehe [[themen/zitatrecht]].

- [ ] Presse-Logos (FAZ, Handelsblatt, TechCrunch) mit Genehmigung oder nur als Namenszug (kein Markenlogo ohne Erlaubnis)
- [ ] Pressezitate: Quelle deutlich angeben einschliesslich des Urhebers (§ 63 UrhG); ein Datum verlangt das Gesetz nicht
- [ ] Umfang der Zitate nicht ueber das fuer Auseinandersetzung Noetige hinaus
- [ ] Hinweis "beraten von X" nur, wenn zutreffend (Irrefuehrungsverbot, § 5 UWG); Freigabe empfohlen, keine gesetzliche Schriftform

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
- GA4 oder Meta Pixel laden vor Consent (§ 25 Abs. 1 TDDDG; zur Einwilligung vgl. BGH, Urt. v. 28.05.2020, I ZR 7/16 (Cookie-Einwilligung II), Gegenstand: vorangekreuzte Checkbox)
- Impressum fehlt oder hat Postfach statt Anschrift (§ 5 DDG)
- Meta Pixel ohne Joint Controller Agreement mit Meta Platforms Ireland (Art. 26 DSGVO; vgl. EuGH, Urt. v. 29.07.2019, C-40/17 Fashion ID, zum Social Plugin: gemeinsame Verantwortung fuer Erhebung und Uebermittlung)
- Newsletter-Versand ohne nachweisbare vorherige ausdrueckliche Einwilligung (§ 7 Abs. 2 Nr. 2 UWG); fehlendes Double-Opt-In = Nachweisrisiko
- BFSG-Pflichten komplett ignoriert bei B2C-Angebot ab 10 Beschaeftigten oder Jahresumsatz und Bilanzsumme jeweils ueber 2 Mio EUR (seit 28.06.2025 anwendbar)

### HIGH

- Cookie-Banner, das Inhalte versperrt, ohne gleichwertige Ablehnen-Moeglichkeit auf erster Ebene
- Datenschutzerklaerung erwaehnt Provider nicht konkret (nur "ggf. Dritte")
- YouTube-Embed vor Einwilligung geladen (der Nocookie-Modus allein genuegt nicht)
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

---

## Aenderungsvermerk (2026-11-14, Batch F stale-only)

- Frontmatter und Disclaimer-Stand auf 2026-11-14 aktualisiert.
- Pass 4 um Kuendigungsbutton § 312k BGB erweitert (greift, wenn eine LP zu Abo-Abschluss fuehrt); Tier-1-belegt gegen gesetze-im-internet.de/bgb/__312k.html.
- **Pass 4 neu:** Elektronische Widerrufsfunktion § 356a BGB bei Landingpages mit Verbraucher-Online-Vertragsschluss (Tier-1 gesetze-im-internet.de/bgb/__356a.html; RL (EU) 2023/2673 per Cellar CELEX:32023L2673 verifiziert, Anwendung ab 19.06.2026).
- Bestandspruefung (ausserhalb Pass 5): alle Pflicht-Normzitate bestaetigt — § 5 DDG, § 18 MStV, Art. 13/26 DSGVO, § 25 TDDDG, § 7 Abs. 2 Nr. 2 UWG, § 5a Abs. 4 UWG, § 5 UWG, § 6 UWG, § 312k BGB, § 1/§ 14/§ 37 BFSG, § 22/§ 23 KUG, § 26 BDSG, § 51 UrhG, § 59 UrhG. BGH I ZR 218/07 (10.02.2011), I ZR 25/19 (13.01.2022), I ZR 91/21, I ZR 163/19; EuGH C-40/17 (Fashion ID), C-673/17 (Planet49); LG Muenchen I 3 O 17493/20 — konsistent zu KB. Keine offenen Marker in dieser Datei. Berichtigt am 2026-11-15: Diese Bestaetigung traf nicht zu. I ZR 218/07 ist kein Double-Opt-In-Urteil (richtig: I ZR 164/09 vom 10.02.2011), "I ZR 91/21" ist nicht belegt (Cookie-Einwilligung II ist I ZR 7/16 vom 28.05.2020), I ZR 25/19 betrifft Inbox-Werbung, I ZR 163/19 betrifft geografische Herkunftsangaben.
- Pass 5 (KI) wurde am selben Tag von einem anderen Agent aktualisiert; hier nicht angetastet.

## Aenderungsvermerk (2026-11-15)

- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1): Double-Opt-In mit BGH I ZR 164/09 statt I ZR 218/07, I ZR 25/19 dort gestrichen; Impressum-Kontaktangaben nach § 5 Abs. 1 Nr. 2 DDG; KI-Content: Betreiber nur Art. 50 Abs. 4, Abs. 2 trifft den Anbieter; BFSG-Schwelle und BFSGV § 3 berichtigt; Cookie-Einwilligung II ist I ZR 7/16; Newsletter-Finding auf nachweisbare Einwilligung umgestellt; I ZR 163/19 gestrichen und mit Marker versehen.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2): Landingpage-Begriff an § 5 DDG, § 18 Abs. 1 MStV angelehnt; Cookie-Banner-Ablehnoption einheitlich nach DSK, OH Digitale Dienste, Rn. 124, 125, 135 (Pruefpunkte zusammengefasst, Finding angepasst); Einwilligungsnachweis neutral nach Art. 7 Abs. 1 DSGVO; GTM, Google Ads Conversion, Fashion ID, Impressum-Datum, Team-Fotos, Pressezitate (§ 63 UrhG), Siegel und Aufbewahrungsangaben berichtigt; Widerrufsfunktion § 356a BGB auf CRIT; fluechtige Anbieterangaben (GA4, hCaptcha, Stock-Lizenzen) durch Pruefhinweise ersetzt.
