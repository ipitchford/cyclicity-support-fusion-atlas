# Laurent polynomial moment problem: computational toolchain and certificates

Session bundle, 20 August 2026. Python 3.12.3, SymPy 1.14.0. All scripts run
standalone from this directory (they import only each other and the standard
library plus SymPy).

## Problem and reduction

For a Laurent polynomial L(z) = Σ_{i=-m}^{n} c_i z^i with c_{-m} = 1, describe
all Laurent polynomials q with Res_0(L^k q) = 0 for every k ≥ 0.

Reduction theorem (proved in-session, two lines of formal residue calculus):
writing φ(τ) = τG(τ) for the local branch of L at z = 0 with L(φ(τ)) = τ^{-m}
and G(0) = 1, the polynomial q = Q′ solves the moment problem iff
[τ^{me}](Q∘φ) = 0 for every e ≥ 1. The solution set 𝔐(L) = {Q} is a free
ℂ[L]-module of rank between 1 and m+n; rank 1 iff every solution is trivial
(q = A′(L)L′). Mechanisms (complete on the composition side by a pole argument):
M2, L = A∘W with A polynomial, W Laurent, gives ℂ[W] ⊆ 𝔐; M3, L = A(z^d),
frees every exponent class other than 0 mod d. Both need their degree parameter
to divide gcd(m,n), so coprime bidegrees are mechanism-free.

## File inventory

- lib.py — shared arithmetic and the primes P61 = 2^61 − 1, P2 = 2^61 − 31
  (dependency; originally from the cyclicity engine).
- laurent.py — the numeric engine: branch series G (Newton), G-power cache,
  condition matrices, exact and mod-p ranks, module_dim(cdict, m, n, M, N, p, E)
  returning (dim, excess) on box[−M, N]. Running it directly executes the
  control suite (mechanism recounts, generic-rank certificates).
- laurent_cls.py — first-generation symbolic classifier (lex Gröbner over
  shape-normalised solutions). WARNING: executes its classification runs at
  import; import lcls.py instead when you only want the functions.
- lcls.py — functions-only copy of the symbolic series machinery
  (sym_branch_G, sym_smul, sym_sinv, classify).
- laurent_cls2.py — shape-system builders (shape_rows, topshapes, botshapes)
  and the first minors-based classify_shape.
- laurent_cls3.py — pivot-guided decide_shape plus the generic number-field
  class NF (ℚ[x]/(f) with Fraction vectors and xgcd inversion) and
  nf_solve_shape for exact pointwise decisions over algebraic parameter points.
- laurent_cls4.py — final-form row-shuffled box-minors classifier
  (box_classify). Excess in box[−M, N] iff rank of the full condition matrix on
  slots k ≠ 0 falls below r* = (M+N) − min(⌊M/m⌋, ⌊N/n⌋); the excess locus lies
  in V(any set of r*-minors); ideal = (1) certifies emptiness for all
  parameters. Row order is shuffled per sample point so successive minors draw
  on different condition depths.

## Certified results (normalisations c_{-m} = c_n = 1, c_0 = 0)

Two rigour lemmas underpin the grades. Monotonicity: A(L) of L-degree K has
z-top exactly nK and z-bottom exactly −mK, so excess is monotone in the box and
only the largest certified box per bidegree matters. Mod-p soundness: condition
entries are p-integral and rank only drops under reduction, so zero excess mod
one large prime certifies the exact statement at that parameter point.

- (1,1): 𝔐 = ℂ[L] for all parameters; certified to box[−4,4] (the only
  candidate locus is the bidegree-degeneration boundary).
- (1,2): 𝔐 = ℂ[L]; certified to box[−4,6] (candidate V(a); a = 0 refuted
  exactly).
- (1,3): 𝔐 = ℂ[L]; certified to box[−3,6] (chain: minors ⟹ excess ⊆ parabola
  a1 = −a2²; restriction onto the parabola ⟹ ⊆ origin; L = 1/z + z³ refuted
  exactly).
- (1,4): 𝔐 = ℂ[L]; certified to box[−2,4] (double restriction telescoped
  V(a1 + a2·a3) → V(2a2 + a3²) → origin, refuted exactly). Box[−3,5]: excess
  bounded by a quintic surface; origin plus twenty on-locus points across two
  primes refuted (sampled grade).
- (2,3): 𝔐 = ℂ[L]; box[−2,3]: excess bounded by an octic surface; twenty-two
  on-locus points across two primes refuted (sampled grade).
- (2,2): complete theorem. Excess locus = {b = a} ∪ {b = −a}, exactly the
  decomposability locus L = A(z ∓ 1/z + w0): the inclusion certified by the
  purified minors ideal V((a−b)^4 (a+b)^4), the reverse inclusion by the trace
  lemma. On the locus 𝔐 = ℂ[W] exactly (exact nullspace {1, W} at depth 40,
  dimension agreement at four nested boxes, conditions verified to depth 60 mod
  two primes, and direct SymPy residue checks through an independent code
  path). Exhibit: L = z^{-2} − 3/z + 3z + z², W = z − 1/z, q = 1 + z^{-2}.

Headline: the Laurent polynomial moment problem is solved for every bidegree
with m + n ≤ 5 at the grades above; every solution is q = A′(L)L′ except at
(2,2) on b = ±a, where solutions are exactly q = (B∘W)′. No exotic solutions
exist in this range, consistent with the Pakovich–Pech–Zvonkin exotic living at
higher bidegree.

## Methodological notes (failure modes found and closed)

1. Shape-wise augmented-rank tests are invalidated by an exact column relation
   (the conditions functional kills L itself); the box-minors reformulation in
   laurent_cls4.py removes shapes entirely.
2. An undersized minor pool manufactured a spurious "exotic" at a1² = −2 in
   bidegree (1,3); the pointwise stage refuted it (excess 0 mod two primes
   where −2 is a residue; 18 inconsistencies in the exact ℚ(√−2) system).
   Lesson: a single-prime scan is blind to any locus whose discriminant is a
   non-residue modulo that prime — vary primes. (−2 is a non-residue mod P61
   but a residue mod P2.)
3. Deterministic pivoting reuses shallow condition rows whose minors vanish
   where truncated rank dips before deeper rows recover; per-sample row
   shuffling (laurent_cls4.py) fixes this and dissolved the ghost factor
   (ab − 2) at (2,2).

Soundness: truncated conditions are necessary, so computed dimensions only
overcount; every zero-excess conclusion is certificate-grade at its box.

Known quirk: laurent.py's Newton loop failed once on a Fraction coefficient
(c_{-1} = 1/2 at a (2,2) test point) in the exact path; unexplained, sidestep
with integer-coordinate test points.

## Reproduction

    python3 laurent.py          # engine controls and generic-rank certificates
    python3 laurent_cls4.py     # (2,2) box classification, row-shuffled minors

Pointwise decisions: laurent.module_dim(L_dict, m, n, M, N, p_or_None, E).

## Sources

Pakovich, Pech, & Zvonkin (2010), arXiv:0910.2691. Pakovich & Muzychuk (2009),
arXiv:0710.4085. Álvarez, Bravo, & Christopher (2014), Ergodic Theory Dynam.
Systems 34(1), 1–20. Álvarez, Bravo, & Mardešić (2013), arXiv:1202.5896.
Bravo, Mardešić, Novikov, & Pontigo-Herrera (2025), arXiv:2312.03081.
