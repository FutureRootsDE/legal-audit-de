---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/markeng/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/markeng/__14.html
  - https://www.gesetze-im-internet.de/markeng/__15.html
  - https://www.dpma.de/
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

# Markengesetz (MarkenG)

## Kurz-Ueberblick

Das MarkenG regelt den Schutz von **Marken (§ 3 ff.)**, **geschaeftlichen Bezeichnungen (§ 5)** und **geographischen Herkunftsangaben (§ 126 ff.)**. Fuer Codebases sind vor allem **§ 14** (Verletzung eingetragener Marken) und **§ 15** (Schutz geschaeftlicher Bezeichnungen) relevant.

Ergaenzt wird das MarkenG durch die **Unionsmarkenverordnung (EU) 2017/1001** (Unionsmarken) und die **Pariser Verbandsuebereinkunft**.

## Schluesselparagraphen / Kernaussagen

### § 14 MarkenG — Ausschliessliches Recht des Markeninhabers

**Abs. 2 — Verletzungstatbestaende**:

1. **Identitaetsschutz** (Doppelidentitaet): Identisches Zeichen fuer identische Waren/Dienstleistungen
2. **Verwechslungsgefahr**: Identisches oder aehnliches Zeichen fuer identische oder aehnliche Waren/Dienstleistungen, wenn Verwechslungsgefahr besteht
3. **Bekanntheitsschutz**: Identisches oder aehnliches Zeichen fuer NICHT-aehnliche Waren, wenn die Marke **im Inland bekannt** ist und die Benutzung die **Unterscheidungskraft oder Wertschaetzung** ohne rechtfertigenden Grund in unlauterer Weise ausnutzt oder beeintraechtigt (Verwaesserung, Ausbeutung)

**Abs. 3 — Benutzungshandlungen** (nicht abschliessend):
- Anbringen auf Waren, Verpackung
- Anbieten, Inverkehrbringen, Lagern
- Einfuehren, Ausfuehren
- **Als Handelsname / Geschaeftsbezeichnung verwenden**
- **Benutzung in Geschaeftspapieren und in der Werbung** — inkl. Online-Werbung, Google Ads, Meta Keywords
- **Benutzung in vergleichender Werbung** entgegen UWG

**Abs. 5 — Unterlassungsanspruch** bei Wiederholungsgefahr (nach erfolgter Verletzung vermutet) oder Erstbegehungsgefahr.

**Abs. 6 — Schadensersatz** bei Vorsatz oder Fahrlaessigkeit. Berechnungsmethoden (Wahlrecht):
1. Konkreter Schaden
2. **Verletzergewinn** (Herausgabe)
3. **Lizenzanalogie** — uebliche Lizenzgebuehr (haeufigste Praxis!)

**Abs. 7** — Haftung von Organen (GmbH-Geschaeftsfuehrer, Vorstand) persoenlich.

### § 15 MarkenG — Geschaeftliche Bezeichnungen

Schuetzt:
- **Unternehmenskennzeichen** (Firma, besondere Geschaeftsabzeichen)
- **Werktitel** (Buecher, Software, Apps, Zeitschriften)

Voraussetzung: **Verkehrsgeltung** oder **originaere Unterscheidungskraft**. Kein DPMA-Eintrag noetig — Schutz entsteht mit Ingebrauchnahme im geschaeftlichen Verkehr.

### § 23 MarkenG — Benutzung von Namen, beschreibenden Angaben, Zubehoer/Ersatzteil

Schranken des Markenschutzes:
- Eigener Name / Adresse (natuerliche Person)
- **Beschreibende Angaben** (Art, Beschaffenheit, Menge, Zeit, geographische Herkunft)
- **Bestimmungshinweise** (Zubehoer/Ersatzteil fuer kompatible Produkte) — z. B. "Huelle fuer iPhone 16"

Voraussetzung: Benutzung **anstaendige Gepflogenheiten** in Gewerbe/Handel.

### § 24 MarkenG — Erschoepfung

Nach erstem Inverkehrbringen im EWR durch oder mit Zustimmung des Markeninhabers ist die Marke erschoepft — Wiederverkauf grundsaetzlich frei. Ausnahme: Umpacken, Veraenderung, Schaedigung des Rufs.

### Wichtig fuer Online-Kontext: § 14a, § 14b

- **§ 14a** — Haftung von Host-Providern/Marktplaetzen (nach LOreal/eBay-Rechtsprechung)
- **§ 14b** — Lagerung von markenverletzenden Waren (nach Coty-Urteil EuGH)

## Typische Fallstricke in Codebases

### Marketing / SEO / Ads

- **Markenname im Meta-Title / Title-Tag** ohne Berechtigung → Verletzung nach § 14 Abs. 3 Nr. 5
- **Google Ads auf fremde Marken buchen**: Abhaengig von Darstellung (Interflora-Rsp.) — bei Verwechslungsgefahr problematisch
- **Affiliate-Links** mit Marken-Keywords (gebrandet) — rechtliche Grauzone, oft unzulaessig
- **Comparative Advertising** (vergleichende Werbung) muss § 6 UWG entsprechen (anstaendig, fair, nicht irrefuehrend)

### Domains / Subdomains

- Eigene Domain mit fremder Marke → hohes Verletzungsrisiko
- **Typosquatting** (apple.de vs. app1e.de) → kennzeichenrechtlich + UWG-verletzend
- **City-Marken**: "Berliner Currywurst" geschuetzt als geographische Herkunftsangabe

### Produktbezeichnungen

- **Keyword-Stuffing** mit fremden Marken in Produkttiteln (bei Amazon / eBay) → klassischer Abmahnfall
- **"kompatibel mit X"** unter § 23 zulaessig, aber nicht "X-Huelle" wenn dadurch Herkunftstaeuschung entsteht

### Code / UI

- **Logo-Verwendung**: Drittanbieter-Logos (Facebook, Google, Microsoft) fuer Buttons — nur nach jeweiliger Brand-Guideline zulaessig
- **Font-Namen mit Markenrechten**: "Helvetica", "Futura" sind Marken — Verwendung in CSS als `font-family: Helvetica` ist zulaessig (technische Referenz), aber nicht kommerzieller Vertrieb
- **App-Namen**: Pruefung im DPMA-Register **vor** Launch!
- **KI-generierte Markenkonflikte**: KI-Bildgeneratoren produzieren oft Logos/Marken von Drittfirmen → rechtliches Risiko im generierten Content

## Relevanz fuer Codebase-Typen

- **Next.js SaaS**: Produktname pruefen (DPMA, EUIPO); keine fremden Marken im Meta-Tag, Title, h1
- **Landingpage**: Keine fremden Marken-Keywords (ausser Zulaessiges nach § 23); Logo-Nutzung (z. B. "wie berichtet in Logoleiste") nur bei Quellen-Richtigkeit und Pressebetrag-Charakter
- **n8n**: Bei Workflow-Namensgebung aufpassen; bei Content-Generierung Marken-Check einbauen
- **E-Commerce**: Produkt-Listings — eigene Marke markenrechtlich schuetzen; fremde Marken nur bei echten Herstellerangaben/Zubehoer ueber § 23; **keine Keyword-Stuffing**
- **Content/Blog**: Redaktioneller Kontext (Berichterstattung) zulaessig; Vorsicht bei Affiliate-Content

## Behoerden-Hinweise

- **Deutsches Patent- und Markenamt (DPMA)**: https://www.dpma.de/ — Marken-Eintragung, Register-Recherche ueber DPMAregister
- **EUIPO**: https://euipo.europa.eu/ — Unionsmarken, eSearch plus
- **WIPO**: Internationale Registrierung (Madrid-Protokoll)

## Zitierbare Urteile

### Grundlegend

- **BGH, Urt. v. 13.09.2007 — I ZR 33/05 "THE HOME STORE"** — Verwechslungsgefahr
- **EuGH, Interflora/Marks & Spencer (C-323/09)** — Keyword Advertising
- **EuGH, LOreal/Bellure (C-487/07)** — Ausbeutung Bekanntheitsschutz
- **EuGH, LOreal/eBay (C-324/09)** — Haftung Online-Marktplaetze
- **EuGH, Coty Germany (C-567/18)** — Lagerhalter-Haftung (Amazon FBA)

### Neuer (2023–2025)

- **BGH, Urt. v. 02.02.2023 — I ZR 220/21 "Ortlieb II"** — Benutzung als Marke vs. beschreibend bei Google Shopping
- **EuGH, Urt. v. 22.06.2023 — C-148/21 (Inditex / Louboutin)** — Amazon-Marketplace-Haftung
- **BGH, Urt. v. 15.02.2024 — I ZR 170/22** — Keyword Advertising Bestandteile

`<<VERIFIKATION AUSSTEHEND>>` — aktuelle BGH-Urteile 2025/2026 zum SEO / Ads beim naechsten Update pruefen.

## Siehe auch

- [[urhg]] — Urheberrecht, Abgrenzung
- UWG (nicht in dieser KB) — lauterkeitsrechtliche Begleitverletzungen
