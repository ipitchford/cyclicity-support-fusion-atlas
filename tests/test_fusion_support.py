#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fusion_support import analyse_phase  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check(phase: str, expected_rank: int, expected_support: set[int]) -> dict:
    result = analyse_phase(phase)
    identity = result["theorem_identity"]
    support = set(result["inverse_at_infinity"]["support"])
    require(identity["all_equal"] is True, f"rank identity failed for {phase}")
    require(identity["twisted_cyclic_rank"] == expected_rank, f"cyclic rank failed for {phase}")
    require(identity["inverse_support_size"] == expected_rank, f"support size failed for {phase}")
    require(support == expected_support, f"support failed for {phase}: {support}")
    return result


def main() -> None:
    quartic = check("x**4 + x", 3, {1, 2, 3})
    collision = check("(x**4 + x)**3", 3, {1, 7, 10})
    quadratic_outer = check("(x**3 + x)**2", 2, {1, 5})
    chebyshev = check("16*x**5 - 20*x**3 + 5*x", 2, {1, 4})
    even_sextic = check("x**6 + x**2 + 1", 3, {1, 3, 5})

    # The Ritt collision viewed through its degree-four right factor Q=x^4+x:
    m4 = collision["fusion_profiles_by_candidate_right_degree"]["4"]
    require(m4["fibre_size_partition"] == [1, 1, 1], "quartic-view fibre partition failed")
    require(m4["right_factor_cyclic_rank"] == 3, "quartic-view factor rank failed")
    require(m4["full_fusion_all_block_spans_equal"] is True, "quartic-view fusion failed")
    require(m4["number_of_distinct_block_spans"] == 1, "quartic-view span count failed")
    require(set(m4["pairwise_intersection_dimension_by_delta"].values()) == {3},
            "quartic-view intersections failed")

    # The same polynomial after the Ritt move P=H(x^3): block lines span W_P.
    m3 = collision["fusion_profiles_by_candidate_right_degree"]["3"]
    require(m3["fibre_size_partition"] == [3], "cubic-view fibre partition failed")
    require(m3["right_factor_cyclic_rank"] == 1, "cubic-view factor rank failed")
    require(m3["full_fusion_all_block_spans_equal"] is False, "cubic-view fusion failed")
    require(m3["number_of_distinct_block_spans"] == 4, "cubic-view span count failed")
    require(m3["pairwise_intersection_dimension_by_delta"]["0"] == 1,
            "cubic-view self-intersection failed")
    require(all(
        m3["pairwise_intersection_dimension_by_delta"][str(delta)] == 0
        for delta in (1, 2, 3)
    ), "cubic-view off-diagonal intersections failed")

    # Independent regression facts.
    require(quartic["fusion_profiles_by_candidate_right_degree"]["4"][
        "right_factor_cyclic_rank"
    ] == 3, "quartic factor regression failed")
    require(quadratic_outer["fusion_profiles_by_candidate_right_degree"]["3"][
        "fibre_size_partition"
    ] == [1, 1], "quadratic-outer regression failed")
    require(chebyshev["theorem_identity"]["twisted_cyclic_rank"] == 2,
            "Chebyshev regression failed")
    require(even_sextic["theorem_identity"]["twisted_cyclic_rank"] == 3,
            "even sextic regression failed")

    print("all support, cyclic-rank, fusion, and Ritt-view tests passed")


if __name__ == "__main__":
    main()
