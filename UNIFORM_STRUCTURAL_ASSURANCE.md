# Assurance record: uniform structural all-degree repair

Status: **targeted proof successor passed; complete atlas remains a candidate**  
Date: 2026-08-21

## Claim matrix

| Claim | Evidence | Status | Limit |
|---|---|---|---|
| Cubic local monodromy is `S_3` | nonsquare discriminant proof | internally proved | standard inertia-at-infinity fact used |
| Quartic local monodromy is `S_4` | direct indecomposability proof plus primitive subgroup argument | internally proved | standard indecomposable/primitive equivalence used |
| Root-dependent radical scalings disappear | written lifted-monodromy proof; seven Lean scaling theorems | kernel-verified algebraic interface | topological monodromy construction not formalised |
| Cubic coefficient obstruction is uniform | exact coefficient formula; constructive mod-3 witness; Lean boundary theorem | kernel-verified combinatorial core | formal-series interpretation supplied in prose |
| Quartic coefficient obstruction is uniform | exact double-sum formula; both `a!=0` and `a=0` mod-4 branches; Lean boundary theorem | kernel-verified combinatorial core | formal-series interpretation supplied in prose |
| Exceptional boundary elimination | predecessor Lean/Singular receipt for `E_2` identities | passed predecessor gate | additive dependency, not duplicated |
| Complete all-degree atlas | structural theorem candidate relative to inherited interfaces | not yet externally established | parent root span, finite-pole descent, remaining primitive audit, and extensions remain |

## Formal inventory

The new Lean source contains 25 theorem declarations:

- 7 scaling theorems;
- 10 exact coefficient theorems;
- 8 uniform witness, nonvanishing, and boundary theorems.

There is no finite upper cutoff.  The two top-level boundary theorems quantify
over arbitrary natural exponents.  The source contains no `sorry`, `admit`, or
axiom declaration.

## What changed

The prior note described the correct residue strategy but left two
load-bearing steps for specialist checking.  This successor:

1. replaces the one-dimensional-subrepresentation sentence by an explicit
   transposition proof;
2. proves the final common rescaling over an algebraically closed field;
3. supplies closed coefficient formulae, not merely selected CAS outputs;
4. constructs a nonzero coefficient from every relevant congruence class;
5. formally reduces simultaneous coefficient vanishing to the exact finite
   boundary sets.

## Permitted claim language

The package may say:

> The monodromy/scaling and uniform all-exponent Newton-descent obligations
> have complete written proofs and a 25-theorem Lean verification of their
> algebraic and combinatorial core.

It may also say that the bounded `m<=32` conditionality has been removed from
this local descent.

It must not say:

- that the entire all-degree atlas is formally verified;
- that polynomial monodromy topology or finite-pole descent is formalised;
- that the result has been externally independently reproduced or peer
  reviewed; or
- that the remaining inherited theorem interfaces are thereby proved.

## Decision

**GO WITH CONTROLS** for integration as an additive proof successor.
**HOLD** on promoting the complete atlas to an externally established theorem
until the remaining interfaces receive comparable audit or formalisation.
