---
aktualisiert: 2026-04-19
quelle-primaer: https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&Art=en&nr=107623&pos=0&anz=1
quellen-sekundaer:
  - https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2020/2020067.html
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=BGH&Datum=28.05.2020&Aktenzeichen=I+ZR+7/16
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

# BGH I ZR 7/16 — „Cookie-Einwilligung II" (Planet49-Folgeurteil)

## Kurz-Überblick

Der Bundesgerichtshof hat am 28. Mai 2020 die deutsche Folgeentscheidung zu EuGH C-673/17 (Planet49) getroffen. Unter dem Kurznamen „Cookie II" hat er bestätigt: Voreingestellte Checkboxen sind keine wirksame Einwilligung. § 15 Abs. 3 TMG a.F. (heute § 25 TDDDG) ist richtlinienkonform im Sinne der ePrivacy-Richtlinie auszulegen. Das Urteil ist die deutsche Umsetzung des EuGH-Spruchs und macht Opt-In-Consent zur bindenden Norm.

## Eckdaten

| Feld | Wert |
|------|------|
| **Aktenzeichen** | I ZR 7/16 |
| **Datum** | 28.05.2020 |
| **Gericht** | BGH, I. Zivilsenat |
| **Vorgeschichte** | OLG Frankfurt a.M. 6 U 30/15; zuvor LG Frankfurt; Vorlage an EuGH C-673/17 |
| **Parteien** | Bundesverband der Verbraucherzentralen (vzbv) gegen Planet49 GmbH |

## Leitsätze (sinngemäß zusammengefasst, da nicht amtlich durchnummeriert)

1. **Für die Einwilligung in das Setzen von Cookies** zur Erstellung von Nutzerprofilen zu Werbezwecken ist keine wirksame Einwilligung i.S.v. § 15 Abs. 3 Satz 1 TMG a.F. (= § 25 TDDDG heute) gegeben, wenn die Einwilligung durch ein vorausgewähltes Kontrollkästchen erteilt wird, das der Nutzer zur Verweigerung seiner Einwilligung abwählen muss.

2. **Richtlinienkonforme Auslegung:** § 15 Abs. 3 Satz 1 TMG ist richtlinienkonform als Umsetzung der Art. 5 Abs. 3, Art. 2 lit. f der Richtlinie 2002/58/EG (ePrivacy) zu verstehen — trotz ursprünglicher nationaler Umsetzungslücke.

3. **Telefonwerbung:** Auch die Einwilligung in Werbeanrufe von zahlreichen Partnerunternehmen ist nur wirksam, wenn der Nutzer das Gewinnspiel wirklich eigenverantwortlich zur Einwilligung nutzt und klar erkennt, was er erlaubt.

## Kernaussagen

### Zur Cookie-Einwilligung

- Vorausgewählte Checkboxen verletzen sowohl **Planet49 (EuGH)** als auch nationale Vorgaben
- Der BGH legte § 15 Abs. 3 TMG a.F. erstmals richtlinienkonform aus — vor diesem Urteil war in Deutschland die Opt-Out-Theorie weit verbreitet
- Konsequenz: **Ab 28.05.2020 ist Opt-In in Deutschland höchstrichterlich geklärt**

### Zur Telefonwerbung (zusätzlich)

- Einwilligung zu Werbeanrufen „von Partnerunternehmen" ist intransparent, wenn Partner nicht bestimmt oder bestimmbar sind
- Der konkrete Umfang („wer darf anrufen, wofür") muss für den Nutzer erkennbar sein
- Liste von 57 Partnern wie im Fall war für die Freiwilligkeit der Einwilligung problematisch

## Rechtliche Bedeutung

- **Deutsche Cookie-Rechtsprechung-Wende:** Vor Cookie II wurde § 15 Abs. 3 TMG weit ausgelegt; Aufsichtsbehörden hatten bereits 2019 eine Positionierung vorgenommen, die BGH bestätigte
- **Grundlage für § 25 TTDSG (seit Dezember 2021) / § 25 TDDDG (seit Mai 2024):** Gesetzgeber hat Rechtsunsicherheit formell beendet
- **Wettbewerbsrechtliche Sanktionierung:** vzbv-Klage nach § 3a UWG i.V.m. § 7 Abs. 2 Nr. 2 UWG

## Praktische Folgen für Codebases

- **Keine Cookies vor aktivem Opt-In** (außer unbedingt erforderlich i.S.v. § 25 Abs. 2 TDDDG)
- **Granulare Einwilligungen** pro Zweck / Anbieter
- **Dokumentationspflicht** der Einwilligung (Zeitstempel, Version, Auswahl)
- **Widerruf-Funktion** in der gleichen Qualität wie Erteilung
- **UWG-Relevanz:** Mitbewerber und Verbraucherverbände können abmahnen

## Folgerechtsprechung / weitere relevante Entscheidungen

- **LG Rostock 3 O 762/19, 15.09.2020** — Ablehnen-Button gleichwertig zu Akzeptieren
- **OLG Köln 6 U 185/21, 03.11.2022** — Dark-Pattern-Cookie-Banner wettbewerbswidrig
- **LG Köln 33 O 376/22, 23.03.2023** — Consent-Verweigerung muss genauso leicht sein wie Erteilung

## Siehe auch

- [[gesetze/tdddg]]
- [[themen/cookie-consent]]
- [[urteile/eugh-planet49]]
- [[behoerden/edsa-leitlinien]]
