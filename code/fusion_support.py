#!/usr/bin/env python3
"""Exact support and block-fusion certificates for polynomial exponential periods.

For a rational polynomial P of degree d >= 2, the program:

1. affinely normalises P to monic, centred, zero-constant form;
2. computes the exact fixed-seed cyclic rank q(P, dx) in the twisted quotient

       Q(s)[x] dx / (d/dx + s P'(x)) Q(s)[x] dx;

3. expands the unique inverse-at-infinity series xi(t) satisfying

       P(xi(t)) = t**d,   xi(t) = t + O(t**-1),

   until q distinct non-zero residue classes modulo d have appeared;
4. returns the canonical support Sigma(P), coefficient witnesses, and the
   fusion profile for every divisor m of d.  A divisor profile applies to a
   decomposition P = R o Q when deg(Q) = m.

The stopping rule is exact because the accompanying theorem proves
q(P, dx) = |Sigma(P)|.  The program handles trusted Q[x] research input; it is
not an untrusted-input parser and does not find polynomial decompositions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import sympy as sp

x, s = sp.symbols("x s")
K = sp.QQ.frac_field(s)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_expr(value: sp.Expr) -> str:
    return sp.sstr(sp.factor(sp.cancel(value)))


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_polynomial(text: str) -> sp.Poly:
    require(isinstance(text, str), "phase must be a string")
    expr = sp.expand(sp.sympify(text, locals={"x": x}))
    require(expr.free_symbols <= {x}, "phase must lie in Q[x]")
    try:
        poly = sp.Poly(expr, x, domain=sp.QQ)
    except (sp.PolynomialError, sp.CoercionFailed) as error:
        raise RuntimeError("phase must lie in Q[x]") from error
    require(poly.degree() >= 2, "phase degree must be at least two")
    return poly


@dataclass(frozen=True)
class Normalisation:
    original: sp.Poly
    normalised: sp.Poly
    source_shift: sp.Rational
    target_shift_before_scaling: sp.Rational
    target_scale: sp.Rational

    def as_dict(self) -> dict[str, str]:
        return {
            "original": sp.sstr(self.original.as_expr()),
            "normalised": sp.sstr(self.normalised.as_expr()),
            "source_change": f"x_old = x_new - ({self.source_shift})",
            "target_shift_before_scaling": sp.sstr(
                self.target_shift_before_scaling
            ),
            "target_scale_divisor": sp.sstr(self.target_scale),
        }


def normalise_phase(poly: sp.Poly) -> Normalisation:
    """Return a monic, centred, zero-constant affine normal form.

    If a_d is the leading coefficient and a_{d-1} the next coefficient, put
    x_old = x_new - a_{d-1}/(d a_d), then subtract the resulting constant and
    divide by a_d.  These source/target affine changes preserve cyclic rank,
    reduced root-span dimension, and support fibre cardinalities.
    """

    d = poly.degree()
    leading = sp.Rational(poly.LC())
    next_coefficient = sp.Rational(poly.nth(d - 1))
    shift = sp.cancel(next_coefficient / (d * leading))
    centred_expr = sp.expand(poly.as_expr().subs(x, x - shift))
    centred = sp.Poly(centred_expr, x, domain=sp.QQ)
    constant = sp.Rational(centred.nth(0))
    normalised_expr = sp.expand((centred.as_expr() - constant) / leading)
    normalised = sp.Poly(normalised_expr, x, domain=sp.QQ)
    require(normalised.LC() == 1, "normalisation failed to make phase monic")
    require(
        normalised.nth(d - 1) == 0,
        "normalisation failed to centre the phase",
    )
    require(
        normalised.nth(0) == 0,
        "normalisation failed to remove the target constant",
    )
    return Normalisation(poly, normalised, shift, constant, leading)


def reduce_twisted(polynomial: sp.Poly, phase: sp.Poly) -> sp.Poly:
    """Unique representative of degree below deg(P)-1 over Q(s)."""

    phase_k = sp.Poly(phase.as_expr(), x, domain=K)
    derivative = phase_k.diff()
    d = phase.degree()
    leading = derivative.LC()
    lower = derivative - sp.Poly(leading * x ** (d - 1), x, domain=K)
    reduced = sp.Poly(polynomial.as_expr(), x, domain=K)

    while not reduced.is_zero and reduced.degree() >= d - 1:
        degree = reduced.degree()
        coefficient = reduced.LC()
        shift = degree - (d - 1)
        derivative_term = shift * x ** (shift - 1) if shift else sp.S.Zero
        tail = sp.Poly(
            derivative_term + s * x**shift * lower.as_expr(),
            x,
            domain=K,
        )
        reduced = (
            reduced
            - sp.Poly(coefficient * x**degree, x, domain=K)
            + tail.mul_ground(-coefficient / (s * leading))
        )
    return reduced


def coordinate_column(polynomial: sp.Poly, phase: sp.Poly) -> sp.Matrix:
    ambient_rank = phase.degree() - 1
    reduced = reduce_twisted(polynomial, phase)
    return sp.Matrix(
        [sp.cancel(reduced.nth(power)) for power in range(ambient_rank)]
    )


def krylov_matrix(phase: sp.Poly) -> sp.Matrix:
    """Columns are [1], [P], ..., [P^(d-2)] in the twisted quotient."""

    ambient_rank = phase.degree() - 1
    phase_k = sp.Poly(phase.as_expr(), x, domain=K)
    iterate = sp.Poly(1, x, domain=K)
    columns: list[sp.Matrix] = []
    for _ in range(ambient_rank):
        columns.append(coordinate_column(iterate, phase))
        iterate *= phase_k
    return sp.Matrix.hstack(*columns)


def first_dependence(matrix: sp.Matrix) -> int:
    for count in range(1, matrix.cols + 1):
        if matrix[:, :count].rank() < count:
            return count - 1
    return matrix.cols


def independence_certificate(matrix: sp.Matrix, rank: int) -> dict[str, Any]:
    require(rank >= 1, "the constant seed has positive rank")
    basis = matrix[:, :rank]
    _rref, pivot_rows = basis.T.rref()
    rows = list(pivot_rows)
    require(len(rows) == rank, "failed to select a full-rank minor")
    minor = sp.factor(basis.extract(rows, range(rank)).det())
    require(minor != 0, "independence minor vanished")
    numerator, denominator = sp.fraction(sp.cancel(minor))
    return {
        "pivot_rows_zero_based": rows,
        "minor_numerator": canonical_expr(numerator),
        "minor_denominator": canonical_expr(denominator),
        "minor_is_nonzero": True,
    }


def dependence_certificate(matrix: sp.Matrix, rank: int) -> dict[str, Any] | None:
    if rank == matrix.cols:
        return None
    basis = matrix[:, :rank]
    target = matrix[:, rank]
    _rref, pivot_rows = basis.T.rref()
    rows = list(pivot_rows)
    square = basis.extract(rows, range(rank))
    rhs = target.extract(rows, [0])
    coefficients = square.inv() * rhs
    residual = basis * coefficients - target
    residual_values = [sp.cancel(value) for value in residual]
    require(all(value == 0 for value in residual_values), "nonzero residual")
    return {
        "dependent_iterate": rank,
        "orientation": "[P^q dx] = sum_i coefficient[i] [P^i dx]",
        "coefficients_low_to_high": [
            canonical_expr(value) for value in coefficients
        ],
        "residual_is_zero": True,
    }


def cyclic_rank_certificate(phase: sp.Poly) -> tuple[int, dict[str, Any]]:
    matrix = krylov_matrix(phase)
    rank = first_dependence(matrix)
    payload = [canonical_expr(value) for value in matrix]
    return rank, {
        "ambient_rank": phase.degree() - 1,
        "cyclic_rank": rank,
        "matrix_shape": list(matrix.shape),
        "matrix_sha256": canonical_hash(payload),
        "independence": independence_certificate(matrix, rank),
        "first_dependence": dependence_certificate(matrix, rank),
    }


def truncated_convolution(
    left: list[sp.Rational], right: list[sp.Rational], degree: int
) -> list[sp.Rational]:
    result = [sp.Rational(0) for _ in range(degree + 1)]
    for i, a in enumerate(left):
        if a == 0 or i > degree:
            continue
        upper = min(len(right) - 1, degree - i)
        for j in range(upper + 1):
            b = right[j]
            if b:
                result[i + j] += a * b
    return result


def power_coefficient(
    coefficients: list[sp.Rational], exponent: int, degree: int
) -> sp.Rational:
    """Coefficient of y^degree in F(y)^exponent, truncated exactly."""

    if exponent == 0:
        return sp.Rational(1) if degree == 0 else sp.Rational(0)
    result = [sp.Rational(1)] + [sp.Rational(0)] * degree
    base = coefficients + [sp.Rational(0)] * (degree + 1 - len(coefficients))
    power = exponent
    while power:
        if power & 1:
            result = truncated_convolution(result, base, degree)
        power >>= 1
        if power:
            base = truncated_convolution(base, base, degree)
    return result[degree]


def next_inverse_coefficient(
    phase: sp.Poly, coefficients: list[sp.Rational], degree: int
) -> sp.Rational:
    """Solve recursively for [y^degree] F in P(F/y)=y^-d.

    The phase is monic and centred.  Writing xi=tF(1/t), the equation is

        F^d + sum_{k<d} p_k y^(d-k) F^k = 1.

    At order degree the unknown coefficient enters only through d*c_degree.
    """

    d = phase.degree()
    known = power_coefficient(coefficients, d, degree)
    for k in range(d):
        coefficient = sp.Rational(phase.nth(k))
        if coefficient == 0:
            continue
        shift = d - k
        if degree >= shift:
            known += coefficient * power_coefficient(
                coefficients, k, degree - shift
            )
    return sp.factor(-known / d)


def inverse_support_certificate(
    phase: sp.Poly, cyclic_rank: int, max_terms: int = 10000
) -> dict[str, Any]:
    """Expand xi until cyclic_rank distinct non-trace residues are witnessed."""

    d = phase.degree()
    coefficients: list[sp.Rational] = [sp.Rational(1)]  # F(0)=1
    support: set[int] = {1 % d}
    witnesses: dict[int, dict[str, Any]] = {
        1 % d: {"t_exponent": 1, "coefficient": "1", "series_order": 0}
    }
    nonzero_terms: list[dict[str, Any]] = [
        {"t_exponent": 1, "coefficient": "1", "residue_mod_degree": 1 % d}
    ]

    if cyclic_rank == 1:
        return {
            "support": [1 % d],
            "support_size": 1,
            "terms_computed": 0,
            "witnesses": {str(key): value for key, value in witnesses.items()},
            "nonzero_terms_through_stopping_order": nonzero_terms,
            "stopping_rule": "support_size equals exact twisted cyclic rank",
        }

    for order in range(1, max_terms + 1):
        coefficient = next_inverse_coefficient(phase, coefficients, order)
        coefficients.append(sp.Rational(coefficient))
        exponent = 1 - order
        if coefficient != 0:
            residue = exponent % d
            nonzero_terms.append(
                {
                    "t_exponent": exponent,
                    "coefficient": canonical_expr(coefficient),
                    "residue_mod_degree": residue,
                }
            )
            require(
                residue != 0,
                "a trace residue appeared after centring; normalisation failed",
            )
            support.add(residue)
            witnesses.setdefault(
                residue,
                {
                    "t_exponent": exponent,
                    "coefficient": canonical_expr(coefficient),
                    "series_order": order,
                },
            )
        if len(support) == cyclic_rank:
            ordered = sorted(support)
            return {
                "support": ordered,
                "support_size": len(ordered),
                "terms_computed": order,
                "witnesses": {
                    str(key): witnesses[key] for key in sorted(witnesses)
                },
                "nonzero_terms_through_stopping_order": nonzero_terms,
                "stopping_rule": "support_size equals exact twisted cyclic rank",
            }
    raise RuntimeError(
        f"failed to witness {cyclic_rank} support classes in {max_terms} terms"
    )


def divisors(number: int) -> list[int]:
    return [value for value in range(1, number + 1) if number % value == 0]


def block_fusion_profile(
    support: Iterable[int], degree: int, right_degree: int
) -> dict[str, Any]:
    require(degree % right_degree == 0, "right degree must divide total degree")
    m = right_degree
    n = degree // m
    sigma = sorted({int(value) % degree for value in support})
    fibres: dict[int, list[int]] = {}
    for residue in sigma:
        c = residue % m
        ell = ((residue - c) // m) % n
        fibres.setdefault(c, []).append(ell)
    for values in fibres.values():
        values.sort()

    stabilizer: list[int] = []
    for delta in range(n):
        valid = True
        for values in fibres.values():
            base = values[0]
            if any((delta * (value - base)) % n != 0 for value in values[1:]):
                valid = False
                break
        if valid:
            stabilizer.append(delta)

    pairwise_intersection: dict[str, int] = {}
    for delta in range(n):
        dimension = 0
        for values in fibres.values():
            base = values[0]
            if all((delta * (value - base)) % n == 0 for value in values[1:]):
                dimension += 1
        pairwise_intersection[str(delta)] = dimension

    profile = sorted((len(values) for values in fibres.values()), reverse=True)
    return {
        "total_degree": degree,
        "right_factor_degree_m": m,
        "outer_degree_n": n,
        "support": sigma,
        "fibres_L_c": {str(key): value for key, value in sorted(fibres.items())},
        "fibre_size_partition": profile,
        "right_factor_cyclic_rank": len(fibres),
        "global_cyclic_rank": len(sigma),
        "each_block_span_dimension": len(fibres),
        "full_fusion_all_block_spans_equal": all(size == 1 for size in profile),
        "block_spans_form_direct_sum": all(size == n for size in profile),
        "equality_stabilizer_H": stabilizer,
        "number_of_distinct_block_spans": n // len(stabilizer),
        "pairwise_intersection_dimension_by_delta": pairwise_intersection,
        "claim_boundary": (
            "This profile applies when P has a polynomial right factor of "
            f"degree {m}; divisibility alone does not assert that such a factor exists."
        ),
    }


def analyse_phase(phase_text: str) -> dict[str, Any]:
    original = parse_polynomial(phase_text)
    normalisation = normalise_phase(original)
    phase = normalisation.normalised
    rank, rank_certificate = cyclic_rank_certificate(phase)
    support_certificate = inverse_support_certificate(phase, rank)
    support = support_certificate["support"]
    profiles = {
        str(m): block_fusion_profile(support, phase.degree(), m)
        for m in divisors(phase.degree()) if m >= 2
    }
    result = {
        "schema": "cyclicity-support-fusion-certificate-v1",
        "status": "pass",
        "input": {"phase": phase_text},
        "input_sha256": canonical_hash({"phase": phase_text}),
        "normalisation": normalisation.as_dict(),
        "degree": phase.degree(),
        "theorem_identity": {
            "twisted_cyclic_rank": rank,
            "inverse_support_size": len(support),
            "reduced_root_span_dimension": len(support),
            "all_equal": rank == len(support),
        },
        "twisted_krylov": rank_certificate,
        "inverse_at_infinity": support_certificate,
        "fusion_profiles_by_candidate_right_degree": profiles,
        "claim_boundary": {
            "proved_by_companion_manuscript": [
                "q(P,dx)=|Sigma(P)|=dim W_P^red",
                "the Fourier block-rank formula for every actual decomposition",
                "Ritt-move invariance of the support classification",
            ],
            "not_computed": [
                "the complete decomposition lattice of P",
                "whether each divisor degree occurs as a right factor",
                "novelty, priority, or external specialist validation",
            ],
        },
    }
    result["certificate_sha256"] = canonical_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, help="trusted Q[x] expression")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyse_phase(args.phase)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
