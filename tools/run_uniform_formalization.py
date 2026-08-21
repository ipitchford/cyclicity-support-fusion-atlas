#!/usr/bin/env python3
"""Run the Lean kernel check for the uniform structural successor."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "formal" / "uniform_verification_protocol.json"
LOCK = ROOT / "formal" / "uniform_verification_lock.json"
LEAN_SOURCE = ROOT / "formal" / "lean" / "CyclicityUniform.lean"
PROOF_NOTE = ROOT / "ALL_DEGREE_STRUCTURAL_REPAIR.md"
DEFAULT_OUTPUT = ROOT / "receipts" / "uniform_structural_formalization_receipt.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(value: Any) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stdout}"
        )
    return completed


def verify_lock() -> dict[str, Any]:
    lock = json.loads(LOCK.read_text())
    claimed = lock.pop("lock_sha256")
    if canonical_hash(lock) != claimed:
        raise RuntimeError("uniform-formalization lock digest mismatch")
    lock["lock_sha256"] = claimed
    for relative, expected in lock["files"].items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"locked source hash mismatch: {relative}")
    return lock


def find_mathlib_project(explicit: Path | None) -> Path:
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit)
    configured = os.environ.get("CYCLICITY_MATHLIB_PROJECT")
    if configured:
        candidates.append(Path(configured))
    candidates.extend(
        [
            ROOT / "formal" / "lean",
            Path.home()
            / "affine_hyperplane_slices"
            / "degree_difference_foundations"
            / "BorderedJacobian",
        ]
    )
    for candidate in candidates:
        mathlib = candidate / ".lake" / "packages" / "mathlib"
        if (candidate / "lakefile.toml").exists() and mathlib.exists():
            return candidate.resolve()
    raise RuntimeError(
        "no populated Mathlib project found; run `lake update` in formal/lean "
        "or pass --mathlib-project"
    )


def theorem_names(source: str) -> list[str]:
    return re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mathlib-project", type=Path)
    args = parser.parse_args()

    lock = verify_lock()
    protocol = json.loads(PROTOCOL.read_text())
    source = LEAN_SOURCE.read_text()
    if re.search(r"\b(sorry|admit|axiom)\b", source):
        raise RuntimeError("Lean source contains a forbidden placeholder or axiom declaration")

    names = theorem_names(source)
    exact = protocol["exact_claims"]
    expected = (
        exact["scaling_theorems"]
        + exact["coefficient_theorems"]
        + exact["uniform_theorems"]
    )
    if names != expected:
        raise RuntimeError(f"Lean theorem inventory mismatch: {names}")

    mathlib_project = find_mathlib_project(args.mathlib_project)
    lean_run = run(["lake", "env", "lean", str(LEAN_SOURCE)], cwd=mathlib_project)
    if lean_run.stdout.strip():
        raise RuntimeError(f"Lean emitted unexpected output:\n{lean_run.stdout}")

    lean_version = run(["lean", "--version"]).stdout.splitlines()[0]
    lake_version = run(["lake", "--version"]).stdout.splitlines()[0]
    mathlib_path = mathlib_project / ".lake" / "packages" / "mathlib"
    mathlib_commit = run(["git", "rev-parse", "HEAD"], cwd=mathlib_path).stdout.strip()

    result = {
        "schema": "cyclicity-uniform-structural-receipt-v1",
        "status": "pass",
        "protocol_sha256": sha256(PROTOCOL),
        "lock_sha256": lock["lock_sha256"],
        "proof_note_sha256": sha256(PROOF_NOTE),
        "lean": {
            "version": lean_version,
            "lake_version": lake_version,
            "mathlib_commit": mathlib_commit,
            "source_sha256": sha256(LEAN_SOURCE),
            "kernel_status": "pass",
            "theorem_count": len(names),
            "theorems": names,
            "placeholder_scan": "pass",
            "uniform_upper_cutoff": None,
        },
        "formalized_boundary": {
            "scaling": "lifted root-of-unity phases through common rescaling",
            "coefficients": "exact selected negative-binomial finite sums over QQ",
            "uniformity": "constructive mod-3 and mod-4 witnesses for arbitrary natural m",
            "cubic_candidates_before_E2": [2, 4],
            "quartic_candidates_before_E2": [2, 3, 5, 6, 9],
        },
        "assurance": {
            "formal_kernel": True,
            "complete_atlas_formalization": False,
            "external_independence": False,
        },
        "claim_boundary": protocol["claim_boundary"],
    }
    result["receipt_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": "pass",
                "theorem_count": len(names),
                "uniform_upper_cutoff": None,
                "receipt_sha256": result["receipt_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
