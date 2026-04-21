---
description: Laedt gezielt einen Knowledge-Base-Chunk (Gesetz/Thema/Urteil/Checkliste/Behoerde/Anwalts-Empfehlung) in den aktuellen Kontext.
argument-hint: <thema-slug | gesetz-slug | urteil-slug>
allowed-tools: Bash, Read, Glob
---

# /legal-kb

Laedt explizit eine oder mehrere KB-Dateien zum Thema `$ARGUMENTS` und zeigt sie an.

## Ablauf

1. **Slug-Normalisierung:** `$ARGUMENTS` → lowercase, Bindestriche statt Spaces.

2. **Suche in dieser Prioritaet:**
   1. `knowledge/themen/<slug>.md`
   2. `knowledge/gesetze/<slug>.md`
   3. `knowledge/urteile/<slug>.md`
   4. `knowledge/checklisten/<slug>.md`
   5. `knowledge/behoerden/<slug>.md`
   6. `knowledge/anwaelte-tools/<slug>.md`

3. **Fuzzy-Match** (wenn exakter Treffer fehlt): `Glob("knowledge/**/*<slug>*.md")` mit `-i`, zeige Treffer + bitte User um Auswahl.

4. **Ausgabe:**
   - Dateipfad
   - YAML-Frontmatter (aktualisiert-Datum, Quellen)
   - Vollstaendiger Inhalt
   - Cross-Refs (Siehe-auch-Links) als anklickbare Liste

5. **Wenn kein Treffer:** Schlage vor:
   - Aehnliche verfuegbare Slugs (aus INDEX.md)
   - `/legal-update <slug>` zur Erstellung des fehlenden Artikels

## Output-Limit

Ein `/legal-kb`-Call laedt max. 3 Dateien in den Kontext, um das Kontextfenster zu schonen. Bei mehr Treffern: Liste anzeigen und User nach gezielter Wahl fragen.
