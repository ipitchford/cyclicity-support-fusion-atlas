# Reproducing the amplitude and Laurent extension

From the repository root, run:

```bash
python3 run_amplitude_laurent_checks.py
```

A passing run prints:

```text
[PASS] ordinary exact replay
[PASS] optimized exact replay
[PASS] byte-identical receipts ...
[PASS] frozen receipt parity
AMPLITUDE-LAURENT GATE PASS
```

The principal command-line analysers are:

```bash
python3 src/amplitude_support.py --phase '(x**4+x)**3' --amplitude '4*x**3'
python3 src/laurent_moments.py --phase 'z**2+z**-2' --primitive 'z'
python3 src/laurent_moments.py --phase 'z+z**-1' --amplitude 'z**-1'
```

The first command compares exact twisted-Krylov rank with primitive inverse
support. The second checks an exact-form Laurent prefix; the third checks a
Laurent one-form with a logarithmic primitive. A **finite_prefix_zero** status
is deliberately not an all-moment certificate.

To render and validate the paper after the renderer has been generated, run:

```bash
python3 tools/render_amplitude_laurent_paper.py
python3 tools/pdf_tex_preflight.py Amplitude-Weighted-Cyclicity-and-Laurent-Moment-Channels.pdf
```

The renderer enables Pandoc's single-backslash TeX-math extension, converts
KaTeX to static MathML, removes hidden TeX annotations, and then scans the
reader-facing PDF for raw control syntax. A qpdf canonicalisation is followed
by a fixed-length, content-derived trailer identifier and a qpdf structural
check, so repeated builds have stable bytes.
