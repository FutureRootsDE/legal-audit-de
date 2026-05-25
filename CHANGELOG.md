# Changelog

Alle wesentlichen Aenderungen an diesem Projekt werden hier dokumentiert.

Format: [Semantic Versioning](https://semver.org/), Datumsformat: YYYY-MM-DD.

---

## [1.2.0] — 2026-05-25

### Hinzugefuegt

- **Pro-Mode** fuer Claude-Pro-Abonnenten (20 USD/Mo, kein Max-Abonnement erforderlich)
  - Sechs permanente Agenten-Varianten: `legal-auditor-pro`, `legal-researcher-pro`,
    `legal-text-writer-pro` neben den drei bestehenden 1M-Varianten
  - Agenten-Routing via Marker-Datei in `${CLAUDE_PLUGIN_DATA}/pro-mode.json`
    (ueberlebt `/plugin install` und Marketplace-Refreshes)
  - `scripts/legal-audit-pro-mode.py` — Toggle-CLI (`enable | disable | status [--json]`)
  - `scripts/sync-pro-variants.py` — Generator fuer Pro-Agenten aus Source-Agenten
    (Single-Source-of-Truth: Prompt-Body nur in 1M-Varianten pflegen)
  - Neuer Command `/legal-pro-mode` — steuert Pro-Mode mit Sub-Befehlen
  - SessionStart-Hook erkennt aktiven Pro-Mode und injiziert Routing-Tabelle als Context
  - Kontext-Management-Protokoll in jedem Pro-Agenten (Groessen-Check, Priorisierung)
  - Pro-Mode-Block in `/legal-status` Output

- **Pro-Mode-Awareness** in allen Dispatch-Commands:
  - `/legal-audit`, `/legal-doc-check`, `/legal-update`, `/legal-audit-de-update`
  - Jeder Command prueft Marker und waehlt Standard- oder Pro-Agent

### Behoben

- **Issue #3:** `marketplace.json` hatte falsches `"source": "./"` Format.
  Korrigiert auf `{"source": "github", "repo": "FutureRootsDE/legal-audit-de"}` —
  ermoeglicht korrekte Installation via Claude Marketplace ohne manuelle Pfadangabe.

- **Issue #4:** Max-Abonnement-Sperre entfernt. Pro-Abonnenten koennen das Plugin
  jetzt im Pro-Mode nutzen (Standard-Kontext statt 1M).

### Architektur

- Standard-Agenten (`claude-opus-4-7[1m]`) bleiben unveraendert — kein Breaking Change
  fuer Max-Abonnenten
- Marker-Persistenz nutzt offiziellen `${CLAUDE_PLUGIN_DATA}` Speicher
- `sync-pro-variants.py --check` kann in CI/CD genutzt werden um Drift zu erkennen
- Chunked-Modus fuer Codebases > 200k Tokens ist geplant fuer v1.4.0

---

## [1.1.0] — 2026-04-21

### Hinzugefuegt

- Claude Marketplace-Struktur (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`)
- `/legal-audit-de-update` Command — kombinierter Plugin + KB-Update
- `/legal-status` Command + `scripts/legal-status.py`
- `scripts/audit-compare.py` — Diff zwischen zwei Audits
- `scripts/find-placeholders.py` — listet VERIFIKATION-AUSSTEHEND-Stellen
- `scripts/legal-audit-pdf.py` — HTML/PDF-Briefing-Generator
- `templates/git-hooks/pre-commit.sh` — Git-Hook-Template fuer rechts-relevante Dateien
- `CONTRIBUTING.md` und `CONTRIBUTING.en.md`
- `CODE_OF_CONDUCT.md`

---

## [1.0.0] — 2026-04-10

### Erstveroeffentlichung

- Kern-Plugin mit drei Agenten: `legal-auditor`, `legal-researcher`, `legal-text-writer`
- Knowledge Base fuer DE/EU-Recht: DSGVO, BDSG, TDDDG, UWG, BGB-AGB, DDG, DSA, DMA,
  AI Act, BFSG, UrhG, MarkenG, NIS2-BSIG, PAngV
- Commands: `/legal-audit`, `/legal-audit-live`, `/legal-doc-check`, `/legal-kb`,
  `/legal-verify`, `/legal-update`
- Hooks: SessionStart (KB-Index), UserPromptSubmit (Trigger-basiertes KB-Laden),
  PostToolUse (Disclaimer-Validierung)
- Checklisten fuer 5 Codebase-Typen: SaaS, Landingpage, n8n, E-Commerce, Content/Blog
- Severity-Matrix: CRIT / HIGH / MED / LOW
- Quellen-Hierarchie: Tier 1 (Primaerquellen) bis Tier 3 (Fach-Einordnung)
