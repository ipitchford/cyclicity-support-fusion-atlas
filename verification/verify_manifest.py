#!/usr/bin/env python3
"""Fail-closed verifier for the package manifest."""

from pathlib import Path

from integrity import verify_manifest


ROOT = Path(__file__).resolve().parents[1]
verify_manifest(ROOT, ROOT / "MANIFEST.sha256", require_complete=True)
print("MANIFEST PASS")

