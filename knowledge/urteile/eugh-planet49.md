---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62017CJ0673
quellen-sekundaer:
  - https://curia.europa.eu/juris/liste.jsf?num=C-673/17
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en
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

# EuGH C-673/17 — „Planet49"

## Kurz-Überblick

Der EuGH hat am 1. Oktober 2019 in der Rechtssache C-673/17 (Bundesverband der Verbraucherzentralen gegen Planet49 GmbH) entschieden, dass eine Einwilligung zum Setzen von Cookies nicht wirksam ist, wenn sie über ein vorausgewähltes Kontrollkästchen erfolgt. Die Einwilligung muss aktiv und informiert sein. Das Urteil ist das zentrale europäische Cookie-Einwilligungs-Urteil und Grundlage für § 25 TDDDG sowie den BGH-Folgebeschluss Cookie II (I ZR 7/16).

## Eckdaten

| Feld | Wert |
|------|------|
| **Aktenzeichen** | C-673/17 |
| **ECLI** | ECLI:EU:C:2019:801 |
| **CELEX** | 62017CJ0673 |
| **Datum** | 01.10.2019 |
| **Gericht** | EuGH, Große Kammer |
| **Vorlagegericht** | BGH (I ZR 7/16) |
| **Parteien** | Bundesverband der Verbraucherzentralen und Verbraucherverbände — Verbraucherzentrale Bundesverband e.V. (vzbv) gegen Planet49 GmbH |

## Sachverhalt

Planet49 veranstaltete ein Online-Gewinnspiel. Nach Eingabe von Postleitzahl, Name und Adresse fanden Nutzer zwei Einwilligungs-Checkboxen:

1. Einwilligung in Werbeanrufe durch Drittunternehmen
2. Einwilligung in Cookies zur Reichweitenmessung / Webanalyse — **vorausgewählt**

Der vzbv hielt beide Einwilligungen für unwirksam.

## Tenor

1. Eine Einwilligung iSv Art. 2 lit. f und Art. 5 Abs. 3 der Richtlinie 2002/58/EG (ePrivacy) in Verbindung mit Art. 2 lit. h der Richtlinie 95/46/EG bzw. Art. 4 Nr. 11 und Art. 6 Abs. 1 lit. a DSGVO **liegt nicht vor**, wenn die Speicherung / der Zugriff auf Cookies durch ein **vorangekreuztes Kontrollkästchen** erlaubt wird, das der Nutzer abwählen muss, um die Einwilligung zu verweigern.

2. Dies gilt **unabhängig davon**, ob die im Endgerät gespeicherten / abgerufenen Informationen personenbezogene Daten sind.

3. Der Nutzer muss in **klarer und umfassender Weise** u. a. über **Funktionsdauer** der Cookies und darüber informiert werden, **ob Dritte** Zugriff erhalten.

## Kernaussagen

### Aktive Einwilligung

- Art. 4 Nr. 11 DSGVO verlangt eine „Willensbekundung ... durch Handlung"
- Stillschweigen, Untätigkeit oder vorausgewählte Kästchen **reichen nicht**
- Kein Unterschied, ob Cookie personenbezogene oder anonyme Daten betrifft (§ 25 TDDDG ist konsequenterweise technik- und datenneutral)

### Informationspflichten

Muss mindestens enthalten (Rn. 75–81):
- Funktionsdauer der Cookies
- Zugriffsmöglichkeiten Dritter
- Vor der Einwilligung bereitgestellt

### Koppelungsverbot (implizit)

Die Einwilligung zur Cookie-Nutzung darf nicht in einer Weise mit der Teilnahme am Gewinnspiel gekoppelt sein, die Zweifel an der Freiwilligkeit weckt.

## Praktische Folgen

- **BGH I ZR 7/16 (Cookie II), 28.05.2020** — Umsetzung in deutsches Recht mit richtlinienkonformer Auslegung
- Alle Cookie-Banner müssen **aktives Anklicken** fordern (kein Vorhaken, kein Scrollen)
- Deutscher Gesetzgeber hat Anlass genommen, den (damaligen) § 25 TTDSG einzuführen (heute TDDDG)
- Wettbewerbsrechtliche Abmahnbarkeit bestätigt

## Folgerechtsprechung

- **LG Rostock 3 O 762/19, 15.09.2020** — Ablehnen-Button gleichwertig zu Akzeptieren
- **EuGH C-252/21 (Meta Platforms), 04.07.2023** — Personalisierte Werbung nur mit Einwilligung
- **EuGH C-604/22 (IAB Europe), 07.03.2024** — TC-String als personenbezogenes Datum

## Anwendung auf Codebases

- **Cookie-Banner:** keine vorausgewählten Kästchen, pro Zweck separat
- **"Alle akzeptieren" und "Ablehnen"** gleich prominent auf erster Ebene
- **Cookie-Informationen vor Einwilligung** sichtbar (Cookie-Tabelle / Dienste-Liste)
- **Speicherdauer** jeder einzelnen Cookie-Kategorie dokumentiert
- **Dritt-Zugriffsmöglichkeiten** (Google, Meta, TikTok etc.) explizit aufgeführt

## Siehe auch

- [[gesetze/tdddg]]
- [[gesetze/dsgvo]]
- [[themen/cookie-consent]]
- [[urteile/bgh-cookie-einwilligung]]
- [[behoerden/edsa-leitlinien]]
