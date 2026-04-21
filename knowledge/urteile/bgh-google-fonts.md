---
aktualisiert: 2026-04-19
quelle-primaer: https://dejure.org/dienste/vernetzung/rechtsprechung?Text=3+O+17493/20
quellen-sekundaer:
  - https://www.ra-plutte.de/lg-muenchen-dynamische-einbindung-google-web-fonts-ist-dsgvo/
  - https://www.it-recht-kanzlei.de/lg-muenchen-I-webfonts-einwilligung-schadensersatz.html
verifiziert-am: 2026-04-19
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-04-19

# LG München I 3 O 17493/20 — „Google Fonts"

## Kurz-Überblick

Das Landgericht München I hat am 20. Januar 2022 entschieden, dass die dynamische Einbindung von Google Fonts (Laden von Google-CDN-Servern) ohne Einwilligung der Website-Besucher rechtswidrig ist und einen Schadenersatzanspruch in Höhe von 100 EUR nach Art. 82 DSGVO begründet. Das Urteil hat eine deutschlandweite Abmahnwelle ausgelöst und den Umgang mit externen Web-Fonts, CDNs und Third-Party-Ressourcen verändert.

**Achtung:** Trotz Dateiname wurde das Urteil vom LG München I erlassen, **nicht** vom BGH. Der Titel der Datei orientiert sich am Auftrag; inhaltlich handelt es sich um das Google-Fonts-Urteil.

## Eckdaten

| Feld | Wert |
|------|------|
| **Aktenzeichen** | 3 O 17493/20 |
| **Datum** | 20.01.2022 |
| **Gericht** | Landgericht München I, 3. Zivilkammer |
| **Parteien** | Privatkläger (Website-Besucher) gegen Website-Betreiber |
| **Streitwert** | Unterlassung + 100 EUR Schadenersatz |

## Sachverhalt

Der Kläger besuchte die Website des Beklagten. Die Website hatte Google Fonts **dynamisch** eingebunden — d. h. die Schriftarten wurden bei jedem Seitenaufruf von fonts.googleapis.com / fonts.gstatic.com (Google Server in den USA) nachgeladen. Dabei wurde die IP-Adresse des Besuchers automatisch an Google übertragen, **ohne** dass eine Einwilligung vorlag. Der Kläger beantragte Unterlassung und Schadenersatz.

## Tenor / Ergebnis

1. **Unterlassungsanspruch** bejaht: Beklagter muss die dynamische Einbindung ohne Einwilligung unterlassen
2. **Schadenersatz nach Art. 82 DSGVO:** 100 EUR für immateriellen Schaden
3. **Begründung:** Die automatische Weitergabe der IP-Adresse an Google stellt einen Eingriff in das allgemeine Persönlichkeitsrecht und Recht auf informationelle Selbstbestimmung dar, der nicht durch ein berechtigtes Interesse nach Art. 6 Abs. 1 lit. f DSGVO gedeckt ist — weil die lokale Einbindung (self-hosted) gleichwertig möglich und damit erforderlich wäre.

## Kernaussagen

### Personenbezug der IP-Adresse

- Bestätigt EuGH C-582/14 (Breyer): IP-Adresse ist personenbezogenes Datum
- Auch dynamische IP genügt, wenn Verknüpfung mit zusätzlichen Infos möglich

### Fehlendes berechtigtes Interesse (Art. 6 Abs. 1 lit. f)

- **Erforderlichkeit fehlt:** Google Fonts können ohne IP-Übertragung bezogen werden (Download und lokales Hosting)
- Kontrollverlust über eigene Daten durch Übertragung an Google („unternehmen, das dafür bekannt ist, Nutzerdaten zu sammeln") ist unverhältnismäßig

### Immaterieller Schaden

- „**Individuelles Unwohlsein**" durch Kontrollverlust genügt
- 100 EUR als Mindestbetrag zur Abschreckung / Prävention

## Kritik und spätere Entwicklungen

### Abmahnwelle 2022/2023

Kurz nach dem Urteil starteten mehrere Abmahnanwälte und angebliche „Betroffene" (oft über automatisierte Crawler) Serienabmahnungen. Viele Forderungen zwischen 100 EUR und 500 EUR. Einige wurden als Rechtsmissbrauch eingestuft:
- **AG München 142 C 12415/22, 30.03.2023** — Rechtsmissbräuchliche Serienabmahnungen unzulässig
- **LG München I 4 O 14719/22, 30.03.2023** — Keine Rechtsgrundlage bei automatisiertem Massenklagen-Geschäftsmodell

### Weitere Gerichte zur Thematik

- **AG Charlottenburg 217 C 40/23, 09.11.2023** — bestätigt 100 EUR bei missbrauchsfreier Klage
- **OLG Köln (verschiedene)** — differenzierte Betrachtung je nach Intensität

### EuGH-Einfluss (C-300/21, Österreichische Post, 04.05.2023)

Der EuGH hat klargestellt, dass **bloßer Kontrollverlust nicht automatisch** immaterieller Schaden ist — aber Befürchtungen / Gefühle können genügen (C-687/21). Damit wackelt die LG-München-Linie teilweise, bleibt aber dem Grunde nach bestätigt.

## Praktische Folgen für Codebases

- **Google Fonts selbst hosten:** `@fontsource/...`, Next.js `next/font/google` (lädt zur Build-Zeit, keine Laufzeit-Requests an Google)
- **Alle CDN-Fonts und -Assets prüfen:**
  - fonts.googleapis.com, fonts.gstatic.com
  - use.fontawesome.com (Font Awesome CDN)
  - jsDelivr, unpkg mit personenbezogenen Daten-Inhalten
- **Google Maps, reCAPTCHA, YouTube:** gleiche Problematik — siehe Cookie-Consent
- **Selbst gehostete Alternativen:**
  - **Fonts:** @fontsource, lokale Dateien
  - **Icons:** SVG-Sprites, Iconify selbst hosten
  - **Captcha:** hCaptcha (CF-EU), Turnstile, Friendly Captcha
  - **Maps:** MapLibre + OpenStreetMap
- **Audit-Empfehlung:** Regelmäßig Network-Tab prüfen — welche externen Requests lädt die Seite vor Consent?

### WordPress-Spezialfall

- Plugin „Local Google Fonts" / „OMGF"
- Elementor + Divi hatten lange Google-Fonts-by-default — Themes prüfen

### Next.js / React

```
// Gut — Build-Time Download:
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"] });
// Nicht:
<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet" />
```

## Siehe auch

- [[gesetze/dsgvo]]
- [[themen/drittland-transfer]]
- [[themen/tracking-analytics]]
- [[themen/cookie-consent]]
- [[urteile/eugh-schrems-ii]]
