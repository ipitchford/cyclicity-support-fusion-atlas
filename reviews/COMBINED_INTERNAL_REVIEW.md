# Internal review: combined 0.7.0 candidate

**Review date:** 21 August 2026
**Artifact:** `Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf`
**Decision:** **PASS for public unrefereed candidate circulation; HOLD for
external theorem promotion.**

## 1. Mathematical architecture

**Pass, with declared imported dependencies.** The manuscript now has one
continuous theorem architecture. The fixed-seed root-span interface feeds the
all-degree classification, which in turn feeds the endpoint table. The
polynomial-amplitude theorem supplies the formal-moment construction used by
the fixed-seed specialisation. The Laurent criterion is clearly separated
from the stronger finite-atlas claim that is not proved.

The inherited Kummer exception and the arbitrary mixed-Dickson issue are
described accurately. The all-degree theorem remains relative to the named
primitive-monodromy, block-kernel, finite-group, and Ritt inputs.

## 2. Claim discipline and source traceability

**Pass for a theorem candidate.** Eight positive claims and four explicit
non-claims are recorded in `CLAIMS_COMBINED.json`. The endpoint theorem is
marked conditional on both Pakovich--Muzychuk and the candidate Atlas. The
reference audit has one definition for every used label and no stale `[EP3]`
companion self-citation. The manuscript makes no absolute novelty or priority
claim.

Residual limitation: the search is broad but not an exhaustive subscription
MathSciNet search, all-language survey, unpublished-work search, or universal
citation-forward closure.

## 3. Computational and formal evidence

**Pass within the stated boundary.** Fresh global and amplitude/Laurent gates
pass in ordinary and optimised Python. Global normal/optimised receipts agree;
the amplitude/Laurent receipts are byte-identical. Mutation tests reject
semantically corrupted receipts after digest recomputation. Lean and exact CAS
checks cover encoded interfaces and regression consequences.

These checks do not fully formalise the proof, reproduce imported
classifications, or constitute unaffiliated verification.

## 4. Document and release integrity

**Pass.** The combined source is generated deterministically from preserved
component sources. The HTML and PDF rebuild byte-for-byte. qpdf reports a
valid document, metadata and bookmarks are present, the PDF has 25 A4 pages,
and text extraction contains no exposed TeX-control pattern. The combined
manifest is independently checked after final rendering.

The two predecessor PDF digests remain unchanged, and the short companion is
retained. No destructive rewrite or public action occurred.

## 5. Reader-facing quality

**Pass.** The title, integrated abstract, Traditional Chinese abstract,
dependency map, and assurance map make the paper intelligible without first
reading the release history. Section numbering is continuous from 1 through
21. The final page set has been visually inspected, with equation-focused
checks in the Kummer, amplitude, endpoint, and Laurent sections. Literal TeX,
detached relation glyphs, clipping, overprinting, and the earlier Chinese
keyword orphan are absent in the final render.

## Required conditions before status promotion

1. independent polynomial-monodromy/Ritt review;
2. independent finite-linear-group review;
3. unaffiliated review of the amplitude, zero-cycle, endpoint, and Laurent
   arguments and their exact implementation;
4. final editorial and publication authorisation; and
5. public-byte readback if a release is later deployed.

Until those conditions are separately evidenced, this review must not be used
as a substitute for external peer review.
