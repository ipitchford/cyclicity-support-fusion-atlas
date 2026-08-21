# Research Quality Gate: independent CAS and local formalisation

## 1. Boundary

- Assessment ID: `cyclicity-independent-formalization-2026-08-21`
- As-of date: 2026-08-21
- Assessor: anonymous internal QA
- Decision: whether the new check should enter the candidate package and
  change the assurance description
- Boundary: assess the Singular bounded elimination and eleven Lean statements,
  not the complete all-degree theorem.

## 2. Claim and intended output

The output claims that a non-SymPy CAS reproduces all cubic/quartic elimination
loci for `2 <= m <= 32`, and that Lean's kernel verifies eleven named local
algebraic statements.  The intended output is a mathematical software and
formal-proof certificate for specialist reviewers of the cyclicity atlas.

## 3. Novelty-gate handoff

The existing applications novelty gate returned **BOUNDED UNCERTAINTY** on
2026-08-21 within parent references and bounded arXiv/HAL searches.  It permits
a newly constructed verification artefact but no absolute originality claim.
That gate named a third-party CAS comparison as a rerun trigger; a refreshed
prior-art search remains due before any novelty claim or publication decision.

## 4. O/S/R assessment

| Dimension | Retrospective prior | Ex-post | Confidence | Evidence-backed justification |
|---|---:|---:|---|---|
| Originality | 2 | 2 | medium | Separate Singular/Lean artefact is newly constructed here, but no refreshed formalisation prior-art search was run. |
| Significance | 3 | 3 | high | It directly tests the previously circular proof repair and caught/binds the quartic sign-sensitive identity. |
| Rigour | 3 | 3 | high for stated boundary | 62 exact saturated loci, 11 kernel-checked statements, source lock, semantic verifier, and mutations; central inherited lemmas remain outside scope. |

Local decision aid: `Q = 100*((2/4)*(3/4)*(3/4))^(1/3) = 65.5`.
This is not an official assessment score.

## 5. Evidence ledger

| Claim or criterion | Evidence | Identifier | Date | Status |
|---|---|---|---|---|
| Bounded second-engine loci | Singular source and receipt | `cleanroom/singular_newton_crosscheck.sing`; `receipts/independent_formalization_receipt.json` | 2026-08-21 | pass |
| Local formal statements | Lean source and kernel receipt | `formal/lean/CyclicityNewton.lean` | 2026-08-21 | pass |
| Source identity | post-implementation lock | `formal/independent_verification_lock.json` | 2026-08-21 | pass |
| Semantic integrity | verifier plus six mutations | `tools/verify_independent_formalization.py`; `tests/test_independent_formalization.py` | 2026-08-21 | pass |
| Claim mapping | human-readable map | `INDEPENDENT_FORMALIZATION.md` | 2026-08-21 | complete |

## 6. Assurance

- Status: **formally verified for the eleven named Lean statements; internally
  reproduced by a second CAS for the bounded sweep**.
- Replay: sealed local runner and receipt; same-environment replay required.
- Independence: different engines and mechanisms, same producer; not external.
- Provenance: exact source, Singular, Lean, Lake, and Mathlib identities recorded.
- Limit: no clean-room external operator or formal statement-correspondence
  review.

## 7. Reception and impact

Reception is **immature**.  No citation, reuse, external replication, or
specialist review is claimed, and no reception metric affects this gate.

## 8. Red flags and disagreements

- The post-implementation lock is not prospective preregistration.
- The Lean statements do not contain the monodromy/scaling lemma, finite-pole
  descent, uniform all-`m` coefficient argument, primitive audit, or extension
  theorem.
- Mathlib was reused from a populated local project rather than rebuilt in a
  fresh isolated environment.
- No independent human checked that the formal statements exactly capture all
  manuscript obligations.

## 9. Decision

**Go with controls** as additive candidate assurance.  Do not promote the
all-degree classification to “formally verified” or “externally independently
reproduced.”  Reassess after a specialist statement-correspondence audit or
formalisation of the monodromy/scaling and uniform coefficient-extraction
steps.

## 10. Sources and metric definitions

- Research Quality Gate rubric v1.0.0; O/S/R use the local 0–4 decision scale.
- `programme/NOVELTY_GATE.md`, search date 2026-08-21.
- Engine identities are recorded in the frozen receipt rather than inferred
  from package names.
