# From inverse support to an exponential-period order benchmark

## Completed scope

This additive, unpublished programme turns the parent inverse-support result
into four research artefacts and stops at the preregistered degree-32
experiment:

1. **EPOB-1**, an exact benchmark for generic differential-equation order,
   inverse support and scalar annihilators;
2. **decomposition-aware fusion reports** attached to exact supplied
   polynomial-composition witnesses;
3. a **Fraction-only replay challenge** using the standard-library rational
   backend and importing no SymPy; and
4. a **sealed prospective quartic-lift experiment** at `m=8`, degree 32.

The broad idea of order-aware creative telescoping is established prior art.
This contribution is a theorem-to-software bridge and benchmark package for
the specific inverse-support invariant. No absolute priority claim is made.

## 1. EPOB-1

EPOB-1 contains ten rational polynomial phases. All ten generic-order and
support answers passed; all nine cases for which an operator is requested also
passed. The order spectrum is

\[
1,2,3,2,3,3,6,3,4,11.
\]

This prevents a system that merely guesses low orders from passing. The most
diagnostic degree-12 comparison is:

| Phase type | Degree | Generic order | Inverse support |
|---|---:|---:|---|
| aligned square | 12 | 3 | `{1,5,9}` |
| misaligned square | 12 | 6 | `{1,3,5,7,9,11}` |
| exceptional Ritt collision `(x^4+x)^3` | 12 | 3 | `{1,7,10}` |
| generic comparison `x^12+x^10+x^3` | 12 | 11 | all non-trace classes |

For the exceptional phase the exact primitive operator is

\[
2(81s+20)I+18s(81s+200)I'
+27s^2(27s+640)I''+6912s^3I'''=0.
\]

On the reference Apple-silicon environment (CPython 3.14.6, SymPy 1.14), the
sum of per-case prediction medians was 5.80 seconds and the corresponding
operator medians totalled 4.37 seconds. These are local descriptive timings,
not cross-system speed claims. Correctness has no timing threshold.

Third-party systems can submit orders, supports and operators to
`tools/verify_epob1_submission.py`. Operators are compared up to a common
nonzero rational-function factor.

## 2. Actual-decomposition fusion

Every supplied chain is first recomposed exactly. Each proper right-factor
suffix is then analysed directly and compared with the parent support-fibre
projection. Four cases and seven validated chains passed:

- the degree-12 exceptional collision in degree orders `3∘4` and `4∘3`;
- the degree-15 Dickson collision in degree orders `3∘5` and `5∘3`;
- the aligned degree-12 square in complete degree chains `2∘3∘2` and
  `3∘2∘2`; and
- the degree-6 rank-creation control `2∘3`.

The Ritt views expose where rank is created. For the exceptional phase the
inner-to-full ranks are `[3,3]` in the `3∘4` view but `[1,3]` in the `4∘3`
view. For the aligned square, creation is `[2,0]` along `2∘3∘2` and `[0,2]`
along `3∘2∘2`. Thus the global rank is Ritt-invariant while its allocation to
levels is presentation-dependent.

These reports validate the supplied chains plus at most one chain returned by
SymPy. They do **not** claim to enumerate the complete decomposition lattice
over the complex numbers.

## 3. Fraction-only replay challenge

The replay challenge recomputed inverse support and exact specialised twisted
rank for twelve cases using `fractions.Fraction` and the earlier verification
library. It explicitly checked that SymPy was not imported. All twelve cases
passed and satisfied

\[
\operatorname{rank}=|\Sigma(P)|.
\]

This is a separate within-programme computational path, not an unaffiliated
reproduction. Its specification and answer key are packaged so that an
external implementation can replace the reference runner.

## 4. Preregistered degree-32 experiment

Before execution, the protocol and runner were sealed at:

- protocol SHA-256
  `9b5bdd27011a1810efe6e77aa041a56772acaf7c220918369e985a338a6f8911`;
- runner SHA-256
  `35a19fc4e521e1dc34b5a5d3be9b9851cab5bcef89cd0f9f2d9fe126716e2cd6`;
- parent commit `ce4e129bed2c1ea5dd7b778488d7bec2b76deb7d`.

The tested family was

\[
P(x)=A(x^8+b),\qquad A(y)=y^4+\beta y^2+\gamma y,\qquad \gamma\ne0.
\]

The candidate inverse-support classes are `{1,9,17,25}`. In three exact
eliminations, classes 9, 17 and 25 were removed in turn. The preregistered
primary prediction was that each resulting ideal, saturated by `gamma != 0`,
would be the unit ideal. The secondary prediction was six distinct confinement
conditions per killed class.

**Result: confirmed.** All three saturated Gröbner bases were `[1]`, and each
case produced six conditions through depth `6d=192`. The single sealed run took
4.69 seconds. Its canonical result digest is
`f72a3468c0acbe193673fe46ba9fb7006bff77aac4d4cb03adf02bea6bf2efae`.

This extends the exact quartic-lift calculation to `m=8` only. It does not
prove the all-degree atlas, the cubic descent, or completeness for all degree-32
polynomials.

## Reproduction

Run the complete gate from the package root:

```bash
python3 run_application_programme_checks.py
```

The gate verifies the published-parent and additive manifests; replays the
order-oracle dependency; exercises positive and mutation controls in ordinary
and optimized Python; regenerates EPOB-1, fusion and Fraction receipts; and
verifies the sealed degree-32 receipt without rerunning the preregistered
experiment.

## Research consequences and next uses

The immediate reusable result is an **order preflight** for creative
telescoping: inverse support supplies the exact generic target order before a
large symbolic operator is constructed. The benchmark makes order collapse,
Ritt-aligned versus misaligned behaviour and rank creation available as common
test cases for computer-algebra systems. The decomposition reports provide a
compact diagnostic for where solution-space blocks fuse. The degree-32 outcome
adds one prospective finite data point to the quartic-lift series while keeping
the uniform theorem obligation open.

