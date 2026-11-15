---
aktualisiert: 2026-11-15
quelle-primaer: https://www.gesetze-im-internet.de/urhg/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/urhg/__44b.html
  - https://www.gesetze-im-internet.de/urhg/__60d.html
  - https://www.lto.de/recht/hintergruende/h/kuenstliche-intelligenz-ki-urheberrecht-text-data-mining-lg-hamburg-310o22723
  - https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=OLG+Hamburg&Datum=10.12.2025&Aktenzeichen=5+U+104/24
verifiziert-am: 2026-10-24
teilverifiziert-am: 2026-11-15
geltungsbereich: [DE]
---

> **Haftungsausschluss — Keine Rechtsberatung**
>
> Dieses Dokument wurde von einer KI (Claude, Anthropic) auf Basis oeffentlicher
> Rechtsquellen erstellt. Es ist **ausdruecklich keine Rechtsberatung** im Sinne
> des § 2 RDG. Eine Pruefung durch einen zugelassenen Rechtsanwalt ist zwingend
> erforderlich, bevor Inhalte produktiv eingesetzt werden.
>
> **Stand:** 2026-10-24

# Urheberrechtsgesetz (UrhG) — Schwerpunkt KI-Training / § 44b

## Kurz-Ueberblick

Das UrhG schuetzt "persoenliche geistige Schoepfungen" (§ 2). Im Kontext von **KI-Training, Web-Scraping und Content-Aggregation** sind insbesondere die Schrankenregelungen **§ 44b UrhG (allgemeines Text-und-Data-Mining)** und **§ 60d UrhG (TDM fuer wissenschaftliche Forschung)** zentral.

Beide setzen Art. 3 und 4 der **DSM-Richtlinie (EU) 2019/790** um. Der entscheidende Streitpunkt — insbesondere fuer kommerzielles KI-Training auf Internet-Daten — ist die **Reichweite des Opt-Out** nach § 44b Abs. 3.

## Schluesselparagraphen / Kernaussagen

### § 44b UrhG — Text und Data Mining (kommerziell zulaessig)

**Abs. 1 — Definition:**
> "Text und Data Mining ist die automatisierte Analyse von einzelnen oder mehreren digitalen oder digitalisierten Werken, um daraus Informationen insbesondere ueber Muster, Trends und Korrelationen zu gewinnen."

**Abs. 2 — Erlaubnis:**
> "Zulaessig sind Vervielfaeltigungen von rechtmaessig zugaenglichen Werken fuer das Text und Data Mining. Die Vervielfaeltigungen sind zu loeschen, wenn sie fuer das Text und Data Mining nicht mehr erforderlich sind."

**Abs. 3 — Opt-Out (zentral fuer KI-Training):**
Die Nutzung ist nur erlaubt, "wenn der Rechtsinhaber sich diese nicht vorbehalten hat. Ein **Nutzungsvorbehalt** bei online zugaenglichen Werken ist nur dann wirksam, wenn er in **maschinenlesbarer Form** erfolgt."

Praktische Umsetzungen des Opt-Out:
- `robots.txt` (strittig, aber haeufig)
- `ai.txt` (herstellerspezifisches Format, kein Standard)
- **TDMRep** (TDM Reservation Protocol): `/.well-known/tdmrep.json`, HTTP-Header `tdm-reservation`, HTML-Meta-Angaben
- HTTP-Header `tdm-reservation` (TDMRep); `Content-Usage` (IETF-Entwurf, ungeprueft)
- **C2PA-Metadaten** in Bildern
- Textuelle AGB-Klauseln (streitig, ob "maschinenlesbar")
- **TDMRep** (Bericht einer W3C Community Group, kein W3C-Standard)

### § 60d UrhG — TDM fuer wissenschaftliche Forschung

Gilt fuer **Forschungsorganisationen** (Universitaeten, nichtkommerzielle Forschungseinrichtungen). Hier ist das Opt-Out **nicht** anwendbar — die Schranke ist zwingend.

Das **LG Hamburg (LAION-Urteil)** hat § 60d auf die LAION-Datensatzerstellung angewandt, da LAION als Forschungsorganisation eingestuft wurde.

### Weitere relevante Normen

- **§ 2 UrhG**: Werkbegriff (Schoepfungshoehe, auch "kleine Muenze"); **§ 72 UrhG**: Lichtbildschutz fuer Fotos ohne Werkqualitaet
- **§ 23 UrhG** — Bearbeitungen / freie Benutzung (durch Reform 2021 reformiert; "hinreichender Abstand")
- **§ 51 UrhG** — Zitatrecht (fuer Content-Erstellung relevant)
- **§ 72 UrhG** — Schutz einfacher Lichtbilder (50 Jahre ab Erscheinen; Untergrenze: mehr als bloss technische Reproduktion)
- **§ 97 UrhG** — Unterlassungs- und Schadensersatzanspruch; **Lizenzanalogie** als Schadensberechnung etabliert
- **§ 95a UrhG** — Umgehung technischer Schutzmassnahmen verboten
- **§ 97a UrhG** — Abmahnung; **Deckelung auf 1.000 EUR Gegenstandswert** (Abs. 3 Satz 2), wenn der Abgemahnte eine natuerliche Person ist, die nicht fuer ihre gewerbliche oder selbstaendige berufliche Taetigkeit handelt (Nr. 1), und nicht bereits zur Unterlassung verpflichtet ist (Nr. 2); gilt nicht, wenn der Wert nach den besonderen Umstaenden des Einzelfalles unbillig ist (Satz 4)

## Typische Fallstricke in Codebases

### KI-Training / Scraping

- **Ignorieren maschinenlesbarer Opt-Outs** (z. B. `noai`/`noimageai` in `robots.txt`, `ai.txt`) — Trainingsnutzung dann nicht durch § 44b gedeckt
- **"Rechtmaessige Zugaenglichkeit"**: Inhalte hinter Paywalls / Logins sind nicht "rechtmaessig zugaenglich" nur durch Scraping-Bypass
- **Keine Loeschung** der Trainings-Vervielfaeltigungen nach Abs. 2 Satz 2
- **Opt-Out-Konflikt mit AI Act GPAI-Pflichten**: Art. 53 AI Act verlangt, dass GPAI-Anbieter Opt-Outs **respektieren**

### Content-Erstellung (Next.js / CMS / Blog)

- **Bildnutzung ohne Lizenznachweis** (selbst wenn "gefundene" Bilder verwendet werden)
- **Keine Dokumentation der Lizenzen** fuer verwendete Assets (Stockfotos, Icons, Fonts)
- **Framework-Templates**: Themes/Plugins koennen eigene Urheberrechte haben
- **Embedding/Framing/Inline-Linking**: Einbetten eines mit Zustimmung des Rechtsinhabers frei zugaenglichen Werks ist grundsaetzlich keine oeffentliche Wiedergabe (EuGH, 21.10.2014, C-348/13; BGH, 09.07.2015, I ZR 46/12). Rechtsverletzend wird es, wenn Schutzmassnahmen gegen Framing umgangen werden (EuGH, 09.03.2021, C-392/19) oder die Quelle selbst rechtswidrig eingestellt ist. Kopieren auf den eigenen Server ist stets Vervielfaeltigung.
- **Eigener KI-generierter Content**: Kein Schutz durch UrhG (kein Schoepfer), aber evtl. wettbewerbsrechtlicher Leistungsschutz
- **Trainingsdaten fuer Inhouse-KI**: Opt-Out der Quelle pruefen!

### Marketplace / UGC

- **Haftungsprivileg fuer Hosting-Diensteanbieter** nur bei neutraler Rolle; bei aktiver Rolle (Redaktion) haftet der Anbieter selbst. § 10 UrhG betrifft nicht die Haftung, sondern die Vermutung der Urheberschaft.
- **Art. 17 DSM-RL / §§ 1, 2, 4, 7 bis 11 UrhDaG** — Diensteanbieter fuer das Teilen von Online-Inhalten (§ 2 Abs. 1) geben hochgeladene Werke selbst oeffentlich wieder; Enthaftung nur bei Lizenzbemuehungen (§ 4) und Blockierung auf Verlangen des Rechtsinhabers (§§ 7, 8). Ausnahmen: Startup-Diensteanbieter (§ 7 Abs. 4), kleine Diensteanbieter (§ 7 Abs. 5).

## Relevanz fuer Codebase-Typen

- **Next.js SaaS**: KI-Features pruefen — respektiert eingesetzte Foundation Model Opt-Outs? Wenn eigene Modelle trainiert werden: § 44b Opt-Out-Compliance
- **Landingpage**: Stockfoto-Lizenzen dokumentieren (siehe [[../themen/urheber-stockfoto]])
- **n8n Automation**: Wenn Workflows Webseiten scrapen/crawlen → Opt-Out-Mechanismen einbauen (robots.txt-Check, ai.txt-Pruefung)
- **E-Commerce**: Produktbilder von Herstellern lizenziert? Modelfotos korrekt? Bei User-Reviews mit Fotos: UGC-Haftungsregelung
- **Content/Blog**: KI-generierter Text kein UrhG-Schutz; zitierte Quellen korrekt nach § 51 UrhG zitieren

## Behoerden-Hinweise

- **Deutsches Patent- und Markenamt (DPMA)**: fuehrt kein Register fuer Urheberrechte (Schutz entsteht ohne Eintragung); zustaendig aber fuer das Register anonymer und pseudonymer Werke (§ 138 UrhG) und als Aufsichtsbehoerde ueber Verwertungsgesellschaften (§ 75 Abs. 1 VGG)
- **Bundesjustizministerium (BMJ)**: Fuer urheberrechtliche Gesetzgebungsvorhaben
- **Verwertungsgesellschaften** (VG Wort, GEMA, VG Bild-Kunst): Fuer kollektive Lizenzierung — relevant bei Musik, VG-Bild-Kunst-Nachveroeffentlichung

## Zitierbare Urteile

### LG Hamburg, Urt. v. 27.09.2024 — Az. 310 O 227/23 ("LAION/Kneschke")

**Sachverhalt**: Fotograf Kneschke klagte gegen LAION (nonprofit, LAION-5B-Datensatz) wegen Nutzung eines Bildes. Kernfragen:
1. Ist das Download fuer Datensatz-Erstellung TDM?
2. Greift Opt-Out nach § 44b Abs. 3?
3. Ist LAION als Forschungsorganisation nach § 60d privilegiert?

**Entscheidung**:
- **§ 60d greift zugunsten LAION** — LAION wurde als Forschungsorganisation eingestuft; kein wirksamer Opt-Out-Vorbehalt
- Gericht bestaetigt: Erstellung von KI-Trainingsdatensaetzen IST Text und Data Mining i.S.v. § 44b / § 60d
- Bezug zum AI Act (VO 2024/1689) als Auslegungshilfe — Unionsgesetzgeber habe TDM-Schranken auf KI-Training bezogen

**Bedeutung**: Erstes wegweisendes deutsches Urteil zur Zulaessigkeit von KI-Trainingsdatensaetzen. Beschraenkt aber auf Forschungskontext (§ 60d). Kommerzielles KI-Training bleibt an § 44b Abs. 3 Opt-Out gebunden.

**Berufungsinstanz — OLG Hamburg, Urt. v. 10.12.2025 — 5 U 104/24** (GRUR 2026, 398): Die Berufung des Klaegers wurde zurueckgewiesen, das erstinstanzliche Urteil im Ergebnis bestaetigt. Das Herunterladen rechtmaessig zugaenglicher Bilder zur Erstellung des LAION-5B-Datensatzes ist Text und Data Mining; LAION e.V. ist als nicht kommerziell taetige Forschungsorganisation nach § 60d UrhG privilegiert, auch wenn eine spaetere Nachnutzung durch kommerzielle Akteure moeglich ist. Da § 60d UrhG keinen Nutzungsvorbehalt kennt (anders als § 44b Abs. 3 UrhG), kam es auf die Wirksamkeit des Vorbehalts in den Nutzungsbedingungen der Bildplattform im Ergebnis nicht an; ob ein in natuerlicher Sprache formulierter Vorbehalt "maschinenlesbar" i.S.v. § 44b Abs. 3 S. 2 UrhG sein kann, bleibt damit offen.

**Revision — BGH, anhaengig: I ZR 281/25** (Stand 2026-10-24 kein Endurteil).

Quelle: dejure.org (Verfahrensgang mit GRUR-Fundstelle und BGH-Az.), Normtext § 44b und § 60d UrhG (gesetze-im-internet.de).

### BGH und EuGH zum Lichtbildschutz und Werkbegriff

- **EuGH, Cofemel (C-683/17)** — Werkbegriff harmonisiert
- **BGH, Urt. v. 30.04.2020 — I ZR 228/15 "Reformistischer Aufbruch II"** (ECLI:DE:BGH:2020:300420UIZR228.15.0) — Berichterstattung ueber Tagesereignisse (§ 50 UrhG), Verhaeltnismaessigkeit
- **BGH, Urt. v. 17.07.2013 — I ZR 129/08 "UsedSoft II"** — Erschoepfung bei heruntergeladenen Programmkopien

## Siehe auch

- [[../themen/ki-content]] — KI-Training, Opt-Out-Mechanismen
- [[../themen/urheber-stockfoto]] — Stock-Foto-Lizenzen (Unsplash, Pexels, Shutterstock)
- [[ai-act]] — GPAI-Pflichten nach Art. 53 AI Act zu TDM-Opt-Out
- [[markeng]] — Abgrenzung zu Markenrecht
