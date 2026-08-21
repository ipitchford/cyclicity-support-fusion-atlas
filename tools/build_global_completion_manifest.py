#!/usr/bin/env python3
"""Freeze the additive manifest for the global all-degree completion."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "GLOBAL_COMPLETION_MANIFEST.sha256"

PATHS = {
    "ALL_DEGREE_GLOBAL_COMPLETION.md",
    "ALL_DEGREE_GLOBAL_REVIEW.md",
    "DICKSON_EXTENSION_COMPLETION.md",
    "GLOBAL_COMPLETION_ASSURANCE.md",
    "GLOBAL_COMPLETION_SOURCE_AUDIT.md",
    "KUMMER_NORMALIZER_MANIFEST.sha256",
    "UNIFORM_STRUCTURAL_MANIFEST.sha256",
    "cleanroom/global_interface_audit.py",
    "formal/global_verification_lock.json",
    "formal/global_verification_protocol.json",
    "formal/lean/CyclicityGlobal.lean",
    "formal/lean/GLOBAL_README.md",
    "programme/GLOBAL_COMPLETION_QUALITY_GATE.md",
    "programme/FINITE_LINEAR_GROUP_REFEREE_REPORT.md",
    "programme/MONODROMY_RITT_REFEREE_REPORT.md",
    "programme/global_completion_quality_gate.json",
    "receipts/global_completion_receipt.json",
    "receipts/global_interface_cas_receipt.json",
    "receipts/kummer_normalizer_receipt.json",
    "run_global_completion_checks.py",
    "tests/test_global_completion.py",
    "tools/build_global_completion_manifest.py",
    "tools/run_global_completion.py",
    "tools/seal_global_completion.py",
    "tools/verify_global_completion.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rendered() -> str:
    missing = sorted(relative for relative in PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"global-completion manifest targets missing: {missing}")
    return "".join(f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(PATHS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = rendered()
    if args.check:
        if not MANIFEST.is_file() or MANIFEST.read_text() != expected:
            raise SystemExit("global-completion manifest mismatch")
        print(f"global-completion manifest verified: {len(PATHS)} paths")
    else:
        MANIFEST.write_text(expected)
        print(
            f"global-completion manifest frozen: {len(PATHS)} paths, "
            f"sha256 {sha256(MANIFEST)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
