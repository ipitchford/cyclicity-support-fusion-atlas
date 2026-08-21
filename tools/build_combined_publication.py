#!/usr/bin/env python3
"""Freeze, verify, archive, and bind the combined v0.7 candidate release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from pdf_tex_preflight import validate_pdf


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.7.0-candidate"
DATE = "2026-08-21"
VERSION_DOI = "10.5281/zenodo.22049564"
CONCEPT_DOI = "10.5281/zenodo.22036029"
MANIFEST = ROOT / "MANIFEST_v0.7.0.sha256"
RECEIPT = ROOT / "receipts" / "combined_publication_receipt.json"
EXCLUDED_RELATIVE = {
    "GLOBAL_PUBLICATION_STATE.json",
    "MANIFEST_v0.7.0.sha256",
    "receipts/combined_archive_receipt.json",
}
EXCLUDED_PARTS = {".git", ".pytest_cache", "__pycache__", "node_modules"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def release_files() -> set[str]:
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in EXCLUDED_RELATIVE:
            continue
        if any(part in EXCLUDED_PARTS for part in Path(relative).parts):
            continue
        files.add(relative)
    return files


def parse_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line_number, line in enumerate(MANIFEST.read_text().splitlines(), 1):
        try:
            digest, relative = line.split("  ", 1)
        except ValueError as exc:
            raise ValueError(f"malformed manifest line {line_number}") from exc
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise ValueError(f"invalid digest on manifest line {line_number}")
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError(f"unsafe manifest path: {relative}")
        if relative in entries:
            raise ValueError(f"duplicate manifest path: {relative}")
        entries[relative] = digest
    return entries


def verify() -> dict[str, str]:
    entries = parse_manifest()
    actual = release_files()
    if set(entries) != actual:
        raise ValueError(
            "release manifest coverage mismatch: "
            f"unlisted={sorted(actual - set(entries))}, "
            f"stale={sorted(set(entries) - actual)}"
        )
    for relative, expected in entries.items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"release manifest digest mismatch: {relative}")
    return entries


def write_receipt() -> None:
    global_receipt = json.loads(
        (ROOT / "receipts/global_completion_receipt.json").read_text()
    )
    amplitude_receipt = json.loads(
        (ROOT / "receipts/amplitude_laurent_test_receipt.json").read_text()
    )
    result = {
        "schema": "cyclicity-combined-publication-receipt-v1",
        "version": VERSION,
        "date": DATE,
        "status": "pass-for-public-unrefereed-candidate-release",
        "documents": {
            "front_matter_sha256": sha256(ROOT / "COMBINED_RELEASE_FRONT.md"),
            "fixed_seed_body_sha256": sha256(ROOT / "COMBINED_GLOBAL_COMPLETION.md"),
            "extension_body_sha256": sha256(ROOT / "COMBINED_AMPLITUDE_LAURENT.md"),
            "back_matter_sha256": sha256(ROOT / "COMBINED_RELEASE_BACK.md"),
            "html_sha256": sha256(
                ROOT / "Inverse-Root-Support-Amplitudes-and-Laurent-Moments.html"
            ),
            "pdf_sha256": sha256(
                ROOT / "Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf"
            ),
            "pdf_pages": 25,
        },
        "verification": {
            "combined_manifest_sha256": sha256(ROOT / "COMBINED_MANIFEST.sha256"),
            "global_receipt_schema": global_receipt["schema"],
            "global_receipt_sha256": global_receipt["receipt_sha256"],
            "amplitude_receipt_schema": amplitude_receipt["schema"],
            "amplitude_receipt_file_sha256": sha256(
                ROOT / "receipts/amplitude_laurent_test_receipt.json"
            ),
            "global_replay": "python3 run_global_completion_checks.py",
            "amplitude_laurent_replay": "python3 run_amplitude_laurent_checks.py",
            "document_gate": "python3 tools/check_combined_release.py",
            "normal_optimized_parity": True,
            "deterministic_document_bytes": True,
        },
        "claim_status": {
            "fixed_seed_all_degree_atlas": "unrefereed-candidate-relative-to-named-imports",
            "rank_preserving_extensions": "unrefereed-candidate-relative-to-named-imports",
            "polynomial_amplitudes": "unrefereed-theorem-candidate",
            "specified_zero_cycles": "unrefereed-theorem-candidate",
            "endpoint_moments_q_at_most_three": "conditional-unrefereed-theorem-candidate",
            "laurent_local_channel": "unrefereed-theorem-candidate",
            "finite_all_laurent_atlas": False,
            "external_independent_reproduction": False,
            "specialist_peer_review": False,
            "priority_certified": False,
        },
        "creator": "Anonymous",
        "licensing": {
            "original_research_text_and_data": "CC0-1.0",
            "original_code_and_tests": "MIT",
            "third_party_material": "existing terms or NOASSERTION",
        },
        "identifiers": {
            "repository": "https://github.com/ipitchford/cyclicity-support-fusion-atlas",
            "evidence_press": "https://evidencepress.org/releases/cyclicity-support-fusion-atlas/",
            "version_doi": VERSION_DOI,
            "concept_doi": CONCEPT_DOI,
            "previous_version_doi": "10.5281/zenodo.22045144",
        },
    }
    result["receipt_sha256"] = canonical_hash(result)
    RECEIPT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def freeze() -> None:
    validate_pdf(ROOT / "Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf")
    write_receipt()
    paths = sorted(release_files())
    MANIFEST.write_text(
        "".join(f"{sha256(ROOT / relative)}  {relative}\n" for relative in paths)
    )
    verify()
    receipt = json.loads(RECEIPT.read_text())
    print(
        json.dumps(
            {
                "status": "frozen",
                "files": len(paths),
                "manifest_sha256": sha256(MANIFEST),
                "receipt_sha256": receipt["receipt_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )


def archive(output: Path) -> None:
    entries = verify()
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = f"cyclicity-support-fusion-atlas-v{VERSION}"
    fixed_time = (2026, 8, 21, 0, 0, 0)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative in sorted(set(entries) | {MANIFEST.name}):
            source = ROOT / relative
            info = zipfile.ZipInfo(f"{prefix}/{relative}", fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o100755 if source.stat().st_mode & 0o111 else 0o100644
            info.external_attr = mode << 16
            bundle.writestr(info, source.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(output) as bundle:
        bad_member = bundle.testzip()
        if bad_member is not None:
            raise RuntimeError(f"archive CRC failure: {bad_member}")
        members = len(bundle.infolist())
    print(
        json.dumps(
            {
                "archive": str(output),
                "files": members,
                "bytes": output.stat().st_size,
                "sha256": sha256(output),
            },
            indent=2,
            sort_keys=True,
        )
    )


def bind_archive(archive_path: Path, output: Path) -> None:
    verify()
    release_receipt = json.loads(RECEIPT.read_text())
    record = {
        "schema": "cyclicity-combined-archive-binding-v1",
        "version": VERSION,
        "date": DATE,
        "archive": archive_path.name,
        "archive_size_bytes": archive_path.stat().st_size,
        "archive_sha256": sha256(archive_path),
        "manifest_sha256": sha256(MANIFEST),
        "release_receipt_sha256": release_receipt["receipt_sha256"],
        "pdf_sha256": release_receipt["documents"]["pdf_sha256"],
        "version_doi": VERSION_DOI,
        "status": "archive-bound",
    }
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("freeze")
    subparsers.add_parser("verify")
    archive_parser = subparsers.add_parser("archive")
    archive_parser.add_argument("output", type=Path)
    bind_parser = subparsers.add_parser("bind-archive")
    bind_parser.add_argument("archive", type=Path)
    bind_parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        freeze()
    elif args.command == "verify":
        entries = verify()
        print(f"v0.7 combined release manifest verified: {len(entries)} files")
    elif args.command == "archive":
        archive(args.output)
    else:
        bind_archive(args.archive, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
