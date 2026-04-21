# legal-audit-de

> Claude Code plugin for systematic **German and EU legal audits** of codebases, live URLs, and legal documents.
>
> **⚠️ This is NOT legal advice.** See [Disclaimer](#disclaimer) below.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Language](https://img.shields.io/badge/content%20language-German-informational)](#language)
[![Scope](https://img.shields.io/badge/scope-DE%20%2F%20EU-blue)](#legal-scope)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-orange)](#installation)

🇩🇪 [Deutsche Version](README.md)

---

## What is `legal-audit-de`?

A Claude Code plugin that acts like an IT / privacy legal audit workflow. It analyzes codebases, live websites, and individual legal documents for violations of **German and EU law** and produces:

- **`LegalAudit.md`** — finding table with severity classification (CRIT / HIGH / MED / LOW)
- **Clean versions** of flagged passages — ready to paste 1:1 into your project
- **Live browser checks** via `chrome-devtools-mcp` (cookie banner blocking, Google Fonts leaks, pre-/post-consent behavior)
- **Single-document reviews** (T&Cs, privacy policy, imprint, withdrawal notice, cookie policy)

## Who is this for?

Designed for developers, founders, and small teams operating in or targeting the German / EU market who:

- Don't have an in-house legal department
- Need to prepare compliance documentation before attorney review
- Want to reduce the hours of attorney billing spent on "obvious" issues
- Work with AI-assisted development and want their tooling to know DE/EU law specifics

**English-speaking engineers in Germany** are explicitly in scope — the plugin handles the rigorous German paragraph references while giving you English-language explanations in the wiki.

## Features

### 🔎 Commands

| Command | Purpose |
|---------|---------|
| `/legal-audit <path>` | Full legal audit of a codebase |
| `/legal-audit-live <url>` | Live browser check of a public URL |
| `/legal-doc-check <file>` | Single-document review (T&C / privacy / imprint / withdrawal / cookie / social bio) |
| `/legal-kb <slug>` | Load a specific KB article into context |
| `/legal-verify <topic>` | Attorney and tool recommendations |
| `/legal-update [--stale-only]` | Refresh KB against primary sources |
| `/legal-audit-de-update` | **NEW** — Update plugin + KB together (marketplace refresh + primary source verification) |
| `/legal-status` | Plugin health (KB age, placeholders, hook status) |

### 🤖 Agents

Three custom agents, all on Claude Opus 4.7 [1M] — maximum citation accuracy:

- `legal-auditor` — scans codebase, classifies findings
- `legal-researcher` — verifies every citation against Tier-1 primary sources
- `legal-text-writer` — produces clean versions with automatic disclaimer injection

### 📚 Knowledge Base

63 curated KB files with primary-source links:

- **Statutes**: GDPR (DSGVO), BDSG, TDDDG (cookies), UWG (competition), PAngV (pricing), BGB (civil code, T&C), DDG (digital services), DSA, DMA, AI Act, BFSG (accessibility), UrhG (copyright), KUG (image rights), MarkenG (trademark), NIS2-BSIG (IT security)
- **Topics**: Cookie consent, tracking, privacy policy, T&C, withdrawal, international transfers, DPA, ROPA, TOM, DPIA, AI transparency, social media, image rights, seal-based advertising, quotation right, tool catalog (80+ tools)
- **Case law**: ECJ Schrems II, Planet49, Fashion ID, Meta/Bundeskartellamt; BGH Cookie Consent, Inbox Advertising; Munich I "Google Fonts"
- **Authorities**: DSK, EDPB, BfDI, state data protection officers
- **Checklists** for SaaS, landing pages, e-commerce, n8n, content/blog, pre-launch

### ⚡ Hook-based context management

The key: the 63 KB files are **not** loaded into every session. Instead:

- **SessionStart hook** loads only `knowledge/INDEX.md` (~1,000 tokens)
- **UserPromptSubmit hook** matches prompts against regex patterns in `.claude/hooks/triggers.json` and loads up to 3 relevant KB chunks on-demand
- **PostToolUse hook** validates disclaimer injection in every written output

This keeps your context window lean while current legal knowledge is always within reach.

## Installation

### Requirements

- [Claude Code](https://claude.com/claude-code) ≥ 2.0
- Python ≥ 3.10 (for hook scripts)
- Optional: [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) for `/legal-audit-live`
- Optional: [Obsidian](https://obsidian.md/) for visual KB navigation (graph view, backlinks)

### Install via marketplace (recommended)

```bash
# In Claude Code — add marketplace, then install plugin
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

That's it. For updates later:
```bash
/plugin marketplace update futureroots-legal
/legal-audit-de-update
```

### As a workspace clone

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de
claude
```

On first start, the SessionStart hook automatically loads `knowledge/INDEX.md`. Then you can run:

```
/legal-audit /path/to/your/project
```

## Quick Start

### 1. Codebase audit

```
/legal-audit /path/to/your/nextjs-saas
```

Claude detects the project type (SaaS / landing page / e-commerce / n8n / content), picks the matching checklist, and dispatches the three agents for full analysis + clean versions + citation verification. Output lands in `docs/legal-audit/` inside the target project.

### 2. Live website check

```
/legal-audit-live https://your-website.com
```

Uses browser automation to check which third-party requests fire before and after cookie consent. Catches classic violations: Google Fonts runtime leaks, trackers before consent, pixels without opt-in.

### 3. Document review

```
/legal-doc-check /path/to/your/tos.md
```

Individual legal texts (T&C, privacy policy, imprint, withdrawal notice, cookie policy) are reviewed against current law. Produces a finding table + fully corrected version.

## Legal scope

**Covered:** GDPR · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · KUG · MarkenG · NIS2-BSIG

**Out of scope:** Criminal law · Employment law · Tax law (except HGB § 257 retention) · Corporate law · Jurisdictions outside DE/EU

## Language

All outputs, findings, and KB articles are in **German**. Code comments and metadata use English.

Why German content? Because German legal paragraph wording is binding in the original language. A slightly off translation of "§ 7 Abs. 3 UWG" into English could mislead an attorney reviewing your output. The plugin therefore keeps all legal text in German — but gives you English-language explanations in the [wiki](https://github.com/FutureRootsDE/legal-audit-de/wiki/Home-English) and this README.

## Source hierarchy

The `legal-researcher` agent verifies every citation against:

**Tier 1** (binding): `eur-lex.europa.eu`, `gesetze-im-internet.de`, `rechtsprechung-im-internet.de`, `curia.europa.eu`, `bundesanzeiger.de`

**Tier 2** (official secondary): `bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, state data protection officers, `bsi.bund.de`

**Tier 3** (context only, never as citation evidence): Law firm blogs

Every verification is logged under `.claude/logs/zitate-verifikation-<date>.log`.

## Architecture

See [CLAUDE.md](CLAUDE.md). Short version:

```
legal-audit-de/
├── plugin.json                 # Plugin manifest
├── CLAUDE.md                   # Claude Code orientation
├── .claude/
│   ├── commands/*.md           # 7 slash commands
│   ├── agents/*.md             # 3 custom agents
│   ├── skills/*/SKILL.md       # 4 skills
│   ├── hooks/*.py              # 3 hooks (SessionStart / PromptSubmit / PostToolUse)
│   └── settings.json           # Hook registration
├── knowledge/                  # 63 KB files (statutes, topics, case law, authorities, checklists, attorney tools)
│   └── INDEX.md                # the only always-loaded file
├── templates/                  # LegalAudit, clean, disclaimer templates
└── scripts/                    # Python helpers
```

## Roadmap

- [ ] Submission to the Claude Code plugin marketplace
- [ ] English KB summary under `knowledge/en/SUMMARY.md` (for non-German-speaking users)
- [ ] Additional checklists: mobile apps (iOS/Android BFSG), API-only services
- [ ] Integration with `trivy`, `bandit`, other security scanners for combined audits
- [ ] CI integration: GitHub Action for automated KB freshness checks

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (German) / [CONTRIBUTING.en.md](CONTRIBUTING.en.md) (English):
- New checklists
- KB articles on special topics
- English wiki translations
- Verification of outdated citations
- Bug reports for incorrect statements

## Disclaimer

> **⚠️ This plugin does NOT provide legal advice within the meaning of § 2 RDG (German Legal Services Act).**
>
> All outputs (LegalAudit.md, clean versions, KB articles, command results) are intended as **technical preparation** for review by a licensed attorney. Final approval by a qualified attorney (specialist for IT law, or a certified data protection expert) is **mandatory** before putting content into production.
>
> Laws and case law change — verify currency before relying on any output.
>
> Use of this plugin is at your own risk. The authors and contributors assume no liability for damages arising from use or reliance on the outputs. See [LICENSE](LICENSE) for the full disclaimer.

## Ethics and responsibility

This plugin is meant to:
- **Reduce preparation time** for legal reviews
- **Democratize standards** — even solo founders should be able to launch compliantly
- **Sensitize developers** to key legal topics in the DE/EU context

This plugin is **not** meant to:
- Replace attorneys or data protection officers
- Legitimize production decisions without human review
- Cover up incorrect or outdated statements (we maintain issues and PRs for that)

If you use the plugin professionally, please indicate that it's a **preparatory tool** and secure attorney sign-off.

## Security

See [SECURITY.md](SECURITY.md) for the vulnerability disclosure policy.

## License

[MIT](LICENSE) — free for any purpose. All rights to cited statutes and judgments remain with their respective holders (EU, Federal Republic of Germany, courts).

## Credits

Built on [Claude Code](https://claude.com/claude-code) by Anthropic.

Inspired by the observation that GDPR compliance is unnecessarily hard for technical teams without a legal department — and that good preparation tooling makes qualified attorney access affordable for solo founders.

---

**Questions? Issues? Contributions?** → [GitHub Issues](https://github.com/FutureRootsDE/legal-audit-de/issues) · [Discussions](https://github.com/FutureRootsDE/legal-audit-de/discussions) · [Wiki](https://github.com/FutureRootsDE/legal-audit-de/wiki)
