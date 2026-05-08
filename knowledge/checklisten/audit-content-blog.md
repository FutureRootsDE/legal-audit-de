---
aktualisiert: 2026-05-08
gilt-fuer: Blog, Corporate-Blog, YouTube-Channel, Podcast, Social-Media-Content, Newsletter
verifiziert-am: 2026-05-08
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. Content-Produktion ist
> urheberrechts-, wettbewerbs- und werbekennzeichnungsrechtlich anspruchsvoll.
>
> **Stand:** 2026-05-08

# Audit-Checkliste: Content / Blog / YouTube / Podcast

## Kurz-Ueberblick

Content-Produktion beruehrt:
1. **UrhG** — Zitat-Recht, Bildrechte, Musik-Lizenzen
2. **UWG** — Schleichwerbung, Influencer-Werbekennzeichnung
3. **MStV § 18** — Impressum fuer journalistisch-redaktionelle Telemedien
4. **DSGVO** — wenn erkennbare Personen gezeigt werden (KUG + Art. 6 DSGVO)
5. **AI Act** — bei KI-generierten Inhalten
6. **MStV / JMStV** — Jugendmedienschutz (Altersfreigaben, v.a. YouTube)

## Pass 1: PII-Identifikation (Personen im Content)

- [ ] Erkennbare Personen im Bild-/Video-Material?
  - Einwilligung nach § 22 KUG **und** Art. 6 DSGVO dokumentiert (Model Release)
  - Ausnahmen § 23 KUG: Personen der Zeitgeschichte, Beiwerk, Versammlungen — dennoch DSGVO pruefen
  - Details und Muster-Freigabe siehe [[themen/fotos-dritter-kug]]
- [ ] Stimmen im Podcast identifizierbar? Gast-Einwilligung schriftlich
- [ ] Interviews: Freigabe vor Veroeffentlichung (Gegenlesen-Pflicht bei journalistisch, sonst aus AVV)
- [ ] Kommentarfunktion / User-Generated-Content → DSGVO-Pflichten fuer User-Daten
- [ ] Newsletter-Verteiler / Podcast-Hosting-Analytics (Spotify, Apple Podcasts)

## Pass 2: Drittland-/Drittanbieter-Transfers

- [ ] **YouTube** (Google LLC USA) — bei eigener Einbettung auf Website: YT-Nocookie oder Consent
- [ ] **Spotify for Podcasters / Podigee / Libsyn** — Podcast-Hosting mit Analytics
- [ ] **Apple Podcasts Analytics** — Daten-Austausch mit Apple
- [ ] **Transcription-Services** (Whisper-API, Descript, Rev) — PII in Transkripten
- [ ] **Newsletter-Tools** (Substack US, Buttondown US, Brevo FR, Mailchimp US) — AVV + ggf. SCC/DPF
- [ ] **Video-Hosting** (Vimeo US, Mux US) — AVV
- [ ] **Social-Media-APIs** (Meta Graph API, X API, TikTok API, LinkedIn API) — Drittland

## Pass 3: Cookie-/Consent-Analyse

- [ ] YouTube-Embed mit Consent (youtube-nocookie.com ist besser, aber nicht 100% cookiefrei)
- [ ] Spotify-Player-Embed mit Consent
- [ ] Kommentar-Systeme (Disqus, Giscus) — Disqus ist US/Tracking-intensiv, Giscus (GitHub) besser
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

- [ ] **§ 5a Abs. 4 UWG** + **§ 22 MStV** — bezahlte Inhalte als **"Werbung"** / **"Anzeige"** / **"bezahlte Partnerschaft"** klar erkennbar (BGH I ZR 90/20, I ZR 125/20, I ZR 126/20 v. 09.09.2021 — "Influencer-Trilogie")
- [ ] Affiliate-Links → Kennzeichnung als solche (auch wenn nicht bezahlt, aber Provisionsbasiert)
- [ ] Pressemuster / PR-Samples → Offenlegung ("PR-Sample", "kostenlos erhalten")
- [ ] YouTube: zusaetzlich "Paid Promotion"-Toggle von Google aktivieren (nicht statt, sondern zusaetzlich)
- [ ] Instagram: "Bezahlte Partnerschaft mit [Marke]" aktivieren + im Post-Text nochmal "Werbung" / "Anzeige"
- [ ] [[themen/werbekennzeichnung]], [[gesetze/uwg]]

## Pass 5: KI-Spezifisch (AI Act-Stufung)

Anwendbarkeit-Stufung: Verbotene Praktiken (Art. 5) und KI-Kompetenz (Art. 4) seit **02.02.2025**, GPAI-Pflichten seit **02.08.2025**, **Vollanwendung Art. 50 (Transparenz) ab 02.08.2026** mit maschinenlesbarem Wasserzeichen.

- [ ] **KI-Kompetenz** Art. 4 AI Act: Schulungs-/Sensibilisierungsnachweis fuer alle Redakteure mit KI-Einsatz
- [ ] **KI-generierter Text** im Blog → Kennzeichnung empfohlen ("Dieser Artikel wurde mit Unterstuetzung von KI erstellt")
- [ ] **KI-generierte Bilder/Audio/Video** im Artikel → Kennzeichnung Pflicht (Art. 50 Abs. 2 AI Act); Wasserzeichen-Pflicht ab 02.08.2026
- [ ] **KI-Stimmen** im Podcast → Transparenzpflicht (Hoerer hat Recht zu wissen, dass keine menschliche Stimme)
- [ ] **Deepfakes** von realen Personen → zwingend als kuenstlich erzeugt kennzeichnen (Art. 50 Abs. 4 AI Act) UND Einwilligung der Person noetig (Persoenlichkeitsrecht / KUG)
- [ ] **Synthetische Avatare** als Sprecher → Kennzeichnung
- [ ] **Verbotene Praktiken** Art. 5: keine manipulativen Subliminal-Techniken, kein Social-Scoring-Content
- [ ] [[gesetze/ai-act]], [[themen/ki-content]], [[themen/ki-transparenz]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar)

BFSG ist seit **28.06.2025 in Anwendung**. Reine redaktionelle Inhalte sind oft nicht direkter BFSG-Anwendungsbereich (siehe Ausnahmen § 1 Abs. 3 BFSG fuer Medieninhalte), aber **kommerzielle Content-Sites mit Newsletter-Verkauf, Online-Kurs-Verkauf, Webshops** sind erfasst.

- [ ] **Anwendungsbereich** § 1 BFSG geprueft
- [ ] YouTube: **Untertitel** (automatisch + korrigiert) fuer alle Videos
- [ ] Podcast: **Transkripte** als PDF/HTML bereitstellen
- [ ] Blog: WCAG 2.1 AA — Kontraste, Alt-Texte, Tastaturnavigation
- [ ] **Barrierefreiheitserklaerung** wenn BFSG-pflichtig (§ 14 BFSG)
- [ ] [[gesetze/bfsg]], [[themen/barrierefreiheit]]

## Pass 7: Urheber / Marken (Hot-Zone!)

### Bild- und Video-Material

- [ ] **Eigene Aufnahmen**: Model-Release-Formular (Einwilligung Person, Nutzungsrechte)
- [ ] **Stock-Bilder**: Shutterstock, Adobe Stock, Getty — Lizenz-ID im CMS hinterlegt
- [ ] **Creative Commons**: Lizenz korrekt zitieren (CC-BY bedeutet Namensnennung!)
- [ ] **Unsplash**: erlaubt kommerziell, aber keine trademarked faces
- [ ] **Screenshots** fremder Websites: kurze Erkennung meist zulaessig (Zitatrecht § 51 UrhG), aber Vorsicht bei Logos
- [ ] **Panoramafreiheit** bei Architektur (§ 59 UrhG) — nur oeffentlicher Raum, nicht Innenraeume
- [ ] **KI-generierte Bilder**: Copyright-Frage komplex — oft kein Urheberrecht (Schoepfungshoehe fehlt), aber moegliche Unterlassung bei Stil-Nachahmung lebender Kuenstler

### Musik (kritisch bei YouTube/Podcast!)

- [ ] **GEMA-Lizenz** bei deutscher/europaeischer Musik
- [ ] **YouTube Audio Library** (Royalty-Free) — erlaubt bei YouTube
- [ ] **Epidemic Sound / Artlist / Soundstripe** — kommerzielle Abo-Lizenz dokumentiert
- [ ] **Podcast**: GEMA-Musik braucht Podcast-Lizenz (GEMA Musicautor-Vertrag) — oft teurer als angenommen
- [ ] **Copyright-Claims** auf YouTube: Monitoring + Streitverfahren-Kenntnis
- [ ] **KI-generierte Musik** (Suno, Udio, Mubert): Lizenz-Status pruefen; Trainingsdaten-Klagen laufen

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
- [ ] Newsletter-Verteiler: bei Abmeldung sofort entfernen, Double-Opt-In-Bestaetigung archivieren (min. 2 Jahre)
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
- [ ] Bei automatisiertem Crossposting (n8n, Zapier): Hinweis nach § 18 Abs. 3 MStV ("automatisiert erstellt")
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
- [ ] Bei "gemacht fuer Kinder" COPPA-Hinweise beachten
- [ ] Paid Promotion korrekt deklariert
- [ ] Musik aus YT Audio Library oder mit Lizenz

### Podcast

- [ ] ID3-Tags im MP3 mit Urheber, Copyright
- [ ] RSS-Feed valide (Impressum-Link, Copyright-Tag)
- [ ] Shownotes mit Quellenangaben
- [ ] Bei Co-Host / Gaesten: Splittung Urheberrechte klaeren

### Newsletter

- [ ] Double-Opt-In mit Bestaetigungs-Mail (BGH "Double-Opt-In II" I ZR 218/07)
- [ ] Abmelde-Link in JEDER Mail (§ 7 Abs. 2 Nr. 2 UWG i.V.m. Abs. 3 — bei Bestandskundenausnahme)
- [ ] Impressum in jeder Mail (§ 5 DDG)
- [ ] Personalisierung nur nach Einwilligung
- [ ] BGH "Inbox-Werbung II" I ZR 25/19 (13.01.2022) — Inbox-Werbung in E-Mail-Postfaechern bedarf Einwilligung
- [ ] [[themen/email-marketing]], [[urteile/bgh-inbox-werbung]], [[gesetze/uwg]]

### Social Media

- [ ] Plattform-AGB einhalten (Meta, TikTok, X)
- [ ] Keine trademarked Hashtags als Post-Marker
- [ ] **Jede Plattform** eigenes Impressum / "Link in Bio"
- [ ] User-Reaktionen moderieren bei beleidigenden Kommentaren — **DSA** Verordnung (EU) 2022/2065 vollanwendbar seit 17.02.2024 (NetzDG aufgehoben durch DDG-Begleitgesetzgebung); Notice-and-Action-Mechanismus fuer Hostingdienste
- [ ] [[gesetze/dsa]]

## Typische Findings

### CRIT

- Kein Impressum im YouTube-Kanal (Abmahn-Garant)
- Bezahlter Post auf Instagram ohne "Werbung"-Kennzeichnung
- Fremde Bilder im Blog ohne Lizenznachweis (und ohne Quellenangabe)
- Newsletter ohne Double-Opt-In + ohne Abmelde-Link (UWG + DSGVO doppelter Verstoss)
- KI-Voice-Clone ohne Einwilligung der realen Person (+Persoenlichkeitsrecht)

### HIGH

- Musik-Untermalung im Video ohne Lizenz-Nachweis
- Einwilligung erkennbarer Personen im Video fehlt (KUG + Art. 6 DSGVO)
- YouTube-Embed auf eigener Website ohne Consent
- Affiliate-Links im Blog ohne Werbe-Hinweis

### MED

- Kein Transkript fuer Podcast (BFSG-Relevanz)
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
