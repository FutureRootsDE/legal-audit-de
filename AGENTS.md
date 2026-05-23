# AGENTS.md — legal-audit-de

> Top-Level-Eintrittspunkt fuer **alle** Agent-CLIs (Codex, Copilot, generisch). Claude Code nutzt parallel `CLAUDE.md`. Inhaltlich identisch — Plattform-Spezifika werden in den jeweiligen `.codex/` / `.github/`-Subverzeichnissen aufgeloest.

---

## Haftungsausschluss — Keine Rechtsberatung

> Dieses Plugin erzeugt **keine Rechtsberatung** im Sinne von § 2 RDG. Alle Outputs (LegalAudit.md, Clean-Versionen, KB-Artikel, Command-Outputs) dienen der **technischen Vorbereitung** einer anwaltlichen Pruefung. Eine abschliessende Pruefung durch einen zugelassenen Rechtsanwalt (Fachanwalt fuer IT-Recht oder spezialisierter Datenschutz-Experte) ist **zwingend erforderlich**, bevor Inhalte produktiv gesetzt werden. Gesetze und Rechtsprechung aendern sich — Aktualitaet stets verifizieren.

Jede vom Plugin erzeugte Output-Datei muss diesen Disclaimer am Kopf tragen. Auf Codex/Copilot fehlt der `PostToolUse`-Hook, der das in Claude Code automatisch validiert — der `legal-text-writer`-Agent prueft den Disclaimer daher **vor** jedem Write selbst.

---

## Was macht das Plugin?

`legal-audit-de` ist ein KI-Rechts-Audit-Workspace fuer deutsches und EU-Recht. Es scannt fremde Codebases, einzelne Rechtsdokumente (AGB, DSE, Impressum) und Live-URLs auf rechtliche Probleme nach **DE/EU-Scope** und liefert:

- `LegalAudit.md` mit Findings, klassifiziert nach Severity (CRIT/HIGH/MED/LOW)
- Clean-Versionen pro Finding (`docs/legal-audit/clean/F-NNN-<slug>.md`) — direkt uebernehmbar
- `SUMMARY.md` als Management-Kurzfassung
- Schatten-Archiv aller Audits (DSGVO-Rechenschaftspflicht Art. 5 Abs. 2)

**Scope:** DSGVO · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · MarkenG · NIS2-BSIG.

**Nicht im Scope:** Strafrecht, Arbeitsrecht, Steuerrecht (ausser HGB § 257 Retention), Gesellschaftsrecht, nicht-EU-Rechtsordnungen.

---

## Plattform-Layouts

| Plattform | Konfigurations-Verzeichnis | Slash-Commands / Prompts | Custom Agents | Skills |
|----|----|----|----|----|
| **Claude Code** | `.claude/`, `.claude-plugin/plugin.json` | `.claude/commands/*.md` | `.claude/agents/*.md` | `.claude/skills/<name>/SKILL.md` |
| **OpenAI Codex CLI** | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.codex/config.toml` | `.codex/prompts/*.md` | `.codex/agents/*.md` | `.codex/skills/<name>/SKILL.md` |
| **GitHub Copilot CLI** | `.github/copilot-instructions.md` | `.github/prompts/<name>/PROMPT.md` | `.github/agents/*.md` | `.github/skills/<name>/SKILL.md` |

**Source of Truth:** `.claude/`. Codex- und Copilot-Adapter werden via `python3 scripts/sync-platforms.py --apply` generiert. CI prueft die Konsistenz mit `--check`.

---

## Commands / Prompts

| Name | Zweck | Plattformen |
|----|----|----|
| `legal-audit <pfad>` | Vollstaendiger Codebase-Audit → LegalAudit.md + clean/ + SUMMARY.md | Claude / Codex / Copilot |
| `legal-audit-live <url>` | Live-Browser-Check via chrome-devtools-mcp (Cookie-Banner, Google-Fonts-Leak, Tracking) | Claude (voll) / Codex+Copilot (nur wenn MCP konfiguriert) |
| `legal-doc-check <datei>` | Einzeldokument-Pruefung (AGB, DSE, Impressum, Widerruf, Cookie-Policy) | Claude / Codex / Copilot |
| `legal-kb <slug>` | KB-Artikel gezielt laden | Claude / Codex / Copilot |
| `legal-verify <thema>` | Fachanwalts-/Tool-Empfehlungen | Claude / Codex / Copilot |
| `legal-update [slug\|--stale-only\|--all\|--fix-pending]` | KB gegen Primaerquellen aktualisieren | Claude (voll) / Codex+Copilot (eingeschraenkt — kein WebSearch, nur WebFetch/http.get auf whitelist-Domains) |
| `legal-status [--verbose\|--json]` | Plugin-Health-Check | Claude / Codex / Copilot |

---

## Custom Agents

Drei Agents, alle als Single-Responsibility ausgelegt:

| Agent | Aufgabe |
|----|----|
| `legal-auditor` | Scant Codebase, klassifiziert Findings nach Severity-Matrix |
| `legal-researcher` | Verifiziert jedes Zitat doppelt gegen Tier-1-Primaerquelle |
| `legal-text-writer` | Erstellt lupenreine Clean-Versionen inkl. Pre-Write-Disclaimer-Check |

**Modell-Hinweis (Plattform-spezifisch):**
- Claude Code: alle drei laufen auf `claude-opus-4-7[1m]` (1M Kontext fuer komplette Gesetzestexte + grosse Codebases). Pro-Abonnenten ohne 1M-Usage-Credits aktivieren Pro-Mode via `python3 scripts/legal-audit-pro-mode.py enable` (swappt auf Standard-Kontext + chunked Execution mit Logfile).
- Codex: User waehlt aequivalentes Modell (`gpt-5` oder grosses-Kontext-Modell).
- Copilot CLI: das `model`-Feld wird ignoriert; Copilot nutzt seinen eigenen Default.

---

## KB-Routing (Plattform-Unterschiede)

In Claude Code laden Hooks die KB-Chunks automatisch:
- `SessionStart-Hook` laedt `knowledge/INDEX.md` (immer).
- `UserPromptSubmit-Hook` matcht den Prompt gegen Schlagwoerter aus `.claude/hooks/triggers.json` und laedt bis zu 3 passende KB-Chunks aus `knowledge/themen/` etc.

In Codex/Copilot fehlt diese Hook-API. Die Skills uebernehmen das Routing daher selbst — siehe Auto-Routing-Block in jedem `.codex/skills/*/SKILL.md` und `.github/skills/*/SKILL.md`.

**Limitation:** Die Auto-Routing-Variante ist token-teurer als der Hook-basierte Ansatz, weil das Skill jeweils `knowledge/INDEX.md` selbst lesen muss. Fuer kurze Audits unkritisch.

---

## Quellen-Hierarchie (verbindlich fuer Zitat-Verifikation)

### Tier 1 — Primaerquellen (nur diese zaehlen als Zitatbeleg)
- `eur-lex.europa.eu` (EU-Primaerrecht, CELEX, konsolidierte Fassungen)
- `gesetze-im-internet.de` (DE-Gesetze, BMJ-offiziell)
- `rechtsprechung-im-internet.de` (DE-Rechtsprechung)
- `curia.europa.eu` (EuGH)
- `bundesanzeiger.de` (Verordnungen)

### Tier 2 — Amtliche Sekundaerquellen
- `bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, Landesbeauftragte, `bsi.bund.de`

### Tier 3 — Fach-Einordnung (**nie** als Zitat-Grundlage)
- `dr-schwenke.de`, `haerting.de`, `datenschutz-notizen.de`, `e-recht24.de`, `it-recht-kanzlei.de`

Der `legal-researcher`-Agent verifiziert vor Publikation jedes Zitat gegen eine Tier-1-Quelle und schreibt ein Log unter `.claude/logs/zitate-verifikation-<YYYY-MM-DD>.log` (bzw. das jeweilige Plattform-Log-Verzeichnis).

---

## Sprachregeln

- **Antworten und KB-Inhalte:** Deutsch, volle Orthographie inklusive Umlaute (ä, ö, ü) und ß.
- **Code-Kommentare:** Englisch (Konvention).
- **In Plattform-Konfig-Files** (TOML, JSON): wo ASCII-only sicherer ist (z.B. fuer YAML-Frontmatter-Felder, die manche Parser nicht UTF-8-handhaben), `ae/oe/ue/ss` verwenden — der Repo-Stil ist konsistent etabliert.

---

## Sicherheits- und Permissions-Modell

Jede Plattform erlaubt nur Tier-1- und Tier-2-Domains fuer WebFetch / http.get. Die Whitelist (~20 Domains) steht in:
- Claude Code: `.claude/settings.json` → `permissions.allow`
- Codex: `.codex-plugin/plugin.json` → native Plugin-Metadaten; `.codex/config.toml` → `[permissions] web_fetch_domains`
- Copilot CLI: in `.github/copilot-instructions.md` als Hinweis (Copilot enforced Permissions ueber GitHub-App-Scopes, nicht ueber Plugin-Config)

Bash-Patterns sind jeweils auf read-only-Operationen beschraenkt (`mkdir`, `chmod`, `find`, `grep`, `cat`, `jq`, `git log`, `git diff`, `git rev-parse`).

---

## Wartung

- KB-Aktualitaet: alle 90 Tage `legal-update --stale-only`.
- Trigger-Katalog (`.claude/hooks/triggers.json`): erweitern, wenn haeufige Prompts keine passenden KB-Chunks laden.
- Cross-Platform-Sync: nach jeder Aenderung in `.claude/` muss `python3 scripts/sync-platforms.py --apply` laufen. CI blockiert Drift.
- Anwalts-/Tool-Liste: halbjaehrlich pruefen.

---

## Verweise

- `CLAUDE.md` — Claude-Code-spezifische Anleitung (deckt Hook-Mechanik im Detail).
- `.github/copilot-instructions.md` — Copilot-CLI-Top-Level-Instructions.
- `.codex-plugin/plugin.json` — natives Codex-Plugin-Manifest.
- `.agents/plugins/marketplace.json` — lokale Codex-Marketplace-Definition fuer `codex plugin marketplace add`.
- `.codex/config.toml` — Codex-Konfiguration (Permissions, Sprache, Disclaimer).
- `README.md` / `README.en.md` — User-Doku mit Installations-Anleitung pro Plattform.
- `CHANGELOG.md` — Versions-Historie.
