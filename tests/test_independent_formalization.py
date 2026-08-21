#!/usr/bin/env python3
"""Adversarial mutation tests for the independent formalization receipt."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "receipts" / "independent_formalization_receipt.json"

import sys

sys.path.insert(0, str(ROOT / "tools"))
from verify_independent_formalization import verify  # noqa: E402


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def rehash(value: dict) -> dict:
    value = copy.deepcopy(value)
    value.pop("receipt_sha256", None)
    value["receipt_sha256"] = canonical_hash(value)
    return value


class IndependentFormalizationMutations(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = json.loads(RECEIPT.read_text())

    def assert_rejected(self, mutated: dict) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            path.write_text(json.dumps(rehash(mutated), indent=2, sort_keys=True) + "\n")
            with self.assertRaises((KeyError, TypeError, ValueError)):
                verify(path)

    def test_frozen_receipt_accepts(self) -> None:
        checked = verify(RECEIPT)
        self.assertEqual(checked["status"], "pass")

    def test_rehashed_survivor_forgery_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        target = next(
            row
            for row in mutated["engines"]["singular"]["records"]
            if row["type"] == "quartic" and row["m"] == 4
        )
        target["empty_after_nondegenerate_saturation"] = False
        target["reduced_standard_basis"] = "cw-1,a"
        self.assert_rejected(mutated)

    def test_rehashed_identity_forgery_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["engines"]["singular"]["positive_resultants"]["quartic"] = (
            "y4+3y3c+3y2c2+yc3-e3"
        )
        self.assert_rejected(mutated)

    def test_rehashed_lean_inventory_forgery_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["engines"]["lean"]["theorems"].pop()
        mutated["engines"]["lean"]["theorem_count"] -= 1
        self.assert_rejected(mutated)

    def test_rehashed_claim_boundary_weakening_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["claim_boundary"] = "The all-degree theorem is formally verified."
        self.assert_rejected(mutated)

    def test_rehashed_source_identity_forgery_rejected(self) -> None:
        mutated = copy.deepcopy(self.receipt)
        mutated["engines"]["lean"]["source_sha256"] = "0" * 64
        self.assert_rejected(mutated)


if __name__ == "__main__":
    unittest.main()
