#!/usr/bin/env python3
"""Adversarial mutations for the Kummer normalizer receipt."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "receipts/kummer_normalizer_receipt.json"
sys.path.insert(0, str(ROOT / "tools"))
from verify_kummer_normalizer import verify  # noqa: E402


def rehash(value: dict) -> dict:
    value = copy.deepcopy(value)
    value.pop("receipt_sha256", None)
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    value["receipt_sha256"] = hashlib.sha256(payload).hexdigest()
    return value


class KummerNormalizerMutations(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = json.loads(RECEIPT.read_text())

    def assert_rejected(self, value: dict) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            path.write_text(json.dumps(rehash(value), indent=2, sort_keys=True) + "\n")
            with self.assertRaises((KeyError, TypeError, ValueError)):
                verify(path)

    def test_frozen_receipt_accepts(self) -> None:
        self.assertEqual(verify(RECEIPT)["status"], "pass")

    def test_theorem_removal_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["lean"]["theorems"].pop()
        value["lean"]["theorem_count"] -= 1
        self.assert_rejected(value)

    def test_all_degree_formalization_promotion_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["assurance"]["complete_all_degree_formalization"] = True
        self.assert_rejected(value)

    def test_external_independence_promotion_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["assurance"]["external_independence"] = True
        self.assert_rejected(value)

    def test_s4_count_mutation_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["cas"]["exact_checks"]["s4_automorphisms"]["automorphism_count"] = 48
        self.assert_rejected(value)

    def test_twisted_intertwiner_mutation_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["cas"]["exact_checks"]["sign_twisted_intertwiners"] = 1
        self.assert_rejected(value)

    def test_exceptional_relation_mutation_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["cas"]["exact_checks"]["exceptional_pair_relation"] = "independent"
        self.assert_rejected(value)

    def test_uniform_full_kernel_promotion_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["assurance"]["uniform_full_kummer_kernel_claim"] = True
        self.assert_rejected(value)

    def test_tetrahedral_axis_mutation_rejected(self) -> None:
        value = copy.deepcopy(self.receipt)
        value["cas"]["exact_checks"]["tetrahedral_normalizer"][
            "normalizer_preserves_coordinate_axes"
        ] = False
        self.assert_rejected(value)


if __name__ == "__main__":
    unittest.main()
