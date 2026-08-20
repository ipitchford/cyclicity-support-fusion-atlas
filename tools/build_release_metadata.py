#!/usr/bin/env python3
"""Freeze the payload/manifest layers or bind a completed release archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
VERIFICATION = ROOT / "verification"
sys.path.insert(0, str(VERIFICATION))

from integrity import package_files, sha256_path, verify_manifest  # noqa: E402


RECEIPT = VERIFICATION / "CURRENT_TARGET_RECEIPT.json"
MANIFEST = ROOT / "MANIFEST.sha256"
PAYLOAD_EXCLUSIONS = {
    "MANIFEST.sha256",
    "verification/CURRENT_TARGET_RECEIPT.json",
}


def canonical_lines(paths: list[str]) -> list[str]:
    return [f"{sha256_path(ROOT / relative)}  {relative}\n" for relative in paths]


def freeze() -> None:
    payload_paths = sorted(package_files(ROOT) - PAYLOAD_EXCLUSIONS)
    payload_lines = canonical_lines(payload_paths)
    payload_root = hashlib.sha256("".join(payload_lines).encode("utf-8")).hexdigest()

    expectations = json.loads((ROOT / "RELEASE_EXPECTATIONS.json").read_text())
    receipt = {
        "schema": "cyclicity-current-target-receipt-v1",
        "version": "0.5.0-candidate",
        "date": "2026-08-20",
        "target": {
            "identity": "sha256 of sorted '<file sha256><two spaces><relative path><newline>' records",
            "payload_content_root_sha256": payload_root,
            "payload_file_count": len(payload_paths),
            "excluded_from_content_root": sorted(PAYLOAD_EXCLUSIONS),
        },
        "claim_status": {
            "T1-T6": "proved-in-unrefereed-candidate",
            "F1": "finite-computer-assisted-theorem-candidate-through-degree-20",
            "C1": "conjecture-all-degrees",
            "A1": "generic-corollary",
            "D1-D2": "exploratory-non-gated",
        },
        "release_gate": {
            "command": "python3 run_core_checks.py",
            "required_modes": ["ordinary Python", "python -O"],
            "atlas_cases": 1152,
            "fail_closed_on": ["anomaly", "missing certificate", "digest mismatch", "unlisted file"],
        },
        "frozen_receipts": {
            "exact_rank_receipt_sha256": expectations["exact_rank_receipt_sha256"],
            "atlas_case_records_sha256": expectations["atlas_case_records_sha256"],
        },
        "documents": {
            "manuscript_sha256": sha256_path(ROOT / "MANUSCRIPT.md"),
            "pdf_sha256": sha256_path(ROOT / "Inverse-Root-Support-and-Fourier-Fusion.pdf"),
            "docx_sha256": sha256_path(ROOT / "Inverse-Root-Support-and-Fourier-Fusion.docx"),
            "html_sha256": sha256_path(ROOT / "Inverse-Root-Support-and-Fourier-Fusion.html"),
        },
        "lineage": [
            {
                "id": "EP1",
                "url": "https://evidencepress.org/releases/cyclicity-loci-exponential-periods/",
                "doi": "10.5281/zenodo.21853682",
            },
            {
                "id": "EP2",
                "url": "https://evidencepress.org/releases/cyclicity-root-span-low-rank/",
                "doi": "10.5281/zenodo.21864884",
            },
        ],
        "assurance_ceiling": [
            "no unaffiliated specialist review",
            "no proof-assistant formalisation",
            "no second-CAS replay of the complete atlas",
            "all-degree atlas remains open",
        ],
        "status": "pass-with-notes-for-specialist-circulation",
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")

    manifest_paths = sorted(package_files(ROOT))
    MANIFEST.write_text("".join(canonical_lines(manifest_paths)))
    verify_manifest(ROOT, MANIFEST, require_complete=True)
    print(
        json.dumps(
            {
                "payload_content_root_sha256": payload_root,
                "payload_file_count": len(payload_paths),
                "manifest_sha256": sha256_path(MANIFEST),
                "manifest_file_count": len(manifest_paths),
                "current_target_receipt_sha256": sha256_path(RECEIPT),
            },
            indent=2,
        )
    )


def archive_receipt(archive: Path, output: Path) -> None:
    verify_manifest(ROOT, MANIFEST, require_complete=True)
    receipt = json.loads(RECEIPT.read_text())
    record = {
        "schema": "cyclicity-archive-binding-receipt-v1",
        "version": "0.5.0-candidate",
        "date": "2026-08-20",
        "archive": archive.name,
        "archive_size_bytes": archive.stat().st_size,
        "archive_sha256": sha256_path(archive),
        "manifest_sha256": sha256_path(MANIFEST),
        "current_target_receipt_sha256": sha256_path(RECEIPT),
        "payload_content_root_sha256": receipt["target"]["payload_content_root_sha256"],
        "pdf_sha256": sha256_path(ROOT / "Inverse-Root-Support-and-Fourier-Fusion.pdf"),
        "status": "archive-bound",
    }
    output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("freeze", help="write the current-target receipt and complete manifest")
    archive_parser = subparsers.add_parser("archive-receipt", help="bind an existing ZIP archive")
    archive_parser.add_argument("archive", type=Path)
    archive_parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.command == "freeze":
        freeze()
    else:
        archive_receipt(args.archive, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
