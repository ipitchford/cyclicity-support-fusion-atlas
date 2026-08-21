#!/usr/bin/env python3
"""Fail-closed integrity checks for the combined v0.7 candidate release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import fitz

from build_combined_sources import derive_amplitude, derive_global
from pdf_tex_preflight import extract_text, validate_pdf


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf"
HTML = ROOT / "Inverse-Root-Support-Amplitudes-and-Laurent-Moments.html"
GLOBAL = ROOT / "COMBINED_GLOBAL_COMPLETION.md"
AMPLITUDE = ROOT / "COMBINED_AMPLITUDE_LAURENT.md"
FRONT = ROOT / "COMBINED_RELEASE_FRONT.md"
BACK = ROOT / "COMBINED_RELEASE_BACK.md"
CLAIMS = ROOT / "CLAIMS_COMBINED.json"
MANIFEST = ROOT / "COMBINED_MANIFEST.sha256"

EXPECTED_CITATIONS = {
    "ABM13",
    "BK16",
    "BKN26",
    "C25",
    "MZ08",
    "P13",
    "PM09",
    "PPZ10",
}
EXPECTED_PREDECESSORS = {
    "Inverse-Root-Support-and-Fourier-Fusion.pdf":
        "e56b4d2a9000a89174b5e3a580ff44c330a83232a9c40333976b917147aa1479",
    "All-Degree-Low-Rank-Coefficient-Atlas.pdf":
        "b0cc6d997a3f74777e522c667840d8bb2c32afd3d2ff699e0d7023db9a65d74a",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_generated_sources() -> dict[str, object]:
    require(GLOBAL.read_text(encoding="utf-8") == derive_global(),
            "combined global source is stale or manually edited")
    require(AMPLITUDE.read_text(encoding="utf-8") == derive_amplitude(),
            "combined amplitude source is stale or manually edited")
    combined = GLOBAL.read_text(encoding="utf-8") + AMPLITUDE.read_text(
        encoding="utf-8"
    )
    sections = [
        int(value)
        for value in re.findall(r"(?m)^# (\d+)\.", combined)
    ]
    require(sections == list(range(1, 22)),
            f"section numbering is not exactly 1 through 21: {sections}")
    code_spans = re.findall(r"`([^`\n]+)`", combined)
    require(
        sorted(set(code_spans)) == ["ALL_DEGREE_STRUCTURAL_REPAIR.md", "mullerthm"],
        f"unexpected inherited code spans remain: {sorted(set(code_spans))}",
    )
    require("[EP3" not in combined, "stale companion self-citation remains")
    require("MANUSCRIPT.md" not in combined, "stale manuscript dependency remains")
    return {"sections": len(sections), "allowed_code_spans": len(code_spans)}


def check_citations() -> dict[str, object]:
    back = BACK.read_text(encoding="utf-8")
    pre_references, _, references = back.partition("# References")
    body = "\n".join(
        [
            FRONT.read_text(encoding="utf-8"),
            GLOBAL.read_text(encoding="utf-8"),
            AMPLITUDE.read_text(encoding="utf-8"),
            pre_references,
        ]
    )
    citations = set(re.findall(r"\[([A-Z][A-Z0-9]{1,8}\d*)\]", body))
    definitions = set(re.findall(r"(?m)^\*\*\[([^]]+)\]\*\*", references))
    require(citations == EXPECTED_CITATIONS,
            f"citation set differs from expected set: {sorted(citations)}")
    require(definitions == citations,
            f"citation definitions do not close: used={sorted(citations)}, definitions={sorted(definitions)}")
    return {"citations": len(citations), "definitions": len(definitions)}


def check_claims_and_anchors() -> dict[str, object]:
    ledger = json.loads(CLAIMS.read_text(encoding="utf-8"))
    require(ledger["version"] == "0.7.0-candidate", "claim-ledger version drift")
    claim_ids = [claim["id"] for claim in ledger["claims"]]
    require(len(claim_ids) == len(set(claim_ids)), "duplicate claim IDs")
    require(len(claim_ids) == 12, f"expected 12 combined claims, found {len(claim_ids)}")
    html_ids = set(re.findall(r'\bid="([^"]+)"', HTML.read_text(encoding="utf-8")))
    checked_anchors = 0
    for claim in ledger["claims"]:
        for basis in claim.get("basis", []):
            path_text, separator, anchor = basis.partition("#")
            path = ROOT / path_text
            require(path.is_file(), f"claim basis does not exist: {basis}")
            if separator:
                require(anchor in html_ids, f"claim HTML anchor does not exist: {basis}")
                checked_anchors += 1
    statuses = {claim["status"] for claim in ledger["claims"]}
    require(
        statuses == {"theorem_candidate", "conditional_theorem_candidate", "not_claimed"},
        f"unexpected claim statuses: {sorted(statuses)}",
    )
    return {"claims": len(claim_ids), "anchors": checked_anchors}


def check_pdf() -> dict[str, object]:
    validate_pdf(PDF)
    completed = subprocess.run(
        ["qpdf", "--check", str(PDF)],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    require(completed.returncode == 0, f"qpdf failed: {completed.stdout}")
    with fitz.open(PDF) as document:
        require(document.page_count == 25, f"expected 25 pages, found {document.page_count}")
        first_page = document[0].rect
        require(abs(first_page.width - 595.276) < 0.1, "PDF width is not A4")
        require(abs(first_page.height - 841.89) < 0.1, "PDF height is not A4")
        metadata = document.metadata
        require(metadata.get("title", "").startswith("Inverse-Root Support"),
                "PDF title metadata missing")
        require("unrefereed theorem candidate" in metadata.get("subject", ""),
                "PDF assurance subject metadata missing")
        bookmarks = document.get_toc(simple=True)
        require(len(bookmarks) == 36, f"expected 36 bookmarks, found {len(bookmarks)}")
    text = extract_text(PDF)
    legacy_tokens = sorted(
        token for token in ("!=", ">=", "<=", "\\qquad", "\\tag{") if token in text
    )
    require(not legacy_tokens, f"legacy source notation exposed in PDF: {legacy_tokens}")
    words = len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))
    require(6500 <= words <= 9000, f"unexpected extracted word count: {words}")
    return {"pages": 25, "bookmarks": 36, "extracted_words": words}


def check_predecessors() -> dict[str, object]:
    for filename, expected in EXPECTED_PREDECESSORS.items():
        path = ROOT / filename
        require(path.is_file(), f"predecessor artifact missing: {filename}")
        actual = sha256(path)
        require(actual == expected,
                f"predecessor artifact changed: {filename}: {actual}")
    return {"preserved_predecessors": len(EXPECTED_PREDECESSORS)}


def check_manifest_if_present() -> dict[str, object]:
    if not MANIFEST.is_file():
        return {"manifest": "not yet present"}
    completed = subprocess.run(
        ["shasum", "-a", "256", "-c", MANIFEST.name],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    require(completed.returncode == 0, f"combined manifest failed:\n{completed.stdout}")
    passed = completed.stdout.count(": OK")
    return {"manifest": "pass", "manifest_files": passed}


def main() -> int:
    checks = {
        "generated_sources": check_generated_sources(),
        "citations": check_citations(),
        "claims": check_claims_and_anchors(),
        "pdf": check_pdf(),
        "predecessors": check_predecessors(),
        "manifest": check_manifest_if_present(),
    }
    print(json.dumps({"status": "pass", "checks": checks}, indent=2, sort_keys=True))
    print("COMBINED RELEASE INTEGRITY GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
