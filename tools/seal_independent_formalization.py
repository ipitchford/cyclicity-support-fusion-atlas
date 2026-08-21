#!/usr/bin/env python3
"""Seal the source identity for the independent Singular/Lean check."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "formal" / "independent_verification_lock.json"
LOCKED_PATHS = (
    "formal/independent_verification_protocol.json",
    "cleanroom/singular_newton_crosscheck.sing",
    "formal/lean/CyclicityNewton.lean",
    "formal/lean/lakefile.toml",
    "formal/lean/lean-toolchain",
    "tools/run_independent_formalization.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> int:
    result = {
        "schema": "cyclicity-independent-formalization-lock-v1",
        "status": "sealed",
        "hash_algorithm": "sha256",
        "files": {relative: sha256(ROOT / relative) for relative in LOCKED_PATHS},
        "seal_boundary": (
            "Post-implementation source-identity lock, not a prospective "
            "preregistration and not evidence of external independence."
        ),
    }
    result["lock_sha256"] = canonical_hash(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "sealed", "lock_sha256": result["lock_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
