# Coefficient-atlas status

## All-degree candidate theorem

In `ALL_DEGREE_GLOBAL_COMPLETION.md`, Theorem 11.1 classifies every complex
polynomial phase with `q(P,dx) <= 3`, up to affine equivalence and lower-rank
intersections, relative to the named primitive-polynomial-monodromy and
finite-projective-group classification inputs. The families are:

1. powers;
2. Dickson polynomials;
3. quadratic-over-power phases;
4. cubic-over-power phases;
5. indecomposable quartics; and
6. the degree-twelve quartic collision.

The same theorem classifies every proper rank-preserving outer extension:
powers extend by powers; aligned Dickson polynomials stay in one dihedral
tower; an odd-centred cubic-over-power phase admits its aligned square; and
the exceptional quartic admits its cubic collision. These claims remain
unrefereed candidates relative to the imported classifications.

## Preserved finite theorem

The v0.5 theorem remains independently meaningful. For degrees two through
twenty, the affine families in `MANUSCRIPT.md` Theorem 13.1 exhaust
`q(P,dx) <= 3` within the recorded computer-algebra trust boundary. Degrees
five through twenty comprise all 1,152 support sets of size at most three
containing the normalised class one. Every case has a frozen ideal digest,
Groebner digest, outcome, and radical-containment witness.

The degree-32 quartic-lift experiment was prospectively sealed and passed. It
is retained as the first finite bridge beyond the parent cutoff and as a
regression control. Neither the degree-20 sweep nor degree-32 experiment is
the proof of the all-degree theorem.

## What changed after v0.5

The predecessor's Conjecture 13.2 is superseded by an additive proof, not by
rewriting the parent manuscript. The decisive uniform ingredients are
invariant-integral finite-pole/infinity descent, the full-block stabiliser,
the source-exact primitive audit, coefficient-stratified Kummer transport,
and a direct arbitrary-outer-polynomial Dickson invariant-field argument.

Adversarial review also found that the proposed uniform full Kummer kernel was
false on `B != 0`, `A^2 = 4B`, and even exponent. The released proof preserves
that counterexample and treats the exceptional stratum separately.
