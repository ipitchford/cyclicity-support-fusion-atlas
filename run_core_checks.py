#!/usr/bin/env python3
"""One-command, fail-closed release replay for the retained claims.

The default route verifies package bytes, replays structural and atlas checks
under ordinary and optimized Python, reruns all 1,152 degree-5-to-20 support
cases, compares regenerated receipts with frozen expected bytes, and executes
semantic corruption controls. Use ``--quick`` only during development.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
VERIFICATION = ROOT / "verification"
sys.path.insert(0, str(VERIFICATION))

from integrity import sha256_path, verify_expected_digest, verify_manifest  # noqa: E402


def run(label: str, argv: list[str], cwd: Path) -> None:
    print(f"[RUN] {label}", flush=True)
    completed = subprocess.run(argv, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"[FAIL] {label}: exit {completed.returncode}")
    print(f"[PASS] {label}", flush=True)


def replay_suite(python_argv: list[str], suffix: str, tmp: Path, full: bool) -> tuple[Path, Path]:
    prefix = python_argv
    exact_receipt = tmp / f"exact_rank_{suffix}.json"
    atlas_receipt = tmp / f"atlas_cases_{suffix}.json"

    commands = [
        ("structural support/fusion tests", prefix + ["tests/test_fusion_support.py"], ROOT),
        ("formal fraction audit", prefix + ["cleanroom/fraction_audit.py"], ROOT),
        ("Fourier-Gamma period spot check", prefix + ["cleanroom/period_matrix_spotcheck.py"], ROOT),
        ("atlas exact-rank controls", prefix + ["verify_atlas.py", "--output", str(exact_receipt)], ROOT / "code"),
        ("support/rank cross-implementation", prefix + ["battery1.py"], VERIFICATION),
        ("deep support controls", prefix + ["battery2.py"], VERIFICATION),
        ("Fourier fusion and heredity", prefix + ["battery3.py"], VERIFICATION),
        ("quartic-lift elimination", prefix + ["battery4b.py"], VERIFICATION),
        ("sparse family-blind search", prefix + ["battery4c.py"], VERIFICATION),
        ("rank-preserving extension loci", prefix + ["battery4d.py"], VERIFICATION),
        ("semantic negative controls", prefix + ["negative_controls.py"], VERIFICATION),
    ]
    for label, argv, cwd in commands:
        run(f"{label} [{suffix}]", argv, cwd)

    if full:
        run(
            f"complete degree-5-to-20 atlas sweep [{suffix}]",
            prefix + ["battery4a_fast.py", "5", "20", "--json", str(atlas_receipt)],
            VERIFICATION,
        )
    return exact_receipt, atlas_receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="omit the 1,152-case atlas sweep")
    parser.add_argument(
        "--development",
        action="store_true",
        help="skip frozen manifest and receipt comparisons while editing",
    )
    args = parser.parse_args()

    python = sys.executable
    print(f"python={python}")
    print(f"version={sys.version.split()[0]}")

    expectations_path = ROOT / "RELEASE_EXPECTATIONS.json"
    expectations = None
    if not args.development:
        verify_manifest(ROOT, ROOT / "MANIFEST.sha256", require_complete=True)
        expectations = json.loads(expectations_path.read_text())
        print("[PASS] complete package manifest")

    with tempfile.TemporaryDirectory(prefix="cyclicity-replay-") as tmp_name:
        tmp = Path(tmp_name)
        normal_exact, normal_atlas = replay_suite([python], "normal", tmp, not args.quick)
        optimized_exact, optimized_atlas = replay_suite(
            [python, "-O"], "optimized", tmp, not args.quick
        )

        if sha256_path(normal_exact) != sha256_path(optimized_exact):
            raise SystemExit("[FAIL] exact-rank receipts differ between normal and optimized runs")
        print("[PASS] exact-rank normal/optimized receipt parity")

        if not args.quick:
            if sha256_path(normal_atlas) != sha256_path(optimized_atlas):
                raise SystemExit("[FAIL] atlas receipts differ between normal and optimized runs")
            print("[PASS] full-atlas normal/optimized receipt parity")

        if expectations is not None:
            verify_expected_digest(normal_exact, expectations["exact_rank_receipt_sha256"])
            verify_expected_digest(
                ROOT / "receipts" / "exact_rank_receipt.json",
                expectations["exact_rank_receipt_sha256"],
            )
            print("[PASS] frozen exact-rank receipt")
            if not args.quick:
                verify_expected_digest(normal_atlas, expectations["atlas_case_records_sha256"])
                verify_expected_digest(
                    ROOT / "receipts" / "atlas_case_records_d5_20.json",
                    expectations["atlas_case_records_sha256"],
                )
                print("[PASS] frozen per-case atlas receipt")

    print("RELEASE GATE PASS" if not args.quick else "QUICK CORE CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
