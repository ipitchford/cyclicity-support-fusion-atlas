# Research Quality Gate: uniform structural repair

## 1. Boundary

- Assessment ID: `cyclicity-uniform-structural-2026-08-21`
- As-of date: 2026-08-21
- Assessor: anonymous internal QA
- Decision: whether the structural repair closes the two targeted obligations
  and should enter the candidate package
- Boundary: monodromy/scaling and uniform Newton coefficients, not the entire
  atlas.

## 2. Claim and intended output

The output proves the equality of radical scaling powers under the full local
`S_3/S_4` action and proves the cubic/quartic Newton obstruction for every
natural exponent.  It is a mathematical proof and formal-proof certificate
for specialists evaluating the all-degree coefficient atlas.

## 3. Novelty handoff

The existing gate remains **BOUNDED UNCERTAINTY**.  No absolute priority claim
is made.  A refreshed formalisation-specific prior-art search remains required
before publication-based originality language.

## 4. O/S/R assessment

| Dimension | Retrospective prior | Ex-post | Confidence | Evidence-backed justification |
|---|---:|---:|---|---|
| Originality | 2 | 2 | medium | Structural synthesis appears distinctive within the bounded search, but formalisation-specific priority was not refreshed. |
| Significance | 3 | 3 | high | Removes the finite-exponent conditionality from the decisive cubic/quartic descent. |
| Rigour | 3 | 3 | high for stated boundary | Complete written derivation, 25 kernel-checked theorems, exact statement mapping, sealed replay, and adversarial mutations. |

Local decision aid: `Q=65.5`.  This is not an official assessment score.

## 5. Evidence ledger

| Criterion | Evidence | Status |
|---|---|---|
| Scaling proof | `ALL_DEGREE_STRUCTURAL_REPAIR.md`, Sections 2–3 | complete candidate proof |
| Uniform coefficients | same, Sections 4–6 | complete candidate proof |
| Kernel verification | `formal/lean/CyclicityUniform.lean` | 25 theorems pass |
| Source identity | `formal/uniform_verification_lock.json` | sealed |
| Semantic integrity | verifier plus seven forged mutations | pass |
| Independent local identities | predecessor Singular/Lean successor | pass |

## 6. Assurance

- Status: formally verified for the algebraic/combinatorial structural core.
- Independence: internal; same producer and statement selector.
- Replay: deterministic same-environment Lean replay.
- Limits: the complex monodromy interpretation is proved in prose but not
  encoded topologically; several inherited global interfaces remain.

## 7. Reception

Reception is **immature**.  No citation, reuse, external replication, or peer
review is claimed.

## 8. Red flags

- Post-implementation seal, not prospective preregistration.
- Formal-series master formula is mapped to exact finite sums in prose rather
  than derived inside Lean's power-series library.
- Finite-pole/infinity-order descent is still unformalised.
- Complete theorem status still depends on inherited proof modules.

## 9. Decision

**Go with controls** for the targeted successor.  The two named obligations
are closed internally and no longer justify a finite-`m` caveat.  Maintain
candidate status for the complete all-degree atlas.

## 10. Reassessment trigger

Reassess after formalising or independently auditing the finite-pole descent,
parent root-span theorem, remaining primitive audit, and rank-preserving
extension theorem.
