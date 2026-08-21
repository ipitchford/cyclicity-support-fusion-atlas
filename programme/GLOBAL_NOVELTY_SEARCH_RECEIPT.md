# Open-index novelty-search receipt

**Date:** 21 August 2026  
**Purpose:** close avoidable bibliography gaps without bypassing subscription
terms  
**Status:** complete for the exact public API result sets named below;
not a claim of universal citation exhaustiveness

## 1. Index and query ledger

The zbMATH Open REST search endpoint was queried with exact and broadened
forms.  Reported result counts were recorded before screening:

| Query | Count |
|---|---:|
| `"fixed-seed cyclicity"` | 0 |
| `"inverse-root support"` | 0 |
| `"exponential Gauss-Manin" AND polynomial` | 0 |
| `"polynomial monodromy" AND composition` | 0 |
| `Gauss-Manin polynomial` | 69 |
| `monodromy polynomial composition` | 29 |
| `"polynomial moment problem"` | 12 |
| `"linear relations" roots polynomial` | 19 |

Zero exact-string results are weak negative evidence only.  The broadened
sets recovered the expected antecedent literatures and were screened for the
fixed-seed/root-span equivalence, the rank-at-most-three coefficient atlas,
and the four extension mechanisms.

## 2. Forward-citation ledger

OpenAlex citing-work endpoints were followed through the complete result set
reported for each seed, with DOI/title deduplication:

| Seed | OpenAlex count | Retrieved |
|---|---:|---:|
| Girstmair root-relations paper | 25 | 25 |
| Pakovich--Muzychuk moment-problem paper | 28 | 28 |
| Combot root-relations algorithm | 1 | 1 |
| Behajaina--Koenig--Neftin composition-monodromy preprint | 0 | 0 |
| Forjan exponential Gauss--Manin preprint | 0 | 0 |

Semantic Scholar citation lists were checked as a separate coverage signal.
They exposed index-count differences, especially five visible citing records
for Combot versus one in OpenAlex.  All visible additional titles were
screened; none stated the target assembled theorem.  The discrepancy is
preserved as evidence that no single citation index is exhaustive.

## 3. Newly material adjacent source

Thierry Combot, *Computing linear relations between polynomial roots*,
Mathematics of Computation, DOI
[10.1090/mcom/4081](https://doi.org/10.1090/mcom/4081), electronically
published March 2025.  It provides polynomial-time algorithms for rational
linear and multiplicative relations among roots of a fixed rational
polynomial.  It is direct prior art for computational root-relation claims,
but its inspected statement does not give the generic inverse-root-span/
fixed-seed cyclic-rank equivalence or the all-degree coefficient atlas.

## 4. AMS free-tool audit

AMS Batch MR Lookup, which is expressly designed for scripted bibliographic
matching, was used in batches below its 100-query limit.  Unique matches were:

| Key | MR number |
|---|---:|
| ABM13 | MR3149848 |
| BD10 | MR2732247 |
| BE04 | MR2143558 |
| Gi99 | MR1692195 |
| Gi03 | MR2008728 |
| GL04 | MR2127946 |
| Hi09 | MR2534091 |
| HR08 | MR2443034 |
| PM09 | MR2551466 |
| Ri22 | MR1501189 |
| Sa99 | MR1671743 |
| Sa08 | MR2454354 |
| Co26 | MR4999549 |
| BK16 | MR3460044 |

Title-only queries for Behajaina--Koenig--Neftin, Zieve--Müller, and Kitaoka
were returned unchanged, meaning that the tool found no unique match from the
supplied data.  This was recorded as `no_unique_match`, not as absence from
the Mathematical Reviews database.

## 5. Remaining MathSciNet boundary

AMS states that full MathSciNet is available by subscription and that general
automated scripted searching/downloading is prohibited except through
AMS-provided free tools.  Batch MR Lookup closes bibliographic verification;
it does not expose topical publication search, reviews, or citation networks.
The inspected third-party marketplace listing supplied no package licence,
source repository, AMS authorization, subscription bypass rationale, or
authentication documentation.  It was therefore not used.

This receipt supports the wording “complete within the retrieved public API
sets.”  It does not support “exhaustive literature search,” “no prior work,”
or any absolute novelty/priority statement.

## 6. Free-route citation supplement

The later `free_research_routes_snapshot.json` replay added Crossref metadata,
OpenCitations Index edges, and a fresh Semantic Scholar inventory for the
three stable DOI seeds.  The canonical snapshot hash is
`e06fed0e4d4a67e815e151314a15a97a6a12303957dfb56d51ac8eb8ca223dc8`.

| Seed | Crossref count | OpenAlex | OpenCitations | Semantic Scholar |
|---|---:|---:|---:|---:|
| Girstmair root-relations paper | 15 | 25 | 17 | 25 |
| Pakovich--Muzychuk moment-problem paper | 27 | 28 | 32 | 64 |
| Combot root-relations algorithm | 3 | 1 | 3 | 5 |

The provider-specific counts and identifier overlaps are retained rather than
collapsed.  Additional titles concerned root-relation algorithms, exponent
lattices, polynomial moments, zero cycles, and matrix groups; none of the
inspected returned material stated the assembled target theorem.  See
`FREE_RESEARCH_ROUTES_AUDIT.md` for route diagnoses, lawful-access limits, and
the exact MathSciNet boundary.
