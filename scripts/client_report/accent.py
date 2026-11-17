"""Accent color for the issuer letterhead: derived from the logo, kept readable on white.

PNG pixels are read with zlib only (8-bit RGB, RGBA, palette, no interlacing); SVG fill colors
come from the markup text. JPEG is not decoded: the caller asks the user once instead.
"""
from __future__ import annotations

import re
import struct
import zlib
from collections import Counter
from pathlib import Path

DEFAULT_ACCENT = "#2F3E46"
MIN_CONTRAST = 4.5
DARKEN_FACTOR = 0.95
MAX_LOGO_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 4_000_000
MAX_LIGHT_LUMINANCE = 0.85
ALPHA_THRESHOLD = 128

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SVG_FILL_RE = re.compile(
    r"fill\s*[=:]\s*[\"']?\s*(#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?)(?![0-9A-Fa-f])"
)

Rgb = tuple[int, int, int]


def _to_rgb(color: str) -> Rgb:
    value = color.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        raise ValueError(f"not a hex color: {color!r}")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _to_hex(rgb: Rgb) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _luminance(rgb: Rgb) -> float:
    def channel(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str = "#FFFFFF") -> float:
    """WCAG 2 contrast ratio between two hex colors."""
    a, b = _luminance(_to_rgb(fg)), _luminance(_to_rgb(bg))
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def ensure_contrast(color: str, min_ratio: float = MIN_CONTRAST) -> str:
    """Darken `color` in 5 percent steps until it reaches `min_ratio` against white."""
    rgb = _to_rgb(color)
    while contrast_ratio(_to_hex(rgb)) < min_ratio and rgb != (0, 0, 0):
        rgb = (int(rgb[0] * DARKEN_FACTOR), int(rgb[1] * DARKEN_FACTOR), int(rgb[2] * DARKEN_FACTOR))
    return _to_hex(rgb)


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def _chunks(data: bytes):
    pos = len(PNG_SIGNATURE)
    while pos + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if len(body) != length:
            return
        yield kind, body
        pos += 12 + length


def _unfilter(raw: bytes, width: int, height: int, bpp: int) -> list[bytearray] | None:
    stride = width * bpp
    if len(raw) < height * (stride + 1):
        return None
    rows: list[bytearray] = []
    prev = bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        ftype = raw[start]
        line = bytearray(raw[start + 1:start + 1 + stride])
        if ftype > 4:
            return None
        if ftype:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                up = prev[i]
                if ftype == 1:
                    add = left
                elif ftype == 2:
                    add = up
                elif ftype == 3:
                    add = (left + up) // 2
                else:
                    add = _paeth(left, up, prev[i - bpp] if i >= bpp else 0)
                line[i] = (line[i] + add) & 0xFF
        rows.append(line)
        prev = line
    return rows


def dominant_color_png(data: bytes) -> str | None:
    """Most frequent opaque, not too light color of an 8-bit non-interlaced PNG, else None."""
    if not data.startswith(PNG_SIGNATURE):
        return None
    header = None
    palette = b""
    trns = b""
    idat = bytearray()
    for kind, body in _chunks(data):
        if kind == b"IHDR" and len(body) == 13:
            header = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            palette = body
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break
    if header is None:
        return None
    width, height, depth, ctype, _comp, _filt, interlace = header
    bpp_by_type = {2: 3, 3: 1, 6: 4}
    if depth != 8 or interlace != 0 or ctype not in bpp_by_type:
        return None
    if width <= 0 or height <= 0 or width * height > MAX_PIXELS:
        return None
    bpp = bpp_by_type[ctype]
    expected = height * (width * bpp + 1)
    try:
        # the length cap bounds memory against decompression bombs
        raw = zlib.decompressobj().decompress(bytes(idat), expected + 1)
    except zlib.error:
        return None
    rows = _unfilter(raw, width, height, bpp)
    if rows is None:
        return None
    counts: Counter[Rgb] = Counter()
    for line in rows:
        for x in range(width):
            if ctype == 2:
                rgb, alpha = (line[x * 3], line[x * 3 + 1], line[x * 3 + 2]), 255
            elif ctype == 6:
                rgb, alpha = (line[x * 4], line[x * 4 + 1], line[x * 4 + 2]), line[x * 4 + 3]
            else:
                index = line[x]
                if index * 3 + 2 >= len(palette):
                    return None
                rgb = (palette[index * 3], palette[index * 3 + 1], palette[index * 3 + 2])
                alpha = trns[index] if index < len(trns) else 255
            if alpha < ALPHA_THRESHOLD or _luminance(rgb) > MAX_LIGHT_LUMINANCE:
                continue
            counts[rgb] += 1
    if not counts:
        return None
    return _to_hex(counts.most_common(1)[0][0])


def svg_fill_colors(text: str) -> list[str]:
    """Fill colors found in SVG markup (`fill="#..."` and `fill:#...`), uppercase 6-digit hex."""
    return [_to_hex(_to_rgb(m.group(1))) for m in SVG_FILL_RE.finditer(text)]


def _dominant_svg(text: str) -> str | None:
    usable = [c for c in svg_fill_colors(text) if _luminance(_to_rgb(c)) <= MAX_LIGHT_LUMINANCE]
    return Counter(usable).most_common(1)[0][0] if usable else None


def derive_accent(logo: Path) -> str | None:
    """Accent color from a PNG or SVG logo, contrast-adjusted; None for JPEG or on failure."""
    path = Path(logo)
    suffix = path.suffix.lower()
    if suffix not in (".png", ".svg"):
        return None
    try:
        if path.stat().st_size > MAX_LOGO_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if suffix == ".png":
        dominant = dominant_color_png(data)
    else:
        dominant = _dominant_svg(data.decode("utf-8", "replace"))
    return ensure_contrast(dominant) if dominant else None
