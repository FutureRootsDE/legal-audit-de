---
aktualisiert: 2026-11-14
quelle-primaer: https://www.gesetze-im-internet.de/bdsg_2018/
quellen-sekundaer:
  - https://www.bfdi.bund.de/
  - https://www.datenschutzkonferenz-online.de/
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
>
> **Fassung:** Fassung vom 30.06.2017, Textnachweis ab 25.05.2018. Zuletzt
> geaendert durch Art. 3 des Gesetzes vom 12.05.2026 (BGBl. 2026 I Nr. 139);
> zusaetzlich textlich erfasst: Art. 3 G v. 03.07.2026 (BGBl. 2026 I Nr. 199)
> — dokumentarische Bearbeitung laut gesetze-im-internet.de noch nicht
> vollstaendig abgeschlossen (Stand 2026-11-14). § 26 BDSG weiterhin
> geltendes Recht; ein neues Beschaeftigtendatengesetz ist Stand 2026-11-14
> nicht verkuendet.

# BDSG — Bundesdatenschutzgesetz (neu, 2018)

## Kurz-Überblick

Das Bundesdatenschutzgesetz (BDSG) in der Fassung vom 30.06.2017 (in Kraft seit 25.05.2018) ist das nationale Ausführungs- und Ergänzungsgesetz zur DSGVO. Es nutzt die Öffnungsklauseln der Verordnung und regelt nationale Besonderheiten wie Beschäftigtendatenschutz, Videoüberwachung, DSB-Pflicht und Durchführung der Bußgeldverfahren.

## Schlüsselparagraphen

### § 1 — Anwendungsbereich
Gilt für die Verarbeitung durch öffentliche und nichtöffentliche Stellen. Bei EU-Recht-Überlagerung gilt DSGVO vorrangig; BDSG ergänzt nur dort, wo Öffnungsklauseln existieren.

### § 2 — Begriffsbestimmungen
Verweist weitgehend auf Art. 4 DSGVO, ergänzt um „öffentliche Stellen des Bundes/der Länder".

### § 4 — Videoüberwachung öffentlich zugänglicher Räume
Nichtöffentliche Stellen dürfen öffentlich zugängliche Räume nur zur Wahrnehmung des Hausrechts oder berechtigter Interessen überwachen. Hinweispflicht (Beschilderung mit Angaben nach Art. 13 DSGVO). **Achtung:** BVerwG (2019, 6 C 2.18) hat § 4 Abs. 1 BDSG für private Anbieter für unanwendbar erklärt — direkt Art. 6 Abs. 1 lit. f DSGVO anwenden.

### § 5 / § 6 — DSB in öffentlichen Stellen
Benennung, Stellung, Aufgaben des Datenschutzbeauftragten der Behörde.

### § 26 — Datenverarbeitung im Beschäftigungskontext
Zentrale Rechtsgrundlage für HR-Daten:
- Abs. 1: Für Begründung/Durchführung/Beendigung des Beschäftigungsverhältnisses
- Abs. 2: Einwilligung Beschäftigter muss freiwillig sein (problematisch wegen Abhängigkeit)
- Abs. 3: Aufdeckung von Straftaten / dokumentierte tatsächliche Anhaltspunkte

**Wichtig:** EuGH C-34/21 (30.03.2023) hat hessische Parallelvorschrift (§ 23 HDSIG) gekippt — § 26 BDSG dürfte als bloße Wiederholung von Art. 6 Abs. 1 lit. b/f DSGVO ebenfalls keine eigenständige Rechtsgrundlage sein. Ein Gesetzentwurf zum Beschäftigtendatenschutzgesetz ist in Diskussion.

### § 38 — DSB in nichtöffentlichen Stellen
Pflicht zur Benennung wenn:
- **Mindestens 20 Personen** ständig mit automatisierter Verarbeitung personenbezogener Daten beschäftigt sind, ODER
- umfangreiche Verarbeitung besonderer Datenkategorien (Art. 9), ODER
- geschäftsmäßige Verarbeitung zu Übermittlungs-/anonymen Markt-/Meinungsforschungszwecken (unabhängig von Personenzahl)

### § 41 — Anwendung der Vorschriften über das Bußgeldverfahren
OWiG findet Anwendung. Bei Verstößen Art. 83 DSGVO plus Ergänzungen.

### § 42 — Strafvorschriften
**Bis zu 3 Jahre Freiheitsstrafe** bei:
- gewerbsmäßiger Weitergabe nicht allgemein zugänglicher personenbezogener Daten (Abs. 1)
- Abs. 2: Erschleichen, gegen Entgelt, in Bereicherungs-/Schädigungsabsicht

### § 43 — Bußgeldvorschriften
Ergänzende Bußgeldtatbestände neben Art. 83 DSGVO.

### § 83 — Schadenersatz (aufgehoben/verweist auf Art. 82 DSGVO)
Verweis auf Art. 82 DSGVO für privatwirtschaftlichen Bereich.

## Typische Fallstricke in Codebases

- **Überwachungssoftware am Arbeitsplatz** (Zeiterfassung, Activity-Monitoring, Keylogger): § 26 BDSG + BAG-Rechtsprechung (z. B. BAG 2 AZR 133/18 zu Keylogger — unzulässig).
- **HR-Tools (Personio, BambooHR) ohne AVV:** Wenn US-gehostet zusätzlich Drittland-Problem.
- **Videoüberwachung von Mitarbeiter-Bereichen** ohne Betriebsratsbeteiligung (§ 87 BetrVG) + Kennzeichnung: doppelt problematisch.
- **Bewerbermanagement:** Unbegrenzte Speicherung von abgelehnten Bewerbern. Faustregel: max. 6 Monate nach Absage.
- **Whistleblower-Plattformen:** HinSchG + § 26 Abs. 3 BDSG + DSGVO.

## Relevanz für Codebase-Typen

- **Next.js SaaS (B2B/HR-Tech):** § 26 BDSG zentral bei HR-Features (Bewerber-Tracking, Performance-Reviews, Zeiterfassung).
- **Landingpage:** Kaum BDSG-spezifisch, eher DSGVO.
- **n8n:** Bei HR-Automation (Onboarding, Offboarding) Rechtsgrundlagen-Matrix erforderlich.
- **E-Commerce:** Mitarbeiter-Accounts im Backoffice → § 26 BDSG.
- **Content/Blog:** Redakteursrollen → § 26 BDSG (marginal).

## Behörden-Hinweise

- **BfDI:** Tätigkeitsberichte und Orientierungshilfe Beschäftigtendatenschutz
- **LfDI BW / LDA Bayern / LDI NRW:** Länderaufsichtsbehörden für nichtöffentliche Stellen
- **DSK Orientierungshilfe Beschäftigtendatenschutz** (2023)

## Zitierbare Urteile

- **BVerwG 6 C 2.18, 27.03.2019** — § 4 BDSG für private Videoüberwachung unanwendbar
- **EuGH C-34/21, 30.03.2023** — HDSIG § 23 gekippt; Implikationen für § 26 BDSG
- **BAG 2 AZR 681/16, 27.07.2017** — Keylogger ohne konkreten Tatverdacht unzulässig (ECLI:DE:BAG:2017:270717.U.2AZR681.16.0; über die Rechtsinformations-API des Bundes am 2026-11-14 primär bestätigt)
- Aussage: Auskunftsanspruch nach Art. 15 DSGVO auch für Beschäftigte. <<VERIFIKATION AUSSTEHEND>> (vgl. Abschnitt "Nicht zitieren: falsch zugeordnete Aktenzeichen")

## Nicht zitieren: falsch zugeordnete Aktenzeichen

- **BAG 2 AZR 133/18** — in Vorgaengerfassungen dieser KB als Keylogger-Entscheidung
  vom 27.07.2017 zitiert. Gegenprobe ueber die Rechtsinformations-API des Bundes
  am 2026-11-14: unter diesem Aktenzeichen ist nur das Urteil des 2. Senats
  vom **23.08.2018** gefuehrt ("Offene Videoueberwachung — Anhoerung vor
  Verdachtskuendigung — Beweisverwertungsverbot", ECLI:DE:BAG:2018:230818.U.2AZR133.18.0).
  Das tatsaechlich gemeinte Urteil ist **BAG 2 AZR 681/16** vom 27.07.2017
  ("Ueberwachung mittels Keylogger — Verwertungsverbot",
  ECLI:DE:BAG:2017:270717.U.2AZR681.16.0); Aktenzeichen in der Liste oben
  korrigiert.
- **BAG 8 AZR 253/20** — in Vorgaengerfassungen dieser KB als Entscheidung
  zum Auskunftsanspruch nach Art. 15 DSGVO vom 05.05.2022 zitiert. Gegenprobe
  ueber die Rechtsinformations-API des Bundes am 2026-11-14: unter diesem
  Aktenzeichen sind nur das Urteil des 8. Senats vom **20.06.2024**
  ("Datenschutz — Gesundheitsdaten — Verarbeitung durch Arbeitgeber —
  Medizinischer Dienst", ECLI:DE:BAG:2024:200624.U.8AZR253.20.0) und der
  Vorlagebeschluss vom 26.08.2021 gefuehrt; beide betreffen die Verarbeitung
  von Gesundheitsdaten im Arbeitsverhaeltnis, nicht den Auskunftsanspruch.
  Ein BAG-Urteil vom 05.05.2022, das den zitierten Satz traegt, ist dort nicht
  nachweisbar (am 05.05.2022 entschied der 2. Senat 2 AZR 483/21 zur
  ausserordentlichen Kuendigung und 2 AZR 363/21 zum immateriellen
  Schadenersatz nach Art. 82 DSGVO — beides nicht deckungsgleich). Zitat
  daher nicht uebernehmen; Aussage bleibt mit Verifikationsmarker.

## Siehe auch

- [[gesetze/dsgvo]]
- [[gesetze/tdddg]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]]

## Aenderungsvermerk

- **2026-11-14**: Frontmatter-Datum und Disclaimer-Stand aktualisiert.
  Fassung-Hinweis ergaenzt (Aenderung durch G v. 12.05.2026
  BGBl. 2026 I Nr. 139, textlich zudem G v. 03.07.2026 BGBl. 2026 I Nr. 199).
  Materielle Paragraphen (§§ 4, 26, 38, 42, 43) gegen gesetze-im-internet.de
  unveraendert; kein neues Beschaeftigtendatengesetz in Kraft.
- **2026-11-14 (Nachlauf PR, API-Gegenprobe)**: BAG 2 AZR 133/18 (bisher
  mit Datum 27.07.2017 fuer Keylogger-Entscheidung zitiert) ueber die
  Rechtsinformations-API des Bundes abgefragt — Treffer: 23.08.2018,
  Videoueberwachung. Aktenzeichen auf **BAG 2 AZR 681/16** korrigiert und
  die eigentliche Keylogger-Entscheidung primaer belegt (ECLI
  DE:BAG:2017:270717.U.2AZR681.16.0). BAG 8 AZR 253/20 ebenfalls geprueft —
  Treffer passen inhaltlich nicht zur KB-Aussage "Auskunftsanspruch Art. 15
  DSGVO auch fuer Beschaeftigte"; Zitat entfernt und in Hinweisblock
  "Nicht zitieren" dokumentiert, Aussage mit Verifikationsmarker belassen.
