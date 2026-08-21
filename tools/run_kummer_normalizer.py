#!/usr/bin/env python3
"""Replay Lean and clean-room CAS checks for the Kummer normalizer lemma."""

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
PROTOCOL = ROOT / "formal" / "kummer_normalizer_protocol.json"
LOCK = ROOT / "formal" / "kummer_normalizer_lock.json"
LEAN_SOURCE = ROOT / "formal" / "lean" / "CyclicityKummer.lean"
CAS_SOURCE = ROOT / "cleanroom" / "kummer_normalizer_audit.py"
DEFAULT_OUTPUT = ROOT / "receipts" / "kummer_normalizer_receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def run(command: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        command, cwd=cwd, check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{completed.stdout}")
    return completed.stdout


def find_mathlib_project(explicit: Path | None) -> Path:
    candidates = []
    if explicit is not None:
        candidates.append(explicit)
    configured = os.environ.get("CYCLICITY_MATHLIB_PROJECT")
    if configured:
        candidates.append(Path(configured))
    candidates.extend([
        ROOT / "formal" / "lean",
        Path.home() / "affine_hyperplane_slices" / "degree_difference_foundations" / "BorderedJacobian",
    ])
    for candidate in candidates:
        if (candidate / "lakefile.toml").exists() and (candidate / ".lake/packages/mathlib").exists():
            return candidate.resolve()
    raise RuntimeError("no populated Mathlib project found")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mathlib-project", type=Path)
    args = parser.parse_args()
    protocol = json.loads(PROTOCOL.read_text())
    lock = json.loads(LOCK.read_text())
    claimed_lock_hash = lock.pop("lock_sha256")
    if canonical_hash(lock) != claimed_lock_hash:
        raise RuntimeError("lock semantic hash mismatch")
    lock["lock_sha256"] = claimed_lock_hash
    for relative, expected in lock["files"].items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"locked source mismatch: {relative}")

    source = LEAN_SOURCE.read_text()
    if re.search(r"\b(sorry|admit|axiom)\b", source):
        raise RuntimeError("Lean source contains a placeholder or axiom declaration")
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != protocol["exact_claims"]["lean_theorems"]:
        raise RuntimeError(f"Lean theorem inventory mismatch: {names}")
    mathlib_project = find_mathlib_project(args.mathlib_project)
    lean_output = run(["lake", "env", "lean", str(LEAN_SOURCE)], mathlib_project)
    if lean_output.strip():
        raise RuntimeError(f"Lean emitted unexpected output:\n{lean_output}")

    with tempfile.TemporaryDirectory(prefix="kummer-normalizer-") as directory:
        cas_path = Path(directory) / "cas.json"
        run([sys.executable, str(CAS_SOURCE), "--output", str(cas_path)], ROOT)
        cas = json.loads(cas_path.read_text())
    cas_hash = cas.pop("receipt_sha256")
    if canonical_hash(cas) != cas_hash:
        raise RuntimeError("CAS semantic hash mismatch")
    cas["receipt_sha256"] = cas_hash
    if cas.get("schema") != "cyclicity-kummer-normalizer-cas-receipt-v2":
        raise RuntimeError("CAS schema mismatch")
    if sorted(cas["exact_checks"]) != sorted(protocol["exact_claims"]["cas_checks"]):
        raise RuntimeError("CAS check inventory mismatch")

    mathlib_path = mathlib_project / ".lake/packages/mathlib"
    result: dict[str, Any] = {
        "schema": "cyclicity-kummer-normalizer-receipt-v2",
        "status": "pass",
        "protocol_sha256": sha256(PROTOCOL),
        "lock_sha256": claimed_lock_hash,
        "proof_note_sha256": sha256(ROOT / "KUMMER_NORMALIZER_COMPLETION.md"),
        "lean": {
            "version": run(["lean", "--version"]).splitlines()[0],
            "mathlib_commit": run(["git", "rev-parse", "HEAD"], mathlib_path).strip(),
            "source_sha256": sha256(LEAN_SOURCE),
            "theorems": names,
            "theorem_count": len(names),
            "kernel_status": "pass",
            "placeholder_scan": "pass",
        },
        "cas": {
            "engine": cas["engine"],
            "semantic_sha256": cas_hash,
            "exact_checks": cas["exact_checks"],
        },
        "assurance": {
            "written_stratified_all_m_transport": True,
            "exceptional_even_relation_encoded": True,
            "uniform_full_kummer_kernel_claim": False,
            "formal_local_algebra": True,
            "separate_cas_implementation": True,
            "complete_all_degree_formalization": False,
            "external_independence": False,
            "peer_reviewed": False,
            "published": False,
        },
        "claim_boundary": protocol["claim_boundary"],
    }
    result["receipt_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "pass", "receipt_sha256": result["receipt_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
