# Inverse-Root Support and Fourier Fusion

Version **0.6.0-candidate** is an additive successor to the public v0.5.0
candidate and the two earlier fixed-seed cyclicity releases.

## Decision

**GO for public specialist circulation as an unrefereed theorem candidate;
HOLD for promotion as an externally established theorem.**

Relative to the named primitive-polynomial-monodromy and finite-projective-
group classification results, the successor proves an all-degree
classification of complex polynomial phases with fixed-seed cyclic rank at
most three. It also classifies all proper rank-preserving outer extensions.
The proof closes the inherited root-span interface, finite-pole/infinity-order
descent, primitive-factor audit, coefficient-stratified Kummer transport, and
arbitrary mixed Dickson chains. The finite degree-20 and preregistered
degree-32 computations remain regression and bridge evidence, not the basis
of the universal claim.

## Start here

- `All-Degree-Low-Rank-Coefficient-Atlas.pdf`: reader-facing successor paper.
- `ALL_DEGREE_GLOBAL_COMPLETION.md`: sealed all-degree proof.
- `ALL_DEGREE_RELEASE.md` and `ALL_DEGREE_RELEASE_BACK_MATTER.md`: release
  framing, correction record, limitations, and disclosures.
- `STATUS.md`, `ASSURANCE.md`, and `GLOBAL_COMPLETION_ASSURANCE.md`: decision
  and assurance ceiling.
- `CLAIMS.json` and `CLAIM_EVIDENCE_MAP.json`: machine-readable claims,
  locators, predecessor bridge, and release gates.
- `GLOBAL_COMPLETION_SOURCE_AUDIT.md` and `CITATION_AUDIT.md`: imported-result
  and literature-search boundaries.
- `MANUSCRIPT.md`: preserved v0.5 predecessor manuscript; its Conjecture 13.2
  is superseded only by the additive proof named above.

## Authoritative replay

```bash
python3 run_global_completion_checks.py
```

The command verifies every bounded predecessor and successor manifest,
replays the repaired Kummer component, checks the global semantic receipt in
ordinary and optimised Python, rejects thirteen adversarial mutations in each
mode, and reruns the independent SymPy and Lean controls. A release replay
must end with all three explicit global-gate lines; silence or timeout is not
a pass.

The deterministic publication archive is controlled separately:

```bash
python3 tools/build_all_degree_release.py verify
```

## Immutable identity

- Repository: <https://github.com/ipitchford/cyclicity-support-fusion-atlas>
- Candidate tag: `v0.6.0-candidate`
- Exact-version DOI: <https://doi.org/10.5281/zenodo.22045144>
- Concept DOI: <https://doi.org/10.5281/zenodo.22036029>
- Reader page: <https://evidencepress.org/releases/cyclicity-support-fusion-atlas/>
- Preserved predecessor: tag `v0.5.0-candidate`, DOI
  <https://doi.org/10.5281/zenodo.22036030>

These surfaces establish availability and byte identity. They do not
establish unaffiliated reproduction, complete formalisation, external
specialist sign-off, journal peer review, correctness of imported
classifications, or settled novelty and priority.

## Rebuild release metadata and archive

After any authorised change to release bytes:

```bash
python3 tools/build_all_degree_release.py freeze
python3 tools/build_all_degree_release.py archive \
  ../cyclicity-support-fusion-atlas-v0.6.0-candidate.zip
python3 tools/build_all_degree_release.py bind-archive \
  ../cyclicity-support-fusion-atlas-v0.6.0-candidate.zip \
  receipts/all_degree_archive_receipt.json
```

The archive builder verifies complete manifest coverage, sorts members, fixes
timestamps, strips host metadata, and records the archive, manifest, release
receipt, and PDF identities together.
