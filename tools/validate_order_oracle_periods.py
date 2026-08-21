#!/usr/bin/env python3
"""Numerical real-line spot checks for selected exact order-oracle operators.

These quadrature checks are deliberately separate from the exact certificate
builder.  They test the period dictionary on convergent real-line examples;
they are not used as proof of the operator relation or of minimality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from mpmath import mp
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fusion_support import parse_polynomial, require, s  # noqa: E402
from order_oracle import order_oracle_certificate  # noqa: E402


def rational_text(value: Any) -> str:
    return str(sp.Rational(str(value)))


def validate_case(case: dict[str, Any], dps: int, threshold: mp.mpf) -> list[dict[str, Any]]:
    phase = parse_polynomial(case["phase"])
    require(phase.degree() % 2 == 0, f"real-line case must have even degree: {case['id']}")
    require(phase.LC() > 0, f"real-line case must have positive leading term: {case['id']}")
    certificate = order_oracle_certificate(case["phase"])
    operator = certificate["scalar_operator_for_original_phase"]
    order = operator["order"]
    symbolic_coefficients = [
        sp.sympify(value, locals={"s": s}) for value in operator["coefficients"]
    ]
    polynomial_coefficients = [
        mp.mpf(str(phase.nth(power))) for power in range(phase.degree() + 1)
    ]

    def evaluate_phase(point: mp.mpf) -> mp.mpf:
        result = mp.mpf("0")
        for coefficient in reversed(polynomial_coefficients):
            result = result * point + coefficient
        return result

    records: list[dict[str, Any]] = []
    mp.dps = dps
    for supplied_s in case["numeric_real_line_s"]:
        exact_s = sp.Rational(str(supplied_s))
        require(exact_s < 0, f"real-line validation requires s < 0: {case['id']}")
        numeric_s = mp.mpf(exact_s.p) / mp.mpf(exact_s.q)
        derivatives: list[mp.mpf] = []
        for derivative_order in range(order + 1):
            def integrand(point: mp.mpf, j: int = derivative_order) -> mp.mpf:
                value = evaluate_phase(point)
                return value**j * mp.exp(numeric_s * value)

            derivatives.append(
                mp.quad(
                    integrand,
                    [-mp.inf, -3, -2, -1, 0, 1, 2, 3, mp.inf],
                )
            )

        evaluated_coefficients = [
            mp.mpf(str(sp.N(value.subs(s, exact_s), dps)))
            for value in symbolic_coefficients
        ]
        terms = [
            evaluated_coefficients[index] * derivatives[index]
            for index in range(order + 1)
        ]
        scale = max(abs(term) for term in terms)
        require(scale > 0, f"zero numerical scale: {case['id']}")
        relative_residual = abs(mp.fsum(terms)) / scale
        require(
            relative_residual <= threshold,
            f"quadrature residual too large for {case['id']} at s={exact_s}: "
            f"{mp.nstr(relative_residual, 12)}",
        )
        records.append(
            {
                "id": case["id"],
                "s": rational_text(supplied_s),
                "order": order,
                "relative_residual": mp.nstr(relative_residual, 20),
                "threshold": mp.nstr(threshold, 5),
                "status": "pass",
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        type=Path,
        default=ROOT / "benchmarks" / "order_oracle_cases.json",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dps", type=int, default=60)
    parser.add_argument("--threshold", default="1e-12")
    args = parser.parse_args()

    require(args.dps >= 30, "at least 30 decimal digits are required")
    threshold = mp.mpf(args.threshold)
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = []
    for case in spec["cases"]:
        if "numeric_real_line_s" in case:
            records.extend(validate_case(case, args.dps, threshold))

    result = {
        "schema": "exponential-period-order-oracle-numerical-spotcheck-v1",
        "status": "pass",
        "decimal_precision": args.dps,
        "record_count": len(records),
        "records": records,
        "claim_boundary": (
            "Numerical real-line quadrature spot control; not theorem evidence, "
            "not an independent implementation, and not a minimality proof."
        ),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
