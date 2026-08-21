# Fraction-only replay challenge

This challenge asks an implementer to recover the canonical inverse support and
generic fixed-seed rank for twelve rational polynomial phases without importing
the production SymPy oracle.

## Inputs

`spec.json` contains ascending rational coefficient arrays, exact rational
specialisation points and inverse-series depths. Expected answers are separated
into `answer_key.json`.

## Required output

For each case return:

- the affine-normalised inverse-support residue classes;
- the generic rank (q(P,dx)); and
- whether the two values agree.

An exact specialised Krylov rank equal to the ambient rank proves generic full
rank. For lower-rank cases, a replay should either work symbolically over
\(\mathbf Q(s)\) or use enough exact specialisations together with the supplied
parent theorem boundary. The reference replay uses multiple exact rational
specialisations and compares with independently reverted support.

## Reference replay

```bash
python3 challenge/reference_fraction_replay.py
```

The runner imports only the standard-library `Fraction` backend in
`verification/lib.py`; it imports neither production module and no CAS. This is
a separate within-programme implementation, not unaffiliated reproduction.

## External participation

An external replay should record source identity, dependency versions, complete
output and any discrepancies. Matching the answer key establishes agreement on
these finite cases only. It does not certify the parent proof or all-degree
atlas.

