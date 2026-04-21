---
aktualisiert: 2026-04-19
quelle-primaer: https://www.gesetze-im-internet.de/urhg/
quellen-sekundaer:
  - https://www.gesetze-im-internet.de/urhg/__44b.html
  - https://www.gesetze-im-internet.de/urhg/__60d.html
  - https://www.lto.de/recht/hintergruende/h/kuenstliche-intelligenz-ki-urheberrecht-text-data-mining-lg-hamburg-310o22723
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
- **`ai.txt`** (TDM Reservation Protocol)
- `Content-Usage`/`TDM-Reservation` HTTP-Header
- **C2PA-Metadaten** in Bildern
- Textuelle AGB-Klauseln (streitig, ob "maschinenlesbar")
- **TDMRep** (W3C-Entwurf)

### § 60d UrhG — TDM fuer wissenschaftliche Forschung

Gilt fuer **Forschungsorganisationen** (Universitaeten, nichtkommerzielle Forschungseinrichtungen). Hier ist das Opt-Out **nicht** anwendbar — die Schranke ist zwingend.

Das **LG Hamburg (LAION-Urteil)** hat § 60d auf die LAION-Datensatzerstellung angewandt, da LAION als Forschungsorganisation eingestuft wurde.

### Weitere relevante Normen

- **§ 2 UrhG** — Werkbegriff (Schoepfungshoehe, "kleine Muenze" bei Fotos + § 72 UrhG Lichtbildschutz)
- **§ 23 UrhG** — Bearbeitungen / freie Benutzung (durch Reform 2021 reformiert; "hinreichender Abstand")
- **§ 51 UrhG** — Zitatrecht (fuer Content-Erstellung relevant)
- **§ 72 UrhG** — Schutz einfacher Lichtbilder (50 Jahre ab Erscheinen; Untergrenze: mehr als bloss technische Reproduktion)
- **§ 97 UrhG** — Unterlassungs- und Schadensersatzanspruch; **Lizenzanalogie** als Schadensberechnung etabliert
- **§ 95a UrhG** — Umgehung technischer Schutzmassnahmen verboten
- **§ 97a UrhG** — Abmahnung; **Deckelung auf 1.000 EUR Gegenstandswert** bei einfach gelagerten Faellen gegen Privatpersonen ausserhalb gewerblicher Taetigkeit

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
- **Embedding vs. Hotlinking**: OEmbed von YouTube typisch zulaessig; **Inline-Hotlinking** fremder Bilder ist oft Urheberrechtsverletzung
- **Eigener KI-generierter Content**: Kein Schutz durch UrhG (kein Schoepfer), aber evtl. wettbewerbsrechtlicher Leistungsschutz
- **Trainingsdaten fuer Inhouse-KI**: Opt-Out der Quelle pruefen!

### Marketplace / UGC

- **Safe Harbor nach § 10 UrhG** nur bei Hostprovider-Status; bei aktiver Rolle (Redaktion) haftet Provider selbst
- **Art. 17 DSM-RL / § 1 UrhDaG** — Upload-Filter-Pflicht fuer "Diensteanbieter fuer das Teilen von Online-Inhalten"

## Relevanz fuer Codebase-Typen

- **Next.js SaaS**: KI-Features pruefen — respektiert eingesetzte Foundation Model Opt-Outs? Wenn eigene Modelle trainiert werden: § 44b Opt-Out-Compliance
- **Landingpage**: Stockfoto-Lizenzen dokumentieren (siehe [[../themen/urheber-stockfoto]])
- **n8n Automation**: Wenn Workflows Webseiten scrapen/crawlen → Opt-Out-Mechanismen einbauen (robots.txt-Check, ai.txt-Pruefung)
- **E-Commerce**: Produktbilder von Herstellern lizenziert? Modelfotos korrekt? Bei User-Reviews mit Fotos: UGC-Haftungsregelung
- **Content/Blog**: KI-generierter Text kein UrhG-Schutz; zitierte Quellen korrekt nach § 51 UrhG zitieren

## Behoerden-Hinweise

- **Deutsches Patent- und Markenamt (DPMA)**: Nicht fuer Urheberrecht zustaendig, aber fuer angrenzendes IP
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

**Berufungsinstanz**: Verfahren ging zur Berufung zum OLG Hamburg. `<<VERIFIKATION AUSSTEHEND>>` — Stand des OLG-Urteils pruefen.

### BGH und EuGH zum Lichtbildschutz und Werkbegriff

- **EuGH, Cofemel (C-683/17)** — Werkbegriff harmonisiert
- **BGH "Reformistischer Aufbruch"** — Zitatrecht § 51 UrhG
- **BGH, Urt. v. 20.09.2012 — I ZR 90/09 "UsedSoft II"** — Erschoepfung bei Software

## Siehe auch

- [[../themen/ki-content]] — KI-Training, Opt-Out-Mechanismen
- [[../themen/urheber-stockfoto]] — Stock-Foto-Lizenzen (Unsplash, Pexels, Shutterstock)
- [[ai-act]] — GPAI-Pflichten nach Art. 53 AI Act zu TDM-Opt-Out
- [[markeng]] — Abgrenzung zu Markenrecht
