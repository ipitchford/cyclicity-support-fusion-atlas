import random, sys
from fractions import Fraction
from lib import *

rng = random.Random(20260819)

def check(name, coeffs, expected=None, N_mult=12, exact=False):
    p = None if exact else P61
    a = centre(coeffs, p)
    d = pdeg(a)
    N = N_mult*d
    S1 = support(coeffs, N, p)
    if not exact:
        S2 = support(coeffs, N, P2)
        if S1 != S2:
            print(f"FAIL  {name}: prime disagreement {sorted(S1)} != {sorted(S2)}")
            return False
    q1 = q_deRham(coeffs, p, rng=rng)
    ok = (q1 == len(S1)) and (expected is None or q1 == expected)
    tag = "PASS" if ok else "FAIL"
    print(f"{tag}  {name:42s} d={d:3d}  |Sigma|={len(S1)}  q_dR={q1}  Sigma={sorted(S1)}"
          + (f"  expected={expected}" if expected is not None else ""))
    return ok

allok = True
print("=== Section 14 controls (exact Fractions, independent implementations) ===")
X = [0,1]
ctrl = [
 ("x^9", monoxp(9), 1),
 ("D_5(x,1)=x^5-5x^3+5x", dickson(5,1), 2),
 ("(x^4+1)^2", pcompose(monoxp(2), poly_from_dict({4:1,0:1})), 2),
 ("x^9+2x^6+3x^3", poly_from_dict({9:1,6:2,3:3}), 3),
 ("x^6-6x^4+9x^2  (D6 lower locus)", poly_from_dict({6:1,4:-6,2:9}), 2),
 ("x^4+x^2+x", poly_from_dict({4:1,2:1,1:1}), 3),
 ("(x^4+x)^3", pcompose(monoxp(3), poly_from_dict({4:1,1:1})), 3),
 ("(x^6+x^2)^2", pcompose(monoxp(2), poly_from_dict({6:1,2:1})), 3),
 ("(x^9+x^3)^2", pcompose(monoxp(2), poly_from_dict({9:1,3:1})), 3),
 ("(x^6+x^4+x^2)^2  mutation", pcompose(monoxp(2), poly_from_dict({6:1,4:1,2:1})), 6),
 ("x^8+x^4+x^2", poly_from_dict({8:1,4:1,2:1}), 4),
 ("(x^8+x^2)^3  mutation", pcompose(monoxp(3), poly_from_dict({8:1,2:1})), 4),
]
for name, c, e in ctrl:
    allok &= check(name, c, e, N_mult=10, exact=True)

print("\n=== Atlas families, multiple parameters (mod-p x2 primes, deep order) ===")
for aa in [1, 2, 7, -3]:
    allok &= check(f"D_7(x,{aa})", dickson(7, aa), 2)
    allok &= check(f"D_9(x,{aa})", dickson(9, aa), 2)
for (m, A) in [(2,3),(3,-2),(5,1)]:
    allok &= check(f"x^{2*m}+{A}x^{m}", poly_from_dict({2*m:1, m:A}), 2)
for (m, A, B) in [(2,1,1),(2,3,-5),(3,2,3),(4,-1,2),(5,1,1)]:
    allok &= check(f"x^{3*m}+{A}x^{2*m}+{B}x^{m}", poly_from_dict({3*m:1, 2*m:A, m:B}), 3)
allok &= check("x^6+2x^4+x^2  (m=2 B=A^2/4 sublocus)", poly_from_dict({6:1,4:2,2:1}), 2)
for (A,B) in [(0,1),(2,3),(-1,5)]:
    allok &= check(f"x^4+{A}x^2+{B}x", poly_from_dict({4:1,2:A,1:B}), 3)
for aa in [1,2,-3,5]:
    allok &= check(f"(x^4+{aa}x)^3", pcompose(monoxp(3), poly_from_dict({4:1,1:aa})), 3)
allok &= check("(x^9+2x^3)^2  aligned square m=3 b=2", pcompose(monoxp(2), poly_from_dict({9:1,3:2})), 3)
allok &= check("(x^12+3x^4)^2  aligned square m=4", pcompose(monoxp(2), poly_from_dict({12:1,4:3})), 3)

print("\n=== Random sweep: q_dR vs |Sigma|, degrees 3..10 ===")
mismatch = 0; total = 0
for d in range(3, 11):
    for trial in range(30):
        # mix of dense and sparse random integer polys
        c = [0]*(d+1); c[d] = 1
        nz = rng.randrange(1, d)  # number of nonzero lower coeffs
        idxs = rng.sample(range(0, d-1), min(nz, d-1))
        for i in idxs:
            c[i] = rng.randrange(-9, 10) or 1
        total += 1
        S = support(c, 12*d, P61)
        S2 = support(c, 12*d, P2)
        if S != S2:
            print("PRIME MISMATCH", c); mismatch += 1; continue
        q1 = q_deRham(c, P61, rng=rng)
        if q1 != len(S):
            mismatch += 1
            print(f"MISMATCH d={d} coeffs={c}  |Sigma|={len(S)} q={q1} Sigma={sorted(S)}")
print(f"random sweep: {total} polynomials, {mismatch} mismatches")
allok &= (mismatch == 0)

print("\nBATTERY 1:", "ALL PASS" if allok else "FAILURES PRESENT")
sys.exit(0 if allok else 1)
