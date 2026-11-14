"""Offline tests: exact placeholders stay clean, deviating variants produce warnings, quoted markers are ignored."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from placeholder_check import find_deviant

SCRIPT = support.SCRIPTS / "find-placeholders.py"


def reasons(text: str) -> list[str]:
    return [d.reason for d in find_deviant(text)]


class DeviantDetection(unittest.TestCase):
    def test_exact_forms_are_clean(self):
        for text in ("BGH I ZR 1/20 <<VERIFIKATION AUSSTEHEND>>", "x <<UNVERIFIZIERT>> y",
                     "<<  VERIFIKATION   AUSSTEHEND  >>", "<<verifikation ausstehend>>"):
            self.assertEqual(find_deviant(text), [], text)

    def test_extra_text_inside_the_marker(self):
        self.assertEqual(reasons("<<VERIFIKATION AUSSTEHEND: Aktenzeichen>>"),
                         ["Zusatztext oder abweichende Schreibweise"])
        self.assertEqual(reasons("<<TEILWEISE VERIFIKATION AUSSTEHEND>>"),
                         ["Zusatztext oder abweichende Schreibweise"])
        self.assertEqual(reasons("<<VERIFIKATION  NOCH AUSSTEHEND>>"),
                         ["Zusatztext oder abweichende Schreibweise"])

    def test_single_closing_or_opening_bracket(self):
        self.assertEqual(reasons("Text <<VERIFIKATION AUSSTEHEND> weiter"), ["einfaches schliessendes >"])
        self.assertEqual(reasons("Text <VERIFIKATION AUSSTEHEND>> weiter"), ["einfaches oeffnendes <"])

    def test_marker_split_over_two_lines(self):
        found = find_deviant("Erste Zeile <<VERIFIKATION\nAUSSTEHEND>> Rest")
        self.assertEqual([(d.line, d.reason) for d in found], [(1, "ueber mehrere Zeilen")])
        found = find_deviant("a\nb <<VERIFIKATION AUSSTEHEND: Quelle\nunklar>>")
        self.assertEqual([d.line for d in found], [2])

    def test_unclosed_marker(self):
        self.assertEqual(reasons("Text <<VERIFIKATION AUSSTEHEND und dann nichts mehr\nnaechste Zeile"),
                         ["nicht geschlossen"])

    def test_markers_in_backticks_are_ignored(self):
        notes = ("- **2026-11-14 (Nachzug)**: Marker `<<VERIFIKATION AUSSTEHEND>>` entfernt, "
                 "`<<VERIFIKATION AUSSTEHEND: x>>` und `<<VERIFIKATION AUSSTEHEND>` stehen nur im Vermerk")
        self.assertEqual(find_deviant(notes), [])

    def test_unrelated_angle_brackets_are_not_flagged(self):
        for text in ("a < b und c > d", "<br>VERIFIKATION", "Pfeil -> VERIFIKATION", "<<Zitat>> ohne Marker"):
            self.assertEqual(find_deviant(text), [], text)

    def test_line_numbers(self):
        self.assertEqual([d.line for d in find_deviant("a\nb\n<<VERIFIKATION AUSSTEHEND>\n")], [3])


class FindPlaceholdersScript(unittest.TestCase):
    def run_script(self, text: str, *args: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            kb = Path(tmp) / "knowledge" / "themen"
            kb.mkdir(parents=True)
            (kb / "t.md").write_text(text, encoding="utf-8")
            env = {**os.environ, "CLAUDE_PROJECT_DIR": tmp}
            return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
                                  encoding="utf-8", env=env)

    def test_warning_on_stderr_exit_zero_and_exact_marker_still_listed(self):
        done = self.run_script("A <<VERIFIKATION AUSSTEHEND>>\nB <<VERIFIKATION AUSSTEHEND: x>>\n")
        self.assertEqual(done.returncode, 0)
        self.assertIn("1 Platzhalter gesamt", done.stdout)
        self.assertIn("WARNUNG", done.stderr)
        self.assertIn("t.md:2", done.stderr)

    def test_json_output_stays_a_plain_list(self):
        done = self.run_script("A <<VERIFIKATION AUSSTEHEND>\n", "--json")
        self.assertEqual(done.stdout.strip(), "[]")
        self.assertIn("einfaches schliessendes >", done.stderr)

    def test_no_warning_for_clean_or_quoted_markers(self):
        done = self.run_script("A <<VERIFIKATION AUSSTEHEND>>\nVermerk: `<<VERIFIKATION AUSSTEHEND>` entfernt\n")
        self.assertEqual(done.stderr, "")


if __name__ == "__main__":
    unittest.main()
