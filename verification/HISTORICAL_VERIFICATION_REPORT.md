# Independent verification report: the cyclicity session bundle

**Target:** `cyclicity-complete-session-bundle-2026-08-19` (SHA-256 `fddde1b94e79fc0737c0392407783e6073ca2362864b2effb1f073cc6f103801`; 77 files).
**Verification dates:** 19–20 August 2026.
**Scope:** the support theorem q(P, dx) = |Σ(P)|, the Fourier block-fusion formula, the coefficient-atlas classification of complex polynomials of cyclic rank at most three, the extension atlas, and the bundle's computational receipts (claims C1–C10 of the claim ledger).
**Method:** line-by-line audit of the proofs, together with computational cross-examination using two implementations written independently of the bundle's code — series reversion by Newton iteration for Σ(P), and twisted de Rham Krylov reduction for q(P, dx) — under exact rational arithmetic and two independent 61-bit prime backends (2⁶¹ − 1 and 2⁶¹ − 31).

## Verdict

The core theorems are proved. The classification is refuted nowhere, and is verified exhaustively, by exact certificates, for every degree from 5 to 20. The general-degree proof of the classification contains one identified, reparable gap in §7.3, whose conclusion is nevertheless confirmed by exact computation for all quartic-lift moduli 2 ≤ m ≤ 7, so the gap first has unverified consequences at degree 32.

## The proved core (C1, C2, C4)

The formal-moment proof of the central identity (§§4–5 of the manuscript) survives a full audit: the μ-recursion cancellation, the connection compatibility, the triangular unit-determinant comparison matrix, and the falling-factorial Vandermonde, the last resting on the fact that no exponent α_r = −(r + n_r d)/d can be a non-negative integer because r ≢ 0 (mod d). Computationally, 278 direct comparisons between the two independent pipelines — all twelve §14 controls in exact arithmetic, 26 family instances across parameters, and 240 random polynomials of degrees 3–10, under both primes — produced zero mismatches. The branch-span theorem (6.1) and the fusion package (Theorems 8.1–8.2 with Corollaries 8.3–8.7) audit sound; the injectivity criterion and the monotonicity q(R∘Q) ≥ q(Q) were re-proved independently. The block-fusion rank formula (8.10) was verified numerically over every block subset of ten structured decompositions with singular-value gaps never below 10¹³, the intersection formula (8.13) on all block pairs, and heredity (8.12) exactly on 200 random compositions under both primes.

One presentational improvement follows from the audit. Given heredity (Corollary 8.3) and the deck symmetry, Σ((x⁴+ax)³) = {1, 7, 10} is forced: the deck symmetry confines the support to {1, 4, 7, 10}, heredity maps it onto Σ(x⁴+ax) = {1, 2, 3} under reduction mod 4, and 4 ↦ 0 lies outside that image. The class-4 vanishing is therefore a two-line theorem rather than a computational observation, and q((x⁴+ax)³) = 3 follows unconditionally from the proved core.

## The classification (C7): exhaustive certification to degree 20

The atlas's structural spine audits sound, including the primitive-monodromy elimination, whose two character computations (A₄ in the icosahedral A₅ representation; S₄ in the Klein PSL₃(2) representation, plain and sign-twisted) were verified by hand. The defect sits in §7.3: the derivation of identity (7.12), A(x^m + b) − A(b) = Q₀(x)^m, is circular. The honestly derivable fibre identity is a product of twisted quartic factors on which the x^{4m−3} coefficient vanishes automatically whenever m ∤ 3, so the intended contradiction presupposes its conclusion; the same structure affects (7.8). Everything feeding the argument is correct, and the concluding family checks exactly, but as written the general-m proof is incomplete.

The verification brackets this gap tightly by an independent route. Reparametrising each (degree, support) case by the low-order coefficients of the inverse series reduces it to at most three unknowns regardless of degree, because a centred polynomial's inverse-series coefficients F₂, …, F_d determine it triangularly and a support hypothesis with |S| ≤ 3 kills all but at most three of them. The confinement conditions then form a heavily overdetermined polynomial system in ≤ 3 variables, and the full solution variety is computable by exact Gröbner bases over ℚ. The sweep covers every degree from 5 to 20 and every admissible support pattern — 1,152 cases in total, the per-degree counts reconciling exactly with 1 + (d−2) + C(d−2, 2) — and every case closes with an exact certificate of one of three kinds: a vacuity certificate (the variety is the whole parameter space, matching a saturating family), a power-only certificate (every non-trivial parameter is nilpotent modulo the Gröbner basis), or a union certificate (radical membership of the product of the predicted components' defining polynomials). At degree 12 with support {1, 7, 10}, for instance, the conditions generate the principal ideal u₃(u₃² + 2u₆)³, whose zero locus is exactly the cubic-over-power plane united with the exceptional curve. Zero anomalies; zero cases uncertified. Atlas exhaustiveness therefore holds for all degrees ≤ 20 independently of the gapped group theory.

A targeted battery then attacked the §7.3 conclusion directly within its own ansatz. Writing A = y⁴ + βy² + γy (the decomposable branch being exactly γ = 0) and P = A(x^m + b), the deck symmetry confines Σ(P) to the four classes {1, m+1, 2m+1, 3m+1}, so rank ≤ 3 requires killing one of the last three. For each m ∈ {3, 4, 5, 6, 7} and each kill class, the vanishing conditions were saturated by γ ≠ 0 and solved exactly. At m = 3 the kill-class-4 variety is nonempty and contains the collision orbit (the control point (β, γ, b) = (−3/8, −1/8, 3/4), the shift-normalised A(z) = z(z+1)³, lies on the variety; its lift has exact support {1, 7, 10} to depth 240 and satisfies the orbit relations p₆ = p₉²/3, p₃ = p₉³/27); exactness of the m = 3 locus is separately settled by the sweep certificate at degree 12. At m = 4, 5, 6 and 7, every kill-class variety is empty after saturation — a conclusion robust to truncation, since additional conditions can only shrink a variety. Combined with the sweep at degrees 8 and 12, the §7.3 conclusion — indecomposable quartic lifts attain rank three only when m | 3 — is confirmed for all 2 ≤ m ≤ 7. Its first unverified instance is degree 32.

## Extensions (C8) and mass search

The extension-preservation loci were computed by exact Gröbner elimination over the outer coefficients, enumerating the surviving-class choices permitted by Corollary 8.6, for six representative inner polynomials and outer degrees 2 and 3. Every locus lands exactly on Theorem 9.1's list: empty for squares of quartics and for any extension of generic cubic-over-power or quadratic-over-power inners (Fermat rigidity, §10.2, confirmed); the single point R = y³ over x⁴ + x, re-verified at rank 3 in exact arithmetic; the single point r₁ = 0 for the aligned squares; and the Dickson cube over D₅(x, 1) collapsing to exactly (r₁, r₂) = (−3, 0), which is D₃(y, 1) — the aligned chain, recovered blind. The stratification boundaries verified on 300 random points: the cubic-over-power sublocus B = A²/4 has rank 2 at m = 2 and rank 3 at m = 3, and quartics have rank 3 exactly when B ≠ 0.

A mass search screened 56,610 binomials and trinomials of degrees 15–24 with a four-vector Krylov filter, confirmed all 378 survivors under a second evaluation point, a second prime and deep support computation, and classified every one as an atlas member. The census reconciles to the unit: 72 cubic-over-power hits at each degree divisible by three (36 trinomial + 18 + 18 binomial patterns), 18 quadratic-over-power binomials at each even degree, and no hits at the prime degrees 17, 19 and 23. Perturbation probes behave exactly as the certificates predict: (x⁴+2x)³ + x³ lights up the forbidden class 4 and jumps to rank 4. The bundle's own receipts replay: `verify_atlas.py` reproduces its pass receipt (SHA-256 `31b35e53…ffaf`) and `tests/test_fusion_support.py` passes end-to-end.

## Claim ledger

| Claim | Verdict | P(true) | Basis |
|---|---|---|---|
| C1 (q = \|Σ\|) | Proved & verified | 0.99 | Full audit; 278 zero-mismatch reconciliations |
| C2 (branch-span) | Proved | 0.99 | Independent proof + audit |
| C3 | Not audited | — | Nothing observed contradicts it |
| C4 (fusion) | Proved & verified | 0.99 | Audit; (8.10)/(8.12)/(8.13) verified |
| C5–C6 (strata mechanics) | Partially verified | ≈ 0.95 | Boundary loci verified on 300 points |
| C7 (exhaustiveness) | Verified for d ≤ 20; general proof gapped | 0.98 (d ≤ 20); ≈ 0.94 (all d) | 1,152 exact certificates; lift ansatz confirmed to m = 7 |
| C8 (extension atlas) | Verified on representative loci | ≈ 0.95 | Exact elimination matches Theorem 9.1 throughout |
| C9 (receipts) | Replayed, pass | 0.99 | Both receipt paths reproduce |
| C10 (novelty) | Out of scope | — | Separate assessment |

## Sanity checks

Three explicit reconciliations. Case counts: the sweep must analyse 1 + (d−2) + C(d−2, 2) supports per degree, predicting 79, 92, 106, 121 and 137 for degrees 14–18; exactly those were observed, and the optimised code path was regression-checked against the known-good degree-14 output before touching new degrees. Search census: the atlas predicts the hit table cell by cell (72/18/0 pattern above); observed exactly. Structural assertion: the theorem that class 0 never appears in a centred support was enforced as a live assertion inside every support computation — roughly 1,600 calls across all batteries — and never fired.

## Limitations

The positive certificates rest on truncated conditions; the logic closes for degrees ≤ 20 because any true rank-≤ 3 polynomial satisfies the truncated conditions and so lies in a certified variety whose members' supports are independently known, leaving implementation error (the verification engine, or SymPy's Gröbner arithmetic over ℚ) as the residual risk, mitigated by positive controls and by three mutually independent formulations agreeing wherever they overlap. Emptiness certificates are truncation-robust unconditionally. Rank computations specialise the parameter s, which is one-sided in principle; multiple evaluation points, two primes, exact spot checks and the identity cross-check mitigate. Degrees ≥ 21 outside the searched sparse families and the lift ansatz rest on the audited-but-gapped general argument. No independent human specialist has reviewed this work. Four external references cited by the bundle were not retrieved during verification and are marked below.

## Recommended repairs

Repair §7.3 by proving (7.12) directly from the fibre identity — the required lemma is that triviality of the scalar character forces the product of twisted factors to collapse to a single m-th power — or reroute: cite the degree-by-degree certificates for d ≤ 20 and the lift-ansatz certificates for m ≤ 7, supplying a fresh argument for m ≥ 8 only. Add the two-line heredity proof of Σ((x⁴+ax)³) = {1, 7, 10}. Record the certificate inventory (1,152 sweep cases of three certificate types; fifteen lift kill-class systems) as a formal artefact of the next atlas version.

## Sources

Bundle-internal, verified by checksum and read directly (19–20 August 2026): Evidence Press session bundle. (2026, 19 August). *cyclicity-complete-session-bundle-2026-08-19* [SHA-256 fddde1b9…3801]: CLAIM_LEDGER.md; SESSION_SYNTHESIS.md; MANUSCRIPT.md (v0.2.0-candidate) with CONTINUATION_ADDENDUM.md, src/fusion_support.py and tests/test_fusion_support.py; COEFFICIENT_ATLAS.md (v0.3.0-candidate) with code/exact_rank.py and code/verify_atlas.py.

Cited by the bundle; not independently retrieved during verification: Burda, Y., & Khovanskii, A. *Polynomials invertible in k-radicals.* https://arxiv.org/abs/1209.5137 · Müller, P., & Zieve, M. E. *On Ritt's polynomial decomposition theorems.* https://arxiv.org/abs/0807.3578 · Calbetó, J. *Finite subgroups of PGL(3,C).* https://arxiv.org/abs/2510.00718 · Álvarez, A., Bravo, J. L., & Mardešić, P. (2014). *Vanishing Abelian integrals on zero-dimensional cycles.* Proceedings of the London Mathematical Society. https://doi.org/10.1112/plms/pdt012

## Artefact contents

`lib.py` (independent support and rank engines with built-in structural assertions); `symconstr.py` (support-constrained symbolic reversion); `battery1.py`–`battery3.py` with logs `out1.log`–`out3.log` (identity, deep support, fusion); `battery4a_fast.py` with `out5_14.log`, `out15_16.log`, `out17_18.log`, `out19.log`, `out20.log` (exhaustive sweep, degrees 5–20); `battery4b.py` with `out4b.log` (quartic-lift kill-class systems, m = 3–7); `battery4c.py` with `out4c.log` (mass search and impostors); `battery4d.py` with `out4d.log` (extension loci); `RECEIPT.json` (machine-readable summary). Reproduction: Python 3 with SymPy; each battery is a standalone script exiting non-zero on any failure.
