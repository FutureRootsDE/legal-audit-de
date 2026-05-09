<!--
  AUTO-GENERATED — DO NOT EDIT DIRECTLY.
  Source: .claude/skills/legal-verify-experts/SKILL.md
  Regenerate via: python3 scripts/sync-platforms.py --apply
-->
---
name: legal-verify-experts
description: Liefert Empfehlungen fuer Fachanwaelte, Kanzleien und Verifizierungs-Tools zu einem Rechtsthema. Nutze diese Skill wenn /legal-verify aufgerufen wird ODER wenn der User nach einem "Anwalt fuer ...", "Kanzlei fuer ...", "Tool zur Pruefung von ..." fragt.
---
# Legal Verify — Expert & Tool Recommendations

Gibt strukturierte Empfehlungen fuer die menschliche / Tool-basierte Verifikation KI-erstellter Rechts-Analysen.

## Wann nutzen

- Expliziter Aufruf: `/legal-verify <thema>`
- Am Ende jedes `/legal-audit` fuer CRIT- und HIGH-Findings
- Wenn der User fragt: "Wen sollte ich fragen?", "Welches Tool pruefen das?"

## Output-Struktur

```markdown
## Empfehlung fuer "<thema>"

### Ideale Qualifikation
- Fachanwalt fuer IT-Recht + <Zusatzqualifikation, z.B. zertifizierter DSB>

### Budget-Ranges (Stand <datum>)
- Spezialisierte B2B-SaaS-Boutique: 500–1.500 EUR (2-4h Review)
- Wirtschaftskanzlei mit IT-Dept: 1.500–3.500 EUR
- Online-Plattform (advocado, anwalt.de): 300–500 EUR (Qualitaet variiert)
- Generalistenkanzlei: NICHT empfohlen

### Konkrete Kanzleien / Anwaelte (Stand <datum>)
<aus knowledge/anwaelte-tools/kanzleien-saas-spezialisiert.md>

### Selbst-Check-Tools (vor Anwalts-Termin)
<aus knowledge/anwaelte-tools/tools-*.md, thematisch passend>

### Typischer Ablauf
1. Pre-Audit mit Selbst-Check-Tool → Befund dokumentieren
2. LegalAudit.md + relevante Clean-Versionen an Kanzlei
3. Anwalts-Termin (physisch/video, 2-4h)
4. Iterations-Runde (1-2 Wochen)
5. Freigabe-Dokument von der Kanzlei einfordern (wichtig fuer Rechenschaftspflicht)
```

## Matching-Regeln

| Thema | Fachanwaltstitel | Zusatzquali |
|-------|------------------|-------------|
| DSGVO/AVV/TOM/DSFA | IT-Recht | Zertif. DSB (udis/BvD/TUEV) |
| AGB/Widerruf/Fernabsatz | IT-Recht oder Vertragsrecht | — |
| UWG/Werbung/Abmahnung | Gewerblicher Rechtsschutz | — |
| Urheber/Marken | Urheber- und Medienrecht | — |
| AI Act / KI-Transparenz | IT-Recht | KI-Compliance-Zertifikat |
| BFSG | IT-Recht | A11y-Koordinator |
| NIS2/KRITIS | IT-Recht | BSI-lizenzierter Auditor |
| Impressum (§ 5 DDG) / DDG | IT-Recht | — |

## Disclaimer

Am Ende jeder Empfehlung:
> Die genannten Kanzleien/Anwaelte sind **keine Mandats-Vermittlung**, sondern illustrative Beispiele aus oeffentlich zugaenglichen Quellen. Konkrete Mandatsverhaeltnisse schliesst der Nutzer selbst. Keine Haftung fuer Aktualitaet oder Qualitaet.

## Update-Frequenz

Kanzlei-Empfehlungen sollten halbjaehrlich per `/legal-update anwaelte-tools` geprueft werden.

## Auto-Routing (Plattform-Fallback fuer Hookless-CLIs)

Diese Plattform (Codex/Copilot) hat keine SessionStart-/UserPromptSubmit-Hooks. Das Skill uebernimmt das KB-Routing daher selbst:

1. **Lies `knowledge/INDEX.md`** zu Beginn jeder Session, falls noch nicht geladen.
2. **Matche Task-Schlagwoerter** (cookie, drittland, ai-act, newsletter, barrierefreiheit, ...) gegen die KB-Kategorien aus dem INDEX.
3. **Lies bis zu 3 passende Chunks** via Read/view aus `knowledge/themen/`, `knowledge/urteile/`, `knowledge/gesetze/`, `knowledge/checklisten/`.
4. **Merke geladene Slugs**, um Doppel-Reads zu vermeiden.

Triggers: siehe `.claude/hooks/triggers.json` (gleiche Schlagwort-Map gilt fuer Codex/Copilot).
