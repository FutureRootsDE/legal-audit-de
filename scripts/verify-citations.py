#!/usr/bin/env python3
"""
Sammelpruefung von Bundesgerichts-Aktenzeichen in knowledge/ gegen die
Rechtsinformations-API des Bundes (https://testphase.rechtsinformationen.bund.de).

Die API ist OPTIONALE Beschleunigung (Testphase, keine Stabilitaetszusage, keine
dokumentierte Datenlizenz). Sie deckt nur sieben Bundesgerichte ab (BGH ab etwa
2010, BFH, BVerwG, BPatG, BAG, BSG, BVerfG). "Kein Treffer" ist deshalb NIE ein
Gegenbeweis; nicht abgedeckte Gerichte (OLG/LG/OVG/VG/LAG, EuGH/EuG) werden nur
ausgewiesen, nicht abgefragt.

Klassifikation je Zitat:
  VERIFIED        Treffer, KB-Datum stimmt oder fehlt
  DATE_MISMATCH   Treffer, aber die KB nennt ein anderes Datum
  NOT_IN_DATASET  abgedecktes Gericht, kein Treffer (kein Gegenbeweis)
  NOT_COVERED     Gericht nicht im Bestand der API
  ERROR           API nicht erreichbar oder Fehlerantwort
  UNCHECKED       nur mit --offline: kein Cache-Eintrag vorhanden

Schreibt standardmaessig nie in KB-Dateien. Nur mit --write-ecli wird fuer
Dateien unter knowledge/urteile/ ohne `ecli:` genau diese eine Zeile ins
Frontmatter eingefuegt (Vorschau mit --dry-run). Marker entfernt das Skript nie.

Die Logik liegt im Paket scripts/citation_check/ (nur Standardbibliothek, kein
Installationsschritt); dieses Skript ist nur der Einstiegspunkt.

Beispiele:
  python scripts/verify-citations.py
  python scripts/verify-citations.py --json --only-pending
  python scripts/verify-citations.py --offline
  python scripts/verify-citations.py --write-ecli --dry-run
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from citation_check.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
