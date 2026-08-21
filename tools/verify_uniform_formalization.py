#!/usr/bin/env python3
"""Semantically verify the uniform structural Lean receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "receipts" / "uniform_structural_formalization_receipt.json"
PROTOCOL = ROOT / "formal" / "uniform_verification_protocol.json"
LOCK = ROOT / "formal" / "uniform_verification_lock.json"
LEAN_SOURCE = ROOT / "formal" / "lean" / "CyclicityUniform.lean"
PROOF_NOTE = ROOT / "ALL_DEGREE_STRUCTURAL_REPAIR.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def checked_digest(value: dict[str, Any], field: str) -> None:
    claimed = value.pop(field, None)
    if not isinstance(claimed, str) or canonical_hash(value) != claimed:
        raise ValueError(f"{field} mismatch")
    value[field] = claimed


def theorem_names(source: str) -> list[str]:
    return re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)


def verify(receipt_path: Path) -> dict[str, Any]:
    protocol = json.loads(PROTOCOL.read_text())
    lock = json.loads(LOCK.read_text())
    checked_digest(lock, "lock_sha256")
    if lock.get("schema") != "cyclicity-uniform-structural-lock-v1":
        raise ValueError("lock schema mismatch")
    for relative, expected in lock["files"].items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"locked source mismatch: {relative}")

    source = LEAN_SOURCE.read_text()
    if re.search(r"\b(sorry|admit|axiom)\b", source):
        raise ValueError("Lean placeholder or axiom declaration detected")
    names = theorem_names(source)
    exact = protocol["exact_claims"]
    expected_names = (
        exact["scaling_theorems"]
        + exact["coefficient_theorems"]
        + exact["uniform_theorems"]
    )
    if names != expected_names or len(names) != 25:
        raise ValueError("source theorem inventory mismatch")

    receipt = json.loads(receipt_path.read_text())
    checked_digest(receipt, "receipt_sha256")
    if receipt.get("schema") != "cyclicity-uniform-structural-receipt-v1":
        raise ValueError("receipt schema mismatch")
    if receipt.get("status") != "pass":
        raise ValueError("receipt status is not pass")
    if receipt.get("protocol_sha256") != sha256(PROTOCOL):
        raise ValueError("protocol identity mismatch")
    if receipt.get("lock_sha256") != lock["lock_sha256"]:
        raise ValueError("lock identity mismatch")
    if receipt.get("proof_note_sha256") != sha256(PROOF_NOTE):
        raise ValueError("proof-note identity mismatch")

    lean = receipt.get("lean", {})
    if lean.get("source_sha256") != lock["files"]["formal/lean/CyclicityUniform.lean"]:
        raise ValueError("Lean source identity mismatch")
    if lean.get("kernel_status") != "pass" or lean.get("placeholder_scan") != "pass":
        raise ValueError("Lean assurance status mismatch")
    if lean.get("theorems") != expected_names or lean.get("theorem_count") != 25:
        raise ValueError("receipt theorem inventory mismatch")
    if lean.get("uniform_upper_cutoff", "missing") is not None:
        raise ValueError("uniform theorem was replaced by a bounded cutoff")
    if not str(lean.get("version", "")).startswith("Lean (version 4.32.1"):
        raise ValueError("Lean version mismatch")
    commit = lean.get("mathlib_commit")
    if not isinstance(commit, str) or len(commit) != 40:
        raise ValueError("Mathlib identity missing")

    expected_formalized = {
        "scaling": "lifted root-of-unity phases through common rescaling",
        "coefficients": "exact selected negative-binomial finite sums over QQ",
        "uniformity": "constructive mod-3 and mod-4 witnesses for arbitrary natural m",
        "cubic_candidates_before_E2": [2, 4],
        "quartic_candidates_before_E2": [2, 3, 5, 6, 9],
    }
    if receipt.get("formalized_boundary") != expected_formalized:
        raise ValueError("formalized mathematical boundary mismatch")
    expected_assurance = {
        "formal_kernel": True,
        "complete_atlas_formalization": False,
        "external_independence": False,
    }
    if receipt.get("assurance") != expected_assurance:
        raise ValueError("assurance classification mismatch")
    if receipt.get("claim_boundary") != protocol["claim_boundary"]:
        raise ValueError("claim boundary mismatch")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    try:
        receipt = verify(args.receipt)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"UNIFORM FORMALIZATION VERIFY FAIL: {exc}")
        return 1
    if not args.quiet:
        print(
            json.dumps(
                {
                    "status": "pass",
                    "theorem_count": receipt["lean"]["theorem_count"],
                    "uniform_upper_cutoff": receipt["lean"]["uniform_upper_cutoff"],
                    "receipt_sha256": receipt["receipt_sha256"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
