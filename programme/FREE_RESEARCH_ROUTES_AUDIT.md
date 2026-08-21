# Free research routes audit

**Date:** 21 August 2026  
**Snapshot:** `free_research_routes_snapshot.json`  
**Canonical snapshot SHA-256:**
`e06fed0e4d4a67e815e151314a15a97a6a12303957dfb56d51ac8eb8ca223dc8`  
**Decision:** broader public-route coverage achieved; novelty remains bounded
uncertainty

## 1. Needed objects

The remaining access problem was divided into five objects rather than called
“a MathSciNet problem”:

1. topical mathematical-literature discovery;
2. bibliographic and identifier verification;
3. forward-citation inventories for named seed papers;
4. lawful full-text locations for theorem comparison; and
5. exact diagnosis of fields that free routes do not expose.

The executable snapshot generator is
`tools/run_free_research_routes_audit.py`.  It stores compact provider records,
query strings, HTTP outcomes, result counts, retrieval time, and a canonical
hash.  Provider result sets remain separate.  It does not merge disagreement
into a fictional universal citation graph.

## 2. Route ladder used

| Object | Route used | Outcome | Material limit |
|---|---|---|---|
| topical mathematics search | zbMATH Open REST API | 8 exact/broadened queries replayed; all 129 broadened records retrieved | API-exposed zbMATH content is not all mathematical writing |
| DOI metadata | Crossref REST API | all 3 DOI seeds resolved | metadata and Crossref citation counts are not full text or complete citation graphs |
| forward citations | OpenAlex REST API | complete one-page result sets for all 3 DOI seeds | provider coverage only |
| independent forward-citation graph | OpenCitations Index REST API | complete returned edge sets for all 3 DOI seeds | provider coverage only; free token is encouraged but no-key requests succeeded |
| independent title-level cross-check | Semantic Scholar Academic Graph REST API | complete returned one-page sets for all 3 DOI seeds | provider coverage and current no-key quota only |
| Mathematical Reviews identity | AMS Batch MR Lookup | 14 unique bibliography matches in the earlier audit | not topical search, reviews, or citation-network access |
| full text | arXiv, EuDML, author repositories, publisher OA pages, and DOI landing pages | theorem statements compared where lawful public text existed | version and licence vary by item |

OpenAlex, OpenCitations, Semantic Scholar, Crossref, and zbMATH calls used
documented official endpoints.  No Google Scholar scraping, paywall bypass,
credential sharing, or scripted full-MathSciNet search was attempted.

## 3. Replayed zbMATH Open search

| Query | Reported/retrieved | Finding |
|---|---:|---|
| `"fixed-seed cyclicity"` | 0/0 | `empty_result`; weak exact-string evidence only |
| `"inverse-root support"` | 0/0 | `empty_result`; weak exact-string evidence only |
| `"exponential Gauss-Manin" AND polynomial` | 0/0 | `empty_result`; broadened search required |
| `"polynomial monodromy" AND composition` | 0/0 | `empty_result`; broadened search required |
| `Gauss-Manin polynomial` | 69/69 | antecedent analytic literature recovered |
| `monodromy polynomial composition` | 29/29 | Burda--Khovanskii and composition/monodromy literature recovered |
| `"polynomial moment problem"` | 12/12 | moment and composition literature recovered |
| `"linear relations" roots polynomial` | 19/19 | root-relation literature recovered |

zbMATH returns HTTP 404 for some valid zero-hit searches.  The generator
records the transport status and provider-specific `empty_result`
interpretation separately; it does not report those calls as network failure.

## 4. Citation-graph comparison

| DOI seed | Crossref count | OpenAlex | OpenCitations | Semantic Scholar |
|---|---:|---:|---:|---:|
| Girstmair, root relations | 15 | 25 | 17 | 25 |
| Pakovich--Muzychuk, polynomial moment problem | 27 | 28 | 32 | 64 |
| Combot, root-relation algorithm | 3 | 1 | 3 | 5 |

The snapshot also records identifier-level overlaps.  Examples include 16 of
17 OpenCitations Girstmair edges matching the OpenAlex set, 27 of 32
OpenCitations Pakovich--Muzychuk edges matching OpenAlex, and only 1 of 3
OpenCitations Combot edges matching OpenAlex.  These are coverage differences,
not contradictory facts about the papers.

Complementary records surfaced work on invariant/additive/multiplicative
relations between polynomial roots, exponent lattices, zero-cycle centre
problems, polynomial moments, decomposition conditions, and matrix-group
algorithms.  Particularly close titles were screened, including *A fast
algorithm for computing multiplicative relations between the roots of a
generic polynomial*, *On Invariant Relations between Zeros of Polynomials*,
*Characterizing Triviality of the Exponent Lattice of a Polynomial Through
Galois and Galois-Like Groups*, and the recent works citing Combot.  None of
the returned title/abstract/theorem material inspected states the assembled
fixed-seed inverse-root-span equivalence together with the all-degree
rank-at-most-three coefficient classification and the complete
rank-preserving-extension list.

That sentence is a non-location result inside the named public sets, not proof
that no antecedent exists.

## 5. MathSciNet diagnosis

The needed but still missing object is **full topical MathSciNet discovery and
its review/citation fields**.  The finding is
`paid_only_for_required_capability`, not `tool_not_discovered` and not
`empty_result`.

AMS free tools lawfully provide MR Lookup/MRef bibliographic matching and other
limited functions.  They do not expose an official free API for the required
full topical search.  AMS terms also prohibit general automated searching or
downloading outside AMS-provided free tools.  A third-party marketplace
listing without source, licence, AMS authorization, or a documented credential
model is not an acceptable workaround.

The next lawful route requiring user action would be an authorized subscriber
conducting a manual topical search and exporting a bounded, terms-compliant
result list for screening.  That would strengthen coverage, but it still could
not certify universal novelty.

## 6. Assurance boundary

This supplement closes the avoidable blanket omission of zbMATH and adds two
genuinely different citation graphs plus Crossref metadata.  It supports
“complete within the retrieved provider result sets on 21 August 2026.”

It does **not** support “exhaustive literature search,” “all citation-forward
coverage,” “no prior work,” “first,” “novel,” or a priority claim.  Unindexed
work, unpublished work, non-English full text, immature coverage of 2026
preprints, and subscriber-only MathSciNet fields remain outside the evidence.
