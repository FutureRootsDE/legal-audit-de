"""Offline tests for scripts/legal-status.py with a temporary mini knowledge base."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)

SCRIPT = support.SCRIPTS / "legal-status.py"
TODAY = date(2026, 11, 14)


def load_module():
    spec = importlib.util.spec_from_file_location("legal_status_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STATUS = load_module()


def doc(front: str, body: str = "Text\n") -> str:
    return f"---\n{front}\n---\n\n{body}"


class MiniKb(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "knowledge" / "themen").mkdir(parents=True)

    def write(self, name: str, text: str, sub: str = "themen") -> None:
        folder = self.root / "knowledge" / sub
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text(text, encoding="utf-8")

    def report(self, verbose: bool = True) -> dict:
        return STATUS.build_report(verbose=verbose, today=TODAY, root=self.root)

    def state_of(self, name: str) -> str:
        files = STATUS.kb_categories(self.root / "knowledge")["themen"]
        path = next(p for p in files if p.name == name)
        return STATUS.scan_file(path, TODAY, self.root)["state"]


class FreshnessCriterion(MiniKb):
    def test_verification_date_decides_not_the_edit_date(self):
        self.write("a.md", doc("aktualisiert: 2026-11-10\nverifiziert-am: 2026-05-08"))
        self.assertEqual(self.state_of("a.md"), "very_stale")
        self.write("b.md", doc("aktualisiert: 2026-01-01\nverifiziert-am: 2026-11-01"))
        self.assertEqual(self.state_of("b.md"), "fresh")

    def test_buckets_at_the_boundaries(self):
        cases = {"2026-08-17": "fresh", "2026-08-16": "stale", "2026-05-19": "stale", "2026-05-18": "very_stale"}
        for verified, expected in cases.items():
            with self.subTest(verified=verified):
                self.write("c.md", doc(f"aktualisiert: {verified}\nverifiziert-am: {verified}"))
                self.assertEqual(self.state_of("c.md"), expected)

    def test_without_verification_date_aktualisiert_counts(self):
        self.write("d.md", doc("aktualisiert: 2026-11-01"))
        self.assertEqual(self.state_of("d.md"), "fresh")
        self.write("e.md", doc("aktualisiert: 2026-01-01"))
        self.assertEqual(self.state_of("e.md"), "very_stale")

    def test_teilverifiziert_is_its_own_state_and_never_fresh(self):
        self.write("tool-katalog.md", doc("aktualisiert: 2026-11-14\nverifiziert-am: 2026-05-08\n"
                                           "teilverifiziert-am: 2026-11-14"))
        self.write("recent.md", doc("aktualisiert: 2026-11-14\nverifiziert-am: 2026-11-14\n"
                                    "teilverifiziert-am: 2026-11-14"))
        self.assertEqual(self.state_of("tool-katalog.md"), "teilverifiziert")
        self.assertEqual(self.state_of("recent.md"), "teilverifiziert")
        aktualitaet = self.report()["kb"]["aktualitaet"]
        self.assertEqual((aktualitaet["fresh_under_90d"], aktualitaet["teilverifiziert"]), (0, 2))

    def test_files_without_usable_frontmatter(self):
        self.write("f.md", "# Ohne Frontmatter\n")
        self.write("h.md", "# Titel\n\nverifiziert-am: 2026-11-14\n")  # field in the body does not count
        self.write("i.md", doc("titel: nur ein Titel"))  # frontmatter without any date field
        for name in ("f.md", "h.md", "i.md"):
            self.assertEqual(self.state_of(name), "no_frontmatter", name)

    def test_unusable_date_in_a_frontmatter_is_its_own_state(self):
        self.write("g.md", doc("aktualisiert: kein-datum"))
        self.write("j.md", doc("aktualisiert: 2026-11-10\nverifiziert-am:"))  # empty value: falls back
        self.write("k.md", doc("aktualisiert: 2027-01-01"))  # future date
        self.write("l.md", doc("aktualisiert: 2026-13-45\nverifiziert-am: gestern"))
        self.assertEqual(self.state_of("g.md"), "invalid_date")
        self.assertEqual(self.state_of("j.md"), "fresh")
        self.assertEqual(self.state_of("k.md"), "invalid_date")
        self.assertEqual(self.state_of("l.md"), "invalid_date")

    def test_quotes_around_the_date_are_tolerated(self):
        self.write("q.md", doc('aktualisiert: "2026-01-01"\nverifiziert-am: \'2026-11-01\''))
        self.assertEqual(self.state_of("q.md"), "fresh")
        self.write("r.md", doc('aktualisiert: "2026-11-01"\nverifiziert-am: "2026-01-01"'))
        self.assertEqual(self.state_of("r.md"), "very_stale")

    def test_invalid_verification_date_falls_back_to_aktualisiert(self):
        self.write("m.md", doc("aktualisiert: 2026-11-01\nverifiziert-am: irgendwann"))
        self.assertEqual(self.state_of("m.md"), "fresh")
        self.write("n.md", doc("aktualisiert: 2026-11-01\nverifiziert-am: 2027-05-05"))  # future
        self.assertEqual(self.state_of("n.md"), "fresh")

    def test_partly_verified_with_a_broken_date_stays_partly_verified(self):
        self.write("o.md", doc("aktualisiert: kaputt\nteilverifiziert-am: 2026-11-14"))
        self.assertEqual(self.state_of("o.md"), "teilverifiziert")

    def test_report_counts_and_lists_the_new_state_additively(self):
        self.write("g.md", doc("aktualisiert: kein-datum"))
        self.write("a.md", doc("aktualisiert: 2026-11-10\nverifiziert-am: 2026-11-10"))
        report = self.report()
        self.assertEqual(report["kb"]["aktualitaet"]["invalid_date"], 1)
        self.assertEqual(report["kb"]["aktualitaet"]["no_frontmatter"], 0)
        self.assertEqual(report["kb"]["aktualitaet"]["fresh_under_90d"], 1)
        self.assertEqual(report["kb"]["invalid_date_files"][0]["path"], "knowledge/themen/g.md")
        self.assertIn("Ungueltiges Datum:      1", STATUS.render_text(report))


class JsonCompatibility(MiniKb):
    def test_existing_keys_stay_and_new_keys_are_added(self):
        self.write("a.md", doc("aktualisiert: 2026-11-01\nverifiziert-am: 2026-11-01", "<<VERIFIKATION AUSSTEHEND>>\n"))
        report = self.report()
        self.assertTrue({"fresh_under_90d", "stale_90_to_180d", "very_stale_over_180d",
                         "no_frontmatter"} <= set(report["kb"]["aktualitaet"]))
        self.assertIn("teilverifiziert", report["kb"]["aktualitaet"])
        for key in ("total", "affected_files", "by_type"):
            self.assertIn(key, report["placeholders"])
        self.assertEqual(report["placeholders"]["total"], 1)
        json.dumps(report)  # serialisable

    def test_verbose_lists_stale_and_partly_verified_files(self):
        self.write("old.md", doc("aktualisiert: 2026-11-01\nverifiziert-am: 2026-01-01"))
        self.write("teil.md", doc("aktualisiert: 2026-11-01\nteilverifiziert-am: 2026-11-01"))
        kb = self.report()["kb"]
        self.assertEqual([f["path"] for f in kb["stale_files"]], ["knowledge/themen/old.md"])
        self.assertEqual([f["path"] for f in kb["teilverifiziert_files"]], ["knowledge/themen/teil.md"])

    def test_deviant_placeholders_are_counted_as_a_warning(self):
        self.write("a.md", doc("aktualisiert: 2026-11-01", "<<VERIFIKATION AUSSTEHEND: Quelle>>\n"))
        deviant = self.report()["placeholders"]["deviant"]
        self.assertEqual(deviant, {"total": 1, "affected_files": 1})
        self.assertIn("WARNUNG", STATUS.render_text(self.report()))

    def test_cli_runs_against_the_real_kb(self):
        done = subprocess.run([sys.executable, str(SCRIPT), "--json"], capture_output=True, text=True,
                              encoding="utf-8", check=True)
        self.assertIn("teilverifiziert", json.loads(done.stdout)["kb"]["aktualitaet"])


GOLDEN_DOCS = {
    "themen/a.md": "---\naktualisiert: 2026-11-10\nverifiziert-am: 2026-11-01\n---\n\n<<VERIFIKATION AUSSTEHEND>>\nText\n",
    "themen/b.md": "---\naktualisiert: 2026-11-10\nverifiziert-am: 2026-05-08\n---\n\n<<VERIFIKATION AUSSTEHEND: Quelle>>\n",
    "themen/c.md": "---\naktualisiert: 2026-01-01\nverifiziert-am: 2026-08-01\n---\n\nText\n",
    "themen/d.md": "---\naktualisiert: 2026-11-14\nverifiziert-am: 2026-05-08\nteilverifiziert-am: 2026-11-14\n---\n\n<<UNVERIFIZIERT>>\n",
    "themen/e.md": "# Ohne Frontmatter\n",
    "gesetze/f.md": "---\naktualisiert: 2026-06-20\n---\n\nText\n",
}


class StructuralRefactorKeepsOutput(MiniKb):
    """Golden files were produced by the code before build_report and render_text were split into helpers."""

    def test_render_text_output_is_unchanged(self):
        report = json.loads((support.FIXTURES / "legal_status_report.json").read_text(encoding="utf-8"))
        golden = (support.FIXTURES / "legal_status_render.txt").read_text(encoding="utf-8")
        self.assertEqual(STATUS.render_text(report), golden)

    def test_build_report_sections_are_unchanged(self):
        for rel, text in GOLDEN_DOCS.items():
            self.write(Path(rel).name, text, Path(rel).parent.name)
        golden = json.loads((support.FIXTURES / "legal_status_report.json").read_text(encoding="utf-8"))
        report = self.report(verbose=True)
        report["kb"]["aktualitaet"].pop("invalid_date")  # added later (additive key), the golden predates it
        report["kb"].pop("invalid_date_files")
        self.assertEqual(report["kb"], golden["kb"])
        self.assertEqual(report["placeholders"], golden["placeholders"])
        self.assertEqual(set(report), set(golden))


if __name__ == "__main__":
    unittest.main()
