---
name: legal-audit-codebase
description: Fuehrt einen systematischen Rechts-Audit einer Codebase durch (DE/EU-Scope). Nutze diese Skill wenn /legal-audit aufgerufen wird ODER wenn der User eine Codebase auf DSGVO/UWG/AGB/DDG/AI-Act/BFSG/UrhG/NIS2-Probleme untersuchen lassen will.
---

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
