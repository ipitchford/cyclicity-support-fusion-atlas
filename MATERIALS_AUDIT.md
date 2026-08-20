# Materials audit and chronological reconstruction

All non-metadata files in the supplied `cyclicity-complete-plus-atlas` source
folder were inventoried. Archives were extracted into a fresh workspace;
supplied archives were not modified.

## 17 August: parent-release assessments

### Fixed-Seed Cyclicity Loci for Polynomial Exponential Periods.md

This older assessment correctly separates unconditional Krylov-rank strata from three analytic questions: complete rapid-decay realisation, the order of one selected contour period, and the original finite-(N) Cauchy contour. Its main open dependency is later replaced by the formal-moment theorem and fixed-cycle determinant. Its warning about single-cycle annihilation remains valid and is retained in the new manuscript.

### Fixed-seed cyclic rank as reduced inverse-root span.md

This assessment identifies \((x^4+x)^3\) as the generating fusion example,
proposes infinity-character support, and lays out the decomposition/Ritt
classification programme. It explicitly warns that Ritt theory alone cannot
turn arbitrary root relations into decompositions. The final universal fusion
theorem answers the structural part; the proposed affine classification
remains exposed at the exceptional-projective step.

## 19 August: staged session bundle

Archive SHA-256:

`fddde1b94e79fc0737c0392407783e6073ca2362864b2effb1f073cc6f103801`

The external `.sha256` sidecar matches the archive. The internal stage archives and manifests were inventoried.

### v0.1.0 unconditional fusion

The first manuscript supplies the formal-moment map, support theorem, root-span equality, fixed-cycle argument, and Fourier fusion formula. Its internal review already calls for checking the formal completion, isomorphism, and Ritt invariance.

### v0.2.0 unconditional fusion

This revision adds the explicit Fourier–Gamma determinant, canonical fusion quotient, chain-defect formula, Ritt fibre-product inequality, and eleven low-rank diamonds. It corrects the moving-cycle formulation and a false additive Ritt inequality. This is the strongest universal source and is preserved verbatim under `source-history/`.

### v0.3.0 coefficient atlas

The atlas proposes the all-degree rank-\(\le3\) families and four
rank-preserving mechanisms. It corrects the earlier claim that the
quartic-cubic collision was the only nontrivial rank-three extension by adding
aligned squares. Its original computational controls validate selected
families and mutations, not exhaustiveness.

### Session synthesis and claim ledger

The ledger is unusually useful because it preserves withdrawn claims: naive block additivity, the provisional atlas, the false additive Ritt inequality, a single-contour Wronskian shortcut, and uniqueness of the quartic rank-three extension. These corrections are retained in the present assurance boundary.

## 20 August: verification artefact

Outer archive SHA-256:

`4017cd9623fffb6813a591d85d9e072ca003741801f0da9c0999d41e7d8e27d1`

The nested verification archive and its sidecar match. The report audits the
universal core positively but identifies a circular step in the
coefficient-atlas quartic lift. Its exact-arithmetic sweep covers degrees
5–20, and targeted lift elimination covers \(m=2,\ldots,7\). The report
itself states that the first uncovered consequence is degree 32. This finding
controls the new release decision.

The verifier is algorithmically separate but was produced by another AI system inside the same research programme. It is not an unaffiliated reproduction.

## 20 August: ODE demonstration

Archive SHA-256:

`0d43abd32973085a2d8a637e3143cb54ea9e7aa3eb50878754d201c99bdb93c4`

The script derives exact operators and checks numerical residuals for representative real-line integrals. It supports the order-oracle application. It does not fail closed when an expected order or residual fails and uses `assert` in a load-bearing reduction. It is retained as exploratory code only.

## 20 August: Gavrilov–Pakovich-labelled application

Archive SHA-256:

`dcaceda7c5bd1ef0c7611677e7a01e1d962cc7146b09dbf1a265ee276c5395f1`

The archive contains `openproblem.py` and one log, but not the imported `lib.py` or a proof write-up. Current rerun, with `lib.py` supplied from the verifier, ends `criterion check: REVIEW` while returning exit status zero. The borderline branch-labelling case shows that the numerical threshold is not a safe oracle. Exact centre-element calculations are promising, but the folder does not justify the label “solution.”

## 20 August: Laurent-polynomial moment bundle

Archive SHA-256:

`d2232daababf71a24d020d4c1a12a61228f80dcb9ec2baa7c4901a2b72503d67`

The bundle proposes a local-branch residue criterion, small-bidegree
certificates, and a complete \((2,2)\) locus. Normal and optimized runs
complete. However, several printed controls show observed excess dimensions
different from the stated expectations without failing, and the README
records prior spurious loci caused by insufficient minors and single-prime
blindness. The project is methodologically relevant but should remain
separate until the baseline module count and fail-closed tests are reconciled.

## 20 August: supplied applications and significance essays

The applications essay contains the valuable ODE-order dictionary and plausible links to creative telescoping, zero-cycle moment problems, catastrophe integrals, and exponential motives. Its probability estimates of novelty are not evidence and have been removed from the new paper.

The significance review already gives the correct high-level diagnosis: the formal support and Fourier fusion theorems are the strongest conceptual results; the coefficient atlas has four-star upside but depends on compressed group and lift arguments. The later verification report turns that general concern into one precise proof gap.

## Metadata files

`.DS_Store` files were inventoried and excluded from the research package because they contain no mathematical content.

## Final disposition

| Material | Disposition |
|---|---|
| Universal v0.2 theorem | Main paper, specialist-review candidate |
| v0.1 and correction history | Preserved source history |
| Atlas through degree 20 | Finite computer-assisted theorem candidate with fail-closed current-byte gate |
| All-degree atlas | Conjecture; HOLD_FOR_REPAIR |
| ODE application | Exploratory appendix |
| Zero-cycle/Gavrilov–Pakovich application | Exploratory; not a claimed solution |
| Laurent moment project | Separate exploratory research line |
