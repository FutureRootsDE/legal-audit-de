---
description: Aktualisiert das legal-audit-de Plugin selbst (neue Plugin-Version vom Marketplace ziehen) UND refreshed die KB gegen Primärquellen. All-in-One-Update.
argument-hint: [--plugin-only | --kb-only | --dry-run]
allowed-tools: Bash, Read, Write, WebFetch, Task
---

# /legal-audit-de-update

Kombinierter Update-Befehl, der zwei Dinge parallel erledigt:

1. **Plugin-Update** — holt die neueste Version von `legal-audit-de` aus dem Marketplace (neue Commands, Agents, Skills, Hooks, KB-Struktur)
2. **KB-Update** — aktualisiert die Wissensdatenbank gegen Primärquellen (Gesetze, Urteile, Behörden-Leitlinien)

Damit gehst du sicher, dass dein lokales Plugin sowohl funktional als auch inhaltlich auf dem aktuellen Stand ist.

## Wichtig

> Dieses Plugin ist **keine Rechtsberatung** im Sinne des § 2 RDG. Auch nach einem Update gilt: jede Ausgabe muss vor produktivem Einsatz durch einen zugelassenen Rechtsanwalt geprüft werden. Updates schließen nicht aus, dass neue Gesetzesänderungen oder Urteile noch nicht in die KB eingepflegt sind — prüfe `/legal-status --verbose` nach dem Update.

## Flags

### `/legal-audit-de-update` (Standard)
Führt beide Schritte in Reihenfolge aus: Plugin-Update zuerst, dann KB-Update.

### `/legal-audit-de-update --plugin-only`
Nur Plugin-Code aktualisieren (Commands, Agents, Hooks). KB bleibt unverändert.

### `/legal-audit-de-update --kb-only`
Nur Knowledge-Base-Dateien aktualisieren. Plugin-Code bleibt unverändert.

### `/legal-audit-de-update --dry-run`
Zeigt nur an, was aktualisiert würde, ohne tatsächlich etwas zu ändern. Hilfreich vor produktiven Systemen.

## Pflichtablauf

### Schritt 1 — Vor-Status festhalten

Aktueller Stand als Baseline für den Diff-Report:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/legal-status.py" --json > /tmp/legal-status-pre.json
```

### Schritt 2 — Plugin-Update (falls nicht `--kb-only`)

**Claude führt folgendes an den User zurück — Plugin-Updates müssen via Claude-Code-CLI laufen, nicht via Plugin-intern:**

```
/plugin marketplace update futureroots-legal
```

Dieser eingebaute Command refreshed das Marketplace-Clone lokal. Nach dem Refresh:

```
/plugin install legal-audit-de@futureroots-legal
```

reinstalliert das Plugin in die aktuelle Version (Claude Code erkennt die Version aus `plugin.json` und ersetzt den Cache nur bei Änderung).

**Alternative** falls das Plugin direkt über einen Git-Clone installiert wurde: manuelles `git pull` im Plugin-Verzeichnis. Siehe `CLAUDE.md` im Plugin-Root für den Pfad.

### Schritt 3 — KB-Update (falls nicht `--plugin-only`)

Dispatch den `legal-researcher`-Agent (Opus 4.7 [1M]) im "Stale-Only"-Modus:

- Agent prüft jede KB-Datei mit `verifiziert-am` > 90 Tage gegen Tier-1-Primärquellen
- Aktualisiert Frontmatter-Felder `aktualisiert:` und `verifiziert-am:`
- Markiert nicht verifizierbare Stellen mit `<<VERIFIKATION AUSSTEHEND>>`
- Schreibt ein Log nach `.claude/logs/kb-update-<timestamp>.log`

Äquivalent zu:

```
/legal-update --stale-only
```

Bei `--dry-run`: Agent läuft nur im Check-Modus, schreibt keine Änderungen.

### Schritt 4 — Post-Status und Diff

Nach beiden Updates:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/legal-status.py" --json > /tmp/legal-status-post.json
```

Diff-Report ausgeben:

- Plugin-Version alt vs. neu
- Anzahl KB-Dateien aktualisiert
- Neu eingeführte `<<VERIFIKATION AUSSTEHEND>>`-Stellen
- Geänderte Rechtsgrundlagen (wenn Agent Gesetzes-Updates erkannt hat, z. B. eine neue Verordnung)

## Output

```
=== legal-audit-de Update Report ===
Datum:        <YYYY-MM-DD HH:MM>
Plugin:       v1.0.0 → v1.0.1  (oder: bereits aktuell)
KB:           63 Dateien geprüft
              7 aktualisiert, 1 neue VERIFIKATION-AUSSTEHEND-Stelle
              5 Dateien älter als 180 Tage — empfohlen: manuelle Review

Wichtige Änderungen:
  • [HIGH] BGH-Urteil I ZR 186/17 hat Follow-Up vom 2026-03-15 — themen/email-marketing.md aktualisiert
  • [MED] Mistral AI DPA-URL geändert — themen/tool-katalog.md aktualisiert
  • [LOW] Neue DSK-Orientierungshilfe zu KI-Chatbots (2026-02-10) — zu integrieren (siehe pending)

Nächste Schritte:
  1. Review der 5 alten Dateien: `/legal-kb <slug>` + manuelle Verifikation
  2. Pending-Stellen auflösen: `/legal-update --fix-pending`
  3. Nach wesentlichen Rechts-Änderungen: bestehende Audits mit `/legal-audit <pfad> --compare` neu prüfen
```

## Nach Abschluss

- Das Update-Log liegt unter `.claude/logs/plugin-update-<timestamp>.log`
- Bestehende Audit-Outputs in `docs/legal-audit/` sind **nicht** automatisch aktualisiert. Bei wesentlichen Rechts-Änderungen bitte `/legal-audit <projekt> --compare` ausführen, um einen Diff-Report zu erhalten.
- Bei kritischen Updates (z. B. neues BGH-Urteil mit Unterlassungs-Implikation): aktive Kunden-Projekte prüfen.

## Haftungsausschluss

Das automatische Plugin- und KB-Update ersetzt **nicht** die manuelle Prüfung wichtiger Rechts-Änderungen durch einen Fachanwalt. Die KB wird bestmöglich aktualisiert, aber:

- Neue Gesetze werden erst nach Aufnahme in die KB wirksam
- Nicht verifizierbare Änderungen bleiben als Platzhalter und müssen manuell aufgelöst werden
- Die Primärquellen-Verfügbarkeit ist nicht garantiert (Server-Ausfälle, Struktur-Änderungen)

**Bei Zweifel: /legal-verify zu Fachanwalt + manuelle Pflege.**

## Siehe auch

- `/legal-status [--verbose]` — Plugin-Gesundheit prüfen vor/nach Update
- `/legal-update [slug|--stale-only|--all|--fix-pending]` — granulares KB-Update
- `/plugin marketplace update futureroots-legal` — reiner Marketplace-Refresh
