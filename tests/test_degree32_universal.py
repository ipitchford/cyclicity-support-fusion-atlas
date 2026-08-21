#!/usr/bin/env python3
"""Mutation controls for the universal degree-32 receipt verifier."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from verify_degree32_universal import canonical_hash, verify  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def require_raises(action, fragment: str) -> None:
    try:
        action()
    except Exception as error:
        require(fragment in str(error), f"unexpected error: {error}")
        return
    raise RuntimeError(f"expected failure containing: {fragment}")


def rehash(receipt: dict) -> None:
    unhashed = dict(receipt)
    unhashed.pop("receipt_sha256", None)
    receipt["receipt_sha256"] = canonical_hash(unhashed)


def main() -> None:
    paths = {
        "preregistration_path": ROOT / "experiments" / "degree32_universal_preregistration.json",
        "lock_path": ROOT / "experiments" / "degree32_universal_lock.json",
        "runner_path": ROOT / "experiments" / "degree32_universal_runner.py",
        "receipt_path": ROOT / "receipts" / "degree32_universal_low_rank_atlas.json",
    }
    receipt = verify(**paths)
    require(len(receipt["records"]) == 466, "verified receipt case count changed")
    with tempfile.TemporaryDirectory(prefix="degree32-universal-mutations-") as tmp_name:
        tmp = Path(tmp_name)

        changed_support = deepcopy(receipt)
        changed_support["records"][10]["support"] = [1, 30]
        rehash(changed_support)
        changed_support_path = tmp / "changed-support.json"
        changed_support_path.write_text(json.dumps(changed_support))
        mutation_paths = dict(paths)
        mutation_paths["receipt_path"] = changed_support_path
        require_raises(lambda: verify(**mutation_paths), "support inventory")

        changed_witness = deepcopy(receipt)
        target = next(record for record in changed_witness["records"] if record.get("witness", {}).get("kind") == "power-only")
        target["witness"]["nilpotence_powers"].pop(next(iter(target["witness"]["nilpotence_powers"])))
        rehash(changed_witness)
        changed_witness_path = tmp / "changed-witness.json"
        changed_witness_path.write_text(json.dumps(changed_witness))
        mutation_paths["receipt_path"] = changed_witness_path
        require_raises(lambda: verify(**mutation_paths), "nilpotence-coordinate coverage")

        changed_boundary = deepcopy(receipt)
        changed_boundary["claim_boundary"] = []
        rehash(changed_boundary)
        changed_boundary_path = tmp / "changed-boundary.json"
        changed_boundary_path.write_text(json.dumps(changed_boundary))
        mutation_paths["receipt_path"] = changed_boundary_path
        require_raises(lambda: verify(**mutation_paths), "claim boundary drift")

    print("degree-32 universal tests passed: exact inventory plus support, witness and boundary mutations")


if __name__ == "__main__":
    main()
