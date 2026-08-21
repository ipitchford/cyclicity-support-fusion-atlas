# Release notes: v0.6.0-candidate

Date: **21 August 2026**  
Status: **public unrefereed theorem candidate relative to named imports**

## Main result

This additive successor promotes the v0.5 all-degree conjecture to a written
all-degree theorem candidate. Relative to named characteristic-zero
primitive-polynomial-monodromy and finite-projective-group classification
results, it classifies every complex polynomial phase with fixed seed `dx`
and cyclic rank at most three. It also classifies all proper rank-preserving
outer extensions.

The six families are powers, Dickson polynomials, quadratic-over-power phases,
cubic-over-power phases, indecomposable quartics, and the degree-twelve
quartic collision. The four extension mechanisms are power towers, aligned
Dickson towers, the aligned square of an odd-centred cubic-over-power phase,
and the cubic collision of the exceptional quartic.

## Substantive corrections

Adversarial review found the proposed uniform full-Kummer-kernel statement to
be false when `B != 0`, `A^2 = 4B`, and the exponent is even. The successor
preserves the counterexample, replaces the claim with a
coefficient-stratified theorem, and supplies an exceptional-stratum descent.

A separate possible gap for arbitrary mixed Dickson chains is closed by a
direct rational-function invariant-field proof for the full outer polynomial.
The bounded Dickson grid remains a regression control and carries no
all-degree evidentiary weight.

## Assurance supplied

- sixteen scoped Lean theorem controls and a placeholder scan;
- ten exact checks in a separate SymPy implementation;
- nineteen repaired Kummer checks;
- ordinary/optimised parity and thirteen semantic receipt mutations per mode;
- preserved bounded manifests and the unchanged v0.5 parent manifest;
- two separate internal model-assisted specialist re-audits after repair;
- a reproducible public-index literature snapshot; and
- static KaTeX rendering, PDF syntax/visual QA, and a fail-closed raw-TeX
  preflight.

These are producer-side controls. No unaffiliated reproduction, complete
formalisation, identified external specialist review, journal peer review, or
priority certification is claimed.

## Replay and identifiers

```bash
python3 run_global_completion_checks.py
python3 tools/build_all_degree_release.py verify
```

- Tag: `v0.6.0-candidate`
- Exact-version DOI: <https://doi.org/10.5281/zenodo.22045144>
- Concept DOI: <https://doi.org/10.5281/zenodo.22036029>
- Preserved predecessor DOI: <https://doi.org/10.5281/zenodo.22036030>
- Reader page: <https://evidencepress.org/releases/cyclicity-support-fusion-atlas/>
