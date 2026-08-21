#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fusion_support import canonical_hash  # noqa: E402
from order_oracle import (  # noqa: E402
    order_oracle_certificate,
    verify_order_oracle_certificate,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def require_raises(action, expected_fragment: str) -> None:
    try:
        action()
    except Exception as error:  # the boundary is deliberately fail-closed
        require(expected_fragment in str(error), f"unexpected error: {error}")
        return
    raise RuntimeError(f"expected failure containing: {expected_fragment}")


def main() -> None:
    spec = json.loads((ROOT / "benchmarks" / "order_oracle_cases.json").read_text())
    certificates = {}
    for case in spec["cases"]:
        certificate = order_oracle_certificate(case["phase"])
        certificates[case["id"]] = certificate
        prediction = certificate["order_prediction"]
        operator = certificate["scalar_operator_for_original_phase"]
        require(certificate["status"] == "pass", f"status failed: {case['id']}")
        require(certificate["degree"] == case["expected_degree"], f"degree failed: {case['id']}")
        require(
            prediction["generic_minimal_order"] == case["expected_order"],
            f"order failed: {case['id']}",
        )
        require(prediction["inverse_support"] == case["expected_support"],
                f"support failed: {case['id']}")
        require(operator["order"] == case["expected_order"], f"operator order failed: {case['id']}")
        require(operator["exact_krylov_residual_zero"] is True,
                f"operator residual failed: {case['id']}")
        require(operator["primitive_integer_polynomial_coefficients"] is True,
                f"primitive operator failed: {case['id']}")
        require(len(operator["coefficients"]) == case["expected_order"] + 1,
                f"coefficient count failed: {case['id']}")
        verify_order_oracle_certificate(certificate)

    power = certificates["power_degree_7"]
    require(
        power["scalar_operator_for_original_phase"]["coefficients"] == ["1", "7*s"],
        "x^7 anchor must give I + 7s I' = 0",
    )

    # The order/support are affine invariants, while the displayed operator is
    # intentionally for the original, unnormalised phase.
    base = order_oracle_certificate("x**4+x")
    affine = order_oracle_certificate("3*((x+2)**4+(x+2))+5")
    require(base["order_prediction"] == affine["order_prediction"],
            "affine order/support invariance failed")
    require(
        base["scalar_operator_for_original_phase"]["coefficients"]
        != affine["scalar_operator_for_original_phase"]["coefficients"],
        "original-phase operator must retain target gauge/scaling data",
    )

    corrupted = deepcopy(base)
    corrupted["scalar_operator_for_original_phase"]["coefficients"][0] = "0"
    require_raises(
        lambda: verify_order_oracle_certificate(corrupted),
        "certificate digest mismatch",
    )

    forged = deepcopy(corrupted)
    forged_without_digest = dict(forged)
    forged_without_digest.pop("certificate_sha256")
    forged["certificate_sha256"] = canonical_hash(forged_without_digest)
    require_raises(
        lambda: verify_order_oracle_certificate(forged),
        "certificate differs from exact recomputation",
    )

    require_raises(lambda: order_oracle_certificate("x + 1"), "degree must be at least two")
    require_raises(lambda: order_oracle_certificate("sin(x)"), "phase must lie in Q[x]")
    require_raises(lambda: order_oracle_certificate("x**3 + pi*x"), "phase must lie in Q[x]")

    print(
        "order-oracle tests passed: eight benchmarks, affine covariance, "
        "known anchor, certificate mutations, and parser failures"
    )


if __name__ == "__main__":
    main()
