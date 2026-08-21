#!/usr/bin/env python3
"""Fast exact generic-rank control for the degree-twelve comparison phase.

The fully symbolic order-eleven certificate is intentionally not part of the
quick oracle gate: its expression swell is substantial and it is not the
low-order use case served by the oracle.  Instead, an exact rational
specialisation attaining the ambient rank proves that this particular phase
has generic rank eleven, since specialised rank cannot exceed generic rank
and the ambient twisted de Rham rank is eleven.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))

from lib import poly_from_dict, q_deRham, support  # noqa: E402


PHASE = "x**12 + x**10 + x**3"
COEFFICIENTS = poly_from_dict({12: 1, 10: 1, 3: 1})
SPECIALISATIONS = [Fraction(3, 7), Fraction(-5, 2)]


def canonical_hash(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build() -> dict:
    ranks = [q_deRham(COEFFICIENTS, s_values=[value]) for value in SPECIALISATIONS]
    ambient_rank = 11
    if max(ranks) != ambient_rank:
        raise RuntimeError(f"degree-twelve generic-rank control failed: {ranks}")
    inverse_support = sorted(support(COEFFICIENTS, 120))
    if inverse_support != list(range(1, 12)):
        raise RuntimeError(f"degree-twelve support control failed: {inverse_support}")
    result = {
        "schema": "exponential-period-order-oracle-generic-control-v1",
        "status": "pass",
        "phase": PHASE,
        "degree": 12,
        "ambient_rank": ambient_rank,
        "specialisations": [
            {"s": str(value), "exact_specialised_rank": rank}
            for value, rank in zip(SPECIALISATIONS, ranks)
        ],
        "inverse_support": inverse_support,
        "generic_rank": ambient_rank,
        "inference": (
            "An exact specialised rank of eleven is bounded above by the generic "
            "rank, while the ambient twisted de Rham rank is eleven."
        ),
        "claim_boundary": (
            "This is an exact rank control, not a frozen symbolic order-eleven "
            "operator and not an independent external reproduction."
        ),
    }
    result["receipt_sha256"] = canonical_hash(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "receipts" / "order_oracle_generic_degree12_control.json",
    )
    args = parser.parse_args()
    result = build()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded, encoding="utf-8")
    print(
        "generic degree-12 exact-rank control PASS "
        f"(rank {result['generic_rank']}, receipt {result['receipt_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
