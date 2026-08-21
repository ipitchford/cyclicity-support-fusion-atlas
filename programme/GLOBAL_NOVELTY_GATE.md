# Novelty gate: all-degree inverse-support classification

**Search date:** 21 August 2026  
**Corpus boundary:** parent bibliography; arXiv and primary manuscripts;
zbMATH Open REST results; complete retrieved OpenAlex citing sets for the five
seed works below; OpenCitations and Crossref checks for three stable DOI seeds;
Semantic Scholar cross-checks; publisher and DOI records  
**Outcome:** **BOUNDED UNCERTAINTY — no absolute novelty or priority language;
the later mathematical PASS permits only a clearly labelled public unrefereed
candidate release**

## 1. Frozen claim

The target is the assembled all-degree statement over \(\mathbf C\): classify
all polynomial phases for which the fixed seed \(dx\) has cyclic rank at most
three, equivalently reduced inverse-root span at most three; classify every
rank-preserving outer extension through all complete decompositions and Ritt
moves; and close the cubic-over-power step by an all-\(m\) Kummer-line
normalizer lemma.  The claim is relative to the named external classification
theorems.

Excluded are claims to have invented twisted de Rham reduction, cyclic-vector
theory, Picard--Fuchs computation, root-relation theory, Ritt decomposition,
primitive polynomial-monodromy classification, or finite projective-group
classification.  No claim to absolute priority, external reproduction, peer
review, or field-wide impact is permitted by this gate.

## 2. Canonical form and fingerprints

| Item | Search form |
|---|---|
| analytic invariant | generic minimal scalar ODE order of all rapid-decay periods with seed \(dx\) |
| algebraic invariant | dimension of the reduced constant span of the roots of \(P(X)-t\) |
| combinatorial form | inverse-support residues modulo \(\deg P\), trace class removed |
| decomposition form | equality/intersection of block root spans under imprimitivity systems |
| extension fingerprint | powers, Dickson chains, odd-centred cubic square, quartic cubic collision |
| exceptional support | degree 12 with support \(\{1,7,10\}\) |
| Kummer fingerprint | transposition eliminant \(2(\zeta+1)^2\) |

## 3. Cross-domain alias map

| Literature | Aliases searched |
|---|---|
| exponential periods | polynomial Laplace integrals, exponential Gauss--Manin, twisted de Rham quotient, fixed cyclic vector, minimal Picard--Fuchs order |
| Galois/monodromy | linear relations among roots, generic inverse roots, permutation-module quotient, primitive polynomial monodromy |
| decomposition | imprimitivity systems, polynomial composition, Ritt moves, generalized second Ritt theorem |
| dynamical systems | zero-dimensional Abelian integrals, polynomial moments, balanced zero-cycles, composition condition |
| finite groups | low-dimensional projective representation, monomial group, octahedral \(S_4\), root-span quotient |

## 4. Concentric search log

| Ring | Query families | Primary results inspected | Consequence |
|---|---|---|---|
| exact strings | "inverse-root support", "fixed-seed cyclicity", "Fourier fusion" with polynomial and monodromy aliases | the two predecessor Evidence Press/GitHub releases; no earlier exact-title collision located | self-records only; no priority inference |
| formula/fingerprint | inverse-root span, support \(\{1,7,10\}\), cubic-over-power, rank-preserving polynomial extension | no equivalent all-degree theorem located in indexed results | negative evidence only |
| analytic aliases | twisted de Rham quotient, exponential Gauss--Manin, Laplace-type reduction, fixed cyclic vector | Jesse Forjan, *Reduction, Exponential Gauss--Manin Systems, and Stokes Phenomena* (Zenodo, May 2026) | broad reduction/Pfaffian framework is prior adjacent work, not an available novelty claim |
| root relations | linear relations among polynomial roots, Galois permutation representation | Girstmair (1999/2003); Kitaoka (2018) | root-relation machinery is established prior art |
| zero-cycles/moments | zero-dimensional Abelian integrals, polynomial moment problem, decomposition condition | Pakovich--Muzychuk; Pakovich; Alvarez Sanchez--Bravo Trinidad--Mardesic; Gavrilov--Pakovich | vanishing and decomposition frameworks are direct antecedents; whole-block equality is not a complete zero-cycle theory |
| decomposition | complete decompositions, Ritt transformations, generalized second Ritt theorem | Ritt; Zieve--Muller; Pakovich | all-decomposition/Ritt machinery is established prior art |
| monodromy | low-dimensional primitive polynomial monodromy, compositions of indecomposables, inversion in low-degree radicals | Burda--Khovanskii; Behajaina--Koenig--Neftin | strong bridge and source dependency; the recent length-two theorem is especially close to the extension audit |
| computational root relations | exact algorithms for rational additive and multiplicative relations among roots | Combot (electronically published 2025; 2026 issue) | direct prior art for computing root relations of a fixed rational polynomial; not an exact collision with generic inverse-root spans |

### Open-index expansion and forward-citation coverage

The expanded search used the public zbMATH Open REST endpoint.  Exact-string
queries for `fixed-seed cyclicity` and `inverse-root support` returned zero
records.  Exact Boolean searches for `exponential Gauss-Manin AND polynomial`
and `polynomial monodromy AND composition` also returned zero.  Broader
queries were therefore screened rather than treated as negative exact-string
evidence:

| zbMATH Open query | Reported records | Screening consequence |
|---|---:|---|
| `Gauss-Manin polynomial` | 69 | established Gauss--Manin antecedents located; no exact assembled theorem found |
| `monodromy polynomial composition` | 29 | Burda--Khovanskii and recent composition-monodromy work recovered |
| `polynomial moment problem` | 12 | moment/composition/zero-cycle antecedents recovered |
| `linear relations roots polynomial` | 19 | Girstmair, Kitaoka, and Combot root-relation work recovered |

Forward-citation screening was complete **within the result sets returned by
OpenAlex on 21 August 2026**, with title/DOI deduplication and a Semantic
Scholar mismatch check:

| Seed work | OpenAlex reported/retrieved citing works | Semantic Scholar role | Outcome |
|---|---:|---|---|
| Girstmair, *Linear relations between roots of polynomials* | 25/25 | citation-list cross-check | adjacent algebra and algorithms; no exact theorem located |
| Pakovich--Muzychuk, *Solution of the polynomial moment problem* | 28/28 | citation-list cross-check | extensive moment/composition literature; no exact theorem located |
| Combot, *Computing linear relations between polynomial roots* | 1/1 | five records visible in the broader cross-check | computational root-relation applications; no exact theorem located |
| Behajaina--Koenig--Neftin | 0/0 | zero citations returned | too recent for meaningful negative inference |
| Forjan | 0/0 | zero citations returned | too recent for meaningful negative inference |

“Complete” here refers only to each API's retrieved result set, not to all
citations in existence.  Differences between OpenAlex and Semantic Scholar
were retained as index-coverage differences, not silently merged into a
claim of exhaustiveness.

A later reproducible free-route supplement compared the three stable DOI seeds
across Crossref, OpenAlex, OpenCitations, and Semantic Scholar.  Counts were
respectively `15/25/17/25` for Girstmair, `27/28/32/64` for
Pakovich--Muzychuk, and `3/1/3/5` for Combot.  Identifier-level overlaps and
all compact returned records are frozen in
`programme/free_research_routes_snapshot.json`; the route interpretation is
in `programme/FREE_RESEARCH_ROUTES_AUDIT.md`.  The disagreement strengthens
the case for multi-index screening while ruling out any claim that one graph
is exhaustive.

Primary online records inspected during this gate include:

- [Forjan, *Reduction, Exponential Gauss--Manin Systems, and Stokes Phenomena*](https://zenodo.org/records/20026908);
- [Behajaina--Koenig--Neftin, *Monodromy groups of polynomials of composition length 2*](https://arxiv.org/abs/2603.27609);
- [Burda--Khovanskii, *Polynomials invertible in k-radicals*](https://arxiv.org/abs/1209.5137);
- [Zieve--Muller, *On Ritt's polynomial decomposition theorems*](https://arxiv.org/abs/0807.3578);
- [Pakovich--Muzychuk, *Solution of the polynomial moment problem*](https://arxiv.org/abs/0710.4085);
- [Pakovich, *Generalized second Ritt theorem and explicit solution of the polynomial moment problem*](https://arxiv.org/abs/0908.2508);
- [Alvarez Sanchez--Bravo Trinidad--Mardesic, *Vanishing Abelian integrals on zero-dimensional cycles*](https://arxiv.org/abs/1101.1777);
- [Kitaoka, *Linear relations among roots of a polynomial*](https://arxiv.org/abs/1810.06791); and
- [Girstmair, *Linear relations between roots of polynomials*](https://eudml.org/doc/207259); and
- [Combot, *Computing linear relations between polynomial roots*](https://doi.org/10.1090/mcom/4081).

## 5. Collision and bridge analysis

### COLLISION: broad reduction and decomposition claims

The statements that polynomial exponential periods admit finite twisted-de
Rham reduction and Pfaffian/Picard--Fuchs systems, that root relations are
controlled by Galois permutation modules, and that all complete polynomial
decompositions are connected by Ritt moves are established prior art.  None
may be promoted as a new general method.

### BRIDGE: low-dimensional monodromy and composition kernels

Burda--Khovanskii's low-degree-radical classification and
Behajaina--Koenig--Neftin's length-two composition-kernel theorem sit very
close to the present classification.  The candidate explicitly imports these
results.  The possible contribution is the bridge from the fixed seed to
reduced inverse-root span and the deduction of the precise rank-preserving
extension list, not the group classifications themselves.

### BOUNDED UNCERTAINTY: exact assembled theorem

No inspected source states the exact equivalence

\[
 q(P,dx)=\dim W_P
\]

together with the displayed all-degree rank-at-most-three coefficient
families and the four rank-preserving extension mechanisms.  This is a
non-location result, not proof of novelty.  The recent date and adjacency of
the imported 2026 monodromy preprint make absolute priority language
especially inappropriate.

## 6. Missingness audit and attempted workarounds

- **MathSciNet:** not searched as a full topical corpus.  The AMS-authorized
  Batch MR Lookup tool was used to match the candidate bibliography: thirteen
  fully specified journal entries matched uniquely in the first batch, and
  Burda--Khovanskii matched after adding its 2016 journal metadata.  The BKN,
  Zieve--Müller, and Kitaoka title-only preprint queries returned no unique
  match.  This closes bibliographic identity checking, not topical discovery
  or citation-network coverage.  The third-party “MathSciNet Research
  Interface” remained unused because it disclosed no source licence, AMS
  authorization, or credential model.
- **zbMATH:** addressed through the public zbMATH Open REST API with exact and
  broadened queries and reported counts above.  This closes the earlier
  blanket omission, but not non-indexed material.
- **Citation-forward coverage:** addressed to completion within the retrieved
  OpenAlex citing sets for five seeds and cross-checked against Semantic
  Scholar, with OpenCitations and Crossref added for three DOI seeds.  It is
  not exhaustive across Google Scholar, MathSciNet, private indexes, or
  citations not yet ingested by those APIs.
- **Remaining limitations:** non-English full-text search, unpublished seminar
  notes, author enquiries, and very recent unindexed work.  Search-engine and
  citation indexing for the 2026 preprints is necessarily immature.

These residual limitations cap the novelty result at bounded uncertainty.

## 7. Outcome by contribution unit

| Contribution unit | Outcome | Confidence | Allowed wording | Forbidden wording |
|---|---|---:|---|---|
| twisted reduction/Pfaffian systems | COLLISION | high | "uses established twisted-de Rham reduction" | "introduces the general reduction framework" |
| root-relation and primitive-monodromy inputs | COLLISION | high | "combines cited classifications" | "classifies primitive polynomial monodromy" |
| all-decomposition/Ritt machinery | COLLISION | high | "uses Ritt moves to make the atlas invariant" | "new Ritt theorem" |
| fixed-seed rank/root-span bridge | BOUNDED UNCERTAINTY | medium | "exact assembled formula not located in the bounded search" | "first" or "novel" |
| all-degree rank-at-most-three classification | BOUNDED UNCERTAINTY | medium | "unrefereed theorem candidate relative to named imports" | settled priority or definitive field claim |
| coefficient-stratified all-\(m\) Kummer transport | BOUNDED UNCERTAINTY | medium | "standalone repaired candidate supplied in this successor" | claim that its ingredients are new or externally validated |
| verification package | CLEAR TO RELEASE | high | "newly constructed reproducibility artifact in this release" | external independent verification |

## 8. Decision and rerun triggers

**BOUNDED UNCERTAINTY.**  The repaired mathematical gates subsequently passed.
A public unrefereed candidate is compatible with this novelty gate only if it
uses contribution-specific language, clearly credits the collisions and
bridges above, and makes no absolute novelty or priority claim.  This update
does not convert the bounded search into exhaustive coverage.

Rerun the gate after an authorized full topical MathSciNet search, external specialist
report, new version or companion to arXiv:2603.27609, discovery of an
equivalent fixed-seed/root-span formula, material OpenAlex/Semantic Scholar
count changes, or any promotion from "candidate" to an established theorem
claim.
