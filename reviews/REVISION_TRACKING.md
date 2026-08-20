# Revision tracking

Paper: *Inverse-Root Support and Fourier Fusion for Polynomial Exponential
Periods*

Round: 1  
Date: 20 August 2026  
Previous decision: Major revisions, hold before release  
Revision target: v0.5.0-candidate

## Major comments

| ID | Issue | Resolution | Location | Status |
|---|---|---|---|---|
| M1 | Atlas theorem absent from core gate; sweep fail-open; receipt path wrong; no per-case records; runtimes conflict | Full sweep added to ordinary and optimised release gate; anomaly and missing-certificate both exit nonzero; receipt path corrected; per-case ideal/GB digests and witnesses retained; semantic corruptions added; three runtimes identified as distinct runs | `run_core_checks.py`; `verification/battery4a_fast.py`; `verification/negative_controls.py`; `REPRODUCIBILITY.md`; `receipts/atlas_case_records_d5_20.json` | RESOLVED |
| M2 | Universal proofs too compressed in flagship | Complete v0.2 proof promoted: moment domain, descent, connection, unit-triangular matrix, active seed, Vandermonde, scalar extension, determinant equation and canonical-factor proof all explicit | Manuscript Sections 4–7 and 9.2 | RESOLVED |
| M3 | Decomposition/Ritt notation undefined; eleven diamonds absent | Complete suffix notation, rank-creating defects, telescoping formula, Fourier corollaries, fibre-product theorem and eleven-row table restored; higher-intersection claim narrowed | Manuscript Sections 8–10 | RESOLVED |
| M4 | Degree-12 residue omission; atlas parameter/equivalence boundaries incomplete | Four deck-compatible classes listed and class 4 excluded by heredity; Dickson convention, every degree/parameter restriction, lower-rank locus, moduli note, low-degree proofs and triangular coordinate map added | Manuscript Section 11 and Theorem 13.1 | RESOLVED |
| M5 | Verification targets old bytes/claims; weak lineage; local paths and missing wrapper | Old report preserved as historical; current T1–T6/F1/C1/A1 map and current-target receipt added; structured predecessor bridge added; subjective probabilities excluded from current evidence; local paths removed; authoritative one-command runner supplied | `CLAIM_EVIDENCE_MAP.json`; `verification/VERIFICATION_REPORT.md`; `verification/CURRENT_TARGET_RECEIPT.json`; Manuscript Section 1; `PROVENANCE.md` | RESOLVED |
| M6 | Literature positioning too thin; zero-cycle abstract overclaim | Hien–Roucairol, Behajaina–König–Neftin and Girstmair corrigendum added; theorem-level comparisons and access boundary supplied; zero-cycle language demoted to a suggested formulation; ODE corollary separated from demonstrations | Abstract; Manuscript Sections 14–15; `CITATION_AUDIT.md` | RESOLVED |

## Minor comments

| ID | Resolution | Location | Status |
|---|---|---|---|
| m1 | Twisted de Rham quotient typesetting corrected | Abstract | RESOLVED |
| m2 | `q(P,dx)` retained consistently; shorthand avoided | throughout | RESOLVED |
| m3 | Dickson convention defined | (13.1) | RESOLVED |
| m4 | Support ambient group and representative convention defined | Sections 3 and 13 | RESOLVED |
| m5 | Determinant non-vanishing replaced by explicit first-order equation | Corollary 7.4 | RESOLVED |
| m6 | Four degree-12 deck classes displayed before exclusion | Section 11 | RESOLVED |
| m7 | Equality stabiliser defined before canonical quotient | Corollary 8.5 | RESOLVED |
| m8 | Eleven diamonds included | Theorem 9.5 | RESOLVED |
| m9 | Rank-preserving and rank-creating levels defined by `delta_i` | Section 9.3 | RESOLVED |
| m10 | Affine equivalence and parameter identifications stated | Theorem 13.1 | RESOLVED |
| m11 | “Exact certificates” replaced by exact-arithmetic case records and precise witness types | Abstract; Section 13; package metadata | RESOLVED |
| m12 | Bostan–Dumas DOI corrected to suffix 515785 | References; citation audit | RESOLVED |
| m13 | Girstmair corrigendum added | References | RESOLVED |
| m14 | Zieve–Müller author order checked against cited arXiv version | References | RESOLVED |
| m15 | “Independent” replaced by “separate within programme”; historical title quarantined | `ASSURANCE.md`; `verification/VERIFICATION_REPORT.md` | RESOLVED |
| m16 | PDF rebuilt as a 32-page tagged A4 document with page numbers, 26 bookmarks and revised page-breaking CSS | final PDF | RESOLVED |
| m17 | Chinese abstract synchronised with final English ceiling | 中文摘要 | RESOLVED |
| m18 | Author-local paths removed from public-facing audit and provenance | `MATERIALS_AUDIT.md`; `PROVENANCE.md` | RESOLVED |
| m19 | One authoritative environment specification added; inherited 3.12.3 record labelled historical | `ENVIRONMENT.txt`; `REPRODUCIBILITY.md` | RESOLVED |
| m20 | “One lemma short” replaced by a precise identified proof obligation | Conjecture 13.2; `ATLAS_STATUS.md` | RESOLVED |

## Strengthening suggestions

| ID | Response | Status |
|---|---|---|
| S1 | Per-case machine records with ideal/GB digests and reduction witnesses added | RESOLVED |
| S2 | Exact versions pinned, but no container/Nix/Guix image is supplied | DELIBERATE_LIMITATION |
| S3 | Six certificate-layer corruptions added | RESOLVED |
| S4 | An unaffiliated specialist review has not occurred | DELIBERATE_LIMITATION |
| S5 | A second CAS has not rerun the full sweep; exact Fraction and separate algorithms cover overlapping strata | DELIBERATE_LIMITATION |
| S6 | Literature section expanded to theorem-level comparisons | RESOLVED |
| S7 | Applications separated into proved, producer-side and exploratory grades | RESOLVED |
| S8 | Complete proof appendix was unnecessary after promoting the full proof into the flagship; the claim dependency map is machine-readable | REVIEWER_DISAGREE |

## Summary

Major items resolved: 6/6  
Minor items resolved: 20/20  
Strengthening suggestions resolved: 4/8  
Deliberate limitations: 3  
Reasoned disagreement: 1
