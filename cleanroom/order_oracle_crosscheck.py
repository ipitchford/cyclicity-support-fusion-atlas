#!/usr/bin/env python3
"""Separate symbolic cross-check of selected order-oracle operators.

This script imports neither ``src/fusion_support.py`` nor
``src/order_oracle.py``.  It reduces the Krylov iterates using polynomials in
``u=1/s`` and compares the resulting rational operator with frozen production
coefficients only up to a common nonzero factor.
"""

from __future__ import annotations

from fractions import Fraction

import sympy as sp


U = sp.Symbol("u")
S = sp.Symbol("s")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def trim(values: list[Fraction]) -> list[Fraction]:
    result = list(values)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def power(base: list[Fraction], exponent: int) -> list[Fraction]:
    result = [Fraction(1)]
    for _ in range(exponent):
        result = multiply(result, base)
    return result


def uadd(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return result


def uscale(values: list[Fraction], scalar: Fraction) -> list[Fraction]:
    return [scalar * value for value in values]


def ushift(values: list[Fraction]) -> list[Fraction]:
    return [Fraction(0)] + list(values)


def uiszero(values: list[Fraction]) -> bool:
    return all(value == 0 for value in values)


def reduce_symbolic(
    polynomial: list[list[Fraction]], phase: list[Fraction]
) -> list[sp.Expr]:
    """Reduce over Q[u], where u=1/s, to x-degree at most d-2."""

    degree = len(phase) - 1
    require(phase[-1] == 1, "clean-room phases must be monic")
    derivative = [Fraction(index) * phase[index] for index in range(1, degree + 1)]
    working = [list(coefficient) for coefficient in polynomial]

    def xdegree(values: list[list[Fraction]]) -> int:
        index = len(values) - 1
        while index >= 0 and uiszero(values[index]):
            index -= 1
        return index

    current_degree = xdegree(working)
    while current_degree >= degree - 1:
        leading = working[current_degree]
        shift = current_degree - degree + 1
        base = uscale(leading, Fraction(1, degree))
        for index, coefficient in enumerate(derivative):
            if coefficient:
                working[shift + index] = uadd(
                    working[shift + index], uscale(base, -coefficient)
                )
        if shift >= 1:
            working[shift - 1] = uadd(
                working[shift - 1], ushift(uscale(base, Fraction(-shift)))
            )
        next_degree = xdegree(working)
        require(next_degree < current_degree, "clean-room reduction failed to lower degree")
        current_degree = next_degree

    padded = working[: degree - 1] + [[Fraction(0)]] * max(
        0, degree - 1 - len(working)
    )
    result: list[sp.Expr] = []
    for coefficient in padded[: degree - 1]:
        rationals = [sp.Rational(value.numerator, value.denominator) for value in coefficient]
        result.append(sp.Poly(list(reversed(rationals)) or [0], U).as_expr())
    return result


def derive_operator(phase: list[Fraction]) -> tuple[int, list[sp.Expr]]:
    phase = trim(phase)
    degree = len(phase) - 1
    require(degree >= 2 and phase[-1] == 1, "invalid clean-room phase")
    iterate = [Fraction(1)]
    basis = sp.zeros(degree - 1, 0)
    for derivative_order in range(degree):
        embedded = [
            [iterate[index]] if index < len(iterate) else [Fraction(0)]
            for index in range(max(len(iterate), degree * degree + 1))
        ]
        column = sp.Matrix(reduce_symbolic(embedded, phase))
        extended = basis.row_join(column)
        if extended.rank() == basis.rank():
            solution = basis.solve(column)
            require(
                all(sp.cancel(value) == 0 for value in basis * solution - column),
                "clean-room dependence residual is nonzero",
            )
            coefficients = [
                -sp.cancel(solution[index].subs(U, 1 / S))
                for index in range(derivative_order)
            ] + [sp.Integer(1)]
            return derivative_order, coefficients
        basis = extended
        iterate = multiply(iterate, phase)
    raise RuntimeError("clean-room derivation found no Krylov dependence")


def proportional(left: list[sp.Expr], right: list[sp.Expr]) -> bool:
    require(len(left) == len(right), "operator lengths differ")
    pivot = next(index for index, value in enumerate(right) if value != 0)
    factor = sp.cancel(left[pivot] / right[pivot])
    return factor != 0 and all(
        sp.cancel(left[index] - factor * right[index]) == 0
        for index in range(len(left))
    )


def polynomial(mapping: dict[int, int | Fraction]) -> list[Fraction]:
    values = [Fraction(0)] * (max(mapping) + 1)
    for exponent, coefficient in mapping.items():
        values[exponent] = Fraction(coefficient)
    return values


def main() -> None:
    quartic = polynomial({4: 1, 2: 1, 1: 1})
    quartic_drop = polynomial({4: 1, 2: 1})
    aligned_square = power(polynomial({6: 1, 2: 1}), 2)
    misaligned_square = power(polynomial({6: 1, 4: 1, 2: 1}), 2)
    exceptional = power(polynomial({4: 1, 1: 1}), 3)
    rank_creation_base = polynomial({3: 1, 1: 1})
    rank_creation = multiply(rank_creation_base, rank_creation_base)
    if len(rank_creation) < len(rank_creation_base):
        rank_creation += [Fraction(0)] * (len(rank_creation_base) - len(rank_creation))
    for index, value in enumerate(rank_creation_base):
        rank_creation[index] += value

    cases = [
        ("power_degree_7", polynomial({7: 1}), 1, ["1", "7*s"]),
        (
            "quartic_rank_3",
            quartic,
            3,
            [
                "1085*s**4 + 2614*s**3 - 1468*s**2 + 1200*s - 48",
                "16*s*(350*s**3 + 220*s**2 - 279*s - 42)",
                "128*s**2*(35*s**2 + 99*s - 30)",
                "256*s**3*(35*s - 6)",
            ],
        ),
        ("quartic_rank_drop", quartic_drop, 2, ["2*s - 1", "4*s*(s + 4)", "16*s**2"]),
        (
            "aligned_square_degree_12",
            aligned_square,
            3,
            ["32*s + 21", "4*s*(112*s + 141)", "16*s**2*(16*s + 243)", "1728*s**3"],
        ),
        (
            "exceptional_collision_degree_12",
            exceptional,
            3,
            ["2*(81*s + 20)", "18*s*(81*s + 200)", "27*s**2*(27*s + 640)", "6912*s**3"],
        ),
        (
            "rank_creation_degree_6",
            trim(rank_creation),
            4,
            [
                "5332*s**5 + 69248*s**4 + 97793*s**3 + 23554*s**2 - 14160*s - 360",
                "s*(51944*s**4 + 441931*s**3 + 419546*s**2 + 68640*s + 12960)",
                "s**2*(190963*s**3 + 1169273*s**2 + 1140480*s + 244620)",
                "216*s**3*(1849*s**2 + 9503*s + 1350)",
                "11664*s**4*(43*s + 5)",
            ],
        ),
    ]

    for name, phase, expected_order, expected_strings in cases:
        observed_order, observed = derive_operator(phase)
        expected = [sp.sympify(value, locals={"s": S}) for value in expected_strings]
        require(observed_order == expected_order, f"clean-room order mismatch: {name}")
        require(proportional(observed, expected), f"clean-room operator mismatch: {name}")
        print(f"[PASS] {name}: order {observed_order}, proportional operator")

    # The order-six mutation is retained in the production exact benchmark but
    # omitted here to keep this separate symbolic path within the quick budget.
    require(len(misaligned_square) - 1 == 12, "misaligned-square construction failed")
    print("clean-room order-oracle cross-check PASS (6 operators)")


if __name__ == "__main__":
    main()
