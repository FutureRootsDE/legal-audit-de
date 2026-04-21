# legal-audit-de v1.1.0 — Plugin Marketplace + Self-Update

Zweites Release. Bringt das Plugin in die offizielle Claude-Code-Plugin-Struktur und ergänzt einen kombinierten Update-Befehl.

## ⚠️ Breaking Change: Installation

Die Installation läuft ab jetzt über den Marketplace:

**Alt (v1.0.0):**
```
/plugin install FutureRootsDE/legal-audit-de
```

**Neu (v1.1.0+):**
```
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

Wer v1.0.0 bereits installiert hat, kann so migrieren:

```
/plugin uninstall legal-audit-de
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

## Was ist neu

### 🏪 Offizielle Marketplace-Struktur

Das Repo ist ab sofort gleichzeitig ein **Plugin-Marketplace** namens `futureroots-legal`. Das heißt:

- Installation über den Standard-Claude-Code-Plugin-Flow
- Automatische Versions-Prüfung und Update-Benachrichtigung
- `plugin.json` liegt jetzt in `.claude-plugin/plugin.json` (Spec-konform)
- `marketplace.json` definiert den Marketplace
- Validiert mit `claude plugin validate .` ✅

### 🔄 `/legal-audit-de-update` — Alles-in-Einem-Update

Neuer Slash-Command, der in einem Rutsch:

1. Das Plugin selbst aktualisiert (Marketplace-Refresh)
2. Die Knowledge-Base gegen Primärquellen verifiziert (KB-Refresh)
3. Einen Diff-Report ausgibt

Flags:
- `/legal-audit-de-update` — beides
- `/legal-audit-de-update --plugin-only` — nur Plugin
- `/legal-audit-de-update --kb-only` — nur KB
- `/legal-audit-de-update --dry-run` — Vorschau ohne Änderungen

### 🧰 Cross-Platform Hooks

Die Hooks wurden von Bash (`*.sh`) auf Python (`*.py`) umgestellt. Damit funktionieren sie auch unter Windows ohne Git Bash oder WSL. Die Hook-Registrierung liegt jetzt in `plugin.json` statt `.claude/settings.json` — folgt der Claude-Code-Plugin-Spec und nutzt `${CLAUDE_PLUGIN_ROOT}` statt `${CLAUDE_PROJECT_DIR}`.

## Bugfixes / Fixes aus v1.0.0

- **Volle deutsche Orthographie**: ä, ö, ü, ß durchgehend in allen Dokumenten (statt ae, oe, ue, ss)
- **Englische README** (`README.en.md`) + englisches **Wiki** (12 Seiten) für internationale Nutzer in Deutschland
- **LICENSE**: deutscher Disclaimer-Block mit korrekten Umlauten

## Technische Details

### Dateistruktur

```
legal-audit-de/
├── .claude-plugin/
│   ├── plugin.json       # Plugin-Manifest (NEU: eigene Location)
│   └── marketplace.json  # Marketplace-Catalog (NEU)
├── .claude/
│   ├── commands/         # 8 Slash-Commands (NEU: /legal-audit-de-update)
│   ├── agents/           # 3 Custom-Agents (unverändert)
│   ├── skills/           # 4 Skills (unverändert)
│   ├── hooks/            # 3 Python-Hooks + 3 Shell-Hooks (Legacy)
│   └── settings.json     # nur Permissions (Hooks raus)
├── knowledge/            # 63 KB-Dateien (unverändert)
├── templates/            # 7 Templates (unverändert)
├── scripts/              # 4 Python-Skripte (unverändert)
├── README.md             # DE mit Umlauten
├── README.en.md          # EN für internationale Nutzer
├── CLAUDE.md             # DE mit Umlauten
├── CONTRIBUTING.md       # DE + CONTRIBUTING.en.md
├── LICENSE               # MIT + bilingual Disclaimer
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── .github/              # Issue + PR Templates
```

### Marketplace-Metadaten

```json
{
  "name": "futureroots-legal",
  "owner": { "name": "FutureRoots DE" },
  "plugins": [
    {
      "name": "legal-audit-de",
      "source": "./",
      "version": "1.1.0",
      "license": "MIT",
      "category": "compliance"
    }
  ]
}
```

Installation per Claude-Code-CLI:
```
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de@futureroots-legal
```

## Migration-Pfad für Plugin-Entwickler

Falls du dieses Plugin selbst geforkt / angepasst hast:

1. `plugin.json` von Root nach `.claude-plugin/plugin.json` verschieben
2. Hooks in `plugin.json` mit `${CLAUDE_PLUGIN_ROOT}` (statt `${CLAUDE_PROJECT_DIR}`) registrieren
3. `.claude/settings.json`: Hooks-Section entfernen, Permissions behalten
4. Optional: eigenen `marketplace.json` erstellen, falls du eigene Plugins anbieten willst

## Disclaimer

Wie immer: **Dieses Plugin ist keine Rechtsberatung** im Sinne des § 2 RDG. Alle Ausgaben dienen der technischen Vorbereitung einer anwaltlichen Prüfung. Eine abschließende Prüfung durch einen zugelassenen Rechtsanwalt ist zwingend erforderlich.

## Links

- [GitHub Issues](https://github.com/FutureRootsDE/legal-audit-de/issues)
- [Discussions](https://github.com/FutureRootsDE/legal-audit-de/discussions)
- [Wiki](https://github.com/FutureRootsDE/legal-audit-de/wiki)
- [Marketplace-Doku](https://code.claude.com/docs/en/plugin-marketplaces)
