# GitHub Copilot Instructions — legal-audit-de

> Diese Datei wird von **GitHub Copilot CLI** beim Session-Start automatisch geladen. Sie ist der Top-Level-Eintrittspunkt fuer Copilot-Sessions in diesem Repository.

---

## Haftungsausschluss — Keine Rechtsberatung

> Dieses Plugin erzeugt **keine Rechtsberatung** im Sinne von § 2 RDG. Alle Outputs (LegalAudit.md, Clean-Versionen, KB-Artikel, Command-Outputs) dienen der **technischen Vorbereitung** einer anwaltlichen Pruefung. Eine abschliessende Pruefung durch einen zugelassenen Rechtsanwalt ist **zwingend erforderlich**, bevor Inhalte produktiv gesetzt werden.

Jede vom Plugin erzeugte Output-Datei muss diesen Disclaimer am Kopf tragen. Copilot CLI hat keinen `PostToolUse`-Hook — der `legal-text-writer`-Agent muss den Disclaimer **vor** jedem Write-Aufruf selbst pruefen.

---

## Sprachregeln

- **User-Antworten und alle Markdown-Inhalte:** Deutsch, mit voller Orthographie (Umlaute ä/ö/ü, ß). Keine ASCII-Substitutionen wie `ae/oe/ue/ss` in Output-Texten — nur dort, wo der Repo-Stil das bereits etabliert hat (z.B. in YAML-Frontmatter-Feldern, die manche Parser nicht UTF-8-handhaben).
- **Code-Kommentare:** Englisch.

---

## Verfuegbare Prompts

Slash-Prompts liegen unter `.github/prompts/`. Aufruf via `gh copilot suggest "fuehre <prompt-name> auf <argument> aus"`:

| Prompt | Aufgabe |
|----|----|
| `legal-audit` | Vollstaendiger Codebase-Audit |
| `legal-audit-live` | Live-Browser-Check (benoetigt MCP) |
| `legal-doc-check` | Einzeldokument-Pruefung (AGB/DSE/Impressum/...) |
| `legal-kb` | KB-Artikel laden |
| `legal-verify` | Anwalts-/Tool-Empfehlungen |
| `legal-update` | KB gegen Primaerquellen aktualisieren |
| `legal-status` | Plugin-Health-Check |

---

## KB-Routing

GitHub Copilot CLI hat **keinen SessionStart-Hook** und **keinen UserPromptSubmit-Hook**. Das Plugin loest das so:

1. Copilot soll bei der ersten KB-relevanten Anfrage `knowledge/INDEX.md` lesen (~200 Zeilen) und merken, welche Schlagworte zu welchen Subdateien gehoeren.
2. Bei Bedarf maximal 3 Subdateien aus `knowledge/themen/`, `knowledge/urteile/`, `knowledge/gesetze/` oder `knowledge/checklisten/` per `view` lesen.
3. Triggers stehen in `.claude/hooks/triggers.json` (gleicher Schlagwort-Katalog gilt fuer Copilot).

---

## Permissions / WebFetch-Whitelist

Copilot CLI verwaltet Permissions ueber GitHub-App-Scopes — eine plugin-lokale Allow-List wie in Claude Code (`.claude/settings.json`) gibt es nicht. Beim Web-Fetch gilt trotzdem die Konvention: **nur** folgende Domains anfragen (Tier-1- und Tier-2-Quellen):

```
eur-lex.europa.eu, gesetze-im-internet.de, rechtsprechung-im-internet.de,
curia.europa.eu, bundesanzeiger.de, bfdi.bund.de,
datenschutzkonferenz-online.de, edpb.europa.eu, bmj.de, bmwk.de,
ec.europa.eu, bsi.bund.de, lda.bayern.de, openjur.de,
e-recht24.de, it-recht-kanzlei.de, datenschutz-notizen.de,
dr-schwenke.de, haerting.de, dsgvo-gesetz.de
```

Andere Domains erfordern explizite User-Zustimmung.

---

## Limitationen gegenueber Claude Code

| Feature | Claude Code | Copilot CLI |
|----|----|----|
| SessionStart-Hook (laedt INDEX.md automatisch) | ✓ | ✗ — Skills laden selbst |
| UserPromptSubmit-Hook (laedt KB-Chunks per Schlagwort) | ✓ | ✗ — Skills routen selbst |
| PostToolUse-Hook (validiert Disclaimer) | ✓ | ✗ — Pre-Write-Check im Agent |
| WebSearch | ✓ | ✗ — nur `web_fetch` auf Whitelist |
| chrome-devtools-mcp fuer Live-Audit | ✓ (wenn MCP konfiguriert) | nur wenn MCP-Server konfiguriert |

---

## Verweise

- `AGENTS.md` — Top-Level-Eintrittspunkt fuer alle Agent-CLIs.
- `CLAUDE.md` — Claude-Code-spezifische Anleitung.
- `README.md` / `README.en.md` — User-Doku mit Installation pro Plattform.
- `.codex/config.toml` — Codex-Pendant zu dieser Datei.
