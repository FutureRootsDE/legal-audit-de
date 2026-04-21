---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/eli/reg/2022/2065/oj
quellen-sekundaer:
  - https://www.bundesnetzagentur.de/DE/Fachthemen/Digitales/DSA/start.html
  - https://gesetz-digitale-dienste.de/
  - https://www.bfdi.bund.de/DE/Buerger/Inhalte/Telemedien/DDG/Digitale_Dienste_Gesetz.html
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

# Digital Services Act (DSA) — VO (EU) 2022/2065

## Kurz-Ueberblick

Die Verordnung (EU) 2022/2065 ueber einen Binnenmarkt fuer digitale Dienste (Digital Services Act, DSA) schafft ein gestuftes Pflichtenregime fuer Vermittlungsdienste im Internet. Sie ist am 16.11.2022 in Kraft getreten und **seit 17.02.2024 fuer alle Anbieter voll anwendbar** (fuer VLOPs/VLOSEs bereits seit 25.08.2023).

In Deutschland wird der DSA durch das **Digitale-Dienste-Gesetz (DDG)** vom 14.05.2024 flankiert. Zustaendig ist die **Bundesnetzagentur** als Digital Services Coordinator (DSC).

Der DSA regelt in einem Stufenmodell Pflichten fuer:
- **Vermittlungsdienste** allgemein (Mere Conduit, Caching, Hosting)
- **Hosting-Dienste**
- **Online-Plattformen** (UGC, Marktplaetze)
- **Sehr grosse Online-Plattformen (VLOPs)** und **sehr grosse Online-Suchmaschinen (VLOSEs)** ab 45 Mio. monatlichen EU-Nutzern

## Schluesselparagraphen / Kernaussagen

### Art. 12 DSA — Kontaktstellen fuer Nutzer

Anbieter von Vermittlungsdiensten muessen eine einzige Kontaktstelle einrichten, die **Nutzern eine rasche, direkte und effiziente Kommunikation** ermoeglicht. Zulaessige Mittel: Telefon, E-Mail, Formular, Chatbot. Der Anbieter muss **ausreichende menschliche und finanzielle Ressourcen** fuer zeitnahe Antworten vorhalten.

Zusaetzlich (Art. 11) ist eine elektronische Kontaktstelle fuer Behoerden und die Kommission zu benennen.

### Art. 14 DSA — Allgemeine Geschaeftsbedingungen

Anbieter muessen in ihren AGB **"klar, einfach, verstaendlich, benutzerfreundlich und eindeutig"** darlegen:
- Informationen zu Einschraenkungen, die sie in Bezug auf Nutzerinhalte auferlegen
- Ihre Content-Moderation-Politik, Verfahren, Massnahmen und Werkzeuge
- Regeln zur algorithmischen Entscheidungsfindung und menschlichen Ueberpruefung

VLOPs/VLOSEs muessen AGB **in den Amtssprachen aller EU-Mitgliedstaaten** bereitstellen, in denen sie Dienste anbieten, sowie **pruefnahe Zusammenfassungen** zur Verfuegung stellen.

### Art. 16 DSA — Melde- und Abhilfeverfahren (Notice-and-Action)

Hosting-Diensteanbieter muessen **leicht zugaengliche Meldemechanismen** einrichten, ueber die Dritte Inhalte melden koennen, die sie fuer rechtswidrig halten. Meldungen muessen:
- **Hinreichend genau und angemessen begruendet** sein
- Die Identifizierung des gemeldeten Inhalts (z. B. URL) enthalten
- Eine Begruendung der Rechtswidrigkeit enthalten

Der Anbieter muss:
- Den Eingang bestaetigen
- **Zeitnah** entscheiden
- Bei dringenden Faellen (Lebensgefahr, Sicherheitsbedrohung) **ohne Verzoegerung** handeln
- Die Entscheidung und die Begruendung mitteilen (Art. 17)

### Weitere zentrale Pflichten

- **Art. 15**: Transparenzberichte (jaehrlich fuer Plattformen; halbjaehrlich fuer VLOPs/VLOSEs)
- **Art. 20**: Internes Beschwerdemanagement bei Plattformen
- **Art. 21**: Aussergerichtliche Streitbeilegung
- **Art. 22**: Bevorzugte Behandlung vertrauenswuerdiger Hinweisgeber (Trusted Flagger)
- **Art. 26–28**: Werbetransparenz, Verbot auf Profiling sensibler Daten, Minderjaehrigenschutz
- **Art. 34/35**: Systemische-Risiko-Bewertung bei VLOPs

## Typische Fallstricke in Codebases

- **Fehlende Kontaktstelle** nach Art. 12 (nicht im Impressum sichtbar oder kein Formular) → Bussgeldrisiko
- **AGB nicht DSA-konform**: Content-Moderation-Praxis nicht offengelegt, keine klare Regelung zur algorithmischen Entscheidung
- **Notice-and-Action-Mechanismus fehlt oder ist zu tief versteckt** (muss leicht zugaenglich sein)
- **Keine Begruendung bei Content-Entfernung** (Art. 17 "Statement of Reasons")
- **Transparenzberichte ueberfaellig** (Art. 15, Art. 24)
- **Dark Patterns in UI** (Art. 25 verbietet irrefuehrendes Design)
- **Werbekennzeichnung unklar** (Art. 26: Erkennbarkeit als Werbung + wer wirbt + warum es dem Nutzer gezeigt wird)
- **Minderjaehrige**: Profiling-basierte Werbung verboten, wenn mit hinreichender Sicherheit erkennbar (Art. 28)

## Relevanz fuer Codebase-Typen

- **Next.js SaaS**: Pflicht zur Kontaktstelle (Impressum/Kontakt-Route), ggf. Notice-and-Action wenn Nutzer-Content (Kommentare, Uploads, Reviews). AGB anpassen.
- **Landingpage**: Typischerweise nicht als Vermittlungsdienst einzustufen — Pflichten minimal, aber Kontaktstelle sinnvoll.
- **n8n**: Wenn n8n-Workflows Inhalte Dritter moderieren/verarbeiten: Protokollierung der Content-Moderation-Entscheidungen sinnvoll.
- **E-Commerce (Marktplatz-Modell)**: Volle Plattformpflichten (Art. 30 "Know Your Business Customer", Produktrueckverfolgbarkeit, Notice-and-Action)
- **Content/Blog mit Kommentarfunktion**: Hosting-Dienst → Art. 16 Notice-and-Action Pflicht

## Behoerden-Hinweise

- **Bundesnetzagentur (Digital Services Coordinator, DSC)**: Zentrale deutsche Aufsicht, angesiedelt beim BNetzA. Informationen: https://www.bundesnetzagentur.de/DE/Fachthemen/Digitales/DSA/start.html
- **BfDI**: Zustaendig fuer datenschutzrechtliche Schnittmengen (insb. Werbung, Profiling, Art. 26–28)
- **EU-Kommission (DG CNECT)**: Direkte Aufsicht ueber VLOPs/VLOSEs
- **DDG** (nationales Durchfuehrungsgesetz): https://gesetz-digitale-dienste.de/

## Zitierbare Urteile

Noch sehr begrenzt — DSA ist erst seit Februar 2024 voll anwendbar. Bisher vor allem:
- Verfahren der EU-Kommission gegen VLOPs (X, TikTok, Meta, AliExpress) — keine Endurteile, sondern Untersuchungsverfahren
- Keine relevante deutsche Rechtsprechung zu Art. 14/16 DSA als Endurteil identifiziert

`<<VERIFIKATION AUSSTEHEND>>` — konkrete deutsche Urteile zu DSA-Pflichten sollten bei naechstem Update geprueft werden.

## Siehe auch

- [[dma]] — Digital Markets Act (Schwestern-VO)
- [[ai-act]] — KI-Verordnung (Transparenzpflichten Art. 50)
- [[bfsg]] — Barrierefreiheit von Online-Diensten
- [[../themen/ki-transparenz]] — Kennzeichnung KI-generierter Inhalte
