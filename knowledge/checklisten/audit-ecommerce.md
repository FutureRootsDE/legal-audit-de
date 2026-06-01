---
aktualisiert: 2026-06-01
gilt-fuer: WooCommerce, Shopware 6, Shopify, Magento, PrestaShop, JTL
verifiziert-am: 2026-06-01
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. E-Commerce ist abmahnintensiv —
> vor Launch zwingend Pruefung durch einen Fachanwalt fuer IT-/E-Commerce-Recht
> oder ein Schutzpaket (z.B. IT-Recht Kanzlei Muenchen).
>
> **Stand:** 2026-05-08

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
  - BGH I ZR 183/22 (10.10.2024) "Aldi-Preisangabe" — auch bei Werbung mit prozentualem Rabatt muss der niedrigste Preis der letzten 30 Tage Bezugspunkt sein
- [ ] **Preis je Masseinheit** bei Getraenken, Lebensmitteln, Kosmetik etc.
- [ ] Keine Phantasie-Preise (UVP muss echte Hersteller-UVP sein, § 5 UWG)
- [ ] [[gesetze/pangv]], [[themen/preisangaben]]

### Widerrufsbelehrung + Widerrufsformular

- [ ] **Muster-Widerrufsbelehrung** nach Anlage 1 zu Art. 246a § 1 Abs. 2 EGBGB
- [ ] **Muster-Widerrufsformular** als PDF oder separate HTML-Seite
- [ ] 14-Tage-Frist korrekt formuliert
- [ ] Ausnahmen konkret aufgelistet (digitaler Content nach Einwilligung, versiegelte Waren, etc. § 312g BGB)
- [ ] Bestaetigungs-Mail nach Kauf enthaelt Widerrufsbelehrung in **Textform** (nicht nur Link!)
- [ ] [[themen/widerrufsbelehrung]]

### Button-Loesung (§ 312j Abs. 3 BGB)

- [ ] Bestell-Button-Text: **"zahlungspflichtig bestellen"** oder gleichbedeutender Wortlaut (z.B. "jetzt kaufen", "kostenpflichtig bestellen")
- [ ] Keine kreativen Varianten wie "Bestellung abschicken", "Weiter", "Anmelden" (abmahnrelevant; bei Verstoss kommt kein Vertrag zustande, § 312j Abs. 4 BGB)
- [ ] **BGH I ZR 159/24 (09.10.2025)**: bei mehrstufigen Bestell-Flows muss der Pflichtwortlaut auf dem **finalen** Button stehen, der die Zahlungspflicht ausloest — nicht auf einem vorherigen Schritt
- [ ] Checkout-Seite: Wesentliche Produktmerkmale, Gesamtpreis, Versand, Laufzeit unmittelbar vor dem Button (§ 312j Abs. 2 BGB)
- [ ] **Abo-Fallen** (Art. 246 § 1 EGBGB): bei wiederkehrenden Leistungen Mindestlaufzeit + Gesamtkosten transparent
- [ ] [[themen/button-loesung]]

### AGB

- [ ] **AGB** mit Einbeziehungsklausel im Checkout ("Ich habe die AGB gelesen und akzeptiere sie")
- [ ] Pre-Tick VERBOTEN — User muss aktiv bestaetigen
- [ ] Klauselkontrolle (§§ 305-309 BGB) — keine ueberraschenden oder unklaren Klauseln
- [ ] **Streitbeilegung-Hinweis** nach Art. 14 ODR-VO (Link zu ec.europa.eu/consumers/odr) — **ACHTUNG**: ODR-Plattform der EU wurde **20.07.2025 abgeschaltet** (VO (EU) 2024/3228); Pflicht zur Verlinkung **entfaellt** seitdem; alte AGB-Klauseln zu ODR ueberpruefen und entfernen <<VERIFIKATION durch Fachanwalt empfohlen>>
- [ ] **VSBG-Hinweis** (§ 36 VSBG): Verbraucherschlichtungsstelle-Bereitschaft JA/NEIN — bleibt unveraendert Pflicht
- [ ] [[themen/agb-muster]], [[gesetze/bgb-agb]]

### Impressum + Datenschutzerklaerung

- [ ] Impressum nach § 5 DDG mit vollen Angaben — [[themen/impressum]]
- [ ] DSE nach Art. 13 DSGVO mit allen Shop-spezifischen Drittanbietern — [[themen/datenschutzerklaerung]]

## Pass 5: KI-Spezifisch (AI Act-Stufung)

Anwendbarkeit-Stufung: Verbotene Praktiken (Art. 5) seit **02.02.2025**, KI-Kompetenz (Art. 4) seit **02.02.2025**, GPAI-Pflichten seit **02.08.2025**, Vollanwendung ab **02.08.2026**.

- [ ] **KI-Kompetenz** Art. 4 AI Act: Schulungsnachweis fuer Mitarbeiter mit KI-Beruehrung
- [ ] KI-Produktempfehlungs-Engine → Einwilligung + ggf. DSFA
- [ ] KI-generierte Produktbeschreibungen → Kennzeichnung empfohlen (insb. bei Bewertungen!)
- [ ] Chatbot mit GPT/Claude-Backend → Art. 50 Abs. 1 AI Act Transparenzpflicht ("Sie interagieren mit einer KI")
- [ ] KI-generierte Produktbilder → Kennzeichnung Art. 50 Abs. 2 AI Act (Wasserzeichen ab 02.08.2026)
- [ ] **Fake Reviews**: §§ 5, 5a UWG sowie § 5b Abs. 3 UWG (Pflicht zur Echtheits-Verifikation) — bei KI-generierten Bewertungen klare Kennzeichnung
- [ ] [[gesetze/ai-act]], [[themen/ki-content]], [[themen/ki-transparenz]]

## Pass 6: Barrierefreiheit (BFSG — seit 28.06.2025 anwendbar — fuer B2C-E-Commerce zwingend!)

BFSG ist **seit 28.06.2025 in Anwendung**. Es betrifft B2C-Online-Shops, sofern nicht Kleinstunternehmen-Ausnahme greift (< 10 MA UND < 2 Mio EUR Jahresumsatz/Bilanzsumme).

- [ ] **Anwendungsbereich** geprueft (§ 1 BFSG): B2C-Shop? Kleinstunternehmen-Ausnahme dokumentiert?
- [ ] WCAG 2.1 AA (BFSGV § 3 setzt EN 301 549 um)
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

- [ ] **Rechnungen** → 10 Jahre (§ 257 HGB, § 147 AO)
- [ ] **Bestelldaten** (fuer Garantie/Gewaehrleistung) → typ. 3 Jahre (Verjaehrung) + 10 Jahre fuer Buchhaltungs-relevante Teile
- [ ] **Kunden-Konten**: Loeschung auf Wunsch, aber Buchhaltungsdaten anonymisieren statt loeschen
- [ ] **Server-Logs** wie SaaS (7-14 Tage IP)
- [ ] **Payment-Transaction-Logs** — nach Payment-Provider-Vorgabe, meist 10 Jahre
- [ ] **Newsletter** — bei Abmeldung sofort deaktivieren, aber Double-Opt-In-Log archivieren

## Pass 9: Trust-Badges / Siegel / Bewertungs-Widgets

E-Commerce lebt von Trust-Signalen — Abmahn-HOT-Zone. Siehe [[themen/siegel-werbung]].

- [ ] **Trusted Shops / eKomi / Trustpilot**: Lizenz aktiv, Zertifikat nachpruefbar; Widget laedt erst nach Consent (oft JS-Abhaengig)
- [ ] **"TUeV-geprueft" / "DEKRA-zertifiziert"**: gueltiges Zertifikat, Pruef-Nummer verlinkt
- [ ] **Stiftung-Warentest-/OEKO-TEST-Logos**: Lizenz-Vertrag, korrektes Heft/Jahr, konkrete Produktbewertung
- [ ] **"Testsieger 2023"** ohne Monat/Heft: abmahnbar (BGH I ZR 163/19)
- [ ] **Eigene "Bestseller"-/"Beliebt"-Badges**: Bewertungsgrundlage transparent (keine reinen Marketing-Behauptungen)
- [ ] **Kundenbewertungen aggregiert** ("4.8 von 5, 1240 Bewertungen"): § 5b Abs. 3 UWG (seit Omnibus-RL 2022) — Pflicht zur Sicherstellung der Echtheit; Methode der Verifikation transparent angeben
- [ ] **Fake-Reviews / KI-generierte Reviews**: §§ 5, 5a UWG, § 5b Abs. 3 UWG — Abmahn- und Bussgeldrisiko (bis 50.000 EUR bei Verbraucherinteressen-Verletzung, § 19 UWG)

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

- 30-Tage-Tiefstpreis-Anzeige fehlt bei reduzierten Artikeln (§ 11 PAngV; BGH I ZR 183/22)
- Button-Text "Weiter" oder "Bestaetigen" statt "zahlungspflichtig bestellen" (§ 312j Abs. 3 BGB; BGH I ZR 159/24)
- Widerrufsbelehrung nicht in Bestaetigungs-Mail als Textform mitgeschickt
- Rechnungs-Archivierung loescht nach 1 Jahr (HGB-Verstoss)
- Meta Pixel ohne Consent + ohne JCA
- BFSG-Barrierefreiheit komplett fehlend bei B2C > 10 MA (seit 28.06.2025 in Anwendung)
- KI-/Fake-Reviews ohne Echtheits-Verifikation (§ 5b Abs. 3 UWG)

### HIGH

- Grundpreisangabe fehlt bei Fertigpackungen
- VSBG-Hinweis fehlt (ODR-Link nicht mehr Pflicht seit 20.07.2025)
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

- **IT-Recht Kanzlei Muenchen** (it-recht-kanzlei.de) — Starter ~10 EUR / Premium ~25 EUR / Unlimited ~55 EUR pro Monat (Stand 06/2026; Preise ohne Gewaehr — Anbieter-Website maassgeblich) — siehe [[anwaelte-tools/tools-generatoren]]
- **Haendlerbund** (haendlerbund.de) — Mitglieds-Modell, Basic-Paket ab ~10 EUR/Monat, Premium ab ~30 EUR/Monat (Stand 06/2026; Preise ohne Gewaehr — Anbieter-Website maassgeblich; Mindestlaufzeit 12 Monate)
- **Trusted Shops Legal Services** (trustedshops.de / legal.trustedshops.com) — Pakete Legal Essential / Premium / Enterprise / Ultimate; Einstieg (Essential) am Markt mit ca. 50 EUR/Monat berichtet, hoehere Tarife auf Anfrage (Stand 06/2026 nicht vollstaendig oeffentlich; Anbieter-Website / Individualangebot maassgeblich; 12 Monate Mindestlaufzeit)
- **eRecht24 Premium** (e-recht24.de) — ab ~15 EUR/Monat bei Jahreszahlung, ~30 EUR/Monat bei monatlicher Zahlung (Stand 06/2026; Preise ohne Gewaehr — Anbieter-Website maassgeblich)

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
