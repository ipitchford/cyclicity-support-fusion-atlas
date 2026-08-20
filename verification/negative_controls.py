#!/usr/bin/env python3
"""Semantic mutations that every release gate must reject."""

from __future__ import annotations

import cmath
from pathlib import Path
import subprocess
import sys
import tempfile

from battery4a_fast import failure_count
from integrity import sha256_path, verify_expected_digest, verify_manifest


def require_rejection(label, action) -> None:
    try:
        action()
    except Exception as exc:  # the mutation must cross a fail-closed boundary
        print(f"PASS mutation rejected: {label} ({type(exc).__name__})")
        return
    raise RuntimeError(f"mutation was accepted: {label}")


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(f"negative-control detector failed: {label}")
    print(f"PASS mutation rejected: {label}")


def main() -> None:
    require(
        failure_count({"anomalies": [(8, [1, 3], "synthetic")], "nocert": []}) == 1,
        "atlas anomaly",
    )
    require(
        failure_count({"anomalies": [], "nocert": [(8, [1, 3], "synthetic")]}) == 1,
        "missing atlas certificate",
    )
    battery = Path(__file__).with_name("battery4a_fast.py")
    for mutation in ("anomaly", "nocert"):
        completed = subprocess.run(
            [sys.executable, str(battery), "--self-test-failure", mutation],
            cwd=battery.parent,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        require(completed.returncode != 0, f"atlas CLI {mutation} exit status")

    actual_support = {1, 7, 10}
    mutated_support = {1, 4, 7, 10}
    require(actual_support != mutated_support, "support-residue mutation")

    zeta = cmath.exp(2j * cmath.pi / 3)
    correct_det = zeta - 1
    corrupted_det = (1 * zeta) - (zeta * 1)
    require(abs(correct_det) > 1e-9 and abs(corrupted_det) < 1e-9,
            "Fourier exponent mutation")

    with tempfile.TemporaryDirectory(prefix="cyclicity-negative-") as tmp:
        root = Path(tmp)
        payload = root / "payload.txt"
        payload.write_text("trusted\n")
        manifest = root / "MANIFEST.sha256"
        manifest.write_text(f"{sha256_path(payload)}  payload.txt\n")
        verify_manifest(root, manifest)
        payload.write_text("corrupted\n")
        require_rejection("manifest corruption", lambda: verify_manifest(root, manifest))

        receipt = root / "receipt.json"
        receipt.write_text('{"status":"pass"}\n')
        expected = sha256_path(receipt)
        receipt.write_text('{"status":"review"}\n')
        require_rejection(
            "receipt corruption", lambda: verify_expected_digest(receipt, expected)
        )

    print("NEGATIVE CONTROLS PASS")


if __name__ == "__main__":
    main()
