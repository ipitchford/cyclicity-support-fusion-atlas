# Reproducing the combined 0.7.0 candidate

Run all commands from the candidate directory. The procedure keeps
mathematical replay, document generation, and artifact integrity as separate
checks so that a failure retains a useful meaning.

## 1. Verify the mathematical components

```bash
python3 run_global_completion_checks.py
python3 run_amplitude_laurent_checks.py
```

The first command transitively checks the fixed-seed predecessor chain,
semantic receipts, mutation controls, independent exact CAS layer, and global
Lean/CAS replay in ordinary and optimised modes. The second requires ordinary
and optimised amplitude/Laurent replays to emit byte-identical receipts.

Expected terminal lines are:

```text
GLOBAL ALL-DEGREE COMPLETION GATE PASS
AMPLITUDE-LAURENT GATE PASS
```

Silence, timeout, or an earlier green line without the terminal receipt is not
a pass.

## 2. Rebuild the unified sources and paper

```bash
python3 tools/build_combined_sources.py
python3 tools/render_combined_paper.py
```

The first command deterministically constructs the renumbered Sections 1--21
from the preserved component sources. The second creates:

- `Inverse-Root-Support-Amplitudes-and-Laurent-Moments.html`;
- `Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf`.

The renderer must report a 25-page PDF, zero exposed-TeX findings, successful
bookmark finalisation, and qpdf validation.

Run the integrated document and lineage gate:

```bash
npm run check:combined
```

It must terminate with `COMBINED RELEASE INTEGRITY GATE PASS`.

## 3. Test deterministic document bytes

```bash
cp Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf /tmp/combined-first.pdf
cp Inverse-Root-Support-Amplitudes-and-Laurent-Moments.html /tmp/combined-first.html
python3 tools/render_combined_paper.py
cmp /tmp/combined-first.pdf Inverse-Root-Support-Amplitudes-and-Laurent-Moments.pdf
cmp /tmp/combined-first.html Inverse-Root-Support-Amplitudes-and-Laurent-Moments.html
```

Both `cmp` commands must be silent and return zero.

## 4. Verify the bound release files

```bash
shasum -a 256 -c COMBINED_MANIFEST.sha256
```

The manifest binds the combined paper, generated sources, component sources,
replay programs and receipts, assurance records, and preserved predecessor
PDFs. It does not assert that unlisted workspace files are unchanged.

## 5. Perform visual QA

Render all PDF pages to images and inspect them page by page. At minimum check:

- bilingual abstracts and the status/dependency front matter;
- Kummer equations and the all-degree theorem;
- the polynomial-amplitude theorem;
- the endpoint classification table;
- the Laurent coefficient formula;
- references, limitations, declarations, and the final page.

This step is mandatory because successful text extraction cannot detect
literal TeX displayed to the reader, detached relation glyphs, clipping,
overprinting, or awkward page breaks.

## Interpretation

A complete pass reproduces the internal `0.7.0-candidate` artifact and its
encoded evidence. It does not supply external peer review, an independent
proof, a priority determination, a DOI, or a public release.
