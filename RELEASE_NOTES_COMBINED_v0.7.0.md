# Release notes: combined 0.7.0-candidate

## Primary change

The 0.7 work is now presented as a single flagship manuscript,
`Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf`, rather than requiring
the reader to reconstruct the theorem from the v0.6 paper and a short
extension.

The unified paper contains:

- the complete reader-facing all-degree fixed-seed theory and coefficient
  atlas for \(q(P)\leq3\);
- the classification of all rank-preserving polynomial extensions;
- arbitrary polynomial amplitudes and the universal rank-zero criterion;
- exact vanishing on any specified zero-dimensional cycle;
- persistent endpoint moments for every low-rank Atlas phase; and
- the exact local inverse criterion for arbitrary Laurent one-forms.

The extension results have been renumbered as Sections 13--21, all internal
self-citations have been replaced by direct theorem references, and the paper
has one reference list, limitation statement, declaration set, and bilingual
abstract.

## Publishing and verification changes

- a fail-closed source combiner generates the unified body from preserved
  component manuscripts;
- the primary renderer explicitly enables Pandoc's single-backslash TeX
  extension before static KaTeX rendering;
- a raw-TeX preflight, qpdf validation, deterministic document identifier,
  bookmarks, metadata, and byte-reproducibility check protect the reader-facing
  artifact;
- a combined claim ledger, assurance statement, status record,
  reproducibility guide, internal review, and manifest bind the merged release;
- fresh ordinary and optimised replays pass for both mathematical layers; and
- all 25 PDF pages receive visual QA, including equation and table hot spots.

## Corrections incorporated

The manuscript preserves the v0.6 Kummer correction: the false uniform
full-kernel assertion is not restored on the exceptional even-exponent
repeated-root stratum. It also preserves the direct arbitrary-degree Dickson
argument and does not promote finite Laurent zero-prefix experiments to an
all-orders theorem.

## Preservation and status

The original fixed-seed paper, Atlas paper, and 12-page amplitude/Laurent
companion remain present as predecessor artifacts. The combined manuscript is
the new primary candidate document; it is not a destructive replacement.

Status is **GO for public unrefereed candidate circulation; HOLD for externally
established theorem promotion**. The exact-version DOI is
`10.5281/zenodo.22049564`; the v0.6 candidate remains an immutable predecessor.
