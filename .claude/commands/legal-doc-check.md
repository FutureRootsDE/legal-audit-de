---
description: Prueft ein einzelnes Dokument (AGB / Datenschutzerklaerung / Impressum / Widerrufsbelehrung / Cookie-Richtlinie) auf rechtliche Maengel nach DE/EU-Recht — ohne Codebase-Kontext. Output: Finding-Liste + Clean-Version.
argument-hint: <datei-pfad> [--typ=agb|dse|impressum|widerruf|cookie|auto] [--out=<zielordner>]
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, WebFetch, Task
---

# /legal-doc-check

Fuehre eine strukturierte Rechts-Pruefung auf einem **einzelnen Dokument** durch, das der User uebergibt. Typische Faelle:

- Anwalts-Entwurf einer DSE / AGB / Impressum **vor** Veroeffentlichung durchcheken
- Bestehendes Live-Dokument gegen aktuelle Rechtslage abklopfen
- Eigenen Entwurf gegen Muster-Klauseln (z.B. aus `templates/`) absichern

**Unterschied zu `/legal-audit`:** kein Codebase-Scan, kein Multi-Pass, kein Cookie-/PII-Fluss. Reine **Text-Analyse** eines Dokuments.

## Flags

### `/legal-doc-check <datei>`
Standard. Typ wird automatisch erkannt (Heuristik: Schluesselwoerter, Struktur). Output landet in `<datei-ordner>/legal-doc-check/`.

### `/legal-doc-check <datei> --typ=<typ>`
Erzwingt einen Dokumenttyp: `agb`, `dse`, `impressum`, `widerruf`, `cookie`, `social-media-bio`.

### `/legal-doc-check <datei> --out=<zielordner>`
Alternativer Output-Ordner (Default: Geschwisterordner `legal-doc-check/` neben der geprueften Datei).

## Pflichtablauf

1. **Validiere die Datei.** Pruefe, dass `$ARGUMENTS` eine existierende Datei ist (`.md`, `.txt`, `.pdf`, `.html`, `.docx`). Bei PDF: `pdftotext` verwenden, wenn verfuegbar; sonst User bitten, eine Text-Version bereitzustellen.

2. **Klassifiziere den Dokumenttyp** (falls nicht per `--typ` erzwungen):
   - **AGB** — Marker: "Allgemeine Geschaeftsbedingungen", "Vertragsschluss", "Haftung", "Anwendbares Recht"
   - **DSE** — Marker: "Datenschutzerklaerung", "Privacy Policy", "Art. 13 DSGVO", "Verantwortlicher"
   - **Impressum** — Marker: "Angaben gemaess § 5 DDG", "Diensteanbieter", Kontaktzeile
   - **Widerrufsbelehrung** — Marker: "Widerrufsrecht", "14 Tage", "Muster-Widerrufsformular"
   - **Cookie-Richtlinie** — Marker: "Cookies", "§ 25 TDDDG", "Consent"
   - **Social-Media-Bio** — Link-Sammlung auf Profil-Seite (Bio, Info, "Impressum und Datenschutz")

   Bei Unsicherheit (< 60% Konfidenz): den User fragen.

3. **Lade passende KB-Chunks** als Referenz:
   - AGB → `knowledge/themen/agb-muster.md`, `knowledge/gesetze/bgb-agb.md`
   - DSE → `knowledge/themen/datenschutzerklaerung.md`
   - Impressum → `knowledge/themen/impressum.md`, `knowledge/gesetze/ddg.md`
   - Widerruf → `knowledge/themen/widerrufsbelehrung.md`, `knowledge/themen/button-loesung.md`
   - Cookie → `knowledge/themen/cookie-consent.md`
   - Social-Media → `knowledge/themen/social-media-datenschutz.md`

4. **Dispatch `legal-auditor`-Agent** (Opus 4.7 [1M]) im Dokument-Modus:
   - Prompt: "Pruefe das beigefuegte Dokument (Typ: <typ>) als Fachanwalts-Review. Klassifiziere Findings nach CRIT/HIGH/MED/LOW. Typische Pruefpunkte pro Typ siehe unten."
   - Agent liefert Finding-Liste als Markdown-Tabelle mit Zitat-Stellen

5. **Dispatch `legal-text-writer`-Agent** (Opus 4.7 [1M]):
   - Erzeugt **eine vollstaendige Clean-Version** des gesamten Dokuments (nicht pro Finding wie bei /legal-audit) — der User soll 1:1 Text zum Uebernehmen bekommen
   - Kopf: Disclaimer-Block aus `templates/disclaimer-block.md`
   - Darunter: vollstaendiges Dokument mit allen Korrekturen, Change-Kommentare als HTML-Kommentare `<!-- Aenderung Finding F-NNN: ... -->`

6. **Zitat-Verifikation:** `legal-researcher`-Agent verifiziert jedes zitierte Gesetz / Urteil gegen Tier-1-Quelle. Log unter `.claude/logs/docu-check-zitate-<YYYY-MM-DD>.log`.

7. **Output-Struktur erzeugen:**
   ```
   <zielordner>/
   ├── DocCheck.md            # Finding-Tabelle + Empfehlungen
   ├── clean.md               # vollstaendige Clean-Version
   └── evidence.md            # urspruengliche Zitat-Stellen mit Kontext
   ```

## Pruefpunkte pro Dokumenttyp

### AGB (§§ 305-310 BGB)

- [ ] **Einbeziehungsklausel** vorhanden (§ 305 Abs. 2 BGB)
- [ ] Wirksamkeit der **Vertragsschluss-Klausel** (kein stillschweigender Vertragsschluss gegen Verbraucherwillen)
- [ ] **Haftungsausschluesse** — keine unzulaessige Haftungsbegrenzung bei Vorsatz/grober Fahrlaessigkeit (§ 309 Nr. 7 BGB)
- [ ] **Gerichtsstands-Klausel** — bei B2C nur Wohnsitzgerichtsstand Verbraucher (§ 29c ZPO)
- [ ] **Rechtswahl-Klausel** — bei B2C Art. 6 Rom-I-VO beachten
- [ ] **Aenderungsvorbehalt** — nicht einseitig ohne Zustimmung (§ 308 Nr. 4 BGB)
- [ ] **Preisanpassungs-Klausel** bei Dauerschuldverhaeltnissen — Voraussetzungen transparent?
- [ ] **Widerrufsbelehrung** separat / integriert (bei B2C-Fernabsatz)
- [ ] **Salvatorische Klausel** — nicht unwirksam per § 306 Abs. 2 BGB
- [ ] **Pauschalisierter Schadensersatz** — Hoehe marktueblich (§ 309 Nr. 5 BGB)
- [ ] **Vertragsstrafe** — bei B2C idR unzulaessig (§ 309 Nr. 6 BGB)

### Datenschutzerklaerung (Art. 13 DSGVO)

- [ ] **Verantwortlicher** mit vollstaendigen Kontaktdaten (Art. 13 Abs. 1 lit. a)
- [ ] **DSB-Kontakt** (Art. 13 Abs. 1 lit. b) — falls DSB-Pflicht nach § 38 BDSG
- [ ] **Zwecke + Rechtsgrundlagen** pro Verarbeitung (Art. 13 Abs. 1 lit. c)
- [ ] Bei **lit. f** (berechtigtes Interesse): konkretes Interesse + Interessenabwaegung erwaehnt
- [ ] **Empfaenger / Empfaenger-Kategorien** (Art. 13 Abs. 1 lit. e) — Drittanbieter namentlich
- [ ] **Drittlandtransfer** mit Garantien (Art. 13 Abs. 1 lit. f) — konkreter Verweis auf SCC / DPF / Adequacy
- [ ] **Speicherdauer** pro Kategorie (Art. 13 Abs. 2 lit. a) — nicht "so lange wie noetig"
- [ ] **Betroffenenrechte** Art. 15-22 benannt
- [ ] **Widerrufsrecht** (Art. 7 Abs. 3) — bei Einwilligungsbasis
- [ ] **Beschwerderecht** bei Aufsichtsbehoerde (Art. 13 Abs. 2 lit. d)
- [ ] **Automatisierte Entscheidungen / Profiling** — Pflicht-Info falls einschlaegig (Art. 22)
- [ ] **Cookie-/Tracking-Abschnitt** mit Consent-Link
- [ ] **Social-Media-Abschnitt** mit Joint-Controller-Verweis (siehe `themen/social-media-datenschutz.md`)
- [ ] **Datum "Stand:"** vorhanden

### Impressum (§ 5 DDG / § 18 MStV)

- [ ] Name + Anschrift (bei juristischen Personen: Rechtsform + Vertreter)
- [ ] E-Mail
- [ ] Telefon ODER zweiter gleichwertiger Kommunikationsweg (EuGH C-298/07)
- [ ] Handelsregister + Nummer
- [ ] USt-ID (bei Unternehmen mit USt-ID)
- [ ] Aufsichtsbehoerde (bei zulassungspflichtigen Berufen)
- [ ] Berufsrechtliche Angaben (bei reglementierten Berufen)
- [ ] **§ 18 Abs. 2 MStV** — "Verantwortlich fuer den Inhalt nach § 18 Abs. 2 MStV" bei journalistisch-redaktionellen Inhalten
- [ ] OS-Plattform-Link der EU (bei B2C-Online-Vertrag)
- [ ] Hinweis zur Verbraucherstreitbeilegung (§ 36 VSBG)

### Widerrufsbelehrung (§§ 355, 312g BGB)

- [ ] Muster-Widerrufsbelehrung Anlage 1 EGBGB VERWENDET oder eigene fehlerfreie?
- [ ] **14-Tage-Frist** genannt
- [ ] **Beginn der Frist** korrekt (je Vertragstyp)
- [ ] **Muster-Widerrufsformular** (Anlage 2 EGBGB) abgedruckt
- [ ] Widerrufs-Adresse mit Telefon, Fax (optional) und E-Mail
- [ ] **Wertersatz-Klausel** wenn Dienstleistung/digitale Inhalte vor Frist-Ende
- [ ] Bei digitalen Inhalten: **Erlöschens-Hinweis** + ausdrueckliche Zustimmung (§ 356 Abs. 5 BGB)

### Cookie-Richtlinie

- [ ] Liste aller Cookies mit Name, Anbieter, Zweck, Laufzeit
- [ ] Unterscheidung **technisch notwendig** vs. **einwilligungsbeduerftig**
- [ ] Rechtsgrundlage je Kategorie (§ 25 TDDDG + Art. 6 DSGVO)
- [ ] Widerrufs-Link zum CMP
- [ ] Drittland-Transfer bei US-Tools

### Social-Media-Bio (Linktree / Profil-Info)

- [ ] Direkter Link zu **Impressum**
- [ ] Direkter Link zu **Datenschutzerklaerung**
- [ ] Bei journalistisch-redaktionellen Profilen: "V.i.S.d.P. <Name, Anschrift>"
- [ ] Bei automatisiertem Posting (n8n/Zapier): Hinweis nach § 18 Abs. 3 MStV

## Disclaimer-Injection

Jede Output-Datei (`DocCheck.md`, `clean.md`, `evidence.md`) beginnt mit dem Disclaimer-Block aus `templates/disclaimer-block.md`. Der `PostToolUse`-Hook validiert das.

## Output-Verifikation

Am Ende muss erfuellt sein:
- [ ] `<zielordner>/DocCheck.md` mit Disclaimer + Finding-Tabelle
- [ ] `<zielordner>/clean.md` mit vollstaendiger korrigierter Version
- [ ] `<zielordner>/evidence.md` mit originalen Zitat-Stellen
- [ ] Zitat-Verifikations-Log in `.claude/logs/`

## Nach Abschluss

Gib dem User eine Kurz-Zusammenfassung:
- Erkannter Dokumenttyp + Konfidenz
- Anzahl Findings pro Severity
- Top-3 CRIT/HIGH mit 1-Zeilen-Beschreibung
- Empfehlung: Fachanwalts-Pruefung bei CRIT-Findings (Kontaktquellen siehe `knowledge/anwaelte-tools/`)
