#!/usr/bin/env python3
"""Score an EPOB-1 submission against the frozen exact answer key."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
S = sp.Symbol("s")


def proportional(observed: list[str], expected: list[str]) -> bool:
    if len(observed) != len(expected):
        return False
    left = [sp.sympify(value, locals={"s": S}) for value in observed]
    right = [sp.sympify(value, locals={"s": S}) for value in expected]
    pivot = next((index for index, value in enumerate(right) if value != 0), None)
    if pivot is None or left[pivot] == 0:
        return False
    factor = sp.cancel(left[pivot] / right[pivot])
    return factor != 0 and all(
        sp.cancel(left[index] - factor * right[index]) == 0
        for index in range(len(left))
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--answer-key", type=Path, default=ROOT / "benchmarks" / "epob1_answer_key.json")
    args = parser.parse_args()
    submission = json.loads(args.submission.read_text())
    if submission.get("schema") != "epob1-submission-v1":
        raise SystemExit("unknown EPOB-1 submission schema")
    observed = {case["id"]: case for case in submission.get("cases", [])}
    answers = json.loads(args.answer_key.read_text())["cases"]
    order_points = support_points = operator_points = 0
    operator_total = 0
    records = []
    for expected in answers:
        case = observed.get(expected["id"], {})
        order_ok = case.get("order") == expected["order"]
        support_ok = case.get("support") == expected["support"]
        operator_ok = None
        if "operator_coefficients_low_to_high" in expected:
            operator_total += 1
            supplied_operator = case.get("operator_coefficients_low_to_high")
            operator_ok = isinstance(supplied_operator, list) and proportional(
                supplied_operator, expected["operator_coefficients_low_to_high"]
            )
            operator_points += int(operator_ok)
        order_points += int(order_ok)
        support_points += int(support_ok)
        records.append({"id": expected["id"], "order": order_ok, "support": support_ok, "operator": operator_ok})
    result = {
        "schema": "epob1-score-v1",
        "status": "pass" if order_points == len(answers) and support_points == len(answers) and operator_points == operator_total else "incomplete-or-mismatch",
        "scores": {
            "order": f"{order_points}/{len(answers)}",
            "support": f"{support_points}/{len(answers)}",
            "operator": f"{operator_points}/{operator_total}",
        },
        "cases": records,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
