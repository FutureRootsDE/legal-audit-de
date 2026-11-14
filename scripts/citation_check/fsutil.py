"""Small filesystem helpers shared by cache and ECLI writer."""
from __future__ import annotations

import os
import stat
from pathlib import Path

REPARSE_POINT = 0x400  # Windows FILE_ATTRIBUTE_REPARSE_POINT (symlink, junction)


def is_link_like(path: Path) -> bool:
    """True for symlinks and Windows junctions/reparse points (checked without following them)."""
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE_POINT)


def is_under(path: Path, parent: Path) -> bool:
    """True if the resolved `path` lies inside the resolved `parent`."""
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False
