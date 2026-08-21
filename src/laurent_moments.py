#!/usr/bin/env python3
"""Exact local-channel checks for Laurent-polynomial residue moments.

Let L(z) have a pole of order m at zero, normalised by c_{-m}=1, and let
A be a Laurent polynomial amplitude.  If phi(tau)=tau*G(tau) is the local inverse with

    L(phi(tau)) = tau**(-m),

then the companion manuscript proves

    Res_0 L(z)**k A(z) dz
      = [tau**(m*k-1)] A(phi(tau))*phi'(tau).

If A=Q', integration by parts gives the equivalent expression

    m*k * [tau**(m*k)] Q(phi(tau)).

Consequently all residue moments vanish exactly when the indicated local
coefficients vanish.  This program checks exact finite prefixes and emits a
decisive non-vanishing witness when one occurs.  A zero prefix is not
mislabelled as an all-k proof.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


z = sp.Symbol("z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_laurent(text: str) -> dict[int, Fraction]:
    require(isinstance(text, str), "Laurent polynomial must be a string")
    expr = sp.expand(sp.sympify(text, locals={"z": z}))
    require(expr.free_symbols <= {z}, "Laurent polynomial must lie in Q[z,z^-1]")
    result: dict[int, Fraction] = {}
    for term in sp.Add.make_args(expr):
        coefficient, power = term.as_coeff_exponent(z)
        require(power.is_Integer, f"nonintegral Laurent exponent in {term}")
        require(coefficient.is_Rational, f"nonrational Laurent coefficient in {term}")
        exponent = int(power)
        value = Fraction(int(coefficient.p), int(coefficient.q))
        result[exponent] = result.get(exponent, Fraction(0)) + value
    return {exponent: value for exponent, value in result.items() if value}


def canonical_laurent(poly: dict[int, Fraction]) -> str:
    expr = sum(
        sp.Rational(value.numerator, value.denominator) * z**exponent
        for exponent, value in poly.items()
    )
    return sp.sstr(sp.expand(expr))


def laurent_multiply(
    left: dict[int, Fraction], right: dict[int, Fraction]
) -> dict[int, Fraction]:
    result: dict[int, Fraction] = {}
    for i, a in left.items():
        for j, b in right.items():
            result[i + j] = result.get(i + j, Fraction(0)) + a * b
    return {exponent: value for exponent, value in result.items() if value}


def laurent_power(poly: dict[int, Fraction], exponent: int) -> dict[int, Fraction]:
    require(exponent >= 0, "Laurent power must be nonnegative")
    result = {0: Fraction(1)}
    base = dict(poly)
    power = exponent
    while power:
        if power & 1:
            result = laurent_multiply(result, base)
        power >>= 1
        if power:
            base = laurent_multiply(base, base)
    return result


def laurent_derivative(poly: dict[int, Fraction]) -> dict[int, Fraction]:
    return {
        exponent - 1: exponent * value
        for exponent, value in poly.items()
        if exponent and exponent * value
    }


def normalise_at_zero(
    phase: dict[int, Fraction]
) -> tuple[dict[int, Fraction], int, Fraction]:
    require(phase, "phase must be nonzero")
    lowest = min(phase)
    highest = max(phase)
    require(lowest < 0 < highest, "phase must have poles at zero and infinity")
    m = -lowest
    scale = phase[lowest]
    normalised = {exponent: value / scale for exponent, value in phase.items()}
    require(normalised[-m] == 1, "failed to normalise the zero-pole coefficient")
    return normalised, m, scale


def series_multiply(
    left: list[Fraction], right: list[Fraction], degree: int
) -> list[Fraction]:
    result = [Fraction(0)] * (degree + 1)
    for i, a in enumerate(left[: degree + 1]):
        if not a:
            continue
        for j, b in enumerate(right[: degree + 1 - i]):
            if b:
                result[i + j] += a * b
    return result


def series_inverse(series: list[Fraction], degree: int) -> list[Fraction]:
    require(series and series[0], "series must have nonzero constant coefficient")
    result = [Fraction(0)] * (degree + 1)
    result[0] = Fraction(1, 1) / series[0]
    for k in range(1, degree + 1):
        total = Fraction(0)
        for i in range(1, min(k, len(series) - 1) + 1):
            total += series[i] * result[k - i]
        result[k] = -result[0] * total
    return result


def series_powers(
    series: list[Fraction], minimum: int, maximum: int, degree: int
) -> dict[int, list[Fraction]]:
    one = [Fraction(1)] + [Fraction(0)] * degree
    result: dict[int, list[Fraction]] = {0: one}
    for exponent in range(1, maximum + 1):
        result[exponent] = series_multiply(result[exponent - 1], series, degree)
    if minimum < 0:
        inverse = series_inverse(series, degree)
        for exponent in range(1, -minimum + 1):
            result[-exponent] = series_multiply(
                result[-(exponent - 1)], inverse, degree
            )
    return result


def zero_inverse_series(
    phase: dict[int, Fraction], m: int, degree: int
) -> list[Fraction]:
    """Solve G^m=1+sum_{i>-m} c_i tau^(i+m) G^(i+m)."""

    g = [Fraction(0)] * (degree + 1)
    g[0] = Fraction(1)
    terms = [(i, c) for i, c in phase.items() if i > -m and c]
    maximum_power = max([m] + [i + m for i, _ in terms])
    for _iteration in range(80):
        powers = series_powers(g, 0, maximum_power, degree)
        equation = list(powers[m])
        equation[0] -= 1
        for exponent, coefficient in terms:
            shift = exponent + m
            source = powers[exponent + m]
            for index in range(degree + 1 - shift):
                equation[shift + index] -= coefficient * source[index]
        if all(value == 0 for value in equation):
            return g

        derivative = [m * value for value in powers[m - 1]]
        for exponent, coefficient in terms:
            shift = exponent + m
            source = powers[exponent + m - 1]
            for index in range(degree + 1 - shift):
                derivative[shift + index] -= (
                    coefficient * (exponent + m) * source[index]
                )
        correction = series_multiply(
            equation, series_inverse(derivative, degree), degree
        )
        g = [value - delta for value, delta in zip(g, correction)]
    raise RuntimeError("Laurent inverse Newton iteration did not converge")


def composed_coefficient(
    primitive: dict[int, Fraction],
    powers: dict[int, list[Fraction]],
    tau_exponent: int,
) -> Fraction:
    result = Fraction(0)
    for exponent, coefficient in primitive.items():
        series_index = tau_exponent - exponent
        if 0 <= series_index < len(powers[exponent]):
            result += coefficient * powers[exponent][series_index]
    return result


def pulled_back_form_coefficient(
    amplitude: dict[int, Fraction],
    powers: dict[int, list[Fraction]],
    g: list[Fraction],
    tau_exponent: int,
) -> Fraction:
    """Return [tau^tau_exponent] A(phi(tau))*phi'(tau), phi=tau*g."""

    degree = len(g) - 1
    phi_derivative = [Fraction(0)] * (degree + 1)
    for index, coefficient in enumerate(g):
        phi_derivative[index] = (index + 1) * coefficient
    result = Fraction(0)
    for exponent, coefficient in amplitude.items():
        product = series_multiply(powers[exponent], phi_derivative, degree)
        series_index = tau_exponent - exponent
        if 0 <= series_index < len(product):
            result += coefficient * product[series_index]
    return result


def direct_residue_moment(
    phase: dict[int, Fraction], primitive: dict[int, Fraction], moment: int
) -> Fraction:
    integrand = laurent_multiply(
        laurent_power(phase, moment), laurent_derivative(primitive)
    )
    return integrand.get(-1, Fraction(0))


def direct_amplitude_residue_moment(
    phase: dict[int, Fraction], amplitude: dict[int, Fraction], moment: int
) -> Fraction:
    integrand = laurent_multiply(laurent_power(phase, moment), amplitude)
    return integrand.get(-1, Fraction(0))


def analyse_laurent_amplitude(
    phase_text: str, amplitude_text: str, moments: int
) -> dict[str, Any]:
    """Compare the inverse-series and direct residues for A(z) dz."""

    require(moments >= 1, "at least one positive moment is required")
    original_phase = parse_laurent(phase_text)
    amplitude = parse_laurent(amplitude_text)
    phase, m, target_scale = normalise_at_zero(original_phase)
    minimum_power = min(amplitude) if amplitude else 0
    maximum_power = max(amplitude) if amplitude else 0
    degree = m * moments - minimum_power + maximum_power + 8
    g = zero_inverse_series(phase, m, degree)
    powers = series_powers(g, minimum_power, maximum_power, degree)

    records: list[dict[str, Any]] = []
    first_nonzero: dict[str, Any] | None = None
    for k in range(1, moments + 1):
        coefficient = pulled_back_form_coefficient(
            amplitude, powers, g, m * k - 1
        )
        direct_normalised = direct_amplitude_residue_moment(phase, amplitude, k)
        require(
            coefficient == direct_normalised,
            f"local form/residue identity failed at moment {k}",
        )
        direct_original = direct_amplitude_residue_moment(
            original_phase, amplitude, k
        )
        require(
            direct_original == target_scale**k * direct_normalised,
            f"target-scaling identity failed at moment {k}",
        )
        record = {
            "k": k,
            "coefficient_tau_mk_minus_1": str(coefficient),
            "normalised_residue": str(direct_normalised),
            "original_residue": str(direct_original),
            "zero": direct_original == 0,
        }
        records.append(record)
        if first_nonzero is None and direct_original != 0:
            first_nonzero = record

    status = "nonvanishing_witness" if first_nonzero else "finite_prefix_zero"
    result: dict[str, Any] = {
        "schema": "laurent-amplitude-residue-certificate-v1",
        "status": status,
        "input": {"phase": phase_text, "amplitude": amplitude_text},
        "normalised_phase": canonical_laurent(phase),
        "zero_pole_order_m": m,
        "target_scale_removed": str(target_scale),
        "moments_checked": moments,
        "records": records,
        "first_nonzero_witness": first_nonzero,
        "identity": (
            "Res_0 L^k A dz = [tau^(m*k-1)] A(phi(tau))*phi'(tau)"
        ),
        "claim_boundary": (
            "A nonzero record disproves persistent vanishing; a zero finite "
            "prefix is not an all-k certificate."
        ),
    }
    result["certificate_sha256"] = canonical_hash(result)
    return result


def analyse_laurent_moments(
    phase_text: str, primitive_text: str, moments: int
) -> dict[str, Any]:
    require(moments >= 1, "at least one positive moment is required")
    original_phase = parse_laurent(phase_text)
    primitive = parse_laurent(primitive_text)
    phase, m, target_scale = normalise_at_zero(original_phase)
    minimum_power = min(primitive) if primitive else 0
    maximum_power = max(primitive) if primitive else 0
    degree = m * moments - minimum_power + maximum_power + 8
    g = zero_inverse_series(phase, m, degree)
    powers = series_powers(g, minimum_power, maximum_power, degree)

    records: list[dict[str, Any]] = []
    first_nonzero: dict[str, Any] | None = None
    for k in range(1, moments + 1):
        coefficient = composed_coefficient(primitive, powers, m * k)
        local_identity_value = m * k * coefficient
        direct_normalised = direct_residue_moment(phase, primitive, k)
        require(
            local_identity_value == direct_normalised,
            f"local coefficient/residue identity failed at moment {k}",
        )
        direct_original = direct_residue_moment(original_phase, primitive, k)
        require(
            direct_original == target_scale**k * direct_normalised,
            f"target-scaling identity failed at moment {k}",
        )
        record = {
            "k": k,
            "coefficient_tau_mk": str(coefficient),
            "normalised_residue": str(direct_normalised),
            "original_residue": str(direct_original),
            "zero": direct_original == 0,
        }
        records.append(record)
        if first_nonzero is None and direct_original != 0:
            first_nonzero = record

    status = "nonvanishing_witness" if first_nonzero else "finite_prefix_zero"
    result: dict[str, Any] = {
        "schema": "laurent-residue-moment-certificate-v1",
        "status": status,
        "input": {"phase": phase_text, "primitive_Q": primitive_text},
        "normalised_phase": canonical_laurent(phase),
        "zero_pole_order_m": m,
        "target_scale_removed": str(target_scale),
        "moments_checked": moments,
        "records": records,
        "first_nonzero_witness": first_nonzero,
        "theorem_criterion": (
            "all moments vanish iff every positive coefficient "
            "[tau^(m*k)] Q(phi(tau)) vanishes"
        ),
        "claim_boundary": (
            "A nonzero record disproves persistent vanishing.  A zero finite prefix "
            "is supporting computation only unless a separate symbolic mechanism or "
            "proof establishes the infinite criterion."
        ),
    }
    result["certificate_sha256"] = canonical_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, help="trusted Q[z,z^-1] expression")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--amplitude",
        help="trusted Laurent amplitude A(z) in A(z) dz",
    )
    input_group.add_argument(
        "--primitive",
        help="trusted Laurent primitive G(z), with amplitude dG",
    )
    parser.add_argument("--moments", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.amplitude is not None:
        result = analyse_laurent_amplitude(args.phase, args.amplitude, args.moments)
    else:
        result = analyse_laurent_moments(args.phase, args.primitive, args.moments)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
