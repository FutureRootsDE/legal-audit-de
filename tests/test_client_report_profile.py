"""Offline tests for client_report.accent and client_report.profile."""
from __future__ import annotations

import struct
import tempfile
import unittest
import zlib
from pathlib import Path

import support  # noqa: F401  (puts scripts/ on sys.path)
from client_report.accent import (
    DEFAULT_ACCENT,
    contrast_ratio,
    derive_accent,
    dominant_color_png,
    ensure_contrast,
    svg_fill_colors,
)
from client_report.models import ReportInputError
from client_report.profile import (
    PROFILE_FILENAME,
    load_profile,
    logo_path,
    profile_dir,
    save_profile,
    validate_profile,
)


def _chunk(kind: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def png_from_pixels(pixels: list[tuple[int, ...]], width: int, height: int, ctype: int = 2, filter_type: int = 0,
                    palette: bytes = b"", trns: bytes = b"") -> bytes:
    """Build an 8-bit PNG; filter 1 (Sub) is applied when requested to exercise unfiltering."""
    bpp = {2: 3, 6: 4, 3: 1}[ctype]
    raw = bytearray()
    for y in range(height):
        row = bytearray()
        for x in range(width):
            px = pixels[y * width + x]
            row += bytes(px)
        if filter_type == 1:
            out = bytearray(row)
            for i in range(len(row) - 1, bpp - 1, -1):
                out[i] = (row[i] - row[i - bpp]) & 0xFF
            raw += bytes([1]) + out
        else:
            raw += bytes([0]) + row
    data = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, ctype, 0, 0, 0))
    if palette:
        data += _chunk(b"PLTE", palette)
    if trns:
        data += _chunk(b"tRNS", trns)
    return data + _chunk(b"IDAT", zlib.compress(bytes(raw))) + _chunk(b"IEND", b"")


def write_png(path: Path, color: tuple[int, int, int]) -> None:
    path.write_bytes(png_from_pixels([color] * 16, 4, 4))


def write_png_mixed(path: Path, majority: tuple[int, int, int], minority: tuple[int, int, int]) -> None:
    """4x4 PNG: 12 pixels of `majority`, 4 pixels of `minority`."""
    path.write_bytes(png_from_pixels([majority] * 12 + [minority] * 4, 4, 4))


class Accent(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def test_contrast_reference_values(self):
        self.assertAlmostEqual(contrast_ratio("#000000"), 21.0, places=1)
        self.assertAlmostEqual(contrast_ratio("#FFFFFF"), 1.0, places=2)

    def test_png_dominant_ignores_white_and_transparent(self):
        p = self.dir / "a.png"
        write_png(p, (31, 78, 121))
        self.assertEqual(derive_accent(p), "#1F4E79")
        write_png_mixed(p, majority=(255, 255, 255), minority=(31, 78, 121))
        self.assertEqual(derive_accent(p), "#1F4E79")
        rgba = png_from_pixels([(200, 0, 0, 0)] * 12 + [(31, 78, 121, 255)] * 4, 4, 4, ctype=6)
        self.assertEqual(dominant_color_png(rgba), "#1F4E79")

    def test_png_sub_filter_and_palette(self):
        sub = png_from_pixels([(10, 20, 30), (10, 20, 30), (50, 60, 70), (10, 20, 30)], 2, 2, filter_type=1)
        self.assertEqual(dominant_color_png(sub), "#0A141E")
        pal = png_from_pixels([(0,), (0,), (1,), (0,)], 2, 2, ctype=3,
                              palette=bytes([31, 78, 121, 250, 250, 250]))
        self.assertEqual(dominant_color_png(pal), "#1F4E79")

    def test_png_unusable_inputs_return_none(self):
        self.assertIsNone(dominant_color_png(b"not a png"))
        self.assertIsNone(dominant_color_png(b"\x89PNG\r\n\x1a\n" + b"\x00" * 5))
        white = png_from_pixels([(255, 255, 255)] * 4, 2, 2)
        self.assertIsNone(dominant_color_png(white))

    def test_light_color_is_darkened(self):
        self.assertGreaterEqual(contrast_ratio(ensure_contrast("#FFD54F")), 4.5)
        self.assertEqual(ensure_contrast("#1F4E79"), "#1F4E79")
        self.assertGreaterEqual(contrast_ratio(ensure_contrast("#FFFFFF")), 4.5)

    def test_default_accent_meets_contrast(self):
        self.assertGreaterEqual(contrast_ratio(DEFAULT_ACCENT), 4.5)

    def test_svg_fill_and_jpg_none(self):
        self.assertEqual(svg_fill_colors('<path fill="#abc"/><g style="fill:#1f4e79;stroke:#fff"/>'),
                         ["#AABBCC", "#1F4E79"])
        svg = self.dir / "l.svg"
        svg.write_text('<svg xmlns="x"><path fill="#1F4E79"/><path fill="#1F4E79"/><path fill="#FFFFFF"/></svg>',
                       encoding="utf-8")
        self.assertEqual(derive_accent(svg), "#1F4E79")
        jpg = self.dir / "l.jpg"
        jpg.write_bytes(b"\xff\xd8\xff\xe0")
        self.assertIsNone(derive_accent(jpg))
        self.assertIsNone(derive_accent(self.dir / "missing.png"))


def _profile(**over):
    base = {
        "company": "Muster Web GmbH",
        "contact": "Erika Muster",
        "address": ["Musterstraße 1", "12345 Musterstadt"],
        "email": "info@example.de",
        "logo_file": "client-test-logo.png",
        "accent_color": "#1F4E79",
    }
    base.update(over)
    return base


class Profile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.env = {"LEGAL_AUDIT_CLIENT_TEST_HOME": str(self.dir / "home")}
        self.logo = self.dir / "mein logo ä.png"
        write_png(self.logo, (31, 78, 121))

    def test_round_trip_in_override_dir(self):
        target = save_profile(_profile(), self.logo, self.env)
        self.assertEqual(target, self.dir / "home" / PROFILE_FILENAME)
        loaded = load_profile(self.env)
        self.assertEqual(loaded, _profile())
        self.assertTrue(logo_path(loaded, self.env).is_file())
        self.assertEqual(logo_path(loaded, self.env).read_bytes(), self.logo.read_bytes())

    def test_load_without_profile_or_logo_is_none(self):
        self.assertIsNone(load_profile(self.env))
        save_profile(_profile(), self.logo, self.env)
        logo_path(_profile(), self.env).unlink()
        self.assertIsNone(load_profile(self.env))

    def test_load_accepts_bom(self):
        save_profile(_profile(), self.logo, self.env)
        target = self.dir / "home" / PROFILE_FILENAME
        target.write_bytes(b"\xef\xbb\xbf" + target.read_bytes())
        self.assertEqual(load_profile(self.env), _profile())

    def test_client_fields_rejected(self):
        issues = validate_profile(_profile(client={"name": "X"}))
        self.assertTrue(any(i.path == "profile.client" for i in issues))

    def test_required_and_format_rules(self):
        self.assertEqual(validate_profile(_profile()), [])
        self.assertTrue(validate_profile(_profile(accent_color="blue")))
        self.assertTrue(validate_profile(_profile(accent_color="#FFF")))
        self.assertTrue(validate_profile(_profile(address=[])))
        no_contact = _profile()
        del no_contact["email"]
        self.assertTrue(validate_profile(no_contact))
        phone_only = _profile(phone="0123")
        del phone_only["email"]
        self.assertEqual(validate_profile(phone_only), [])
        missing = _profile()
        del missing["company"]
        self.assertTrue(validate_profile(missing))

    def test_logo_file_must_be_bare_name(self):
        for bad in ("../x.png", "..\\x.png", "/etc/passwd", "C:\\x.png", "logo.png", "client-test-logo.exe"):
            self.assertTrue(validate_profile(_profile(logo_file=bad)), bad)

    def test_save_rejects_bad_logos(self):
        cases = {
            "x.gif": b"GIF89a",
            "x.png": b"this is not a png",
            "x.svg": b"plain text",
            "x.jpg": b"\x89PNG\r\n\x1a\n",
        }
        for name, content in cases.items():
            bad = self.dir / name
            bad.write_bytes(content)
            with self.assertRaises(ValueError, msg=name):
                save_profile(_profile(), bad, self.env)
        with self.assertRaises(ValueError):
            save_profile(_profile(), self.dir, self.env)
        with self.assertRaises(ValueError):
            save_profile(_profile(), self.dir / "missing.png", self.env)

    def test_oversize_logo_rejected(self):
        import client_report.profile as profile_module

        old = profile_module.MAX_LOGO_BYTES
        profile_module.MAX_LOGO_BYTES = 10
        try:
            with self.assertRaises(ValueError):
                save_profile(_profile(), self.logo, self.env)
        finally:
            profile_module.MAX_LOGO_BYTES = old

    def test_invalid_data_raises_input_error_and_writes_nothing(self):
        with self.assertRaises(ReportInputError):
            save_profile(_profile(accent_color="red"), self.logo, self.env)
        self.assertFalse((self.dir / "home").exists())

    def test_logo_format_change_removes_old_copy(self):
        save_profile(_profile(), self.logo, self.env)
        svg = self.dir / "l.svg"
        svg.write_text('<?xml version="1.0"?><svg xmlns="x"></svg>', encoding="utf-8")
        save_profile(_profile(), svg, self.env)
        self.assertFalse((self.dir / "home" / "client-test-logo.png").exists())
        self.assertEqual(load_profile(self.env)["logo_file"], "client-test-logo.svg")

    def test_svg_logo_is_copied_as_file_only(self):
        svg = self.dir / "l.svg"
        svg.write_text("<svg xmlns='x'><script>1</script></svg>", encoding="utf-8")
        save_profile(_profile(), svg, self.env)
        self.assertTrue((self.dir / "home" / "client-test-logo.svg").is_file())

    def test_dir_order(self):
        self.assertEqual(profile_dir({"CLAUDE_PLUGIN_DATA": "/d"}), Path("/d"))
        self.assertEqual(profile_dir({"CODEX_HOME": "/c"}), Path("/c/legal-audit-de-client-test"))
        self.assertEqual(profile_dir({"COPILOT_HOME": "/p"}), Path("/p/legal-audit-de-client-test"))
        self.assertEqual(
            profile_dir({"LEGAL_AUDIT_CLIENT_TEST_HOME": "/o", "CLAUDE_PLUGIN_DATA": "/d"}), Path("/o")
        )
        self.assertEqual(profile_dir({}).name, "legal-audit-de-client-test")


if __name__ == "__main__":
    unittest.main()
