#!/usr/bin/env python3
"""Semantically verify the frozen Singular/Lean formalization receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "receipts" / "independent_formalization_receipt.json"
PROTOCOL = ROOT / "formal" / "independent_verification_protocol.json"
LOCK = ROOT / "formal" / "independent_verification_lock.json"


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


def verify(receipt_path: Path) -> dict[str, Any]:
    protocol = json.loads(PROTOCOL.read_text())
    lock = json.loads(LOCK.read_text())
    checked_digest(lock, "lock_sha256")
    if lock.get("schema") != "cyclicity-independent-formalization-lock-v1":
        raise ValueError("lock schema mismatch")
    for relative, expected in lock["files"].items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"locked source mismatch: {relative}")

    receipt = json.loads(receipt_path.read_text())
    checked_digest(receipt, "receipt_sha256")
    if receipt.get("schema") != "cyclicity-independent-formalization-receipt-v1":
        raise ValueError("receipt schema mismatch")
    if receipt.get("status") != "pass":
        raise ValueError("receipt status is not pass")
    if receipt.get("protocol_sha256") != sha256(PROTOCOL):
        raise ValueError("protocol identity mismatch")
    if receipt.get("lock_sha256") != lock["lock_sha256"]:
        raise ValueError("lock identity mismatch")

    singular = receipt["engines"]["singular"]
    lean = receipt["engines"]["lean"]
    if singular.get("source_sha256") != lock["files"]["cleanroom/singular_newton_crosscheck.sing"]:
        raise ValueError("Singular source identity mismatch")
    if lean.get("source_sha256") != lock["files"]["formal/lean/CyclicityNewton.lean"]:
        raise ValueError("Lean source identity mismatch")
    if not str(singular.get("version", "")).startswith("Singular for "):
        raise ValueError("Singular engine identity missing")
    if not str(lean.get("version", "")).startswith("Lean (version 4.32.1"):
        raise ValueError("Lean engine identity mismatch")
    if lean.get("kernel_status") != "pass":
        raise ValueError("Lean kernel status is not pass")

    records = singular.get("records")
    if not isinstance(records, list) or len(records) != 62 or singular.get("case_count") != 62:
        raise ValueError("Singular case count mismatch")
    expected_pairs = {(kind, m) for kind in ("cubic", "quartic") for m in range(2, 33)}
    actual_pairs = {(record.get("type"), record.get("m")) for record in records}
    if actual_pairs != expected_pairs:
        raise ValueError("Singular case inventory mismatch")
    for record in records:
        kind = record["type"]
        survivor = 2 if kind == "cubic" else 3
        if record.get("empty_after_nondegenerate_saturation") != (record["m"] != survivor):
            raise ValueError(f"altered survivor classification: {kind} m={record['m']}")
        expected_basis = "aw-1" if (kind, record["m"]) == ("cubic", 2) else (
            "cw-1,a" if (kind, record["m"]) == ("quartic", 3) else "1"
        )
        if record.get("reduced_standard_basis") != expected_basis:
            raise ValueError(f"altered standard basis: {kind} m={record['m']}")
        if not isinstance(record.get("condition_count"), int) or record["condition_count"] < 0:
            raise ValueError("invalid condition count")

    expected_cas = protocol["exact_claims"]["singular_bounded_elimination"]
    expected_identities = {
        "cubic": expected_cas["cubic_positive_resultant"],
        "quartic": expected_cas["quartic_positive_resultant"],
    }
    if singular.get("positive_resultants") != expected_identities:
        raise ValueError("positive resultant identity mismatch")
    raw_digest = singular.get("raw_output_sha256")
    if not isinstance(raw_digest, str) or len(raw_digest) != 64:
        raise ValueError("Singular raw-output digest missing")

    expected_lean = protocol["exact_claims"]["lean_kernel"]
    theorem_names = (
        expected_lean["root_map_identities"]
        + expected_lean["coefficient_obstructions"]
        + expected_lean["displayed_elementary_identities"]
    )
    if lean.get("theorems") != theorem_names or lean.get("theorem_count") != len(theorem_names):
        raise ValueError("Lean theorem inventory mismatch")
    commit = lean.get("mathlib_commit")
    if not isinstance(commit, str) or len(commit) != 40:
        raise ValueError("Mathlib identity missing")

    expected_separation = {
        "algebra_engine": "Singular, not SymPy",
        "formal_kernel": "Lean 4 with Mathlib",
        "orchestrator": "Python standard library only",
        "external_independence": False,
    }
    if receipt.get("separation") != expected_separation:
        raise ValueError("independence classification mismatch")
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
        print(f"INDEPENDENT FORMALIZATION VERIFY FAIL: {exc}")
        return 1
    if not args.quiet:
        print(
            json.dumps(
                {
                    "status": "pass",
                    "singular_cases": receipt["engines"]["singular"]["case_count"],
                    "lean_theorems": receipt["engines"]["lean"]["theorem_count"],
                    "receipt_sha256": receipt["receipt_sha256"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
