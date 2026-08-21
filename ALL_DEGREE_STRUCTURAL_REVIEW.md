# Adversarial review: structural all-degree repair

Status: **PASS WITH NOTES for the targeted obligations**  
Date: 2026-08-21

## 1. Review boundary

This review asks whether `ALL_DEGREE_STRUCTURAL_REPAIR.md` genuinely closes
the monodromy/scaling and uniform all-`m` coefficient arguments identified as
open in the preceding assurance record.  It does not reassess the parent
root-span theorem or the complete coefficient atlas from first principles.

## 2. Monodromy audit

The cubic argument is complete within elementary Galois/monodromy theory: the
discriminant has simple zeros and is not a square, excluding `A_3`.

The quartic argument correctly proves indecomposability directly from the
trace-normalised coefficients.  The remaining inference uses the standard
polynomial-monodromy facts that indecomposable means primitive and that
inertia at infinity is a full degree cycle.  In degree four, the primitive
subgroup conclusion is exhaustive: cyclic and dihedral groups are imprimitive,
and `A_4` has no four-cycle.

The review found no hidden assumption that the radicals themselves have
ordinary `S_n` monodromy.  The proof only needs the radical monodromy to
project onto the root permutation group, allowing independent `m`-th-root
phases in each coordinate.

## 3. Scaling audit

The key equation after continuation is correctly indexed by `sigma^{-1}`.
Raising it to the `m`-th power removes all rootwise phases.  The resulting
vector of scaling powers is projectively invariant under every permutation.

The transposition proof is stronger and clearer than the earlier
representation-language sentence.  A third coordinate exists because
`n=3,4`; it is nonzero; and it is fixed by the transposition.  This forces the
projective scalar to be one and hence forces the swapped coordinates to agree.

Lean checks this argument over an arbitrary field and checks the final common
rescaling over an arbitrary algebraically closed field.  The statement match
to the complex setting is direct.

## 4. Uniform coefficient audit

The master series expansion is formal: for any requested coefficient only
finitely many `k` contribute.  The coefficient of each power `e^k` is treated
separately, so cancellation between different `k` is impossible.

The cubic coefficient formula is the ordinary negative-binomial coefficient.
The quartic formula correctly includes both the negative-binomial choice of
total degree and the binomial choice between `a t^2` and `c t^3`.

All six selected quartic residual coefficients were re-derived.  In
particular:

- residual five contains the factor `2*choose(k+2,2)*a*c`;
- residual six on `a=0` contains `choose(k+2,2)*c^2`;
- residual nine on `a=0` contains `-choose(k+3,3)*c^3`.

The modular tables cover all exponents, with precisely the claimed small
boundaries.  Lean proves the Euclidean-division identities and coefficient
nonvanishing for arbitrary natural `m`; there is no finite upper cutoff.

## 5. Boundary-case audit

The first-power-sum argument intentionally leaves cubic `m=4` and quartic
`m=2,3,5,6,9` on the appropriate loci.  The second elementary-symmetric
derivatives eliminate exactly these cases, except cubic `m=2` and quartic
`m=3,a=0`.

The `m=5` quartic row is sometimes stated too quickly.  Here its dependence on
`e` is handled correctly: identically zero first forces `a=0`, then forces
`c=0`, contradicting the standing `c != 0` condition.

## 6. Formal assurance and its limit

The new Lean source proves the combinatorial and algebraic interfaces, but it
does not encode analytic continuation, polynomial monodromy as a topological
construction, or the finite-pole descent.  Consequently the correct assurance
description is:

> kernel-verified structural algebra conditional on the explicitly stated
> monodromy and coefficient-formula interfaces, with a complete written proof
> of those interfaces in the complex polynomial setting.

It is not a complete formalisation of the all-degree atlas and is not external
peer review.

## 7. Decision

**PASS WITH NOTES.**  The two targeted gaps are no longer reasons to keep the
Newton descent conditional on a finite exponent range.  The overall theorem
remains a candidate until the parent root-span, finite-pole descent, remaining
primitive classification, and extension interfaces receive comparable audit
or formalisation.
