"""Runner of the norm mode (--check-norms): extraction, law checks, BGBl. references, output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

from .bgbl import BgblChecker
from .http_core import FetchFn
from .norm_check import changed_after_verification, check_all
from .norm_client import NormClient
from .norm_extract import scan_kb_norms
from .norm_report import build_summary, json_payload, render_text


def run_norm_mode(args: argparse.Namespace, kb_path: Path, cache_dir: Path | None, cache_warning: str | None,
                  fetch: FetchFn | None, sleep: Callable[[float], None], out, err) -> int:
    extraction = scan_kb_norms(kb_path)
    client = NormClient(fetch=fetch, cache_dir=cache_dir, rate=args.norm_rate, offline=args.offline,
                        cache_ttl_seconds=args.cache_ttl_days * 24 * 3600, sleep=sleep)
    norms, laws = check_all(extraction.norms, client)
    changed = changed_after_verification(extraction.norms, laws)
    checker = BgblChecker(fetch=fetch, max_checks=args.max_bgbl, offline=args.offline, sleep=sleep,
                          progress=lambda message: print(message, file=err, flush=True))
    bgbl, bgbl_info = checker.check_all(extraction.bgbl)
    warnings = ([cache_warning] if cache_warning else []) + client.warnings + extraction.skipped
    summary = build_summary(norms, laws, extraction.eu_counts, bgbl, client.requests_made,
                            checker.requests_made, len(extraction.skipped))
    payload = json_payload(norms, laws, changed, bgbl, bgbl_info, summary, warnings)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else render_text(payload), file=out)
    return 0
