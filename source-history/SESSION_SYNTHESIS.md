# Integrated synthesis

## 1. Starting problem

The two source projects left two linked gaps.

1. The period equations depended on analytic hypotheses about admissible contours, differentiation under the integral sign and vanishing boundary terms.
2. The low-rank root-span project classified indecomposable phases but left decomposable block fusion under polynomial decompositions and Ritt moves unresolved.

The session addressed the first gap by constructing a direct algebraic rank decomposition and explicit rapid-decay periods. It addressed the second through a cyclic-support invariant, then pushed from structural support profiles to affine coefficient families.

## 2. Direct algebraic rank theorem

Affinely normalise a degree-\(d\) polynomial to

\[
P(x)=x^d+\sum_{j=0}^{d-2}p_jx^j.
\]

Let \(\xi_P(t)=t+O(t^{-1})\) be the normalised inverse branch satisfying

\[
P(\xi_P(t))=t^d.
\]

Decompose the Laurent series into exponent residues modulo \(d\):

\[
\xi_P(t)=\sum_{r\in\mathbf Z/d\mathbf Z}X_r(t),
\qquad
\Sigma(P)=\{r:X_r\ne0\}.
\]

A formal moment transform maps the twisted de Rham quotient

\[
\mathcal H_P=
\frac{\mathbf C(s)[x]dx}
{\{(\partial_xf+sP'f)dx\}}
\]

to the direct sum of rank-one Kummer channels. The transform has a triangular matrix with nonzero diagonal on the standard basis. The seed \([dx]\) occupies exactly the channels indexed by \(\Sigma(P)\). Distinct fractional exponents give independent channels. Hence

\[
\boxed{q(P,dx)=|\Sigma(P)|.}
\]

The inverse roots near infinity are Fourier transforms of the nonzero residue components, so

\[
\boxed{q(P,dx)=|\Sigma(P)|=
\dim_{\mathbf C}W_P^{\mathrm{red}}.}
\]

This route removes formal stationary phase as a load-bearing premise for the rank equality.

## 3. Explicit rapid-decay period system

For a sector in the \(s\)-plane, choose fixed decay rays

\[
\phi_k=\frac{\pi-\theta_0+2\pi k}{d}
\]

and contours joining adjacent rays through the origin. Uniform bounds of the form

\[
\Re(sP(re^{i\phi_k}))\le-cr^d+C
\]

justify absolute convergence, all parameter derivatives and twisted integration by parts.

For

\[
\Pi_{k,j}(s)=\int_{\Gamma_k}x^je^{sP(x)}dx,
\]

the scaled limit is

\[
 s^{(j+1)/d}\Pi_{k,j}(s)
 \longrightarrow
 \frac{\Gamma((j+1)/d)}{d}
 e^{\pi i(j+1)/d}
 (\zeta_d^{j+1}-1)\zeta_d^{k(j+1)}.
\]

The limiting matrix is diagonal times Fourier–Vandermonde, hence invertible. The explicit rapid-decay periods therefore separate the quotient near \(s=0\), and the first-order connection propagates nondegeneracy throughout a sector.

This establishes the complete period system needed for the rank theorem. A particular single contour can still have lower scalar order if its functional kills part of the cyclic module; the correct condition is differential-module injectivity, not an ordinary Wronskian slogan.

## 4. Exact block-fusion formula

Let

\[
P=R\circ Q,
\qquad m=\deg Q,
\qquad n=\deg R,
\qquad d=mn.
\]

For each residue \(c\pmod m\), define

\[
L_c=\{\ell\pmod n:c+m\ell\in\Sigma(P)\}.
\]

If \(V_a\) is the span of the \(a\)-th \(Q\)-block, then for every set of outer blocks \(A\),

\[
\boxed{
\dim\sum_{a\in A}V_a
=
\sum_{c:L_c\ne\varnothing}
\operatorname{rank}
\left(\zeta_n^{a\ell}\right)_{a\in A,\ell\in L_c}.
}
\]

Consequences include:

\[
q(Q,dx)=|\pi_m\Sigma(P)|,
\]

full fusion precisely when the projection \(\Sigma(P)\to\mathbf Z/m\mathbf Z\) is injective, and no fusion precisely when each nonempty fibre is all of \(\mathbf Z/n\mathbf Z\).

Equality classes of block spans are monodromy invariant. They therefore determine an actual coarser right factor

\[
P=R^\sharp\circ Q^\sharp,
\qquad Q^\sharp=S\circ Q.
\]

Thus repeated block-span equality is not merely a linear accident.

## 5. Complete decompositions and Ritt moves

For a complete decomposition with suffix degrees \(m_i\), all ranks are projections of the same global support:

\[
r_i=|\pi_{m_i}\Sigma(P)|.
\]

The sequence is nonincreasing towards the right, and its defects telescope:

\[
q(P)-q(P_k)=\sum_i(r_i-r_{i+1}).
\]

When \(q(P)\le3\), at most two levels can create rank above a power suffix, at most one above a rank-two suffix, and none above a rank-three suffix.

For an adjacent coprime Ritt move with degrees \(a,b\) above a suffix of degree \(h\), support projection gives the four ranks

\[
r_0,\,r_a,\,r_b,\,r_2.
\]

A fibre-product inequality follows from the Chinese remainder theorem. At total rank at most three, it yields eleven possible unordered rank diamonds. The table classifies every actual low-rank Ritt move at the invariant level, while leaving polynomial realisability as a separate question.

## 6. Affine coefficient atlas for rank at most three

Relative to the structural theorem and imported finite-group classifications, the proposed affine normal forms over \(\mathbf C\) are:

### Rank one

\[
P\sim x^d.
\]

### Rank two

\[
P\sim D_d(x,a),\quad a\ne0,
\]

or

\[
P\sim x^{2m}+Ax^m,
\quad m\ge2,
\quad A\ne0.
\]

### Rank three

\[
P\sim x^{3m}+Ax^{2m}+Bx^m,
\quad m\ge2,
\]

apart from its stated lower-rank loci;

\[
P\sim x^4+Ax^2+Bx,
\quad B\ne0;
\]

or

\[
P\sim(x^4+ax)^3,
\quad a\ne0.
\]

The realised supports, after normalising the leading infinity character to \(1\), are:

| Rank | Family | Support |
|---:|---|---|
| 1 | power | \(\{1\}\) |
| 2 | Dickson | \(\{1,d-1\}\) |
| 2 | quadratic over a power | \(\{1,m+1\}\) |
| 3 | cubic over a power | \(\{1,m+1,2m+1\}\) |
| 3 | quartic | \(\{1,2,3\}\) |
| 3 | exceptional collision | \(\{1,7,10\}\) |

## 7. Proper rank-preserving extensions

The proposed complete list is:

1. power chains;
2. aligned Dickson chains;
3. aligned rank-three squares
   \[
   Q=x^{3m}+bx^m,
   \qquad P=Q^2;
   \]
4. the quartic cubic collision
   \[
   Q=x^4+ax,
   \qquad P=Q^3.
   \]

The aligned-square family corrects the earlier provisional claim that the quartic collision was the only nontrivial rank-three extension.

## 8. Degree-twelve collision

For

\[
P=(x^4+x)^3=H(x^3),
\qquad H(y)=y(y+1)^3,
\]

one has

\[
\Sigma(P)=\{1,7,10\}\pmod{12}.
\]

Viewed through the degree-four right factor, the support profile is \([1,1,1]\), so all three quartic block spans coincide. Viewed through the degree-three right factor, the profile is \([3]\), so four distinct block lines span the same global three-space. The Ritt move changes the projection, not the global support.

## 9. Assurance boundary

The package contains exact symbolic controls, clean-room finite controls, mutations, negative controls and a numerical period-matrix spot check. These support the implementations and the displayed examples.

The package remains a same-producer theorem candidate. It has not received external specialist review, independent reproduction, formal verification or a dedicated priority search. The finite \({\rm PGL}_3\) reduction and quartic tetrahedron argument are the most important targets for adversarial review.
