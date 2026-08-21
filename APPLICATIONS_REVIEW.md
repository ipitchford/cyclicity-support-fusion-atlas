# Internal adversarial review: benchmark through degree 32

Review date: 2026-08-21  
Review status: **PASS WITH NOTES for specialist circulation as an unpublished,
unrefereed application programme**

This review is internal. It is not external specialist review, independent
reproduction or an editorial decision.

## 1. Review question

Does the programme convert the order oracle into useful, reproducible research
artefacts and complete the prospective degree-32 test without conflating local
computation with a uniform theorem?

## 2. Load-bearing findings

### 2.1 Benchmark correctness and performance are separated — passed

The frozen answer key contains no timing threshold. Exact orders, supports and
operators determine correctness; local medians are descriptive. This prevents
the unexpectedly short run from becoming an unsupported complexity or
cross-system speed claim.

### 2.2 The corpus discriminates genuine structural collapse — passed

The ten cases span orders 1 through 11 and compare degree-12 phases of orders
3, 6 and 11. Rank-drop and rank-creation controls stop a constant-low-order
heuristic from passing. A public verifier accepts scalar operators up to a
common nonzero rational factor.

### 2.3 Actual decomposition is validated before fusion analysis — passed

Every supplied chain is recomposed exactly. Proper suffix ranks agree with the
parent support projection in every report, and alternative Ritt views retain
the same global rank. The software explicitly avoids claiming that the listed
chains exhaust all decompositions over the complex numbers.

### 2.4 Replay independence is bounded correctly — passed with limitation

The replay uses `fractions.Fraction`, imports no SymPy and covers twelve cases.
It nevertheless reuses the earlier verification library and was constructed
inside the same programme. The documentation calls it a separate replay path,
not independent external reproduction.

### 2.5 The degree-32 test was genuinely prospective — passed

Protocol and runner hashes were frozen before the first `m=8` execution. The
receipt starts after the recorded seal time, embeds the lock and has a verified
canonical digest. The verifier checks the unit ideals, residue classes,
condition counts, finite depth and adjudication without rerunning the
experiment.

### 2.6 Uniform-theorem leakage — prevented

The confirmed outcome concerns `A(x^8+b)` with quartic `A` and `gamma != 0`.
It is not promoted to all degree-32 polynomials, all quartic lifts or the
all-degree atlas. The programme therefore closes its stated finite scope while
leaving the general proof obligation visible.

## 3. Verification results

- EPOB-1: 10/10 order and support cases; 9/9 operator cases.
- Submission verifier: correct reference passes; a corrupted operator fails.
- Decomposition fusion: four cases, seven validated chains, exact parity under
  ordinary and optimized Python.
- Fraction replay: twelve cases, exact rank/support identity, no SymPy import,
  byte-identical replay receipts.
- Degree 32: both preregistered predictions confirmed in the single sealed run.
- Mutations: invalid composition, wrong replay answer and rehashed semantic
  result corruption all fail closed.
- Parent, order-oracle and application manifests retain bounded byte identity.

## 4. Residual limitations

1. The parent mathematical theorem remains an unrefereed candidate.
2. No external specialist has reproduced EPOB-1 or the degree-32 elimination.
3. No second computer-algebra system has produced the operators or Gröbner
   certificates.
4. The decomposition tool reports named witnesses, not the complete lattice.
5. The degree-32 calculation is one finite ansatz and one preregistered depth.
6. The bounded novelty search found established order-aware telescoping prior
   art and did not establish priority for the inverse-support bridge.
7. The successor is not tagged, archived, assigned a DOI or publicly released.

## 5. Decision

The programme satisfies the requested stopping point. Its exact artefacts,
mutation controls, prospective seal, replay parity and claim boundaries are
mutually consistent.

**Decision: accept as a complete local candidate through the preregistered
degree-32 experiment; suitable for specialist circulation with the assurance
and quality records attached. Publication and claims beyond this scope require
separate review and authority.**

