#!/usr/bin/env python3
"""Seal source identities for the Kummer normalizer successor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "formal" / "kummer_normalizer_lock.json"
PATHS = [
    "KUMMER_NORMALIZER_COMPLETION.md",
    "KUMMER_NORMALIZER_ASSURANCE.md",
    "cleanroom/kummer_normalizer_audit.py",
    "formal/kummer_normalizer_protocol.json",
    "formal/lean/CyclicityKummer.lean",
    "formal/lean/KUMMER_README.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> int:
    result: dict[str, Any] = {
        "schema": "cyclicity-kummer-normalizer-lock-v2",
        "status": "sealed",
        "hash_algorithm": "sha256",
        "files": {relative: sha256(ROOT / relative) for relative in PATHS},
        "seal_boundary": "Additive repaired coefficient-stratified transport identity lock; not prospective preregistration, external review, complete formalization, proof of novelty, or publication.",
    }
    result["lock_sha256"] = canonical_hash(result)
    LOCK.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "sealed", "lock_sha256": result["lock_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
