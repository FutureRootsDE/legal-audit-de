"""Locate Chrome or Edge and print a report HTML file to PDF in headless mode.

PDF_MODE is "cli" (spike 2026-11-17): Chrome 157 writes a tagged PDF from the command line,
so no CDP client is needed. Edge detaches and exits before the file exists, so print_pdf
polls for the finished file after the process ended.
"""
from __future__ import annotations

import os
import platform
import shutil
import signal
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Callable, Mapping

CHROME_ENV = "LEGAL_AUDIT_CHROME"
PDF_MODE = "cli"
VIRTUAL_TIME_BUDGET_MS = 15000
PDF_WAIT_SECONDS = 60.0  # how long to wait for the file after the process ended
PDF_POLL_INTERVAL = 0.25
PDF_STABLE_POLLS = 2  # consecutive polls with unchanged size
PDF_MAGIC = b"%PDF-"

LINUX_NAMES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
    "microsoft-edge-stable",
)
KILL_WAIT_SECONDS = 10
WIN_CHROME = Path("Google") / "Chrome" / "Application" / "chrome.exe"
WIN_EDGE = Path("Microsoft") / "Edge" / "Application" / "msedge.exe"
WIN_ROOT_VARS = ("ProgramFiles", "ProgramFiles(x86)", "LocalAppData")
MAC_APPS = (
    "Google Chrome.app/Contents/MacOS/Google Chrome",
    "Chromium.app/Contents/MacOS/Chromium",
    "Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)
MAC_PATHS = tuple(f"/Applications/{app}" for app in MAC_APPS)


class ChromeNotFound(Exception):
    """No Chrome or Edge executable could be located."""


class PdfError(Exception):
    """Printing the report to PDF failed."""


def candidate_paths(system: str, env: Mapping[str, str]) -> list[Path]:
    """Known install locations for the given OS name (platform.system())."""
    if system == "Windows":
        roots = [env[name] for name in WIN_ROOT_VARS if env.get(name)]
        chromes = [Path(root) / WIN_CHROME for root in roots]
        edges = [Path(root) / WIN_EDGE for root in roots]
        return chromes + edges
    if system == "Darwin":
        user_apps = Path.home() / "Applications"
        return [Path(p) for p in MAC_PATHS] + [user_apps / app for app in MAC_APPS]
    return []


def find_chrome(
    env: Mapping[str, str] | None = None,
    system: str | None = None,
    which: Callable[[str], str | None] = shutil.which,
    exists: Callable[[Path], bool] = Path.is_file,
) -> Path | None:
    """Return the browser to use: env override first, then known paths, then PATH lookup.

    A set LEGAL_AUDIT_CHROME that does not point to a file raises ChromeNotFound instead of
    silently falling back to another browser.
    """
    env = os.environ if env is None else env
    system = platform.system() if system is None else system
    override = env.get(CHROME_ENV)
    if override:
        if not exists(Path(override)):
            raise ChromeNotFound(
                f"Die Umgebungsvariable {CHROME_ENV} zeigt auf keine vorhandene Datei: {override}"
            )
        return Path(override)
    for path in candidate_paths(system, env):
        if exists(path):
            return path
    if system != "Windows":
        for name in LINUX_NAMES:
            found = which(name)
            if found:
                return Path(found)
    return None


def pdf_args(chrome: Path, html: Path, pdf: Path, profile_dir: Path) -> list[str]:
    """Argument list verified in the spike; always an isolated profile and a file URI."""
    return [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--disable-extensions",
        f"--user-data-dir={profile_dir}",
        "--no-pdf-header-footer",
        f"--virtual-time-budget={VIRTUAL_TIME_BUDGET_MS}",
        "--generate-pdf-document-outline",
        f"--print-to-pdf={pdf}",
        html.resolve().as_uri(),
    ]


def _is_pdf(pdf: Path) -> bool:
    try:
        with pdf.open("rb") as handle:
            return handle.read(len(PDF_MAGIC)) == PDF_MAGIC
    except OSError:
        return False


def _wait_for_pdf(pdf: Path, wait: float, interval: float) -> bool:
    """Poll until the PDF exists, starts with %PDF- and its size stayed stable."""
    deadline = time.monotonic() + wait
    last_size = -1
    stable = 0
    while True:
        if _is_pdf(pdf):
            try:
                size = pdf.stat().st_size
            except OSError:
                size = -1
            stable = stable + 1 if size == last_size and size > 0 else 0
            last_size = size
            if stable >= PDF_STABLE_POLLS:
                return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(interval)


def _kill_tree(proc: subprocess.Popen) -> None:
    """Terminate the browser and every child it started (Chrome spawns several processes)."""
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, timeout=KILL_WAIT_SECONDS
            )
        else:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        proc.kill()
    try:
        proc.wait(timeout=KILL_WAIT_SECONDS)
    except subprocess.TimeoutExpired:
        pass


def _run_browser(args: list[str], timeout: float) -> int:
    """Run the browser without capturing output; on timeout the whole process tree is killed."""
    extra = {} if os.name == "nt" else {"start_new_session": True}
    proc = subprocess.Popen(
        args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **extra
    )
    try:
        return proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        raise


def print_pdf(
    html: Path,
    pdf: Path,
    chrome: Path | None = None,
    timeout: int = 120,
    wait: float = PDF_WAIT_SECONDS,
    interval: float = PDF_POLL_INTERVAL,
) -> Path:
    """Print html to pdf with headless Chrome or Edge and return the pdf path."""
    chrome = chrome or find_chrome()
    if chrome is None:
        raise ChromeNotFound("Chrome oder Edge nicht gefunden.")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    if pdf.exists():
        pdf.unlink()
    with tempfile.TemporaryDirectory(prefix="legal-audit-chrome-", ignore_cleanup_errors=True) as profile:
        args = pdf_args(chrome, html, pdf, Path(profile))
        try:
            returncode = _run_browser(args, timeout)
        except subprocess.TimeoutExpired as exc:
            raise PdfError(f"Der Browser hat nach {timeout} Sekunden nicht geantwortet.") from exc
        except OSError as exc:
            raise PdfError(f"Der Browser konnte nicht gestartet werden: {exc.strerror or exc}") from exc
        # Edge exits with 0 before the file exists, so the wait ignores the exit code.
        if _wait_for_pdf(pdf, wait, interval):
            return pdf
        raise PdfError(
            f"Die PDF-Datei wurde nicht erzeugt (Exit-Code {returncode}, "
            f"Wartezeit {int(wait)} Sekunden). Bitte Chrome oder Edge prüfen."
        )
