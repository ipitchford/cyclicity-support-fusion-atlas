# Reproducibility

## Authoritative environment

`ENVIRONMENT.txt` records the operating system and principal engines used for
the v0.6 gate. Python dependencies remain pinned in `requirements.txt`; KaTeX
is pinned in `package-lock.json`. The Lean receipt records both the compiler
commit and the Mathlib commit. Earlier environment records and receipts remain
historical cross-version evidence, not competing current specifications.

No container, Nix, or Guix lock is supplied. A clean-machine rerun may
therefore require equivalent toolchain installation before replay.

## One-command all-degree gate

From the package root:

```bash
python3 run_global_completion_checks.py
```

The command:

1. verifies the immutable v0.5 parent bytes and every bounded successor
   manifest;
2. replays the predecessor uniform all-`m` gate, including the repaired
   nineteen-check Kummer component;
3. verifies the global semantic receipt under ordinary and optimised Python;
4. rejects thirteen deliberate global receipt mutations in each mode;
5. reruns the separate exact SymPy implementation under ordinary and
   optimised Python and requires frozen-byte parity;
6. rebuilds the global Lean/CAS receipt and requires ordinary/optimised and
   frozen-byte parity; and
7. ends only with `GLOBAL ALL-DEGREE COMPLETION GATE PASS`,
   `PUBLIC UNREFEREED-CANDIDATE RELEASE GO`, and
   `EXTERNALLY ESTABLISHED THEOREM PROMOTION REMAINS HOLD`.

`--skip-engine-recompute` verifies frozen receipts without rerunning Lean and
SymPy. It is a diagnostic convenience, not the authoritative release replay.
The v0.5 exhaustive degree-20 gate remains independently replayable with
`python3 run_core_checks.py`.

## Formal and computational scope

The Lean layer checks sixteen named consequences involving pole order,
spanning, scalar extensions, and primitive characters. It does not formalise
Laurent-series/function-field integrality, the direct Dickson invariant-field
argument, Kummer or Ritt theory, or the imported classification theorems.

The separate SymPy path performs ten exact global checks and bounded
regressions over 2,079 pole-floor cases and 81 Dickson composition pairs. The
Kummer component performs nineteen exact checks. These computations validate
their encodings and catch semantic corruption; they do not independently
certify the entire source-to-encoding bridge.

## Reader-document build and raw-TeX stop rule

The archival paper is assembled from `ALL_DEGREE_RELEASE.md`, the sealed proof
`ALL_DEGREE_GLOBAL_COMPLETION.md`, and
`ALL_DEGREE_RELEASE_BACK_MATTER.md`. The build uses Pandoc parsing, static
KaTeX 0.18.4 rendering, WeasyPrint PDF generation, and PyMuPDF finalisation:

```bash
python3 tools/render_all_degree_paper.py
python3 tools/pdf_tex_preflight.py All-Degree-Low-Rank-Coefficient-Atlas.pdf
```

The preflight scans rendered text for leaked TeX delimiters and commands. It
is required in addition to PDF syntax checks and rasterised-page visual QA,
because text extraction alone previously failed to reveal literal display
math on reader-facing pages. Any raw-TeX finding is a release blocker.

## Deterministic release archive

```bash
python3 tools/build_all_degree_release.py freeze
python3 tools/build_all_degree_release.py archive \
  ../cyclicity-support-fusion-atlas-v0.6.0-candidate.zip
python3 tools/build_all_degree_release.py bind-archive \
  ../cyclicity-support-fusion-atlas-v0.6.0-candidate.zip \
  receipts/all_degree_archive_receipt.json
```

The root manifest covers every public payload byte except the manifest itself,
the archive binding written after the archive exists, and the workflow-only
`GLOBAL_PUBLICATION_STATE.json`. The archive uses sorted paths, fixed UTC
timestamps, normalised permissions, and no host metadata. A qualifying
release replay occurs again from a fresh extraction of that archive.

## Trust and exclusion boundary

The imported primitive-polynomial-monodromy and finite-projective-group
classification results are pinned and scoped but not re-proved. The two
specialist re-audits are internal and model-assisted. No external independent
reproduction, complete formalisation, journal review, or priority
certification is claimed. Positive-characteristic, zero-cycle,
Laurent-polynomial, and arbitrary-amplitude extensions remain outside the
theorem.
