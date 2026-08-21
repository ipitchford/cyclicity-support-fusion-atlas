#!/usr/bin/env python3
"""Freeze, verify, archive, and bind the additive v0.6 candidate release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from pdf_tex_preflight import validate_pdf


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.6.0-candidate"
DATE = "2026-08-21"
MANIFEST = ROOT / "MANIFEST.sha256"
RECEIPT = ROOT / "receipts" / "all_degree_release_receipt.json"
EXCLUDED_RELATIVE = {
    "GLOBAL_PUBLICATION_STATE.json",
    "MANIFEST.sha256",
    "receipts/all_degree_archive_receipt.json",
}
EXCLUDED_PARTS = {".git", ".pytest_cache", "__pycache__", "node_modules"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


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
        if Path(relative).is_absolute() or ".." in Path(relative).parts or relative in entries:
            raise ValueError(f"unsafe or duplicate manifest path: {relative}")
        entries[relative] = digest
    return entries


def verify() -> dict[str, str]:
    entries = parse_manifest()
    actual = release_files()
    if set(entries) != actual:
        raise ValueError(
            f"release manifest coverage mismatch: unlisted={sorted(actual-set(entries))}, "
            f"stale={sorted(set(entries)-actual)}"
        )
    for relative, expected in entries.items():
        path = ROOT / relative
        if sha256(path) != expected:
            raise ValueError(f"release manifest digest mismatch: {relative}")
    return entries


def write_receipt() -> None:
    global_receipt = json.loads((ROOT / "receipts/global_completion_receipt.json").read_text())
    kummer_receipt = json.loads((ROOT / "receipts/kummer_normalizer_receipt.json").read_text())
    result = {
        "schema": "cyclicity-all-degree-release-receipt-v1",
        "version": VERSION,
        "date": DATE,
        "status": "pass-for-public-unrefereed-candidate-release",
        "documents": {
            "source_front_matter_sha256": sha256(ROOT / "ALL_DEGREE_RELEASE.md"),
            "proof_note_sha256": sha256(ROOT / "ALL_DEGREE_GLOBAL_COMPLETION.md"),
            "back_matter_sha256": sha256(ROOT / "ALL_DEGREE_RELEASE_BACK_MATTER.md"),
            "html_sha256": sha256(ROOT / "All-Degree-Low-Rank-Coefficient-Atlas.html"),
            "pdf_sha256": sha256(ROOT / "All-Degree-Low-Rank-Coefficient-Atlas.pdf"),
        },
        "verification": {
            "global_receipt_schema": global_receipt["schema"],
            "global_receipt_sha256": global_receipt["receipt_sha256"],
            "global_receipt_file_sha256": sha256(ROOT / "receipts/global_completion_receipt.json"),
            "global_manifest_sha256": sha256(ROOT / "GLOBAL_COMPLETION_MANIFEST.sha256"),
            "kummer_receipt_schema": kummer_receipt["schema"],
            "kummer_receipt_sha256": kummer_receipt["receipt_sha256"],
            "parent_v0_5_manifest_sha256": sha256(ROOT / "PARENT_v0.5.0_MANIFEST.sha256"),
            "main_replay": "python3 run_global_completion_checks.py",
            "normal_optimized_parity": True,
            "global_mutation_count_per_mode": 13,
        },
        "claim_status": {
            "all_degree_low_rank_classification": "proved-in-unrefereed-candidate-relative-to-named-imports",
            "rank_preserving_extensions": "proved-in-unrefereed-candidate-relative-to-named-imports",
            "complete_formalization": False,
            "external_independent_reproduction": False,
            "specialist_peer_review": False,
            "novelty_priority_certified": False,
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
            "version_doi": "10.5281/zenodo.22045144",
            "concept_doi": "10.5281/zenodo.22036029",
        },
    }
    result["receipt_sha256"] = canonical_hash(result)
    RECEIPT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def freeze() -> None:
    validate_pdf(ROOT / "All-Degree-Low-Rank-Coefficient-Atlas.pdf")
    write_receipt()
    paths = sorted(release_files())
    MANIFEST.write_text("".join(f"{sha256(ROOT/relative)}  {relative}\n" for relative in paths))
    verify()
    print(
        json.dumps(
            {
                "status": "frozen",
                "files": len(paths),
                "manifest_sha256": sha256(MANIFEST),
                "receipt_sha256": json.loads(RECEIPT.read_text())["receipt_sha256"],
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
        for relative in sorted(set(entries) | {"MANIFEST.sha256"}):
            source = ROOT / relative
            info = zipfile.ZipInfo(f"{prefix}/{relative}", fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100755 if source.stat().st_mode & 0o111 else 0o100644) << 16
            bundle.writestr(info, source.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(output) as bundle:
        bad = bundle.testzip()
        if bad is not None:
            raise RuntimeError(f"archive CRC failure: {bad}")
        members = len(bundle.infolist())
    print(json.dumps({"archive": str(output), "files": members, "bytes": output.stat().st_size, "sha256": sha256(output)}, indent=2))


def bind_archive(archive_path: Path, output: Path) -> None:
    verify()
    release_receipt = json.loads(RECEIPT.read_text())
    record = {
        "schema": "cyclicity-all-degree-archive-binding-v1",
        "version": VERSION,
        "date": DATE,
        "archive": archive_path.name,
        "archive_size_bytes": archive_path.stat().st_size,
        "archive_sha256": sha256(archive_path),
        "manifest_sha256": sha256(MANIFEST),
        "release_receipt_sha256": release_receipt["receipt_sha256"],
        "pdf_sha256": release_receipt["documents"]["pdf_sha256"],
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
        print(f"v0.6 release manifest verified: {len(entries)} files")
    elif args.command == "archive":
        archive(args.output)
    else:
        bind_archive(args.archive, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
