#!/usr/bin/env python3
"""Fail-closed gate for the unpublished Exponential-Period Order Oracle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
VERIFICATION = ROOT / "verification"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(VERIFICATION))
sys.path.insert(0, str(TOOLS))

from build_order_oracle_manifest import ORACLE_PATHS  # noqa: E402
from integrity import parse_manifest, sha256_path, verify_manifest  # noqa: E402


def run(label: str, argv: list[str], cwd: Path = ROOT) -> None:
    print(f"[RUN] {label}", flush=True)
    completed = subprocess.run(argv, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"[FAIL] {label}: exit {completed.returncode}")
    print(f"[PASS] {label}", flush=True)


def require_equal(left: Path, right: Path, label: str) -> None:
    if sha256_path(left) != sha256_path(right):
        raise SystemExit(f"[FAIL] {label}: byte mismatch")
    print(f"[PASS] {label}", flush=True)


def verify_oracle_manifest() -> None:
    manifest = ROOT / "ORDER_ORACLE_MANIFEST.sha256"
    entries = parse_manifest(manifest)
    if set(entries) != ORACLE_PATHS:
        missing = sorted(ORACLE_PATHS - set(entries))
        stale = sorted(set(entries) - ORACLE_PATHS)
        raise SystemExit(f"[FAIL] oracle manifest coverage: missing={missing}, stale={stale}")
    for relative, expected in entries.items():
        path = ROOT / relative
        if not path.is_file() or sha256_path(path) != expected:
            raise SystemExit(f"[FAIL] oracle manifest digest: {relative}")
    print("[PASS] bounded order-oracle manifest", flush=True)


def compare_certificate_directories(left: Path, right: Path, frozen: Path) -> None:
    expected_names = sorted(path.name for path in frozen.glob("*.json"))
    for directory, label in ((left, "normal"), (right, "optimized")):
        names = sorted(path.name for path in directory.glob("*.json"))
        if names != expected_names:
            raise SystemExit(f"[FAIL] {label} certificate inventory mismatch")
    for name in expected_names:
        require_equal(left / name, right / name, f"certificate parity: {name}")
        require_equal(left / name, frozen / name, f"frozen certificate: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--development",
        action="store_true",
        help="skip frozen manifests and receipt-byte comparisons",
    )
    parser.add_argument(
        "--skip-numerical",
        action="store_true",
        help="skip the non-theorem quadrature spot controls",
    )
    args = parser.parse_args()

    python = sys.executable
    print(f"python={python}")
    print(f"version={sys.version.split()[0]}")

    if not args.development:
        # Confirm every byte named by the immutable parent manifest remains
        # unchanged, while allowing the additive successor files.
        verify_manifest(ROOT, ROOT / "MANIFEST.sha256", require_complete=False)
        print("[PASS] published-parent listed bytes unchanged", flush=True)
        verify_oracle_manifest()

    with tempfile.TemporaryDirectory(prefix="order-oracle-gate-") as tmp_name:
        tmp = Path(tmp_name)
        normal_receipt = tmp / "normal_receipt.json"
        optimized_receipt = tmp / "optimized_receipt.json"
        normal_cases = tmp / "normal_cases"
        optimized_cases = tmp / "optimized_cases"
        normal_generic = tmp / "normal_generic.json"
        optimized_generic = tmp / "optimized_generic.json"

        run("oracle regression and mutation tests [normal]", [python, "tests/test_order_oracle.py"])
        run("oracle regression and mutation tests [optimized]", [python, "-O", "tests/test_order_oracle.py"])
        run("separate symbolic operator cross-check [normal]", [python, "cleanroom/order_oracle_crosscheck.py"])
        run("separate symbolic operator cross-check [optimized]", [python, "-O", "cleanroom/order_oracle_crosscheck.py"])
        run(
            "exact benchmark regeneration [normal]",
            [
                python,
                "tools/build_order_oracle_receipt.py",
                "--output",
                str(normal_receipt),
                "--certificate-dir",
                str(normal_cases),
            ],
        )
        run(
            "exact benchmark regeneration [optimized]",
            [
                python,
                "-O",
                "tools/build_order_oracle_receipt.py",
                "--output",
                str(optimized_receipt),
                "--certificate-dir",
                str(optimized_cases),
            ],
        )
        run(
            "generic degree-12 exact-rank control [normal]",
            [python, "tools/generic_degree12_rank_control.py", "--output", str(normal_generic)],
        )
        run(
            "generic degree-12 exact-rank control [optimized]",
            [python, "-O", "tools/generic_degree12_rank_control.py", "--output", str(optimized_generic)],
        )

        require_equal(normal_receipt, optimized_receipt, "normal/optimized receipt parity")
        require_equal(normal_generic, optimized_generic, "normal/optimized generic-control parity")
        if not args.development:
            require_equal(
                normal_receipt,
                ROOT / "receipts" / "order_oracle_benchmark_receipt.json",
                "frozen benchmark receipt",
            )
            require_equal(
                normal_generic,
                ROOT / "receipts" / "order_oracle_generic_degree12_control.json",
                "frozen generic-control receipt",
            )
            compare_certificate_directories(
                normal_cases,
                optimized_cases,
                ROOT / "receipts" / "order_oracle_cases",
            )

        if not args.skip_numerical:
            live_numerical = tmp / "numerical.json"
            run(
                "rapid-decay real-line numerical spot controls",
                [python, "tools/validate_order_oracle_periods.py", "--output", str(live_numerical)],
            )
            live = json.loads(live_numerical.read_text())
            if live.get("status") != "pass" or live.get("record_count") != 7:
                raise SystemExit("[FAIL] numerical spot-control summary")
            print("[PASS] seven numerical period/operator residual controls", flush=True)

    print("ORDER ORACLE GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
