---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/
  - https://www.bfdi.bund.de/
  - https://www.edpb.europa.eu/
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
Zusätzlich: Datenkategorien + Quelle (Abs. 2 lit. f). Frist: innerhalb eines Monats, spätestens bei erster Kommunikation.

### Formatvorgaben (Art. 12 DSGVO)
- Präzise, transparent, verständlich
- Klare und einfache Sprache (laiengerecht)
- Unentgeltlich
- Schriftlich oder elektronisch

## Typische Fallstricke in Codebases

- **Copy-Paste aus Generator ohne Anpassung:** Auflistung von Diensten, die gar nicht eingesetzt werden, oder umgekehrt fehlende reale Dienste.
- **Fehlende Nennung aller Third-Party-Dienste:** CDN (Cloudflare), Fonts (Google Fonts — selbst hosten!), Maps (Google Maps), Analytics, CRM (HubSpot, Salesforce), Error-Tracking (Sentry, Datadog).
- **Kein Link zu Datenschutzerklärung im Footer** auf jeder Seite: verstößt gegen „leichte Zugänglichkeit".
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
- **EDSA Leitlinien zur Transparenz (WP260 rev.01)** — Kriterien für „klar und einfach"
- **BayLDA-Prüfschema** Datenschutzerklärungen (aktualisiert 2023)

## Zitierbare Urteile

- **EuGH C-154/21 (RW / Österreichische Post), 12.01.2023** — Auskunftsanspruch umfasst konkrete Empfänger, nicht nur Kategorien, wenn möglich
- **OLG Düsseldorf 20 U 75/20, 09.02.2022** — Abmahnfähigkeit von fehlerhaften Datenschutzerklärungen nach UWG (teils umstritten, noch BGH)
- **LG München I 3 O 17493/20, 20.01.2022** — 100 EUR immaterieller Schaden bei Google Fonts ohne Transparenz
- **EuGH C-319/22, 09.11.2023** — Fahrzeug-Identifizierungsnummer als personenbezogenes Datum (Implikation für Erklärungs-Schema)

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[themen/drittland-transfer]]
