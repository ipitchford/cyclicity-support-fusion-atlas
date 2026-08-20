# Author-run Wolfram Language spot check

**Date:** 19 August 2026  
**Role:** cross-CAS spot check generated in the same producer workflow  
**Independence:** not independent reproduction

## Formal inverse coefficients

Input:

```wl
Module[{u, a, b, c, xi, expr, equations, sol},
 xi = 1/u + a u^2 + b u^5 + c u^8;
 expr = Expand[u^4 (xi^4 + xi - u^-4)];
 equations = Thread[Coefficient[expr, u, #] & /@ {3, 6, 9} == 0];
 sol = Solve[equations, {a, b, c}, Rationals];
 <|"equations" -> equations, "solution" -> sol,
   "residualWithSolution" -> Series[expr /. First[sol], {u, 0, 13}]|>
]
```

Returned solution:

```text
a -> -1/4
b -> -1/32
c -> 0
```

Thus

```text
xi(t) = t - (1/4)t^-2 - (1/32)t^-5 + 0*t^-8 + ...
```

The zero coefficient in residue `4 mod 12` agrees with the quartic trace
argument.

## Polynomial identities

Input checked:

```wl
Expand[(x^4 + x)^3 - x^3 (x^3 + 1)^3]
PolynomialReduce[
  Expand[((z x)^4 + z x) - z (x^4 + x)],
  {z^3 - 1}, z][[2]]
```

Returned residuals:

```text
0
0
```

These confirm the Ritt identity and `Q(z x)=z Q(x)` modulo `z^3=1`.
