#!/usr/bin/env python3
"""Freeze the uniform structural all-degree successor manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "UNIFORM_STRUCTURAL_MANIFEST.sha256"

PATHS = {
    "ALL_DEGREE_STRUCTURAL_REPAIR.md",
    "ALL_DEGREE_STRUCTURAL_REVIEW.md",
    "INDEPENDENT_FORMALIZATION_MANIFEST.sha256",
    "UNIFORM_STRUCTURAL_ASSURANCE.md",
    "formal/lean/CyclicityUniform.lean",
    "formal/lean/UNIFORM_README.md",
    "formal/uniform_verification_lock.json",
    "formal/uniform_verification_protocol.json",
    "programme/UNIFORM_STRUCTURAL_QUALITY_GATE.md",
    "programme/uniform_structural_quality_gate.json",
    "receipts/uniform_structural_formalization_receipt.json",
    "run_uniform_structural_checks.py",
    "tests/test_uniform_formalization.py",
    "tools/build_uniform_structural_manifest.py",
    "tools/run_uniform_formalization.py",
    "tools/seal_uniform_formalization.py",
    "tools/verify_uniform_formalization.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rendered() -> str:
    missing = sorted(relative for relative in PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"uniform-structural manifest targets missing: {missing}")
    return "".join(f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(PATHS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = rendered()
    if args.check:
        if not MANIFEST.is_file() or MANIFEST.read_text() != expected:
            raise SystemExit("uniform-structural manifest mismatch")
        print(f"uniform-structural manifest verified: {len(PATHS)} paths")
    else:
        MANIFEST.write_text(expected)
        print(
            f"uniform-structural manifest frozen: {len(PATHS)} paths, "
            f"sha256 {sha256(MANIFEST)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
