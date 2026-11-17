"""Report folder naming and safe paths inside a report folder (spec 6.7, 6.8 "Untrusted Input").

Everything here treats its input as hostile: URLs come from the command line, evidence paths
from findings.json, which the model writes from content of the audited website.
"""
from __future__ import annotations

import ipaddress
import re
from datetime import date
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

ALLOWED_SCHEMES = ("http", "https")
EVIDENCE_DIR = "evidence"
ASSETS_DIR = "assets"
MAX_SLUG_CHARS = 63
MAX_SUFFIX = 999
WINDOWS_RESERVED = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
    | {f"COM{i}" for i in range(10)} | {f"LPT{i}" for i in range(10)}
    | {f"COM{c}" for c in "¹²³"} | {f"LPT{c}" for c in "¹²³"}
)
RESERVED_SUFFIX = "-host"

MAX_HOST_CHARS = 253
MAX_LABEL_CHARS = 63

# Always used with fullmatch: `$` would accept a trailing newline.
HOST_RE = re.compile(r"[a-z0-9-]+(\.[a-z0-9-]+)*")
# Whitespace, control characters and the backslash (browsers read it as "/", urlsplit does not).
UNSAFE_URL_RE = re.compile(r"[\s\x00-\x1f\x7f\\]")
SLUG_DROP_RE = re.compile(r"[^a-z0-9-]")
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")


def domain_from_url(url: str) -> str:
    """Host of an http(s) URL: lower case, IDN as Punycode, without port, trailing dot or `www.`."""
    if not isinstance(url, str):
        raise ValueError("URL muss ein Text sein")
    url = url.strip()
    if not url or UNSAFE_URL_RE.search(url):
        raise ValueError("URL ist leer oder enthält Leerzeichen, Steuerzeichen oder einen Backslash")
    parts = urlsplit(url)
    if parts.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("nur http- und https-URLs sind erlaubt")
    try:
        parts.port  # noqa: B018  (raises ValueError on an invalid port)
    except ValueError as exc:
        raise ValueError("ungültiger Port in der URL") from exc
    host = (parts.hostname or "").rstrip(".")
    if ":" in host:
        raise ValueError("IPv6-Adressen werden nicht unterstützt")
    if host.startswith("www.") and len(host) > len("www."):
        host = host[len("www."):]
    try:
        host = host.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("Hostname ist kein gültiger Domainname") from exc
    if not HOST_RE.fullmatch(host):
        raise ValueError("Hostname fehlt oder enthält unzulässige Zeichen")
    _check_host_shape(host)
    return host


def _check_host_shape(host: str) -> None:
    """RFC 1035 limits plus IPv4 handling for an ASCII host that already matches HOST_RE.

    IPv4 addresses are allowed (the spec is silent on them; local fixture runs use 127.0.0.1),
    but only as a valid dotted quad: an all-numeric last label is never a domain name (RFC 3696
    section 2), so "256.1.1.1" or "1.2.3" is rejected instead of being read as a host name.
    IPv6 is rejected earlier.
    """
    if len(host) > MAX_HOST_CHARS:
        raise ValueError(f"Hostname länger als {MAX_HOST_CHARS} Zeichen")
    labels = host.split(".")
    for label in labels:
        if len(label) > MAX_LABEL_CHARS:
            raise ValueError(f"Abschnitt des Hostnamens länger als {MAX_LABEL_CHARS} Zeichen")
        if label.startswith("-") or label.endswith("-"):
            raise ValueError("Abschnitt des Hostnamens beginnt oder endet mit einem Bindestrich")
    if labels[-1].isdigit():
        try:
            ipaddress.IPv4Address(host)
        except ValueError as exc:
            raise ValueError("Hostname ist weder Domainname noch gültige IPv4-Adresse") from exc


def domain_slug(domain: str) -> str:
    """Folder-safe form of a domain: only [a-z0-9-], dots become `-`, at most 63 characters."""
    slug = SLUG_DROP_RE.sub("", str(domain).lower().replace(".", "-"))
    slug = slug[:MAX_SLUG_CHARS].strip("-")
    if not slug:
        raise ValueError("Domain ergibt keinen gültigen Ordnernamen")
    if slug.upper() in WINDOWS_RESERVED:
        slug += RESERVED_SUFFIX
    return slug


def new_report_dir(base: Path, day: date, domain: str) -> Path:
    """Create `<base>/<JJJJ-MM-TT>-<slug>` with `evidence/` and `assets/`; suffix -2, -3, ... if taken.

    An existing folder or file is never reused or overwritten (mkdir without exist_ok is atomic).
    """
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    root = base.resolve()
    stem = f"{day.strftime('%Y-%m-%d')}-{domain_slug(domain)}"
    for n in range(1, MAX_SUFFIX + 1):
        candidate = base / (stem if n == 1 else f"{stem}-{n}")
        if candidate.resolve().parent != root:
            raise ValueError("Report-Ordner läge außerhalb des Basisordners")
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        (candidate / EVIDENCE_DIR).mkdir()
        (candidate / ASSETS_DIR).mkdir()
        return candidate
    raise FileExistsError(f"zu viele Report-Ordner für {stem}")


def _check_parts(rel: str) -> None:
    """Reject anything that is not a plain relative POSIX path with ordinary segments."""
    if CONTROL_RE.search(rel):
        raise ValueError("Pfad enthält Steuerzeichen")
    if "\\" in rel:
        raise ValueError("Pfad darf keinen Backslash enthalten, nur „/“ als Trenner")
    if ":" in rel or PureWindowsPath(rel).drive or PurePosixPath(rel).is_absolute():
        raise ValueError("Pfad muss relativ zum Report-Ordner sein (kein Laufwerk, kein absoluter Pfad)")
    for part in rel.split("/"):
        if part in ("", ".", ".."):
            raise ValueError("Pfad darf keine leeren Abschnitte, „.“ oder „..“ enthalten")
        if part != part.rstrip(" ."):
            raise ValueError("Pfadabschnitte dürfen nicht auf Punkt oder Leerzeichen enden")
        if part.split(".")[0].upper() in WINDOWS_RESERVED:
            raise ValueError(f"reservierter Windows-Gerätename im Pfad: {part}")


def safe_evidence_path(report_dir: Path, rel: str) -> Path:
    """Resolved path of an existing file inside `report_dir`; raises ValueError otherwise.

    Symlinks are followed by resolve(), so a link pointing outside the folder is rejected.
    """
    if not isinstance(rel, str) or not rel.strip():
        raise ValueError("Pfad fehlt")
    _check_parts(rel)
    root = Path(report_dir).resolve()
    target = (root / rel).resolve()
    if target == root or not target.is_relative_to(root):
        raise ValueError("Pfad liegt außerhalb des Report-Ordners")
    if not target.is_file():
        raise ValueError(f"Datei fehlt im Report-Ordner: {rel}")
    return target
