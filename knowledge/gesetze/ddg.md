---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/ddg/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/ddg/__5.html
  - https://www.bmj.de/DE/themen/digitales/digitale_dienste/DDG/DDG_node.html
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

# DDG — Digitale-Dienste-Gesetz

## Kurz-Ueberblick

Das **Digitale-Dienste-Gesetz (DDG)** ist am **14. Mai 2024** in Kraft getreten
und loest das bisherige Telemediengesetz (TMG) und Teile des Netzwerk-
durchsetzungsgesetzes (NetzDG) ab. Es dient der Umsetzung und Durchfuehrung
der EU-Verordnung **Digital Services Act (DSA) 2022/2065**.

Fuer die Anbieter von Websites, Online-Shops, Apps und SaaS-Portalen ist vor
allem **§ 5 DDG** (Impressumspflicht) praxisrelevant — inhaltlich unveraendert
gegenueber dem frueheren § 5 TMG.

## Schluesselparagraphen / Kernaussagen

### § 5 DDG — Allgemeine Informationspflichten (Impressumspflicht)

Diensteanbieter muessen fuer geschaeftsmaessige, in der Regel gegen Entgelt
angebotene Telemedien folgende Informationen **leicht erkennbar, unmittelbar
erreichbar und staendig verfuegbar** halten:

**Abs. 1 Nr. 1 — Identitaet:**

- Name und Anschrift, unter der sie niedergelassen sind
- bei juristischen Personen: Rechtsform, Vertretungsberechtigter
- ggf. Angaben zum gezeichneten Kapital und noch ausstehenden Einlagen

**Abs. 1 Nr. 2 — Schnelle Kontaktaufnahme:**

- Angaben, die eine schnelle elektronische Kontaktaufnahme und unmittelbare
  Kommunikation ermoeglichen
- insbesondere **E-Mail-Adresse**
- zweiter Kommunikationsweg (Telefon oder Online-Formular) — aus EuGH
  C-649/17 Amazon EU abgeleitet

**Abs. 1 Nr. 3 — Behoerdliche Zulassung:**

- soweit erforderlich: Aufsichtsbehoerde einschliesslich Anschrift
  (z.B. bei erlaubnispflichtigen Taetigkeiten: Makler, Versicherungsvermittler,
  Anwaelte, Steuerberater, Heilberufe)

**Abs. 1 Nr. 4 — Registereintrag:**

- Handelsregister, Vereinsregister, Partnerschaftsregister,
  Genossenschaftsregister + Registernummer

**Abs. 1 Nr. 5 — Berufsbezeichnung (reglementiert):**

- Kammer
- gesetzliche Berufsbezeichnung und Staat der Verleihung
- Bezeichnung der berufsrechtlichen Regelungen und Link / Fundstelle

**Abs. 1 Nr. 6 — Steuernummern:**

- Umsatzsteuer-Identifikationsnummer nach § 27a UStG, sofern vorhanden
- alternativ: Wirtschafts-Identifikationsnummer nach § 139c AO

**Abs. 1 Nr. 7 — Liquidations-/Abwicklungsstatus:**

- AG, KGaA, GmbH: Hinweis auf Abwicklung oder Liquidation

**Abs. 1 Nr. 8 — Audiovisuelle Mediendienste:**

- Sitzstaat
- zustaendige Regulierungs-/Aufsichtsbehoerde

### § 18 Medienstaatsvertrag (MStV) — Verantwortlicher i.S. Presserecht

Fuer **journalistisch-redaktionelle Angebote** (Blogs, News-Sites, Podcasts mit
redaktionellem Inhalt) ist zusaetzlich ein **Verantwortlicher im Sinne des
§ 18 Abs. 2 MStV** zu benennen:

- Vor- und Zuname
- Anschrift (ladungsfaehig, kein Postfach)

Mehrere Verantwortliche moeglich, wenn nach Sachgebieten gegliedert.

### Weitere Normen im DDG

- **§§ 7-10 DDG** — Haftungsprivilegien fuer Host-Provider, Caching,
  reine Durchleitung (entsprechen Art. 4-6 DSA).
- **§§ 11-16 DDG** — Durchsetzung des DSA (Bundesnetzagentur als
  "Digital Services Coordinator" fuer Deutschland).
- **§§ 17 ff DDG** — Trusted Flaggers, Beschwerdemanagement bei grossen
  Plattformen.

## Typische Fallstricke in Codebases

1. **Impressum zu tief verlinkt:** Der Footer-Link muss mit **max. zwei Klicks**
   erreichbar sein (BGH I ZR 151/02 "Impressumspflicht").
2. **Nur "impressum@..."-Mailto:** E-Mail-Adresse + zweiter Kontaktweg
   erforderlich (Telefon/Chat/Formular).
3. **Keine USt-IdNr trotz vorhandener:** Wenn eine USt-IdNr vorhanden ist, MUSS
   sie ins Impressum — "sofern vorhanden" heisst nicht "optional wenn egal".
4. **Kein Impressum auf Landingpage-Varianten:** Jede oeffentlich zugaengliche
   Instance einer Website braucht Impressum; kein "private" Sub-Route.
5. **Social-Media-Profile ohne Impressum:** Instagram/TikTok/YouTube-Profile
   mit geschaeftlicher Nutzung brauchen Impressum — typisch: Link in Bio.
6. **Fehlender MStV-Verantwortlicher bei Blog:** Redaktionelle Beitraege ohne
   genannten "verantwortlich nach § 18 Abs. 2 MStV" sind abmahnfaehig.
7. **API-gesteuerte Impressumsdaten:** CMS-Feld "company_name" leer in
   Staging-/Preview-Builds → Impressum-Validator fehlt.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** `/impressum`-Route mit Server-gerendertem Content,
  automatische Pflege aus zentraler "company"-Config; Footer-Link auf allen
  Seiten (inkl. Auth-Routes, 404).
- **Landingpage:** Impressum + Datenschutz MUSSEN vorhanden sein, auch bei
  Coming-Soon-Pages, sobald Business-Kontext erkennbar.
- **n8n-Workflows:** Falls Workflow eine oeffentliche Webhook-UI (Forms)
  bereitstellt, Impressum in Form-Footer einbauen.
- **E-Commerce:** Shop-Templates pflegen Impressum meist automatisch;
  dennoch Kategorie-, Produkt- und Checkout-Seiten pruefen.
- **Content/Blog:** Zusaetzlich MStV-Verantwortlicher; bei Gastautoren ggf.
  pro Artikel "Autor"-Angabe.

## Behoerden-Hinweise

- **Bundesnetzagentur (BNetzA)** — Digital Services Coordinator Deutschland
  (ab 17.02.2024), zustaendig fuer DSA-Durchsetzung.
- **Landesmedienanstalten** — zustaendig fuer § 18 MStV (journalistische
  Inhalte).
- **Landes-Datenschutzbehoerden** — nicht fuer Impressum, aber oft angrenzend
  (Datenschutzerklaerung).

## Zitierbare Urteile

- **BGH I ZR 151/02** (20.07.2006): "Zwei-Klick-Regel" fuer Impressum-
  Erreichbarkeit.
- **BGH I ZR 228/03** (14.07.2005): Mobiltelefon-Nummer kann genuegen, wenn
  dauerhaft erreichbar.
- **EuGH C-298/07** (16.10.2008, "deutsche internet versicherung AG"):
  Zweiter Kommunikationsweg neben E-Mail erforderlich.
- **BGH I ZR 228/14** (07.07.2016, "English alphabet"): Anforderung an
  verstaendliche, hier: deutschsprachige Kontaktaufnahme.
- **OLG Duesseldorf I-20 U 17/07** (18.12.2007): Mobilnummer als Telefonkontakt
  ausreichend.
- **OLG Muenchen 29 U 3698/20** zur Impressumspflicht bei
  Instagram-Business-Profilen.

## Siehe auch

- [[themen/impressum]]
- [[gesetze/uwg]] — Impressumsverletzung = UWG-Verstoss ueber § 3a UWG
- [[gesetze/bgb-agb]]
