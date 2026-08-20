# Claim ledger and correction history

| ID | Claim | Current status | Main dependency or limitation |
|---|---|---|---|
| C1 | \(q(P,dx)=|\Sigma(P)|\) for every polynomial phase | Proved in the candidate package by a direct formal-moment transform | Specialist verification of the formal algebra is still desirable |
| C2 | \(|\Sigma(P)|=\dim W_P^{\mathrm{red}}\) | Proved in the candidate package by Fourier decomposition of inverse roots | Same candidate-status boundary as C1 |
| C3 | Explicit fixed rapid-decay cycles give an invertible period matrix on a sector | Proved in v0.2 by uniform decay and Fourier–Gamma asymptotics | Full Stokes matrices at infinity are not computed and are not needed for the rank theorem |
| C4 | The Fourier-submatrix formula classifies sums, intersections and equality of block spans | Proved at the structural support level | A divisor profile describes an actual decomposition only when the relevant polynomial right factor exists |
| C5 | Equal block spans define a canonical coarser polynomial right factor | Proved in v0.2 using monodromy-invariant block coarsening | Depends on the standard decomposition/intermediate-field correspondence |
| C6 | All low-rank adjacent Ritt moves lie in eleven rank diamonds | Proved combinatorially for actual moves with total rank at most three | The table does not assert that each combinatorial row is polynomially realised |
| C7 | The displayed affine coefficient families exhaust \(q\le3\) | Complete theorem candidate in v0.3 | Relative to C1–C2 and imported primitive-monodromy, finite-projective-group and Ritt classifications |
| C8 | Proper rank-preserving extensions are powers, aligned Dickson chains, aligned rank-three squares and the quartic cubic collision | Complete theorem candidate in v0.3 | The finite-group reduction and quartic tetrahedron argument require closest external scrutiny |
| C9 | The exact computational examples have the stated cyclic ranks | Replayed and passed during consolidation | Computational controls validate examples and code, not the classification proof |
| C10 | Novelty or priority | Not established | Requires a dedicated prior-art search and external specialist assessment |

## Withdrawn or corrected intermediate claims

1. **Naive composition gap:** the proposed lower bound that block dimensions must add was refuted by \((x^4+x)^3\).
2. **Provisional affine atlas:** the initial list omitted Ritt-aligned fusion and was withdrawn.
3. **Additive Ritt inequality:** the proposed inequality
   \[
   r_a+r_b\ge r_0+r_2
   \]
   fails already for a rank-four support control; only the exact fibre-product constraint is retained.
4. **Single-contour Wronskian shortcut:** an ordinary Wronskian condition did not express the required \(\mathbf C(s)\)-linear non-annihilation and was removed.
5. **Unique rank-three extension claim:** the assertion that \((x^4+ax)^3\) was the only nontrivial rank-three preserving extension was corrected by the family
   \[
   (x^{3m}+bx^m)^2.
   \]

## Evidence hierarchy

- **Proof text:** manuscripts and addenda in the stage directories.
- **Exact implementation evidence:** symbolic twisted-de Rham Krylov reducers and support computations.
- **Independent-within-package fault controls:** clean-room finite arithmetic implementation and mutation tests.
- **Numerical consistency evidence:** Fourier–Gamma period-matrix spot check.
- **Missing assurance:** external expert review, independent reproduction, formal proof assistant encoding and priority search.
