#!/usr/bin/env python3
"""Semantically verify the global-completion receipts and source lock."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "receipts" / "global_completion_receipt.json"
CAS_RECEIPT = ROOT / "receipts" / "global_interface_cas_receipt.json"
PROTOCOL = ROOT / "formal" / "global_verification_protocol.json"
LOCK = ROOT / "formal" / "global_verification_lock.json"
LEAN_SOURCE = ROOT / "formal" / "lean" / "CyclicityGlobal.lean"
PROOF_NOTE = ROOT / "ALL_DEGREE_GLOBAL_COMPLETION.md"
SOURCE_AUDIT = ROOT / "GLOBAL_COMPLETION_SOURCE_AUDIT.md"
REVIEW = ROOT / "ALL_DEGREE_GLOBAL_REVIEW.md"
DICKSON_PROOF = ROOT / "DICKSON_EXTENSION_COMPLETION.md"
KUMMER_RECEIPT = ROOT / "receipts" / "kummer_normalizer_receipt.json"
KUMMER_MANIFEST = ROOT / "KUMMER_NORMALIZER_MANIFEST.sha256"
FINITE_GROUP_REAUDIT = ROOT / "programme" / "FINITE_LINEAR_GROUP_REFEREE_REPORT.md"
MONODROMY_RITT_REAUDIT = ROOT / "programme" / "MONODROMY_RITT_REFEREE_REPORT.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def checked_digest(value: dict[str, Any], field: str) -> None:
    claimed = value.pop(field, None)
    if not isinstance(claimed, str) or canonical_hash(value) != claimed:
        raise ValueError(f"{field} mismatch")
    value[field] = claimed


def theorem_names(source: str) -> list[str]:
    return re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)


def expected_theorems(protocol: dict[str, Any]) -> list[str]:
    claims = protocol["exact_claims"]
    return (
        claims["pole_order_theorems"]
        + claims["full_block_theorems"]
        + claims["scalar_extension_theorems"]
        + claims["primitive_character_theorems"]
    )


def verify_manifest(path: Path) -> None:
    seen: set[str] = set()
    for line in path.read_text().splitlines():
        digest, relative = line.split("  ", 1)
        if relative in seen or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"invalid manifest row: {relative}")
        seen.add(relative)
        target = ROOT / relative
        if not target.is_file() or sha256(target) != digest:
            raise ValueError(f"manifest source mismatch: {relative}")
    if not seen:
        raise ValueError("empty Kummer manifest")


def verify_cas(protocol: dict[str, Any]) -> dict[str, Any]:
    cas = json.loads(CAS_RECEIPT.read_text())
    checked_digest(cas, "receipt_sha256")
    if cas.get("schema") != "cyclicity-global-interface-cas-receipt-v1":
        raise ValueError("CAS schema mismatch")
    if cas.get("status") != "pass":
        raise ValueError("CAS status is not pass")
    if cas.get("engine") != {"name": "SymPy", "version": "1.14.0"}:
        raise ValueError("CAS engine identity mismatch")
    requirements = protocol["cas_requirements"]
    if sorted(cas.get("exact_checks", {})) != sorted(requirements["exact_check_keys"]):
        raise ValueError("CAS exact-check inventory mismatch")
    bounded = cas.get("bounded_regression_controls", {})
    if bounded.get("dickson_case_count") != requirements["bounded_dickson_case_count"]:
        raise ValueError("Dickson regression count mismatch")
    if bounded.get("floor_case_count") != requirements["bounded_floor_case_count"]:
        raise ValueError("floor regression count mismatch")
    if bounded.get("all_degree_claim") is not False:
        raise ValueError("bounded CAS controls promoted to an all-degree claim")
    expected_assurance = {
        "independent_implementation": True,
        "symbolic_identity_checks": True,
        "finite_group_classification_reproved": False,
        "external_independence": False,
    }
    if cas.get("assurance") != expected_assurance:
        raise ValueError("CAS assurance boundary mismatch")
    return cas


def verify(receipt_path: Path) -> dict[str, Any]:
    protocol = json.loads(PROTOCOL.read_text())
    lock = json.loads(LOCK.read_text())
    checked_digest(lock, "lock_sha256")
    if lock.get("schema") != "cyclicity-global-completion-lock-v2":
        raise ValueError("lock schema mismatch")
    for relative, expected in lock["files"].items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"locked source mismatch: {relative}")

    source = LEAN_SOURCE.read_text()
    if re.search(r"\b(sorry|admit|axiom)\b", source):
        raise ValueError("Lean placeholder or axiom declaration detected")
    names = theorem_names(source)
    expected_names = expected_theorems(protocol)
    if names != expected_names or len(names) != 16:
        raise ValueError("Lean theorem inventory mismatch")

    source_text = SOURCE_AUDIT.read_text()
    source_ids = protocol["source_identities"]
    required_tokens = [
        source_ids["behajaina_koenig_neftin"]["arxiv"],
        *source_ids["behajaina_koenig_neftin"]["locators"],
        source_ids["burda_khovanskii"]["arxiv"],
        source_ids["burda_khovanskii"]["source_archive_sha256"],
        source_ids["burda_khovanskii"]["locator"],
        source_ids["calbeto"]["arxiv"],
        source_ids["calbeto"]["source_archive_sha256"],
        *source_ids["calbeto"]["locators"],
    ]
    if any(token not in source_text for token in required_tokens):
        raise ValueError("source-audit identity or theorem locator missing")

    cas = verify_cas(protocol)
    verify_manifest(KUMMER_MANIFEST)
    from verify_kummer_normalizer import verify as verify_kummer

    kummer = verify_kummer(KUMMER_RECEIPT)
    receipt = json.loads(receipt_path.read_text())
    checked_digest(receipt, "receipt_sha256")
    if receipt.get("schema") != "cyclicity-global-completion-receipt-v2":
        raise ValueError("receipt schema mismatch")
    if receipt.get("status") != "pass":
        raise ValueError("receipt status is not pass")
    if receipt.get("protocol_sha256") != sha256(PROTOCOL):
        raise ValueError("protocol identity mismatch")
    if receipt.get("lock_sha256") != lock["lock_sha256"]:
        raise ValueError("lock identity mismatch")
    if receipt.get("proof_note_sha256") != sha256(PROOF_NOTE):
        raise ValueError("proof-note identity mismatch")
    if receipt.get("source_audit_sha256") != sha256(SOURCE_AUDIT):
        raise ValueError("source-audit identity mismatch")
    if receipt.get("review_sha256") != sha256(REVIEW):
        raise ValueError("review identity mismatch")

    requirements = protocol["component_requirements"]
    expected_components = {
        "dickson": {
            "proof_note_sha256": sha256(DICKSON_PROOF),
            "proof_kind": requirements["dickson"]["proof_kind"],
            "bounded_grid_is_proof": False,
            "covers_arbitrary_outer_degree": True,
        },
        "kummer": {
            "receipt_schema": requirements["kummer"]["receipt_schema"],
            "receipt_sha256": kummer["receipt_sha256"],
            "file_sha256": sha256(KUMMER_RECEIPT),
            "manifest_sha256": sha256(KUMMER_MANIFEST),
            "uniform_full_kummer_kernel_claim": False,
            "exceptional_even_relation_encoded": True,
        },
        "internal_reaudits": {
            "finite_linear_group": {
                "status": requirements["internal_reaudits"]["finite_linear_group"],
                "report_sha256": sha256(FINITE_GROUP_REAUDIT),
            },
            "monodromy_ritt": {
                "status": requirements["internal_reaudits"]["monodromy_ritt"],
                "report_sha256": sha256(MONODROMY_RITT_REAUDIT),
            },
            "external_independence": False,
        },
    }
    if receipt.get("proof_components") != expected_components:
        raise ValueError("proof-component identity or assurance mismatch")

    lean = receipt.get("lean", {})
    if lean.get("source_sha256") != lock["files"]["formal/lean/CyclicityGlobal.lean"]:
        raise ValueError("Lean source identity mismatch")
    if lean.get("kernel_status") != "pass" or lean.get("placeholder_scan") != "pass":
        raise ValueError("Lean assurance status mismatch")
    if lean.get("theorems") != expected_names or lean.get("theorem_count") != 16:
        raise ValueError("receipt theorem inventory mismatch")
    if not str(lean.get("version", "")).startswith("Lean (version 4.32.1"):
        raise ValueError("Lean version mismatch")
    commit = lean.get("mathlib_commit")
    if not isinstance(commit, str) or len(commit) != 40:
        raise ValueError("Mathlib identity missing")

    receipt_cas = receipt.get("cas", {})
    if receipt_cas.get("receipt_sha256") != cas["receipt_sha256"]:
        raise ValueError("CAS semantic receipt identity mismatch")
    if receipt_cas.get("file_sha256") != sha256(CAS_RECEIPT):
        raise ValueError("CAS byte identity mismatch")
    if sorted(receipt_cas.get("exact_check_keys", [])) != sorted(
        protocol["cas_requirements"]["exact_check_keys"]
    ):
        raise ValueError("embedded CAS inventory mismatch")
    if receipt_cas.get("bounded_regression_controls") != cas["bounded_regression_controls"]:
        raise ValueError("embedded bounded-control boundary mismatch")

    expected_interfaces = {
        "inherited_root_span": "written DFT and disjoint-residue proof; q equality imports the parent formal-moment theorem",
        "finite_pole_infinity_order": "written invariant-integral descent plus Lean degree-to-constancy kernel",
        "primitive_factor_audit": "source-exact group intersections, stabilisers, and restriction-character numerators",
        "rank_preserving_extensions": "full-block stabiliser, repaired stratified Kummer transport, direct all-degree Dickson invariant-field proof, quartic kernels, and non-repetition",
    }
    if receipt.get("interfaces") != expected_interfaces:
        raise ValueError("interface completion map mismatch")
    expected_assurance = {
        "candidate_complete_relative_to_named_imports": True,
        "formal_kernel": True,
        "independent_cas_implementation": True,
        "complete_atlas_formalization": False,
        "imported_classifications_formalized": False,
        "uniform_full_kummer_kernel_claim": False,
        "internal_separate_reaudits": True,
        "external_independence": False,
        "peer_reviewed": False,
        "published": False,
    }
    if receipt.get("assurance") != expected_assurance:
        raise ValueError("global assurance boundary mismatch")
    if receipt.get("claim_boundary") != protocol["claim_boundary"]:
        raise ValueError("claim boundary mismatch")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    try:
        receipt = verify(args.receipt)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"GLOBAL COMPLETION VERIFY FAIL: {exc}")
        return 1
    if not args.quiet:
        print(
            json.dumps(
                {
                    "status": "pass",
                    "lean_theorem_count": receipt["lean"]["theorem_count"],
                    "cas_exact_check_count": len(receipt["cas"]["exact_check_keys"]),
                    "receipt_sha256": receipt["receipt_sha256"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
