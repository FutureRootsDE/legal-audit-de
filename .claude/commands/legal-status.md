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
    - Aktuell (< 90 Tage): 58 Dateien
    - Stale (> 90 Tage): 0 Dateien
    - Sehr Stale (> 180 Tage): 0 Dateien

Platzhalter (zu recherchieren):
  VERIFIKATION AUSSTEHEND: 18
  UNVERIFIZIERT: 12
  Betroffene Dateien: 11
  Empfehlung: /legal-update --fix-pending

Audit-Historie:
  Gesamt: N Audits
  Letztes Audit: <projekt> am <datum> (<severity-counts>)

Hook-Status:
  SessionStart: OK (INDEX.md laedt ~1076 Tokens)
  UserPromptSubmit: OK (22 Trigger-Patterns aktiv)
  PostToolUse: OK

Empfohlene Aktionen:
  - /legal-update --fix-pending  (30 Platzhalter aufloesen)
  - /legal-update --stale-only   (0 stale Dateien — aktuell nicht noetig)
```

## Follow-up

Nach dem Status-Report: schlage dem User konkrete naechste Schritte vor, basierend auf den Findings:
- Wenn Platzhalter > 10: `/legal-update --fix-pending` empfehlen
- Wenn Stale-Dateien > 0: `/legal-update --stale-only` empfehlen
- Wenn kein Audit > 30 Tage: routinemaessiger Re-Audit des letzten Projekts
- Wenn Hook-Probleme: auf Hook-Scripts in `.claude/hooks/` hinweisen
