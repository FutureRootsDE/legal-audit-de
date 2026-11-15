---
aktualisiert: 2026-11-15
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-012021-examples-regarding-personal-data-breach_en
  - https://www.bfdi.bund.de/
verifiziert-am: 2026-11-14
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

# Meldepflicht bei Datenpannen — Art. 33 / 34 DSGVO

## Kurz-Überblick

Bei einer Verletzung des Schutzes personenbezogener Daten (Data Breach) muss der Verantwortliche nach Art. 33 DSGVO die zuständige Aufsichtsbehörde **unverzüglich und möglichst binnen 72 Stunden nach Bekanntwerden** melden (Art. 33 Abs. 1 DSGVO). Betroffene sind nach Art. 34 DSGVO zusätzlich zu benachrichtigen, wenn ein **hohes Risiko** besteht. Die 72-Stunden-Frist läuft ab „Bekanntwerden" — praktisch: sobald mit hinreichender Wahrscheinlichkeit eine Verletzung feststeht.

## Kernaussagen

### Art. 4 Nr. 12 — Definition „Verletzung des Schutzes personenbezogener Daten"

> eine Verletzung der Sicherheit, die, ob unbeabsichtigt oder unrechtmäßig, zur Vernichtung, zum Verlust, zur Veränderung, oder zur unbefugten Offenlegung von beziehungsweise zum unbefugten Zugang zu personenbezogenen Daten führt, die übermittelt, gespeichert oder auf sonstige Weise verarbeitet wurden

Drei Kategorien:
- **Vertraulichkeitsverletzung:** unbefugter Zugang/Offenlegung
- **Integritätsverletzung:** unbefugte/unbeabsichtigte Veränderung
- **Verfügbarkeitsverletzung:** unbeabsichtigter/unbefugter Verlust oder Vernichtung

### Art. 33 — Meldung an die Aufsichtsbehörde

**Abs. 1:**
- **unverzüglich und möglichst binnen 72 Stunden** nach Bekanntwerden
- Ausnahme: Wenn „voraussichtlich nicht zu einem Risiko" für Betroffene → keine Meldepflicht (aber Dokumentation, Abs. 5)
- Bei Verspätung: Begründung für Verzögerung

**Abs. 3 — Mindestinhalt der Meldung:**
- (a) Art der Verletzung, Kategorien/Anzahl Betroffener, Kategorien/Anzahl Datensätze
- (b) Kontaktdaten DSB / Auskunftsperson
- (c) Wahrscheinliche Folgen
- (d) Ergriffene / vorgeschlagene Maßnahmen

**Abs. 4 — Stufenweise Meldung möglich**, wenn nicht alle Informationen in 72h verfügbar.

**Abs. 5 — Dokumentationspflicht ALLER Vorfälle**, auch nicht-meldepflichtiger.

### Art. 33 Abs. 2 — Meldung Auftragsverarbeiter → Verantwortlicher

Auftragsverarbeiter muss „unverzüglich" melden. **Kein eigener 72-Stunden-Countdown** — Frist läuft beim Verantwortlichen ab dessen Kenntnis.

### Art. 34 — Benachrichtigung der Betroffenen

Pflicht bei **hohem Risiko**. Inhalt: klar, einfach, mit Maßnahmen.

**Ausnahmen (Abs. 3):**
- (a) Ausreichende TOM vor Vorfall (z. B. Ende-zu-Ende-Verschlüsselung) → Daten praktisch unlesbar
- (b) Nachfolgende Maßnahmen lassen Risiko nicht mehr eintreten
- (c) Unverhältnismäßiger Aufwand → öffentliche Bekanntmachung als Alternative

### Risiko- vs. Hoch-Risiko-Bewertung

EDSA Leitlinie 9/2022 + WP250: **Severity × Likelihood**. Hohe Risikofaktoren:
- Sensible Daten (Gesundheit, Finanzen, Kinder)
- Große Anzahl Betroffener
- Irreversibilität des Schadens
- Identifizierbarkeit der Personen

## Typische Fallstricke in Codebases

- **„Nur" verlorenes Notebook:** ohne Verschlüsselung = Meldung; mit FDE ggf. keine Meldung.
- **Ransomware-Angriff:** auch bei erfolgreicher Backup-Wiederherstellung meist meldepflichtig (Vertraulichkeits-Vermutung bei Exfiltration).
- **Phishing-Erfolg auf Mitarbeiter-Account:** sobald Daten zugänglich waren → Meldung.
- **S3-Bucket öffentlich ohne ACL:** klassischer Fall, meldepflichtig.
- **Fehlgesendete E-Mail mit Anhang:** typischer Vorfall; je nach Inhalt meldepflichtig oder nicht.
- **Dev-Datenbank-Dump ohne Anonymisierung öffentlich erreichbar:** meldepflichtig.
- **GitHub Secret-Leak:** Meldung je nach Scope (eigene Daten / Kundendaten); Secret sofort rotieren.
- **Fehlende Breach-Response-Runbooks:** keine 72h-Einhaltung möglich.
- **Logging zu schwach**, um Betroffene zu bestimmen: erschwert Meldung und zeigt TOM-Lücken.
- **Meldung ohne DSB-Abstimmung**: führt oft zu unvollständigen Angaben.

## 72-Stunden-Workflow (Template)

```
T+0   Detection (Alert, Beschwerde, Aufsicht)
T+1   Triage: Ist es eine Verletzung i.S.d. Art. 4 Nr. 12?
T+2   Incident-Response-Team aktivieren, DSB/CISO einbeziehen
T+4   Scope-Analyse: Welche Daten / Personen / Systeme?
T+8   Containment + Forensics
T+24  Risiko-Bewertung (Severity × Likelihood)
T+48  Meldeentwurf (Behörde + ggf. Betroffene)
T+72  Meldung über Portal der Aufsichtsbehoerde
T+n   Nachbericht, Lessons Learned, Maßnahmen-Update
```

### Melde-Portale (Auswahl)

- **BfDI:** Online-Formular unter bfdi.bund.de
- **LfDI BW:** https://www.baden-wuerttemberg.datenschutz.de/datenpanne-melden
- **LDA Bayern:** https://www.lda.bayern.de/de/datenpanne.html
- **BlnBDI:** https://www.datenschutz-berlin.de
- **LDI NRW, LfDI RLP, HmbBfDI**: jeweils eigene Formulare

## Relevanz für Codebase-Typen

- **Next.js SaaS:**
  - Sentry/Datadog mit Incident-Prozess koppeln
  - Playbook im Runbook-Repo
  - Breach-Notification-API für Enterprise-Kunden als Feature
- **Landingpage:**
  - Risiko meist gering — trotzdem Hosting-Incidents beachten (Shared-Hosting-Breach)
- **n8n:**
  - Credentials-Rotation-Plan wenn Zugriff kompromittiert
  - Workflow-Audit-Log analysieren
- **E-Commerce:**
  - Zahlungsdaten-Leaks = immer hohes Risiko → Art. 34; zusätzlich vertragliche Meldepflichten aus PCI DSS gegenüber Acquirer/Kartenorganisation
  - PSD2/BaFin-Meldungen parallel
- **Content/Blog:**
  - WP-Hack (häufig): Datenbank-Analyse erforderlich (wp_users, wp_comments)

## Behörden-Hinweise

- **EDSA Leitlinien 9/2022** zu Benachrichtigungen bei Datenschutzverletzungen
- **EDSA Leitlinien 01/2021** (Beispiele für Datenschutzverletzungen)
- **DSK Kurzpapier Nr. 18** — Risikobewertung (verwandtes Thema)
- **EDSA Leitlinien 9/2022 zur Meldung von Verletzungen des Schutzes personenbezogener Daten, Version 2.0 vom 28.03.2023** (ersetzen WP 250 rev.01)
- **BfDI Infoblatt „Meldung einer Datenschutzverletzung"**

## Zitierbare Urteile

- **EuGH C-340/21 (Natsionalna agentsia), 14.12.2023** — Cyberangriff führt nicht automatisch zu TOM-Verstoß; Beweislast liegt aber beim Verantwortlichen
- **EuGH C-687/21, 25.01.2024**: Irrtümliche Weitergabe an Dritte belegt für sich keine ungeeigneten TOM; hat der Dritte die Daten nachweislich nicht zur Kenntnis genommen, ist die bloße Befürchtung künftigen Missbrauchs kein immaterieller Schaden (Tenor 5). Befürchtung als möglicher Schaden: EuGH C-340/21, Tenor 6.
- **BGH VI ZR 10/24 (Facebook-Scraping), 18.11.2024** — Urteil im nach § 552b ZPO bestimmten Leitentscheidungsverfahren: bereits der kurzzeitige Verlust der Kontrolle ueber personenbezogene Daten kann einen immateriellen Schaden nach Art. 82 DSGVO begruenden; Groessenordnung im Ausgangsverfahren ca. 100 EUR
- **EuGH C-655/23 (IP/Quirin Privatbank), 04.09.2025** — Auch negative Gefuehle nach unbefugter Weitergabe von Daten koennen immateriellen Schaden begruenden <<VERIFIKATION AUSSTEHEND>>
- **OLG Düsseldorf 16 U 275/20, 28.10.2021**: 2.000 EUR immaterieller Schadensersatz für unverschlüsselten Versand von Gesundheitsdaten an eine falsche E-Mail-Adresse
- **LG Köln 28 O 328/21, 18.05.2022**: 1.200 EUR Schadensersatz nach Art. 82 DSGVO

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/tom]]
- [[themen/dsfa]]
- [[themen/verarbeitungsverzeichnis]]
- [[urteile/bgh-vi-zr-10-24-kontrollverlust]]

## Aenderungsvermerk 2026-11-14

- BGH VI ZR 10/24 (18.11.2024) als neue Leitentscheidung zum Kontrollverlust
  ergaenzt (Quelle: BGH-Pressemitteilung, ECLI:DE:BGH:2024:181124UVIZR10.24.0).
- EuGH C-655/23 (04.09.2025, XING) als Hinweis aufgenommen, Aktenzeichen noch
  verifikationsoffen.
- Digital-Omnibus-Hinweis: Die Kommission hat am 19.11.2025 einen Vorschlag
  vorgelegt, der u. a. die 72h-Frist in Art. 33 DSGVO zugunsten einer
  risiko-triggered Meldung mit 96h anpassen moechte. Status 2026-11-14: **nur
  Kommissionsvorschlag**, noch nicht verkuendet. Bis zur Verkuendung gilt die
  72-Stunden-Frist aus Art. 33 Abs. 1 DSGVO unveraendert.
- Zwei OLG-/LG-Aktenzeichen mit Verifikationsmarker versehen.
- Stand/verifiziert-am auf 2026-11-14 vereinheitlicht.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  Meldefrist nach Wortlaut Art. 33 Abs. 1 ("unverzueglich und moeglichst
  binnen 72 Stunden"); Art. 4 Nr. 12 im Wortlaut; EuGH C-687/21 (Tenor 5)
  berichtigt, C-340/21 Tenor 6 ergaenzt; BGH VI ZR 10/24 als Urteil im
  Leitentscheidungsverfahren bezeichnet; Parteibezeichnung C-655/23
  berichtigt; OLG Duesseldorf 16 U 275/20 (Gegenstand) und LG Koeln
  28 O 328/21 (Datum 18.05.2022, Gegenstand) berichtigt, Marker dort
  entfernt; PCI-DSS-Pflichten als vertraglich gekennzeichnet; EDSA
  Leitlinien 9/2022 v2.0 statt WP 250; URL LDA Bayern korrigiert.
