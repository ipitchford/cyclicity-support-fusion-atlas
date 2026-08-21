#!/usr/bin/env python3
"""Resultant-based cross-check of cubic and quartic powered-root loci."""

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


def digest(expressions: list[sp.Expr]) -> str:
    text = "\n".join(sp.srepr(sp.expand(expression)) for expression in expressions)
    return hashlib.sha256(text.encode()).hexdigest()


def coefficient_conditions(expressions: list[sp.Expr], parameter: sp.Symbol) -> list[sp.Expr]:
    values = []
    for expression in expressions:
        values.extend(
            coefficient
            for coefficient in sp.Poly(sp.diff(expression, parameter), parameter).all_coeffs()
            if coefficient != 0
        )
    return values


def is_unit(basis: sp.GroebnerBasis) -> bool:
    return len(basis.exprs) == 1 and basis.exprs[0] == 1


def powered_root_polynomial(phase: sp.Expr, m: int, x: sp.Symbol, y: sp.Symbol) -> sp.Poly:
    result = sp.Poly(sp.resultant(phase, y - x**m, x), y)
    if result.LC() != 1:
        result = sp.Poly(result.as_expr() / result.LC(), y)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-m", type=int, default=12)
    parser.add_argument("--output", type=Path, default=ROOT / "receipts" / "newton_resultant_crosscheck.json")
    args = parser.parse_args()
    if args.max_m < 9:
        raise SystemExit("max-m must be at least 9")

    x, y, a, c, e, w = sp.symbols("x y a c e w")
    records = []
    positive = {}
    for degree, kind, phase, nonzero, variables, survivor in (
        (3, "cubic", x**3 + a * x + e, a, (a, w), 2),
        (4, "quartic", x**4 + a * x**2 + c * x + e, c, (a, c, w), 3),
    ):
        for m in range(2, args.max_m + 1):
            powered = powered_root_polynomial(phase, m, x, y)
            coefficients = powered.all_coeffs()[1:degree]
            conditions = coefficient_conditions(coefficients, e)
            basis = sp.groebner(conditions + [w * nonzero - 1], *variables, order="lex", domain="QQ")
            empty = is_unit(basis)
            if empty != (m != survivor):
                raise RuntimeError(f"{kind} resultant locus mismatch at m={m}: empty={empty}")
            if kind == "quartic" and m == 3 and sp.reduced(a, basis)[1] != 0:
                raise RuntimeError("quartic resultant m=3 locus does not force a=0")
            if m == survivor:
                expression = powered.as_expr().subs(a, 0) if kind == "quartic" else powered.as_expr()
                positive[kind] = sp.sstr(sp.factor(expression))
            records.append({
                "type": kind,
                "m": m,
                "empty_after_nondegenerate_saturation": empty,
                "coefficient_digest": digest(coefficients),
                "condition_digest": digest(conditions),
                "basis_digest": digest(list(basis.exprs)),
            })

    expected_cubic = y * (a + y) ** 2 - e**2
    expected_quartic = y * (c + y) ** 3 + e**3
    if sp.expand(sp.sympify(positive["cubic"]) - expected_cubic) != 0:
        raise RuntimeError("cubic positive resultant identity mismatch")
    if sp.expand(sp.sympify(positive["quartic"]) - expected_quartic) != 0:
        raise RuntimeError("quartic positive resultant identity mismatch")

    result = {
        "schema": "newton-resultant-crosscheck-v1",
        "status": "pass",
        "m_range": [2, args.max_m],
        "method": "direct resultants Res_x(q_e(x), y-x^m); imports no Newton checker code",
        "records": records,
        "positive_resultants": positive,
        "claim_boundary": "Separate within-programme SymPy derivation; bounded control, not an all-m proof or external reproduction.",
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
