---
aktualisiert: 2026-04-19
quelle-primaer: https://artificialintelligenceact.eu/article/50/
quellen-sekundaer:
  - https://eur-lex.europa.eu/eli/reg/2024/1689/oj
  - https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50
  - https://www.srd-rechtsanwaelte.de/blog/kennzeichnungspflicht-code-of-practice-zur-transparenz-von-ki-generierten-inhalten
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

# KI-Transparenz (Art. 50 AI Act) — Kennzeichnung und Hinweispflichten

## Kurz-Ueberblick

**Art. 50 VO (EU) 2024/1689** regelt die Transparenz- und Kennzeichnungspflichten fuer bestimmte KI-Systeme. Die Pflichten sind ab **02.08.2026** anwendbar — d. h. im **April 2026 muessen Anbieter und Betreiber JETZT vorbereiten**.

Art. 50 greift auch dann, wenn die KI **nicht** als Hochrisiko-KI klassifiziert ist. Damit ist Art. 50 **der praxisrelevanteste Teil des AI Act fuer typische Webanwendungen und SaaS**.

Parallel dazu hat die Kommission am **03.03.2026** den **zweiten Entwurf des Code of Practice** zur Kennzeichnung KI-generierter Inhalte veroeffentlicht (Art. 50 Abs. 7 AI Act).

## Die vier Transparenzpflichten nach Art. 50

### Art. 50 Abs. 1 — Chatbot-Hinweis

**Wer ist Adressat?** Anbieter (!) von KI-Systemen, die **direkt mit natuerlichen Personen interagieren**.

**Pflicht**: Systeme sind so zu konzipieren, dass **betroffene Personen informiert werden**, dass sie mit einer KI interagieren — **ausser es ist offensichtlich** (aus Sicht einer angemessen informierten, aufmerksamen Person).

**Ausnahmen**:
- Offensichtlichkeit (z. B. explizit gekennzeichnete Support-Chatbots moeglicherweise)
- Gesetzlich zulaessige Nutzung zur Straftatenerkennung etc.

**Praxis-Empfehlung**:
- Hinweis *"Du chattest mit einem KI-Assistenten"* vor Beginn der Konversation
- Nicht-dismissible Kennzeichnung im Chat-Widget
- Nicht nur im Impressum oder AGB "verstecken" — muss **vor/bei Interaktion** sichtbar sein

### Art. 50 Abs. 2 — Wasserzeichen / technische Kennzeichnung

**Wer ist Adressat?** Anbieter von KI-Systemen, die **synthetische Audio-, Bild-, Video- oder Textinhalte** erzeugen oder manipulieren.

**Pflicht**: Outputs muessen in einem **maschinenlesbaren Format** markiert sein und als **kuenstlich erzeugt/manipuliert erkennbar** gemacht werden.

**Technische Loesungen (Code of Practice Entwurf 03/2026)**:
- **C2PA** (Coalition for Content Provenance and Authenticity) — Metadaten
- **SynthID** (Google) oder **Stable Signature** (Meta) fuer Bilder
- Audio-Wasserzeichen (z. B. VoiceEngine-Watermark)
- Text-Wasserzeichen (aktiv erforscht, teilweise noch instabil)

**Ausnahmen**:
- Assistenzfunktionen, die "nur Standardbearbeitung" leisten (z. B. Rechtschreibkorrektur)
- Strafverfolgung, Forschung (eng)

### Art. 50 Abs. 3 — Emotions-/Biometrische-Kategorisierungssysteme

**Wer ist Adressat?** **Betreiber** (Nutzer) eines Emotionserkennungs- oder biometrischen Kategorisierungssystems.

**Pflicht**: Betroffene Personen **vor der Verarbeitung** ueber den Einsatz informieren.

Zusaetzliche DSGVO-Anforderungen (Art. 9 DSGVO — besondere Kategorie personenbezogener Daten) bleiben unberuehrt. **Einsatz am Arbeitsplatz und in Bildungseinrichtungen ist ohnehin weitgehend verboten** (Art. 5 Abs. 1 lit. f AI Act).

### Art. 50 Abs. 4 — Deepfake-Kennzeichnung

**Wer ist Adressat?** **Betreiber**, die KI-Systeme zur Erzeugung oder Manipulation von **Deepfakes** einsetzen.

**Pflicht**: Inhalte muessen als **kuenstlich erzeugt oder manipuliert offengelegt werden**.

**Ausnahmen**:
- **Kuenstlerische, kreative, satirische, fiktionale oder analoge Werke**: Kennzeichnung in einer Weise, die **Darstellung und Genuss nicht stoert**, aber Existenz des manipulierten Inhalts erkennen laesst
- Strafverfolgungszwecke

Fuer **Texte** zu Angelegenheiten von oeffentlichem Interesse: Kennzeichnungspflicht, ausser menschliche Redaktion hat uebernommen.

### Art. 50 Abs. 5 — Barrierefreiheit

Transparenzpflichten muessen **wahrnehmbar, barrierefrei** umgesetzt werden (Schnittmenge mit BFSG).

### Art. 50 Abs. 6/7 — Leitlinien und Code of Practice

Kommission veroeffentlicht Leitlinien und foerdert Code of Practice. Erfuellung des CoP kann als Nachweis der Erfuellung dienen.

## Typische Fallstricke in Codebases

- **Kein "Du sprichst mit KI"-Hinweis** bei Chatbot (klassisches Problem bei Support-Bots in SaaS)
- **Chatbot-Hinweis zu tief versteckt** (nur in AGB, nicht vor Interaktion sichtbar)
- **KI-generierte Marketing-Bilder ohne Wasserzeichen / C2PA-Metadaten**
- **KI-generierte Blog-Artikel ohne Kennzeichnung** (ab 02.08.2026 problematisch, besonders bei Themen von oeffentlichem Interesse)
- **Deepfake-artige Produktvideos ohne Disclaimer** (z. B. generierte Personen im Testimonial-Video)
- **Emotionserkennung in Sales-Tools** (z. B. Call-Center-Analyse) — oft verboten oder mind. transparenzpflichtig
- **KI-Kompetenz-Pflicht nach Art. 4** wird vergessen: Wer KI einsetzt, muss Mitarbeiter schulen — schon **seit 02.02.2025** in Kraft!
- **Keine Dokumentation**, dass Kennzeichnung umgesetzt ist — bei Behoerdenanfrage nicht nachweisbar

## Pflicht-Elemente fuer Codebase-Integration

Fuer **LLM-Chat-Integrationen** (typischer SaaS-Fall):

```
// Pseudocode — JSX/Vue-agnostisch
<ChatWidget>
  <InitialMessage prominent>
    "Du chattest mit einem KI-Assistenten (Claude/Anthropic).
     Antworten koennen Fehler enthalten. Weiterer Hinweis im Impressum."
  </InitialMessage>
  <!-- Nicht wegklickbar gestalten bis Erstinteraktion -->
</ChatWidget>
```

Fuer **KI-Bildgenerierung**:
- C2PA-Metadaten in EXIF schreiben
- Sichtbare Wasserzeichen (Pflicht ab 02.08.2026)
- Audit-Log wer wann welche KI genutzt hat
- Hinweis in Dateinamen (z. B. `-ai-generated.png`)

Fuer **KI-generierten Text im CMS**:
- Frontmatter-Feld `ai_generated: true`
- Hinweis im Artikel-Footer (sinngemaess): *"Dieser Artikel wurde unter Einsatz von KI (ChatGPT/Claude) verfasst und redaktionell geprueft."*

## Relevanz fuer Codebase-Typen

- **Next.js SaaS**: Art. 50 Abs. 1 bei Chatbot; Abs. 2 wenn Bild/Text generiert wird. Hohe Relevanz.
- **Landingpage**: Art. 50 Abs. 1 bei LandingPage-Chatbot. Oft uebersehen.
- **n8n Automation**: Bei Content-Automation: Abs. 2 & 4 bei Bildern und Videos; Abs. 1 wenn n8n-Bot auf Social Media antwortet.
- **E-Commerce**: KI-Produktempfehlungen sind meist NICHT Art. 50 (kein Deepfake, kein Content-Output). Aber: KI-generierte Produktfotos → Abs. 2; KI-Reviews → Abs. 2/4.
- **Content/Blog**: Ab 02.08.2026 Kennzeichnungspflicht fuer KI-Artikel, insb. zu oeffentlichen Themen.

## Behoerden-Hinweise

- **EU AI Office**: Federfuehrend fuer Leitlinien und Code of Practice
- **AI Act Service Desk**: https://ai-act-service-desk.ec.europa.eu/
- **Bundesnetzagentur**: In DE als Marktueberwachungsbehoerde vorgesehen (detailliert in KI-Marktueberwachungsgesetz, Stand pruefen `<<VERIFIKATION AUSSTEHEND>>`)

## Zitierbare Urteile

**Noch keine** — Art. 50 erst ab 02.08.2026 anwendbar.

## Siehe auch

- [[../gesetze/ai-act]] — Vollstaendiger AI Act
- [[../gesetze/dsa]] — Art. 26 DSA Werbetransparenz (ueberschneidend)
- [[ki-content]] — KI-Training & Urheberrecht
- [[barrierefreiheit]] — BFSG-Anforderung (Schnittmenge mit Art. 50 Abs. 5)
