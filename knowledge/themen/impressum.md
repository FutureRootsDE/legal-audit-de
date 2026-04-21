---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/ddg/__5.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/mstv/
  - https://www.bundesnetzagentur.de/DE/Fachthemen/Digitales/DSA/DSA_node.html
  - https://www.e-recht24.de/impressum-generator/
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

# Impressum — § 5 DDG + § 18 MStV

## Kurz-Ueberblick

Jeder geschaeftsmaessige Telemedien-Anbieter (nahezu jede kommerzielle
Website, jede SaaS-App, jeder Online-Shop, jedes geschaeftlich genutzte
Social-Media-Profil) benoetigt ein **Impressum** nach § 5 DDG
(**Digitale-Dienste-Gesetz, Inkrafttreten 14.05.2024**; Nachfolger § 5 TMG).

Bei redaktionell-journalistischen Angeboten zusaetzlich ein **Verantwortlicher
nach § 18 Abs. 2 MStV**.

Impressum muss **leicht erkennbar, unmittelbar erreichbar, staendig
verfuegbar** sein (BGH I ZR 151/02: Zwei-Klick-Regel).

## Schluesselparagraphen / Kernaussagen

### § 5 DDG — Pflichtangaben

**Bei natuerlichen Personen / Einzelunternehmern:**

1. **Name + Vorname** (nicht: nur "Max M.", sondern voll)
2. **Ladungsfaehige Anschrift** (keine Postfach-Adresse)
3. **E-Mail** + **zweiter Kommunikationsweg** (Telefonnummer oder
   Online-Formular)
4. ggf. **Umsatzsteuer-ID** (§ 27a UStG) — nur Pflicht, wenn vorhanden,
   aber dann MUSS angegeben werden
5. bei Kleinunternehmern: Hinweis gemaess § 19 UStG sinnvoll, aber nicht
   zwingend

**Bei juristischen Personen (GmbH, AG, UG, Verein, etc.):**

6. **Firma / Name** wie im Handelsregister
7. **Rechtsform** (GmbH, UG, AG, GbR, KG, OHG, e.V. usw.)
8. **Vertretungsberechtigte** (Geschaeftsfuehrer, Vorstand) mit Namen
9. **Register + Registernummer** (Handelsregister HRB/HRA, Vereinsregister VR)
10. **Registergericht** (z.B. Amtsgericht Charlottenburg)
11. ggf. gezeichnetes Kapital und ausstehende Einlagen (bei AG/KGaA mit
    freiwilliger Angabe)
12. ggf. Liquidations-/Abwicklungshinweis

**Bei reglementierten Berufen (Anwalt, Arzt, Steuerberater, Architekt etc.):**

13. **Kammer** (z.B. Rechtsanwaltskammer Muenchen)
14. **Gesetzliche Berufsbezeichnung** + Staat der Verleihung
15. **Link zu berufsrechtlichen Regelungen** (oder Fundstelle)

**Bei Aufsichtsbehoerde-Pflicht:**

16. **Aufsichtsbehoerde** einschliesslich Anschrift (z.B. IHK, BaFin)

### § 18 MStV — Verantwortlicher fuer redaktionelle Inhalte

Zusaetzlich bei journalistisch-redaktionellen Angeboten:

- "V.i.S.d.P." oder "Verantwortlich i.S.v. § 18 Abs. 2 MStV"
- Vor- und Zuname
- vollstaendige Anschrift

Mehrere Verantwortliche fuer unterschiedliche Rubriken moeglich.

### EU-Plattform-Angaben (DSA / VSBG)

- **OS-Plattform-Link:** Art. 14 Abs. 1 ODR-VO — Link zur EU-ODR-Plattform
  (ec.europa.eu/consumers/odr/) bei Online-Kaufvertraegen
- **VSBG-Hinweis** (§ 36 VSBG): Information zur Verbraucherschlichtung
  erforderlich

### Erreichbarkeit

- **Zwei-Klick-Regel** (BGH I ZR 151/02): Impressum muss von jeder Seite
  mit max. 2 Klicks erreichbar sein
- **Bezeichnung:** "Impressum", "Kontakt", "Anbieterkennzeichnung" —
  nicht: versteckt unter "About".
- **Funktionierender Link** in sichtbarem Footer

## Typische Fallstricke in Codebases

1. **Impressum nur im Footer einer bestimmten Landingpage:** Jede Route
   inkl. 404, Fehlerseiten, Login/Signup-Seiten braucht Link.
2. **Footer mit "dialog"-Impressum:** Popup/Modal nicht ausreichend, muss
   dauerhaft als Seite abrufbar sein (BGH-Rechtsprechung).
3. **USt-IdNr. fehlt** trotz Vorhandensein: klassische Abmahnung.
4. **Mailto-Link ohne zweite Kontaktmoeglichkeit** (EuGH C-298/07):
   zusaetzliche Telefonnummer oder Formular erforderlich.
5. **Handelsregister-Angabe ohne Ortsname:** "HRB 12345" reicht nicht, muss
   das Registergericht benannt werden.
6. **Geschaeftsfuehrer falsch / veraltet:** Aktualitaet des Impressums ist
   Pflicht; automatische Sync mit CRM sinnvoll.
7. **Fehlender MStV-Verantwortlicher** bei Blog/YouTube/Podcast: regelmaessig
   abgemahnt.
8. **Instagram/TikTok-Biolink-Impressum:** Link muss funktionieren und direkt
   aufs Impressum zeigen; Link-in-Bio-Tools (Linktree) akzeptabel, sofern
   Impressum-Link dort deutlich.
9. **Impressum nur auf Englisch:** Fuer deutsche Zielgruppe unzulaessig.
10. **"Koops.de" mit AGB-Link statt Impressum-Link im Footer:** alle
    Pflichtseiten trennen.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** `/impressum`-Route mit statischem MDX / CMS-Content;
  Footer-Komponente mit Links; Sitemap enthaelt Impressum.
- **Landingpage:** Zwingend, auch bei "Coming Soon"-Pages mit Business-
  Kontext.
- **n8n-Workflows:** Falls Trigger-Forms oeffentlich: Impressum-Link ins
  Form-Footer. Bei AI-generierten Landingpages: Template-Pflicht.
- **E-Commerce:** Shopify / Shopware / WooCommerce-Templates DE haben
  Impressum-Modul; USt-IdNr., Registerdaten manuell pflegen.
- **Content/Blog:** Impressum + MStV-Verantwortlicher pro Artikel ggf.
  Autor-Angabe (Autoren-Seite verlinken).

## Behoerden-Hinweise

- **Bundesnetzagentur (BNetzA)** — Digital Services Coordinator (DSA-Durch-
  setzung seit 17.02.2024).
- **Landesmedienanstalten** — Kontrolle bei redaktionellen Inhalten nach MStV.
- **Gewerbeaufsicht** — gewerberechtliche Flankierung.
- **Ordnungswidrigkeiten** nach § 13 DDG: Bussgeld bis **50.000 EUR**.

## Zitierbare Urteile

- **BGH I ZR 151/02** (20.07.2006): "Zwei-Klick-Regel" — Impressum muss
  innerhalb von zwei Klicks erreichbar sein.
- **BGH I ZR 228/03** (14.07.2005): Mobiltelefonnummer als Kontakt ausreichend,
  wenn dauerhaft erreichbar.
- **EuGH C-298/07** (16.10.2008, "deutsche internet versicherung AG"):
  Zweiter Kontaktweg neben E-Mail erforderlich (Telefon oder alternativer
  Kanal, der ebenso direkt ist).
- **OLG Duesseldorf I-20 U 17/07** (18.12.2007): Mobilnummer ausreichend.
- **OLG Muenchen 29 U 3698/20** (14.01.2021): Impressumspflicht bei
  Instagram-Business-Profilen.
- **OLG Frankfurt 6 U 184/13** (26.06.2014): "About"-Reiter statt "Impressum"
  unzureichend.
- **BGH I ZR 118/12** (05.12.2013): Abgrenzung B2C / rein privater Web-Auftritt.

## Siehe auch

- [[gesetze/ddg]]
- [[gesetze/uwg]] — § 3a Rechtsbruch bei Impressumsverstoss
- [[themen/agb-muster]]
