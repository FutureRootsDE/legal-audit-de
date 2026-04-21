---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/uwg_2004/__7.html
quellen-sekundaer:
  - https://www.bfdi.bund.de/DE/Buerger/Inhalte/DatenschutzAZ/Werbung/Werbung-node.html
  - https://www.datenschutzkonferenz-online.de/
  - https://www.dr-schwenke.de/newsletter-rechtssicher/
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

# E-Mail-Marketing — Rechtliche Anforderungen

## Kurz-Ueberblick

E-Mail-Werbung an Verbraucher (B2C) und auch an Geschaeftskunden (B2B) ist in
Deutschland ohne **vorherige ausdrueckliche Einwilligung** (§ 7 Abs. 2 Nr. 2 UWG)
rechtswidrig. Zusaetzlich greifen die DSGVO (Art. 6 Abs. 1 lit. a) und — bei
Kopplung mit Tracking — das TTDSG / § 25 TTDSG.

Drei Saeulen der Compliance:

1. **Double-Opt-In** — zweistufige Einwilligung als Beweisstandard.
2. **Bestandskundenausnahme** — § 7 Abs. 3 UWG fuer bestehende Kundenbeziehungen.
3. **Abmelde-/Widerspruchslink** — in jeder einzelnen Werbemail (Art. 21 DSGVO,
   § 7 Abs. 2 Nr. 4 UWG).

## Schluesselparagraphen / Kernaussagen

### § 7 Abs. 2 Nr. 2 UWG — Einwilligungspflicht

Werbung per elektronischer Post (E-Mail, SMS, Messenger) benoetigt eine
**vorherige, ausdrueckliche, freiwillige, informierte, spezifische**
Einwilligung. Die Einwilligung muss in unmittelbarem Zusammenhang mit der
Werbemassnahme erfolgen und der Werbende muss sie nachweisen koennen
(Beweislast beim Versender).

**Konkrete Anforderungen (Double-Opt-In laut BGH I ZR 164/09):**

1. Formular-Eintrag (Single Opt-In) mit aktiver Handlung (leere Checkbox,
   die der Nutzer anhaken muss, oder expliziter "Anmelden"-Klick).
2. Versand einer **Bestaetigungs-Mail** an die angegebene Adresse mit einem
   **eindeutigen Bestaetigungslink**.
3. Klick auf den Link dokumentiert = Einwilligung.
4. **Logging** des Vorgangs: IP, User-Agent, Timestamp des Eintrags +
   Timestamp der Bestaetigung + genauer Einwilligungstext.

### § 7 Abs. 3 UWG — Bestandskundenausnahme

Vier kumulative Voraussetzungen:

1. E-Mail-Adresse **im Zusammenhang mit dem Verkauf** einer Ware/DL erhalten
   (nicht: nur Newsletter-Anmeldung, nicht: Lead-Magnet-Download).
2. Bewerbung nur fuer **aehnliche eigene** Waren/DL (z.B. Kaffeemaschine
   gekauft → Kaffeekapseln bewerben: OK; Kaffeemaschine gekauft → Waschmaschine
   bewerben: nicht OK).
3. Kunde **hat nicht widersprochen**.
4. Bei Adress-Erhebung UND bei **jeder Verwendung** klarer Hinweis auf
   Widerspruchsrecht (kein Aufwand ueber Basistarif).

### Art. 21 DSGVO — Widerspruchsrecht bei Direktwerbung

Jede betroffene Person hat das Recht, jederzeit der Verarbeitung
personenbezogener Daten zu Zwecken der Direktwerbung zu widersprechen. Der
Widerspruch muss **einfach und kostenfrei** moeglich sein — praktische
Umsetzung: One-Click-Unsubscribe-Link im Footer jeder Werbemail.

### § 7 Abs. 4 UWG — Identitaet

Identitaet des Absenders darf nicht verschleiert werden. Pflichtangaben in
der Mail:

- korrekter Absender-Name
- gueltige Reply-Adresse
- Impressum / Link zum Impressum

### Art. 13 DSGVO — Informationspflichten beim Opt-In

Beim Erheben der E-Mail-Adresse muss informiert werden:

- Identitaet des Verantwortlichen
- Zweck (E-Mail-Marketing)
- Rechtsgrundlage (Einwilligung Art. 6 Abs. 1 lit. a DSGVO)
- Empfaenger (insb. externer Newsletter-Provider → **Auftragsverarbeitung
  Art. 28 DSGVO**)
- Speicherdauer
- Rechte (Widerruf, Auskunft, Loeschung)
- ggf. Drittlandtransfer (z.B. Mailchimp → USA → DPF / SCC)

## Typische Fallstricke in Codebases

1. **Single-Opt-In (nur Formular-Submit):** Reicht NICHT, selbst wenn
   DSGVO-Checkbox dabei. Beweislast kann nicht erfuellt werden.
2. **Bestaetigungs-Mail = bereits Werbung:** Die Opt-In-Bestaetigungs-Mail
   darf KEINEN Werbe-Inhalt haben (OLG Muenchen 29 U 1563/20).
3. **Pre-checked Checkbox** bei Signup: nach Planet49 (EuGH C-673/17) unwirksam.
4. **Kopplung mit anderer Leistung** ("Erhalten Sie 10% Rabatt, wenn Sie
   unseren Newsletter abonnieren"): kann zulaessig sein, aber nicht an Vertrag
   koppeln (Art. 7 Abs. 4 DSGVO Kopplungsverbot).
5. **Forward-/Tell-a-Friend-Funktion:** Nachricht an Dritten ohne dessen
   Einwilligung → Direktwerbung des Versenders, abmahnfaehig (BGH I ZR 218/07).
6. **Logging luecken:** Kein Audit-Log → keine Einwilligung nachweisbar →
   Prozess verloren.
7. **Abmeldelink fuehrt zu 404 oder erfordert Login:** verstoesst gegen
   Art. 21 DSGVO / § 7 Abs. 2 Nr. 4 UWG; ein-Klick-Abmeldung Pflicht.
8. **Transaktions-Mail mit Marketing:** "Ihre Rechnung + 'passende Produkte'"
   ist rechtlich Werbung, nicht Transaktion.
9. **Re-Engagement-Kampagnen an alte Listen:** Opt-In > 24 Monate alt? Gefahr,
   dass Einwilligung verfristet / nicht mehr zeitgemaess ist (str., Tendenz
   Aufsicht: ja).
10. **Purchased Lists / Lead-Boersen:** Nahezu immer rechtswidrig (keine
    direkte Einwilligung gegenueber dem Werbenden).

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Signup-Form darf Newsletter-Opt-In NICHT mit ToS-Acceptance
  koppeln. Separate Checkbox "Ich moechte den Newsletter erhalten" (leer).
  Verwendung von react-hook-form + audit-log-Endpunkt.
- **Landingpage:** Lead-Magnet-Download mit Double-Opt-In Kaskade; erste Mail
  enthaelt Lead-Magnet + Opt-In-Bestaetigung gekoppelt → unsauber, besser:
  Bestaetigungs-Mail (nur DOI-Link), dann Lead-Magnet nach Bestaetigung.
- **n8n-Workflows:** Pre-Send-Filter gegen Abmelde-Liste (PostgreSQL-Table
  `unsubscribed_at IS NOT NULL`). Bei Kampagnen: letzten 30 Tage Bounce-Rate
  + Opt-In-Alter als Gating-Kriterium.
- **E-Commerce:** Bestandskundenausnahme § 7 Abs. 3 nutzen: Filter
  "last_order_at > NOW() - INTERVAL 2 YEARS" plus nur fuer "aehnliche
  Produkte" (gleiche Kategorie).
- **Content/Blog:** RSS-to-Email-Automation nur nach DOI; Gastautoren-Kommentar-
  Notifies nur bei Opt-In.

## Behoerden-Hinweise

- **Landes-Datenschutzbehoerden:** zustaendig fuer DSGVO-Verstoesse; Bussgelder
  bis 20 Mio. EUR / 4 % Jahresumsatz.
- **Wettbewerbszentrale, IDO, vzbv:** klassische UWG-Abmahner.
- **BfDI (Bundesbeauftragter):** nur fuer Telekom-/Post-Unternehmen und
  Bundesbehoerden zustaendig.
- **Konferenz der unabhaengigen Datenschutzaufsichtsbehoerden (DSK):**
  Orientierungshilfen: "Werbung" (2022), "Direktwerbung" (FAQ).

## Zitierbare Urteile

- **BGH I ZR 164/09** (10.02.2011 / Folgeurteil 2012, "Double-Opt-In"):
  Anerkennung des DOI-Standards.
- **BGH I ZR 218/07** (10.02.2011, "Payback"): Einwilligung muss bewusst und
  eindeutig sein; Opt-Out-Loesungen nicht ausreichend.
- **BGH I ZR 186/17** (13.01.2022, "Inbox-Werbung II"): Auch Inbox-Placements
  in Freemail-Postfaechern sind Werbung. Siehe [[urteile/bgh-inbox-werbung]].
- **EuGH C-102/20** (25.11.2021): Vorabentscheidung zum Begriff "elektronische
  Post" — breit auszulegen.
- **EuGH C-673/17** (01.10.2019, "Planet49"): Pre-ticked Checkboxen unwirksam.
- **BGH I ZR 61/20** (09.09.2021, "Influencer I/II/III"): Kommerzielle
  Kommunikation kennzeichnen.
- **OLG Muenchen 29 U 1563/20**: Bestaetigungs-Mail darf keine Werbung
  enthalten.

## Siehe auch

- [[gesetze/uwg]] — § 7 UWG
- [[themen/werbekennzeichnung]]
- [[urteile/bgh-inbox-werbung]]
