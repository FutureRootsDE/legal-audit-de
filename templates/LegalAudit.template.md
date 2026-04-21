> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Audit wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen und der angegebenen Codebase erstellt. Es ist **ausdruecklich
> keine Rechtsberatung** im Sinne des § 2 RDG. Eine Pruefung durch einen
> zugelassenen Rechtsanwalt (insbesondere Fachanwalt fuer IT-Recht oder
> spezialisierten Datenschutz-Experten) ist **zwingend erforderlich**, bevor
> Inhalte produktiv eingesetzt werden. Gesetze und Rechtsprechung aendern sich —
> Aktualitaet selbst verifizieren.
>
> **Stand:** <YYYY-MM-DD> | **Quellen:** siehe Fussnoten pro Finding

# Legal Audit — <PROJEKTNAME>

| Metadatum | Wert |
|-----------|------|
| **Auditiert am** | <YYYY-MM-DD HH:MM UTC> |
| **Codebase-Pfad** | `<absoluter pfad>` |
| **Git-Commit** | `<sha>` |
| **Codebase-Typ** | Next.js SaaS / Landingpage / n8n / E-Commerce / Content |
| **Geprueft auf** | DSGVO · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · MarkenG · NIS2 |
| **NICHT geprueft** | Strafrecht, Arbeitsrecht, Steuerrecht (ausser HGB § 257), Gesellschaftsrecht, Nicht-EU-Rechtsordnungen |
| **Gesamt-Severity** | CRIT: N · HIGH: N · MED: N · LOW: N |
| **Audit-Engine** | legal-audit-de v1.0 / legal-auditor (haiku) + legal-researcher (sonnet) + legal-text-writer (sonnet) |
| **Zitat-Verifikations-Log** | `.claude/logs/zitate-verifikation-<YYYY-MM-DD>.log` |

## Zusammenfassung

<2-4 Saetze: wichtigste Findings in einem Absatz, mit Verweis auf SUMMARY.md fuer Management-View>

## Finding-Inhaltsverzeichnis

| ID | Severity | Rechtsgebiet | Titel | Clean-Version |
|----|----------|--------------|-------|---------------|
| F-001 | CRIT | DSGVO Art. 44 | <titel> | `clean/F-001-<slug>.md` |
| F-002 | HIGH | UWG § 7 | <titel> | `clean/F-002-<slug>.md` |
| ... | ... | ... | ... | ... |

---

## Findings

### Finding F-NNN: <pragnante 1-Zeilen-Beschreibung>

**Severity:** CRIT | HIGH | MED | LOW
**Rechtsgebiet:** <Gesetz + Paragraph / Artikel>

**Fundstellen:**
- `<relativer-pfad>:<zeile>` — <kurz-zitat oder Referenz>

**Problem:**
<2-4 Saetze: was ist das Problem rechtlich, warum brisant, welche Folge>

**Behoerden-/Gerichts-Referenzen:**
- <Aktenzeichen / Beschluss> (siehe `knowledge/urteile/<slug>.md`)
- <weitere>

**Empfohlene Korrektur:** → siehe `clean/F-NNN-<slug>.md`

**Anwalts-/Tool-Verifikation:**
- Fachanwalts-Kategorie: <siehe legal-verify>
- Selbst-Check-Tool: <z.B. webbkoll.dataskydd.net, PrivacyScore>

---

<!-- weitere Findings -->

## Nicht-geprueft / Offene Punkte

- <Bereiche, die explizit nicht geprueft wurden>
- <Unsicherheiten, die ein Anwalt klaeren muss>

## Naechste Schritte

1. CRIT-Findings priorisieren — binnen 48h Anwalts-Termin
2. HIGH-Findings binnen 2 Wochen
3. MED/LOW in Ticket-System uebernehmen
4. `/legal-verify <thema>` fuer jedes CRIT/HIGH ausfuehren, um Kanzlei zu finden
5. Nach Anwalts-Pruefung: Freigabe-Dokument der Kanzlei anfordern und mit diesem Audit archivieren

## Quellen (global)

- eur-lex.europa.eu (EU-Primaerquellen)
- gesetze-im-internet.de (DE-Primaerquellen)
- rechtsprechung-im-internet.de (DE-Rechtsprechung)
- curia.europa.eu (EuGH-Rechtsprechung)
- datenschutzkonferenz-online.de (DSK-Beschluesse)
- edpb.europa.eu (EDSA-Leitlinien)
- bfdi.bund.de (BfDI-Hinweise)

Pro Finding sind spezifische Quellen in den jeweiligen `knowledge/urteile/*.md` und `knowledge/gesetze/*.md` dokumentiert.
