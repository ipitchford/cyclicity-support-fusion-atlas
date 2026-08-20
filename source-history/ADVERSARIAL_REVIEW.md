# Internal adversarial review

**Object reviewed:** `MANUSCRIPT.md`, version 0.2.0-candidate  
**Review type:** producer-side mathematical fault search  
**Independence:** none; this is not external specialist review

## Verdict

The direct formal-moment theorem and Fourier block law survive the audit. The
review found one gap in the v0.1 analytic exposition and one false proposed
strengthening during continuation. Both have been corrected before this
bundle was frozen:

1. v0.1 differentiated moving rapid-decay chains without explicitly fixing a
   local trivialisation. Version 0.2 uses fixed sectorial ray contours and an
   explicit nonzero Fourier–Gamma period determinant.
2. A proposed universal additive inequality for Ritt intermediate ranks fails
   in rank four. Version 0.2 claims only the exact Chinese-remainder
   fibre-product constraint and the independently enumerated rank-at-most-three
   table.

No critical contradiction was found after those corrections. The principal
claim boundary remains important: the manuscript classifies fusion for a
supplied polynomial and its actual decompositions; it does not enumerate all
affine low-rank polynomial families.

## Load-bearing checks

### 1. Formal moment transform

For a channel exponent `k=r+nd`, the recurrence gives

```text
k*mu(r,n) + d*mu(r,n+1) = 0.
```

Hence the transform kills

```text
(d/dt + s*d*t^(d-1)) t^k.
```

Under `x=xi(t)` and `P(xi)=t^d`, this is exactly the pullback of
`(d/dx+sP')q`. Pullbacks of polynomial forms have a uniform lower bound on
their `s`-adic coefficient valuations, so the infinite positive-`s` tail is a
well-defined formal series.

### 2. Isomorphism rather than a one-way map

For `0<=j<=d-2`, centring gives

```text
xi(t)^j xi'(t) = t^j + O(t^(j-2)).
```

The moment matrix lies in `Mat_(d-1)(C[[s]])`; its constant term is triangular
with diagonal one. The source and target both have rank `d-1`, so the map is
an isomorphism.

### 3. Seed support and cyclic rank

In channel `r!=0`, the coefficient attached to `a_k t^k` is
`k*mu(r,n)`, which cannot vanish. Distinct terms occupy distinct integral
powers of `s`, so a nonzero support channel cannot cancel internally. The
leading Kummer exponents are distinct modulo integers; their derivative-frame
determinant has a nonzero Vandermonde leading term. Thus the seed rank is
exactly `|Sigma(P)|`.

### 4. Root-span equality

The inverse-root vector is the discrete Fourier transform of the channel
vector. Nonzero channels have disjoint Laurent exponent classes and are
constant-linearly independent. Centring removes the trace channel. Hence the
reduced root-span dimension is also `|Sigma(P)|`.

### 5. Fixed analytic cycles

For a sector of width below `pi`, the chosen fixed rays satisfy

```text
Re(s P(re^(i phi_k))) <= -c r^d + C
```

uniformly on compact subsectors. This justifies all parameter derivatives and
kills twisted-exact boundary terms. After `u=s^(1/d)x`, the lower terms tend to
zero and Young's inequality supplies a uniform integrable majorant. The
limiting period matrix is a nonzero diagonal matrix times a Vandermonde matrix.
Its determinant is nonzero near `s=0`, and the first-order determinant equation
prevents later zeros within the sector.

The exact full-order criterion for a chosen single contour is injectivity of
the induced differential-module map. Version 0.2 does not use an ordinary
Wronskian as a shortcut for this `C(s)`-linear condition.

### 6. Block indexing and Fourier law

For `P=R o Q`, with degrees `d=mn`, one has

```text
Q(x_j) ~ zeta_n^j t^m.
```

Thus a block is `j=a+n*b`. Fourier transformation in `b` isolates exponent
residues modulo `m`. Inside each residue fibre, the block vectors have
coefficient rows from the `n`-point Fourier matrix. Directness across residue
fibres gives the stated rank formula.

### 7. Canonical fusion quotient

Geometric monodromy sends `V(B)` to `V(gB)`. Equality of spans is therefore
invariant under the whole monodromy group, not merely the infinity cycle. The
unions of equality classes form a genuine block system. Standard
intermediate-field correspondence and Lüroth then give a right factor; unique
total ramification at infinity makes it polynomial. The degree formula follows
from the equality stabiliser's cosets.

### 8. Decomposition-chain defects

For suffix degrees `m_(i+1) | m_i`, reduction modulo `m_(i+1)` can only merge
support classes. The projected support cardinalities are monotone and their
successive differences telescope. If the global rank is at most three, no
more than two positive differences can occur above a rank-one suffix, one
above a rank-two suffix and none above a rank-three suffix.

### 9. Ritt diamonds

For a nontrivial coprime-degree move, the pair of residues modulo `ah` and
`bh` determines the residue modulo `abh`. This proves the fibre-product bound.
The rank-at-most-three table follows by enumerating partitions of sets of size
one, two and three whose two intermediate refinements have discrete common
refinement and both refine the bottom partition.

The withdrawn additive inequality fails for

```text
(a,b,h)=(2,3,1), S={0,1,3,4}, ranks=(1,2,2,4).
```

This counterexample is retained in the manuscript and sanity checks.

## Computational controls

The production tests pass. A separate script,
`cleanroom/fraction_audit.py`, imports neither the production module nor a
computer-algebra package. Using exact `Fraction` arithmetic, it passes:

- 9 named phases;
- 12 deterministic random centred phases;
- 4 right-factor projection controls; and
- all 11 low-rank Ritt diamond types.

Its rank calculation is specialised at four rational nonzero values of `s`,
and its inverse expansion is finite. A separate numerical fixed-ray quadrature
checks the signs and convergence of the Fourier--Gamma period matrix for
`P=x^4+x^2+x`. Both are fault controls, not proofs or external reproduction.

## Failure modes explicitly excluded

- Treating every divisor of `deg(P)` as an actual right-factor degree.
- Treating an arbitrary contour as rapid-decay or automatically full-order.
- Calling the inverse-at-infinity Laurent series a dynamical Böttcher
  coordinate.
- Inferring an affine family atlas from the support-fibre classification.
- Claiming the false additive Ritt inequality beyond rank three.
- Treating same-producer clean-room replay as external verification.

## Recommended external checks

1. An irregular-connections specialist should check the fixed-ray rapid-decay
   homology model, the Fourier–Gamma sign conventions and the determinant
   continuation argument.
2. A polynomial-decomposition specialist should check the canonical fusion
   quotient and the wording around nontrivial coprime-degree Ritt neighbours.
3. A second implementation should reproduce the inverse coefficients and
   twisted ranks over `Q(s)` without importing either supplied implementation.
4. A prior-art search should target formal Mellin/Laplace transforms of
   inverse-at-infinity branches, character-support formulae for polynomial root
   spans and monodromy-invariant span quotients.
