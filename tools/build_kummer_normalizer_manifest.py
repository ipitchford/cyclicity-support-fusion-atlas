#!/usr/bin/env python3
"""Build or verify the bounded Kummer normalizer manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "KUMMER_NORMALIZER_MANIFEST.sha256"
PATHS = {
    "KUMMER_NORMALIZER_COMPLETION.md",
    "KUMMER_NORMALIZER_ASSURANCE.md",
    "cleanroom/kummer_normalizer_audit.py",
    "formal/kummer_normalizer_lock.json",
    "formal/kummer_normalizer_protocol.json",
    "formal/lean/CyclicityKummer.lean",
    "formal/lean/KUMMER_README.md",
    "receipts/kummer_normalizer_receipt.json",
    "run_kummer_normalizer_checks.py",
    "tests/test_kummer_normalizer.py",
    "tools/build_kummer_normalizer_manifest.py",
    "tools/run_kummer_normalizer.py",
    "tools/seal_kummer_normalizer.py",
    "tools/verify_kummer_normalizer.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rendered() -> str:
    missing = sorted(relative for relative in PATHS if not (ROOT / relative).is_file())
    if missing:
        raise RuntimeError(f"missing manifest paths: {missing}")
    return "".join(f"{sha256(ROOT / relative)}  {relative}\n" for relative in sorted(PATHS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = rendered()
    if args.check:
        if not MANIFEST.is_file() or MANIFEST.read_text() != expected:
            raise SystemExit("Kummer normalizer manifest mismatch")
        print(f"Kummer normalizer manifest verified: {len(PATHS)} paths")
    else:
        MANIFEST.write_text(expected)
        print(f"Kummer normalizer manifest frozen: {len(PATHS)} paths; sha256 {sha256(MANIFEST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
