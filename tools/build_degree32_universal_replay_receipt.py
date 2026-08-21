#!/usr/bin/env python3
"""Record byte parity between ordinary and optimized universal sweeps."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", type=Path, default=ROOT / "receipts" / "degree32_universal_low_rank_atlas.json")
    parser.add_argument("--optimized", type=Path, required=True)
    parser.add_argument("--primary-seconds", type=float, required=True)
    parser.add_argument("--optimized-seconds", type=float, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "receipts" / "degree32_universal_replay.json")
    args = parser.parse_args()
    primary_bytes = args.primary.read_bytes()
    optimized_bytes = args.optimized.read_bytes()
    if primary_bytes != optimized_bytes:
        raise SystemExit("ordinary and optimized universal receipts differ")
    primary = json.loads(primary_bytes)
    result = {
        "schema": "degree32-universal-replay-receipt-v1",
        "status": "pass",
        "ordinary": {
            "mode": "python3",
            "terminal_reported_seconds": args.primary_seconds,
            "file_sha256": sha256_path(args.primary),
        },
        "optimized": {
            "mode": "python3 -O",
            "terminal_reported_seconds": args.optimized_seconds,
            "file_sha256": sha256_path(args.optimized),
        },
        "byte_identical": True,
        "mathematical_receipt_sha256": primary["receipt_sha256"],
        "case_count": len(primary["records"]),
        "claim_boundary": "Within-programme deterministic parity; not external independent reproduction.",
    }
    result["replay_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
