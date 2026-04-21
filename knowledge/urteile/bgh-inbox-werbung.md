---
aktualisiert: 2026-04-19
quelle-primaer: https://www.bundesgerichtshof.de/
quellen-sekundaer:
  - https://curia.europa.eu/juris/liste.jsf?num=C-102/20
  - https://www.dr-schwenke.de/
  - https://dejure.org/
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

# BGH I ZR 186/17 — "Inbox-Werbung II"

## Kurz-Ueberblick

- **Gericht:** Bundesgerichtshof (1. Zivilsenat)
- **Aktenzeichen:** I ZR 186/17
- **Entscheidungstermin:** **13.01.2022** (Urteil; nach Vorabentscheidung
  des EuGH)
- **EuGH-Vorlage:** C-102/20, Urteil vom **25.11.2021**
- **Vorlagebeschluss des BGH:** 30.01.2020 (Aussetzung und EuGH-Vorlage)
- **Vorinstanz:** OLG Nuernberg, Urteil vom 15.08.2017 — 3 U 805/16
- **Parteien:** Klaegerin StWL Staedtische Werke Lauf a. d. Pegnitz GmbH
  (Energieversorger) ./. Beklagte eprimo GmbH (Energieversorger)

`<<VERIFIKATION AUSSTEHEND — Die Parteienzuordnung in Sekundaerquellen ist
konsistent, aber die oeffentlich zugaenglichen amtlichen Urteils-URLs waren
zum Verifikationszeitpunkt nicht direkt abrufbar. Querpruefung mit juris oder
Heymanns-Verlag empfohlen.>>`

## Sachverhalt

Die Beklagte **eprimo** liess ueber einen externen Dienstleister Werbung im
E-Mail-Posteingang von **T-Online-Freemail-Nutzern** einblenden. Die Werbung
erschien **als eingeblendeter Eintrag innerhalb der regulaeren E-Mail-Liste**
(Inbox-Advertising), war optisch aehnlich aufgebaut wie eine normale E-Mail,
jedoch mit Kennzeichen "Anzeige" / "Werbung".

Die Klaegerin **StWL** (Mitbewerberin im Strommarkt) sah darin eine
wettbewerbsrechtlich unzulaessige E-Mail-Werbung ohne Einwilligung der
Adressaten und klagte auf Unterlassung.

## Rechtsfragen

1. Ist in das Postfach eingeblendete Werbung "elektronische Post" im Sinne
   von **Art. 13 Abs. 1 RL 2002/58/EG** (ePrivacy-Richtlinie) und damit von
   **§ 7 Abs. 2 Nr. 2 UWG**?
2. Stellt das bloße Anzeigen in der Inbox eine "Nachricht" dar, deren
   Absenden an den Nutzer ohne dessen Einwilligung verboten ist?
3. Greift das Verbot "hartnaeckige unerwuenschte Ansprache" nach Anhang I
   Nr. 26 UGP-Richtlinie (ungefragte Werbung)?

## EuGH-Vorabentscheidung C-102/20 (25.11.2021)

Der EuGH entschied:

- **Inbox-Placements sind "Verwendung elektronischer Post" i.S.v. Art. 13
  Abs. 1 RL 2002/58/EG.** Entscheidend: Werbung wird an einem Ort angezeigt,
  der fuer persoenliche Nachrichten reserviert ist.
- Eine Einwilligung des Nutzers ist erforderlich, wenn die Werbung sich
  optisch als private E-Mail aussert und mit gleichen Mitteln der
  Aufmerksamkeit rechnet.
- Ob eine **"Werbemittel-Beschraenkung"** vorliegt, ist im Einzelfall am
  Erscheinungsbild zu messen.

## BGH-Urteil 13.01.2022

Der BGH uebernahm die EuGH-Rechtsprechung und entschied:

- Die konkrete Form der eprimo-Inbox-Werbung ist **Werbung mittels
  elektronischer Post** i.S.v. § 7 Abs. 2 Nr. 2 UWG.
- Ohne Einwilligung der betroffenen Nutzer ist die Werbung **unzulaessige
  unzumutbare Belaestigung**.
- Unterlassungsanspruch des Mitbewerbers nach §§ 8, 3, 7 UWG ist begruendet.

Damit war klargestellt: Inbox-Advertising in Freemail-Diensten (GMX, Web.de,
T-Online, Yahoo) unterliegt denselben Einwilligungs-Anforderungen wie klassische
Werbe-E-Mails.

## Bedeutung fuer Codebases

1. **Display-Werbung mit E-Mail-Kontext** (Inbox-Ads, Push-Notifications im
   Messenger) benoetigt ebenfalls Einwilligung des Empfaengers, wenn sie im
   "persoenlichen" Kommunikationsraum erscheint.
2. **Programmatic Advertising Networks** koennen nicht beliebig
   E-Mail-Postfaecher monetarisieren — rechtliche Pruefung der Platzierungen
   notwendig.
3. **Transaktions-E-Mails mit Banner-Werbung** sind potenziell betroffen,
   wenn Banner stark wirbt.
4. **Push-Benachrichtigungen von Apps mit Werbeinhalt** sind auf § 7 UWG hin
   zu pruefen (str., Tendenz: analog).

## Relevanz fuer Codebase-Typen

- **SaaS/Shop:** Keine unaufgeforderte Banner-Werbung in User-Postfaechern
  des eigenen Produkts, wenn Drittwerbung.
- **Newsletter-Tools:** Inbox-Native-Ads (z.B. Gmail Sponsored Promotions)
  rechtlich problematisch fuer den buchenden Werbetreibenden.
- **n8n-Workflows:** Workflows, die automatisiert E-Mails / In-App-Messages
  versenden, muessen sauber zwischen Transaktion und Werbung trennen.

## Tenor (sinngemaess)

Die Revision der Beklagten gegen das Urteil des OLG Nuernberg wird
zurueckgewiesen. Unterlassungsanspruch der Klaegerin wegen Inbox-Werbung
bestaetigt.

## Siehe auch

- [[gesetze/uwg]] — § 7 UWG
- [[themen/email-marketing]]
- EuGH C-102/20 (25.11.2021) — Vorabentscheidung
