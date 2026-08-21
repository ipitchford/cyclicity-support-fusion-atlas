#!/usr/bin/env python3
"""Freeze the bounded order-oracle extension manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ORDER_ORACLE_MANIFEST.sha256"

ORACLE_PATHS = {
    "MANUSCRIPT.md",
    "ORDER_ORACLE.md",
    "ORDER_ORACLE_ASSURANCE.md",
    "ORDER_ORACLE_CLAIMS.json",
    "ORDER_ORACLE_ENVIRONMENT.json",
    "ORDER_ORACLE_REVIEW.md",
    "benchmarks/order_oracle_cases.json",
    "cleanroom/order_oracle_crosscheck.py",
    "receipts/order_oracle_benchmark_receipt.json",
    "receipts/order_oracle_cases/aligned_square_degree_12.json",
    "receipts/order_oracle_cases/dickson_degree_5.json",
    "receipts/order_oracle_cases/exceptional_collision_degree_12.json",
    "receipts/order_oracle_cases/misaligned_square_degree_12.json",
    "receipts/order_oracle_cases/power_degree_7.json",
    "receipts/order_oracle_cases/quartic_rank_3.json",
    "receipts/order_oracle_cases/quartic_rank_drop.json",
    "receipts/order_oracle_cases/rank_creation_degree_6.json",
    "receipts/order_oracle_generic_degree12_control.json",
    "receipts/order_oracle_numerical_spotcheck.json",
    "requirements.txt",
    "run_order_oracle_checks.py",
    "src/fusion_support.py",
    "src/order_oracle.py",
    "tests/test_order_oracle.py",
    "tools/build_order_oracle_manifest.py",
    "tools/build_order_oracle_receipt.py",
    "tools/generic_degree12_rank_control.py",
    "tools/validate_order_oracle_periods.py",
    "verification/lib.py"
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def freeze() -> None:
    missing = sorted(relative for relative in ORACLE_PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"order-oracle manifest targets missing: {missing}")
    lines = [f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(ORACLE_PATHS)]
    MANIFEST.write_text("".join(lines), encoding="utf-8")
    print(f"order-oracle manifest frozen: {len(lines)} paths, sha256 {sha256(MANIFEST)}")


if __name__ == "__main__":
    freeze()
