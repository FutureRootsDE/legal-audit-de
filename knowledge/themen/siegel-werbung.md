---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/uwg_2004/__5.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/uwg_2004/__5a.html
  - https://www.rechtsprechung-im-internet.de/
  - https://www.bundesgerichtshof.de/
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

# Siegel- und Testergebnis-Werbung (TUEV, Trusted Shops, Stiftung Warentest)

## Kurz-Ueberblick

Werbung mit Siegeln, Testergebnissen, Pruefplaketten und "Empfehlungs-Badges"
ist **extrem abmahngefaehrdet**. Die Rechtsprechung — allen voran der BGH —
verlangt bei Siegel-Werbung strikte **Informationsangaben** zur Pruefung,
Fundstelle und zum Zeitpunkt.

Kernsaetze:

1. Jede Siegel-/Testsieger-Werbung ohne **Fundstelle** ist in der Regel
   irrefuehrend nach § 5 UWG.
2. Selbst-erfundene, gekaufte ohne Pruefung, oder laengst abgelaufene Siegel
   sind irrefuehrend.
3. Auch bei "Testsieger"-Aussagen muss die konkrete Ausgabe/Zeitpunkt und die
   Vergleichsbasis erkennbar sein.

## Schluesselparagraphen / Kernaussagen

### § 5 Abs. 1 UWG — Irrefuehrende geschaeftliche Handlungen

> "Unlauter handelt, wer eine irrefuehrende geschaeftliche Handlung vornimmt,
> die geeignet ist, den Verbraucher oder sonstigen Marktteilnehmer zu einer
> geschaeftlichen Entscheidung zu veranlassen, die er andernfalls nicht
> getroffen haette."

Typische Irrefuehrungstatbestaende (Abs. 2):

- Nr. 1: wesentliche Merkmale der Ware/Dienstleistung (Beschaffenheit, Vorteile,
  Auszeichnungen)
- Nr. 3: Art, Eigenschaften und Rechte des Unternehmers (einschliesslich
  Befaehigungsnachweise, Auszeichnungen, Preise)

### § 5a UWG — Irrefuehrung durch Unterlassen

> "Unlauter handelt auch, wer einen Verbraucher oder sonstigen Marktteilnehmer
> irrefuehrt, indem er ihm eine wesentliche Information vorenthaelt […]"

Abs. 2 erfasst: Verheimlichen wesentlicher Informationen, unklare/
unverstaendliche/zweideutige Bereitstellung, nicht rechtzeitige Bereitstellung.

**Kernaussage fuer Siegel:** Das Vorenthalten der Fundstelle, Ausgabe oder
Pruefgrundlage ist ein Verstoss nach § 5a UWG — auch unabhaengig von § 5.

### Anlage zu § 3 Abs. 3 UWG (Schwarze Liste, Nr. 2, 4)

Immer unzulaessig (ohne Abwaegung):

- Nr. 2: Verwenden von **Guetezeichen, Qualitaetskennzeichen** ohne die
  erforderliche Genehmigung
- Nr. 4: Unwahre Behauptung, ein Unternehmer/eine Ware sei von einer
  oeffentlichen/privaten Stelle bestaetigt/genehmigt/zugelassen

## Pflichtangaben bei Siegel-Verwendung (Checkliste aus Rspr.)

Fuer **jedes** Siegel/Testergebnis in Werbung muss fuer den Verbraucher
ohne Muehe erkennbar sein:

1. **Welche Stelle** hat geprueft? (TUEV Sued, TUEV Rheinland, Stiftung
   Warentest, TrustedShops, DEKRA, Fokus Money etc.)
2. **Was wurde geprueft?** (konkretes Pruefkriterium / Produktkategorie)
3. **Wann wurde geprueft?** (Ausgabe-Datum, Version des Siegels)
4. **Wo findet sich die Fundstelle?** (Heft, URL, Pruefbericht)
5. **Vergleichsbasis:** bei "Testsieger" — gegen wen / wie viele Produkte?

Die Angaben muessen beim Siegel **unmittelbar** stehen, nicht erst durch
Klick-Kaskaden erreichbar sein.

## Typische Fallstricke in Codebases / Webseiten

| Problem | Risiko | Fix |
|---|---|---|
| "Testsieger" ohne Ausgabe / Datum / Fundstelle | § 5 / § 5a UWG | Direkt am Siegel: "Stiftung Warentest, Heft 11/2024, Note 'Gut'" |
| TUEV-Logo ohne genaues Pruefprodukt + Datum | § 5 UWG | Pruefzertifikat-Nr. + Ablaufdatum neben Siegel |
| "Trusted Shops zertifiziert" mit abgelaufenem Zertifikat | § 5 UWG | Automatisierter Check gegen TS-API |
| Eigene "5-Sterne-Bewertung" auf Homepage | Schwarze Liste Nr. 2/4 | Nur echte Bewertungen (ggf. von Google Reviews, Trustpilot) |
| Self-branded "Nr. 1"-Badges ohne Quelle | § 5 UWG | Seriöse Studie mit Datum und Vergleichsbasis nennen |
| Siegel-Verlinkung auf Homepage der Pruefstelle statt Pruefbericht | § 5a UWG | Deeplink auf konkreten Pruefbericht |
| Vorlauefige / abgelaufene TUEV-Gutachten | § 5 UWG | Expiration-Monitoring |
| Marketing-Text: "von 95% der Kunden empfohlen" ohne Studie | § 5 UWG | Konkrete Studie (n, Methode, Datum) verlinken |

## Relevanz fuer Codebase-Typen

### E-Commerce / SaaS-Landingpages

- Trust-Badges im Footer: jedes Siegel mit Datenblatt (Aussteller, Datum,
  Pruefgegenstand) im Code-Kommentar + Frontend
- Checkout-Trust-Elemente (Trusted Shops, TUEV): API-Status pruefen

### Content/Blog

- Listicles "Top 10 Tools 2026" + "Testsieger"-Label: Methodik-Seite verlinken
- Affiliate-Reviews mit "Empfehlung"-Badge: ggf. als [[werbekennzeichnung]]
  zusaetzlich kennzeichnen

### Next.js

```tsx
// BAD — Siegel ohne Kontext
<img src="/trusted-shops.png" alt="Trusted Shops" />

// GOOD — Kontext direkt am Siegel + Deeplink
<a href="https://www.trustedshops.de/bewertung/info_XYZ.html">
  <img src="/trusted-shops.png" alt="Trusted Shops Kaeufersiegel 2026" />
  <span>Trusted Shops zertifiziert seit 2020 — Zertifikat-Nr. XYZ,
    gueltig bis 31.12.2026</span>
</a>
```

## Behoerden-Hinweise / Gerichtspraxis

- **Wettbewerbszentrale** (Bad Homburg): fuehrt Abmahnprotokolle, regelmaessig
  Siegel-Werbung Thema des Jahres
- **Verbraucherzentrale NRW / Bundesverband**: Klaeger in vielen Siegel-Fall-
  Verfahren (u.a. als Verbraucherschutzverband, § 8 UWG)
- **IHK-Merkblaetter**: Werbung mit Testergebnissen und Pruefzeichen

## Zitierbare Urteile

### BGH I ZR 93/20 (Testsieger), 13.01.2022 `<<VERIFIKATION AUSSTEHEND>>`

Aktenzeichen + exaktes Datum aus Originalquelle (BGH-Entscheidungsdatenbank,
dejure.org) final zu verifizieren. Ueberlieferte Kernaussage:

> Bei Werbung mit einem Testergebnis muss eine Fundstelle der konkreten
> Testveroeffentlichung angegeben werden, damit der Verbraucher die
> Testergebnisse nachpruefen kann. Dies gilt auch fuer die Verwendung des
> Testsieger-Siegels als Qualitaetskennzeichnung.

### BGH I ZR 50/14 (Testsiegel), 05.11.2015

Kernsatz: Bei Werbung mit einem Testsiegel muss die Fundstelle des Tests leicht
auffindbar sein; auf einer Web-Darstellung reicht kein versteckter Link.

### OLG Frankfurt 6 U 169/23 (Stiftung-Warentest-Siegel) `<<VERIFIKATION AUSSTEHEND>>`

Aktenzeichen + Datum final zu verifizieren. Ueberlieferte Tendenz:
Bei Stiftung-Warentest-Siegel-Werbung ohne Ausgabe und Fundstelle liegt
Irrefuehrung vor.

### BGH I ZR 183/15 (Warnhinweis Nahrungsergaenzung), 11.05.2017

Fuer Transparenz bei Werbeaussagen, auf die sich Siegel-Werbung mit-stuetzt.

### BGH I ZR 13/18 (Zertifikat unterlassen), 26.03.2020 `<<VERIFIKATION AUSSTEHEND>>`

Urteil-Details final zu verifizieren. Thema: abgelaufene Zertifikate weiter-
gefuehrt.

## Praxis-Check (Was Code-Reviewer konkret pruefen)

- [ ] Jedes Siegel auf der Website hat im unmittelbaren Kontext:
  - Name der Pruefstelle
  - Pruefgegenstand / Produktkategorie
  - Datum / Ausgabe / Gueltigkeit
  - URL oder Fundstelle (deep-linked auf Pruefbericht)
- [ ] Trust-Badges (TUEV, DEKRA, Trusted Shops) haben ein Ablaufdatum-Monitoring
      (CI-Check oder Cronjob); bei Ablauf: Siegel automatisch entfernen
- [ ] Keine selbst-erfundenen "Qualitaetssiegel" wie "Bestellen mit Sicherheit"
      mit Gold-Sternen ohne neutralen Aussteller
- [ ] "Testsieger"-Aussagen nennen: Ausgabe, Heft, Jahr, Vergleichsbasis
- [ ] Affiliate-"Empfehlungs-Badges": Hinweis auf bezahlte Partnerschaft
      (siehe [[werbekennzeichnung]])
- [ ] "von 95% der Kunden empfohlen" — Studie benennen: n, Methode, Zeitraum
- [ ] Keine falschen Claims wie "von der Stiftung XYZ ausgezeichnet", wenn
      es die Stiftung nicht gibt / keine Auszeichnung erfolgte
- [ ] Bei "Nr. 1 in Deutschland" / "Marktfuehrer": Quellenbeleg dokumentiert

## Dokumentations-Vorlage (zum Einbinden in Legal-Repo)

```yaml
# siegel-registry.yaml
- siegel: "Trusted Shops Kaeufersiegel"
  aussteller: "Trusted Shops GmbH"
  zertifikat_nr: "XYZ1234"
  pruefgegenstand: "Online-Shop <domain>"
  vergeben_am: "2025-02-01"
  gueltig_bis: "2026-02-01"
  fundstelle: "https://www.trustedshops.de/bewertung/info_XYZ1234.html"
  letzte_pruefung: "2026-04-19"
```

## Siehe auch

- [[werbekennzeichnung]] — Werbung, Influencer, UWG
- [[preisangaben]] — Preiswerbung und Irrefuehrung
- [[impressum]] — Unternehmerangaben bei Werbung
- [[ki-content]] — KI-generierte "Zertifikat"-Bilder Risiko
