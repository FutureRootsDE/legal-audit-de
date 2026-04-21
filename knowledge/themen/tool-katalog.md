---
aktualisiert: 2026-04-19
quelle-primaer: https://www.datenschutzkonferenz-online.de/media/oh/OH_Digitale_Dienste.pdf
quellen-sekundaer:
  - https://www.edpb.europa.eu/
  - https://www.bfdi.bund.de/
  - https://www.dataprivacyframework.gov/list
  - https://www.gesetze-im-internet.de/tddg/
verifiziert-am: 2026-04-19
geltungsbereich: [DE, EU]
---

> **Haftungsausschluss — Keine Rechtsberatung**
> Dieses Dokument wurde mit Unterstützung KI-gestützter Recherche erstellt und dient ausschließlich der internen Orientierung. Es ersetzt keine anwaltliche Beratung. Rechtslage, Behörden-Praxis und Tool-Konfigurationen können sich jederzeit ändern — prüfe im Einzelfall mit aktueller Primärquelle. Die Einordnung einzelner Tools (Einwilligungspflicht, Drittland-Status) hängt stets von der konkreten Konfiguration und vom Einsatzkontext ab.
> **Stand:** 2026-04-19

# Tool-Katalog — DSGVO-Einordnung gängiger Web-Tools

## Kurz-Ueberblick

Katalog von rund 100 verbreiteten Web-/SaaS-Tools mit Einordnung nach Einwilligungspflicht (§ 25 TDDDG), Drittland-Transfer (Art. 44 ff. DSGVO) und typischer Code-Spur. Er dient als Referenz-Matrix für den `legal-auditor`-Agent, der beim Scan einer Codebase erkannte npm-Pakete, Composer-Pakete, Script-Tags und Domain-Calls mit diesem Katalog abgleicht. Jede Zeile enthält das Tool, den rechtlichen Verantwortlichen (Anbieter), die Einwilligungs-Bewertung, die Drittland-Einordnung, die üblichen Code-Artefakte zur Erkennung und eine kurze Bemerkung zu Praxis-Besonderheiten.

## Legende

| Einwilligung? | Erklärung |
|---|---|
| ✅ Nicht nötig | § 25 Abs. 2 Nr. 2 TDDDG — unbedingt erforderlich für den vom Nutzer angeforderten Dienst |
| ⚠️ Bedingt | Abhängig von Konfiguration: einwilligungsfrei möglich (z. B. Self-Host ohne Cookies, Server-Side, anonymisiert) oder auf berechtigtes Interesse stützbar |
| ❌ Pflicht | § 25 Abs. 1 TDDDG — immer Opt-In vor Ladung / Ausführung |

| Drittland | Erklärung |
|---|---|
| 🇪🇺 EU | Verarbeitung in EU/EWR |
| 🇺🇸 US-DPF | USA mit EU-US Data Privacy Framework-Zertifizierung (seit 10.07.2023) |
| 🇺🇸 US-kritisch | USA ohne aktive DPF-Zertifizierung oder Tool außerhalb des Zertifizierungs-Scopes |
| 🌐 Drittland | Sonstiges Drittland — SCCs + TIA erforderlich |
| 🔀 Variabel | Anbieter bietet Region-Wahl (EU oder US) — hängt von Tenant-Konfiguration ab |

## Kategorien

### Web-Analytics (10 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Google Analytics 4 | Google LLC | ❌ | 🇺🇸 US-DPF | `gtag`, `googletagmanager.com/gtag/js`, `@next/third-parties/google` | Einwilligungspflichtig (auch IP-anonymisiert); AVV + SCCs ergänzend; Consent Mode v2 nötig |
| Plausible Analytics | Plausible Insights OÜ (Estland) | ✅ | 🇪🇺 EU (Hetzner DE) | `plausible.io/api/event`, `@plausible.io/tracker` | Cookie-frei, keine PII, laut Anbieter ohne Banner nutzbar; Self-Host (MIT) verfügbar |
| Matomo (Self-Host) | InnoCraft Ltd (NZ, Software) | ⚠️ | 🇪🇺 EU (wenn selbst gehostet) | `matomo.js`, `piwik.js`, `_paq.push` | Cookie-less-Mode + IP-Anonymisierung + respectDoNotTrack → einwilligungsfrei möglich laut Aufsichtsbehörden |
| Matomo Cloud | InnoCraft Ltd | ❌ | 🇪🇺 EU (Frankreich) | `*.matomo.cloud` | Cloud-Variante setzt Cookies standardmäßig |
| Fathom Analytics | Conva Ventures Inc. (Kanada) | ✅ | 🇺🇸 US-DPF (EU-isolated Pipeline) | `usefathom.com/script.js`, `cdn.usefathom.com` | Cookie-frei; EU-Besucher-IPs nach Schrems II auf EU-Infrastruktur isoliert |
| Simple Analytics | Simple Analytics B.V. (NL) | ✅ | 🇪🇺 EU (Niederlande) | `scripts.simpleanalyticscdn.com`, `queue.simpleanalyticscdn.com` | Cookie-frei, kein persönlicher Identifier |
| PostHog | PostHog Inc. (US) | ❌ (Default) / ⚠️ (Self-Host, cookieless) | 🔀 US-DPF oder 🇪🇺 EU (Frankfurt) | `posthog-js`, `app.posthog.com`, `eu.i.posthog.com` | PostHog Cloud EU seit 2023; Self-Host + Cookieless möglich; sonst einwilligungspflichtig |
| Mixpanel | Mixpanel Inc. | ❌ | 🇺🇸 US-DPF | `mixpanel-browser`, `api.mixpanel.com`, `api-eu.mixpanel.com` | EU-Residency via "EU Data Residency"-Tier buchbar |
| Amplitude | Amplitude Inc. | ❌ | 🇺🇸 US-DPF | `@amplitude/analytics-browser`, `api2.amplitude.com`, `api.eu.amplitude.com` | EU-Endpoint verfügbar; trotzdem Einwilligung nötig |
| Heap | Heap Inc. (Contentsquare) | ❌ | 🇺🇸 US-DPF | `heap.js`, `heapanalytics.com` | Session-Recording möglich → ggf. DSFA nötig |
| Pirsch Analytics | Emvi Software GmbH (DE) | ✅ | 🇪🇺 EU (Deutschland) | `pirsch.io/pirsch.js`, `api.pirsch.io` | Deutsches Unternehmen, Hetzner-Hosting, cookie-frei |

### Werbe- / Tracking-Pixel (10 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Meta Pixel (Facebook) | Meta Platforms Ireland Ltd. | ❌ | 🇺🇸 US-DPF | `fbq(`, `connect.facebook.net/.../fbevents.js` | Gemeinsame Verantwortlichkeit (C-210/16 Fashion ID); Joint-Controller-Vertrag nötig |
| Google Ads Conversion | Google Ireland Ltd. | ❌ | 🇺🇸 US-DPF | `gtag('event', 'conversion'`, `googleadservices.com`, `google.com/pagead` | Consent Mode v2 seit 2024 Pflicht für EU-Traffic |
| LinkedIn Insight Tag | LinkedIn Ireland | ❌ | 🇺🇸 US-DPF | `_linkedin_partner_id`, `snap.licdn.com/li.lms-analytics/insight.min.js` | |
| TikTok Pixel | TikTok Technology Ltd. (IE) / ByteDance | ❌ | 🌐 Drittland (CN-Verbindung kritisch) | `ttq.`, `analytics.tiktok.com/i18n/pixel/events.js` | TikTok-Nutzung für Behörden z. T. untersagt; DSFA ratsam |
| Pinterest Tag | Pinterest Europe Ltd. | ❌ | 🇺🇸 US-DPF | `pintrk(`, `s.pinimg.com/ct/core.js` | |
| Reddit Pixel | Reddit Inc. | ❌ | 🇺🇸 US-DPF | `rdt(`, `redditstatic.com/ads/pixel.js` | |
| Microsoft Clarity | Microsoft Corp. | ❌ | 🇺🇸 US-DPF | `clarity.ms/tag/`, `clarity('set'` | Session-Replay → DSFA-Verdacht |
| Microsoft Advertising UET | Microsoft Corp. | ❌ | 🇺🇸 US-DPF | `uetq`, `bat.bing.com/bat.js` | |
| X / Twitter Pixel | X Corp. | ❌ | 🇺🇸 US-kritisch (DPF-Status umstritten) | `twq(`, `static.ads-twitter.com/uwt.js` | |
| Outbrain Pixel | Outbrain Inc. | ❌ | 🇺🇸 US-DPF | `OB_ADV_ID`, `widgets.outbrain.com/outbrain.js` | |

### Tag-Manager (3 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Google Tag Manager | Google Ireland Ltd. | ⚠️ | 🇺🇸 US-DPF | `googletagmanager.com/gtm.js`, `dataLayer.push` | GTM-Container selbst ist umstritten: Rheinland-Pfalz-LfDI setzt Einwilligung voraus, andere Behörden bei reiner Ladung noch nicht; Consent Mode v2 einplanen |
| Adobe Launch / Tags | Adobe Inc. | ⚠️ | 🇺🇸 US-DPF | `assets.adobedtm.com/launch-*.min.js` | Analog zu GTM; Rule-Konfiguration entscheidet |
| Matomo Tag Manager | InnoCraft Ltd | ⚠️ | 🇪🇺 EU (Self-Host) | `container_*.js` auf eigener Domain | Cookie-free + Self-Host → einwilligungsfrei möglich |

### Consent Management Platforms (10 Tools)

Eine CMP selbst ist zur Einwilligungs-Erfüllung "unbedingt erforderlich" (§ 25 Abs. 2 Nr. 2 TDDDG) und benötigt keine eigene Einwilligung. Geprüft werden muss nur der Drittland-Transfer.

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Usercentrics | Usercentrics GmbH (DE) | ✅ | 🇪🇺 EU | `app.usercentrics.eu`, `cookie/v2/accept` | Deutscher Anbieter, CNIL-anerkannt |
| Cookiebot (by Usercentrics) | Cybot A/S (DK) | ✅ | 🇪🇺 EU | `consent.cookiebot.com`, `consentcloud.js` | LG Köln 23 O 172/22 zu Cookiebot + Google-Fonts-Problem prüfen (2023) |
| Klaro! | KIProtect GmbH (DE) | ✅ | 🇪🇺 EU (Self-Host) | `klaro.js`, `klaro-no-css.js` | Open-Source, self-hostbar |
| Osano | Osano Inc. (US) | ✅ | 🇺🇸 US-DPF | `cmp.osano.com`, `osano.js` | |
| Iubenda | iubenda s.r.l. (IT) | ✅ | 🇪🇺 EU | `cdn.iubenda.com`, `cs.iubenda.com` | |
| OneTrust | OneTrust LLC (US) | ✅ | 🇺🇸 US-DPF | `cdn.cookielaw.org`, `otSDKStub.js`, `otBannerSdk.js` | |
| TrustArc | TrustArc Inc. (US) | ✅ | 🇺🇸 US-DPF | `consent.trustarc.com`, `truste.js` | |
| Borlabs Cookie | Borlabs GmbH (DE) | ✅ | 🇪🇺 EU | WordPress-Plugin, `borlabs-cookie/*.js` | Marktführer im deutschen WP-Bereich |
| Complianz | Complianz B.V. (NL) | ✅ | 🇪🇺 EU | WordPress-Plugin, `complianz/*` | |
| consentmanager.net | consentmanager AB (SE) | ✅ | 🇪🇺 EU | `cdn.consentmanager.net/delivery/*.js` | IAB TCF 2.2-zertifiziert |

### Heatmap / Session-Replay (6 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Hotjar | Hotjar Ltd. (Contentsquare Gruppe, MT) | ❌ | 🇪🇺 EU (Irland) | `static.hotjar.com/c/hotjar-*.js`, `hj(` | Session-Replay → DSFA prüfen |
| Microsoft Clarity | Microsoft Corp. | ❌ | 🇺🇸 US-DPF | `clarity.ms/tag/` | Siehe Tracking-Pixel |
| FullStory | FullStory Inc. (US) | ❌ | 🇺🇸 US-DPF | `edge.fullstory.com/s/fs.js`, `FS.` | DSFA-pflichtig (umfangreiches Session-Replay) |
| LogRocket | LogRocket Inc. (US) | ❌ | 🇺🇸 US-DPF | `cdn.logrocket.io/LogRocket.min.js`, `LogRocket.init` | |
| Mouseflow | Mouseflow ApS (DK) | ❌ | 🇪🇺 EU | `cdn.mouseflow.com/projects/*.js` | |
| Smartlook | Smartlook.com s.r.o. (CZ) | ❌ | 🇪🇺 EU | `web-sdk.smartlook.com/recorder.js` | |

### Chat / Customer Support (8 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Intercom | Intercom Inc. (US) / Intercom R&D Ltd. (IE) | ❌ | 🔀 US-DPF / 🇪🇺 EU (EU-Data-Hosting buchbar) | `widget.intercom.io`, `Intercom(` | Cookies werden vor Chat-Nutzung gesetzt → Consent |
| Drift | Drift.com Inc. (Salesloft, US) | ❌ | 🇺🇸 US-DPF | `js.driftt.com/include/*.js`, `drift.load` | |
| Crisp | Crisp IM SAS (FR) | ❌ | 🇪🇺 EU (Frankreich) | `client.crisp.chat/l.js`, `CRISP_WEBSITE_ID` | Französischer Anbieter |
| Userlike | Userlike UG (DE) | ❌ | 🇪🇺 EU (Deutschland) | `userlike-cdn-widgets.s3-eu-west-1.amazonaws.com` | Deutscher Anbieter |
| tawk.to | tawk.to inc. (US) | ❌ | 🇺🇸 US-DPF | `embed.tawk.to/*/default` | Kostenlos, aber Daten in US |
| Zendesk Chat / Messaging | Zendesk Inc. (US) | ❌ | 🇺🇸 US-DPF | `static.zdassets.com/ekr/snippet.js`, `zE(` | EU-Data-Residency als Add-on |
| Freshchat | Freshworks Inc. (US) | ❌ | 🇺🇸 US-DPF | `wchat.freshchat.com/js/widget.js` | EU-Pod verfügbar |
| HubSpot Chat | HubSpot Inc. (US) | ❌ | 🇺🇸 US-DPF | `js.hs-scripts.com/*.js`, `js-eu1.hs-scripts.com` | EU-Hosting über `-eu1`-Subdomain möglich |

### E-Mail-Marketing / CRM (10 Tools)

Meist serverseitig → § 25 TDDDG nicht einschlägig. Einwilligung **für den Newsletter-Versand** folgt aus § 7 Abs. 2 Nr. 3 UWG (Double-Opt-In). Spalte "Einwilligung" bezieht sich hier auf Embed-Scripts / Trackings.

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Mailchimp | Intuit Inc. / The Rocket Science Group | ❌ (Tracking-Pixel in Mails) | 🇺🇸 US-DPF | `chimpstatic.com/mcjs-connected/js/*`, `list-manage.com` | AVV-Vorlage vorhanden |
| Brevo (ex Sendinblue) | Sendinblue SAS (FR) | ❌ (Tracking) | 🇪🇺 EU (Frankreich) | `sibautomation.com`, `sendinblue.com/bat.js` | Französischer Anbieter, DSGVO-freundlich |
| CleverReach | CleverReach GmbH & Co. KG (DE) | ❌ (Tracking) | 🇪🇺 EU (Deutschland) | `cleverreach.com/f/*` (Formulare) | Deutscher Anbieter |
| Rapidmail | Rapidmail GmbH (DE) | ❌ (Tracking) | 🇪🇺 EU (Deutschland) | `rapidmail.de/form/*` | Deutscher Anbieter |
| ActiveCampaign | ActiveCampaign LLC (US) | ❌ | 🇺🇸 US-DPF | `trackcmp.net`, `activehosted.com` | Site-Tracking setzt Cookies |
| HubSpot Marketing | HubSpot Inc. (US) | ❌ | 🇺🇸 US-DPF | `js.hs-scripts.com`, `js.hs-analytics.net`, `forms.hubspot.com` | EU-Region über `-eu1` verfügbar |
| Klaviyo | Klaviyo Inc. (US) | ❌ | 🇺🇸 US-DPF | `static.klaviyo.com/onsite/js/klaviyo.js`, `_learnq` | E-Commerce-Fokus |
| ConvertKit / Kit | Kit.com Inc. (US) | ❌ | 🇺🇸 US-DPF | `ck.convertkit.com/*`, `f.convertkit.com` | |
| SendGrid | Twilio Inc. (US) | ⚠️ (serverseitig primär) | 🇺🇸 US-DPF | `sendgrid.net`, Mail-Header `X-SG-EID` | Transaktional; Open-Tracking deaktivierbar |
| Resend | Resend Inc. (US) | ⚠️ (serverseitig) | 🇺🇸 US-DPF | `resend.com/api`, npm `resend` | Neuer Anbieter, AVV vorhanden |

### Payment (6 Tools)

Payment-Provider sind üblicherweise "zur Vertragsanbahnung unbedingt erforderlich" (§ 25 Abs. 2 Nr. 2 TDDDG) — dies umfasst allerdings nur die Zahlungsabwicklung selbst, nicht Anti-Fraud-/Advertising-Cookies.

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Stripe | Stripe Inc. (US) / Stripe Payments Europe (IE) | ✅ (Checkout) / ❌ (Stripe Radar vor Checkout) | 🇺🇸 US-DPF | `js.stripe.com/v3/`, `@stripe/stripe-js`, `@stripe/react-stripe-js` | Stripe.js lädt Fraud-Detection-Fingerprint — LG Münster 016 O 103/24 (2024) zur Einwilligungsfrage beachten |
| PayPal | PayPal (Europe) S.à r.l. (LU) | ✅ (Checkout) / ❌ (Button-Tracking) | 🇪🇺 EU (Luxemburg, Transfers an US-Mutter) | `paypal.com/sdk/js`, `@paypal/react-paypal-js` | SDK lädt Tracking, vor Checkout-Klick Einwilligung empfohlen |
| Mollie | Mollie B.V. (NL) | ✅ | 🇪🇺 EU (Niederlande) | `api.mollie.com`, Composer `mollie/mollie-api-php` | EU-Anbieter, DSGVO-freundlich |
| Adyen | Adyen N.V. (NL) | ✅ | 🇪🇺 EU (Niederlande) | `checkoutshopper-live.adyen.com`, `@adyen/adyen-web` | EU-Anbieter |
| Braintree | Braintree (PayPal, US) | ✅ (Checkout) / ❌ (Fraud-Pixel) | 🇺🇸 US-DPF | `js.braintreegateway.com/web/*`, `braintree-web` | |
| Klarna | Klarna Bank AB (SE) | ✅ (Checkout) / ❌ (On-Site-Messaging-Widget) | 🇪🇺 EU (Schweden) | `x.klarnacdn.net/kp/lib/*.js`, `klarna-payments` | Klarna Messaging → Cookies & Einwilligung |

### Fonts / CDN (6 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Google Fonts (remote) | Google Ireland Ltd. | ❌ | 🇺🇸 US-DPF | `fonts.googleapis.com`, `fonts.gstatic.com` | **LG München I 3 O 17493/20** (20.01.2022): 100 € Schmerzensgeld bei remote-Einbindung ohne Einwilligung — Self-Host Pflicht-Praxis |
| Google Fonts (self-host) | lokal ausgeliefert | ✅ | 🇪🇺 EU (eigener Server) | `/fonts/*.woff2`, `@fontsource/*` (npm) | DSGVO-unkritisch |
| Adobe Fonts (Typekit) | Adobe Inc. (US) | ❌ | 🇺🇸 US-DPF | `use.typekit.net/*.js`, `p.typekit.net` | Lädt Tracking-Kit; Einwilligung erforderlich |
| Fontsource | Community / OSS | ✅ | 🇪🇺 EU (lokal) | `@fontsource/<font>` (npm) | 1500+ Fonts als npm-Paket, lokal gebundled |
| Bunny Fonts | BunnyWay d.o.o. (SI) | ✅ | 🇪🇺 EU (Slowenien) | `fonts.bunny.net/css` | Google-Fonts-API-kompatibel, kein Logging |
| jsDelivr | Prospect One (PL) | ⚠️ | 🇪🇺 EU (Polen) / Multi-CDN | `cdn.jsdelivr.net/*` | IP geht an CDN; für Libraries i. d. R. "unbedingt erforderlich" |
| cdnjs (Cloudflare) | Cloudflare Inc. (US) | ⚠️ | 🇺🇸 US-DPF | `cdnjs.cloudflare.com/ajax/libs/*` | IP an Cloudflare; Self-Host empfohlen |

### Video- / Media-Embed (6 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| YouTube Embed | Google Ireland Ltd. | ❌ | 🇺🇸 US-DPF | `youtube.com/embed/*`, `<iframe src="youtube.com/embed`, `react-player` | Selbst `youtube-nocookie.com` setzt Cookies bei Play-Click → 2-Klick-Lösung + Einwilligung |
| Vimeo Embed | Vimeo.com Inc. (US) | ❌ | 🇺🇸 US-DPF | `player.vimeo.com/video/*`, `@vimeo/player` | "Do-Not-Track"-Mode: `?dnt=1`-Parameter reduziert Tracking |
| Wistia | Wistia Inc. (US) | ❌ | 🇺🇸 US-DPF | `fast.wistia.com/embed/*`, `wistia-player` | |
| Cloudflare Stream | Cloudflare Inc. (US) | ❌ | 🇺🇸 US-DPF | `customer-*.cloudflarestream.com`, `embed.cloudflarestream.com` | |
| Mux | Mux Inc. (US) | ❌ | 🇺🇸 US-DPF | `stream.mux.com/*`, `@mux/mux-player` | |
| Loom | Loom Inc. / Atlassian (US) | ❌ | 🇺🇸 US-DPF | `loom.com/embed/*`, `cdn.loom.com` | |

### Form-Builder (5 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Typeform | Typeform S.L. (ES) | ❌ | 🇪🇺 EU (Spanien) | `embed.typeform.com/next/embed.js`, `@typeform/embed` | EU-Anbieter; Form-Embed setzt Cookies |
| Jotform | Jotform Inc. (US) | ❌ | 🇺🇸 US-DPF | `form.jotform.com/jsform/*`, `cdn.jotfor.ms` | EU-Safe-Mode mit EU-Servern buchbar |
| Tally | Tally Forms bvba (BE) | ✅ (Basic) | 🇪🇺 EU (Belgien) | `tally.so/embed/*`, `tally.so/widgets/embed.js` | Cookie-frei-Default |
| Formspree | Formspree Inc. (US) | ⚠️ (serverseitig) | 🇺🇸 US-DPF | `formspree.io/f/*` als `<form action>` | Nur Form-Submit → serverseitig, keine Client-Cookies |
| Google Forms | Google Ireland Ltd. | ❌ | 🇺🇸 US-DPF | `docs.google.com/forms/*`, `<iframe src="docs.google.com/forms` | Lädt Google-Cookies |

### Error / Monitoring (6 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Sentry | Functional Software Inc. (US) / Sentry GmbH (DE, EU-Tenant) | ⚠️ | 🔀 US-DPF / 🇪🇺 EU (de.sentry.io) | `@sentry/browser`, `@sentry/nextjs`, `Sentry.init` | Error-Monitoring kann als "unbedingt erforderlich" eingeordnet werden (Sicherheit), wenn `sendDefaultPii: false` und Session-Replay aus |
| Datadog RUM | Datadog Inc. (US) | ❌ | 🇺🇸 US-DPF | `@datadog/browser-rum`, `datadoghq.com`, `datadoghq.eu` | EU-Site als `.eu`-Domain |
| Rollbar | Rollbar Inc. (US) | ⚠️ | 🇺🇸 US-DPF | `rollbar.com/rollbar.js`, `@rollbar/browser` | |
| Bugsnag | SmartBear / Insight Hub | ⚠️ | 🇺🇸 US-DPF | `@bugsnag/js`, `notify.bugsnag.com` | |
| LogRocket | LogRocket Inc. (US) | ❌ | 🇺🇸 US-DPF | `cdn.logrocket.io/LogRocket.min.js` | Session-Replay → Einwilligung zwingend |
| Raygun | Raygun Ltd. (NZ) | ⚠️ | 🌐 Drittland (Neuseeland hat EU-Angemessenheitsbeschluss) | `cdn.raygun.io/*.js`, `Raygun.init` | Neuseeland Angemessenheits-Level |

### Social-Media-Embeds (8 Tools)

Alle Social Plugins setzen Cookies beim Laden und übertragen IP + User-Agent an den Plattform-Betreiber (C-210/16 "Fashion ID"). Konsequenz: Einwilligung + 2-Klick-Lösung. Alternative: statische Vorschau-Bilder + Deep-Link.

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Facebook Like / Share | Meta Platforms Ireland | ❌ | 🇺🇸 US-DPF | `connect.facebook.net/*/sdk.js`, `fb-root`, `fb:like` | Joint-Controller (C-210/16) |
| X / Twitter Embed | X Corp. | ❌ | 🇺🇸 US-kritisch | `platform.twitter.com/widgets.js`, `<blockquote class="twitter-tweet">` | DPF-Status umstritten |
| Instagram Embed | Meta Platforms Ireland | ❌ | 🇺🇸 US-DPF | `www.instagram.com/embed.js`, `<blockquote class="instagram-media">` | |
| LinkedIn Embed | LinkedIn Ireland | ❌ | 🇺🇸 US-DPF | `platform.linkedin.com/in.js`, `<script type="IN/*">` | |
| YouTube Embed | Google Ireland | ❌ | 🇺🇸 US-DPF | s. Video/Media | nocookie-Variante erlaubt, trotzdem Einwilligung |
| TikTok Embed | TikTok Technology Ltd. | ❌ | 🌐 Drittland | `www.tiktok.com/embed.js`, `<blockquote class="tiktok-embed">` | China-Mutterkonzern; DSFA erwägen |
| Pinterest Embed | Pinterest Europe | ❌ | 🇺🇸 US-DPF | `assets.pinterest.com/js/pinit.js` | |
| Reddit Embed | Reddit Inc. | ❌ | 🇺🇸 US-DPF | `embed.redditmedia.com/widgets/platform.js` | |

### Maps (4 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Google Maps (Embed / API) | Google Ireland Ltd. | ❌ | 🇺🇸 US-DPF | `maps.googleapis.com/maps/api/js`, `<iframe src="google.com/maps/embed">` | Lädt Google-Cookies; 2-Klick-Lösung oder Static-Map-Variante |
| Mapbox | Mapbox Inc. (US) | ⚠️ | 🇺🇸 US-DPF | `api.mapbox.com`, `mapbox-gl.js`, `react-map-gl` | IP an Mapbox, Telemetry deaktivierbar |
| Leaflet + OpenStreetMap | OpenStreetMap Foundation (UK) | ✅ | 🇪🇺 EU (Tile-Server in DE verfügbar) | `leaflet.js`, `tile.openstreetmap.org` | Tile-IP-Transfer; i. d. R. unproblematisch |
| MapLibre GL JS | MapLibre Community / OSS | ✅ | 🇪🇺 EU (wenn EU-Tiles) | `maplibre-gl.js`, `maplibre-gl-js` | Fork von Mapbox GL JS; Tile-Provider konfigurierbar |

### A/B-Testing (4 Tools)

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| Google Optimize | Google (abgekündigt 30.09.2023) | — | — | `googleoptimize.com/optimize.js` | **Nicht mehr verfügbar** — bei Fund in Code: Dead-Code, entfernen |
| VWO | Wingify Software Pvt. Ltd. (IN) | ❌ | 🌐 Drittland (Indien, kein Angemessenheitsbeschluss) | `dev.visualwebsiteoptimizer.com/lib/*.js`, `_vwo_code` | SCCs + TIA nötig |
| Optimizely | Optimizely Inc. (US) | ❌ | 🇺🇸 US-DPF | `cdn.optimizely.com/js/*.js`, `optimizelyDataClient` | |
| Unbounce | Unbounce Marketing Solutions Inc. (CA) | ❌ | 🌐 Drittland (Kanada hat EU-Angemessenheitsbeschluss, 2001/2019) | `unbouncepages.com`, `d3pkntwtp2ukl5.cloudfront.net` | Kanada-Angemessenheit erleichtert Transfer |

### AI / ML APIs (6 Tools)

Alle AI-APIs sind **serverseitig** — § 25 TDDDG greift nur bei clientseitigem Embed (Chat-Widget). AVV-Abschluss und Drittland-Bewertung stehen im Vordergrund.

| Tool | Anbieter | Einwilligung | Drittland | Code-Spur | Bemerkung |
|---|---|---|---|---|---|
| OpenAI API | OpenAI LLC (US) | ⚠️ (serverseitig) | 🇺🇸 US-DPF | `openai` (npm/pip), `api.openai.com/v1/*` | AVV-Vorlage unter `openai.com/policies/data-processing-addendum`; EU-Residency Okt. 2024 angekündigt |
| Anthropic Claude | Anthropic PBC (US) | ⚠️ (serverseitig) | 🇺🇸 US-DPF | `@anthropic-ai/sdk`, `anthropic` (pip), `api.anthropic.com` | DPA vorhanden; Default: 30 Tage Retention (Zero-Retention auf Antrag) |
| Mistral AI | Mistral AI SAS (FR) | ⚠️ (serverseitig) | 🇪🇺 EU (Frankreich) | `@mistralai/mistralai`, `api.mistral.ai` | EU-Anbieter |
| Azure OpenAI | Microsoft Ireland (EU-Region) | ⚠️ (serverseitig) | 🔀 🇪🇺 EU / 🇺🇸 US-DPF (Region-Wahl) | `openai.azure.com`, `@azure/openai` | EU-Regionen (`westeurope`, `germanywestcentral`) verfügbar |
| Google Gemini / Vertex AI | Google Ireland | ⚠️ (serverseitig) | 🔀 🇪🇺 EU / 🇺🇸 US-DPF | `generativelanguage.googleapis.com`, `@google/generative-ai` | Vertex AI mit EU-Region; Gemini-API meist US |
| Cohere | Cohere Inc. (CA) | ⚠️ (serverseitig) | 🌐 Drittland (Kanada angemessen) | `cohere-ai` (npm), `api.cohere.com` | |

## Nicht im Katalog (expliziter Verweis)

Zu Tools, die nicht hier gelistet sind: Einordnung per ad-hoc-Check. Ein Tool ist **generell einwilligungsbedürftig**, wenn es mindestens eines der folgenden Kriterien erfüllt:

1. Es setzt Cookies oder nutzt Local/Session-Storage vor einer expliziten Nutzer-Aktion (§ 25 Abs. 1 TDDDG)
2. Es überträgt personenbezogene Daten (IP-Adresse, User-Agent, Client-ID, Fingerprint) an einen Drittanbieter, der nicht als Auftragsverarbeiter agiert
3. Es greift **kein** Ausnahmetatbestand nach § 25 Abs. 2 Nr. 2 TDDDG (unbedingt erforderlich für den vom Nutzer angeforderten Dienst)

**Prüf-Workflow für neues Tool:**
1. Anbieter-URL / npm-Registry / Datenschutzerklärung des Anbieters lesen
2. DPF-Liste prüfen: https://www.dataprivacyframework.gov/list (Active-Status)
3. AVV-Vorlage beim Anbieter suchen
4. Self-Host-Option prüfen
5. Bei Unklarheit: `legal-auditor`-Agent oder Datenschutzbeauftragten einschalten

## Config-Hinweise pro Haupttool

### Google Analytics 4 — datenschutzkonform einbinden

- **IP-Anonymisierung**: seit GA4 Default (nicht mehr abschaltbar); Vorgänger UA nutzte `anonymizeIp: true`.
- **Google Signals**: in GA4 deaktivieren, wenn keine separate Einwilligung für Cross-Device-Tracking vorliegt.
- **User-ID / User-Properties**: nur mit ausdrücklicher Einwilligung befüllen.
- **Consent Mode v2**: seit März 2024 Pflicht; setzt die Default-Consent-Signale (`ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`) standardmäßig auf `denied` und erst nach CMP-Entscheidung auf `granted`.
- **AVV**: im GA4-Admin → "Konten-Einstellungen" → "Datenverarbeitung für Werbung" akzeptieren.
- **Data-Retention**: auf 2 Monate reduzieren (Standard 14 Monate).

### Google Tag Manager — datenschutzkonform einbinden

- GTM-Container erst nach Consent laden (z. B. via CMP-Integration).
- Consent Mode v2 in GTM-Workspace aktivieren; jede Tag-Definition erhält eine Consent-Anforderung (`analytics_storage`, `ad_storage`).
- Server-Side GTM (sGTM) bietet bessere DSGVO-Position: First-Party-Domain + serverseitige Proxy-Verarbeitung.
- Vorsicht: GTM selbst ist umstritten — mehrere LfDIs (insb. LfDI Rheinland-Pfalz, Baden-Württemberg) fordern Einwilligung schon für das Laden des Containers.

### Meta Pixel — datenschutzkonform einbinden

- Joint-Controller-Vertrag mit Meta (Art. 26 DSGVO) abschließen: https://www.facebook.com/legal/controller_addendum
- Pixel erst nach Einwilligung laden (Hard-Blocking im CMP).
- **Advanced Matching** (gehashte E-Mail/Telefon) nur mit separater Einwilligung.
- **Conversions API (CAPI)** ist serverseitig, aber rechtlich identisch bewertet → ebenfalls Einwilligung nötig.
- Datenschutzerklärung muss Fashion-ID-Joint-Controllership benennen.

### Stripe — datenschutzkonform einbinden

- `js.stripe.com/v3/` erst auf der Checkout-Seite laden — nicht global einbetten. Stripe Radar (Fraud-Detection) sammelt Browser-Fingerprint bei jedem Load.
- **Stripe Payment Element / Checkout Session**: primäre Nutzung ist "unbedingt erforderlich" (Art. 6 Abs. 1 lit. b DSGVO, Vertragsanbahnung).
- DPA bei Stripe aktivieren: Dashboard → Settings → Legal → "Data Processing Agreement" akzeptieren.
- **LG Münster 016 O 103/24** (Juli 2024): Zu globalem Stripe.js-Embed ohne Einwilligung siehe Urteils-Eintrag.
- SCCs sind Teil des Stripe-DPA (Modul 2, Controller→Processor).

### YouTube-Embed — privacy-enhanced

- `youtube-nocookie.com/embed/VIDEO_ID` statt `youtube.com/embed/VIDEO_ID` verwenden.
- **Trotzdem**: YouTube setzt beim Play-Click Cookies (`VISITOR_INFO1_LIVE`, `YSC`, `PREF`) → Einwilligung bleibt erforderlich.
- **Empfehlung 2-Klick-Lösung**: Statisches Thumbnail-Bild + "Video anzeigen"-Button; erst nach Klick wird `<iframe>` eingebunden.
- React-Implementierung: `react-lite-youtube-embed` (https://github.com/ibrahimcesar/react-lite-youtube-embed) bindet Placeholder + on-demand Loading.

### Google Fonts — lokal einbinden

- `@fontsource/<font-name>` via npm installieren, im Build-Prozess gebundled.
- Alternative 1: Self-Host per CSS `@font-face` aus `/public/fonts/` (woff2-Dateien von google-webfonts-helper.herokuapp.com beziehen).
- Alternative 2: Bunny Fonts (`fonts.bunny.net`) als API-kompatibler Proxy.
- **LG München I, 3 O 17493/20** (20.01.2022): Remote-Einbindung ohne Einwilligung = DSGVO-Verstoß, 100 € immaterieller Schaden.
- Next.js-Spezifikum: `next/font/google` lädt Fonts **build-time** und self-hostet sie automatisch seit Next 13.

### Intercom — datenschutzkonform einbinden

- Intercom-Widget erst nach Consent laden, nicht im `<head>`.
- **EU-Data-Hosting** ("EU Regional Data Hosting") im Intercom-Admin aktivieren → Daten bleiben in Irland/Dublin (Zusatzkosten).
- DPA bei Intercom im Admin-Panel signieren: Settings → Data Privacy → "Data Processing Addendum".
- User-Identification (`intercomSettings.user_id`) nur mit Einwilligung setzen — sonst anonymer Modus.

### Sentry — datenschutzkonform einbinden

- `@sentry/browser` mit `sendDefaultPii: false` initialisieren (Default).
- `beforeSend`-Hook nutzen, um sensible Daten (Auth-Header, Body) zu entfernen.
- **Session Replay** nur mit Einwilligung aktivieren — standardmäßig aus.
- EU-Region über `sentry.io/organizations/*/settings/data-region/` wählen (`de.sentry.io` Endpoint).
- DPA bei Sentry GmbH (EU-Entity) signieren.

## Siehe auch

- [[themen/cookie-consent]]
- [[themen/tracking-analytics]]
- [[themen/drittland-transfer]]
- [[themen/avv-muster]]
- [[themen/datenschutzerklaerung]]
- [[gesetze/tdddg]]
- [[gesetze/dsgvo]]
- [[urteile/bgh-google-fonts]]
- [[urteile/lg-muenchen-google-fonts]]
- [[checklisten/tool-einfuehrung]]
