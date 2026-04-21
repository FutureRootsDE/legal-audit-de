---
aktualisiert: 2026-04-19
gilt-fuer: WooCommerce, Shopware 6, Shopify, Magento, PrestaShop, JTL
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. E-Commerce ist abmahnintensiv —
> vor Launch zwingend Pruefung durch einen Fachanwalt fuer IT-/E-Commerce-Recht
> oder ein Schutzpaket (z.B. IT-Recht Kanzlei Muenchen).
>
> **Stand:** 2026-04-19

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

### Preisangabenverordnung (PAngV)

- [ ] **Gesamtpreis inkl. USt** sichtbar (§ 1 PAngV)
- [ ] **Grundpreis** bei Fertigpackungen (EUR/kg, EUR/Liter) — § 4 PAngV
- [ ] **"zzgl. Versand"** Hinweis + Link zur Versandkostenuebersicht
- [ ] **Streichpreis / Reduzierung**: **30-Tage-Tiefstpreis** muss angezeigt werden (§ 11 PAngV neu seit 2022)
- [ ] **Preis je Masseinheit** bei Getraenken, Lebensmitteln, Kosmetik etc.
- [ ] Keine Phantasie-Preise (UVP muss echte Hersteller-UVP sein)
- [ ] [[gesetze/pangv]], [[themen/preisangaben]]

### Widerrufsbelehrung + Widerrufsformular

- [ ] **Muster-Widerrufsbelehrung** nach Anlage 1 zu Art. 246a § 1 Abs. 2 EGBGB
- [ ] **Muster-Widerrufsformular** als PDF oder separate HTML-Seite
- [ ] 14-Tage-Frist korrekt formuliert
- [ ] Ausnahmen konkret aufgelistet (digitaler Content nach Einwilligung, versiegelte Waren, etc. § 312g BGB)
- [ ] Bestaetigungs-Mail nach Kauf enthaelt Widerrufsbelehrung in **Textform** (nicht nur Link!)
- [ ] [[themen/widerrufsbelehrung]]

### Button-Loesung (§ 312j BGB)

- [ ] Bestell-Button-Text: **"zahlungspflichtig bestellen"** oder **"jetzt kaufen"** (klar verpflichtender Wortlaut)
- [ ] Keine kreativen Varianten wie "Bestellung abschicken" oder "Weiter" (abmahnrelevant)
- [ ] Checkout-Seite: Wesentliche Produktmerkmale, Gesamtpreis, Versand, Laufzeit unmittelbar vor dem Button
- [ ] [[themen/button-loesung]]

### AGB

- [ ] **AGB** mit Einbeziehungsklausel im Checkout ("Ich habe die AGB gelesen und akzeptiere sie")
- [ ] Pre-Tick VERBOTEN — User muss aktiv bestaetigen
- [ ] Klauselkontrolle (§§ 305-310 BGB) — keine ueberraschenden oder unklaren Klauseln
- [ ] **Streitbeilegung-Hinweis** nach Art. 14 ODR-VO (Link zu ec.europa.eu/consumers/odr) — Pflicht fuer alle Online-Haendler
- [ ] **VSBG-Hinweis** (§ 36 VSBG): Verbraucherschlichtungsstelle-Bereitschaft JA/NEIN
- [ ] [[themen/agb-muster]]

### Impressum + Datenschutzerklaerung

- [ ] Impressum nach § 5 DDG mit vollen Angaben — [[themen/impressum]]
- [ ] DSE nach Art. 13 DSGVO mit allen Shop-spezifischen Drittanbietern — [[themen/datenschutzerklaerung]]

## Pass 5: KI-Spezifisch

- [ ] KI-Produktempfehlungs-Engine → Einwilligung + ggf. DSFA
- [ ] KI-generierte Produktbeschreibungen → Kennzeichnung empfohlen (insb. bei Bewertungen!)
- [ ] Chatbot mit GPT-Backend → Art. 50 AI Act Transparenzpflicht
- [ ] **Fake Reviews**: §§ 5, 5a UWG — bei KI-generierten Bewertungen klare Kennzeichnung
- [ ] [[gesetze/ai-act]], [[themen/ki-content]]

## Pass 6: Barrierefreiheit (BFSG — gilt fuer E-Commerce B2C zwingend!)

BFSG betrifft Online-Shops ab 2025-06-28 **ausnahmslos** (bei B2C und > 10 MA / > 2 Mio EUR Umsatz).

- [ ] WCAG 2.1 AA
- [ ] Checkout komplett barrierefrei (Tastatur, Screen-Reader)
- [ ] Alt-Texte fuer alle Produktbilder
- [ ] Farbkontrast bei Produkt-Beschriftungen
- [ ] Barrierefreiheitserklaerung
- [ ] [[gesetze/bfsg]]

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
- [ ] **Kundenbewertungen aggregiert** ("4.8 von 5, 1240 Bewertungen"): § 5b UWG — echte Bewertungen, Herkunft klar
- [ ] **Fake-Reviews / KI-generierte Reviews**: §§ 5, 5a UWG — Abmahn- und Bussgeldrisiko

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

- 30-Tage-Tiefstpreis-Anzeige fehlt bei reduzierten Artikeln (PAngV § 11)
- Button-Text "Weiter" oder "Bestaetigen" statt "zahlungspflichtig bestellen"
- Widerrufsbelehrung nicht in Bestaetigungs-Mail als Textform mitgeschickt
- Rechnungs-Archivierung loescht nach 1 Jahr (HGB-Verstoss)
- Meta Pixel ohne Consent + ohne JCA

### HIGH

- Grundpreisangabe fehlt bei Fertigpackungen
- ODR-Link / VSBG-Hinweis fehlt
- Fake UVP / Streichpreis ohne Nachweis
- BFSG-Barrierefreiheit nicht umgesetzt (bei B2C > 10 MA)
- Shopify-Hosting ohne erwaehnte SCC-Absicherung

### MED

- AGB-Klauselkontrolle hat problematische Klauseln ("Haftungsausschluss fuer Folgeschaeden")
- Kundenkonto-Loeschung loest nicht alle Tabellen (Wunschliste, Bewertungs-Historie vergessen)
- Telefonnummer des Kunden als Pflichtfeld (Datenminimierung — meist nicht erforderlich)

### LOW

- Captcha-Tool (Google reCAPTCHA) statt EU-Alternative

## Empfohlene Schutzpakete

- **IT-Recht Kanzlei Muenchen** (it-recht-kanzlei.de) — Starter ~10 EUR / Premium ~25 EUR / Unlimited ~55 EUR pro Monat — siehe [[anwaelte-tools/tools-generatoren]]
- **Haendlerbund** (haendlerbund.de) <<VERIFIKATION AUSSTEHEND>> — Mitglieds-Modell ab ~10 EUR/Monat
- **Trusted Shops Legal-Texte** (trustedshops.de) — Pake ab ~30 EUR/Monat <<UNVERIFIZIERT>>
- **eRecht24 Premium** (e-recht24.de) ab ~15 EUR/Monat

## Siehe auch

- [[gesetze/pangv]]
- [[gesetze/uwg]]
- [[gesetze/bgb-agb]]
- [[gesetze/dsgvo]]
- [[gesetze/tdddg]]
- [[gesetze/bfsg]]
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
