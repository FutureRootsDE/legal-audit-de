---
aktualisiert: 2026-04-19
quelle-primaer: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
quellen-sekundaer:
  - https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en
  - https://www.bfdi.bund.de/SharedDocs/Kurzmeldungen/DE/2023/17_Angemessenheitsbeschluss-EU-US-DPF.html
  - https://www.datenschutzkonferenz-online.de/media/ah/230904_DSK_Ah_EU_US.pdf
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

# Drittland-Transfer — Schrems II, SCCs, TIA, EU-US Data Privacy Framework

## Kurz-Überblick

Übermittlungen personenbezogener Daten in Drittländer (außerhalb EWR) sind nach Art. 44–50 DSGVO nur unter strengen Voraussetzungen zulässig. Zentrale Instrumente: Angemessenheitsbeschluss (Art. 45), geeignete Garantien wie Standardvertragsklauseln (Art. 46), Ausnahmen (Art. 49). Seit dem EuGH-Urteil Schrems II (16.07.2020) ist eine Transfer Impact Assessment (TIA) Pflicht. Für USA gilt seit 10.07.2023 der EU-US Data Privacy Framework (DPF) — jedoch nur für DPF-zertifizierte Organisationen.

## Kernaussagen

### Rechtsrahmen Art. 44–50 DSGVO

**Art. 44** — Allgemeiner Grundsatz:
Übermittlung nur zulässig, wenn Schutzniveau im Drittland „nicht unterlaufen" wird.

**Art. 45** — Angemessenheitsbeschluss:
EU-Kommission stellt fest, dass Drittland angemessenes Schutzniveau bietet. Derzeit (Stand April 2026) u. a.: Andorra, Argentinien, Färöer, Guernsey, Isle of Man, Israel, Japan, Jersey, Kanada (kommerziell), Neuseeland, Schweiz, Südkorea, Uruguay, UK, **USA (DPF-zertifizierte Unternehmen)**.

**Art. 46** — Geeignete Garantien (ohne Angemessenheitsbeschluss):
- Standardvertragsklauseln (Standard Contractual Clauses, SCCs) — aktuelle Fassung 2021/914/EU vom 04.06.2021
- Binding Corporate Rules (BCR) für Konzerne
- Genehmigte Verhaltensregeln / Zertifizierungen

**Art. 49** — Ausnahmen für bestimmte Fälle:
- Einwilligung nach ausdrücklicher Information über Risiken
- Vertragserfüllung (restriktiv ausgelegt)
- Wichtige Gründe öffentlichen Interesses
- Rechtsansprüche

### EU-US Data Privacy Framework (DPF, seit 10.07.2023)

- **Angemessenheitsbeschluss 2023/1795 vom 10.07.2023**
- Nachfolger des durch Schrems II gekippten Privacy Shield
- **Organisations-spezifisch**: nur für Unternehmen, die sich aktiv über das US-Handelsministerium (DoC) unter DPF zertifizieren und auf der offiziellen Liste unter `dataprivacyframework.gov` geführt sind
- **Rechtsbehelfs-Mechanismus**: Data Protection Review Court (DPRC); Exec. Order 14086/2022 regelt Bulk-Interception-Einschränkungen
- **Schrems III** (NOYB-Klage) anhängig — DPF könnte erneut kippen. Safety-Net: SCCs + TIA parallel pflegen.
- Praktisch: Für nicht-DPF-zertifizierte US-Anbieter gelten weiterhin SCCs + TIA + ggf. ergänzende Maßnahmen

### Transfer Impact Assessment (TIA) — Pflicht seit Schrems II

Dokumentierte Bewertung mit mindestens folgenden Punkten:
1. **Kategorie der Daten** (Art. 4, 9 DSGVO — sensible Daten? Massendaten?)
2. **Empfänger und Zweck**
3. **Rechtslage im Drittland** (Zugriffsrechte staatlicher Behörden, FISA 702, Cloud Act)
4. **Abwägung**, ob SCCs praktisch wirksam sein können
5. **Ergänzende Maßnahmen** („supplementary measures" nach EDSA Empfehlungen 01/2020):
   - **Technisch:** Verschlüsselung mit EU-seitig gehaltenen Schlüsseln, Pseudonymisierung, Split-Processing
   - **Organisatorisch:** strikter Minimalzugriff, Audit-Rechte, Transparenzberichte
   - **Vertraglich:** Challenge-Rechte bei Behördenanfragen, Notification-Klauseln

### Aktuelle SCCs (2021/914/EU)

Vier Module:
- **Modul 1:** Controller → Controller
- **Modul 2:** Controller → Processor
- **Modul 3:** Processor → Processor (Sub-Auftragsverarbeiter)
- **Modul 4:** Processor → Controller (Rückfluss)

Pflicht-Bestandteil: **Klausel 14** (Erklärung zur TIA), **Anhang III** (technische und organisatorische Maßnahmen).

## Typische Fallstricke in Codebases

- **AWS/Azure/GCP mit EU-Region gebucht, aber Kontroll-Ebene US:** DSK sieht Zugriffsrisiken durch US-Muttergesellschaft (Cloud Act) — bei Non-DPF-Setup: TIA + ergänzende Maßnahmen.
- **Vercel-Edge-Functions:** Global replication — Kundendaten möglicherweise außerhalb EU. Vercel ist DPF-zertifiziert, aber Infrastruktur-Bestandteile (z. B. Cloudflare) separat prüfen.
- **Supabase:** Cloud-Version basiert auf AWS; EU-Region `eu-central-1` (Frankfurt) verfügbar — Check ob DPF relevant oder EU-only ausreicht.
- **Stripe:** DPF-zertifiziert; Datenverarbeitung dennoch transparent in Datenschutzerklärung aufführen (Art. 13 Abs. 1 lit. f).
- **Sentry/Datadog (Error-Monitoring):** Sentry EU-Region verfügbar; User-Context (E-Mail, User-ID) filtern.
- **ChatGPT/Anthropic-API:** OpenAI ist DPF-zertifiziert; Anthropic ebenfalls. Aber: API-Eingaben dürfen keine personenbezogenen Daten enthalten ohne Rechtsgrundlage.
- **Google Fonts dynamisch:** Load zieht IP nach USA — LG München I 3 O 17493/20: 100 EUR immat. Schaden. **Lösung:** selbst hosten (`@fontsource`).
- **reCAPTCHA v3:** unbeschränkt IP-übermittlung an Google. Alternative: hCaptcha (Cloudflare EU), Turnstile.
- **Zapier/Make/n8n-Cloud:** US-Hosting — prüfen, ob DPF + AVV + TIA vorliegen.

## Relevanz für Codebase-Typen

- **Next.js SaaS:** Hosting-Location (Vercel, Netlify) + Datenbank (Supabase, Neon, PlanetScale) + Auth (Clerk, Auth0, Supabase Auth) + Mail (Resend, Postmark) — alle Drittanbieter im Datenschutz-Verzeichnis erfassen.
- **Landingpage:** Tracking-Tools sind Hauptproblem (siehe tracking-analytics.md).
- **n8n:** Self-hosted in EU minimiert Drittland-Problem; bei n8n-Cloud: DPF-Status prüfen.
- **E-Commerce:** Payment Provider (Stripe DPF; PayPal EU-Hub in Luxemburg), Fulfillment, Tax-Tools (Avalara, TaxJar) erfassen.
- **Content/Blog:** CDN (Cloudflare hat DPF + EU-Data-Localization-Suite), Font-Quellen (statt Google Fonts besser lokal), Embed-Quellen (YouTube).

## Behörden-Hinweise

- **EDSA Empfehlungen 01/2020** zu ergänzenden Maßnahmen nach Schrems II
- **EDSA Empfehlungen 02/2020** zur Festlegung ausreichender Garantien
- **DSK Anwendungshinweise zum DPF vom 04.09.2023**
- **EU-Kommission:** Liste der Angemessenheitsbeschlüsse
- **BfDI FAQ Drittland-Transfer** (aktualisiert 2023/2024)

## Zitierbare Urteile

- **EuGH C-311/18 (Schrems II), 16.07.2020** — Privacy Shield ungültig; SCCs nur mit TIA
- **EuGH C-362/14 (Schrems I), 06.10.2015** — Safe Harbor ungültig
- **DSB Österreich, 22.04.2022** — GA Universal unvereinbar (vor DPF)
- **CNIL, 10.02.2022** — Google Analytics Sanktion
- **Garante (IT), 09.06.2022** — Caffeina Media / GA-Entscheidung

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/tracking-analytics]]
- [[themen/avv-muster]]
- [[urteile/eugh-schrems-ii]]
