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
from .cache import default_cache_dir, prepare_cache_dir
from .classify import build_results, summarize
from .ecli_writer import atomic_write, plan_ecli_updates
from .extract import scan_kb
from .models import DEFAULT_CACHE_TTL_DAYS
from .report import json_payload, render_ecli, render_report

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
MAX_RATE_PER_SECOND = 10.0


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
                   help="Cache-Verzeichnis (Standard: pro Nutzer, Windows %%LOCALAPPDATA%%\\citation-check\\cache, "
                        "sonst $XDG_CACHE_HOME/citation-check bzw. ~/.cache/citation-check; nie im Repo)")
    p.add_argument("--no-cache", action="store_true", help="keinen Cache lesen oder schreiben")
    p.add_argument("--cache-ttl-days", type=float, default=DEFAULT_CACHE_TTL_DAYS,
                   help="maximales Alter von Cache-Eintraegen in Tagen (Standard 7)")
    p.add_argument("--timeout", type=float, default=15.0, help="Timeout je Anfrage in Sekunden")
    p.add_argument("--strict", action="store_true", help="Exit 1 bei DATE_MISMATCH")
    p.add_argument("--write-ecli", action="store_true",
                   help="ecli: in knowledge/urteile/*.md eintragen (nur eindeutig VERIFIED)")
    p.add_argument("--dry-run", action="store_true", help="mit --write-ecli: nur Vorschau")
    return p


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


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
    requested = Path(args.cache_dir) if args.cache_dir else default_cache_dir()
    if _inside(requested, ROOT):
        print(f"Fehler: --cache-dir darf nicht im Repo liegen ({requested}).", file=err)
        return None, None, False
    cache_dir, warning = prepare_cache_dir(requested)
    if warning:
        print(f"WARNUNG: {warning}", file=err)
    return cache_dir, warning, True


def _write_phase(args: argparse.Namespace, kb_path: Path, client: ApiClient) -> tuple[list[dict], list[dict]]:
    updates, skipped = plan_ecli_updates(kb_path, client, fresh=not args.dry_run)
    if not args.dry_run:
        for update in updates:
            atomic_write(update["path"], update["data"])
    return updates, skipped


def main(argv: list[str] | None = None, fetch: FetchFn | None = None,
         sleep: Callable[[float], None] = time.sleep, stdout=None, stderr=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _validate_args(parser, args)
    out, err = _setup_streams(stdout, stderr)
    cache_dir, cache_warning, ok = _resolve_cache(args, err)
    if not ok:
        return 2
    kb_path = Path(args.path)
    if not kb_path.is_dir():
        print(f"Fehler: KB-Verzeichnis nicht gefunden: {kb_path}", file=err)
        return 2

    client = ApiClient(fetch=fetch, cache_dir=cache_dir, rate=args.rate, timeout=args.timeout,
                       offline=args.offline, sleep=sleep,
                       cache_ttl_seconds=args.cache_ttl_days * 24 * 3600)
    if cache_warning:
        client.warnings.append(cache_warning)
    citations = scan_kb(kb_path)
    if args.only_pending:
        citations = [c for c in citations if c.pending]
    results = build_results(citations, client)
    summary = summarize(results, client, args.offline)

    updates: list[dict] | None = None
    skipped: list[dict] = []
    if args.write_ecli:
        updates, skipped = _write_phase(args, kb_path, client)
        summary["api_requests"] = client.requests_made

    if args.json:
        payload = json_payload(results, summary, client.warnings, updates, skipped, args.dry_run)
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=out)
    else:
        print(render_report(results, summary, client.warnings), file=out)
        if updates is not None:
            print(render_ecli(updates, skipped, args.dry_run), file=out)
    return 1 if args.strict and summary["counts"]["DATE_MISMATCH"] else 0
