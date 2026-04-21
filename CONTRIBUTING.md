# Contributing to legal-audit-de

Vielen Dank, dass du zur Weiterentwicklung dieses Plugins beitragen moechtest! Rechtsthemen aendern sich staendig, und jede Aktualisierung hilft der gesamten Community.

## Wichtiger Hinweis zu Rechts-Inhalten

**Keine Rechtsberatung.** Dieses Plugin erzeugt technische Vor-Arbeit fuer anwaltliche Pruefungen, keine verbindlichen Rechtsauskuenfte. Wenn du Beitraege einreichst:

- Alle Zitate gegen **Tier-1-Primaerquellen** pruefen (siehe `CLAUDE.md`, Abschnitt "Quellen-Hierarchie")
- Unsichere oder nicht verifizierbare Aussagen mit `<<VERIFIKATION AUSSTEHEND>>` markieren
- Sekundaerquellen (Kanzlei-Blogs, eRecht24 etc.) NIEMALS als Zitatbeleg — nur zur Einordnung

## Wie du beitragen kannst

### 🐛 Bug-Report / falsche Rechts-Information

Bitte ein [Issue](https://github.com/FutureRootsDE/legal-audit-de/issues/new) mit:

- Genauem Pfad zur betroffenen Datei
- Zitat der fraglichen Stelle
- Primaerquelle, die das Gegenteil belegt (mit Link)
- Gewuenschte Korrektur

### ✨ Neue KB-Artikel

Neue Artikel unter `knowledge/themen/` mit folgendem Frontmatter:

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
- Disclaimer-Block direkt nach dem Frontmatter (aus `templates/disclaimer-block.md`)
- Cross-Ref-Block am Ende (`## Siehe auch`) mit Wiki-Links
- Eintrag in `knowledge/INDEX.md`
- Trigger-Pattern in `.claude/hooks/triggers.json` (falls Auto-Loading gewuenscht)

### 🔄 KB-Aktualisierung

Wenn ein Gesetz/Urteil/Behoerden-Leitlinie sich geaendert hat:

1. Datei bearbeiten
2. `verifiziert-am:` im Frontmatter aktualisieren
3. `<<VERIFIKATION AUSSTEHEND>>`-Platzhalter entfernen, wenn nun verifiziert
4. PR mit Link zur Primaerquelle

### 🧰 Neue Commands / Agenten / Skills

Format wie bestehende Artefakte in `.claude/commands/`, `.claude/agents/`, `.claude/skills/`. Wichtig:
- Frontmatter korrekt (description, argument-hint, allowed-tools)
- Disclaimer-Referenz im Output-Path
- Beschreibung der Severity-Klassifikation

### 🌍 Uebersetzungen

Englische Kurzfassungen in `knowledge/en/SUMMARY.md` sind willkommen. Bitte beachten:
- Deutsch bleibt Primaersprache (Paragraphen-Formulierungen sind bindend)
- Englisch nur als Uebersicht, keine vollstaendige Uebertragung

## Entwicklungs-Setup

```bash
git clone https://github.com/FutureRootsDE/legal-audit-de.git
cd legal-audit-de

# Python-Dependencies fuer Hooks + Skripte
python -m venv .venv
source .venv/bin/activate   # oder .venv\Scripts\activate unter Windows
pip install -r requirements.txt  # falls vorhanden

# Hooks testbar?
python .claude/hooks/session_start.py
python .claude/hooks/prompt_submit.py <<< "test prompt about cookies"

# Scripts ausprobieren
python scripts/legal-status.py
python scripts/find-placeholders.py
```

## Commit-Message-Konvention

```
<typ>(<scope>): <kurze Beschreibung>

<body>

<footer>
```

Typen: `feat`, `fix`, `docs`, `kb`, `test`, `refactor`, `chore`

Scopes: `commands`, `agents`, `skills`, `hooks`, `knowledge`, `templates`, `scripts`

Beispiele:
- `feat(commands): add /legal-kb-preview to show KB file without loading`
- `kb(urteile): update BGH Cookie-Einwilligung II (I ZR 7/16) with 2025 follow-up`
- `fix(hooks): correct regex for ai-act trigger pattern`

## Pull-Request-Prozess

1. Fork das Repo + Branch (`feat/xyz`, `fix/xyz`, `kb/xyz`)
2. Aenderungen committen (siehe Commit-Konvention)
3. PR eroeffnen mit:
   - Beschreibung der Aenderung
   - Falls KB-Aenderung: Link zur Primaerquelle
   - Checkliste:
     - [ ] Disclaimer im Output-Path validiert
     - [ ] Zitate gegen Tier-1-Quellen geprueft
     - [ ] `aktualisiert:` / `verifiziert-am:` gepflegt
     - [ ] Cross-Refs aktualisiert
4. Review durch Maintainer
5. Merge

## Code of Conduct

Siehe [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — kurzform: sei freundlich, respektiere diverse Perspektiven, konstruktive Kritik willkommen, Diskriminierung / Belaestigung wird nicht toleriert.

## Lizenz

Alle Beitraege fallen unter die [MIT-License](LICENSE) des Projekts.

## Fragen?

[Issue eroeffnen](https://github.com/FutureRootsDE/legal-audit-de/issues/new) oder [Discussion starten](https://github.com/FutureRootsDE/legal-audit-de/discussions).
