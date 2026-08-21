#!/usr/bin/env python3
"""Fail-closed replay for the amplitude and Laurent successor."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(label: str, argv: list[str]) -> None:
    print(f"[RUN] {label}", flush=True)
    completed = subprocess.run(argv, cwd=ROOT, check=False)
    if completed.returncode:
        raise SystemExit(f"[FAIL] {label}: exit {completed.returncode}")
    print(f"[PASS] {label}", flush=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="amplitude-laurent-") as tmp_name:
        tmp = Path(tmp_name)
        normal = tmp / "normal.json"
        optimized = tmp / "optimized.json"
        run("ordinary exact replay", [sys.executable, "tests/test_amplitude_laurent.py", "--receipt", str(normal)])
        run("optimized exact replay", [sys.executable, "-O", "tests/test_amplitude_laurent.py", "--receipt", str(optimized)])
        if normal.read_bytes() != optimized.read_bytes():
            raise SystemExit("[FAIL] ordinary and optimized receipts differ")
        print(f"[PASS] byte-identical receipts sha256={sha256(normal)}")

        frozen = ROOT / "receipts" / "amplitude_laurent_test_receipt.json"
        if frozen.exists() and frozen.read_bytes() != normal.read_bytes():
            raise SystemExit("[FAIL] regenerated receipt differs from frozen receipt")
        if frozen.exists():
            print("[PASS] frozen receipt parity")

    print("AMPLITUDE-LAURENT GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
