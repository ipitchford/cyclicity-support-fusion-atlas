# Reproducibility

## Authoritative environment

`ENVIRONMENT.txt` records the principal engines. Python dependencies are
pinned in `requirements.txt`; KaTeX is pinned in `package-lock.json`. The Lean
receipt records compiler and Mathlib commits. No container, Nix, or Guix lock
is supplied, so clean-machine reruns may require equivalent toolchain
installation.

## Mathematical gates

```bash
python3 run_global_completion_checks.py
python3 run_amplitude_laurent_checks.py
```

The global command checks the predecessor chain, scoped Lean/CAS receipts,
ordinary/optimised parity, semantic mutations, and separate exact
implementations. The amplitude/Laurent command checks ordinary/optimised
byte-parity, primitive-support/Krylov agreement, direct/local Laurent
residues, endpoint examples, and corruption controls.

Expected terminal receipts are:

```text
GLOBAL ALL-DEGREE COMPLETION GATE PASS
AMPLITUDE-LAURENT GATE PASS
```

Silence, timeout, or an earlier green line is not a pass.

## Combined document

```bash
python3 tools/build_combined_sources.py
python3 tools/render_combined_paper.py
python3 tools/check_combined_release.py
```

The renderer uses Pandoc's single-backslash mathematics extension, static
KaTeX, WeasyPrint, PyMuPDF, qpdf, a content-derived identifier, and a
fail-closed exposed-TeX scan. The integrated gate checks continuous numbering,
claim anchors, citation closure, predecessor digests, metadata, bookmarks,
page geometry, text extraction, and the focused manifest. Visual inspection of
all 25 pages remains a separate required gate.

## Deterministic publication archive

```bash
python3 tools/build_combined_publication.py freeze
python3 tools/build_combined_publication.py archive \
  ../cyclicity-support-fusion-atlas-v0.7.0-candidate.zip
python3 tools/build_combined_publication.py bind-archive \
  ../cyclicity-support-fusion-atlas-v0.7.0-candidate.zip \
  receipts/combined_archive_receipt.json
```

The v0.7 manifest covers every archive byte except itself, the archive binding
written after the archive exists, and operational publication-state files.
Archive members are sorted, timestamped deterministically, and assigned
normalised permissions. A fresh extraction must reproduce the mathematical and
document gates.

## Trust boundary

The imported monodromy and finite-group classifications are pinned and scoped
but not re-proved. Lean and exact CAS cover stated consequences, not every
semantic bridge. Producer replay, deterministic bytes, a DOI, and public
readback do not establish independent reproduction, peer review, formal proof,
novelty, priority, or truth.
