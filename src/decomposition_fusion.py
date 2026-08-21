#!/usr/bin/env python3
"""Attach exact Fourier-fusion data to verified polynomial decompositions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.polys.polytools import decompose

from fusion_support import analyse_phase, canonical_expr, parse_polynomial, require, x


SCHEMA = "decomposition-aware-fusion-report-v1"


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compose(outer: sp.Poly, inner: sp.Poly) -> sp.Poly:
    return sp.Poly(sp.expand(outer.as_expr().subs(x, inner.as_expr())), x, domain=sp.QQ)


def compose_chain(factors: list[sp.Poly]) -> sp.Poly:
    require(factors, "decomposition chain is empty")
    result = factors[-1]
    for factor in reversed(factors[:-1]):
        result = compose(factor, result)
    return result


def suffix_polynomial(factors: list[sp.Poly], start: int) -> sp.Poly:
    return compose_chain(factors[start:])


def chain_key(factors: list[sp.Poly]) -> tuple[str, ...]:
    return tuple(canonical_expr(factor.as_expr()) for factor in factors)


def factor_is_indecomposable(factor: sp.Poly) -> bool:
    pieces = decompose(factor.as_expr(), x)
    return len(pieces) == 1


def validate_chain(phase: sp.Poly, name: str, factor_texts: list[str]) -> dict[str, Any]:
    require(len(factor_texts) >= 2, f"chain {name} must have at least two factors")
    factors = [parse_polynomial(text) for text in factor_texts]
    reconstructed = compose_chain(factors)
    require(reconstructed == phase, f"chain {name} does not compose to the supplied phase")
    return {
        "name": name,
        "factors": factors,
        "factor_texts": factor_texts,
        "factor_degrees": [factor.degree() for factor in factors],
        "all_factors_indecomposable_over_Q_by_sympy": all(
            factor_is_indecomposable(factor) for factor in factors
        ),
    }


def analyse_chain(phase_text: str, phase_analysis: dict[str, Any], chain: dict[str, Any]) -> dict[str, Any]:
    factors = chain["factors"]
    phase_rank = phase_analysis["theorem_identity"]["twisted_cyclic_rank"]
    nodes = []
    ranks_from_inner_to_full = []
    for start in range(len(factors) - 1, 0, -1):
        suffix = suffix_polynomial(factors, start)
        suffix_text = sp.sstr(suffix.as_expr())
        suffix_analysis = analyse_phase(suffix_text)
        suffix_rank = suffix_analysis["theorem_identity"]["twisted_cyclic_rank"]
        profile = phase_analysis["fusion_profiles_by_candidate_right_degree"].get(
            str(suffix.degree())
        )
        require(profile is not None, f"missing divisor profile for actual suffix degree {suffix.degree()}")
        require(
            profile["right_factor_cyclic_rank"] == suffix_rank,
            f"support projection disagrees with actual suffix rank in {chain['name']}",
        )
        ranks_from_inner_to_full.append(suffix_rank)
        nodes.append({
            "suffix_start_zero_based": start,
            "suffix": suffix_text,
            "suffix_degree": suffix.degree(),
            "actual_suffix_rank": suffix_rank,
            "actual_suffix_support": suffix_analysis["inverse_at_infinity"]["support"],
            "predicted_rank_from_parent_support_projection": profile["right_factor_cyclic_rank"],
            "fibre_size_partition": profile["fibre_size_partition"],
            "number_of_distinct_block_spans": profile["number_of_distinct_block_spans"],
            "full_fusion": profile["full_fusion_all_block_spans_equal"],
            "direct_sum": profile["block_spans_form_direct_sum"],
            "pairwise_intersection_dimension_by_delta": profile[
                "pairwise_intersection_dimension_by_delta"
            ],
        })
    ranks_from_inner_to_full.append(phase_rank)
    rank_creation = [
        ranks_from_inner_to_full[index + 1] - ranks_from_inner_to_full[index]
        for index in range(len(ranks_from_inner_to_full) - 1)
    ]
    return {
        "name": chain["name"],
        "factors_outer_to_inner": chain["factor_texts"],
        "factor_degrees": chain["factor_degrees"],
        "exact_composition_validated": True,
        "all_factors_indecomposable_over_Q_by_sympy": chain[
            "all_factors_indecomposable_over_Q_by_sympy"
        ],
        "proper_suffix_nodes_inner_to_outer": nodes,
        "ranks_inner_to_full": ranks_from_inner_to_full,
        "rank_creation_by_level": rank_creation,
        "total_rank_creation": sum(rank_creation),
    }


def analyse_decompositions(
    phase_text: str, supplied_chains: list[dict[str, Any]]
) -> dict[str, Any]:
    phase = parse_polynomial(phase_text)
    phase_analysis = analyse_phase(phase_text)
    validated = [
        validate_chain(phase, chain["name"], chain["factors_outer_to_inner"])
        for chain in supplied_chains
    ]

    automatic_texts = [sp.sstr(value) for value in decompose(phase.as_expr(), x)]
    if len(automatic_texts) >= 2:
        automatic = validate_chain(phase, "sympy_discovered_chain", automatic_texts)
        known_keys = {chain_key(chain["factors"]) for chain in validated}
        if chain_key(automatic["factors"]) not in known_keys:
            validated.append(automatic)

    reports = [analyse_chain(phase_text, phase_analysis, chain) for chain in validated]
    result = {
        "schema": SCHEMA,
        "status": "pass",
        "phase": phase_text,
        "degree": phase.degree(),
        "global_rank": phase_analysis["theorem_identity"]["twisted_cyclic_rank"],
        "global_support": phase_analysis["inverse_at_infinity"]["support"],
        "validated_chain_count": len(reports),
        "chains": reports,
        "ritt_consistency": {
            "all_chains_compose_exactly": True,
            "every_actual_suffix_rank_matches_support_projection": True,
            "global_rank_same_across_chains": True,
        },
        "claim_boundary": (
            "The supplied chains and at most one SymPy-discovered chain are exact "
            "decomposition witnesses. This report does not assert that they exhaust "
            "the complete decomposition lattice over C."
        ),
    }
    result["report_sha256"] = canonical_hash(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--chains", type=Path, required=True, help="JSON array of chain objects")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    chains = json.loads(args.chains.read_text())
    result = analyse_decompositions(args.phase, chains)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
