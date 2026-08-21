#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amplitude_support import analyse_amplitude, canonical_hash  # noqa: E402
from laurent_moments import (  # noqa: E402
    analyse_laurent_amplitude,
    analyse_laurent_moments,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def amplitude_case(
    phase: str,
    amplitude: str,
    expected_rank: int,
    expected_support: set[int],
) -> dict:
    result = analyse_amplitude(phase, amplitude)
    identity = result["theorem_identity"]
    support = set(result["primitive_inverse_at_infinity"]["support"])
    require(identity["all_equal"] is True, f"amplitude identity failed for {phase}, {amplitude}")
    require(identity["twisted_amplitude_cyclic_rank"] == expected_rank, "amplitude rank failed")
    require(support == expected_support, f"amplitude support failed: {support}")
    return result


def exact_segment_moment(phase: sp.Expr, primitive: sp.Expr, a: sp.Expr, b: sp.Expr, k: int) -> sp.Expr:
    x = sp.Symbol("x")
    integrand = sp.expand(phase**k * sp.diff(primitive, x))
    antiderivative = sp.integrate(integrand, x)
    return sp.simplify(antiderivative.subs(x, b) - antiderivative.subs(x, a))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    cases: list[dict] = []
    cases.append(amplitude_case("x**7", "1", 1, {1}))
    exact = amplitude_case("x**7", "x**6", 0, set())
    require(exact["universal_vanishing"]["primitive_factors_through_phase"] is True,
            "power exactness witness failed")

    cases.append(amplitude_case("16*x**5-20*x**3+5*x", "1", 2, {1, 4}))
    cases.append(amplitude_case("(x**4+x)**3", "4*x**3", 4, {1, 4, 7, 10}))

    centre7 = amplitude_case(
        "(x**4+x)**3", "7*x**6+7*x**3", 3, {1, 7, 10}
    )
    centre10 = amplitude_case(
        "(x**4+x)**3", "10*x**9-10*x**3", 3, {1, 7, 10}
    )
    require(
        set(centre7["primitive_inverse_at_infinity"]["support"]).isdisjoint({4, 8}),
        "degree-seven zero-cycle Fourier exclusion failed",
    )
    require(
        set(centre10["primitive_inverse_at_infinity"]["support"]).isdisjoint({4, 8}),
        "degree-ten zero-cycle Fourier exclusion failed",
    )
    cases.extend([centre7, centre10])

    translated = amplitude_case("(x+2)**4+(x+2)", "1", 3, {1, 2, 3})
    cases.append(translated)

    # Endpoint moment controls for the exceptional degree-12 collision.
    x = sp.Symbol("x")
    q4 = x**4 + x
    phase = q4**3
    for k in range(8):
        require(exact_segment_moment(phase, q4, sp.Integer(0), sp.Integer(-1), k) == 0,
                f"quartic-factor endpoint moment failed at k={k}")

    omega = sp.exp(2 * sp.pi * sp.I / 3)
    for k in range(8):
        value = exact_segment_moment(phase, x**3, sp.Integer(1), omega, k)
        require(sp.simplify(sp.expand_complex(value)) == 0,
                f"cubic-factor endpoint moment failed at k={k}")

    laurent_cases = [
        analyse_laurent_moments("z+z**-1", "z", 8),
        analyse_laurent_moments("z**2+z**-2", "z", 12),
        analyse_laurent_moments(
            "z**2+5*z-5*z**-1+z**-2", "z-z**-1", 12
        ),
        analyse_laurent_moments("z+z**-1", "z+z**-1", 12),
    ]
    require(laurent_cases[0]["status"] == "nonvanishing_witness",
            "Laurent negative control did not expose a moment")
    require(all(case["status"] == "finite_prefix_zero" for case in laurent_cases[1:]),
            "Laurent mechanism control has a nonzero prefix")

    laurent_amplitude_cases = [
        analyse_laurent_amplitude("z+z**-1", "z**-1", 12),
        analyse_laurent_amplitude("z**2+z**-2", "1", 12),
    ]
    require(
        laurent_amplitude_cases[0]["status"] == "nonvanishing_witness"
        and laurent_amplitude_cases[0]["first_nonzero_witness"]["k"] == 2,
        "logarithmic Laurent amplitude did not expose its second moment",
    )
    require(
        laurent_amplitude_cases[1]["status"] == "finite_prefix_zero",
        "deck-symmetry Laurent amplitude has a nonzero prefix",
    )

    # Semantic mutation controls: even after recomputing the outer digest, a
    # fresh exact analysis must disagree with the corrupted payload.
    mutated_amplitude = copy.deepcopy(cases[0])
    mutated_amplitude["primitive_inverse_at_infinity"]["support"] = [2]
    mutated_amplitude.pop("certificate_sha256")
    mutated_amplitude["certificate_sha256"] = canonical_hash(mutated_amplitude)
    fresh_amplitude = analyse_amplitude(
        mutated_amplitude["input"]["phase"], mutated_amplitude["input"]["amplitude"]
    )
    require(mutated_amplitude != fresh_amplitude, "amplitude mutation was not detected")

    mutated_laurent = copy.deepcopy(laurent_cases[1])
    mutated_laurent["records"][0]["zero"] = False
    mutated_laurent.pop("certificate_sha256")
    mutated_laurent["certificate_sha256"] = canonical_hash(mutated_laurent)
    fresh_laurent = analyse_laurent_moments("z**2+z**-2", "z", 12)
    require(mutated_laurent != fresh_laurent, "Laurent mutation was not detected")

    receipt = {
        "schema": "amplitude-laurent-test-receipt-v1",
        "status": "pass",
        "amplitude_case_digests": [case["certificate_sha256"] for case in cases],
        "rank_zero_case_digest": exact["certificate_sha256"],
        "laurent_case_digests": [case["certificate_sha256"] for case in laurent_cases],
        "laurent_amplitude_case_digests": [
            case["certificate_sha256"] for case in laurent_amplitude_cases
        ],
        "endpoint_moments_checked": 16,
        "semantic_mutations_rejected": 2,
        "claim_boundary": {
            "amplitude_cases": "exact theorem-to-CAS comparisons",
            "endpoint_cases": "finite direct regressions for proved composition mechanisms",
            "laurent_zero_prefixes": "finite evidence, not all-moment certificates",
        },
    }
    receipt["receipt_sha256"] = canonical_hash(receipt)
    encoded = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
