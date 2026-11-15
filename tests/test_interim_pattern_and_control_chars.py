"""Interim-order title pattern (word boundary after the R suffix) and a control-character guard for scripts/."""
from __future__ import annotations

import unittest

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import eu_sparql

ALLOWED_CONTROL = {0x09, 0x0A, 0x0D}


class InterimTitleSuffixTest(unittest.TestCase):
    def test_file_number_with_r_suffix_is_interim(self):
        for title in ("Rechtssache C-204/21 R", "Rechtssache T-1/20 R", "C-204/21 R",
                      "Kommission gegen Polen. Rechtssache C-204/21 R.", "Rechtssache C-204/21 P R"):
            with self.subTest(title=title):
                self.assertTrue(eu_sparql.is_interim_title(title))

    def test_other_suffixes_and_plain_numbers_are_not_interim(self):
        for title in ("Rechtssache C-204/21 RENV", "Rechtssache C-204/21 REC", "Rechtssache C-204/21 rev",
                      "Rechtssache C-204/21 P", "Rechtssache C-204/21", "C-204/21 Rn. 5", "XC-204/21 R"):
            with self.subTest(title=title):
                self.assertFalse(eu_sparql.is_interim_title(title))

    def test_pattern_contains_no_control_characters(self):
        self.assertFalse([c for c in eu_sparql.INTERIM_TITLE.pattern if ord(c) < 0x20])


class ScriptsControlCharacterTest(unittest.TestCase):
    def test_no_control_characters_in_script_sources(self):
        offenders = []
        for path in sorted(support.SCRIPTS.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            data = path.read_bytes()
            for offset, byte in enumerate(data):
                if byte < 0x20 and byte not in ALLOWED_CONTROL:
                    line = data.count(b"\n", 0, offset) + 1
                    offenders.append(f"{path.relative_to(support.SCRIPTS)}:{line}: 0x{byte:02x}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
