# Source audit for the global all-degree completion

Status: **source identities and theorem scopes checked; imported results not
reproved**  
Date: 2026-08-21

## 1. Purpose

This audit pins the external classification results used by
`ALL_DEGREE_GLOBAL_COMPLETION.md`.  It distinguishes source transcription from
new deduction.  An arXiv identifier or source-archive hash establishes which
bytes were inspected; it does not establish that the imported theorem is true
or that the present application is correct.

## 2. Behajaina--Koenig--Neftin

Source: A. Behajaina, J. Koenig, D. Neftin, *Monodromy groups of polynomials
of composition length 2*, arXiv:2603.27609v2, 31 July 2026,
<https://arxiv.org/html/2603.27609v2>.

This is a current public preprint, not represented here as peer-reviewed.

| Imported result | Exact scope used here | Application |
|---|---|---|
| Theorem 2.3 | outer `AGL_1` polynomial of prime degree, inner `S_4`; except the displayed cubic Ritt collision the block kernel contains `V_4^p` | excludes rank-preserving quartic extensions except `(x^4+ax)^3` |
| Theorem 2.4 | two `S_4` factors; kernel contains `V_4^4` | excludes an `S_4` outer factor |
| Theorem 2.7 | nonsolvable outer factor and inner `S_4`; kernel contains `V_4^{deg g}` | excludes every nonsolvable outer factor |
| Theorem 3.3 | exhaustive indecomposable polynomial monodromy alternatives in characteristic zero | partitions the primitive-factor and quartic-extension audits |
| Theorem 6.1 | chains of odd-prime dihedral factors without adjacent Chebyshev Ritt alignment have a large terminal kernel | contextual cross-check only; the revised Section 7 directly classifies arbitrary rank-preserving Dickson extensions through the finite torus normalizer |

Theorem 3.3 was transcribed as follows: prime cyclic/dihedral groups; the two
degree-four `S_4` types; natural `S_n` and odd-degree natural `A_n`; and the
twelve almost-simple exceptions

`PGL_2(5), PSL_3(2), PGL_2(7), PGammaL_2(8), PGammaL_2(9), PSL_2(11),
M_11, PSL_3(3), PSL_4(2), PGammaL_3(4), M_23, PSL_5(2)`

in degrees `6,7,8,9,10,11,11,13,15,21,23,31`.

The public HTML also states that some exceptional cases rely on Magma checks
and points to an ancillary program.  This package does not relabel those
source computations as a new independent verification.

## 3. Müller list through Burda--Khovanskii

Source: Y. Burda and A. Khovanskii, *Polynomials invertible in k-radicals*,
arXiv:1209.5137v1, <https://arxiv.org/abs/1209.5137>.

The downloaded TeX source theorem labelled `thm:mullerthm` lists natural
`S_n`, odd natural `A_n`, prime affine cyclic/dihedral actions, and the same
exceptional projective and Mathieu actions.  It was used as a second
source-to-list comparison, not as a second proof of Müller's classification.

Downloaded source-archive SHA-256:

`480784bdc15acc8dfe0d31dc37b6d78834e75bb0531ee70f02a1d000d892a7a7`

## 4. Calbetó finite projective subgroup tables

Source: G. G. Calbetó, *On the finite irreducible subgroups of GL_n(C) and
PGL_n(C)*, arXiv:2510.00718v1, 1 October 2025,
<https://arxiv.org/abs/2510.00718>.

The source tables inspected were:

- Table 1: primitive subgroups of `PGL_2(C)` are `A_4`, `S_4`, `A_5`;
- Table 2: primitive subgroups of `PGL_3(C)` are
  `A_5`, `PSL_2(7)`, `A_6`, and the three Hessian groups `H_1,H_2,H_3`.

Downloaded source-archive SHA-256:

`24e8ee90ad6270ca52f2db696a0c7891dc4b99f3d1012ee5936875b9835280e7`

## 5. Exact intersections and stabiliser tests

For projective dimension two, intersecting the primitive `PGL_2` table with
the polynomial-monodromy list leaves formal nonsolvable candidates `S_4` in
degree four and `A_5` in degree five.  Their point stabilisers in the root
actions are `S_3` and `A_4`, neither cyclic, whereas a finite subgroup of
`PGL_2(C)` fixing a point is cyclic.

For projective dimension three, a nonsolvable irreducible candidate cannot be
monomial and hence lies in the primitive `PGL_3` table.  The source-exact
intersection is

`A_5` in degree five and `PSL_3(2) = PSL_2(7)` in degree seven.

The remaining projective-line tests are the exact restriction-character
numerators

`3 + 3(-1) + 8(0) = 0`,

`3 + 9(-1) + 8(0) + 6(1) = 0`, and

`3 + 6 - 3 - 6 = 0`.

They are independently recomputed in both the Lean and SymPy controls.
The character values were cross-checked against the ATLAS representation
pages for `A_5` and `L_2(7)=L_3(2)` and the LMFDB complex character tables:

- <https://brauer.maths.qmul.ac.uk/Atlas/alt/A5/>;
- <https://brauer.maths.qmul.ac.uk/Atlas/lin/L32/>;
- <https://www.lmfdb.org/Groups/Abstract/60.5>;
- <https://www.lmfdb.org/Groups/Abstract/168.42>.

In particular the three-dimensional `PSL_2(7)` character takes values
`3,-1,0,1` on classes of orders `1,2,3,4`, and the ATLAS identifies the
degree-seven point stabiliser as `S_4`.

## 6. Assurance boundary

Closed by this audit: source versions, theorem numbers, hypotheses actually
used, group/degree transcription, table intersection, and the local character
sums.

Not closed by this audit: the proofs of the imported classification theorems,
the correctness of source-side Magma computations, the representation
characters themselves, external specialist review, or novelty.
