#!/usr/bin/env python3
"""Add stable folios, metadata, and a checked outline to the v0.7 paper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


OUTLINE_TITLES = [
    "Abstract",
    "中文摘要",
    "Candidate status and additive lineage",
    "1. Three notions of persistent vanishing",
    "2. Primitive-amplitude support",
    "3. Exact zero-cycle classification",
    "4. Endpoint moments and the imported theorem",
    "5. Persistent endpoint moments for every q(P)≤3",
    "6. Laurent phases and arbitrary Laurent amplitudes",
    "7. Why the Laurent result stops here",
    "8. Exact computational checks",
    "9. Assurance boundary and open problems",
    "References",
    "Data and code availability",
    "Ethics declaration",
    "Author contributions (CRediT)",
    "Conflict of interest",
    "Funding",
    "AI disclosure",
]


def normalise(value: str) -> str:
    return " ".join(value.replace("≤", "≤").split()).casefold()


def find_page(document: fitz.Document, title: str) -> int | None:
    needle = normalise(title)
    if title.startswith("5. Persistent endpoint moments"):
        needle = normalise("5. Persistent endpoint moments for every")
    for page_index, page in enumerate(document):
        page_text = normalise(page.get_text("text"))
        if needle in page_text:
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
        footer = fitz.Rect(
            0, page.rect.height - 22, page.rect.width, page.rect.height - 8
        )
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
            "title": "Amplitude-Weighted Cyclicity and Laurent Moment Channels",
            "author": "Anonymous",
            "subject": "Public unrefereed theorem candidate, version 0.7.0-candidate",
            "keywords": "polynomial moments, Laurent moments, inverse-root support, cyclic rank, zero-cycles",
            "creator": "Evidence Press candidate workflow",
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
