---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/bfsg/
quellen-sekundaer:
  - https://www.bundesfachstelle-barrierefreiheit.de/DE/Fachwissen/Produkte-und-Dienstleistungen/Barrierefreiheitsstaerkungsgesetz/FAQ/faq_node.html
  - https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/barrierefreiheitsstaerkungsgesetz.html
  - https://www.bundesregierung.de/breg-de/aktuelles/barrierefreiheitsstaerkungsgesetz-2353790
verifiziert-am: 2026-04-19
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# Barrierefreiheitsstaerkungsgesetz (BFSG)

## Kurz-Ueberblick

Das BFSG setzt die **EU-Richtlinie 2019/882** (European Accessibility Act, EAA) in deutsches Recht um. Es ist am **28.06.2025** in Kraft getreten und verpflichtet Hersteller und Dienstleister, bestimmte Produkte und Dienstleistungen **barrierefrei** zu gestalten.

**Kernaussage:** Wer B2C-Produkte (z. B. Notebooks, Smartphones, Geldautomaten) oder B2C-Dienstleistungen (insb. **E-Commerce, SaaS, Banking, Messenger, E-Book-Reader**) anbietet, muss WCAG-konforme Barrierefreiheit gewaehrleisten — ausser er faellt unter die Kleinstunternehmen-Ausnahme.

**Stand 2026-04:** Aktive Marktueberwachung laeuft. **Abmahnwellen** seit Sommer 2025 (CLAIM Rechtsanwalts GmbH) und erneute Welle seit Februar 2026 (Kanzlei MK Berlin). Bussgelder bis **100.000 EUR** moeglich. Ob UWG-Abmahnungen dogmatisch haltbar sind, ist **noch nicht hoechstrichterlich geklaert** (Stand Maerz 2026).

## Schluesselparagraphen / Kernaussagen

### § 1 BFSG — Anwendungsbereich

**Produkte** (§ 1 Abs. 2): Hardwaresysteme/Betriebssysteme fuer Universalrechner, Selbstbedienungsterminals (Geldautomaten, Fahrkartenautomaten, Check-in-Automaten), Verbraucherendgeraete fuer Telekommunikation/audiovisuelle Medien, E-Book-Lesegeraete.

**Dienstleistungen** (§ 1 Abs. 3):
- Telekommunikationsdienste
- Elemente von Personenbefoerderungsdiensten (Websites, mobile Apps, elektronische Tickets, Reiseinformationen)
- Bankdienstleistungen fuer Verbraucher
- **E-Books und dafuer bestimmte Software**
- **Dienstleistungen im elektronischen Geschaeftsverkehr (E-Commerce)** — Websites, mobile Apps, elektronische Bestellvorgaenge **gegenueber Verbrauchern**
- **Zugang zu audiovisuellen Medien**

### § 3 BFSG — Barrierefreiheit; Grundanforderungen

Definition Barrierefreiheit: "**Auffindbarkeit, Zugaenglichkeit und Nutzbarkeit** fuer Menschen mit Behinderungen in der allgemein ueblichen Weise, ohne besondere Erschwernis und grundsaetzlich ohne fremde Hilfe."

Konkrete Anforderungen: **BFSGV (Durchfuehrungsverordnung)** verweist auf **harmonisierte Normen**, insbesondere **EN 301 549** (die ihrerseits auf **WCAG 2.1 Level AA** verweist). Praktisch gilt fuer Websites also **WCAG 2.1 AA** (ab WCAG 2.2 empfohlen).

### Kleinstunternehmen-Ausnahme (§ 3 Abs. 3 BFSG)

**Nur fuer Dienstleistungen**, NICHT fuer Produkte:

Kleinstunternehmen = weniger als **10 Beschaeftigte UND** Jahresumsatz **hoechstens 2 Mio. EUR** (oder Jahresbilanzsumme hoechstens 2 Mio. EUR).

**Beide Bedingungen** muessen **gleichzeitig** erfuellt sein.

Beispiele:
- 3 Mitarbeiter, 3 Mio. EUR Umsatz → **NICHT befreit**
- 15 Mitarbeiter, 1 Mio. EUR Umsatz → **NICHT befreit**
- 4 Mitarbeiter, 500.000 EUR Umsatz → **befreit**

**Wichtig**: Kleinstunternehmen, die **Produkte** in Verkehr bringen, sind **nie** befreit.

### § 14/15 BFSG — Pflichten der Dienstleister

Dienstleister muessen:
- Barrierefreie Gestaltung nach Grundanforderungen
- **Informationen ueber Funktionsweise der Barrierefreiheit** bereitstellen
- Informationen **gemeinsam mit oder in der Dienstleistung** verfuegbar
- Bei Verstoessen: **Abhilfe schaffen** oder Dienstleistung einstellen

### § 16/17 BFSG — Barrierefreiheitserklaerung (sinngemaess, exakter §-Bezug je nach Fassung)

Pflicht zur Veroeffentlichung einer **Barrierefreiheitserklaerung** mit:
- Beschreibung, wie Barrierefreiheit erreicht wird
- Kontaktmoeglichkeit fuer Barrierefreiheitsbeschwerden
- Hinweis auf Marktueberwachungsbehoerde

### § 37 BFSG — Bussgelder

Bis **100.000 EUR** pro Verstoss. Zustaendig: Marktueberwachungsbehoerden der Laender.

## Typische Fallstricke in Codebases

- **Kein Skip-Link** zum Hauptinhalt (WCAG 2.4.1)
- **Keine oder falsche Alt-Texte** auf Bildern (WCAG 1.1.1)
- **Formulare ohne Labels** bzw. nicht mit `for`/`id` verknuepft (WCAG 1.3.1)
- **Kontrast unzureichend** (4.5:1 Body, 3:1 Large Text; WCAG 1.4.3)
- **Fokus-Sichtbarkeit fehlt** (WCAG 2.4.7)
- **Tastaturnavigation** bricht auf (WCAG 2.1.1)
- **Cookie-Banner nicht barrierefrei** (haeufiger Fehler)
- **Video ohne Untertitel/Transkript** (WCAG 1.2.2, 1.2.3)
- **ARIA-Rollen falsch verwendet** (eigene Widgets ohne korrektes ARIA)
- **Sprache nicht deklariert** (`<html lang="de">`; WCAG 3.1.1)
- **Keine Barrierefreiheitserklaerung** im Footer
- **Checkout-Prozess** nicht screenreader-tauglich (bei E-Commerce)

## Relevanz fuer Codebase-Typen

- **Next.js SaaS (B2C)**: **Volle BFSG-Pflicht**, wenn nicht Kleinstunternehmen. WCAG 2.1 AA umsetzen, Barrierefreiheitserklaerung pflichtig.
- **Next.js SaaS (B2B only)**: BFSG **nicht anwendbar** (keine Verbraucherdienstleistung).
- **Landingpage** (rein werblich, ohne Transaktion): Typisch **nicht** BFSG-pflichtig — aber: wenn Kontaktformular/Buchung → grenzwertig, lieber barrierefrei.
- **n8n-Kundenportal** (wenn Kunden = Verbraucher darueber interagieren): BFSG-pflichtig.
- **E-Commerce**: **Kern-Anwendungsfall** — volle Pflicht. Checkout barrierefrei, Produktseiten, Formulare, Cookie-Banner.
- **Content/Blog**: BFSG greift nur, wenn gewerblicher Dienst mit B2C-Charakter und nicht Kleinstunternehmen; redaktioneller Medieninhalt ist nicht direkt BFSG-pflichtig, aber WCAG ist Good Practice.

## Behoerden-Hinweise

- **Bundesfachstelle Barrierefreiheit**: https://www.bundesfachstelle-barrierefreiheit.de/ — offizielle FAQ und Praxishilfen
- **Marktueberwachung**: In den Bundeslaendern (z. B. in Bayern: Regierung von Mittelfranken; in NRW: Bezirksregierung Arnsberg). Adressenliste bei BMAS.
- **BMAS**: https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/barrierefreiheitsstaerkungsgesetz.html

## Zitierbare Urteile

**Noch keine hoechstrichterliche BFSG-Rechtsprechung** (Stand 2026-04). Erste LG-/OLG-Entscheidungen zu Abmahnfaehigkeit sind erwartet, liegen aber nach oeffentlich zugaenglichen Quellen **noch nicht** als Endurteile vor.

`<<VERIFIKATION AUSSTEHEND>>` — beim naechsten Update pruefen, ob BGH/OLG zur UWG-Abmahnfaehigkeit von BFSG-Verstoessen entschieden hat.

Hintergrund aus EU-Ebene:
- **EuGH, Urt. v. 19.10.2023, C-660/21** (betrifft EAA-Ausstrahlung, nicht BFSG direkt)

## Siehe auch

- [[../themen/barrierefreiheit]] — WCAG 2.1/2.2 AA-Checkliste, BFSGV-Details
- [[dsa]] — auch Art. 14 DSA verlangt verstaendliche AGB (Schnittmenge)
