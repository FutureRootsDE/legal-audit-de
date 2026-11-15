---
aktualisiert: 2026-11-15
gilt-fuer: WooCommerce, Shopware 6, Shopify, Magento, PrestaShop, JTL
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. E-Commerce ist abmahnintensiv —
> vor Launch zwingend Pruefung durch einen Fachanwalt fuer IT-/E-Commerce-Recht
> oder ein Schutzpaket (z.B. IT-Recht Kanzlei Muenchen).
>
> **Stand:** 2026-11-14

# Audit-Checkliste: E-Commerce-Shop

## Kurz-Ueberblick

E-Commerce-Shops haben die **hoechste Abmahnfrequenz** — v.a. wegen PAngV, Widerrufsbelehrung, Button-Loesung. Wettbewerber und Abmahnvereine (z.B. IDO Interessenverband, Wettbewerbszentrale) scannen systematisch.

**Minimum-Schutz-Schichten:**
1. Rechtstexte-Schutzpaket (IT-Recht Kanzlei ~25 EUR/Monat oder Haendlerbund)
2. Trusted Shops / Trustedshops-Kaeuferschutz fuer Vertrauen
3. SSL/TLS (Pflicht wegen PCI-DSS + Art. 32 DSGVO)

## Pass 1: PII-Identifikation

- [ ] Kunden-Konto-Daten (Name, Adresse, E-Mail, Telefon, Geburtsdatum falls erhoben)
- [ ] Bestell-Historie + Bestellpositionen
- [ ] Zahlungs-Daten (Stripe/PayPal/Klarna — via Token, nicht im Shop gespeichert)
- [ ] Versand-Adressen (ggf. abweichend von Rechnungs-Adresse)
- [ ] Rechnungs-Archiv (PDF + Datenbank) — 10 Jahre Retention
- [ ] Wunschliste, Warenkorb-Abbrueche
- [ ] Tracking-Daten (GA4 Enhanced Ecommerce)
- [ ] Bewertungen (mit Namen / Nickname)
- [ ] Support-Tickets (Zendesk/Freshdesk-Integration)

## Pass 2: Drittland-/Drittanbieter-Transfers

### Payment

- [ ] **Stripe** — getrennte Verantwortlichkeit; AVV + Stripe Data Processing Agreement
- [ ] **PayPal** — LU-Sitz, EU-Konform, aber bei bestimmten Funktionen JCA
- [ ] **Klarna / AfterPay / Ratepay** — AVV + Bonitaetspruefung erfordert eigene Informationspflicht Art. 14
- [ ] **SOFORT / giropay / EPS** — AVV pruefen
- [ ] Kreditkarten-Daten: **niemals** selbst hosten — PCI-DSS-Level 1 Anforderungen extrem hoch

### Versand

- [ ] DHL, Hermes, UPS, DPD — AVV + Versanddaten-Schnittstelle dokumentiert
- [ ] Kein US-Versandleister ohne SCC/DPF

### Marketing / Tracking

- [ ] GA4 Enhanced Ecommerce nur mit Consent
- [ ] Meta Pixel + Conversion API — JCA Art. 26
- [ ] Google Merchant Center — Produkt-Feed ohne PII
- [ ] Retargeting (Criteo, AdRoll, Quantcast) — Einwilligung + DPIA bei Profiling
- [ ] Bewertungs-Dienste (Trustpilot, Trusted Shops) — AVV

### Logistik / ERP

- [ ] ERP-Integration (JTL-Wawi, SAP, Xentral) — AVV
- [ ] Lagerpartner / Fulfillment (Amazon FBA, Shipwire) — AVV

## Pass 3: Cookie-/Consent-Analyse

Besonderheit Shop: **Warenkorb-Cookie ist technisch notwendig** (kein Consent). Alles darueber hinaus (Tracking, Retargeting) = Consent.

- [ ] Warenkorb/Session/Login = "unbedingt erforderlich"
- [ ] Wishlist-Persistence (wenn nicht login-gebunden) = Gray Area — tendenziell Consent
- [ ] "Zuletzt angesehene Produkte" = Personalisierung = Consent
- [ ] Produktempfehlungen via ML = Consent
- [ ] Komplexere Tabelle in [[themen/cookie-consent]]

## Pass 4: Pflicht-Texte E-Commerce (Abmahn-HOT-Zone!)

### Preisangabenverordnung (PAngV 2022 — gilt seit 28.05.2022)

- [ ] **Gesamtpreis inkl. USt** sichtbar (§ 3 PAngV n.F.)
- [ ] **Grundpreis** bei Fertigpackungen (EUR/kg, EUR/Liter) — § 4 PAngV
- [ ] **"zzgl. Versand"** Hinweis + Link zur Versandkostenuebersicht (§ 6 Abs. 1 PAngV)
- [ ] **Streichpreis / Preisermaessigung**: **30-Tage-Tiefstpreis** muss angegeben werden (§ 11 PAngV — Umsetzung Modernisierungs-RL (EU) 2019/2161)
  - EuGH, Urt. v. 26.09.2024, C-330/23 (Aldi Sued), ECLI:EU:C:2024:804: Auch eine prozentuale Preisermaessigung ist auf Grundlage des niedrigsten Preises der letzten 30 Tage zu berechnen.
  - BGH, Urt. v. 09.10.2025, I ZR 183/24 (Jacobs Kroenung), ECLI:DE:BGH:2025:091025UIZR183.24.0: Der niedrigste Gesamtpreis der letzten 30 Tage ist in einer eindeutigen, klaren und verstaendlichen Weise anzugeben (§ 11 Abs. 1 i. V. m. § 1 Abs. 3 Satz 2 PAngV); die Unlauterkeit folgt aus §§ 5a, 5b UWG, nicht aus § 3a UWG.
- [ ] **Preis je Masseinheit** bei Getraenken, Lebensmitteln, Kosmetik etc.
- [ ] Keine Phantasie-Preise (UVP muss echte Hersteller-UVP sein, § 5 UWG)
- [ ] [[gesetze/pangv]], [[themen/preisangaben]]

### Widerrufsbelehrung + Widerrufsformular

- [ ] **Muster-Widerrufsbelehrung** nach Anlage 1 zu Art. 246a § 1 Abs. 2 EGBGB in der seit 19.06.2026 geltenden Fassung: informiert gegebenenfalls ueber das Bestehen und die Platzierung der Widerrufsfunktion nach § 356a BGB (Art. 246a § 1 Abs. 2 Satz 1 Nr. 1 EGBGB n. F., BGBl. 2026 I Nr. 28)
- [ ] **Muster-Widerrufsformular** als PDF oder separate HTML-Seite
- [ ] 14-Tage-Frist korrekt formuliert
- [ ] Ausnahmen konkret aufgelistet (digitaler Content nach Einwilligung, versiegelte Waren, etc. § 312g BGB)
- [ ] Bestaetigungs-Mail nach Kauf enthaelt Widerrufsbelehrung in **Textform** (nicht nur Link!)
- [ ] **Elektronische Widerrufsfunktion nach § 356a BGB** (gesetze-im-internet.de/bgb/__356a.html) bei allen Fernabsatzvertraegen, die ueber eine Online-Benutzeroberflaeche geschlossen werden (nicht nur Finanzdienstleistungen): Pflichtschaltflaeche "Vertrag widerrufen" (oder eine andere gleichbedeutende eindeutige Formulierung) waehrend der gesamten Widerrufsfrist erreichbar + Bestaetigungsschaltflaeche "Widerruf bestaetigen" (oder eine andere gleichbedeutende eindeutige Formulierung) + Eingangsbestaetigung auf dauerhaftem Datentraeger inkl. Datum und Uhrzeit (§ 356a Abs. 1-4 BGB); anzuwenden seit **19.06.2026** (Umsetzung RL (EU) 2023/2673, CELEX:32023L2673) — Severity CRIT bei B2C-Shop ohne Widerrufsbutton
- [ ] **Harmonisierte Mitteilung zum gesetzlichen Gewaehrleistungsrecht** nach DVO (EU) 2025/1960 in den vorvertraglichen Informationen (Art. 246a § 1 Abs. 1 EGBGB)
- [ ] [[themen/widerrufsbelehrung]]

### Button-Loesung (§ 312j Abs. 3 BGB)

- [ ] Bestell-Button-Text: **"zahlungspflichtig bestellen"** oder gleichbedeutender Wortlaut (z.B. "jetzt kaufen", "kostenpflichtig bestellen")
- [ ] Keine kreativen Varianten wie "Bestellung abschicken", "Weiter", "Anmelden" (abmahnrelevant; bei Verstoss kommt kein Vertrag zustande, § 312j Abs. 4 BGB)
- [ ] **BGH, Urt. v. 09.10.2025, I ZR 159/24** (ECLI:DE:BGH:2025:091025UIZR159.24.0): Bei Verstoss gegen § 312j Abs. 3 BGB ist der Vertrag nach § 312j Abs. 4 BGB nicht schwebend, sondern endgueltig unwirksam; ein Neuabschluss ist durch Bestaetigung nach § 141 BGB moeglich. Den Pflichtwortlaut der Schaltflaeche regelt § 312j Abs. 3 Satz 2 BGB, nicht dieses Urteil.
- [ ] Checkout-Seite: Wesentliche Produktmerkmale, Gesamtpreis, Versand, Laufzeit unmittelbar vor dem Button (§ 312j Abs. 2 BGB)
- [ ] **Abo-Fallen** (Art. 246a § 1 Abs. 1 Satz 1 Nr. 8, 14, 15 EGBGB i. V. m. § 312j Abs. 2 BGB): bei wiederkehrenden Leistungen Mindestlaufzeit + Gesamtkosten transparent
- [ ] **Kuendigungsbutton § 312k BGB** bei Abo-/Dauerschuldverhaeltnissen mit Verbrauchern: Schaltflaeche "Vertraege hier kuendigen" (oder gleichwertig) auf der Website + Bestaetigungsseite mit Button "jetzt kuendigen", staendig verfuegbar und leicht zugaenglich (§ 312k Abs. 2 BGB); Bestaetigung der Kuendigung sofort auf elektronischem Wege in Textform (§ 312k Abs. 4 BGB); Folge bei Verstoss: jederzeitige fristlose Kuendigung durch Verbraucher moeglich (§ 312k Abs. 6 BGB) — Severity CRIT
- [ ] [[themen/button-loesung]]

### AGB

- [ ] **AGB** mit Einbeziehungsklausel im Checkout ("Ich habe die AGB gelesen und akzeptiere sie")
- [ ] Pre-Tick VERBOTEN — User muss aktiv bestaetigen
- [ ] Klauselkontrolle (§§ 305-309 BGB) — keine ueberraschenden oder unklaren Klauseln
- [ ] **Streitbeilegungs-Hinweis** nach Art. 14 Abs. 1 VO (EU) 524/2013 ist entfallen: Die **OS-Plattform der EU wurde am 20.07.2025 eingestellt** und die VO (EU) 524/2013 mit Wirkung vom **20.07.2025** durch **VO (EU) 2024/3228** vom 19.12.2024, Art. 1 aufgehoben (CELEX 32024R3228; am 2026-11-14 am Cellar-Volltext verifiziert). Links auf https://ec.europa.eu/consumers/odr/ sowie entsprechende AGB-/Impressumsklauseln entfernen. **Unberuehrt:** VSBG-Hinweis nach § 36 VSBG (Teilnahme an nationaler Verbraucherschlichtungsstelle) bleibt bestehen.
- [ ] **VSBG-Hinweis** (§ 36 VSBG): Verbraucherschlichtungsstelle-Bereitschaft JA/NEIN. Ausnahme: Die Hinweispflicht nach § 36 Abs. 1 Nr. 1 VSBG entfaellt fuer Unternehmer, die am 31.12. des Vorjahres hoechstens zehn Personen beschaeftigt haben (§ 36 Abs. 3 VSBG); darunter besteht die Hinweispflicht nur bei Teilnahmepflicht (§ 36 Abs. 1 Nr. 2 VSBG)
- [ ] [[themen/agb-muster]], [[gesetze/bgb-agb]]

### Impressum + Datenschutzerklaerung

- [ ] Impressum nach § 5 DDG mit vollen Angaben — [[themen/impressum]]
- [ ] DSE nach Art. 13 DSGVO mit allen Shop-spezifischen Drittanbietern — [[themen/datenschutzerklaerung]]

### Allgemeine Produktsicherheitsverordnung (GPSR)

- [ ] **GPSR Verordnung (EU) 2023/988** beachtet: **gilt ab 13.12.2024** (Art. 52; per Cellar CELEX:32023R0988 verifiziert); produktbezogene Informationspflichten beim Onlinehandel inkl. Fernabsatz (Art. 19: u.a. Name/Anschrift Hersteller, Name/Anschrift des EU-Verantwortlichen nach Art. 16, eindeutige Produktidentifikation, Warnhinweise in deutscher Sprache fuer DE-Markt) — Severity HIGH
- [ ] Pflichten ergeben sich unmittelbar aus der VO (EU) 2023/988; § 3 Abs. 5 ProdSG betrifft nur das Ausstellen nicht konformer Produkte und ist keine allgemeine Verweisung auf die VO

### Umweltaussagen / Nachhaltigkeitssiegel

- [ ] **EmpCo-Richtlinie (EU) 2024/825** (Empowering Consumers for the Green Transition, CELEX:32024L0825, per Cellar verifiziert): Mitgliedstaaten erlassen bis 27.03.2026, Anwendung ab **27.09.2026**; umgesetzt durch G v. 12.02.2026 (BGBl. 2026 I Nr. 43, Drittes UWG-Aenderungsgesetz), in Kraft seit 27.09.2026; Uebergangsvorschrift § 15b UWG (Art. 5 G v. 22.10.2026, BGBl. 2026 I Nr. 322) (siehe [[gesetze/uwg]]): Verbot irrefuehrender Umweltaussagen (§ 5 Abs. 2 Nr. 1, Abs. 3 Nr. 3/4 UWG), Beschraenkung der Nutzung von Nachhaltigkeitssiegeln ohne zertifiziertes System (Anhang Nrn. 2a, 4a-4c, 10a, 23d UWG), ergaenzte Informationspflichten § 5b Abs. 3a UWG — Severity HIGH

## Pass 5: KI-Spezifisch (AI Act-Stufung)

Anwendbarkeit (Stand 2026-11-14, inkl. VO (EU) 2026/1744 Digital Omnibus on AI): Verbotene Praktiken (Art. 5) seit **02.02.2025** (neue NCII/CSAM-Verbote ab 02.12.2026), KI-Kompetenz (Art. 4) seit **02.02.2025** (seit 27.07.2026 Verhaltenspflicht), GPAI-Pflichten seit **02.08.2025**, **Art. 50 Transparenz seit 02.08.2026 anwendbar** (Altbestand-Markierung bis 02.12.2026, Art. 111 Abs. 4).

- [ ] **KI-Kompetenz** Art. 4 KI-VO n. F. (seit 27.07.2026 i. d. F. VO (EU) 2026/1744): "Massnahmen ergreifen" zur Unterstuetzung der KI-Kompetenz; **keine Pflicht** zur **Garantie** eines bestimmten Niveaus (Art. 4 Abs. 1 Satz 2 n. F.) — Nachweis geeigneter Foerdermassnahmen fuer Mitarbeiter mit KI-Beruehrung dennoch dokumentieren
- [ ] KI-Produktempfehlungs-Engine → Einwilligung + ggf. DSFA
- [ ] KI-generierte Produktbeschreibungen → Kennzeichnung empfohlen (insb. bei Bewertungen!)
- [ ] Chatbot mit GPT/Claude-Backend → Art. 50 Abs. 1 AI Act Transparenzpflicht seit 02.08.2026 ("Sie interagieren mit einer KI")
- [ ] KI-generierte Produktbilder → Die maschinenlesbare Markierung nach Art. 50 Abs. 2 AI Act trifft den Anbieter des Generators, nicht den Shop. Der Shop als Betreiber muss nur Deepfakes offenlegen (Art. 50 Abs. 4 AI Act); im Uebrigen Irrefuehrungsverbot (§ 5 UWG) beachten
- [ ] **Fake Reviews**: §§ 5, 5a UWG; § 5b Abs. 3 UWG ist eine Informationspflicht, ob und wie sichergestellt wird, dass Bewertungen von Verbrauchern stammen (keine Pruefpflicht; auch der Hinweis, dass nicht geprueft wird, erfuellt sie). Unzulaessig sind Echtheitsbehauptungen ohne angemessene Pruefung (Anhang Nr. 23b UWG) und gefaelschte Bewertungen (Anhang Nr. 23c UWG). Bei KI-generierten Bewertungen klare Kennzeichnung
- [ ] [[gesetze/ai-act]], [[themen/ki-content]], [[themen/ki-transparenz]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar — fuer B2C-E-Commerce zwingend!)

BFSG ist **seit 28.06.2025 in Anwendung**. Es betrifft B2C-Online-Shops, sofern nicht Kleinstunternehmen-Ausnahme greift (weniger als 10 Beschaeftigte und Jahresumsatz oder Jahresbilanzsumme hoechstens 2 Mio EUR, § 2 Nr. 17 BFSG; Ausnahme nur fuer Dienstleistungen, § 3 Abs. 3 BFSG).

- [ ] **Anwendungsbereich** geprueft (§ 1 BFSG): B2C-Shop? Kleinstunternehmen-Ausnahme dokumentiert?
- [ ] WCAG 2.1 AA als Pruefraster: § 3 BFSGV verweist auf den Stand der Technik; Konformitaetsvermutung nach § 4 BFSG, EN 301 549 / WCAG 2.1 AA nur darueber; Anforderungen §§ 12, 19 BFSGV
- [ ] Checkout komplett barrierefrei (Tastatur, Screen-Reader, Fehlermeldungen formuliert)
- [ ] Alt-Texte fuer alle Produktbilder
- [ ] Farbkontrast bei Produkt-Beschriftungen, Preise, Buttons
- [ ] **Barrierefreiheitserklaerung** veroeffentlicht (§ 14 BFSG)
- [ ] **Feedback-Mechanismus** fuer Barrieren
- [ ] Bussgeldrahmen bis 100.000 EUR (§ 37 BFSG)
- [ ] [[gesetze/bfsg]], [[themen/barrierefreiheit]]

## Pass 7: Urheber / Marken / Wettbewerb

- [ ] Produktbilder: Herstellerfreigabe oder eigene Fotos; Stockbilder mit Lizenz
- [ ] Produktbeschreibungen: keine woertlichen Uebernahmen von Hersteller ohne Freigabe (Urheberrecht)
- [ ] Marken der Hersteller korrekt zitiert (Nominatives Fair Use ok, aber Logo-Nutzung oft Lizenz noetig)
- [ ] **Keine Kopien/Markenfaelschungen** — strafrechtlich relevant
- [ ] Vergleichende Werbung nach § 6 UWG zulaessig, aber Grenzen
- [ ] **Keine Lockvogelangebote** (§ 5 UWG — Produkt muss verfuegbar sein in angemessener Menge)

## Pass 8: Logs / Retention / Buchhaltung

- [ ] **Rechnungen/Buchungsbelege** → 8 Jahre (§ 257 Abs. 1 Nr. 4, Abs. 4 HGB; § 147 Abs. 1 Nr. 4, Abs. 3 AO; § 14b Abs. 1 UStG); Buecher, Inventare, Abschluesse → 10 Jahre; Handels- und Geschaeftsbriefe → 6 Jahre; Ausnahme 10 Jahre fuer Kredit-, Versicherungs- und Wertpapierinstitute (§ 257 Abs. 4 Satz 2 HGB)
- [ ] **Bestelldaten** (fuer Garantie/Gewaehrleistung) → typ. 3 Jahre (Verjaehrung); buchhaltungsrelevante Teile: 8 Jahre als Buchungsbeleg, 6 Jahre als Handelsbrief (§ 257 Abs. 4 HGB, § 147 Abs. 3 AO)
- [ ] **Kunden-Konten**: Loeschung auf Wunsch, aber Buchhaltungsdaten anonymisieren statt loeschen
- [ ] **Server-Logs** wie SaaS (7-14 Tage IP)
- [ ] **Payment-Transaction-Logs** — nach Payment-Provider-Vorgabe, meist 10 Jahre
- [ ] **Newsletter** — bei Abmeldung sofort deaktivieren, aber Double-Opt-In-Log archivieren

## Pass 9: Trust-Badges / Siegel / Bewertungs-Widgets

E-Commerce lebt von Trust-Signalen — Abmahn-HOT-Zone. Siehe [[themen/siegel-werbung]].

- [ ] **Trusted Shops / eKomi / Trustpilot**: Lizenz aktiv, Zertifikat nachpruefbar; Widget laedt erst nach Consent (oft JS-Abhaengig)
- [ ] **"TUeV-geprueft" / "DEKRA-zertifiziert"**: gueltiges Zertifikat, Pruef-Nummer verlinkt
- [ ] **Stiftung-Warentest-/OEKO-TEST-Logos**: Lizenz-Vertrag, korrektes Heft/Jahr, konkrete Produktbewertung
- [ ] **"Testsieger 2023"** ohne Monat/Heft: abmahnbar <<VERIFIKATION AUSSTEHEND>>
- [ ] **Eigene "Bestseller"-/"Beliebt"-Badges**: Bewertungsgrundlage transparent (keine reinen Marketing-Behauptungen)
- [ ] **Kundenbewertungen aggregiert** ("4.8 von 5, 1240 Bewertungen"): § 5b Abs. 3 UWG (seit Omnibus-RL 2022): Information, ob und wie sichergestellt wird, dass Bewertungen von Verbrauchern stammen (keine Pruefpflicht); unzulaessig sind Echtheitsbehauptungen ohne angemessene Pruefung (Anhang Nr. 23b UWG) und gefaelschte Bewertungen (Anhang Nr. 23c UWG)
- [ ] **Fake-Reviews / KI-generierte Reviews**: §§ 5, 5a UWG, § 5b Abs. 3 UWG. Hauptrisiko Abmahnung; Bussgeld nur bei weitverbreitetem Verstoss (§ 5c UWG) im Rahmen einer koordinierten Durchsetzungsmassnahme (§ 19 Abs. 5 UWG, Art. 21 VO (EU) 2017/2394): bis 50.000 EUR bzw. bis 4 % des Jahresumsatzes bei Unternehmen ab 1,25 Mio EUR Jahresumsatz

## Pass 10: Social-Media-Verknuepfung

- [ ] Instagram-Shop / Facebook-Shop synchronisiert? — Produktdaten-Austausch via Meta Commerce Manager + JCA Art. 26
- [ ] Pinterest-Tag: nur mit Consent
- [ ] Social-Share-Buttons auf Produkt-Seite: Shariff statt Live-Plugins
- [ ] Eigene Social-Profile mit Impressum-Link + DSE-Link — siehe [[themen/social-media-datenschutz]]

## Pass 11: Fotos im Shop / Persoenlichkeitsrechte

- [ ] **Produktfotos mit Models**: Model-Release-Vertrag + DSGVO-Einwilligung dokumentiert (siehe [[themen/fotos-dritter-kug]])
- [ ] **"Unser Team"-Seite**: wie Landingpage (Pass 10 dort)
- [ ] **Kundenfotos aus Reviews** ("So sieht es an mir aus"): explizite Upload-Lizenz in Review-Bedingungen

## Pass 12: Pressestimmen / Zitate

- [ ] Pressezitate auf Homepage: § 51 UrhG + Quelle — siehe [[themen/zitatrecht]]
- [ ] "Empfohlen von [Influencer]": Werbekennzeichnung (siehe Pass 4 UWG)

## Pass 13: Live-Browser-Check (Shop-kritisch!)

`/legal-audit-live <shop-url>` ist fuer Shops PFLICHT vor Launch:

- [ ] Checkout-Seite: keine Tracker waehrend Kaufabschluss (DSGVO lit. b reicht, aber Analytics = Consent)
- [ ] Produkt-Detail-Seite pre-consent: KEIN Meta Pixel, Google Remarketing, Criteo-Request
- [ ] Button-Loesung: Text enthaelt "zahlungspflichtig" — visuell pruefbar via Screenshot
- [ ] 30-Tage-Tiefstpreis tatsaechlich dargestellt (nicht nur im Schema.org-Markup)
- [ ] Tool-Liste abgleichen mit [[themen/tool-katalog]]

## Typ-spezifische Besonderheiten

- **WooCommerce**: Plugin-Wildwuchs — jedes aktive Plugin pruefen auf Datenabfluss (WooCommerce Google Analytics, Facebook for WooCommerce etc.)
- **Shopware 6**: Built-in-Consent-Manager nutzen oder CMP-Integration (Usercentrics, Cookiebot)
- **Shopify**: US-basiert — AVV mit Shopify International Ltd. (Irland), aber Sub-Prozessoren (CA, US) ueber SCC
- **Headless Commerce** (Shopify + Next.js Frontend): Checkout-Daten bei Shopify, aber Tracking im Frontend — Consent muss beides abdecken
- **Marktplaetze** (eBay, Amazon): Eigene Pflichten — Amazon-AGB, aber trotzdem **eigene** Rechtstexte noetig

## Typische Findings

### CRIT

- 30-Tage-Tiefstpreis-Anzeige fehlt bei reduzierten Artikeln (§ 11 PAngV; EuGH C-330/23; BGH I ZR 183/24)
- Button-Text "Weiter" oder "Bestaetigen" statt "zahlungspflichtig bestellen" (§ 312j Abs. 3 Satz 2 BGB; Folge: Vertrag endgueltig unwirksam, § 312j Abs. 4 BGB, BGH I ZR 159/24)
- Widerrufsbelehrung nicht in Bestaetigungs-Mail als Textform mitgeschickt
- Rechnungs-Archivierung loescht nach 1 Jahr (HGB-Verstoss)
- Meta Pixel ohne Consent + ohne JCA
- BFSG-Barrierefreiheit komplett fehlend bei B2C ab 10 Beschaeftigten oder Umsatz und Bilanzsumme ueber 2 Mio EUR (seit 28.06.2025 in Anwendung)
- Hinweis nach § 5b Abs. 3 UWG fehlt; Echtheitsbehauptung ohne angemessene Pruefung oder gefaelschte Bewertungen (§ 5b Abs. 3, Anhang Nr. 23b, 23c UWG)

### HIGH

- Grundpreisangabe fehlt bei Fertigpackungen
- VSBG-Hinweis fehlt bei mehr als 10 Beschaeftigten (vorher Beschaeftigtenzahl klaeren; ODR-Link nicht mehr Pflicht seit 20.07.2025)
- Fake UVP / Streichpreis ohne Nachweis
- BFSG-Anforderungen teilweise nicht umgesetzt (Alt-Texte, Tastaturfokus)
- Shopify-Hosting ohne erwaehnte SCC-Absicherung
- AI-Chatbot ohne Art. 50 AI Act Transparenz-Hinweis

### MED

- AGB-Klauselkontrolle hat problematische Klauseln ("Haftungsausschluss fuer Folgeschaeden")
- Kundenkonto-Loeschung loest nicht alle Tabellen (Wunschliste, Bewertungs-Historie vergessen)
- Telefonnummer des Kunden als Pflichtfeld (Datenminimierung — meist nicht erforderlich)

### LOW

- Captcha-Tool (Google reCAPTCHA) statt EU-Alternative

## Empfohlene Schutzpakete

- **IT-Recht Kanzlei Muenchen** (it-recht-kanzlei.de) — Starter ~10 EUR / Premium ~25 EUR / Unlimited ~55 EUR pro Monat — siehe [[anwaelte-tools/tools-generatoren]]
- **Haendlerbund** (haendlerbund.de) — Starter ab ca. 9,90 EUR/Monat, Business ab ca. 57,90 EUR/Monat, Professional ab ca. 119,90 EUR/Monat (Anbieterangaben Stand 2026-07-08; Tier-3-Marktinfo, keine Rechtsquelle)
- **Trusted Shops Legal-Texte** (trustedshops.de) — Basis-Rechtstexter kostenlos; kostenpflichtige Abmahnschutz- und Legal-Services-Pakete mit variabler Preisstruktur (Anbieterangaben Stand 2026-07-08; Tier-3-Marktinfo)
- **eRecht24 Premium** (e-recht24.de) ab ~15 EUR/Monat

## Siehe auch

- [[gesetze/pangv]]
- [[gesetze/uwg]] — § 5b Abs. 3 (Bewertungen), § 7 (Direktwerbung)
- [[gesetze/bgb-agb]] — § 312j (Button-Loesung), §§ 305-309 (AGB-Kontrolle), § 355 (Widerruf)
- [[gesetze/dsgvo]]
- [[gesetze/tdddg]]
- [[gesetze/bfsg]] — seit 28.06.2025 anwendbar
- [[gesetze/ai-act]]
- [[themen/preisangaben]]
- [[themen/widerrufsbelehrung]]
- [[themen/button-loesung]]
- [[themen/agb-muster]]
- [[themen/impressum]]
- [[themen/datenschutzerklaerung]]
- [[themen/email-marketing]]
- [[themen/siegel-werbung]]
- [[themen/zitatrecht]]
- [[themen/fotos-dritter-kug]]
- [[themen/social-media-datenschutz]]
- [[themen/tool-katalog]]
- [[urteile/bgh-cookie-einwilligung]]
- [[urteile/bgh-inbox-werbung]]
- [[anwaelte-tools/tools-generatoren]]

---

## Aenderungsvermerk (2026-11-14, Batch F stale-only)

- Frontmatter und Disclaimer-Stand auf 2026-11-14 aktualisiert.
- Pass 4 (Button-Loesung) um Kuendigungsbutton § 312k BGB fuer Abo-/Dauerschuldverhaeltnisse erweitert; Tier-1-belegt gegen gesetze-im-internet.de/bgb/__312k.html.
- **Pass 4 (Widerrufsbelehrung) neu:** Elektronische Widerrufsfunktion nach § 356a BGB (Tier-1 gesetze-im-internet.de/bgb/__356a.html; RL (EU) 2023/2673 per Cellar CELEX:32023L2673 verifiziert — Umsetzung bis 19.12.2025, Anwendung ab 19.06.2026). Gilt NICHT nur fuer Finanzdienstleistungen, sondern fuer alle Fernabsatzvertraege ueber Online-Benutzeroberflaeche.
- Pass 4 (AGB/ODR): Marker am 2026-11-14 aufgeloest. Primaerbeleg VO (EU) 2024/3228 vom 19.12.2024, Art. 1 (CELEX 32024R3228, Cellar-Volltext): Aufhebung VO (EU) 524/2013 mit Wirkung 20.07.2025, Einstellung der OS-Plattform.
- Pass 4 (GPSR): Marker aufgeloest. Primaerquelle Cellar CELEX:32023R0988, Art. 52 "Sie gilt ab dem 13. Dezember 2024" (berichtigt am 2026-11-15; zuvor faelschlich Art. 47, der die Evaluierung regelt). Produktbezogene Fernabsatz-Informationspflichten in Art. 19.
- Pass 4 (EmpCo): Marker aufgeloest. Primaerquelle Cellar CELEX:32024L0825 (Mitgliedstaaten erlassen bis 27.03.2026, Anwendung ab 27.09.2026). Deutsche UWG-Umsetzung Tier-1-belegt via knowledge/gesetze/uwg.md (Gesetz vom 22.10.2026, BGBl. 2026 I Nr. 322, § 15b UWG).
- Bestandspruefung (ausserhalb Pass 5): Normzitate durchgesehen. Berichtigt am 2026-11-15: Die Bestaetigung "alle Pflicht-Normzitate bestaetigt" und "konsistent zu KB" traf nicht zu. "BGH I ZR 183/22 (10.10.2024)" ist nicht belegt (richtig: EuGH C-330/23 und BGH I ZR 183/24 vom 09.10.2025), I ZR 159/24 traegt nicht den Pflichtwortlaut der Schaltflaeche, I ZR 163/19 betrifft geografische Herkunftsangaben und Kollektivmarken; ferner waren u. a. die Aufbewahrungsfristen (§ 257 HGB, § 147 AO), § 5b Abs. 3 UWG, § 36 VSBG und Art. 246 EGBGB ungenau oder falsch wiedergegeben.
- Pass 5 (KI) wurde am selben Tag von einem anderen Agent aktualisiert; hier nicht angetastet.

## Aenderungsvermerk (2026-11-15)

- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1): Aufbewahrungsfristen auf 8/10/6 Jahre berichtigt; 30-Tage-Tiefstpreis mit EuGH C-330/23 und BGH I ZR 183/24 statt I ZR 183/22; I ZR 159/24 nur noch fuer die endgueltige Unwirksamkeit nach § 312j Abs. 4 BGB; Abo-Fallen auf Art. 246a EGBGB; § 312k Abs. 4 "sofort"; VSBG-Ausnahme § 36 Abs. 3; Widerrufsbelehrung in der Fassung seit 19.06.2026; Pruefpunkt harmonisierte Gewaehrleistungsmitteilung (DVO (EU) 2025/1960); GPSR Art. 52 und § 3 Abs. 5 ProdSG eingeordnet; EmpCo-Umsetzung durch G v. 12.02.2026 (BGBl. 2026 I Nr. 43), § 15b UWG nur Uebergangsvorschrift (berichtigt auch den EmpCo-Vermerk oben); Art. 50 Abs. 2 KI-VO als Anbieterpflicht, Shop nur Art. 50 Abs. 4; § 5b Abs. 3 UWG als Informationspflicht; Bussgeld § 19 UWG eingegrenzt; BFSG-Kleinstunternehmen und BFSGV § 3 berichtigt; I ZR 163/19 gestrichen und mit Marker versehen.
