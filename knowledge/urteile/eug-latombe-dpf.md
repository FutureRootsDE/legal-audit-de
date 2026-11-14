---
aktualisiert: 2026-11-14
quelle-primaer: https://publications.europa.eu/resource/celex/62023TJ0553
ecli: ECLI:EU:T:2025:831
quellen-sekundaer:
  - https://curia.europa.eu/juris/liste.jsf?num=T-553/23
  - https://curia.europa.eu/juris/liste.jsf?num=C-703/25
  - https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32023D1795
verifiziert-am: 2026-11-14
geltungsbereich: [EU, DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-11-14

# EuG T-553/23 — "Latombe/Kommission" (EU-US Data Privacy Framework)

## Kurz-Ueberblick

- **Gericht:** Gericht der Europaeischen Union (Zehnte erweiterte Kammer)
- **Rechtssache:** T-553/23, Philippe Latombe ./. Europaeische Kommission
  (Streithelferin: Irland; Streithelfer: Vereinigte Staaten von Amerika)
- **Urteil:** 03.09.2025
- **ECLI:** ECLI:EU:T:2025:831
- **CELEX:** 62023TJ0553
- **Streitgegenstand:** Nichtigkeitsklage gegen den Durchfuehrungsbeschluss
  (EU) 2023/1795 der Kommission vom 10.07.2023 ueber die Angemessenheit
  des durch den EU-US Data Privacy Framework (DPF) gewaehrleisteten
  Schutzniveaus (CELEX:32023D1795).

Das EuG hat die Nichtigkeitsklage des franzoesischen Abgeordneten Philippe
Latombe **abgewiesen** und damit den DPF-Angemessenheitsbeschluss der
Kommission erstinstanzlich bestaetigt. Gegen das Urteil ist das Rechtsmittel
C-703/25 P beim EuGH anhaengig (eingelegt am 31.10.2025).

## Tenor (sinngemaess)

1. Die Klage wird abgewiesen.
2. Herr Philippe Latombe traegt seine eigenen Kosten sowie die Kosten der
   Europaeischen Kommission einschliesslich der Kosten des Verfahrens des
   vorlaeufigen Rechtsschutzes.
3. Irland traegt seine eigenen Kosten.
4. Die Vereinigten Staaten von Amerika tragen ihre eigenen Kosten.

## Kernaussagen

- **Wirksamer Rechtsbehelf nach Art. 47 GRCh**: Der mit EO 14086 errichtete
  **Data Protection Review Court (DPRC)** stellt in seiner Kombination mit
  den vorgelagerten Beschwerdestufen einen wirksamen Rechtsbehelf im Sinne
  der Grundrechtecharta dar. Der im Schrems-II-Urteil (EuGH C-311/18)
  identifizierte zentrale Mangel des Privacy Shield (fehlender effektiver
  Rechtsschutz durch die US-Ombudsperson) ist durch die Neukonstruktion
  nicht fortbestehend.
- **Verhaeltnismaessigkeit der Bulk-Collection**: Die durch EO 14086
  normierten Grenzen (zwoelf abschliessend festgelegte Zwecke, Grundsaetze
  der Erforderlichkeit und Verhaeltnismaessigkeit, Ausuebung durch die
  Intelligence Community unter Aufsicht) genuegen den unionsrechtlichen
  Anforderungen an einen unbestimmten, aber kontrollierten Zugriff zur
  nationalen Sicherheit.
- **Pruefungsmassstab**: Der Angemessenheitsbeschluss wird nach den im
  Zeitpunkt seines Erlasses (10.07.2023) bestehenden Rechts- und
  Faktenlage geprueft. Spaetere Entwicklungen im US-Rechtsgefuege sind
  nicht Gegenstand der Entscheidung — und koennen die Pruefung in
  anderen Verfahren gleichwohl beeinflussen.
- **Massgebliche Vorschriften**: Art. 45 DSGVO (Angemessenheitsbeschluss);
  GRCh Art. 7, 8, 47; EO 14086; AG Regulation 28 CFR Part 201 (DPRC).

## Bedeutung fuer Audits

- **DPF-Transfer bleibt zulaessig**: Fuer DPF-zertifizierte US-Empfaenger
  gilt der Angemessenheitsbeschluss (EU) 2023/1795 unveraendert fort;
  ein zusaetzliches Transfer-Impact-Assessment (TIA) ist nicht erforderlich
  (siehe [[themen/drittland-transfer]], Abschnitt DPF).
- **Resilienz-Planung**: Das Rechtsmittel C-703/25 P ist anhaengig; eine
  (vollstaendige oder teilweise) Aufhebung des DPF-Beschlusses durch den
  EuGH ist nicht ausgeschlossen. Fuer auditrelevante Verarbeitungen
  (z. B. US-Cloud, Analytics) empfiehlt sich die **Dokumentation einer
  Ruecknahme-Option** (SCCs + ergaenzende Massnahmen vorbereitet;
  EU-Alternative gelistet).
- **Bulk-Access im TIA**: Fuer Transfers ausserhalb DPF (reine SCC-/
  BCR-Faelle) bleibt die Bulk-Access-Diskussion unveraendert relevant.
  Das Urteil liefert keine Freizeichnung fuer Nicht-DPF-Transfers.

## Abgrenzung

- **Nur Nichtigkeitsklage, keine Vorlagefrage**: T-553/23 hat keine
  Vorlagefragen zur DSGVO oder zur GRCh beantwortet; es handelt sich um
  eine unmittelbare Klage gegen den Angemessenheitsbeschluss (Art. 263
  AEUV). Die EuGH-Linie aus Schrems II wird angewandt, nicht modifiziert.
- **Keine Aussage zur US-Rechtsentwicklung nach 2023**: Spaetere
  Aenderungen am DPRC, an EO 14086 oder an FISA 702 bleiben
  nachzupruefen; gegebenenfalls ueber den Ueberwachungsmechanismus der
  Kommission (regelmaessige Review-Zyklen des DPF).
- **"Schrems III" als eigenstaendiges Verfahren**: In der publizierten
  Curia-Verfahrensliste zum Stand 2026-11-14 nicht als eigener Verfahrens-
  gegenstand nachweisbar; anhaengig ist allein das Rechtsmittel C-703/25 P.

## Siehe auch

- [[urteile/eugh-schrems-ii]]
- [[themen/drittland-transfer]]
- [[themen/tracking-analytics]]
- [[themen/avv-muster]]

## Quellen

- EuG, Urteil vom 03.09.2025, T-553/23, Latombe/Kommission — Volltext ueber
  EUR-Lex (`publications.europa.eu/resource/celex/62023TJ0553`, abgerufen am
  2026-11-14). Tenor, Rubrum und Pruefungsmassstab unmittelbar am Volltext
  belegt.
- Durchfuehrungsbeschluss (EU) 2023/1795 der Kommission vom 10.07.2023
  (CELEX:32023D1795).
- Mitteilung zum Rechtsmittel C-703/25 P im Amtsblatt der EU, EUR-Lex
  ELI `C/2025/6610`.

## Aenderungsvermerk

- **2026-11-14**: Datei neu angelegt; Primaerbeleg ueber EUR-Lex (CELEX
  62023TJ0553). ECLI:EU:T:2025:831 aus Primaerquelle uebernommen.
  Rechtsmittel C-703/25 P anhaengig.
