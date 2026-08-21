#!/usr/bin/env python3
"""Composite gate for the independent Singular/Lean successor."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
VERIFICATION = ROOT / "verification"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(VERIFICATION))
sys.path.insert(0, str(TOOLS))

from build_application_programme_manifest import APPLICATION_PATHS  # noqa: E402
from build_degree32_universal_manifest import PATHS as DEGREE32_PATHS  # noqa: E402
from build_independent_formalization_manifest import PATHS as FORMAL_PATHS  # noqa: E402
from integrity import parse_manifest, sha256_path, verify_manifest  # noqa: E402


def run(label: str, argv: list[str]) -> None:
    print(f"[RUN] {label}", flush=True)
    completed = subprocess.run(argv, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"[FAIL] {label}: exit {completed.returncode}")
    print(f"[PASS] {label}", flush=True)


def require_equal(left: Path, right: Path, label: str) -> None:
    if sha256_path(left) != sha256_path(right):
        raise SystemExit(f"[FAIL] {label}: byte mismatch")
    print(f"[PASS] {label}", flush=True)


def verify_bounded_manifest(path: Path, expected_paths: set[str], label: str) -> None:
    entries = parse_manifest(path)
    if set(entries) != expected_paths:
        missing = sorted(expected_paths - set(entries))
        stale = sorted(set(entries) - expected_paths)
        raise SystemExit(f"[FAIL] {label} coverage: missing={missing}, stale={stale}")
    for relative, expected in entries.items():
        target = ROOT / relative
        if not target.is_file() or sha256_path(target) != expected:
            raise SystemExit(f"[FAIL] {label} digest: {relative}")
    print(f"[PASS] {label}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-predecessor-gate",
        action="store_true",
        help="skip the degree-32 composite gate while retaining all manifest checks",
    )
    parser.add_argument(
        "--skip-engine-recompute",
        action="store_true",
        help="validate the frozen receipt without rerunning Singular and Lean",
    )
    parser.add_argument(
        "--mathlib-project",
        type=Path,
        help="populated Mathlib Lake project for the live Lean replay",
    )
    args = parser.parse_args()
    python = sys.executable
    print(f"python={python}")
    print(f"version={sys.version.split()[0]}")

    verify_manifest(ROOT, ROOT / "MANIFEST.sha256", require_complete=False)
    print("[PASS] published-parent listed bytes unchanged", flush=True)
    verify_bounded_manifest(
        ROOT / "APPLICATIONS_MANIFEST.sha256", APPLICATION_PATHS, "bounded application manifest"
    )
    verify_bounded_manifest(
        ROOT / "DEGREE32_UNIVERSAL_MANIFEST.sha256", DEGREE32_PATHS, "bounded degree-32 manifest"
    )
    verify_bounded_manifest(
        ROOT / "INDEPENDENT_FORMALIZATION_MANIFEST.sha256",
        FORMAL_PATHS,
        "bounded independent-formalization manifest",
    )
    if not args.skip_predecessor_gate:
        run("predecessor degree-32 successor gate", [python, "run_degree32_universal_checks.py"])

    run("formalization semantic verifier [normal]", [python, "tools/verify_independent_formalization.py"])
    run(
        "formalization semantic verifier [optimized]",
        [python, "-O", "tools/verify_independent_formalization.py"],
    )
    run(
        "formalization mutation controls [normal]",
        [python, "-m", "unittest", "tests/test_independent_formalization.py", "-v"],
    )
    run(
        "formalization mutation controls [optimized]",
        [python, "-O", "-m", "unittest", "tests/test_independent_formalization.py", "-v"],
    )

    if not args.skip_engine_recompute:
        with tempfile.TemporaryDirectory(prefix="independent-formalization-gate-") as tmp_name:
            tmp = Path(tmp_name)
            normal = tmp / "normal.json"
            optimized = tmp / "optimized.json"
            base = ["tools/run_independent_formalization.py"]
            if args.mathlib_project is not None:
                base.extend(["--mathlib-project", str(args.mathlib_project)])
            run("live Singular/Lean replay [normal]", [python, *base, "--output", str(normal)])
            run(
                "live Singular/Lean replay [optimized]",
                [python, "-O", *base, "--output", str(optimized)],
            )
            require_equal(normal, optimized, "normal/optimized engine replay parity")
            require_equal(
                normal,
                ROOT / "receipts" / "independent_formalization_receipt.json",
                "frozen independent-formalization receipt",
            )

    print("INDEPENDENT SINGULAR/LEAN SUCCESSOR GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
