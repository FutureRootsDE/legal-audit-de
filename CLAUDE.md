# CLAUDE.md — legal-audit-de

Dieses Dokument gibt Claude Code (claude.ai/code) Orientierung, wenn das Plugin in einem Workspace aktiv ist.

---

## Projekt-Kurzbeschreibung

**legal-audit-de** ist ein Claude-Code-Plugin, das eine spezialisierte Audit-Umgebung für **deutsches und EU-Recht** bereitstellt. Es agiert wie ein IT-/Datenschutz-Fachaudit-Prozess: scannt fremde Codebases systematisch auf rechtliche Probleme, dokumentiert Findings in `LegalAudit.md` im Zielprojekt und liefert „lupenreine" Korrektur-Versionen, die 1:1 übernommen werden können.

**Scope** (aktiviert): DSGVO · BDSG · TDDDG · UWG · PAngV · BGB/AGB · DDG · DSA · DMA · AI Act · BFSG · UrhG · MarkenG · NIS2-BSIG.

**Nicht im Scope:** Strafrecht, Arbeitsrecht, Steuerrecht (außer HGB § 257 Retention), Gesellschaftsrecht, nicht-EU-Rechtsordnungen.

---

## HAFTUNGSAUSSCHLUSS — KEINE RECHTSBERATUNG

> Dieses Plugin erzeugt **keine Rechtsberatung** im Sinne des § 2 RDG. Alle Ausgaben (LegalAudit.md, Clean-Versionen, KB-Artikel, Command-Outputs) dienen der **technischen Vorbereitung** einer anwaltlichen Prüfung. Eine abschließende Prüfung durch einen zugelassenen Rechtsanwalt (Fachanwalt für IT-Recht oder spezialisierter Datenschutz-Experte) ist **zwingend erforderlich**, bevor Inhalte produktiv gesetzt werden. Gesetze und Rechtsprechung ändern sich — Aktualität stets verifizieren.

Jede vom Plugin erzeugte Output-Datei trägt diesen Disclaimer am Kopf. Der `PostToolUse`-Hook (`post_write.py`) warnt, wenn er fehlt.

---

## Commands — Quick Reference

| Command | Zweck |
|---------|-------|
| `/legal-audit <pfad>` | Vollständiger Rechts-Audit einer Codebase → `<pfad>/docs/legal-audit/` |
| `/legal-audit <pfad> --compare` | Audit + Diff-Report gegen letztes Audit aus `audits/`-Archiv |
| `/legal-audit <pfad> --pdf` | Audit + generiert `anwalts-briefing.html` (+ PDF wenn pandoc vorhanden) |
| `/legal-audit-live <url>` | Live-Browser-Check via chrome-devtools-mcp: Cookie-Banner-Blocking, Google-Fonts-Leak, Pre-/Post-Consent-Verhalten |
| `/legal-doc-check <datei>` | Einzel-Dokument-Prüfung (AGB / DSE / Impressum / Widerruf / Cookie-Richtlinie / Social-Bio) ohne Codebase-Kontext |
| `/legal-kb <slug>` | KB-Artikel gezielt in den Kontext laden |
| `/legal-verify <thema>` | Fachanwalts-/Tool-Empfehlungen |
| `/legal-update [slug\|--stale-only\|--all\|--fix-pending]` | KB gegen Primärquellen aktualisieren |
| `/legal-audit-de-update [--plugin-only\|--kb-only\|--dry-run]` | Plugin + KB gemeinsam aktualisieren (Marketplace-Refresh + Primärquellen) |
| `/legal-status [--verbose\|--json]` | Plugin-Gesundheit: KB-Alter, Platzhalter, Hook-Status, Audit-Historie |

Details in `.claude/commands/*.md`. Hilfs-Skripte unter `scripts/`:
- `legal-status.py` — Status-Report
- `audit-compare.py` — Diff zwischen zwei Audits (`--auto <pfad>` findet vorheriges)
- `find-placeholders.py` — listet alle `<<VERIFIKATION AUSSTEHEND>>`/`<<UNVERIFIZIERT>>`-Stellen
- `legal-audit-pdf.py` — bundled HTML/PDF-Briefing aus Audit-Ordner

## Integration in Zielprojekte

Für Projekte, die regelmäßig rechts-relevante Änderungen durchmachen: installiere das Git-Pre-Commit-Hook-Template aus `templates/git-hooks/pre-commit.sh`. Details siehe `templates/git-hooks/README.md`. Der Hook warnt (oder blockt bei `LEGAL_AUDIT_STRICT=1`), wenn rechts-relevante Dateien ohne aktuellen Audit committet werden.

---

## Architektur

### Verzeichnisstruktur

```
legal-audit-de/
├── CLAUDE.md                           # diese Datei
├── plugin.json                         # Plugin-Manifest
├── README.md                           # Repo-README
├── LICENSE                             # MIT
├── .claude/
│   ├── settings.json                   # Hook-Registrierung, Permissions
│   ├── commands/{legal-audit,legal-audit-live,legal-doc-check,legal-kb,legal-verify,legal-update,legal-status}.md
│   ├── agents/{legal-auditor,legal-researcher,legal-text-writer}.md
│   ├── skills/{legal-audit-codebase,legal-kb-lookup,legal-verify-experts,legal-update-sources}/SKILL.md
│   └── hooks/
│       ├── session_start.py
│       ├── prompt_submit.py
│       ├── post_write.py
│       └── triggers.json               # Schlagwort-zu-KB-Mapping
├── knowledge/                          # KB-Vault, on-demand geladen
│   ├── INDEX.md                        # einzige immer-geladene Datei
│   ├── gesetze/                        # DSGVO, BDSG, TDDDG, UWG, BGB-AGB, DDG,
│   │                                   # DSA, DMA, AI-Act, BFSG, UrhG, MarkenG,
│   │                                   # NIS2-BSIG, PAngV
│   ├── themen/                         # Cookie-Consent, Tracking, DSE, Impressum,
│   │                                   # AGB, Widerruf, Button-Lösung, Newsletter,
│   │                                   # Drittland, AVV, VVT, TOM, DSFA,
│   │                                   # KI-Transparenz, BFSG, Werbekennzeichnung,
│   │                                   # Preisangaben, Stockfoto, KI-Content,
│   │                                   # Datenpanne-Meldepflicht, Social-Media,
│   │                                   # Fotos-Dritter-KUG, Siegel-Werbung,
│   │                                   # Zitatrecht, Tool-Katalog
│   ├── urteile/                        # EuGH + BGH + OLG Schlüsselurteile
│   ├── behoerden/                      # DSK, EDSA, BfDI, Landesbeauftragte
│   ├── checklisten/                    # Audit-Checklisten pro Codebase-Typ
│   └── anwaelte-tools/                 # Verifikations-Empfehlungen
├── audits/                             # Schatten-Archiv aller Audits (lokal, .gitignored)
├── templates/                          # LegalAudit-, Clean-, Disclaimer-Templates
└── scripts/                            # Python-Hilfsskripte
```

### Hook-Mechanik (Kern-Innovation)

Ziel: **Kontextfenster schlank halten, Rechtswissen trotzdem parat.**

- **SessionStart-Hook** (`session_start.py`) lädt nur `knowledge/INDEX.md` (Inhaltsverzeichnis, ~1.000 Tokens).
- **UserPromptSubmit-Hook** (`prompt_submit.py`) liest den User-Prompt, matcht gegen Regex-Patterns in `.claude/hooks/triggers.json` und lädt bis zu 3 passende KB-Chunks als `additionalContext`.
- **PostToolUse-Hook** (`post_write.py`, nach `Write`/`Edit`) validiert, dass jede in `docs/legal-audit/**` oder `knowledge/**` geschriebene Datei den Disclaimer-Block enthält; warnt bei fehlendem Disclaimer oder doppelten Finding-IDs.

Schlagwort-Beispiele: `cookie|consent` → `themen/cookie-consent.md`, `drittland|schrems` → `themen/drittland-transfer.md` + `urteile/eugh-schrems-ii.md`, `ai.act|ki.vo` → `themen/ki-transparenz.md` + `gesetze/ai-act.md`.

Der volle Trigger-Katalog steht in `.claude/hooks/triggers.json`.

---

## Audit-Output (im Zielprojekt)

```
<zielprojekt>/docs/legal-audit/
├── LegalAudit.md           # Findings mit Severity (CRIT/HIGH/MED/LOW)
├── SUMMARY.md              # Management-Kurzfassung
├── clean/                  # lupenreine Korrektur-Versionen pro Finding
│   └── F-NNN-<slug>.md
└── evidence/               # Screenshots, Code-Zitate, Quellen-Refs
```

Parallel wird eine Schatten-Kopie nach `${CLAUDE_PROJECT_DIR}/audits/<projekt>-<timestamp>/` abgelegt (Nachweis-Kette für DSGVO-Rechenschaftspflicht Art. 5 Abs. 2).

### Severity-Matrix

| Level | Kriterium |
|-------|-----------|
| CRIT | Aktuelle Abmahnwelle, Bußgeld > 10k möglich, strafrechtlich relevant |
| HIGH | Dokumentierte Abmahnfälle, Unterlassungsanspruch |
| MED | Formale Pflichtverletzung, Einzelanspruch möglich |
| LOW | Best-Practice-Verstoß |

Grundsatz: **Im Zweifel eine Stufe höher** klassifizieren — Abmahnkosten sind asymmetrisch.

---

## Agenten

Alle drei Custom-Agents laufen auf **Claude Opus 4.7 [1M]** (`claude-opus-4-7[1m]`). Begründung: Rechtsarbeit erfordert maximale Genauigkeit bei Zitaten, Paragraphen-Zuordnung und Formulierungen — ein falsches Aktenzeichen oder eine unsaubere AGB-Klausel kann abmahnbar werden. Das 1M-Kontextfenster erlaubt zudem, komplette Gesetzestexte + große Codebases gleichzeitig zu verarbeiten.

| Agent | Modell | Aufgabe |
|-------|--------|---------|
| `legal-auditor` | Opus 4.7 [1M] | Scannt Codebase, klassifiziert Findings nach Severity-Matrix |
| `legal-researcher` | Opus 4.7 [1M] | Recherchiert Primärquellen, verifiziert JEDES Zitat doppelt (Tier-1-Kaskade) |
| `legal-text-writer` | Opus 4.7 [1M] | Erstellt lupenreine Clean-Versionen inkl. Disclaimer-Injection |

---

## Quellen-Hierarchie (verbindlich für Zitat-Verifikation)

### Tier 1 — Primärquellen (nur diese zählen als Zitatbeleg)
1. `eur-lex.europa.eu` (EU-Primärrecht, CELEX, konsolidierte Fassungen)
2. `gesetze-im-internet.de` (DE-Gesetze, BMJ-offiziell)
3. `rechtsprechung-im-internet.de` (DE-Rechtsprechung)
4. `curia.europa.eu` (EuGH)
5. `bundesanzeiger.de` (Verordnungen)

### Tier 2 — Amtliche Sekundärquellen
- `bfdi.bund.de`, `datenschutzkonferenz-online.de`, `edpb.europa.eu`, Landesbeauftragte, `bsi.bund.de`

### Tier 3 — Fach-Einordnung (**nie** als Zitat-Grundlage)
- `dr-schwenke.de`, `haerting.de`, `datenschutz-notizen.de`, `e-recht24.de`, `it-recht-kanzlei.de`

Der `legal-researcher`-Agent verifiziert vor Publikation jedes Zitat gegen eine Tier-1-Quelle und schreibt ein Log unter `.claude/logs/zitate-verifikation-<YYYY-MM-DD>.log`.

---

## Codebase-Typ-Erkennung

| Marker | Typ | Checkliste |
|--------|-----|------------|
| `package.json` mit `next` | Next.js SaaS | `checklisten/audit-saas.md` |
| `package.json` mit `astro` / nur HTML | Landingpage | `checklisten/audit-landingpage.md` |
| `*.workflow.json` / n8n-Export | n8n | `checklisten/audit-n8n.md` |
| `woocommerce` / `shopify` / Stripe + Checkout | E-Commerce | `checklisten/audit-ecommerce.md` |
| vorwiegend `.md` + `content/` | Content/Blog | `checklisten/audit-content-blog.md` |
| unklar | generisch | `checklisten/general-pre-launch.md` |

---

## Arbeitsweise

- **Antworten auf Deutsch** (volle Orthographie inkl. Umlaute und ß).
- **Kommentare im Code Englisch** (Konvention), aber juristischer Content **ausschließlich Deutsch**.
- **Vor jeder destruktiven Aktion** (Delete, force-push, DB-Reset) explizite Bestätigung einholen.
- **Vor Implementierung** recherchieren: vorhandene Funktionen/Utilities wiederverwenden statt Neu-Erfinden.
- **Immutability**: bei jeder KB-Datei neue Version schreiben, nie stilles Mutieren.

---

## Wartung

- **KB-Aktualität:** alle 90 Tage `/legal-update --stale-only` ausführen.
- **Trigger-Katalog:** `.claude/hooks/triggers.json` erweitern, wenn häufige Prompts keine passenden KB-Chunks laden.
- **Checklisten-Evolution:** Nach jedem Audit prüfen, ob neue Muster in die Checklisten aufgenommen werden müssen.
- **Anwalts-/Tool-Liste:** Halbjährlich per `/legal-update anwaelte-tools` prüfen.
