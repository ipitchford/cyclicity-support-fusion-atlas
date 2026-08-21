#!/usr/bin/env python3
"""Semantic verifier for the Kummer normalizer successor receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "receipts/kummer_normalizer_receipt.json"
PROTOCOL = ROOT / "formal/kummer_normalizer_protocol.json"
LOCK = ROOT / "formal/kummer_normalizer_lock.json"
LEAN = ROOT / "formal/lean/CyclicityKummer.lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def checked(value: dict[str, Any], field: str) -> None:
    claimed = value.pop(field, None)
    if not isinstance(claimed, str) or canonical_hash(value) != claimed:
        raise ValueError(f"{field} mismatch")
    value[field] = claimed


def verify(path: Path) -> dict[str, Any]:
    protocol = json.loads(PROTOCOL.read_text())
    lock = json.loads(LOCK.read_text())
    checked(lock, "lock_sha256")
    if lock.get("schema") != "cyclicity-kummer-normalizer-lock-v2":
        raise ValueError("lock schema mismatch")
    for relative, expected in lock["files"].items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"locked source mismatch: {relative}")
    source = LEAN.read_text()
    if re.search(r"\b(sorry|admit|axiom)\b", source):
        raise ValueError("Lean placeholder detected")
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != protocol["exact_claims"]["lean_theorems"]:
        raise ValueError("Lean theorem inventory mismatch")

    receipt = json.loads(path.read_text())
    checked(receipt, "receipt_sha256")
    if receipt.get("schema") != "cyclicity-kummer-normalizer-receipt-v2" or receipt.get("status") != "pass":
        raise ValueError("receipt identity/status mismatch")
    if receipt.get("protocol_sha256") != sha256(PROTOCOL):
        raise ValueError("protocol identity mismatch")
    if receipt.get("lock_sha256") != lock["lock_sha256"]:
        raise ValueError("lock identity mismatch")
    if receipt.get("proof_note_sha256") != sha256(ROOT / "KUMMER_NORMALIZER_COMPLETION.md"):
        raise ValueError("proof-note identity mismatch")
    if receipt.get("lean", {}).get("theorems") != names or receipt["lean"].get("theorem_count") != 5:
        raise ValueError("Lean receipt inventory mismatch")
    if receipt["lean"].get("kernel_status") != "pass" or receipt["lean"].get("placeholder_scan") != "pass":
        raise ValueError("Lean kernel status mismatch")
    if sorted(receipt.get("cas", {}).get("exact_checks", {})) != sorted(protocol["exact_claims"]["cas_checks"]):
        raise ValueError("CAS receipt inventory mismatch")
    checks = receipt["cas"]["exact_checks"]
    if checks.get("transposition_characteristic_identity") is not True:
        raise ValueError("transposition identity mismatch")
    if checks.get("kummer_reflection_characteristic_identity") is not True:
        raise ValueError("Kummer reflection identity mismatch")
    if checks.get("transposition_elimination") != "-2*(z + 1)**2":
        raise ValueError("transposition elimination mismatch")
    if checks.get("three_cycle_obstruction") != "coprime coefficient equations":
        raise ValueError("three-cycle obstruction mismatch")
    if checks.get("discriminant_quotient_degree") != 1:
        raise ValueError("discriminant quotient degree mismatch")
    if checks.get("exceptional_cubic_factorization") is not True:
        raise ValueError("exceptional cubic factorization mismatch")
    if checks.get("exceptional_pair_relation") != "y_i*y_j=(y_k+r)^2":
        raise ValueError("exceptional pair relation mismatch")
    if checks.get("exceptional_even_square_factorization") is not True:
        raise ValueError("exceptional even square factorization mismatch")
    if checks.get("dickson_degree_six_target_translation") is not True:
        raise ValueError("Dickson degree-six translation mismatch")
    if checks.get("affine_power_cubic_identity") is not True:
        raise ValueError("affine-power cubic identity mismatch")
    if checks.get("affine_power_fourier_determinant_nonzero") is not True:
        raise ValueError("affine-power Fourier determinant mismatch")
    if checks.get("affine_power_sign_solution_count") != 1:
        raise ValueError("affine-power sign solution mismatch")
    automorphisms = checks.get("s4_automorphisms", {})
    if automorphisms != {"all_inner": True, "automorphism_count": 24, "inner_count": 24}:
        raise ValueError("S4 automorphism audit mismatch")
    if checks.get("octahedral_realisation") != {
        "faithful_body_diagonal_action": True,
        "rotation_count": 24,
    }:
        raise ValueError("octahedral realization mismatch")
    if checks.get("ordinary_centralizer") != 1:
        raise ValueError("ordinary centralizer mismatch")
    if checks.get("sign_twisted_intertwiners") != 0:
        raise ValueError("sign-twisted intertwiner mismatch")
    if checks.get("a4_automorphisms") != {
        "all_realized_by_octahedral_conjugation": True,
        "automorphism_count": 24,
    }:
        raise ValueError("A4 automorphism audit mismatch")
    if checks.get("tetrahedral_normalizer") != {
        "automorphism_representatives_signed_monomial": True,
        "character_intertwiner_dimensions": [1, 1, 1],
        "linear_character_count": 3,
        "normalizer_preserves_coordinate_axes": True,
        "projective_centralizer_representatives_diagonal": True,
        "rotation_count": 12,
    }:
        raise ValueError("tetrahedral normalizer audit mismatch")
    expected_assurance = {
        "written_stratified_all_m_transport": True,
        "exceptional_even_relation_encoded": True,
        "uniform_full_kummer_kernel_claim": False,
        "formal_local_algebra": True,
        "separate_cas_implementation": True,
        "complete_all_degree_formalization": False,
        "external_independence": False,
        "peer_reviewed": False,
        "published": False,
    }
    if receipt.get("assurance") != expected_assurance:
        raise ValueError("assurance boundary mismatch")
    if receipt.get("claim_boundary") != protocol["claim_boundary"]:
        raise ValueError("claim boundary mismatch")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()
    try:
        receipt = verify(args.receipt)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"KUMMER NORMALIZER VERIFY FAIL: {exc}")
        return 1
    print(json.dumps({"status": receipt["status"], "receipt_sha256": receipt["receipt_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
