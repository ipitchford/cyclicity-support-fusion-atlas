# Combined manuscript: assurance statement

**Status:** `0.7.0-candidate`, internal theorem candidate, 21 August 2026.
**Internal manuscript gate:** **PASS**.
**Public unrefereed-candidate gate:** **GO**.
**External theorem-promotion gate:** **HOLD**.

## Decision

**GO for public unrefereed candidate circulation. HOLD for externally
established theorem promotion.** The combined document accurately
binds the fixed-seed all-degree theory to the amplitude, zero-cycle, endpoint,
and Laurent extensions. Both executable verification stacks pass in ordinary
and optimised Python. The all-degree classification nevertheless remains
relative to named imported results and has not received unaffiliated
specialist review.

## Claim-to-evidence map

| Claim | Manuscript location | Evidence and dependency | Assurance |
|---|---|---|---|
| fixed-seed rank equals inverse support and reduced root span | Theorem 2.1 | algebraic Fourier argument; formal-moment construction in Theorem 14.1 | theorem candidate |
| complete all-degree coefficient atlas for \(q(P)\leq3\) | Theorem 11.1 | Sections 3--10; imported monodromy and finite-group classifications | conditional theorem candidate |
| all proper rank-preserving polynomial extensions are listed | Sections 7--10 | repaired Kummer strata; direct Dickson invariant-field argument | conditional theorem candidate |
| arbitrary polynomial-amplitude rank equals primitive inverse support | Theorem 14.1 | self-contained formal-moment and Fourier proof; exact regression controls | theorem candidate |
| a specified zero-cycle vanishes exactly on Fourier-annihilated active channels | Theorem 15.1 | self-contained discrete Fourier proof | theorem candidate |
| endpoint table covers every Atlas phase with \(q(P)\leq3\) | Theorem 17.1 | Pakovich--Muzychuk plus Theorem 11.1 and right-factor audit | conditional theorem candidate |
| Laurent residue moments equal the stated local inverse coefficients | Theorem 18.1 | formal residue change of variable; exact direct/local comparisons | theorem candidate |
| a finite zero prefix proves persistent Laurent vanishing | not asserted | prohibited inference | not claimed |
| all persistent Laurent solutions are composition solutions | not asserted | known indecomposable case study [PPZ10] | not claimed |

The machine-readable version is `CLAIMS_COMBINED.json`.

## Fresh replay evidence

The global gate reports:

- 16 Lean theorems and 10 exact global CAS checks;
- 81 bounded Dickson regression cases;
- ordinary/optimised parity;
- 14 semantic mutation tests in each mode; and
- frozen global receipt digest
  `7bfaca3adf5bcd71c66cae2c674a3b560500e596e420d0de55920790b35a8b43`.

The amplitude/Laurent gate reports ordinary/optimised byte parity at:

`ab1805e3f1fbb8192c9c8f18ed4fb58fee74d93ea02ede76b313dedf3cedaf1b`.

The amplitude checks encode primitive-support/Krylov agreement, direct versus
local Laurent residues, endpoint regression moments, and semantic corruption
controls. These are exact implementation checks, not a formalisation of every
proof sentence.

## Combined-document controls

The combined source is generated from the preserved all-degree and extension
sources. Numbering, internal references, and obsolete companion self-citations
are transformed by a fail-closed builder. The rendering path uses Pandoc with
`tex_math_single_backslash`, static KaTeX, WeasyPrint, qpdf structural checks,
and a content-derived PDF identifier. A second clean render must be byte
identical to the first.

Visual QA is a distinct gate. Text extraction alone cannot detect equations
left as literal TeX, detached relation glyphs, clipping, or page-orphaning.
The final audit therefore inspects every rendered page and gives extra
attention to the Kummer repair, all-degree theorem, amplitude theorem,
endpoint table, and Laurent coefficient formula.

## Boundaries and residual risks

- Primitive polynomial monodromy, finite projective linear groups, and the
  composition-length-two kernel input are imported rather than reproved.
- The 2026 monodromy source is a preprint; its source-side Magma computations
  are not independently certified here.
- Lean does not formalise the full algebraic-function-field, monodromy,
  Kummer, Ritt, or Laurent-series argument.
- The package has no unaffiliated CAS implementation of the new amplitude and
  Laurent layer and no unaffiliated specialist proof review.
- The literature work is broad and source-verified but not exhaustive in
  subscription MathSciNet, every language, unpublished work, or universal
  citation-forward closure. No absolute novelty or priority claim is made.
- The Laurent theorem is a criterion for a specified input, not a finite
  classification of every Laurent pair.

## Legitimate next status upgrade

External promotion requires, at minimum, independent specialists to audit the
polynomial-monodromy/Ritt and finite-linear-group interfaces, plus an
unaffiliated check of the amplitude/Laurent proofs and replay. A publication
action can preserve the present unrefereed label, but cannot itself satisfy
those mathematical review requirements.
