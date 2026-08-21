# Newton-sum repair of the cubic and quartic lift descent

Status: **candidate proof repair; internally checked, unrefereed**  
Date: 2026-08-21

## 1. Purpose and exact boundary

The parent coefficient-atlas draft reduced the all-degree rank-at-most-three
classification to primitive cubic and quartic lifts above a maximal power
suffix. Its final step replaced a product of twisted factors by one scalar
power. That replacement was not justified and was withdrawn.

This note replaces it with a symmetric-power argument. It proves the needed
restriction using only the first elementary symmetric functions of the
powered roots. It does not use the withdrawn scalar-collapse identity.

The conclusion is relative to the parent support/root-span theorem, the
low-dimensional primitive audit and the rank-preserving extension arguments.
Those dependencies remain unrefereed theorem candidates.

## 2. Removing the scaling ambiguity

Let the first rank-increasing indecomposable factor have degree `n=3` or
`n=4`, and let `u_i` be chosen `m`-th radicals of its translated roots. At
rank `n-1` their lines have one relation

\[
\lambda_1u_1+\cdots+\lambda_nu_n=0.
\tag{2.1}
\]

No coefficient vanishes: otherwise transitivity and uniqueness of the
relation would force every coefficient to vanish. Put `v_i=lambda_i u_i`, so
that `sum v_i=0`.

After the power case is removed, degree three has monodromy `S_3`. An
indecomposable quartic has primitive monodromy containing the four-cycle at
infinity; the only such subgroup is `S_4`. Monodromy sends the unique
trace-zero relation to a scalar multiple of itself. Taking `m`-th powers in
that transformation shows that the projective vector

\[
(\lambda_1^m,\ldots,\lambda_n^m)
\tag{2.2}
\]

spans a one-dimensional subrepresentation of the natural permutation
module. For `S_3` and `S_4`, the only such line in that module is the constant
line. Hence all `lambda_i^m` are equal. After one common rescaling,

\[
v_i^m=y_i-b.
\tag{2.3}
\]

Thus powering the trace-normalised radicals introduces no residual
root-dependent twist. This is the step that the earlier draft needed but did
not prove.

More explicitly, monodromy now sends the tuple `(v_i)` to a permutation
followed by one common scalar whose `m`-th power is one. Hence
`e_k(v)^m` is single-valued for every `k`. It has no finite poles because the
radicals are integral over the target line. At infinity its pole order is
`k/n`. For `k<n` this is strictly below one, so the invariant rational
function `e_k(v)^m` is constant. The lower elementary symmetric functions of
the `v_i` are therefore constant. The last one has pole order one after taking
the `m`-th power and is affine and nonconstant in the target coordinate.
Consequently the varying polynomial of the `v_i` really has the form used in
Section 3: all coefficients except its constant term are fixed.

## 3. Newton generating identity

For roots `v_1,...,v_n`, write

\[
p_r=\sum_i v_i^r.
\]

If

\[
\prod_i(1-v_it)=B(t)+e t^n,
\]

where `e` is the varying last elementary symmetric function, then

\[
p_r=-r[t^r]\log(B(t)+e t^n)
\tag{3.1}
\]

and therefore

\[
\frac{\partial p_r}{\partial e}
=-r[t^{r-n}]\frac1{B(t)+e t^n}.
\tag{3.2}
\]

The powered roots `v_i^m` are, up to the common scaling already removed, the
roots of one fixed outer polynomial whose constant term alone varies with the
target value. Consequently their first `n-1` elementary symmetric functions
must be independent of `e`. In particular `p_m` and

\[
E_2(m)=\frac{p_m^2-p_{2m}}2
\tag{3.3}
\]

must be independent of `e`.

## 4. Cubic lift

The trace-normalised cubic is

\[
X^3+aX+e,
\qquad a\ne0,
\]

so `B(t)=1+a t^2`. Expanding (3.2),

\[
\frac{\partial p_m}{\partial e}
=-m\sum_{k=0}^{\lfloor(m-3)/3\rfloor}
(-e)^k[t^{m-3-3k}](1+a t^2)^{-k-1}.
\tag{4.1}
\]

Let `K=floor((m-3)/3)` and take the coefficient with largest `e`-degree.
Its residual exponent is `0`, `1` or `2`.

- Residue zero gives the nonzero constant coefficient of the binomial
  series.
- Residue two gives a nonzero multiple of `a`.
- Residue one vanishes, but if `K>=1` the preceding `e`-coefficient has
  residual exponent four and is a nonzero multiple of `a^2`.

Therefore `p_m` can be independent of `e`, with `a!=0`, only for `m=2` or
`m=4`. At `m=4`, direct Newton reduction gives

\[
\frac{\partial E_2(4)}{\partial e}=8ae,
\]

which is not identically zero. Hence

\[
\boxed{m=2.}
\tag{4.2}
\]

For `m=2`, the powered roots have elementary symmetric functions

\[
E_1=-2a,\qquad E_2=a^2,\qquad E_3=e^2,
\]

and hence satisfy

\[
Y(Y+a)^2-e^2=0.
\tag{4.3}
\]

This is exactly the aligned degree-six Dickson/power-square mechanism already
listed in the atlas.

## 5. Quartic lift

The indecomposable trace-normalised quartic is

\[
X^4+aX^2+cX+e,
\qquad c\ne0,
\]

so `B(t)=1+a t^2+c t^3`. Formula (3.2) becomes

\[
\frac{\partial p_m}{\partial e}
=-m\sum_{k=0}^{\lfloor(m-4)/4\rfloor}
(-e)^k[t^{m-4-4k}](1+a t^2+c t^3)^{-k-1}.
\tag{5.1}
\]

Again inspect the largest `e`-degree and its residual exponent modulo four.

- Residue zero gives a nonzero constant.
- Residue three gives a nonzero multiple of `c`.
- Residue two gives a nonzero multiple of `a`. If `a=0`, the preceding
  coefficient has residual exponent six and is a nonzero multiple of `c^2`,
  except for the boundary case `m=6`.
- Residue one first gives zero. The preceding coefficient has residual
  exponent five and is a nonzero multiple of `ac`; if `a=0`, the next has
  residual exponent nine and is a nonzero multiple of `c^3`. The boundary
  cases are `m=5` and `m=9`.

Including `m<4`, independence of `p_m` is therefore possible only at

\[
m=2,\quad m=3,\quad m=5,\quad
m=6\text{ with }a=0,\quad
m=9\text{ with }a=0.
\tag{5.2}
\]

The second elementary symmetric function eliminates every remaining case
except one:

\[
\begin{array}{c|c}
m&\partial E_2(m)/\partial e\\ \hline
2&2,\\
3&-3a,\\
5&-5(a^3-2ae-c^2),\\
6\ (a=0)&6e^2,\\
9\ (a=0)&54c^2e^2.
\end{array}
\tag{5.3}
\]

Since `c!=0`, only `m=3` with `a=0` survives. For that case the powered
roots have

\[
E_1=-3c,\qquad E_2=3c^2,\qquad E_3=-c^3,\qquad E_4=e^3.
\]

Their polynomial is

\[
Y(Y+c)^3+e^3,
\tag{5.4}
\]

and substitution gives the exceptional collision

\[
\boxed{(x^4+cx)^3.}
\tag{5.5}
\]

## 6. Consequence for the all-degree atlas

The Newton argument proves exactly the two lift restrictions for which the
earlier proof used the circular scalar collapse. Relative to the remaining
parent lemmas, the first rank-increasing factor is therefore one of the listed
power, Dickson, cubic-over-power, quartic or exceptional mechanisms. The
rank-preserving extension theorem then yields no further families.

Accordingly, this repairs the identified local obstruction to the all-degree
rank-at-most-three coefficient atlas. Promotion of Conjecture 13.2 to a
theorem still requires specialist checking of:

1. the monodromy/scaling lemma in Section 2;
2. the inherited low-dimensional primitive audit;
3. the finite-pole and infinity-order argument making the lower elementary
   symmetric functions constant; and
4. the inherited rank-preserving extension classification.

The accompanying symbolic check confirms the Newton identities and saturated
candidate loci through `m=32`. That bounded calculation is a fault control,
not the all-`m` proof; the all-`m` content is the coefficient-extraction
argument in (4.1) and (5.1).
