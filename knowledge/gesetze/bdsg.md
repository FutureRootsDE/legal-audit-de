---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/bdsg_2018/
quellen-sekundaer:
  - https://www.bfdi.bund.de/
  - https://www.datenschutzkonferenz-online.de/
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
- **BAG 2 AZR 133/18, 27.07.2017** — Keylogger ohne konkreten Tatverdacht unzulässig
- **BAG 8 AZR 253/20, 05.05.2022** — Auskunftsanspruch nach Art. 15 DSGVO auch für Beschäftigte

## Siehe auch

- [[gesetze/dsgvo]]
- [[gesetze/tdddg]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]]
