# Full review: *Inverse-Root Support and Fourier Fusion for Polynomial Exponential Periods*

**Manuscript version:** 0.4.0-candidate, dated 20 August 2026
**Recommendation:** **Major revisions — hold before Evidence Press release**
**Confidence:** **High (0.88)**
**Fatal concerns identified:** **None**

## 1. Executive assessment

This theoretical and computer-assisted mathematics manuscript proposes a single invariant—the non-zero residue support (\Sigma(P)) of a normalised inverse branch at infinity—as the organising principle for three problems concerning polynomial exponential periods. Its strongest result is the claimed universal identity
[
q(P,dx)=|\Sigma(P)|=\dim_{\mathbf C}W_P^{\mathrm{red}},
]
proved through an explicit formal-moment decomposition into rank-one Kummer channels. The associated Fourier block-fusion formula is conceptually strong and appears reusable beyond the immediate low-rank classification. I found no internal contradiction in this universal support/fusion core.

I nevertheless recommend **major revisions and an Evidence Press release hold**. The decisive weaknesses are not the manuscript’s unrefereed candidate status, which I treat as neutral under the stated publishing protocol. They are mismatches between public claims and their present evidence gates: the degree-(\le20) atlas is not included in the fail-closed core runner; its sweep script can exit successfully after an anomaly or missing certificate; the verification receipt targets an earlier bundle rather than the submitted bytes; and several load-bearing proofs are substantially more complete in `source-history/` than in the flagship manuscript. The decomposition-chain and Ritt-move section also contains undefined notation and an unsupported “eleven rank diamonds” claim. These are substantial but bounded repairs. The strongest feature is the universal Fourier-support calculus; the most important required repair is to make the finite-atlas theorem and its assurance record genuinely replayable and claim-aligned.

## 2. Scope and evidence limits

### Manuscript type, field and audience

This is a **theoretical and computational mathematics manuscript** at the intersection of:

* algebraic analysis and twisted de Rham theory;
* polynomial decomposition and monodromy;
* inverse-root relations;
* symbolic computation and computer-assisted classification.

Its natural audience comprises specialists in algebraic analysis, differential modules, polynomial monodromy/decomposition, symbolic computation and zero-dimensional Abelian integrals.

### Materials inspected

I inspected the complete submitted archive, including:

* `MANUSCRIPT.md`, HTML, DOCX and PDF renderings;
* `README.md`, `ASSURANCE.md`, `ATLAS_STATUS.md` and `CLAIMS.json`;
* reproducibility, citation, materials and internal review reports;
* the exact-rank and support code;
* verification batteries and retained logs;
* machine-readable receipts;
* the more detailed proof manuscripts under `source-history/`;
* exploratory ordinary differential equation, zero-cycle and Laurent-polynomial materials.

The external archive SHA-256 is

`69eadb34bae7846c3186c9583a0de4d707351c687f9123aa54c7e771f3506ace`

and matches the supplied sidecar exactly. The internal manifest lists 64 files, all 64 of which match their recorded digests. The archive contains 65 files in total when the manifest itself is counted.

### Review standard

I applied a combined standard of:

1. mathematical validity and self-containment;
2. consistency between theorem statements, proofs, code and receipts;
3. fail-closed reproducibility for computer-assisted claims;
4. accurate claim ceilings and assurance labels;
5. literature positioning and provisional originality;
6. Evidence Press release-contract fidelity.

The absence of prior peer review, journal publication or unaffiliated reproduction is **not itself an adverse finding**. Evidence Press expressly publishes unrefereed work while distinguishing availability, internal replay and external assurance. Its operating model nevertheless requires structured claim ceilings, remaining risks, parent links and assurance targets. ([Evidence Press][1])

### Evidence limits

I did not have raw data because none are relevant to the mathematical claims. I did not independently rerun the entire degree-5-to-20 Gröbner sweep end to end during this review. I instead:

* verified the archive and internal manifest;
* audited the sweep’s mathematical and program logic;
* recalculated the case counts and supplied-log aggregates;
* inspected the exact-rank receipt;
* checked the core test structure and retained logs;
* replayed bounded core and low-degree checks;
* compared the flagship proofs against the fuller source-history proofs.

Thus, **“not independently rerun in full during this review” does not mean “not run by the producer”**. The supplied logs report a complete run, but the current package does not yet make that run a reliable fail-closed release gate.

The literature search was targeted rather than exhaustive. Non-location of an antecedent is not proof of priority.

## 3. Contribution and positioning

### Strongest defensible thesis

The strongest defensible thesis is:

> For a complex polynomial phase (P), the differential rank generated by the fixed amplitude (dx), the number of active congruence channels in the inverse branch at infinity, and the reduced constant span of the inverse roots are equal. Moreover, for every actual polynomial decomposition, the dimensions of sums of root-block spans are computable from explicit finite Fourier matrices.

This thesis is materially stronger and better supported than the proposed all-degree rank-(\le3) coefficient atlas.

### Claim-to-evidence map

| Claim                                         | Principal manuscript location | Evidence supplied                                     | Assessment                                                                    |                                                     |                                                                       |
| --------------------------------------------- | ----------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------- |
| (q(P,dx)=                                     | \Sigma(P)                     | )                                                     | Theorems 3.1–3.2                                                              | Formal-moment proof; exact support/rank comparisons | No contradiction found; proof should be expanded in the flagship text |
| (                                             | \Sigma(P)                     | =\dim W_P^{\mathrm{red}})                             | Theorem 3.2                                                                   | Discrete Fourier transform of inverse branches      | Persuasive and comparatively complete                                 |
| Complete block-sum rank formula               | Theorem 5.1                   | Fourier decomposition; structured decomposition tests | Persuasive; wording should distinguish what is immediate from what is derived |                                                     |                                                                       |
| Canonical coarser factor from equality fusion | Theorem 6.1                   | Monodromy invariance, intermediate fields, Lüroth     | Plausible, but too compressed for a load-bearing universal theorem            |                                                     |                                                                       |
| (q\le3) atlas through degree 20               | Theorem 8.1                   | 1,152 reported exact Gröbner checks                   | Computational logic is credible; release assurance is not yet fail-closed     |                                                     |                                                                       |
| All-degree atlas                              | Conjecture 8.2                | Gapped proof plus finite evidence                     | Correctly labelled conjectural                                                |                                                     |                                                                       |
| Generic period-ODE order                      | §9.1 and claim A1             | Cyclic-module argument plus exploratory examples      | Defensible only with the generic/non-annihilation boundary retained           |                                                     |                                                                       |
| Exact zero-cycle character test               | Abstract and §9.2             | Exploratory script ending `REVIEW`                    | Abstract overstates what has been established                                 |                                                     |                                                                       |

### Originality and significance

**Reviewer inference:** the explicit formal-moment route and the Fourier block-fusion formula appear to be the manuscript’s most original contributions. My targeted search did not find the exact identity (q=|\Sigma|) or the stated all-block Fourier-rank formula in the external literature. That supports a provisional originality judgement, but it does not establish priority.

The significance is potentially substantial. The manuscript turns a differential-module rank problem and a collection of decomposition-specific root-span questions into finite support and Fourier calculations. This is conceptually economical and may make previously difficult examples transparent. However, the broader applications remain mostly prospective, and the all-degree atlas—the result most likely to attract a classification audience—remains conjectural.

The current title and abstract are close to the correct hierarchy but still place too much weight on the word **“certified”** and on the zero-cycle application relative to the assurance actually delivered.

## 4. Major comments

### 1. Major: the finite-atlas theorem is not protected by a fail-closed release gate

**Issue**

Theorem 8.1 and claim F1 are retained as finite computer-assisted theorems, while the subtitle advertises a “certified low-rank atlas”. Yet the executable release gate does not run the exhaustive atlas battery, and the atlas battery itself can return success after conditions that its own output calls anomalous or uncertified.

**Manuscript and package evidence**

* `MANUSCRIPT.md`, Theorem 8.1, states that 1,152 cases have no anomaly or uncertified case and calls the result a finite theorem.
* `CLAIMS.json`, F1, records the basis as “1152 exact Groebner support certificates”.
* `run_core_checks.py`, lines 36–43, runs `verify_atlas.py` and batteries 1–3 only. It does **not** run `battery4a_fast.py` over degrees 5–20.
* `battery4a_fast.py`, lines 192–197, computes `bad = len(r['anomalies'])` and prints a status. It neither:

  * includes `nocert` in `bad`, nor
  * returns a non-zero exit status when `bad>0`.
* `verification/VERIFICATION_REPORT.md`, line 66, says every battery exits non-zero on any failure. That statement is false for battery 4A as submitted.
* `run_core_checks.py`, line 45, looks for `code/exact_rank_receipt.json`, whereas the submitted receipt is under `receipts/`. The digest is therefore silently omitted in a clean run.
* The retained sweep logs aggregate to 45 vacuous/full-family cases, 884 power-only cases and 223 union cases, correctly totalling 1,152. Their recorded sweep times total **674.2 seconds**, whereas `REPRODUCIBILITY.md`, line 50, reports **855.6 seconds**.
* No separate, machine-readable certificate object is retained for each case. The scripts recompute Gröbner bases and report aggregate outcomes.

**Why it matters**

This does not show that Theorem 8.1 is false. It shows that the package can display “CORE CHECKS PASS” without testing the theorem’s exhaustive evidence and that its exhaustive script can return success despite a missing certificate. That is precisely the kind of semantic gap a certificate-backed candidate release should prevent.

Calling every run a “certificate” also risks conflating:

1. an exact computation under a trusted symbolic engine;
2. a retained, independently checkable proof object; and
3. a log asserting that the computation passed.

The current package provides mainly the first and third.

**Required revision or decisive test**

Before retaining Theorem 8.1 as a certified finite theorem:

1. Make battery 4A terminate non-zero whenever either `anomalies` or `nocert` is non-empty.
2. Add every degree batch to the release gate, or provide a deterministic batch runner and a fail-closed aggregator.
3. Verify the internal manifest and all expected receipt hashes in the runner.
4. Move the receipt path to the actual location and compare it against an expected digest rather than merely printing it.
5. Emit a machine-readable inventory with one record per support case, its outcome type, defining ideal or Gröbner basis digest, reduction witness and software/version metadata.
6. Add negative controls that deliberately introduce:

   * an anomaly;
   * a missing certificate;
   * a corrupted receipt;
   * a corrupted manifest entry.
     Each must make the release runner fail.
7. Resolve the 674.2/855.6-second provenance discrepancy.
8. Publish a clean-environment transcript for the current archive hash.

The decisive test is a one-command clean replay in which the unmodified package passes all 1,152 cases and each deliberately corrupted control exits non-zero.

Until then, safer wording is:

> “An exact-arithmetic Gröbner sweep under the supplied SymPy-based engine reports closure of all 1,152 support cases through degree 20.”

### 2. Major: the universal proofs are not sufficiently self-contained in the flagship manuscript

**Issue**

The universal support theorem is likely the paper’s durable contribution, yet several steps needed to audit it are present only in the older source-history manuscript. The public proof is too compressed to support its universal theorem status unaided.

**Manuscript evidence**

In Theorem 3.1, the flagship proof states that pullback followed by the formal moments induces an isomorphism and that the comparison matrix lies in (\operatorname{Mat}_{d-1}(\mathbf C[[s]])). The fuller source-history proof additionally explains:

* why the moment map is well defined on bounded-above Laurent forms;
* why extension to completed pullbacks does not create uncontrolled double Laurent series;
* why the pullbacks have a uniform lower bound on (s)-adic valuation;
* why no negative powers of (s) enter the comparison matrix;
* the precise seed component
  [
  v_r=\sum_n(r+nd)a_{r+nd}\mu_{r,n}s^{-n}e_r;
  ]
* why (v_r\neq0) exactly when (X_r\neq0);
* how the leading exponents (\alpha_r=-n_r-r/d) are distinct;
* why scalar extension from (\mathbf C(s)) to (\mathbf C((s))) preserves cyclic rank.

The flagship compresses these to two sentences at lines 145–157.

Theorem 4.1 similarly concludes that the determinant “cannot acquire a zero inside the sector because the period matrix solves the first-order connection”. That conclusion needs the explicit statement that the period matrix is a fundamental solution on the selected simply connected punctured sector and that its determinant satisfies the corresponding scalar first-order equation.

Theorem 6.1 compresses the canonical-factor argument to one sentence invoking monodromy, intermediate fields, Lüroth’s theorem and total ramification at infinity.

**Why it matters**

These are not expository ornaments. They are the points at which formal completions, infinite Laurent expansions, differential-module rank and polynomial rather than merely rational factorisation enter. A specialist may be able to reconstruct the missing details, but a universal theorem should not require locating an earlier manuscript to do so.

I found no contradiction in the fuller argument. The concern is therefore **insufficiently reported proof**, not demonstrated invalidity.

**Required revision or decisive test**

Restore the fuller lemmas to the flagship manuscript or a formally designated proof appendix:

1. domain and continuity of the moment transform;
2. descent through twisted exact forms;
3. connection compatibility;
4. the unit-triangular comparison matrix, including the absence of negative (s)-powers;
5. the active-seed formula and falling-factorial Vandermonde;
6. invariance of rank under scalar extension;
7. the fundamental-solution argument for the period determinant;
8. the full canonical-factor proof, including:

   * why the equality classes yield a block system on roots;
   * why the intermediate generator has only one pole and hence can be chosen polynomial;
   * why uniqueness is affine.

A decisive test is an independent specialist’s ability to verify T1–T4 from the flagship manuscript and its explicitly linked appendices without consulting undocumented source history.

### 3. Major: the decomposition-chain and Ritt-move section states results that it does not define or demonstrate

**Issue**

Section 6 compresses several non-trivial results past the point of intelligibility. Important notation is undefined, and the assertion of “exactly eleven unordered rank diamonds” is neither listed nor proved.

**Manuscript evidence**

* `MANUSCRIPT.md`, lines 265–269, introduces a “complete decomposition”, suffix degrees (m_i), ranks (r_i) and (P_k) without defining the decomposition (P=P_1\circ\cdots\circ P_k) or the suffixes.
* “Rank-creating level” is not defined.
* The telescoping formula
  [
  q(P)-q(P_k)=\sum_i(r_i-r_{i+1})
  ]
  has an indexing boundary that cannot be checked from the compressed text.
* The assertion that low rank gives “exactly eleven unordered rank diamonds” is not accompanied by the eleven cases, their hypotheses or their derivation.
* The fuller source-history manuscript defines
  [
  Q_i=P_i\circ\cdots\circ P_k,\qquad m_i=\deg Q_i,
  ]
  and contains the omitted table and argument.
* The abstract says that “every sum, intersection, and coincidence” is the rank of an explicit Fourier submatrix. Theorem 5.1 directly gives dimensions of sums. Pairwise intersections follow from dimension identities or the more explicit omitted corollary; arbitrary intersections require a separate statement.
* Theorem 5.1’s useful corollaries—exact heredity, pairwise intersections, equality stabiliser, full fusion and no fusion—are largely omitted from the flagship.

**Why it matters**

The Ritt/decomposition claims are central to the manuscript’s advertised advance beyond the earlier Evidence Press release. They also connect the universal theorem to the coefficient atlas. As submitted, readers cannot determine the precise scope of the “eleven diamonds” claim or reproduce its proof.

**Required revision or decisive test**

Restore:

1. the complete decomposition and suffix notation;
2. the precise monotonicity and telescoping statements with indices;
3. a definition of rank-creating levels;
4. the eleven-diamond table and its derivation;
5. the omitted Fourier-fusion corollaries;
6. a precise distinction among:

   * dimensions of sums directly supplied by Theorem 5.1;
   * pairwise intersections derived from those dimensions;
   * equality of blocks;
   * any asserted higher intersections.

The decisive test is that every noun and symbol in the Ritt paragraph has a prior definition and every enumerative assertion can be traced to a displayed proposition, table or proof.

### 4. Major: the degree-12 proof and finite-atlas statement need exact parameter and family boundaries

**Issue**

The exceptional degree-12 collision is valid, but its short proof omits one residue class. The atlas table also omits parameter restrictions needed for a literal “if and only if” classification.

**Manuscript evidence**

For
[
P=(x^4+x)^3,
]
the deck symmetry confines (\Sigma(P)) to
[
{1,4,7,10}\pmod{12},
]
not directly to ({1,7,10}). Exact heredity modulo four maps the support onto
[
\Sigma(x^4+x)={1,2,3}\pmod4.
]
The residue (4\pmod{12}) maps to (0\pmod4), which is absent from the target support. It is therefore excluded. The flagship’s phrase “the only possible lift” skips this necessary line.

The displayed atlas also needs the full restrictions used by its source theorem, including:

* (D_d(x,a)): (a\neq0), with the appropriate lower-degree boundary;
* (x^{2m}+Ax^m): (m\ge2), (A\neq0);
* (x^{3m}+Ax^{2m}+Bx^m): (m\ge2), with all lower-rank loci stated;
* (x^4+Ax^2+Bx): (B\neq0);
* ((x^4+ax)^3): (a\neq0).

The manuscript mentions some lower-rank loci after the table, but the table itself can still be read as assigning every parameter value to the displayed rank row.

**Why it matters**

The collision is used as the emblematic example refuting naïve block additivity. Its proof should be exact. More importantly, an “if and only if” atlas is only as precise as its normal forms, equivalence convention and parameter exclusions.

**Required revision or decisive test**

* Add the explicit exclusion (4\mapsto0) in the degree-12 proof.
* Define the Dickson-polynomial convention.
* Put all non-zero, degree and lower-rank restrictions directly in the theorem statement.
* State whether duplicate parameterisations and intersections among families are being classified or merely covered.
* Give the exact map from the inverse-series certificate coordinates to each affine normal form.
* Demonstrate degrees two through four rather than calling them merely “direct”.

### 5. Major: the submitted assurance record targets earlier bytes and does not yet satisfy the project’s own lineage standard

**Issue**

The package is internally hash-consistent, but its strongest verification report and receipt target a prior session bundle, with different claim identifiers and file counts.

**Manuscript and package evidence**

* Current archive: SHA-256 `69eadb…0ace`.
* `verification/VERIFICATION_REPORT.md` targets `cyclicity-complete-session-bundle-2026-08-19`, SHA-256 `fddde1…3801`, comprising 77 files.
* That report evaluates claims C1–C10.
* The current `CLAIMS.json` uses T1–T4, F1, C1 and A1.
* No exact mapping states which old claims, proof bytes and test outcomes carry forward unchanged into each current claim.
* `ASSURANCE.md` labels internal replay as “passed with packaging note”, although the degree-20 sweep is absent from the core gate and its standalone sweep is fail-open.
* `MATERIALS_AUDIT.md` exposes an author-local absolute path beginning `/Users/admin/`.
* `REPRODUCIBILITY.md` refers to an original `REPRODUCE_ALL.sh` not included in the current package.
* The verifier’s table assigns subjective probabilities such as 0.99. These are reviewer judgements, not mathematical certificates, and should not be presented as another evidence type.

The currently published Evidence Press predecessor, dated 9 August 2026, describes a conditional support theorem and leaves compositional block fusion as an obstruction. The submitted candidate substantially changes that ceiling and should link explicitly to the predecessor, identifying what is inherited, corrected and superseded. ([Evidence Press][2])

**Why it matters**

A previous-bundle verification can legitimately support unchanged material, but only through an explicit byte and claim bridge. Without it, “the current release passed verification” is stronger than the evidence warrants. This is especially important for a site whose stated model relies on immutable artefacts, structured parent links and non-conflation of internal replay with external assurance. ([Evidence Press][1])

**Required revision or decisive test**

1. Issue a current-target receipt naming the submitted archive hash.
2. Map every current claim to:

   * exact source files and theorem locators;
   * inherited prior claims;
   * current tests and receipts;
   * the applicable assurance ceiling.
3. Record the predecessor as a structured parent and explain:

   * which conditional claim has become unconditional;
   * which block-fusion obstruction has been resolved;
   * which all-degree classification claim has been withdrawn to conjecture.
4. Replace subjective `P(true)` fields with clearly labelled reviewer confidence, or remove them from machine evidence.
5. Remove local absolute paths.
6. include or delete references to missing wrapper scripts.
7. After repair, generate a frozen current-byte verification report and publication transcript.

### 6. Major: the literature and application claims do not yet support the manuscript’s strongest novelty and significance language

**Issue**

The manuscript sensibly says that non-location is not proof of novelty, but its literature comparison is too short for the breadth of its claims. The abstract also turns an exploratory zero-cycle observation into an “exact character test”.

**Manuscript and external evidence**

The twisted de Rham and rapid-decay context is broader than the references currently explain. Sabbah supplies a general twisted de Rham framework; Bloch–Esnault and Hien establish rapid-decay/de Rham pairings; and Hien–Roucairol explicitly study integral representations for exponential Gauss–Manin systems. These works do not appear to state the candidate’s fixed-seed support formula, but they are necessary for locating its analytic contribution accurately. ([arXiv][3])

The root-relation literature requires particular care. Álvarez Sánchez, Bravo Trinidad and Mardešić explicitly provide zero-cycle vanishing examples not expressible as sums of composition terms. That supports the manuscript’s caveat that equality fusion of whole block spans is narrower than an arbitrary inverse-root relation, but it also means that §9.2 cannot be framed as a complete exact test without a theorem comparing the two settings. ([arXiv][4])

The polynomial-monodromy search should include the recent 2026 work of Behajaina, König and Neftin on monodromy groups of compositions of two indecomposable polynomials. It does not automatically prove or refute the atlas, but it is directly relevant to the manuscript’s proposed all-degree monodromy route and was revised shortly before this review. ([arXiv][5])

The manuscript cites Girstmair’s 1999 root-relations paper without its 2003 corrigendum. ([EuDML][6])

In the application material:

* §9.2 explicitly says that no proof manuscript closes the zero-cycle criterion and that the script prints `REVIEW` while returning success.
* Nevertheless, the abstract advertises “an exact character test for zero-cycle identities”.
* §9.1 correctly retains a generic/non-annihilation condition, but its demonstration script is expressly fail-open.

**Why it matters**

The literature gap limits both novelty calibration and the interpretation of the application claims. The abstract is also the most likely text to be repeated by Evidence Press. It must not promote an exploratory calculation to a proved application.

**Required revision or decisive test**

* Expand §10 into theorem-level comparisons rather than field-level summaries.
* Add the Girstmair corrigendum and discuss whether it affects any invoked result.
* Add Hien–Roucairol and the recent composition-length-two monodromy work.
* State which sources were examined in full text and which only at abstract/metadata level.
* Replace “exact character test for zero-cycle identities” with:

  > “a Fourier-channel formulation suggesting exact tests for selected zero-cycle identities”
  > unless a general theorem and proof are added.
* Separate the proved generic ODE-order corollary from the exploratory operator demonstrations.
* Develop the zero-cycle and Laurent applications as separate outputs until their dependencies and fail-closed tests are complete.

## 5. Rigour, results and inference

### 5.1 Formal-moment decomposition and cyclic rank

The fuller proof architecture is coherent:

1. The twisted de Rham quotient has rank (d-1).
2. Pullback along (x=\xi(t)) turns the twisted differential into
   [
   \partial_t+sdt^{d-1}.
   ]
3. The recursion
   [
   \mu_{r,n+1}=-\frac{r+nd}{d}\mu_{r,n}
   ]
   gives formal integration by parts in each residue channel.
4. The comparison matrix on (1,x,\ldots,x^{d-2}) has unit-triangular constant term.
5. The seed is active precisely in the support channels.
6. Derivative columns have a non-zero falling-factorial Vandermonde leading term.

I found no invalid cancellation or vanishing factor in this chain. In particular, (r+nd\neq0) for (1\le r\le d-1), so every moment coefficient used in the recurrence is non-zero.

The principal risk is formal exposition: the completed pullback and (s)-adic boundedness must be reported, not merely presumed.

### 5.2 Root-span equality

The equality with the reduced inverse-root span is the cleanest proof in the manuscript. The inverse branches
[
x_j=\sum_r\zeta_d^{jr}X_r
]
are related to the residue channels by an invertible discrete Fourier transform. The non-zero (X_r) are constant-linearly independent because their Laurent supports occupy disjoint congruence classes. Removing the trace channel gives the stated dimension.

This argument appears sound as written, subject to defining carefully whether (W_P^{\mathrm{red}}) is taken in a local splitting field near infinity or in the corresponding algebraic-function field. The dimension is unchanged, but the ambient field should be explicit.

### 5.3 Fourier fusion

For a decomposition (P=R\circ Q), the block roots decompose into vectors
[
Y_{a,c}=\sum_{\ell\in L_c}\zeta_n^{a\ell}X_{c+m\ell}.
]
Because different (c)-summands have disjoint Laurent supports, their dimensions add, and the span within each summand is the row rank of the displayed Fourier submatrix.

I find this calculation convincing. It establishes dimensions of all block sums directly. Equality and pairwise intersection formulae are valid corollaries once their derivations are restored. The manuscript should avoid implying that every conceivable lattice operation on arbitrary sums is itself literally a single Fourier-submatrix rank unless that extension is stated and proved.

### 5.4 Canonical fusion factor

The proposed route is standard in outline:

* equality of block spans is monodromy invariant;
* invariant coarsenings correspond to intermediate fields;
* Lüroth makes the intermediate field rational;
* polynomial total ramification at infinity permits a polynomial generator;
* the cyclic inertia indexing identifies the degree.

No contradiction emerged. However, this is exactly where a one-line appeal to several theories can hide a gap. The theorem should be considered **plausibly proved but insufficiently reported** until the intermediate-field and polynomiality steps are written out.

### 5.5 Degree-20 atlas calculations

I recalculated the number of support cases. For each (d), supports of size at most three containing the normalised class (1) number
[
1+(d-2)+\binom{d-2}{2}.
]
Therefore
[
\sum_{d=5}^{20}
\left[
1+(d-2)+\binom{d-2}{2}
\right]
=1152.
]

The supplied result categories reconcile:
[
45+884+223=1152.
]

The reported certificate logic is mathematically meaningful:

* **vacuous/full-family:** the constrained variety is the entire permitted parameter space and is matched to a saturating family;
* **power-only:** powers of the non-power parameters reduce to zero modulo the Gröbner basis;
* **union:** a power of the product of defining equations for the predicted components reduces to zero.

A genuine support-(\le3) polynomial must satisfy the truncated confinement equations. Thus, when the truncated variety is shown to lie in a union of families whose complete support is proved independently, the argument can establish finite exhaustiveness. Emptiness conclusions are robust to adding further equations.

Residual trust remains in:

* the inverse-series construction;
* the translation from support equations to coefficient families;
* the code constructing each ideal;
* SymPy’s exact rational Gröbner arithmetic;
* the claim that the displayed families have the asserted complete support.

These are acceptable trust assumptions for a candidate computer-assisted theorem only when precisely recorded and protected by a fail-closed gate.

### 5.6 Consistency checks

| Check                                |                                             Result | Interpretation                                         |
| ------------------------------------ | -------------------------------------------------: | ------------------------------------------------------ |
| External ZIP SHA-256 against sidecar |                                              Match | Submitted archive identity is secure                   |
| Internal manifest                    |                                  64/64 files match | No internal file corruption detected                   |
| Atlas support-case count             |                                              1,152 | Agrees with theorem and logs                           |
| Atlas result categories              |                             45 + 884 + 223 = 1,152 | Internally reconciled                                  |
| Retained sweep runtimes              |                                      674.2 seconds | Conflicts with 855.6 seconds in reproducibility report |
| Support/rank comparison log          |            278 comparisons, zero reported mismatch | Strong producer-side consistency evidence              |
| Heredity log                         |  200 pairs under two primes, zero reported failure | Supports implementation consistency                    |
| Degree-12 collision                  |                                         ({1,7,10}) | Correct after explicitly excluding class (4)           |
| All-degree atlas                     | First uncovered quartic lift reported at degree 32 | Correctly kept conjectural                             |

The tests reduce the risk of a simple implementation error. They do not replace the missing current-byte, fail-closed release chain.

### 5.7 Selective reporting and analytic flexibility

I found no basis to allege selective reporting, p-hacking or post-hoc hypothesis construction. The package preserves abandoned claims and the identified circular proof step, which is a material strength.

There is nonetheless a **risk indicator** of design-to-family confirmation in the atlas: certificate varieties are tested against predicted components derived from the proposed classification. The risk is reduced by exact Gröbner containment, mutation controls and family support proofs. It would be reduced further by:

* retaining per-case proof objects;
* adding family-blind decomposition of selected varieties;
* having an unaffiliated verifier reconstruct the case generator;
* using a second computer algebra system on a stratified sample.

## 6. External literature check

### Search record

**Review date:** 20 August 2026.

**Search systems and repositories:** live indexed web search, arXiv, publisher/DOI pages, EuDML/Centre Mersenne records, Evidence Press and official REF pages.

**Representative search strings:**

* `"inverse-root support" polynomial`
* `"cyclic rank" "inverse roots" polynomial`
* `"q(P,dx)" polynomial exponential period`
* `polynomial exponential periods inverse branches twisted de Rham`
* `polynomial monodromy inverse branches linear relations composition Ritt`
* exact searches for cited titles, DOIs, corrigenda and recent monodromy work.

**Inclusion logic:** exact or near-exact theorem antecedents; foundational twisted de Rham and rapid-decay sources; original polynomial decomposition and monodromy sources; root-relation and zero-cycle papers; recent work potentially affecting the all-degree classification. Older landmark results were retained where decisive.

**Coverage limitation:** this was not an exhaustive MathSciNet/Zentralblatt citation-network review. Some assessments used publisher abstracts or bibliographic records; arXiv sources and open journal versions were examined more fully.

### Pivotal comparisons

**Twisted de Rham and rapid decay.** Sabbah studies twisted de Rham complexes in broad algebraic settings. Bloch and Esnault define rapid-decay-style homology for irregular connections on curves and establish a perfect integration pairing. Hien generalises rapid-decay/de Rham duality, while Hien and Roucairol obtain integral representations for exponential Gauss–Manin systems. These sources establish the analytic ecosystem, but my search did not locate the manuscript’s explicit one-variable fixed-seed identity or its formal-moment channel formula. ([arXiv][3])

**Polynomial decomposition and monodromy.** Ritt gives the classical decomposition framework; Zieve and Müller describe the space of complete polynomial decompositions more effectively; Burda and Khovanskii use primitive polynomial monodromy in a bounded-radical classification. The 2026 Behajaina–König–Neftin work addresses monodromy groups of compositions of two indecomposable polynomials and is especially relevant to any proposed group-theoretic completion of the all-degree atlas. None of these sources, on the evidence reviewed, states the Fourier block-span formula. ([OA Monitor Ireland][7])

**Inverse-root relations.** Girstmair is a direct antecedent for constant linear relations among polynomial roots, and the corrigendum must be acknowledged. The candidate should state exactly which parts of this theory it uses and whether the corrigendum affects them. ([EuDML][6])

**Zero-dimensional Abelian integrals.** Álvarez Sánchez, Bravo Trinidad and Mardešić formulate and solve important zero-cycle vanishing problems under specified hypotheses and explicitly note non-composition examples. Pakovich and Muzychuk solve the polynomial moment problem in a related composition-theoretic setting. The candidate’s Fourier support may offer a useful new language here, but the current examples do not yet constitute a general solution or exact complete criterion. ([arXiv][4])

### Implications for originality, significance and credibility

* **Originality:** provisionally favourable. No exact antecedent for (q=|\Sigma|) or the complete Fourier block-sum formula was located.
* **Significance:** potentially high within a specialist domain, particularly if the calculus proves useful in decomposition, differential-equation and zero-cycle problems.
* **Credibility:** strengthened by alignment with established twisted de Rham, rapid-decay and monodromy frameworks, but weakened by insufficient theorem-level comparison and omission of a recent directly relevant monodromy paper and a corrigendum.
* **Unresolved gap:** a broader D-module and computational-algebra priority audit could still reveal equivalent formulations under different terminology.

## 7. Minor comments

1. In the abstract’s definition of (\mathcal H_P),
   `\mathbf C(s)[x],dx`
   appears to be a typesetting error for (\mathbf C(s)[x],dx).

2. Define the shorthand (q(P)) before switching from (q(P,dx)) in Sections 6–8.

3. Define the normalisation and parameter convention for the Dickson polynomial (D_d(x,a)).

4. State explicitly whether all support sets are subsets of (\mathbf Z/d\mathbf Z) and whether representatives are always taken in ({1,\ldots,d-1}).

5. Replace the sentence that the period determinant “cannot acquire a zero” with the corresponding fundamental-matrix or scalar determinant equation.

6. In the degree-12 example, write the four deck-compatible classes ({1,4,7,10}) before using heredity to exclude (4).

7. Restore the equality-stabiliser (H_m(P)) definition before using it in Theorem 6.1.

8. Include the eleven rank diamonds rather than referring to an absent classification.

9. Explain “rank-preserving extension” and “rank-creating level” on first use.

10. Add an exact normal-form/equivalence statement to Theorem 8.1: source affine changes, target affine changes and any parameter identifications should be explicit.

11. Replace “1,152 exact certificates” with a more exact description unless individual proof objects are retained.

12. The Bostan–Dumas DOI is mistyped as `10.4169/000298910X515775`; the article record gives `10.4169/000298910X515785`. ([JSTOR][8])

13. Add Girstmair’s one-page 2003 corrigendum, DOI `10.4064/aa110-2-10`. ([EuDML][6])

14. Check the author order of the Müller/Zieve reference against the cited version.

15. Separate “algorithmically separate within the programme” from “independent” throughout. The current manuscript usually does this correctly; the report title still says “Independent verification report”.

16. The PDF is generally clean, but an awkward page break separates prose from the displayed ((x^4+ax)^3) expression, and the final reference page is largely blank. Page numbers and PDF bookmarks would improve navigation.

17. Synchronise the Chinese abstract after revising the English claims. It should not retain stronger wording than the final English abstract.

18. Remove the local `/Users/admin/...` path from `MATERIALS_AUDIT.md`.

19. Record one authoritative environment specification. The package currently mentions both Python 3.12.3 and 3.14.6.

20. Avoid wording such as “one lemma short” in the conclusion unless the missing descent lemma is known to be sufficient without further classification changes. “One presently identified proof obligation” is safer.

## 8. Prioritised revision plan

### Must fix before the claims are publishable

1. Make the degree-20 atlas sweep fail closed and include it in the release gate.
2. Produce a current-byte receipt and claim mapping for archive hash `69eadb…0ace`.
3. Restore the load-bearing formal-moment, cyclicity and canonical-factor proof details.
4. Define the decomposition-chain notation and include the eleven Ritt rank diamonds or remove that claim.
5. Correct the degree-12 lift argument and state every atlas parameter boundary.
6. Reconcile the atlas runtime and receipt-path inconsistencies.
7. Correct the abstract’s zero-cycle overclaim.
8. Add structured lineage to the two preceding Evidence Press cyclicity releases, specifying inherited and superseded claims.
9. Add the Girstmair corrigendum, the recent composition-length-two monodromy work and the missing exponential Gauss–Manin comparison.
10. Ensure that every retained release claim is represented in the fail-closed runner or explicitly labelled non-gated.

### Should fix to strengthen the paper

1. Retain per-case machine-readable atlas certificate records.
2. Supply a container, Nix/Guix environment or otherwise fully locked environment.
3. Add corruption and mutation tests for every certificate layer.
4. Have an unaffiliated specialist review the formal completion and canonical-factor arguments.
5. Cross-check a stratified atlas sample in a second computer algebra system.
6. Expand the theorem-by-theorem literature comparison.
7. Separate the applications into proved corollaries, producer-side demonstrations and speculative directions.
8. Add a proof appendix with complete notation and a claim-to-lemma dependency graph.

### Could improve presentation or future work

1. Add PDF bookmarks, page numbers and improved equation-page breaking.
2. Formalise the support theorem or certificate checker in a proof assistant.
3. Develop the zero-cycle examples into a separate theorem paper.
4. Develop the Laurent-polynomial calculations as a separate package after repairing their control dimensions.
5. Provide a small interactive support/fusion calculator for reproducible examples.

## 9. Editorial recommendation

**Recommendation: Major revisions — hold before Evidence Press release.**

**Confidence:** High, 0.88.

The recommendation is not based on the work being unrefereed or unpublished. Those are normal and accurately disclosed features of an Evidence Press candidate. The hold follows from four bounded release defects:

1. the finite-atlas theorem is not in the fail-closed core gate;
2. the exhaustive sweep can exit successfully after an anomaly or missing certificate;
3. the strongest verification targets prior bytes and prior claim identifiers;
4. universal and Ritt-related proofs are not self-contained in the flagship manuscript.

I found no fatal mathematical defect in the universal support/root-span identity or the Fourier fusion formula. The all-degree classification is properly demoted to a conjecture, so its known circular step is not a reason to reject the structural paper.

The decision would change to **release as an unrefereed theorem candidate** once the fail-closed atlas gate, current-byte receipt, proof restorations, lineage record and claim-language repairs are complete. If those repairs are not made, the release should demote F1 from “certified theorem” to a reported producer-side exact computation and remove “certified low-rank atlas” from the subtitle.

## 10. Provisional REF calibration

### Framework used

The most relevant unit is **REF Unit of Assessment 10: Mathematical Sciences**, under Main Panel B. REF 2029 retains the 34-unit structure, but, as of this review date, detailed panel criteria and the quality-rating implementation were still being developed; current official guidance says that the panel criteria will set out the rating system. I therefore use the established REF 2021 generic definitions together with the supplied 12-point high/medium/low matrix. ([REF 2029][9])

| Dimension                  | Indicative grade | 12-point calibration | Rationale                                                                                                                                                                                                                             | Confidence |
| -------------------------- | ---------------- | -------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **Originality**            | **3*** Medium    |             **8/12** | The formal-moment support formula and Fourier fusion calculus appear conceptually distinct; no exact antecedent was found. Priority search remains non-exhaustive, and directly relevant recent monodromy work is not yet integrated. | Medium–low |
| **Significance**           | **3*** Low       |             **7/12** | The universal reduction could become an important specialist tool. Present applications are preliminary, the all-degree atlas is open, and external uptake has not yet occurred. Candidate status itself is not penalised.            | Medium–low |
| **Rigour**                 | **2*** High      |             **6/12** | The detailed universal proof appears credible and the finite computations are substantial, but the submitted flagship omits load-bearing details and the finite theorem’s release gate is fail-open and not current-byte aligned.     | Medium     |
| **Overall output quality** | **2*** High      |             **6/12** | Holistically, the work is internationally recognisable and contains a plausible 3* conceptual core, but the manuscript and assurance package as submitted do not yet reach a consistently robust 3* standard.                         | Medium     |

The overall rating is **holistic, not an arithmetic average**. Completion of the mandatory revisions—particularly proof self-containment and a fail-closed current-byte atlas certificate chain—would plausibly move the output to **3* Low or 3* Medium**. A 4* judgement would require much stronger priority confirmation, mature external significance and exceptionally secure proof/certificate presentation.

This calibration is **indicative only and not an official REF panel decision**.

## 11. References

### Twisted de Rham theory, irregular connections and exponential periods

Bloch, S., & Esnault, H. (2004). Homology for irregular connections. *Journal de Théorie des Nombres de Bordeaux, 16*(2), 357–371. [https://doi.org/10.5802/jtnb.450](https://doi.org/10.5802/jtnb.450) ([jtnb.centre-mersenne.org][10])

Hien, M. (2009). Periods for flat algebraic connections. *Inventiones Mathematicae, 178*, 1–22. [https://doi.org/10.1007/s00222-009-0185-7](https://doi.org/10.1007/s00222-009-0185-7) ([Springer][11])

Hien, M., & Roucairol, C. (2008). Integral representations for solutions of exponential Gauss–Manin systems. *Bulletin de la Société Mathématique de France, 136*(4), 505–532. [https://doi.org/10.24033/bsmf.2564](https://doi.org/10.24033/bsmf.2564) ([arXiv][12])

Sabbah, C. (1999). On a twisted de Rham complex. *Tohoku Mathematical Journal, 51*(1), 125–140. [https://doi.org/10.2748/tmj/1178224856](https://doi.org/10.2748/tmj/1178224856) ([Project Euclid][13])

### Polynomial decomposition, monodromy and root relations

Behajaina, A., König, J., & Neftin, D. (2026). *Monodromy groups of polynomials of composition length 2* [Preprint]. arXiv. [https://arxiv.org/abs/2603.27609](https://arxiv.org/abs/2603.27609) ([arXiv][14])

Burda, Y., & Khovanskii, A. (2012). *Polynomials invertible in (k)-radicals* [Preprint]. arXiv. [https://arxiv.org/abs/1209.5137](https://arxiv.org/abs/1209.5137) ([arXiv][15])

Girstmair, K. (1999). Linear relations between roots of polynomials. *Acta Arithmetica, 89*(1), 53–96. [https://doi.org/10.4064/aa-89-1-53-96](https://doi.org/10.4064/aa-89-1-53-96)

Girstmair, K. (2003). Corrigendum to the paper “Linear relations between roots of polynomials”. *Acta Arithmetica, 110*(2), 203. [https://doi.org/10.4064/aa110-2-10](https://doi.org/10.4064/aa110-2-10) ([EuDML][6])

Ritt, J. F. (1922). Prime and composite polynomials. *Transactions of the American Mathematical Society, 23*, 51–66. [https://doi.org/10.1090/S0002-9947-1922-1501189-9](https://doi.org/10.1090/S0002-9947-1922-1501189-9) ([OA Monitor Ireland][7])

Zieve, M. E., & Müller, P. (2008). *On Ritt’s polynomial decomposition theorems* [Preprint]. arXiv. [https://arxiv.org/abs/0807.3578](https://arxiv.org/abs/0807.3578) ([arXiv][16])

### Zero-dimensional cycles and moment problems

Álvarez Sánchez, A., Bravo Trinidad, J. L., & Mardešić, P. (2013). Vanishing Abelian integrals on zero-dimensional cycles. *Proceedings of the London Mathematical Society, 107*(6), 1302–1330. [https://doi.org/10.1112/plms/pdt012](https://doi.org/10.1112/plms/pdt012) ([London Mathematical Society][17])

Álvarez Sánchez, A., Bravo Trinidad, J. L., & Mardešić, P. (2012). *Inductive solution of the tangential center problem on zero-cycles* [Preprint]. arXiv. [https://arxiv.org/abs/1202.5896](https://arxiv.org/abs/1202.5896) ([arXiv][18])

Pakovich, F., & Muzychuk, M. (2009). Solution of the polynomial moment problem. *Proceedings of the London Mathematical Society, 99*(3), 633–657. [https://doi.org/10.1112/plms/pdp010](https://doi.org/10.1112/plms/pdp010) ([arXiv][19])

### Publication and assessment framework

Evidence Press. (2026). *Evidence Press operating model*. [https://evidencepress.org/operating-model/](https://evidencepress.org/operating-model/) ([Evidence Press][1])

Evidence Press. (2026, August 9). *Fixed-seed cyclic rank from inverse roots*. [https://evidencepress.org/releases/cyclicity-root-span-low-rank/](https://evidencepress.org/releases/cyclicity-root-span-low-rank/) ([Evidence Press][2])

Research Excellence Framework. (2022). *Guidance on REF 2021 results*. [https://2021.ref.ac.uk/guidance-on-results/guidance-on-ref-2021-results/](https://2021.ref.ac.uk/guidance-on-results/guidance-on-ref-2021-results/) ([REF 2021][20])

Research Excellence Framework. (2025–2026). *REF 2029 units of assessment and panel guidance*. [https://2029.ref.ac.uk/panels/units-of-assessment/](https://2029.ref.ac.uk/panels/units-of-assessment/) ([REF 2029][9])

**[END]**

[1]: https://evidencepress.org/operating-model/ "https://evidencepress.org/operating-model/"
[2]: https://evidencepress.org/releases/cyclicity-root-span-low-rank/ "https://evidencepress.org/releases/cyclicity-root-span-low-rank/"
[3]: https://arxiv.org/abs/math/9805087 "https://arxiv.org/abs/math/9805087"
[4]: https://arxiv.org/abs/1101.1777 "https://arxiv.org/abs/1101.1777"
[5]: https://arxiv.org/abs/2603.27609 "https://arxiv.org/abs/2603.27609"
[6]: https://eudml.org/doc/278654 "https://eudml.org/doc/278654"
[7]: https://oamonitor.ireland.openaire.eu/national/search/publication?pid=10.1090%2Fs0002-9947-1922-1501189-9&utm_source=chatgpt.com "Prime and composite polynomials"
[8]: https://www.jstor.org/stable/10.4169/000298910x515785 "https://www.jstor.org/stable/10.4169/000298910x515785"
[9]: https://2029.ref.ac.uk/panels/units-of-assessment/ "https://2029.ref.ac.uk/panels/units-of-assessment/"
[10]: https://jtnb.centre-mersenne.org/item/JTNB_2004__16_2_357_0/?utm_source=chatgpt.com "Homology for irregular connections"
[11]: https://link.springer.com/article/10.1007/s00222-009-0185-7 "https://link.springer.com/article/10.1007/s00222-009-0185-7"
[12]: https://arxiv.org/abs/0704.1739 "https://arxiv.org/abs/0704.1739"
[13]: https://projecteuclid.org/journals/tohoku-mathematical-journal/volume-51/issue-1/On-a-twisted-de-Rham-complex/10.2748/tmj/1178224856.full "https://projecteuclid.org/journals/tohoku-mathematical-journal/volume-51/issue-1/On-a-twisted-de-Rham-complex/10.2748/tmj/1178224856.full"
[14]: https://arxiv.org/html/2603.27609v2 "https://arxiv.org/html/2603.27609v2"
[15]: https://arxiv.org/abs/1209.5137 "https://arxiv.org/abs/1209.5137"
[16]: https://arxiv.org/abs/0807.3578 "https://arxiv.org/abs/0807.3578"
[17]: https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/plms/pdt012?utm_source=chatgpt.com "Vanishing Abelian integrals on zeroâ•'dimensional cycles - London ..."
[18]: https://arxiv.org/abs/1202.5896 "https://arxiv.org/abs/1202.5896"
[19]: https://arxiv.org/abs/0710.4085 "https://arxiv.org/abs/0710.4085"
[20]: https://2021.ref.ac.uk/guidance-on-results/guidance-on-ref-2021-results/index.html "https://2021.ref.ac.uk/guidance-on-results/guidance-on-ref-2021-results/index.html"
