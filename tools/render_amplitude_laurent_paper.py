#!/usr/bin/env python3
"""Render and fail-closed preflight the additive v0.7 amplitude paper."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from pdf_tex_preflight import validate_pdf


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "AMPLITUDE_LAURENT_EXTENSION.md"
HTML = ROOT / "Amplitude-Weighted-Cyclicity-and-Laurent-Moment-Channels.html"
PDF = ROOT / "Amplitude-Weighted-Cyclicity-and-Laurent-Moment-Channels.pdf"
PDF_ID_PATTERN = re.compile(
    rb"/ID\s*\[\s*<([0-9A-Fa-f]{32})>\s*<([0-9A-Fa-f]{32})>\s*\]"
)


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
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(argv)}\n"
            f"{completed.stdout}"
        )


def normalise_pdf_identifier(pdf: Path) -> str:
    """Replace both trailer IDs by a deterministic content-derived value.

    The hexadecimal fields retain their exact byte length, so cross-reference
    offsets do not change. qpdf validates the result immediately afterwards.
    """

    payload = pdf.read_bytes()
    matches = list(PDF_ID_PATTERN.finditer(payload))
    if len(matches) != 1:
        raise RuntimeError(f"expected one PDF trailer ID, found {len(matches)}")
    zero_id = b"0" * 32
    canonical = PDF_ID_PATTERN.sub(
        b"/ID [<" + zero_id + b"><" + zero_id + b">]", payload
    )
    identifier = hashlib.sha256(canonical).hexdigest()[:32].upper().encode("ascii")
    deterministic = PDF_ID_PATTERN.sub(
        b"/ID [<" + identifier + b"><" + identifier + b">]", payload
    )
    if len(deterministic) != len(payload):
        raise RuntimeError("PDF identifier normalisation changed file length")
    pdf.write_bytes(deterministic)
    return identifier.decode("ascii")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="amplitude-laurent-paper-") as directory:
        temporary = Path(directory)
        raw_html = temporary / "paper-with-tex-spans.html"
        static_html = temporary / "paper-static-katex.html"
        draft_pdf = temporary / "paper-draft.pdf"
        finalised_pdf = temporary / "paper-finalised.pdf"
        run(
            [
                "pandoc",
                "--standalone",
                "--from=markdown+tex_math_dollars+tex_math_single_backslash+raw_html",
                "--to=html5",
                "--katex",
                "--css=paper.css",
                "--css=amplitude-laurent-paper.css",
                str(SOURCE),
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
        rendered = static_html.read_text(encoding="utf-8")
        if "<annotation" in rendered or "application/x-tex" in rendered:
            raise RuntimeError("static KaTeX output retained a TeX annotation")
        HTML.write_text(rendered, encoding="utf-8")
        run(["weasyprint", str(HTML), str(draft_pdf)])
        run(
            [
                sys.executable,
                str(ROOT / "tools" / "finalize_amplitude_laurent_pdf.py"),
                str(draft_pdf),
                str(finalised_pdf),
            ]
        )
        run(["qpdf", "--deterministic-id", str(finalised_pdf), str(PDF)])
        pdf_identifier = normalise_pdf_identifier(PDF)
        run(["qpdf", "--check", str(PDF)])
    preflight = validate_pdf(PDF)
    print(
        json.dumps(
            {
                "status": "pass",
                "html": str(HTML),
                "pdf": str(PDF),
                "pdf_identifier": pdf_identifier,
                "raw_tex_findings": preflight["raw_tex_findings"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
