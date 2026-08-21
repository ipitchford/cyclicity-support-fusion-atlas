# Global-completion Lean layer

Run from a populated Mathlib project:

```sh
lake env lean /absolute/path/to/formal/lean/CyclicityGlobal.lean
```

`CyclicityGlobal.lean` checks the arithmetic conversion from an infinity-order
bound to polynomial constancy, the full-block spanning implication, the
rank-three scalar equations, the collision non-repetition calculation, and
the exceptional character sums.

It deliberately does **not** formalise Laurent-series inversion, integrality
in algebraic function fields, monodromy, Ritt theory, or finite-group
classification.  The receipt must therefore retain
`complete_atlas_formalization: false`.
