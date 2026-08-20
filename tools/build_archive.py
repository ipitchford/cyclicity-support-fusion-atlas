#!/usr/bin/env python3
"""Build a sorted, metadata-minimal ZIP for the frozen candidate package."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))

from integrity import package_files, verify_manifest  # noqa: E402


FIXED_TIMESTAMP = (2026, 8, 20, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    manifest = ROOT / "MANIFEST.sha256"
    verify_manifest(ROOT, manifest, require_complete=True)
    paths = sorted(package_files(ROOT) | {"MANIFEST.sha256"})
    prefix = ROOT.name

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        args.output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for relative in paths:
            source = ROOT / relative
            info = zipfile.ZipInfo(f"{prefix}/{relative}", FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o100755 if source.stat().st_mode & 0o111 else 0o100644
            info.external_attr = mode << 16
            archive.writestr(info, source.read_bytes(), compresslevel=9)

    with zipfile.ZipFile(args.output) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"archive CRC failure: {bad}")
        member_count = len(archive.infolist())

    print(f"archive={args.output}")
    print(f"files={member_count}")
    print(f"bytes={args.output.stat().st_size}")
    print(f"sha256={sha256(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
