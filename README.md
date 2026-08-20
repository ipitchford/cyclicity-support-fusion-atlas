# Inverse-Root Support and Fourier Fusion

Version **0.5.0-candidate** is an additive public successor to the v0.4.0
review package and to the two earlier fixed-seed cyclicity releases.

## Decision

**PASS_WITH_NOTES for specialist circulation as an unrefereed theorem
candidate.**

The universal support/root-span identity and Fourier block-fusion calculus are
presented with complete proofs. The affine coefficient atlas is a finite
computer-assisted theorem candidate through degree twenty, backed by a
fail-closed 1,152-case exact-arithmetic sweep. The all-degree atlas remains
Conjecture 13.2 because the quartic/cubic descent is not closed.

## Start here

- `MANUSCRIPT.md` and the PDF: complete mathematical argument.
- `STATUS.md` and `ASSURANCE.md`: claim ceiling and evidence vector.
- `CLAIMS.json` and `CLAIM_EVIDENCE_MAP.json`: machine-readable claims,
  locators, predecessor bridge and release gates.
- `reviews/RESPONSE_TO_REVIEW.md`: point-by-point round-one resolution.
- `reviews/CONFIRMATION_REVIEW_R2.md`: frozen-target confirmation and calibrated
  field-facing assessment.
- `REPRODUCIBILITY.md`: authoritative replay and trust boundary.
- `MATERIALS_AUDIT.md`: chronological disposition of every supplied material.
- `source-history/`: preserved earlier manuscripts, corrections and
  exploratory programmes.

## Authoritative replay

```bash
python3 run_core_checks.py
```

The command verifies the manifest, executes all retained tests under ordinary
and optimised Python, reruns every atlas case, compares regenerated receipts
with frozen hashes and requires semantic corruptions to fail.

## Immutable identity

- Repository: <https://github.com/ipitchford/cyclicity-support-fusion-atlas>
- Candidate tag: `v0.5.0-candidate`
- Version DOI: <https://doi.org/10.5281/zenodo.22036030>
- Reader page: <https://evidencepress.org/releases/cyclicity-support-fusion-atlas/>

These surfaces establish stable availability and byte identity. They do not
establish independent reproduction, formal verification, specialist review,
editorial peer review, novelty, priority or the all-degree atlas.

## Rebuild release metadata and archive

After any authorised change to the package bytes:

```bash
python3 tools/build_release_metadata.py freeze
python3 tools/build_archive.py ../cyclicity-support-fusion-atlas-v0.5.0-candidate.zip
python3 tools/build_release_metadata.py archive-receipt \
  ../cyclicity-support-fusion-atlas-v0.5.0-candidate.zip \
  ../cyclicity-support-fusion-atlas-v0.5.0-candidate.archive-receipt.json
```

The archive builder sorts members, fixes timestamps, strips host metadata and
verifies the complete manifest before writing.
