---
aktualisiert: 2026-11-14
quelle-primaer: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
quellen-sekundaer:
  - http://data.europa.eu/eli/reg/2026/1744/oj
  - https://digital-strategy.ec.europa.eu/en/library/commission-opinion-assessment-code-practice-transparency-ai-generated-content
  - https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
  - https://bundesnetzagentur.de/EN/Areas/Digitalisation/AI/04_Transparency/code_of_practice/start.html
  - https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50
  - https://www.gesetze-im-internet.de/ki-mig/
  - https://recht.bund.de/bgbl/1/2026/223
verifiziert-am: 2026-11-14
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
> **Status-Hinweis:** Art. 50 KI-VO ist seit **02.08.2026 anwendbar**. Chatbot-
> Hinweise, Deepfake-Kennzeichnung und maschinenlesbare Markierung synthetischer
> Inhalte sind damit bereits seit ueber drei Monaten geltendes Recht. Der
> Digital Omnibus on AI (VO (EU) 2026/1744, in Kraft seit 27.07.2026) hat die
> Transparenzpflichten des Art. 50 Abs. 1 bis 4 inhaltlich **nicht entschaerft**;
> er fuehrt lediglich in Art. 111 Abs. 4 eine Uebergangsfrist bis 02.12.2026 fuer
> die maschinenlesbare Markierung durch generative KI-Systeme ein, die bereits
> vor dem 02.08.2026 in Verkehr gebracht wurden. Wortlaut Art. 111 Abs. 4
> KI-VO n. F. (Art. 1 Nr. 39 Buchst. b Omnibus-VO): "Anbieter von KI-Systemen,
> einschließlich KI-Systemen mit allgemeinem Verwendungszweck, die synthetische
> Audio-, Bild-, Video- oder Textinhalte erzeugen, die vor dem 2. August 2026
> in Verkehr gebracht wurden, treffen die erforderlichen Maßnahmen, um
> Artikel 50 Absatz 2 bis zum 2. Dezember 2026 nachzukommen."

# KI-Transparenz (Art. 50 AI Act) — Kennzeichnung und Hinweispflichten

## Kurz-Ueberblick

**Art. 50 VO (EU) 2024/1689** (geaendert durch VO (EU) 2026/1744) regelt die Transparenz- und Kennzeichnungspflichten fuer bestimmte KI-Systeme. Die Pflichten sind seit **02.08.2026** anwendbar. Art. 50 greift auch dann, wenn die KI **nicht** als Hochrisiko-KI klassifiziert ist. Damit ist Art. 50 **der praxisrelevanteste Teil der KI-VO fuer typische Webanwendungen und SaaS**.

Der **Code of Practice on Transparency of AI-Generated Content** wurde in finaler Fassung am **10.06.2026** von der Kommission veröffentlicht. Die **Commission Opinion C(2026) 4839 vom 08.07.2026** (Veröffentlichung 09.07.2026 auf digital-strategy.ec.europa.eu, "Commission opinion on the assessment of the Code of Practice on Transparency of AI-Generated Content") stellt die Angemessenheit zur Erfüllung von Art. 50 Abs. 2, 4 und 5 fest; das KI-Gremium hat am 09.07.2026 eine eigene Angemessenheitsstellungnahme abgegeben. Die Bundesnetzagentur hostet eine englischsprachige Zusammenfassung unter bundesnetzagentur.de (Bereich "Digitalisation/AI/04_Transparency").

Die am **08.05.2026** veröffentlichten **Entwurf-Leitlinien der Kommission zu Art. 50** wurden am **20.07.2026** in finaler Fassung publiziert ("Guidelines on transparency obligations under Article 50 of the AI Act"; Primärquelle digital-strategy.ec.europa.eu, zusätzlich Freshfields- und Faegre-Drinker-Alerts).

## Die vier Transparenzpflichten nach Art. 50

### Art. 50 Abs. 1 — Chatbot-Hinweis

**Adressat:** Anbieter von KI-Systemen, die direkt mit natuerlichen Personen interagieren.

**Pflicht:** System so konzipieren, dass betroffene Personen informiert werden, dass sie mit einer KI interagieren — **ausser es ist offensichtlich** (aus Sicht einer angemessen informierten, aufmerksamen Person).

**Ausnahmen:**
- Offensichtlichkeit
- gesetzlich zulaessige Nutzung zur Straftatenerkennung etc.

**Praxis-Empfehlung:**
- Hinweis *"Du chattest mit einem KI-Assistenten"* vor Beginn der Konversation
- nicht-dismissible Kennzeichnung im Chat-Widget
- nicht nur im Impressum oder in den AGB "verstecken" — der Hinweis muss **vor/bei Interaktion** sichtbar sein

### Art. 50 Abs. 2 — Wasserzeichen / maschinenlesbare Kennzeichnung

**Adressat:** Anbieter von KI-Systemen, die **synthetische Audio-, Bild-, Video- oder Textinhalte** erzeugen oder manipulieren.

**Pflicht:** Outputs muessen in einem **maschinenlesbaren Format** markiert und als kuenstlich erzeugt/manipuliert erkennbar gemacht werden.

**Übergangsfrist nach Art. 111 Abs. 4 KI-VO n. F. (eingefügt durch Art. 1 Nr. 39 Buchst. b Omnibus-VO, in Kraft 27.07.2026):** Anbieter von KI-Systemen (einschließlich GPAI), die synthetische Audio-, Bild-, Video- oder Textinhalte erzeugen und vor dem **02.08.2026** in Verkehr gebracht wurden, treffen die erforderlichen Maßnahmen, um Art. 50 Abs. 2 bis zum **02.12.2026** nachzukommen. Für Neuprodukte ab 02.08.2026 gilt die Pflicht sofort.

**Technische Loesungen (aufgegriffen im Code of Practice vom 10.06.2026):**
- **C2PA** (Coalition for Content Provenance and Authenticity) — Metadaten
- **SynthID** (Google) bzw. **Stable Signature** (Meta) fuer Bilder
- Audio-Wasserzeichen
- Text-Wasserzeichen (noch nicht ausgereift; der Code of Practice akzeptiert alternative Nachweise)

**Ausnahmen:**
- Assistenzfunktionen mit Standardbearbeitung (z.B. Rechtschreibkorrektur)
- Strafverfolgung, Forschung (eng)

### Art. 50 Abs. 3 — Emotions- / biometrische Kategorisierungssysteme

**Adressat:** **Betreiber** eines Emotionserkennungs- oder biometrischen Kategorisierungssystems.

**Pflicht:** Betroffene Personen **vor der Verarbeitung** ueber den Einsatz informieren.

DSGVO-Anforderungen (Art. 9 DSGVO, besondere Kategorien personenbezogener Daten) bleiben unberuehrt. Einsatz am Arbeitsplatz und in Bildungseinrichtungen ist bereits nach Art. 5 Abs. 1 lit. f KI-VO weitgehend verboten.

### Art. 50 Abs. 4 — Deepfake-Kennzeichnung

**Adressat:** **Betreiber**, die KI-Systeme zur Erzeugung oder Manipulation von Deepfakes einsetzen.

**Pflicht:** Inhalte muessen als kuenstlich erzeugt oder manipuliert offengelegt werden.

**Ausnahmen:**
- kuenstlerische, kreative, satirische, fiktionale oder analoge Werke: Kennzeichnung in einer Weise, die Darstellung und Genuss nicht stoert, aber die Existenz des manipulierten Inhalts erkennen laesst
- Strafverfolgung

Fuer Texte zu Angelegenheiten von oeffentlichem Interesse: Kennzeichnungspflicht, ausser menschliche Redaktion hat uebernommen.

**Zusatz-Verbote ab 02.12.2026 (Art. 113 Abs. 3 Buchst. a KI-VO n. F.):** Durch Art. 1 Nr. 7 VO (EU) 2026/1744 wird Art. 5 Abs. 1 Unterabs. 1 KI-VO um die Buchstaben **ba** (nicht einvernehmliche intime Bildnisse, NCII) und **bb** (Material i. S. v. Art. 2 Buchst. c und e RL 2011/93/EU, CSAM) ergänzt. Die neuen Abs. 1a und 1b konkretisieren die Voraussetzungen: Inverkehrbringen/Inbetriebnahme eines solchen KI-Systems ist **nur** verboten, wenn (i) die Erzeugung oder Manipulation die **Zweckbestimmung** des Systems ist oder (ii) sie aufgrund Gestaltung, Training, Architektur, Fähigkeiten oder nutzerseitiger Funktionen ein nach vernünftigem Ermessen absehbares und reproduzierbares Ergebnis ist **und** das System nicht über zumutbare technische Schutzvorkehrungen verfügt. **Verwendung** ist nur verboten, wenn der Betreiber das System zu genau diesem Zweck einsetzt. Die Buchstaben ba und bb erfassen damit nicht jeden nicht-einvernehmlichen intimen Deepfake pauschal, sondern knüpfen an die Systemgestaltung bzw. Zweckbestimmung an.

### Art. 50 Abs. 5 — Barrierefreiheit

Transparenzpflichten muessen **wahrnehmbar und barrierefrei** umgesetzt werden (Schnittmenge mit BFSG).

### Art. 50 Abs. 6/7 — Leitlinien und Code of Practice

Die Kommission veröffentlicht Leitlinien und fördert einen Praxisleitfaden (Code of Practice). Befolgung kann als Konformitätsnachweis dienen. **Abs. 7 wurde durch Art. 1 Nr. 20 VO (EU) 2026/1744 neu gefasst** (nicht bloß redaktionell): Die Kommission prüft "unter weitestgehender Berücksichtigung der Stellungnahme des KI-Gremiums nach dem Verfahren des Artikels 56 Absatz 6 Unterabsatz 1, ob die Befolgung dieser Praxisleitfäden angemessen ist, um die Einhaltung der in den Absätzen 2 und 4 dieses Artikels festgelegten Pflichten zu gewährleisten". Nur wenn sie den Praxisleitfaden für **unangemessen** hält, kann sie einen Durchführungsrechtsakt nach dem Prüfverfahren des Art. 98 Abs. 2 erlassen. Die bisherige unbedingte Durchführungsrechtsakt-Befugnis entfällt damit.

## Typische Fallstricke in Codebases

- **Kein "Du sprichst mit KI"-Hinweis** bei Chatbot (seit 02.08.2026 anwendbar, nicht mehr "in Vorbereitung")
- **Chatbot-Hinweis zu tief versteckt** (nur in AGB, nicht vor Interaktion sichtbar)
- **KI-generierte Marketing-Bilder ohne maschinenlesbare Markierung / C2PA-Metadaten**
- **KI-generierte Blog-Artikel** ohne Kennzeichnung, besonders bei Themen von oeffentlichem Interesse
- **Deepfake-artige Produktvideos** ohne Disclaimer (z.B. generierte Personen im Testimonial)
- **Emotionserkennung in Sales-Tools** (Call-Center-Analyse) — oft verboten oder mind. transparenzpflichtig
- **KI-Kompetenz Art. 4** nicht dokumentiert: Pflicht bleibt bestehen, nur Formulierung durch Omnibus von "stellen sicher" zu "ergreifen Massnahmen" entschaerft — Schulungsdokumentation bleibt faktisch notwendig
- **Keine Dokumentation**, dass Kennzeichnung umgesetzt ist — bei Behoerdenanfrage nicht nachweisbar
- **Legacy-Systeme vor 02.08.2026** ohne Nachruestungs-Plan bis 02.12.2026 (Art. 111 Abs. 4)

## Pflicht-Elemente fuer Codebase-Integration

Fuer **LLM-Chat-Integrationen** (typischer SaaS-Fall):

```
// Pseudocode — JSX/Vue-agnostisch
<ChatWidget>
  <InitialMessage prominent>
    "Du chattest mit einem KI-Assistenten (Claude/Anthropic).
     Antworten koennen Fehler enthalten. Weiterer Hinweis im Impressum."
  </InitialMessage>
  <!-- nicht wegklickbar bis Erstinteraktion -->
</ChatWidget>
```

Fuer **KI-Bildgenerierung**:
- C2PA-Metadaten in EXIF schreiben
- sichtbare Wasserzeichen oder zumindest maschinenlesbare Markierung (Pflicht seit 02.08.2026)
- Audit-Log, wer wann welche KI genutzt hat
- Hinweis in Dateinamen (z.B. `-ai-generated.png`)

Fuer **KI-generierten Text im CMS**:
- Frontmatter-Feld `ai_generated: true`
- Hinweis im Artikel-Footer (sinngemaess): *"Dieser Artikel wurde unter Einsatz von KI (ChatGPT/Claude) verfasst und redaktionell geprueft."*

## Relevanz fuer Codebase-Typen

- **Next.js SaaS**: Art. 50 Abs. 1 bei Chatbot; Abs. 2 bei Bild-/Textgenerierung. Hohe Relevanz. Altbestand bis 02.12.2026 nachruesten.
- **Landingpage**: Art. 50 Abs. 1 bei LandingPage-Chatbot. Oft uebersehen.
- **n8n Automation**: bei Content-Automation Abs. 2 und 4 bei Bildern und Videos; Abs. 1 wenn n8n-Bot auf Social Media antwortet.
- **E-Commerce**: KI-Produktempfehlungen regelmaessig NICHT Art. 50; KI-generierte Produktfotos aber Abs. 2.
- **Content/Blog**: Kennzeichnungspflicht fuer KI-Artikel seit 02.08.2026, insbesondere bei Themen von oeffentlichem Interesse.

## Behoerden-Hinweise

- **Büro für Künstliche Intelligenz (EU AI Office)**: federführend für Leitlinien und Code of Practice; seit 27.07.2026 eigenständige Durchsetzungsbefugnisse nach Art. 75a bis 75d KI-VO n. F. gegenüber den Akteuren nach Art. 75 Abs. 1 (bestimmte GPAI-basierte KI-Systeme sowie VLOP/VLOSE-integrierte Systeme), nicht pauschal gegenüber allen GPAI-Anbietern.
- **AI Act Service Desk**: https://ai-act-service-desk.ec.europa.eu/
- **Bundesnetzagentur**: nach § 2 Abs. 1 **KI-MIG** (ausgefertigt 22.07.2026, BGBl. 2026 I Nr. 223 vom 28.07.2026, in Kraft seit 29.07.2026) **koordinierende Marktüberwachungsbehörde und Auffangbehörde** für die KI-VO, soweit das Gesetz nichts anderes bestimmt. Sektorale Sonderzuständigkeiten bleiben bestehen: Produkte nach Anhang I bei den jeweils zuständigen Marktüberwachungsbehörden (§ 2 Abs. 2), BaFin für Finanzdienstleistungen (§ 2 Abs. 3 und 4), Landesbehörden für Landeseinrichtungen und bestimmte Medienangebote (§ 2 Abs. 6 und 8), eigene Aufsicht für die Deutsche Welle. Die KI-Marktüberwachungskammer nach § 2 Abs. 5 KI-MIG ist für bestimmte Hochrisiko-Felder zuständig (Strafverfolgung, Migration, Justiz, Demokratie, Beschäftigung, kritische Infrastruktur, Zugang zu wesentlichen Diensten). Bußgeldzuständigkeit folgt der jeweiligen Marktüberwachungszuständigkeit. Primärquellen: https://www.gesetze-im-internet.de/ki-mig/ und https://recht.bund.de/bgbl/1/2026/223. Die BNetzA betreibt zusätzlich eine englischsprachige Zusammenfassungsseite zum Code of Practice on Transparency unter bundesnetzagentur.de/EN/Areas/Digitalisation/AI/04_Transparency/.

## Zitierbare Urteile

Keine bisher. Art. 50 ist erst seit 02.08.2026 anwendbar; Rechtsprechung entsteht erfahrungsgemaess mit Zeitversatz.

## Siehe auch

- [[../gesetze/ai-act]] — vollstaendige KI-VO inkl. Digital Omnibus
- [[../gesetze/dsa]] — Art. 26 DSA Werbetransparenz (ueberschneidend)
- [[ki-content]] — KI-Training und Urheberrecht
- [[barrierefreiheit]] — BFSG-Anforderung (Schnittmenge mit Art. 50 Abs. 5)

## Aenderungsvermerk

- **2026-11-14 (Korrekturlauf nach Gegenprobe am Volltext VO 2026/1744)**: Art. 111 Abs. 4 KI-VO n. F. im Wortlaut übernommen (Platzhalter aufgelöst). Chronologie Code of Practice on Transparency präzisiert (Finalfassung 10.06.2026, Opinion C(2026) 4839 vom 08.07.2026, Angemessenheitsstellungnahme KI-Gremium 09.07.2026); finale Art.-50-Leitlinien der Kommission vom 20.07.2026 ergänzt (vorheriger Marker aufgelöst). Formulierung "vollständig verboten" für NCII/CSAM durch die am Verordnungs-Wortlaut orientierten Voraussetzungen des Art. 5 Abs. 1a/1b ersetzt. Art. 50 Abs. 7 KI-VO n. F. nicht mehr als "redaktionell", sondern als Neufassung mit bedingter Durchführungsrechtsakt-Befugnis dargestellt. BNetzA-Rolle nach § 2 KI-MIG als "koordinierende Marktüberwachungsbehörde und Auffangbehörde" präzisiert.
- **2026-11-14 (Voraufnahme)**: Status umgestellt von "ab 02.08.2026" auf "seit 02.08.2026 anwendbar".
- **2026-10-24**: BNetzA-Zuständigkeit nach KI-MIG ergänzt.
