---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/ddg/__5.html
quellen-sekundaer:
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62017CJ0040
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62016CJ0210
  - https://www.gesetze-bayern.de/Content/Document/MStV-18
  - https://www.heise.de/extras/socialmedia/
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

# Social-Media-Profile & Plugins — Datenschutz und Impressum

## Kurz-Ueberblick

Jedes geschaeftlich genutzte Social-Media-Profil (Facebook-Seite, Instagram-Business,
TikTok-Business, X-Company, LinkedIn Company Page, YouTube-Kanal, Pinterest-Business)
ist ein **Telemedium** im Sinne des DDG und unterliegt damit:

1. **Impressumspflicht** (§ 5 DDG; bei journalistisch-redaktionellen Inhalten zusaetzlich § 18 MStV)
2. **Datenschutzerklaerungspflicht** (Art. 13 DSGVO) — trotz technischer Einschraenkungen
   der Plattform (kein eigenes Dokument? dann als Link in Bio/Info/Verknuepfung)
3. **Gemeinsame Verantwortlichkeit** mit Plattform-Betreiber gemaess Art. 26 DSGVO
   (Joint-Controller-Agreement mit Meta/TikTok/X/LinkedIn/Google ist zwingend)

Ebenso fallen **eingebettete Social-Media-Plugins** (Like-Button, Share-Button,
YouTube-Embed, Instagram-Feed-Widget) auf der eigenen Website unter diese Regeln.
Seit EuGH "Fashion ID" ist der Website-Betreiber fuer die **Erhebung und
Uebermittlung** der Daten gemeinsam verantwortlich.

## Schluesselparagraphen / Kernaussagen

### § 5 DDG (Allgemeine Informationspflichten — Impressum)

Diensteanbieter muessen folgende Angaben **"leicht erkennbar, unmittelbar
erreichbar und staendig verfuegbar"** halten:

1. Name und Anschrift (bei juristischen Personen Rechtsform + Vertretungsberechtigte)
2. Angaben fuer schnelle elektronische Kontaktaufnahme (E-Mail)
3. Ggf. zustaendige Aufsichtsbehoerde
4. Handelsregister + Nummer
5. Bei reglementierten Berufen: Berufskammer, Berufsbezeichnung, Regelungsstaat
6. USt-ID / Wirtschafts-ID
7. Ggf. Abwicklung/Liquidation
8. Bei audiovisuellen Diensten: Sitzland + Regulierungsbehoerde

### § 18 Abs. 2 MStV (Journalistisch-redaktionell)

> "Anbieter von Telemedien mit journalistisch-redaktionell gestalteten Angeboten
> […] haben zusaetzlich einen Verantwortlichen mit Angabe des Namens und der
> Anschrift zu benennen."

**Trifft zu**, wenn die Seite regelmaessig Nachrichten, Meinungsbeitraege oder
Analysen veroeffentlicht — also bei fast jedem Content-Marketing-Account.

### § 18 Abs. 3 MStV (Social Bots / KI-Content)

> "Anbieter von Telemedien in sozialen Netzwerken sind verpflichtet, bei mittels
> eines Computerprogramms automatisiert erstellten Inhalten […] den Umstand der
> Automatisierung kenntlich zu machen."

Siehe dazu ausfuehrlich [[ki-transparenz]].

### Art. 26 DSGVO (Gemeinsam Verantwortliche)

Fanpage-Betreiber und Plattform-Betreiber sind **gemeinsam** verantwortlich.
Das verlangt:

- Joint-Controller-Vereinbarung (wird von Meta, LinkedIn etc. bereitgestellt)
- Transparente Information der Betroffenen (Art. 26 Abs. 2 DSGVO)
- Zugaenglichkeit der wesentlichen Inhalte fuer Betroffene

## Typische Fallstricke in Codebases / Webseiten

| Problem | Risiko | Fix |
|---|---|---|
| Social-Media-Icons als Hotlink auf Plattform (Facebook-Icon laedt `facebook.com/plugins/...`) | Datenuebermittlung an US-Server **vor Einwilligung** (Drittland-Transfer, siehe [[drittland-transfer]]) | Shariff-Button (lokal) oder 2-Klick-Loesung |
| `<iframe src="youtube.com/...">` ohne Einwilligung | YouTube setzt Cookies + traegt IP an Google US | `youtube-nocookie.com` + Consent-Gate |
| Instagram-Feed-Widget (embed) | Meta-Tracking aktiv | Serverseitiger Feed-Proxy oder Consent-Gate |
| Fehlendes Impressum im TikTok-Profil (nur Link in Bio) | § 5 DDG-Verstoss, Abmahnrisiko | Impressum-Link in Bio (Linktree, eigene Domain) |
| Datenschutzerklaerung fehlt auf Fanpage | EuGH C-210/16 | DSE auf eigener Website + Verlinkung im "Info"-Bereich |
| Kein Joint-Controller-Agreement mit Meta unterzeichnet | Art. 26 DSGVO-Verstoss | Meta-Anhang "Informationen zu Page Insights" akzeptieren + referenzieren |

## Relevanz fuer Codebase-Typen

### Next.js SaaS / Landingpage

```tsx
// FALSCH — direkter Embed laedt Drittanbieter vor Consent
<iframe src="https://www.youtube.com/embed/xyz" />

// RICHTIG — nur nach Consent + nocookie-Variante
{hasConsent('youtube') && (
  <iframe src="https://www.youtube-nocookie.com/embed/xyz" />
)}
```

Siehe [[cookie-consent]] fuer Consent-Management.

### E-Commerce

- Produkt-Seiten mit "Share on Facebook"-Buttons: Shariff einsetzen
- Bewertungs-Widgets (Trustami, Trusted Shops) pruefen auf Plugin-Charakter

### Content/Blog

- RSS-Feed-Autoposting auf X/LinkedIn: Impressum **im Profil** pflegen
- Embed-Codes (Twitter-Blockquote, Instagram-Embed) auditieren

### n8n

- Wenn n8n-Workflows automatisiert Social-Media-Posts erstellen: § 18 Abs. 3 MStV
  verlangt Kennzeichnung als automatisiert erstellter Inhalt

## Behoerden-Hinweise / Gerichtspraxis

- **BayLDA, LfDI Baden-Wuerttemberg, LfD Niedersachsen**: mehrfach Hinweise,
  dass Betrieb von Facebook-Fanpages ohne JCA unzulaessig ist
- **DSK-Entschliessung vom 05.09.2018**: Fanpage-Betreiber muessen ihren
  datenschutzrechtlichen Pflichten nachkommen
- **Konferenz der unabhaengigen Datenschutzaufsichtsbehoerden** (Positionspapier 2022):
  Facebook-Fanpages nur rechtskonform betreibbar, wenn alle Anforderungen
  (inkl. Drittlandtransfer nach Schrems II) erfuellt sind

## Zitierbare Urteile

### EuGH C-210/16 (Wirtschaftsakademie Schleswig-Holstein), 05.06.2018

> Der Betreiber einer auf Facebook unterhaltenen Fanpage ist gemeinsam mit
> Facebook fuer die Verarbeitung der personenbezogenen Daten der Besucher seiner
> Seite i.S.v. Art. 2 Buchst. d der Richtlinie 95/46/EG verantwortlich.

Kernfolge: Joint-Controller-Pflicht auch ohne Zugriff auf die Rohdaten.

### EuGH C-40/17 (Fashion ID), 29.07.2019

> Der Betreiber einer Website, der in diese ein Social-Plugin [Facebook Like-Button]
> einbindet, […] ist fuer die Verarbeitungsvorgaenge der Erhebung und
> Uebermittlung der personenbezogenen Daten der Besucher seiner Website an
> Facebook gemeinsam mit diesem Anbieter verantwortlich.

Kernfolge: Pflicht zur Einwilligung **vor** Laden des Plugins; Shariff-/2-Klick-
Loesung praxisueblich.

### VG Schleswig-Holstein, 4 LA 12/23 (2024) `<<VERIFIKATION AUSSTEHEND>>`

Bestaetigung der Anordnung gegenueber oeffentlichen Stellen, Facebook-Fanpages
abzuschalten. Aktenzeichen noch final zu verifizieren.

## Praxis-Check (Was Code-Reviewer konkret pruefen)

- [ ] Jede Social-Media-Profil-Bio/Info enthaelt einen **direkten Link** auf
      Impressum und Datenschutzerklaerung der eigenen Website
- [ ] Datenschutzerklaerung der eigenen Website enthaelt Abschnitte zu allen
      genutzten Plattformen (FB/IG/X/TT/LI/YT/Pin)
- [ ] Joint-Controller-Agreement (Meta "Page Insights Anhang", LinkedIn,
      TikTok Page Insights) dokumentiert abgehakt
- [ ] Keine Plugin-Scripts (facebook-sdk, twitter-widgets, youtube-embed)
      laden **vor** Consent
- [ ] Fuer YouTube-Embeds: `youtube-nocookie.com`-Domain verwendet
- [ ] Fuer Instagram-Embeds: serverseitiger Proxy oder Consent-Gate
- [ ] Automatisierte Posts sind als "automatisiert erstellt" gekennzeichnet
      (§ 18 Abs. 3 MStV)
- [ ] Netzwerk-Analyse (DevTools) zeigt **keine** Requests an Drittdienste
      vor Klick auf "Akzeptieren"

## Einsatzfertiger DSE-Passus (zum Einbinden in die eigene Datenschutzerklaerung)

> **Social Media und Einbindung externer Inhalte**
>
> Auf unserer Website sind Buttons/Verlinkungen zu unseren Profilen in folgenden
> sozialen Netzwerken integriert: [Facebook, Instagram, X, LinkedIn, YouTube,
> TikTok, Pinterest]. Die Buttons laden **keine** Inhalte der Plattformen, bevor
> Sie nicht aktiv darauf geklickt haben (2-Klick-Loesung / Shariff).
>
> Beim Besuch unserer Profile auf diesen Plattformen werden personenbezogene
> Daten durch den Plattformbetreiber verarbeitet. Fuer die Verarbeitung durch
> den Plattformbetreiber sind wir **gemeinsam mit** diesem verantwortlich
> (Art. 26 DSGVO). Die wesentlichen Inhalte der Vereinbarungen finden Sie unter:
>
> - Meta (Facebook/Instagram): https://www.facebook.com/legal/terms/page_controller_addendum
> - LinkedIn: https://legal.linkedin.com/pages-joint-controller-addendum
> - X (Twitter): https://twitter.com/de/privacy
> - TikTok: https://www.tiktok.com/legal/page/eea/privacy-policy/de
> - YouTube (Google): https://policies.google.com/privacy
> - Pinterest: https://policy.pinterest.com/de/privacy-policy
>
> Rechtsgrundlage der Einbindung ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes
> Interesse an Praesenz) bzw. Art. 6 Abs. 1 lit. a DSGVO (Einwilligung) beim
> Laden eingebetteter Plattform-Inhalte.

Siehe [[datenschutzerklaerung]] fuer vollstaendige Struktur.

## Siehe auch

- [[impressum]] — allgemeine Impressumspflicht nach § 5 DDG
- [[datenschutzerklaerung]] — Pflicht-Sections der DSE
- [[cookie-consent]] — Consent-Management fuer Plugin-Loads
- [[drittland-transfer]] — Schrems II, Meta/Google als US-Dienste
- [[tracking-analytics]] — Social-Pixel (Meta-Pixel, LinkedIn Insight Tag)
- [[ki-transparenz]] — Kennzeichnung automatisierter Inhalte (§ 18 MStV)
- [[verarbeitungsverzeichnis]] — Eintrag fuer Social-Media-Verarbeitungen
