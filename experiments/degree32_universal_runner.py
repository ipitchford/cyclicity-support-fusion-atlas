#!/usr/bin/env python3
"""Run the sealed exhaustive degree-32 low-rank coefficient-atlas sweep."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERIFICATION = ROOT / "verification"
sys.path.insert(0, str(VERIFICATION))

from battery4a_fast import failure_count, run, software_identity  # noqa: E402


DEPENDENCIES = [
    ROOT / "verification" / "battery4a_fast.py",
    ROOT / "verification" / "symconstr.py",
    ROOT / "verification" / "lib.py",
]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_seal(preregistration_path: Path, lock_path: Path) -> dict[str, Any]:
    require(lock_path.is_file(), "universal degree-32 lock is missing; refusing to compute")
    lock = json.loads(lock_path.read_text())
    require(lock.get("schema") == "degree32-universal-lock-v1", "unknown universal degree-32 lock schema")
    observed = {
        "preregistration_sha256": sha256_path(preregistration_path),
        "runner_sha256": sha256_path(Path(__file__).resolve()),
        "dependency_sha256": {
            str(path.relative_to(ROOT)): sha256_path(path) for path in DEPENDENCIES
        },
    }
    for key, value in observed.items():
        require(lock.get(key) == value, f"sealed {key} mismatch")
    require(lock.get("execution_state_at_seal") == "not_run", "universal sweep was not prospectively sealed")
    return lock


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preregistration",
        type=Path,
        default=ROOT / "experiments" / "degree32_universal_preregistration.json",
    )
    parser.add_argument(
        "--lock",
        type=Path,
        default=ROOT / "experiments" / "degree32_universal_lock.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "receipts" / "degree32_universal_low_rank_atlas.json",
    )
    args = parser.parse_args()
    lock = verify_seal(args.preregistration, args.lock)
    preregistration = json.loads(args.preregistration.read_text())
    coverage = preregistration["coverage"]
    require(coverage["degree"] == 32, "sealed target degree drift")
    require(coverage["expected_case_count"] == 466, "sealed case count drift")

    results = run(32, 32)
    summary = {
        "cases": len(results["records"]),
        "vacuous_full_family": results["vacuous_ok"],
        "exact_power_only": results["exact_poweronly"],
        "exact_union": results["exact_union"],
        "anomalies": len(results["anomalies"]),
        "no_certificate": len(results["nocert"]),
    }
    expected = coverage["expected_outcome_counts"]
    if failure_count(results):
        adjudication = "falsified" if results["anomalies"] else "partial"
    elif summary == {"cases": coverage["expected_case_count"], **expected}:
        adjudication = "confirmed"
    else:
        adjudication = "partial"

    receipt = {
        "schema": "degree32-universal-low-rank-atlas-receipt-v1",
        "status": "complete",
        "adjudication": adjudication,
        "range": [32, 32],
        "software": software_identity(),
        "seal": lock,
        "theorem_target": preregistration["theorem_target"],
        "coverage": coverage,
        "summary": summary,
        "records": results["records"],
        "claim_boundary": preregistration["claim_boundary"],
    }
    unhashed = dict(receipt)
    receipt["receipt_sha256"] = canonical_hash(unhashed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "adjudication": adjudication,
        "summary": summary,
        "receipt_sha256": receipt["receipt_sha256"],
        "output": str(args.output),
    }, indent=2, sort_keys=True))
    return 0 if adjudication == "confirmed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
