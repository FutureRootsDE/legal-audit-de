---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
quellen-sekundaer:
  - https://artificialintelligenceact.eu/implementation-timeline/
  - https://ai-act-service-desk.ec.europa.eu/
  - https://artificialintelligenceact.eu/article/50/
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

# KI-Verordnung (EU AI Act) — VO (EU) 2024/1689

## Kurz-Ueberblick

Die Verordnung (EU) 2024/1689 zur Festlegung harmonisierter Vorschriften fuer Kuenstliche Intelligenz ist die **weltweit erste umfassende KI-Regulierung**. Sie ist am **01.08.2024 in Kraft getreten** und entfaltet ihre Pflichten in einem **Stufenplan bis 2027** (teilweise bis 2030).

Der AI Act verfolgt einen **risikobasierten Ansatz**:
- **Verbotene KI-Praktiken** (Art. 5) — Social Scoring, manipulative KI, biometrische Echtzeit-Identifizierung im oeffentlichen Raum etc.
- **Hochrisiko-KI** (Anhang I + Anhang III) — umfassende Konformitaetspflichten
- **KI-Systeme mit Transparenzpflichten** (Art. 50) — Chatbots, Deepfakes, KI-Content
- **Allgemeine KI-Modelle (GPAI)** (Art. 51–56) — Foundation Models wie Claude, GPT, Gemini
- **Minimalrisiko** — keine Pflichten

## Stufenplan (Stand 2026-04)

| Datum | Was gilt |
|-------|----------|
| **01.08.2024** | Inkrafttreten |
| **02.02.2025** | Verbotene Praktiken (Art. 5), KI-Kompetenz-Pflicht (Art. 4) — **gilt** |
| **02.08.2025** | GPAI-Pflichten (Art. 51–56), Governance (Art. 64–70), Sanktionen (Art. 99–100), notifizierte Stellen — **gilt** |
| **02.08.2026** | **Vollanwendung**: Hochrisiko-KI nach Anhang III, Transparenz Art. 50, KI-Reallabore — **in < 4 Monaten aktiv** |
| **02.08.2027** | Hochrisiko-KI nach Anhang I (Produkte mit CE-Kennzeichnung); GPAI vor 02.08.2025 muss compliant sein |
| **31.12.2030** | Grosse IT-Systeme der Union (Migration) |

**Aktueller operativer Stand (April 2026):**
- Verbotene Praktiken und KI-Kompetenz: **voll anwendbar**
- GPAI-Pflichten: **voll anwendbar** (Anbieter muessen Code of Practice oder aequivalente Konformitaetspfade nutzen)
- Art. 50 Transparenzpflichten: **Anwendung ab 02.08.2026** — Vorbereitung jetzt!
- Zweiter Entwurf des **Code of Practice** zur KI-Kennzeichnung wurde am **03.03.2026** veroeffentlicht

## Schluesselparagraphen / Kernaussagen

### Art. 5 — Verbotene KI-Praktiken (seit 02.02.2025)

- Subliminale/manipulative Techniken, die Schaden verursachen
- Ausnutzung der Schutzbeduerftigkeit (Alter, Behinderung, soziale/wirtschaftliche Lage)
- **Social Scoring** durch Behoerden oder private Akteure mit benachteiligender Wirkung
- Praediktive Polizeiarbeit allein auf Profiling basierend
- Ungezieltes Scraping von Gesichtsbildern fuer Datenbanken (wie Clearview AI)
- **Emotionserkennung am Arbeitsplatz / in Bildungseinrichtungen** (Ausnahmen: medizinisch, sicherheitsrelevant)
- Biometrische Kategorisierung nach sensiblen Merkmalen (Rasse, politische Ansichten, sexuelle Orientierung)
- **Echtzeit-Fernidentifizierung** im oeffentlichen Raum durch Strafverfolgung (nur enge Ausnahmen)

### Art. 6 + Anhang III — Hochrisiko-KI (ab 02.08.2026)

Acht Bereiche:
1. Biometrie (Fernidentifizierung, Kategorisierung, Emotionserkennung)
2. Kritische Infrastruktur (Verkehr, Energie, Wasser)
3. Bildung (Zugang, Bewertung)
4. Beschaeftigung, Personalmanagement, Selbststaendigkeit (Recruiting, Entlassung, Leistungsbewertung)
5. Grundlegende private/oeffentliche Dienste (Bonitaet, Notfalldienste, Sozialleistungen, Krankenversicherung)
6. Strafverfolgung
7. Migration, Asyl, Grenzkontrollen
8. Justiz und demokratische Prozesse

Pflichten: Risikomanagement (Art. 9), Data Governance (Art. 10), technische Dokumentation (Art. 11), Aufzeichnungspflichten (Art. 12), Transparenz gegenueber Betreibern (Art. 13), menschliche Aufsicht (Art. 14), Genauigkeit/Robustheit/Cybersicherheit (Art. 15), Konformitaetsbewertung (Art. 43), Registrierung (Art. 49), CE-Kennzeichnung (Art. 48).

### Art. 50 — Transparenzpflichten fuer bestimmte KI-Systeme (ab 02.08.2026)

Unmittelbar relevant fuer nahezu **jede SaaS-Anwendung mit KI-Integration**:

**Abs. 1**: Anbieter muessen KI-Systeme, die mit Menschen interagieren, so konzipieren, dass der Nutzer informiert wird, dass er mit einer KI interagiert — **es sei denn, dies ist offensichtlich**.

**Abs. 2**: Anbieter von KI, die synthetische Audio/Bild/Video/Text-Inhalte erzeugt, muessen **technisch markieren (z. B. Wasserzeichen, C2PA-Metadaten)**, dass der Output KI-erzeugt ist.

**Abs. 3**: Betreiber eines Emotionserkennungs- oder biometrischen Kategorisierungssystems muessen betroffene Personen **vor der Verarbeitung** informieren.

**Abs. 4**: Betreiber, die KI-generierte **Deepfakes** verbreiten, muessen diese **als kuenstlich erzeugt kennzeichnen**. Ausnahmen: kuenstlerische, satirische, fiktive Werke — dort aber Hinweis in einer Weise, die die Wahrnehmung nicht stoert.

**Ausnahme Strafverfolgung**: Art. 50 gilt nicht, wenn Nutzung gesetzlich zur Aufdeckung/Verhinderung/Untersuchung von Straftaten zugelassen ist.

### Art. 51–56 — Allgemeine KI-Modelle (GPAI) (seit 02.08.2025)

Anbieter von Foundation Models (Claude, GPT, Gemini, Llama etc.) muessen:
- Technische Dokumentation fuehren (Art. 53)
- Nachgelagerten Anbietern Informationen bereitstellen
- **Policy zum Urheberrecht** festlegen, die insbesondere den **maschinenlesbaren Opt-Out nach § 44b UrhG / Art. 4 DSM-RL beachtet**
- Oeffentliche Zusammenfassung der Trainingsdaten veroeffentlichen
- Bei **systemischem Risiko** (rechnerische Schwelle: **10^25 FLOP** Trainingsaufwand): zusaetzliche Evaluations-, Risikominderungs- und Meldepflichten

### Sanktionen (Art. 99)

- Verstoesse gegen verbotene Praktiken: bis **35 Mio. EUR oder 7 %** des weltweiten Jahresumsatzes
- Verstoesse gegen andere Pflichten: bis **15 Mio. EUR oder 3 %**
- Falsche Informationen an Behoerden: bis **7,5 Mio. EUR oder 1 %**

## Typische Fallstricke in Codebases

- **Chatbot ohne KI-Hinweis** (Art. 50 Abs. 1) — klassischer Fall bei SaaS-Support-Bots
- **KI-Bildgenerierung ohne Wasserzeichen** (Art. 50 Abs. 2) — z. B. Stable Diffusion / DALL-E / Flux-Integration in Tools
- **Deepfake in Marketing/Content** ohne Kennzeichnung (Art. 50 Abs. 4)
- **Emotionserkennung** in UX-Tools, Sales-Analytics, Recruiting → **fast immer verboten oder hochrisikant**
- **Hochrisiko-KI in HR** (Recruiting-Tools, automatisierte Bewerbersichtung) — Konformitaetsbewertung erforderlich
- **GPAI-Feintuning**: Nachgelagerte Anbieter koennen selbst GPAI-Pflichten uebernehmen, wenn sie substantielle Modifikation vornehmen
- **Trainingsdaten-Opt-Out nicht beachtet** beim Eigen-Training → Konflikt mit § 44b UrhG
- **KI-Kompetenz** (Art. 4): Mitarbeiter, die KI einsetzen, muessen **nachweislich geschult** sein — Dokumentation erforderlich

## Relevanz fuer Codebase-Typen

- **Next.js SaaS mit LLM-Integration** (Chat, Assistent): **Art. 50 Abs. 1** Hinweispflicht; wenn Bilder/Texte generiert werden auch Abs. 2
- **Landingpage mit Chatbot**: Art. 50 Abs. 1 — Hinweis "Du chattest mit einer KI"
- **n8n-Workflows mit Claude/OpenAI**: Bei automatisierter Content-Erstellung → Wasserzeichen/Kennzeichnung erforderlich; Hochrisiko nur wenn HR/Scoring/Bildung
- **E-Commerce mit KI-Produktempfehlungen / Personalisierung**: Meist kein Hochrisiko, aber Art. 50 wenn Chatbot oder KI-Content
- **Content/Blog mit KI-generierten Artikeln**: Ab 02.08.2026 Kennzeichnungspflicht fuer synthetischen Content

## Behoerden-Hinweise

- **EU AI Office** (unter DG CNECT): Zentrale EU-Koordination, insbesondere fuer GPAI
- **Deutschland**: Bundesnetzagentur als Marktueberwachungsbehoerde (KI-Marktueberwachungsgesetz in Beratung / teilweise verabschiedet — `<<VERIFIKATION AUSSTEHEND>>` zum exakten Stand des deutschen Durchfuehrungsgesetzes im April 2026)
- **AI Act Service Desk**: https://ai-act-service-desk.ec.europa.eu/ — offizielle EU-Infostelle
- **Offizielle Leitlinien**: Kommission veroeffentlicht laufend Guidelines (z. B. zu verbotenen Praktiken Februar 2025, zu GPAI Juli 2025)

## Zitierbare Urteile

**Keine relevanten Endurteile bisher.** Der AI Act ist neu und Hochrisiko/Art. 50 erst ab 02.08.2026 anwendbar. Rechtsprechung gibt es praktisch noch nicht.

Indirekt relevant:
- **LG Hamburg, Urt. v. 27.09.2024, 310 O 227/23 (LAION/Kneschke)** — zu § 44b UrhG / TDM; erwaehnt den AI Act als Auslegungshilfe (siehe [[urhg]])

## Siehe auch

- [[../themen/ki-transparenz]] — Art. 50 AI Act Detailbetrachtung
- [[../themen/ki-content]] — KI-Training und Urheberrecht (§ 44b UrhG)
- [[urhg]] — Urheberrecht, TDM-Schranke
- [[dsa]]
- [[dma]]
