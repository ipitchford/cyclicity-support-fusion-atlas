---
title: "Continuation addendum: explicit rapid-decay cycles, canonical fusion quotients, and low-rank Ritt diamonds"
author: "Anonymous"
date: "19 August 2026"
version: "0.2.0-candidate"
---

**Status:** unrefereed theorem candidate and producer-side correction. This
addendum strengthens `MANUSCRIPT.md` version 0.1.0. It does not claim external
specialist review, independent reproduction, formal verification, or settled
novelty and priority.

# 1. Revised position

The direct formal-moment proof and the inverse-support block formula in version
0.1.0 survive line-by-line audit. Three changes are needed.

1. The former rapid-decay paragraph differentiated a family of moving chains
   without first fixing a local topological trivialisation. The conclusion was
   standard, but that proof was incomplete as written. Sections 2–4 below
   replace it with fixed sectorial contours and an explicit non-singular
   Fourier–Gamma period matrix.
2. Equality of block spans has more structure than version 0.1.0 recorded. It
   defines a monodromy-invariant coarsening and therefore an **actual
   polynomial right factor**. Section 5 proves the canonical fusion-quotient
   theorem.
3. At rank at most three, every adjacent Ritt move belongs to one of eleven
   rank diamonds. Section 7 gives the complete table and the exact
   fibre-product constraint behind it.

The resulting claim is exact at the structural level: for a supplied
polynomial and any of its actual decompositions, all fusion ranks, equality
classes, intersections, decomposition-chain defects, and Ritt-move rank
changes are determined by one inverse-support set. An affine coefficient-family
atlas remains a separate inverse-realisability problem.

# 2. Fixed rapid-decay contours on an \(s\)-sector

Let

\[
P(x)=x^d+O(x^{d-2}),\qquad d\ge2,
\]

be monic and centred. Fix \(\theta_0\in\mathbf R\) and
\(0<\varepsilon<\pi/2\), and put

\[
\mathfrak S=
\{s\in\mathbf C^*:|\arg s-\theta_0|<\varepsilon\}.
\]

For \(k\in\mathbf Z/d\mathbf Z\), choose the fixed ray angle

\[
\phi_k=\frac{\pi-\theta_0+2\pi k}{d}.
\tag{2.1}
\]

Let \(\rho_k\) be the ray \(x=re^{i\phi_k}\), \(r\ge0\). Define
\(\Gamma_k\) to run from infinity to the origin along \(\rho_k\), then from
the origin to infinity along \(\rho_{k+1}\).

## Proposition 2.1 — Uniform rapid decay

For every compact subsector \(K\Subset\mathfrak S\), there are constants
\(R,c,C>0\) such that

\[
\Re(sP(re^{i\phi_k}))\le -c r^d+C
\tag{2.2}
\]

for every \(s\in K\), every \(r\ge R\), and every \(k\).

### Proof

By construction,

\[
\Re\bigl(se^{id\phi_k}\bigr)
=-|s|\cos(\arg s-\theta_0).
\]

On a compact subsector this is at most \(-c_0<0\). Since
\(P(x)=x^d+O(x^{d-2})\), the lower-degree terms are bounded by
\(C_1r^{d-2}\), uniformly in the finitely many directions. Enlarging \(R\)
absorbs this error into half of the leading negative term. \(\square\)

It follows that, for every polynomial \(A\),

\[
I_{k,A}(s)=\int_{\Gamma_k}A(x)e^{sP(x)}\,dx
\tag{2.3}
\]

converges absolutely and locally uniformly on \(\mathfrak S\). The contours
are fixed; no chain-velocity term occurs when differentiating.

## Proposition 2.2 — Differentiation and twisted exactness

For every \(j\ge0\),

\[
\partial_s^j I_{k,A}(s)
=
\int_{\Gamma_k}P(x)^jA(x)e^{sP(x)}\,dx.
\tag{2.4}
\]

For every polynomial \(f\),

\[
\int_{\Gamma_k}
(\partial_xf+sP'f)e^{sP(x)}\,dx=0.
\tag{2.5}
\]

### Proof

On compact subsectors, Proposition 2.1 dominates every differentiated
integrand by

\[
C(1+r)^N e^{-cr^d},
\]

which is integrable. Dominated differentiation proves (2.4). Equation (2.5)
comes from

\[
(\partial_xf+sP'f)e^{sP}dx=d(fe^{sP});
\]

the two finite endpoints at the origin cancel and the two ends at infinity
vanish by rapid decay. \(\square\)

# 3. The explicit rapid-decay basis

Radially compactify the affine line. The chosen directions give \(d\) marked
decay points at infinity. Since the compactified disc is contractible,

\[
H_1^{\mathrm{rd}}(\mathbf A^1,e^{sP})
\cong
\widetilde H_0(\{\rho_0,\ldots,\rho_{d-1}\};\mathbf C),
\tag{3.1}
\]

and hence has dimension \(d-1\). Under this identification,

\[
[\Gamma_k]\longmapsto e_{k+1}-e_k.
\]

Therefore

\[
[\Gamma_0],\ldots,[\Gamma_{d-2}]
\tag{3.2}
\]

form a basis, while

\[
\sum_{k=0}^{d-1}[\Gamma_k]=0.
\tag{3.3}
\]

This is an explicit sectorial rapid-decay basis. It is constant over
\(\mathfrak S\), so it gives the required flat local trivialisation directly.

# 4. Fourier–Gamma nondegeneracy

For \(0\le k,j\le d-2\), set

\[
\Pi_{k,j}(s)=
\int_{\Gamma_k}x^j e^{sP(x)}\,dx.
\tag{4.1}
\]

Let \(\zeta_d=e^{2\pi i/d}\). Approach zero on the central ray
\(s=\rho e^{i\theta_0}\), \(\rho\downarrow0\), and choose the corresponding
branch of \(s^{1/d}\). Substitution \(u=s^{1/d}x\) gives

\[
sP(x)=u^d+
\sum_{j=0}^{d-2}p_j s^{1-j/d}u^j.
\tag{4.2}
\]

The lower terms tend to zero. Young's inequality supplies an integrable bound
uniformly for small \(s\), so dominated convergence applies on every scaled
ray contour.

## Theorem 4.1 — Explicit period-matrix asymptotic

Put \(r=j+1\). Then

\[
\boxed{
\lim_{\rho\downarrow0}
 s^{r/d}\Pi_{k,j}(s)
=
\frac{\Gamma(r/d)}{d}
 e^{\pi i r/d}
 (\zeta_d^r-1)\zeta_d^{kr}.
}
\tag{4.3}
\]

Consequently

\[
\det\Pi(s)
=
C_d s^{-(d-1)/2}(1+o(1)),
\qquad C_d\ne0.
\tag{4.4}
\]

### Proof

After scaling, the two rays of \(\Gamma_k\) have angles

\[
\psi_k=\frac{\pi+2\pi k}{d},
\qquad
\psi_{k+1}=\frac{\pi+2\pi(k+1)}{d}.
\]

Along either ray, \(e^{u^d}=e^{-v^d}\), where \(v\) is the radial
coordinate. The integral from the origin to infinity on angle \(\psi\) is

\[
\frac1d\Gamma(r/d)e^{ir\psi}.
\]

The first leg of \(\Gamma_k\) has the opposite orientation, so their
difference is exactly (4.3). The constant matrix is a diagonal matrix with
nonzero entries

\[
\frac{\Gamma(r/d)}d e^{\pi ir/d}(\zeta_d^r-1)
\]

multiplied by

\[
(\zeta_d^{kr})_{
0\le k\le d-2,\ 1\le r\le d-1}.
\]

The latter is a Vandermonde matrix on the distinct numbers
\(\zeta_d,\ldots,\zeta_d^{d-1}\), hence invertible. Finally,

\[
\sum_{r=1}^{d-1}\frac rd=\frac{d-1}{2},
\]

which gives (4.4). \(\square\)

## Corollary 4.2 — Unconditional period realisation

The matrix \(\Pi(s)\) is invertible for every \(s\in\mathfrak S\). Thus the
fixed contour basis separates every class in

\[
\mathcal H_P=
\frac{\mathbf C(s)[x]dx}
{\{(\partial_xf+sP'f)dx\}}.
\]

Every quotient relation gives the corresponding differential relation for all
rapid-decay periods, and no additional relation vanishes against the complete
period system.

### Proof

Equation (4.4) gives invertibility for all sufficiently small \(s\) on the
central ray. Proposition 2.2 makes \(\Pi\) a solution matrix of the first-order
connection on \(\mathcal H_P\). Its determinant therefore satisfies

\[
(\det\Pi)'=\operatorname{tr}(A(s))\det\Pi
\]

on \(\mathfrak S\). A nonzero solution of this scalar equation cannot acquire
a zero. \(\square\)

This proof removes the analytic conditionality without importing stationary
phase or general rapid-decay duality. General duality theorems remain a useful
external consistency check, but they are no longer load-bearing in one
variable.

## Corollary 4.3 — Universal local monodromy

After one anticlockwise turn around \(s=0\), the decay rays rotate by
\(-2\pi/d\), so

\[
[\Gamma_k]\longmapsto[\Gamma_{k-1}].
\tag{4.5}
\]

Together with \(\sum_k[\Gamma_k]=0\), this gives characteristic polynomial

\[
\frac{\lambda^d-1}{\lambda-1}
\]

and eigenvalues \(\zeta_d^{-r}\), \(1\le r\le d-1\), exactly matching the
Kummer channels of the formal moment transform. This computes the sectorial
continuation at \(s=0\). Stokes matrices at \(s=\infty\) are additional
critical-value data, not prerequisites for the rank theorem.

A single contour can still annihilate a nonzero differential submodule of the
fixed-seed cyclic module. Its scalar period has minimal order \(q(P,dx)\) over
\(\mathbf C(s)\) exactly when the induced differential-module map on that
cyclic module has zero kernel, equivalently when no nonzero class in the module
has identically zero period on the chosen contour. This is a concrete
non-annihilation condition, not a convergence assumption.

# 5. Canonical fusion quotients are polynomial factors

Let \(P=R\circ Q\). Let \(\Omega\) be the roots of \(P(X)-z\), and let
\(\mathcal B\) be the block system induced by \(Q\). For
\(B\in\mathcal B\), put

\[
V(B)=\operatorname{span}_{\mathbf C}\{x:x\in B\}.
\]

Define

\[
B\sim B'\quad\Longleftrightarrow\quad V(B)=V(B').
\tag{5.1}
\]

## Theorem 5.1 — Canonical span quotient

The unions of the \(\sim\)-classes form a monodromy-invariant block system.
Hence there is a polynomial factorisation

\[
P=R^{\sharp}\circ Q^{\sharp},
\qquad
Q^{\sharp}=S\circ Q,
\tag{5.2}
\]

unique up to an affine change of the intermediate variable, whose blocks are
exactly those unions. Distinct \(Q^{\sharp}\)-blocks have distinct root spans.

If \(m=\deg Q\), \(n=\deg R\), and \(H_m(P)\) is the equality stabiliser from
version 0.1.0, then

\[
\boxed{
\deg Q^{\sharp}=m|H_m(P)|,
\qquad
\deg R^{\sharp}=\frac n{|H_m(P)|}.
}
\tag{5.3}
\]

### Proof

Let \(G\) be geometric monodromy. For every \(g\in G\),

\[
gV(B)=V(gB).
\]

Therefore equality of spans is preserved by \(G\). The unions of equivalence
classes form a \(G\)-invariant partition of \(\Omega\), hence a block system.
The standard intermediate-field correspondence and Lüroth's theorem produce
a rational right factor; total ramification over infinity makes it polynomial.
Because the new partition coarsens the \(Q\)-partition, the new right factor
has the form \(S\circ Q\).

In the cyclic infinity indexing, equality classes are the cosets of
\(H_m(P)\). Each new block therefore contains \(|H_m(P)|\) old blocks, which
gives (5.3). The definition of the quotient makes the remaining spans
pairwise distinct. \(\square\)

Thus repeated equality of block spans is never merely accidental linear
algebra. It exposes a canonical hidden factor, although full fusion may give
only the trivial right factor \(Q^{\sharp}=P\).

The partial-fusion control \(P=x^8+x^4\), viewed through \(Q=x^2\), has
support \(\{1,5\}\) modulo eight and equality stabiliser
\(\{0,2\}\subset\mathbf Z/4\mathbf Z\). Its four block lines form two equal
pairs, and the theorem recovers the coarser right factor \(Q^{\sharp}=x^4\).

# 6. Fusion defects along a decomposition chain

Let

\[
P=P_1\circ P_2\circ\cdots\circ P_k
\tag{6.1}
\]

be a complete decomposition, and let

\[
Q_i=P_i\circ\cdots\circ P_k,
\qquad m_i=\deg Q_i.
\]

Set

\[
r_i=q(Q_i,dx)=|\pi_{m_i}(\Sigma(P))|.
\tag{6.2}
\]

Since \(m_{i+1}\mid m_i\),

\[
r_1\ge r_2\ge\cdots\ge r_k.
\tag{6.3}
\]

Define the local fusion defect

\[
\delta_i=r_i-r_{i+1}\ge0.
\tag{6.4}
\]

Then

\[
\boxed{
q(P,dx)-q(P_k,dx)
=
\sum_{i=1}^{k-1}\delta_i.
}
\tag{6.5}
\]

A level has \(\delta_i=0\) exactly when the composition
\(Q_i=P_i\circ Q_{i+1}\) has full block fusion.

## Corollary 6.1 — Low-rank chain sparsity

If \(q(P,dx)\le3\), then every complete decomposition has:

- at most two rank-increasing levels above a rightmost power;
- at most one rank-increasing level above a rightmost Chebyshev factor; and
- no rank-increasing level above a rightmost rank-three quartic.

The remaining levels are rank-preserving full-fusion extensions. This reduces
an arbitrarily long decomposition chain to at most two rank-creation events,
although classifying all rank-preserving extensions remains nontrivial.

# 7. Ritt diamonds

Consider an adjacent nontrivial Ritt move above a fixed suffix of degree \(h\).
Let the interchanged coprime degrees be \(a\) and \(b\). The two local chains
have intermediate suffix degrees \(ah\) and \(bh\), while their endpoints have
degrees \(h\) and \(abh\).

For the fixed support \(\Sigma(P)\), write

\[
r_0=|\pi_h\Sigma(P)|,
\quad
r_a=|\pi_{ah}\Sigma(P)|,
\quad
r_b=|\pi_{bh}\Sigma(P)|,
\quad
r_2=|\pi_{abh}\Sigma(P)|.
\tag{7.1}
\]

## Theorem 7.1 — Ritt fibre-product constraint

Let

\[
S=\pi_{abh}\Sigma(P).
\]

For each occupied residue \(c\) modulo \(h\), put

\[
S_c=\{u\in S:u\equiv c\pmod h\},
\quad
A_c=\pi_{ah}(S_c),
\quad
B_c=\pi_{bh}(S_c).
\tag{7.2}
\]

Then the map

\[
S_c\longrightarrow A_c\times B_c,
\qquad
u\longmapsto(\nu\bmod ah,\nu\bmod bh)
\tag{7.3}
\]

is injective. Consequently

\[
\boxed{
|S_c|\le |A_c|\,|B_c|
\quad\text{for every }c,
\qquad
r_2\le\sum_c|A_c|\,|B_c|.
}
\tag{7.4}
\]

### Proof

Two residues in \(S_c\) with the same images modulo \(ah\) and \(bh\) are
congruent modulo \(\operatorname{lcm}(ah,bh)=abh\), because
\(\gcd(a,b)=1\). They are therefore the same element of \(S\). The counting
bounds follow. \(\square\)

A stronger-looking additive inequality need not hold once \(|S|\ge4\). For
example, with \((a,b,h)=(2,3,1)\) and
\(S=\{0,1,3,4\}\), the intermediate ranks are \(2,2\), while the endpoint
ranks are \(1,4\).

## Theorem 7.2 — Complete rank-at-most-three Ritt table

If \(r_2\le3\), the unordered pair \(\{r_a,r_b\}\) is exactly one of the
following eleven possibilities.

| Top rank \(r_2\) | Bottom rank \(r_0\) | Intermediate ranks \(\{r_a,r_b\}\) |
|---:|---:|---:|
| 1 | 1 | \(\{1,1\}\) |
| 2 | 1 | \(\{1,2\}\) |
| 2 | 1 | \(\{2,2\}\) |
| 2 | 2 | \(\{2,2\}\) |
| 3 | 1 | \(\{1,3\}\) |
| 3 | 1 | \(\{2,2\}\) |
| 3 | 1 | \(\{2,3\}\) |
| 3 | 1 | \(\{3,3\}\) |
| 3 | 2 | \(\{2,3\}\) |
| 3 | 2 | \(\{3,3\}\) |
| 3 | 3 | \(\{3,3\}\) |

### Proof

For \(|S|=1\), the claim is immediate. For \(|S|=2\), if the bottom partition
is discrete then both intermediate partitions are discrete. If the bottom has
one block, the two intermediate partitions cannot both have one block because
their common refinement must be discrete.

For \(|S|=3\), a discrete bottom forces both intermediates to be discrete. If
the bottom has two blocks, each intermediate has two or three blocks; they
cannot both have two, because both would then equal the unique two-block
refinement of that bottom partition and their common refinement would still
have two blocks. If the bottom has one block, an intermediate of rank one
forces the other to have rank three; two distinct rank-two partitions may have
discrete common refinement; and all remaining rank-two/rank-three combinations
are allowed. This gives exactly the displayed table. \(\square\)

The table classifies the rank behaviour of every actual low-rank Ritt move.
It does not assert that every combinatorial row is realised by a polynomial
identity; existence of the move remains governed by Ritt's monomial and
Chebyshev forms.

For

\[
(x^4+x)^3=H(x^3),
\]

take \((a,b,h)=(3,4,1)\). The bottom and top ranks are \((1,3)\), while the
two intermediate ranks are \(3\) and \(1\). It is the extremal diamond

\[
\boxed{(r_0;\,r_a\leftrightarrow r_b;\,r_2)
=(1;\,3\leftrightarrow1;\,3).}
\tag{7.5}
\]

# 8. What remains of inverse realisability

The structural problem requested in the parent programme is now reduced to
finite data:

1. \(\Sigma(P)\) gives every block rank by Fourier projection.
2. Equality fusion produces the canonical polynomial quotient of Theorem 5.1.
3. A rank-at-most-three decomposition chain has at most two rank-creating
   levels.
4. Every adjacent move lies in the eleven-row Ritt table.

The unsolved residue is an affine normal-form problem: classify the polynomial
coefficient families that realise the admissible supports and rank-preserving
extensions. The chain-sparsity theorem divides it into three targets.

- **Power suffixes:** classify at most two rank-creating extensions and all
  subsequent full-fusion levels.
- **Chebyshev suffixes:** classify at most one rank-creating extension and the
  rank-preserving Chebyshev/monomial moves around it.
- **Quartic suffixes:** every outer level must preserve rank three, so the whole
  problem is equivariant full-fusion rigidity. The family
  \((x^4+ax)^3+b\) is the first nontrivial orbit, not yet an exhaustive atlas.

This is a substantially smaller frontier than arbitrary block fusion. It is
also the correct stopping boundary: support projections solve the linear
fusion problem, while coefficient-family enumeration requires an additional
polynomial realisability theorem.

# 9. Clean-room computational control

`cleanroom/fraction_audit.py` imports neither the production module nor a
computer-algebra library. It uses exact `Fraction` arithmetic to:

- reduce twisted Krylov columns after specialising \(s\) at four rational
  values;
- expand the inverse at infinity through \(8d\) coefficients;
- compare sampled cyclic rank with observed support on nine named controls
  and twelve deterministic random phases;
- verify right-factor support projection on four compositions; and
- enumerate exactly the eleven low-rank Ritt diamonds while checking the
  fibre-product bound (7.4).

The run passes. Its limitations are explicit: specialisation is an independent
fault control rather than a symbolic proof over \(\mathbf Q(s)\); finite
inverse expansion does not prove support exhaustiveness; and producer-side
replay is not external reproduction.

# References

Hien, M. (2009). Periods for flat algebraic connections. *Inventiones
Mathematicae, 178*, 1–22. https://doi.org/10.1007/s00222-009-0185-7

Müller, P., & Zieve, M. E. (2008). *On Ritt's polynomial decomposition
theorems*. arXiv. https://arxiv.org/abs/0807.3578

Ritt, J. F. (1922). Prime and composite polynomials. *Transactions of the
American Mathematical Society, 23*(1), 51–66.
https://doi.org/10.1090/S0002-9947-1922-1501189-9
