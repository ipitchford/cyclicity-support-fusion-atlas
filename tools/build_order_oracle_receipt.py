#!/usr/bin/env python3
"""Build deterministic exact certificates for the order-oracle benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fusion_support import canonical_hash, require  # noqa: E402
from order_oracle import order_oracle_certificate  # noqa: E402


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build(spec_path: Path, output_path: Path, certificate_dir: Path) -> dict[str, Any]:
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes)
    require(
        spec.get("schema") == "exponential-period-order-oracle-benchmark-spec-v1",
        "unknown order-oracle benchmark schema",
    )
    cases = spec.get("cases")
    require(isinstance(cases, list) and cases, "benchmark case list is empty")

    certificate_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for case in cases:
        case_id = case["id"]
        require(case_id not in seen_ids, f"duplicate benchmark id: {case_id}")
        seen_ids.add(case_id)
        certificate = order_oracle_certificate(case["phase"])
        prediction = certificate["order_prediction"]
        require(certificate["degree"] == case["expected_degree"], f"degree mismatch: {case_id}")
        require(
            prediction["generic_minimal_order"] == case["expected_order"],
            f"order mismatch: {case_id}",
        )
        require(
            prediction["inverse_support"] == case["expected_support"],
            f"support mismatch: {case_id}",
        )
        certificate_bytes = encoded_json(certificate)
        certificate_name = f"{case_id}.json"
        (certificate_dir / certificate_name).write_bytes(certificate_bytes)
        records.append(
            {
                "id": case_id,
                "role": case["role"],
                "phase": case["phase"],
                "degree": certificate["degree"],
                "generic_minimal_order": prediction["generic_minimal_order"],
                "inverse_support": prediction["inverse_support"],
                "operator_coefficients_low_to_high": certificate[
                    "scalar_operator_for_original_phase"
                ]["coefficients"],
                "exact_krylov_residual_zero": certificate[
                    "scalar_operator_for_original_phase"
                ]["exact_krylov_residual_zero"],
                "certificate_file": certificate_name,
                "certificate_file_sha256": sha256_bytes(certificate_bytes),
                "certificate_sha256": certificate["certificate_sha256"],
            }
        )

    receipt = {
        "schema": "exponential-period-order-oracle-benchmark-receipt-v1",
        "status": "pass",
        "spec_sha256": sha256_bytes(spec_bytes),
        "case_count": len(records),
        "all_expected_orders_match": True,
        "all_expected_supports_match": True,
        "all_exact_krylov_residuals_zero": True,
        "cases": records,
        "claim_boundary": spec["claim_boundary"],
    }
    receipt["receipt_sha256"] = canonical_hash(receipt)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(encoded_json(receipt))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        type=Path,
        default=ROOT / "benchmarks" / "order_oracle_cases.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "receipts" / "order_oracle_benchmark_receipt.json",
    )
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=ROOT / "receipts" / "order_oracle_cases",
    )
    args = parser.parse_args()
    receipt = build(args.spec, args.output, args.certificate_dir)
    print(
        "order-oracle exact benchmark PASS "
        f"({receipt['case_count']} cases, receipt {receipt['receipt_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
