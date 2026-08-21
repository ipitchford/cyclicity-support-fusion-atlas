#!/usr/bin/env python3
"""Freeze the degree-32 universal and Newton-descent successor manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "DEGREE32_UNIVERSAL_MANIFEST.sha256"

PATHS = {
    "ALL_DEGREE_NEWTON_DESCENT.md",
    "ALL_DEGREE_NEWTON_REVIEW.md",
    "APPLICATIONS_MANIFEST.sha256",
    "DEGREE32_UNIVERSAL.md",
    "DEGREE32_UNIVERSAL_ASSURANCE.md",
    "cleanroom/newton_resultant_crosscheck.py",
    "experiments/degree32_universal_lock.json",
    "experiments/degree32_universal_preregistration.json",
    "experiments/degree32_universal_runner.py",
    "receipts/degree32_universal_low_rank_atlas.json",
    "receipts/degree32_universal_replay.json",
    "receipts/newton_descent_check.json",
    "receipts/newton_resultant_crosscheck.json",
    "run_degree32_universal_checks.py",
    "tests/test_degree32_universal.py",
    "tools/build_degree32_universal_manifest.py",
    "tools/build_degree32_universal_replay_receipt.py",
    "tools/check_newton_descent.py",
    "tools/seal_degree32_universal.py",
    "tools/verify_degree32_universal.py",
    "verification/battery4a_fast.py",
    "verification/lib.py",
    "verification/symconstr.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze() -> None:
    missing = sorted(relative for relative in PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"degree-32 successor manifest targets missing: {missing}")
    MANIFEST.write_text("".join(f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(PATHS)))
    print(f"degree-32 successor manifest frozen: {len(PATHS)} paths, sha256 {sha256(MANIFEST)}")


if __name__ == "__main__":
    freeze()
