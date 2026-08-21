# Lean reproduction

`CyclicityNewton.lean` contains eleven kernel-checked statements supporting the
local cubic/quartic Newton descent.  It does not claim to formalise the
all-degree theorem.

For a fresh environment:

```console
lake update
lake env lean CyclicityNewton.lean
```

The sealed run used Lean 4.32.1 and Mathlib tag `v4.32.1`, commit
`520045ab14e26149ee970e2e617ca04b09bde5d6`.

The project-level runner may instead reuse any populated Mathlib project at
the same revision:

```console
python3 ../../tools/run_independent_formalization.py \
  --mathlib-project /path/to/populated/mathlib-project
```
