# Internal adversarial review: Exponential-Period Order Oracle

Review date: 2026-08-21  
Review status: **PASS WITH NOTES for specialist circulation as an unpublished,
unrefereed research extension**

This is an internal review of the implementation and research note. It is not
external specialist review, independent reproduction or an editorial decision.

## 1. Review question

Does the extension correctly and reproducibly turn the parent manuscript's
generic minimal-ODE-order corollary into an exact operator oracle without
overstating contourwise minimality, computational independence or publication
status?

## 2. Load-bearing findings

### 2.1 Original phase versus normalised support — resolved

An early implementation risk was to derive the displayed operator only for the
affine-normalised phase. That would preserve the order but generally give the
wrong coefficients for the requested original integral, because a target shift
introduces an exponential gauge and a target scaling changes the differential
variable. The final implementation computes support on the normal form and the
Krylov operator directly on the original polynomial. An affine regression test
requires equal order/support but different operator coefficients.

### 2.2 Full ambient rank needs one additional Krylov column — resolved

The parent rank calculator stores the (d-1) columns needed to determine rank.
If (q=d-1), those columns are all independent and do not yet display the
first dependence. The oracle therefore constructs columns through
\([P^{d-1}dx]\). The degree-four rank-three benchmark exercises this boundary.

### 2.3 Exact operator normalisation — passed

The first relation is solved on a deterministic nonsingular minor. Rational
denominators in (s) are cleared, the common polynomial factor and scalar
content are removed, and the sign is fixed from the highest-derivative
coefficient. The resulting list lies in \(\mathbf Z[s]\). Substitution into the
original exact Krylov matrix must have identically zero residual.

### 2.4 Same-path confirmation risk — mitigated, not eliminated

The support and production operator share the parent symbolic reduction family.
A separate script therefore derives six representative operators using a
different (u=1/s) polynomial reduction and imports neither production module.
It compares operators only up to a common nonzero factor. This is a meaningful
within-programme fault control, but it still uses SymPy and is not an
unaffiliated or second-CAS reproduction.

### 2.5 Generic versus individual-cycle minimality — correctly bounded

The research note and JSON schema consistently say that the order is minimal
for a generic functional on the complete rapid-decay period solution space.
They do not claim minimality for every individual contour. Arbitrary contour
admissibility is also excluded.

### 2.6 High-order expression swell — honestly routed

The fully symbolic degree-twelve order-eleven comparison is inappropriate for
the quick gate. It is not replaced by a numerical guess. Two exact rational
specialisations attain the ambient rank eleven, which proves generic rank
eleven for the named comparison phase. The low-order exceptional phase retains
its complete symbolic operator.

## 3. Verification results

- Eight production certificates match their specified degrees, supports and
  orders.
- Orders represented in the corpus are 1, 2, 3, 4 and 6.
- Six operators agree with the separate symbolic derivation up to a common
  nonzero factor.
- The exceptional degree-twelve phase has the frozen primitive order-three
  operator displayed in the research note.
- The generic comparison phase has exact specialised rank eleven at
  (s=3/7) and (s=-5/2), and all eleven inverse-support classes occur.
- Seven convergent real-line numerical checks pass the relative-residual
  threshold (10^{-12}); these are correctly excluded from theorem evidence.
- An altered operator coefficient is rejected with the original digest and
  after forging a matching outer digest.
- Degree-one, non-polynomial and non-rational expressions fail closed.
- Ordinary and optimised Python produce byte-identical exact receipts.
- Every byte listed in the published parent manifest remains unchanged.

## 4. Residual limitations

1. The mathematical basis remains an unrefereed theorem candidate.
2. There is no unaffiliated replay, second-CAS derivation or proof-assistant
   formalisation.
3. The implementation accepts trusted rational polynomial expressions only.
4. It does not construct contours, compute decomposition lattices or handle
   weighted seeds (g(x)dx).
5. No third-party creative-telescoping integration or performance comparison
   has yet been performed.
6. The extension has not been tagged, archived, assigned a DOI or published on
   Evidence Press.

## 5. Decision

The extension satisfies its stated research contract. The exact algebraic
certificate, negative controls, separate symbolic path, prospective generic
comparison and numerical dictionary checks are mutually consistent. The
remaining gaps are assurance and integration boundaries, not hidden failures
of the implemented claims.

**Decision: accept for specialist circulation as a complete unpublished and
unrefereed research extension, with the assurance record attached.**

