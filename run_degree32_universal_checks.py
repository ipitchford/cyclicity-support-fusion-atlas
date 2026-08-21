#!/usr/bin/env python3
"""Composite gate for the universal degree-32 and Newton-descent successor."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parent
VERIFICATION = ROOT / "verification"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(VERIFICATION))
sys.path.insert(0, str(TOOLS))

from build_application_programme_manifest import APPLICATION_PATHS  # noqa: E402
from build_degree32_universal_manifest import PATHS  # noqa: E402
from integrity import parse_manifest, sha256_path, verify_manifest  # noqa: E402


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


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


def verify_replay_receipt() -> None:
    path = ROOT / "receipts" / "degree32_universal_replay.json"
    replay = json.loads(path.read_text())
    supplied = replay.get("replay_sha256")
    unhashed = dict(replay)
    unhashed.pop("replay_sha256", None)
    if supplied != canonical_hash(unhashed):
        raise SystemExit("[FAIL] degree-32 replay receipt digest")
    primary = ROOT / "receipts" / "degree32_universal_low_rank_atlas.json"
    mathematical = json.loads(primary.read_text())
    file_digest = sha256_path(primary)
    checks = (
        replay.get("schema") == "degree32-universal-replay-receipt-v1",
        replay.get("status") == "pass",
        replay.get("byte_identical") is True,
        replay.get("case_count") == 466,
        replay.get("mathematical_receipt_sha256") == mathematical.get("receipt_sha256"),
        replay.get("ordinary", {}).get("file_sha256") == file_digest,
        replay.get("optimized", {}).get("file_sha256") == file_digest,
    )
    if not all(checks):
        raise SystemExit("[FAIL] degree-32 replay receipt semantics")
    print("[PASS] frozen ordinary/optimized replay receipt", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--recompute-degree32",
        action="store_true",
        help="rerun both 466-case modes; about 27 minutes on the recorded host",
    )
    parser.add_argument(
        "--skip-application-gate",
        action="store_true",
        help="skip the predecessor composite replay while retaining manifest checks",
    )
    args = parser.parse_args()
    python = sys.executable
    print(f"python={python}")
    print(f"version={sys.version.split()[0]}")

    verify_manifest(ROOT, ROOT / "MANIFEST.sha256", require_complete=False)
    print("[PASS] published-parent listed bytes unchanged", flush=True)
    verify_bounded_manifest(ROOT / "APPLICATIONS_MANIFEST.sha256", APPLICATION_PATHS, "bounded application manifest")
    verify_bounded_manifest(ROOT / "DEGREE32_UNIVERSAL_MANIFEST.sha256", PATHS, "bounded degree-32 successor manifest")
    if not args.skip_application_gate:
        run("predecessor application programme gate", [python, "run_application_programme_checks.py"])

    with tempfile.TemporaryDirectory(prefix="degree32-universal-gate-") as tmp_name:
        tmp = Path(tmp_name)
        run("degree-32 semantic verifier [normal]", [python, "tools/verify_degree32_universal.py"])
        run("degree-32 semantic verifier [optimized]", [python, "-O", "tools/verify_degree32_universal.py"])
        run("degree-32 mutation controls [normal]", [python, "tests/test_degree32_universal.py"])
        run("degree-32 mutation controls [optimized]", [python, "-O", "tests/test_degree32_universal.py"])
        verify_replay_receipt()

        newton_normal = tmp / "newton-normal.json"
        newton_optimized = tmp / "newton-optimized.json"
        run("Newton descent bounded control [normal]", [python, "tools/check_newton_descent.py", "--output", str(newton_normal)])
        run("Newton descent bounded control [optimized]", [python, "-O", "tools/check_newton_descent.py", "--output", str(newton_optimized)])
        require_equal(newton_normal, newton_optimized, "Newton control parity")
        require_equal(newton_normal, ROOT / "receipts" / "newton_descent_check.json", "frozen Newton control")

        resultant_normal = tmp / "resultant-normal.json"
        resultant_optimized = tmp / "resultant-optimized.json"
        run("resultant cross-check [normal]", [python, "cleanroom/newton_resultant_crosscheck.py", "--output", str(resultant_normal)])
        run("resultant cross-check [optimized]", [python, "-O", "cleanroom/newton_resultant_crosscheck.py", "--output", str(resultant_optimized)])
        require_equal(resultant_normal, resultant_optimized, "resultant cross-check parity")
        require_equal(resultant_normal, ROOT / "receipts" / "newton_resultant_crosscheck.json", "frozen resultant cross-check")

        if args.recompute_degree32:
            primary = tmp / "degree32-normal.json"
            optimized = tmp / "degree32-optimized.json"
            run("universal degree-32 recomputation [normal]", [python, "experiments/degree32_universal_runner.py", "--output", str(primary)])
            run("universal degree-32 recomputation [optimized]", [python, "-O", "experiments/degree32_universal_runner.py", "--output", str(optimized)])
            require_equal(primary, optimized, "degree-32 recomputation parity")
            require_equal(primary, ROOT / "receipts" / "degree32_universal_low_rank_atlas.json", "frozen degree-32 receipt")

    print("DEGREE-32 UNIVERSAL SUCCESSOR GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
