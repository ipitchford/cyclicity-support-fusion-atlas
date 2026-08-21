# Assurance statement: coefficient-stratified Kummer transport successor

**Status:** repaired candidate theorem proved in writing; named finite algebra
replayed in Lean and by a separate SymPy/Python implementation.

## What is established in writing

- a divisor/Kummer argument for the full diagonal kernel away from the
  explicit even-`m`, `B!=0`, `A^2=4B` stratum;
- exact detection of the Kummer relations on that stratum and a decomposition
  descent showing that it is either the rank-two Dickson overlap (`m=2`) or
  an already-used aligned square that cannot admit another rank-preserving
  step;
- separate treatment of the affine-power cubic locus `3B=A^2`, where the
  outer monodromy is `C_3` rather than `S_3`;
- all-`m` preservation of the Kummer lines on every full-kernel stratum; and
- the monomial transport and coefficient conclusions used by the
  cubic-over-power extension audit.

## Machine-checked scope

Lean checks the characteristic-polynomial identities and algebraic line-cycle
obstructions.  The clean-room program checks the same identities through a
different implementation, verifies the exceptional relations and polynomial
factorisations, checks the affine-power Fourier equations, exhaustively
reconstructs all 24 automorphisms of `S_4`, and computes the octahedral
ordinary and sign-twisted intertwiner dimensions.

## What is not claimed

This is not a complete formalization of Kummer theory, divisor valuations,
the block-stabiliser lemma, the decomposition descent, polynomial monodromy,
Ritt theory, or the parent all-degree classification.  The clean-room program
is an independent implementation within the same research programme, not
external independent reproduction or peer review.  The two internal referee
reports that found the original counterexample remain historical HOLD
receipts; a fresh audit of this repair is required before any theorem release.
