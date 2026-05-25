---
name: legal-audit-codebase
description: Fuehrt einen systematischen Rechts-Audit einer Codebase durch (DE/EU-Scope). Nutze diese Skill wenn /legal-audit aufgerufen wird ODER wenn der User eine Codebase auf DSGVO/UWG/AGB/DDG/AI-Act/BFSG/UrhG/NIS2-Probleme untersuchen lassen will.
---
<!--
  AUTO-GENERATED — DO NOT EDIT DIRECTLY.
  Source: .claude/skills/legal-audit-codebase/SKILL.md
  Regenerate via: python3 scripts/sync-platforms.py --apply
-->
# Legal Audit einer Codebase

Diese Skill orchestriert den vollstaendigen Audit-Workflow, wenn Claude mit einer fremden Codebase konfrontiert wird.

## Wann nutzen

- Expliziter Aufruf: `/legal-audit <pfad>`
- User fragt: "Pruefe diese Codebase rechtlich", "Ist meine App DSGVO-konform?", "Legal-Check fuer \<projekt\>"
- Proaktiv nach grossen Refactorings in Auth-/Tracking-/Consent-Code

## Ablauf

```
1. Codebase-Typ klassifizieren (package.json / Dateistruktur)
2. Passende Checkliste aus knowledge/checklisten/ laden
3. Dispatch legal-auditor-Agent (haiku) — erstellt Finding-Liste
4. Pro Finding:
   a. Dispatch legal-text-writer-Agent (sonnet) → docs/legal-audit/clean/F-NNN-*.md
   b. Bei unklarer Rechtslage: Zwischenfrage an legal-researcher
5. Zitat-Verifikation via legal-researcher (Tier-1-Primaerquellen)
6. LegalAudit.md + SUMMARY.md zusammenstellen
7. Schatten-Kopie nach legal-audit-de/audits/<projektname>-<timestamp>/
8. Dem User: Top-3-CRIT/HIGH + Anwalts-/Tool-Empfehlung
```

## Checkliste-Auswahl

| Codebase-Typ | Checkliste |
|--------------|------------|
| Next.js/React SaaS | `checklisten/audit-saas.md` |
| Marketing-Landingpage | `checklisten/audit-landingpage.md` |
| n8n-Workflows | `checklisten/audit-n8n.md` |
| E-Commerce | `checklisten/audit-ecommerce.md` |
| Content/Blog | `checklisten/audit-content-blog.md` |
| Generisch/unklar | `checklisten/general-pre-launch.md` |

## Wichtige Regeln

- **Disclaimer-Pflicht:** Jede Output-Datei beginnt mit dem Block aus `templates/disclaimer-block.md`. Der `PostToolUse`-Hook validiert das.
- **Kein Halluzinieren:** Zitate, Aktenzeichen, Paragraphen werden vom `legal-researcher` verifiziert. Im Zweifel Zitat weglassen.
- **Scope-Grenze:** Strafrecht, Arbeitsrecht, Steuerrecht, nicht-EU-Jurisdiktionen werden im Audit-Report explizit als "nicht geprueft" ausgewiesen — nie implizit mit abfrtigen.
- **Severity im Zweifel nach oben:** Lieber CRIT als HIGH, der User kann runtergraden. Grund: Abmahnkosten sind asymmetrisch.

## Auto-Routing (Plattform-Fallback fuer Hookless-CLIs)

Diese Plattform (Codex/Copilot) hat keine SessionStart-/UserPromptSubmit-Hooks. Das Skill uebernimmt das KB-Routing daher selbst:

1. **Lies `knowledge/INDEX.md`** zu Beginn jeder Session, falls noch nicht geladen.
2. **Matche Task-Schlagwoerter** (cookie, drittland, ai-act, newsletter, barrierefreiheit, ...) gegen die KB-Kategorien aus dem INDEX.
3. **Lies bis zu 3 passende Chunks** via Read/view aus `knowledge/themen/`, `knowledge/urteile/`, `knowledge/gesetze/`, `knowledge/checklisten/`.
4. **Merke geladene Slugs**, um Doppel-Reads zu vermeiden.

Triggers: siehe `.claude/hooks/triggers.json` (gleiche Schlagwort-Map gilt fuer Codex/Copilot).

## Pro-Mode-Erkennung (Hookless-CLI-Fallback)

Da Codex und Copilot keinen SessionStart-Hook haben, der den Pro-Mode-Marker liest,
muss das Skill den Marker vor dem Dispatch eines `legal-*`-Subagents selbst pruefen:

1. **Pruefe** in dieser Reihenfolge auf `enabled: true`:
   - `~/.codex/legal-audit-de-pro-mode.json` (auf Codex)
   - `~/.copilot/legal-audit-de-pro-mode.json` (auf Copilot)
   - Fallback `~/.claude/legal-audit-de-pro-mode.json`
2. **Wenn aktiv,** dispatche die `-pro`-Variante:
   - `legal-auditor-pro`     statt `legal-auditor`
   - `legal-researcher-pro`  statt `legal-researcher`
   - `legal-text-writer-pro` statt `legal-text-writer`
3. **Sonst** dispatche die Default-1M-Variante.

Aktivieren via: `python3 scripts/legal-audit-pro-mode.py enable`.
