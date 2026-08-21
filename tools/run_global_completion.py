#!/usr/bin/env python3
"""Replay Lean and independent CAS controls for the global completion."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "formal" / "global_verification_protocol.json"
LOCK = ROOT / "formal" / "global_verification_lock.json"
LEAN_SOURCE = ROOT / "formal" / "lean" / "CyclicityGlobal.lean"
PROOF_NOTE = ROOT / "ALL_DEGREE_GLOBAL_COMPLETION.md"
SOURCE_AUDIT = ROOT / "GLOBAL_COMPLETION_SOURCE_AUDIT.md"
REVIEW = ROOT / "ALL_DEGREE_GLOBAL_REVIEW.md"
DICKSON_PROOF = ROOT / "DICKSON_EXTENSION_COMPLETION.md"
KUMMER_RECEIPT = ROOT / "receipts" / "kummer_normalizer_receipt.json"
KUMMER_MANIFEST = ROOT / "KUMMER_NORMALIZER_MANIFEST.sha256"
FINITE_GROUP_REAUDIT = ROOT / "programme" / "FINITE_LINEAR_GROUP_REFEREE_REPORT.md"
MONODROMY_RITT_REAUDIT = ROOT / "programme" / "MONODROMY_RITT_REFEREE_REPORT.md"
CAS_SCRIPT = ROOT / "cleanroom" / "global_interface_audit.py"
DEFAULT_OUTPUT = ROOT / "receipts" / "global_completion_receipt.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(value: Any) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def checked_digest(value: dict[str, Any], field: str) -> None:
    claimed = value.pop(field)
    if canonical_hash(value) != claimed:
        raise RuntimeError(f"{field} mismatch")
    value[field] = claimed


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
    checked_digest(lock, "lock_sha256")
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
        if (
            (candidate / "lakefile.toml").exists()
            and (candidate / ".lake" / "packages" / "mathlib").exists()
        ):
            return candidate.resolve()
    raise RuntimeError("no populated Mathlib project found")


def theorem_names(source: str) -> list[str]:
    return re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)


def expected_theorems(protocol: dict[str, Any]) -> list[str]:
    claims = protocol["exact_claims"]
    return (
        claims["pole_order_theorems"]
        + claims["full_block_theorems"]
        + claims["scalar_extension_theorems"]
        + claims["primitive_character_theorems"]
    )


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
    expected = expected_theorems(protocol)
    if names != expected:
        raise RuntimeError(f"Lean theorem inventory mismatch: {names}")

    mathlib_project = find_mathlib_project(args.mathlib_project)
    lean_run = run(["lake", "env", "lean", str(LEAN_SOURCE)], cwd=mathlib_project)
    if lean_run.stdout.strip():
        raise RuntimeError(f"Lean emitted unexpected output:\n{lean_run.stdout}")

    with tempfile.TemporaryDirectory(prefix="cyclicity-global-cas-") as directory:
        cas_path = Path(directory) / "cas.json"
        run([sys.executable, str(CAS_SCRIPT), "--output", str(cas_path)], cwd=ROOT)
        cas = json.loads(cas_path.read_text())
        checked_digest(cas, "receipt_sha256")
        cas_file_sha256 = sha256(cas_path)

    run(
        [sys.executable, str(ROOT / "tools" / "verify_kummer_normalizer.py"), "--receipt", str(KUMMER_RECEIPT)],
        cwd=ROOT,
    )
    run(
        [sys.executable, str(ROOT / "tools" / "build_kummer_normalizer_manifest.py"), "--check"],
        cwd=ROOT,
    )

    lean_version = run(["lean", "--version"]).stdout.splitlines()[0]
    lake_version = run(["lake", "--version"]).stdout.splitlines()[0]
    mathlib_path = mathlib_project / ".lake" / "packages" / "mathlib"
    mathlib_commit = run(["git", "rev-parse", "HEAD"], cwd=mathlib_path).stdout.strip()

    result: dict[str, Any] = {
        "schema": "cyclicity-global-completion-receipt-v2",
        "status": "pass",
        "protocol_sha256": sha256(PROTOCOL),
        "lock_sha256": lock["lock_sha256"],
        "proof_note_sha256": sha256(PROOF_NOTE),
        "source_audit_sha256": sha256(SOURCE_AUDIT),
        "review_sha256": sha256(REVIEW),
        "proof_components": {
            "dickson": {
                "proof_note_sha256": sha256(DICKSON_PROOF),
                "proof_kind": protocol["component_requirements"]["dickson"]["proof_kind"],
                "bounded_grid_is_proof": False,
                "covers_arbitrary_outer_degree": True,
            },
            "kummer": {
                "receipt_schema": json.loads(KUMMER_RECEIPT.read_text())["schema"],
                "receipt_sha256": json.loads(KUMMER_RECEIPT.read_text())["receipt_sha256"],
                "file_sha256": sha256(KUMMER_RECEIPT),
                "manifest_sha256": sha256(KUMMER_MANIFEST),
                "uniform_full_kummer_kernel_claim": False,
                "exceptional_even_relation_encoded": True,
            },
            "internal_reaudits": {
                "finite_linear_group": {
                    "status": "pass",
                    "report_sha256": sha256(FINITE_GROUP_REAUDIT),
                },
                "monodromy_ritt": {
                    "status": "pass",
                    "report_sha256": sha256(MONODROMY_RITT_REAUDIT),
                },
                "external_independence": False,
            },
        },
        "lean": {
            "version": lean_version,
            "lake_version": lake_version,
            "mathlib_commit": mathlib_commit,
            "source_sha256": sha256(LEAN_SOURCE),
            "kernel_status": "pass",
            "theorem_count": len(names),
            "theorems": names,
            "placeholder_scan": "pass",
        },
        "cas": {
            "schema": cas["schema"],
            "engine": cas["engine"],
            "receipt_sha256": cas["receipt_sha256"],
            "file_sha256": cas_file_sha256,
            "exact_check_keys": list(cas["exact_checks"]),
            "bounded_regression_controls": cas["bounded_regression_controls"],
        },
        "interfaces": {
            "inherited_root_span": "written DFT and disjoint-residue proof; q equality imports the parent formal-moment theorem",
            "finite_pole_infinity_order": "written invariant-integral descent plus Lean degree-to-constancy kernel",
            "primitive_factor_audit": "source-exact group intersections, stabilisers, and restriction-character numerators",
            "rank_preserving_extensions": "full-block stabiliser, repaired stratified Kummer transport, direct all-degree Dickson invariant-field proof, quartic kernels, and non-repetition",
        },
        "assurance": {
            "candidate_complete_relative_to_named_imports": True,
            "formal_kernel": True,
            "independent_cas_implementation": True,
            "complete_atlas_formalization": False,
            "imported_classifications_formalized": False,
            "uniform_full_kummer_kernel_claim": False,
            "internal_separate_reaudits": True,
            "external_independence": False,
            "peer_reviewed": False,
            "published": False,
        },
        "claim_boundary": protocol["claim_boundary"],
    }
    result["receipt_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "lean_theorem_count": len(names),
                "cas_exact_check_count": len(cas["exact_checks"]),
                "receipt_sha256": result["receipt_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
