#!/usr/bin/env bash
# Pre-Commit-Hook: warnt, wenn rechts-relevante Dateien ohne vorheriges Re-Audit geaendert werden.
#
# Installation im Zielprojekt:
#   cp templates/git-hooks/pre-commit.sh <zielprojekt>/.git/hooks/pre-commit
#   chmod +x <zielprojekt>/.git/hooks/pre-commit
#
# Oder als Husky-Hook (empfohlen fuer Teams):
#   .husky/pre-commit → bash <pfad-zu-diesem-skript>
#
# Verhalten:
#   - Prueft, ob gestagte Dateien rechtlich sensibel sind (Impressum, DSE, AGB, Tracking-Scripts, AVV-Konfig)
#   - Wenn ja + docs/legal-audit/LegalAudit.md aelter als Standard-Frist (30 Tage): WARNUNG
#   - User kann weiterhin committen (non-blocking), aber wird erinnert
#
# Konfiguration per Env-Vars:
#   LEGAL_AUDIT_MAX_AGE_DAYS   (default: 30)
#   LEGAL_AUDIT_STRICT         (wenn "1": blockt Commit bei veraltetem Audit)

set -euo pipefail

MAX_AGE_DAYS="${LEGAL_AUDIT_MAX_AGE_DAYS:-30}"
STRICT="${LEGAL_AUDIT_STRICT:-0}"

# Patterns fuer rechts-relevante Dateien
SENSITIVE_PATTERNS=(
  # Pflicht-Texte
  "datenschutz"
  "privacy"
  "impressum"
  "imprint"
  "agb"
  "terms"
  "widerruf"
  "cookie"
  "consent"

  # Tracking-/Analytics-Integration
  "google-analytics"
  "gtm"
  "google-tag-manager"
  "meta-pixel"
  "facebook-pixel"
  "posthog"
  "hotjar"
  "segment"
  "plausible"
  "matomo"

  # Auth / User-Daten
  "auth"
  "user-profile"
  "account-deletion"
  "account-delete"

  # AVV / DPA
  "avv"
  "dpa"
  "subprocessor"
)

# Layouts / Root-Komponenten die Tracking-Scripts injizieren koennen
LAYOUT_PATTERNS=(
  "src/app/layout.tsx"
  "src/app/layout.jsx"
  "app/layout.tsx"
  "pages/_app.tsx"
  "pages/_document.tsx"
  "astro.config.mjs"
  "nuxt.config.ts"
)

STAGED=$(git diff --cached --name-only --diff-filter=ACMR)
if [[ -z "$STAGED" ]]; then
  exit 0
fi

SENSITIVE_FILES=""
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  lower=$(echo "$file" | tr '[:upper:]' '[:lower:]')

  for pat in "${SENSITIVE_PATTERNS[@]}"; do
    if [[ "$lower" == *"$pat"* ]]; then
      SENSITIVE_FILES+="  $file  (Pattern: $pat)"$'\n'
      break
    fi
  done

  for lay in "${LAYOUT_PATTERNS[@]}"; do
    if [[ "$lower" == "$lay" || "$lower" == *"$lay" ]]; then
      SENSITIVE_FILES+="  $file  (Layout/Root-Komponente)"$'\n'
      break
    fi
  done
done <<<"$STAGED"

if [[ -z "$SENSITIVE_FILES" ]]; then
  exit 0
fi

# Pruefe Audit-Alter
AUDIT_FILE="docs/legal-audit/LegalAudit.md"
AUDIT_AGE_DAYS=-1
AUDIT_STATUS="FEHLT"

if [[ -f "$AUDIT_FILE" ]]; then
  AUDIT_MTIME=$(stat -c %Y "$AUDIT_FILE" 2>/dev/null || stat -f %m "$AUDIT_FILE" 2>/dev/null || echo 0)
  NOW=$(date +%s)
  AUDIT_AGE_DAYS=$(( (NOW - AUDIT_MTIME) / 86400 ))
  if (( AUDIT_AGE_DAYS <= MAX_AGE_DAYS )); then
    AUDIT_STATUS="AKTUELL ($AUDIT_AGE_DAYS Tage alt)"
  else
    AUDIT_STATUS="VERALTET ($AUDIT_AGE_DAYS Tage alt, max $MAX_AGE_DAYS)"
  fi
fi

# Ausgabe
echo "" >&2
echo "==== legal-audit-de Pre-Commit Legal-Check ====" >&2
echo "" >&2
echo "Rechts-relevante Dateien in diesem Commit:" >&2
echo "$SENSITIVE_FILES" >&2
echo "Letztes Legal-Audit: $AUDIT_STATUS" >&2
echo "" >&2

if [[ "$AUDIT_STATUS" == "FEHLT" ]]; then
  echo "⚠  HINWEIS: Noch kein Audit durchgefuehrt." >&2
  echo "   Empfehlung: cd <anwalt_claude> && claude → /legal-audit \"$(pwd)\"" >&2
  if [[ "$STRICT" == "1" ]]; then
    echo "STRICT-Modus aktiv — Commit blockiert. Audit durchfuehren oder STRICT=0." >&2
    exit 1
  fi
elif [[ "$AUDIT_AGE_DAYS" -gt "$MAX_AGE_DAYS" ]]; then
  echo "⚠  WARNUNG: Legal-Audit ist veraltet ($AUDIT_AGE_DAYS Tage alt)." >&2
  echo "   Empfehlung: Re-Audit durchfuehren." >&2
  echo "   → /legal-audit \"$(pwd)\" --compare" >&2
  if [[ "$STRICT" == "1" ]]; then
    echo "STRICT-Modus aktiv — Commit blockiert." >&2
    exit 1
  fi
else
  echo "✓  Audit-Status OK — aber pruefe, ob die Aenderungen neue Findings ausloesen." >&2
fi

echo "" >&2
echo "Dieser Hook ist non-blocking (ausser STRICT=1). Commit geht weiter." >&2
echo "=============================================" >&2
echo "" >&2

exit 0
