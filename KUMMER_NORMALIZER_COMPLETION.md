# The coefficient-stratified all-`m` Kummer-line transport theorem

## 1. Purpose and exact boundary

This note repairs the standalone argument deferred from Lemma 8.1 of
`ALL_DEGREE_GLOBAL_COMPLETION.md`.  It proves monomial Kummer-line transport
on every cubic-over-power stratum where transport is required and treats the
one even-exponent stratum with a non-full Kummer kernel by decomposition
descent.  It also separates the affine-power cubic locus, whose outer
monodromy is cyclic rather than `S_3`.

The proof is algebraic and uniform in `m`.  It does not infer an all-degree
theorem from checks at finitely many exponents.  It imports the full-block
stabiliser interface stated in Section 6 of the global completion and the
standard facts about `Aut(S_4)` and the tetrahedral representation that are
also reproduced in the accompanying finite-group audit.

## 2. Kummer independence and the missed collision locus

Let

\[
H(Y)=Y^3+AY^2+BY+C,
\]

let `y_1,y_2,y_3` be the generic roots of `H(Y)-t` in its splitting field
`L/C(t)`, and put `u_i^m=y_i`.  On the nonpower cubic locus

\[
3B\ne A^2,
\tag{2.1}
\]

the geometric monodromy of `H` is `S_3`.  Except when

\[
B\ne0,\qquad A^2=4B,\qquad 2\mid m,
\tag{2.2}
\]

the Kummer classes of the `y_i` are independent and hence

\[
\operatorname{Gal}(L(u_1,u_2,u_3)/L)\cong\mu_m^3.
\tag{2.3}
\]

Indeed, if `B\ne0` and `A^2\ne4B`, the three roots of
`H(Y)-C=Y(Y^2+AY+B)` are distinct.  Above `t=C` there is, for each `i`, a
divisor with

\[
v(y_i)=1,\qquad v(y_j)=0\quad(j\ne i).
\tag{2.4}
\]

Thus `\prod y_i^{e_i}\in L^{*m}` forces every `e_i=0 mod m`.

If `B\ne0` and `A^2=4B`, write `A=2r`, `B=r^2`, where `r\ne0`.  At a divisor
where `y_i=0` and the other two roots collide at `-r`, normalised valuations
give

\[
v(y_i)=2,\qquad v(y_j)=0\quad(j\ne i).
\tag{2.5}
\]

The three conjugate divisors force `2e_i=0 mod m`.  This proves independence
when `m` is odd.  When `m` is even the conclusion is false: Vieta and
`H(y_k)-C=t-C` give, for `{i,j,k}={1,2,3}`,

\[
y_i y_j=(y_k+r)^2,
\qquad
y_i^{m/2}y_j^{m/2}=(y_k+r)^m.
\tag{2.6}
\]

This is the exceptional stratum (2.2), treated by descent in Section 6.

If `B=0`, then `A\ne0` on (2.1), and
`H(Y)-C=Y^2(Y+A)`.  The three conjugate divisors above `t=C` give, modulo
`m`,

\[
e_1+e_2=e_1+e_3=e_2+e_3=0.
\tag{2.7}
\]

For odd `m` this forces every `e_i=0`.  For even `m` the only additional
candidate is `e_1=e_2=e_3=m/2`.  Since `y_1y_2y_3=t-C`, that candidate would
make `t-C` a square in `L`.  The unique quadratic subfield of the `S_3`
splitting field is cut out by

\[
\Delta(t)=(t-C)\bigl(4A^3-27(t-C)\bigr).
\tag{2.8}
\]

If `t-C` were a square in `L`, uniqueness of that quadratic subfield would
make the nonconstant linear function `4A^3-27(t-C)` a square in `C(t)`, which
it is not.  This proves (2.3).

Consequently every nonexceptional nonpower block action contains

\[
D_m=\{\operatorname{diag}(\zeta_1,\zeta_2,\zeta_3):\zeta_i^m=1\},
\tag{2.9}
\]

and the quotient permutes the coordinate lines as `S_3`.

## 3. Uniqueness of the three-line system for `m>=3`

### Theorem 3.1 (spectral line-system obstruction)

Let `G<=GL_3(C)` contain `D_m` and permute the coordinate lines transitively.
If `m>=3`, the coordinate lines are the unique unordered decomposition of
`C^3` into three one-dimensional subspaces permuted by `G`.

### Proof

Let `L_1\oplus L_2\oplus L_3=C^3` be another such decomposition and take a
primitive `m`-th root `zeta`.  Each

\[
d_i=\operatorname{diag}(1,\ldots,\zeta,\ldots,1)
\]

has characteristic polynomial

\[
(X-\zeta)(X-1)^2.
\tag{3.1}
\]

If `d_i` induced a transposition on the `L_j`, its characteristic polynomial
in a line-adapted basis would be `(X-a)(X^2-q)`.  Comparing coefficients with
(3.1) and eliminating `a,q` gives

\[
2(\zeta+1)^2=0.
\tag{3.2}
\]

Thus `\zeta=-1`, impossible for a primitive root of order `m>=3`.  If `d_i`
induced a three-cycle, its characteristic polynomial would be `X^3-q`; the
`X^2` and `X` coefficients would require both `\zeta+2=0` and
`2\zeta+1=0`, again impossible.

Every `d_i` therefore fixes each `L_j`.  The simultaneous one-dimensional
weight spaces of `D_m` are exactly the coordinate lines, because its three
coordinate characters are distinct.  Hence the two line systems coincide.
\(\square\)

Every linear conjugacy between two such block actions is consequently
monomial.

## 4. Exponent two

For a nonpower cubic, the projective image of `D_2\rtimes S_3` is the
order-24 octahedral group `S_4`.  Its normalizer in `PGL_3(C)` is itself:
every automorphism of `S_4` is inner, the ordinary centralizer is scalar, and
the sign-twisted intertwiner space is zero.  Every octahedral matrix is signed
monomial, so every projective normalizer preserves the three opposite-axis
pairs and hence the Kummer lines.

The affine-power cubic locus is

\[
3B=A^2,\qquad A\ne0,
\tag{4.1}
\]

where, after putting `a=A/3`,

\[
H(Y)=(Y+a)^3+\text{constant}.
\tag{4.2}
\]

Here the outer monodromy is `C_3`.  The Kummer kernel is nevertheless full,
because `A^2\ne4B`, and the projective exponent-two group is tetrahedral
`A_4`.  Its projective normalizer preserves the same three coordinate axes.
One direct proof is to map a normalizer to `Aut(A_4)\cong S_4`: the
automorphism is realised by an octahedral signed-monomial matrix, while the
remaining projective centralizer consists of the three character-twisted
intertwiners, represented by diagonal matrices.  Both parts preserve the
coordinate axes.

Thus the monomial transport conclusion also holds on (4.1) when `m=2`.

## 5. Coefficient transport on the full-kernel strata

Let a rank-preserving block transport be written, after numbering the lines,
as

\[
U'_i=c_iU_{\pi(i)},\qquad a_i=c_i^m.
\tag{5.1}
\]

The powered triples `Y_i=U_i^m` and `a_iY_i` have the same fixed first and
second elementary symmetric functions.

On the nonpower `S_3` locus, the homogeneous constant relation space among
the generic cubic roots is zero when `A\ne0` and is the trace line when
`A=0`.  Indeed, the natural permutation representation is the sum of the
trivial line and the irreducible standard plane.  The standard plane maps
injectively because the roots are distinct; the trivial line maps to
`y_1+y_2+y_3=-A`.  It follows that all `a_i` are one scalar `c`.  The fixed
coefficients give

\[
cA=A,\qquad c^2B=B.
\tag{5.2}
\]

If `A\ne0`, then `c=1`.  If `A=0` and `B\ne0`, the sole nontrivial possibility
is `c=-1`.  This produces exactly

\[
Q=x^{3m}+b x^m,\qquad P=Q^2,
\qquad b\ne0.
\tag{5.3}
\]

On the affine-power locus (4.1), label the roots
`y_i=-a+\omega^i w`, where `\omega^3=1`.  After absorbing the permutation in
the labelling, preservation of the first symmetric function gives

\[
\sum a_i=3,\qquad \sum a_i\omega^i=0.
\tag{5.4}
\]

Preservation of the second symmetric function, equivalently of
`\sum(a_iy_i)^2`, gives all three Fourier coefficients of `(a_i^2)` and hence

\[
a_1^2=a_2^2=a_3^2=1.
\tag{5.5}
\]

Together with `\sum a_i=3`, this forces `a_1=a_2=a_3=1`.  Therefore the
affine-power cubic branch has no nontrivial rank-preserving fibre quotient.

## 6. The exceptional even stratum is an already-used square

On (2.2), write `m=2k`, `A=2r`, and `B=r^2`.  Then

\[
H(x^{2k})-C=x^{2k}(x^{2k}+r)^2
=\bigl(x^{3k}+rx^k\bigr)^2.
\tag{6.1}
\]

If `k=1`, put `a=-r/3`.  Since `D_3(x,a)=x^3+rx` and

\[
D_2(D_3(x,a),a^3)=D_3(x,a)^2-2a^3=D_6(x,a),
\tag{6.2}
\]

(6.1) is, up to target translation, the rank-two Dickson overlap.  It is not
an exact-rank-three block.

If `k>=2`, set `F=x^{3k}+rx^k`.  This lies on the nonexceptional odd-centred
branch of Section 5, whose complete fibre-equivalence calculation permits
only the degree-two quotient `F\mapsto F^2`.  Equation (6.1) is already that
quotient.  If a nonlinear polynomial `R` preserved rank after (6.1), then
`(R\circ(Y^2))\circ F` would be a rank-preserving fibre quotient of `F` of
degree `2 deg R>2`, a contradiction.  Hence the exceptional even stratum
admits no further rank-preserving extension.  No normalizer claim for its
reduced Kummer kernel is needed.

Combining Sections 3--6 proves the transport and non-repetition statements
needed by the cubic-over-power extension classification for every `m>=2`.

## 7. Assurance boundary

The accompanying Lean file checks the characteristic-polynomial identities
and their coefficient obstructions without placeholders.  The clean-room
SymPy/Python program independently checks those identities, the affine-power
and exceptional factorisations, the exceptional pair relation, the Fourier
coefficient system in Section 5, the `S_4` automorphism calculation, and the
octahedral intertwiner spaces.  These controls validate the finite algebra
they name.  They do not formalize function-field valuations, Kummer theory,
the block-stabiliser extension theorem, the decomposition descent, Ritt
theory, or the complete all-degree theorem.
