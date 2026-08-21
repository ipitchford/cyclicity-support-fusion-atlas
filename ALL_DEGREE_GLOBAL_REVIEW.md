# Adversarial review: global low-rank completion

Date: 2026-08-21  
Artifact reviewed: `ALL_DEGREE_GLOBAL_COMPLETION.md`  
Review mode: internal, source-aware, adversarial; no claim of external
independence

## Reviewer configuration

- primary role: editor-in-chief in algebraic analysis;
- methodology: algebraic function fields, integrality, and local order at
  infinity;
- domain: polynomial monodromy, primitive permutation groups, and Ritt
  decomposition;
- secondary perspective: finite complex linear groups and character
  restriction;
- devil's-advocate focus: hidden analytic assumptions, nonfaithful projective
  actions, partial block kernels, exceptional Ritt moves, and repeatable
  rank-preserving steps.

## Decision

**PASS as an internally complete theorem candidate relative to the named
imported classification results.**

**GO for a clearly labelled public unrefereed candidate release.  HOLD for
promotion as an externally established all-degree theorem.**  Two separate
internal specialist re-audits now pass: one for finite linear groups and the
repaired coefficient-stratified Kummer argument, and one for polynomial
monodromy/Ritt theory and the direct all-degree Dickson argument.  These are
strong internal checks, not external independence or peer review.

## Traceability to the four requested interfaces

| Interface | Location | Adversarial finding | Internal status |
|---|---|---|---|
| inherited root-span | Theorem 2.1, Corollary 2.2 | Fourier inversion and disjoint Laurent residue classes prove `dim W=|Sigma|`; `q=|Sigma|` remains correctly traced to the parent formal-moment theorem | closed relative to parent theorem |
| finite-pole/infinity descent | Lemma 3.1, Corollary 3.2 | invariance puts `f_k^m` in `C(z)`; integrality puts it in `C[z]`; order `<1` forces a constant; the top coefficient is computed exactly | closed |
| primitive-factor audit | Proposition 5.1, source audit | every group, degree, stabiliser, and character numerator is explicit; the dimension-three monomial/primitive dichotomy removes the former opaque kernel step | closed relative to Müller/Calbetó/ATLAS inputs |
| rank-preserving extensions | Sections 6--9 | the full-block stabiliser supplies absolute block monodromy; Kummer transport is coefficient-stratified; Dickson extensions are classified directly for arbitrary outer degree; quartic kernels and non-repetition are explicit | closed as an internally re-audited candidate |

## Major attacks performed

### 1. Does the pole argument still hide analytic boundedness?

No.  The key object is `f_k^m`, not `f_k`.  Monodromy invariance puts it in
the rational base field, transitivity of integrality makes it integral over
`C[z]`, and normality of `C[z]` makes it a polynomial.  The infinity estimate
then bounds an integer polynomial degree.  This is an algebraic divisor/order
argument and does not invoke Liouville's theorem or a contour estimate.

### 2. Can two different Laurent channels cancel?

No over constants: each channel has exponents in one residue class modulo the
degree, and these supports are disjoint.  This proves linear independence of
the nonzero channels.  The review notes, correctly, that identifying cyclic
rank with the channel count also imports the parent formal-moment theorem; the
successor does not silently reprove it.

### 3. Is the primitive intersection incomplete?

No omitted candidate was found.  In dimension two the source table contains
`A_4,S_4,A_5`; only `S_4` degree four and `A_5` degree five intersect the
polynomial list, and their point stabilisers are noncyclic.  In dimension
three an irreducible imprimitive image is monomial and solvable.  The
nonsolvable intersection of the primitive table and polynomial list is
exactly `A_5` degree five and `PSL_3(2)` degree seven.  The displayed
restriction multiplicities vanish.

### 4. Does equal block span imply equal point configurations?

The predecessor's unsafe shortcut is not reused.  Lemma 6.1 only concludes
that an element fixing one full block pointwise fixes a spanning set and is
the identity.  It uses this to forbid partial-support kernels, which is the
correct inference.

### 5. Are the rank-preserving transports exhaustive?

The original uniform Kummer-kernel assertion was false on
`B!=0`, `A^2=4B`, and even `m`.  It has been withdrawn.  The successor now
separates this stratum, records the exact Kummer relation, treats `m=2` as the
rank-two Dickson overlap, and descends `m=2k`, `k>=2`, through the already
classified phase `x^(3k)+b x^k`.  It also separates the affine-power cubic
locus `3B=A^2`, whose cubic monodromy is `C_3`, and verifies the tetrahedral
normaliser and Fourier coefficient equations there.

Lemma 6.3 replaces the former kernel-image shortcut: the full setwise block
stabiliser restricts surjectively to the absolute block monodromy.  On the
nonexceptional cubic strata this full action preserves the three Kummer
weight lines, after which the coefficient equations give only the
odd-cubic involution.

For rank two, the direct Dickson proof starts with an arbitrary outer
polynomial `R`.  Fourier projection recovers the uniformizer `U`; all other
blocks have uniformizers `cU` or `c/U`; the entire splitting field is
`C(U)`; and the Galois group is the dihedral group of order
`2m deg R`.  Its invariant field is generated by `D_(m deg R)`, so every
rank-preserving extension is the aligned Dickson extension.  This covers
mixed decompositions, repeated primes, quadratic overlaps, and all Ritt moves
without promoting the bounded Dickson grid into a proof.

For the quartic, Theorems 2.3, 2.4, and 2.7 of the cited preprint cover the
three exhaustive outer-monodromy classes from Theorem 3.3.  Every
noncollision case has a proper-support `V_4` product and contradicts Lemma
6.1.  The collision and its scalar normaliser calculation are explicit.

## Notes requiring external attention

1. The 2026 Behajaina--Koenig--Neftin source is a public arXiv preprint and
   includes source-side Magma calculations.  Its theorems are legitimate
   named hypotheses here, but should receive independent specialist checking
   before a public theorem claim.
2. The repaired Kummer and Dickson arguments have passed separate internal
   specialist re-audits.  External specialists should still check their
   function-field, monodromy, and finite-linear-group inputs before any claim
   of external establishment.
3. Lean verifies the order-to-constancy arithmetic, spanning implication,
   scalar eliminations, and character numerators.  It does not verify
   algebraic-function-field integrality, monodromy, Ritt theory, or the group
   classifications.
4. The SymPy Dickson grid is a bounded regression control only.  The
   all-degree Dickson statement rests on the direct rational-function
   invariant-field proof, not on that grid or on the long-chain preprint.
5. The novelty search now includes zbMATH Open, OpenAlex citation-forward
   coverage, Semantic Scholar cross-checking, and AMS Batch MR Lookup for
   bibliography identity.  Its outcome is bounded uncertainty, not a claim
   of exhaustive MathSciNet discovery, novelty, or priority.

## Editorial assessment

- correctness as a theorem candidate relative to named imports: **PASS after
  two separate internal repair re-audits**;
- transparency of assurance boundary: **exemplary**;
- reproducibility of local algebra: **strong after Lean and CAS replay**;
- candidate-release status: **GO, only with “public unrefereed theorem
  candidate” labelling**;
- external validation: **not yet present**;
- recommended next gate: genuinely external specialist review and independent
  reproduction, while preserving the present candidate status until then.
