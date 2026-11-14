# Anwalt_Claude — Knowledge Base Index

**Stand:** 2026-11-14 | **KB-Version:** 1.2 | **Letztes `/legal-update --all`:** 2026-05-08 | **Letztes `/legal-update --stale-only`:** 2026-11-14

Diese Knowledge Base ist ein **Obsidian-kompatibler Markdown-Vault** mit Primaer-Rechtsinformationen fuer deutsches und europaeisches Recht. Sie wird via Hooks on-demand in Claude-Sitzungen geladen — diese INDEX.md ist die **einzige immer-geladene Datei** (via SessionStart-Hook). Alle anderen Dateien werden nur geladen, wenn der UserPromptSubmit-Hook passende Schlagwoerter erkennt (siehe `.claude/hooks/triggers.json`) oder der User `/legal-kb <slug>` aufruft.

## Disclaimer (global, gilt fuer alle KB-Dateien)

> Die hier gesammelten Inhalte sind **keine Rechtsberatung** im Sinne des § 2 RDG. Sie dienen der technischen Vorbereitung einer anwaltlichen Pruefung. Primaerquellen sind in jedem Einzelartikel verlinkt — bei Abweichungen gilt stets die Primaerquelle.

## Scope-Gebiete

| Gebiet | Verzeichnis | Kern-Dateien |
|--------|-------------|--------------|
| Datenschutz (DSGVO/BDSG/TDDDG) | `gesetze/`, `themen/` | `dsgvo.md`, `bdsg.md`, `tdddg.md`, `avv-muster.md`, `verarbeitungsverzeichnis.md`, `tom.md`, `dsfa.md`, `drittland-transfer.md`, `datenschutzerklaerung.md`, `cookie-consent.md`, `tracking-analytics.md`, `meldepflicht-datenpanne.md` |
| Marketing (UWG/PAngV) | `gesetze/`, `themen/` | `uwg.md` (inkl. EmpCo-Richtlinie (EU) 2024/825 / Greenwashing-Umsetzung), `pangv.md` (Preisangabengesetz ab 01.01.2027), `email-marketing.md`, `werbekennzeichnung.md`, `preisangaben.md` |
| Vertragsrecht (BGB) | `gesetze/`, `themen/` | `bgb-agb.md`, `agb-muster.md`, `widerrufsbelehrung.md` (§ 356a BGB elektronische Widerrufsfunktion), `button-loesung.md` (§ 312j Abs. 3 + § 312k + § 356a BGB) |
| Telemedien/Plattform (DDG/DSA/DMA) | `gesetze/`, `themen/` | `ddg.md`, `dsa.md`, `dma.md`, `impressum.md` |
| KI / Barrierefreiheit (AI Act / BFSG) | `gesetze/`, `themen/` | `ai-act.md` (VO (EU) 2024/1689 i. d. F. VO (EU) 2026/1744 "Digital Omnibus on AI" seit 27.07.2026), `bfsg.md`, `ki-transparenz.md`, `barrierefreiheit.md`, `ki-content.md` |
| Urheber/Marken (UrhG/MarkenG) | `gesetze/`, `themen/` | `urhg.md`, `markeng.md`, `urheber-stockfoto.md`, `fotos-dritter-kug.md`, `zitatrecht.md` |
| IT-Sicherheit (NIS2) | `gesetze/` | `nis2-bsig.md` |
| Social Media / Plattform-Pflege | `themen/` | `social-media-datenschutz.md` |
| Werbung mit Siegeln/Auszeichnungen | `themen/` | `siegel-werbung.md` |
| Tool-Katalog (DSGVO-Einordnung von ~80 SaaS-Tools) | `themen/` | `tool-katalog.md` |

## Rechtsprechung (Auswahl)

Unter `urteile/`:
- `eugh-schrems-ii.md` — C-311/18, Drittland-Transfer USA (DPF-Beschluss 10.07.2023 verifiziert)
- `eugh-planet49.md` — C-673/17, Cookie-Einwilligung
- `bgh-cookie-einwilligung.md` — I ZR 7/16, VI ZR 225/20
- `bgh-google-fonts.md` — LG Muenchen I 3 O 17493/20 (+ EuGH C-340/21 Folge-Anker)
- `bgh-inbox-werbung.md` — **I ZR 25/19, 13.01.2022** (zuvor faelschlich I ZR 186/17 zitiert — am 2026-05-08 ueberall korrigiert)
- `eugh-meta-bundeskartellamt.md` — C-252/21 (+ OLG Duesseldorf-Verfahrensende 10.10.2024)
- `bgh-vi-zr-10-24-kontrollverlust.md` — BGH VI ZR 10/24, 18.11.2024 (Leitentscheidung Kontrollverlust als immaterieller Schaden Art. 82 DSGVO, Facebook-Scraping)
- `eug-latombe-dpf.md` — EuG T-553/23 „Latombe", 03.09.2025 (DPF-Angemessenheitsbeschluss erstinstanzlich bestaetigt; Rechtsmittel C-703/25 P anhaengig)
- `eugh-c-654-25-google-fonts-vorlage.md` — EuGH C-654/25 (anhaengig; BGH-Vorlage VI ZR 258/24 vom 28.08.2025 zu Google Fonts, dynamische IP-Adresse, provozierter DSGVO-Verstoss)

## Behoerden / Leitlinien

Unter `behoerden/`:
- `dsk-beschluesse.md` — Datenschutzkonferenz Bund/Laender
- `edsa-leitlinien.md` — European Data Protection Board
- `bfdi-leitfaeden.md` — Bundesbeauftragter
- `landesbeauftragte-kontakte.md` — LDA Bayern, LDI NRW, BlnBDI etc.

## Audit-Checklisten

Unter `checklisten/`:
- `audit-saas.md` — Next.js/React SaaS
- `audit-landingpage.md` — Marketing-/Landingpage
- `audit-ecommerce.md` — Shop-Systeme
- `audit-n8n.md` — n8n-Workflows
- `audit-content-blog.md` — Content/Blog/YouTube
- `general-pre-launch.md` — generischer Pre-Launch-Check

## Anwalts-/Tool-Empfehlungen

Unter `anwaelte-tools/`:
- `fachanwaelte-it-recht.md` — Qualifikationen, Zertifikate
- `datenschutzbeauftragte.md` — BvD, udis, TUEV-zertifiziert
- `kanzleien-saas-spezialisiert.md` — konkrete Empfehlungen
- `tools-generatoren.md` — eRecht24, IT-Recht-KL, Trusted Shops
- `tools-consent-mgmt.md` — Usercentrics, Cookiebot, Klaro, Osano
- `tools-scanner.md` — webbkoll, PrivacyScore, privacytools.io
- `tools-aufsichtsbehoerden.md` — Meldewege

## Cross-Ref-Konventionen

- Obsidian-Style Wiki-Links: `[[themen/cookie-consent]]`
- YAML-Frontmatter pro Datei: `aktualisiert`, `quelle-primaer`, `verifiziert-am`, `geltungsbereich`
- Aenderung in einer Datei sollte per `## Siehe auch`-Block Cross-Ref-Dateien aktualisieren

## Bearbeitungs-Hinweise

- Primaer-Befuellung erfolgt durch `legal-researcher`-Agent via `/legal-update`
- Manuelle Eingriffe sind erlaubt, muessen aber `verifiziert-am:` im Frontmatter aktualisieren
- Sekundaerquellen (Schwenke, Haerting, e-recht24) NIE als Zitat-Grundlage, nur zur Einordnung

## Update-Historie (letzter `--all`-Run)

- **2026-05-08:** `/legal-update --all` ueber alle 63 KB-Dateien. Logs:
  - `.claude/logs/kb-updates.log` (62 Eintraege)
  - `.claude/logs/zitate-verifikation-2026-05-08.log` (134 Eintraege)
  - Schatten-Report: `audits/legal-update-2026-05-08-summary.md`
- **Hauptfunde:** 6 schwerwiegende Aktenzeichen-Korrekturen (I ZR 186/17 → I ZR 25/19; I ZR 93/20 → I ZR 134/20; I ZR 151/02 → I ZR 228/03; OLG Koeln 15 U 66/18 → 15 U 110/18; LG Mainz 3 O 12/20 falsche Zuordnung; OLG Hamburg 3 U 37/22 → 3 W 38/22). § 7 UWG Abs. 4 entfernt (existiert nicht). NEU ergaenzt: BGH I ZR 159/24 (Button-Loesung 09.10.2025), BGH I ZR 183/24 (Streichpreis 09.10.2025), OLG Hamburg 5 U 104/24 (LAION-Berufung 10.12.2025), EuGH C-604/22 (IAB Europe). ODR-Plattform-Pflicht aus Checklisten entfernt (abgeschaltet 20.07.2025).
- **2026-11-14:** `/legal-update --stale-only` ueber Themen- und Checklisten-Batches; Abschlusslauf mit Konsistenz-Normierung der Aktenzeichen-Marker, Aufloesen des ODR-Markers (VO (EU) 2024/3228) und KI-Kompetenz-Angleichung (Art. 4 KI-VO n. F.). Logs:
  - `.claude/logs/kb-update-2026-11-14-abschluss.log`
- **Verbleibende Platzhalter (Stand 2026-11-14, nach Review-Korrekturlauf PR #17):** 53 Marker laut `git grep -c "<<VERIFIKATION AUSSTEHEND>>" -- knowledge/`; `scripts/find-placeholders.py` zaehlt zusaetzlich sonstige Markerarten (insgesamt 91 Report-Zeilen) (inkl. der neu in Hinweisbloecke verschobenen Aussagen zu BAG 2 AZR 133/18 bzw. 8 AZR 253/20, BGH VIII ZR 21/19, VIII ZR 6/10, I ZR 61/20, I ZR 118/12, I ZR 102/10, I ZR 228/14). Schwerpunkte: strittige Aktenzeichen und Pricing-Angaben. Der zuvor gemeldete Verifikationsmarker zum neuen § 356a BGB-Wortlaut ist aufgeloest — die konsolidierte Fassung auf gesetze-im-internet.de zeigt jetzt die neue Paragraphenfassung (Umsetzung RL (EU) 2023/2673, BGBl. 2026 I Nr. 28 vom 05.02.2026, Anwendung seit 19.06.2026). Fehlzitate BGH I ZR 173/16 und I ZR 143/19 aus "Zitierbare Urteile" von preisangaben.md und pangv.md entfernt; der Befund ist in einem Hinweisblock dokumentiert. Naechster Recheck: `/legal-update --fix-pending`.
