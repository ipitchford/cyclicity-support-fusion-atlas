import sys, time
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ
from symconstr import reversion_given_p, compose_ring, conds_to_exprs, staircase_dim, reduces_to_zero
from lib import support, pcompose, poly_from_dict, monoxp
from fractions import Fraction

def lift_search(m, K_mult=6, stab_mult=8):
    """A(x^m+b), A=y^4+be*y^2+ga*y. For each killed class c in {m+1,2m+1,3m+1}:
       Groebner of the vanishing conditions; saturated by ga != 0."""
    d = 4*m
    R = ring("be,ga,b", QQ)[0]
    be, ga, b = R.gens
    A_list = [R.zero, ga, be, R.zero, R.one]          # y^4 + be y^2 + ga y
    inner = [R.zero]*(m+1); inner[0] = b; inner[m] = R.one   # x^m + b
    P = compose_ring(A_list, inner, R)
    if not (all(x == R.zero for x in P[d+1:]) and P[d] == R.one and P[d-1] == R.zero):
        raise RuntimeError(f"symbolic composition failed monic-centred check for m={m}")
    P = P[:d+1]
    plist = {j: P[j] for j in range(0, d-1)}
    plist[0] = R.zero                                  # drop constant (target translation)
    K = K_mult*d
    results = {}
    for c in (m+1, 2*m+1, 3*m+1):
        Sallow = frozenset({1, m+1, 2*m+1, 3*m+1}) - {c}
        F, conds = reversion_given_p(d, plist, K, R, S=Sallow)
        # sanity: every collected condition should be in the killed class
        for n, _ in conds:
            if (1-n) % d != c:
                raise RuntimeError(
                    f"unexpected condition class at n={n}: {(1-n)%d} instead of {c}"
                )
        exprs, syms = conds_to_exprs(conds, R)
        sbe, sga, sb = syms
        w = sp.Symbol('w')
        Gsat = sp.groebner(exprs + [w*sga - 1], sbe, sga, sb, w,
                           order='grevlex', domain='QQ')
        empty = (len(Gsat.exprs) == 1 and Gsat.exprs[0] == 1)
        info = dict(nconds=len(conds), empty_saturated=empty)
        if not empty:
            G = sp.groebner(exprs, sbe, sga, sb, order='grevlex', domain='QQ')
            info['dim'] = staircase_dim(G, [sbe, sga, sb])
            info['GB'] = [sp.factor(g) for g in G.exprs]
            # stability: conditions in (K, stab_mult*d] reduce to 0 mod G
            F2, conds2 = reversion_given_p(d, plist, stab_mult*d, R, S=Sallow)
            hi = [(n, g) for n, g in conds2 if n > K]
            exprs2, _ = conds_to_exprs(hi, R)
            info['stable'] = all(reduces_to_zero(e, G) for e in exprs2)
            info['Gsat_gens'] = [sp.factor(g) for g in Gsat.exprs][:6]
        results[c] = info
    return d, results

t0 = time.time()
allok = True
print("=== Battery 4B: quartic lifts A(x^m+b), A = y^4 + be y^2 + ga y, kill one class ===")
for m in (3, 4, 5, 6, 7):
    d, res = lift_search(m)
    for c, info in sorted(res.items()):
        if info['empty_saturated']:
            print(f"m={m} d={d:2d} kill class {c:2d}: EMPTY after ga!=0 saturation "
                  f"({info['nconds']} conditions)  -> only decomposable ga=0 branch")
        else:
            print(f"m={m} d={d:2d} kill class {c:2d}: NONEMPTY dim={info['dim']} "
                  f"stable(to 8d)={info['stable']}  GB={info['GB']}")
            if not (m == 3 and c == 4):
                print("  ^^^ ANOMALY: unexpected non-degenerate solution locus"); allok = False
print(f"[{time.time()-t0:.1f}s]")

# --- positive control for m=3, kill class 4: the (x^4+ax)^3 orbit ---
print("\n--- m=3 positive control: point (be,ga,b)=(-3/8,-1/8,3/4) from A(z)=z(z+1)^3 shifted ---")
m, d = 3, 12
R = ring("be,ga,b", QQ)[0]
be, ga, b = R.gens
A_list = [R.zero, ga, be, R.zero, R.one]
inner = [R.zero, R.zero, R.zero, R.one]; inner[0] = b
P = compose_ring(A_list, inner, R)[:d+1]
plist = {j: P[j] for j in range(0, d-1)}; plist[0] = R.zero
F, conds = reversion_given_p(d, plist, 6*d, R, S=frozenset({1,7,10}))
exprs, syms = conds_to_exprs(conds, R)
pt = {syms[0]: sp.Rational(-3,8), syms[1]: sp.Rational(-1,8), syms[2]: sp.Rational(3,4)}
onvar = all(sp.simplify(e.subs(pt)) == 0 for e in exprs)
print("point lies on kill-4 variety:", onvar)
allok &= onvar
# numeric confirmation via the trusted pipeline: P at that point, support to depth 240
Pnum = pcompose([0, Fraction(-1,8), Fraction(-3,8), 0, 1],
                [Fraction(3,4), 0, 0, 1])
Pnum[0] = 0
S = support(Pnum, 240)
print("support of lift at control point (exact, depth 240):", sorted(S))
allok &= (S == frozenset({1,7,10}))
# orbit relations: sparse quadrinomial with p6 = p9^2/3, p3 = p9^3/27, others 0
p9, p6, p3 = Pnum[9], Pnum[6], Pnum[3]
rel = (p6 == p9**2/3) and (p3 == p9**3/27) and all(Pnum[j] == 0 for j in range(1, 12) if j not in (3, 6, 9))
print(f"orbit relations p6=p9^2/3, p3=p9^3/27, sparsity: {rel}  (p9={p9}, p6={p6}, p3={p3})")
allok &= rel

print("\nBATTERY 4B:", "PASS - lifts collapse exactly as the atlas predicts" if allok else "REVIEW REQUIRED")
sys.exit(0 if allok else 1)
