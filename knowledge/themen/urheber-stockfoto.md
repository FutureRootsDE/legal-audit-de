---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/urhg/
quellen-sekundaer:
  - https://unsplash.com/license
  - https://www.pexels.com/license/
  - https://help.unsplash.com/en/articles/2612315-can-i-use-unsplash-images-for-personal-or-commercial-projects
  - https://www.it-recht-kanzlei.de/Kommentar/16356/Verwendung_der_Bilder_bei_unsplash.php
  - https://www.e-recht24.de/urheberrecht/13169-rechtliches-zu-online-bilddatenbanken.html
  - https://krassevideos.de/blog/2025/04/08/abmahnwelle-2025-vorsicht-bei-bildern-aus-ai-pexels-unsplash-co/
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

# Stock-Foto-Lizenzierung — Unsplash, Pexels, Pixabay, Shutterstock, Adobe Stock, Creative Commons

## Kurz-Ueberblick

Bilder sind einer der **haeufigsten Abmahnungsgegenstaende** in Deutschland. Abmahnungen kommen vor, gerade auch gegen Nutzer von **kostenlosen Stockfoto-Plattformen** (Pexels, Unsplash, Pixabay) um — haeufig Betrugsszenarien, bei denen Fotos **irrtuemlich dort hochgeladen** wurden und der wahre Urheber nun Ansprueche geltend macht.

Zentrale Regel: **Eine Plattform-Lizenz bindet nur, wenn der Hochladende der wahre Rechteinhaber ist**. Die Plattformen pruefen das in der Regel **nicht**. Haftung des Plattformnutzers (gewerblich!) ist verschuldensunabhaengig auf Unterlassung, schuldhaft auf Schadensersatz (§§ 97, 97a UrhG).

## Lizenz-Uebersicht

### Unsplash ("Unsplash License")

- **Kommerzielle und private Nutzung** erlaubt, kostenfrei
- **Keine Attribution-Pflicht** (aber empfohlen)
- **Keine Bildlizenz-Weitergabe** als Stock-Foto-Datenbank
- Einschraenkungen laut Anbieter (unsplash.com/license, Stand 2026-11-15): "Images cannot be sold without significant modification ..."
- **Wichtig**: Unsplash schliesst jede Haftung aus — Risiko liegt beim Nutzer
- CC0 galt **frueher**; seither **proprietaere Unsplash-Lizenz** (Wechseldatum an der Lizenzseite des Anbieters pruefen)

### Pexels

- **Free Stock Photo & Video License**
- Kommerzielle und private Nutzung
- Keine Attribution noetig (empfohlen)
- Einschraenkungen laut Anbieter (pexels.com/license, Stand 2026-11-15): "Identifiable people may not appear in a bad light ..."
- Ebenfalls Haftungsausschluss fuer Uploads Dritter

### Pixabay

- **Pixabay-Lizenz**: Bedingungen laut Lizenzseite des Anbieters; zum Zeitpunkt des Downloads lesen und archivieren

### Shutterstock / Adobe Stock / iStock (bezahlt)

- Lizenzumfang (Standard, Enhanced/Extended), Auflagengrenzen sowie Model- und Property-Releases richten sich nach den Lizenzbedingungen der jeweiligen Agentur; dort pruefen
- **Download-Nachweis** und Lizenz-Nummer unbedingt **archivieren**

### Creative Commons (CC)

- **CC BY**: Namensnennung erforderlich — spezifische Nennung des Urhebers, Link zur Lizenz, ggf. Aenderungen vermerken
- **CC BY-SA**: "Share-Alike" — Bearbeitungen unter gleicher Lizenz
- **CC BY-NC**: Nicht kommerziell — fuer Unternehmenswebsites typisch **nicht nutzbar**
- **CC BY-ND**: Bearbeitungen duerfen erstellt, aber nicht weitergegeben (veroeffentlicht) werden
- **CC0**: Verzicht auf Urheber- und verwandte Schutzrechte, soweit rechtlich moeglich, sonst umfassende Rechtseinraeumung; "kein Urheberrecht" ist verkuerzt. Persoenlichkeits- und Markenrechte gesondert beachten

## Abmahnmuster

### Typische Abmahngruende

1. **Fehlende / falsche Urheberbenennung** bei CC-Bildern oder alten Unsplash-Bildern (frueher CC0 mit Empfehlung, spaeter neue Lizenz)
2. **Nutzung gestohlener Uploads** auf Pexels/Pixabay/Unsplash — wahrer Urheber mahnt ab
3. **"Fake-Unsplash-Hochladungen"**: Fremde laden kopierte Fotos hoch → Nutzer in gutem Glauben → Abmahnung
4. **Keine Lizenzdokumentation** (Nachweis, dass zum Zeitpunkt der Nutzung die jeweilige Lizenz galt)
5. **Ueberschreitung der Lizenzbedingungen** (z. B. CC BY-NC kommerziell genutzt; Standard-Lizenz mit Enhanced-Nutzung)
6. **Model Rights** bei erkennbaren Personen ohne Model-Release
7. **Markenrechte / Designrechte** auf Produktbildern (z. B. markengeschuetzte Logos im Hintergrund)

### Typische Forderungshoehen

- Abmahnkosten (Anwaltsgebuehr) bei kleineren Faellen: **150–500 EUR** (Erfahrungswert, kein Beleg; Deckel § 97a UrhG bei Privatpersonen 1.000 EUR Gegenstandswert; bei gewerblicher Nutzung kein Deckel)
- Lizenzanaloger Schadensersatz: **MFM-Tabelle** als Leitplanke; haeufig **300 EUR – 3.000 EUR** pro Bild (Erfahrungswert, kein Beleg; in BGH I ZR 187/17 bemassen die Instanzgerichte die Lizenzgebuehr mit 100 EUR, Rn. 5, also unter dieser Spanne)
- Wegen fehlender Urhebernennung kann ein Zuschlag auf die fiktive Lizenzgebuehr verlangt werden; 100 % ist Instanzpraxis, keine feste Vorgabe des BGH.

## Typische Fallstricke in Codebases

- **Bilder per `background-image: url(...)`** geladen, nicht im CMS → Lizenz-Nachweis schwierig
- **`next/image`-Assets** ohne Attribution-Metadaten
- **Headless CMS** (Sanity, Strapi) ohne Lizenz-Feld pro Asset
- **Drittanbieter-Widgets** (Shop-Templates, Theme Bibliotheken) mit unklaren Bild-Rechten
- **KI-Bildgenerierung** kann Bildnisse realer Personen (Recht am eigenen Bild, § 22 KUG), Marken/Logos oder urheberrechtlich geschuetzte Werke wiedergeben
- **Git-Commit** mit fremden Bildern → langfristiger Nachweisverlust
- **CDN** cached Bilder ueber Jahre → Loeschung bei Lizenzende schwierig

## Checkliste: Rechtssichere Bildnutzung

### Vor der Nutzung

- [ ] Lizenztext der Plattform lesen **zum Zeitpunkt des Downloads**
- [ ] **Screenshot** der Lizenzseite + Download-Page archivieren
- [ ] **Download-Rechnung / Download-Link / Lizenz-ID** speichern (bei bezahlten Agenturen)
- [ ] Pruefen, ob Personen auf dem Bild erkennbar sind → **Model-Release** vorhanden?
- [ ] Pruefen, ob Markenzeichen/Design auf dem Bild zu sehen sind
- [ ] Bei CC-Bildern: **Urheber + Lizenz + Quelle + ggf. Bearbeitungshinweis** vorbereiten

### Bei der Nutzung

- [ ] Alt-Text pflegen (auch WCAG-relevant)
- [ ] Urheberbenennung so, wie Urheber bzw. Lizenz sie vorgeben (§ 13 Satz 2 UrhG); ein Sammel-Bildnachweis (Impressum/Footer) genuegt nur, wenn die Lizenz ihn zulaesst
- [ ] Bei CC BY: *"Foto: Max Mustermann (Link zur Quelle) / CC BY 4.0 (Link auf https://creativecommons.org/licenses/by/4.0/)"*, bei Bearbeitung mit Zusatz "bearbeitet"

### Nach der Nutzung

- [ ] **Lizenznachweis waehrend der gesamten Nutzung und mindestens 10 Jahre danach archivieren**: § 102 UrhG verweist auf die Verjaehrungsvorschriften des BGB (§§ 195, 199 BGB: 3 Jahre ab Schluss des Jahres der Kenntnis, kenntnisunabhaengige Hoechstfristen bis 10 bzw. 30 Jahre) und in Satz 2 auf § 852 BGB (Restschadensersatz verjaehrt erst nach zehn Jahren von seiner Entstehung an); der Unterlassungsanspruch entsteht bei fortdauernder Nutzung laufend neu. 10 Jahre sind ein Mindestwert.
- [ ] Bei Loeschung: Caches / CDN / Archive ebenfalls leeren
- [ ] Bei Plattform-Lizenz-Aenderungen: Migration dokumentieren

## Empfehlung: Lizenz-Stack fuer Codebases

Empfohlene Hierarchie nach Rechtssicherheit:

1. **Eigene Fotos** (sicher, aber Aufwand)
2. **Bezahlte Agenturen** (Adobe Stock, Shutterstock, iStock) — mit Lizenznummer archiviert
3. **CC BY** mit sauberer Attribution
4. **Unsplash / Pexels / Pixabay** — nur mit **Screenshot der Lizenzseite** und Bewusstsein fuer Restrisiko
5. **KI-generiert** (Flux, DALL-E, Midjourney) — vertraglich pruefen (ToS der Anbieter); Content-Prompting so, dass keine Drittmarken/Personen entstehen

## Relevanz fuer Codebase-Typen

- **Next.js SaaS / Landingpage**: **Hoch** — Hero-Bilder, Feature-Grafiken typisch
- **n8n**: Automatisierte Bildgenerierung (z. B. Social-Media-Workflows) → Lizenz-Audit-Trail aufbauen
- **E-Commerce**: Produktbilder meist vom Hersteller oder Eigenproduktion → vertraglich klaeren; User-Generated Reviews mit Bildern → Haftungsprivileg fuer Hosting nach Art. 6 DSA (VO (EU) 2022/2065), frueher § 10 TMG
- **Content/Blog**: Hoechstes Risiko (viele Bilder, schnelle Publikation) — Bildnachweis-Seite im Footer empfohlen

## Behoerden-Hinweise

- **BMJV (Bundesministerium der Justiz und fuer Verbraucherschutz)**: urheberrechtliche Gesetzgebung; **DPMA**: Aufsichtsbehoerde ueber die Verwertungsgesellschaften (§ 75 Abs. 1 VGG)
- **VG Bild-Kunst**: Kollektive Wahrnehmung fuer Bildrechte; betreibt **"VG Bild-Kunst Opt-Out"**-Portal fuer KI-TDM
- **Presserat**: Nicht zustaendig, aber ethische Leitplanken

## Zitierbare Urteile

### Grundlegend

- **BGH, Urt. v. 15.01.2015, I ZR 148/13 "Motorradteile"**: Verjaehrung bei Dauerhandlung (LS 1), Restschadensersatz als fiktive Lizenzgebuehr (LS 2), materieller und immaterieller Schadensersatz bei Verletzung des Rechts auf Anerkennung der Urheberschaft (LS 3); nicht als Beleg fuer die Haftung des Webseiteninhabers verwenden
- **BGH, Urt. v. 13.09.2018, I ZR 187/17** (Schadensersatz bei Fotonutzung, Zuschlag bei fehlender Urhebernennung)
- **LG Koeln, Urt. v. 30.01.2014, 14 O 427/13** (ECLI:DE:LGK:2014:0130.14O427.13.00): Stockfoto-Plattform, Urheberbenennung nach § 13 UrhG auch bei Abruf der Bilddatei ueber die Direkt-URL (einstweilige Verfuegung bestaetigt)
- **OLG Koeln, Urt. v. 31.10.2014, 6 U 60/14** (ECLI:DE:OLGK:2014:1031.6U60.14.00; Vorinstanz LG Koeln 28 O 232/13): CC-BY-NC-Lizenz; der Lizenzverstoss (Bearbeitung, Urheberbezeichnung) begruendet einen Unterlassungsanspruch; Lizenzschaden null, MFM-Tabelle nicht anwendbar (Rn. 104)

### Speziell zu Gratis-Plattformen

- Bisher kein hoechst- oder obergerichtliches Endurteil gezielt zum
  "gutglaeubigen Nutzer-Schutz bei falsch hochgeladenen Pexels/Pixabay-
  Bildern" identifiziert; Einzelfallentscheidungen auf LG-Ebene. Belastbarer
  Grundsatz bleibt: Das UrhG kennt **keinen gutglaeubigen Erwerb von
  Nutzungsrechten** (h.M.). Wer ein Bild uebernimmt, das ein Nichtberechtigter
  hochgeladen hat, haftet daher auch bei Gutglaeubigkeit auf Unterlassung und
  ggf. Schadensersatz nach Lizenzanalogie. Zum KI-Training siehe das beim BGH
  anhaengige Revisionsverfahren I ZR 281/25 (LAION, [[../gesetze/urhg]]).
  Naechste Pruefung: 2027-02. <<VERIFIKATION AUSSTEHEND>>

## Siehe auch

- [[../gesetze/urhg]]
- [[ki-content]] — KI-Bildgenerierung und Urheberrechte
- [[ki-transparenz]] — Wasserzeichen / C2PA bei KI-Bildern

## Aenderungsvermerk 2026-11-14

- Frontmatter-Daten und Disclaimer-Stand auf 2026-11-14.
- Platzhalter zum fehlenden Endurteil zu "gutglaeubigen Nutzer-Schutz" bei
  falsch hochgeladenen Gratis-Stockfotos bleibt bestehen; gezielte Suche
  ergab weiterhin nur LG-Einzelfallentscheidungen. Marker auf das einzeilige
  Standardformat des Verifikationsmarkers normalisiert, naechste Pruefung
  2027-02.
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 1):
  Archivierungsfrist fuer Lizenznachweise von "3 Jahre" auf Nutzung plus
  mindestens 10 Jahre (§ 102 UrhG, §§ 195, 199, 852 BGB); LG Koeln
  14 O 427/13 und OLG Koeln 6 U 60/14 inhaltlich berichtigt (mit ECLI;
  OLG Koeln: Lizenzschaden null, MFM nicht anwendbar); Eintrag "LG Koeln
  14 O 41/22 (Unsplash-CC0)" gestrichen (das Aktenzeichen betrifft ein
  Urteil vom 11.05.2023 zu Sandalen).
- 2026-11-15: Korrekturen aus doppelter unabhaengiger Pruefung (Runde 2):
  BGH I ZR 187/17 ohne den Namen "Reformistischer Aufbruch" (gehoert zu
  I ZR 228/15); BGH I ZR 148/13 nach den Leitsaetzen gefasst; Eintrag
  "BGH I ZR 50/22" gestrichen (kein Nachweis in der Bundes-API);
  Urhebernennungs-Zuschlag als Instanzpraxis; Haftungsprivileg nach Art. 6
  DSA; CC0, CC BY-ND und CC BY-Format an den Lizenztexten ausgerichtet;
  Urhebernennung nach § 13 Satz 2 UrhG; BMJV und DPMA (§ 75 Abs. 1 VGG);
  Plattform-Wechseldaten, Kanzleinamen und Abmahnwellen-Zeitraeume gestrichen,
  Betragsspannen als Erfahrungswert gekennzeichnet.
