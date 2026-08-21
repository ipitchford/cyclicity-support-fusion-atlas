# Uniform completion of the Dickson extension branch

**Date:** 21 August 2026  
**Status:** written all-degree candidate proof; fresh internal re-audit required

## Statement

Let `Q=D_m(x,a)` with `a!=0` and `m>=3`.  If

\[
P=R\circ Q,\qquad q(P)=q(Q)=2,
\]

then, up to affine target changes,

\[
P=D_{mn}(x,a),\qquad R=D_n(y,a^m),
\]

where `n=deg R`.  This holds for arbitrary `n` and does not assume that a
chosen complete decomposition has uniformly aligned adjacent factors.

## Proof

Uniformise a generic `Q`-fibre by

\[
x=U+a/U,qquad D_m(x,a)=U^m+a^m/U^m.
\]

Its root span is `<U,U^{-1}>`.  A second block has a uniformizer `V`; equality
of its span with the first gives

\[
V=\alpha U+\beta U^{-1},\qquad
V^{-1}=\gamma U+\delta U^{-1}.
\]

Expanding `VV^{-1}=1` and using the transcendence of `U` gives
`alpha gamma=beta delta=0`.  Invertibility leaves exactly
`V=cU` or `V=cU^{-1}`.

Let `M` be the splitting field of `P(X)-t`.  If the reference-block roots are

\[
x_j=\zeta_m^jU+a\zeta_m^{-j}U^{-1}\qquad(0\le j<m),
\]

then, because `m>=3`, the two Fourier projections are

\[
U=\frac1m\sum_{j=0}^{m-1}\zeta_m^{-j}x_j,
\qquad
\frac aU=\frac1m\sum_{j=0}^{m-1}\zeta_m^jx_j.
\]

Thus the reference block recovers `U` and `a/U`, so `C(U)<=M`.  The preceding
calculation applied to every block puts every inverse root in `C(U)`, hence
`M=C(U)`.

The finite Galois group `Gamma=Gal(C(U)/C(t))` acts by `U->cU` or `U->c/U`.
It contains the block group

\[
D_m=\langle U\mapsto\zeta_mU,\ U\mapsto a/U\rangle.
\]

Its rotational subgroup is a finite subgroup of `C^*`, hence `mu_N`.  Since
the reflection `U->a/U` is already present, `|Gamma|=2N`.  But

\[
|\Gamma|=[C(U):C(t)]=2\deg P=2m\deg R=2mn,
\]

so `N=mn` and `Gamma=D_N`.  Therefore

\[
C(t)=C(U)^\Gamma
=C(U^N+a^N/U^N)
=C(D_N(x,a)).
\]

The polynomial generators `P(x)` and `D_N(x,a)` differ by a Mobius
transformation.  Their unique pole at infinity forces its denominator to be
constant, so it is affine.  Finally the Dickson identity

\[
D_{mn}(x,a)=D_n(D_m(x,a),a^m)
\]

identifies the composite.  More explicitly, if `P=A circ D_{mn}` for an
affine `A`, then

\[
R\circ D_m=A\circ D_n\circ D_m.
\]

The substitution homomorphism `C[Y] -> C[x]`, `F -> F(D_m(x,a))`, is
injective because `D_m(x,a)` is nonconstant.  Hence
`R=A circ D_n`, with Dickson parameter `a^m`.  This proves the statement.

## Why this closes mixed chains

The proof starts with the full outer polynomial `R`, not a selected adjacent
pair in a complete decomposition.  Consequently it is insensitive to mixed
aligned/nonaligned presentations, repeated prime degrees, quadratic overlaps,
or the order of Ritt moves.  Every rank-preserving presentation has the same
global dihedral invariant field and is therefore an aligned Dickson extension.

## Assurance boundary

This is a uniform function-field argument, not an inference from the bounded
Dickson regression grid.  It imports standard facts about automorphisms of
`C(U)`, finite subgroups of `C^*`, and invariant fields of dihedral actions.
Those facts and the field-containment step are not formalized in Lean here.
