# Internal specialist referee report: monodromy, Kummer kernels, and Ritt extensions

**Date:** 2026-08-21  
**Review type:** separate internal model audit; not external peer review  
**Verdict:** **HOLD**  
**Release decision:** **A public unrefereed candidate release presenting the all-degree classification as scientifically supported is not supportable in the present state.**

## 1. Scope and assurance boundary

I reviewed the frozen mathematical claims in:

- `KUMMER_NORMALIZER_COMPLETION.md`;
- `KUMMER_NORMALIZER_ASSURANCE.md`;
- `KUMMER_NORMALIZER_MANIFEST.sha256`;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`;
- `ALL_DEGREE_STRUCTURAL_REPAIR.md`;
- `GLOBAL_COMPLETION_SOURCE_AUDIT.md`;
- `formal/kummer_normalizer_protocol.json`; and
- `receipts/kummer_normalizer_receipt.json`.

I also inspected the cited local Burda--Khovanskii and Calbeto source archives present at `/private/tmp/burda.tar` and `/private/tmp/calbeto.tar`. Their SHA-256 hashes agree with `GLOBAL_COMPLETION_SOURCE_AUDIT.md`, Sections 3--4. I checked the live public arXiv v2 statement of Behajaina--Koenig--Neftin only to verify theorem scope; this does not make the present audit external peer review.

The review was restricted to:

1. fullness of the Kummer kernel in the `B != 0` and `B = 0` cases;
2. cubic `S_3` monodromy;
3. passage from full-block diagonal subdirectness to a linear conjugacy;
4. exhaustiveness of rank-preserving extensions and Ritt moves; and
5. non-repetition of the exceptional rank-three extensions.

All submitted proof and manuscript files were treated as read-only. This report is the only new research file.

## 2. Executive assessment

The local spectral normalizer calculation is good **conditional on the block group containing the stated full diagonal Kummer subgroup**. The `B = 0` Kummer argument also survives scrutiny. The central `B != 0` assertion, however, is false on a ramified codimension-one locus that is not excluded by the hypotheses.

For

\[
H(Y)=Y(Y+b)^2+C=Y^3+2bY^2+b^2Y+C,\qquad b\ne0,
\]

and generic roots `y_1,y_2,y_3` of `H(Y)-t`, one has, with `s=t-C`,

\[
y_k(y_k+b)^2=s=y_1y_2y_3,
\]

and hence, for `{i,j,k}={1,2,3}`,

\[
y_i y_j=\frac{s}{y_k}=(y_k+b)^2.
\tag{2.1}
\]

If the Kummer exponent is even, `m=2r`, then

\[
(y_i y_j)^r=(y_k+b)^m.
\tag{2.2}
\]

Thus the exponent vector `(r,r,0)` is a nonzero relation in `L^*/L^{*m}`. The three Kummer classes are not independent and the claimed kernel `mu_m^3` is not full.

This is not an `S_3` failure: the discriminant here is

\[
-(t-C)\bigl(4b^3+27(t-C)\bigr),
\]

which is nonsquare, so the cubic still has geometric monodromy `S_3`. It is exactly a missing ramification case. It is also exactly the cubic displayed in the claimed non-repetition rewrite in `ALL_DEGREE_GLOBAL_COMPLETION.md`, equation (8.5). Consequently the current proof of non-repetition uses the false full-kernel lemma precisely where that lemma fails.

I found a counterexample to the local all-`m` Kummer lemma, not an explicit additional rank-preserving polynomial family. Read-only exact-rank diagnostics on small representatives were consistent with the claimed non-repetition outcome, but they do not repair the proof or justify an all-degree release.

## 3. Prioritized findings

### P0 — The full Kummer kernel claim is false for `B != 0`

**Locators:**

- `KUMMER_NORMALIZER_COMPLETION.md`, Section 2, lines 32--38, especially the assertion at lines 35--38;
- `KUMMER_NORMALIZER_COMPLETION.md`, equations (2.1) and (2.4), lines 27--29 and 65--73;
- `KUMMER_NORMALIZER_ASSURANCE.md`, lines 6--13;
- `formal/kummer_normalizer_protocol.json`, lines 26--34;
- `receipts/kummer_normalizer_receipt.json`, lines 2--10 and 53--58;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, Lemma 8.1, lines 420--447; and
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, non-repetition argument, lines 474--482.

**Problem.** The sentence “If `B != 0`, then `Y=0` is unramified for `H`” only says that the root `Y=0` itself is simple. It does not say that the place `t=C` is unramified in the splitting field. When

\[
A^2=4B\ne0,
\]

the other two roots of `H(Y)-C=Y(Y^2+AY+B)` collide. At a place of the Galois closure where `y_i=0`, the base uniformizer `t-C` has valuation two and `v(y_i)=2`, not one. Therefore the isolating valuation asserted at lines 35--38 does not exist.

Taking `A=2b`, `B=b^2` gives the explicit relations (2.1)--(2.2), which directly disprove independence in `L^*/L^{*m}` for every even `m`.

**Why it matters.** The full diagonal subgroup `D_m` is the hypothesis used by the line-system normalizer proof. Without it, Sections 3--4 of `KUMMER_NORMALIZER_COMPLETION.md` cannot simply be applied. The defect is load-bearing in the global argument because the claimed first exceptional extension is rewritten as

\[
Y(Y+b)^2=Y^3+2bY^2+b^2Y
\]

at `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 474--482, with an even Kummer exponent. That is the counterexample locus.

For `m=2`, this locus is also the degree-six Dickson overlap: `(x^3+bx)^2` is affine in the target to a Dickson polynomial. Thus the blanket statement “Exact rank three means `(A,B)!=(0,0)`” at `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 420--423, needs an explicit lower-rank exclusion. For even `m>=4`, the rank-three case remains relevant and needs a corrected subgroup/normalizer analysis.

**Required repair.** Split the `B != 0` proof into at least:

1. `A^2 != 4B`, where the three roots of `H(Y)-C` are distinct and the original isolating valuations work;
2. `A^2=4B`, `m` odd, where the corrected order-two valuation still proves independence because `2` is invertible modulo `m`; and
3. `A^2=4B`, `m` even, where the full-kernel statement must be replaced by the actual Kummer subgroup and its linear/projective normalizer.

The non-repetition result must then be reproved independently on the third branch. Until that is done, the all-degree theorem is not internally closed.

### P1 — The `S_3` hypothesis is not satisfied by the whole cubic family used in Section 8

**Locators:**

- `KUMMER_NORMALIZER_COMPLETION.md`, lines 11--14, 20--25, 65--73, and 132--157;
- `ALL_DEGREE_STRUCTURAL_REPAIR.md`, Section 2.1, lines 31--53;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 412--447 and 450--464.

**Problem.** The structural proof of `S_3` monodromy is correct for the trace-normalized nonpower cubic

\[
X^3+aX+T,\qquad a\ne0.
\]

For the general cubic `Y^3+AY^2+BY+C`, however, the centered linear coefficient is

\[
B-A^2/3.
\]

The condition `(A,B)!=(0,0)` in the Kummer/global argument does not imply that this is nonzero. On the locus

\[
3B=A^2,\qquad A\ne0,
\]

the cubic is affine-equivalent to a power:

\[
H(Y)=(Y+A/3)^3+\text{constant},
\]

so its geometric monodromy is `C_3`, not `S_3`.

This also invalidates the statement at `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 450--453, that the constant-linear relation space of the generic cubic roots is zero whenever `A!=0`. On the cyclic cubic locus the roots have the form `-a+zeta_3^i w` and admit a non-trace constant-linear relation.

**Why it matters.** For `m=2`, the projective group is tetrahedral `A_4`, not the octahedral `S_4` asserted in `KUMMER_NORMALIZER_COMPLETION.md`, lines 134--157. Its normalizer may still give the desired monomial conclusion, but that is a different argument. The powered-coefficient step likewise needs a separate analysis because the relation space changes.

**Required repair.** Add the missing nonpower condition `3B!=A^2` wherever `S_3` is invoked, and treat the affine-power cubic branch separately in the extension classification. Do not use the trace-relation dichotomy from lines 450--453 on that branch.

### P1 — Diagonal subdirectness identifies the actual kernel images, not automatically the full block monodromy

**Locators:**

- `ALL_DEGREE_GLOBAL_COMPLETION.md`, Lemma 6.1 and Corollary 6.2, lines 311--336;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, proof of Lemma 8.1, lines 434--447; and
- `KUMMER_NORMALIZER_COMPLETION.md`, Section 5, lines 159--174.

**Problem.** Lemma 6.1 proves that each coordinate projection of the outer block kernel is injective. Each projection is, tautologically, surjective onto its own image, so the kernel is a diagonal subdirect product of those **images**. The text then applies a normalizer theorem for the full block group containing `D_m` and quotient `S_3`. No argument is supplied that a coordinate image of the outer block kernel equals that full absolute monodromy group, or even contains the full Kummer subgroup. Base change by the outer splitting field can shrink a coordinate kernel through a field intersection.

There is a plausible repair using the full setwise block stabilizer rather than only the outer block kernel: the restriction of the block stabilizer to a block should be identified with the absolute monodromy of `Q`, and an element transporting one block to another then conjugates these full induced actions on the common span. But this restriction-surjectivity statement and its compatibility with the common linear representation must be stated and proved.

**Why it matters.** Without that bridge, the linear map obtained from block transport is known to normalize only the actual coordinate image. The hypotheses of Theorems 3.1 and 4.1 in `KUMMER_NORMALIZER_COMPLETION.md` do not follow from Corollary 6.2 as written.

**Required repair.** Supply a function-field or covering-space lemma proving full block-stabilizer surjectivity and use that lemma explicitly. Alternatively, classify the normalizer of every possible coordinate image that can arise after base change.

### P1 — Non-repetition of the aligned square is not proved

**Locators:**

- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 462--482;
- `KUMMER_NORMALIZER_COMPLETION.md`, lines 159--175.

**Problem.** The only stated reason that the aligned square cannot repeat is that, after rewriting it as a cubic over `x^{2m}`, the quadratic coefficient is nonzero and equation (8.3) forces the scalar `c=1`. But the rewritten cubic is exactly `H(Y)=Y(Y+b)^2`, and the new Kummer exponent is even. P0 shows that the full Kummer group and therefore the preceding monomial transport proof are unavailable at exactly this point.

**Assessment.** I did not find an actual repeated rank-preserving extension. For example, a read-only exact-rank diagnostic with `b=1` gives rank three for `(x^6+x^2)^2` and rank six for `(x^6+x^2)^4`. This is finite evidence only. It supports the intended result but cannot replace an all-degree argument.

**Required repair.** Give a direct inverse-support calculation for a second extension, or compute the actual even-`m` Kummer subgroup on `A^2=4B` and prove its normalizer still forces a trivial fibre equivalence. The result must cover every `m>=2`, not a finite range.

### P2 — The long Dickson-chain citation does not by itself close mixed aligned/non-aligned chains

**Locators:**

- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 349--388;
- `GLOBAL_COMPLETION_SOURCE_AUDIT.md`, lines 23--30.

**Problem.** The cited Behajaina--Koenig--Neftin Theorem 6.1 applies to a chain of odd-prime dihedral factors under the hypothesis that **every adjacent composition** is not linearly equivalent to the corresponding Chebyshev composition. The prose at lines 384--388 concludes that arbitrary long rank-preserving Dickson chains are exactly the aligned chains, but it does not give the Ritt-normalization induction for a mixed chain containing both aligned and non-aligned adjacent pairs.

This may be repairable by moving aligned Chebyshev factors through Ritt moves and applying the theorem or the length-two result to a terminal non-aligned segment. That reduction is not written, and it is part of the requested exhaustion claim.

**Required repair.** State and prove an induction: after allowed affine changes and adjacent Ritt moves, either the whole dihedral chain consolidates to one Dickson polynomial or a terminal segment satisfies the hypotheses of the large-kernel theorem and contradicts Corollary 6.2. Treat repeated prime degrees and the quadratic/power overlap explicitly.

### P2 — The receipt and assurance state exceed what the checked algebra establishes

**Locators:**

- `KUMMER_NORMALIZER_ASSURANCE.md`, lines 3--13;
- `formal/kummer_normalizer_protocol.json`, lines 5--34;
- `receipts/kummer_normalizer_receipt.json`, lines 2--10, 37, and 53--58;
- `KUMMER_NORMALIZER_MANIFEST.sha256`, lines 1--14.

**Problem.** The manifest is internally consistent: all fourteen listed hashes verify. The Lean/CAS inventory also honestly excludes formalized Kummer theory and valuation arguments. Nevertheless, the receipt records `written_all_m_local_lemma: true` and `status: pass`, while the assurance says the full diagonal kernel is established for every `m>=2`. Those semantic conclusions are false because the unformalized valuation step omitted the locus `A^2=4B`.

**Required repair.** Change the successor state to HOLD until the mathematical repair is complete. Add an explicit semantic negative control for

\[
H(Y)=Y(Y+1)^2+C,
\]

checking the relation `(y_i y_j)^{m/2}=(y_k+1)^m` for even `m`. Hash integrity must remain clearly separated from theorem correctness.

### P3 — Parameter boundaries and group names need local clarification

**Locators:**

- `KUMMER_NORMALIZER_COMPLETION.md`, lines 11--14 and 20--25;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 420--423;
- `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 474--482.

The local statements should name all exceptional parameter loci when they first arise:

- `3B=A^2`: affine-power cubic, quotient `C_3` rather than `S_3`;
- `A^2=4B`: collision of the two nonzero roots above `t=C`;
- `m=2, A^2=4B`: lower-rank Dickson overlap; and
- even `m, A^2=4B`: non-full Kummer kernel.

This is not merely stylistic: making these boundaries explicit prevents the same hidden-genericity error from being reintroduced after the P0 repair.

## 4. Topic-by-topic determinations

### 4.1 Fullness of the Kummer kernel

| Case | Determination | Reason |
|---|---|---|
| `B=0`, `A!=0` | **PASS** | The three ramified divisors give the pair-sum congruences. For odd `m` they force zero; for even `m` the sole residual class is `(m/2,m/2,m/2)`. Since the cubic is genuinely `S_3` and `Delta=(t-C)(4A^3-27(t-C))`, the unique quadratic-subfield argument correctly excludes `t-C` being a square in `L`. |
| `B!=0`, `A^2!=4B` | **PASS for the stated valuation method** | All three roots of `H(Y)-C` are distinct, so the isolating valuations with pattern `(1,0,0)` exist. |
| `B!=0`, `A^2=4B`, odd `m` | **SALVAGEABLE, NOT CORRECT AS WRITTEN** | The isolating valuation has order two, so it gives `2e_i=0 mod m`; oddness of `m` then forces `e_i=0`. |
| `B!=0`, `A^2=4B`, even `m` | **FAIL** | Equation (2.2) is a nontrivial Kummer relation. The kernel is not `mu_m^3`. |

### 4.2 `S_3` monodromy

`ALL_DEGREE_STRUCTURAL_REPAIR.md`, Section 2.1 is correct: a centered nonpower cubic `X^3+aX+T` with `a!=0` has nonsquare discriminant and hence `S_3` monodromy. The use of that fact in the Kummer/global note is overbroad because `(A,B)!=(0,0)` does not exclude `3B=A^2`.

The P0 counterexample remains `S_3`, so repairing the monodromy hypothesis alone does not repair the Kummer lemma.

### 4.3 Spectral and octahedral normalizers

Conditional on containing the full `D_m`:

- the characteristic-polynomial obstruction in Theorem 3.1 correctly rules out a transposition or three-cycle induced by a primitive diagonal generator for `m>=3`;
- the common weight spaces are therefore the coordinate lines;
- the projective `S_4` normalizer argument for `m=2` is sound for the octahedral representation, including the sign-twist check.

These are genuine strengths. They do not imply that the group hypotheses hold on every parameter locus.

### 4.4 Rank-preserving quartic extensions

The source-to-case use of Behajaina--Koenig--Neftin is accurate:

- Theorem 2.3 covers prime-degree `AGL_1` outer factors with inner `S_4` and isolates the cubic Ritt collision;
- Theorem 2.4 covers an `S_4` outer factor; and
- Theorem 2.7 covers nonsolvable outer factors.

Together with the indecomposable monodromy list, those three cases are exhaustive for the rightmost indecomposable outer factor. Each noncollision kernel contains a coordinate-supported `V_4`, contradicting Corollary 6.2. I found no source-scope error in this branch.

The subsequent normalizer argument for non-repetition of `(x^4+ax)^3` is plausible and no counterexample was found. It is not affected by the P0 Kummer defect.

### 4.5 Ritt moves and overall exhaustiveness

The power and two-dimensional Fermat/Dickson calculations are coherent. The quartic Ritt collision is source-backed. The cubic branch and its non-repetition are not closed because of P0 and the cyclic-cubic subcase. The long Dickson-chain prose also needs the mixed-chain induction identified at P2.

Therefore the list of four extension mechanisms may still be correct, but the present artifacts do not prove that it is exhaustive.

## 5. Circularity, genericity, and counterexample audit

### Circularity

I did not find a direct logical cycle in the spectral normalizer proof itself. The principal structural issue is instead an unjustified strengthening:

\[
\text{diagonal subdirect product of coordinate images}
\quad\Longrightarrow\quad
\text{normalizer of the full absolute block group}.
\]

That implication requires an additional block-stabilizer/full-monodromy lemma.

### Hidden genericity

Two unannounced exceptional loci are used as though generic arguments covered them:

1. `A^2=4B`, where `t=C` is ramified in the splitting field even though the zero root is simple; and
2. `3B=A^2`, where the cubic is affine-power and has `C_3` rather than `S_3` monodromy.

### Missing ramification case

The omitted `A^2=4B` case is the source of the explicit Kummer counterexample and is the decisive defect.

### Counterexample search outcome

- **Found:** a uniform counterexample to full Kummer independence for every even exponent, equations (2.1)--(2.2).
- **Not found:** an actual additional all-degree rank-three extension family.
- **Finite diagnostic only:** a second square of a small aligned-square example raises the exact rank from three to six, consistent with non-repetition but not proving it.

## 6. Required revision order

1. **P0:** withdraw the full-kernel/pass claim and repair the `A^2=4B` Kummer calculation for all `m`.
2. **P0:** reprove aligned-square non-repetition on the actual even-`m` Kummer subgroup or by a direct inverse-support argument.
3. **P1:** separate the affine-power cubic locus `3B=A^2` from the `S_3` branch and redo the root-relation/coefficient argument there.
4. **P1:** replace the kernel-image shortcut by a precise block-stabilizer/full-monodromy conjugacy lemma.
5. **P2:** write the Ritt-normalization induction for mixed aligned/non-aligned Dickson chains.
6. **P2:** update the protocol, receipt, assurance, and semantic negative controls only after the mathematical repairs pass a new independent audit.

## 7. Final verdict and release statement

**Verdict: HOLD.**

The package has strong local algebra, good source traceability, and an honest formalization boundary. Those strengths do not offset a false load-bearing lemma. Because the false statement is used at the exact parameter locus of the claimed aligned-square non-repetition, the rank-preserving extension classification is not presently established.

Accordingly:

- **Public unrefereed candidate release as a completed all-degree theorem:** **NO-GO**.
- **Private/internal circulation explicitly labelled “HOLD: counterexample to Kummer fullness; classification proof under repair”:** scientifically appropriate.
- **Possible future candidate release:** only after the P0/P1 repairs are written, the assurance artifacts are regenerated rather than merely rehashed, and a new specialist audit confirms the corrected Kummer subgroup, transport lemma, and non-repetition argument.

## 8. Repair re-audit — 2026-08-21

### Re-audit verdict

- **Repaired coefficient-stratified Kummer/monodromy successor:** **PASS** as an internal written theorem candidate, relative to its stated standard group-theoretic and function-field inputs.
- **Complete all-degree classification and public unrefereed candidate release:** **HOLD**.

The former P0 and P1 defects are repaired. The previous mixed Dickson-chain P2 is unchanged and remains load-bearing for Theorem 11.1. Accordingly, the earlier global HOLD and public-release NO-GO are narrowed but not lifted.

### Verification traceability

| Prior finding | Revised location | Re-audit status | Independent verification |
|---|---|---|---|
| P0: false uniform full Kummer kernel on `B!=0`, `A^2=4B`, even `m` | `KUMMER_NORMALIZER_COMPLETION.md`, Section 2, lines 34--79 | **FULLY ADDRESSED** | The note now distinguishes the unramified locus, the order-two valuation on `A^2=4B`, the odd-`m` consequence, and the genuine even-`m` relation `y_i^{m/2}y_j^{m/2}=(y_k+r)^m`. It no longer claims `mu_m^3` on the exceptional stratum. |
| P1: affine-power cubic incorrectly treated as `S_3` | `KUMMER_NORMALIZER_COMPLETION.md`, Section 4, lines 168--191, and Section 5, lines 228--246; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 454--489 and 530--539 | **FULLY ADDRESSED** | The locus `3B=A^2`, `A!=0` is explicitly assigned outer monodromy `C_3`. For `m>=3`, full Kummer independence plus the spectral theorem preserves the axes. For `m=2`, the tetrahedral `A_4` normalizer is treated separately. The first- and second-symmetric-function Fourier equations force all powered transport scalars to equal one. |
| P1: kernel subdirectness did not imply conjugacy of full absolute block groups | `ALL_DEGREE_GLOBAL_COMPLETION.md`, Lemma 6.3, lines 338--370 | **FULLY ADDRESSED** | If `M` is the splitting field of `P(X)-t`, the setwise block stabilizer is `Gal(M/C(t,z))=Gal(M/C(z))`. The splitting field `L_B` of `Q(X)-z` is a Galois intermediate field contained in `M`, so restriction is surjective onto `Gal(L_B/C(z))=Mon(Q)`. A block transporter conjugates these full stabilizers and, under full fusion, their actions on the common span. This is the required full-group linear conjugacy. |
| P0/P1: aligned-square non-repetition used the false full kernel exactly on the exceptional stratum | `KUMMER_NORMALIZER_COMPLETION.md`, Section 6, lines 248--278; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 491--503 and 541--554 | **FULLY ADDRESSED** | Writing `m=2k` gives `H(x^{2k})-C=(x^{3k}+rx^k)^2`. For `k=1` this is the translated degree-six Dickson overlap. For `k>=2`, it is already the unique degree-two quotient of the nonexceptional odd-centred phase `F=x^{3k}+rx^k`. Any further nonlinear quotient of `F^2` would compose with the square to give a rank-preserving quotient of `F` of degree greater than two, contradicting the already completed nonexceptional calculation. This descent does not invoke a normalizer for the reduced exceptional Kummer kernel and is not circular. |
| P2: arbitrary mixed aligned/non-aligned odd-prime Dickson chains | `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 418--422 | **NOT ADDRESSED** | The text is materially the same two-sentence appeal to Behajaina--Koenig--Neftin Theorem 6.1. That theorem handles a chain in which every adjacent pair is non-aligned. The successor still supplies neither a Ritt-normalization induction nor a kernel-propagation argument for a chain containing both aligned and non-aligned adjacent pairs. |

### Detailed determinations on the repaired branches

#### Lemma 6.3

**PASS.** The field-theoretic bridge is correct. Since `t=R(z)`, one has `C(t,z)=C(z)`. Every root of `Q(X)-z` is a root of `P(X)-t`, so its splitting field lies in `M`. Restriction from the block stabilizer is therefore onto the absolute geometric block monodromy. This repairs the earlier unjustified passage from a diagonal subdirect product of kernel images to the full block action.

#### Exceptional even-`m` descent

**PASS.** The repaired proof accepts, rather than suppresses, the non-full Kummer kernel. Its factorization

\[
H(x^{2k})-C=(x^{3k}+rx^k)^2
\]

routes the exceptional phase through the already classified nonexceptional odd-centred phase. The `k=1` Dickson overlap and `k>=2` exact-rank-three cases are separated correctly. The non-repetition contradiction uses only composition of outer quotients and the completed fibre-equivalence group of `F`; it does not assume the conclusion being proved.

#### Affine-power `C_3` branch

**PASS.** The repaired proof uses the correct cyclic cubic monodromy. The tetrahedral exponent-two normalizer and the `m>=3` spectral argument both preserve the Kummer axes. With `Y_i=-a+omega^i w`, preservation of `e_1` yields

\[
\sum a_i=3,\qquad \sum a_i\omega^i=0,
\]

and preservation of `e_2`, equivalently the second power sum after `e_1` is fixed, gives all Fourier coefficients of `(a_i^2)` and hence `a_i^2=1`. The sum condition forces every `a_i=1`. No hidden genericity remains on this branch.

#### Aligned-square non-repetition

**PASS.** The revised decomposition descent is uniform in the original exponent and closes the specific locus on which the first report found the counterexample to Kummer fullness. Read-only finite diagnostics are no longer carrying the conclusion.

### Sole remaining load-bearing obligation: mixed Dickson chains

The global theorem still asserts at `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 418--422, that the cited long-chain theorem supplies the aligned-Dickson conclusion for arbitrary chains. The stated source hypothesis does not cover a mixed chain directly. For example, a chain may contain a maximal aligned Chebyshev segment next to a non-aligned dihedral pair; it is neither wholly aligned nor a chain in which every adjacent pair is non-aligned.

One of the following repairs is required:

1. **Ritt-normalization route.** Prove that adjacent aligned Chebyshev factors can be moved and consolidated, with compatible affine changes, until either the entire chain is one Dickson composition or a terminal non-aligned segment satisfies the cited large-kernel theorem. Then prove that its proper-support kernel survives in the block kernel of the full composition and contradicts Corollary 6.2. The proof must address repeated prime degrees and isolate degree two as the power overlap.
2. **Direct uniformization route.** Expand lines 383--415 into a global proposition: classify every finite transitive collection of equal Dickson planes `span(U,U^{-1})`, prove that its constants form the complete cyclic/dihedral orbit, and prove that the quotient polynomial is exactly `D_n` with the compatible parameter. If established for an arbitrary outer polynomial at once, this would make the mixed-chain appeal unnecessary.

Merely restating Theorem 6.1 or checking more finite Dickson examples will not close this obligation.

### New-issue scan

No new P0 or P1 defect was found in Lemma 6.3, the coefficient-stratified Kummer proof, the affine-power branch, or exceptional non-repetition. The updated Kummer manifest verifies all listed successor bytes, but that identity/replay result remains separate from the unformalized function-field and decomposition arguments, as the successor correctly states.

A minor clarity improvement would be to carry the target translation explicitly in the exceptional descent: from `Q=F^2+C`, a further outer factor is rewritten as `(R circ (Y+C) circ Y^2) circ F`, not literally `(R circ Y^2) circ F`. This does not change the degree argument or the verdict.

### Re-audit release statement

The repaired Kummer successor is scientifically supportable for internal specialist circulation as a **PASS-level theorem candidate** with its stated assurance boundary. The complete all-degree theorem is not yet supportable for public unrefereed candidate release because its exhaustive rank-two extension step still depends on the unresolved mixed Dickson-chain P2.

**Final re-audit disposition: HOLD until the mixed Dickson-chain obligation is proved and independently rechecked.**

## 9. Second repair re-audit — 2026-08-21: direct Dickson completion

### Decision

- **Direct all-degree Dickson extension theorem:** **PASS**.
- **Prior mixed-chain P2:** **FULLY ADDRESSED**.
- **Complete all-degree classification:** **PASS** as an internal written theorem candidate, relative to the standard function-field and imported classification inputs stated in `ALL_DEGREE_GLOBAL_COMPLETION.md`.

This second repair supplies the direct-uniformization route requested at Section 8, lines 385--390, of this report. It does not try to extend Behajaina--Koenig--Neftin Theorem 6.1 beyond that theorem's hypotheses. Instead it classifies an arbitrary outer polynomial `R` in one step. The mathematical reason for the preceding global HOLD is therefore removed.

### Verification of the new proof

| Proof obligation | Exact revised location | Re-audit determination |
|---|---|---|
| Full-fusion field inclusions and `M=C(U)` | `DICKSON_EXTENSION_COMPLETION.md`, lines 25--46; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 383--420 | **PASS.** For `m>=3`, the roots `x_k=zeta_m^k U+a zeta_m^{-k}U^{-1}` in one Dickson block recover `U` and `a/U` by the two Fourier projections. Thus `C(U)<=M`. Rank preservation and Corollary 2.2 identify every block span with the same plane `<U,U^{-1}>`. A uniformizer `V` of any other block and its inverse lie in this plane. Expanding `VV^{-1}=1` forces the change of basis to be diagonal or antidiagonal, so `V=cU` or `cU^{-1}`. Hence every root of `P(X)-t` lies in `C(U)`, while `t=P(U+a/U)` also lies there; therefore the splitting field is exactly `M=C(U)`. |
| Finite torus-normalizer classification | `DICKSON_EXTENSION_COMPLETION.md`, lines 48--62; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 423--444 | **PASS.** Because `M=C(U)`, the Galois action preserves the common root plane. Applying the same product calculation to `sigma(U)` and `sigma(U^{-1})` puts every automorphism in the normalizer `U mapsto cU` or `c/U`. The rotation kernel is a finite subgroup of `C^*`, hence `mu_N`; the already present reflection `U mapsto a/U` makes the quotient by rotations nontrivial and gives a dihedral group of order `2N`. No omitted cyclic, polyhedral, or exceptional subgroup can occur inside this normalizer. |
| Degree calculation | `DICKSON_EXTENSION_COMPLETION.md`, lines 55--62; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 431--444 | **PASS.** The rational map `U mapsto P(U+a/U)` has poles of order `deg P=mn` at both `U=0` and `U=infinity`, so its degree is `2mn`; there is no cancellation at either pole. Since `C(U)/C(t)` is the splitting field and hence Galois, `|Gamma|=[C(U):C(t)]=2mn`. Thus `N=mn`, including composite and repeated-prime outer degrees. |
| Dihedral invariant field | `DICKSON_EXTENSION_COMPLETION.md`, lines 63--68; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 446--453 | **PASS.** First taking invariants of `mu_N` gives `C(U^N)`; the reflection sends `U^N` to `a^N/U^N`, whose fixed field is generated by `U^N+a^N/U^N`. By the Dickson uniformization identity this is `C(D_N(x,a))`, and its degree is `2N`, as required. |
| Affine generator and outer-factor conclusion | `DICKSON_EXTENSION_COMPLETION.md`, lines 70--78; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 455--463 | **PASS.** Equality `C(P(x))=C(D_N(x,a))` makes the two generators Mobius-related. Since both are nonconstant polynomials in `x`, the denominator must be constant, so the relation is affine. With `N=mn`, the identity `D_N=D_n circ D_m` with parameter `a^m` gives `R circ D_m=A circ D_n circ D_m`; injectivity of substitution by the nonconstant polynomial `D_m` yields `R=A circ D_n`. This establishes the claimed outer factor, not only the composite. |
| Arbitrary `R`, mixed chains, and Ritt moves | `DICKSON_EXTENSION_COMPLETION.md`, lines 80--86; `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 465--470 and 754--758 | **PASS.** The proof never decomposes `R` and never assumes prime degrees, adjacent nonalignment, or a particular Ritt presentation. It applies directly with `n=deg R`. Consequently mixed aligned/nonaligned factorizations, repeated prime degrees, quadratic outer factors, and any sequence of Ritt moves all describe the same globally dihedral polynomial. The degree-two Dickson polynomial itself is a rank-one power overlap, while degree-two outer extensions are already included by `n=2`. BKN Theorem 6.1 is now expressly only a contextual cross-check. |

### Circularity, genericity, and counterexample scan

No circularity was found. The argument uses only the previously established full-fusion equivalence, elementary Fourier recovery in a Dickson block, the splitting-field definition, automorphisms of `C(U)`, and elementary invariants of a finite dihedral action. It does not use Theorem 11.1, Ritt normalization, or the conclusion that the full composite is Dickson.

No hidden genericity was found. The proof works over the generic transcendental `t`, assumes exactly `a!=0` and `m>=3`, and treats arbitrary `n=deg R`. The excluded cases are appropriate: `a=0` is the power family and `D_2(x,a)=x^2-2a` is affine-equivalent to a rank-one quadratic power. No counterexample survives the field-degree and invariant-field calculation.

Two non-load-bearing expository expansions would improve the standalone note:

1. write the two Fourier formulas recovering `U` and `a/U` explicitly and cite the full-fusion implication from Corollary 2.2; and
2. spell out the injectivity of `F(y) mapsto F(D_m(x,a))` when passing from the affine equivalence of `P` to the formula for `R`.

Both steps are already forced by the written setup and neither is a revision condition for the verdict.

### Updated release statement

The prior mathematical HOLD is lifted. On the scope audited in this report, the all-degree theorem is scientifically supportable for a **clearly labelled public unrefereed candidate release**. Such a release must preserve the stated assurance boundary: this is a written internal proof audit relative to named classification inputs, not formal verification, external independent reproduction, novelty certification, or specialist peer review.

**Final second-repair disposition: PASS. No P0--P2 mathematical obligation from this referee report remains open.**

## 10. Post-edit confirmation — 2026-08-21

The two optional P3 expansions identified above are now present and correct.

- `DICKSON_EXTENSION_COMPLETION.md`, lines 43--59, and `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 412--435, explicitly recover `U` and `a/U` from the block roots. The formulas follow from `sum_j zeta_m^{2j}=0` for `m>=3` and introduce no extra genericity assumption.
- `DICKSON_EXTENSION_COMPLETION.md`, lines 91--100, and `ALL_DEGREE_GLOBAL_COMPLETION.md`, lines 469--483, explicitly use injectivity of `F(Y) mapsto F(D_m(x,a))`. This correctly upgrades the affine identification of the composite to `R=A circ D_n`, with Dickson parameter `a^m`.

Audited source SHA-256 values after those edits:

```text
a5a3b39a90d4c2b44c09b1ffdc78a7c14e0ecf8cc201ea35c36cb4c5b9e3219c  DICKSON_EXTENSION_COMPLETION.md
d58272c1a007c6e1f15cea28b089af64df565c4ff8cc4878f1192de54461d04c  ALL_DEGREE_GLOBAL_COMPLETION.md
```

**Post-edit disposition: PASS unchanged.**
