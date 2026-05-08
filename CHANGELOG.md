# Changelog

Alle nennenswerten Aenderungen am Plugin **legal-audit-de** werden in diesem Dokument festgehalten. Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionierung nach [Semantic Versioning](https://semver.org/lang/de/).

> **Disclaimer:** Saemtliche KB-Inhalte stellen **keine Rechtsberatung** im Sinne des § 2 RDG dar. Sie dienen der technischen Vorbereitung einer anwaltlichen Pruefung. Eine abschliessende Pruefung durch einen zugelassenen Fachanwalt fuer IT-Recht ist zwingend erforderlich.

---

## [1.2.0] — 2026-05-08

### Hintergrund

Erstmaliger Vollzug von `/legal-update --all` ueber die gesamte KB (63 Dateien) durch sieben parallele `legal-researcher`-Subagenten (Claude Opus 4.7 [1M]). Tier-1-Verifikation gegen `eur-lex.europa.eu`, `gesetze-im-internet.de`, `curia.europa.eu`, `bundesgerichtshof.de`, `rechtsprechung-im-internet.de`, `edpb.europa.eu`, `datenschutzkonferenz-online.de`, `bfdi.bund.de` sowie alle 16 Landesdatenschutzbehoerden. Hybrid-Verifikation via dejure.org/rewis.io/openjur.de wo direkter Tier-1-Fetch nicht verfuegbar.

### Fixed (kritische Aktenzeichen-Korrekturen, Tier-1-verifiziert)

- **`urteile/bgh-inbox-werbung.md`, `gesetze/uwg.md`, `themen/email-marketing.md`, `checklisten/audit-content-blog.md`:** Aktenzeichen "Inbox-Werbung II" korrigiert von `BGH I ZR 186/17` (= App-Zentrum-Verfahren) auf **`BGH I ZR 25/19, 13.01.2022`**.
- **`themen/siegel-werbung.md`:** Aktenzeichen "Testsiegel" korrigiert von `BGH I ZR 93/20` auf **`BGH I ZR 134/20, 15.04.2021`** (Testsiegel auf Produktabbildung).
- **`themen/impressum.md`:** Aktenzeichen "Zwei-Klick-Regel" korrigiert von `BGH I ZR 151/02` (= Markenrechtsfall "Jeans I/II") auf **`BGH I ZR 228/03, 20.07.2006`**.
- **`themen/fotos-dritter-kug.md`:** Aktenzeichen OLG Koeln (KUG/DSGVO) korrigiert von `15 U 66/18` auf **`15 U 110/18, 08.10.2018`**.
- **`themen/verarbeitungsverzeichnis.md`:** Falsche Tenor-Zuordnung korrigiert: `LG Mainz 3 O 12/20` ist **5.000 EUR Schadensersatz wegen rechtswidriger SCHUFA-Meldung (Art. 82 DSGVO)**, nicht "1,24 Mio Bussgeld VVT-Maengel".
- **`gesetze/pangv.md`:** Aktenzeichen OLG Hamburg korrigiert von `3 U 37/22` auf **`3 W 38/22, 12.12.2022`**.
- **`gesetze/uwg.md`, `themen/email-marketing.md`, `themen/tool-katalog.md`:** Falscher Verweis auf "§ 7 Abs. 4 UWG" entfernt — dieser Absatz existiert nicht. Korrektur auf Abs. 2 (telefonisch) bzw. Abs. 3 (Email-Bestandskunden-Ausnahme).
- **`themen/werbekennzeichnung.md`:** Pamela-Reif-Verwechslung behoben — `BGH I ZR 90/20` betraf tatsaechlich Luisa-Maxime Huss; Pamela-Reif-Verfahren (OLG Karlsruhe 6 U 38/19) wurde in Revision zurueckgenommen.
- **`themen/tool-katalog.md`:** § 7 Abs. 2 Nr. 3 UWG (Newsletter) korrigiert auf Nr. 2.

### Added (neue Tier-1-Urteile seit letztem KB-Stand)

- **`gesetze/bgb-agb.md`, `themen/button-loesung.md`, `checklisten/audit-saas.md`, `audit-ecommerce.md`, `general-pre-launch.md`:** **`BGH I ZR 159/24, 09.10.2025`** (Online-Maklervertrag) — Bereicherungsanspruch ausgeschlossen bei fehlender Button-Loesung.
- **`themen/preisangaben.md`, `checklisten/audit-ecommerce.md`, `general-pre-launch.md`:** **`BGH I ZR 183/24, 09.10.2025`** (Streichpreis-Werbung) — verschaerfte Anforderungen § 11 PAngV.
- **`themen/ki-content.md`:** **`OLG Hamburg 5 U 104/24, 10.12.2025`** (LAION-Berufung) — KI-Training auf Fotos urheberrechtlich erlaubt, Revision zugelassen.
- **`themen/cookie-consent.md`:** **`EuGH C-604/22, 07.03.2024`** (IAB Europe) — TC String ist personenbezogenes Datum.
- **`urteile/bgh-google-fonts.md`, `urteile/eugh-schrems-ii.md`:** **`EuGH C-340/21, 14.12.2023`** als Folgeentscheidung Schrems II.
- **`themen/werbekennzeichnung.md`:** **`BGH I ZR 35/21, 13.01.2022`** (Influencer III) — Kennzeichnungspflicht bei Eigen-Werbung.
- **`themen/social-media-datenschutz.md`:** **`OVG SH 4 LB 20/13, 25.11.2021`** (Facebook-Fanpage-Deaktivierung).
- **`urteile/eugh-meta-bundeskartellamt.md`:** Folge-Verfahrensende OLG Duesseldorf 10.10.2024.
- **`urteile/eugh-schrems-ii.md`:** DPF-Beschluss 10.07.2023 (CELEX 32023D1795) verifiziert.

### Changed (strukturelle Updates)

- **AI Act-Stufenplan einheitlich** in allen 6 Checklisten + `themen/ki-content.md` + `ki-transparenz.md`: 02.02.2025 (verbotene Praktiken + KI-Kompetenz Art. 4) / 02.08.2025 (GPAI-Pflichten) / 02.08.2026 (Vollanwendung Hochrisiko-Pflichten + Wasserzeichen).
- **BFSG-Pruefpunkte ergaenzt** in `audit-saas.md`, `audit-ecommerce.md`, `audit-landingpage.md`, `general-pre-launch.md` (anwendbar seit 28.06.2025).
- **DDG-Cross-Refs** korrigiert in `themen/impressum.md`, `themen/social-media-datenschutz.md` — § 5 DDG (Impressum), § 33 DDG (Bussgelder).
- **TDDDG URL-Korrektur:** `gesetze-im-internet.de/tdddg/` liefert HTTP 404; `/ttdsg/` bleibt offizieller Pfad.
- **Behoerden-Daten verifiziert:** Alle 16 Landesdatenschutzbehoerden + BfDI gegen offizielle Webseiten gegengeprueft. BayLDA-Praesident Michael Will (ernannt 01.02.2025), BlnBDI Meike Kamp, LDI NRW Postfach 20 04 44 (40102 Duesseldorf), BfDI-Status (Specht-Riemenschneider, Ruecktritt 17.03.2026 dokumentiert, Nachfolge-Wahl noch offen).
- **DSK-Beschluss-Liste** in `behoerden/dsk-beschluesse.md` mit 8 neuen Beschluessen 2024-2025 ergaenzt.
- **EDSA-Guidelines** in `behoerden/edsa-leitlinien.md` mit 9 neuen Guidelines/Recommendations 2024-2026 ergaenzt; Consent-or-Pay als Opinion 08/2024 praezisiert.
- **CMP-Pricing aktualisiert** in `anwaelte-tools/tools-consent-mgmt.md` (Stand 2026-05-08): Usercentrics, Cookiebot, Borlabs Cookie, Klaro, Osano.
- **Generator-Pricing aktualisiert** in `anwaelte-tools/tools-generatoren.md`: eRecht24 (Basic 30/Business 80/Enterprise 180/Ultimate 1600 EUR mtl.), IT-Recht-Kanzlei, datenschutz-generator.de.
- **Klarstellung Fachanwalts-Bezeichnung:** "Fachanwalt fuer Datenschutzrecht" existiert nicht — siehe `anwaelte-tools/fachanwaelte-it-recht.md`.

### Removed

- **ODR-Plattform-Pflicht** entfernt aus `checklisten/audit-ecommerce.md`, `general-pre-launch.md`, `anwaelte-tools/tools-aufsichtsbehoerden.md` (Plattform abgeschaltet 20.07.2025 via VO (EU) 2024/3228).
- **NetzDG-Bezug** in `checklisten/audit-content-blog.md` ersetzt durch DSA (DSA voll anwendbar seit 17.02.2024, NetzDG durch DDG-Begleitgesetz aufgehoben).

### Statistik

- **Verarbeitete Dateien:** 63 (alle KB-Dateien).
- **Frontmatter-Updates** auf `aktualisiert: 2026-05-08`: 62.
- **Substantielle Inhalts-Edits:** 36 Dateien.
- **Platzhalter:** 42 → 18 (24 aufgeloest, 57% Reduktion).
- **Tier-1-Verifikations-Aufrufe:** ~85 WebFetch + ~48 WebSearch.
- **KB-Version:** 1.1 → 1.2.

### Hinweise fuer Anwender

- **EUR-Lex und curia.europa.eu liefern via WebFetch oft leere Antworten** (JS-Rendering). Bei produktiver Nutzung der KB jeden Aktenzeichen-Eintrag manuell im Browser auf eur-lex/curia/rechtsprechung-im-internet.de oeffnen.
- **Pricing-Werte** in `anwaelte-tools/tools-consent-mgmt.md` und `tools-generatoren.md` haben Tageswert 2026-05-08 — Anbieter passen Tarife oft an. Alle Werte tragen explizites Datum.
- **Eckert Rechtsanwaelte** (`eckert-rechtsanwaelte.de`) leitet auf `knolle.de` (KNOLLE SOCIETAeT, Offenbach) um — Profil passt nicht. Empfehlung: Eintrag beim naechsten Update entfernen.
- **DPF-Periodenueberpruefung** der EU-Kommission noch offen — bei Veroeffentlichung Update.
- **Verbleibende 18 Platzhalter** in 16 Dateien: bewusst belassen weil Tier-1-Quelle aktuell nicht aufloesbar oder Information noch nicht oeffentlich (z.B. KI-Marktueberwachungsgesetz-Status, erste BSI-NIS2-Bussgelder, BFSG-Erstrechtsprechung). Naechster `/legal-update --fix-pending` empfohlen Q3-2026.

---

## [1.1.0] — 2026-04-21

### Added

- Marketplace-Konfiguration fuer Claude-Code-Plugin-Distribution.
- `/legal-audit-de-update`-Skill fuer KB-Aktualisierung.

---

## [1.0.0] — 2026-04-21

### Added

- Initiales Open-Source-Release.
- Vollstaendige Knowledge Base fuer DE/EU-Rechtsaudits (DSGVO, BDSG, TDDDG, UWG, BGB/AGB, DDG, DSA, DMA, AI Act, BFSG, UrhG, MarkenG, NIS2-BSIG, PAngV).
- Sieben Slash-Commands (`/legal-audit`, `/legal-audit-live`, `/legal-doc-check`, `/legal-kb`, `/legal-verify`, `/legal-update`, `/legal-status`).
- Drei Custom-Agents auf Claude Opus 4.7 [1M]: `legal-auditor`, `legal-researcher`, `legal-text-writer`.
- Hook-System fuer kontextschonendes On-Demand-Loading der KB.
- Audit-Templates und Clean-Versionen pro Finding.

---

[1.2.0]: https://github.com/FutureRootsDE/legal-audit-de/releases/tag/v1.2.0
[1.1.0]: https://github.com/FutureRootsDE/legal-audit-de/releases/tag/v1.1.0
[1.0.0]: https://github.com/FutureRootsDE/legal-audit-de/releases/tag/v1.0.0
