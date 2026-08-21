# Internal review: amplitude and Laurent extension

**Review date:** 21 August 2026
**Decision:** GO for internal candidate circulation; HOLD for external theorem
publication.

## Scope reviewed

The review covered the manuscript, polynomial-amplitude certificate engine,
Laurent inverse-series engine, endpoint controls, frozen receipt, claim ledger,
literature audit, rendered HTML/PDF, and predecessor preservation.

## Mathematical findings

1. **Polynomial-amplitude theorem:** the replacement of the seed pullback
   \(d\xi\) by \(d(G(\xi))\) is compatible with the existing formal moment
   isomorphism. Differentiation kills only the trace constant and cannot erase
   a nonzero residue channel. The Kummer-channel Vandermonde argument therefore
   gives the asserted rank.
2. **Rank-zero criterion:** empty non-trace support makes the primitive constant
   on generic fibres, hence an element of
   \(\mathbf C(P)\cap\mathbf C[x]=\mathbf C[P]\). This is sharper and cleaner
   than a finite coefficient argument.
3. **Zero-cycle criterion:** the Fourier equivalence is exact for a specified
   cycle. The manuscript correctly avoids upgrading it to a composition-only
   theorem for all balanced cycles.
4. **Endpoint classification:** the table is a valid specialisation of the
   Pakovich--Muzychuk theorem provided the v0.6 all-degree right-factor audit is
   accepted. Incomparable Dickson and exceptional factors are correctly
   represented by sums of subalgebras.
5. **Laurent theorem:** the change-of-variable residue identity applies to
   arbitrary Laurent one-forms, including the \(z^{-1}dz\) class. Exact-form
   amplitudes are a corollary. The PPZ case study is correctly used to reject a
   global composition-only overclaim.

## Computational findings

- Ordinary and optimised exact replays are byte-identical.
- The frozen receipt matches.
- The polynomial engine compares twisted-Krylov rank with an independently
  extracted inverse support.
- The Laurent engine compares local inverse coefficients with direct residue
  extraction at every tested moment.
- A logarithmic amplitude, target scaling, deck symmetry, and nonvanishing are
  represented among the controls.
- Two semantic corruptions are detected after recomputing their outer hashes.
- Sixteen endpoint moments are finite regressions only and are labelled as
  such.

## Publication and visual findings

The first close visual pass found a real renderer defect: KaTeX's overlaid
not-equal glyph split into a slash and detached equals sign under WeasyPrint.
The source now states those relations in renderer-stable words. The final
12-page PDF has been visually inspected page by page. The classification table
is readable, equations are typeset, no content is clipped, all required
bookmarks resolve, and the raw-TeX preflight reports zero findings.

## Remaining objections

- No external specialist has reviewed the amplitude proof or endpoint table.
- The endpoint table remains conditional on the unrefereed v0.6 Atlas.
- The implementation is one SymPy lineage, not a genuinely independent CAS or
  proof-assistant formalisation of this successor.
- The literature audit is not an exhaustive MathSciNet, zbMATH, or
  citation-forward closure and cannot certify priority.
- No finite all-Laurent normal-form theorem has been proved.

These are external-assurance and open-classification limits, not concealed
failures of the stated candidate theorems.
