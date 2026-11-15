---
aktualisiert: 2026-11-15
gilt-fuer: Blog, Corporate-Blog, YouTube-Channel, Podcast, Social-Media-Content, Newsletter
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Content-Produktion ist
> urheberrechts-, wettbewerbs- und werbekennzeichnungsrechtlich anspruchsvoll.
>
> **Stand:** 2026-11-14

# Audit-Checkliste: Content / Blog / YouTube / Podcast

## Kurz-Ueberblick

Content-Produktion beruehrt:
1. **UrhG** — Zitat-Recht, Bildrechte, Musik-Lizenzen
2. **UWG** — Schleichwerbung, Influencer-Werbekennzeichnung
3. **MStV § 18** — Impressum fuer journalistisch-redaktionelle Telemedien
4. **DSGVO** — wenn erkennbare Personen gezeigt werden (KUG + Art. 6 DSGVO)
5. **AI Act** — bei KI-generierten Inhalten
6. **JMStV** — Jugendmedienschutz (u. a. entwicklungsbeeintraechtigende Angebote § 5 JMStV; v. a. YouTube)

## Pass 1: PII-Identifikation (Personen im Content)

- [ ] Erkennbare Personen im Bild-/Video-Material?
  - Einwilligung nach § 22 Satz 1 KUG dokumentiert (Model Release); datenschutzrechtliche Rechtsgrundlage nach Art. 6 Abs. 1 DSGVO festgelegt, bei Einwilligung (lit. a) nachweisbar (Art. 7 Abs. 1 DSGVO)
  - Ausnahmen § 23 KUG: Personen der Zeitgeschichte, Beiwerk, Versammlungen — dennoch DSGVO pruefen
  - Details und Muster-Freigabe siehe [[themen/fotos-dritter-kug]]
- [ ] Stimmen im Podcast identifizierbar? Gast-Einwilligung schriftlich
- [ ] Interviews: Freigabe vor Veroeffentlichung vereinbaren und dokumentieren (keine gesetzliche Gegenlese-/Autorisierungspflicht; ein AVV regelt dies nicht)
- [ ] Kommentarfunktion / User-Generated-Content → DSGVO-Pflichten fuer User-Daten
- [ ] Newsletter-Verteiler / Podcast-Hosting-Analytics (Spotify, Apple Podcasts)

## Pass 2: Drittland-/Drittanbieter-Transfers

- [ ] **YouTube** — bei eigener Einbettung auf Website: Einbindung vor Einwilligung technisch pruefen (Consent oder YT-Nocookie)
- [ ] **Spotify for Podcasters / Podigee / Libsyn** — Podcast-Hosting mit Analytics
- [ ] **Apple Podcasts Analytics** — Daten-Austausch mit Apple
- [ ] **Transcription-Services** (Whisper-API, Descript, Rev) — PII in Transkripten
- [ ] **Newsletter-Tools** (Substack, Buttondown, Brevo, Mailchimp) — AVV + ggf. SCC/DPF
- [ ] **Video-Hosting** (Vimeo, Mux) — AVV
- [ ] **Social-Media-APIs** (Meta Graph API, X API, TikTok API, LinkedIn API) — Drittland

## Pass 3: Cookie-/Consent-Analyse

- [ ] YouTube-Embed mit Consent (Einbindung vor Einwilligung technisch pruefen, auch bei youtube-nocookie.com)
- [ ] Spotify-Player-Embed mit Consent
- [ ] Kommentar-Systeme (Disqus, Giscus): Einbindung vor Einwilligung technisch pruefen
- [ ] Social-Share-Buttons nur als statische Links, nicht als iframes (Shariff-Loesung)
- [ ] Newsletter-Anmeldeformular: Double-Opt-In + Checkbox fuer DSE

## Pass 4: Pflicht-Texte

### Impressum bei journalistisch-redaktionellen Angeboten

- [ ] **§ 5 DDG** + **§ 18 Abs. 2 MStV** — zusaetzlich **"Verantwortlicher im Sinne des § 18 Abs. 2 MStV"** mit Namen + Anschrift
- [ ] Fuer Blogs mit regelmaessiger journalistischer Berichterstattung verpflichtend
- [ ] YouTube-Kanal-Impressum: ueber Kanal-Links setzen (Pflicht!)
- [ ] Podcast: im RSS-Feed (iTunes-Tags) oder Show-Notes verlinkt
- [ ] Auf allen Social-Media-Profilen (Instagram, TikTok, X/Twitter) Link zum Impressum

### Datenschutzerklaerung

- [ ] Abschnitt fuer Kommentar-Funktion
- [ ] Abschnitt fuer Newsletter
- [ ] Abschnitt fuer Social-Media-Plugins / Embeds
- [ ] Speicherdauer von User-Beitraegen transparent

### Werbekennzeichnung

- [ ] **§ 5a Abs. 4 UWG** + **§ 22 MStV**: kommerziellen Zweck kenntlich machen, z. B. als **"Werbung"** / **"Anzeige"** / **"bezahlte Partnerschaft"**. Bei Handlungen zugunsten eines fremden Unternehmens liegt ein kommerzieller Zweck nicht vor, wenn der Handelnde kein Entgelt und keine aehnliche Gegenleistung erhaelt oder sich versprechen laesst; die Gegenleistung wird vermutet, es sei denn, er macht glaubhaft, dass er keine erhalten hat (§ 5a Abs. 4 Saetze 2 und 3 UWG). Eigenwerbung ist regelmaessig eine geschaeftliche Handlung zugunsten des eigenen Unternehmens. Die BGH-Urteile vom 09.09.2021 (I ZR 90/20, I ZR 125/20, I ZR 126/20) ergingen zu § 5a Abs. 6 UWG a. F.; Einordnung siehe [[themen/werbekennzeichnung]]
- [ ] Affiliate-Links → Kennzeichnung als solche (auch wenn nicht bezahlt, aber Provisionsbasiert)
- [ ] Pressemuster / PR-Samples → Offenlegung ("PR-Sample", "kostenlos erhalten")
- [ ] YouTube: zusaetzlich "Paid Promotion"-Toggle von Google aktivieren (nicht statt, sondern zusaetzlich)
- [ ] Instagram: "Bezahlte Partnerschaft mit [Marke]" aktivieren + im Post-Text nochmal "Werbung" / "Anzeige"
- [ ] [[themen/werbekennzeichnung]], [[gesetze/uwg]]

## Pass 5: KI-Spezifisch (AI Act-Stufung)

Anwendbarkeit (Stand 2026-11-14, inkl. VO (EU) 2026/1744 Digital Omnibus on AI): Verbotene Praktiken (Art. 5) und KI-Kompetenz (Art. 4) seit **02.02.2025** (Art. 4 seit 27.07.2026 Verhaltenspflicht; zwei neue Verbote NCII/CSAM ab 02.12.2026), GPAI-Pflichten seit **02.08.2025**, **Art. 50 (Transparenz) seit 02.08.2026 anwendbar** mit maschinenlesbarer Markierung (Altbestand vor 02.08.2026 nachzuruesten bis 02.12.2026, Art. 111 Abs. 4).

- [ ] **KI-Kompetenz** Art. 4 KI-VO n. F. (seit 27.07.2026 i. d. F. VO (EU) 2026/1744): "Massnahmen ergreifen" zur Unterstuetzung der KI-Kompetenz; **keine Pflicht** zur **Garantie** eines bestimmten Niveaus (Art. 4 Abs. 1 Satz 2 n. F.) — Nachweis geeigneter Foerdermassnahmen fuer alle Redakteure mit KI-Einsatz dennoch dokumentieren
- [ ] **KI-generierter Text** zu Angelegenheiten von oeffentlichem Interesse → Offenlegungspflicht nach Art. 50 Abs. 4 UAbs. 2 KI-VO; Ausnahme nur, wenn der Text einer menschlichen Ueberpruefung oder redaktionellen Kontrolle unterzogen wurde und eine natuerliche oder juristische Person die redaktionelle Verantwortung traegt
- [ ] **KI-generierter Text** sonstig → Kennzeichnung empfohlen ("Dieser Artikel wurde mit Unterstuetzung von KI erstellt")
- [ ] **KI-generierte Bilder/Audio/Video** im Artikel → Als Betreiber Offenlegungspflicht nur bei Deepfakes (Art. 50 Abs. 4 UAbs. 1 AI Act); sonst Kennzeichnung empfohlen. Die maschinenlesbare Markierung nach Art. 50 Abs. 2 AI Act trifft den Anbieter des KI-Systems
- [ ] **KI-Stimmen** im Podcast → Offenlegungspflicht nur, wenn es sich um einen Deepfake handelt (Art. 50 Abs. 4 UAbs. 1 AI Act); sonst Kennzeichnung empfohlen
- [ ] **Deepfakes** von realen Personen → zwingend als kuenstlich erzeugt kennzeichnen (Art. 50 Abs. 4 AI Act) UND Einwilligung der Person noetig (Persoenlichkeitsrecht / KUG)
- [ ] **Synthetische Avatare** als Sprecher: Offenlegungspflicht nur, wenn der Avatar ein Deepfake ist (Art. 50 Abs. 4 UAbs. 1 i. V. m. Art. 3 Nr. 60 KI-VO) oder bei direkter Interaktion (Art. 50 Abs. 1); sonst Kennzeichnung empfohlen
- [ ] **Verbotene Praktiken** Art. 5: keine manipulativen Subliminal-Techniken, kein Social-Scoring-Content
- [ ] [[gesetze/ai-act]], [[themen/ki-content]], [[themen/ki-transparenz]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist seit **28.06.2025 in Anwendung**. Reine redaktionelle Inhalte sind oft nicht direkter BFSG-Anwendungsbereich (siehe Ausnahmen § 1 Abs. 4 BFSG fuer Medieninhalte; neue Videos und Podcasts sind davon nicht ausgenommen), aber **kommerzielle Content-Sites mit Newsletter-Verkauf, Online-Kurs-Verkauf, Webshops** sind erfasst.

- [ ] **Anwendungsbereich** § 1 BFSG geprueft
- [ ] YouTube: **Untertitel** (automatisch + korrigiert) fuer alle Videos
- [ ] Podcast: **Transkripte** als PDF/HTML bereitstellen
- [ ] Blog: WCAG 2.1 AA — Kontraste, Alt-Texte, Tastaturnavigation
- [ ] **Barrierefreiheitserklaerung** wenn BFSG-pflichtig (§ 14 BFSG)
- [ ] [[gesetze/bfsg]], [[themen/barrierefreiheit]]

## Pass 7: Urheber / Marken (Hot-Zone!)

### Bild- und Video-Material

- [ ] **Eigene Aufnahmen**: Model-Release-Formular (Einwilligung Person, Nutzungsrechte)
- [ ] **Stock-Bilder**: Shutterstock, Adobe Stock, Getty — Lizenz-ID im CMS hinterlegt, Lizenzbedingungen des Anbieters pruefen
- [ ] **Creative Commons**: Lizenz korrekt zitieren (CC-BY bedeutet Namensnennung!)
- [ ] **Unsplash**: Lizenzbedingungen des Anbieters pruefen
- [ ] **Screenshots** fremder Websites: nur mit Zitatzweck zulaessig, Umfang durch den Zweck gerechtfertigt (§ 51 Satz 1 und 3 UrhG), Quellenangabe (§ 63 UrhG); Logos zusaetzlich markenrechtlich pruefen
- [ ] **Panoramafreiheit** bei Architektur (§ 59 UrhG) — nur oeffentlicher Raum, nicht Innenraeume
- [ ] **KI-generierte Bilder**: ohne persoenliche geistige Schoepfung kein Werk (§ 2 Abs. 2 UrhG); ein Stil als solcher ist nicht geschuetzt; Risiko bei Uebernahme konkreter geschuetzter Werke oder Werkteile (§ 23 UrhG)

### Musik (kritisch bei YouTube/Podcast!)

- [ ] **GEMA-Lizenz** bei deutscher/europaeischer Musik
- [ ] **YouTube Audio Library**: Lizenzbedingungen des Anbieters pruefen (Nutzungsumfang)
- [ ] **Epidemic Sound / Artlist / Soundstripe** — Lizenzbedingungen des Anbieters pruefen, Lizenz dokumentieren
- [ ] **Podcast**: GEMA-Musik braucht eine Lizenz (GEMA-Tarif VR-OD 14 (Podcasts), laut GEMA, Stand 2026-11-14)
- [ ] **Copyright-Claims** auf YouTube: Monitoring + Streitverfahren-Kenntnis
- [ ] **KI-generierte Musik** (Suno, Udio, Mubert): Lizenz-Status pruefen; erste deutsche Entscheidung zu KI-Training und Ausgabe geschuetzter Liedtexte: LG Muenchen I, Urt. v. 11.11.2025, 42 O 14139/24 (GEMA gegen OpenAI), laut Pressemitteilung des Gerichts; weitere Verfahren anhaengig

### Text-Zitate

- [ ] **§ 51 UrhG Zitatrecht**: Zweck (Auseinandersetzung), Umfang (nicht laenger als noetig), Quellenangabe — Detail-Pruefung siehe [[themen/zitatrecht]]
- [ ] **Keine ueber-weiten "Zitate"** (ganze Absaetze ohne erkennbare Auseinandersetzung)
- [ ] **Bildzitate** (Screenshots, Memes): Zitatzweck + unveraenderte Uebernahme + Quelle
- [ ] **Presseveroeffentlichungs-Recht** (§ 87f ff. UrhG) — bei News-Aggregation kritisch

### Marken

- [ ] Eigener Kanal-Name / Brand auf Marken-Verletzung gepruefta (DPMA, EUIPO, WIPO)
- [ ] Fremde Marken nur als Nennung (keine suggestive Assoziation/Verwechslungsgefahr)
- [ ] Merchandising mit Marken-Bezug = Lizenz noetig (Panini, etc.)

## Pass 8: Logs / Retention

- [ ] Blog-Kommentare: Retention-Regel (z.B. Loeschung bei User-Anfrage, sonst unbegrenzt)
- [ ] Newsletter-Verteiler: nach Abmeldung keine Werbung mehr (Art. 7 Abs. 3, Art. 21 Abs. 3 DSGVO); Einwilligungsnachweis (Double-Opt-In) aufbewahren, solange die Einwilligung genutzt wird, und danach bis zum Ablauf moeglicher Anspruchsfristen (Art. 7 Abs. 1 DSGVO); keine gesetzliche Zweijahresfrist
- [ ] YouTube-Analytics-Daten: bei Google gespeichert, eigene Retention nur in Exports
- [ ] Podcast-Analytics: beim Hoster

## Pass 9: Siegel / Auszeichnungen im Content

Bei Produkttests, Review-Blogs, Affiliate-Content tauchen oft Siegel auf — Vorsicht bei irrefuehrender Darstellung. Siehe [[themen/siegel-werbung]].

- [ ] "Redaktions-Testsieger"-Label: eigene Test-Kriterien transparent offenlegen
- [ ] "Von uns empfohlen": keine wirtschaftliche Beziehung verschwiegen (§ 5a UWG)
- [ ] Fremde Testsieger-Logos (Stiftung Warentest, ÖKO-TEST): Lizenz haben oder weglassen
- [ ] Affiliate-Partner-Badges: Werbekennzeichnung parallel (Pass 4)

## Pass 10: Social-Media-Profile des Kanals

Neben eigener Website: jedes Social-Profil ist eigenstaendiges Telemedium. Siehe [[themen/social-media-datenschutz]].

- [ ] Instagram / TikTok / X / LinkedIn / YouTube: Impressum-Link in Bio / Info / Kanal-Details
- [ ] DSE-Link ebenfalls verlinkt (Joint-Controller-Info mit Plattform)
- [ ] Bei automatisiertem Crossposting (n8n, Zapier): Hinweis nach § 18 Abs. 3 MStV ("automatisiert erstellt"), wenn das Nutzerkonto seinem aeusseren Erscheinungsbild nach fuer die Nutzung durch natuerliche Personen bereitgestellt wurde
- [ ] Eingebettete Posts auf eigenem Blog (Twitter-Blockquote, Instagram-Embed): 2-Klick-Loesung oder Consent-Gate

## Pass 11: Live-Browser-Check

`/legal-audit-live <blog-url>` ergaenzt den Code-Scan:

- [ ] Embeds (YouTube, Spotify, Twitter, Instagram) laden **vor** Consent? → CRIT
- [ ] Comment-System (Disqus) laedt Google-/FB-Scripts vor Consent
- [ ] Newsletter-Pop-up (Sumo, OptinMonster): DSE-Link sichtbar, DOI-Pflicht umgesetzt
- [ ] Tool-Katalog [[themen/tool-katalog]] fuer vollstaendige Tracker-Liste

## Spezifisches nach Plattform

### YouTube

- [ ] Kanal-Impressum unter "Details" hinterlegt (Pflicht!)
- [ ] Community-Guidelines eingehalten
- [ ] Altersbeschraenkungen korrekt gesetzt
- [ ] Bei "gemacht fuer Kinder": YouTube-Einstellung korrekt setzen (COPPA ist US-Recht); fuer DE/EU massgeblich Art. 8 DSGVO und § 5 JMStV
- [ ] Paid Promotion korrekt deklariert
- [ ] Musik aus YT Audio Library oder mit Lizenz

### Podcast

- [ ] ID3-Tags im MP3 mit Urheber, Copyright
- [ ] RSS-Feed valide (Impressum-Link, Copyright-Tag)
- [ ] Shownotes mit Quellenangaben
- [ ] Bei Co-Host / Gaesten: Splittung Urheberrechte klaeren

### Newsletter

- [ ] Double-Opt-In mit Bestaetigungs-Mail (BGH, Urt. v. 10.02.2011, I ZR 164/09 (Double-opt-in-Verfahren))
- [ ] Abmelde-Link in JEDER Mail (§ 7 Abs. 2 Nr. 3 Buchst. c UWG i.V.m. Abs. 3 — bei Bestandskundenausnahme)
- [ ] Absenderidentitaet in jeder Mail erkennbar (§ 6 Abs. 1 DDG, § 7 Abs. 2 Nr. 3 UWG)
- [ ] Personalisierung nur nach Einwilligung
- [ ] BGH "Inbox-Werbung II" I ZR 25/19 (13.01.2022) — Inbox-Werbung in E-Mail-Postfaechern bedarf Einwilligung
- [ ] **Paid Newsletter / Abo-Modell**: Kuendigungsschaltflaeche § 312k BGB (Wortlaut "Vertraege hier kuendigen" + "jetzt kuendigen" auf Bestaetigungsseite, staendig verfuegbar; Folge bei Verstoss: fristlose Kuendigung jederzeit, § 312k Abs. 6 BGB) — Severity CRIT
- [ ] [[themen/email-marketing]], [[urteile/bgh-inbox-werbung]], [[gesetze/uwg]]

### Social Media

- [ ] Plattform-AGB einhalten (Meta, TikTok, X)
- [ ] Keine trademarked Hashtags als Post-Marker
- [ ] **Jede Plattform** eigenes Impressum / "Link in Bio"
- [ ] User-Reaktionen moderieren bei beleidigenden Kommentaren — **DSA** Verordnung (EU) 2022/2065 vollanwendbar seit 17.02.2024 (NetzDG besteht fort: §§ 2 bis 3f weggefallen, §§ 1, 4, 4a, 5, 6 gelten fort); Melde- und Abhilfeverfahren (Art. 16 DSA) trifft den Hostingdiensteanbieter, auf fremder Plattform also den Plattformbetreiber, nicht den Kanalinhaber; bei eigener Kommentarfunktion (Blog) ist der Betreiber insoweit selbst Hostingdiensteanbieter
- [ ] [[gesetze/dsa]]

## Typische Findings

### CRIT

- Kein Impressum im YouTube-Kanal (Abmahn-Garant)
- Bezahlter Post auf Instagram ohne "Werbung"-Kennzeichnung
- Fremde Bilder im Blog ohne Lizenznachweis (und ohne Quellenangabe)
- Newsletter ohne nachweisbare vorherige ausdrueckliche Einwilligung (§ 7 Abs. 2 Nr. 2 UWG, Art. 7 Abs. 1 DSGVO) bzw. ohne gueltige Abmeldeadresse (§ 7 Abs. 2 Nr. 3 lit. c UWG); fehlendes Double-Opt-In ist Nachweisrisiko, kein eigener Verstoss
- KI-Voice-Clone ohne Einwilligung der realen Person (+Persoenlichkeitsrecht)

### HIGH

- Musik-Untermalung im Video ohne Lizenz-Nachweis
- Einwilligung erkennbarer Personen im Video fehlt (KUG + Art. 6 DSGVO)
- YouTube-Embed auf eigener Website ohne Consent
- Affiliate-Links im Blog ohne Werbe-Hinweis

### MED

- Kein Transkript fuer Podcast, wenn der Podcast Teil einer BFSG-pflichtigen Dienstleistung ist (§ 1 Abs. 3 BFSG) und nicht vor dem 28.06.2025 veroeffentlicht wurde (§ 1 Abs. 4 Nr. 1 BFSG)
- Screenshots fremder Marken zu gross / ohne klare Zitat-Funktion
- Kommentar-Funktion speichert IP unlimited

### LOW

- Alt-Texte fehlen bei einzelnen Bildern

## Siehe auch

- [[gesetze/urhg]]
- [[gesetze/markeng]]
- [[gesetze/uwg]]
- [[gesetze/ddg]] — § 5 Impressum
- [[gesetze/ai-act]]
- [[gesetze/bfsg]]
- [[themen/urheber-stockfoto]]
- [[themen/werbekennzeichnung]]
- [[themen/ki-content]]
- [[themen/email-marketing]]
- [[themen/impressum]]
- [[themen/zitatrecht]]
- [[themen/fotos-dritter-kug]]
- [[themen/siegel-werbung]]
- [[themen/social-media-datenschutz]]
- [[themen/tool-katalog]]
- [[urteile/bgh-inbox-werbung]]

---

## Aenderungsvermerk (2026-11-14, Batch F stale-only)

- Frontmatter und Disclaimer-Stand auf 2026-11-14 aktualisiert.
- Pass 4 (Newsletter) um Kuendigungsschaltflaeche § 312k BGB erweitert; Tier-1-belegt gegen gesetze-im-internet.de/bgb/__312k.html.
- Bestandspruefung (ausserhalb Pass 5): alle Pflicht-Normzitate und Aktenzeichen bestaetigt — § 5 DDG, § 18 Abs. 2+3/§ 22 MStV, Art. 6/26 DSGVO, § 22/§ 23 KUG, § 26 BDSG, § 5a Abs. 4 UWG, § 7 Abs. 2 Nr. 2/Abs. 3 UWG, § 51 UrhG, § 59 UrhG, §§ 87f ff. UrhG, § 1/§ 14 BFSG, DSA VO (EU) 2022/2065 (anwendbar seit 17.02.2024), § 312k BGB. BGH-Aktenzeichen I ZR 90/20, 125/20, 126/20 (09.09.2021 — Influencer-Trilogie) und I ZR 218/07 (10.02.2011 — Double-Opt-In II), I ZR 25/19 (13.01.2022 — Inbox-Werbung II) konsistent zu KB. Keine offenen Marker in dieser Datei. Berichtigt am 2026-11-15: Diese Bestaetigung traf nicht zu. I ZR 218/07 ist kein Double-Opt-In-Urteil (richtig: I ZR 164/09 vom 10.02.2011); ferner waren § 1 Abs. 3 BFSG, § 5 DDG fuer Newsletter, Art. 50 Abs. 4 "S. 2" KI-VO und die Aussage zur Aufhebung des NetzDG ungenau oder falsch.
- Pass 5 (KI) und Datumsangaben zum AI Act durch anderen Agent am selben Tag separat aktualisiert; hier nicht angetastet.

## Aenderungsvermerk (2026-11-15)

- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1): Werbekennzeichnung an § 5a Abs. 4 Saetze 2 und 3 UWG und [[themen/werbekennzeichnung]] angeglichen (keine allgemeine Kennzeichnungspflicht); KI-Texte Art. 50 Abs. 4 UAbs. 2 mit vollstaendiger Ausnahme; KI-Bilder/Audio/Video und KI-Stimmen: Betreiberpflicht nur bei Deepfakes, Art. 50 Abs. 2 trifft den Anbieter; BFSG-Ausnahmen § 1 Abs. 4; Crossposting-Hinweis § 18 Abs. 3 MStV nur bei personenaehnlichen Konten; Double-Opt-In mit I ZR 164/09; Absenderidentitaet statt Impressum in jeder Mail; Paid Newsletter § 312k auf CRIT; NetzDG besteht fort.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2): JMStV statt MStV/JMStV; Model Release § 22 Satz 1 KUG, Art. 6 Abs. 1 und Art. 7 Abs. 1 DSGVO; Interview-Freigabe ohne gesetzliche Pflicht; Screenshots § 51 Satz 1 und 3, § 63 UrhG; KI-Bilder § 2 Abs. 2, § 23 UrhG; Avatare Art. 50 Abs. 4 UAbs. 1 i. V. m. Art. 3 Nr. 60; Melde- und Abhilfeverfahren Art. 16 DSA; Newsletter-Nachweis Art. 7 Abs. 1 DSGVO ohne gesetzliche Zweijahresfrist; COPPA als US-Recht; BFSG-Podcast-Transkript; LG Muenchen I 42 O 14139/24 laut Pressemitteilung; fluechtige Anbieterangaben (Sitz, Lizenzinhalte, Cookie-Verhalten) durch Pruefhinweise ersetzt.
