# EPOB-1: Exponential-Period Order Benchmark, version 1

Status: frozen functional benchmark; reference timings are environment-specific.

## Purpose

EPOB-1 tests exact systems that predict or derive scalar differential equations
for

\[
I_\Gamma(s)=\int_\Gamma e^{sP(x)}\,dx
\]

with rational polynomial (P). It is designed around structural rank collapse:
same-degree phases can have very different generic minimal orders.

The benchmark does not claim that order bounds, minimal telescopers or
order-aware creative telescoping are new. It supplies a reproducible corpus for
the inverse-support bridge established by the parent manuscript.

## Tracks

### Track A — generic-order prediction

Return the generic minimal order and canonical inverse support. Ten cases are
scored, including a generic degree-twelve stress case of order eleven.

### Track B — scalar operator

Return polynomial coefficients (a_0(s),\ldots,a_q(s)) for

\[
\sum_{j=0}^q a_j(s)I^{(j)}(s)=0.
\]

Nine cases are scored. Operators are equivalent when they differ by a common
nonzero rational function. Primitive integer normalisation is recommended but
not required for correctness.

### Track C — performance

Measure prediction and operator construction separately. Report the complete
environment and do not compare times across machines without normalisation.
The reference runner reports medians but the frozen answer key contains no
timing thresholds.

## Corpus design

The cases include:

- power and Dickson anchors;
- a quartic rank drop;
- an affine target/source transformation;
- aligned and misaligned degree-twelve squares;
- the exceptional degree-twelve Ritt collision;
- a degree-six rank-creation control; and
- a generic degree-twelve rank-only stress case.

An implementation that returns only low orders cannot pass because the corpus
contains exact orders 4, 6 and 11.

## Running the reference implementation

```bash
python3 tools/run_epob1.py --repeats 3 \
  --output receipts/epob1_reference_run.json
```

Validate a third-party submission:

```bash
python3 tools/verify_epob1_submission.py submission.json
```

## Submission schema

```json
{
  "schema": "epob1-submission-v1",
  "system": {"name": "...", "version": "...", "environment": "..."},
  "cases": [
    {
      "id": "power_degree_7",
      "order": 1,
      "support": [1],
      "operator_coefficients_low_to_high": ["1", "7*s"],
      "elapsed_seconds": 0.0
    }
  ]
}
```

The generic degree-twelve stress case omits the operator field. Missing results
score as failures; errors must be reported rather than silently skipped.

## Assurance boundary

The reference answer key derives from the unrefereed parent theorem candidate
and exact replay package. EPOB-1 is a benchmark artefact, not an external
verification of that theorem and not evidence of performance superiority.

