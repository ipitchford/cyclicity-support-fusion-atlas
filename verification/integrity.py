#!/usr/bin/env python3
"""Hash and manifest primitives used by the release gate and its mutations."""

from __future__ import annotations

import hashlib
from pathlib import Path


IGNORED_NAMES = {"MANIFEST.sha256", ".DS_Store"}
IGNORED_PARTS = {"__pycache__", ".git"}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_files(root: Path) -> set[str]:
    files = set()
    for path in root.rglob("*"):
        if not path.is_file() or path.name in IGNORED_NAMES:
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        files.add(relative.as_posix())
    return files


def parse_manifest(manifest: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line_number, raw in enumerate(manifest.read_text().splitlines(), 1):
        if not raw.strip():
            continue
        try:
            digest, relative = raw.split("  ", 1)
        except ValueError as exc:
            raise ValueError(f"malformed manifest line {line_number}") from exc
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError(f"invalid SHA-256 on manifest line {line_number}")
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"unsafe path on manifest line {line_number}: {relative}")
        if relative in entries:
            raise ValueError(f"duplicate manifest path: {relative}")
        entries[relative] = digest
    return entries


def verify_manifest(root: Path, manifest: Path, require_complete: bool = True) -> None:
    entries = parse_manifest(manifest)
    for relative, expected in entries.items():
        target = root / relative
        if not target.is_file():
            raise FileNotFoundError(f"manifest target missing: {relative}")
        observed = sha256_path(target)
        if observed != expected:
            raise ValueError(
                f"manifest digest mismatch for {relative}: {observed} != {expected}"
            )
    if require_complete:
        actual = package_files(root)
        listed = set(entries)
        if actual != listed:
            missing = sorted(actual - listed)
            stale = sorted(listed - actual)
            raise ValueError(f"manifest coverage mismatch: unlisted={missing}, stale={stale}")


def verify_expected_digest(path: Path, expected: str) -> None:
    observed = sha256_path(path)
    if observed != expected:
        raise ValueError(f"receipt digest mismatch for {path.name}: {observed} != {expected}")
