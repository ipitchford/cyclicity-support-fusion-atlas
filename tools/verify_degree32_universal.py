#!/usr/bin/env python3
"""Semantically verify the sealed universal degree-32 low-rank receipt."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = [
    ROOT / "verification" / "battery4a_fast.py",
    ROOT / "verification" / "symconstr.py",
    ROOT / "verification" / "lib.py",
]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def expected_supports() -> list[list[int]]:
    classes = list(range(1, 32))
    supports = [[1]]
    supports.extend([[1, value] for value in classes if value != 1])
    supports.extend(
        [[1, left, right] for left, right in itertools.combinations(classes, 2) if left != 1 and right != 1]
    )
    return supports


def inverse_index(residue: int) -> int:
    value = (1 - residue) % 32
    return 32 if value == 0 else value


def expected_families(support: set[int]) -> list[str]:
    families = ["power"]
    if {1, 31} <= support:
        families.append("dickson")
    if {1, 17} <= support:
        families.append("quadO")
    return sorted(families)


def verify(
    preregistration_path: Path,
    lock_path: Path,
    runner_path: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    preregistration = json.loads(preregistration_path.read_text())
    lock = json.loads(lock_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    require(preregistration.get("schema") == "degree32-universal-low-rank-preregistration-v1", "unknown preregistration schema")
    require(lock.get("schema") == "degree32-universal-lock-v1", "unknown lock schema")
    require(lock.get("preregistration_sha256") == sha256_path(preregistration_path), "preregistration seal mismatch")
    require(lock.get("runner_sha256") == sha256_path(runner_path), "runner seal mismatch")
    require(
        lock.get("dependency_sha256") == {
            str(path.relative_to(ROOT)): sha256_path(path) for path in DEPENDENCIES
        },
        "dependency seal mismatch",
    )
    require(lock.get("execution_state_at_seal") == "not_run", "computation was not prospectively sealed")

    require(receipt.get("schema") == "degree32-universal-low-rank-atlas-receipt-v1", "unknown receipt schema")
    supplied_hash = receipt.get("receipt_sha256")
    unhashed = dict(receipt)
    unhashed.pop("receipt_sha256", None)
    require(supplied_hash == canonical_hash(unhashed), "receipt digest mismatch")
    require(receipt.get("seal") == lock, "embedded seal mismatch")
    require(receipt.get("status") == "complete", "receipt is incomplete")
    require(receipt.get("adjudication") == "confirmed", "universal degree-32 result is not confirmed")
    require(receipt.get("theorem_target") == preregistration["theorem_target"], "theorem target drift")
    require(receipt.get("coverage") == preregistration["coverage"], "coverage drift")
    require(receipt.get("claim_boundary") == preregistration["claim_boundary"], "claim boundary drift")

    expected_summary = {
        "cases": 466,
        "vacuous_full_family": 3,
        "exact_power_only": 406,
        "exact_union": 57,
        "anomalies": 0,
        "no_certificate": 0,
    }
    require(receipt.get("summary") == expected_summary, "summary differs from preregistered counts")
    records = receipt.get("records", [])
    supports = expected_supports()
    require(len(records) == len(supports) == 466, "case inventory length mismatch")
    require([record.get("support") for record in records] == supports, "support inventory or ordering mismatch")

    counts = {"vacuous-full-family": 0, "power-only": 0, "union": 0}
    for record in records:
        support = set(record["support"])
        families = expected_families(support)
        dimension = 1 if families == ["power"] else 2
        require(record.get("degree") == 32, "record degree mismatch")
        require(record.get("truncation") == {"K1": 128, "K2": 192}, "truncation drift")
        require(record.get("predicted_families") == families, "predicted-family mismatch")
        require(record.get("predicted_dimension") == dimension, "predicted-dimension mismatch")
        require(record.get("stability") is True, "condition ideal was not stable through 6d")
        witness = record.get("witness", {})
        full_family = len(support) == dimension
        if full_family:
            require(record.get("status") == "vacuous-full-family", "full family did not receive a vacuity certificate")
            require(witness == {"free_coordinates": dimension}, "vacuity witness mismatch")
            require(record.get("ideal_digest") is None and record.get("groebner_digest") is None, "vacuous case has unexpected ideal")
            counts["vacuous-full-family"] += 1
            continue

        require(record.get("status") == "certified", "non-vacuous case is not certified")
        require(record.get("computed_dimension") == dimension, "computed-dimension mismatch")
        for key in ("ideal_digest", "groebner_digest"):
            digest = record.get(key)
            require(isinstance(digest, str) and len(digest) == 64, f"invalid {key}")
        if dimension == 1:
            require(witness.get("kind") == "power-only", "power-only witness missing")
            expected_keys = {f"u{inverse_index(residue)}" for residue in support if residue != 1}
            powers = witness.get("nilpotence_powers", {})
            require(set(powers) == expected_keys, "nilpotence-coordinate coverage mismatch")
            require(all(isinstance(power, int) and 1 <= power <= 24 for power in powers.values()), "invalid nilpotence exponent")
            counts["power-only"] += 1
        else:
            require(witness.get("kind") == "union", "union witness missing")
            require(isinstance(witness.get("product_power"), int) and 1 <= witness["product_power"] <= 24, "invalid union exponent")
            counts["union"] += 1

    require(counts == {"vacuous-full-family": 3, "power-only": 406, "union": 57}, "semantic witness counts mismatch")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preregistration", type=Path, default=ROOT / "experiments" / "degree32_universal_preregistration.json")
    parser.add_argument("--lock", type=Path, default=ROOT / "experiments" / "degree32_universal_lock.json")
    parser.add_argument("--runner", type=Path, default=ROOT / "experiments" / "degree32_universal_runner.py")
    parser.add_argument("--receipt", type=Path, default=ROOT / "receipts" / "degree32_universal_low_rank_atlas.json")
    args = parser.parse_args()
    receipt = verify(args.preregistration, args.lock, args.runner, args.receipt)
    print(json.dumps({
        "status": "pass",
        "adjudication": receipt["adjudication"],
        "cases": len(receipt["records"]),
        "receipt_sha256": receipt["receipt_sha256"],
        "computation_reexecuted": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
