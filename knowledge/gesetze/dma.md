---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32022R1925
quellen-sekundaer:
  - https://digital-markets-act.ec.europa.eu/gatekeepers-portal_en
  - https://epthinktank.eu/2025/04/24/digital-markets-act-enforcement-state-of-play/
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

# Digital Markets Act (DMA) — VO (EU) 2022/1925

## Kurz-Ueberblick

Die Verordnung (EU) 2022/1925 ueber bestreitbare und faire Maerkte im digitalen Sektor (Digital Markets Act, DMA) richtet sich an **"Gatekeeper"** — grosse Plattformen mit erheblicher Marktmacht. Sie ist am **02.05.2023 in Kraft getreten**; die operativen Pflichten fuer benannte Gatekeeper gelten seit **07.03.2024**.

Der DMA ist ein ex-ante-Regulierungsinstrument: Er stellt Wettbewerbsregeln **vor** Marktmachtmissbrauch auf, statt wie das kartellrechtliche ex-post-Regime erst nach Missbrauch einzugreifen.

**Fuer kleine und mittlere Unternehmen ist der DMA als Regulierungsadressat irrelevant** — die Schwellen liegen bei Gruppenumsatz (>= 7,5 Mrd. EUR in der EU in 3 Jahren) oder Marktkapitalisierung (>= 75 Mrd. EUR) und min. 45 Mio. monatlichen EU-Endnutzern + 10.000 gewerblichen Nutzern. Er ist jedoch relevant als **Rechteregime fuer gewerbliche Nutzer und Endnutzer**, die gegenueber Gatekeepern Ansprueche haben.

## Schluesselparagraphen / Kernaussagen

### Art. 3 DMA — Benennung als Gatekeeper

Ein Unternehmen ist Gatekeeper, wenn es:
1. **Erheblichen Einfluss auf den Binnenmarkt** hat (quantitativ widerlegbar vermutet bei >= 7,5 Mrd. EUR Jahresumsatz in der EU oder >= 75 Mrd. EUR Marktkapitalisierung)
2. **Einen zentralen Plattformdienst** betreibt, der **wichtiges Zugangstor** fuer gewerbliche Nutzer zu Endnutzern ist (>= 45 Mio. monatliche aktive EU-Endnutzer + >= 10.000 gewerbliche EU-Nutzer)
3. Eine **gefestigte und dauerhafte Position** hat (vermutet bei Erfuellung der Schwellen in 3 letzten Geschaeftsjahren)

Benennung durch die EU-Kommission; Widerlegung innerhalb 45 Arbeitstage moeglich.

### Aktuell benannte Gatekeeper (Stand 2026-04)

**7 Gatekeeper, 24+ zentrale Plattformdienste:**
- **Alphabet (Google)**: Google Search, Google Play, Chrome, YouTube, Google Maps, Google Ads, Android
- **Amazon**: Amazon Marketplace, Amazon Ads
- **Apple**: App Store, iOS, iPadOS, Safari
- **ByteDance**: TikTok
- **Meta**: Facebook, Instagram, WhatsApp, Messenger, Meta Ads, Marketplace
- **Microsoft**: LinkedIn, Windows (PC-OS)
- **Booking.com**: Online-Reisevermittlung (spaeter hinzugefuegt)

Quelle: https://digital-markets-act.ec.europa.eu/gatekeepers-portal_en

### Art. 5 DMA — Verbote (unmittelbare Pflichten)

- Verbot der **Zusammenfuehrung personenbezogener Daten** zwischen zentralem Plattformdienst und anderen Diensten ohne Einwilligung
- Verbot der **Parity-Klauseln** gegenueber gewerblichen Nutzern ("most favored nation")
- Verbot, gewerbliche Nutzer an **ausserhalb der Plattform erfolgender Kundenansprache** zu hindern (Anti-Steering)
- Verbot, Endnutzern den **Zugang zu extern erworbenen Inhalten/Abos** zu verwehren
- Transparenzanspruch bei **Werbepreisen und -leistungen**

### Art. 6 DMA — Handlungspflichten (nach Konkretisierung)

- **Interoperabilitaet** fuer Messaging-Dienste (WhatsApp, Messenger)
- **App-Sideloading** und alternative App-Stores (iOS)
- **Browser/Suchmaschinen-Wahlbildschirme**
- **Fairer und diskriminierungsfreier Zugang** zu App-Stores und Such-Rankings
- **Kein Self-Preferencing** eigener Dienste
- **Datenportabilitaet** fuer Endnutzer
- **Daten-Zugang** fuer gewerbliche Nutzer (die "ihre" auf der Plattform erzeugten Daten)

### Durchsetzung

- Bussgelder bis **10 %** des weltweiten Jahresumsatzes (Art. 30)
- Bei Wiederholung bis **20 %**
- Bei systematischer Nichtbefolgung: **strukturelle Massnahmen** (Unbundling)
- Laufende Nichtbefolgungsverfahren gegen Apple, Meta, Alphabet (Stand 2025)

## Typische Fallstricke in Codebases

Typische SaaS- und E-Commerce-Codebases sind **nicht direkt DMA-verpflichtet**. Relevanz entsteht indirekt:

- **Abhaengigkeit von Gatekeepern**: Wenn eigenes Produkt ueber Apple App Store / Google Play vertrieben wird → Rechte als gewerblicher Nutzer (Anti-Steering, faire Rankings, Zugang zu Nutzerdaten nach Einwilligung)
- **Interoperabilitaetsansprueche**: Messaging-Anbieter koennen Interop mit WhatsApp verlangen (Art. 7)
- **Werbe-SDKs**: Wenn Meta/Google-Werbesysteme eingebunden → Transparenz-Rechte hinsichtlich Preisen und Leistung
- **Datenportabilitaet**: Nutzer koennen kontinuierliche Echtzeit-Datenportabilitaet verlangen — relevant fuer Integrationen

## Relevanz fuer Codebase-Typen

- **Next.js SaaS / Landingpage / n8n / Content/Blog**: Primaer als **Berechtigter** gegenueber Gatekeepern (App-Store-Praesenz, Ads, Analytics). Kaum direkte Codepflichten.
- **E-Commerce**: Als gewerblicher Nutzer von Marktplaetzen (Amazon): Anspruch auf eigene Kundendaten, keine Parity-Klauseln, Anti-Steering-Rechte.

## Behoerden-Hinweise

- **Zustaendigkeit zentral bei EU-Kommission (DG COMP)**: https://digital-markets-act.ec.europa.eu/
- Nationale Wettbewerbsbehoerden (Bundeskartellamt) koennen ergaenzend taetig werden, aber primaere DMA-Durchsetzung liegt bruessellastig

## Zitierbare Urteile

- **EU-Kommission, Non-Compliance Decisions (23.04.2024 / 2025)**: Erste Nichtbefolgungsverfahren gegen Apple (Anti-Steering App Store) und Meta (Pay-or-Consent-Modell)
- `<<VERIFIKATION AUSSTEHEND>>` — Endurteile EuGH zu DMA-Benennungen sind in Arbeit (Klagen von ByteDance, Meta, Apple gegen Benennungen/Durchfuehrungsbeschluesse)

## Siehe auch

- [[dsa]] — Digital Services Act (Schwester-VO)
- [[ai-act]] — KI-Verordnung
- [[../themen/ki-transparenz]]
