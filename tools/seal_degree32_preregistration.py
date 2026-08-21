#!/usr/bin/env python3
"""Seal the degree-32 protocol and runner before the first m=8 execution."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preregistration", type=Path, default=ROOT / "experiments" / "degree32_preregistration.json")
    parser.add_argument("--runner", type=Path, default=ROOT / "experiments" / "degree32_quartic_lift.py")
    parser.add_argument("--output", type=Path, default=ROOT / "experiments" / "degree32_preregistration_lock.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("preregistration lock already exists; refusing to overwrite")
    lock = {
        "schema": "degree32-preregistration-lock-v1",
        "sealed_utc": datetime.now(timezone.utc).isoformat(),
        "preregistration": args.preregistration.name,
        "preregistration_sha256": sha256(args.preregistration),
        "runner": args.runner.name,
        "runner_sha256": sha256(args.runner),
        "parent_git_commit": "ce4e129bed2c1ea5dd7b778488d7bec2b76deb7d",
        "execution_state_at_seal": "not_run",
    }
    args.output.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    print(json.dumps(lock, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
