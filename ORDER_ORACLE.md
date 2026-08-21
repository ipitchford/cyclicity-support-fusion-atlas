# The Exponential-Period Order Oracle

## Exact generic ODE orders and scalar operators from inverse support

Status: **complete research extension; unpublished and unrefereed**  
Parent: *Inverse-Root Support and Fourier Fusion*, v0.5.0-candidate  
Parent release: <https://evidencepress.org/releases/cyclicity-support-fusion-atlas/>  
Parent DOI: <https://doi.org/10.5281/zenodo.22036030>

## Abstract

Let (P\in\mathbf Q[x]) have degree (d\ge2), and let

\[
I_\Gamma(s)=\int_\Gamma e^{sP(x)}\,dx
\]

be a polynomial exponential period over a rapid-decay cycle. The parent
theorem identifies the cyclic rank of the seed (dx), the dimension of the
reduced inverse-root span, and the cardinality of the inverse-at-infinity
support:

\[
q(P,dx)=\dim W_P^{\mathrm{red}}=|\Sigma(P)|.
\]

The same cyclic relation gives a scalar differential operator for every such
period. This extension makes that consequence effective. For trusted rational
input it returns the affine-normalised support, the generic minimal order, a
primitive operator with coefficients in \(\mathbf Z[s]\) for the original
input phase, and an exact zero-residual certificate. Eight frozen benchmarks
cover ranks one through six, affine rank drops, rank creation, aligned
composition and the exceptional degree-twelve Ritt collision. The exceptional
phase \((x^4+x)^3\) has order three, while the exact comparison phase
\(x^{12}+x^{10}+x^3\) has rank eleven. Seven real-line quadrature checks test
the period dictionary but are explicitly excluded from theorem evidence.

## 1. Mathematical contract

In the twisted quotient

\[
\mathcal H_P=
\mathbf Q(s)[x],dx/
(\partial_x+sP'(x))\mathbf Q(s)[x],dx,
\]

the first Krylov dependence has the form

\[
[P^qdx]=\sum_{j=0}^{q-1}c_j(s)[P^jdx].
\tag{1}
\]

For the fixed-sector rapid-decay cycles constructed in the parent manuscript,
differentiation under the integral sign gives

\[
I_\Gamma^{(j)}(s)=\int_\Gamma P(x)^j e^{sP(x)}\,dx.
\tag{2}
\]

Pairing (1) with a cycle therefore yields

\[
I_\Gamma^{(q)}-
\sum_{j=0}^{q-1}c_j(s)I_\Gamma^{(j)}=0.
\tag{3}
\]

Clearing denominators and removing the common polynomial and integer content
produces a deterministic primitive operator

\[
L_P=\sum_{j=0}^{q}a_j(s)D_s^j,
\qquad a_j\in\mathbf Z[s].
\tag{4}
\]

The period matrix in the parent theorem shows that order (q=|\Sigma(P)|) is
minimal for a generic functional on the complete period solution space. The
qualifier is load-bearing: an individual cycle can annihilate an active
Fourier channel and satisfy a lower-order equation.

## 2. What the oracle computes

For an input expression in \(\mathbf Q[x]\), the oracle:

1. parses and affinely normalises the phase for support computation;
2. computes the exact twisted-Krylov rank over \(\mathbf Q(s)\);
3. reverts the normalised phase at infinity until the theorem-certified
   number of non-trace residue classes has appeared;
4. derives the first Krylov dependence for the **original** phase;
5. clears denominators and primitive-normalises its scalar operator;
6. substitutes that operator back into the original Krylov matrix and requires
   an exact zero residual; and
7. binds the result to its input and complete payload with SHA-256.

The distinction between normalised support and original-phase operator is
essential. Translation in the source preserves the period after a change of
variable, but a target shift introduces an exponential gauge factor and a
target scaling changes the differential variable. Those transformations
preserve order; they do not preserve the displayed coefficients of (L_P).

## 3. Command-line use

Generate a certificate:

```bash
python3 src/order_oracle.py \
  --phase '(x**4+x)**3' \
  --output exceptional.json
```

Verify it by digest and exact recomputation:

```bash
python3 src/order_oracle.py --verify-certificate exceptional.json
```

The coefficient list is ordered from (I) through (I^{(q)}). For
(P=x^7), the output is `["1", "7*s"]`, namely

\[
I+7sI'=0.
\]

Input is a trusted SymPy-style rational polynomial expression. The parser is
not an untrusted network-service boundary.

## 4. Frozen exact benchmark

| Case | Degree | \(\Sigma(P)\) | Generic order |
|---|---:|---|---:|
| (x^7) | 7 | \(\{1\}\) | 1 |
| (D_5(x,1)=16x^5-20x^3+5x) | 5 | \(\{1,4\}\) | 2 |
| (x^4+x^2+x) | 4 | \(\{1,2,3\}\) | 3 |
| (x^4+x^2) | 4 | \(\{1,3\}\) | 2 |
| \((x^6+x^2)^2\) | 12 | \(\{1,5,9\}\) | 3 |
| \((x^6+x^4+x^2)^2\) | 12 | \(\{1,3,5,7,9,11\}\) | 6 |
| \((x^4+x)^3\) | 12 | \(\{1,7,10\}\) | 3 |
| \((x^3+x)^2+(x^3+x)\) | 6 | \(\{1,2,4,5\}\) | 4 |

The misaligned square and the degree-six rank-creation phase are semantic
negative controls: an implementation returning only the advertised low orders
cannot pass. Every case has a separate complete JSON certificate as well as a
summary receipt.

## 5. The exceptional degree-twelve operator

For

\[
P(x)=(x^4+x)^3,
\]

the oracle returns

\[
\begin{aligned}
0={}&2(81s+20)I
+18s(81s+200)I'\\
&+27s^2(27s+640)I''
+6912s^3I'''.
\end{aligned}
\tag{5}
\]

Thus a degree-twelve phase has a three-dimensional generic period solution
space. The exact control phase (x^{12}+x^{10}+x^3) attains rank eleven at
each of (s=3/7) and (s=-5/2). Since specialised rank cannot exceed generic
rank, and the ambient twisted de Rham rank is eleven, this proves that the
comparison phase has generic rank eleven without requiring the large symbolic
order-eleven operator in the quick gate. Its inverse support contains all
eleven non-trace classes.

The contrast is therefore exact:

\[
\text{same degree }12,
\qquad 11\longrightarrow3
\]

under the exceptional composition structure. It is a benchmark result, not a
claim that every individual contour realizes order three.

## 6. Verification architecture

The fail-closed oracle gate separates four evidence layers.

| Layer | Check | Evidential role |
|---|---|---|
| Parent integrity | Every byte listed in the published v0.5 manifest retains its frozen digest | proves the extension did not rewrite the parent evidence |
| Algebraic identity | The primitive operator has zero residual in the original exact Krylov matrix | exact operator certificate |
| Benchmark replay | Eight certificates regenerate byte-for-byte under ordinary and optimised Python | determinism and regression control |
| Period spot check | Seven real-line quadratures satisfy their operators below a fixed relative threshold | numerical dictionary check only |

Certificate mutation tests alter an operator coefficient both with and without
recomputing the outer digest. The verifier rejects the first as a digest
mismatch and the second as an exact-recomputation mismatch. Invalid degree-one,
non-polynomial and non-rational inputs must also fail.

Run the complete extension gate with:

```bash
python3 run_order_oracle_checks.py
```

## 7. Intended use

The immediate use is an exact preflight for symbolic integration systems. The
oracle can tell a creative-telescoping or holonomic-reduction workflow the
generic target order before it attempts to construct the operator. It can
also distinguish exceptional low-order phases from same-degree generic ones
and provide exact regression objects for computer-algebra implementations.

The present package does **not** integrate with an external telescoping system,
measure end-to-end speedups, or establish software performance claims. Those
are prospective engineering benchmarks.

## 8. Scope and limitations

- Coefficients are rational. The parent mathematics is over characteristic
  zero, but the released parser and exact arithmetic contract are \(\mathbf Q[x]\).
- The seed is (dx). Weighted periods \(g(x)dx\) need their own support and
  cyclicity analysis.
- The tool does not construct rapid-decay contours or decide whether an
  arbitrary supplied contour is admissible.
- Minimality is generic on the complete solution space, not universal for
  each single cycle.
- The tool does not compute a polynomial decomposition lattice. Its sibling
  fusion calculator reports divisor profiles subject to the actual-factor
  boundary.
- The coefficient atlas is proved only through degree twenty within its stated
  computer-algebra trust base; the oracle itself does not require an
  all-degree inverse-realisability classification.
- The fully symbolic high-order stress case is outside the quick gate because
  of expression swell. This is a performance boundary, not a replacement of
  exact low-order certificates by numerical guesses.
- External specialist review, unaffiliated reproduction, proof-assistant
  formalisation, novelty and priority remain open.

## 9. Research conclusion

The oracle turns the parent work's generic ODE-order corollary into an exact,
auditable computational object. Its main contribution is not a new theorem
beyond the parent support and period results. It is the effective bridge from
inverse support to a primitive scalar operator for the original phase, with a
certificate design that keeps algebraic proof, numerical illustration and
assurance status separate. The degree-twelve order-(3) versus order-(11)
comparison is the clearest demonstration of what that bridge exposes.

