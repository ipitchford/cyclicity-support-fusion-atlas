# Research quality gate: cyclicity application programme

## 1. Boundary and as-of date

As of 2026-08-21, this assessment covers EPOB-1, the named-chain fusion
reports, the Fraction-only replay challenge and the sealed `m=8`, degree-32
quartic-lift experiment. It assesses suitability as an unpublished specialist
candidate, not publication readiness of the parent theorem.

## 2. Claim and intended output

The claim is that four exact, reusable application artefacts have been built
and verified for rational polynomial phases with fixed seed `dx`, ending in a
prospective finite degree-32 elimination. The output types are software,
benchmark, verification challenge and finite mathematical experiment.

Object identity is fixed by the parent inverse support `Sigma(P)` in
`Z/deg(P)Z`, with trace class zero removed. Operator coefficients are ordered
from `D_s^0` upward. Support uses an affine normal form while displayed
operators apply to the original phase. The degree-32 boundary is the family
`A(x^8+b)`, not every polynomial of degree 32.

## 3. Novelty-gate handoff and prior-art status

Outcome: **BOUNDED UNCERTAINTY**. Order-aware creative telescoping, minimal
telescopers and order-degree trade-offs collide with established literature.
No exact collision was located for the inverse-support benchmark bridge in the
bounded primary-source search, but absence from that search is not priority
clearance. Permitted language is “a benchmark and application layer for the
parent inverse-support theorem candidate.”

## 4. Ex-ante and ex-post scores

| Dimension | Ex ante | Ex post | Confidence | Evidence-backed reason |
|---|---:|---:|---|---|
| Originality | 2 | 2 | medium | Broad order-aware telescoping is prior art; the specialised bridge was not located in a bounded search. |
| Significance | 3 | 3 | medium | A discriminating benchmark, exact order preflight, Ritt-view fusion diagnostics and prospective degree-32 point can guide CAS work and further conjectures. |
| Rigour | 3 | 3 | high | Exact arithmetic, frozen protocols, negative controls, ordinary/optimized parity and explicit finite boundaries pass; external reproduction is absent. |

Vector: **(2, 3, 3, internally checked, immature)**. The local geometric-mean
decision aid is

`Q = 100 * ((2/4)*(3/4)*(3/4))^(1/3) = 65.52`.

This scalar is not an official assessment score and does not replace the
dimension-specific evidence.

## 5. Evidence ledger

| ID | Evidence | Claim supported |
|---|---|---|
| PARENT | `MANIFEST.sha256`; parent commit `ce4e129…` | exact parent byte identity |
| ORACLE | `ORDER_ORACLE_MANIFEST.sha256` | order prediction and operator dependency |
| EPOB1 | `benchmarks/epob1_*`; `receipts/epob1_reference_run.json` | 10/10 order/support and 9/9 operator results |
| FUSION | `receipts/decomposition_fusion_*` | exact supplied chains and suffix-fusion agreement |
| REPLAY | `receipts/fraction_replay_challenge_receipt.json` | twelve Fraction-only exact checks |
| D32-LOCK | `experiments/degree32_preregistration_lock.json` | prospective protocol and runner identity |
| D32-RESULT | result digest `f72a3468…` | confirmed finite primary and secondary endpoints |
| MUTATION | `tests/test_application_programme.py` | rejection of four corruption classes |
| GATE | `run_application_programme_checks.py` | integrated ordinary/optimized replay and manifest checks |

## 6. Assurance status and limits

Status: **internally checked**. The package replays deterministic stages in
temporary directories and contains a no-SymPy Fraction path, but every check
was produced inside one programme. Independent reproduction, formal
verification, external peer review and a second-CAS derivation are not
established within this boundary.

## 7. Reception and maturity

Reception is **immature** because this extension is unpublished as of
2026-08-21. Citation, reuse and uptake metrics are not applicable and are not
set to zero. Maturity will be reconsidered no earlier than six months after a
persistent public release, unless a substantive external reproduction or
objection arrives sooner.

## 8. Red flags, missing evidence and disagreement

The main red flag is promotion of the finite `m=8` outcome into an all-degree
theorem. Missing evidence comprises an unaffiliated replay, a second CAS,
external mathematical proof review, full decomposition-lattice certification
and calibrated cross-machine benchmark data. No blinded second reviewer was
available, so reviewer disagreement is not measured rather than assumed zero.

## 9. Decision and reassessment

**Decision: candidate.** Accept for specialist circulation as a complete local
programme through the preregistered degree-32 experiment, with all assurance
boundaries attached. Do not describe it as independently verified, peer
reviewed, published or all-degree complete.

Next scheduled reassessment: **2027-02-21**, or earlier upon a third-party EPOB
submission, external degree-32 replay, specialist proof review, substantive
counterexample, or successor experiment.

## 10. Sources and metric definitions

Primary prior-art sources are Chen and Kauers, *Trading Order for Degree in
Creative Telescoping* (arXiv:1108.4508); Bostan, Chen, Chyzak, Li and Xin,
*Hermite Reduction and Creative Telescoping for Hyperexponential Functions*
(arXiv:1301.5038); and Bostan, Lairez and Salvy, *Creative telescoping for
rational functions using the Griffiths-Dwork method* (arXiv:1301.4313).

Originality, significance and rigour use the 0–4 research-quality-gate rubric.
Assurance and reception are recorded separately. `Q` is the geometric mean of
the three normalised core dimensions. Benchmark medians are local wall-clock
descriptions and are not quality, complexity or performance-superiority
metrics.

