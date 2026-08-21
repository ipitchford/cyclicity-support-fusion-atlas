#!/usr/bin/env python3
"""Fail-closed gate for EPOB-1 through the sealed degree-32 experiment."""

from __future__ import annotations

import argparse
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

from build_application_programme_manifest import APPLICATION_PATHS  # noqa: E402
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


def verify_bounded_manifest() -> None:
    manifest = ROOT / "APPLICATIONS_MANIFEST.sha256"
    entries = parse_manifest(manifest)
    if set(entries) != APPLICATION_PATHS:
        missing = sorted(APPLICATION_PATHS - set(entries))
        stale = sorted(set(entries) - APPLICATION_PATHS)
        raise SystemExit(f"[FAIL] application manifest coverage: missing={missing}, stale={stale}")
    for relative, expected in entries.items():
        path = ROOT / relative
        if not path.is_file() or sha256_path(path) != expected:
            raise SystemExit(f"[FAIL] application manifest digest: {relative}")
    print("[PASS] bounded application manifest", flush=True)


def validate_epob_receipt(path: Path) -> None:
    result = json.loads(path.read_text())
    answers = {case["id"]: case for case in json.loads((ROOT / "benchmarks" / "epob1_answer_key.json").read_text())["cases"]}
    if result.get("status") != "pass" or result.get("scores") != {
        "operator": "9/9", "order": "10/10", "support": "10/10"
    }:
        raise SystemExit("[FAIL] EPOB score summary")
    records = result.get("cases", [])
    if len(records) != len(answers):
        raise SystemExit("[FAIL] EPOB case coverage")
    for record in records:
        expected = answers.get(record.get("id"))
        if expected is None or record.get("order") != expected["order"] or record.get("support") != expected["support"]:
            raise SystemExit(f"[FAIL] EPOB functional result: {record.get('id')}")
        if record.get("status") != "pass":
            raise SystemExit(f"[FAIL] EPOB case status: {record.get('id')}")
    print(f"[PASS] EPOB functional receipt: {path.name}", flush=True)


def write_reference_submission(path: Path) -> None:
    answers = json.loads((ROOT / "benchmarks" / "epob1_answer_key.json").read_text())
    cases = []
    for answer in answers["cases"]:
        cases.append({
            key: value
            for key, value in answer.items()
            if key in {"id", "order", "support", "operator_coefficients_low_to_high"}
        })
    path.write_text(json.dumps({
        "schema": "epob1-submission-v1",
        "system": {"name": "reference", "version": answers["version"], "environment": "gate"},
        "cases": cases,
    }))


def compare_directories(left: Path, right: Path, frozen: Path) -> None:
    expected_names = sorted(path.name for path in frozen.glob("*.json"))
    for directory, label in ((left, "normal"), (right, "optimized")):
        names = sorted(path.name for path in directory.glob("*.json"))
        if names != expected_names:
            raise SystemExit(f"[FAIL] decomposition report inventory: {label}")
    for name in expected_names:
        require_equal(left / name, right / name, f"decomposition parity: {name}")
        require_equal(left / name, frozen / name, f"frozen decomposition report: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--development", action="store_true", help="skip frozen-manifest and frozen-byte checks")
    parser.add_argument("--skip-oracle-gate", action="store_true", help="skip nested order-oracle replay")
    args = parser.parse_args()
    python = sys.executable
    print(f"python={python}")
    print(f"version={sys.version.split()[0]}")

    if not args.development:
        verify_manifest(ROOT, ROOT / "MANIFEST.sha256", require_complete=False)
        print("[PASS] published-parent listed bytes unchanged", flush=True)
        verify_bounded_manifest()
    if not args.skip_oracle_gate:
        run("order-oracle dependency gate", [python, "run_order_oracle_checks.py", "--skip-numerical"])

    with tempfile.TemporaryDirectory(prefix="application-programme-gate-") as tmp_name:
        tmp = Path(tmp_name)
        run("application negative controls [normal]", [python, "tests/test_application_programme.py"])
        run("application negative controls [optimized]", [python, "-O", "tests/test_application_programme.py"])

        epob_normal = tmp / "epob-normal.json"
        epob_optimized = tmp / "epob-optimized.json"
        run("EPOB-1 reference [normal]", [python, "tools/run_epob1.py", "--repeats", "1", "--output", str(epob_normal)])
        run("EPOB-1 reference [optimized]", [python, "-O", "tools/run_epob1.py", "--repeats", "1", "--output", str(epob_optimized)])
        validate_epob_receipt(epob_normal)
        validate_epob_receipt(epob_optimized)
        validate_epob_receipt(ROOT / "receipts" / "epob1_reference_run.json")
        submission = tmp / "epob-reference-submission.json"
        write_reference_submission(submission)
        run("EPOB-1 public submission verifier", [python, "tools/verify_epob1_submission.py", str(submission)])

        fusion_normal = tmp / "fusion-normal.json"
        fusion_optimized = tmp / "fusion-optimized.json"
        fusion_normal_dir = tmp / "fusion-normal-cases"
        fusion_optimized_dir = tmp / "fusion-optimized-cases"
        run("decomposition-aware fusion [normal]", [python, "tools/build_decomposition_fusion_receipt.py", "--output", str(fusion_normal), "--report-dir", str(fusion_normal_dir)])
        run("decomposition-aware fusion [optimized]", [python, "-O", "tools/build_decomposition_fusion_receipt.py", "--output", str(fusion_optimized), "--report-dir", str(fusion_optimized_dir)])
        require_equal(fusion_normal, fusion_optimized, "decomposition receipt parity")
        compare_directories(fusion_normal_dir, fusion_optimized_dir, ROOT / "receipts" / "decomposition_fusion_cases")
        if not args.development:
            require_equal(fusion_normal, ROOT / "receipts" / "decomposition_fusion_receipt.json", "frozen decomposition receipt")

        replay_normal = tmp / "fraction-normal.json"
        replay_optimized = tmp / "fraction-optimized.json"
        run("Fraction-only replay [normal]", [python, "challenge/reference_fraction_replay.py", "--output", str(replay_normal)])
        run("Fraction-only replay [optimized]", [python, "-O", "challenge/reference_fraction_replay.py", "--output", str(replay_optimized)])
        require_equal(replay_normal, replay_optimized, "Fraction replay parity")
        if not args.development:
            require_equal(replay_normal, ROOT / "receipts" / "fraction_replay_challenge_receipt.json", "frozen Fraction replay")

        run("sealed degree-32 receipt [normal; no recomputation]", [python, "tools/verify_degree32_receipt.py"])
        run("sealed degree-32 receipt [optimized; no recomputation]", [python, "-O", "tools/verify_degree32_receipt.py"])

    print("APPLICATION PROGRAMME GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
