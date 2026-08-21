#!/usr/bin/env python3
"""Render the v0.6 paper and remove WeasyPrint-visible MathML TeX annotations."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from pdf_tex_preflight import validate_pdf


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "All-Degree-Low-Rank-Coefficient-Atlas.html"
PDF = ROOT / "All-Degree-Low-Rank-Coefficient-Atlas.pdf"
SOURCES = [
    ROOT / "ALL_DEGREE_RELEASE.md",
    ROOT / "ALL_DEGREE_GLOBAL_COMPLETION.md",
    ROOT / "ALL_DEGREE_RELEASE_BACK_MATTER.md",
]


def run(argv: list[str]) -> None:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(argv)}\n{completed.stdout}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="all-degree-paper-") as directory:
        temporary = Path(directory)
        raw_html = temporary / "paper-with-tex-spans.html"
        static_html = temporary / "paper-static-katex.html"
        draft_pdf = temporary / "paper-draft.pdf"
        run(
            [
                "pandoc",
                "--standalone",
                "--from=markdown+tex_math_dollars+tex_math_single_backslash+raw_html",
                "--to=html5",
                "--katex",
                "--css=paper.css",
                "--css=all-degree-paper.css",
                *[str(path) for path in SOURCES],
                "--output",
                str(raw_html),
            ]
        )
        run(
            [
                "node",
                str(ROOT / "tools" / "render_static_katex.js"),
                str(raw_html),
                str(static_html),
            ]
        )
        rendered = static_html.read_text()
        if "<annotation" in rendered or "application/x-tex" in rendered:
            raise RuntimeError("static KaTeX output retained a TeX annotation")
        HTML.write_text(rendered)
        run(["weasyprint", str(HTML), str(draft_pdf)])
        run(
            [
                sys.executable,
                str(ROOT / "tools" / "finalize_all_degree_pdf.py"),
                str(draft_pdf),
                str(PDF),
            ]
        )
    preflight = validate_pdf(PDF)
    print(
        json.dumps(
            {
                "status": "pass",
                "html": str(HTML),
                "pdf": str(PDF),
                "static_math_renderer": "KaTeX 0.18.4",
                "raw_tex_findings": preflight["raw_tex_findings"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
