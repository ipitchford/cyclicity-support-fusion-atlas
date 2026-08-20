# Current-target verification report

Target: **v0.5.0-candidate payload identified by the complete
`MANIFEST.sha256` inventory**

Status: **PASS_WITH_NOTES**

This report supersedes the current-use role of the earlier C1–C10 report,
which is preserved as `HISTORICAL_VERIFICATION_REPORT.md` with its original
77-file target and subjective confidence fields.

## Claim results

| Current claim | Result | Evidence ceiling |
|---|---|---|
| T1, universal cyclic rank equals inverse support | PASS on written proof and scoped replay | unrefereed theorem candidate |
| T2, inverse support equals reduced root span | PASS on written proof | unrefereed theorem candidate |
| T3, Fourier–Gamma period determinant | PASS on written proof; numerical spot control passes | unrefereed theorem candidate |
| T4, Fourier block-sum ranks | PASS on written proof and structured cases | unrefereed theorem candidate |
| T5, canonical coarser factor | PASS on expanded intermediate-field and one-pole proof | unrefereed theorem candidate |
| T6, eleven low-rank Ritt diamonds | PASS on explicit table, proof and Fraction audit | unrefereed theorem candidate |
| F1, affine atlas through degree twenty | PASS under stated exact-computation trust boundary | finite computer-assisted theorem candidate |
| C1, all-degree affine atlas | OPEN | conjecture; degree 32 first uncovered quartic lift |
| A1, generic minimal ODE order | PASS with generic/non-annihilation boundary | corollary |
| D1–D2, zero-cycle and Laurent directions | NON-GATED | exploratory |

## Deterministic evidence

- The full atlas runner records 1,152 cases: 45 full-family, 884 power-only,
  223 union, zero anomaly and zero missing certificate.
- Every case has an ideal digest, Gröbner digest, outcome and reduction
  witness in `receipts/atlas_case_records_d5_20.json`.
- Ordinary and optimised runs must regenerate byte-identical receipts matching
  `RELEASE_EXPECTATIONS.json`.
- Injected anomaly, missing-certificate, support, Fourier, receipt and manifest
  mutations must be rejected.
- Structural tests, exact Fraction controls, 278 support/rank comparisons,
  ten fusion cases and 200 two-prime heredity pairs are included in the
  one-command runner.
- A clean extraction of the frozen preliminary archive completed the entire
  ordinary and optimised runner, including both 1,152-case sweeps, receipt
  parity and frozen-hash comparison, and returned `RELEASE GATE PASS`.

## Residual boundaries

The finite computation trusts the inverse-series construction,
source-to-encoding bridge, case generator, Python runtime and SymPy's exact
rational Gröbner arithmetic. No proof assistant or second computer algebra
system checks all 1,152 cases. The verification is within the commissioned AI
programme and is not unaffiliated reproduction.

The all-degree atlas is not promoted. The earlier circular descent is retained
as an objection, not hidden by the successful finite sweep.
