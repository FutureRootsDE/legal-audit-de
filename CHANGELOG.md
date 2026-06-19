# Changelog

Alle nennenswerten Aenderungen am Plugin **legal-audit-de** werden in diesem Dokument festgehalten. Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionierung nach [Semantic Versioning](https://semver.org/lang/de/).

> **Disclaimer:** Saemtliche KB-Inhalte stellen **keine Rechtsberatung** im Sinne des § 2 RDG dar. Sie dienen der technischen Vorbereitung einer anwaltlichen Pruefung. Eine abschliessende Pruefung durch einen zugelassenen Fachanwalt fuer IT-Recht ist zwingend erforderlich.

---

## [Unreleased]

### Hintergrund Doku-Site

Eigenstaendige Documentation-Site unter `docs/` fuer GitHub Pages, statt READMEs als alleinige Quelle. Mehrseitige Navigation (Startseite, Setup, Commands, KB-Uebersicht, MCP-Integration) mit just-the-docs als Remote-Theme. Voraussetzung: GitHub Pages muss im Repo unter Settings → Pages → Source = `main` Branch, Folder = `/docs` aktiviert werden. Diese Aktivierung kann nur durch einen Repo-Maintainer mit Admin-Rechten erfolgen.

### Added Doku-Site

- **`docs/_config.yml`** mit `remote_theme: just-the-docs/just-the-docs`, deutscher Beschreibung, Suche, Callouts (warning / note / tipp), Footer mit Disclaimer-Hinweis.
- **`docs/index.md`** Landing-Page mit Hero, Scope-Tabelle, Schnellstart fuer Claude Code, Verweisen auf alle Unterseiten.
- **`docs/setup.md`** Installation fuer alle drei CLIs (Claude Code, Codex CLI, Copilot CLI), Pro-Mode-Toggle, optionale Hilfs-MCPs (`chrome-devtools-mcp`, `rechtsinformationen-bund-de-mcp`).
- **`docs/commands.md`** Vollstaendige Slash-Befehlsreferenz mit Optionen, Severity-Matrix, Hilfsskript-Tabelle.
- **`docs/knowledge-base.md`** Aufbau der KB, Quellen-Hierarchie (Tier 1/2/3), Gesetzes-Tabelle, Schluesselurteile, Trigger-Beispiele, Frontmatter-Konvention inkl. der seit dem MCP-Patch optionalen `eli`- und `ecli`-Felder.
- **`docs/mcp-integration.md`** Vollanleitung fuer den optionalen `rechtsinformationen`-MCP-Server: drei Installationsvarianten, drei Registrierungs-Scopes, Tool-Praeferenz-Tabelle, Anti-Fallen, Troubleshooting.

### Hintergrund

Optionale Anbindung an den MCP-Server [`wolfgangihloff/rechtsinformationen-bund-de-mcp`](https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp), der das offizielle Bundes-Portal [`rechtsinformationen.bund.de`](https://docs.rechtsinformationen.bund.de) ueber das Model Context Protocol erschliesst. Tip vom Community-Feedback nach dem v1.3.x-Release: strukturierter Zugriff mit ELI/ECLI-Identifiern statt HTML-Scraping per WebFetch macht Zitat-Verifikation robuster, insbesondere bei Re-Releases des Portals. Die Integration ist bewusst **opt-in** — der MCP-Server haengt von einem lokalen Node.js-Build des Drittautors ab und nutzt eine API, die selbst noch "testphase" ist; das Default-Setup des Plugins soll ohne diese Abhaengigkeit lauffaehig bleiben.

### Added

- **Opt-in MCP-Integration**: `templates/mcp/` mit `rechtsinformationen.mcp.json.example` (Beispiel-Konfiguration fuer projekt- oder user-scoped `.mcp.json`) und ausfuehrlicher Setup-Doku (`templates/mcp/README.md`) inklusive drei Installationsoptionen (Upstream-Build, npm-Third-Party-Wrapper, Skip), drei Registrierungs-Scopes (Projekt, User, Plugin) und Troubleshooting-Tabelle. **Kein** `.mcp.json` im Plugin-Root, damit Default-Installs ohne Node.js-Setup nicht brechen.
- **Optionale `eli:` / `ecli:` Frontmatter-Felder** in der KB-Datei-Struktur (dokumentiert in `legal-researcher.md`). Stabile, kanonische Identifier nach den Standards [ELI](http://publications.europa.eu/eli) und [ECLI](https://e-justice.europa.eu/ecli) ueberleben URL-Reshuffles. Bestehende KB-Dateien bleiben unveraendert; Felder sind nicht verpflichtend.

### Changed

- **`legal-researcher.md` und `legal-researcher-pro.md` (beide 1M und Pro-Mode, Claude/Codex/Copilot)**: neuer Abschnitt "Optional: MCP-beschleunigte Verifikation". Der Agent bevorzugt `mcp__rechtsinformationen__*`-Tools, wenn vorhanden, und faellt sonst still auf WebFetch zurueck. Anti-Fallen explizit dokumentiert: historische Gesetzesfassungen, Aenderungsgesetze (TMG→DDG, TTDSG→TDDDG) und leere/fehlgeformte Responses triggern Fallback. Log-Konvention erweitert: `VERIFIED mcp:rechtsinformationen eli:...`.
- **`post_write.py`-Hook**: Disclaimer-Ausnahme-Liste fuer Meta-Dateien (`README*.md`, `INDEX.md`, `tool-katalog.md`) ergaenzt. Spiegelt das `grep -v`-Filter aus `.github/workflows/validate.yml:disclaimer-check` — vorher haben PostToolUse-Warnungen auf juristisch nicht-substantielle Meta-Dateien geschossen, was bei der neuen `templates/mcp/README.md` aufgefallen waere.

### Architektur-Hinweise

- **Kein Plugin-Root-`.mcp.json`** — wuerde Plugin-Enable bei jedem User triggern, der den Upstream-Server nicht installiert hat. Daher template-only.
- **Sync-Generatoren unveraendert.** `sync-pro-variants.py --apply` und `sync-platforms.py --apply` haben die MCP-Erweiterung deterministisch in alle sechs Researcher-Varianten propagiert (Claude/Codex/Copilot je 1M + Pro).
- **Quellen-Hierarchie unveraendert.** MCP-Server ist Tier-1-Werkzeug (Quelle = `rechtsinformationen.bund.de` ist das selbe BMJ-Datenbestand wie `gesetze-im-internet.de`), aber keine eigene Tier-Stufe; bleibt als Verifikations-Beschleuniger eingeordnet.

### Bewusst NICHT enthalten

- **Auto-Install des MCP-Servers** (z.B. via `npx -y` im Plugin-Root-`.mcp.json`). Begruendung: der einzige npm-Wrapper ist von einem Drittautor (`@iflow-mcp/...`), aktuell ca. 23 monatliche Downloads — Supply-Chain-Risiko nicht zumutbar in einem rechts-relevanten Tooling-Stack.
- **Backfill bestehender KB-Dateien mit ELI/ECLI**. Wird in einem separaten `/legal-update --add-identifiers`-Lauf nachgezogen (eigene Spec, eigener PR), damit dieser PR rein additiv und reviewbar bleibt.

---

## [1.3.2] — 2026-05-24

### Hintergrund

Schliesst die Pro-Abo-Sperre fuer Claude-Pro-Abonnenten (20 USD/mo). v1.3.0/1.3.1 pinnten alle drei `legal-*`-Agents fest auf `model: claude-opus-4-7[1m]` — Pro-User trafen beim ersten Dispatch den Fehler `1M context requires usage credits or Max plan` und konnten das Plugin gar nicht nutzen. v1.3.2 fuehrt einen sauberen, atomaren, dokumentations-konformen Pro-Mode ein, **ohne** die bestehenden 1M-Agents zu mutieren.

### Added

- **`/legal-pro-mode enable|disable|status`** — neuer Slash-Command. Setzt einen atomaren Marker in `${CLAUDE_PLUGIN_DATA}/pro-mode.json` (per [plugins-reference.md](https://code.claude.com/docs/en/plugins-reference) als "persistent directory for plugin state that survives updates" dokumentiert). Plattform-Fallbacks: `~/.claude/legal-audit-de-pro-mode.json`, `~/.codex/legal-audit-de-pro-mode.json`, `~/.copilot/legal-audit-de-pro-mode.json`.
- **Drei `-pro`-Agent-Varianten:** `.claude/agents/legal-auditor-pro.md`, `legal-researcher-pro.md`, `legal-text-writer-pro.md`. Identischer Prompt-Body wie die 1M-Pendants, nur `model: claude-opus-4-7` (Standard-Kontext) und ein vorangestellter Pro-Mode-Protokoll-Block.
- **`scripts/legal-audit-pro-mode.py`** — CLI-Tool fuer den Toggle (atomares `os.replace` Write, exit code 2 bei plattformuebergreifender Inkonsistenz statt 1 wegen `set -e`-Kompatibilitaet).
- **`scripts/sync-pro-variants.py`** — Generator, der die drei `-pro`-Varianten deterministisch aus den 1M-Varianten ableitet (Single-Source-of-Truth fuer den Prompt-Body). Modi `--check` (CI) und `--apply` (Maintainer).
- **SessionStart-Hook erweitert** (`.claude/hooks/session_start.py`): liest den Pro-Mode-Marker und ergaenzt bei aktiver Aktivierung einen System-Reminder im `additionalContext`, der den Orchestrator anweist, die `-pro`-Varianten zu dispatchen.
- **Auto-Routing-Block fuer Codex/Copilot** (`scripts/sync-platforms.py:AUTO_ROUTING_BLOCK_DE`): Pro-Mode-Erkennung in jedem generierten `*/skills/*/SKILL.md`, da diese Plattformen keinen SessionStart-Hook haben.
- **`legal-status`-Erweiterung:** neuer `pro_mode`-Block im JSON-Output und ein eigener Block im Text-Output mit Marker-Pfad, Set-Datum und Vollstaendigkeits-Check der Agent-Varianten.
- **Vier Commands Pro-Mode-aware:** `/legal-audit`, `/legal-doc-check`, `/legal-update`, `/legal-audit-de-update` enthalten jetzt eine "Pro-Mode-Awareness"-Sektion (vor dem Pflichtablauf) plus eine Agent-Marker-Tabelle (am Ende), die Default- und Pro-Mode-Dispatch-Namen gegenueberstellt.

### Fixed

- **Codex-Marketplace (`.agents/plugins/marketplace.json`)** verwendet jetzt `{"source":"github","repo":"FutureRootsDE/legal-audit-de"}` statt `{"source":"local","path":"./"}`. Das Discriminator-Schema ist per [plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces) korrekt; der bisherige `local`-Wert hat den `codex plugin marketplace add FutureRootsDE/legal-audit-de`-Workflow gebrochen (resolves den Codex-Anteil von Issue #3, das bisher nur auf Claude-Seite gefixt war).
- **Claude-Marketplace (`.claude-plugin/marketplace.json`)** auf das gleiche Schema umgestellt: `{"source":"github","repo":"FutureRootsDE/legal-audit-de"}` (statt `"source": "./"`). Konsistente Discriminator-Form auf beiden Plattformen.

### Architektur-Hinweise

- **Pro-Mode ist nicht-destruktiv:** Toggle veraendert **keine** Agent-Files, sondern setzt nur Marker im user-scope-Persistenz-Verzeichnis. Damit ueberlebt der Pro-Mode-Status `/plugin install`, Marketplace-Refresh und `/legal-audit-de-update`.
- **Atomicity:** Marker-Writes nutzen `tempfile.mkstemp` + `os.replace`, was unter POSIX atomar ist. Halbe Marker-States koennen nicht entstehen.
- **Drift-Schutz:** CI (`validate.yml`) prueft sowohl `sync-platforms.py --check` als auch `sync-pro-variants.py --check`. Aenderungen am 1M-Agent-Body propagieren via `sync-pro-variants.py --apply` in die `-pro`-Varianten.

### Bewusst NICHT enthalten (v1.4.0)

- **`--chunked`-Flag** fuer `/legal-audit` (sequentielle Multi-Pass-Ausfuehrung fuer Codebases > ~150 KB). Saubere Trennung von Concerns: Pro-Mode = Modell-Swap; `--chunked` = Execution-Strategie (auch fuer Max/Team-User nuetzlich). Eigenes Spec, eigener PR.

---

## [1.3.1] — 2026-05-09

### Hintergrund

Schliesst die Codex-spezifischen Luecken aus v1.3.0. Diese Version geht zu **100 %** auf den ersten externen Community-Beitrag zum Repo zurueck — herzlichen Dank an [@AllstarGER](https://github.com/AllstarGER) fuer PR [#1](https://github.com/FutureRootsDE/legal-audit-de/pull/1), der nicht nur die Codex-spezifischen Plugin-Metadaten beigesteuert, sondern auch einen kritischen Frontmatter-Order-Bug aus v1.3.0 gefixt und das Ergebnis tatsaechlich gegen die echte Codex CLI verifiziert hat (`HOME=/tmp/... codex plugin marketplace add /tmp/legal-audit-de`). Squash-merged in Commit `5b1b212`.

### Added

- **Native Codex plugin metadata:** `.codex-plugin/plugin.json` (mit `interface`-Block: `displayName`, `category: "Compliance"`, `capabilities: ["Interactive", "Write"]`, `defaultPrompt`, `brandColor`) und `.agents/plugins/marketplace.json` (mit `policy.installation`/`policy.authentication`), beide generiert von `scripts/sync-platforms.py`. Damit ist das Repo erstmals via `codex plugin marketplace add FutureRootsDE/legal-audit-de` direkt als Codex-Plugin installierbar — analog zu `.claude-plugin/plugin.json` fuer Claude Code.
- **`validate_frontmatter_start()`** in `scripts/sync-platforms.py` — prueft nach jedem `sync()`-Lauf, dass jede generierte Adapter-Datei mit `---\n` an Byte 0 startet. Exit 1 bei Verletzung.

### Changed

- **Frontmatter-Order-Fix:** generierte Codex- und Copilot-Adapter (`*/agents/*.md`, `*/prompts/*.md`, `*/skills/*/SKILL.md`) hatten in v1.3.0 den `<!-- AUTO-GENERATED -->`-Kommentar VOR dem YAML-Frontmatter. Damit stand `---` nicht an Byte 0 — viele Markdown-Plugin-Loader (inkl. Codex) erkennen Frontmatter nur an Position 0. Die Reihenfolge ist jetzt: Frontmatter → Auto-Generated-Kommentar → Body.
- **`python` → `python3`** in README.md, README.en.md, AGENTS.md, CONTRIBUTING.md, PORT_HEADER (sync-platforms.py). Portabler auf Ubuntu-CI und Linux ohne `python`-Symlink.
- **DRY-Refactor** in `scripts/sync-platforms.py`: gemeinsamer Helper `render_ported_markdown()` ersetzt drei dupliziert geschriebene Render-Bloecke in `port_command`/`port_agent`/`port_skill`.

---

## [1.3.0] — 2026-05-09

### Hintergrund

Erstes plattform-uebergreifendes Release. `legal-audit-de` ist ab v1.3.0 zusaetzlich zu Claude Code auch auf **OpenAI Codex CLI** und **GitHub Copilot CLI** lauffaehig — unter Beibehaltung von `.claude/` als Source of Truth. Adapter werden via Generator (`scripts/sync-platforms.py`) deterministisch erzeugt; CI blockt PRs bei Drift.

### Added

- **Multi-Platform-Support:**
  - Neues Verzeichnis `.codex/` mit `config.toml`, `prompts/` (8 Prompts), `agents/` (3 Agents), `skills/` (4 Skills mit Auto-Routing).
  - Neues Verzeichnis `.github/prompts/`, `.github/agents/`, `.github/skills/` fuer GitHub Copilot CLI.
  - `AGENTS.md` (Top-Level) als plattform-uebergreifender Eintrittspunkt — wird von Codex automatisch geladen.
  - `.github/copilot-instructions.md` als Copilot-CLI-Top-Level-Instructions.
- **Sync-Tooling:** `scripts/sync-platforms.py` mit `--check` (CI), `--apply` (Maintainer), `--verbose`. Erzeugt aus `.claude/`-Source deterministisch alle Plattform-Adapter, ersetzt Tool-Namen und Pfad-Variablen, injiziert Auto-Routing-Block in Skills.
- **GitHub Actions:**
  - `.github/workflows/validate.yml` — bei jedem Push/PR: Sync-Check, Disclaimer-Check (Knowledge Base + Templates), Platzhalter-Scan, Markdown-Lint.
  - `.github/workflows/release.yml` — bei Tag-Push (`v*.*.*`): Pre-Release-Validation, Bundle-Build pro Plattform (Claude/Codex/Copilot ZIPs), automatische GH-Release-Erstellung mit aus CHANGELOG extrahierten Notes.
- **Pre-Write-Disclaimer-Check** im `legal-text-writer`-Agent — schliesst die Luecke auf Codex/Copilot, wo der `PostToolUse`-Hook fehlt.

### Changed

- **README.md / README.en.md:** Neuer "Installation"-Abschnitt mit getrennten Sektionen fuer Claude Code, Codex CLI und Copilot CLI; Tagline und Badges um Multi-Platform-Hinweis erweitert; Architektur-Tree zeigt Source-of-Truth- und Generator-Markierungen; Roadmap aktualisiert.
- **`legal-text-writer`-Agent** (`.claude/agents/legal-text-writer.md`): neue Sektion "Pre-Write-Disclaimer-Check (Plattform-uebergreifend)" mit explizitem Vorgehen vor jedem Write/create. In Claude Code redundant (Hook validiert ohnehin), auf Codex/Copilot die einzige Sicherung.
- **Auto-Routing in Skills** (Codex/Copilot-Versionen): jedes generierte `SKILL.md` enthaelt einen Auto-Routing-Block, der erklaert, wie das Skill `knowledge/INDEX.md` selbst liest und passende KB-Chunks zieht — Ersatz fuer fehlende SessionStart-/UserPromptSubmit-Hooks. Source-Skills in `.claude/skills/` bleiben unveraendert (Hooks decken das dort ab).

### Fixed

- v1.2.0 retroaktiv getaggt (Commit `c832bcb`), damit das Tag-zu-Commit-Mapping konsistent bleibt fuer den Release-Workflow.

### Limitations (dokumentiert)

- **Kein WebSearch** in Codex/Copilot — Tier-1-Verifikation laeuft nur via WebFetch/`http.get` auf der Whitelist-Domain-Liste.
- **chrome-devtools-mcp** fuer `/legal-audit-live` benoetigt MCP-Server-Konfiguration auf Codex/Copilot; in Claude Code direkt verfuegbar.
- **`model:`-Felder** in Custom Agents werden auf Copilot CLI ignoriert; Codex-User waehlen aequivalentes Modell mit grossem Kontext.

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
