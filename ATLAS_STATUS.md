# Coefficient-atlas status

## Retained theorem

For every complex polynomial of degree two through twenty, the affine families
in Theorem 13.1 exhaust `q(P,dx) <= 3`, subject to the recorded
computer-algebra trust boundary.

Degrees two through four are proved directly in the manuscript. Degrees five
through twenty comprise every support set of size at most three containing
the normalised class one:

```text
sum_{d=5}^{20} [1 + (d-2) + binomial(d-2,2)] = 1,152.
```

Each case has a frozen ideal digest, Gröbner digest, outcome and
radical-containment witness. The runner fails on an anomaly or missing
certificate and executes under ordinary and optimised Python.

## All-degree boundary

The all-degree atlas is **Conjecture 13.2**. The supplied quartic and cubic
lift argument assumes the scalar collapse that it needs to prove. Exact
elimination covers quartic lift moduli two through seven; the first uncovered
case is modulus eight, total degree thirty-two.

The next mathematical target is a non-circular twisted-factor descent or an
independent monodromy argument. More finite tables do not by themselves close
that universal step.
