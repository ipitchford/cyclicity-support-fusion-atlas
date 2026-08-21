#!/usr/bin/env python3
"""Adversarial receipt mutations for the global all-degree completion."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "receipts" / "global_completion_receipt.json"
sys.path.insert(0, str(ROOT / "tools"))
from verify_global_completion import verify  # noqa: E402


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def rehash(value: dict) -> dict:
    value = copy.deepcopy(value)
    value.pop("receipt_sha256", None)
    value["receipt_sha256"] = canonical_hash(value)
    return value


class GlobalCompletionMutations(unittest.TestCase):
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

    def test_rehashed_complete_formalization_claim_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["assurance"]["complete_atlas_formalization"] = True
        self.assert_rejected(mutated)

    def test_rehashed_imported_classification_claim_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["assurance"]["imported_classifications_formalized"] = True
        self.assert_rejected(mutated)

    def test_rehashed_external_independence_claim_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["assurance"]["external_independence"] = True
        self.assert_rejected(mutated)

    def test_rehashed_source_audit_identity_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["source_audit_sha256"] = "0" * 64
        self.assert_rejected(mutated)

    def test_rehashed_bounded_cas_promotion_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["cas"]["bounded_regression_controls"]["all_degree_claim"] = True
        self.assert_rejected(mutated)

    def test_rehashed_uniform_kummer_kernel_promotion_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["assurance"]["uniform_full_kummer_kernel_claim"] = True
        self.assert_rejected(mutated)

    def test_rehashed_kummer_component_mutation_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["proof_components"]["kummer"]["receipt_sha256"] = "0" * 64
        self.assert_rejected(mutated)

    def test_rehashed_dickson_proof_mutation_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["proof_components"]["dickson"]["bounded_grid_is_proof"] = True
        self.assert_rejected(mutated)

    def test_rehashed_internal_review_promotion_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["proof_components"]["internal_reaudits"]["external_independence"] = True
        self.assert_rejected(mutated)

    def test_rehashed_interface_removal_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["interfaces"].pop("rank_preserving_extensions")
        self.assert_rejected(mutated)

    def test_rehashed_claim_boundary_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["claim_boundary"] = "The all-degree atlas is externally established."
        self.assert_rejected(mutated)

    def test_rehashed_publication_claim_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["assurance"]["published"] = True
        self.assert_rejected(mutated)


if __name__ == "__main__":
    unittest.main()
