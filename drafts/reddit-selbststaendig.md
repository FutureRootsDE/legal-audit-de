# Reddit-Draft — r/selbststaendig

Subreddit: r/selbststaendig
Zielgruppe: Solo-Selbstständige, Kleinunternehmer, Freelancer (gemischt technisch / nicht-technisch)
Status: Entwurf — vor Posten bitte Claims, Preise und Versionsnummer gegen aktuellen Stand prüfen.

---

## Titel

Open-Source-Tool für DSGVO/UWG-Vorabprüfung — entstanden, weil ich meine eigenen Anwaltsrechnungen leid war

---

## Body

**Hintergrund:**

Ich bin Solo-Gründer, baue seit einem knappen halben Jahr ein B2B-SaaS in Richtung Steuer-Compliance. Kleinunternehmer-Status, keine Rechtsabteilung, kein DSB, kein Pufferbudget. Vor dem geplanten Launch ging jede Frage zu Cookie-Banner, AVV, Datenschutzerklärung oder Impressum an eine Kanzlei. Pro Runde 300–500 EUR, zwei Wochen Wartezeit, und hinterher oft Korrekturen an Stellen, die ich selbst hätte finden können — wenn ich nur gewusst hätte, wonach ich suchen muss.

Zwei reale Beispiele aus meinem eigenen Entwurf:

- Impressum zitierte noch **§ 5 TMG** statt **§ 5 DDG**. TMG ist seit dem 14.05.2024 weg. Kein direkter Abmahngrund, aber ein Qualitätsmangel, der den Anwalt unnötig Zeit kostet (= mein Geld).
- Datenschutzerklärung schrieb **„TTDSG § 25 Abs. 2"**. Wurde am gleichen Datum in **TDDDG** umbenannt. Wieder kein Drama, aber peinlich — und hätte ich selbst sehen können, wenn das passende Werkzeug existiert hätte.

Hat es nicht. Also habe ich es gebaut.

**Was es ist:**

Ein Plugin für Claude Code (das CLI-Tool von Anthropic), das eine Website oder einen Code-Stand systematisch durchgeht, Findings nach Schweregrad klassifiziert (CRIT / HIGH / MED / LOW) und für jedes Finding eine sauber formulierte Korrekturversion liefert. Zitate werden gegen **eur-lex.europa.eu**, **gesetze-im-internet.de** und **curia.europa.eu** verifiziert — nicht gegen Kanzlei-Blogs. Output ist eine Briefing-Datei, die ihr eurem Anwalt zur **Freigabe** vorlegt, nicht zur Erst-Prüfung.

Konkret kann es:

- Codebase-Audit (Next.js, WordPress, Shopify, n8n, statische Sites)
- Live-Browser-Check einer URL: Welche Tracker laden **vor** Consent? Lädt Google Fonts trotz „self-hosted"-Bekenntnis? Hat das Cookie-Banner einen gleichrangigen Ablehnen-Button (Stichwort EuGH Planet49)?
- Einzeldokument-Review (AGB / DSE / Impressum / Widerrufsbelehrung / Cookie-Richtlinie)
- Knowledge-Base mit 63 Artikeln zu DSGVO, BDSG, TDDDG, UWG, PAngV, BGB-AGB, DDG, DSA, DMA, AI Act, BFSG, UrhG, MarkenG, NIS2 — inklusive Schlüsselurteile (Schrems II, Planet49, Google Fonts, Meta–Bundeskartellamt, Inbox-Werbung II, IAB Europe)

**Ein Stück Ehrlichkeit zur eigenen Tool-Qualität:**

Beim letzten internen Re-Check der eigenen Wissensbasis (`/legal-update --all`) sind 6 schwere Aktenzeichen-Fehler aus der initialen KI-Befüllung aufgefallen und korrigiert worden — z. B. stand bei „Inbox-Werbung II" das falsche Aktenzeichen, und ein erfundener „§ 7 Abs. 4 UWG" hatte sich eingeschlichen. Lehre für alle, die mit KI an Rechtsinhalten arbeiten: KI-generierte Rechts-Inhalte gehören **immer** gegen die Primärquelle gegengeprüft, bevor sie irgendwo als Referenz dienen. Das Tool macht das jetzt automatisiert für sich selbst — was es vor dem Launch *nicht* getan hat.

**Was es ausdrücklich nicht ist:**

- **Keine Rechtsberatung im Sinne § 2 RDG.** Jede Ausgabe trägt den Disclaimer, das steht auch in der MIT-Lizenz. Die Logik ist: ihr übergebt eurem Anwalt eine saubere Vorarbeit — ihr setzt Rechtstexte nicht ohne anwaltlichen Review live.
- **Kein Ersatz für einen Datenschutzbeauftragten**, wenn ihr nach § 38 BDSG einen bestellen müsst (ab 20 Personen mit ständiger automatisierter PII-Verarbeitung).
- **Scope ist strikt DE/EU.** Keine US-/UK-/CH-Logik. Wer international skaliert, prüft pro Jurisdiktion getrennt.

**Voraussetzung (ehrlich):**

Das Plugin läuft in Claude Code, einer Kommandozeilen-Umgebung. Wer noch nie ein Terminal aufhatte, braucht entweder eine halbe Stunde Einarbeitung oder jemanden im Team / Freundeskreis, der das übernimmt. Ist kein Web-Tool, kein Klick-und-fertig. Dafür komplett lokal — keine Daten verlassen euren Rechner außer zu Anthropic während der Analyse.

**Warum Open Source unter MIT:**

Weil ich überzeugt bin, dass viele Solo-Selbstständige, Kleinunternehmer und kleine Teams genau dieses Vorbereitungsproblem haben. Wenn eure erste Version 30 % besser beim Anwalt ankommt, zahlt ihr weniger für die gleiche Freigabe. Wenn jemand das kommerziell weiterbauen will — die Lizenz erlaubt es.

**Links:**

- GitHub: github.com/FutureRootsDE/legal-audit-de
- Aktuelles Release: **v1.3.1 (09.05.2026)**
- Changelog im Repo, inkl. aller Aktenzeichen-Korrekturen und der neuen BGH-Urteile vom 09.10.2025 (Button-Lösung, Streichpreis-Werbung)

Seit v1.3.0 läuft das Plugin nicht nur in Claude Code, sondern auch in der **OpenAI Codex CLI** und **GitHub Copilot CLI** — wer also lieber bei OpenAI oder GitHub bleibt, kann das Tool dort genauso nutzen. v1.3.1 ist übrigens zu 100 % aus dem ersten externen Community-PR entstanden (Danke an @AllstarGER), der die Codex-Integration tatsächlich gegen die echte Codex CLI verifiziert und einen Frontmatter-Bug aus v1.3.0 mitgefixt hat. Genau dafür ist Open Source da.

Installation:

```
# Claude Code
/plugin marketplace add FutureRootsDE/legal-audit-de
/plugin install legal-audit-de

# Codex CLI
codex plugin marketplace add FutureRootsDE/legal-audit-de

# Copilot CLI: siehe README im Repo
```

Über Feedback und PRs freue ich mich — besonders, wenn jemand Fehler in der Wissensbasis findet. Zitate mit Link zur Primärquelle baue ich schnell ein, Kanzlei-Blog-Verweise nicht.

---

## Vor dem Posten prüfen

- [ ] Subreddit-Regeln r/selbststaendig: Self-Promotion-Ratio (i. d. R. 9:1), Tool-/Werbe-Regeln, Wochentag/Megathread-Pflicht
- [ ] Versionsnummer aktuell: **v1.3.1 (09.05.2026)** — vor Posten gegen letzten Tag im Repo abgleichen
- [ ] Aktenzeichen-Fehler-Beispiele („Inbox-Werbung II", „§ 7 Abs. 4 UWG") sind im öffentlichen CHANGELOG v1.2.0 dokumentiert — okay zu erwähnen
- [ ] Multi-Platform-Claim (Claude Code / Codex CLI / Copilot CLI) entspricht v1.3.0+ — okay
- [ ] Codex-Installations-Befehl gegen aktuelle Codex-CLI-Syntax verifizieren (war in v1.3.1 PR getestet)
- [ ] Kein „Rechtsberatung"-Wording im Titel oder Body — Disclaimer-Position prüfen
- [ ] Flair setzen (vermutlich „Tool" / „Empfehlung" / „Diskussion" — je nach Sub-Konvention)
