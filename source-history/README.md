# Cyclicity loci, inverse-root spans and polynomial block fusion

## Complete research-session bundle

**Date:** 19 August 2026  
**Status:** internally checked theorem candidates; not externally refereed  
**Scope:** every manuscript, addendum, review, source file, receipt and frozen stage archive produced in the session that began from the two Evidence Press releases on fixed-seed cyclicity and low-rank inverse-root spans.

## What this bundle contains

The work progressed through three cumulative stages.

### Stage 1 — Unconditional support invariant and block-fusion formula

`stages/cyclicity-unconditional-fusion-v0.1.0-candidate/`

This stage develops the direct formal-moment route to

\[
q(P,dx)=|\Sigma(P)|=\dim_{\mathbf C}W_P^{\mathrm{red}},
\]

and gives the exact Fourier-submatrix formula for sums, intersections and equality of root-block spans under a decomposition \(P=R\circ Q\). It analyses the degree-twelve Ritt collision

\[
(x^4+x)^3=H(x^3),\qquad H(y)=y(y+1)^3,
\]

with support \(\{1,7,10\}\pmod{12}\).

### Stage 2 — Explicit rapid-decay periods, canonical factors and Ritt diamonds

`stages/cyclicity-unconditional-fusion-v0.2.0-candidate/`

This stage supplies fixed rapid-decay contours, locally uniform differentiation, twisted integration by parts and an explicit Fourier–Gamma asymptotic whose nonzero determinant separates the twisted de Rham quotient. It also proves that equal block spans define an actual coarser polynomial factor, decomposes rank growth along complete decompositions, and classifies all low-rank adjacent Ritt diamonds at the support-projection level.

### Stage 3 — Affine coefficient atlas and rank-preserving extensions

`stages/cyclicity-coefficient-atlas-v0.3.0-candidate/`

This stage gives the proposed affine coefficient classification for \(q(P)\le3\), the realised support sets and the complete proposed list of proper rank-preserving polynomial extensions. The principal rank-three mechanisms are

\[
(x^{3m}+b x^m)^2
\quad\text{and}\quad
(x^4+a x)^3.
\]

The coefficient atlas is relative to the preceding support/root-span theorem and to imported classifications of primitive polynomial monodromy, finite projective linear groups and Ritt decompositions.

## Navigation

- `SESSION_SYNTHESIS.md` — integrated theorem narrative.
- `CLAIM_LEDGER.md` — claim status, dependencies and corrections.
- `REPRODUCE_ALL.sh` — reruns every available computational control in temporary copies of the frozen stages.
- `verification-logs/` — fresh consolidation-time replay outputs.
- `stage-archives/` — self-contained ZIP archives and checksums for each stage.
- `stages/` — complete extracted stage contents.
- `SHA256SUMS.txt` — hashes for every file in the master bundle except itself.
- `BUNDLE_CONTENTS.json` — machine-readable inventory and verification summary.

## Verification performed during consolidation

The following controls passed on 19 August 2026:

1. v0.1 production support, cyclic-rank, fusion and Ritt-view tests;
2. v0.2 production tests;
3. v0.2 clean-room finite audit: 9 named cases, 12 deterministic random cases, 4 composition cases and all 11 low-rank Ritt diamond types;
4. v0.2 Fourier–Gamma period-matrix numerical spot check;
5. v0.3 exact twisted-de Rham Krylov audit of 12 representatives and mutations;
6. internal SHA-256 manifests for v0.1 and v0.2.

These controls test implementations and displayed examples. They do not replace specialist review of the proofs, independent reproduction, or a dedicated novelty search.

## Frozen and replayed material

The stage archives preserve the artefacts generated at each point in the session. The extracted stage directories match those archives. Fresh replay output is stored separately under `verification-logs/`, so rerunning tests does not silently alter the frozen evidence.

## Claim boundary

The strongest warranted description is **complete theorem-candidate package**. The bundle does not claim peer review, formal verification, independent reproduction, or established priority. The finite-projective-group reduction and the quartic tetrahedron argument in the coefficient atlas deserve the closest external scrutiny.
