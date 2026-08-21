#!/usr/bin/env python3
"""Adversarial mutations for the uniform structural receipt."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "receipts" / "uniform_structural_formalization_receipt.json"
sys.path.insert(0, str(ROOT / "tools"))
from verify_uniform_formalization import verify  # noqa: E402


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def rehash(value: dict) -> dict:
    value = copy.deepcopy(value)
    value.pop("receipt_sha256", None)
    value["receipt_sha256"] = canonical_hash(value)
    return value


class UniformFormalizationMutations(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = json.loads(RECEIPT.read_text())

    def assert_rejected(self, mutated: dict) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            path.write_text(json.dumps(rehash(mutated), indent=2, sort_keys=True) + "\n")
            with self.assertRaises((KeyError, TypeError, ValueError)):
                verify(path)

    def test_frozen_receipt_accepts(self) -> None:
        self.assertEqual(verify(RECEIPT)["status"], "pass")

    def test_rehashed_theorem_removal_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["lean"]["theorems"].pop()
        mutated["lean"]["theorem_count"] -= 1
        self.assert_rejected(mutated)

    def test_rehashed_finite_cutoff_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["lean"]["uniform_upper_cutoff"] = 32
        self.assert_rejected(mutated)

    def test_rehashed_complete_atlas_claim_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["assurance"]["complete_atlas_formalization"] = True
        self.assert_rejected(mutated)

    def test_rehashed_proof_identity_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["proof_note_sha256"] = "0" * 64
        self.assert_rejected(mutated)

    def test_rehashed_candidate_boundary_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["formalized_boundary"]["quartic_candidates_before_E2"] = [2, 3]
        self.assert_rejected(mutated)

    def test_rehashed_claim_boundary_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["claim_boundary"] = "The complete all-degree atlas is formally verified."
        self.assert_rejected(mutated)


if __name__ == "__main__":
    unittest.main()
