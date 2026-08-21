# Independent-engine CAS and kernel formalisation

Status: **PASS for the stated local algebra; theorem status unchanged**  
Date: 2026-08-21

## 1. Outcome

The Newton-descent boundary has now been checked through two mechanisms that
do not use the existing SymPy implementation:

1. **Singular 4.4.1** independently computed direct resultants and saturated
   elimination ideals for every cubic and quartic exponent `2 <= m <= 32`.
2. **Lean 4.32.1 + Mathlib** kernel-checked eleven polynomial statements:
   both positive powered-root identities, all exceptional coefficient
   obstructions displayed in the proof note, and three elementary-symmetric
   reductions.

Singular found exactly the expected loci:

- cubic, with `a != 0`: only `m=2` survives;
- quartic, with `c != 0`: only `m=3` survives, and its standard basis is
  `cw-1,a`, so the survivor forces `a=0`;
- every other case has reduced standard basis `1` after the relevant
  nondegeneracy saturation.

The positive resultants are

\[
y(y+a)^2-e^2
\quad\text{and}\quad
y(y+c)^3+e^3.
\]

The second sign is therefore independently confirmed as positive.

## 2. Statement-identity map

| Mathematical statement | Singular | Lean | Boundary |
|---|---|---|---|
| Cubic survivor `m=2` | saturated resultant locus | `cubic_powered_root` | local algebra |
| Cubic `m=4` obstruction | unit saturated ideal | `cubic_m4_forces_power` | local algebra |
| Quartic survivor `m=3,a=0` | basis `cw-1,a` | `quartic_powered_root`, `quartic_m3_forces_a_zero` | local algebra |
| Quartic `m=2,5,6,9` obstructions | unit saturated ideals | four named obstruction theorems | displayed boundary cases |
| All other `m <= 32` | unit saturated ideals | not formalised individually | bounded fault control |
| Uniform all-`m` exclusion | not established by the sweep | not formalised | prose coefficient-extraction proof |
| Monodromy/scaling and finite-pole descent | not checked | not formalised | inherited proof obligations |

The map matters because a kernel pass proves the formal statement in the Lean
file, not automatically the surrounding theorem.  Here the formal statements
have been kept close to equations (4.2), (4.3), (5.3), and (5.4) of
`ALL_DEGREE_NEWTON_DESCENT.md`.

## 3. Separation from the earlier checks

The Singular program imports no project module and invokes no Python algebra.
It constructs

\[
\operatorname{Res}_x(q_e(x),y-x^m),
\]

extracts the `e`-dependence of the first `n-1` coefficients, and computes a
lexicographic standard basis after adding `wa-1` or `wc-1`.  The Python runner
only launches processes, parses output, and computes hashes using the standard
library.

The Lean source imports Mathlib but no generated Singular output, SymPy
expression, or project checker.  Mathlib tactics construct proof terms that
Lean's kernel checks.

This is a genuine engine and proof-mechanism separation inside the same
research programme.  It is not external independent reproduction because the
same producer selected the statements, wrote the two sources, and interpreted
their relationship to the manuscript.

## 4. Reproduction

Requirements:

- Singular 4.4.1 or a compatible later version;
- Lean 4.32.1;
- Mathlib revision `v4.32.1` (checked commit
  `520045ab14e26149ee970e2e617ca04b09bde5d6`);
- Python 3 standard library.

With a populated Mathlib project available:

```console
python3 tools/run_independent_formalization.py \
  --mathlib-project /path/to/populated/mathlib-project
python3 tools/verify_independent_formalization.py
python3 -m unittest tests/test_independent_formalization.py -v
```

For a new environment, first run `lake update` inside `formal/lean`, then pass
that directory through `--mathlib-project`.

## 5. Assurance conclusion

This successor materially strengthens the local Newton-descent repair:

- the bounded algebra has been reproduced in a different CAS;
- the displayed positive identities and exceptional obstructions have
  machine-checked proofs;
- source identity, engine identity, case coverage, claim boundary, and
  adversarial receipt mutations are bound by the verification layer.

It does **not** make the all-degree classification a formally verified theorem.
The monodromy/scaling lemma, uniform coefficient-extraction argument,
finite-pole descent, inherited primitive audit, and rank-preserving extension
classification still require specialist proof audit or further formalisation.
