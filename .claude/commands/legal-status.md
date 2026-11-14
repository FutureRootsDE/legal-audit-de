---
description: Zeigt den Gesundheits-Status des legal-audit-de-Workspaces (KB-Alter, Platzhalter, Audit-Historie, Hook-Config).
argument-hint: [--verbose | --json]
allowed-tools: Bash, Read, Glob, Grep
---

# /legal-status

Diagnose des gesamten Workspace-Zustands. Nutze diesen Command:
- Regelmaessig (alle 4 Wochen) fuer routinemaessige Wartung
- Nach groesseren Audit-Runs, um zu sehen, was aktualisiert werden sollte
- Beim Onboarding einer neuen Session, um zu wissen wo man steht

## Ablauf

1. **Rufe das Status-Script auf:**
   ```bash
   python "${CLAUDE_PROJECT_DIR}/scripts/legal-status.py"
   ```

2. **Bei `--verbose`:** Zusaetzlich pro-Datei-Details anzeigen (alle Stale-Dateien, alle Platzhalter-Zeilen).

3. **Bei `--json`:** Nur JSON-Output (fuer Weiterverarbeitung in Skripten).

## Output-Struktur

```
=== legal-audit-de Status ===

Knowledge Base:
  Gesamt: 58 Dateien
  Kategorien: 14 Gesetze, 20 Themen, 6 Urteile, 4 Behoerden, 6 Checklisten, 7 Anwaelte-Tools, 1 INDEX
  Aktualitaet:
    (Alter der Verifikation: verifiziert-am, ersatzweise aktualisiert)
    - Aktuell (< 90 Tage): 57 Dateien
    - Stale (90 bis 180 Tage): 0 Dateien
    - Sehr Stale (> 180 Tage): 0 Dateien
    - Teilverifiziert: 1 Datei (teilverifiziert-am, zaehlt nie als frisch)
    - Ohne Frontmatter: 0 Dateien

Platzhalter (zu recherchieren):
  VERIFIKATION AUSSTEHEND: 18
  UNVERIFIZIERT: 12
  Betroffene Dateien: 11
  WARNUNG (nur bei Treffern): abweichende Platzhalter-Formen, z.B. Zusatztext, einfaches ">" oder ueber zwei Zeilen
  Empfehlung: /legal-update --fix-pending

Audit-Historie:
  Gesamt: N Audits
  Letztes Audit: <projekt> am <datum> (<severity-counts>)

Hook-Status:
  SessionStart: OK (INDEX.md laedt ~1076 Tokens)
  UserPromptSubmit: OK (22 Trigger-Patterns aktiv)
  PostToolUse: OK

Pro-Mode:
  Status:           deaktiviert | AKTIV
  Marker:           ${CLAUDE_PLUGIN_DATA}/pro-mode.json  (wenn aktiv)
  Agent-Varianten:  3/3 (OK)

Empfohlene Aktionen:
  - /legal-update --fix-pending  (30 Platzhalter aufloesen)
  - /legal-update --stale-only   (0 stale Dateien — aktuell nicht noetig)
```

## Follow-up

Nach dem Status-Report: schlage dem User konkrete naechste Schritte vor, basierend auf den Findings:
- Wenn Platzhalter > 10: `/legal-update --fix-pending` empfehlen
- Wenn Stale-Dateien > 0 (`verifiziert-am` 90 Tage oder aelter, ersatzweise `aktualisiert`): `/legal-update --stale-only` empfehlen
- Wenn teilverifizierte Dateien > 0: `/legal-update <slug>` fuer die vollstaendige Verifikation empfehlen (`--stale-only` erfasst sie nicht)
- Wenn abweichende Platzhalter-Formen gemeldet werden: `python scripts/find-placeholders.py` zeigt Datei und Zeile
- Wenn kein Audit > 30 Tage: routinemaessiger Re-Audit des letzten Projekts
- Wenn Hook-Probleme: auf Hook-Scripts in `.claude/hooks/` hinweisen
- Wenn `pro_mode.variants_complete: false`: `python3 scripts/sync-pro-variants.py --apply` empfehlen
- Wenn Pro-Mode aktiv aber `legal-status` zeigt ungewollte Modell-Fehler: `python3 scripts/legal-audit-pro-mode.py disable` zur Rueckkehr in 1M-Default
