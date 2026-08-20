# Fixed-Seed Cyclicity Loci for Polynomial Exponential Periods 

## Judgement

**Promote the analytic programme to first scientific priority, but correct the dependency claim.**

A failure of the analytic bridge would **not invalidate the algebraic stratification results themselves**. The determinantal ideals, quartic and quintic factorisations, fibre ranks and invariant-submodule statements live in the twisted de Rham quotient and are unconditional algebraic claims. The release explicitly says that the quotient relation is unconditional and that the corresponding period equation requires a horizontal rapid-decay cycle, differentiation under the integral sign and vanishing boundary terms. ([GitHub][1])

What failure would invalidate is considerably more important for the intended application:

| Claim                                                                                    | Dependence on the analytic bridge                                               |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Rank strata of the algebraic Krylov matrix                                               | None                                                                            |
| Rank strata of a **complete basis of rapid-decay periods**                               | Requires the de Rham–rapid-decay comparison and uniform differentiation         |
| Minimal differential order of one **specified contour period**                           | Additionally requires that contour not to annihilate part of the algebraic span |
| Interpretation of the quartic degeneration as the limit of the original Cauchy integrals | Requires uniform contour deformation and tail control                           |
| Any large-(N) consequence for the Furter construction                                    | Requires all of the above, plus a quantitative nonvanishing bound               |

Thus the correct diagnosis is: **the algebra survives, but its analytic meaning and its use in the original problem remain conditional**.

## The phrase “stationary-phase bridge” conceals two different theorems

### 1. Algebraic de Rham ↔ rapid-decay periods

For a polynomial exponential connection, one needs to realise the quotient

[
\mathcal H_\Phi
===============

A[x]/{q_x+\Phi_xq}
]

as the dual of a rapid-decay homology local system. This is not principally a stationary-phase theorem. It is an irregular de Rham comparison theorem.

The general foundation is strong. Bloch and Esnault proved a perfect pairing between irregular de Rham cohomology and rapid-decay homology on algebraic curves; Hien extended the duality to flat algebraic connections in arbitrary dimensions; Hien and Roucairol represented solutions of exponential Gauss–Manin systems by rapid-decay period integrals. ([Numdam][2])

That literature makes a wholesale failure of this first bridge unlikely. The missing result is a **clean family-specific theorem with uniform hypotheses**, not the invention of rapid-decay homology from scratch.

The exact target should be:

> **Uniform period-realisation theorem.**
> Let (U) be a simply connected parameter chamber for a fixed-degree polynomial phase (\Phi(x;\theta)), with the leading coefficient bounded away from zero. Choose a flat rapid-decay basis
> (\Gamma_1(\theta),\ldots,\Gamma_r(\theta)), where (r=\deg_x\Phi-1), and the monomial de Rham basis (e_1,\ldots,e_r). Then:
>
> 1. the period matrix
>    [
>    P_{\alpha i}(\theta)
>    =\int_{\Gamma_\alpha(\theta)}
>    e_i(x)e^{\Phi(x;\theta)},dx
>    ]
>    is invertible;
> 2. all derivatives needed for the Krylov calculation may be passed under the integral uniformly on compact subsets of (U);
> 3. twisted-exact terms integrate to zero uniformly;
> 4. for the algebraic Krylov matrix (M_k), the analytic derivative matrix satisfies
>    [
>    Y_k=P,M_k.
>    ]

It follows immediately that

[
\operatorname{rank}Y_k(\theta)
==============================

\operatorname{rank}M_k(\theta).
]

That identity would transfer the algebraic determinantal strata exactly to the **complete period system**.

For the quartic and quintic cases, the analytic estimates should be elementary enough to make the theorem self-contained. On each fixed decay sector one seeks a bound

[
\Re \Phi(x;\theta)\le -c|x|^m+C
]

uniformly for (\theta) in a compact chamber. Every finite collection of parameter derivatives is then dominated by

[
C_N(1+|x|^N)e^{-c|x|^m},
]

which is integrable. The same estimate kills the endpoint in

[
D_\Phi(q)e^\Phi,dx=d(qe^\Phi).
]

General theory can certify the topology and perfectness; these explicit bounds can certify the exact family used by the release.

### 2. Original Cauchy contour ↔ quartic rapid-decay class

This is the genuinely load-bearing and higher-risk bridge. The original source does not merely need some rapid-decay cycles to exist. It needs the **particular finite-(N) coefficient contour** to converge, after deformation and scaling, to a known nonzero combination of them.

For the phase

[
\Psi(W)=W^4-\frac32KW^2+bW
]

on the constrained transition curve

[
R(K,b)=-3K^3+K+3b^2=0,
]

the source release already identifies the four indispensable tasks:

1. Stokes-compatible continuation of the principal and local cycles;
2. a lower bound for
   [
   \max{|\mathcal Z_0|,|\mathcal Z_1|},
   \qquad
   \mathcal Z_0=\int_{\Gamma_0}e^\Psi dW,\quad
   \mathcal Z_1=\int_{\Gamma_0}\Psi e^\Psi dW;
   ]
3. a contour-deformation and tail error smaller than that bound;
4. compatible estimates in the adjoining double-saddle charts. 

The closure theorem should therefore have a **relative-error form**, not merely a pointwise asymptotic expansion. After restoring the release’s normalising factors, one wants something of the form

[
\mathbf J_N(K,b)
================

B_N(K,b)
\begin{pmatrix}
\mathcal Z_0(K,b)[2mm]
\mathcal Z_1(K,b)
\end{pmatrix}
+
\mathbf E_N(K,b),
]

with

[
|\mathbf E_N(K,b)|
\le
\eta_N,L(K,b),
\qquad
\eta_N\longrightarrow0,
]

where

[
L(K,b)\le
\max{|\mathcal Z_0(K,b)|,|\mathcal Z_1(K,b)|}
]

is explicit and positive throughout the relevant compactified transition family, including equal-critical-value fibres and the boundary charts.

A formal quartic limit without this relative inequality cannot establish nonvanishing. An absolute (o(1)) error is insufficient when the limiting period itself can approach zero.

## Stokes data should be narrowed to the part actually needed

Full Stokes matrices are valuable, but they are **not the first logical gate for the algebraic rank strata**. Across a Stokes wall, a rapid-decay basis changes through an invertible transition matrix (S):

[
P^{+}=S P^{-}.
]

Therefore

[
\operatorname{rank}(P^{+}M_k)
=============================

\operatorname{rank}(P^{-}M_k).
]

The complete-system rank is basis-invariant. Stokes matrices record the extended monodromy data of an irregular differential equation, but rank preservation only needs invertibility. ([Springer][3])

Explicit Stokes information becomes essential when one asks a different question:

> Which linear functional on the rapid-decay period space is represented by the original coefficient contour after every wall crossing?

That named contour can undergo cancellations even though the complete period matrix remains nonsingular. Consequently, the immediate target should be **Stokes-compatible tracking of the original contour class**, not a comprehensive tabulation of every Stokes multiplier.

## Recommended order of work

### Gate 1 — Local analytic comparison

Prove the uniform rapid-decay basis, perfect period pairing, contour differentiation and integration-by-parts theorem for the depressed quartic and odd quintic families. Then verify computationally at several regular parameter values that the numerical period derivative matrix and the exact Krylov matrix have the same rank.

This closes the analytic interpretation of the stand-alone cyclicity release.

### Gate 2 — Identify the original contour class

Start from the finite-(N) Cauchy contour before scaling. Deform it with explicit endpoint sectors and orientations. Record its coordinates in a rapid-decay basis in every chamber and the transition rule across every relevant Stokes wall.

This is where a genuine obstruction could first appear.

### Gate 3 — Prove non-annihilation

Prove that the resulting class does not annihilate the rank-two span generated by the limiting amplitudes. Equivalently, establish that (\mathcal Z_0) and (\mathcal Z_1) do not vanish simultaneously on that class, with quantitative control at the exceptional and boundary fibres.

A negative theorem here would also be substantial: it would show that the algebraic rank-two result cannot supply the intended Furter bound for the original contour.

### Gate 4 — Uniform finite-(N) transfer

Only after Gate 3 should the programme complete the tail estimates, double-saddle matching and projective-chart gluing. The required error threshold is now defined by the lower bound from Gate 3.

Degree-six or degree-seven extensions, multivariate algorithms, rational amplitudes and broad numerical period tooling should wait. An independent replay of the existing algebra should continue in parallel because it protects against proving an analytic bridge to an incorrect matrix; it is assurance rather than downstream refinement.

## Decisive failure modes

The programme should declare a meaningful negative result if it establishes any of the following:

* the scaled Cauchy contour becomes zero in the relevant rapid-decay homology;
* the contour class lies in the annihilator of the algebraic rank-two submodule at a relevant fibre;
* (\mathcal Z_0=\mathcal Z_1=0) for that class somewhere on the compactified transition family;
* Stokes continuation produces a cancellation that destroys the required uniform lower bound;
* tail or adjoining-chart contributions remain of the same order as the quartic contribution.

None would refute the determinant or rank calculations. Each would refute the proposed route from those calculations to a finite-(N) nonvanishing theorem.

## Sanity check

For a full rapid-decay basis, (P) is square and invertible, so

[
\operatorname{rank}(PM_k)=\operatorname{rank}(M_k).
]

For one selected contour, however, the period derivatives form only one row,

[
\lambda P M_k,
]

and multiplication by that row functional can reduce rank. Thus even a perfect de Rham–rapid-decay comparison does **not** prove that the original contour period has the generic algebraic differential order. The contour-class and non-annihilation theorem remains indispensable.

A sharper restatement of the priority claim is therefore:

> **Promote the analytic realisation to first priority, with the original-contour identification and quantitative nonvanishing bound as the decisive target. The algebraic determinantal strata remain unconditional; what depends on this work is their interpretation as period ranks and their use in the large-(N) stationary-phase argument. Full Stokes matrices are secondary to tracking the relevant contour class and proving that the deformation error remains below its period lower bound.**

## Sources

### Evidence Press releases

Anonymous. (2026, August 8). *Fixed-seed cyclicity loci for polynomial exponential periods* (Version 0.2.1). Evidence Press. [https://evidencepress.org/releases/cyclicity-loci-exponential-periods/](https://evidencepress.org/releases/cyclicity-loci-exponential-periods/)

Anonymous. (2026, August 1). *Irreducible pushforwards and constrained quartic transitions: Two reusable methods from a study of Furter’s (R(3)) conjecture*. Evidence Press. [https://evidencepress.org/releases/irreducible-pushforwards-quartic-transitions/](https://evidencepress.org/releases/irreducible-pushforwards-quartic-transitions/)

### Rapid-decay homology and exponential periods

Bloch, S., & Esnault, H. (2004). Homology for irregular connections. *Journal de Théorie des Nombres de Bordeaux, 16*(2), 357–371. [https://doi.org/10.5802/jtnb.450](https://doi.org/10.5802/jtnb.450)

Hien, M. (2009). Periods for flat algebraic connections. *Inventiones Mathematicae, 178*(1), 1–22. [https://doi.org/10.1007/s00222-009-0185-7](https://doi.org/10.1007/s00222-009-0185-7)

Hien, M., & Roucairol, C. (2008). Integral representations for solutions of exponential Gauß–Manin systems. *Bulletin de la Société Mathématique de France, 136*(4), 505–532. [https://doi.org/10.24033/bsmf.2564](https://doi.org/10.24033/bsmf.2564)

### Stokes structures

Sabbah, C. (2013). *Introduction to Stokes structures*. Springer. [https://doi.org/10.1007/978-3-642-31695-1](https://doi.org/10.1007/978-3-642-31695-1)

[1]: https://github.com/ipitchford/cyclicity-loci-exponential-periods/blob/main/MANUSCRIPT.md "cyclicity-loci-exponential-periods/MANUSCRIPT.md at main · ipitchford/cyclicity-loci-exponential-periods · GitHub"
[2]: https://www.numdam.org/articles/10.5802/jtnb.450/ "Homology for irregular connections"
[3]: https://link.springer.com/book/10.1007/978-3-642-31695-1?utm_source=chatgpt.com "Introduction to Stokes Structures | Springer Nature Link"
