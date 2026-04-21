---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/kurzpapiere.html
  - https://www.bfdi.bund.de/
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

# Verzeichnis von Verarbeitungstätigkeiten (VVT) — Art. 30 DSGVO

## Kurz-Überblick

Das Verzeichnis von Verarbeitungstätigkeiten (VVT) ist die interne Datenschutz-Dokumentation, die die DSGVO von fast jedem Unternehmen verlangt. Es dient als Nachweis der Rechenschaftspflicht (Art. 5 Abs. 2 DSGVO) und ist Grundlage für Audits, Betroffenenauskünfte und DSFAs. Bei Anfrage muss es der Aufsichtsbehörde vorgelegt werden (Art. 30 Abs. 4).

## Kernaussagen

### Pflicht zur Führung (Art. 30 Abs. 5)

**Grundsätzlich pflichtig**, außer wenn ALLE drei Kriterien erfüllt:
1. Unternehmen mit weniger als 250 Mitarbeitern, UND
2. Verarbeitung ist **nicht** risikoreich für Betroffene, UND
3. Verarbeitung ist **gelegentlich**, UND
4. **keine** besonderen Kategorien (Art. 9) oder strafrechtlichen Daten (Art. 10)

→ In der Praxis: **Fast jedes Unternehmen braucht ein VVT**, weil die laufende Verarbeitung von Mitarbeiter- und Kundendaten selten „nur gelegentlich" ist.

### Zwei Perspektiven

**Verantwortlicher (Art. 30 Abs. 1):**
- (a) Name und Kontaktdaten des Verantwortlichen (+ Vertreter, DSB)
- (b) Zwecke der Verarbeitung
- (c) Kategorien betroffener Personen + Kategorien personenbezogener Daten
- (d) Kategorien von Empfängern (inkl. Drittländer)
- (e) Drittland-Übermittlungen + Garantien
- (f) Vorgesehene Löschfristen (falls möglich)
- (g) Allgemeine Beschreibung der TOM (Art. 32)

**Auftragsverarbeiter (Art. 30 Abs. 2):**
- (a) Name Auftragsverarbeiter + Verantwortliche + ggf. DSB
- (b) Kategorien der Verarbeitung im Auftrag
- (c) Drittland-Übermittlungen
- (d) TOM-Beschreibung

## Template-Struktur (pro Verarbeitungstätigkeit)

```
Nr. / Bezeichnung: [z. B. "Newsletter-Versand"]
Verantwortlicher: [Firmenname, Adresse]
Zweck: [z. B. "Informationsversand an eingewillige Empfaenger"]
Rechtsgrundlage: [z. B. Art. 6 Abs. 1 lit. a DSGVO]
Kategorien Betroffener: [z. B. Newsletter-Abonnenten]
Datenkategorien: [E-Mail, Vorname, Anmelde-IP, Anmeldezeitpunkt]
Empfaenger: [Mail-Dienstleister Postmark (DPF)]
Drittland: [USA via DPF]
Garantien: [DPF-Zertifizierung + SCCs als Fallback]
Loeschfristen: [3 Monate nach Abmeldung, Beweis-Archiv 3 Jahre]
TOM: [TLS, 2FA, Rollen-/Rechte-Konzept]
Sub-Auftragsverarbeiter: [AWS via Postmark]
DSFA durchgefuehrt: [Nein — geringes Risiko]
Quelle der Daten: [Aktive Anmeldung via Double-Opt-In]
```

### Typische VVT-Einträge für Tech-Unternehmen

1. Bewerbermanagement
2. Mitarbeiterverwaltung (HR)
3. Lohnabrechnung
4. Kundenverwaltung (CRM)
5. Vertragsabwicklung
6. Rechnungsstellung / Buchhaltung
7. Website-Hosting / Logs
8. Kontaktformular
9. Newsletter-Versand
10. Web-Analytics
11. Marketing-Kampagnen
12. Social-Media-Auftritte
13. Videoüberwachung (falls vorhanden)
14. Support-Ticketing
15. Besucher-Management (Empfang)

## Typische Fallstricke in Codebases

- **VVT ist Word-Dokument ohne Versionierung:** Datenquellen ändern sich ständig; Pflege muss organisiert sein.
- **Neues Feature / neuer Service ohne VVT-Update:** Gängiger DevOps-Gap. Lösung: VVT-Update in Definition-of-Done für Features mit PII.
- **Drittanbieter-Liste nicht synchron mit AVV-Ordner:** VVT nennt Dienst X, aber kein AVV vorhanden — oder umgekehrt.
- **Löschfristen nur vage („solange erforderlich"):** konkrete Trigger benennen (z. B. „3 Jahre nach Vertragsende gemäß § 147 AO").
- **Fehlende Mitarbeiter-Verarbeitung:** Fokus auf Kundendaten, aber HR wird übersehen.
- **Keine Zuordnung zu Datenbank-Tabellen / API-Endpoints:** VVT lebt losgelöst vom tatsächlichen Code. Empfehlung: technische Referenzen (z. B. DB-Schema, Tabelle `users`, Spalten `email`, `name`) im VVT ergänzen.

## Relevanz für Codebase-Typen

- **Next.js SaaS:** VVT-Tabelle pro Feature (Auth, Onboarding, Billing, Support). Als Markdown/YAML in Repo pflegbar.
- **Landingpage:** Kleineres VVT (5–10 Einträge), kann im Excel/Notion liegen.
- **n8n:** Jeder Workflow, der personenbezogene Daten verarbeitet, = ein VVT-Eintrag. `name`, `description`, `tags`-Felder für Dokumentation nutzen.
- **E-Commerce:** Häufig 20+ Einträge (Shop-Stack mit Payment, Versand, Fraud, Reviews, Analytics).
- **Content/Blog:** VVT überschaubar (Hosting, Kommentare, Analytics, Newsletter).

## Tools zur VVT-Führung

**Open Source / kostenlos:**
- CSV/Excel-Templates (z. B. BayLDA Muster)
- Markdown-Tabellen im Git-Repo (empfehlenswert für Dev-Teams — versioniert!)
- Obsidian + Datenbank-Plugin
- OneTrust Community Edition

**Kommerziell:**
- OneTrust, TrustArc, DataGuard
- Proliance GmbH, Caralegal, Ecomply
- audatis Manager, Activemind

## Behörden-Hinweise

- **DSK Kurzpapier Nr. 1** — Verzeichnis von Verarbeitungstätigkeiten
- **BayLDA Muster-VVT** (Excel-Download)
- **LfDI BW Praxisleitfaden zum VVT**
- **Art.-29-Gruppe WP 248** (noch bezugsrelevant für Risikobewertung)

## Zitierbare Urteile

- **LG Mainz 3 O 12/20, 12.11.2021** — Bußgeld für mangelhafte VVT-Führung (ca. 1,24 Mio. EUR)
- **Bayerisches LDA-Tätigkeitsbericht 2022** — Schwerpunkt Dokumentationsmängel
- **OVG Lüneburg 11 LA 104/22, 19.03.2024** — VVT-Einsicht durch Aufsichtsbehörde rechtmäßig

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/avv-muster]]
- [[themen/tom]]
- [[themen/dsfa]]
