#!/usr/bin/env python3
"""
Bundles a LegalAudit.md + all clean/*.md + SUMMARY.md into a single printable HTML
(which can be saved as PDF via Browser-Print) and, if pandoc is available, also directly to PDF.

Usage:
  python legal-audit-pdf.py <audit-directory>
      — audit-directory = path to docs/legal-audit/ oder audits/<name>/

Output:
  <audit-directory>/anwalts-briefing.html    (always)
  <audit-directory>/anwalts-briefing.pdf     (if pandoc is available)
"""
import argparse
import html
import os
import shutil
import subprocess
import sys
from pathlib import Path


HTML_SHELL = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Anwalts-Briefing — {title}</title>
<style>
  @page {{ margin: 2cm; }}
  body {{ font-family: Georgia, "Times New Roman", serif; line-height: 1.5; max-width: 750px; margin: 0 auto; padding: 2em; color: #111; }}
  h1 {{ page-break-before: always; border-bottom: 3px solid #2c5aa0; padding-bottom: 0.3em; }}
  h1:first-of-type {{ page-break-before: avoid; }}
  h2 {{ color: #2c5aa0; margin-top: 2em; }}
  h3 {{ color: #555; }}
  blockquote {{ border-left: 4px solid #c00; background: #fee; padding: 0.8em 1em; font-style: normal; }}
  code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }}
  pre {{ background: #f4f4f4; padding: 1em; border-radius: 4px; overflow-x: auto; font-size: 0.85em; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
  th, td {{ border: 1px solid #ccc; padding: 0.5em 0.8em; text-align: left; }}
  th {{ background: #f0f4fa; }}
  .meta {{ background: #f8f8f8; padding: 1em; border-radius: 4px; margin-bottom: 2em; font-size: 0.9em; }}
  .toc a {{ color: #2c5aa0; text-decoration: none; }}
  .toc a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
{content}
</body>
</html>
"""


def render_markdown(text: str) -> str:
    """Very lightweight MD→HTML. For production quality, prefer pandoc."""
    try:
        import markdown  # type: ignore
        return markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])
    except ImportError:
        # Fallback: pre-escaped in <pre>
        escaped = html.escape(text)
        return f"<pre style='white-space: pre-wrap; font-family: inherit;'>{escaped}</pre>"


def collect_sources(audit_dir: Path) -> list[tuple[str, Path]]:
    """Liefert (titel, path) in der Reihenfolge, in der sie im PDF erscheinen sollen."""
    sources: list[tuple[str, Path]] = []

    for name, title in [
        ("SUMMARY.md", "Executive Summary"),
        ("LegalAudit.md", "Legal Audit — Findings"),
    ]:
        p = audit_dir / name
        if p.exists():
            sources.append((title, p))

    clean = audit_dir / "clean"
    if clean.exists():
        for md in sorted(clean.glob("*.md")):
            stem = md.stem
            sources.append((f"Clean Version — {stem}", md))

    return sources


def build_html(audit_dir: Path, project_title: str) -> str:
    sources = collect_sources(audit_dir)
    if not sources:
        raise RuntimeError(f"Keine Audit-Dateien gefunden in {audit_dir}")

    parts = []

    # TOC
    toc_items = []
    for idx, (title, _) in enumerate(sources, start=1):
        safe_anchor = f"doc-{idx}"
        toc_items.append(f'<li><a href="#{safe_anchor}">{html.escape(title)}</a></li>')
    parts.append('<div class="meta">')
    parts.append(f"<h1>Anwalts-Briefing — {html.escape(project_title)}</h1>")
    parts.append(f'<p><strong>Audit-Verzeichnis:</strong> {html.escape(str(audit_dir))}</p>')
    parts.append(f'<p><strong>Dokumente:</strong> {len(sources)}</p>')
    parts.append('<h2>Inhalt</h2>')
    parts.append(f'<ol class="toc">{"".join(toc_items)}</ol>')
    parts.append('</div>')

    # Sections
    for idx, (title, path) in enumerate(sources, start=1):
        safe_anchor = f"doc-{idx}"
        parts.append(f'<section id="{safe_anchor}">')
        parts.append(f"<h1>{html.escape(title)}</h1>")
        md_text = path.read_text(encoding="utf-8", errors="replace")
        parts.append(render_markdown(md_text))
        parts.append(f'<p style="color:#888;font-size:0.8em;margin-top:2em;"><em>Quelle: {html.escape(str(path))}</em></p>')
        parts.append('</section>')

    content = "\n".join(parts)
    return HTML_SHELL.format(title=html.escape(project_title), content=content)


def try_pandoc(html_path: Path, pdf_path: Path) -> bool:
    """Versucht HTML→PDF via pandoc. Gibt True bei Erfolg zurueck."""
    if not shutil.which("pandoc"):
        return False
    try:
        subprocess.run(
            ["pandoc", str(html_path), "-o", str(pdf_path), "--pdf-engine=wkhtmltopdf"],
            check=True,
            capture_output=True,
        )
        return True
    except Exception:
        # Versuch 2: ohne wkhtmltopdf (pandoc-eigener Default)
        try:
            subprocess.run(["pandoc", str(html_path), "-o", str(pdf_path)], check=True, capture_output=True)
            return True
        except Exception:
            return False


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("audit_dir", help="Pfad zu docs/legal-audit/ oder audits/<name>/")
    p.add_argument("--title", default=None, help="Projekt-Titel (default: Verzeichnisname)")
    args = p.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    audit_dir = Path(args.audit_dir).expanduser().resolve()
    if not audit_dir.exists():
        print(f"FEHLER: Verzeichnis nicht gefunden: {audit_dir}", file=sys.stderr)
        return 1

    title = args.title or audit_dir.name
    html_text = build_html(audit_dir, title)
    html_path = audit_dir / "anwalts-briefing.html"
    html_path.write_text(html_text, encoding="utf-8")
    print(f"HTML geschrieben: {html_path}")

    pdf_path = audit_dir / "anwalts-briefing.pdf"
    if try_pandoc(html_path, pdf_path):
        print(f"PDF geschrieben: {pdf_path}")
    else:
        print(
            "[Hinweis] pandoc nicht verfuegbar oder fehlgeschlagen. "
            "Oeffne anwalts-briefing.html im Browser und drucke als PDF "
            "(Ctrl+P → 'Als PDF speichern')."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
