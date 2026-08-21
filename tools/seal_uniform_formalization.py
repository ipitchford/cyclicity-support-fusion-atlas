#!/usr/bin/env python3
"""Seal source identity for the uniform structural successor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "formal" / "uniform_verification_lock.json"
LOCKED_PATHS = (
    "ALL_DEGREE_STRUCTURAL_REPAIR.md",
    "ALL_DEGREE_STRUCTURAL_REVIEW.md",
    "formal/uniform_verification_protocol.json",
    "formal/lean/CyclicityUniform.lean",
    "formal/lean/UNIFORM_README.md",
    "tools/run_uniform_formalization.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> int:
    result = {
        "schema": "cyclicity-uniform-structural-lock-v1",
        "status": "sealed",
        "hash_algorithm": "sha256",
        "files": {relative: sha256(ROOT / relative) for relative in LOCKED_PATHS},
        "seal_boundary": (
            "Post-implementation source-identity lock. It is not prospective "
            "preregistration, external review, or proof of the unformalized interfaces."
        ),
    }
    result["lock_sha256"] = canonical_hash(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "sealed", "lock_sha256": result["lock_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
