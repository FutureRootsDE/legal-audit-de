---
aktualisiert: 2026-11-15
quelle-primaer: https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&Art=en&nr=107623&pos=0&anz=1
quellen-sekundaer:
  - https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2020/2020067.html
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=BGH&Datum=28.05.2020&Aktenzeichen=I+ZR+7/16
verifiziert-am: 2026-11-14
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

# BGH I ZR 7/16 — „Cookie-Einwilligung II" (Planet49-Folgeurteil)

## Kurz-Überblick

Der Bundesgerichtshof hat am 28. Mai 2020 die deutsche Folgeentscheidung zu EuGH C-673/17 (Planet49) getroffen. Unter dem Kurznamen „Cookie II" hat er bestätigt: Voreingestellte Checkboxen sind keine wirksame Einwilligung. § 15 Abs. 3 TMG a.F. (heute § 25 TDDDG) ist richtlinienkonform im Sinne der ePrivacy-Richtlinie auszulegen. Das Urteil ist die deutsche Umsetzung des EuGH-Spruchs und macht Opt-In-Consent zur bindenden Norm.

## Eckdaten

| Feld | Wert |
|------|------|
| **Aktenzeichen** | I ZR 7/16 |
| **Datum** | 28.05.2020 |
| **Gericht** | BGH, I. Zivilsenat |
| **Vorgeschichte** | LG Frankfurt a.M., Urt. v. 10.12.2014, 2-6 O 30/14; OLG Frankfurt a.M., Urt. v. 17.12.2015, 6 U 30/15; BGH, Vorlagebeschluss v. 05.10.2017; EuGH C-673/17 |
| **Parteien** | Bundesverband der Verbraucherzentralen (vzbv) gegen Planet49 GmbH |

## Leitsätze (amtlich, zwei, nummeriert)

1. **Telefonwerbung:** „Eine wirksame Einwilligung in telefonische Werbung im Sinne von § 7 Abs. 2 Nr. 2 Fall 1 UWG liegt nicht vor, wenn der Verbraucher bei der Erklärung der Einwilligung mit einem aufwendigen Verfahren der Abwahl von in einer Liste aufgeführten Partnerunternehmen konfrontiert wird, das ihn dazu veranlassen kann, von der Ausübung dieser Wahl Abstand zu nehmen und stattdessen dem Unternehmer die Wahl der Werbepartner zu überlassen. Weiß der Verbraucher mangels Kenntnisnahme vom Inhalt der Liste und ohne Ausübung des Wahlrechts nicht, die Produkte oder Dienstleistungen welcher Unternehmer die Einwilligung erfasst, liegt keine Einwilligung für den konkreten Fall vor." (Rn. 27 f.; § 7 Abs. 2 Nr. 2 Fall 1 UWG a.F., heute § 7 Abs. 2 Nr. 1 UWG)

2. **Cookies:** „§ 15 Abs. 3 Satz 1 TMG ist mit Blick auf Art. 5 Abs. 3 Satz 1 der Richtlinie 2002/58/EG dahin richtlinienkonform auszulegen, dass der Diensteanbieter Cookies zur Erstellung von Nutzungsprofilen für Zwecke der Werbung oder Marktforschung nur mit Einwilligung des Nutzers einsetzen darf. Eine elektronisch zu erklärende Einwilligung des Nutzers, die den Abruf von auf seinem Endgerät gespeicherten Informationen mithilfe von Cookies im Wege eines voreingestellten Ankreuzkästchens gestattet, genügt diesem Einwilligungserfordernis nicht." (Rn. 47)

## Kernaussagen

### Zur Cookie-Einwilligung

- Vorausgewählte Checkboxen verletzen sowohl **Planet49 (EuGH)** als auch nationale Vorgaben
- Der BGH legte § 15 Abs. 3 TMG a.F. erstmals richtlinienkonform aus — vor diesem Urteil war in Deutschland die Opt-Out-Theorie weit verbreitet
- Konsequenz: **Ab 28.05.2020 ist Opt-In in Deutschland höchstrichterlich geklärt**

### Zur Telefonwerbung (zusätzlich)

- Die Einwilligung war unwirksam, weil sie nicht für den konkreten Fall und nicht in Kenntnis der Sachlage erteilt wurde (Liste von 57 Unternehmen; ohne Abwahl wählte der Veranstalter bis zu 30 Werbepartner nach freiem Ermessen aus, Rn. 5, 24, 27 f.)
- Der konkrete Umfang („wer darf anrufen, wofür") muss für den Nutzer erkennbar sein
- Die Begründung ist nicht die Freiwilligkeit der Einwilligung

## Rechtliche Bedeutung

- **Deutsche Cookie-Rechtsprechung-Wende:** Vor Cookie II wurde § 15 Abs. 3 TMG weit ausgelegt; Aufsichtsbehörden hatten bereits 2019 eine Positionierung vorgenommen, die BGH bestätigte
- **Grundlage für § 25 TTDSG (seit Dezember 2021) / § 25 TDDDG (seit Mai 2024):** Gesetzgeber hat Rechtsunsicherheit formell beendet
- **Verfahrensart:** Verbandsklage nach §§ 1, 3 Abs. 1 Satz 1 Nr. 1 UKlaG i.V.m. § 307 Abs. 1, Abs. 2 Nr. 1 BGB (AGB-Kontrolle); Maßstab für die Telefonwerbungsklausel § 7 Abs. 2 Nr. 2 Fall 1 UWG a.F., für die Cookie-Klausel § 15 Abs. 3 Satz 1 TMG a.F. (Rn. 23, 41); kein § 3a UWG

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

## Aenderungsvermerk

- 2026-11-14: geprueft gegen die Rechtsinformations-API des Bundes
  (`/v1/rechtsprechung?fileNumber=I ZR 7/16&court=BGH`); Gericht, Datum
  (28.05.2020, "Cookie-Einwilligung II") und Zuordnung zum I. Zivilsenat
  bestaetigt, Vorlagebeschluss vom 05.10.2017 (ECLI:DE:BGH:2017:051017BIZR7.16.0)
  als Zwischenstufe ergaenzt. Inhalt unveraendert — keine neuen
  BGH-Entscheidungen zu dieser Rechtsfrage seit 2026-05-08 bekannt.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  Vorgeschichte mit LG-/OLG-Daten und Vorlagebeschluss; die zwei amtlichen
  Leitsaetze woertlich (LS 1 Telefonwerbung, LS 2 Cookies), Zusatz
  "Umsetzungsluecke" gestrichen; Telefonwerbung: konkreter Fall statt
  Freiwilligkeit; Verfahrensart UKlaG/AGB-Kontrolle statt § 3a UWG.
