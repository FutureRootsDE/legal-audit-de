---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/urhg/__44b.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/urhg/__60d.html
  - https://www.lto.de/recht/hintergruende/h/kuenstliche-intelligenz-ki-urheberrecht-text-data-mining-lg-hamburg-310o22723
  - https://www.cmshs-bloggt.de/rechtsthemen/kuenstliche-intelligenz/erstes-urteil-deutschlands-zur-urheberrechtlichen-zulaessigkeit-des-ki-trainings-ergangen/
  - https://eur-lex.europa.eu/eli/reg/2024/1689/oj
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

Privilegierte Forschungsorganisationen; **kein Opt-Out** moeglich (zwingende Schranke). Die Privilegierung entfaellt bei kommerziellem Charakter der Aktivitaet.

### LG Hamburg Urt. v. 27.09.2024 — LAION/Kneschke (Az. 310 O 227/23)

- Erstes deutsches Urteil zur urheberrechtlichen Zulaessigkeit von KI-Trainingsdatensaetzen.
- **Ergebnis**: LAION durfte das streitgegenstaendliche Foto fuer den LAION-5B-Datensatz nutzen — **aufgrund § 60d UrhG** (Forschungsprivileg), nicht wegen § 44b.
- Gericht bestaetigt allgemein: Erstellung von KI-Trainingsdaten IST TDM.
- AI Act (Art. 53) wird zur Auslegungshilfe herangezogen.
- **Grenze**: Die Entscheidung gilt fuer Forschungskontext; kommerzielles Training bleibt an § 44b Abs. 3 Opt-Out gebunden.

**Berufungsinstanz** `<<VERIFIKATION AUSSTEHEND>>` — OLG Hamburg-Urteil sollte beim naechsten Update geprueft werden.

### Art. 53 AI Act (ab 02.08.2025)

GPAI-Anbieter (= Anbieter von Foundation Models) muessen:
- Eine **Policy zur Respektierung der EU-Urheberrechte** erstellen
- Insbesondere **maschinenlesbare Opt-Outs nach Art. 4 DSM-RL / § 44b Abs. 3 UrhG respektieren**
- Eine **oeffentliche, hinreichend detaillierte Zusammenfassung** der Trainingsdaten bereitstellen (Template Summary durch Kommission)

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

### Tier 3 — nicht "maschinenlesbar" i.S.v. § 44b Abs. 3

- Reine natuerlichsprachliche AGB-Klauseln ohne technisches Label
- Nur-Mensch-lesbare Urheberhinweise in PDFs
- Allgemeine Nutzungsbedingungen ohne technisches Format

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
- Wenn KI-Bild Logos/Markenzeichen/Charaktere erkennbar enthaelt, kann das **Verletzung sein** — unabhaengig davon, dass KI es "generiert" hat
- Empfehlung: **KI-Output auf bekannte Markenzeichen/Werke pruefen**, insbesondere bei gewerblicher Nutzung

## Typische Fallstricke in Codebases

- **Eigenes Scraping fuer Inhouse-KI-Training** ohne Opt-Out-Check
- **Kein Audit-Log** der Trainingsdatenquellen (Art. 53 Abs. 1 lit. d AI Act: Training-Content-Summary)
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

- **BMJ (Bundesjustizministerium)**: Gesetzgebungsstand § 44b UrhG
- **EU-Kommission (DG CNECT)**: Art. 53 AI Act Guidelines, Template fuer Training Data Summary (veroeffentlicht ca. 2025)
- **VG Wort / VG Bild-Kunst**: Vertreten kollektive Rechte — Diskussion ueber KI-Training-Lizenzen laeuft

## Zitierbare Urteile

- **LG Hamburg, Urt. v. 27.09.2024 — 310 O 227/23 (LAION/Kneschke)** (siehe oben)
- **US: Thomson Reuters v. ROSS Intelligence** (Februar 2025) — US-Court: kein Fair Use fuer kommerzielles KI-Training auf Westlaw-Daten (US-Recht, nicht direkt anwendbar, aber Signal)
- `<<VERIFIKATION AUSSTEHEND>>` — weitere anhaengige Verfahren (Getty Images / Stability AI, New York Times / OpenAI)

## Siehe auch

- [[../gesetze/urhg]]
- [[../gesetze/ai-act]]
- [[ki-transparenz]]
- [[urheber-stockfoto]]
