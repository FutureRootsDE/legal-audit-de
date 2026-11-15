---
aktualisiert: 2026-11-15
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html
  - https://www.iso.org/standard/27001
verifiziert-am: 2026-11-14
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

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

Genehmigte Verhaltensregeln (Art. 40) und Zertifizierungen (Art. 42) können als Faktor für den Nachweis herangezogen werden.

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
| **BSI C5** | BSI | Cloud Computing | Cloud-Anbieter aller Herkunft (Testat); Version 2025/26 beachten |
| **SOC 2 Type II** | AICPA | Security, Availability, Confidentiality | US-lastige SaaS |
| **TISAX** | VDA | Automotive | Automotive-Lieferketten |
| **CCM** | Cloud Security Alliance | Cloud Controls | Cross-Framework-Mapping |
| **§ 30 BSIG (NIS-2)** | Gesetzgeber / BSI | Pflicht-Risikomanagementmaßnahmen (10 Mindestmaßnahmen, Abs. 2) | Für besonders wichtige und wichtige Einrichtungen verbindlich; für andere als Maßstab |

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
  - Bestelldaten-Retention nach § 147 Abs. 3 AO (10 Jahre für Bücher und Jahresabschlüsse, 8 Jahre für Buchungsbelege, 6 Jahre für sonstige Unterlagen; abgewogen gegen Löschanspruch)
- **Content/Blog:**
  - WordPress: Updates, starke Admin-Passwörter, Login-Schutz (Limit Login Attempts)
  - Backup-Routine (Updraft, BackWPup)
  - Keine PII in Kommentar-System

## Behörden-Hinweise

- **BSI Leitfaden „Stand der Technik"** (jährlich aktualisiert)
- **§ 30 BSIG** (BSI-Gesetz vom 02.12.2025, BGBl. 2025 I Nr. 301, in Kraft seit 06.12.2025): gesetzlicher Mindestkatalog
- **DSK Kurzpapier Nr. 18** — Risiko für die Rechte und Freiheiten natürlicher Personen (Grundlage der Risikobewertung nach Art. 32)
- **ENISA Guidelines for SMEs on the Security of Personal Data Processing**
- **BSI C5 Kriterienkatalog** (für Cloud-Anbieter)
- **TeleTrusT Handreichung „Stand der Technik in der IT-Sicherheit"** (inoffiziell, häufig zitiert)

## Zitierbare Urteile

- **LG Köln 28 O 1/20, 18.03.2020** — Datenverlust durch fehlende Backups = Ersatzpflicht <<VERIFIKATION AUSSTEHEND>>
- **EuGH C-340/21 (Natsionalna agentsia), 14.12.2023**: Unbefugte Offenlegung bzw. unbefugter Zugang durch Dritte belegt für sich keine ungeeigneten TOM (Tenor 1); die Beweislast für die Geeignetheit trägt der Verantwortliche (Tenor 3)
- **LAG Hamm 14 Sa 545/21, 23.02.2022** — Schadenersatz bei unzureichender Zugriffskontrolle <<VERIFIKATION AUSSTEHEND>>
- **BGH VI ZR 10/24, 18.11.2024** — Leitentscheidung Facebook-Scraping: Kontrollverlust als immaterieller Schaden; verstaerkt den Druck auf dokumentierte TOM

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/meldepflicht-datenpanne]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/avv-muster]]
- [[urteile/bgh-vi-zr-10-24-kontrollverlust]]

## Aenderungsvermerk 2026-11-14

- NIS2-Hinweis: Das BSI-Gesetz (BSIG) gilt in der Fassung des
  NIS-2-Umsetzungsgesetzes (gesetze-im-internet.de/bsig_2025). Detail in
  [[gesetze/nis2-bsig]].
- BGH VI ZR 10/24 ergaenzt.
- Zwei LG-/LAG-Aktenzeichen mit Verifikationsmarker versehen.
- Stand/verifiziert-am auf 2026-11-14 vereinheitlicht.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  NIS2-Hinweis berichtigt (BSIG in der Fassung des NIS-2-Umsetzungsgesetzes
  gilt); EuGH C-340/21 an Tenor 1 und 3 ausgerichtet; § 147 Abs. 3 AO
  Fristen aufgeschluesselt; Fehlverweis DSK Kurzpapier Nr. 2 durch Nr. 18
  ersetzt; BSI C5 nicht auf deutsche Anbieter beschraenkt; Art. 32 Abs. 3
  am Wortlaut ausgerichtet.
- 2026-11-15: Korrekturen aus doppelter unabhängiger Prüfung (Runde 2):
  § 30 BSIG (Risikomanagementmassnahmen, in Kraft seit 06.12.2025) in die
  Rahmenwerk-Tabelle und die Behoerden-Hinweise aufgenommen.
