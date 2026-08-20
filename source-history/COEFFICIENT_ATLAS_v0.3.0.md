# Affine coefficient families for inverse-root rank at most three

## Exact realisability and rank-preserving polynomial extensions

**Version:** 0.3.0-candidate  
**Date:** 19 August 2026  
**Status:** theorem candidate, internally checked but not externally refereed  
**Dependency:** the unconditional support/root-span theorem in
`cyclicity-unconditional-fusion-v0.2.0-candidate/MANUSCRIPT.md`

## Abstract

Let \(P\in\mathbf C[x]\) have degree \(d\ge2\), let \(q(P)\) be the
fixed-seed cyclic rank of \([dx]\), and let \(\Sigma(P)\) be the residue
support of its normalised inverse at infinity.  The preceding candidate proves

\[
q(P)=|\Sigma(P)|=\dim_{\mathbf C}W_P^{\rm red}.
\]

This note closes the remaining affine realisability problem for
\(q(P)\le3\), relative to that theorem and to the standard classifications of
primitive polynomial monodromy, finite subgroups of
\({\rm PGL}_2(\mathbf C)\) and \({\rm PGL}_3(\mathbf C)\), and Ritt
polynomial decomposition.

Up to invertible affine changes of source and target, the exact list is:

\[
\begin{array}{c|l}
q&\text{normal forms}\\ \hline
1&x^d,\\[2mm]
2&D_d(x,a)\ (a\ne0),\quad x^{2m}+A x^m\ (m\ge2,\ A\ne0),\\[2mm]
3&x^{3m}+A x^{2m}+B x^m\ (m\ge2),\\
 &x^4+A x^2+B x\ (B\ne0),\\
 &(x^4+a x)^3\ (a\ne0),
\end{array}
\]

with the lower-rank subloci stated precisely below.  Here \(D_d(x,a)\) is
the Dickson polynomial, defined by

\[
D_d\!\left(u+\frac au,a\right)=u^d+\left(\frac au\right)^d.
\]

The only proper rank-preserving extensions are:

1. power chains;
2. aligned Dickson chains;
3. \((x^{3m}+b x^m)^2\), with \(m\ge2\) and \(b\ne0\); and
4. \((x^4+a x)^3\), with \(a\ne0\).

The third item corrects the earlier provisional claim that the quartic cubic
collision was the only nontrivial rank-three extension.

# 1. Normalisation and claim boundary

Two polynomials are **affine-equivalent** when

\[
P=\ell_1\circ Q\circ\ell_2
\]

for invertible affine maps \(\ell_1,\ell_2\).  We use monic centred normal
forms and suppress an additive target constant.  Thus a displayed polynomial
represents its whole affine orbit.

The proof below imports three standard classifications.

1. Müller’s classification of primitive polynomial monodromy groups containing
   a full cycle.
2. The classical finite-subgroup classifications for
   \({\rm PGL}_2(\mathbf C)\) and primitive finite subgroups of
   \({\rm PGL}_3(\mathbf C)\).
3. Ritt’s first and second polynomial-decomposition theorems.

Everything else is proved here.  Novelty and priority are not claimed.  The
support/root-span identity on which this note rests is itself a candidate
result pending specialist review.

# 2. Main coefficient atlas

## Theorem 2.1 — Exact affine classification for \(q\le3\)

Let \(P\in\mathbf C[x]\), \(\deg P=d\ge2\).

### Rank one

\[
q(P)=1
\quad\Longleftrightarrow\quad
P\sim x^d.
\tag{2.1}
\]

### Rank two

\(q(P)=2\) if and only if \(P\) is affine-equivalent to one of:

\[
D_d(x,a),\qquad a\ne0,\quad d\ge3,
\tag{2.2}
\]

or

\[
x^{2m}+A x^m,
\qquad m\ge2,\quad A\ne0.
\tag{2.3}
\]

The two families meet in degree four.  Formula (2.3) is the target-translated
form of \((x^m+b)^2\), with \(b\ne0\).

### Rank three

\(q(P)=3\) if and only if \(P\) is affine-equivalent to one of the following
exact-rank members.

#### Cubic over a power

\[
P=x^{3m}+A x^{2m}+B x^m,
\qquad m\ge2.
\tag{2.4}
\]

Its lower-rank loci are exactly:

\[
A=B=0 \quad(q=1),
\tag{2.5}
\]

and

\[
m=2,
\qquad B=\frac{A^2}{4},
\qquad A\ne0
\quad(q=2).
\tag{2.6}
\]

Every other member of (2.4) has rank three.

#### Quartics

\[
P=x^4+A x^2+B x,
\qquad B\ne0.
\tag{2.7}
\]

When \(B=0\), the rank is two for \(A\ne0\) and one for \(A=0\).

#### The exceptional Ritt collision

\[
P=(x^4+a x)^3,
\qquad a\ne0.
\tag{2.8}
\]

These three rank-three families are mutually distinct, except for ordinary
affine reparametrisations within a family.

# 3. The realised support sets

Fix the infinity generator for which the leading inverse term has character
\(1\).  Up to multiplication of all labels by a unit modulo \(d\), the exact
supports are:

| Rank | Degree | Coefficient family | \(\Sigma(P)\) |
|---:|---:|---|---|
| 1 | \(d\) | power | \(\{1\}\) |
| 2 | \(d\) | Dickson | \(\{1,d-1\}\) |
| 2 | \(2m\) | quadratic over a power | \(\{1,m+1\}\) |
| 3 | \(3m\) | cubic over a power | \(\{1,m+1,2m+1\}\) |
| 3 | 4 | quartic | \(\{1,2,3\}\) |
| 3 | 12 | exceptional collision | \(\{1,7,10\}\) |

For the power-composite families, the support statement follows immediately
from the deck symmetry.  If \(P=H(x^m)\), then

\[
P(\zeta_m x)=P(x),
\]

so the normalised inverse contains only exponents congruent to \(1\bmod m\).
There are two or three available residue classes according as
\(\deg H=2\) or \(3\); exact rank forces all of them to occur.

For Dickson polynomials, write

\[
x=U+\frac aU,
\qquad
D_d(x,a)=U^d+\left(\frac aU\right)^d.
\]

The branch \(U\sim t\) has exponents congruent to \(1\bmod d\), while
\(a/U\) has exponents congruent to \(-1\bmod d\).

For (2.8), direct inversion begins

\[
\xi(t)=t-\frac a4t^{-2}-\frac{a^2}{32}t^{-5}
       +0\,t^{-8}+\cdots.
\tag{3.1}
\]

The three observed residues are \(1,10,7\bmod12\); rank three excludes a
fourth channel.

# 4. A stable line forces a power

The next lemma is the principal structural simplification.

## Lemma 4.1 — One-dimensional submodule lemma

If the reduced root-span representation \(W_P\) contains a nonzero
monodromy-stable line, then \(P\) is affine-equivalent to a power.

### Proof

Let \(G\) be the geometric monodromy group and let \(L=\mathbf C f\subseteq
W_P\) carry the character \(\chi\).  At a chosen point above infinity, the
normalised inverse has one pole channel, namely the leading character
\(1\); every other residue channel is regular there.  If \(f\) belonged to a
non-leading channel, stability of \(L\) would make it regular at every point
above infinity.  Roots are integral over \(\mathbf C[z]\), so \(f\) has no
finite poles either.  It would therefore be constant.  The reduced span has no
trivial infinity channel, so this is impossible.  Hence

\[
\chi(\tau)=\zeta_d,
\]

where \(\tau\) is the full \(d\)-cycle at infinity.

Let \(H\) be the stabiliser of one root.  The chosen root has a nonzero
projection to \(L\).  Since \(H\) fixes that root, it fixes its projection, so
\(H\subseteq\ker\chi\).  Now

\[
[G:H]=d,
\qquad
|\chi(G)|\ge d.
\]

The inclusion gives \(|\chi(G)|\le d\), hence equality and
\(H=\ker\chi\).  Thus \(H\) is normal.  The root action is faithful, so the
core of \(H\) is trivial; consequently \(H=1\), \(G\simeq C_d\), and the
polynomial is affine-equivalent to \(x^d\). \(\square\)

## Corollary 4.2 — Low non-power spans are irreducible

A non-power root-span representation of dimension two or three is irreducible.
Indeed, every reducible complex representation of either dimension has a
stable line.

# 5. Rank cannot grow from two to three

## Lemma 5.1 — Exclusion of the \([2,1]\) profile

There is no decomposition

\[
P=R\circ Q
\]

with

\[
q(Q)=2,
\qquad q(P)=3.
\tag{5.1}
\]

### Proof

The support-fibre profile would have to be \([2,1]\).  In the Fourier block
notation of the preceding manuscript, every \(Q\)-block plane then has the
form

\[
V_a=L\oplus\ell_a,
\]

where the singleton support fibre supplies the same nonzero line \(L\) in
every block.  Geometric monodromy permutes the block planes, so

\[
0\ne L\subseteq\bigcap_aV_a
\]

is globally stable.  Lemma 4.1 would make \(P\) a power, contrary to
\(q(P)=3\). \(\square\)

Thus a rank-three phase built above a power must jump directly from rank one to
rank three.  It cannot pass through rank two.

# 6. The first rank-increasing factor

Take a complete decomposition and choose the maximal suffix of rank one.
After affine normalisation it is

\[
Q_0=x^m+b.
\tag{6.1}
\]

Let \(A\) be the next indecomposable outer factor and put

\[
P_0=A\circ Q_0.
\]

Let \(y_1,\ldots,y_n\) be the roots of \(A(Y)-z\), and choose
\(u_i^m=y_i-b\).  The roots in the \(i\)-th block are the scalar multiples
\(\zeta_m^ju_i\), so that block spans the line

\[
\ell_i=\mathbf C u_i.
\tag{6.2}
\]

Maximality of the rank-one suffix implies that the \(\ell_i\) are distinct;
otherwise the canonical fusion quotient would give a larger rank-one suffix.
The primitive monodromy of \(A\) acts faithfully on these lines.

## Lemma 6.1 — Low-dimensional primitive audit

If \(\dim\langle u_i\rangle\le3\), the indecomposable factor \(A\) is one of:

1. a prime-degree power;
2. a prime-degree Dickson/Chebyshev polynomial; or
3. a quartic.

The nonsolvable exceptional groups in Müller’s primitive list do not occur.

### Proof

For a two-dimensional span, the pointwise projective stabiliser of at least
three distinct points of \(\mathbf P^1\) is trivial.  Thus the primitive
monodromy of \(A\) embeds in \({\rm PGL}_2(\mathbf C)\).  Intersecting the
finite-subgroup list for \({\rm PGL}_2\) with Müller’s polynomial list leaves
cyclic and dihedral groups, together with the formal candidates \(S_4\) and
\(A_5\).  Their point stabilisers in degrees four and five are respectively
\(S_3\) and \(A_4\).  A finite subgroup of \({\rm PGL}_2\) fixing a point is
cyclic, so neither candidate can stabilise a block line.

For a three-dimensional span, let \(K\) be the subgroup fixing every block
line projectively.  If \(K\) is non-scalar, its simultaneous eigenspaces form
three one-dimensional imprimitivity spaces.  The primitive block quotient then
maps into \(S_3\), and is solvable.  Hence any nonsolvable candidate embeds in
\({\rm PGL}_3(\mathbf C)\).

The intersection of Müller’s list with the classical primitive
\({\rm PGL}_3\)-list leaves only two candidates that have the required
permutation degree: \(A_5\) in degree five and
\({\rm PSL}_3(2)\simeq{\rm PSL}_2(7)\) in degree seven.  Their point
stabilisers are \(A_4\) and \(S_4\).

For the three-dimensional icosahedral representation,

\[
\dim V^{A_4}
=\frac{3+3(-1)+8(0)}{12}=0,
\]

and the same calculation excludes the two nontrivial one-dimensional
characters of \(A_4\), because the character is zero on the eight
three-cycles.  Thus \(A_4\) fixes no projective point.

For the Klein three-dimensional representation, restriction to the point
stabiliser \(S_4\) has character values \(3,-1,0,1\) on the identity,
order-two, order-three and order-four classes.  Hence

\[
\frac{3+9(-1)+8(0)+6(1)}{24}=0,
\]

and multiplication by the sign character also gives zero.  Thus \(S_4\)
fixes no projective point.  Both exceptional candidates are excluded.

The remaining solvable primitive polynomial groups are the cyclic and
dihedral families and the degree-four case. \(\square\)

# 7. Solving the three primitive lift cases

## 7.1 Outer power

Let \(A(Y)=Y^p\), with \(p\) prime.  For \(b\ne0\),

\[
P=(x^m+b)^p,
\qquad
\xi(t)=t(1-bt^{-m})^{1/m}.
\tag{7.1}
\]

Every binomial coefficient is nonzero.  Modulo \(mp\), the exponents occupy
all \(p\) classes

\[
1,1-m,\ldots,1-(p-1)m.
\]

Therefore

\[
q(P)=p.
\tag{7.2}
\]

Low rank permits only \(p=2\) or \(p=3\), giving the quadratic- and
cubic-over-power families.  The case \(b=0\) is a power.

## 7.2 Outer Dickson factor

Let \(A=D_p(Y,a)\), where \(p\) is an odd prime.  Its roots can be written

\[
y_j=\zeta_p^jU+a\zeta_p^{-j}U^{-1}.
\tag{7.3}
\]

Suppose the \(m\)-th radicals of \(y_j-b\) span a plane.  The projective
\(D_p\)-orbit is a regular \(p\)-gon.  After choosing homogeneous
representatives,

\[
v_j=\rho^j(V+\zeta_p^{kj}W)
\]

for some unit \(k\bmod p\).  The Fourier residues occurring in \(v_j^m\)
are an affine translate of

\[
\{0,k,2k,\ldots,mk\}\pmod p.
\tag{7.4}
\]

No Fourier component can cancel: after factoring a power of \(W\), each is a
nonzero polynomial in the nonconstant function \(V/W\).  Thus the number of
residues is

\[
\min(p,m+1).
\tag{7.5}
\]

The right side of \(v_j^m=y_j-b\) has only the residues \(0,1,-1\).
For \(p\ge5\), (7.5) forces \(m=2\).  Coefficient comparison then gives the
half-angle Dickson identity

\[
D_p(D_2(x,c),c^2)=D_{2p}(x,c),
\tag{7.6}
\]

up to affine scaling.  The resulting rank is two.

For \(p=3\), three block lines can span either a plane or a three-space.  The
three-space case is precisely a cubic over a power.  In the plane case, choose
radicals \(v_1,v_2,v_3\) with

\[
v_1+v_2+v_3=0,
\qquad
v_i^m=y_i-b.
\tag{7.7}
\]

The uniqueness of the relation makes monodromy act by a common scalar followed
by a permutation.  Hence \(e_2(v)^m\) is rational in \(z\).  It has no finite
poles and pole order \(2/3<1\) at infinity, so \(e_2(v)\) is constant.  Put

\[
Q_0(x)=x^3+e_2(v)x.
\]

The product \(e_3(v)^m\) is affine in \(z\), and comparison of the two sets of
roots gives, after affine rescaling,

\[
A(x^m+b)-A(b)=Q_0(x)^m.
\tag{7.8}
\]

The left side is a polynomial in \(x^m\).  If \(e_2(v)\ne0\), the term
\(x^{3m-2}\) occurs on the right with nonzero coefficient.  Therefore
\(m\mid2\), and \(m=2\).  This is again (7.6), now with \(p=3\).  If
\(e_2(v)=0\), the phase is a power and no rank increase occurs.

Thus an outer Dickson factor creates rank three only in degree three; it creates
rank two in the aligned quadratic half-angle case.

## 7.3 Outer quartic

Let \(A\) be an indecomposable quartic and suppose

\[
q(A(x^m+b))=3.
\tag{7.9}
\]

The four radical lines form a projective tetrahedron.  Scale their generators
so that

\[
v_1+v_2+v_3+v_4=0,
\qquad
v_i^m=y_i-b.
\tag{7.10}
\]

Every projective automorphism of a tetrahedron is a permutation of its
vertices.  Uniqueness of (7.10) therefore makes monodromy act by a common
scalar followed by a permutation.  For \(k=2,3\), the function
\(e_k(v)^m\) is monodromy-invariant, has no finite pole, and has pole order
\(k/4<1\) at infinity.  Hence \(e_2(v)\) and \(e_3(v)\) are constants.

Set

\[
Q_0(x)=x^4+e_2(v)x^2-e_3(v)x.
\tag{7.11}
\]

As in the cubic argument, \(e_4(v)^m\) is affine in \(z\), and comparison of
roots yields

\[
A(x^m+b)-A(b)=Q_0(x)^m
\tag{7.12}
\]

up to a nonzero target scaling.  Indecomposability forces \(e_3(v)\ne0\).
The term \(x^{4m-3}\) on the right is therefore nonzero, while every exponent
on the left is divisible by \(m\).  Hence \(m\mid3\), so \(m=3\).
The term \(x^{10}\) in \(Q_0(x)^3\) then forces \(e_2(v)=0\).  Consequently

\[
Q_0=x^4+a x,
\qquad
A(y)=y(y+a)^3
\]

up to affine changes, and

\[
A(x^3)=(x^4+a x)^3.
\tag{7.13}
\]

This is the unique quartic lift.  The case \(m=1\) gives the ordinary quartic
family itself.

# 8. Proof of the coefficient atlas

Take a complete decomposition of \(P\) and read ranks from the right.

* Rank-one suffixes compose to one affine power.
* Lemma 5.1 forbids a rank-two-to-rank-three step.
* Lemma 6.1 and Section 7 classify the first rank increase above a power.

For rank two, the first increase gives either a quadratic over a power or a
Dickson phase.  Section 10 below shows that only Dickson phases admit further
rank-two-preserving extensions, and those extensions stay Dickson.

For rank three, the first increase gives a cubic over a power, an
indecomposable quartic, or the quartic lift (7.13).  Section 11 shows that a
cubic-over-power phase admits at most one aligned square extension, while an
equivariant quartic admits exactly the cubic extension (7.13).  Neither result
can be extended again.  This proves the exhaustiveness in Theorem 2.1.

The lower-rank loci follow from the rank-one and rank-two classifications.  In
(2.4), the only rank-one point is \(A=B=0\).  A rank-two member must be
Dickson or quadratic-over-power.  Comparing the deck group and degrees leaves
only \(m=2\), where

\[
x^6+A x^4+\frac{A^2}{4}x^2
\]

is a target translate and scaling of \(D_6\).  For quartics, \(B=0\) gives

\[
x^4+A x^2
=\left(x^2+\frac A2\right)^2-\frac{A^2}{4}.
\]

# 9. Complete theorem on rank-preserving extensions

## Theorem 9.1 — Rank-preserving extension atlas

Let

\[
P=R\circ Q,
\qquad \deg R>1,
\qquad q(P)=q(Q)\le3.
\tag{9.1}
\]

Up to affine changes, exactly one of the following occurs.

### Rank one: powers

\[
Q=x^m,
\qquad
P=x^{mn},
\qquad
R=y^n.
\tag{9.2}
\]

### Rank two: Dickson chains

\[
Q=D_m(x,a),
\qquad
P=D_{mn}(x,a),
\qquad
R=D_n(y,a^m),
\tag{9.3}
\]

with \(m\ge3\).  This uses

\[
D_{mn}(x,a)=D_n(D_m(x,a),a^m).
\tag{9.4}
\]

No exact quadratic-over-power phase has a proper rank-two right factor, except
for the degree-four overlap already represented by Dickson polynomials.

### Rank three: aligned square

\[
Q=x^{3m}+b x^m,
\qquad
P=Q^2,
\qquad m\ge2,
\qquad b\ne0.
\tag{9.5}
\]

Equivalently, a cubic-over-power normal form

\[
P=x^{3M}+A x^{2M}+B x^M
\tag{9.6}
\]

has a proper rank-three right factor exactly when

\[
M\ \text{is even},
\qquad
M\ge4,
\qquad
B=\frac{A^2}{4},
\qquad
A\ne0.
\tag{9.7}
\]

The right factor is

\[
Q=x^{3M/2}+\frac A2x^{M/2}.
\tag{9.8}
\]

### Rank three: quartic cubic collision

\[
Q=x^4+a x,
\qquad
P=Q^3,
\qquad a\ne0.
\tag{9.9}
\]

There are no other rank-preserving extensions.

# 10. Why rank two has only Dickson extensions

## 10.1 Dickson block planes

For a fibre of \(D_m(x,a)\), choose \(U\) so that its roots span

\[
\langle U,U^{-1}\rangle.
\]

If another fibre has the same plane and parameter \(V\), then both \(V\) and
\(V^{-1}\) lie in this span.  Write

\[
V=\alpha U+\beta U^{-1},
\qquad
V^{-1}=\gamma U+\delta U^{-1}.
\]

Multiplying and using the nonconstancy of \(U\) gives

\[
\alpha\gamma=0,
\qquad
\beta\delta=0.
\]

Thus

\[
V=cU
\quad\text{or}\quad
V=cU^{-1}.
\tag{10.1}
\]

A finite outer orbit is therefore a cyclic multiplicative orbit together with
inversion.  Its orbit polynomial is Dickson, and (9.4) follows.  This proves
that every rank-two-preserving extension of a Dickson phase is aligned
Dickson.

## 10.2 Quadratic over a power

For

\[
Q=(x^m+b)^2,
\]

a fibre block plane has generators \(U,V\) satisfying

\[
U^m+V^m=-2b.
\tag{10.2}
\]

For \(m\ge3\), every linear automorphism of the binary Fermat form
\(U^m+V^m\) is monomial: it scales the two coordinates and may swap them.
Preservation of the nonzero level in (10.2) forces the \(m\)-th powers of the
scalars to be one.  The corresponding fibre parameter can only remain fixed
or change sign before being squared, so no distinct fibre with the same block
plane is produced.  Hence no proper full-fusion extension exists.

When \(m=2\), the phase is the degree-four Dickson overlap and is covered by
Section 10.1.

# 11. Why rank three has exactly two extension mechanisms

## 11.1 Cubic over a power

Write

\[
Q=H(x^m),
\qquad
H(Y)=Y^3+A Y^2+B Y+C,
\qquad m\ge2,
\tag{11.1}
\]

and suppose another \(Q\)-fibre has the same three-space.  The roots in a
fibre lie on three intrinsic Kummer lines.  A block transport must therefore
be monomial:

\[
U_i' = c_iU_{\pi(i)}.
\tag{11.2}
\]

Put \(a_i=c_i^m\).  The triples \(U_i^m\) and \((U_i')^m\) have the same
fixed first and second elementary symmetric functions.  The only
constant-linear relation among generic cubic roots is their trace relation;
the translated-power cubic is checked directly and gives the same conclusion.
Therefore

\[
a_1=a_2=a_3=c.
\tag{11.3}
\]

The fixed coefficients give

\[
c(-A)=-A,
\qquad
c^2B=B.
\tag{11.4}
\]

For exact rank three, \((A,B)\ne(0,0)\).  A nontrivial value of \(c\) is
possible exactly when

\[
A=0,
\qquad B\ne0,
\qquad c=-1.
\tag{11.5}
\]

After removing the target constant,

\[
H(-Y)=-H(Y).
\]

Thus the complete fibre-equivalence group is the involution \(y\mapsto-y\),
and the only nontrivial outer quotient is \(R(y)=y^2\).  This gives (9.5).

The square cannot be repeated.  Rewriting it as a cubic over the power
\(x^{2m}\) gives the outer cubic

\[
Y(Y+b)^2=Y^3+2bY^2+b^2Y,
\]

whose quadratic coefficient is nonzero; condition (11.5) no longer holds.

## 11.2 Quartic blocks

Let

\[
Q=x^4+A x^2+B x,
\qquad B\ne0.
\tag{11.6}
\]

The four roots in a fibre form a projective tetrahedron with the unique trace
relation.  Equality of two block three-spaces therefore sends the roots by

\[
x_i' = c x_{\pi(i)}.
\tag{11.7}
\]

The fixed quadratic and cubic elementary symmetric functions give

\[
c^2A=A,
\qquad
c^3B=B.
\tag{11.8}
\]

Since \(B\ne0\), a nontrivial solution exists exactly when

\[
A=0,
\qquad c^3=1.
\]

Then

\[
Q(cx)=cQ(x),
\]

and the fibre-equivalence group is \(\mu_3\).  Its quotient polynomial is
\(R(y)=y^3\), proving (9.9).

After cubing, the quartic monodromy \(S_4\) remains a normal subgroup in its
standard three-dimensional representation.  Its linear normaliser is
\(\mathbf C^\times S_4\).  A scalar preserving the resulting phase
\((x^4+B x)^3\) changes no fibre: \(c^3=1\) is already a deck symmetry.
Hence no further rank-three extension exists.

# 12. Support projection under the preserving extensions

The support maps make the two rank-three mechanisms transparent.

### Aligned square

For

\[
Q=x^{3m}+b x^m,
\]

\[
\Sigma(Q)=\{1,m+1,2m+1\}\pmod{3m}.
\]

For \(P=Q^2\), viewed as a cubic over \(x^{2m}\),

\[
\Sigma(P)=\{1,2m+1,4m+1\}\pmod{6m}.
\]

Reduction modulo \(3m\) is bijective onto \(\Sigma(Q)\).

### Quartic cubic collision

\[
\Sigma((x^4+a x)^3)=\{1,7,10\}\pmod{12},
\]

and reduction modulo four gives

\[
\{1,3,2\}=\Sigma(x^4+a x).
\]

Thus both extensions satisfy the full-fusion injectivity criterion exactly.

# 13. Affine moduli

The normal forms retain parameters to display the coefficient strata, although
some can be scaled away over \(\mathbf C\).

* All nonzero parameters in the quadratic-over-power family represent one
  affine orbit for each \(m\).
* All \(D_d(x,a)\) with \(a\ne0\) are affine-equivalent to a Chebyshev
  normalisation.
* In the cubic-over-power family, source scaling sends
  \((A,B)\mapsto(A\lambda^{-m},B\lambda^{-2m})\); when \(A\ne0\), the ratio
  \(B/A^2\) is an affine modulus.
* In the quartic family, source scaling sends
  \((A,B)\mapsto(A\lambda^{-2},B\lambda^{-3})\); the ratio \(A^3/B^2\) is
  the generic modulus.
* Every \((x^4+a x)^3\), \(a\ne0\), lies in one affine orbit.

# 14. Exact computational controls

`code/verify_atlas.py` imports the exact twisted-Krylov reducer in
`code/exact_rank.py` and works over \(\mathbf Q(s)\).  It checks twelve
representatives and mutations, including:

\[
q((x^4+x)^3)=3,
\]

\[
q((x^6+x^2)^2)=q((x^9+x^3)^2)=3,
\]

\[
q((x^6+x^4+x^2)^2)=6,
\]

and

\[
q((x^8+x^2)^3)=4.
\]

The checks distinguish the aligned extension loci from nearby mutations.  They
are exact implementation controls, not substitutes for the classification
proof.

# 15. Assurance statement

The coefficient atlas is proved relative to the support/root-span theorem in
the preceding candidate and to the imported finite-group and Ritt
classifications.  The correction from one to two rank-three extension
mechanisms arose from the explicit counterfamily

\[
(x^{3m}+b x^m)^2.
\]

That correction is retained prominently because it tests the proof method:
full-fusion rigidity must classify the entire scalar-equivariance group of a
block family, not only quartic scalar symmetries.

The package has not received external specialist review, independent
reproduction, or a dedicated priority search.  The strongest warranted claim
is therefore **complete theorem candidate**, not established literature.

# References

* Burda, Y., & Khovanskii, A.  *Polynomials invertible in k-radicals*.
  arXiv:1209.5137.
* Calbetó, J.  *Finite subgroups of PGL(3,C)*.  arXiv:2510.00718.
* Müller, P., & Zieve, M. E.  *On Ritt’s polynomial decomposition theorems*.
  arXiv:0807.3578.
* Müller, P.  Classification results on primitive polynomial monodromy groups
  containing a full cycle, as quoted and used in Burda--Khovanskii.
