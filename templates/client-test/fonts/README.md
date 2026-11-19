# Schriften für den Website-CheckUp-Report

Die Schriften werden beim Rendern als Data-URI in `report.html` eingebettet (`scripts/client_report/render.py`).
Es gibt keine externen Font-Requests.

## Quelle und Version

| Datei im Repo | Paket (npm-Registry) | Datei im Paket | Bytes | SHA-256 |
|---|---|---|---|---|
| `IBMPlexSans-Regular.woff2` | `@ibm/plex-sans@1.1.0` | `fonts/split/woff2/IBMPlexSans-Regular-Latin1.woff2` | 20984 | `b5ad7bd39f996144915f0ad9849a90183b27d8c28ad97ed98af5b1bebc51f6b1` |
| `IBMPlexSans-Italic.woff2` | `@ibm/plex-sans@1.1.0` | `fonts/split/woff2/IBMPlexSans-Italic-Latin1.woff2` | 22924 | `0a06b98143f3453b81f3c396241a01c6c4cff84c1a77bf0c75b18bd603018506` |
| `IBMPlexSans-SemiBold.woff2` | `@ibm/plex-sans@1.1.0` | `fonts/split/woff2/IBMPlexSans-SemiBold-Latin1.woff2` | 22260 | `fff0ab3a88b0b4aa0b693e4f0201359a15183b08e3fa5696d1918d8f0ade8ad5` |
| `IBMPlexSans-Bold.woff2` | `@ibm/plex-sans@1.1.0` | `fonts/split/woff2/IBMPlexSans-Bold-Latin1.woff2` | 21256 | `914f1400f363e636b6f9cc7965aa807ff01e93586e1437617525cba0a62aa78d` |
| `IBMPlexMono-Regular.woff2` | `@ibm/plex-mono@2.5.0` | `fonts/split/woff2/IBMPlexMono-Regular-Latin1.woff2` | 17544 | `e8993d946649b9d01abb1ed06d574b19d8ea3e66b5c3948602db335c44c18e56` |
| `OFL.txt` | beide Pakete, identisch | `LICENSE.txt` | 4456 | `7e6b2818edbd8f6a01ae80641cc8f16a51080d08fb4e532be3a0b6f74adb07da` |

Die Tarballs wurden am 2026-11-17 aus der npm-Registry bezogen und gegen `dist.integrity` geprüft:

- `@ibm/plex-sans@1.1.0`: `sha512-WPgvO6Yfj2w5YbhyAr1tv95RUz4LRJlqN+CmYvBglabXteufP1D1E9BABMde+ZIKdRbFJDoKF5eQzfhpnbgZcQ==`
- `@ibm/plex-mono@2.5.0`: `sha512-STBJIPxPomOYPmBMO7z5TKPJUotAF9u3gAUumTqVgwgrAO+K4FRNh0MlhsoJjKhJKsMbBJR10/bk4inkj/wc1w==`

Der SHA-256 von `OFL.txt` gilt für die Originaldatei mit CRLF-Zeilenenden; Git kann die Zeilenenden im Repo normalisieren.
Die woff2-Dateien sind binär und unverändert.

Dieselben Dateien liegen auch in den GitHub-Releases unter https://github.com/IBM/plex/releases.

## Zeichenumfang

Latin1-Teilmenge (unicode-range laut Paket-CSS): Umlaute, `ß`, `§`, `•`, `„“`, `…`.
Die Statussymbole ✓ ▲ ✕ und das Kästchen ☐ fehlen in dieser Teilmenge; der Renderer zeichnet sie
deshalb als eingebettete SVG-Grafik bzw. per CSS, immer mit Textlabel daneben
(Spike `docs/superpowers/spikes/2026-11-17-pagedjs-chrome-pdf.md`, Befund 2).

## Lizenz

SIL Open Font License 1.1, „Copyright © 2017 IBM Corp. with Reserved Font Name "Plex"“. Volltext in `OFL.txt`.
Die Schriften werden unverändert weitergegeben und nicht unter dem Namen „Plex“ verändert.
