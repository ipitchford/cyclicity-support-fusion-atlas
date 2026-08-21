# Exponential-Period Order Oracle: assurance record

Status: **complete unpublished research extension; unrefereed**

## Evidence vector

| Dimension | State | Evidence | Boundary |
|---|---|---|---|
| Mathematical basis | inherited theorem candidate | parent Theorems 5.2 and 7.3; parent Section 14.1 | ordinary proof checking remains external |
| Exact operator derivation | passed | first Krylov dependence over \(\mathbf Q(s)\), primitive \(\mathbf Z[s]\) coefficients, exact zero residual | same production implementation family as the parent symbolic reducer |
| Separate symbolic derivation | passed within programme | six operators independently reduced over \(\mathbf Q[u]\), \(u=1/s\), without importing either production module | still SymPy-based and not unaffiliated reproduction |
| Exact benchmark | passed | eight frozen cases, including rank-drop and rank-creation negative controls | finite benchmark, not exhaustive software verification |
| Generic degree-12 contrast | passed | exact rational specialisations attain ambient rank eleven; exceptional phase has frozen order-three operator | no frozen symbolic order-eleven operator |
| Numerical period check | passed | seven convergent real-line quadrature residuals below \(10^{-12}\) | numerical spot control only |
| Mutation detection | passed | altered coefficient rejected before and after forged outer digest | mutation coverage is finite |
| Optimised-mode parity | required by gate | ordinary and `python -O` receipts must match byte-for-byte | one Python/SymPy implementation environment |
| Published-parent integrity | required by gate | all paths in the frozen v0.5 manifest retain their recorded digests | permits additive unlisted successor files |
| Independent external replay | not established | none supplied | no unaffiliated actor |
| Specialist/editorial review | not established | internal research review only | no journal decision or specialist sign-off |
| Formal verification | not established | none supplied | no proof assistant or axiom footprint |
| Novelty and priority | inherited open boundary | no new literature audit for the software formulation | non-location would not prove priority |
| Publication | not undertaken | local successor working tree only | no new Git tag, DOI, GitHub release or Evidence Press page |

## Claim ceiling

The extension may be described as an exact implementation and certificate
system for the parent manuscript's generic minimal-ODE-order corollary. It may
not be described as independently verified, peer reviewed, formally verified,
published, or as demonstrating a speedup in a third-party computer-algebra
system.

The operator annihilates every rapid-decay period covered by the parent
analytic construction. Its order is minimal for a generic functional on the
complete solution space. No universal minimal-order claim is made for every
individual cycle.

## Trust base

- the parent formal-moment and Fourier--Gamma period arguments;
- the phase parser and affine-normalisation map;
- exact twisted reduction and Krylov rank computation;
- inverse-series support computation;
- operator denominator clearing and primitive normalisation;
- Python 3.14, SymPy 1.14 and their exact rational arithmetic;
- benchmark specification, runner and frozen receipts.

The numerical layer additionally trusts mpmath quadrature and is excluded from
the theorem-evidence layer.
