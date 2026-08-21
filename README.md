# Inverse-Root Support, Polynomial Amplitudes, and Laurent Moment Channels

Version **0.7.0-candidate** is the combined flagship successor in the
`cyclicity-support-fusion-atlas` lineage.

## Decision

**GO for public specialist circulation as an unrefereed theorem candidate;
HOLD for promotion as an externally established theorem.**

The unified paper presents the all-degree fixed-seed coefficient atlas for
complex polynomial phases with cyclic rank at most three, relative to named
classification inputs, together with every rank-preserving polynomial
extension. It then treats arbitrary polynomial amplitudes, exact vanishing on
a specified zero-cycle, persistent endpoint moments for every Atlas phase, and
an exact local inverse criterion for Laurent moments.

No finite all-Laurent normal-form atlas, external specialist review,
independent reproduction, complete formalisation, or priority certification is
claimed.

## Start here

- `Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf`: 25-page primary
  manuscript.
- `COMBINED_RELEASE_FRONT.md`, `COMBINED_GLOBAL_COMPLETION.md`,
  `COMBINED_AMPLITUDE_LAURENT.md`, and `COMBINED_RELEASE_BACK.md`: accessible
  manuscript sources.
- `COMBINED_STATUS.md` and `COMBINED_ASSURANCE.md`: publication decision and
  assurance boundary.
- `CLAIMS_COMBINED.json`: machine-readable positive claims and non-claims.
- `REPRODUCE_COMBINED.md`: exact replay, rendering, manifest, and visual-QA
  route.
- `COMBINED_MANIFEST.sha256`: focused theorem/document seal.
- `MANIFEST_v0.7.0.sha256`: complete v0.7 public archive inventory.

The v0.6 Atlas PDF and v0.7 short amplitude/Laurent companion remain present
as predecessor artifacts. They are not deleted or rewritten in place.

## Authoritative replay

```bash
python3 run_global_completion_checks.py
python3 run_amplitude_laurent_checks.py
python3 tools/check_combined_release.py
python3 tools/build_combined_publication.py verify
```

The first two commands replay the mathematical components in ordinary and
optimised Python with semantic mutation controls. The third checks the merged
document, claims, citations, predecessor hashes, PDF structure, and focused
manifest. The fourth checks complete publication-manifest coverage.

## Immutable identity

- Repository: <https://github.com/ipitchford/cyclicity-support-fusion-atlas>
- Candidate tag: `v0.7.0-candidate`
- Exact-version DOI: <https://doi.org/10.5281/zenodo.22049564>
- Concept DOI: <https://doi.org/10.5281/zenodo.22036029>
- Reader page:
  <https://evidencepress.org/releases/cyclicity-support-fusion-atlas/>
- Preserved v0.6 DOI: <https://doi.org/10.5281/zenodo.22045144>

These surfaces establish availability, version identity, and byte integrity.
They do not establish mathematical correctness, unaffiliated reproduction,
peer review, acceptance, novelty, or priority.

## Deterministic archive

```bash
python3 tools/build_combined_publication.py freeze
python3 tools/build_combined_publication.py archive \
  ../cyclicity-support-fusion-atlas-v0.7.0-candidate.zip
python3 tools/build_combined_publication.py bind-archive \
  ../cyclicity-support-fusion-atlas-v0.7.0-candidate.zip \
  receipts/combined_archive_receipt.json
```

Original research prose and structured records are released under CC0-1.0;
original code and tests are MIT. Third-party material retains its existing
terms or `NOASSERTION`, as detailed in `LICENSES.md`.
