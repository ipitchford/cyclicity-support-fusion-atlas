# Candidate status: combined fixed-seed, amplitude, and Laurent theory

**Version:** 0.7.0-candidate
**Base commit:** 0dbec12158b37de8e46fe92fab7fc3030f224bce
**Branch:** research/amplitudes-laurent-v0.7
**Primary manuscript:** `Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf`
**State:** GO for public unrefereed candidate circulation; HOLD for external
theorem promotion.

## What is combined

The primary manuscript now presents one numbered argument rather than a paper
and a detached supplement:

1. Sections 1--12 give the fixed-seed inverse-root interface, all-degree
   coefficient atlas for \(q(P)\leq3\), and every rank-preserving polynomial
   extension.
2. Sections 13--17 extend the theory to arbitrary polynomial amplitudes,
   specified zero-cycles, and all persistent endpoint moments for Atlas
   phases.
3. Sections 18--21 give the exact Laurent local-channel criterion, its sharp
   boundary, computational controls, and open problems.
4. One consolidated reference list, limitation statement, declaration set,
   and bilingual front matter govern the whole manuscript.

## Verification completed

- the inherited global completion gate passes under ordinary and optimised
  Python, including its transitive predecessor checks, mutation controls,
  independent CAS implementation, and Lean/CAS replay;
- the amplitude/Laurent gate passes under ordinary and optimised Python with
  byte-identical receipts;
- the combined source builder rejects stale companion self-citations;
- the PDF renderer enables single-backslash TeX mathematics, performs a
  fail-closed exposed-TeX scan, validates the file with qpdf, and assigns a
  content-derived identifier;
- the combined HTML/PDF build is deterministic; and
- cross-references, citation labels, bookmarks, metadata, text extraction,
  page geometry, and all 25 rendered pages have been audited.

## Assurance boundary

The package supports a **public unrefereed theorem candidate relative to the
named imported classifications**. It does not establish external specialist
review, independent reproduction, complete proof-assistant formalisation,
priority, journal acceptance, or mathematical infallibility. The endpoint
classification also imports the peer-reviewed Pakovich--Muzychuk polynomial
moment theorem.

No finite all-Laurent normal-form atlas is claimed. The Laurent result is an
exact infinite coefficient criterion for each specified phase and amplitude.

## Preservation

The combined manuscript is additive. It does not delete, replace in place, or
rewrite the predecessor papers or the short extension. In particular, the
following predecessor PDF digests remain unchanged:

- `Inverse-Root-Support-and-Fourier-Fusion.pdf`:
  `e56b4d2a9000a89174b5e3a580ff44c330a83232a9c40333976b917147aa1479`;
- `All-Degree-Low-Rank-Coefficient-Atlas.pdf`:
  `b0cc6d997a3f74777e522c667840d8bb2c32afd3d2ff699e0d7023db9a65d74a`.

Publication is authorised separately by the publisher. Completion requires
immutable GitHub and Zenodo identities, guarded deployment, and canonical
public-byte readback; this status file alone does not evidence those events.
