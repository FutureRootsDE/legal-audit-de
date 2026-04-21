---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/bfsg/
quellen-sekundaer:
  - https://www.bundesfachstelle-barrierefreiheit.de/DE/Fachwissen/Produkte-und-Dienstleistungen/Barrierefreiheitsstaerkungsgesetz/FAQ/faq_node.html
  - https://www.w3.org/TR/WCAG22/
  - https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
  - https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/barrierefreiheitsstaerkungsgesetz.html
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# Barrierefreiheit — BFSG-Scope, WCAG 2.1/2.2 AA & Pflicht-Elemente

## Kurz-Ueberblick

Das **BFSG** (gilt seit 28.06.2025) verpflichtet Anbieter bestimmter B2C-Produkte und -Dienstleistungen zur Barrierefreiheit. Technische Referenz sind die **harmonisierten Normen**, insbesondere **EN 301 549** (die ihrerseits auf **WCAG 2.1 Level AA** verweist; **WCAG 2.2** ist die aktuellere W3C-Empfehlung).

**Stand 2026-04**: Abmahnwellen durch spezialisierte Kanzleien sind in vollem Gange; Marktueberwachungsbehoerden der Laender fuehren erste Kontrollen durch. Bussgelder bis **100.000 EUR** pro Verstoss.

## BFSG-Scope — wer ist betroffen?

### Betroffene Dienstleistungen (§ 1 Abs. 3 BFSG, B2C-orientiert)

1. **Telekommunikationsdienste** (z. B. Messenger, VoIP)
2. **Elemente von Personenbefoerderung** (Webseiten, Apps, elektronische Tickets)
3. **Bankdienstleistungen fuer Verbraucher** (Online-Banking, Kreditkartenservices)
4. **E-Books und dafuer bestimmte Software**
5. **Dienstleistungen im elektronischen Geschaeftsverkehr (E-Commerce)** — Websites/Apps gegenueber Verbrauchern mit Bestell-/Vertragsabschluss-Funktion
6. **Zugang zu audiovisuellen Medien**

### Betroffene Produkte (§ 1 Abs. 2 BFSG)

- Hardwaresysteme/Betriebssysteme fuer Universalrechner (Smartphones, Laptops)
- Selbstbedienungsterminals (ATM, Fahrkarten-, Check-in-Automaten)
- Verbraucherendgeraete (Telekom, audiovisuell)
- E-Book-Lesegeraete

### Ausnahme: Kleinstunternehmen (§ 3 Abs. 3 BFSG)

**Nur Dienstleistungen, NICHT Produkte**. Beide Bedingungen kumulativ:
- **< 10 Beschaeftigte** UND
- **Jahresumsatz ≤ 2 Mio. EUR** (oder Bilanzsumme ≤ 2 Mio. EUR)

**Beispiele**:

| Mitarbeiter | Jahresumsatz | BFSG-pflichtig? |
|---|---|---|
| 3 | 3 Mio. EUR | JA |
| 15 | 1 Mio. EUR | JA |
| 4 | 0,5 Mio. EUR | Nein (Ausnahme greift) |
| 9 | 1,9 Mio. EUR | Nein (Ausnahme greift) |

**Achtung**: Wer Produkte in Verkehr bringt, ist nie befreit.

### B2B-Befreiung

Reine B2B-Dienstleistungen fallen **nicht** unter das BFSG. Entscheidend ist die **Adressatenperspektive**. Bei Mischformen (B2C + B2B) entscheidet der Verbraucher-Aspekt.

## WCAG 2.1 / 2.2 AA — Pflicht-Elemente

Das BFSG verweist ueber die BFSGV auf EN 301 549, die wiederum auf WCAG 2.1 AA verweist. **WCAG 2.2** hat 9 neue Kriterien; praktisch sollte man auf 2.2 abzielen.

### 4 Prinzipien

1. **Wahrnehmbar (Perceivable)** — Inhalte durch Sinne erfassbar
2. **Bedienbar (Operable)** — Bedienungselemente und Navigation funktionieren
3. **Verstaendlich (Understandable)** — Inhalte und Bedienung
4. **Robust** — Kompatibilitaet mit assistiven Technologien

### Level AA — Kern-Erfolgskriterien

**Wahrnehmbar:**
- **1.1.1 Alt-Text** fuer Nicht-Text-Inhalte
- **1.2.2 Untertitel** fuer Audio in Videos
- **1.2.3 Transkript / Audiodeskription**
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
- **2.4.1 Skip-Link** zum Hauptinhalt (Block Bypass)
- **2.4.3 Fokusreihenfolge** logisch
- **2.4.4 Linkzweck** aus Kontext erkennbar
- **2.4.7 Fokus sichtbar**
- **2.4.11 (WCAG 2.2)** — Fokus NICHT verdeckt durch sticky headers etc.
- **2.5.5** — Klickflaechen mind. 24x24 CSS-Pixel (WCAG 2.2: Zielgroesse)
- **2.5.7 Dragging Movements** (WCAG 2.2) — alternative nicht-draggable Bedienung

**Verstaendlich:**
- **3.1.1 Seitensprache** deklariert (`<html lang="de">`)
- **3.1.2 Sprachwechsel** im Content markiert (`<span lang="en">`)
- **3.2.3 Konsistente Navigation**
- **3.3.1 Fehler-Identifikation**
- **3.3.3 Fehlerkorrektur-Vorschlaege**
- **3.3.4 Fehlervermeidung** (bei Rechts-/Finanz-/Datenverarbeitung: Aufhebungs-/Aenderungsfunktion)
- **3.3.7 Redundante Eingaben (WCAG 2.2)** — bereits eingegebene Daten nicht wiederholt abfragen
- **3.3.8 Accessible Authentication (WCAG 2.2)** — keine kognitiven Puzzles (Captchas, die Denken verlangen)

**Robust:**
- **4.1.2 Name, Role, Value** fuer alle UI-Komponenten (korrektes ARIA, wenn noetig)
- **4.1.3 Status Messages** (per ARIA live region)

## Pflicht-Elemente fuer BFSG-konforme Websites

### 1. Barrierefreiheitserklaerung

Pflichtinhalte (nach BFSG + BFSGV):
- **Vereinbarkeit** der Website mit den Anforderungen (vollstaendig / teilweise / nicht)
- **Nicht barrierefreie Inhalte** mit Begruendung (z. B. "Archiv-PDFs vor 2020")
- **Erstellung** der Erklaerung (Datum, Methode: Selbst- oder Fremdbewertung)
- **Feedback-Kontakt** fuer Barrierefreiheitsbeschwerden
- **Durchsetzungsverfahren** / zustaendige Marktueberwachungsbehoerde

Ueblicher Link: Footer, erreichbar ueber "Barrierefreiheit" oder "Barrierefreiheitserklaerung".

### 2. Skip-Link

```html
<a href="#main" class="skip-link">Zum Hauptinhalt springen</a>
<!-- sichtbar bei Fokus, visuell unauffaellig -->
```

### 3. Semantische HTML-Struktur

- `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`
- Genau **eine** `<h1>` pro Seite
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
- Kein auto-play mit Audio

### 7. Cookie-Banner / Consent-UI

Oft schwere Verstoesse:
- Fokus-Management fehlt
- "Akzeptieren"-Button per Tastatur schwer erreichbar
- Zustimmung und Ablehnung gleichwertig gestaltet (DSGVO + BFSG)

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
- **Drittanbieter-Widgets** (Chat, Booking, Payment) — oft NICHT barrierefrei; Anbieter-Pflicht nach § 14 BFSG

### E-Commerce spezifisch

- **Checkout** ueber mehrere Steps ohne Fortschrittsanzeige
- **Payment-iframe** (Stripe/PayPal) nicht getestet mit Screenreader
- **Produkt-Varianten-Selektor** (Farbe/Groesse) ohne zugaengliche Labels
- **Warenkorb-Update** nicht angekuendigt
- **AGB-Checkbox** zu klein, ohne Label-Verknuepfung

### n8n-Portale / SaaS-Interfaces

- Haeufig **B2B** und daher BFSG-frei, aber BITV 2.0 fuer oeffentliche Stellen; auch Good Practice
- Drag-and-Drop Workflows ohne Tastatur-Alternative

## Relevanz fuer Codebase-Typen

- **Next.js SaaS (B2C)**: **hochrelevant**, volle BFSG-Pflicht wenn nicht Kleinstunternehmen
- **Next.js SaaS (B2B only)**: Nicht BFSG; optional BITV, ISO 30071-1, internationale Maerkte
- **Landingpage (rein Werbe, keine Transaktion)**: typischerweise nicht BFSG, aber Good Practice
- **n8n Kundenportal (B2C)**: BFSG-pflichtig
- **E-Commerce**: Voll pflichtig; **abmahnrisikoreich**
- **Content/Blog**: Nicht im Kern betroffen, aber WCAG-Compliance ist SEO-/Reichweite-Faktor

## Behoerden-Hinweise

- **Bundesfachstelle Barrierefreiheit** (FAQ, Praxishilfen): https://www.bundesfachstelle-barrierefreiheit.de/
- **Marktueberwachung Laender**: Zustaendige Behoerde je nach Bundesland (z. B. Regierung von Mittelfranken fuer Bayern; Bezirksregierung Arnsberg fuer NRW)
- **BITV-Beratungsstelle** (fuer oeffentliche Stellen, nicht BFSG direkt)

## Zitierbare Urteile

**Noch keine hoechstrichterliche BFSG-Rechtsprechung**. `<<VERIFIKATION AUSSTEHEND>>` — erste OLG/BGH-Entscheidungen zu UWG-Abmahnfaehigkeit und Bussgeldern sollten beim naechsten Update geprueft werden.

Relevant aus Nachbargebieten:
- **LSG Nordrhein-Westfalen, Urt. v. 29.10.2019 — L 13 SB 55/19** (zu Barrierefreiheit im weiteren Sinne)

US-Parallele: **Robles v. Dominos Pizza** (9th Cir. 2019) — ADA Title III fuer Websites.

## Siehe auch

- [[../gesetze/bfsg]]
- [[../gesetze/dsa]] — Art. 14 DSA verlangt ebenfalls "verstaendliche" AGB
- [[ki-transparenz]] — Art. 50 Abs. 5 AI Act verlangt zugaengliche Kennzeichnung
