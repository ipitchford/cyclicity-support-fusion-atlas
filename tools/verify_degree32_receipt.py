#!/usr/bin/env python3
"""Verify the sealed degree-32 receipt without rerunning the experiment."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify(
    preregistration_path: Path,
    lock_path: Path,
    runner_path: Path,
    result_path: Path,
) -> dict[str, Any]:
    preregistration = json.loads(preregistration_path.read_text())
    lock = json.loads(lock_path.read_text())
    result = json.loads(result_path.read_text())

    require(
        preregistration.get("schema") == "degree32-quartic-lift-preregistration-v1",
        "unknown degree-32 preregistration schema",
    )
    require(
        lock.get("schema") == "degree32-preregistration-lock-v1",
        "unknown degree-32 lock schema",
    )
    require(
        lock.get("preregistration_sha256") == sha256_path(preregistration_path),
        "preregistration digest does not match the seal",
    )
    require(
        lock.get("runner_sha256") == sha256_path(runner_path),
        "runner digest does not match the seal",
    )
    require(lock.get("execution_state_at_seal") == "not_run", "experiment was not sealed prospectively")

    require(result.get("schema") == "degree32-quartic-lift-result-v1", "unknown result schema")
    require(result.get("status") == "complete", "degree-32 result is incomplete")
    supplied_digest = result.get("result_sha256")
    unhashed = dict(result)
    unhashed.pop("result_sha256", None)
    require(supplied_digest == canonical_hash(unhashed), "degree-32 result digest mismatch")
    require(result.get("seal") == lock, "embedded result seal differs from the lock")

    object_spec = preregistration["object"]
    method = preregistration["method"]
    require(result.get("m") == object_spec["m"] == 8, "unexpected lift index")
    require(result.get("degree") == object_spec["degree"] == 32, "unexpected degree")
    require(
        result.get("inverse_reversion_depth") == method["inverse_reversion_depth"] == 192,
        "unexpected reversion depth",
    )
    require(result.get("claim_boundary") == preregistration["claim_boundary"], "claim boundary drift")

    sealed = datetime.fromisoformat(lock["sealed_utc"])
    started = datetime.fromisoformat(result["started_utc"])
    completed = datetime.fromisoformat(result["completed_utc"])
    require(sealed <= started <= completed, "degree-32 timestamps violate prospective order")
    require(result.get("elapsed_seconds", -1) >= 0, "invalid elapsed time")

    records = result.get("records", [])
    killed_classes = object_spec["killed_classes_tested"]
    require([record.get("killed_class") for record in records] == killed_classes, "killed-class coverage mismatch")
    candidate_classes = set(object_spec["candidate_support_classes"])
    for record in records:
        killed = record["killed_class"]
        require(record.get("allowed_classes") == sorted(candidate_classes - {killed}), "allowed-class mismatch")
        require(record.get("condition_count") == 6, "secondary condition-count prediction failed")
        orders = record.get("condition_orders", [])
        require(len(orders) == 6 and len(set(orders)) == 6, "condition-order coverage mismatch")
        require(
            all((1 - order) % 32 == killed and order <= 192 for order in orders),
            "condition order has the wrong residue class or exceeds the frozen depth",
        )
        require(record.get("empty_after_gamma_saturation") is True, "nonempty saturated locus recorded")
        require(record.get("saturated_basis") == ["1"], "unit-ideal certificate missing")

    primary = all(record["empty_after_gamma_saturation"] for record in records)
    secondary = all(record["condition_count"] == 6 for record in records)
    adjudication = "confirmed" if primary and secondary else "mixed" if primary else "falsified"
    require(result.get("primary_prediction_confirmed") is primary, "primary adjudication mismatch")
    require(result.get("secondary_prediction_confirmed") is secondary, "secondary adjudication mismatch")
    require(result.get("adjudication") == adjudication == "confirmed", "degree-32 adjudication mismatch")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preregistration", type=Path, default=ROOT / "experiments" / "degree32_preregistration.json")
    parser.add_argument("--lock", type=Path, default=ROOT / "experiments" / "degree32_preregistration_lock.json")
    parser.add_argument("--runner", type=Path, default=ROOT / "experiments" / "degree32_quartic_lift.py")
    parser.add_argument("--result", type=Path, default=ROOT / "receipts" / "degree32_quartic_lift_result.json")
    args = parser.parse_args()
    result = verify(args.preregistration, args.lock, args.runner, args.result)
    print(json.dumps({
        "status": "pass",
        "adjudication": result["adjudication"],
        "degree": result["degree"],
        "result_sha256": result["result_sha256"],
        "experiment_recomputed": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
