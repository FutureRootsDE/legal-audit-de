"""Hardening tests from the second review: runtime bounds, field lengths, years, ports, IDN,
terminal-safe messages, German usage errors and the plugin temp file for profile data."""
from __future__ import annotations

import contextlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report import cli, profile
from client_report.catalog import load_catalog
from client_report.derive import berlin_date, check_date, derive
from client_report.models import ReportInputError, ValidationIssue
from client_report.schema import (
    MAX_OTHER_CHARS,
    MAX_PROSE_CHARS,
    MAX_VERBATIM_CHARS,
    normalize_reference,
    validate_input,
)
from client_report.textcheck import find_forbidden, load_forbidden_phrases, normalize
from client_report_support import make_report_dir, open_result, valid_findings, write_png

CAT = load_catalog()
PHRASES = load_forbidden_phrases()
FAST_REJECT_SECONDS = 2.0
FAST_PROSE_SECONDS = 0.5


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    stdin = mock.Mock()
    stdin.isatty.return_value = False
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), mock.patch.object(sys, "stdin", stdin):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


def elapsed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


class TextcheckRuntime(unittest.TestCase):
    def test_long_whitespace_run_is_linear(self):
        text = "a" + " " * 200_000 + "b"
        self.assertLess(elapsed(lambda: normalize(text)), FAST_PROSE_SECONDS)

    def test_percent_spacing_still_normalised(self):
        self.assertEqual(normalize("100%konform"), normalize("100 % konform"))
        self.assertEqual(normalize("100 \t %   konform"), "100 % konform")

    def test_covered_check_is_not_quadratic(self):
        text = "rechtswidrig " * 20_000
        took = elapsed(lambda: self.assertEqual(find_forbidden(text, PHRASES), ["rechtswidrig"]))
        self.assertLess(took, FAST_REJECT_SECONDS)

    def test_covered_semantics_kept(self):
        self.assertEqual(find_forbidden("rechtswidrig", PHRASES), ["rechtswidrig"])
        self.assertEqual(find_forbidden("rechtswidrig und widrig", PHRASES), ["rechtswidrig", "widrig"])
        self.assertEqual(find_forbidden("widrig", ["widrig", "widrig"]), ["widrig"])
        # equal spans of two spellings cover nothing: both are reported
        self.assertEqual(find_forbidden("Mängel", ["Mangel", "Maengel"]), ["Mangel", "Maengel"])


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.rd = make_report_dir(Path(self._tmp.name))
        self.addCleanup(self._tmp.cleanup)

    def issues(self, findings):
        return validate_input(findings, CAT, self.rd)


class FieldLengths(Base):
    def test_one_megabyte_prose_rejected_fast(self):
        f = valid_findings(CAT)
        f["summary"]["sentences"][0] = "Die Seite lädt Schriften. " * 40_000
        took = elapsed(lambda: setattr(self, "found", self.issues(f)))
        self.assertLess(took, FAST_REJECT_SECONDS)
        self.assertEqual([i.path for i in self.found], ["summary.sentences[0]"])
        self.assertIn(str(MAX_PROSE_CHARS), self.found[0].message)

    def test_one_megabyte_url_and_key_rejected_fast(self):
        f = valid_findings(CAT)
        f["run"]["user_agent"] = "x" * 1_000_000
        f["run"]["tools"] = {"y" * 1_000_000: "1"}
        took = elapsed(lambda: setattr(self, "found", self.issues(f)))
        self.assertLess(took, FAST_REJECT_SECONDS)
        self.assertEqual(sorted(i.path for i in self.found), ["run.tools", "run.user_agent"])
        self.assertTrue(all(len(str(i)) < 200 for i in self.found))

    def test_prose_at_limit_checks_fast(self):
        f = valid_findings(CAT)
        f["summary"]["sentences"][0] = ("Die Seite lädt Schriften. " * 200)[:MAX_PROSE_CHARS]
        took = elapsed(lambda: self.assertEqual(self.issues(f), []))
        self.assertLess(took, FAST_PROSE_SECONDS)

    def test_verbatim_limit_is_higher(self):
        f = valid_findings(CAT)
        r = open_result("CK-03", "notice", "LOW")
        r["evidence"] = [{"kind": "dom", "excerpt": "<div>" * (MAX_PROSE_CHARS // 4)}]
        f["results"] = [r]
        self.assertEqual(self.issues(f), [])
        r["evidence"][0]["excerpt"] = "x" * (MAX_VERBATIM_CHARS + 1)
        self.assertEqual([i.path for i in self.issues(f)], ["results[0].evidence[0].excerpt"])

    def test_other_strings_bounded(self):
        f = valid_findings(CAT)
        f["issuer"]["company"] = "x" * (MAX_OTHER_CHARS + 1)
        self.assertEqual([i.path for i in self.issues(f)], ["issuer.company"])

    def test_messages_german_and_dash_free(self):
        f = valid_findings(CAT)
        f["issuer"]["company"] = "x" * (MAX_OTHER_CHARS + 1)
        message = self.issues(f)[0].message
        self.assertIn("Zeichen", message)
        for bad in ("—", "–", " - "):
            self.assertNotIn(bad, message)


class Years(Base):
    def test_far_future_year_rejected_by_schema(self):
        f = valid_findings(CAT)
        f["run"]["started_utc"] = "9999-12-31T23:30:00Z"
        f["run"]["finished_utc"] = "9999-12-31T23:59:00Z"
        self.assertEqual(sorted(i.path for i in self.issues(f)), ["run.finished_utc", "run.started_utc"])

    def test_check_date_reports_input_error_not_overflow(self):
        for value in ("9999-12-31T23:30:00Z", "1999-12-31T12:00:00Z", "2101-01-01T00:00:00Z"):
            with self.assertRaises(ReportInputError) as ctx:
                check_date({"run": {"started_utc": value}})
            self.assertEqual(ctx.exception.issues[0].path, "run.started_utc")
        self.assertEqual(check_date({"run": {"started_utc": "2100-12-31T22:00:00Z"}}), date(2100, 12, 31))

    def test_derive_never_overflows(self):
        f = valid_findings(CAT)
        f["run"]["started_utc"] = "9999-12-31T23:30:00Z"
        with self.assertRaises(ReportInputError):
            derive(f, CAT)

    def test_berlin_date_public(self):
        self.assertEqual(berlin_date(datetime(2026, 11, 17, 23, 30)), date(2026, 11, 18))
        self.assertEqual(berlin_date(datetime(2026, 6, 18, 21, 59)), date(2026, 6, 18))


class References(Base):
    def refs_issues(self, refs):
        f = valid_findings(CAT)
        f["results"] = [open_result("CK-03", "notice", "LOW") | {"references": refs}]
        return [i.path for i in self.issues(f)]

    def test_port_range(self):
        self.assertEqual(self.refs_issues(["https://a.de:443/", "https://a.de:65535/x"]), [])
        self.assertEqual(self.refs_issues(["https://a.de:0/", "https://a.de:65536/", "https://a.de:99999/"]),
                         ["results[0].references[0]", "results[0].references[1]", "results[0].references[2]"])

    def test_idn_hosts(self):
        self.assertEqual(self.refs_issues(["https://bücher.de/a?b=1#c"]), [])
        self.assertEqual(self.refs_issues(["https://" + "a" * 70 + ".de/", "https://[::1]/"]),
                         ["results[0].references[0]", "results[0].references[1]"])

    def test_normalize_reference(self):
        self.assertEqual(normalize_reference("https://Bücher.de:8443/pfad?q=1#f"),
                         "https://xn--bcher-kva.de:8443/pfad?q=1#f")
        self.assertEqual(normalize_reference("https://example.de/x"), "https://example.de/x")
        self.assertIsNone(normalize_reference("https://a.de:0/"))
        self.assertIsNone(normalize_reference("http://a.de/"))

    def test_report_data_uses_punycode(self):
        f = valid_findings(CAT)
        f["results"] = [open_result("CK-03", "notice", "LOW") | {"references": ["https://bücher.de/"]}]
        model, _ = derive(f, CAT)
        row = next(r for r in model.results if r.entry.id == "CK-03")
        self.assertEqual(list(row.data["references"]), ["https://xn--bcher-kva.de/"])
        self.assertEqual(f["results"][0]["references"], ["https://bücher.de/"])  # input not mutated


class CliMessages(unittest.TestCase):
    def test_control_characters_escaped_in_issue_output(self):
        err = io.StringIO()
        exc = ReportInputError([ValidationIssue("run.domain", "a\x1b[31mb‮c\x07")])
        with contextlib.redirect_stderr(err):
            cli._report_issues(exc)
        text = err.getvalue()
        self.assertNotIn("\x1b", text)
        self.assertNotIn("‮", text)
        self.assertIn("\\x1b", text)
        self.assertIn("\\u202e", text)
        self.assertIn("\\x07", text)

    def test_usage_errors_fully_german(self):
        cases = (
            (["gibtsnicht"], "Unbekannter Befehl", ("invalid choice", "choose from")),
            (["profile", "save", "--data"], "fehlt ein Wert", ("expected one argument",)),
            (["profile", "save"], "Pflichtangabe fehlt", ("required",)),
            (["check", "--xyz"], "Unbekannte Angabe", ("unrecognized",)),
        )
        for argv, german, english in cases:
            code, _, err = run_cli_safe(argv)
            self.assertEqual(code, 1, argv)
            self.assertIn(german, err, argv)
            for word in english:
                self.assertNotIn(word, err, argv)

    def test_usage_error_escapes_control_characters(self):
        _, _, err = run_cli_safe(["bad\x1b[2Jname"])
        self.assertNotIn("\x1b", err)
        self.assertIn("\\x1b", err)


def run_cli_safe(argv):
    """Parser errors call sys.exit; return (code, out, err) instead of raising."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = cli.main(argv)
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


class InitBerlinDay(unittest.TestCase):
    def test_init_without_date_uses_berlin_day(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp).resolve()
            home, work = tmp_path / "home", tmp_path / "work"
            work.mkdir()
            logo = tmp_path / "logo.png"
            write_png(logo, (31, 78, 121))
            data = tmp_path / "p.json"
            data.write_text(json.dumps({"company": "Muster GmbH", "contact": "E. Muster",
                                        "address": ["Hauptstraße 1"], "email": "a@b.de"}), encoding="utf-8")
            cwd = os.getcwd()
            os.chdir(work)
            try:
                with mock.patch.dict(os.environ, {"LEGAL_AUDIT_CLIENT_TEST_HOME": str(home)}):
                    self.assertEqual(run_cli(["profile", "save", "--data", str(data), "--logo", str(logo),
                                              "--accent", "default"])[0], 0)
                    late = datetime(2026, 11, 17, 23, 30)
                    with mock.patch.object(cli, "_utc_now", return_value=late):
                        code, out, err = run_cli(["init", "https://example.de/"])
            finally:
                os.chdir(cwd)
            self.assertEqual(code, 0, err)
            folder = Path(out.strip().splitlines()[-1])
            self.assertTrue(folder.name.startswith("2026-11-18"), folder.name)
            findings = json.loads((folder / "findings.json").read_text(encoding="utf-8"))
            self.assertEqual(findings["run"]["started_utc"], "2026-11-17T23:30:00Z")


class TempDataFile(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)
        patcher = mock.patch.object(tempfile, "tempdir", str(self.root))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_tempfile_prints_fresh_path_in_plugin_folder(self):
        code, out, _ = run_cli(["tempfile"])
        self.assertEqual(code, 0)
        path = Path(out.strip())
        self.assertEqual(path.parent, self.root / profile.TEMP_DIRNAME)
        self.assertTrue(path.parent.is_dir())
        self.assertFalse(path.exists())
        self.assertTrue(path.name.startswith("profile-") and path.suffix == ".json")
        self.assertNotEqual(path, Path(run_cli(["tempfile"])[1].strip()))

    def _save(self, data_path, extra=()):
        logo = self.root / "logo.png"
        write_png(logo, (31, 78, 121))
        home = self.root / "home"
        with mock.patch.dict(os.environ, {"LEGAL_AUDIT_CLIENT_TEST_HOME": str(home)}):
            return run_cli(["profile", "save", "--data", str(data_path), "--logo", str(logo),
                            "--accent", "default", *extra])

    def test_consume_deletes_temp_file_on_success_and_error(self):
        good = {"company": "Muster GmbH", "contact": "E. Muster", "address": ["Hauptstraße 1"], "email": "a@b.de"}
        for payload, expected in ((good, 0), ({"company": "x"}, 1), ("kein json", 1)):
            path = Path(run_cli(["tempfile"])[1].strip())
            path.write_text(payload if isinstance(payload, str) else json.dumps(payload), encoding="utf-8")
            code, _, _ = self._save(path, ["--consume"])
            self.assertEqual(code, expected)
            self.assertFalse(path.exists(), payload)

    def test_consume_keeps_files_outside_plugin_folder(self):
        outside = self.root / "eigene.json"
        outside.write_text("{}", encoding="utf-8")
        code, _, err = self._save(outside, ["--consume"])
        self.assertEqual(code, 1)
        self.assertTrue(outside.exists())
        self.assertIn("nicht gelöscht", err)

    def test_without_consume_file_stays(self):
        path = Path(run_cli(["tempfile"])[1].strip())
        path.write_text("{}", encoding="utf-8")
        self._save(path)
        self.assertTrue(path.exists())

    def test_consume_rejects_traversal_out_of_folder(self):
        folder = self.root / profile.TEMP_DIRNAME
        folder.mkdir()
        victim = self.root / "victim.json"
        victim.write_text("{}", encoding="utf-8")
        self._save(folder / ".." / "victim.json", ["--consume"])
        self.assertTrue(victim.exists())

    # -- redirected plugin temp folder (symlink, Windows junction)

    def _redirect_folder(self, kind: str) -> Path:
        """Replace the plugin temp folder by a link to a foreign folder; returns that target."""
        target = self.root / "fremd"
        target.mkdir()
        link = self.root / profile.TEMP_DIRNAME
        if kind == "junction":
            if os.name != "nt":
                self.skipTest("Junctions gibt es nur unter Windows")
            done = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                                  capture_output=True, timeout=30)
            if done.returncode != 0:
                self.skipTest("mklink /J nicht verfügbar")
            self.assertFalse(link.is_symlink())   # the gap this guards: junctions are no symlinks
        else:
            try:
                os.symlink(target, link, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks hier nicht erlaubt")
        self.addCleanup(lambda: os.path.lexists(link) and (os.rmdir(link) if os.name == "nt" else os.unlink(link)))
        return target

    def _assert_redirect_refused(self, target: Path):
        code, out, err = run_cli(["tempfile"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Temp-Ordner nicht nutzbar", err)
        self.assertIn("Verknüpfung", err)
        foreign = target / f"profile-{'a' * 32}.json"
        foreign.write_text(json.dumps({"company": "Muster GmbH", "contact": "E. Muster",
                                       "address": ["Hauptstraße 1"], "email": "a@b.de"}), encoding="utf-8")
        via_link = self.root / profile.TEMP_DIRNAME / foreign.name
        code, _, err = self._save(via_link, ["--consume"])
        self.assertEqual(code, 1)
        self.assertIn("nicht gelöscht", err)
        self.assertTrue(foreign.exists())
        self.assertFalse((self.root / "home" / profile.PROFILE_FILENAME).exists())
        self.assertEqual(sorted(p.name for p in target.iterdir()), [foreign.name])

    def test_junction_as_temp_folder_is_refused(self):
        self._assert_redirect_refused(self._redirect_folder("junction"))

    def test_symlink_as_temp_folder_is_refused(self):
        self._assert_redirect_refused(self._redirect_folder("symlink"))

    def test_reparse_point_attribute_counts_as_redirect(self):
        folder = self.root / profile.TEMP_DIRNAME
        folder.mkdir()
        real_lstat = os.lstat

        def fake_lstat(path, *args, **kwargs):
            st = real_lstat(path, *args, **kwargs)
            if Path(path) == folder:
                return mock.Mock(st_mode=st.st_mode, st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
            return st

        with mock.patch.object(profile.os, "lstat", side_effect=fake_lstat):
            code, _, err = run_cli(["tempfile"])
        self.assertEqual(code, 1)
        self.assertIn("Verknüpfung", err)

    # -- --consume deletes exactly the checked file

    def test_consume_unlink_failure_is_only_a_warning(self):
        path = Path(run_cli(["tempfile"])[1].strip())
        path.write_text(json.dumps({"company": "Muster GmbH", "contact": "E. Muster",
                                    "address": ["Hauptstraße 1"], "email": "a@b.de"}), encoding="utf-8")
        real_unlink = Path.unlink
        calls = []

        def locked(self_path, *args, **kwargs):
            if self_path.name == path.name:
                calls.append(self_path)
                raise PermissionError(13, "Datei ist gesperrt")
            return real_unlink(self_path, *args, **kwargs)

        with mock.patch.object(Path, "unlink", autospec=True, side_effect=locked):
            code, out, err = self._save(path, ["--consume"])
        self.assertEqual(code, 0, err)
        self.assertIn("Profil gespeichert", out)
        self.assertIn("Warnung", err)
        self.assertIn("nicht gelöscht", err)
        self.assertTrue((self.root / "home" / profile.PROFILE_FILENAME).is_file())
        self.assertEqual(calls, [path])   # the checked path itself, unresolved, exactly once

    def test_consume_unlink_failure_keeps_error_exit_code(self):
        path = Path(run_cli(["tempfile"])[1].strip())
        path.write_text("kein json", encoding="utf-8")
        with mock.patch.object(Path, "unlink", autospec=True, side_effect=PermissionError(13, "gesperrt")):
            code, _, err = self._save(path, ["--consume"])
        self.assertEqual(code, 1)
        self.assertIn("Warnung", err)

    def test_consume_symlinked_data_file_is_refused(self):
        folder = self.root / profile.TEMP_DIRNAME
        folder.mkdir()
        victim = self.root / "victim.json"
        victim.write_text("{}", encoding="utf-8")
        link = folder / f"profile-{'b' * 32}.json"
        try:
            os.symlink(victim, link)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks hier nicht erlaubt")
        code, _, err = self._save(link, ["--consume"])
        self.assertEqual(code, 1)
        self.assertIn("nicht gelöscht", err)
        self.assertTrue(victim.exists())
        self.assertTrue(os.path.lexists(link))


if __name__ == "__main__":
    unittest.main()
