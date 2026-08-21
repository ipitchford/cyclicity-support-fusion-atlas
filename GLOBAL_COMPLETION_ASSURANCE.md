# Assurance statement: global all-degree completion

Date: 2026-08-21  
Internal gate: **PASS**  
Public unrefereed-candidate release gate: **GO**  
Externally established theorem gate: **HOLD FOR EXTERNAL SPECIALIST REVIEW**

## Outcome

The inherited root-span interface, finite-pole/infinity-order descent,
remaining low-dimensional primitive-factor audit, and rank-preserving
extension analysis are closed in `ALL_DEGREE_GLOBAL_COMPLETION.md` as an
all-degree theorem candidate over `C`, relative to the named imported
classification theorems.

The repaired successor also contains a coefficient-stratified Kummer theorem,
which explicitly withdraws the false full-kernel assertion on the exceptional
even-exponent stratum, and a direct rational-function proof classifying every
Dickson extension for arbitrary outer degree.  The latter removes the former
mixed-chain reliance on a long-chain preprint theorem.

The successor is additive.  It preserves the sealed uniform all-`m`
predecessor through `UNIFORM_STRUCTURAL_MANIFEST.sha256` and does not modify
the published-parent manifest.

## Replay evidence

- Lean 4.32.1 / Mathlib commit
  `520045ab14e26149ee970e2e617ca04b09bde5d6`: 16 theorems, no `sorry`,
  `admit`, or declared `axiom`;
- SymPy 1.14.0: 10 exact table/intersection, character, scalar-elimination,
  and collision checks;
- bounded regression controls: 2,079 pole-floor cases and 81 Dickson
  composition pairs, explicitly carrying `all_degree_claim: false`;
- thirteen adversarial receipt mutations are rejected and the frozen receipt
  is accepted, under both normal and optimized Python (14 tests per mode);
- the Kummer v2 semantic receipt and all 14 files in its bounded manifest are
  verified transitively by the global v2 receipt;
- two separate internal repair re-audits pass: finite-linear-group/Kummer and
  polynomial-monodromy/Ritt/Dickson;
- source identities: arXiv:2603.27609v2, arXiv:1209.5137v1, and
  arXiv:2510.00718v1, with downloaded TeX source hashes for the latter two.

Semantic identities for the sealed v2 gate:

- global source lock:
  `b2be73c61d4e77d11d0c5559cb0797e95e35f678952a9b3ce3f156d8bb992ad0`;
- independent global-interface CAS receipt:
  `da2c5b165ba486094ec3d2b9054f17a25ef5d9b3ab36f5ab5912877dea2a8c75`;
- repaired Kummer component receipt:
  `4b50a66a1fef7619685b43c94258142ff6edd461ecef5ffd8589af289aef7e5a`;
- global completion receipt:
  `7bfaca3adf5bcd71c66cae2c674a3b560500e596e420d0de55920790b35a8b43`.

## What the pass means

The local proof architecture is complete enough for a clearly labelled public
unrefereed candidate release: every requested interface has a named statement,
proof, dependency boundary, replay evidence, and a separate internal
specialist re-audit.  The former equal-span/equal-configuration shortcut has
been replaced by the full-block stabiliser lemma.  Finite computation is no
longer being used to infer the all-degree claim.

## What the pass does not mean

It does not mean that the entire theorem is formalized.  The Lean layer does
not encode Laurent series, algebraic function-field integrality, polynomial
monodromy, Ritt theory, or finite-group classification.  The SymPy table is an
independent implementation of local deductions, not an independent proof of
the imported theorems.

It also does not establish external reproduction, peer review, novelty,
acceptance, publication, or correctness of source-side Magma computations.
The 2026 length-two monodromy paper is a current public preprint.

## Next legitimate status upgrade

Promotion beyond “public unrefereed theorem candidate” requires at least:

1. an independent polynomial-monodromy/Ritt referee to check the block-kernel
   and Kummer-line transport applications; and
2. an independent finite-linear-group referee to check the primitive table
   intersection, stabilisers, characters, and normalisers.

Until those reviews are recorded, the correct public-facing status remains
**public unrefereed theorem candidate relative to named classification
results**.  Publication under that label does not lift this hold.
