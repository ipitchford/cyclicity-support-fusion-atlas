# Amplitude and Laurent extension: assurance statement

**Status:** `0.7.0-candidate`, internal theorem candidate, 21 August 2026.

## Decision

**GO for internal candidate circulation; HOLD for publication as an externally
validated theorem.**  The new algebraic results and exact replay pass, but the
all-degree low-rank phase classification they specialise remains unrefereed,
and the successor has not received independent specialist review.

## Claim ledger

| Claim | Basis | Assurance |
|---|---|---|
| Polynomial-amplitude rank equals primitive inverse support size | self-contained formal-moment and Fourier proof | theorem candidate |
| Rank zero iff the primitive lies in `C[P]` | algebraic corollary with exact CAS controls | theorem candidate |
| Specified zero-cycle vanishes iff its Fourier transform annihilates the primitive support | self-contained DFT proof | theorem candidate |
| Endpoint moment solutions are sums through endpoint-equal right factors | Pakovich--Muzychuk, DOI 10.1112/plms/pdp010 | imported peer-reviewed theorem |
| Table covers every phase with fixed-seed rank at most three | imported moment theorem plus v0.6 Atlas right-factor audit | conditional on unrefereed Atlas candidate |
| Laurent residues equal local inverse coefficients | formal change-of-variable proof for arbitrary Laurent amplitudes | theorem candidate |
| Finite Laurent zero prefixes imply persistent vanishing | explicitly not claimed | prohibited inference |
| All Laurent solutions are composition solutions | contradicted as a general template by PPZ10 | explicitly not claimed |

## Exact verification

Run:

```bash
python3 run_amplitude_laurent_checks.py
```

The gate requires:

- ordinary exact replay;
- optimised (`python -O`) exact replay;
- byte-identical receipts;
- parity with the frozen receipt;
- exact Krylov/support agreement;
- direct/local Laurent residue agreement;
- sixteen direct endpoint regression moments; and
- rejection of two semantically corrupted receipts after digest recomputation.

The frozen generated receipt is
`receipts/amplitude_laurent_test_receipt.json`.  Its content digest is recorded
inside the file; the replay gate separately compares the complete file bytes.

## Boundaries

- The v0.6 Atlas imports named primitive-monodromy and finite-group
  classifications and remains unrefereed.
- The present work does not independently reprove Pakovich--Muzychuk.
- Exact software checks encoded consequences and examples, not the full
  source-to-theorem bridge.
- No complete proof-assistant formalisation or independent CAS implementation
  of this successor has yet been supplied.
- The literature search is source-verified but not exhaustive in MathSciNet,
  zbMATH, all languages, or unpublished work.  No priority claim is made.
- The Laurent theorem is an infinite coefficient criterion for a fixed input,
  not a finite family atlas for all Laurent pairs.
- The zero-cycle theorem is exact for a specified cycle; it does not collapse
  the balanced-cycle literature to a composition-only description.

## Additive preservation

The successor was developed in a separate worktree from the immutable
`v0.6.0-candidate` tag.  The predecessor PDFs remain present:

- `Inverse-Root-Support-and-Fourier-Fusion.pdf`;
- `All-Degree-Low-Rank-Coefficient-Atlas.pdf`.

No predecessor file, release page, DOI record, tag, or publication-state
receipt was deleted or rewritten.
