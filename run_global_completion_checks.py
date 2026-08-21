#!/usr/bin/env python3
"""Composite replay gate for the global all-degree completion successor."""

from __future__ import annotations

import argparse
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
from build_degree32_universal_manifest import PATHS as DEGREE32_PATHS  # noqa: E402
from build_global_completion_manifest import PATHS as GLOBAL_PATHS  # noqa: E402
from build_independent_formalization_manifest import PATHS as INDEPENDENT_PATHS  # noqa: E402
from build_uniform_structural_manifest import PATHS as UNIFORM_PATHS  # noqa: E402
from integrity import parse_manifest, sha256_path  # noqa: E402


PARENT_MANIFEST_SHA256 = "5fa7af3d4602e6257319a556809066ff1bda262255011b4720d304da7657fde0"
PARENT_METADATA_OVERRIDES = {
    ".gitignore",
    ".github/workflows/replay.yml",
    ".zenodo.json",
    "AI_INDEX.md",
    "ASSURANCE.md",
    "ATLAS_STATUS.md",
    "CITATION.cff",
    "CITATION_AUDIT.md",
    "CLAIMS.json",
    "CLAIM_EVIDENCE_MAP.json",
    "ENVIRONMENT.txt",
    "LICENSES.md",
    "PROVENANCE.md",
    "README.md",
    "REPRODUCIBILITY.md",
    "SOURCES.md",
    "STATUS.md",
}


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


def verify_bounded_manifest(
    path: Path,
    expected_paths: set[str],
    label: str,
    aliases: dict[str, Path] | None = None,
) -> None:
    entries = parse_manifest(path)
    if set(entries) != expected_paths:
        missing = sorted(expected_paths - set(entries))
        stale = sorted(set(entries) - expected_paths)
        raise SystemExit(f"[FAIL] {label} coverage: missing={missing}, stale={stale}")
    aliases = aliases or {}
    for relative, expected in entries.items():
        target = aliases.get(relative, ROOT / relative)
        if not target.is_file() or sha256_path(target) != expected:
            raise SystemExit(f"[FAIL] {label} digest: {relative}")
    print(f"[PASS] {label}", flush=True)


def verify_parent_continuity() -> None:
    """Preserve the parent receipt and fail on undeclared in-place changes.

    A successor must replace root-facing metadata, so requiring every v0.5
    pathname to retain its old bytes would make an honest version update
    impossible.  The old manifest itself is pinned here; all parent paths must
    still exist, and only the declared publication-metadata paths may differ.
    """

    manifest = ROOT / "PARENT_v0.5.0_MANIFEST.sha256"
    if sha256_path(manifest) != PARENT_MANIFEST_SHA256:
        raise SystemExit("[FAIL] published-parent manifest identity mismatch")
    entries = parse_manifest(manifest)
    missing: set[str] = set()
    changed: set[str] = set()
    for relative, expected in entries.items():
        target = ROOT / relative
        if not target.is_file():
            missing.add(relative)
        elif sha256_path(target) != expected:
            changed.add(relative)
    if missing:
        raise SystemExit(f"[FAIL] published-parent paths missing: {sorted(missing)}")
    unexpected = changed - PARENT_METADATA_OVERRIDES
    absent = PARENT_METADATA_OVERRIDES - changed
    if unexpected or absent:
        raise SystemExit(
            "[FAIL] published-parent continuity mismatch: "
            f"unexpected_changes={sorted(unexpected)}, "
            f"missing_declared_overrides={sorted(absent)}"
        )
    print(
        "[PASS] published-parent manifest preserved; "
        f"{len(changed)} declared successor metadata overrides",
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-predecessor-gate",
        action="store_true",
        help="skip live predecessor orchestration while retaining every predecessor manifest check",
    )
    parser.add_argument(
        "--skip-engine-recompute",
        action="store_true",
        help="validate frozen global receipts without rerunning Lean and SymPy",
    )
    parser.add_argument("--mathlib-project", type=Path)
    args = parser.parse_args()
    python = sys.executable
    print(f"python={python}")
    print(f"version={sys.version.split()[0]}")

    verify_parent_continuity()
    verify_bounded_manifest(
        ROOT / "APPLICATIONS_MANIFEST.sha256",
        APPLICATION_PATHS,
        "bounded application manifest",
        {"MANIFEST.sha256": ROOT / "PARENT_v0.5.0_MANIFEST.sha256"},
    )
    verify_bounded_manifest(
        ROOT / "DEGREE32_UNIVERSAL_MANIFEST.sha256", DEGREE32_PATHS, "bounded degree-32 manifest"
    )
    verify_bounded_manifest(
        ROOT / "INDEPENDENT_FORMALIZATION_MANIFEST.sha256",
        INDEPENDENT_PATHS,
        "bounded independent-formalization manifest",
    )
    verify_bounded_manifest(
        ROOT / "UNIFORM_STRUCTURAL_MANIFEST.sha256",
        UNIFORM_PATHS,
        "bounded uniform-structural manifest",
    )
    verify_bounded_manifest(
        ROOT / "GLOBAL_COMPLETION_MANIFEST.sha256",
        GLOBAL_PATHS,
        "bounded global-completion manifest",
    )

    if not args.skip_predecessor_gate:
        run(
            "predecessor uniform all-m gate",
            [
                python,
                "run_uniform_structural_checks.py",
                "--successor-root",
                "--skip-predecessor-gate",
                "--skip-engine-recompute",
            ],
        )

    run("global semantic verifier [normal]", [python, "tools/verify_global_completion.py"])
    run(
        "global semantic verifier [optimized]",
        [python, "-O", "tools/verify_global_completion.py"],
    )
    run(
        "global mutation controls [normal]",
        [python, "-m", "unittest", "tests/test_global_completion.py", "-v"],
    )
    run(
        "global mutation controls [optimized]",
        [python, "-O", "-m", "unittest", "tests/test_global_completion.py", "-v"],
    )

    if not args.skip_engine_recompute:
        with tempfile.TemporaryDirectory(prefix="global-completion-gate-") as directory:
            tmp = Path(directory)
            cas_normal = tmp / "cas-normal.json"
            cas_optimized = tmp / "cas-optimized.json"
            run(
                "live independent CAS replay [normal]",
                [python, "cleanroom/global_interface_audit.py", "--output", str(cas_normal)],
            )
            run(
                "live independent CAS replay [optimized]",
                [python, "-O", "cleanroom/global_interface_audit.py", "--output", str(cas_optimized)],
            )
            require_equal(cas_normal, cas_optimized, "normal/optimized CAS parity")
            require_equal(
                cas_normal,
                ROOT / "receipts" / "global_interface_cas_receipt.json",
                "frozen independent CAS receipt",
            )

            normal = tmp / "global-normal.json"
            optimized = tmp / "global-optimized.json"
            base = ["tools/run_global_completion.py"]
            if args.mathlib_project is not None:
                base.extend(["--mathlib-project", str(args.mathlib_project)])
            run("live global Lean/CAS replay [normal]", [python, *base, "--output", str(normal)])
            run(
                "live global Lean/CAS replay [optimized]",
                [python, "-O", *base, "--output", str(optimized)],
            )
            require_equal(normal, optimized, "normal/optimized global replay parity")
            require_equal(
                normal,
                ROOT / "receipts" / "global_completion_receipt.json",
                "frozen global completion receipt",
            )

    print("GLOBAL ALL-DEGREE COMPLETION GATE PASS")
    print("PUBLIC UNREFEREED-CANDIDATE RELEASE GO")
    print("EXTERNALLY ESTABLISHED THEOREM PROMOTION REMAINS HOLD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
