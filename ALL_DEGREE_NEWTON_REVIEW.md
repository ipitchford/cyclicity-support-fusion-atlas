# Internal adversarial review: Newton descent and all-degree boundary

Review date: 2026-08-21  
Decision: **PASS WITH NOTES as a candidate repair of the identified gap**

This is producer-side review. It is not external mathematical refereeing.

## 1. Exact repaired step

The withdrawn draft inferred a scalar-power identity from a product of
twisted quartic factors. The new argument does not make that inference. It
uses only necessary constancy of the first elementary symmetric functions of
the powered radicals, then classifies that constancy by Newton sums.

## 2. Scaling lemma

The trace-normalising coefficients could initially have different `m`-th
powers. Uniqueness of the relation makes their `m`-th-power vector span a
one-dimensional submodule of the natural root-permutation module. After the
power/imprimitive cases are removed, the relevant groups are `S_3` and `S_4`;
their natural permutation modules have only the constant one-dimensional
submodule. Thus the powers are equal and one common rescaling gives
`v_i^m=y_i-b`.

This step is load-bearing and should be checked by a polynomial-monodromy
specialist.

## 3. Constancy of lower coefficients

Monodromy acts on the trace-normalised radicals by a common `m`-th root of
unity and a permutation. Hence `e_k(v)^m` is rational in the target. It has no
finite poles and pole order `k/n<1` at infinity for `k<n`, so it is constant.
The last symmetric function has order one and is affine. This supplies the
one-parameter cubic or quartic used by the Newton calculation.

## 4. Uniform Newton obstruction

Differentiating

`p_r=-r[t^r] log(B(t)+e*t^n)`

reduces the all-`m` question to coefficients of negative powers of a two- or
three-term series. Inspecting the largest power of `e`, and at most the two
preceding powers, leaves only a finite boundary list. `E_2` eliminates every
boundary except cubic `m=2` and quartic `m=3,a=0`.

The residue argument is genuinely uniform; the bounded CAS sweep is not used
to extrapolate it.

## 5. Independent-path finding

A direct-resultant implementation reproduced all cubic and quartic loci
through `m=12`. It caught a sign error in the first draft of the quartic
resultant: the exact polynomial is `Y(Y+c)^3+e^3`. The note was corrected
before its manifest was frozen. The sign does not alter the affine family.

## 6. Residual obligations

The repaired lift step does not independently reprove:

1. the parent support/root-span identity;
2. the imported classification of low-dimensional primitive polynomial
   monodromy;
3. the canonical-fusion and rank-preserving-extension theorems; or
4. the analytic period interpretation.

These dependencies have internal evidence but no external specialist sign-off.

## 7. Decision

The Newton descent is a coherent non-circular replacement for the exact gap
recorded in Conjecture 13.2. Relative to the inherited lemmas, it closes the
remaining cubic/quartic lift classification and therefore supports an
all-degree rank-at-most-three theorem candidate.

**Do not silently rewrite the published-parent bytes or call the all-degree
theorem externally established. Prepare it as an additive successor for
specialist review.**

