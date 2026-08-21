#!/usr/bin/env python3
"""Exact scalar-ODE oracle for polynomial exponential periods.

For trusted rational input ``P in Q[x]``, this module computes the canonical
inverse support of the affine-normalised phase and an exact scalar differential
operator annihilating every rapid-decay period

    I_Gamma(s) = integral_Gamma exp(s P(x)) dx.

The operator comes directly from the first Krylov dependence in the twisted
de Rham quotient.  Its order is minimal for a generic functional on the
complete period solution space.  A particular contour may annihilate an
active channel and therefore satisfy an equation of smaller order.

The parser is intentionally for trusted research input.  It is not a safe
service boundary for arbitrary expressions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

import sympy as sp

from fusion_support import (
    K,
    analyse_phase,
    canonical_expr,
    canonical_hash,
    coordinate_column,
    first_dependence,
    parse_polynomial,
    require,
    s,
    x,
)


SCHEMA = "exponential-period-order-oracle-certificate-v1"


def _matrix_sha256(matrix: sp.Matrix) -> str:
    values = [canonical_expr(value) for value in matrix]
    payload = json.dumps(values, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _pivot_solution(matrix: sp.Matrix, rank: int) -> tuple[list[int], sp.Matrix]:
    """Solve the first dependence using a deterministic nonsingular minor."""

    require(rank < matrix.cols, "operator derivation needs a dependent Krylov column")
    basis = matrix[:, :rank]
    target = matrix[:, rank]
    _rref, pivot_rows = basis.T.rref()
    rows = list(pivot_rows)
    require(len(rows) == rank, "failed to select a full-rank Krylov minor")
    square = basis.extract(rows, range(rank))
    rhs = target.extract(rows, [0])
    solution = square.inv() * rhs
    residual = basis * solution - target
    require(
        all(sp.cancel(value) == 0 for value in residual),
        "first Krylov dependence has a nonzero exact residual",
    )
    return rows, solution


def _operator_krylov_matrix(phase: sp.Poly) -> sp.Matrix:
    """Return columns ``[1],...,[P^(d-1)]``, including one dependence."""

    ambient_rank = phase.degree() - 1
    phase_k = sp.Poly(phase.as_expr(), x, domain=K)
    iterate = sp.Poly(1, x, domain=K)
    columns: list[sp.Matrix] = []
    for _ in range(ambient_rank + 1):
        columns.append(coordinate_column(iterate, phase))
        iterate *= phase_k
    return sp.Matrix.hstack(*columns)


def _lcm_polynomial_denominators(expressions: Iterable[sp.Expr]) -> sp.Poly:
    common = sp.Poly(1, s, domain=sp.QQ)
    for expression in expressions:
        _numerator, denominator = sp.fraction(sp.cancel(expression))
        denominator_poly = sp.Poly(denominator, s, domain=sp.QQ)
        common = sp.lcm(common, denominator_poly)
    return common


def _primitive_integer_coefficients(expressions: list[sp.Expr]) -> list[sp.Expr]:
    """Return a deterministic primitive integer polynomial coefficient list."""

    denominator = _lcm_polynomial_denominators(expressions)
    polynomial_expressions: list[sp.Expr] = []
    for expression in expressions:
        cleared = sp.cancel(denominator.as_expr() * expression)
        try:
            polynomial = sp.Poly(cleared, s, domain=sp.QQ)
        except sp.PolynomialError as error:
            raise RuntimeError("failed to clear operator denominator") from error
        polynomial_expressions.append(sp.expand(polynomial.as_expr()))

    nonzero_polynomials = [
        sp.Poly(expression, s, domain=sp.QQ)
        for expression in polynomial_expressions
        if expression != 0
    ]
    require(nonzero_polynomials, "zero differential operator")

    common_factor = nonzero_polynomials[0]
    for polynomial in nonzero_polynomials[1:]:
        common_factor = sp.gcd(common_factor, polynomial)
    if common_factor.degree() >= 0:
        polynomial_expressions = [
            sp.cancel(expression / common_factor.as_expr())
            for expression in polynomial_expressions
        ]

    rational_coefficients = [
        sp.Rational(coefficient)
        for expression in polynomial_expressions
        for coefficient in sp.Poly(expression, s, domain=sp.QQ).all_coeffs()
    ]
    scalar_denominator = 1
    for coefficient in rational_coefficients:
        scalar_denominator = sp.ilcm(scalar_denominator, int(coefficient.q))
    integer_expressions = [
        sp.expand(scalar_denominator * expression)
        for expression in polynomial_expressions
    ]

    integer_values = [
        abs(int(coefficient))
        for expression in integer_expressions
        for coefficient in sp.Poly(expression, s, domain=sp.ZZ).all_coeffs()
        if coefficient != 0
    ]
    scalar_gcd = 0
    for value in integer_values:
        scalar_gcd = math.gcd(scalar_gcd, value)
    require(scalar_gcd >= 1, "failed to primitive-normalise operator")
    primitive = [sp.expand(expression / scalar_gcd) for expression in integer_expressions]

    highest_derivative = sp.Poly(primitive[-1], s, domain=sp.ZZ)
    if highest_derivative.LC() < 0:
        primitive = [-expression for expression in primitive]
    return primitive


def exact_scalar_operator(phase: sp.Poly) -> dict[str, Any]:
    """Derive and exactly verify the primitive scalar operator for ``phase``."""

    matrix = _operator_krylov_matrix(phase)
    order = first_dependence(matrix)
    require(order >= 1, "the constant seed must have positive cyclic rank")
    require(order < matrix.cols, "ambient Krylov matrix did not include a dependence")
    pivot_rows, solution = _pivot_solution(matrix, order)

    # [P^order dx] = sum_i solution[i] [P^i dx].  Period pairing turns
    # [P^j dx] into the j-th s derivative, so the raw operator is
    # D^order - sum_i solution[i] D^i.
    rational_coefficients = [-sp.cancel(value) for value in solution] + [sp.Integer(1)]
    coefficients = _primitive_integer_coefficients(rational_coefficients)

    residual = sp.zeros(matrix.rows, 1)
    for derivative_order, coefficient in enumerate(coefficients):
        residual += matrix[:, derivative_order] * coefficient
    require(
        all(sp.cancel(value) == 0 for value in residual),
        "primitive scalar operator has a nonzero exact residual",
    )

    coefficient_strings = [canonical_expr(value) for value in coefficients]
    return {
        "order": order,
        "independent_variable": "s",
        "derivation_symbol": "D_s",
        "coefficient_order": "low_derivative_to_high_derivative",
        "coefficients": coefficient_strings,
        "equation": "sum_{j=0}^q coefficients[j] * I^(j)(s) = 0",
        "leading_derivative_coefficient": coefficient_strings[-1],
        "primitive_integer_polynomial_coefficients": True,
        "pivot_rows_zero_based": pivot_rows,
        "exact_krylov_residual_zero": True,
        "original_phase_krylov_matrix_sha256": _matrix_sha256(matrix),
    }


def order_oracle_certificate(phase_text: str) -> dict[str, Any]:
    """Return the exact order/support/operator certificate for ``phase_text``."""

    original = parse_polynomial(phase_text)
    support_analysis = analyse_phase(phase_text)
    operator = exact_scalar_operator(original)
    predicted_order = support_analysis["theorem_identity"]["inverse_support_size"]
    require(
        operator["order"] == predicted_order,
        "original-phase operator order disagrees with normalised inverse support",
    )

    result = {
        "schema": SCHEMA,
        "status": "pass",
        "input": {"phase": phase_text},
        "input_sha256": canonical_hash({"phase": phase_text}),
        "degree": original.degree(),
        "normalisation": support_analysis["normalisation"],
        "order_prediction": {
            "generic_minimal_order": predicted_order,
            "inverse_support": support_analysis["inverse_at_infinity"]["support"],
            "inverse_support_size": predicted_order,
            "twisted_cyclic_rank": support_analysis["theorem_identity"][
                "twisted_cyclic_rank"
            ],
            "reduced_root_span_dimension": support_analysis["theorem_identity"][
                "reduced_root_span_dimension"
            ],
            "all_equal": support_analysis["theorem_identity"]["all_equal"],
        },
        "scalar_operator_for_original_phase": operator,
        "minimality_certificate_for_normalised_phase": support_analysis["twisted_krylov"],
        "inverse_at_infinity_certificate": support_analysis["inverse_at_infinity"],
        "claim_boundary": {
            "annihilation": (
                "The displayed operator annihilates every rapid-decay period "
                "I_Gamma(s)=integral_Gamma exp(sP(x)) dx."
            ),
            "minimality": (
                "Its order is minimal for a generic functional on the complete "
                "period solution space; a particular cycle may have lower order."
            ),
            "input": "Trusted rational polynomial expressions only.",
            "not_established": [
                "that an arbitrary contour is rapid-decay",
                "minimality for every individual cycle",
                "novelty, priority, specialist review, or independent reproduction",
            ],
        },
    }
    result["certificate_sha256"] = canonical_hash(result)
    return result


def verify_order_oracle_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    """Fail closed on any certificate mutation or recomputation mismatch."""

    require(isinstance(certificate, dict), "certificate must be a JSON object")
    require(certificate.get("schema") == SCHEMA, "unknown oracle certificate schema")
    supplied_digest = certificate.get("certificate_sha256")
    require(isinstance(supplied_digest, str), "certificate digest is missing")
    unhashed = dict(certificate)
    unhashed.pop("certificate_sha256", None)
    require(canonical_hash(unhashed) == supplied_digest, "certificate digest mismatch")
    phase = certificate.get("input", {}).get("phase")
    require(isinstance(phase, str), "certificate phase is missing")
    recomputed = order_oracle_certificate(phase)
    require(recomputed == certificate, "certificate differs from exact recomputation")
    return {
        "schema": "exponential-period-order-oracle-verification-v1",
        "status": "pass",
        "certificate_sha256": supplied_digest,
        "phase": phase,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--phase", help="trusted Q[x] expression")
    action.add_argument("--verify-certificate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    if args.verify_certificate:
        supplied = json.loads(args.verify_certificate.read_text(encoding="utf-8"))
        result = verify_order_oracle_certificate(supplied)
    else:
        result = order_oracle_certificate(args.phase)
    if args.compact:
        encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    else:
        encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
