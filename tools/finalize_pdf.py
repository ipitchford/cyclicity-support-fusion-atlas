#!/usr/bin/env python3
"""Add stable folios and a navigable outline to the rendered paper PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


OUTLINE_TITLES = [
    "Abstract",
    "中文摘要",
    "1. Claim boundary and relation to the parent releases",
    "2. Algebraic setup and affine normalisation",
    "3. The inverse-at-infinity support",
    "4. A direct formal moment transform",
    "5. The unconditional fixed-seed rank theorem",
    "6. Equality with the reduced inverse-root span",
    "7. Explicit analytic realisation without a moving-cycle gap",
    "8. Block spans for a polynomial decomposition",
    "9. All complete decompositions and Ritt moves",
    "10. Complete low-rank fusion profiles",
    "11. The generating Ritt collision",
    "12. Exact finite computation",
    "13. Affine coefficient atlas through degree twenty",
    "14. Consequences and research directions",
    "15. Theorem-level relation to prior work",
    "16. Assurance, novelty, and remaining work",
    "17. Reproducibility",
    "Data and code availability",
    "Ethics declaration",
    "Author contributions (CRediT)",
    "Conflict of interest",
    "Funding",
    "AI disclosure",
    "References",
]


def find_page(document: fitz.Document, title: str) -> int | None:
    needle = " ".join(title.split()).casefold()
    minimum_index = 0 if title in {"Abstract", "中文摘要"} else 2
    for page_index in range(document.page_count - 1, minimum_index - 1, -1):
        lines = {
            " ".join(line.split()).casefold()
            for line in document[page_index].get_text("text").splitlines()
        }
        if needle in lines:
            return page_index + 1
    for page_index in range(document.page_count - 1, minimum_index - 1, -1):
        page = document[page_index]
        haystack = " ".join(page.get_text("text").split()).casefold()
        if needle in haystack:
            return page_index + 1
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()

    if args.input_pdf.resolve() == args.output_pdf.resolve():
        raise SystemExit("input and output PDF paths must differ")

    document = fitz.open(args.input_pdf)
    for page_number, page in enumerate(document, start=1):
        footer = fitz.Rect(0, page.rect.height - 22, page.rect.width, page.rect.height - 8)
        page.insert_textbox(
            footer,
            str(page_number),
            fontsize=8,
            fontname="helv",
            color=(0.31, 0.37, 0.42),
            align=fitz.TEXT_ALIGN_CENTER,
            overlay=True,
        )

    outline: list[list[int | str]] = []
    missing: list[str] = []
    for title in OUTLINE_TITLES:
        page_number = find_page(document, title)
        if page_number is None:
            missing.append(title)
            continue
        level = 1
        outline.append([level, title, page_number])

    document.set_toc(outline)
    metadata = document.metadata
    metadata.update(
        {
            "title": "Inverse-Root Support and Fourier Fusion for Polynomial Exponential Periods",
            "author": "Anonymous",
            "subject": "Unrefereed theorem candidate, version 0.5.0",
            "keywords": "polynomial decomposition, cyclic vectors, inverse roots, Fourier support, Ritt theory",
        }
    )
    document.set_metadata(metadata)
    document.save(args.output_pdf, garbage=4, deflate=True, clean=True)
    document.close()

    print(
        json.dumps(
            {
                "pages": len(fitz.open(args.output_pdf)),
                "bookmarks": len(outline),
                "missing_bookmarks": missing,
                "output": str(args.output_pdf),
            },
            indent=2,
        )
    )
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
