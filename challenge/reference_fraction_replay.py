#!/usr/bin/env python3
"""CAS-free reference replay for the inverse-support challenge."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))

from lib import q_deRham, support  # noqa: E402


def digest(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=ROOT / "challenge" / "spec.json")
    parser.add_argument("--answer-key", type=Path, default=ROOT / "challenge" / "answer_key.json")
    parser.add_argument("--output", type=Path, default=ROOT / "receipts" / "fraction_replay_challenge_receipt.json")
    args = parser.parse_args()
    if "sympy" in sys.modules:
        raise RuntimeError("CAS-free replay unexpectedly imported SymPy")
    spec = json.loads(args.spec.read_text())
    answers = {case["id"]: case for case in json.loads(args.answer_key.read_text())["cases"]}
    records = []
    for case in spec["cases"]:
        coefficients = [Fraction(value) for value in case["coefficients_ascending"]]
        s_values = [Fraction(value) for value in case["s_specialisations"]]
        observed_support = sorted(support(coefficients, case["support_depth"]))
        observed_rank = q_deRham(coefficients, s_values=s_values)
        expected = answers[case["id"]]
        if observed_support != expected["support"] or observed_rank != expected["rank"]:
            raise RuntimeError(
                f"challenge mismatch {case['id']}: support={observed_support}, rank={observed_rank}"
            )
        if observed_rank != len(observed_support):
            raise RuntimeError(f"rank/support identity mismatch: {case['id']}")
        record = {
            "id": case["id"],
            "rank": observed_rank,
            "support": observed_support,
            "rank_equals_support_size": True,
            "exact_rational_specialisations": case["s_specialisations"],
            "support_depth": case["support_depth"],
            "status": "pass",
        }
        records.append(record)
        print(f"[PASS] {case['id']}: rank {observed_rank}, support {observed_support}")
    result = {
        "schema": "inverse-support-fraction-replay-receipt-v1",
        "status": "pass",
        "implementation": "stdlib Fraction backend; no SymPy import",
        "case_count": len(records),
        "cases": records,
        "claim_boundary": spec["claim_boundary"],
    }
    result["receipt_sha256"] = digest(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("FRACTION-ONLY REPLAY CHALLENGE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
