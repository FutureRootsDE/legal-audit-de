---
aktualisiert: 2026-04-19
quellen-sekundaer:
  - https://webbkoll.5july.net/
  - https://observatory.mozilla.org/
  - https://privacyscore.org/
  - https://www.ssllabs.com/
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU, weltweit]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Die hier genannten Scanner-Tools liefern **technische Indikatoren**. Sie
> ersetzen keine juristische Pruefung. Ein "gruenes" Webbkoll-Ergebnis bedeutet
> nicht DSGVO-Konformitaet; ein "rotes" Ergebnis ist nicht automatisch ein
> DSGVO-Verstoss.
>
> **Stand:** 2026-04-19

# Scanner- und Audit-Tools

## Kategorie-Ueberblick

Automatisierte Scanner pruefen Websites/APIs auf Datenschutz- und Sicherheits-
Indikatoren. Sie sind **schnell** (wenige Sekunden pro Scan) und decken
haeufige Probleme auf, ersetzen aber nie den Full-Audit mit JSON-Export-
Analyse, PII-Inventar und Vertragspruefung.

## Tier 1: Datenschutz-Scanner

### Webbkoll (5th of July Foundation)

| Feld | Wert |
|------|------|
| URL | https://webbkoll.5july.net/ (neue Domain seit 2024/25) |
| Frueher | webbkoll.dataskydd.net (redirected; ALTE URL nicht mehr benutzen) |
| Betreiber | 5th of July Foundation, Schweden; Entwicklung von dataskydd.net |
| Was wird geprueft | HTTPS-Redirect, HSTS, Referrer-Policy, Cookies (first- und third-party), externe Requests (Third-Party-Ressourcen), Server-Location, CSP-Header |
| Privatsphaere des Tools | Scan-Ergebnisse 24h im Server-Speicher; IP-Adressen werden nicht geloggt; nur ein essentieller Session-Cookie (CSRF-Schutz); Quellcode auf Codeberg |
| Nutzbarkeit | Single-URL-Scan, kostenlos, kein Account noetig |
| Alte URL-Hinweis | Wer Links zu `webbkoll.dataskydd.net` hat, bitte auf `webbkoll.5july.net` migrieren |

### PrivacyScore (Community-Projekt)

| Feld | Wert |
|------|------|
| URL | https://privacyscore.org/ |
| Betreiber | Forschungs-Community <<VERIFIKATION AUSSTEHEND — Projekt-Status 2026>> |
| Features | Tracker-Erkennung, Security-Header, Server-Fingerprinting |
| Status | Verfuegbarkeit schwankt, Alternativen: Webbkoll |

### privacytools.io (Ersatz-Community-Site)

| Feld | Wert |
|------|------|
| Status | Originale privacytools.io wurde 2021 aufgespalten; die aktive Community-Alternative ist **privacyguides.org** |
| URL Nachfolger | https://www.privacyguides.org/ |
| Inhalt | Empfehlungen fuer datenschutzfreundliche Tools (Browser, VPN, E-Mail, Cloud, etc.) |
| Hinweis | **Kein Scanner**, sondern kuratierte Tool-Liste |

## Tier 2: Security-Scanner (Server/TLS/HTTP-Header)

### Mozilla Observatory

| Feld | Wert |
|------|------|
| URL | https://observatory.mozilla.org/ |
| Betreiber | Mozilla Foundation |
| Was wird geprueft | HTTP-Security-Header (CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy), Cookie-Attribute (Secure, HttpOnly, SameSite), Subresource Integrity |
| Bewertung | A+ bis F, detaillierte Empfehlungen |
| Relevanz fuer DSGVO | hoher — Art. 32 "Integritaet/Vertraulichkeit" verlangt Security-Standards |

### SSL Labs (Qualys)

| Feld | Wert |
|------|------|
| URL | https://www.ssllabs.com/ssltest/ |
| Was wird geprueft | TLS-Konfiguration, Cipher-Suites, Zertifikats-Kette, Vulnerabilitaeten (Heartbleed, POODLE, etc.) |
| Bewertung | A+ bis F |
| Relevanz | Art. 32 — TLS muss state-of-the-art sein |

### Security Headers (securityheaders.com)

| Feld | Wert |
|------|------|
| URL | https://securityheaders.com/ |
| Was wird geprueft | HTTP-Security-Header (CSP, X-Content-Type-Options, HSTS, etc.) |
| Bewertung | A+ bis F |
| Besonderheit | Einfach, fokussiert, schnell |

## Tier 3: A11y/Barrierefreiheits-Scanner (BFSG)

### axe DevTools (Deque)

| Feld | Wert |
|------|------|
| URL | https://www.deque.com/axe/ |
| Verfuegbarkeit | Chrome-/Firefox-Extension (kostenlos), Pro-Version, CLI, CI-Integration |
| Was wird geprueft | WCAG 2.1 A/AA/AAA Automated Checks (deckt ca. 30-50% ab), manuelle Pruefungen noetig |
| Relevanz | BFSG-Pflicht ab 2025-06-28 (bei B2C + > 10 MA / > 2 Mio EUR Umsatz) |

### Lighthouse Accessibility (Google)

| Feld | Wert |
|------|------|
| URL | integriert in Chrome DevTools (F12 → Lighthouse) |
| Was wird geprueft | Subset von axe-core, generiert Accessibility-Score |
| Relevanz | gut fuer Schnellcheck, axe detaillierter |

### WAVE (WebAIM)

| Feld | Wert |
|------|------|
| URL | https://wave.webaim.org/ |
| Was wird geprueft | Visuelle Darstellung der Probleme direkt auf der Seite |
| Besonderheit | Gut fuer visuelle Review mit Kunden |

## Tier 4: DSGVO-Checklisten-Tools

### BayLDA "Pruef Dich selbst" <<UNVERIFIZIERT>>

- Die bayerische Aufsichtsbehoerde (BayLDA) bietet intermittierend Online-Selbstcheck-Tools an
- URL: https://www.lda.bayern.de/ → Bereich "Online-Services"

### IT-Recht Kanzlei Website-Scanner

- Teil der Schutzpakete (siehe [[anwaelte-tools/tools-generatoren]])
- Integriert in Abo ab Starter-Paket
- Scannt Cookies, eingebettete Dienste, Impressum / DSE / AGB auf Vollstaendigkeit

### Cookiebot Free Cookie-Scan

- URL: https://www.cookiebot.com/de/cookie-scanner/
- Single-URL-Scan als Teaser fuer das Abo
- Listet erkannte Cookies + Zwecke

## Tier 5: Forensik / Tracker-Analyse

### Ghostery (Browser-Extension)

| Feld | Wert |
|------|------|
| URL | https://www.ghostery.com/ |
| Was macht es | zeigt Tracker auf jeder Website in Echtzeit |
| Relevanz fuer Audit | schnelle Einordnung welche Third-Party-Services aktiv sind |

### uBlock Origin mit Filterlisten

- Kostenlose Open-Source-Extension
- Macht Tracker, Scripts, iframes sichtbar (Developer-Tools-Ansicht)
- Relevant fuer manuelle Audits

### PrivacyBadger (EFF)

- URL: https://privacybadger.org/
- Automatisches Blockieren von Trackern
- Fuer Audit weniger hilfreich (blockiert, statt auflistet)

## Tier 6: Browser-DevTools (manuell)

Das wichtigste Audit-Tool ist eigentlich der Browser selbst:

- **Network-Tab** (F12 → Network) — alle HTTP-Requests, Ziel-Domains, Payload
- **Application → Cookies** — first- und third-party Cookies
- **Application → Storage** — localStorage / sessionStorage / IndexedDB
- **Application → Service Workers** — haeufig uebersehener Tracking-Vektor
- **Console** — Errors, Warnings, Tracking-Debug

**Pflicht-Workflow vor jedem Audit:**
1. Fresh Incognito-Tab, DevTools offen
2. URL laden, Network-Tab einfrieren (Throttling)
3. Cookie-Banner NICHT akzeptieren
4. Pruefen: was laedt VOR Consent? Alles bis auf notwendige Scripts ist problematisch
5. Screenshot der Network-Liste als Beweis
6. Dann Consent akzeptieren, erneut pruefen
7. Widerruf simulieren (Cookie-Banner zurueck), alle Cookies muessten geloescht werden

## Scanner-Workflow fuer vollstaendigen Audit

```
1. Webbkoll-Scan (5 sek)                    → Grobueberblick
2. Mozilla Observatory (1 min)               → Security-Header
3. SSL Labs (3 min)                          → TLS-Config
4. Lighthouse Accessibility (Chrome)         → Erstes A11y-Level
5. axe DevTools Extension                    → Detailliertes A11y
6. Manuell DevTools Network-Tab (10-30 min)  → tatsaechliches Tracking-Verhalten
7. Cookiebot / IT-Recht Scanner (falls Abo)  → Cookie-Inventar
8. JSON-Export / Codebase-Review             → Konfigurations-Tiefe
```

## Grenzen automatischer Scanner

Scanner sehen **nicht**:
- AVV-Vertraege (rechtlich, offline)
- Verarbeitungsverzeichnis (internes Dokument)
- TOM-Dokument (intern)
- Joint-Controller-Agreements
- Datenfluesse im Backend (Server-side API-Calls)
- Mobile Apps (nur Web)
- Interne Prozesse (Datenpannen-Reaktion, Betroffenen-Rechte-Workflow)
- Loeschkonzepte und tatsaechliche Umsetzung

## Wichtiger Update-Hinweis — Webbkoll Domain-Wechsel

Die frueher unter `webbkoll.dataskydd.net` bekannte Software wird jetzt unter
`webbkoll.5july.net` betrieben. Alte Links (auch in Dokumenten und INDEX-Files)
sollten migriert werden. Die Betreiberschaft ging von **dataskydd.net** zur
**5th of July Foundation** (Schweden). Quellcode weiterhin frei verfuegbar
auf Codeberg.

## Siehe auch

- [[themen/tom]] — technische und organisatorische Massnahmen
- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[gesetze/dsgvo]] — Art. 32
- [[gesetze/bfsg]] — Barrierefreiheit
- [[anwaelte-tools/tools-consent-mgmt]]
- [[anwaelte-tools/tools-generatoren]]
- [[checklisten/audit-saas]]
- [[checklisten/audit-landingpage]]
