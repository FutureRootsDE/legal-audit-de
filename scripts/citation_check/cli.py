"""Command line interface of the citation check."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Callable

from .api import ApiClient, FetchFn
from .cache import default_cache_dir_vetted, prepare_cache_dir
from .classify import LookupMap, build_results, summarize
from .ecli_writer import EcliOutcome, apply_updates, plan_ecli_updates
from .extract import scan_kb
from .fsutil import is_under
from .models import DEFAULT_CACHE_TTL_DAYS
from .report import json_payload, render_ecli, render_report

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
MAX_RATE_PER_SECOND = 10.0
EXIT_USAGE = 2
EXIT_WRITE_FAILED = 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Bundesgerichts-Aktenzeichen in knowledge/ gegen die "
                                            "Rechtsinformations-API des Bundes pruefen (optional).")
    p.add_argument("--path", default=str(ROOT / "knowledge"), help="KB-Verzeichnis (Standard: knowledge/)")
    p.add_argument("--json", action="store_true", help="JSON statt lesbarem Bericht")
    p.add_argument("--offline", action="store_true", help="nur Extraktion und Cache, keine Anfragen")
    p.add_argument("--only-pending", action="store_true",
                   help="nur Zitate mit <<VERIFIKATION AUSSTEHEND>> in derselben Zeile")
    p.add_argument("--rate", type=float, default=2.0, help="max. Anfragen pro Sekunde (Standard 2)")
    p.add_argument("--cache-dir", default=None,
                   help="Cache-Verzeichnis (Standard: pro Nutzer, Windows %%LOCALAPPDATA%%\\citation-check\\cache "
                        "(nur unterhalb des Nutzerprofils), sonst $XDG_CACHE_HOME/citation-check bzw. "
                        "~/.cache/citation-check; nie im Repo). Cache-Treffer sind gekennzeichnet "
                        "(source: cache im JSON, Quelle: Cache im Bericht): lokale Cache-Dateien sind nicht "
                        "authentisch pruefbar, Vorschlaege aus dem Cache gelten als UNGEPRUEFT")
    p.add_argument("--no-cache", action="store_true", help="keinen Cache lesen oder schreiben")
    p.add_argument("--cache-ttl-days", type=float, default=DEFAULT_CACHE_TTL_DAYS,
                   help="maximales Alter von Cache-Eintraegen in Tagen (Standard 7)")
    p.add_argument("--timeout", type=float, default=15.0,
                   help="Gesamtzeit je Anfrage in Sekunden (inkl. Lesen der Antwort)")
    p.add_argument("--strict", action="store_true", help="Exit 1 bei DATE_MISMATCH")
    p.add_argument("--write-ecli", action="store_true",
                   help="ecli: in knowledge/urteile/*.md eintragen (nur eindeutig VERIFIED, frisch abgefragt; "
                        "Exit 3 bei Schreibfehlern)")
    p.add_argument("--dry-run", action="store_true", help="mit --write-ecli: nur Vorschau")
    return p


def _validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.dry_run and not args.write_ecli:
        parser.error("--dry-run ist nur zusammen mit --write-ecli sinnvoll")
    if not 0 < args.rate <= MAX_RATE_PER_SECOND:
        parser.error(f"--rate muss > 0 und <= {MAX_RATE_PER_SECOND:g} sein")
    if args.timeout <= 0:
        parser.error("--timeout muss > 0 sein")
    if args.cache_ttl_days <= 0:
        parser.error("--cache-ttl-days muss > 0 sein")
    if args.write_ecli and not args.dry_run and args.offline:
        parser.error("--write-ecli ohne --dry-run braucht frische API-Abfragen und ist mit --offline unvereinbar")


def _setup_streams(stdout, stderr):
    if stdout is None and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if stderr is None and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    return stdout or sys.stdout, stderr or sys.stderr


def _resolve_cache(args: argparse.Namespace, err) -> tuple[Path | None, str | None, bool]:
    """Return (cache dir, warning, ok). ok is False for a fatal usage error."""
    if args.no_cache:
        return None, None, True
    if args.cache_dir:
        requested, warning = Path(args.cache_dir), None
    else:
        requested, warning = default_cache_dir_vetted()
    if requested is not None and is_under(requested, ROOT):
        print(f"Fehler: --cache-dir darf nicht im Repo liegen ({requested}).", file=err)
        return None, None, False
    if requested is not None:
        requested, warning = prepare_cache_dir(requested)
    if warning:
        print(f"WARNUNG: {warning}", file=err)
    return requested, warning, True


def _write_phase(args: argparse.Namespace, kb_path: Path, client: ApiClient, known: LookupMap) -> EcliOutcome:
    updates, skipped = plan_ecli_updates(kb_path, client, fresh=not args.dry_run, known=known)
    outcome = EcliOutcome(updates=updates, skipped=skipped, dry_run=args.dry_run)
    if not args.dry_run:
        applied = apply_updates(updates, kb_path)
        outcome.written, outcome.failed = applied.written, applied.failed
        outcome.skipped = skipped + applied.skipped
    return outcome


def _emit(args: argparse.Namespace, out, results, summary, warnings, ecli: EcliOutcome | None) -> None:
    if args.json:
        print(json.dumps(json_payload(results, summary, warnings, ecli), ensure_ascii=False, indent=2), file=out)
        return
    print(render_report(results, summary, warnings), file=out)
    if ecli is not None:
        print(render_ecli(ecli), file=out)


def _exit_code(args: argparse.Namespace, summary: dict, ecli: EcliOutcome | None) -> int:
    if ecli is not None and ecli.failed:
        return EXIT_WRITE_FAILED
    return 1 if args.strict and summary["counts"]["DATE_MISMATCH"] else 0


def main(argv: list[str] | None = None, fetch: FetchFn | None = None,
         sleep: Callable[[float], None] = time.sleep, stdout=None, stderr=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _validate_args(parser, args)
    out, err = _setup_streams(stdout, stderr)
    cache_dir, cache_warning, ok = _resolve_cache(args, err)
    kb_path = Path(args.path)
    if not ok:
        return EXIT_USAGE
    if not kb_path.is_dir():
        print(f"Fehler: KB-Verzeichnis nicht gefunden: {kb_path}", file=err)
        return EXIT_USAGE

    client = ApiClient(fetch=fetch, cache_dir=cache_dir, rate=args.rate, timeout=args.timeout,
                       offline=args.offline, sleep=sleep,
                       cache_ttl_seconds=args.cache_ttl_days * 24 * 3600)
    client.warnings.extend([cache_warning] if cache_warning else [])
    citations = scan_kb(kb_path, client.warnings)
    if args.only_pending:
        citations = [c for c in citations if c.pending]
    known: LookupMap = {}
    results = build_results(citations, client, fresh=args.write_ecli and not args.dry_run, lookups=known)
    ecli = _write_phase(args, kb_path, client, known) if args.write_ecli else None
    summary = summarize(results, client, args.offline)
    _emit(args, out, results, summary, client.warnings, ecli)
    return _exit_code(args, summary, ecli)
