> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument beschreibt technische Hook-Integration. Es ist keine Rechtsberatung.
>
> **Stand:** 2026-04-19

# Git-Hooks fuer Zielprojekte

Das `pre-commit.sh` in diesem Verzeichnis ist ein Template, das du in **jedem Projekt**, das du mit legal-audit-de auditiert hast, installieren kannst. Es warnt (oder blockt) wenn rechts-relevante Dateien committet werden, ohne dass ein aktueller Audit vorliegt.

## Was der Hook prueft

**Staging-Dateien gegen diese Schlagwoerter im Pfad:**
- Pflicht-Texte: `datenschutz`, `privacy`, `impressum`, `imprint`, `agb`, `terms`, `widerruf`, `cookie`, `consent`
- Tracking-Integration: `google-analytics`, `gtm`, `google-tag-manager`, `meta-pixel`, `facebook-pixel`, `posthog`, `hotjar`, `segment`, `plausible`, `matomo`
- Auth/User-Daten: `auth`, `user-profile`, `account-deletion`
- AVV: `avv`, `dpa`, `subprocessor`

**Plus Root-Komponenten** (Layouts), weil die gerne Tracking-Scripts injizieren:
- `src/app/layout.tsx`, `pages/_app.tsx`, `astro.config.mjs`, `nuxt.config.ts` u.a.

## Installations-Varianten

### Variante 1: Vanilla Git-Hook (Einzel-Entwickler)

```bash
cd <zielprojekt>
cp <anwalt_claude>/templates/git-hooks/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Nachteil: nicht versioniert, jeder Entwickler muss manuell installieren.

### Variante 2: Husky (empfohlen fuer Teams)

```bash
cd <zielprojekt>
pnpm add -D husky
pnpm exec husky init

# Verweise in .husky/pre-commit:
echo 'bash "$(git rev-parse --show-toplevel)"/scripts/legal-precommit.sh' > .husky/pre-commit

# Skript ins Projekt uebernehmen:
mkdir -p scripts
cp <anwalt_claude>/templates/git-hooks/pre-commit.sh scripts/legal-precommit.sh
chmod +x scripts/legal-precommit.sh

git add scripts/legal-precommit.sh .husky/pre-commit package.json
git commit -m "chore: add legal-audit pre-commit hook"
```

Vorteil: versioniert, automatisch beim `pnpm install` im Team aktiv.

### Variante 3: Lefthook / Lint-Staged

Kann als Step in bestehende Lint-Staged/Lefthook-Config eingebunden werden:

**lint-staged** (`package.json`):
```json
{
  "lint-staged": {
    "*": ["bash scripts/legal-precommit.sh"]
  }
}
```

**lefthook** (`lefthook.yml`):
```yaml
pre-commit:
  commands:
    legal-audit-check:
      run: bash scripts/legal-precommit.sh
```

## Konfiguration via Env-Vars

| Variable | Default | Zweck |
|----------|---------|-------|
| `LEGAL_AUDIT_MAX_AGE_DAYS` | `30` | Maximal-Alter des letzten Audits in Tagen |
| `LEGAL_AUDIT_STRICT` | `0` | `1` = Commit blockieren bei veraltetem Audit, `0` = nur warnen |

Beispiel in `.envrc` (fuer direnv) oder `package.json`-Scripts:
```bash
export LEGAL_AUDIT_MAX_AGE_DAYS=14
export LEGAL_AUDIT_STRICT=1
```

## Verhalten

| Szenario | Output | Exit-Code |
|----------|--------|-----------|
| Keine sensiblen Dateien im Commit | kein Output | 0 |
| Sensible Datei + Audit aktuell | Hinweis "Audit-Status OK" | 0 |
| Sensible Datei + Audit veraltet + STRICT=0 | WARNUNG | 0 (non-blocking) |
| Sensible Datei + Audit veraltet + STRICT=1 | WARNUNG + Block | 1 |
| Sensible Datei + kein Audit + STRICT=0 | HINWEIS | 0 |
| Sensible Datei + kein Audit + STRICT=1 | HINWEIS + Block | 1 |

## Troubleshooting

**Hook schlaegt nicht an, obwohl sensible Datei committet wurde:**
→ Pruefe, ob Pattern im Dateinamen enthalten ist (case-insensitive). Erweitere `SENSITIVE_PATTERNS` im Skript, wenn dein Projekt andere Namen nutzt.

**Hook blockiert unerwuenschte Commits:**
→ `LEGAL_AUDIT_STRICT=0` setzen, oder Hook komplett bypassen mit `git commit --no-verify` (nur im Notfall).

**Hook ignoriert Audit, obwohl `docs/legal-audit/LegalAudit.md` existiert:**
→ Pruefe mit `stat <file>`, ob die Datei-Mtime sinnvoll ist. Auf Windows ggf. `stat -c %Y` vs. `stat -f %m` pruefen.
