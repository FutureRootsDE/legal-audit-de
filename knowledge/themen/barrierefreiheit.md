---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/bfsg/
quellen-sekundaer:
  - https://www.bundesfachstelle-barrierefreiheit.de/DE/Fachwissen/Produkte-und-Dienstleistungen/Barrierefreiheitsstaerkungsgesetz/FAQ/faq_node.html
  - https://www.w3.org/TR/WCAG22/
  - https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
  - https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/barrierefreiheitsstaerkungsgesetz.html
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

# Barrierefreiheit — BFSG-Scope, WCAG 2.1/2.2 AA & Pflicht-Elemente

## Kurz-Ueberblick

Das **BFSG** (gilt seit 28.06.2025) verpflichtet Anbieter bestimmter B2C-Produkte und -Dienstleistungen zur Barrierefreiheit. Massgeblich ist § 4 BFSG: Bei Einhaltung harmonisierter Normen wird die Konformitaet vermutet. In der Praxis herangezogen werden **EN 301 549** (die ihrerseits auf **WCAG 2.1 Level AA** verweist) und die aktuellere W3C-Empfehlung **WCAG 2.2**; eine Vorgabe der BFSGV sind diese Standards nicht. Ob eine Fassung der EN 301 549 als harmonisierte Norm zur RL (EU) 2019/882 im Amtsblatt der EU veroeffentlicht ist: <<VERIFIKATION AUSSTEHEND>>

**Stand 2026-11-14**: Abmahnungen kommen vor. Die MLBF AoeR (gemeinsame Marktueberwachungsstelle der Laender, Magdeburg) hat zum Jahresbeginn 2026 ihre Raeume bezogen und am 29.01.2026 ihre Marktueberwachungsstrategien beschlossen; ein Beginn aktiver Kontrollen im Januar 2026 ist auf der Behoerdenseite nicht dokumentiert. Bussgeld bis **100.000 EUR**, u. a. wenn eine Dienstleistung entgegen § 14 Abs. 1 angeboten wird (§ 37 Abs. 1 Nr. 8, Abs. 2 BFSG); bis **10.000 EUR** bei Verstoessen gegen Informations- und Auskunftspflichten (z. B. § 14 Abs. 4 Satz 2, Abs. 5 Satz 1). Zur UWG-Abmahnfaehigkeit siehe [[../gesetze/bfsg]].

## BFSG-Scope — wer ist betroffen?

### Betroffene Dienstleistungen (§ 1 Abs. 3 BFSG, B2C-orientiert)

1. **Telekommunikationsdienste** (z. B. Messenger, VoIP)
2. **Elemente von Personenbefoerderungsdiensten** im Luft-, Bus-, Schienen- und Schiffsverkehr (Webseiten, Apps, elektronische Tickets); im Stadt-, Vorort- und Regionalverkehr nur Selbstbedienungsterminals
3. **Bankdienstleistungen fuer Verbraucher** (Online-Banking, Kreditkartenservices)
4. **E-Books und dafuer bestimmte Software**
5. **Dienstleistungen im elektronischen Geschaeftsverkehr (E-Commerce)** — Websites/Apps gegenueber Verbrauchern mit Bestell-/Vertragsabschluss-Funktion

Dienste, die Zugang zu audiovisuellen Mediendiensten bieten, sind keine Dienstleistung nach § 1 Abs. 3 BFSG; erfasst sind insoweit nur Verbraucherendgeraete (§ 1 Abs. 2 Nr. 4 BFSG).

### Betroffene Produkte (§ 1 Abs. 2 BFSG)

- Hardwaresysteme/Betriebssysteme fuer Universalrechner (Smartphones, Laptops)
- Selbstbedienungsterminals, darunter Zahlungsterminals (§ 1 Abs. 2 Nr. 2 Buchst. a BFSG), ATM, Fahrkarten-, Check-in-Automaten
- Verbraucherendgeraete (Telekom, audiovisuell)
- E-Book-Lesegeraete

### Ausnahme: Kleinstunternehmen (§ 3 Abs. 3 BFSG)

**Nur Dienstleistungen, NICHT Produkte**. Beide Bedingungen kumulativ:
- **< 10 Beschaeftigte** UND
- **Jahresumsatz ≤ 2 Mio. EUR** (oder Bilanzsumme ≤ 2 Mio. EUR)

**Beispiele**:

| Mitarbeiter | Jahresumsatz | BFSG-pflichtig? |
|---|---|---|
| 3 | 3 Mio. EUR Umsatz, Bilanzsumme > 2 Mio. EUR | JA (bei Bilanzsumme ≤ 2 Mio. EUR greift die Ausnahme trotz 3 Mio. EUR Umsatz) |
| 15 | 1 Mio. EUR | JA |
| 4 | 0,5 Mio. EUR | Nein (Ausnahme greift) |
| 9 | 1,9 Mio. EUR | Nein (Ausnahme greift) |

**Achtung**: Die Kleinstunternehmen-Ausnahme gilt nicht fuer Produkte. Unabhaengig davon gelten die Ausnahmen nach §§ 16, 17 BFSG: Die Barrierefreiheitsanforderungen gelten nur, soweit sie keine grundlegende Veraenderung der Wesensmerkmale bewirken (§ 16 Abs. 1) und nicht zu einer unverhaeltnismaessigen Belastung nach Anlage 4 fuehren (§ 17 Abs. 1). Voraussetzung ist eine eigene Beurteilung, deren Dokumentation (Aufbewahrung fuenf Jahre, § 17 Abs. 2) und die Unterrichtung der Marktueberwachungsbehoerde.

### B2B-Befreiung

Reine B2B-Dienstleistungen fallen **nicht** unter das BFSG. Entscheidend ist die **Adressatenperspektive**. Bei Mischformen (B2C + B2B) entscheidet der Verbraucher-Aspekt.

## WCAG 2.1 / 2.2 AA — Pflicht-Elemente

In der Praxis wird EN 301 549 herangezogen, die auf WCAG 2.1 AA verweist; eine Vorgabe der BFSGV ist das nicht (zur Konformitaetsvermutung nach § 4 BFSG siehe Kurz-Ueberblick). **WCAG 2.2** hat 9 neue Kriterien; praktisch sollte man auf 2.2 abzielen.

### 4 Prinzipien

1. **Wahrnehmbar (Perceivable)** — Inhalte durch Sinne erfassbar
2. **Bedienbar (Operable)** — Bedienungselemente und Navigation funktionieren
3. **Verstaendlich (Understandable)** — Inhalte und Bedienung
4. **Robust** — Kompatibilitaet mit assistiven Technologien

### Level A und AA — Kern-Erfolgskriterien

**Wahrnehmbar:**
- **1.1.1 Alt-Text** fuer Nicht-Text-Inhalte
- **1.2.2 Untertitel** fuer Audio in Videos
- **1.2.3 Transkript / Audiodeskription**
- **1.2.5 Audiodeskription (aufgezeichnet)**, Stufe AA
- **1.3.1 Informationen und Beziehungen** (Semantik: Ueberschriften, Listen, Tabellen, Labels)
- **1.3.4 Ausrichtung** (kein Zwang zu Landscape/Portrait)
- **1.4.3 Kontrast** 4.5:1 (Normal), 3:1 (Large Text >= 18pt oder 14pt bold)
- **1.4.4 Textgroesse** 200 % ohne Funktionsverlust
- **1.4.10 Reflow** (kein horizontales Scrollen bei 320 CSS-Pixeln)
- **1.4.11 Nicht-Text-Kontrast** 3:1 fuer UI-Komponenten und Grafiken
- **1.4.12 Text-Abstaende** anpassbar
- **1.4.13 Content on Hover/Focus** — muss dismissable, hoverable, persistent sein

**Bedienbar:**
- **2.1.1 Tastatur** — alle Funktionen per Keyboard
- **2.1.2 Keine Tastaturfalle** — Fokus kann aus Element heraus
- **2.4.1 Bloecke umgehen**: Mechanismus zum Ueberspringen wiederholter Inhaltsbloecke (z. B. Skip-Link, Landmarks, Ueberschriftenstruktur)
- **2.4.3 Fokusreihenfolge** logisch
- **2.4.4 Linkzweck** aus Kontext erkennbar
- **2.4.7 Fokus sichtbar**
- **2.4.11 (WCAG 2.2)** — Fokus NICHT verdeckt durch sticky headers etc.
- **2.5.8 Target Size (Minimum)** (WCAG 2.2, AA): Zielgroesse mind. 24x24 CSS-Pixel oder ausreichender Abstand (2.5.5 = AAA, 44x44)
- **2.5.7 Dragging Movements** (WCAG 2.2) — alternative nicht-draggable Bedienung

**Verstaendlich:**
- **3.1.1 Seitensprache** deklariert (`<html lang="de">`)
- **3.1.2 Sprachwechsel** im Content markiert (`<span lang="en">`)
- **3.2.3 Konsistente Navigation**
- **3.3.1 Fehler-Identifikation**
- **3.3.3 Fehlerkorrektur-Vorschlaege**
- **3.3.4 Fehlervermeidung** (rechtliche Verpflichtungen, Finanztransaktionen, Aenderung/Loeschung von Nutzerdaten): mindestens eines von: umkehrbar, auf Fehler geprueft mit Korrekturmoeglichkeit, vor Abschluss ueberpruef-, bestaetig- und korrigierbar
- **3.3.7 Redundante Eingaben (WCAG 2.2)** — bereits eingegebene Daten nicht wiederholt abfragen
- **3.3.8 Accessible Authentication (WCAG 2.2)** — keine kognitiven Puzzles (Captchas, die Denken verlangen)

**Robust:**
- **4.1.2 Name, Role, Value** fuer alle UI-Komponenten (korrektes ARIA, wenn noetig)
- **4.1.3 Status Messages** (per ARIA live region)

## Pflicht-Elemente fuer BFSG-konforme Websites

### 1. Barrierefreiheitserklaerung

Pflichtinhalte: Information nach § 14 Abs. 1 Nr. 2 i. V. m. Anlage 3 Nr. 1 BFSG (in den AGB oder auf andere deutlich wahrnehmbare Weise, selbst barrierefrei; Aufbewahrung nach § 14 Abs. 2):
- a) **allgemeine Beschreibung** der Dienstleistung
- b) **Erlaeuterungen zur Durchfuehrung** der Dienstleistung
- c) Beschreibung, wie die Dienstleistung die **Barrierefreiheitsanforderungen erfuellt**
- d) **zustaendige Marktueberwachungsbehoerde** (MLBF, siehe Behoerden-Hinweise)

Good Practice, gesetzlich nicht vorgeschrieben:
- **Vereinbarkeit** der Website mit den Anforderungen (vollstaendig / teilweise / nicht)
- **Nicht barrierefreie Inhalte** mit Begruendung (z. B. Archiv-PDFs, die vor dem 28.06.2025 veroeffentlicht wurden; Ausnahmen nach § 1 Abs. 4 BFSG pruefen)
- **Erstellungsdatum** der Information
- **Feedback-Kontakt** fuer Barrierefreiheitsbeschwerden

### Ausgenommene Inhalte (§ 1 Abs. 4 BFSG)

§ 1 Abs. 4 Nr. 1 bis 5 BFSG nimmt bestimmte Inhalte aus. Fuer Websites besonders relevant ist Nr. 4: Inhalte Dritter, die vom Dienstleistungserbringer weder finanziert noch entwickelt werden und nicht seiner Kontrolle unterliegen. Die uebrigen Ausnahmen vor Verwendung am Gesetzestext pruefen.

### Uebergangsbestimmungen (§ 38 BFSG)

- **§ 38 Abs. 1**: Uebergang bis 27.06.2030 fuer bereits eingesetzte Produkte und fuer Altvertraege.
- **§ 38 Abs. 2**: Selbstbedienungsterminals laengstens bis 15 Jahre nach ihrer Ingebrauchnahme.
- **Kein allgemeiner Aufschub fuer Websites und Apps**: fuer sie gelten die Anforderungen seit 28.06.2025.

Ueblicher Link: Footer, erreichbar ueber "Barrierefreiheit" oder "Barrierefreiheitserklaerung".

### 2. Skip-Link

```html
<a href="#main" class="skip-link">Zum Hauptinhalt springen</a>
<!-- sichtbar bei Fokus, visuell unauffaellig -->
```

### 3. Semantische HTML-Struktur

- `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`
- Ueberschriftenstruktur programmatisch erkennbar und beschreibend (WCAG 1.3.1, 2.4.6); genau eine `<h1>` je Seite ist bewaehrte Praxis, keine WCAG-Anforderung
- Ueberschriften-Hierarchie ohne Luecken

### 4. Kontrast

- **WCAG AA**: 4.5:1 normaler Text, 3:1 grosser Text
- Tools: axe DevTools, Lighthouse, Contrast Checker

### 5. Formulare

- `<label for="id">` fuer jedes `<input>`
- `aria-describedby` fuer Hilfetexte und Fehlermeldungen
- `aria-invalid="true"` bei Fehlern
- Visueller und programmatischer Fehlerhinweis
- **Autocomplete**-Attribute wo moeglich (WCAG 1.3.5)

### 6. Multimedia

- Untertitel (closed captions)
- Transkript
- Audiodeskription bei visuellen Informationen
- Automatisch abgespieltes Audio ueber 3 Sekunden nur mit Mechanismus zum Anhalten/Stoppen oder zur Lautstaerkeregelung (WCAG 1.4.2)

### 7. Cookie-Banner / Consent-UI

Oft schwere Verstoesse:
- Fokus-Management fehlt
- Ablehnung nicht gleichwertig zur Zustimmung gestaltet (Einwilligungsrecht: § 25 Abs. 1 TDDDG, DSGVO; keine BFSG-Anforderung)
- Schaltflaechen nicht per Tastatur bedienbar (WCAG 2.1.1)

## Typische Fallstricke in Codebases

### Next.js / React / Vue

- **`<div>`-Suppe statt Semantik**
- **`onClick` auf `<div>` ohne `role="button"` und keyboard handler**
- Modal-Dialoge ohne Focus-Trap und ohne `aria-modal`
- Tooltip/Popover als `:hover`-only (keine Tastatur-Erreichbarkeit)
- **Dynamic Content** nicht per `aria-live` angekuendigt
- Icon-Buttons ohne `aria-label` oder `<span class="sr-only">`
- **Dark Mode** mit unzureichendem Kontrast
- **next/image** ohne `alt`
- **Drittanbieter-Widgets** (Chat, Booking, Payment): oft NICHT barrierefrei. Verpflichtet ist der Dienstleistungserbringer (Betreiber der Website), nicht der Widget-Hersteller; ausgenommen sind nur Inhalte Dritter, die der Betreiber weder finanziert noch entwickelt noch kontrolliert (§ 1 Abs. 4 Nr. 4 BFSG)

### E-Commerce spezifisch

- **Checkout** ueber mehrere Steps ohne Fortschrittsanzeige
- **Payment-iframe** (Stripe/PayPal) nicht getestet mit Screenreader
- **Produkt-Varianten-Selektor** (Farbe/Groesse) ohne zugaengliche Labels
- **Warenkorb-Update** nicht angekuendigt
- **AGB-Checkbox** zu klein, ohne Label-Verknuepfung

### n8n-Portale / SaaS-Interfaces

- Haeufig **B2B** und daher nicht vom BFSG erfasst (§ 1 Abs. 3 BFSG: "fuer Verbraucher"); BITV 2.0 gilt fuer oeffentliche Stellen des Bundes (§ 12 BGG), fuer Laender und Kommunen gilt Landesrecht; sonst Good Practice
- Drag-and-Drop Workflows ohne Tastatur-Alternative

## Relevanz fuer Codebase-Typen

- **Next.js SaaS (B2C)**: **hochrelevant**, volle BFSG-Pflicht wenn nicht Kleinstunternehmen
- **Next.js SaaS (B2B only)**: Nicht BFSG; optional BITV, ISO 30071-1, internationale Maerkte
- **Landingpage (rein Werbe, keine Transaktion)**: typischerweise nicht BFSG, aber Good Practice
- **n8n Kundenportal (B2C)**: BFSG-pflichtig, wenn es eine Dienstleistung nach § 1 Abs. 3 BFSG ist (insbesondere elektronischer Geschaeftsverkehr, § 1 Abs. 3 Nr. 5 i. V. m. § 2 Nr. 26) und keine Kleinstunternehmen-Ausnahme (§ 3 Abs. 3) greift
- **E-Commerce** gegenueber Verbrauchern: pflichtig (§ 1 Abs. 3 Nr. 5 BFSG), ausser Kleinstunternehmen (§ 3 Abs. 3 BFSG)
- **Content/Blog**: Nicht im Kern betroffen, aber WCAG-Compliance ist SEO-/Reichweite-Faktor

## Behoerden-Hinweise

- **Bundesfachstelle Barrierefreiheit** (FAQ, Praxishilfen): https://www.bundesfachstelle-barrierefreiheit.de/
- **Marktueberwachung**: MLBF AoeR (Magdeburg), gemeinsame Stelle aller 16 Laender (mlbf-barrierefrei.de); in der Information nach Anlage 3 Nr. 1 Buchst. d BFSG anzugeben
- **Verbraucher- und Verbandsantrag (§ 32 BFSG)**: Verbraucher koennen bei der Marktueberwachungsbehoerde beantragen, gegen einen Verstoss einzuschreiten (§ 32 Abs. 1 BFSG); Antragsweg ueber die MLBF
- **Bundesfachstelle Barrierefreiheit** (§ 13 Abs. 2 BGG: Erstberatung, auf Anfrage auch fuer die Wirtschaft); die Ueberwachungsstelle des Bundes fuer Barrierefreiheit von Informationstechnik (§ 13 Abs. 3 BGG) prueft nur oeffentliche Stellen des Bundes, nicht BFSG-Pflichtige
- **Meldepflicht und Stichproben**: Genuegt die Dienstleistung den Barrierefreiheitsanforderungen nicht, informiert der Dienstleistungserbringer unverzueglich die Marktueberwachungsbehoerde (§ 14 Abs. 4 Satz 2 BFSG); der Verstoss ist bussgeldbewehrt (§ 37 Abs. 1 Nr. 2 BFSG). Die Marktueberwachungsbehoerde prueft Dienstleistungen auch ohne konkreten Anlass anhand angemessener Stichproben (§ 28 Abs. 2 BFSG).

## Zitierbare Urteile

**Stand 2026-11-14: weiterhin keine hoechstrichterliche BFSG-Rechtsprechung** zur UWG-Abmahnfaehigkeit dokumentiert. Abmahnungen kommen vor. Erste OLG/BGH-Endurteile zu § 3a UWG i.V.m. BFSG sind fuer 2027 zu erwarten; naechste Pruefung: 2027-02. <<VERIFIKATION AUSSTEHEND>>

Relevant aus Nachbargebieten:
- **LSG Nordrhein-Westfalen, Urt. v. 29.10.2019 — L 13 SB 55/19** <<VERIFIKATION AUSSTEHEND>> (zu Barrierefreiheit im weiteren Sinne)

US-Parallele: **Robles v. Dominos Pizza** (9th Cir. 2019) — ADA Title III fuer Websites.

## Siehe auch

- [[../gesetze/bfsg]]
- [[../gesetze/dsa]] — Art. 14 Abs. 1 DSA verlangt von Anbietern von Vermittlungsdiensten AGB in "klarer, einfacher, verstaendlicher, benutzerfreundlicher und eindeutiger Sprache" (nur Vermittlungsdienste, keine BFSG-Pflicht)
- [[ki-transparenz]] — Art. 50 Abs. 5 AI Act verlangt zugaengliche Kennzeichnung

## Aenderungsvermerk 2026-11-14

- Frontmatter-Daten und Disclaimer-Stand auf 2026-11-14.
- 2026-11-14: geprueft am Primaertext BFSG
  (gesetze-im-internet.de/bfsg/BJNR297010021.html) und am
  Anwendungsstichtag 28.06.2025; § 1 (Anwendungsbereich), § 2 Nr. 17
  und § 3 Abs. 3 (Kleinstunternehmen), § 14 mit Anlage 3
  (Dienstleistungsanforderungen, Information), § 37 (Bussgeld) und § 38
  (Uebergang) im Volltext bestaetigt. (Berichtigt am 2026-11-15: die
  fruehere Fassung nannte die URL BJNR097010021 und ordnete §§ 3, 14, 37
  falsch zu.)
- Platzhalter zur BFSG-Rechtsprechung (§ 3a UWG i.V.m. BFSG) bleibt bestehen:
  gezielte Suche nach ersten OLG/BGH-Endurteilen ergab bis 2026-11-14 keinen
  belastbaren Tier-1-Treffer; Marker normalisiert, naechste Pruefung
  2027-02.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  EN 301 549 / WCAG nicht mehr als Vorgabe der BFSGV, sondern als
  Praxisstandard mit Verweis auf § 4 BFSG (Amtsblatt-Listung offen, Marker);
  Bussgeldrahmen nach § 37 differenziert; Personenbefoerderung praezisiert,
  "Zugang zu audiovisuellen Medien" als Dienstleistung gestrichen,
  Zahlungsterminals ergaenzt; §§ 16, 17 statt "nie befreit"; WCAG 2.5.8
  statt 2.5.5; Pflichtinformation nach § 14 i. V. m. Anlage 3 Nr. 1;
  Abschnitte zu § 1 Abs. 4 und § 38 ergaenzt; Widget-Pflicht beim
  Dienstleistungserbringer; MLBF als Marktueberwachung; § 32 BFSG.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2):
  Meldepflicht (§ 14 Abs. 4 Satz 2) und Stichproben (§ 28 Abs. 2) ergaenzt;
  Kleinstunternehmen-Beispiel mit Bilanzsumme; WCAG-Kriterien 1.2.5, 2.4.1,
  3.3.4, 1.4.2 und h1-Hinweis berichtigt; Consent-UI ohne BFSG-Zuordnung der
  Gleichwertigkeit; B2B/BITV, Kundenportal und E-Commerce an § 1 Abs. 3
  ausgerichtet; Bundesfachstelle und Ueberwachungsstelle (§ 13 BGG);
  Art. 14 Abs. 1 DSA praezisiert; Kontrollbeginn laut MLBF-Seite praezisiert;
  Kanzleinamen gestrichen; LSG-Aktenzeichen mit Marker versehen.
