# Uniform structural Lean successor

`CyclicityUniform.lean` formalises the algebraic and combinatorial core of the
monodromy/scaling lemma and the all-exponent coefficient descent.

It contains 25 theorem declarations and no `sorry`, `admit`, or axiom
declaration.  Its two top-level boundary theorems quantify over arbitrary
natural exponents; they are not finite sweeps.

With Mathlib already populated:

```console
lake env lean CyclicityUniform.lean
```

Or use the sealed project runner:

```console
python3 tools/run_uniform_formalization.py \
  --mathlib-project /path/to/populated/mathlib-project
```

The checked environment used Lean 4.32.1 and Mathlib commit
`520045ab14e26149ee970e2e617ca04b09bde5d6`.

The formal boundary deliberately exposes, rather than hides, the remaining
interfaces: polynomial monodromy as topology, analytic finite-pole descent,
the parent root-span theorem, and rank-preserving extensions.
