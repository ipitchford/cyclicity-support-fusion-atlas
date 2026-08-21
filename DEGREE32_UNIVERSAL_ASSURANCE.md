# Assurance record: universal degree-32 atlas and Newton descent

Status: **complete internal successor; unrefereed and unpublished**

| Dimension | State | Evidence | Boundary |
|---|---|---|---|
| Prospective identity | passed | protocol, runner and three inherited engine hashes sealed before execution | producer-controlled seal |
| Degree-32 support coverage | passed | all 466 subsets containing class one with size at most three | does not enumerate larger supports |
| Exact elimination | passed | Gröbner bases and radical witnesses over `Q` | trusts SymPy exact arithmetic |
| Condition stability | passed | every `4d` ideal contains all tested conditions through `6d` | truncation safety follows for containment, not equality of infinite ideals |
| Family coverage | passed | 3 full, 406 power-only, 57 union certificates | rank threshold `q<=3` only |
| Mutation detection | passed | forged support, nilpotence witness and boundary changes rejected after rehashing | finite mutations |
| Optimized replay | passed | byte-identical 466-case receipt | same machine and implementation |
| Cubic Newton descent | candidate proof passed internally | arbitrary-`m` coefficient extraction; symbolic control through `m=32` | inherited monodromy dependencies |
| Quartic Newton descent | candidate proof passed internally | arbitrary-`m` coefficient extraction; only `m=3,a=0` survives | inherited monodromy dependencies |
| Separate resultant route | passed within programme | direct resultants through `m=12`; imports no Newton checker | still SymPy and same producer |
| All-degree atlas | candidate repair, not promoted | identified circular lift step has a non-circular replacement | complete specialist audit pending |
| Independent reproduction | not established | none supplied | internal parity is not independence |
| Publication | not undertaken | additive local files only | no commit, tag, DOI or deployment |

## Claim ceiling

The successor may be described as an exhaustive finite computer-assisted
classification of all degree-32 polynomials at the threshold `q(P,dx)<=3`.
It may also be described as supplying a candidate Newton-sum repair of the
identified cubic/quartic obstruction to the all-degree proof.

It may not yet be described as an externally verified or peer-reviewed
all-degree theorem. Promotion requires checking the inherited primitive-group,
finite-pole and rank-preserving-extension arguments together with the new
scaling lemma.

