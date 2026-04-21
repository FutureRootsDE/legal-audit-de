---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html
  - https://www.iso.org/standard/27001
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# TOM — Technische und organisatorische Maßnahmen (Art. 32 DSGVO)

## Kurz-Überblick

Technische und organisatorische Maßnahmen (TOM) sind nach Art. 32 DSGVO verpflichtend, um ein dem Risiko angemessenes Schutzniveau zu gewährleisten. Die alte Anlage zu § 9 BDSG-alt (acht Gebote) ist seit 2018 formal abgelöst, die inhaltliche Struktur aber nach wie vor praktische Grundlage — ergänzt durch die DSGVO-Kriterien (Art. 32 Abs. 1 lit. a-d). Als Referenz-Rahmen dienen BSI IT-Grundschutz, ISO/IEC 27001 sowie C5 (Cloud).

## Kernaussagen — Art. 32 DSGVO

### Abs. 1 — Pflichtkriterien

> Unter Berücksichtigung des Stands der Technik, der Implementierungskosten und der Art, des Umfangs, der Umstände und der Zwecke der Verarbeitung sowie der unterschiedlichen Eintrittswahrscheinlichkeit und Schwere des Risikos für die Rechte und Freiheiten natürlicher Personen

müssen folgende (beispielhafte) Maßnahmen umgesetzt werden:
- (a) Pseudonymisierung und Verschlüsselung
- (b) Fähigkeit, Vertraulichkeit, Integrität, Verfügbarkeit und Belastbarkeit der Systeme sicherzustellen
- (c) Fähigkeit zur raschen Wiederherstellung (Disaster Recovery)
- (d) Verfahren zur regelmäßigen Überprüfung, Bewertung und Evaluierung

### Abs. 2 — Risikobewertung

Risiken müssen bewertet werden für: unbefugter Zugriff, Verlust, Zerstörung, Veränderung, Offenlegung.

### Abs. 3 — Verhaltensregeln / Zertifizierungen

Genehmigte Verhaltensregeln (Art. 40) und Zertifizierungen (Art. 42) können als Nachweis dienen.

## Strukturierung der TOM (praxisbewährt)

### 1. Vertraulichkeit
- **Zutrittskontrolle:** Zaun, Zugangskontrolle, Alarm, Videoüberwachung für Serverräume
- **Zugangskontrolle:** Passwort-Policy, 2FA/MFA, SSO, Sperren bei Fehlversuchen
- **Zugriffskontrolle:** Rollen-/Rechte-Konzept (RBAC), Least Privilege, Review-Prozess
- **Trennungskontrolle:** Multi-Tenancy-Separation, Staging/Prod-Trennung, Test-Daten anonymisiert
- **Pseudonymisierung:** IDs statt Klarnamen, Token-Systeme
- **Verschlüsselung:** TLS 1.2+, Disk-Encryption (LUKS, BitLocker), Datenbank-Verschlüsselung at-rest, E-Mail-Verschlüsselung (S/MIME, PGP)

### 2. Integrität
- **Weitergabekontrolle:** VPN, TLS, verschlüsselte Mail, SFTP
- **Eingabekontrolle:** Audit-Logs, Änderungsprotokolle, Integritätsprüfungen (Hashes)

### 3. Verfügbarkeit und Belastbarkeit
- **Wiederherstellbarkeit:** Backup-Konzept (3-2-1-Regel), Restore-Tests
- **Zuverlässigkeit:** Monitoring, Load-Balancing, Redundanz
- **Datensicherung:** Offsite-Backup, Immutability, Ransomware-Schutz
- **Business Continuity Plan (BCP)**

### 4. Regelmäßige Überprüfung
- **Datenschutz-Management:** PDCA-Zyklus, DSB-Berichte
- **Incident-Response:** Meldeketten, Runbooks
- **Auditierung:** Interne Audits, externe Penetration-Tests, SOC 2 / ISO 27001
- **Mitarbeitersensibilisierung:** Schulungen, Phishing-Tests

## Referenz-Rahmenwerke

| Rahmenwerk | Herausgeber | Fokus | Relevanz für Codebase |
|------------|-------------|-------|----------------------|
| **BSI IT-Grundschutz** | BSI | Deutsche Behörden-Standards | Bausteine für konkrete Maßnahmen |
| **ISO/IEC 27001** | ISO | Information Security Management System | Globaler Gold-Standard |
| **ISO/IEC 27018** | ISO | Schutz von PII in Cloud | Cloud-Anbieter-Prüfung |
| **BSI C5** | BSI | Cloud Computing | Für deutsche Cloud-Anbieter |
| **SOC 2 Type II** | AICPA | Security, Availability, Confidentiality | US-lastige SaaS |
| **TISAX** | VDA | Automotive | Automotive-Lieferketten |
| **CCM** | Cloud Security Alliance | Cloud Controls | Cross-Framework-Mapping |

## Typische Fallstricke in Codebases

- **`.env` in Repo eingecheckt:** klassischer Vertraulichkeits-Bruch → sofort secret rotation.
- **Datenbank-Passwörter hart codiert / in Docker-Compose ohne Secrets:** nutze Vault / Doppler / AWS Secrets Manager.
- **API-Keys in Mobile-Apps:** reversible → Proxy-Backend nötig.
- **Logs mit PII / Passwörtern / Tokens:** Logger filtern (`winston` / `pino` mit Redaction).
- **Keine Rate-Limits → Brute-Force möglich:** `express-rate-limit`, Cloudflare Rate Limits.
- **Fehlende HTTPS-Redirects / HSTS:** Standard-Header-Set pflegen (Helmet.js, Next.js `headers()`).
- **Keine Backup-Tests:** „Backups existieren" reicht nicht — Restore muss funktionieren.
- **Keine Mehr-Faktor-Authentisierung für Admin-Accounts:** Kern-Anforderung nach BSI Stand der Technik.
- **Session-Cookies ohne `Secure`, `HttpOnly`, `SameSite`:** Cookies sichern.
- **Keine `Content-Security-Policy` / unsichere CORS-Konfiguration:** OWASP-Basics.
- **Unverschlüsselter Support-Zugriff** auf Produktionsdaten („mal eben in die DB schauen"): Audit-Log + Approval-Flow.
- **SSH-Passwort-Auth statt Keys:** nur Keys erlauben, 22 → höheren Port, fail2ban.
- **Keine Security-Updates-Automation:** Dependabot / Renovate aktivieren.
- **Staging-Daten sind Prod-Dump ohne Anonymisierung:** DSK sieht das kritisch.

## Relevanz für Codebase-Typen

- **Next.js SaaS:**
  - Environment-Secrets via Vercel / Doppler
  - Auth (Clerk/Supabase) mit MFA aktivieren
  - `next-safe-action` / Zod-Validierung an allen Boundaries
  - Sentry mit PII-Scrubbing
  - Vercel DPF + Sub-Prozessor-Liste
- **Landingpage:**
  - Minimaler Stack — reicht oft Cloudflare + statisches Hosting
  - Formular-Daten nicht clientseitig zwischenspeichern
- **n8n:**
  - Self-hosted: `N8N_ENCRYPTION_KEY` rotieren, MFA aktivieren, Workflow-Versionierung
  - Credentials verschlüsseln (nativ), regelmäßige Exports sichern
  - Nginx / Traefik vor n8n mit Let's Encrypt
  - Webhooks mit Signatur-Validierung
- **E-Commerce:**
  - PCI-DSS wenn Karteninhaber-Daten durchlaufen (Stripe-Checkout reduziert Scope)
  - Fraud-Detection / 3DS2
  - Bestelldaten-Retention nach § 147 AO (steuerlich 6–10 Jahre, abgewogen gegen Löschanspruch)
- **Content/Blog:**
  - WordPress: Updates, starke Admin-Passwörter, Login-Schutz (Limit Login Attempts)
  - Backup-Routine (Updraft, BackWPup)
  - Keine PII in Kommentar-System

## Behörden-Hinweise

- **BSI Leitfaden „Stand der Technik"** (jährlich aktualisiert)
- **DSK Kurzpapier Nr. 2** — Grundlagen für TOM
- **ENISA Guidelines for SMEs on the Security of Personal Data Processing**
- **BSI C5 Kriterienkatalog** (für Cloud-Anbieter)
- **TeleTrusT Handreichung „Stand der Technik in der IT-Sicherheit"** (inoffiziell, häufig zitiert)

## Zitierbare Urteile

- **LG Köln 28 O 1/20, 18.03.2020** — Datenverlust durch fehlende Backups = Ersatzpflicht
- **EuGH C-340/21 (Natsionalna agentsia), 14.12.2023** — Auch nicht-absichtliche Offenlegung = DSGVO-Verstoß; Beweislast für angemessene TOM liegt beim Verantwortlichen
- **LAG Hamm 14 Sa 545/21, 23.02.2022** — Schadenersatz bei unzureichender Zugriffskontrolle

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/meldepflicht-datenpanne]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/avv-muster]]
