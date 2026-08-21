#!/usr/bin/env python3
"""Run the independent Singular CAS and Lean kernel verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "formal" / "independent_verification_protocol.json"
LOCK = ROOT / "formal" / "independent_verification_lock.json"
SINGULAR_SOURCE = ROOT / "cleanroom" / "singular_newton_crosscheck.sing"
LEAN_SOURCE = ROOT / "formal" / "lean" / "CyclicityNewton.lean"
DEFAULT_OUTPUT = ROOT / "receipts" / "independent_formalization_receipt.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(payload.encode())


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
        raise RuntimeError("independent-formalization lock digest mismatch")
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


def parse_singular(output: str, protocol: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    if "? error occurred" in output or "FAIL|" in output:
        raise RuntimeError(f"Singular reported an internal error:\n{output}")
    if output.count("SINGULAR_NEWTON_PASS") != 1:
        raise RuntimeError("Singular pass sentinel missing or repeated")

    records: list[dict[str, Any]] = []
    identities: dict[str, str] = {}
    for line in output.splitlines():
        if line.startswith("CASE|"):
            _, kind, raw_m, raw_empty, raw_count, basis = line.split("|", 5)
            records.append(
                {
                    "type": kind,
                    "m": int(raw_m),
                    "empty_after_nondegenerate_saturation": bool(int(raw_empty)),
                    "condition_count": int(raw_count),
                    "reduced_standard_basis": basis,
                }
            )
        elif line.startswith("IDENTITY|"):
            _, kind, expression = line.split("|", 2)
            identities[kind] = expression

    expected = protocol["exact_claims"]["singular_bounded_elimination"]
    expected_pairs = {(kind, m) for kind in ("cubic", "quartic") for m in range(2, 33)}
    actual_pairs = {(record["type"], record["m"]) for record in records}
    if len(records) != 62 or actual_pairs != expected_pairs:
        raise RuntimeError("Singular case coverage mismatch")
    for record in records:
        survivor = 2 if record["type"] == "cubic" else 3
        expected_empty = record["m"] != survivor
        if record["empty_after_nondegenerate_saturation"] != expected_empty:
            raise RuntimeError(f"unexpected Singular locus: {record}")
    quartic_three = next(r for r in records if r["type"] == "quartic" and r["m"] == 3)
    if quartic_three["reduced_standard_basis"] != "cw-1,a":
        raise RuntimeError("quartic m=3 basis does not certify a=0 and c!=0")
    expected_identities = {
        "cubic": expected["cubic_positive_resultant"],
        "quartic": expected["quartic_positive_resultant"],
    }
    if identities != expected_identities:
        raise RuntimeError(f"Singular positive identities mismatch: {identities}")
    return records, identities


def lean_theorem_names(source: str) -> list[str]:
    return re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mathlib-project", type=Path)
    parser.add_argument("--singular", default=shutil.which("Singular") or "Singular")
    args = parser.parse_args()

    lock = verify_lock()
    protocol = json.loads(PROTOCOL.read_text())
    mathlib_project = find_mathlib_project(args.mathlib_project)

    singular_run = run([args.singular, "-q", str(SINGULAR_SOURCE)])
    records, identities = parse_singular(singular_run.stdout, protocol)

    lean_names = lean_theorem_names(LEAN_SOURCE.read_text())
    expected_lean = protocol["exact_claims"]["lean_kernel"]
    required_names = (
        expected_lean["root_map_identities"]
        + expected_lean["coefficient_obstructions"]
        + expected_lean["displayed_elementary_identities"]
    )
    if lean_names != required_names:
        raise RuntimeError(f"Lean theorem inventory mismatch: {lean_names}")
    lean_run = run(["lake", "env", "lean", str(LEAN_SOURCE)], cwd=mathlib_project)
    if lean_run.stdout.strip():
        raise RuntimeError(f"Lean emitted unexpected output:\n{lean_run.stdout}")

    singular_version = run([args.singular, "--version"]).stdout.splitlines()[0]
    lean_version = run(["lean", "--version"]).stdout.splitlines()[0]
    lake_version = run(["lake", "--version"]).stdout.splitlines()[0]
    mathlib_path = mathlib_project / ".lake" / "packages" / "mathlib"
    mathlib_commit = run(["git", "rev-parse", "HEAD"], cwd=mathlib_path).stdout.strip()

    result = {
        "schema": "cyclicity-independent-formalization-receipt-v1",
        "status": "pass",
        "protocol_sha256": sha256(PROTOCOL),
        "lock_sha256": lock["lock_sha256"],
        "engines": {
            "singular": {
                "version": singular_version,
                "source_sha256": sha256(SINGULAR_SOURCE),
                "raw_output_sha256": sha256_bytes(singular_run.stdout.encode()),
                "case_count": len(records),
                "records": records,
                "positive_resultants": identities,
            },
            "lean": {
                "version": lean_version,
                "lake_version": lake_version,
                "mathlib_commit": mathlib_commit,
                "source_sha256": sha256(LEAN_SOURCE),
                "kernel_status": "pass",
                "theorem_count": len(lean_names),
                "theorems": lean_names,
            },
        },
        "separation": {
            "algebra_engine": "Singular, not SymPy",
            "formal_kernel": "Lean 4 with Mathlib",
            "orchestrator": "Python standard library only",
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
                "singular_cases": len(records),
                "lean_theorems": len(lean_names),
                "receipt_sha256": result["receipt_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
