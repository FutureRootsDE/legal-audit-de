# Anwalt_Claude — Knowledge Base Index

**Stand:** 2026-05-08 | **KB-Version:** 1.2 | **Letztes `/legal-update --all`:** 2026-05-08

Diese Knowledge Base ist ein **Obsidian-kompatibler Markdown-Vault** mit Primaer-Rechtsinformationen fuer deutsches und europaeisches Recht. Sie wird via Hooks on-demand in Claude-Sitzungen geladen — diese INDEX.md ist die **einzige immer-geladene Datei** (via SessionStart-Hook). Alle anderen Dateien werden nur geladen, wenn der UserPromptSubmit-Hook passende Schlagwoerter erkennt (siehe `.claude/hooks/triggers.json`) oder der User `/legal-kb <slug>` aufruft.

## Disclaimer (global, gilt fuer alle KB-Dateien)

> Die hier gesammelten Inhalte sind **keine Rechtsberatung** im Sinne des § 2 RDG. Sie dienen der technischen Vorbereitung einer anwaltlichen Pruefung. Primaerquellen sind in jedem Einzelartikel verlinkt — bei Abweichungen gilt stets die Primaerquelle.

## Scope-Gebiete

| Gebiet | Verzeichnis | Kern-Dateien |
|--------|-------------|--------------|
| Datenschutz (DSGVO/BDSG/TDDDG) | `gesetze/`, `themen/` | `dsgvo.md`, `bdsg.md`, `tdddg.md`, `avv-muster.md`, `verarbeitungsverzeichnis.md`, `tom.md`, `dsfa.md`, `drittland-transfer.md`, `datenschutzerklaerung.md`, `cookie-consent.md`, `tracking-analytics.md`, `meldepflicht-datenpanne.md` |
| Marketing (UWG/PAngV) | `gesetze/`, `themen/` | `uwg.md`, `pangv.md`, `email-marketing.md`, `werbekennzeichnung.md`, `preisangaben.md` |
| Vertragsrecht (BGB) | `gesetze/`, `themen/` | `bgb-agb.md`, `agb-muster.md`, `widerrufsbelehrung.md`, `button-loesung.md` |
| Telemedien/Plattform (DDG/DSA/DMA) | `gesetze/`, `themen/` | `ddg.md`, `dsa.md`, `dma.md`, `impressum.md` |
| KI / Barrierefreiheit (AI Act / BFSG) | `gesetze/`, `themen/` | `ai-act.md`, `bfsg.md`, `ki-transparenz.md`, `barrierefreiheit.md`, `ki-content.md` |
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
- **Verbleibende Platzhalter:** 18 (16 VERIFIKATION AUSSTEHEND + 2 UNVERIFIZIERT) in 16 Dateien — siehe `scripts/find-placeholders.py --json`. Naechster Recheck: `/legal-update --fix-pending`.
