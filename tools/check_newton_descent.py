#!/usr/bin/env python3
"""Bounded exact fault control for the all-degree Newton descent proof."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def expression_digest(expressions: list[sp.Expr]) -> str:
    payload = "\n".join(sp.srepr(sp.expand(value)) for value in expressions)
    return hashlib.sha256(payload.encode()).hexdigest()


def power_sums(degree: int, coefficients: dict[int, sp.Expr], limit: int) -> dict[int, sp.Expr]:
    """Newton sums for x^degree + sum coefficients[j] x^(degree-j)."""
    values: dict[int, sp.Expr] = {0: sp.Integer(degree)}
    for order in range(1, limit + 1):
        total = sp.Integer(0)
        for shift, coefficient in coefficients.items():
            if order - shift <= 0:
                continue
            total += coefficient * values[order - shift]
        if order <= degree:
            total += order * coefficients.get(order, sp.Integer(0))
        values[order] = sp.expand(-total)
    return values


def conditions_in_parameter(expressions: list[sp.Expr], parameter: sp.Symbol) -> list[sp.Expr]:
    conditions: list[sp.Expr] = []
    for expression in expressions:
        polynomial = sp.Poly(sp.expand(expression), parameter)
        conditions.extend(coefficient for coefficient in polynomial.all_coeffs() if coefficient != 0)
    return conditions


def is_unit(groebner: sp.GroebnerBasis) -> bool:
    return len(groebner.exprs) == 1 and groebner.exprs[0] == 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-m", type=int, default=32)
    parser.add_argument("--output", type=Path, default=ROOT / "receipts" / "newton_descent_check.json")
    args = parser.parse_args()
    if args.max_m < 9:
        raise SystemExit("max-m must cover the quartic boundary candidates through m=9")

    a, c, e, w = sp.symbols("a c e w")
    cubic = power_sums(3, {2: a, 3: e}, 2 * args.max_m)
    quartic = power_sums(4, {2: a, 3: c, 4: e}, 3 * args.max_m)
    records = []

    for m in range(2, args.max_m + 1):
        first = cubic[m]
        second = sp.expand((first**2 - cubic[2 * m]) / 2)
        conditions = conditions_in_parameter([sp.diff(first, e), sp.diff(second, e)], e)
        basis = sp.groebner(conditions + [w * a - 1], a, w, order="lex", domain="QQ")
        empty = is_unit(basis)
        if empty != (m != 2):
            raise RuntimeError(f"cubic Newton locus mismatch at m={m}: empty={empty}")
        records.append({
            "type": "cubic",
            "m": m,
            "nonpower_saturation": "a != 0",
            "empty": empty,
            "conditions_sha256": expression_digest(conditions),
            "basis_sha256": expression_digest(list(basis.exprs)),
        })

    for m in range(2, args.max_m + 1):
        first = quartic[m]
        second = sp.expand((first**2 - quartic[2 * m]) / 2)
        conditions = conditions_in_parameter([sp.diff(first, e), sp.diff(second, e)], e)
        basis = sp.groebner(conditions + [w * c - 1], a, c, w, order="lex", domain="QQ")
        empty = is_unit(basis)
        if empty != (m != 3):
            raise RuntimeError(f"quartic Newton locus mismatch at m={m}: empty={empty}")
        if m == 3 and sp.reduced(a, basis)[1] != 0:
            raise RuntimeError("quartic m=3 locus does not force a=0")
        records.append({
            "type": "quartic",
            "m": m,
            "nondegenerate_saturation": "c != 0",
            "empty": empty,
            "surviving_locus": "a=0" if m == 3 else None,
            "conditions_sha256": expression_digest(conditions),
            "basis_sha256": expression_digest(list(basis.exprs)),
        })

    cubic_positive = [
        cubic[2],
        sp.expand((cubic[2] ** 2 - cubic[4]) / 2),
        e**2,
    ]
    quartic_positive = [
        quartic[3].subs(a, 0),
        sp.expand((quartic[3] ** 2 - quartic[6]) / 2).subs(a, 0),
        sp.expand((quartic[3] ** 3 - 3 * quartic[3] * quartic[6] + 2 * quartic[9]) / 6).subs(a, 0),
        e**3,
    ]
    if [sp.factor(value) for value in cubic_positive] != [-2 * a, a**2, e**2]:
        raise RuntimeError("cubic m=2 positive identity failed")
    if [sp.factor(value) for value in quartic_positive] != [-3 * c, 3 * c**2, -c**3, e**3]:
        raise RuntimeError("quartic m=3 positive identity failed")

    result = {
        "schema": "newton-descent-bounded-check-v1",
        "status": "pass",
        "m_range": [2, args.max_m],
        "records": records,
        "positive_identities": {
            "cubic_m2": [sp.sstr(value) for value in cubic_positive],
            "quartic_m3_a0": [sp.sstr(value) for value in quartic_positive],
        },
        "claim_boundary": "Bounded symbolic fault control only; the all-m proof is the coefficient-extraction argument in ALL_DEGREE_NEWTON_DESCENT.md.",
    }
    result["receipt_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "pass",
        "m_range": result["m_range"],
        "record_count": len(records),
        "receipt_sha256": result["receipt_sha256"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
