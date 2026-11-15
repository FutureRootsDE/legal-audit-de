---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/urhg/__44b.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/urhg/__60d.html
  - https://eur-lex.europa.eu/eli/reg/2024/1689/oj
  - http://data.europa.eu/eli/reg/2026/1744/oj
  - https://digital-strategy.ec.europa.eu/en/policies/gpai-code-practice
  - https://www.lto.de/recht/hintergruende/h/kuenstliche-intelligenz-ki-urheberrecht-text-data-mining-lg-hamburg-310o22723
  - https://www.cmshs-bloggt.de/rechtsthemen/kuenstliche-intelligenz/erstes-urteil-deutschlands-zur-urheberrechtlichen-zulaessigkeit-des-ki-trainings-ergangen/
  - https://www.dr-bahr.com/news/nutzung-von-fotos-durch-ki-urheberrechtlich-erlaubt-laion-fall.html
verifiziert-am: 2026-11-14
teilverifiziert-am: 2026-11-15
geltungsbereich: [DE, EU]
eli: http://data.europa.eu/eli/reg/2024/1689/oj
eli-aendvo: http://data.europa.eu/eli/reg/2026/1744/oj
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
> **Status-Hinweis (November 2026):** Fuer GPAI-Anbieter gelten Art. 53 KI-VO
> (Urheber-Policy + Trainingsdaten-Summary) seit 02.08.2025. Die ursprünglich
> fuer 02.08.2026 (Anhang III) bzw. 02.08.2027 (Anhang I) vorgesehenen
> Hochrisiko-Pflichten wurden durch den **Digital Omnibus on AI
> (VO (EU) 2026/1744, in Kraft 27.07.2026 nach ihrem Art. 4)** auf **02.12.2027** bzw.
> **02.08.2028** verschoben. Die Transparenzpflichten des Art. 50 (Chatbot,
> synthetische Inhalte, Deepfakes) gelten planmaessig seit **02.08.2026**.

# KI-Training & Urheberrecht — § 44b UrhG, Opt-Out und kommerzieller TDM

## Kurz-Ueberblick

KI-Training mit urheberrechtlich geschuetzten Werken steht in DE/EU auf der Grundlage von **§ 44b UrhG** (kommerziell) bzw. **§ 60d UrhG** (Forschung), die Art. 3 und 4 der **DSM-Richtlinie (EU) 2019/790** umsetzen. Die **TDM-Schranke** erlaubt automatisierte Analyse rechtmaessig zugaenglicher Werke — allerdings mit einem **kritischen Opt-Out fuer Rechteinhaber**.

Seit **02.08.2025** verlangt **Art. 53 AI Act** zusaetzlich, dass GPAI-Anbieter eine **Policy zur Einhaltung des Unionsurheberrechts** implementieren und insbesondere **maschinenlesbare Opt-Outs respektieren** muessen. Damit wird die zivilrechtliche Grenze aus § 44b zur **regulatorischen Compliance-Pflicht fuer KI-Anbieter** erhoben.

## Kernaussagen

### § 44b UrhG (kommerzielles TDM)

1. **Was ist TDM?** Automatisierte Analyse digitaler Werke zur Gewinnung von Informationen ueber Muster, Trends, Korrelationen.
2. **Erlaubt**: Vervielfaeltigung rechtmaessig zugaenglicher Werke fuer TDM; Loeschung nach Abschluss erforderlich.
3. **Opt-Out**: Rechtsinhaber kann sich die Nutzung vorbehalten. Bei **online zugaenglichen Werken** nur wirksam in **maschinenlesbarer Form**.

### § 60d UrhG (Forschungs-TDM)

Privilegierte Forschungsorganisationen; **kein Opt-Out** moeglich (zwingende Schranke). Privilegiert sind Forschungsorganisationen, die eine der drei Alternativen des § 60d Abs. 2 Satz 2 UrhG erfuellen; ausgeschlossen bei bestimmendem Einfluss und bevorzugtem Ergebniszugang eines privaten Unternehmens (§ 60d Abs. 2 Satz 3 UrhG).

### LG Hamburg Urt. v. 27.09.2024 — LAION/Kneschke (Az. 310 O 227/23)

- Erstes deutsches Urteil zur urheberrechtlichen Zulaessigkeit von KI-Trainingsdatensaetzen.
- **Ergebnis**: LAION durfte das streitgegenstaendliche Foto fuer den LAION-5B-Datensatz nutzen — **aufgrund § 60d UrhG** (Forschungsprivileg); ob auch § 44b UrhG greift, liess das LG offen (obiter).
- Das Gericht bewertete nur den Download und Abgleich fuer den Datensatz als TDM (laut Pressemitteilung des Gerichts).
- AI Act (Art. 53) wird zur Auslegungshilfe herangezogen.
- **Grenze**: Ueber die anschliessende Verwendung zum KI-Training hat die Kammer ausdruecklich nicht entschieden (laut Pressemitteilung des Gerichts); kommerzielles TDM bleibt an den Nutzungsvorbehalt nach § 44b Abs. 3 UrhG gebunden.

**Berufungsinstanz**: **OLG Hamburg, Urt. v. 10.12.2025 — 5 U 104/24** —
Berufung des Klaegers zurueckgewiesen, erstinstanzliches Urteil bestaetigt.
Laut Pressemitteilung des Gerichts: Tragend ist § 44b UrhG, weil der
Nutzungsvorbehalt nicht maschinenlesbar war (§ 44b Abs. 3 Satz 2 UrhG);
zusaetzlich § 60d UrhG, weil kein bestimmender Einfluss eines privaten
Unternehmens bestehe (§ 60d Abs. 2 Satz 3 UrhG). Nicht rechtskraeftig,
**Revision zum BGH zugelassen**. (Beleg: Pressemitteilung des
Hanseatischen OLG).

### Art. 53 AI Act (seit 02.08.2025)

GPAI-Anbieter (= Anbieter von Foundation Models) muessen:
- Eine **Policy zur Respektierung der EU-Urheberrechte** erstellen
- Insbesondere **maschinenlesbare Opt-Outs nach Art. 4 DSM-RL / § 44b Abs. 3 UrhG respektieren**
- Eine **oeffentliche, hinreichend detaillierte Zusammenfassung** der Trainingsdaten bereitstellen (Template Summary durch Kommission)

Der **General-Purpose AI Code of Practice** wurde in finaler Fassung am **10.07.2025** veroeffentlicht und liefert einen praxisnahen Konformitaetspfad fuer Art. 53 (Safety-, Transparenz- und Copyright-Kapitel). Signatoren laut Kommissionsseite "Signatories of the GPAI Code of Practice" (digital-strategy.ec.europa.eu, abgerufen 2026-11-14): 22 Unterzeichner laut Kommission, u.a. Anthropic, OpenAI, Google, Microsoft, Mistral, Cohere, IBM, Aleph Alpha, Black Forest Labs; xAI hat nur das Safety-Kapitel gezeichnet. Die Seite nennt kein Datum je Zeichnung; Zahl vor Verwendung neu abrufen.

Durch die **VO (EU) 2026/1744 (Digital Omnibus on AI, in Kraft 27.07.2026)** erhält das Büro für Künstliche Intelligenz nach den neuen Art. 75a bis 75d KI-VO eigenständige Aufsichts- und Durchsetzungsbefugnisse — allerdings nicht gegen "GPAI-Anbieter" pauschal, sondern nur gegen die **Akteure nach Art. 75 Abs. 1 KI-VO n. F.** (Anbieter von KI-Systemen auf Grundlage eines GPAI-Modells desselben Anbieters bzw. Konzernanbieters, mit Ausnahmen für Anhang-I-Produkte, bestimmte Anhang-III-Systeme und Strafverfolgung; zudem KI-Systeme, die VLOP/VLOSE i. S. v. VO (EU) 2022/2065 bilden oder in sie integriert sind). Dazu zählen nach Art. 75a Informationsersuchen und Inspektionen, nach Art. 75b Verpflichtungszusagen, nach Art. 75c Geldbußen (sinngemäß Art. 99 Abs. 3 bis 7) und Zwangsgelder; diese "dürfen gegebenenfalls 5 % der durchschnittlichen Tageseinnahmen oder des durchschnittlichen weltweiten Jahresumsatzes im vorangegangenen Geschäftsjahr pro Tag, berechnet ab dem durch den Beschluss bestimmten Tag, nicht übersteigen" (Art. 75c Abs. 5 KI-VO n. F.). Fünfjährige Verjährung (Art. 75c Abs. 8). Art. 75d regelt Verteidigungs- und Akteneinsichtsrechte. Die Aufsicht und Durchsetzung **gegenüber Anbietern von KI-Modellen mit allgemeinem Verwendungszweck** (GPAI-Modelle) liegt dagegen nach **Art. 88 KI-VO** weiterhin bei der Kommission / beim Büro für Künstliche Intelligenz als **ausschließlicher Zuständigkeit**; Erwägungsgrund 31 der VO (EU) 2026/1744 verweist auf die ausschließliche Befugnis nach Art. 88 und präzisiert den Umfang der ausschließlichen Systemaufsicht des Büros für KI.

## Opt-Out-Mechanismen in der Praxis

Da § 44b Abs. 3 "maschinenlesbar" verlangt, haben sich verschiedene technische Ansaetze entwickelt:

### Tier 1 — weitgehend anerkannt

- **`robots.txt` mit user-agents wie `GPTBot`, `CCBot`, `ClaudeBot`, `Google-Extended`, `PerplexityBot`**
- **C2PA-Metadaten** in Bildern mit `do_not_train`-Assertion
- HTTP-Response-Header `X-Robots-Tag: noai, noimageai`

### Tier 2 — im Entwurf, zunehmend Praxis

- **`ai.txt`** (TDM Reservation Protocol; Text-Datei im Root)
- **W3C TDMRep** (TDM Reservation Protocol) — HTTP-Header `TDM-Reservation: 1` und `tdmrep.json`
- EPUB-Metadaten fuer Verlage

### Tier 3 — umstritten: rein natuerlichsprachliche Vorbehalte

- Reine natuerlichsprachliche AGB-Klauseln ohne technisches Label
- Nur-Mensch-lesbare Urheberhinweise in PDFs
- Allgemeine Nutzungsbedingungen ohne technisches Format

Das OLG Hamburg (10.12.2025, 5 U 104/24, nicht rechtskraeftig) hielt einen solchen Vorbehalt laut Pressemitteilung des Gerichts fuer nicht maschinenlesbar; das LG Hamburg (27.09.2024, obiter) neigte laut Pressemitteilung des Gerichts zur Gegenansicht; ErwG 18 DSM-RL nennt ausdruecklich auch "Geschaeftsbedingungen einer Website". Bis zur BGH-Entscheidung zusaetzlich technisches Format setzen.

**Empfehlung fuer eigene Webseiten** (Opt-Out als Urheber):
```text
# robots.txt
User-agent: GPTBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
User-agent: CCBot
Disallow: /
User-agent: Google-Extended
Disallow: /
User-agent: PerplexityBot
Disallow: /
User-agent: anthropic-ai
Disallow: /
```

Plus `ai.txt`:
```text
User-Agent: *
Disallow: *
```

## Urheberrecht bei KI-Output

### Kein eigener Urheberschutz fuer reinen KI-Output

KI-generierte Werke ohne menschliche Schoepfungshoehe sind **NICHT urheberrechtlich geschuetzt** (mangels Werkqualitaet nach § 2 UrhG). Das bedeutet:
- Keine eigene Abwehrrechte des Generierers gegen Kopie
- Wettbewerbsrechtlicher Leistungsschutz (UWG) kann greifen
- Bei menschlicher Bearbeitung / Kuration eigene Schoepfungshoehe moeglich

### Risiko: KI-Output verletzt Dritt-Urheberrechte

- KI-Modell kann Trainingsdaten **reproduzieren** → "Memorization"-Problem
- LG Muenchen I, Urt. v. 11.11.2025, 42 O 14139/24 (GEMA ./. OpenAI), nicht rechtskraeftig (laut Pressemitteilung des Gerichts): Memorisierung von Liedtexten im Modell und ihre Wiedergabe in Outputs greifen in Verwertungsrechte ein und sind nicht durch die TDM-Schranke (§ 44b UrhG) gedeckt
- Wenn KI-Bild Logos/Markenzeichen/Charaktere erkennbar enthaelt, kann das **Verletzung sein** — unabhaengig davon, dass KI es "generiert" hat
- Empfehlung: **KI-Output auf bekannte Markenzeichen/Werke pruefen**, insbesondere bei gewerblicher Nutzung

## Typische Fallstricke in Codebases

- **Eigenes Scraping fuer Inhouse-KI-Training** ohne Opt-Out-Check
- **Zusammenfassung der Trainingsinhalte**: Die Pflicht zur oeffentlichen Zusammenfassung der Trainingsinhalte (Art. 53 Abs. 1 Buchst. d KI-VO) trifft nur Anbieter von KI-Modellen mit allgemeinem Verwendungszweck; wer Drittmodelle per API nutzt, ist nicht Adressat
- **KI-Output ohne Content-Filter** auf Markenverletzungen
- **Code-Assistenten** (Copilot, Claude Code) koennen lizenzgeschuetzten Open-Source-Code reproduzieren → GPL-Ansteckung-Risiko
- **Keine eigene Opt-Out-Mechanismen** auf eigener Seite, wodurch Inhalte unkontrolliert in Trainingsdatensaetze fliessen
- **TDM-Reservation-Protokoll nicht implementiert** trotz Content-Seite

## Relevanz fuer Codebase-Typen

- **Next.js SaaS mit eigener LLM-Integration**: Nutzung von Drittmodellen (Claude/GPT) ist compliance-freundlicher, da Modellanbieter Art. 53 AI Act einhalten muessen. Eigene Feintuning-Datensaetze → § 44b beachten.
- **Landingpage**: Opt-Out fuer eigene Inhalte setzen (robots.txt, ai.txt).
- **n8n-Scraping-Workflows**: Respekt vor `robots.txt`, `ai.txt`, HTTP-Headern zwingend!
- **E-Commerce**: Produktfotos eigener Herstellung → Opt-Out moeglich; KI-generierte Produktfotos auf Markenzeichen pruefen.
- **Content/Blog**: Entscheidung: eigene Inhalte in Trainingsdatensaetze geben (SEO-Vorteil Citation) oder ausschliessen (Schutz der Schoepfungshoehe)?

## Behoerden-Hinweise

- **BMJV (Bundesministerium der Justiz und fuer Verbraucherschutz)**: Gesetzgebungsstand § 44b UrhG
- **EU-Kommission**: Leitlinien fuer Anbieter von KI-Modellen mit allgemeinem Verwendungszweck; Vorlage fuer die oeffentliche Zusammenfassung der Trainingsinhalte (veroeffentlicht 24.07.2025)
- **VG Wort / VG Bild-Kunst**: Vertreten kollektive Rechte — Diskussion ueber KI-Training-Lizenzen laeuft

## Zitierbare Urteile

- **LG Hamburg, Urt. v. 27.09.2024 — 310 O 227/23 (LAION/Kneschke)** (siehe oben)
- **OLG Hamburg, Urt. v. 10.12.2025 — 5 U 104/24 (LAION-Berufung)**: bestaetigt
  Erstinstanz; tragend § 44b UrhG (Nutzungsvorbehalt nicht maschinenlesbar),
  zusaetzlich § 60d UrhG; nicht rechtskraeftig, Revision zum BGH zugelassen
  (laut Pressemitteilung des Gerichts).
- **US: Thomson Reuters v. ROSS Intelligence** (Februar 2025) — US-Court: kein
  Fair Use fuer kommerzielles KI-Training auf Westlaw-Daten (US-Recht, nicht
  direkt anwendbar, aber Signal).
- **NYT v. OpenAI / Microsoft** (S.D.N.Y., laufend): Verfahren ueber direkte
  Reproduktion urheberrechtlicher Inhalte; Beschluesse zu Discovery 2025.
- **Getty Images (US) Inc. & Ors v. Stability AI Ltd [2025] EWHC 2863 (Ch)**,
  UK High Court, Urteil vom 04.11.2025 (Smith J). Getty hat seine
  urheberrechtlichen Hauptansprüche im Verfahren fallen gelassen; das Gericht
  hat nicht entschieden, ob das Training in UK Urheberrechte verletzt. Der
  verbliebene Anspruch auf sekundäre Urheberrechtsverletzung wurde abgewiesen
  (Stable Diffusion gilt nicht als "infringing copy", da das Modell keine
  Werke speichert oder reproduziert). Teilweise Erfolg bei Marken, weil
  einige Ausgaben das Getty-Wasserzeichen trugen. Berufungszulassung zur
  sekundären Verletzung (AIPPI-Meldung Januar 2026). UK-Recht, für DE/EU
  nicht bindend, Signal für Beweisanforderungen bei "Memorization".

## Siehe auch

- [[../gesetze/urhg]]
- [[../gesetze/ai-act]]
- [[ki-transparenz]]
- [[urheber-stockfoto]]

## Aenderungsvermerk

- **2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1)**: § 60d-Privilegierung nach Abs. 2 Satz 2 und 3 praezisiert; Art. 75c Abs. 5 im Wortlaut; Erwaegungsgrund 31 (nicht 19) der VO (EU) 2026/1744; dejure.org nicht mehr als Tier-1-Beleg; Inkrafttreten der VO (EU) 2026/1744 nach Art. 4; Zeichnerzahl GPAI-Kodex mit Quelle und Abrufdatum, Marker aufgeloest.
- **2026-11-14 (Korrekturlauf nach Gegenprobe am Volltext VO 2026/1744)**: Art. 75a bis 75d KI-VO n. F. am Verordnungs-Wortlaut präzisiert (Adressatenkreis "Akteure nach Art. 75 Abs. 1", nicht "GPAI-Anbieter" pauschal; Zwangsgeld-Bemessung; Art. 75d bestätigt); Platzhalter aufgelöst. Getty Images v. Stability AI [2025] EWHC 2863 (Ch) vom 04.11.2025 als Urteil (nicht mehr "laufend") übernommen.
- **2026-11-14 (Voraufnahme)**: Art. 53-Darstellung aktualisiert; Hochrisiko-Daten (Anhang III 02.12.2027, Anhang I 02.08.2028).
- **2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2)**: LG Muenchen I (GEMA ./. OpenAI, 42 O 14139/24) zur Memorisierung ergaenzt; Art. 53 Abs. 1 Buchst. d: Adressatenkreis klargestellt; LG und OLG Hamburg (LAION) nach der Pressemitteilung des Gerichts praezisiert (tragende Gruende, Reichweite); Tier 3 der Opt-Out-Mechanismen als umstritten; BMJV und Kommissionsangaben berichtigt.
