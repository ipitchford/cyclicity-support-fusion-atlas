#!/usr/bin/env python3
"""Run the EPOB-1 reference benchmark and record correctness plus timings."""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
import platform
import statistics
import sys
import time

import mpmath
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from fusion_support import analyse_phase, parse_polynomial, require  # noqa: E402
from generic_degree12_rank_control import build as generic_control  # noqa: E402
from order_oracle import exact_scalar_operator  # noqa: E402


def timed(callable_object, repeats: int):
    samples = []
    value = None
    for _ in range(repeats):
        gc.collect()
        started = time.perf_counter()
        value = callable_object()
        samples.append(time.perf_counter() - started)
    return value, samples


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=ROOT / "benchmarks" / "epob1_spec.json")
    parser.add_argument("--answer-key", type=Path, default=ROOT / "benchmarks" / "epob1_answer_key.json")
    parser.add_argument("--output", type=Path, default=ROOT / "receipts" / "epob1_reference_run.json")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    require(args.repeats >= 1, "repeats must be positive")
    spec = json.loads(args.spec.read_text())
    answers = {case["id"]: case for case in json.loads(args.answer_key.read_text())["cases"]}
    records = []

    for case in spec["cases"]:
        expected = answers[case["id"]]
        if case["track"] == "rank_only":
            control, samples = timed(generic_control, args.repeats)
            observed_order = control["generic_rank"]
            observed_support = control["inverse_support"]
            operator = None
            prediction_samples = samples
            operator_samples = []
        else:
            analysis, prediction_samples = timed(lambda: analyse_phase(case["phase"]), args.repeats)
            phase = parse_polynomial(case["phase"])
            operator, operator_samples = timed(lambda: exact_scalar_operator(phase), args.repeats)
            observed_order = analysis["theorem_identity"]["twisted_cyclic_rank"]
            observed_support = analysis["inverse_at_infinity"]["support"]
            require(operator["order"] == observed_order, f"operator/order mismatch: {case['id']}")

        require(observed_order == expected["order"], f"order mismatch: {case['id']}")
        require(observed_support == expected["support"], f"support mismatch: {case['id']}")
        if operator is not None:
            require(
                operator["coefficients"] == expected["operator_coefficients_low_to_high"],
                f"operator mismatch: {case['id']}",
            )
        records.append({
            "id": case["id"],
            "track": case["track"],
            "degree": expected["degree"],
            "ambient_order": expected["degree"] - 1,
            "order": observed_order,
            "support": observed_support,
            "compression_ratio_ambient_over_order": f"{expected['degree'] - 1}/{observed_order}",
            "prediction_seconds": prediction_samples,
            "prediction_median_seconds": statistics.median(prediction_samples),
            "operator_seconds": operator_samples,
            "operator_median_seconds": statistics.median(operator_samples) if operator_samples else None,
            "operator_coefficient_characters": (
                sum(len(value) for value in operator["coefficients"]) if operator else None
            ),
            "status": "pass",
        })
        print(f"[PASS] {case['id']}: degree {expected['degree']}, order {observed_order}")

    result = {
        "schema": "epob1-reference-run-v1",
        "status": "pass",
        "benchmark_version": spec["version"],
        "repeats": args.repeats,
        "environment": {
            "python": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "mpmath": mpmath.__version__,
        },
        "scores": {
            "order": f"{len(records)}/{len(records)}",
            "support": f"{len(records)}/{len(records)}",
            "operator": f"{sum(r['track'] == 'operator' for r in records)}/{sum(r['track'] == 'operator' for r in records)}",
        },
        "cases": records,
        "claim_boundary": "Reference correctness and local timings only; no cross-system performance claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("EPOB-1 REFERENCE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
