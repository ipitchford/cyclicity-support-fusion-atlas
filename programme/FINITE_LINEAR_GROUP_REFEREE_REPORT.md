# Finite linear group referee report

Date: 2026-08-21  
Review status: internal model audit; not external peer review  
Specialist remit: finite complex linear groups, projective representations,
systems of imprimitivity, and character restriction

## Verdict

**HOLD.**

The conditional finite-linear-group arguments are mostly sound: the
three-line uniqueness theorem is correct when the full diagonal group `D_m`
is present; the octahedral `S_4` is self-normalising in `PGL_3(C)`; the
projective-centraliser/sign-twist reduction is valid; and the `A_5` and
`PSL_3(2)` stabiliser restrictions do exclude projective fixed lines.

However, the preceding assertion that the Kummer kernel is `mu_m^3` for every
coefficient pair and every `m>=2` is false.  A missed even-`m` coefficient
stratum invalidates the universal hypothesis used to invoke those otherwise
correct normaliser arguments.  The clean-room program does not test this
stratum.  The current package therefore does not support the claimed
all-`m` local lemma or an internally complete all-degree proof.

**Public unrefereed candidate release is not scientifically supportable in the
current form.**  Release should remain on hold until the false uniform lemma
is repaired or narrowed, its downstream cases are re-audited, and the
successor artifacts and receipts are regenerated.  Merely retaining the label
"unrefereed" would not cure a known false assurance claim.

## Frozen scope and checks performed

The following submitted artifacts were read without modification:

- `KUMMER_NORMALIZER_COMPLETION.md`;
- `KUMMER_NORMALIZER_ASSURANCE.md`;
- `KUMMER_NORMALIZER_MANIFEST.sha256`;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`;
- `ALL_DEGREE_GLOBAL_REVIEW.md`;
- `GLOBAL_COMPLETION_SOURCE_AUDIT.md`;
- `cleanroom/kummer_normalizer_audit.py`;
- `formal/lean/CyclicityKummer.lean`;
- `formal/kummer_normalizer_protocol.json`;
- `receipts/kummer_normalizer_receipt.json`.

All fourteen entries in `KUMMER_NORMALIZER_MANIFEST.sha256` matched their
current bytes.  A fresh direct run of
`cleanroom/kummer_normalizer_audit.py` passed and returned semantic receipt
hash

`92f6439bd9e953614b05ecd303e3c5e00a9a33737568dabf1841fbaff5fc3f7e`,

matching `receipts/kummer_normalizer_receipt.json`.  This establishes replay
and integrity only; the counterexample below also explains why the passing
replay does not validate the universal lemma.

## Priority findings

### P0 — the claimed full Kummer kernel has an explicit even-`m` counterexample

Locators:

- `KUMMER_NORMALIZER_COMPLETION.md`, Section 2, especially lines 35-38 and
  65-73;
- `KUMMER_NORMALIZER_ASSURANCE.md`, lines 6-13;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, Section 8, lines 420-447 and 474-482;
- `ALL_DEGREE_GLOBAL_REVIEW.md`, lines 76-83 and 96-99.

Take `r!=0` and

\[
 H(Y)=Y(Y+r)^2+C=Y^3+2rY^2+r^2Y+C.
\]

Thus `B=r^2!=0` and `A^2=4B`.  This is a nonpower cubic with generic
monodromy `S_3`: its discriminant, up to a nonzero scalar, is
`(t-C)(4r^3+27(t-C))`, hence is not a square in `C(t)`.

Let `y_1,y_2,y_3` be the roots of `H(Y)-t`.  For every permutation
`{i,j,k}={1,2,3}`, Vieta and the defining equation give

\[
 y_1y_2y_3=t-C=y_k(y_k+r)^2,
 \qquad
 y_i y_j=(y_k+r)^2.
\tag{R1}
\]

If `m` is even, (R1) yields the nonzero Kummer relations

\[
 y_i^{m/2}y_j^{m/2}=(y_k+r)^m\in L^{*m}.
\tag{R2}
\]

Consequently the classes of the `y_i` are not independent in
`L^*/L^{*m}`, and

\[
 \operatorname{Gal}(L(u_1,u_2,u_3)/L)\not\simeq \mu_m^3.
\]

The exact error in the written valuation proof is also visible locally.  At
`t=C`, the zero root is simple but the other two roots collide at `-r`.
Therefore the place of the `S_3` splitting field above `t=C` is ramified, and
the normalised valuation of the zero root is `2`, not `1` as asserted at
lines 35-38.  For odd `m`, multiplication by `2` is invertible modulo `m`, so
this particular defect does not change the intended conclusion.  For even
`m`, it leaves exactly the type of relations displayed in (R2).

This is a theorem-level defect, not a missing citation or a finite-check
qualification.  It directly contradicts the assurance statement that a full
diagonal kernel has been proved for every `m>=2`.  Moreover, the exceptional
cubic is exactly the rewrite used at `ALL_DEGREE_GLOBAL_COMPLETION.md` lines
474-482 to claim that an aligned square cannot repeat: equation (8.5) has
`A=2b`, `B=b^2`, and hence `A^2=4B`.  The gap therefore strikes an essential
non-repetition step, not only a coefficient locus that can be discarded as
lower rank.

Required repair:

1. split the `B!=0` argument into `A^2!=4B` and `A^2=4B`;
2. compute the Kummer relation module on the exceptional stratum rather than
   assuming `D_m`;
3. reprove line transport there, or reroute the stratum through an already
   classified decomposition;
4. update the theorem statement, assurance text, protocol, negative controls,
   receipts, and all dependent review/gate documents.

### P1 — the `m=2` octahedral premise and the stated exact-rank test are not uniform

Locators:

- `KUMMER_NORMALIZER_COMPLETION.md`, Section 4, lines 132-157;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 420-447;
- `KUMMER_NORMALIZER_ASSURANCE.md`, lines 8-13.

On the exceptional stratum above with `m=2`, (R1) implies that all three
classes `[y_i]` in `L^*/L^{*2}` coincide.  Each is nonsquare (for example, its
valuation at a place over infinity is odd), so the Kummer kernel has order two
and acts by the scalar `-I`.  Its projective image is trivial.  The projective
block action is therefore `S_3`, not the order-24 octahedral `S_4` asserted in
Section 4.

There is a compatible rank diagnosis which the global text currently misses:

\[
 H(x^2)-C=x^2(x^2+r)^2=(x(x^2+r))^2.
\tag{R3}
\]

The cubic `x^3+rx` is a Dickson/Chebyshev cubic after scaling, and its square
is affine-equivalent to the corresponding degree-six Dickson polynomial.
Thus this `m=2` stratum is rank two, not exact rank three.  The sentence
"Exact rank three means `(A,B)!=(0,0)`" at
`ALL_DEGREE_GLOBAL_COMPLETION.md` lines 420-422 is therefore false as written.

This observation may permit a repair of the `m=2` branch by excluding and
rerouting (R3), but it does not repair the submitted universal lemma.  For
larger even `m`, the same Kummer relations remain and require an actual proof
with the reduced diagonal subgroup or a different complete decomposition.

### P1 — the clean-room replay omits precisely the exceptional coefficient stratum

Locators:

- `cleanroom/kummer_normalizer_audit.py`, `symbolic_audit`, lines 169-204;
- `cleanroom/kummer_normalizer_audit.py`, receipt construction, lines 214-235;
- `formal/lean/CyclicityKummer.lean`, lines 3-9 and 13-66;
- `formal/kummer_normalizer_protocol.json`, lines 13-24 and 34;
- `receipts/kummer_normalizer_receipt.json`, lines 16-35.

The clean-room program correctly checks:

- the characteristic-polynomial identities for a transposition and a
  three-cycle on a competing line system;
- the coefficient obstruction `-2(z+1)^2`;
- the `B=0` discriminant identity;
- all 24 automorphisms of abstract `S_4` and their innerness;
- faithfulness of the octahedral action on four body diagonals;
- ordinary centraliser dimension one and sign-twisted intertwiner dimension
  zero.

It does not introduce the coefficient `B` in its cubic calculation, test the
`B!=0, A^2=4B` collision, compute any Kummer relation module, or enumerate
systems of imprimitivity.  The Lean file is even narrower and accurately says
that it does not formalise Kummer theory, valuations, imprimitivity, or the
`S_4` normaliser.

Accordingly, the finite enumeration checks the algebraic ingredients it names,
but it does **not** check the prose claim that the full kernel and local
normaliser lemma hold for all coefficients and all `m`.  A passing receipt is
fully compatible with the counterexample (R1)-(R2).  A required new negative
control is the family `A=2r, B=r^2` for even `m`, with expected detection of a
nontrivial relation rather than expected full-kernel success.

### P2 — primitive-factor character exclusions are correct, but lift and outer-twist coverage should be explicit

Locators:

- `ALL_DEGREE_GLOBAL_COMPLETION.md`, Proposition 5.1, lines 258-306;
- `GLOBAL_COMPLETION_SOURCE_AUDIT.md`, lines 82-108;
- `ALL_DEGREE_GLOBAL_REVIEW.md`, lines 59-67.

No counterexample was found in these two restriction calculations.

For `A_5`, the restriction of either ordinary three-dimensional irreducible to
the point stabiliser `A_4` has no one-dimensional constituent.  The trivial
multiplicity is

\[
 (3+3(-1)+8(0))/12=0,
\]

and the two nontrivial linear characters give the same result because the
three-dimensional character vanishes on the two `A_4` classes of
three-cycles.  The outer automorphism of `A_5` swaps the two three-dimensional
characters only through their values on the two order-five classes; `A_4`
contains no order-five elements, so the exclusion is unchanged.

For `PSL_3(2)\simeq PSL_2(7)`, the point stabiliser is `S_4`, whose only linear
characters are `1` and `sgn`.  With class sizes `1,6,3,8,6` for identity,
transpositions, double transpositions, three-cycles, and four-cycles, and
character values `3,-1,-1,0,1`, the two numerators are respectively

\[
 3+9(-1)+8(0)+6(1)=0
\]

and

\[
 3+6-3-6=0.
\]

The outer automorphism/complex-conjugate three-dimensional choice changes the
order-seven values, not the values appearing in an `S_4` restriction, so it
does not reopen a projective line.

The manuscript should nevertheless state why ordinary character restriction
is legitimate after starting with a subgroup of `PGL_3(C)`.  In the concrete
cases, the embeddings are the ordinary icosahedral and Klein
three-dimensional representations.  Equivalently, the possible nontrivial
Schur-cover scalar cannot act as `-I` in odd dimension on the relevant perfect
double cover, since its determinant would be `-1`.  One sentence closing this
lift/projective-scalar point would make the exclusion self-contained at the
claimed level.

There is also a frozen-evidence traceability issue: the submitted
`CyclicityKummer.lean` and `kummer_normalizer_audit.py` contain no `A_5` or
`PSL_3(2)` character checks, while `GLOBAL_COMPLETION_SOURCE_AUDIT.md` lines
97-99 and `ALL_DEGREE_GLOBAL_REVIEW.md` lines 100-103 refer to Lean and SymPy
recomputations.  Those statements may refer to controls outside this frozen
review set, but they are not evidenced by the files submitted to this referee.
This is not a defect in the hand calculation above; it is an assurance-packet
locator gap.

### P3 — machine-check and review language must be narrowed after the repair

Locators:

- `KUMMER_NORMALIZER_COMPLETION.md`, lines 176-185;
- `KUMMER_NORMALIZER_ASSURANCE.md`, lines 1-21;
- `ALL_DEGREE_GLOBAL_REVIEW.md`, lines 21-30 and 110-117;
- `programme/GLOBAL_COMPLETION_QUALITY_GATE.md`, lines 3-18 and 21-26.

The receipt itself is commendably explicit that valuations and Kummer theory
are not formalised.  Other prose nevertheless says the local all-`m` lemma is
proved or validated, and the earlier review labels the residual issue as
external rather than mathematical.  The exact counterexample means those
statements are now stale.

After the mathematics is repaired, distinguish three statements:

1. coefficient identities are checked in Lean;
2. finite `S_4` automorphism and intertwiner computations are replayed in
   SymPy;
3. Kummer-class independence and the coefficient-stratified transport theorem
   are proved in prose unless and until separately formalised.

The new referee decision should supersede, not silently overwrite, the older
internal `PASS WITH NOTES` assessment.

## Determinations on the requested technical questions

| Question | Determination | Reason |
|---|---|---|
| Uniqueness of the three-line system for `m>=3` | **PASS, conditional on `D_m<=G`** | The characteristic-polynomial argument excludes transpositions unless `zeta=-1` and excludes three-cycles; distinct diagonal weights then force the coordinate lines.  No exceptional `m>=3` occurs inside this conditional theorem.  The defect is failure of its hypothesis on the exceptional even-`m` coefficient stratum. |
| `m=2` octahedral normaliser in `PGL_3(C)` | **PASS as a group theorem; FAIL as a universal block-action premise** | For the full signed-monomial block group, the projective image is the rotational octahedral `S_4` and is self-normalising.  On (R1), the projective kernel collapses and the block image is only `S_3`. |
| Projective centraliser/sign twist | **PASS** | A projective centraliser gives a scalar map `lambda(g)` which is a linear character.  `S_4` has only `1` and `sgn`; Schur irreducibility gives a scalar ordinary centraliser, and the octahedral character is not sign-invariant.  The clean-room dimensions `1` and `0` reproduce this exactly. |
| Primitive `A_5` and `PSL_3(2)` factors | **PASS WITH CLARIFICATION** | All linear characters of `A_4` and `S_4` are covered, and outer-twisted/conjugate three-dimensional representations have the same relevant restrictions.  Add an explicit lift/projective-scalar sentence and exact control locators. |
| Clean-room enumeration versus prose | **PARTIAL** | It faithfully checks the spectral and finite-`S_4` ingredients.  It does not check Kummer independence, coefficient strata, line-system uniqueness itself, or the primitive-factor restrictions in the submitted control file. |

## Required revision gate

The verdict can be reconsidered only after all of the following are present in
an additive successor:

1. a corrected Kummer-kernel proposition covering the exceptional locus
   `B!=0, A^2=4B`, with even and odd `m` separated;
2. a corrected exact-rank statement at `m=2` and an explicit routing of the
   degree-six Dickson overlap;
3. a proof of line transport for any remaining exact-rank exceptional even-`m`
   cases, without invoking the false inclusion `D_m<=G`;
4. a clean-room counterexample/stratification control which fails if the full
   kernel is asserted on (R1);
5. revised assurance, protocol, review, and publication-gate documents with
   new hashes and receipts;
6. a fresh specialist re-review of the corrected finite-linear-group step.

Until then, the appropriate scientific status is **HOLD: theorem candidate
contains a known uniform-proof failure**.

## Repair re-audit — 2026-08-21

### Re-audit verdict

**PASS for the repaired finite-linear-group and Kummer-transport successor.**

The preceding HOLD remains part of the historical audit trail, but its
blocking P0/P1 findings are closed by the coefficient-stratified successor.
The false uniform full-kernel assertion has been withdrawn; the exceptional
even-exponent relation is stated exactly; the `m=2` Dickson overlap is routed
out of exact rank three; the remaining exceptional cases descend to the
already-classified aligned square; and the affine-power cubic is treated with
its correct `C_3` outer monodromy and tetrahedral projective image.

This PASS removes the finite-linear-group HOLD on an explicitly labelled
public **unrefereed candidate** release.  It does not constitute external peer
review, formal verification of the valuation/descent arguments, or authority
to describe the all-degree theorem as externally established.  Other
programme gates remain logically independent.

### Replayed successor evidence

The repaired artifacts were inspected read-only.  All fourteen hashes in
`KUMMER_NORMALIZER_MANIFEST.sha256` verified.  A fresh direct run of
`cleanroom/kummer_normalizer_audit.py` returned

`281da4693f34d0cfd26fa131653c3ae0db343d7d0a301dc9dbf4adf7cb58b718`,

matching the v2 CAS semantic hash in
`receipts/kummer_normalizer_receipt.json` lines 13-60.  The v2 semantic
verifier accepted receipt hash

`4b50a66a1fef7619685b43c94258142ff6edd461ecef5ffd8589af289aef7e5a`,

and all nine receipt mutation tests passed.  As before, these checks establish
the named finite algebra and receipt integrity, not the unformalised
function-field arguments.

### Prior-finding traceability

| Prior finding | Repair locator | Re-audit determination |
|---|---|---|
| P0: false full `mu_m^3` kernel on `A^2=4B`, even `m` | `KUMMER_NORMALIZER_COMPLETION.md` Section 2, lines 18-111, especially (2.5)-(2.6) at lines 59-79 | **Closed.**  The normalized valuation is corrected from `1` to `2`; the relations `y_i y_j=(y_k+r)^2` are stated; full-kernel scope is explicitly withdrawn on this stratum. |
| P1: `m=2` projective image incorrectly asserted to be octahedral on the exceptional stratum | `KUMMER_NORMALIZER_COMPLETION.md` Section 6, lines 248-266; `ALL_DEGREE_GLOBAL_COMPLETION.md` lines 454-456 and 491-503 | **Closed.**  The exceptional `m=2` polynomial is identified, up to target translation, with the rank-two degree-six Dickson overlap.  No octahedral premise is used there. |
| P1: exceptional even stratum not handled for larger `m` | `KUMMER_NORMALIZER_COMPLETION.md` Section 6, lines 268-278; `ALL_DEGREE_GLOBAL_COMPLETION.md` lines 497-503 and 541-554 | **Closed.**  Writing `m=2k` gives `H(x^{2k})-C=F^2` with `F=x^{3k}+rx^k`.  Any further rank-preserving `R` would make `(R\circ(Y^2))\circ F` a quotient of `F` of degree `2 deg R>2`, contradicting the already-complete nonexceptional calculation. |
| P1: clean-room blind spot | `cleanroom/kummer_normalizer_audit.py` lines 292-328 and 330-344; v2 protocol lines 20-26 and 41-43 | **Closed at the stated machine boundary.**  The v2 control encodes the exceptional factorisation and pair relation, the even square factorisation, the Dickson translation, and the affine-power Fourier system.  It also rejects promotion of a uniform full-kernel claim. |
| P2: projective/outer-twist clarification | repaired `A_4` argument at `KUMMER_NORMALIZER_COMPLETION.md` lines 168-191 and v2 finite enumeration at `cleanroom/kummer_normalizer_audit.py` lines 169-261 | **Closed for the new tetrahedral branch.**  All automorphisms and all three linear-character intertwiners are covered.  The earlier manually verified `A_5`/`PSL_3(2)` restriction note remains nonblocking and outside the changed successor. |
| P3: machine assurance overstated the universal lemma | `KUMMER_NORMALIZER_COMPLETION.md` lines 280-290; `formal/kummer_normalizer_protocol.json` line 46; v2 receipt assurance lines 2-11 | **Closed.**  The formal/CAS boundary now expressly excludes valuations, Kummer theory, block-stabiliser descent, and the all-degree theorem, and records `uniform_full_kummer_kernel_claim: false`. |

### Focused mathematical findings

#### A. Tetrahedral `A_4` normalizer — PASS

Locators:

- `KUMMER_NORMALIZER_COMPLETION.md`, Section 4, lines 159-191;
- `cleanroom/kummer_normalizer_audit.py`, lines 169-261;
- `formal/kummer_normalizer_protocol.json`, lines 31-32 and 43;
- `receipts/kummer_normalizer_receipt.json`, lines 19-25 and 44-55.

On the affine-power locus `3B=A^2`, `A!=0`, the cubic is
`(Y+A/3)^3+constant`.  Since `A^2!=4B` there, the Kummer kernel is full.  At
`m=2`, quotienting `D_2\rtimes C_3` by scalar `-I` gives the tetrahedral
`A_4` in its irreducible three-dimensional rotation representation.

The normalizer argument is exhaustive.  A projective normalizer induces an
element of `Aut(A_4)\cong S_4`.  All 24 such automorphisms are realised by the
octahedral signed-monomial group.  After removing one such representative, a
normalizer projectively centralises `A_4`, so its scalar multiplier is one of
the three linear characters of `A_4`.  The three corresponding intertwiner
spaces all have dimension one; representatives are `I`,
`diag(1,omega,omega^2)`, and its inverse.  These are diagonal, while the
automorphism representatives are signed monomial.  Hence every projective
normalizer preserves the three coordinate axes.  Outer automorphisms and
projective-scalar twists are both included; no extra normalizer coset is
missed.

For `m>=3`, the already-verified spectral theorem applies because the full
`D_m` is present and the `C_3` quotient remains transitive on the axes.

#### B. Exceptional even-`m` descent — PASS

Locators:

- `KUMMER_NORMALIZER_COMPLETION.md`, equations (2.6), (6.1), and (6.2), lines
  59-79 and 248-278;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, Section 8, lines 491-503 and 541-554;
- v2 CAS, `cleanroom/kummer_normalizer_audit.py`, lines 292-307.

The repair uses the counterexample rather than attempting to erase it.  For
`A=2r`, `B=r^2`, and `m=2k`, it factors the entire phase as

\[
H(x^{2k})-C=(x^{3k}+rx^k)^2=F^2.
\]

When `k=1`, the displayed Dickson identity proves that this is a rank-two
overlap.  When `k>=2`, `F` lies on the nonexceptional odd-centred branch
`A=0`, `B=r`, so the full-kernel transport proof applies to `F` and shows that
its complete rank-preserving quotient has degree at most two, with `F\mapsto
F^2` the sole nontrivial case.  A further nonlinear quotient of `F^2` would
compose to a quotient of `F` of degree greater than two.  This is a valid
descent and needs no assertion about the reduced exceptional Kummer kernel.

#### C. Affine-power coefficient equations — PASS

Locators:

- `KUMMER_NORMALIZER_COMPLETION.md`, Section 5, lines 228-246;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 530-539;
- `cleanroom/kummer_normalizer_audit.py`, lines 309-328.

With roots `y_i=-a+omega^i w`, constancy of the first elementary symmetric
function gives

\[
\sum a_i=3,\qquad \sum a_i\omega^i=0.
\]

Because the first sum is fixed, constancy of the second elementary symmetric
function is equivalent to constancy of `sum (a_i y_i)^2`.  Comparing the
three Fourier coefficients in `1,w,w^2` gives the full Fourier transform of
`(a_i^2)` and hence `a_1^2=a_2^2=a_3^2=1`.  The sum `3` then forces all
`a_i=1`.  The argument permits arbitrary complex transport scalars before the
squared equations; it does not assume signs prematurely.  Thus the
affine-power branch has no nontrivial fibre quotient.

#### D. Circularity audit — PASS WITH ONE P3 PRESENTATION NOTE

Locators:

- `ALL_DEGREE_GLOBAL_COMPLETION.md`, Lemma 6.3, lines 338-370;
- `KUMMER_NORMALIZER_COMPLETION.md`, Sections 5 then 6, lines 193-278;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 497-503.

The earlier unsafe passage from a coordinate projection of the outer block
kernel to absolute block monodromy has been removed.  Lemma 6.3 instead uses
the full setwise block stabilizer.  Its restriction to the splitting field of
`Q(X)-z` is surjective because that splitting field is a Galois intermediate
field of `M/C(t,z)`.  An element carrying one block to another therefore
conjugates the two full induced block-monodromy representations on their
common span.  This input is independent of the Kummer normalizer conclusion.

The proof dependency is now acyclic:

1. Lemma 6.3 supplies full block monodromy without using line transport.
2. Full Kummer independence plus the spectral/finite-group arguments prove
   transport on the nonexceptional strata.
3. The coefficient calculation classifies all quotients of the odd-centred
   nonexceptional phase `F`.
4. Only then does decomposition descent exclude another quotient after `F^2`.

The standalone repair presents this order correctly.  The global Section 8
still says at lines 499-500 that "the nonexceptional calculation below" proves
the input used inside Lemma 8.1.  This is an apparent forward-reference cycle,
not a mathematical one, because the cited standalone Sections 5-6 give the
acyclic proof.  At the next editorial pass, split Lemma 8.1 into a
nonexceptional transport lemma followed by exceptional descent, or cite the
standalone ordering explicitly.  This P3 clarity repair is recommended but
does not reinstate HOLD.

### Final repair disposition

No P0, P1, or P2 defect remains in the repaired finite-linear-group scope.
The sole new note is the P3 ordering clarification above.  The current
specialist disposition is therefore **PASS**, with the assurance boundary
preserved: internal proof candidate and reproducible finite algebra, not
external peer review or a complete formalization.
