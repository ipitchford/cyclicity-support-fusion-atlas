# Universal degree-32 low-rank coefficient atlas

Status: **confirmed finite computer-assisted theorem candidate; internally
replayed, unrefereed and unpublished**

## Theorem candidate

For every complex polynomial `P` of degree 32,

\[
q(P,dx)\le3
\]

if and only if `P` is affine-equivalent to one of

\[
x^{32},\qquad D_{32}(x,a)\ (a\ne0),\qquad
x^{32}+Ax^{16}\ (A\ne0).
\]

Their normalised inverse supports are respectively

\[
\{1\},\qquad \{1,31\},\qquad \{1,17\}.
\]

In particular, no complex polynomial of degree 32 has exact fixed-seed cyclic
rank three. A polynomial outside the three displayed families has rank at
least four; this result does not determine its exact higher rank.

## Exhaustive coverage

After making the phase monic and centred and suppressing a target constant,
every rank-at-most-three phase has a support

\[
S\subseteq\{1,\ldots,31\},\qquad 1\in S,\qquad |S|\le3.
\]

There are exactly

\[
1+30+\binom{30}{2}=466
\]

such sets. The sealed runner constructed the universal confinement ideal for
every set over `Q`, using the inverse coordinates permitted by that support.
It formed a Gröbner basis from equations through order `4d=128` and reduced
all additional equations through `6d=192`.

The prospective counts were confirmed exactly:

| Certificate | Count | Meaning |
|---|---:|---|
| full-family | 3 | the power, Dickson and quadratic-over-power supports |
| power-only | 406 | every non-leading inverse coordinate is nilpotent |
| union | 57 | the variety lies in the union of the applicable rank-two components |
| anomaly | 0 | no extra component or dimension |
| missing certificate | 0 | every case closes fail-closed |

All 466 condition ideals were stable through depth 192.

## Prospective and replay identities

The computation was sealed before execution against parent commit
`ce4e129bed2c1ea5dd7b778488d7bec2b76deb7d` and the preceding application
manifest. The ordinary run completed in 808.2 seconds; the optimized replay
completed in 817.6 seconds. Their mathematical receipts are byte-identical.

- canonical mathematical receipt:
  `fbb09a99a6dba6802c1589b3e7aa5ea85f5cb3649f60a68fe81b5d8833f3b43f`;
- receipt-file SHA-256:
  `3d6791222e2a7c7159238ef2eda93a21035e234730d4b7f5259e3a0f25acfa36`;
- replay receipt:
  `df63f922ba3863dfbe0c88ae97971c3953aa17e4ee68c785241dae0249b77167`.

## Why the finite proof applies to every complex coefficient vector

This is not a sampling argument. A support hypothesis with at most three
classes leaves at most three low inverse coordinates. Every phase with that
support supplies a point of the corresponding exact confinement variety.
The recorded radical witness places the entire variety inside the predicted
family components. The triangular inverse-series map then returns the phase
coefficients. Because all defining calculations and reductions are over
`Q`, the set-theoretic containment holds after extension to `C`.

## Reproduction

Verify the frozen result without recomputing it:

```bash
python3 tools/verify_degree32_universal.py
```

Run the successor composite gate:

```bash
python3 run_degree32_universal_checks.py
```

The expensive 466-case recomputation is available as an explicit optional
gate mode; ordinary and optimized executions together take about 27 minutes
on the recorded environment.

## Boundary

The theorem candidate is universal for the degree-32 threshold `q<=3`. It is
not a classification of every higher rank, not a proof-assistant artefact,
not external reproduction, and not by itself the all-degree atlas.

