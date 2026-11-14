---
aktualisiert: 2026-11-14
quelle-primaer: https://rewis.io/urteile/urteil/lhm-20-01-2022-3-o-1749320/
quellen-sekundaer:
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Text=3+O+17493/20
  - https://www.ra-plutte.de/lg-muenchen-dynamische-einbindung-google-web-fonts-ist-dsgvo/
  - https://www.it-recht-kanzlei.de/lg-muenchen-I-webfonts-einwilligung-schadensersatz.html
  - https://curia.europa.eu/site/upload/docs/application/pdf/2026-02/vi_zr_258-24.pdf
verifiziert-am: 2026-11-14
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

# LG München I 3 O 17493/20 — „Google Fonts"

> **Hinweis zur Benennung:** Eine BGH-Sachentscheidung zu „Google Fonts"
> existiert bislang **nicht**. Leitend ist das erstinstanzliche Urteil des
> LG München I (20.01.2022, 3 O 17493/20); der BGH hat mit Beschluss
> **VI ZR 258/24 vom 28.08.2025** dem EuGH Vorlagefragen zu
> provozierten Google-Fonts-Datenverstoessen vorgelegt (anhaengig als
> **EuGH C-654/25**). Der Datei-Slug „bgh-google-fonts" ist historisch
> gewachsen; inhaltlicher Kern bleibt das LG-Muenchen-Urteil + die noch
> offene EuGH-Vorlage.

## Kurz-Überblick

Das Landgericht München I hat am 20. Januar 2022 entschieden, dass die dynamische Einbindung von Google Fonts (Laden von Google-CDN-Servern) ohne Einwilligung der Website-Besucher rechtswidrig ist und einen Schadenersatzanspruch in Höhe von 100 EUR nach Art. 82 DSGVO begründet. Das Urteil hat eine deutschlandweite Abmahnwelle ausgelöst und den Umgang mit externen Web-Fonts, CDNs und Third-Party-Ressourcen verändert.

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

Der EuGH hat klargestellt, dass der **bloße Verstoß gegen die DSGVO nicht automatisch** einen Schadenersatzanspruch begründet — die negative Folge muss nachgewiesen werden. Allerdings gibt es **keine Erheblichkeitsschwelle** (kein Bagatellausschluss).

### EuGH-Einfluss (C-340/21, Bulgarische Post, 14.12.2023)

Der EuGH hat in einer weiteren Entscheidung klargestellt, dass die **Befürchtung eines Datenmissbrauchs** durch Dritte nach einer DSGVO-Verletzung einen immateriellen Schaden darstellen kann (Hacking-Fall). Damit bleibt die LG-München-Linie für Google-Fonts-Verfahren grundsätzlich anschlussfähig, sofern der konkrete Kontrollverlust dargelegt wird.

### BGH-Vorlage an EuGH (28.08.2025, VI ZR 258/24 → EuGH C-654/25)

Der BGH (VI. Zivilsenat) hat mit Beschluss vom **28.08.2025, Az. VI ZR 258/24**,
dem EuGH Fragen zu **massenhaft provozierten Google-Fonts-Abmahnungen**
vorgelegt (anhaengiges EuGH-Verfahren **C-654/25**): u.a. ob eine bewusst
herbeigefuehrte Datenuebermittlung (durch Crawler-gestuetzte Simulation eines
Website-Besuchs allein zur Dokumentation des Verstosses) ueberhaupt einen
ersatzfaehigen immateriellen Schaden i.S.v. Art. 82 DSGVO begruendet und wie
das Konzept personenbezogener Daten bei dynamischen IP-Adressen in dieser
Konstellation auszulegen ist. Volltext der Vorlagefragen: curia.europa.eu
(vi_zr_258-24.pdf). Die EuGH-Entscheidung steht aus; bis dahin ist die
LG-Muenchen-Linie fuer Massen-Abmahnungen rechtsunsicher. Die Schlussantraege
von Generalanwalt Szpunar werden fuer 2026 erwartet, waren zum Stand
2026-11-14 noch nicht veroeffentlicht <<VERIFIKATION AUSSTEHEND>>.

### BGH VI ZR 10/24 „Facebook-Scraping" (18.11.2024) als Leitentscheidung Art. 82 DSGVO

Der VI. Zivilsenat hat im ersten foermlichen Leitentscheidungsverfahren
(§ 552b ZPO) am **18.11.2024** entschieden: Der „blosse und kurzzeitige
Verlust der Kontrolle" ueber personenbezogene Daten infolge einer
DSGVO-Verletzung kann einen ersatzfaehigen immateriellen Schaden i.S.v.
Art. 82 Abs. 1 DSGVO begruenden, ohne dass konkrete psychische
Beeintraechtigungen dargelegt werden muessen. Folgerechtsprechung u.a.
BGH VI ZR 109/23, Urteil vom 28.01.2025 (Darlegung eines immateriellen Schadens
nach Art. 82 Abs. 1 DSGVO bei Nutzung einer E-Mail-Adresse zu Werbezwecken;
ECLI:DE:BGH:2025:280125UVIZR109.23.0, primaer bestaetigt ueber die
Rechtsinformations-API des Bundes am 2026-11-14; die oft genannte konkrete
Schadenssumme von 500 EUR ist in der Primaerquelle nicht wiedergegeben
und daher hier mit Verifikationsmarker versehen <<VERIFIKATION AUSSTEHEND>>).
Fuer
Google-Fonts-Faelle bedeutet das: Die Art-82-Grundlage traegt im Prinzip,
die Frage des Rechtsmissbrauchs bei provozierten Verstoessen bleibt aber
offen bis zur EuGH-Entscheidung C-654/25. Quelle: BGH-Volltext VI ZR 10/24
ueber juris.bundesgerichtshof.de; Einordnung bei vzbv und
beck-aktuell.

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

## Aenderungsvermerk

- 2026-11-14: Klarstellung ergaenzt, dass es keine BGH-Sachentscheidung zu
  „Google Fonts" gibt; Datei dokumentiert LG Muenchen I 3 O 17493/20 und die
  BGH-Vorlage. BGH-Aktenzeichen der EuGH-Vorlage als **VI ZR 258/24**
  (Beschluss 28.08.2025, EuGH Az. C-654/25) konkretisiert (zuvor nur „Sommer
  2025"). BGH VI ZR 10/24 (Facebook-Scraping, 18.11.2024) als Leitentscheidung
  zu Art. 82 Abs. 1 DSGVO ergaenzt. Status der Schlussantraege Szpunar noch
  nicht verifizierbar, Marker gesetzt.
