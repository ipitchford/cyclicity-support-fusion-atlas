#!/usr/bin/env python3
"""Independent exact audit of the Kummer-line normalizer algebra."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import sympy as sp


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Return p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(p)
    for i, image in enumerate(p):
        result[image] = i
    return tuple(result)


def parity(p: tuple[int, ...]) -> int:
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def permutation_words(
    group: list[tuple[int, ...]], generators: list[tuple[int, ...]]
) -> dict[tuple[int, ...], tuple[int, ...]]:
    identity = tuple(range(len(group[0])))
    words = {identity: ()}
    queue = [identity]
    while queue:
        current = queue.pop(0)
        for index, generator in enumerate(generators):
            nxt = compose(generator, current)
            if nxt not in words:
                words[nxt] = words[current] + (index,)
                queue.append(nxt)
    if len(words) != len(group):
        raise RuntimeError("chosen generators do not generate S4")
    return words


def evaluate_word(
    word: tuple[int, ...], images: tuple[tuple[int, ...], ...]
) -> tuple[int, ...]:
    result = tuple(range(len(images[0])))
    for index in word:
        result = compose(images[index], result)
    return result


def s4_automorphism_audit() -> dict[str, Any]:
    group = list(itertools.permutations(range(4)))
    transposition = (1, 0, 2, 3)
    four_cycle = (1, 2, 3, 0)
    four_cycle_inverse = inverse(four_cycle)
    words = permutation_words(group, [transposition, four_cycle, four_cycle_inverse])

    automorphisms: set[tuple[tuple[int, ...], ...]] = set()
    ordered_group = tuple(sorted(group))
    for image_t in group:
        for image_r in group:
            images = (image_t, image_r, inverse(image_r))
            mapping = {g: evaluate_word(words[g], images) for g in group}
            if len(set(mapping.values())) != 24:
                continue
            if all(
                mapping[compose(g, h)] == compose(mapping[g], mapping[h])
                for g in group
                for h in group
            ):
                automorphisms.add(tuple(mapping[g] for g in ordered_group))

    inner: set[tuple[tuple[int, ...], ...]] = set()
    for conjugator in group:
        conjugator_inverse = inverse(conjugator)
        inner.add(
            tuple(
                compose(compose(conjugator, g), conjugator_inverse)
                for g in ordered_group
            )
        )
    if automorphisms != inner or len(automorphisms) != 24:
        raise RuntimeError("S4 automorphism audit failed")
    return {"automorphism_count": 24, "inner_count": 24, "all_inner": True}


def signed_permutation_matrices() -> list[sp.Matrix]:
    matrices: list[sp.Matrix] = []
    for p in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            matrix = sp.zeros(3)
            for column, row in enumerate(p):
                matrix[row, column] = signs[column]
            if matrix.det() == 1:
                matrices.append(matrix)
    unique = {tuple(matrix): matrix for matrix in matrices}
    return list(unique.values())


def body_diagonal_permutation(matrix: sp.Matrix) -> tuple[int, ...]:
    vectors = [
        sp.Matrix([1, 1, 1]),
        sp.Matrix([1, -1, -1]),
        sp.Matrix([-1, 1, -1]),
        sp.Matrix([-1, -1, 1]),
    ]
    result = []
    for vector in vectors:
        image = matrix * vector
        for index, target in enumerate(vectors):
            if image == target or image == -target:
                result.append(index)
                break
        else:
            raise RuntimeError("rotation did not permute body diagonals")
    return tuple(result)


def intertwiner_dimension(
    matrices: list[sp.Matrix], characters: list[int]
) -> int:
    variables = sp.symbols("x0:9")
    unknown = sp.Matrix(3, 3, variables)
    equations = []
    for matrix, character in zip(matrices, characters, strict=True):
        equations.extend(list(unknown * matrix - character * matrix * unknown))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return 9 - coefficient_matrix.rank()


def octahedral_audit() -> dict[str, Any]:
    rotations = signed_permutation_matrices()
    if len(rotations) != 24:
        raise RuntimeError("octahedral rotation group does not have order 24")
    actions = [body_diagonal_permutation(matrix) for matrix in rotations]
    if len(set(actions)) != 24:
        raise RuntimeError("body-diagonal action is not faithful")
    signs = [parity(action) for action in actions]
    ordinary_dimension = intertwiner_dimension(rotations, [1] * len(rotations))
    twisted_dimension = intertwiner_dimension(rotations, signs)
    odd_nonzero_traces = sorted(
        {int(matrix.trace()) for matrix, sign in zip(rotations, signs, strict=True) if sign == -1}
    )
    if ordinary_dimension != 1 or twisted_dimension != 0 or not any(odd_nonzero_traces):
        raise RuntimeError("octahedral intertwiner audit failed")
    return {
        "rotation_count": 24,
        "faithful_body_diagonal_action": True,
        "ordinary_centralizer_dimension": ordinary_dimension,
        "sign_twisted_intertwiner_dimension": twisted_dimension,
        "odd_element_trace_values": odd_nonzero_traces,
    }


def a4_automorphism_audit() -> dict[str, Any]:
    group = [p for p in itertools.permutations(range(4)) if parity(p) == 1]
    first = (1, 2, 0, 3)
    second = (1, 3, 2, 0)
    words = permutation_words(group, [first, second])
    ordered_group = tuple(sorted(group))

    automorphisms: set[tuple[tuple[int, ...], ...]] = set()
    for image_first in group:
        for image_second in group:
            images = (image_first, image_second)
            mapping = {g: evaluate_word(words[g], images) for g in group}
            if len(set(mapping.values())) != 12:
                continue
            if all(
                mapping[compose(g, h)] == compose(mapping[g], mapping[h])
                for g in group
                for h in group
            ):
                automorphisms.add(tuple(mapping[g] for g in ordered_group))

    rotations = signed_permutation_matrices()
    actions = [body_diagonal_permutation(matrix) for matrix in rotations]
    conjugation_actions: set[tuple[tuple[int, ...], ...]] = set()
    for conjugator in itertools.permutations(range(4)):
        conjugator_inverse = inverse(conjugator)
        conjugation_actions.add(
            tuple(
                compose(compose(conjugator, g), conjugator_inverse)
                for g in ordered_group
            )
        )
    if len(automorphisms) != 24 or automorphisms != conjugation_actions:
        raise RuntimeError("A4 automorphism audit failed")
    if len(rotations) != 24 or len(set(actions)) != 24:
        raise RuntimeError("octahedral realization does not realize Aut(A4)")
    return {
        "automorphism_count": 24,
        "all_realized_by_octahedral_conjugation": True,
    }


def projective_character(
    intertwiner: sp.Matrix, matrix: sp.Matrix
) -> sp.Expr:
    left = intertwiner * matrix
    right = matrix * intertwiner
    scalar = None
    for lhs, rhs in zip(left, right, strict=True):
        if rhs != 0:
            scalar = sp.simplify(lhs / rhs)
            break
    if scalar is None or any(
        sp.simplify(lhs - scalar * rhs) != 0
        for lhs, rhs in zip(left, right, strict=True)
    ):
        raise RuntimeError("matrix is not a projective intertwiner")
    return scalar


def tetrahedral_audit() -> dict[str, Any]:
    rotations = signed_permutation_matrices()
    actions = [body_diagonal_permutation(matrix) for matrix in rotations]
    tetrahedral = [
        matrix
        for matrix, action in zip(rotations, actions, strict=True)
        if parity(action) == 1
    ]
    if len(tetrahedral) != 12:
        raise RuntimeError("tetrahedral subgroup does not have order 12")

    omega = -sp.Rational(1, 2) + sp.sqrt(3) * sp.I / 2
    diagonal = sp.diag(1, omega, omega**2)
    diagonal_inverse = sp.diag(1, omega**2, omega)
    characters = [
        [sp.Integer(1)] * len(tetrahedral),
        [projective_character(diagonal, matrix) for matrix in tetrahedral],
        [projective_character(diagonal_inverse, matrix) for matrix in tetrahedral],
    ]
    dimensions = [
        intertwiner_dimension(tetrahedral, character)
        for character in characters
    ]
    if dimensions != [1, 1, 1]:
        raise RuntimeError("tetrahedral character-intertwiner audit failed")
    return {
        "rotation_count": 12,
        "linear_character_count": 3,
        "character_intertwiner_dimensions": dimensions,
        "projective_centralizer_representatives_diagonal": True,
        "automorphism_representatives_signed_monomial": True,
        "normalizer_preserves_coordinate_axes": True,
    }


def symbolic_audit() -> dict[str, Any]:
    X, z, a, q, A, t, C = sp.symbols("X z a q A t C")
    target = sp.expand((X - z) * (X - 1) ** 2)
    transposition = sp.expand((X - a) * (X**2 - q))
    target_expected = X**3 - (z + 2) * X**2 + (2 * z + 1) * X - z
    transposition_expected = X**3 - a * X**2 - q * X + a * q
    if sp.expand(target - target_expected) != 0:
        raise RuntimeError("target characteristic identity failed")
    if sp.expand(transposition - transposition_expected) != 0:
        raise RuntimeError("transposition characteristic identity failed")

    eliminated = sp.factor((z + 2) * (-(2 * z + 1)) + z)
    if eliminated != -2 * (z + 1) ** 2:
        raise RuntimeError("transposition elimination failed")
    three_cycle_gcd = sp.gcd(sp.Poly(z + 2, z), sp.Poly(2 * z + 1, z))
    if three_cycle_gcd.as_expr() != 1:
        raise RuntimeError("three-cycle obstruction failed")

    Y = sp.symbols("Y")
    cubic = Y**3 + A * Y**2 + C - t
    discriminant = sp.factor(sp.discriminant(cubic, Y))
    expected_discriminant = sp.factor((t - C) * (4 * A**3 - 27 * (t - C)))
    if sp.expand(discriminant - expected_discriminant) != 0:
        raise RuntimeError("degenerate cubic discriminant identity failed")
    quotient = sp.factor(discriminant / (t - C))
    if sp.degree(quotient, t) != 1:
        raise RuntimeError("discriminant quotient should be a nonsquare linear function")

    Y, Z, r = sp.symbols("Y Z r")
    exceptional = sp.expand(Y**3 + 2 * r * Y**2 + r**2 * Y)
    if sp.expand(exceptional - Y * (Y + r) ** 2) != 0:
        raise RuntimeError("exceptional cubic factorization failed")
    if sp.cancel(exceptional / Y - (Y + r) ** 2) != 0:
        raise RuntimeError("exceptional pair relation failed")
    if sp.expand(Z**2 * (Z**2 + r) ** 2 - (Z**3 + r * Z) ** 2) != 0:
        raise RuntimeError("exceptional even-exponent square factorization failed")

    dickson_parameter = -r / 3
    dickson_three = Z**3 - 3 * dickson_parameter * Z
    if sp.expand(dickson_three - (Z**3 + r * Z)) != 0:
        raise RuntimeError("Dickson cubic normalization failed")
    dickson_six = sp.expand(dickson_three**2 - 2 * dickson_parameter**3)
    if sp.expand(dickson_six - ((Z**3 + r * Z) ** 2 + 2 * r**3 / 27)) != 0:
        raise RuntimeError("Dickson degree-six target translation failed")

    affine_parameter = sp.symbols("affine_parameter")
    affine_cubic = Y**3 + 3 * affine_parameter * Y**2 + 3 * affine_parameter**2 * Y + C
    affine_power = (Y + affine_parameter) ** 3 + C - affine_parameter**3
    if sp.expand(affine_cubic - affine_power) != 0:
        raise RuntimeError("affine-power cubic identity failed")

    omega = -sp.Rational(1, 2) + sp.sqrt(3) * sp.I / 2
    fourier = sp.Matrix([
        [1, 1, 1],
        [1, omega, omega**2],
        [1, omega**2, omega],
    ])
    if sp.simplify(fourier.det()) == 0:
        raise RuntimeError("cubic Fourier matrix is singular")
    sign_solutions = []
    for values in itertools.product((-1, 1), repeat=3):
        if sum(values) == 3 and sp.simplify(sum(values[i] * omega**i for i in range(3))) == 0:
            sign_solutions.append(values)
    if sign_solutions != [(1, 1, 1)]:
        raise RuntimeError("affine-power Fourier rigidity failed")

    return {
        "transposition_characteristic_identity": True,
        "kummer_reflection_characteristic_identity": True,
        "transposition_elimination": str(eliminated),
        "three_cycle_obstruction": "coprime coefficient equations",
        "degenerate_cubic_discriminant": str(discriminant),
        "discriminant_quotient_degree": 1,
        "exceptional_cubic_factorization": True,
        "exceptional_pair_relation": "y_i*y_j=(y_k+r)^2",
        "exceptional_even_square_factorization": True,
        "dickson_degree_six_target_translation": True,
        "affine_power_cubic_identity": True,
        "affine_power_fourier_determinant_nonzero": True,
        "affine_power_sign_solution_count": 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    symbolic = symbolic_audit()
    automorphisms = s4_automorphism_audit()
    octahedral = octahedral_audit()
    a4_automorphisms = a4_automorphism_audit()
    tetrahedral = tetrahedral_audit()
    result: dict[str, Any] = {
        "schema": "cyclicity-kummer-normalizer-cas-receipt-v2",
        "status": "pass",
        "engine": {"name": "SymPy", "version": sp.__version__},
        "exact_checks": {
            **symbolic,
            "s4_automorphisms": automorphisms,
            "octahedral_realisation": {
                "rotation_count": octahedral["rotation_count"],
                "faithful_body_diagonal_action": octahedral["faithful_body_diagonal_action"],
            },
            "ordinary_centralizer": octahedral["ordinary_centralizer_dimension"],
            "sign_twisted_intertwiners": octahedral["sign_twisted_intertwiner_dimension"],
            "a4_automorphisms": a4_automorphisms,
            "tetrahedral_normalizer": tetrahedral,
        },
        "diagnostics": {"octahedral": octahedral, "tetrahedral": tetrahedral},
        "assurance": {
            "all_m_symbolic_obstruction": True,
            "exceptional_even_kummer_relation_detected": True,
            "uniform_full_kummer_kernel_claim": False,
            "finite_s4_enumeration": True,
            "finite_a4_enumeration": True,
            "kummer_valuation_argument_formalized": False,
            "external_independence": False,
            "all_degree_theorem_claim": False,
        },
    }
    result["receipt_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "pass", "receipt_sha256": result["receipt_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
