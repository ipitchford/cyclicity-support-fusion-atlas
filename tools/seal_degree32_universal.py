#!/usr/bin/env python3
"""Seal the universal degree-32 protocol, runner and inherited engines."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = [
    ROOT / "verification" / "battery4a_fast.py",
    ROOT / "verification" / "symconstr.py",
    ROOT / "verification" / "lib.py",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preregistration", type=Path, default=ROOT / "experiments" / "degree32_universal_preregistration.json")
    parser.add_argument("--runner", type=Path, default=ROOT / "experiments" / "degree32_universal_runner.py")
    parser.add_argument("--output", type=Path, default=ROOT / "experiments" / "degree32_universal_lock.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("universal degree-32 lock already exists; refusing to overwrite")
    parent_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()
    application_manifest = ROOT / "APPLICATIONS_MANIFEST.sha256"
    lock = {
        "schema": "degree32-universal-lock-v1",
        "sealed_utc": datetime.now(timezone.utc).isoformat(),
        "execution_state_at_seal": "not_run",
        "parent_git_commit": parent_commit,
        "application_manifest_sha256": sha256(application_manifest),
        "preregistration": args.preregistration.name,
        "preregistration_sha256": sha256(args.preregistration),
        "runner": args.runner.name,
        "runner_sha256": sha256(args.runner),
        "dependency_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in DEPENDENCIES
        },
    }
    args.output.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    print(json.dumps(lock, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
