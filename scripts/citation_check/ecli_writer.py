"""Planning and writing of the optional `ecli:` frontmatter line in knowledge/urteile/*.md."""
from __future__ import annotations

import hashlib
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .api import ApiClient
from .classify import LookupMap, classify
from .extract import MAX_FILE_BYTES, _rel, extract_citations, find_dates
from .fsutil import is_link_like, is_under
from .models import Citation
from .text import short

ECLI_WRITE_RE = re.compile(r"ECLI:DE:[A-Z]+:[0-9]{4}:[A-Z0-9.]+")  # strict: only this is ever written to the KB
ECLI_COURT_CODES = {"BGH": "BGH", "BFH": "BFH", "BVerwG": "BVERWG", "BAG": "BAG",
                    "BSG": "BSG", "BVerfG": "BVERFG", "BPatG": "BPATG"}

WARNING_LIMIT = 300


class _Skip(Exception):
    """A file is left untouched; `reason` is reported."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class EcliUpdate:
    file: str
    path: Path
    az: str
    ecli: str
    data: bytes
    digest: str  # sha256 of the bytes read while planning (lost-update guard)
    from_cache: bool


@dataclass
class ApplyResult:
    written: list[EcliUpdate] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)
    failed: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class EcliOutcome:
    """Everything the report needs to know about a --write-ecli run."""
    updates: list[EcliUpdate] = field(default_factory=list)
    written: list[EcliUpdate] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)
    failed: list[dict] = field(default_factory=list)
    dry_run: bool = False


def digest_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def _unique_ecli(hits: list[dict], date: str | None, court: str) -> str:
    """The one strictly valid ECLI of the court's hits; raises _Skip if there is none or it is ambiguous."""
    candidates = [h for h in hits if date is None or h.get("date") == date]
    valid = {h["ecli"] for h in candidates
             if isinstance(h.get("ecli"), str) and ECLI_WRITE_RE.fullmatch(h["ecli"])}
    if not valid:
        raise _Skip("kein ECLI im Treffer oder ECLI entspricht nicht dem strengen Muster")
    code = ECLI_COURT_CODES.get(court)
    matching = {e for e in valid if code is not None and e.split(":")[2] == code}
    if not matching:
        raise _Skip(f"ECLI passt nicht zum Gericht {court}")
    if len(matching) > 1:
        raise _Skip("mehrere Treffer, ohne eindeutiges Datum nicht entscheidbar")
    return matching.pop()


def _warn(warnings: list[str] | None, message: str) -> None:
    if warnings is not None:
        warnings.append(short(message, WARNING_LIMIT))


def atomic_write(path: Path, data: bytes, guard: Callable[[], None] | None = None,
                 warnings: list[str] | None = None) -> None:
    """Write `data` via a temp file. `guard` runs right before os.replace (after write and fsync)
    and may raise _Skip; the temp file is then removed and the target stays untouched."""
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=".tmp-ecli-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.chmod(tmp_name, path.stat().st_mode & 0o777)
        except OSError as exc:
            _warn(warnings, f"{path.name}: Dateirechte nicht uebernommen (chmod): {exc}")
        if guard is not None:
            guard()
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError as exc:
            _warn(warnings, f"{path.name}: Temp-Datei {Path(tmp_name).name} nicht entfernt: {exc}")
        raise


def _regular_file(path: Path, urteile: Path) -> None:
    """Raise _Skip unless `path` is a regular, non-linked file below the real urteile directory."""
    if is_link_like(path):
        raise _Skip("Symlink oder Verzeichnis-Link, nicht angefasst")
    if not path.is_file() or not is_under(path, urteile):
        raise _Skip("keine regulaere Datei unterhalb von urteile/")


def _read_for_plan(md: Path, urteile: Path) -> bytes:
    _regular_file(md, urteile)
    try:
        with md.open("rb") as handle:
            raw = handle.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        raise _Skip(f"nicht lesbar: {short(exc)}") from None
    if len(raw) > MAX_FILE_BYTES:
        raise _Skip("Datei zu gross")
    return raw


def _plan_file(md: Path, rel: str, urteile: Path, client: ApiClient, fresh: bool,
               known: LookupMap) -> EcliUpdate:
    raw = _read_for_plan(md, urteile)
    try:
        lines = _split_lines(raw.decode("utf-8"))
    except UnicodeDecodeError:
        raise _Skip("nicht lesbar: kein UTF-8") from None
    bounds = _frontmatter_bounds(lines)
    if bounds is None:
        raise _Skip("kein Frontmatter")
    if any(re.match(r"ecli\s*:", ln) for ln in lines[1:bounds[1]]):
        raise _Skip("ecli bereits vorhanden")
    citation, date = _main_reference(lines, bounds[1] + 1)
    if citation is None:
        raise _Skip("kein Haupt-Aktenzeichen erkannt")
    if not citation.covered:
        raise _Skip(f"{short(citation.court)} nicht im Bestand der API")
    key = (citation.court, citation.az)
    if key not in known:
        known[key] = client.lookup(*key, fresh=fresh)
    lookup = known[key]
    status = classify(Citation(rel, 0, citation.az, citation.court, True, date, False, ""), lookup)
    if status != "VERIFIED":
        raise _Skip(f"{citation.az}: {status}")
    ecli = _unique_ecli(lookup.hits, date, citation.court)
    eol = "\r\n" if lines[bounds[1]].endswith("\r\n") else "\n"
    new_lines = lines[:bounds[1]] + [f"ecli: {ecli}{eol}"] + lines[bounds[1]:]
    return EcliUpdate(rel, md, citation.az, ecli, "".join(new_lines).encode("utf-8"),
                      digest_of(raw), lookup.from_cache)


def plan_ecli_updates(kb_path: Path, client: ApiClient, fresh: bool = False,
                      known: LookupMap | None = None) -> tuple[list[EcliUpdate], list[dict]]:
    """Return (updates, skipped). Updates carry the new file bytes, never written here.

    `known` shares lookup results with the report step so no Aktenzeichen is queried twice.
    """
    known = known if known is not None else {}
    folder = kb_path / "urteile"
    if is_link_like(folder):
        return [], [{"file": _rel(folder, kb_path), "reason": "urteile ist ein Symlink oder Verzeichnis-Link"}]
    if not folder.is_dir():
        return [], []
    updates: list[EcliUpdate] = []
    skipped: list[dict] = []
    for md in sorted(folder.glob("*.md")):
        rel = _rel(md, kb_path)
        try:
            updates.append(_plan_file(md, rel, folder, client, fresh, known))
        except _Skip as skip:
            skipped.append({"file": rel, "reason": skip.reason})
    return updates, skipped


def _final_guard(update: EcliUpdate, urteile: Path) -> None:
    """Last check right before the replace: no link, still below urteile/, unchanged since planning."""
    if is_link_like(urteile):
        raise _Skip("urteile ist ein Symlink oder Verzeichnis-Link, nicht angefasst")
    _regular_file(update.path, urteile)
    try:
        current = update.path.read_bytes()
    except OSError as exc:
        raise _Skip(f"nicht lesbar: {short(exc)}") from None
    if digest_of(current) != update.digest:
        raise _Skip("Datei seit der Planung geaendert, uebersprungen")


def apply_updates(updates: list[EcliUpdate], kb_path: Path) -> ApplyResult:
    """Write each update; a failing file never stops the others."""
    result = ApplyResult()
    urteile = kb_path / "urteile"
    for update in updates:
        try:
            atomic_write(update.path, update.data, guard=lambda u=update: _final_guard(u, urteile),
                         warnings=result.warnings)
        except _Skip as skip:
            result.skipped.append({"file": update.file, "reason": skip.reason})
        except OSError as exc:
            result.failed.append({"file": update.file, "error": short(exc)})
        else:
            result.written.append(update)
    return result
