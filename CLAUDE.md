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
| `/legal-client-test <url>` | Website-CheckUp für Agenturen: passive Prüfung (Consent, Drittanbieter, Sicherheit, Barrierefreiheit, Pflichtangaben) und Report als HTML plus getaggtes PDF mit eigenem Briefkopf; Prüfkatalog v1 mit 56 Tests, Skript `scripts/client-test.py`, ohne Rechtsberatung |
| `/legal-doc-check <datei>` | Einzel-Dokument-Prüfung (AGB / DSE / Impressum / Widerruf / Cookie-Richtlinie / Social-Bio) ohne Codebase-Kontext |
| `/legal-kb <slug>` | KB-Artikel gezielt in den Kontext laden |
| `/legal-verify <thema>` | Fachanwalts-/Tool-Empfehlungen |
| `/legal-update [slug\|--stale-only\|--all\|--fix-pending]` | KB gegen Primärquellen aktualisieren |
| `/legal-audit-de-update [--plugin-only\|--kb-only\|--dry-run]` | Plugin + KB gemeinsam aktualisieren (Marketplace-Refresh + Primärquellen) |
| `/legal-status [--verbose\|--json]` | Plugin-Gesundheit: KB-Alter, Platzhalter, Hook-Status, Audit-Historie, Pro-Mode-Status |
| `/legal-pro-mode enable\|disable\|status` | Pro-Mode-Toggle (Standard-Kontext statt 1M) für Claude-Pro-Abonnenten |

Details in `.claude/commands/*.md`. Hilfs-Skripte unter `scripts/` (u. a. `client-test.py` mit den Unterbefehlen check, profile, init, plan, render, pdf für `/legal-client-test`, nur Standardbibliothek; Bibliothek `scripts/client_report/`). Bekannte Einschränkung: Copilot bildet `${CLAUDE_PLUGIN_ROOT}` auf `${GITHUB_WORKSPACE}` ab, `/legal-client-test` läuft dort nur, wenn das Plugin-Repo selbst der Workspace ist:
- `legal-status.py` (`--verbose`, `--json`): Status-Report; Frische nach `verifiziert-am` (ersatzweise `aktualisiert`, auch bei ungueltigem `verifiziert-am`), ungueltiges oder zukuenftiges Datum als eigener Zustand "ungueltiges Datum", `teilverifiziert-am` als eigener Zustand "teilverifiziert" (nie frisch), Warnung bei abweichenden Platzhalter-Formen
- `audit-compare.py` — Diff zwischen zwei Audits (`--auto <pfad>` findet vorheriges)
- `find-placeholders.py` (`--json`, `--group-by-file`): listet alle `<<VERIFIKATION AUSSTEHEND>>`/`<<UNVERIFIZIERT>>`-Stellen; abweichende oder defekte Marker (Zusatztext, einfaches `>`, ueber zwei Zeilen, nicht geschlossen) erscheinen als WARNUNG auf stderr, Marker in Backticks werden ignoriert
- `legal-audit-pdf.py` — bundled HTML/PDF-Briefing aus Audit-Ordner
- `legal-audit-pro-mode.py`: Pro-Mode-Marker setzen, löschen, abfragen (Quelle für `/legal-pro-mode`)
- `sync-pro-variants.py`: `-pro`-Agentenvarianten aus den 1M-Varianten erzeugen (`--apply`, `--check`)
- `sync-platforms.py`: Codex- und Copilot-Adapter aus `.claude/` erzeugen (`--apply`, `--check`)
- `placeholder_check.py`: gemeinsames Modul für die Platzhalter-Erkennung (von `find-placeholders.py` und `legal-status.py` genutzt)
- `verify-citations.py`: prueft Bundesgerichts-Aktenzeichen der KB gegen die Rechtsinformations-API des Bundes (optional; `--path`, `--only-pending`, `--json`, `--offline`, `--today`, `--strict` (Exit 1 bei DATE_MISMATCH), `--timeout`, `--rate`, `--eu-rate`, `--norm-rate`, `--no-cache`, `--cache-dir`, `--cache-ttl-days` (Standard 7), `--write-ecli --dry-run`); duenner Einstiegspunkt, Logik im Paket `citation_check/` daneben (nur Standardbibliothek); Cache-Treffer sind im Bericht und JSON gekennzeichnet (`source: cache`) und gelten als ungeprueft; Exit 3 bei Schreibfehlern von `--write-ecli`; bekannte Grenzen: Datumsbindung nur bei klarem Bezug (Daten nach Vermerkwoertern wie Stand/geprueft/eingelegt und Daten ab dem Lauftag (`--today`, Standard heute) sind keine Entscheidungsdaten, ein Datum in einer Klammer hinter einem Aktenzeichen gehoert nie zum nachfolgenden, im Zweifel kein Datum), Kurzform-Aufzaehlungen wie `I ZR 90/20, 125/20 und 126/20` werden aufgeloest (Folgeglieder `NNN/JJ` direkt per Komma, und oder sowie angeschlossen; ein Datum vor oder nach der Liste gilt fuer alle Glieder), BVerwG-Aktenzeichen ohne Gerichtsnamen in der Zeile werden nur in `knowledge/urteile/` erkannt, wenn Gericht-Zeile, Frontmatter, Dateiname oder Ueberschrift das BVerwG nennen, die Zeile kein Vorinstanz-Signal (Vorinstanz, vorgehend, LG, OLG, VG, EuGH usw.) enthaelt und das Registerzeichen zum BVerwG passt (sonst NOT_COVERED); Netzwerkfehler erscheinen nur als feste Kategorie ohne Text aus der Ausnahme. EU-Rechtsprechung (EuGH/EuG) wird standardmaessig gegen den Cellar des Amts fuer Veroeffentlichungen der EU geprueft (SPARQL, hoechstens 1 Anfrage pro Sekunde, eine Zeitueberschreitung wird nicht wiederholt, `--no-eu` schaltet ab; zusaetzlicher Status `PENDING` fuer anhaengige Verfahren oder nur Schlussantraege; Beschluesse im vorlaeufigen Rechtsschutz zaehlen nur fuer Aktenzeichen mit Suffix R, `name_hint` als reiner Hinweis); `--check-norms` ist ein eigener Modus und prueft Normzitate gegen gesetze-im-internet.de (Paragraph, Ueberschrift, Absatz, Stand) sowie BGBl.-Fundstellen gegen recht.bund.de (`--max-bgbl N`, Standard 0, 30 Sekunden Abstand laut robots.txt); je Zitat weisen `checked`/`unchecked` (JSON) bzw. `[nicht geprueft: ...]` (Text) aus, welche Teile verglichen wurden: Grenzen sind, dass Nr. und lit. (sowie Halbsatz, Alternative) nie geprueft werden, Saetze nur bei eindeutiger Zuordnung zur Absatzmarke (auch eingeschobene Absaetze wie (1a)) und Absaetze mit Buchstaben nur gegen vorhandene Absatzmarken; Gesetzesdaten aus dem Cache stehen im Bericht als "Quelle: Cache (ungeprueft)"; `--strict` liefert hier Exit 1 bei NORM_MISSING, ABSATZ_MISSING oder BGBL_MISSING, `--timeout` gilt fuer beide Backends; beide Backends schreiben nie in die KB (ausser `--write-ecli`, das jetzt auch EU-ECLI eintraegt).

## Integration in Zielprojekte

Für Projekte, die regelmäßig rechts-relevante Änderungen durchmachen: installiere das Git-Pre-Commit-Hook-Template aus `templates/git-hooks/pre-commit.sh`. Details siehe `templates/git-hooks/README.md`. Der Hook warnt (oder blockt bei `LEGAL_AUDIT_STRICT=1`), wenn rechts-relevante Dateien ohne aktuellen Audit committet werden.

---

## Architektur

### Verzeichnisstruktur

```
legal-audit-de/
├── CLAUDE.md                           # diese Datei
├── AGENTS.md                           # Einstieg für Codex und andere Agent-CLIs
├── README.md / README.en.md            # Repo-README (DE / EN)
├── CHANGELOG.md, CONTRIBUTING.md       # Änderungshistorie, Mitwirkung
├── LICENSE                             # MIT
├── .claude-plugin/
│   ├── plugin.json                     # Plugin-Manifest inkl. Hook-Registrierung
│   └── marketplace.json                # Marketplace-Metadaten
├── .claude/
│   ├── settings.json                   # Permissions
│   ├── commands/{legal-audit,legal-audit-live,legal-client-test,legal-doc-check,legal-kb,legal-verify,legal-update,legal-audit-de-update,legal-status,legal-pro-mode}.md
│   ├── agents/{legal-auditor,legal-researcher,legal-text-writer}.md   # plus je eine -pro-Variante
│   ├── skills/{legal-audit-codebase,legal-kb-lookup,legal-verify-experts,legal-update-sources}/SKILL.md
│   └── hooks/
│       ├── session_start.py
│       ├── prompt_submit.py
│       ├── post_write.py
│       ├── *.sh                        # Shell-Wrapper je Hook
│       └── triggers.json               # Schlagwort-zu-KB-Mapping (35 Muster)
├── .codex/, .codex-plugin/, .agents/   # generiert von scripts/sync-platforms.py (Codex)
├── .github/                            # Copilot-Adapter (generiert), workflows/ (validate.yml, release.yml), Issue-Templates
├── knowledge/                          # KB-Vault, on-demand geladen: 65 Dateien plus INDEX.md (gesetze 14, themen 25, urteile 9, behoerden 4, checklisten 6, anwaelte-tools 7)
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
│   ├── urteile/                        # EuGH, EuG, BGH und LG Schlüsselurteile
│   ├── behoerden/                      # DSK, EDSA, BfDI, Landesbeauftragte
│   ├── checklisten/                    # Audit-Checklisten pro Codebase-Typ
│   └── anwaelte-tools/                 # Verifikations-Empfehlungen
├── audits/                             # Schatten-Archiv aller Audits (lokal, .gitignored)
├── templates/                          # LegalAudit-, Clean-, Disclaimer-Templates, git-hooks/, mcp/, client-test/ (Katalog, HTML-Vorlage, CSS, IBM Plex OFL-1.1)
├── docs/                               # Doku-Site (GitHub Pages)
├── tests/                              # Offline-Unit-Tests (`python -m unittest discover -s tests`)
└── scripts/                            # Python-Hilfsskripte, Pakete citation_check/ und client_report/, Einstieg client-test.py
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

Im Default laufen alle drei Custom-Agents auf **Claude Opus 4.7 [1M]** (`claude-opus-4-7[1m]`). Begründung: Rechtsarbeit erfordert maximale Genauigkeit bei Zitaten, Paragraphen-Zuordnung und Formulierungen — ein falsches Aktenzeichen oder eine unsaubere AGB-Klausel kann abmahnbar werden. Das 1M-Kontextfenster erlaubt zudem, komplette Gesetzestexte + große Codebases gleichzeitig zu verarbeiten.

| Agent | Default-Modell | Pro-Mode-Variante | Aufgabe |
|-------|----------------|-------------------|---------|
| `legal-auditor` | Opus 4.7 [1M] | `legal-auditor-pro` (Opus 4.7, Standard-Kontext) | Scannt Codebase, klassifiziert Findings nach Severity-Matrix |
| `legal-researcher` | Opus 4.7 [1M] | `legal-researcher-pro` | Recherchiert Primärquellen, verifiziert JEDES Zitat doppelt (Tier-1-Kaskade) |
| `legal-text-writer` | Opus 4.7 [1M] | `legal-text-writer-pro` | Erstellt lupenreine Clean-Versionen inkl. Disclaimer-Injection |

### Pro-Mode (Standard-Kontext statt 1M)

Claude-Pro-Abonnenten (20 USD/mo) haben **keinen Zugriff** auf 1M-Kontext — der erste 1M-Agent-Dispatch endet mit `1M context requires usage credits or Max plan`. Das Plugin liefert deshalb drei `-pro`-Varianten der Agents mit `model: claude-opus-4-7` (200 K Standard-Kontext); die Commands dispatchen sie automatisch, wenn der Pro-Mode-Marker aktiv ist.

**Aktivieren:**
```bash
python3 scripts/legal-audit-pro-mode.py enable
# oder im Plugin:
/legal-pro-mode enable
```

**Marker-Ort:** `${CLAUDE_PLUGIN_DATA}/pro-mode.json` — per [Anthropic-Doku](https://code.claude.com/docs/en/plugins-reference) explizit als "persistent directory for plugin state that survives updates" dokumentiert. Der Marker überlebt `/plugin install` und Marketplace-Refresh.

**Wie es funktioniert:**
1. Der `SessionStart`-Hook liest den Marker und injiziert bei aktivem Pro-Mode einen System-Reminder, der den Orchestrator anweist, die `-pro`-Varianten zu dispatchen.
2. Jedes Command-Markdown (`/legal-audit`, `/legal-doc-check`, `/legal-update`, `/legal-audit-de-update`) enthält eine "Pro-Mode-Awareness"-Sektion und eine Agent-Marker-Tabelle.
3. Auf Codex/Copilot (kein SessionStart-Hook) prüft das Skill den Marker selbst via Auto-Routing-Block.

**Wartung:** Die `-pro`-Varianten werden via `python3 scripts/sync-pro-variants.py --apply` deterministisch aus den 1M-Varianten generiert. CI prüft Drift im `validate.yml`.

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

### Optional: MCP-Beschleunigung via `rechtsinformationen-bund-de-mcp`

Wer den MCP-Server [`wolfgangihloff/rechtsinformationen-bund-de-mcp`](https://github.com/wolfgangihloff/rechtsinformationen-bund-de-mcp) lokal installiert und in `.mcp.json` (Projekt) oder `~/.claude.json` (User) registriert, bekommt strukturierten ELI/ECLI-Zugriff auf das offizielle Bundesportal `rechtsinformationen.bund.de` statt HTML-Scraping. Der `legal-researcher`-Agent erkennt den Server am Tool-Praefix `mcp__rechtsinformationen__*` und nutzt ihn dann bevorzugt; ohne den Server laeuft der WebFetch-Fallback unveraendert weiter. Setup-Anleitung: `templates/mcp/README.md`. Plugin-Root bleibt MCP-frei, damit der Default-Install ohne Node.js/Build-Schritt funktioniert.

### Optional: direkte Abfrage der Rechtsinformations-API des Bundes

Fuer Aktenzeichen der sieben Bundesgerichte (BGH, BFH, BVerwG, BPatG, BAG, BSG, BVerfG) kann der `legal-researcher` die offene API `https://testphase.rechtsinformationen.bund.de/v1` direkt abfragen, ohne MCP-Server und ohne Key; `python scripts/verify-citations.py` macht das als Sammelpruefung. Grenzen: Die API ist eine **Testphase** ohne Stabilitaetszusage und ohne dokumentierte Datenlizenz, BGH ist erst ab etwa 2010 enthalten, Landesgerichte, EU-Gerichte und viele Gesetze (BGB, UWG, EGBGB) fehlen. Ein Treffer (ECLI, Datum) zaehlt als Primaerbeleg; **kein Treffer ist nie ein Gegenbeweis** und fuehrt zurueck auf die Tier-1-Kaskade. Es gibt keine harte Abhaengigkeit: bei Ausfall laeuft alles wie bisher.

### Optional: EU-Rechtsprechung im Cellar des Amts fuer Veroeffentlichungen

Fuer Aktenzeichen des EuGH und des EuG (`C-311/18`, `T-553/23`, auch mit Suffix `P`, `PPU`, `R` und als verbundene Rechtssachen) liefert der Cellar (SPARQL-Endpunkt `https://publications.europa.eu/webapi/rdf/sparql`, ohne Key) CELEX, ECLI, Datum und Dokumenttyp (Urteil, Beschluss, Schlussantraege, Gutachten, Mitteilung ueber die Einreichung). Empfohlener Zugangsweg statt EUR-Lex-HTML (die EUR-Lex-Seiten sind fuer automatische Clients nicht lesbar). `python scripts/verify-citations.py` fragt ihn standardmaessig ab (`--no-eu` schaltet ab). Grenzen: Fuer das Datum zaehlt das Urteil, ersatzweise der Beschluss; Schlussantraege sind nie das Entscheidungsdatum. Kein Dokument im Bestand (`NOT_IN_DATASET`) ist ausdruecklich kein Gegenbeweis (z. B. anhaengige Verfahren); `PENDING` heisst anhaengig oder nur Schlussantraege, ohne Entscheidung. `name_hint` (Kurzname der KB-Zeile gegen den amtlichen Titel) ist nur ein Hinweis und nie ein Verdikt. Hoefliche Nutzung: hoechstens 1 Anfrage pro Sekunde, eine Abfrage je Aktenzeichen, Cache 7 Tage; Quellenangabe bei Weiterverwendung: Amt fuer Veroeffentlichungen der Europaeischen Union (Cellar). Gelesene Bedingungen (Stand 2026-11-14): Rechtlicher Hinweis des Amts (CC BY 4.0 fuer redaktionelle Inhalte, Quellenangabe), Cellar-Dokumentation (SPARQL-Schnittstelle oeffentlich mit GET-Beispielen, Linked Open Data), robots.txt von op.europa.eu (`Allow: /`, nur Portal-Pfade gesperrt, nicht `/webapi/`); eine veroeffentlichte Mengenbegrenzung steht dort nicht.

### Optional: Normen und BGBl.-Fundstellen (`--check-norms`)

`python scripts/verify-citations.py --check-norms` extrahiert Normzitate (`§ 356a BGB`, `§ 5a Abs. 4 Satz 2 UWG`, `Art. 246a § 1 EGBGB`) und prueft je eindeutiger Norm gegen die XML-Gesamtausgabe von `https://www.gesetze-im-internet.de` (ein Abruf je Gesetz, gecacht): Paragraph vorhanden, amtliche Ueberschrift, Zahl der Absaetze, Satzzahl nur wenn zuverlaessig bestimmbar. Klassen `NORM_OK`, `NORM_MISSING`, `ABSATZ_MISSING`, `NORM_UNKNOWN_LAW`, `NORM_OLD_VERSION` (a. F.), `ERROR`; je Gesetz der Stand (Datum und BGBl.-Fundstelle der letzten Aenderung) und eine Hinweisliste "Gesetz nach `verifiziert-am` der zitierenden Datei geaendert". EU-Verordnungen (DSGVO, KI-VO usw.) werden nur gezaehlt. Grenzen: Der Inhalt einer Aussage zum Paragraphen bleibt Sache der Fachpruefung; MStV, Landesrecht und aufgehobene Gesetze (TMG) sind `NORM_UNKNOWN_LAW`; `Art. N § M` prueft Artikel und Paragraph nur bei Gesetzen, die so gegliedert sind (EGBGB). BGBl.-Fundstellen (`BGBl. 2026 I Nr. 322`) werden nur mit `--max-bgbl N` gegen `https://www.recht.bund.de/bgbl/1/<jahr>/<nr>/VO.html` geprueft: robots.txt wird bei jedem Lauf gelesen und eingehalten (Crawl-delay 30 Sekunden, laenger dauernde Laeufe zeigen den Fortschritt); nur Teil I ab 2023. Gelesene Bedingungen (Stand 2026-11-14): robots.txt von gesetze-im-internet.de (`Disallow:` leer, alles erlaubt) und die Hinweise der Seite (Abschnitt 6 bietet das XML und `gii-toc.xml` ausdruecklich fuer automatisierte Weiterverarbeitung an); robots.txt von recht.bund.de (`Disallow: /SiteGlobals/` und `/de/serviceseiten/`, `Crawl-delay: 30`, `/bgbl/` offen); die Nutzungsbedingungen von recht.bund.de liegen im fuer Bots gesperrten Pfad `/de/serviceseiten/` und wurden deshalb nicht abgerufen, darum ist die BGBl.-Pruefung standardmaessig aus.

KB-Frontmatter unterstuetzt seit dieser Integration die optionalen Felder `eli:` (ELI-URI fuer Gesetze) und `ecli:` (ECLI fuer Urteile). Beide sind nicht verpflichtend, aber bei Verfuegbarkeit stabiler als URLs allein.

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

- **KB-Aktualität:** alle 90 Tage `/legal-update --stale-only` ausführen (stale = `verifiziert-am` 90 Tage oder älter, ersatzweise `aktualisiert`).
- **Trigger-Katalog:** `.claude/hooks/triggers.json` erweitern, wenn häufige Prompts keine passenden KB-Chunks laden.
- **Checklisten-Evolution:** Nach jedem Audit prüfen, ob neue Muster in die Checklisten aufgenommen werden müssen.
- **Anwalts-/Tool-Liste:** Halbjährlich per `/legal-update anwaelte-tools` prüfen.
- **Release:** Nach dem Merge eines Release-PR läuft der Workflow `release.yml` (Auslöser: Tag `vX.Y.Z`) und baut Bundles sowie GitHub-Release selbst; Tag, GitHub-Release und Bundles nicht von Hand anlegen.
- **Verifikationsstand (Stand 2026-11-15):** `python scripts/legal-status.py --json` meldet 66 KB-Dateien (65 plus `INDEX.md`): 28 frisch, 37 teilverifiziert (`teilverifiziert-am`, nie frisch), 0 stale, 1 ohne Frontmatter; `python scripts/find-placeholders.py` zählt 52 offene Marker `<<VERIFIKATION AUSSTEHEND>>` in 37 Dateien, keinen `<<UNVERIFIZIERT>>`.
- **CI:** `validate.yml` mit den Jobs Platform-Adapter Sync-Check, Zitatprüfung Unit-Tests (`python -m unittest discover -s tests`, zuletzt 676 Tests, 8 übersprungen), Pro-Mode Agent-Variant Drift-Check, Pro-Mode Toggle Smoke-Test, Disclaimer-Validation, Platzhalter-Scan (informativ) und Markdown-Lint (relaxed).
