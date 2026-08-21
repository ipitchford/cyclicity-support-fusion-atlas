#!/usr/bin/env python3
"""Fail closed when a rendered PDF exposes raw TeX control syntax."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


CONTROL_PATTERN = re.compile(
    r"\\(?:begin|end|frac|dfrac|tfrac|tag|mapsto|langle|rangle|mathbf|mathbb|"
    r"mathcal|operatorname|boxed|square|qquad|quad|sum|prod|zeta|Gamma|Delta|Sigma|"
    r"alpha|beta|gamma|delta|epsilon|lambda|mu|omega|circ|text)(?![A-Za-z])"
)
DELIMITER_PATTERN = re.compile(r"(?:\\\[|\\\]|\$\$)")


def find_raw_tex(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        matches = sorted(
            {match.group(0) for pattern in (CONTROL_PATTERN, DELIMITER_PATTERN) for match in pattern.finditer(line)}
        )
        if matches:
            findings.append(
                {
                    "line": line_number,
                    "tokens": matches,
                    "context": line[:240],
                }
            )
    return findings


def extract_text(pdf: Path) -> str:
    with tempfile.TemporaryDirectory(prefix="pdf-tex-preflight-") as directory:
        output = Path(directory) / "text.txt"
        completed = subprocess.run(
            ["pdftotext", "-layout", str(pdf), str(output)],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"pdftotext failed ({completed.returncode}): {completed.stdout}")
        return output.read_text(errors="replace")


def validate_pdf(pdf: Path) -> dict[str, object]:
    if not pdf.is_file():
        raise FileNotFoundError(pdf)
    text = extract_text(pdf)
    findings = find_raw_tex(text)
    if findings:
        preview = json.dumps(findings[:10], ensure_ascii=False)
        raise ValueError(f"raw TeX detected in rendered PDF: {preview}")
    return {
        "status": "pass",
        "pdf": str(pdf),
        "characters_scanned": len(text),
        "raw_tex_findings": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    try:
        result = validate_pdf(args.pdf)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"PDF TEX PREFLIGHT FAIL: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
