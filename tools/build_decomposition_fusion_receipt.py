#!/usr/bin/env python3
"""Build frozen decomposition-aware fusion reports for named exact chains."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decomposition_fusion import analyse_decompositions  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=ROOT / "benchmarks" / "decomposition_fusion_cases.json")
    parser.add_argument("--output", type=Path, default=ROOT / "receipts" / "decomposition_fusion_receipt.json")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "receipts" / "decomposition_fusion_cases")
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    args.report_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    for case in spec["cases"]:
        report = analyse_decompositions(case["phase"], case["chains"])
        path = args.report_dir / f"{case['id']}.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        summaries.append({
            "id": case["id"],
            "degree": report["degree"],
            "global_rank": report["global_rank"],
            "global_support": report["global_support"],
            "validated_chain_count": report["validated_chain_count"],
            "report_file": path.name,
            "report_sha256": report["report_sha256"],
            "status": "pass",
        })
        print(f"[PASS] {case['id']}: {report['validated_chain_count']} validated chains")
    receipt = {
        "schema": "decomposition-aware-fusion-benchmark-receipt-v1",
        "status": "pass",
        "case_count": len(summaries),
        "cases": summaries,
        "claim_boundary": spec["claim_boundary"],
    }
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("DECOMPOSITION-AWARE FUSION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
