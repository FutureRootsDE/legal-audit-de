---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/urhg/__51.html
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/urhg/__51a.html
  - https://www.gesetze-im-internet.de/urhg/__63.html
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62017CJ0476
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62017CJ0516
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62017CJ0469
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

# Zitatrecht — § 51 UrhG, Pastiche, Quellenangabe

## Kurz-Ueberblick

Das Zitatrecht nach § 51 UrhG erlaubt es, fremde urheberrechtlich geschuetzte
Werke ohne Erlaubnis des Urhebers zu nutzen — aber nur unter **strengen**
Voraussetzungen:

1. **Zitat-Zweck**: Das fremde Werk muss als **Beleg** dienen oder
   **inhaltliche Auseinandersetzung** ermoeglichen. "Schmueckendes Beiwerk"
   ist kein Zitat.
2. **Umfang gerechtfertigt**: Nicht mehr Umfang als noetig.
3. **Eigener Werk-Charakter**: Das zitierende Werk muss ein **selbststaendiges
   Werk** sein.
4. **Quellenangabe** (§ 63 UrhG) ist Pflicht.
5. Veroeffentlichtes Werk: Nur bereits veroeffentlichte Werke duerfen zitiert
   werden.

Seit 2021 (UrhG-DSM-Umsetzung) gilt zusaetzlich **§ 51a UrhG** — Karikatur,
Parodie, Pastiche als eigene Schranke.

Fuer **Marketing-Seiten** wichtig: "Werbe-Zitate" (z.B. Einstein-Zitate zu
Motivation, "Promis empfehlen unser Produkt") sind in der Regel **kein
zulaessiges Zitat** nach § 51 UrhG.

## Schluesselparagraphen / Kernaussagen

### § 51 UrhG (Zitat)

> "Zulaessig ist die Vervielfaeltigung, Verbreitung und oeffentliche Wiedergabe
> eines veroeffentlichten Werkes zum Zweck des Zitats, sofern die Nutzung in
> ihrem Umfang durch den besonderen Zweck gerechtfertigt ist. Zulaessig ist
> dies insbesondere, wenn
>
> 1. einzelne Werke nach der Veroeffentlichung in ein selbstaendiges
>    wissenschaftliches Werk zur Erlaeuterung des Inhalts aufgenommen werden,
> 2. Stellen eines Werkes nach der Veroeffentlichung in einem selbstaendigen
>    Sprachwerk angefuehrt werden,
> 3. einzelne Stellen eines erschienenen Werkes der Musik in einem
>    selbstaendigen Werk der Musik angefuehrt werden."

- **Nr. 1 — Grosszitat**: nur in wissenschaftlichen Werken, ganze Werke
  zitierbar (z.B. Gemaelde in Dissertation).
- **Nr. 2 — Kleinzitat**: in Sprachwerken, nur **Stellen/Ausschnitte**, nicht
  das ganze Werk.
- **Nr. 3 — Musikzitat**: nur einzelne Stellen.

### § 51a UrhG (Karikatur, Parodie, Pastiche) — seit 07.06.2021

> "Zulaessig ist die Vervielfaeltigung, die Verbreitung und die oeffentliche
> Wiedergabe eines veroeffentlichten Werkes zum Zweck der Karikatur, der
> Parodie und des Pastiches."

- Umsetzung von Art. 17 Abs. 7 DSM-RL (EU) 2019/790
- "Pastiche": stilistische Uebernahme (z.B. Sampling, Memes, Remixes)
- Einzelfallabwaegung: Kuenstlerische Auseinandersetzung vs. wirtschaftliche
  Ausnutzung

### § 63 UrhG (Quellenangabe) — IMMER Pflicht

> "Wenn ein Werk oder ein Teil eines Werkes [...] vervielfaeltigt oder
> verbreitet wird, ist stets die Quelle deutlich anzugeben."

- Urheber + ggf. Verlag
- Kenntlichmachen von Kuerzungen/Aenderungen
- Entfaellt nur, wenn Quelle unbekannt (selten)

## Zitat-Voraussetzungen im Ueberblick

| Voraussetzung | Anforderung |
|---|---|
| Zitatzweck | Beleg, Auseinandersetzung, Erlaeuterung — NICHT Illustration/Schmuck |
| Umfang | so wenig wie noetig |
| Selbststaendigkeit | eigene geistige Leistung des Zitierenden erforderlich |
| Werk veroeffentlicht | vorher legal erschienen |
| Unveraendert | kein Eingriff in den Werkcharakter (Aenderungen offenlegen) |
| Quelle | § 63 UrhG: Urheber + Fundstelle |
| Kein Verstoss gegen Urheberpersoenlichkeit | § 14 UrhG (Entstellung) |

## Typische Fallstricke in Codebases / Webseiten

| Problem | Risiko | Fix |
|---|---|---|
| Einstein-/Steve-Jobs-Zitat auf Landingpage | Kein Zitatzweck (§ 51), schmueckend | Eigene Aussage oder freie Inhalte (gemeinfrei) |
| Foto eines Gemaeldes als Illustration im Blog | Kein Kleinzitat, strenger Massstab fuer Bildzitate | Lizenz einholen oder Public-Domain-Bild |
| Song-Snippet in Produktvideo | Regelmaessig kein Zitat, GEMA-Lizenz noetig | Royalty-free Musik oder Lizenz |
| Wikipedia-Artikel copy/paste ohne Quelle | § 63 UrhG + CC-BY-SA-Lizenz verletzt | Quelle + Lizenzhinweis setzen |
| Meme mit Filmszene auf Twitter | § 51a UrhG nur bei echter Parodie | Pruefen: parodistische Auseinandersetzung? |
| Interview-Auszug ohne Zustimmung | Interview = urheberrechtlich geschuetzt + KUG | Zustimmung + Quelle |
| Forschungsabbildung ohne Nennung | § 51 Nr. 1 + § 63 UrhG | Vollstaendige Zitation mit Urheber/Verlag |
| Promi-Zitat fuer Werbung | Kein § 51 UrhG + § 22 KUG Persoenlichkeitsrecht | Lizenzvertrag noetig |

## Relevanz fuer Codebase-Typen

### Content/Blog

- CMS-Feld "Quelle" fuer jedes zitierte Werk Pflicht
- Bild-Zitate nur in klar wissenschaftlichem oder kritischem Kontext
- Lizenz-Logo bei CC-Bildern automatisch ausgegeben

### E-Commerce

- Produktbeschreibungen: kein fremder Text ohne Lizenz (Herstellerfreigabe)
- Herstellerlogos: Lizenz (oft ok bei Produktverkauf, aber nicht fuer Werbung)

### Next.js SaaS / Landingpage

- "Kunden-Zitate" auf Testimonials: nur mit Zustimmung + reale Person
- Keine beruehmten Motivations-Zitate als Design-Element ohne Pruefung
  (oft sind die Zitate selbst gemeinfrei, aber Uebersetzungen geschuetzt)

### Video/Shorts

- Filmzitate: strenger Massstab, EuGH Pelham + Spiegel Online beachten
- Kurze Samples in Musik: nur bei § 51a (Pastiche) mit Abwaegung

## Behoerden-Hinweise / Gerichtspraxis

- **Deutsches Patent- und Markenamt / ZPUe**: Zustaendig fuer
  urheberrechtliche Verwertungsgesellschaften (GEMA, VG Wort, VG Bild-Kunst)
- **BGH**: Strenge Linie bei "Zier-Zitaten"
- **EuGH**: Harmonisiert Zitat-Schranke ueber DSM-RL + InfoSoc-RL

## Zitierbare Urteile

### BGH I ZR 241/95 (Kleinzitat), 20.12.2007 `<<VERIFIKATION AUSSTEHEND>>`

Exaktes Datum/Aktenzeichen final zu verifizieren — Angaben variieren je nach
Quelle. Ueberlieferte Kernaussage: Kleinzitat nur zulaessig, wenn das zitierte
Werk in einem inneren Zusammenhang mit der eigenen Darstellung steht (**Beleg-
oder Erlaeuterungsfunktion**).

### BGH I ZR 102/10 (Elektronischer Pressespiegel), 16.01.2014

Kernsatz: Blosses Anfuehren fremder Inhalte ohne innere Auseinandersetzung
ist kein Zitat.

### EuGH C-476/17 (Pelham / Metall auf Metall), 29.07.2019

> "Die Entnahme eines Audiofragmentes aus einem Tontraeger, um es — in geaenderter
> und beim Hoeren nicht wiedererkennbarer Form — in einen neuen Tontraeger
> aufzunehmen, stellt keine Vervielfaeltigung iSv Art. 2 Buchst. c der Richtlinie
> 2001/29 dar."

Kernfolge: Sampling ist zulaessig, wenn das Fragment **unkenntlich** ist.
Bei erkennbaren Samples ggf. Pastiche-Schranke (§ 51a UrhG) einschlaegig.

### EuGH C-516/17 (Spiegel Online), 29.07.2019

> "Die Verwendung von Zitaten erfordert grundsaetzlich keine vorherige
> Zustimmung des Urhebers, sofern bestimmte Bedingungen erfuellt sind;
> Hyperlinks koennen als Zitate fungieren."

Kernfolge: Auch Links koennen als Zitat i.S.v. Art. 5 Abs. 3 lit. d InfoSoc-RL
gelten. Werk muss rechtmaessig veroeffentlicht worden sein.

### EuGH C-469/17 (Funke Medien / Afghanistan Papiere), 29.07.2019

Kernaussage: Urheberrecht kann nicht durch ausserhalb der Schranken liegende
Grundrechte (Pressefreiheit) ueberwunden werden — aber die bestehenden
Schranken (Zitat, Berichterstattung) sind im Lichte der Grundrechte
auszulegen.

### BGH I ZR 55/19 (Afghanistan-Papiere II), 30.04.2020

Umsetzung der EuGH-Rechtsprechung im deutschen Urheberrecht; enger Zitat-
Begriff, journalistische Berichterstattung privilegiert.

## Praxis-Check (Was Code-Reviewer konkret pruefen)

- [ ] Jedes Zitat hat einen klaren **Belegzweck** (nicht nur Illustration)
- [ ] Umfang des Zitats ist auf das **Erforderliche** beschraenkt
- [ ] Eigene inhaltliche Auseinandersetzung ist erkennbar (nicht bloss Listicle)
- [ ] **Quellenangabe** vorhanden: Urheber + Werk + Fundstelle (URL, Buch-Seite)
- [ ] Zitiertes Werk war zuvor **legal veroeffentlicht**
- [ ] Bei Bildzitaten: strenger Massstab (wissenschaftlich/kritisch) geprueft
- [ ] Keine "Motivations-Zitate" von Steve Jobs/Einstein als Design-Element
      ohne gemeinfreie Basis
- [ ] Musik-/Filmausschnitte: Lizenz + GEMA geklaert
- [ ] CC-Lizenzen (CC-BY, CC-BY-SA): Namensnennung + Lizenzlink korrekt
- [ ] Kuerzungen/Aenderungen sind gekennzeichnet ("[…]", "[Name]")
- [ ] Promi-Zitate fuer Werbung: Lizenz + KUG-Zustimmung ([[fotos-dritter-kug]])

## Formatierung eines korrekten Zitats (Beispiel)

```markdown
> "Das wichtigste ist, nicht aufzuhoeren zu fragen."
>
> — Albert Einstein, zitiert nach: [Werk XY, Verlag, Jahr, Seite 42]

Wikipedia — Artikel "Albert Einstein", abgerufen am 19.04.2026 (CC-BY-SA 4.0),
Quelle: https://de.wikipedia.org/wiki/Albert_Einstein
```

## Siehe auch

- [[urheber-stockfoto]] — Lizenzpflicht bei Fotos/Stock
- [[fotos-dritter-kug]] — Bildnisse + KUG
- [[werbekennzeichnung]] — Testimonials und Promi-Zitate
- [[ki-content]] — KI-generierte Werke und Zitatrecht
- [[datenschutzerklaerung]] — Quellenangabe bei fremden Inhalten
