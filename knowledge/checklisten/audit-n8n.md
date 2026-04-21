---
aktualisiert: 2026-04-19
gilt-fuer: n8n-Workflow-Exports (JSON), self-hosted und Cloud
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) erstellt. Es ist
> **keine Rechtsberatung** im Sinne des § 2 RDG. n8n-Workflows sind oft
> "schattenhafte" Datenverarbeitung, die in Verarbeitungsverzeichnissen und
> Datenschutzerklaerungen fehlt. Vor jeder Produktiv-Nutzung pruefen.
>
> **Stand:** 2026-04-19

# Audit-Checkliste: n8n-Workflows

## Kurz-Ueberblick

n8n-Workflows orchestrieren Datenfluesse zwischen Systemen (APIs, Datenbanken, Webhooks). DSGVO-Risiko entsteht durch:
1. **Versteckte Drittanbieter-Aufrufe** (oft US-APIs in `httpRequest`-Nodes ohne AVV)
2. **PII in Execution-Logs** (n8n speichert Payloads per Default lang)
3. **Webhook-Endpunkte ohne Auth** (DSGVO Art. 32 — Integritaet/Vertraulichkeit)
4. **Cron-gesteuerte Batch-Verarbeitung** ohne Fehler-Alerting

## Vorab: Workflow-JSON besorgen

```bash
# n8n REST API
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  https://n8n.example.com/api/v1/workflows/WORKFLOW_ID > workflow.json
```

Oder Export ueber n8n-UI (Einstellungen → Export JSON).

## Pass 1: PII-Identifikation im Workflow

Ziel: jeder Node und jede Expression identifizieren, die mit PII arbeitet.

- [ ] **Trigger-Nodes** — wo kommen Daten rein?
  - `webhook` — was postet der Webhook? Welches externe System?
  - `scheduleTrigger` / `cron` — welche Quelle wird abgefragt?
  - `emailImap` — liest E-Mails mit? Dann PII im Payload!
- [ ] **Code-Nodes** (`code`, `function`) — Custom JavaScript/Python, das PII verarbeiten kann
  - Werden Daten geloggt via `console.log`? → landet in Execution-Log
  - Werden Daten transformiert oder aus dem Workflow weitergegeben?
- [ ] **HTTP-Request-Nodes** (`httpRequest`) — API-Calls
  - Target-URL auf US-Hosts pruefen (openai.com, api.anthropic.com, api.elevenlabs.io, fal.ai, api.mistral.ai)
  - Headers enthalten Auth-Token? → Credential-Pruefung
  - Body enthaelt PII?
- [ ] **Datenbank-Nodes** (`postgres`, `mysql`, `mongoDb`) — was wird gelesen/geschrieben?
- [ ] **File-Nodes** — lokale Dateien mit PII (Downloads, Uploads)
- [ ] **Email-Nodes** (`emailSend`, `gmail`) — Empfaenger + Inhalte

### Ergebnis: Provider-Matrix aufstellen

| Node-Typ | Anzahl | Provider | Drittland? | AVV? | Consent/Rechtsgrundlage? |
|----------|--------|----------|-----------|------|-------------------------|
| httpRequest → OpenAI | z.B. 3 | OpenAI Inc. | USA | ? | Art. 6/f + DPF |
| httpRequest → Anthropic | 2 | Anthropic PBC | USA | ? | Art. 6/f + SCC |
| httpRequest → FAL.ai | 1 | FAL Labs | USA | ? | SCC + TIA |
| httpRequest → ElevenLabs | 1 | ElevenLabs Inc. | USA | ? | SCC + TIA |
| postgres | 2 | Eigene DB (Hetzner) | DE | n/a | n/a |

## Pass 2: Drittland-/Drittanbieter-Transfers

- [ ] Fuer JEDEN externen Provider: existiert AVV? (Tier-1-Pflicht)
- [ ] US-Provider: DPF-Status pruefen (dataprivacyframework.gov → Unternehmenssuche)
- [ ] Nicht-DPF-Provider: SCCs unterzeichnet?
- [ ] TIA dokumentiert bei sensitiven Daten (Art. 46 DSGVO + Schrems II)
- [ ] Provider in Datenschutzerklaerung des Verantwortlichen aufgelistet?
- [ ] Sub-Prozessor-Changes monitoren (Provider-Vendor-Seiten abonnieren)

### Typische Provider in n8n-Workflows (AI-Content-Stack)

| Provider | Land | Typische AVV | Besonderheit |
|----------|------|-------------|--------------|
| OpenAI | USA | ja (DPA/BAA) | DPF-zertifiziert |
| Anthropic | USA | ja (DPA) | EU-Data-Processing-Addendum verfuegbar |
| Mistral | FR | ja | EU-Provider, klarster Fall |
| ElevenLabs | USA | ja (per Request) | kein DPF — SCC zwingend |
| FAL.ai | USA | ja | SCC noetig |
| Stability AI | UK/USA | ja | SCC/Ade-Abkommen UK |
| Google Cloud (Vertex AI) | EU-Region waehlen | ja | DPF + SCC |
| Azure OpenAI | EU-Region waehlen | ja | Microsoft DPA |

## Pass 3: n8n-spezifische Datenpersistenz

n8n speichert Workflow-Executions in PostgreSQL — **jede Execution enthaelt die vollstaendigen Payloads**.

- [ ] **Execution-Data-Retention** konfiguriert?
  - Environment: `EXECUTIONS_DATA_PRUNE=true`
  - `EXECUTIONS_DATA_MAX_AGE=336` (Stunden, z.B. 14 Tage)
  - Standard n8n ist "behalte alles" — das ist i.d.R. DSGVO-widrig
- [ ] **Execution-Data-Save-On-Success** — bei erfolgreichen Durchlaeufen: Full / Minimal / None
- [ ] **Execution-Data-Save-On-Error** — bei Fehlern: Full empfohlen fuer Debug, aber Retention kurz halten
- [ ] **Execution-Data-Save-Manual-Executions** — Dev-Runs im Produktiv-DB: abschalten
- [ ] **Binary-Data-Storage**: FS / S3 — Retention-Job noetig
- [ ] **Credentials**: verschluesselt mit `N8N_ENCRYPTION_KEY` (Pflicht-Env-Var setzen, nicht Default!)
- [ ] **PostgreSQL-Backups**: Retention max. 30 Tage, verschluesselt

### PostgreSQL-Query fuer Execution-Payloads (Audit)

```sql
-- Alte Executions mit PII finden
SELECT id, "workflowId", "startedAt", mode, status, LENGTH(data::text) AS payload_size
FROM execution_entity
WHERE "startedAt" < NOW() - INTERVAL '14 days'
ORDER BY "startedAt" DESC
LIMIT 100;

-- Anzahl Executions pro Workflow (last 30d)
SELECT "workflowId", COUNT(*) AS exec_count
FROM execution_entity
WHERE "startedAt" > NOW() - INTERVAL '30 days'
GROUP BY "workflowId"
ORDER BY exec_count DESC;
```

## Pass 4: Webhook-Security

Webhook-Endpunkte sind oeffentlich erreichbar und oft das schwaechste Glied.

- [ ] **Auth-Header** konfiguriert (`X-API-Key` oder HMAC-Signatur)?
- [ ] **Rate-Limiting** vor n8n (Traefik / Cloudflare)?
- [ ] **TLS** zwingend (kein HTTP, kein self-signed)?
- [ ] **IP-Whitelisting** moeglich? (bei B2B oft ja)
- [ ] **CORS-Konfiguration** streng?
- [ ] **HMAC-Verification** im Workflow (Code-Node, das Signatur vs. Shared Secret prueft)?
- [ ] **Webhook-URL** nicht geleakt in Repo/README (Geheim halten)?

## Pass 5: KI-Spezifisch (n8n)

Bei KI-lastigen Workflows (Claude/GPT fuer Content-Generierung, Flux/Ideogram fuer Bilder, ElevenLabs fuer TTS):

- [ ] **Prompt-Inhalte** ohne PII (oder mit Consent)
- [ ] **Output-Verantwortlichkeit**: KI-Halluzinationen erkennen, manueller Review-Schritt
- [ ] **Bias in AI-Entscheidungen** bei Klassifikation (z.B. Content-Kategorisierung)
- [ ] **Kennzeichnung** bei KI-generiertem Output (Art. 50 AI Act)
- [ ] **DSFA** bei systematischer Bewertung von Menschen
- [ ] **Training auf Nutzerdaten** bei Provider ausschalten (OpenAI Business-Tier / API ist Default-Out, Consumer-ChatGPT ist Default-In)
- [ ] [[gesetze/ai-act]], [[themen/ki-transparenz]]

## Pass 6: Barrierefreiheit

n8n-Workflows sind Backend — keine direkte WCAG-Pruefung. Aber:

- [ ] Generierte Content-Outputs (Blog-Posts, Podcasts) auf Barrierefreiheit pruefen
- [ ] Untertitel bei generierten Videos (Audio-Beschreibungen fuer Hoerbeeintraechtigte)
- [ ] Alt-Texte bei generierten Bildern (KI kann das automatisch)

## Pass 7: Urheber / Marken

- [ ] **Scraping-Nodes** (WebScraper, HTTP-Scraper) — Robots.txt respektieren, Nutzungsbedingungen der Quelle
- [ ] **RSS-Feeds** — meist erlaubt, aber keine massive Content-Uebernahme ohne Quellenangabe
- [ ] **Stock-API-Nodes** (Unsplash API, Pexels) — Lizenzbedingungen im Workflow-Output dokumentieren
- [ ] **KI-Output-Rechte**: OpenAI/Anthropic-ToS pruefen zu Nutzungsrecht an generierten Inhalten
- [ ] **Markenrecht** bei automatisierten Social-Posts (keine Brand-Jacking)

## Pass 8: Logs / Retention / Monitoring

- [ ] n8n-Container-Logs (docker logs) — Rotation konfiguriert
- [ ] **Fehler-Alerting**: bei Cron-Job-Fehler Admin-Benachrichtigung (Slack, E-Mail, Discord) — "stille" Cron-Fehler sind DSGVO-relevant (Datenintegritaet Art. 5 Abs. 1 lit. f)
- [ ] **Workflow-Audit-Log** wer hat welchen Workflow geaendert (n8n User-Management Pflicht ab mehreren Entwicklern)
- [ ] **Execution-Limits** (Timeout, Memory) konfiguriert — verhindert DoS
- [ ] **Disaster Recovery**: PostgreSQL-Backup-Restore-Test alle 3 Monate

## Typ-spezifische Besonderheiten

- **n8n Cloud** (n8n.io SaaS) — Sitz in DE, aber unbedingt AVV mit n8n GmbH anfordern
- **Self-hosted auf Hetzner / anderem EU-Hoster**: AVV mit Hoster, volle Kontrolle ueber Logs/Retention
- **n8n auf Vercel/AWS** — Drittland-Pruefung Hosting-Provider zusaetzlich
- **Mehrere Workflows als Sub-Workflows**: Datenfluesse zwischen Workflows dokumentieren (ein Workflow-Aufruf = interne Verarbeitung, kein neuer Drittanbieter-Transfer)

## Typische Findings (typische n8n-Produktiv-Workflows)

### CRIT

- `N8N_ENCRYPTION_KEY` nicht gesetzt (Default-Key = Credentials-Leak-Risiko bei Backup-Kompromiss)
- Webhook-Endpunkt ohne Auth mit PII-Payload
- httpRequest-Node sendet PII an US-API ohne AVV/SCC
- Execution-Retention unendlich → wachsende Datenbank mit PII aus dem Jahr X
- DB-Credentials im Klartext in Code-Node (nicht als Credential-Referenz)

### HIGH

- Cron-Fehler-Alerting fehlt → Datenverarbeitung kann stillschweigend stehen bleiben
- Workflow nicht im Verarbeitungsverzeichnis (Art. 30) gelistet
- KI-Provider-Aufruf ohne Hinweis in Datenschutzerklaerung des Verantwortlichen
- Kein Test-/Staging-Trennung (Entwickler testen an Produktiv-Daten)
- n8n-User-Management nicht aktiv (alle Nutzer mit Admin-Rechten)

### MED

- Execution-Data enthaelt vollstaendige E-Mail-Inhalte (PII-Minimisierung bei Save-Mode "Full")
- Code-Node macht `console.log(item)` mit PII → Container-Logs wachsen unkontrolliert
- Workflow-Versionskontrolle (Export zu Git) fehlt
- Credentials-Namen enthalten PII ("stripe_kunde_meier.com" statt "stripe_prod")

### LOW

- Workflow-Beschreibung / Node-Notes fehlen (Dokumentationspflicht indirekt aus Art. 30)

## Empfohlene Workflow-Scans (halbautomatisch)

Beim Audit: JSON extrahieren und per Skript pruefen:

```bash
# Grep nach US-API-Calls im Workflow-JSON
grep -oE '"url": "https://[^"]+"' workflow.json | sort -u

# Suche nach unverschluesselten Credentials im JSON (sollte NIE sichtbar sein)
grep -iE '(apiKey|token|secret)":\s*"[^"]{8,}' workflow.json

# Webhook-Nodes ohne Auth-Header
jq '.nodes[] | select(.type == "n8n-nodes-base.webhook") | .parameters' workflow.json
```

## Siehe auch

- [[gesetze/dsgvo]] — Art. 30, 32, 46
- [[gesetze/bdsg]]
- [[themen/avv-muster]]
- [[themen/drittland-transfer]]
- [[themen/verarbeitungsverzeichnis]]
- [[themen/tom]] — TOM-Kategorien fuer n8n-Infrastruktur
- [[themen/ki-transparenz]]
- [[urteile/eugh-schrems-ii]]
- [[checklisten/audit-saas]]
- [[anwaelte-tools/tools-scanner]]
