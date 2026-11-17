# Spike: Paged.js und Chrome-PDF (Task 3)

Datum: 2026-11-17. Umgebung: Windows 11, Chrome 157.0.8103.51, Edge 157.0.4341.60, Python 3.10.6. Alle Messungen offline (alle Assets inline, kein Netzwerkzugriff nötig). Wegwerf-Dateien lagen im Scratch-Ordner, nichts davon im Repo.

## Entscheidung

| Konstante | Wert | Grund |
|---|---|---|
| `PAGED_JS_ENABLED` | **False** | Mit Paged.js ist die CLI-Ausgabe nicht stabil (Kriterium b verletzt). |
| Getaggtes PDF | **ja**, ohne weitere Schalter | Chrome 157 schreibt `/StructTreeRoot` in der CLI von selbst. |
| TOC-Seitenzahlen | **nein** (Fallback Spec 6.6) | Chrome kennt `target-counter()` nicht; Paged.js scheidet aus. |
| `PDF_MODE` | **"cli"** | Kein CDP-Client (Task 10b) nötig, getaggtes PDF kommt aus der CLI. |

Regel aus dem Plan (Task 3, Step 4): Ist (b) mit Paged.js nicht stabil, gilt die Variante ohne Paged.js. Zusätzlich gilt: Ein getaggtes PDF hat Vorrang vor TOC-Seitenzahlen. Folge: Überblick ohne Spalte "Seite", Finding-IDs bleiben klickbare Anker. Es entstehen kein `templates/client-test/vendor/` und keine Paged.js-Lizenzdatei.

## Messung

Testdokument: 12 Seiten (Inhaltsverzeichnis plus 11 Abschnitte, h1 bis h3, `<code>`, `<img alt>`), `@page` mit `@top-center` "Vertraulich" und `@bottom-right` `"Seite " counter(page) " von " counter(pages)`, IBM Plex Sans und Mono als Data-URI, TOC mit `a::after { content: target-counter(attr(href), page) }`. Variante "paged" bindet Paged.js 0.4.3 inline ein (503181 Byte), Variante "plain" nicht.

Argumentliste: `--headless=new --disable-gpu --no-first-run --disable-extensions --user-data-dir=<tmp> --no-pdf-header-footer --virtual-time-budget=15000 --generate-pdf-document-outline --print-to-pdf=<out.pdf> <file-uri>`

| Messung | Chrome ohne Paged.js | Chrome mit Paged.js | Edge ohne Paged.js |
|---|---|---|---|
| (a) PDF ohne Netz, unter 60 s | ja, 0,9 bis 1,3 s | ja, ca. 1 s (aber siehe b) | ja, ca. 2,5 s |
| (b) Seitenzahl über 3 Läufe | 12, 12, 12 (stabil) | 1, 2, 1 (instabil) | 12, 12, 12 |
| (c) Kopf und "Seite x von y" je Seite | ja, alle 12 Seiten (pdftotext) | nicht auswertbar | nicht geprüft |
| (d) TOC-Seitenzahlen | nein, `target-counter` wird ignoriert | n/a | nein |
| (e) `/StructTreeRoot` | ja (plus `/MarkInfo`, `/Lang de`) | teils (nur bei Fehlläufen mit 2 bis 3 Seiten) | ja |
| (f) `/Outlines` | ja | teils | ja |

Weitere Versuche mit Paged.js, alle ohne Erfolg: `--virtual-time-budget=60000` (Läufe mit 3, 1, 1 Seiten), zusätzlich `--run-all-compositor-stages-before-draw` (1, 1, 1 Seiten). Edge mit Paged.js: 1 Seite. Paged.js ist mit der CLI-Druckroute damit nicht brauchbar.

Details der Variante ohne Paged.js (Chrome):
- Strukturbaum: `Document`, `H1` x12, `H2` x11, `H3` x11, `P`, `Link` x11, `Code` x11, `Figure` x1 mit `/Alt (Beispielbild)`; Lesereihenfolge gleich DOM-Reihenfolge.
- Eingebettete Fonts: IBMPlexSans, IBMPlexSans-Bold, IBMPlexMono. Umlaute, `•`, `„…“` stehen korrekt im Textlayer.
- Die Läufe sind nicht byte-identisch (Zeitstempel und Dokument-ID), aber seitengleich.
- Kopf "Vertraulich" und "Seite n von 12" stehen nativ über `@page`-Margin-Boxen auf jeder Seite. `counter(pages)` funktioniert in Chrome 157 ohne Paged.js.

## Befunde für Task 8 und Task 10

1. **Edge startet detached** (Task 10): Der Edge-Prozess kehrt mit Exit-Code 0 zurück, bevor die PDF-Datei geschrieben ist. Chrome blockiert dagegen bis zum Ende. `print_pdf` muss nach dem Prozessende bis zu einem Zeitlimit auf die Datei warten (Polling auf Existenz und `%PDF-`-Anfang, danach kurz stabilisieren), sonst scheitert der Edge-Fallback. Ein temporäres Profil darf erst nach dem Polling gelöscht werden.
2. **Statussymbole fehlen in der Plex-Teilmenge** (Task 8): Die Latin1-Teilmenge enthält `•` (U+2022), `„ “`, `–`, `›`, aber nicht `✓ ▲ ✕`. Chrome fällt dann auf Systemschriften zurück (im Test Segoe UI Symbol), das Bild hängt vom Betriebssystem ab. Empfehlung: Statussymbole als Inline-SVG oder CSS-Formen mit Textlabel daneben rendern, nicht als Zeichen.
3. **Keine TOC-Seitenzahlen** (Task 8): Überblick ohne Spalte "Seite"; die Finding-ID verlinkt per `<a href="#id">` (im PDF als Link-Annotation erhalten, 11 von 11 im Test).
4. **Alt-Texte**: `<img alt>` landet als `/Alt` an einem `Figure`-Knoten; `evidence[].alt` genügt für das getaggte PDF.
5. `--generate-pdf-document-outline` erzeugt `/Outlines` aus h1 bis h3.
6. Titel: Chrome übernimmt `<title>` als PDF-Titel; `<html lang="de">` wird zu `/Lang (de)`.

## Asset-Quellen (für Task 8)

Offiziell vom npm-Registry-Tarball bezogen, Lizenz OFL-1.1 (IBM Plex) bzw. MIT (Paged.js):

| Asset | Quelle | Datei | Bytes | SHA-256 (Anfang) |
|---|---|---|---|---|
| IBM Plex Sans 1.1.0 | `@ibm/plex-sans` | `fonts/split/woff2/IBMPlexSans-Regular-Latin1.woff2` | 20984 | b5ad7bd39f996144 |
| | | `IBMPlexSans-Italic-Latin1.woff2` | 22924 | 0a06b98143f3453b |
| | | `IBMPlexSans-SemiBold-Latin1.woff2` | 22260 | fff0ab3a88b0b4aa |
| | | `IBMPlexSans-Bold-Latin1.woff2` | 21256 | 914f1400f363e636 |
| IBM Plex Mono 2.5.0 | `@ibm/plex-mono` | `IBMPlexMono-Regular-Latin1.woff2` | 17544 | e8993d946649b9d0 |
| Paged.js 0.4.3 (nicht übernommen) | `pagedjs@0.4.3` | `dist/paged.polyfill.min.js` | 503181 | f44e35a6d5106d81 |

Lizenztext für die Fonts: `package/LICENSE.txt` der beiden Plex-Pakete (SIL OFL 1.1, "Copyright 2017 IBM Corp. with Reserved Font Name Plex"), SHA-256 7e6b2818edbd8f6a. Die Latin1-Teilmenge deckt Umlaute, `ß`, `•`, `–`, `„“` ab (unicode-range laut Paket-CSS). Task 8 kann die Dateien aus denselben Tarballs neu beziehen und die vollständigen SHA-256-Werte in `fonts/README.md` eintragen; der Plan nennt als Quelle die GitHub-Releases, die npm-Pakete enthalten dieselben Dateien.
