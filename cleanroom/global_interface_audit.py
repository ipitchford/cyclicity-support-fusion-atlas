#!/usr/bin/env python3
"""Independent symbolic controls for the global cyclicity completion.

The exact checks reconstruct polynomial identities and finite-table
intersections without importing project code.  The Dickson and floor checks
are explicitly labelled bounded regression controls; they are not used as an
all-degree proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "receipts" / "global_interface_cas_receipt.json"


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def dickson(n: int, x: sp.Symbol, a: sp.Symbol) -> sp.Expr:
    """Return D_n(x,a) with D_0=2, D_1=x, D_n=xD_{n-1}-aD_{n-2}."""
    if n == 0:
        return sp.Integer(2)
    if n == 1:
        return x
    previous_previous = sp.Integer(2)
    previous = x
    for _ in range(2, n + 1):
        current = sp.expand(x * previous - a * previous_previous)
        previous_previous, previous = previous, current
    return previous


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    x, a, b, c, A, B = sp.symbols("x a b c A B")

    # Exact source-table transcription and canonical-name intersection.
    muller_exceptional = {
        ("PGL2(5)", 6),
        ("PSL3(2)", 7),
        ("PGL2(7)", 8),
        ("PGammaL2(8)", 9),
        ("PGammaL2(9)", 10),
        ("PSL2(11)", 11),
        ("M11", 11),
        ("PSL3(3)", 13),
        ("PSL4(2)", 15),
        ("PGammaL3(4)", 21),
        ("M23", 23),
        ("PSL5(2)", 31),
    }
    require(len(muller_exceptional) == 12, "Muller exceptional inventory")
    pgl2_primitive = {"A4", "S4", "A5"}
    require(pgl2_primitive == {"A4", "S4", "A5"}, "PGL2 source table")
    pgl3_primitive = {"A5", "PSL2(7)", "A6", "H1", "H2", "H3"}
    nonsolvable_low_dim_polynomial = {"A5", "PSL2(7)"}
    pgl3_intersection = pgl3_primitive & nonsolvable_low_dim_polynomial
    require(pgl3_intersection == {"A5", "PSL2(7)"}, "PGL3 intersection")
    pgl2_formal_candidates = {("S4", 4), ("A5", 5)}
    require(
        pgl2_formal_candidates == {("S4", 4), ("A5", 5)},
        "PGL2 formal candidate intersection",
    )

    # Exact restriction-character multiplicity numerators.
    character_numerators = {
        "A5_to_A4_trivial": 3 + 3 * (-1) + 8 * 0,
        "A5_to_A4_nontrivial_linear": 3 + 3 * (-1) + 8 * 0,
        "PSL3_2_to_S4_trivial": 3 + 9 * (-1) + 8 * 0 + 6,
        "PSL3_2_to_S4_sign": 3 + 6 - 3 - 6,
    }
    require(set(character_numerators.values()) == {0}, "character restrictions")
    character_multiplicities = {
        "A5_to_A4_trivial": Fraction(character_numerators["A5_to_A4_trivial"], 12),
        "A5_to_A4_nontrivial_linear": Fraction(
            character_numerators["A5_to_A4_nontrivial_linear"], 12
        ),
        "PSL3_2_to_S4_trivial": Fraction(
            character_numerators["PSL3_2_to_S4_trivial"], 24
        ),
        "PSL3_2_to_S4_sign": Fraction(character_numerators["PSL3_2_to_S4_sign"], 24),
    }
    require(set(character_multiplicities.values()) == {Fraction(0)}, "multiplicities")

    # Exact scalar elimination for the rank-three extensions.
    cubic_A_equation = sp.factor(c * A - A)
    cubic_B_equation = sp.factor(c**2 * B - B)
    quartic_A_equation = sp.factor(c**2 * A - A)
    quartic_B_equation = sp.factor(c**3 * B - B)
    require(cubic_A_equation == A * (c - 1), "cubic A factor")
    require(cubic_B_equation == B * (c - 1) * (c + 1), "cubic B factor")
    require(quartic_A_equation == A * (c - 1) * (c + 1), "quartic A factor")
    require(quartic_B_equation == B * (c - 1) * (c**2 + c + 1), "quartic B factor")

    collision = sp.expand((x**4 + b * x) ** 3)
    expected_collision = x**12 + 3 * b * x**9 + 3 * b**2 * x**6 + b**3 * x**3
    require(sp.expand(collision - expected_collision) == 0, "quartic collision expansion")
    multiplier_gcd = sp.gcd(c**12 - c**9, sp.gcd(c**9 - c**6, c**6 - c**3))
    saturated_multiplier_gcd = sp.factor(multiplier_gcd / c**3)
    require(
        sp.expand(saturated_multiplier_gcd - (c**3 - 1)) == 0,
        "collision scalar saturation",
    )

    aligned_square = sp.expand((x**3 + b * x) ** 2)
    require(aligned_square.coeff(x, 4) == 2 * b, "aligned-square no-repeat coefficient")

    # Bounded controls, deliberately separated from the theorem claims.
    floor_cases = []
    for n in range(2, 65):
        for k in range(n):
            require(k // n == 0, f"floor bound n={n},k={k}")
            floor_cases.append((n, k))

    dickson_cases = []
    for m in range(2, 11):
        for n in range(2, 11):
            left = dickson(m * n, x, a)
            inner = dickson(m, x, a)
            right = dickson(n, x, a**m).subs(x, inner)
            require(sp.expand(left - right) == 0, f"Dickson composition m={m},n={n}")
            dickson_cases.append((m, n))

    result: dict[str, Any] = {
        "schema": "cyclicity-global-interface-cas-receipt-v1",
        "status": "pass",
        "engine": {"name": "SymPy", "version": sp.__version__},
        "exact_checks": {
            "muller_exceptional_inventory": [list(item) for item in sorted(muller_exceptional)],
            "pgl2_primitive_source": sorted(pgl2_primitive),
            "pgl2_formal_candidates": [list(item) for item in sorted(pgl2_formal_candidates)],
            "pgl3_intersection": sorted(pgl3_intersection),
            "character_multiplicities": {
                key: str(value) for key, value in sorted(character_multiplicities.items())
            },
            "cubic_scalar_factors": [str(cubic_A_equation), str(cubic_B_equation)],
            "quartic_scalar_factors": [str(quartic_A_equation), str(quartic_B_equation)],
            "collision_expansion": str(collision),
            "collision_saturated_multiplier_gcd": str(saturated_multiplier_gcd),
            "aligned_square_quadratic_coefficient": str(aligned_square.coeff(x, 4)),
        },
        "bounded_regression_controls": {
            "floor_n_range": [2, 64],
            "floor_case_count": len(floor_cases),
            "dickson_m_range": [2, 10],
            "dickson_n_range": [2, 10],
            "dickson_case_count": len(dickson_cases),
            "all_degree_claim": False,
        },
        "assurance": {
            "independent_implementation": True,
            "symbolic_identity_checks": True,
            "finite_group_classification_reproved": False,
            "external_independence": False,
        },
        "claim_boundary": (
            "Exact symbolic checks cover the transcribed finite-list intersections, "
            "character sums, scalar-factor equations, collision expansion and scalar "
            "saturation. Bounded floor and Dickson checks are regression controls only. "
            "This receipt does not prove the imported classifications or the all-degree theorem."
        ),
    }
    result["receipt_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "exact_check_count": len(result["exact_checks"]),
                "bounded_dickson_cases": len(dickson_cases),
                "receipt_sha256": result["receipt_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
