---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62018CJ0311
quellen-sekundaer:
  - https://curia.europa.eu/juris/liste.jsf?num=C-311/18
  - https://noyb.eu/de/cjeu-schrems-ii
  - https://www.edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en
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

# EuGH C-311/18 — „Schrems II"

## Kurz-Überblick

Der EuGH hat am 16. Juli 2020 in der Rechtssache C-311/18 (Data Protection Commissioner gegen Facebook Ireland und Maximillian Schrems) den EU-US-Privacy-Shield-Beschluss (2016/1250) wegen fehlenden angemessenen Schutzniveaus für ungültig erklärt. Gleichzeitig bestätigte er die grundsätzliche Gültigkeit der Standardvertragsklauseln (SCCs) — allerdings nur, wenn vor jeder Übermittlung die Rechtslage im Drittland geprüft wird (Transfer Impact Assessment, TIA). Das Urteil prägt bis heute jede Drittland-Übermittlung.

## Eckdaten

| Feld | Wert |
|------|------|
| **Aktenzeichen** | C-311/18 |
| **ECLI** | ECLI:EU:C:2020:559 |
| **CELEX** | 62018CJ0311 |
| **Datum** | 16.07.2020 |
| **Gericht** | EuGH, Große Kammer |
| **Vorlagegericht** | High Court (Irland), Art. 267 AEUV |
| **Parteien** | Data Protection Commissioner gegen Facebook Ireland Ltd., Maximillian Schrems (Beteiligte: USA, EPIC, BSA, Digitaleurope) |

## Tenor (zusammengefasst)

1. **Art. 2 und 4 DSGVO** sind so auszulegen, dass Übermittlungen personenbezogener Daten zu kommerziellen Zwecken durch einen EU-Wirtschaftsakteur an einen anderen Wirtschaftsakteur in einem Drittland in den Anwendungsbereich der DSGVO fallen — **unabhängig davon**, ob die Daten von den Behörden des Drittlands zu Zwecken der nationalen Sicherheit weiterverarbeitet werden.

2. **Durchführungsbeschluss 2016/1250 (Privacy Shield) ist ungültig.**

3. **Durchführungsbeschluss 2010/87 (Standardvertragsklauseln Controller-to-Processor) ist gültig**, aber Datenexporteur und -importeur müssen **vor Übermittlung prüfen**, ob im Drittland ein Schutzniveau gewährleistet ist, das dem EU-Niveau im Wesentlichen gleichwertig ist. Andernfalls sind ergänzende Maßnahmen erforderlich oder die Übermittlung ist auszusetzen.

4. **Aufsichtsbehörden sind verpflichtet**, eine SCC-gestützte Übermittlung zu untersagen oder auszusetzen, wenn kein angemessenes Schutzniveau gewährleistet werden kann.

## Kernaussagen

### Zum Privacy Shield (ungültig)

- US-Überwachungsprogramme (PRISM, UPSTREAM unter FISA 702, EO 12333) erlauben behördliche Zugriffe, die **nicht auf das absolut Notwendige beschränkt** sind → Verstoß gegen Art. 7, 8, 47 GRCh
- Die **Ombudsperson** bietet keinen effektiven Rechtsschutz iSd Art. 47 GRCh — keine Unabhängigkeit, keine verbindlichen Entscheidungen, keine gerichtliche Überprüfbarkeit
- Im Ergebnis: USA gewährleisten **kein „im Wesentlichen gleichwertiges" Schutzniveau**

### Zu den Standardvertragsklauseln (bedingt gültig)

- SCCs können „geeignete Garantien" iSv Art. 46 DSGVO darstellen
- Bei strukturellen Defiziten des Empfängerstaats sind die SCCs allein aber **nicht ausreichend**
- Der Datenexporteur muss **Einzelfallprüfung** durchführen und ggf. ergänzende Maßnahmen ergreifen
- Wenn keine ausreichende Abhilfe möglich: Übermittlung aussetzen

### Zum Transfer Impact Assessment (neu etabliert)

Die Kernverpflichtung, die Schrems II für jede Drittland-Übermittlung etabliert:

1. Identifikation der Übermittlung + Rechtsgrundlage (SCCs / BCR / Derogation)
2. Prüfung von Drittland-Recht und -Praxis (Government Access)
3. Bewertung der Wirksamkeit der Garantien in diesem Kontext
4. Ergänzende Maßnahmen definieren (technisch / organisatorisch / vertraglich)
5. Regelmäßige Überprüfung

## Praktische Folgen (post-Schrems-II)

- **2021/914/EU** (neue SCCs vom 04.06.2021) enthält explizite TIA-Pflicht in Klausel 14
- **EDSA Empfehlungen 01/2020** zu ergänzenden Maßnahmen (finale Version 18.06.2021)
- **EU-US Data Privacy Framework (10.07.2023)** ersetzt Privacy Shield — aber nur für DPF-zertifizierte Unternehmen
- **Schrems III** (NOYB) anhängig gegen das DPF

## Anwendung auf Codebases

- Vor Einsatz jedes US-Dienstes: DPF-Zertifizierung prüfen (dataprivacyframework.gov) oder TIA dokumentieren
- Alternative EU-Dienste wählen wo möglich (Hetzner, OVH, Scaleway, IONOS, EU-Region bei Cloudanbietern)
- Verschlüsselung mit EU-seitig gehaltenen Schlüsseln als ergänzende Maßnahme
- Pseudonymisierung am Datenexport-Punkt

## Weitere Anwendungen in der Rechtsprechung

- **CNIL (FR), 10.02.2022** — Google Analytics Sanktion auf Basis Schrems II
- **DSB Österreich, 22.04.2022** — Universal Analytics unvereinbar
- **Garante (IT), 09.06.2022** — Bestätigung CNIL-Linie
- **LfD Bayern** Orientierungshilfe Mailchimp (März 2021)

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/drittland-transfer]]
- [[themen/tracking-analytics]]
- [[themen/avv-muster]]
- [[behoerden/edsa-leitlinien]]
