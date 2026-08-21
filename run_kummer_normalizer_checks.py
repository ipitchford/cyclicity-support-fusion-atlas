#!/usr/bin/env python3
"""Composite gate for the standalone Kummer normalizer successor."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def run(label: str, command: list[str]) -> None:
    print(f"[RUN] {label}", flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"[FAIL] {label}: exit {completed.returncode}")
    print(f"[PASS] {label}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-engine-recompute", action="store_true")
    parser.add_argument("--mathlib-project", type=Path)
    args = parser.parse_args()
    python = sys.executable
    run("semantic verifier [normal]", [python, "tools/verify_kummer_normalizer.py"])
    run("semantic verifier [optimized]", [python, "-O", "tools/verify_kummer_normalizer.py"])
    run("mutation controls [normal]", [python, "-m", "unittest", "tests/test_kummer_normalizer.py", "-v"])
    run("mutation controls [optimized]", [python, "-O", "-m", "unittest", "tests/test_kummer_normalizer.py", "-v"])
    if not args.skip_engine_recompute:
        with tempfile.TemporaryDirectory(prefix="kummer-gate-") as directory:
            temporary = Path(directory)
            normal = temporary / "normal.json"
            optimized = temporary / "optimized.json"
            base = ["tools/run_kummer_normalizer.py"]
            if args.mathlib_project is not None:
                base.extend(["--mathlib-project", str(args.mathlib_project)])
            run("live Lean/CAS replay [normal]", [python, *base, "--output", str(normal)])
            run("live Lean/CAS replay [optimized]", [python, "-O", *base, "--output", str(optimized)])
            if normal.read_bytes() != optimized.read_bytes():
                raise SystemExit("[FAIL] normal/optimized replay parity")
            if normal.read_bytes() != (ROOT / "receipts/kummer_normalizer_receipt.json").read_bytes():
                raise SystemExit("[FAIL] frozen receipt parity")
            print("[PASS] live/frozen and normal/optimized receipt parity")
    print("KUMMER NORMALIZER SUCCESSOR GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
