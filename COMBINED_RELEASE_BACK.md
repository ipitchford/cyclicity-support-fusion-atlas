# Imported classification sources

The all-degree proof imports four classification inputs.

- Behajaina, König, and Neftin [BKN26], Theorems 2.3, 2.4, 2.7, and 3.3,
  provide the length-two block kernels and characteristic-zero primitive
  monodromy alternatives. This is a 2026 preprint whose source-side Magma
  calculations are not independently certified here.
- Burda and Khovanskii [BK16] transmit the Müller primitive-polynomial list and
  provide a source-to-list comparison.
- Calbetó [C25], Tables 1 and 2, supplies the low-dimensional finite
  projective-group lists.
- Zieve and Müller [MZ08] supply the modern Ritt-decomposition framework.

The endpoint classification imports the necessary-and-sufficient polynomial
moment theorem of Pakovich and Muzychuk [PM09] and uses Pakovich's explicit
right-factor refinement [P13]. Álvarez, Bravo, and Mardešić [ABM13] and
Pakovich, Pech, and Zvonkin [PPZ10] delimit the zero-cycle and Laurent
composition claims.

# References

**[ABM13]** Álvarez, A., Bravo, J. L., and Mardešić, P. (2013). “Vanishing
Abelian integrals on zero-dimensional cycles.” *Proceedings of the London
Mathematical Society* 107(6), 1302–1330.
[doi:10.1112/plms/pdt012](https://doi.org/10.1112/plms/pdt012).

**[BKN26]** Behajaina, A., König, J., and Neftin, D. (2026). “Monodromy groups
of polynomials of composition length 2.” *arXiv preprint*, version 2.
[arXiv:2603.27609](https://arxiv.org/abs/2603.27609).

**[BK16]** Burda, Y., and Khovanskii, A. (2016). “Polynomials invertible in
k-radicals.” *Arnold Mathematical Journal* 2(1), 121–138.
[doi:10.1007/s40598-015-0036-0](https://doi.org/10.1007/s40598-015-0036-0);
[arXiv:1209.5137](https://arxiv.org/abs/1209.5137).

**[C25]** Calbetó, G. G. (2025). “On the finite irreducible subgroups of
\(GL_n(\mathbf C)\) and \(PGL_n(\mathbf C)\).” *arXiv preprint*, version 1.
[arXiv:2510.00718](https://arxiv.org/abs/2510.00718).

**[MZ08]** Zieve, M. E., and Müller, P. (2008). “On Ritt's polynomial
decomposition theorems.” *arXiv preprint*.
[arXiv:0807.3578](https://arxiv.org/abs/0807.3578).

**[P13]** Pakovich, F. (2013). “Generalized ‘second Ritt theorem’ and explicit
solution of the polynomial moment problem.” *Compositio Mathematica* 149(4),
705–728.
[doi:10.1112/S0010437X12000620](https://doi.org/10.1112/S0010437X12000620).

**[PM09]** Pakovich, F., and Muzychuk, M. (2009). “Solution of the polynomial
moment problem.” *Proceedings of the London Mathematical Society* 99(3),
633–657. [doi:10.1112/plms/pdp010](https://doi.org/10.1112/plms/pdp010).

**[PPZ10]** Pakovich, F., Pech, C., and Zvonkin, A. (2010). “Laurent
polynomial moment problem: A case study.” *Contemporary Mathematics* 532,
177–194. [doi:10.1090/conm/532/10490](https://doi.org/10.1090/conm/532/10490).

::: {.backmatter}

# Data and code availability

The candidate package contains the component manuscripts, generated combined
sources, exact programs, Lean sources, CAS checks, negative controls, frozen
receipts, claim ledgers, literature audits, and deterministic rendering tools.
No confidential data are used. Generated combined sources identify their
builder and can be reproduced from the preserved component files.

# Limitations

The all-degree theorem imports named results on primitive polynomial monodromy,
finite projective linear groups, and composition-length-two kernels. The
package does not formalise those classifications, algebraic function-field
integrality, Kummer theory, or Ritt theory in full. The 2026 kernel source is a
current preprint and includes source-side Magma computations not independently
reproduced here.

The amplitude and Laurent programs verify exact encoded consequences and
examples. They do not constitute independent formal proofs of every semantic
bridge. Finite zero prefixes are not promoted to persistent Laurent
vanishing. Theorem 18.1 is an exact coefficient criterion for a specified
input, not a finite normal-form classification of every Laurent pair.

The literature audit used named public databases, open full texts, Crossref,
OpenCitations, OpenAlex, Semantic Scholar, zbMATH Open, and AMS Batch MR
Lookup. It was not an exhaustive topical MathSciNet search, universal
citation-forward closure, non-English full-text search, or unpublished-work
survey. No absolute novelty or priority claim is made.

# Ethics declaration

This mathematical research uses no human participants, animals, personal
data, or sensitive datasets. No ethics approval was required.

# Author contributions (CRediT)

**Anonymous:** Conceptualization, Formal analysis, Investigation, Methodology,
Software, Validation, Writing—original draft, and Writing—review and editing.
Ian Pitchford served as repository maintainer and Evidence Press publisher;
this operational role is not scholarly authorship.

# Conflict of interest

No conflict of interest is declared.

# Funding

No external funding is declared.

# AI disclosure

OpenAI language-model and Codex systems assisted with source discovery, proof
development, drafting, exact computation, adversarial tests, citation checks,
and formatting. Their outputs are producer-side work products, not independent
expert evidence. The package preserves proofs, source audits, receipts,
negative controls, and correction history. No human peer review or unaffiliated
reproduction is inferred from model agreement.

# Candidate citation and rendering notice

Scholarly creator: **Anonymous**. Version: **0.7.0-candidate, combined
manuscript**. Exact-version DOI:
[10.5281/zenodo.22049564](https://doi.org/10.5281/zenodo.22049564).

Static equation rendering uses KaTeX 0.18.4 under the MIT licence. qpdf is used
for structural validation and deterministic PDF canonicalisation. These tools
remain third-party software under their own licences.

:::
