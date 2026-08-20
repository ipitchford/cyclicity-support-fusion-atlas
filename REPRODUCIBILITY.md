# Reproducibility

## Authoritative environment

`ENVIRONMENT.txt` records macOS 26.5.2 arm64, Python 3.14.6, SymPy 1.14.0,
NumPy 2.4.2, mpmath 1.3.0, PyMuPDF 1.27.1, Pandoc 3.9, Chrome
151.0.7922.138 and qpdf 12.3.2. `requirements.txt` pins the Python packages.
The earlier Python 3.12.3 receipt is retained as historical cross-version
evidence, not as a competing current specification.

## One-command release gate

From the package root:

```bash
python3 run_core_checks.py
```

The default command:

1. verifies every package file against `MANIFEST.sha256` and rejects unlisted
   or stale entries;
2. runs structural support/fusion tests, the Fraction audit and the
   Fourier–Gamma spot check;
3. runs exact-rank, support/rank, deep-support, fusion/heredity, quartic-lift,
   family-blind sparse-search and extension-locus batteries;
4. reruns all 1,152 degree-5-to-20 Gröbner cases;
5. repeats the suite with assertions disabled under `python3 -O`;
6. requires ordinary and optimised receipts to be byte-identical and equal to
   `RELEASE_EXPECTATIONS.json`; and
7. rejects eight deliberate semantic corruptions, including fail-open exit
   behaviour and corrupted manifest or receipt bytes.

`--quick --development` omits the exhaustive sweep and frozen-byte checks. It
is a development convenience, not a release result.

## Document build

The archival HTML and DOCX are generated from `MANUSCRIPT.md` with Pandoc's
`tex_math_dollars` and `tex_math_single_backslash` extensions enabled. The
HTML uses native MathML and `paper.css`; headless Chrome prints the A4 PDF.
`tools/finalize_pdf.py` then adds folios, metadata and 26 content-resolved
bookmarks. `qpdf --check` and representative rasterised pages supply syntax
and visual controls. The exact commands and tools remain inspectable in the
package rather than being treated as manuscript evidence.

## Current full sweep

The current ordinary run completed all 1,152 cases in 573.2 seconds:

- 45 vacuous/full-family cases;
- 884 power-only radical-containment cases;
- 223 union-of-components cases;
- 0 anomalies; and
- 0 missing certificates.

The 674.2-second figure in inherited batch logs and the 855.6-second figure in
the v0.4 review are retained as different runs on different execution paths.
They are not merged into one provenance claim. The current authoritative
receipt omits wall time because time is environment-dependent.

The clean extracted-archive release replay completed the normal sweep in
602.2 seconds and the optimised sweep in 559.4 seconds. Both produced the same
case census and byte-identical receipts matching the frozen expectations; the
top-level command returned `RELEASE GATE PASS`.

## Per-case record

`receipts/atlas_case_records_d5_20.json` contains one record per support case:
degree, support, truncation bounds, predicted families and dimension,
stability result, defining-ideal and Gröbner-basis digests, outcome and
reduction witness, plus software versions.

## Trust and exclusion boundary

Exact arithmetic does not remove trust in the inverse-series implementation,
case enumeration, coefficient-family bridge or computer algebra system. No
proof-assistant checker is supplied.

The ODE, zero-cycle and Laurent programs are exploratory. They are preserved
but excluded because their existing controls can report `REVIEW` or a
dimension mismatch without failing.
