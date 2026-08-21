#!/usr/bin/env python3
"""Freeze the independent Singular/Lean successor manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "INDEPENDENT_FORMALIZATION_MANIFEST.sha256"

PATHS = {
    "DEGREE32_UNIVERSAL_MANIFEST.sha256",
    "INDEPENDENT_FORMALIZATION.md",
    "cleanroom/singular_newton_crosscheck.sing",
    "formal/independent_verification_lock.json",
    "formal/independent_verification_protocol.json",
    "formal/lean/CyclicityNewton.lean",
    "formal/lean/README.md",
    "formal/lean/lakefile.toml",
    "formal/lean/lean-toolchain",
    "programme/INDEPENDENT_FORMALIZATION_QUALITY_GATE.md",
    "programme/independent_formalization_quality_gate.json",
    "receipts/independent_formalization_receipt.json",
    "run_independent_formalization_checks.py",
    "tests/test_independent_formalization.py",
    "tools/build_independent_formalization_manifest.py",
    "tools/run_independent_formalization.py",
    "tools/seal_independent_formalization.py",
    "tools/verify_independent_formalization.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rendered() -> str:
    missing = sorted(relative for relative in PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"independent-formalization manifest targets missing: {missing}")
    return "".join(f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(PATHS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = rendered()
    if args.check:
        if not MANIFEST.is_file() or MANIFEST.read_text() != expected:
            raise SystemExit("independent-formalization manifest mismatch")
        print(f"independent-formalization manifest verified: {len(PATHS)} paths")
    else:
        MANIFEST.write_text(expected)
        print(
            f"independent-formalization manifest frozen: {len(PATHS)} paths, "
            f"sha256 {sha256(MANIFEST)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
