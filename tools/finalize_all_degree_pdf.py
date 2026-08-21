#!/usr/bin/env python3
"""Add stable folios, metadata, and a navigable outline to the v0.6 paper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


OUTLINE_TITLES = [
    "Abstract",
    "中文摘要",
    "Candidate status and correction record",
    "Reproducibility and assurance map",
    "1. Purpose and assurance boundary",
    "2. The inherited root-span interface",
    "3. Finite-pole and infinity-order descent",
    "4. A stable line and the first rank increase",
    "5. Source-exact primitive-factor audit",
    "6. The full-block kernel lemma",
    "7. Rank-preserving extensions in ranks one and two",
    "8. Rank-three cubic-over-power extensions",
    "9. Rank-three quartic extensions",
    "10. Completion of the first-increase cases",
    "11. All-degree theorem",
    "12. What is and is not closed",
    "Sources used for imported classification steps",
    "Data and code availability",
    "Limitations",
    "Ethics declaration",
    "Author contributions (CRediT)",
    "Conflict of interest",
    "Funding",
    "AI disclosure",
    "Citation",
]


def find_page(document: fitz.Document, title: str) -> int | None:
    needle = " ".join(title.split()).casefold()
    for page_index, page in enumerate(document):
        lines = {
            " ".join(line.split()).casefold()
            for line in page.get_text("text").splitlines()
        }
        if needle in lines:
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
        else:
            outline.append([1, title, page_number])
    document.set_toc(outline)
    document.set_metadata(
        {
            "title": "Inverse-Root Support and Fourier Fusion for Polynomial Exponential Periods: All-Degree Low-Rank Completion",
            "author": "Anonymous",
            "subject": "Public unrefereed theorem candidate, version 0.6.0-candidate",
            "keywords": "polynomial exponential periods, inverse-root support, cyclic rank, Ritt theory, Dickson polynomials, Kummer theory",
            "creator": "Evidence Press publication workflow",
        }
    )
    document.save(args.output_pdf, garbage=4, deflate=True, clean=True)
    pages = document.page_count
    document.close()
    print(
        json.dumps(
            {
                "pages": pages,
                "bookmarks": len(outline),
                "missing_bookmarks": missing,
                "output": str(args.output_pdf),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())

