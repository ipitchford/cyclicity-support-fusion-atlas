#!/usr/bin/env python3
"""Freeze the bounded benchmark-to-degree-32 application programme manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "APPLICATIONS_MANIFEST.sha256"

APPLICATION_PATHS = {
    "APPLICATIONS_ASSURANCE.md",
    "APPLICATIONS_PROGRAMME.md",
    "APPLICATIONS_REVIEW.md",
    "MANIFEST.sha256",
    "ORDER_ORACLE_MANIFEST.sha256",
    "benchmarks/EPOB1.md",
    "benchmarks/decomposition_fusion_cases.json",
    "benchmarks/epob1_answer_key.json",
    "benchmarks/epob1_spec.json",
    "challenge/README.md",
    "challenge/answer_key.json",
    "challenge/reference_fraction_replay.py",
    "challenge/spec.json",
    "experiments/degree32_preregistration.json",
    "experiments/degree32_preregistration_lock.json",
    "experiments/degree32_quartic_lift.py",
    "programme/NOVELTY_GATE.md",
    "programme/QUALITY_GATE.json",
    "programme/QUALITY_GATE.md",
    "programme/novelty_target.yaml",
    "receipts/decomposition_fusion_cases/aligned_square_degree_12.json",
    "receipts/decomposition_fusion_cases/dickson_degree_15.json",
    "receipts/decomposition_fusion_cases/exceptional_collision_degree_12.json",
    "receipts/decomposition_fusion_cases/rank_creation_degree_6.json",
    "receipts/decomposition_fusion_receipt.json",
    "receipts/degree32_quartic_lift_result.json",
    "receipts/epob1_reference_run.json",
    "receipts/fraction_replay_challenge_receipt.json",
    "run_application_programme_checks.py",
    "src/decomposition_fusion.py",
    "tests/test_application_programme.py",
    "tools/build_application_programme_manifest.py",
    "tools/build_decomposition_fusion_receipt.py",
    "tools/run_epob1.py",
    "tools/seal_degree32_preregistration.py",
    "tools/verify_degree32_receipt.py",
    "tools/verify_epob1_submission.py",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def freeze() -> None:
    missing = sorted(relative for relative in APPLICATION_PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"application manifest targets missing: {missing}")
    lines = [f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(APPLICATION_PATHS)]
    MANIFEST.write_text("".join(lines), encoding="utf-8")
    print(f"application manifest frozen: {len(lines)} paths, sha256 {sha256(MANIFEST)}")


if __name__ == "__main__":
    freeze()
