# Contributing to legal-audit-de

Thank you for contributing to this plugin! Legal topics change constantly, and every update helps the whole community.

🇩🇪 [Deutsche Version](CONTRIBUTING.md)

## Important note on legal content

**Not legal advice.** This plugin produces technical preparation for attorney reviews, not binding legal statements. When you submit contributions:

- Verify all citations against **Tier-1 primary sources** (see `CLAUDE.md`, section "Quellen-Hierarchie")
- Mark uncertain or unverifiable statements with `<<VERIFIKATION AUSSTEHEND>>`
- Never use secondary sources (law firm blogs, eRecht24, etc.) as citation evidence — only for context

## How to contribute

### 🐛 Bug report / incorrect legal information

Please open an [Issue](https://github.com/FutureRootsDE/legal-audit-de/issues/new) with:

- Exact path to the affected file
- Quote the problematic passage
- Primary source that contradicts it (with link)
- Suggested correction

### ✨ New KB articles

New articles go under `knowledge/themen/` with the following frontmatter:

```yaml
---
aktualisiert: 2026-04-21
quelle-primaer: https://www.gesetze-im-internet.de/...
quellen-sekundaer:
  - https://...
verifiziert-am: 2026-04-21
geltungsbereich: [DE, EU]
---
```

Plus:
- Disclaimer block directly after the frontmatter (from `templates/disclaimer-block.md`)
- Cross-reference block at the end (`## Siehe auch`) with wiki links
- Entry in `knowledge/INDEX.md`
- Trigger pattern in `.claude/hooks/triggers.json` (if auto-loading is desired)

**KB content must be in German** — paragraph wording is binding in the original language. Only translate when the meta-discussion (e.g. how to contribute) is meant for an international audience.

### 🔄 KB update

When a statute, case, or authority guideline has changed:

1. Edit the file
2. Update `verifiziert-am:` in the frontmatter
3. Remove `<<VERIFIKATION AUSSTEHEND>>` placeholders when verified
4. Submit PR with a link to the primary source

### 🧰 New commands / agents / skills

Format like existing artifacts in `.claude/commands/`, `.claude/agents/`, `.claude/skills/`. Important:
- Correct frontmatter (description, argument-hint, allowed-tools)
- Disclaimer reference in the output path
- Description of the severity classification

### 🌍 Translations

Contributions to the English wiki pages or `knowledge/en/SUMMARY.md` are welcome. Please note:
- German remains the primary language for KB content (paragraph wording is binding in the original)
- English serves as an entry and overview layer, not as a replacement for the German legal text
- When translating wiki pages, keep the file naming pattern `<Name>-English.md`

## Development setup

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de

# Python dependencies for hooks + scripts
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt  # if present

# Test hooks
python .claude/hooks/session_start.py
python .claude/hooks/prompt_submit.py <<< "test prompt about cookies"

# Try scripts
python scripts/legal-status.py
python scripts/find-placeholders.py
```

## Commit message convention

```
<type>(<scope>): <short description>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `kb`, `test`, `refactor`, `chore`

Scopes: `commands`, `agents`, `skills`, `hooks`, `knowledge`, `templates`, `scripts`

Examples:
- `feat(commands): add /legal-kb-preview to show KB file without loading`
- `kb(urteile): update BGH Cookie-Einwilligung II (I ZR 7/16) with 2025 follow-up`
- `fix(hooks): correct regex for ai-act trigger pattern`

## Pull request process

1. Fork the repo + create a branch (`feat/xyz`, `fix/xyz`, `kb/xyz`)
2. Commit changes (following the commit convention)
3. Open a PR with:
   - Description of the change
   - For KB changes: link to the primary source
   - Checklist:
     - [ ] Disclaimer validated in output path
     - [ ] Citations checked against Tier-1 sources
     - [ ] `aktualisiert:` / `verifiziert-am:` maintained
     - [ ] Cross-references updated
4. Maintainer review
5. Merge

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — short form: be kind, respect diverse perspectives, constructive criticism welcome, harassment and discrimination are not tolerated.

## License

All contributions fall under the project's [MIT License](LICENSE).

## Questions?

[Open an issue](https://github.com/FutureRootsDE/legal-audit-de/issues/new) or [start a discussion](https://github.com/FutureRootsDE/legal-audit-de/discussions).
