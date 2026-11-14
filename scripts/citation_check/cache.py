"""Local JSON cache of API hits and vetting of the cache directory."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import time
from pathlib import Path
from typing import Callable

from .hits import sanitize_hit

MAX_CACHE_ENTRY_BYTES = 5_000_000
REPARSE_POINT = 0x400  # Windows FILE_ATTRIBUTE_REPARSE_POINT (symlink, junction)


class HitCache:
    """Entries are untrusted input: validated on read, written atomically."""

    def __init__(self, cache_dir: Path | None, ttl_seconds: float, offline: bool = False,
                 warnings: list[str] | None = None,
                 now: Callable[[], float] = time.time) -> None:
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        self.offline = offline
        self.warnings = warnings if warnings is not None else []
        self._now = now

    def now_epoch(self) -> float:
        return self._now()

    def path(self, court: str, az: str) -> Path | None:
        if self.cache_dir is None:
            return None
        digest = hashlib.sha256(f"{court}|{az}".encode("utf-8")).hexdigest()
        return self.cache_dir / f"{digest}.json"

    def read(self, court: str, az: str) -> list[dict] | None:
        path = self.path(court, az)
        if path is None:
            return None
        try:
            if path.is_symlink() or not path.is_file():
                return None
            if path.stat().st_size > MAX_CACHE_ENTRY_BYTES:
                return None
            entry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return self._validated_hits(entry, court, az)

    def _validated_hits(self, entry: object, court: str, az: str) -> list[dict] | None:
        """Return hits of a cache entry, or None if it is malformed or stale."""
        if not isinstance(entry, dict) or set(entry) != {"court", "az", "fetched_at", "hits"}:
            return None
        if entry["court"] != court or entry["az"] != az:
            return None
        fetched = entry["fetched_at"]
        if isinstance(fetched, bool) or not isinstance(fetched, (int, float)):
            return None
        age = self.now_epoch() - fetched
        if age < -60 or (not self.offline and age > self.ttl_seconds):
            return None
        hits = entry["hits"]
        if not isinstance(hits, list):
            return None
        if any(not isinstance(h, dict) or sanitize_hit(h) != h for h in hits):
            return None
        return hits

    def write(self, court: str, az: str, hits: list[dict]) -> None:
        path = self.path(court, az)
        if path is None:
            return
        entry = {"court": court, "az": az, "fetched_at": self.now_epoch(), "hits": hits}
        tmp_name = None
        try:
            self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(dir=self.cache_dir, prefix=".tmp-cache-", suffix=".json")
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False))
            os.replace(tmp_name, path)
            tmp_name = None
        except OSError as exc:
            self.warnings.append(f"Cache nicht schreibbar ({self.cache_dir}): {exc}")
        finally:
            if tmp_name is not None:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass


def default_cache_dir() -> Path:
    """Per-user cache location (never the shared system temp directory)."""
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "citation-check" / "cache"
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = xdg if xdg and os.path.isabs(xdg) else str(Path.home() / ".cache")
    return Path(base) / "citation-check"


def _current_uid() -> int | None:
    return os.getuid() if hasattr(os, "getuid") else None


def prepare_cache_dir(path: Path) -> tuple[Path | None, str | None]:
    """Create (mode 0700) and vet the cache directory.

    Returns (usable path or None, warning). A directory that is a symlink, owned by
    someone else or writable by group/others disables the cache for this run.
    """
    try:
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = os.lstat(path)
    except OSError as exc:
        return None, f"Cache deaktiviert: {path} nicht nutzbar ({exc})."
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & REPARSE_POINT:
        return None, f"Cache deaktiviert: {path} ist ein Symlink oder Verzeichnis-Link."
    if not stat.S_ISDIR(info.st_mode):
        return None, f"Cache deaktiviert: {path} ist kein Verzeichnis."
    uid = _current_uid()
    if uid is not None:
        if info.st_uid != uid:
            return None, f"Cache deaktiviert: {path} gehoert einem anderen Nutzer."
        if info.st_mode & 0o022:
            return None, f"Cache deaktiviert: {path} ist fuer Gruppe oder Andere schreibbar."
    return path, None
