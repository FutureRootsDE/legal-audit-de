"""Planning and writing of the optional `ecli:` frontmatter line in knowledge/urteile/*.md."""
from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

from .api import ApiClient
from .classify import classify
from .extract import _rel, extract_citations, find_dates
from .models import Citation

ECLI_WRITE_RE = re.compile(r"ECLI:DE:[A-Z]+:\d{4}:[A-Z0-9.]+")  # strict: only this is ever written to the KB


def _split_lines(text: str) -> list[str]:
    return [p for p in re.split(r"(?<=\n)", text) if p]


def _frontmatter_bounds(lines: list[str]) -> tuple[int, int] | None:
    if not lines or lines[0].strip("﻿\r\n ") != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip("\r\n ") == "---":
            return 0, idx
    return None


def _main_reference(lines: list[str], body_start: int) -> tuple[Citation | None, str | None]:
    """Main Aktenzeichen (and date) of a judgment file: Eckdaten row, else H1."""
    az_line = next((ln for ln in lines[body_start:] if "**Aktenzeichen" in ln), None)
    if az_line is None:
        az_line = next((ln for ln in lines[body_start:] if ln.startswith("# ")), None)
    if az_line is None:
        return None, None
    found = extract_citations(az_line, "")
    date_line = next((ln for ln in lines[body_start:]
                      if re.search(r"\*\*(?:Datum|Entscheidungstermin|Entscheidungsdatum)", ln)), None)
    dates = find_dates(date_line) if date_line else []
    return (found[0] if found else None), (dates[0][2] if dates else None)


def _unique_ecli(hits: list[dict], date: str | None) -> tuple[str | None, str]:
    candidates = [h for h in hits if date is None or h.get("date") == date]
    eclis = {h["ecli"] for h in candidates
             if isinstance(h.get("ecli"), str) and ECLI_WRITE_RE.fullmatch(h["ecli"])}
    if len(eclis) == 1:
        return eclis.pop(), ""
    if not eclis:
        return None, "kein ECLI im Treffer oder ECLI entspricht nicht dem strengen Muster"
    return None, "mehrere Treffer, ohne eindeutiges Datum nicht entscheidbar"


def atomic_write(path: Path, data: bytes) -> None:
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=".tmp-ecli-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.chmod(tmp_name, path.stat().st_mode & 0o777)
        except OSError:
            pass
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def plan_ecli_updates(kb_path: Path, client: ApiClient, fresh: bool = False) -> tuple[list[dict], list[dict]]:
    """Return (updates, skipped). Updates carry the new file bytes, never written here."""
    updates: list[dict] = []
    skipped: list[dict] = []
    folder = kb_path / "urteile"
    for md in sorted(folder.glob("*.md")) if folder.is_dir() else []:
        rel = _rel(md, kb_path)

        def skip(reason: str) -> None:
            skipped.append({"file": rel, "reason": reason})

        try:
            text = md.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            skip(f"nicht lesbar: {exc}")
            continue
        lines = _split_lines(text)
        bounds = _frontmatter_bounds(lines)
        if bounds is None:
            skip("kein Frontmatter")
            continue
        if any(re.match(r"ecli\s*:", ln) for ln in lines[1:bounds[1]]):
            skip("ecli bereits vorhanden")
            continue
        citation, date = _main_reference(lines, bounds[1] + 1)
        if citation is None:
            skip("kein Haupt-Aktenzeichen erkannt")
            continue
        if not citation.covered:
            skip(f"{citation.court} nicht im Bestand der API")
            continue
        lookup = client.lookup(citation.court, citation.az, fresh=fresh)
        main = Citation(rel, 0, citation.az, citation.court, True, date, False, "")
        status = classify(main, lookup)
        if status != "VERIFIED":
            skip(f"{citation.az}: {status}")
            continue
        ecli, reason = _unique_ecli(lookup.hits, date)
        if ecli is None:
            skip(f"{citation.az}: {reason}")
            continue
        closing = lines[bounds[1]]
        eol = "\r\n" if closing.endswith("\r\n") else "\n"
        new_lines = lines[:bounds[1]] + [f"ecli: {ecli}{eol}"] + lines[bounds[1]:]
        updates.append({"file": rel, "path": md, "az": citation.az, "ecli": ecli,
                        "data": "".join(new_lines).encode("utf-8")})
    return updates, skipped
