---
aktualisiert: 2026-11-15
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/
  - https://www.bfdi.bund.de/
  - https://www.edpb.europa.eu/
  - https://curia.europa.eu/juris/liste.jsf?num=C-21/23
verifiziert-am: 2026-11-14
teilverifiziert-am: 2026-11-15
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

# Datenschutzerklärung — Art. 13 / 14 DSGVO

## Kurz-Überblick

Eine Datenschutzerklärung ist die öffentliche Informationspflicht gegenüber allen Personen, deren Daten verarbeitet werden. Sie ergibt sich aus Art. 13 DSGVO (Daten direkt beim Betroffenen erhoben) und Art. 14 DSGVO (Daten von Dritten). Sie ist keine Einwilligung und darf diese nicht ersetzen. Fehlende oder lückenhafte Datenschutzerklärungen gehören zu den häufigsten Abmahngründen und Bußgeldursachen.

## Kernaussagen — Pflichtinhalte

### Art. 13 DSGVO — Pflichtangaben bei direkter Erhebung

**Abs. 1:**
- (a) Name/Kontaktdaten des Verantwortlichen + ggf. Vertreter
- (b) Kontaktdaten des Datenschutzbeauftragten (soweit benannt)
- (c) Zwecke der Verarbeitung + Rechtsgrundlage
- (d) Bei Art. 6 Abs. 1 lit. f: berechtigte Interessen konkret nennen
- (e) Empfänger/Empfängerkategorien
- (f) Ggf. Drittlandtransfer + Garantien (Art. 46 oder Angemessenheitsbeschluss)

**Abs. 2:**
- (a) Speicherdauer / Kriterien
- (b) Betroffenenrechte (Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch, Datenübertragbarkeit)
- (c) Widerrufsrecht bei Einwilligung
- (d) Beschwerderecht bei Aufsichtsbehörde
- (e) Ob Pflicht zur Bereitstellung besteht + Folgen der Nichtbereitstellung
- (f) Automatisierte Entscheidungen / Profiling — Logik, Tragweite, Folgen

### Art. 14 DSGVO — Ergänzende Angaben bei Fremderhebung
Zusätzlich: Datenkategorien (Art. 14 Abs. 1 lit. d) und Quelle (Art. 14 Abs. 2 lit. f). Frist: innerhalb eines Monats, spätestens bei erster Kommunikation.

### Formatvorgaben (Art. 12 DSGVO)
- Präzise, transparent, verständlich und **leicht zugänglich** (Abs. 1 S. 1)
- Klare und einfache Sprache
- Schriftlich oder in anderer Form, gegebenenfalls elektronisch (Abs. 1 S. 2)
- Unentgeltlich (Abs. 5 S. 1)

## Typische Fallstricke in Codebases

- **Copy-Paste aus Generator ohne Anpassung:** Auflistung von Diensten, die gar nicht eingesetzt werden, oder umgekehrt fehlende reale Dienste.
- **Fehlende Nennung aller Third-Party-Dienste:** CDN (Cloudflare), Fonts (Google Fonts — selbst hosten!), Maps (Google Maps), Analytics, CRM (HubSpot, Salesforce), Error-Tracking (Sentry, Datadog).
- **Kein ständig erreichbarer Link zur Datenschutzerklärung** (üblich: Footer jeder Seite): Risiko eines Verstoßes gegen die „leicht zugängliche Form" (Art. 12 Abs. 1 S. 1 DSGVO).
- **Datenschutzerklärung nur auf Deutsch** bei englischsprachigem Service / internationale Kundschaft: Sprache muss für Zielgruppe verständlich sein.
- **Generische Speicherdauer „solange erforderlich":** DSK fordert konkrete Fristen oder wenigstens nachvollziehbare Kriterien.
- **Keine Update-Historie / Stand-Datum:** Bei Änderungen muss Transparenz gewährleistet sein.
- **Eingebettete iFrames (YouTube, Maps) ohne Hinweis** auf Drittland-Transfer.
- **Newsletter-Double-Opt-In nicht dokumentiert** in Datenschutzerklärung.

## Relevanz für Codebase-Typen

- **Next.js SaaS:** Separate Seite `/datenschutz` mit statischem MDX-Inhalt. Dynamisch gepflegte Dienste-Liste aus Config-File empfehlenswert. Link in Footer-Component global.
- **Landingpage:** Häufig zu knapp — Marketing-Pixel, Formular-Anbieter (Typeform, Tally), A/B-Test-Tool (VWO, Optimizely), Chat-Widget alle deklarieren.
- **n8n:** Wenn n8n als SaaS für Kunden (z. B. Automatisierungsagentur) angeboten wird: eigene Datenschutzerklärung für n8n-UI + AVV für Kundendaten.
- **E-Commerce:** Zahlungsdienstleister (Stripe, PayPal, Klarna), Versanddienstleister (DHL API), Bonitätsprüfung (SCHUFA/Creditreform), Customer-Reviews (Trustpilot, Trusted Shops) — alle einzeln.
- **Content/Blog:** Kommentar-System (Disqus), Share-Buttons (Shariff empfohlen statt nativer Buttons), Autoren-Profile.

## Behörden-Hinweise

- **DSK Kurzpapier Nr. 10** — Informationspflichten bei Dritt- und Direkterhebung
- **Art.-29-Gruppe, Leitlinien für Transparenz (WP260 rev.01)**, vom EDSA am 25.05.2018 übernommen (Endorsement 1/2018): Kriterien für „klar und einfach"
- **BayLDA-Prüfschema** Datenschutzerklärungen (aktualisiert 2023)

## Zitierbare Urteile

- **EuGH C-154/21 (RW / Österreichische Post), 12.01.2023** — Auskunftsanspruch umfasst konkrete Empfänger, nicht nur Kategorien, wenn möglich
- **EuGH C-21/23 (Lindenapotheke), 04.10.2024** — DSGVO-Verstoesse koennen von Mitbewerbern per UWG verfolgt werden; nationale Klagebefugnis bleibt zulaessig. Daten zu apothekenpflichtigen, nicht verschreibungspflichtigen Arzneimitteln sind Gesundheitsdaten nach Art. 9 DSGVO.
- **BGH, Urteil vom 27.03.2025, I ZR 223/19 (Arzneimittelbestelldaten II)** — Folgeentscheidung zu C-21/23: Verarbeitung von Gesundheitsdaten ohne ausdrückliche Einwilligung (Art. 9 Abs. 2 lit. a DSGVO) ist Verstoß gegen eine Marktverhaltensregelung (§ 3a UWG); Mitbewerber sind klagebefugt. Eine allgemeine Abmahnfähigkeit jeder fehlerhaften Datenschutzerklärung folgt daraus nicht.
- **LG München I 3 O 17493/20, 20.01.2022** — 100 EUR immaterieller Schaden bei Weitergabe der IP-Adresse an Google (Google Fonts) ohne Einwilligung und ohne Rechtfertigungsgrund
- **BGH VI ZR 10/24, 18.11.2024 (Leitentscheidung Facebook-Scraping)** — Blosser und kurzzeitiger Kontrollverlust kann bereits immaterieller Schaden nach Art. 82 DSGVO sein; fuer den blossen Kontrollverlust haette der Senat keine Bedenken gegen einen Ausgleich in einer Groessenordnung von 100 EUR (Rn. 100)
- **EuGH C-319/22, 09.11.2023** — Fahrzeug-Identifizierungsnummer als personenbezogenes Datum (Implikation für Erklärungs-Schema)

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[themen/drittland-transfer]]
- [[urteile/bgh-vi-zr-10-24-kontrollverlust]]
- [[urteile/eug-latombe-dpf]]

## Aenderungsvermerk 2026-11-14

- "OLG Duesseldorf 20 U 75/20, 09.02.2022" entfernt: Aktenzeichen liess sich gegen
  Tier-1-Quellen (rechtsprechung-im-internet.de, NRWE) nicht verifizieren; die
  einschlaegige Rechtsprechung zur Abmahnfaehigkeit kommt jetzt vom EuGH
  C-21/23 (Lindenapotheke) und dessen BGH-Umsetzung.
- EuGH C-21/23 (04.10.2024) und BGH-Umsetzung sowie BGH VI ZR 10/24 (18.11.2024,
  Kontrollverlust als immaterieller Schaden) ergaenzt.
- Stand/verifiziert-am auf 2026-11-14 vereinheitlicht.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  BGH-Folgeentscheidungen zu C-21/23 belegt (I ZR 223/19 und I ZR 222/19
  vom 27.03.2025, § 3a UWG), Marker entfernt; C-21/23 Tenor
  ("apothekenpflichtige, nicht verschreibungspflichtige" Arzneimittel);
  LG Muenchen I 3 O 17493/20 praezisiert; BGH VI ZR 10/24 Rn. 100
  (Schadenshoehe, nicht Streitwert); Art. 14 Abs. 1 lit. d ergaenzt;
  WP260 rev.01 als Art.-29-Leitlinie mit EDSA-Endorsement bezeichnet.
- 2026-11-15: Korrekturen aus doppelter unabhängiger Prüfung (Runde 2):
  Formatvorgaben nach Art. 12 Abs. 1 und 5 DSGVO (leicht zugaenglich,
  Unentgeltlichkeit in Abs. 5); Footer-Link als uebliche Umsetzung statt
  Pflicht formuliert.
