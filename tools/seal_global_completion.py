#!/usr/bin/env python3
"""Seal source identity for the global all-degree completion successor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "formal" / "global_verification_lock.json"
LOCKED_PATHS = (
    "ALL_DEGREE_GLOBAL_COMPLETION.md",
    "ALL_DEGREE_GLOBAL_REVIEW.md",
    "DICKSON_EXTENSION_COMPLETION.md",
    "GLOBAL_COMPLETION_SOURCE_AUDIT.md",
    "KUMMER_NORMALIZER_MANIFEST.sha256",
    "receipts/kummer_normalizer_receipt.json",
    "programme/FINITE_LINEAR_GROUP_REFEREE_REPORT.md",
    "programme/MONODROMY_RITT_REFEREE_REPORT.md",
    "cleanroom/global_interface_audit.py",
    "formal/global_verification_protocol.json",
    "formal/lean/CyclicityGlobal.lean",
    "formal/lean/GLOBAL_README.md",
    "tools/run_global_completion.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    result: dict[str, Any] = {
        "schema": "cyclicity-global-completion-lock-v2",
        "status": "sealed",
        "hash_algorithm": "sha256",
        "files": {relative: sha256(ROOT / relative) for relative in LOCKED_PATHS},
        "seal_boundary": (
            "Post-implementation source-identity lock for an internal theorem candidate. "
            "It is not prospective preregistration, external review, a formalization of "
            "the imported classifications, publication, or proof of novelty."
        ),
    }
    result["lock_sha256"] = canonical_hash(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "sealed", "lock_sha256": result["lock_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
