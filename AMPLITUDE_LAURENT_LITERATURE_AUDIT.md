# Literature audit for the amplitude and Laurent extension

**Audit date:** 21 August 2026.

## Method

The audit used primary full texts on arXiv and DOI metadata cross-checks from
Crossref.  It also compared the claims with the source-history Laurent and
zero-cycle materials in the Atlas bundle.  The search was designed to locate
load-bearing theorems and counterexamples, not to establish priority.

## Load-bearing sources

1. **Pakovich and Muzychuk, “Solution of the polynomial moment problem.”**
   Primary preprint: <https://arxiv.org/abs/0710.4085>.  DOI metadata verified
   as *Proceedings of the London Mathematical Society* 99(3), 633–657,
   DOI 10.1112/plms/pdp010.  Used for the necessary-and-sufficient sum over
   endpoint-equal right factors.
2. **Pakovich, “Generalized ‘second Ritt theorem’ and explicit solution of the
   polynomial moment problem.”** DOI metadata verified as *Compositio
   Mathematica* 149(4), 705–728, DOI 10.1112/S0010437X12000620.  Used as an
   explicit right-factor refinement and consistency check.
3. **Álvarez, Bravo, and Mardešić, “Vanishing Abelian integrals on
   zero-dimensional cycles.”** Primary preprint:
   <https://arxiv.org/abs/1101.1777>.  DOI metadata verified as *Proceedings of
   the London Mathematical Society* 107(6), 1302–1330,
   DOI 10.1112/plms/pdt012.  Used to bound composition claims for balanced
   zero-cycles.
4. **Pakovich, Pech, and Zvonkin, “Laurent polynomial moment problem: A case
   study.”** Primary preprint: <https://arxiv.org/abs/0910.2691>.  DOI metadata
   verified as *Contemporary Mathematics* 532, 177–194,
   DOI 10.1090/conm/532/10490.  Its indecomposable example rules out presenting
   simple composition as a general all-Laurent classification.

## Source-history findings

The inherited `source-history/laurent-moment-exploratory` programs are useful
finite experiments but are not theorem certificates.  Their reported
“mismatches” for `z^2+z^-2` and `z^3+z^-3` compare observations only with a
composition prediction.  Both phases have an evident deck symmetry
`L=R(z^d)`, which supplies an additional vanishing mechanism.  The successor
corrects the interpretation rather than altering historical files.

The inherited zero-cycle material correctly identified two primitives for the
exceptional phase `(x^4+x)^3`.  The successor replaces numerical borderline
decisions with the exact Fourier-support criterion and exact rational
arithmetic.

## Provisional novelty statement

The search located broad twisted de Rham literature and the named moment
problem results, but did not locate the exact arbitrary-amplitude identity

`cyclic rank of [A dx] = non-trace support size of G(xi)`.

This is a provisional non-location, not a novelty or priority certificate.

## Coverage limitations

This audit lacks an exhaustive topical MathSciNet search, exhaustive zbMATH
search, complete citation-forward closure across every index, non-English
full-text coverage, thesis coverage, and unpublished-work coverage.  Crossref
confirms bibliographic identity, not mathematical correctness.  The cited
primary texts were inspected for the roles assigned above; no source is used
to support a stronger claim than it states.
