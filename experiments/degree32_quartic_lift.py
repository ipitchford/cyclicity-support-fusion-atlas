#!/usr/bin/env python3
"""Sealed prospective m=8 quartic-lift elimination."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any

import sympy as sp
from sympy import QQ
from sympy.polys.rings import ring


ROOT = Path(__file__).resolve().parents[1]
VERIFICATION = ROOT / "verification"
sys.path.insert(0, str(VERIFICATION))

from symconstr import (  # noqa: E402
    compose_ring,
    conds_to_exprs,
    reversion_given_p,
    reduces_to_zero,
    staircase_dim,
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def verify_seal(preregistration: Path, lock_path: Path) -> dict[str, Any]:
    lock = json.loads(lock_path.read_text())
    if lock.get("schema") != "degree32-preregistration-lock-v1":
        raise RuntimeError("unknown preregistration lock schema")
    checks = {
        "preregistration_sha256": sha256_path(preregistration),
        "runner_sha256": sha256_path(Path(__file__).resolve()),
    }
    for key, observed in checks.items():
        if lock.get(key) != observed:
            raise RuntimeError(f"sealed {key} mismatch: {observed} != {lock.get(key)}")
    return lock


def run_killed_class(m: int, killed_class: int, depth: int) -> dict[str, Any]:
    degree = 4 * m
    coefficient_ring = ring("beta,gamma,b", QQ)[0]
    beta, gamma, b = coefficient_ring.gens
    outer = [coefficient_ring.zero, gamma, beta, coefficient_ring.zero, coefficient_ring.one]
    inner = [coefficient_ring.zero] * (m + 1)
    inner[0] = b
    inner[m] = coefficient_ring.one
    phase = compose_ring(outer, inner, coefficient_ring)[: degree + 1]
    if phase[degree] != coefficient_ring.one or phase[degree - 1] != coefficient_ring.zero:
        raise RuntimeError("symbolic quartic lift is not monic and centred")
    coefficients = {index: phase[index] for index in range(degree - 1)}
    coefficients[0] = coefficient_ring.zero
    full_classes = {1, m + 1, 2 * m + 1, 3 * m + 1}
    allowed = frozenset(full_classes - {killed_class})
    _series, conditions = reversion_given_p(
        degree, coefficients, depth, coefficient_ring, S=allowed
    )
    for order, _condition in conditions:
        observed_class = (1 - order) % degree
        if observed_class != killed_class:
            raise RuntimeError(
                f"condition class mismatch at order {order}: {observed_class} != {killed_class}"
            )
    expressions, symbols = conds_to_exprs(conditions, coefficient_ring)
    sbeta, sgamma, sb = symbols
    w = sp.Symbol("w")
    saturated = sp.groebner(
        expressions + [w * sgamma - 1],
        sbeta,
        sgamma,
        sb,
        w,
        order="grevlex",
        domain="QQ",
    )
    empty = len(saturated.exprs) == 1 and saturated.exprs[0] == 1
    result = {
        "killed_class": killed_class,
        "allowed_classes": sorted(allowed),
        "condition_count": len(conditions),
        "condition_orders": [order for order, _condition in conditions],
        "conditions_sha256": canonical_hash(
            [sp.sstr(sp.factor(expression)) for expression in expressions]
        ),
        "empty_after_gamma_saturation": empty,
        "saturated_basis": [sp.sstr(sp.factor(value)) for value in saturated.exprs],
    }
    if not empty:
        unsaturated = sp.groebner(
            expressions, sbeta, sgamma, sb, order="grevlex", domain="QQ"
        )
        result.update({
            "unsaturated_dimension": staircase_dim(unsaturated, [sbeta, sgamma, sb]),
            "unsaturated_basis": [sp.sstr(sp.factor(value)) for value in unsaturated.exprs],
            "saturated_basis_first_six": [
                sp.sstr(sp.factor(value)) for value in saturated.exprs[:6]
            ],
        })
        # A nonempty finding gets a fixed, preregistered 8d stability check.
        _series2, conditions2 = reversion_given_p(
            degree, coefficients, 8 * degree, coefficient_ring, S=allowed
        )
        high = [(order, value) for order, value in conditions2 if order > depth]
        high_expressions, _ = conds_to_exprs(high, coefficient_ring)
        result["stable_through_8d"] = all(
            reduces_to_zero(expression, unsaturated) for expression in high_expressions
        )
        result["additional_condition_count_through_8d"] = len(high)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preregistration",
        type=Path,
        default=ROOT / "experiments" / "degree32_preregistration.json",
    )
    parser.add_argument(
        "--lock",
        type=Path,
        default=ROOT / "experiments" / "degree32_preregistration_lock.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "receipts" / "degree32_quartic_lift_result.json",
    )
    args = parser.parse_args()
    lock = verify_seal(args.preregistration, args.lock)
    preregistration = json.loads(args.preregistration.read_text())
    m = preregistration["object"]["m"]
    degree = preregistration["object"]["degree"]
    depth = preregistration["method"]["inverse_reversion_depth"]
    killed_classes = preregistration["object"]["killed_classes_tested"]
    if (m, degree, depth, killed_classes) != (8, 32, 192, [9, 17, 25]):
        raise RuntimeError("sealed preregistration does not match the runner contract")

    started = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()
    records = [run_killed_class(m, killed_class, depth) for killed_class in killed_classes]
    primary_confirmed = all(record["empty_after_gamma_saturation"] for record in records)
    secondary_confirmed = all(record["condition_count"] == 6 for record in records)
    if primary_confirmed and secondary_confirmed:
        adjudication = "confirmed"
    elif primary_confirmed:
        adjudication = "mixed"
    else:
        adjudication = "falsified"
    result = {
        "schema": "degree32-quartic-lift-result-v1",
        "status": "complete",
        "adjudication": adjudication,
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.perf_counter() - t0,
        "seal": lock,
        "m": m,
        "degree": degree,
        "inverse_reversion_depth": depth,
        "primary_prediction_confirmed": primary_confirmed,
        "secondary_prediction_confirmed": secondary_confirmed,
        "records": records,
        "claim_boundary": preregistration["claim_boundary"],
    }
    result["result_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "adjudication": adjudication,
        "primary_prediction_confirmed": primary_confirmed,
        "secondary_prediction_confirmed": secondary_confirmed,
        "elapsed_seconds": result["elapsed_seconds"],
        "result_sha256": result["result_sha256"],
    }, indent=2))
    return 0 if adjudication in {"confirmed", "mixed", "falsified"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
