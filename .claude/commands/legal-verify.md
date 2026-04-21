---
description: Gibt Empfehlungen fuer Fachanwaelte, spezialisierte Kanzleien und Verifizierungs-Tools fuer ein Rechtsthema.
argument-hint: <thema | audit-id | rechtsgebiet>
allowed-tools: Read, Glob
---

# /legal-verify

Gib konkrete Empfehlungen, wer und/oder welches Tool die KI-Analyse zu `$ARGUMENTS` verifizieren sollte.

## Ablauf

1. **Klassifiziere das Thema:**
   - Datenschutz/DSGVO/AVV/TOM → Fachanwalt IT-Recht mit DSB-Schwerpunkt
   - AGB/Widerruf/Fernabsatz → Fachanwalt IT-Recht / Vertragsrecht
   - UWG/Marketing/Abmahnung → Fachanwalt gewerblicher Rechtsschutz
   - Urheberrecht/Marken/Bildrechte → Fachanwalt Urheber- und Medienrecht
   - BFSG/Barrierefreiheit → Spezialberatung (BFSG-Koordinatoren) + A11y-Audit-Tools
   - AI Act → IT-Recht + KI-Compliance-Beratung
   - NIS2/KRITIS → Fachanwalt IT-Recht + BSI-lizenzierter Auditor

2. **Lies** `knowledge/anwaelte-tools/fachanwaelte-it-recht.md`, `kanzleien-saas-spezialisiert.md`, `tools-generatoren.md`, `tools-consent-mgmt.md`, `tools-scanner.md`.

3. **Gib strukturierte Empfehlung zurueck:**

```markdown
## Anwalts-Empfehlung fuer "$ARGUMENTS"

### Ideale Qualifikation
- <Fachanwaltstitel + evt. Zusatzqualifikation>

### Konkrete Kanzlei-Kategorien (Budget-Range)
- Spezialisierte B2B-SaaS-Boutique: 500–1.500 EUR
- Wirtschaftskanzlei mit IT-Sektor: 1.500–3.000 EUR
- Online-Plattform (advocado, anwalt.de): 300–500 EUR (Qualitaet variiert)

### Konkret benannte Kanzleien / Anwaelte (Stand <datum>)
- <aus knowledge/anwaelte-tools/kanzleien-saas-spezialisiert.md>

### Verifizierungs-Tools (Selbst-Check VOR Anwalts-Termin)
- <scanner/generatoren, je nach Thema>

### Typischer Prozess
1. Pre-Audit mit Selbst-Check-Tool
2. Anwalts-Termin (2-4h fuer Review von LegalAudit.md + Clean-Versionen)
3. Iteration bis Freigabe
4. Dokumentation der Pruefung (fuer § 5 Abs. 2 BDSG Rechenschaftspflicht)
```

4. **Disclaimer:** Beende die Antwort mit dem Hinweis, dass Kanzlei-Empfehlungen keine Mandats-Vermittlung sind und konkrete Mandatsverhaeltnisse selbst zu schliessen sind.
