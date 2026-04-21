---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.datenschutzkonferenz-online.de/
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-012021-examples-regarding-personal-data-breach_en
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

# Meldepflicht bei Datenpannen — Art. 33 / 34 DSGVO

## Kurz-Überblick

Bei einer Verletzung des Schutzes personenbezogener Daten (Data Breach) muss der Verantwortliche nach Art. 33 DSGVO die zuständige Aufsichtsbehörde **innerhalb von 72 Stunden** melden. Betroffene sind nach Art. 34 DSGVO zusätzlich zu benachrichtigen, wenn ein **hohes Risiko** besteht. Die 72-Stunden-Frist läuft ab „Bekanntwerden" — praktisch: sobald mit hinreichender Wahrscheinlichkeit eine Verletzung feststeht.

## Kernaussagen

### Art. 4 Nr. 12 — Definition „Verletzung des Schutzes personenbezogener Daten"

> Eine Verletzung der Sicherheit, die zur Vernichtung, zum Verlust, zur Veränderung, zur unbefugten Offenlegung oder zum unbefugten Zugang zu personenbezogenen Daten führt.

Drei Kategorien:
- **Vertraulichkeitsverletzung:** unbefugter Zugang/Offenlegung
- **Integritätsverletzung:** unbefugte/unbeabsichtigte Veränderung
- **Verfügbarkeitsverletzung:** unbeabsichtigter/unbefugter Verlust oder Vernichtung

### Art. 33 — Meldung an die Aufsichtsbehörde

**Abs. 1:**
- **72 Stunden** ab Bekanntwerden
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
- **LDA Bayern:** https://www.lda.bayern.de/de/datenpannen.html
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
  - Zahlungsdaten-Leaks = immer hohes Risiko → Art. 34 zusätzlich PCI-Meldepflichten
  - PSD2/BaFin-Meldungen parallel
- **Content/Blog:**
  - WP-Hack (häufig): Datenbank-Analyse erforderlich (wp_users, wp_comments)

## Behörden-Hinweise

- **EDSA Leitlinien 9/2022** zu Benachrichtigungen bei Datenschutzverletzungen
- **EDSA Leitlinien 01/2021** (Beispiele für Datenschutzverletzungen)
- **DSK Kurzpapier Nr. 18** — Risikobewertung (verwandtes Thema)
- **Art.-29-Gruppe WP 250 rev.01** (weiterhin relevant für Einstufung)
- **BfDI Infoblatt „Meldung einer Datenschutzverletzung"**

## Zitierbare Urteile

- **EuGH C-340/21 (Natsionalna agentsia), 14.12.2023** — Cyberangriff führt nicht automatisch zu TOM-Verstoß; Beweislast liegt aber beim Verantwortlichen
- **EuGH C-687/21 (MediaMarktSaturn), 25.01.2024** — Bloßer Kontrollverlust allein nicht automatisch immaterieller Schaden, aber Befürchtungen können genügen
- **OLG Düsseldorf 16 U 275/20, 28.10.2021** — Schadenersatz bei unverschlüsseltem USB-Stick-Verlust
- **LG Köln 28 O 328/21, 15.06.2022** — Bußgeld-Risiko bei verspäteter Meldung

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/tom]]
- [[themen/dsfa]]
- [[themen/verarbeitungsverzeichnis]]
