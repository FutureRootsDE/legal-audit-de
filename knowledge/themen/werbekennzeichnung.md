---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/uwg_2004/__5a.html
quellen-sekundaer:
  - https://www.die-medienanstalten.de/themen/werbung
  - https://www.lfm-nrw.de/leitfaeden/influencer
  - https://www.bmj.de/DE/themen/verbraucherrecht/lauterkeitsrecht/
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

# Werbekennzeichnung — Influencer, Sponsored, Native

## Kurz-Ueberblick

Werbung muss als solche erkennbar sein ("Trennungs-" und "Kennzeichnungsgebot").
Rechtsgrundlagen:

- **§ 5a Abs. 4 UWG** — kommerziellen Zweck kenntlich machen (seit UWG-Novelle
  2022 neu gefasst)
- **§ 6 TMG (a.F.) / § 6 DDG** — Kennzeichnungspflicht fuer kommerzielle
  Kommunikation
- **§ 22 MStV** — Werbung und Sponsoring in Rundfunk/Telemedien
- **Anhang zu § 3 Abs. 3 UWG** (Nr. 11): als Information getarnte Werbung ist
  per se unzulaessig

Diese Regeln gelten fuer Blogposts, Instagram-/TikTok-/YouTube-Posts,
Podcast-Werbung, Native Ads, Advertorials, Affiliate-Content.

## Schluesselparagraphen / Kernaussagen

### § 5a Abs. 4 UWG — Kommerziellen Zweck kenntlich machen

"Unlauter handelt auch, wer den **kommerziellen Zweck einer geschaeftlichen
Handlung** nicht kenntlich macht, sofern sich dieser nicht unmittelbar aus den
Umstaenden ergibt, und das Nichtkenntlichmachen geeignet ist, den Verbraucher
zu einer geschaeftlichen Entscheidung zu veranlassen, die er andernfalls nicht
getroffen haette."

**Ausnahme bei kostenloser Handlung:** Kein kommerzieller Zweck bei einer
Handlung **zugunsten eines fremden Unternehmens**, wenn der Handelnde **kein
Entgelt oder keine aehnliche Gegenleistung** erhaelt oder erwartet.

**Beweislast-Umkehr:** Entgelt / Gegenleistung werden **vermutet**; der
Handelnde muss glaubhaft machen, dass er nichts erhalten hat.

"Gegenleistung" umfasst:

- Geld
- kostenlose Produkte ("Gifted") — ueber Bagatellgrenze hinaus
- Rabatte / Einladungen / Reisen
- Affiliate-Links (Umsatzbeteiligung)
- Tausch-/Kooperations-Leistungen

### Anhang zu § 3 Abs. 3 UWG Nr. 11

Per se unzulaessig: "der vom Unternehmer finanzierte Einsatz **redaktioneller
Inhalte** zu Zwecken der Verkaufsfoerderung, ohne dass sich dieser Zusammenhang
aus dem Inhalt oder aus der Art der optischen oder akustischen Darstellung
eindeutig ergibt (als Information getarnte Werbung)".

### § 6 DDG (frueher § 6 TMG) — Kommerzielle Kommunikation

Fuer Diensteanbieter:

1. kommerzielle Kommunikation muss klar als solche erkennbar sein
2. Person, in deren Auftrag erfolgt, muss klar identifizierbar sein
3. Angebote zur Verkaufsfoerderung (Rabatte, Zugaben, Gewinnspiele) muessen
   klar erkennbar sein und Teilnahmebedingungen leicht zugaenglich, klar und
   unzweideutig sein

### § 22 MStV — Werbung / Sponsoring in Telemedien

Journalistisch-redaktionelle Inhalte mit Werbung muessen durch geeignete
Mittel vom redaktionellen Inhalt getrennt werden ("Trennungsgebot").

## Typische Fallstricke in Codebases

1. **Hashtag am Ende der Tag-Wolke:** `#produkt #style #foodie #werbung` am
   Ende eines Instagram-Posts: NICHT ausreichend (KG Berlin 5 U 51/18,
   OLG Frankfurt 6 W 35/19).
2. **Englische Labels fuer deutsche Zielgruppe:** "#ad", "#sponsored",
   "#sp" ohne deutschen Zusatz: nicht gerichtsfest (Tendenz: "Werbung",
   "Anzeige" ausschreiben).
3. **"in Zusammenarbeit mit" / "supported by" / "PR Sample":** von der
   Rechtsprechung nicht einheitlich als ausreichend anerkannt.
4. **Gifted Products ohne Gegenleistung behauptet:** Beweislast § 5a Abs. 4
   S. 2 UWG — Vermutung der Gegenleistung. Dokumentation des Sachverhalts
   wichtig.
5. **Affiliate-Links ohne Hinweis:** Produktlinks mit Provisions-ID
   ("ref=XY"): eindeutig kommerziell — Kennzeichnung Pflicht.
6. **Redaktioneller Artikel mit verstecktem Advertorial:** "Das beste
   Produkt 2026" ohne Werbekennzeichnung, wenn der Hersteller bezahlt hat =
   Verstoss gegen Nr. 11 der schwarzen Liste.
7. **Podcast: Werbung in der Mitte ohne Trenner:** Akustischer Trenner
   ("Werbung" / Jingle) erforderlich vor/nach Werbeblock.
8. **Auto-generierte Social-Ads / Dynamic Product Ads:** Plattform-Labeling
   ("Gesponsert") reicht in der Regel; problematisch bei Embedded Influencer-
   Content.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Falls SaaS einen Affiliate-/Referral-Link-Flow hat,
  Disclosure in Email-Templates der Partner-Kampagnen generieren (Template
  enthaelt "#Werbung" prominent).
- **Landingpage:** Testimonials / Customer-Logos als Werbung kennzeichnen,
  wenn diese zitiert bezahlt wurden.
- **n8n-Workflows (z.B. SmarteHuette42):** YouTube-Description-Generator
  muss bei Sponsoring-Deals automatisch "Werbung" + Transparenz-Hinweis
  einfuegen; Metadata-Workflow als Gate.
- **E-Commerce:** Influencer-Marketing-Briefings in das Vertrags-Template
  schriftlich mit Kennzeichnungspflicht; Brand-Guidelines: "Werbung" in
  erster Zeile der Caption.
- **Content/Blog:** Sponsored Article Flag im CMS (WordPress / Sanity):
  Rendered als prominenter Banner "Werbung — bezahlter Beitrag" oben.

## Behoerden-Hinweise

- **Landesmedienanstalten (LMA) / ZAK** — Werbeaufsicht fuer redaktionell-
  journalistische Inhalte inkl. Influencer.
- **Wettbewerbszentrale** — regelmaessige Abmahnwelle 2018-2022 gegen
  Influencer.
- **VSW Verband Sozialer Wettbewerb** — typischer Abmahner.

## Zitierbare Urteile

- **BGH I ZR 90/20** (09.09.2021, "Influencer I" — Pamela Reif):
  Kennzeichnungspflicht auch ohne Entgelt, wenn starker Werbe-Uebergewicht
  gegeben.
- **BGH I ZR 125/20** (09.09.2021, "Influencer II" — Hummels): ohne
  Gegenleistung keine kommerzielle Kommunikation i.S.v. § 5a UWG (a.F.).
- **BGH I ZR 126/20** (09.09.2021, "Influencer III" — Leni Hummels):
  Wirkung von Tap-Tags.
- **KG Berlin 5 U 51/18** (08.01.2019): "#ad" am Ende der Caption nicht
  ausreichend.
- **OLG Frankfurt 6 W 35/19** (24.10.2019): Tap-Tags sind kennzeichnungs-
  pflichtige Werbung.
- **OLG Muenchen 6 U 1362/20** (25.06.2020): Kennzeichnung muss auf den ersten
  Blick erkennbar sein.
- **EuGH C-371/20** (02.09.2021, "Peek & Cloppenburg/Gotha"): zu getarnten
  redaktionellen Werbeanzeigen.

## Siehe auch

- [[gesetze/uwg]] — § 5a Abs. 4 UWG
- [[gesetze/ddg]] — § 6 DDG (ehemals § 6 TMG)
- [[themen/email-marketing]]
