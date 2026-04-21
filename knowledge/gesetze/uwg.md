---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/uwg_2004/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/uwg_2004/__7.html
  - https://www.gesetze-im-internet.de/uwg_2004/__5a.html
  - https://www.bmj.de/DE/themen/verbraucherrecht/lauterkeitsrecht/uwg_node.html
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

# UWG — Gesetz gegen den unlauteren Wettbewerb

## Kurz-Ueberblick

Das Gesetz gegen den unlauteren Wettbewerb (UWG) schuetzt Mitbewerber, Verbraucher
und sonstige Marktteilnehmer vor unlauteren geschaeftlichen Handlungen sowie das
Interesse der Allgemeinheit an unverfaelschtem Wettbewerb (§ 1 UWG).

Fuer Codebases besonders relevant:

- **§ 7 UWG** — unzumutbare Belaestigungen (E-Mail-/SMS-Marketing, Cold-Call)
- **§ 5 UWG** — irrefuehrende geschaeftliche Handlungen
- **§ 5a UWG** — Irrefuehrung durch Unterlassen (Influencer-Kennzeichnung)
- **§ 5b UWG** — wesentliche Informationen (Preis, Anbieter)
- **§§ 8-11 UWG** — Rechtsfolgen: Unterlassung, Beseitigung, Schadensersatz
- Anhang zu § 3 Abs. 3 UWG ("schwarze Liste") — per se unzulaessige Handlungen

Die UWG-Novelle 2022 ("Gesetz zur Staerkung des Verbraucherschutzes im Wettbewerbs-
und Gewerberecht") hat § 5a neu gefasst und § 9 Abs. 2 UWG (individueller
Schadensersatz-Anspruch von Verbrauchern bei vorsaetzlicher Irrefuehrung) eingefuehrt.

## Schluesselparagraphen / Kernaussagen

### § 7 UWG — Unzumutbare Belaestigungen

**Abs. 1:** "Eine geschaeftliche Handlung, durch die ein Marktteilnehmer in
unzumutbarer Weise belaestigt wird, ist unzulaessig."

**Abs. 2 Nr. 2 — Elektronische Post / SMS / Fax / Auto-Dialer:** Unzumutbare
Belaestigung liegt stets vor bei Werbung "unter Verwendung einer automatischen
Anrufmaschine, eines Faxgeraetes oder elektronischer Post, ohne dass eine
vorherige ausdrueckliche Einwilligung des Adressaten vorliegt".

Konsequenz: Newsletter-Versand ohne dokumentierte **Double-Opt-In-Einwilligung**
ist abmahnfaehig. Der Werbende traegt die Darlegungs- und Beweislast fuer die
Einwilligung (siehe BGH I ZR 218/07 "Payback").

**Abs. 3 — Bestandskundenausnahme:** Abweichend von Abs. 2 Nr. 2 ist eine
Einwilligung fuer E-Mail-Werbung **nicht erforderlich**, wenn kumulativ:

1. der Unternehmer die E-Mail-Adresse im Zusammenhang mit dem **Verkauf einer
   Ware oder Dienstleistung** von seinem Kunden erhalten hat,
2. er die Adresse zur **Direktwerbung fuer eigene aehnliche Waren oder
   Dienstleistungen** verwendet,
3. der Kunde der Verwendung **nicht widersprochen** hat und
4. der Kunde bei Erhebung der Adresse und bei **jeder Verwendung** klar und
   deutlich darauf hingewiesen wird, dass er der Verwendung jederzeit
   widersprechen kann, **ohne dass hierfuer andere als die Uebermittlungskosten
   nach den Basistarifen** entstehen.

**Abs. 4:** Bei jeder Werbung unter elektronischer Post muss die Identitaet des
Absenders, in dessen Auftrag die Nachricht uebermittelt wird, nicht verschleiert
oder verheimlicht werden und eine gueltige Adresse fuer Widerruf enthalten sein.

### § 5a Abs. 4 UWG — Kommerzielle Kommunikation kennzeichnen

"Unlauter handelt auch, wer den kommerziellen Zweck einer geschaeftlichen
Handlung nicht kenntlich macht, sofern sich dieser nicht unmittelbar aus den
Umstaenden ergibt, und das Nichtkenntlichmachen geeignet ist, den Verbraucher
zu einer geschaeftlichen Entscheidung zu veranlassen, die er andernfalls nicht
getroffen haette."

Entscheidend fuer Influencer-Posts: "Ein kommerzieller Zweck liegt bei einer
Handlung zugunsten eines fremden Unternehmens nicht vor, wenn der Handelnde
kein Entgelt oder keine aehnliche Gegenleistung fuer die Handlung von dem
fremden Unternehmen erhaelt oder sich versprechen laesst."

Beweislast: Die Gegenleistung wird **vermutet**, sofern der Handelnde nicht
glaubhaft macht, dass er keine erhalten hat.

### § 8 UWG — Unterlassungs-/Beseitigungsanspruch

Aktivlegitimiert sind:

- **Mitbewerber** (§ 8 Abs. 3 Nr. 1)
- qualifizierte **Wirtschaftsverbaende** (Nr. 2, nach Eintragung in Liste)
- qualifizierte **Verbraucherverbaende** (Nr. 3)
- **IHK/HWK** (Nr. 4)

Klassisches Abmahn-Risiko bei Online-Shops, SaaS-Signup-Seiten und Influencer-
Content.

### Anhang zu § 3 Abs. 3 UWG — "Schwarze Liste"

Enthaelt 32 per se unzulaessige Handlungen, u.a.:

- Nr. 11: als Information getarnte redaktionelle Werbung ohne Kennzeichnung
- Nr. 17: unverlangte telefonische Werbung gegenueber Verbrauchern
- Nr. 26: hartnaeckiges Bedraengen per E-Mail/Telefon/Fax

## Typische Fallstricke in Codebases

1. **Newsletter-Signup ohne Double-Opt-In:** Einfaches "E-Mail eintragen + Send"
   reicht NICHT. Erforderlich: Bestaetigungs-Mail mit Link, geloggter Timestamp
   + IP + verwendeter Einwilligungstext.
2. **Pre-ticked Checkboxen:** Bereits angekreuzte Consent-Boxen sind unwirksam
   (EuGH C-673/17 "Planet49", auf § 7 UWG uebertragen).
3. **Fehlender Abmeldelink:** Jede Werbe-E-Mail muss einen funktionierenden
   Unsubscribe-Mechanismus enthalten (§ 7 Abs. 2 Nr. 4, Abs. 4 UWG; auch
   Art. 21 DSGVO).
4. **Transaktions-Mails mit Cross-Selling:** "Ihre Bestellung #123 — Vielleicht
   interessiert Sie auch..." ist Werbung i.S.v. § 7 UWG und braucht Einwilligung.
5. **Influencer-Kooperationen ohne Kennzeichnung:** Automatisch generierte
   Affiliate-Links, Creator-Codes oder Gifted-Product-Posts MUSSEN als
   "#Werbung" / "#Anzeige" erkennbar sein. "#ad" reicht laut BGH-Rechtsprechung
   nicht aus, wenn am Ende einer Hashtag-Liste versteckt.
6. **Tracking ohne Consent:** Zwar primaer DSGVO/TTDSG, aber §§ 5, 5a UWG bei
   verschleierten Tracking-Hinweisen.

## Relevanz fuer Codebase-Typen

- **Next.js SaaS:** Signup-Flow mit Marketing-Consent muss Double-Opt-In
  implementieren; separate Checkbox fuer Newsletter (nicht gekoppelt an ToS).
- **Landingpage:** Contact-Forms mit "Jetzt Angebot anfordern" plus
  stillschweigend versandten Nurturing-Mails sind riskant — expliziter Consent
  erforderlich.
- **n8n-Workflows:** Automatisierte E-Mail-Sequenzen (Drip-Campaigns) brauchen
  Consent-State aus der Datenquelle (CRM, DB); Workflow sollte Opt-Out-Flags
  filtern BEVOR er sendet.
- **E-Commerce:** Bestandskundenausnahme nach § 7 Abs. 3 nutzen, aber nur fuer
  "aehnliche Waren/DL" + jedem Mailing Opt-Out beifuegen.
- **Content/Blog:** Sponsored Posts und Affiliate-Reviews: Kennzeichnung
  "Werbung" prominent AM ANFANG, nicht unten.

## Behoerden-Hinweise

- **Zustaendig fuer Durchsetzung:** keine zentrale Bundesbehoerde — Zivilrechtsweg
  ueber Abmahnung, einstweilige Verfuegung, Unterlassungsklage.
- **Bundeskartellamt:** nur bei marktmaechtigen Unternehmen (vgl. EuGH
  C-252/21 Meta).
- **Wettbewerbszentrale (Zentrale zur Bekaempfung unlauteren Wettbewerbs):**
  haeufigster Abmahner gegen unlautere B2C-Werbung.
- **Verbraucherzentrale Bundesverband (vzbv):** klagt regelmaessig gegen Plattformen.

## Zitierbare Urteile

- **BGH I ZR 186/17** (13.01.2022, "Inbox-Werbung II", nach EuGH C-102/20):
  Eingeblendete Werbung im E-Mail-Posteingang ist elektronische Post i.S.v.
  § 7 Abs. 2 Nr. 2 UWG und benoetigt Einwilligung. Siehe
  [[urteile/bgh-inbox-werbung]].
- **BGH I ZR 218/07** (10.02.2011, "Payback"): Einwilligung muss aktiv und
  bewusst erklaert werden; Opt-Out-Mechanismen reichen nicht.
- **BGH I ZR 164/09** (14.03.2012, "Double-Opt-In"): Best-Practice-Standard
  fuer Einwilligungs-Nachweis.
- **BGH I ZR 90/20** (09.09.2021, "Influencer I/II/III"): Kennzeichnungspflicht
  fuer kommerzielle Instagram-Posts.
- **BGH I ZR 186/21** "Cookie-Einwilligung" — verweist auf § 25 TTDSG.
- **EuGH C-673/17** (01.10.2019, "Planet49"): Vorangekreuzte Consent-Checkbox
  ist unwirksam.

## Siehe auch

- [[gesetze/bgb-agb]] — Verbraucherschutz-Normen
- [[gesetze/ddg]] — Impressumspflicht § 5 DDG
- [[themen/email-marketing]]
- [[themen/werbekennzeichnung]]
- [[urteile/bgh-inbox-werbung]]
