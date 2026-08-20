import sys, time, itertools
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ
from symconstr import reversion_given_p, compose_ring, conds_to_exprs
from lib import (support, q_deRham, pcompose, poly_from_dict, monoxp, dickson,
                 padd, P61, P2, centre, pdeg)
from fractions import Fraction
import random
rng = random.Random(4242)

def ground(R, q):
    return R.one*sp.nsimplify(q) if False else R.ground_new(QQ(q))

def extension_search(name, Qcoeffs, n, expected):
    """Q fixed integer-coeff centred; R = y^n + r_{n-1}y^{n-1}+...+r_1 y symbolic.
       Rank preservation q(R.Q)=q(Q) <=> exactly one surviving class above each c in Sigma(Q).
       Returns dict choice->solutions; prints comparison with expected description."""
    m = pdeg(Qcoeffs)
    d = n*m
    SigQ = support(Qcoeffs, 12*m, P61)
    if support(Qcoeffs, 12*m, P2) != SigQ:
        raise RuntimeError(f"prime disagreement for {name}")
    varnames = ",".join(f"r{i}" for i in range(1, n))
    R = ring(varnames, QQ)[0]
    rs = {i+1: g for i, g in enumerate(R.gens)}
    router = [R.zero]*(n+1); router[n] = R.one
    for i in range(1, n): router[i] = rs[i]
    qlist = [R.ground_new(QQ(int(c))) for c in Qcoeffs]
    P = compose_ring(router, qlist, R)[:d+1]
    if not (P[d] == R.one and P[d-1] == R.zero):
        raise RuntimeError(f"symbolic composition failed monic-centred check for {name}")
    plist = {j: P[j] for j in range(0, d-1)}; plist[0] = R.zero
    K = 6*d
    others = sorted(c for c in SigQ if c != 1 % m)
    found = []
    syms = [sp.Symbol(f"r{i}") for i in range(1, n)]
    for choice in itertools.product(range(n), repeat=len(others)):
        keep = {1} | {(c + m*l) % d for c, l in zip(others, choice)}
        Sallow = frozenset(keep)
        F, conds = reversion_given_p(d, plist, K, R, S=Sallow)
        if not conds:
            found.append((Sallow, "NO CONDITIONS - full r-space (verify numerically!)"))
            continue
        exprs, _ = conds_to_exprs(conds, R)
        if n == 2:
            g = sp.factor(sp.gcd(exprs))
            sols = sp.solve(g, syms[0]) if g != 1 else []
            if g == 0: found.append((Sallow, "ALL r1"))
            elif sols: found.append((Sallow, sorted(sols)))
        else:
            G = sp.groebner(exprs, *syms, order='lex', domain='QQ')
            if not (len(G.exprs) == 1 and G.exprs[0] == 1):
                sols = sp.solve(list(G.exprs), syms, dict=True)
                found.append((Sallow, sols if sols else f"nonzero-dim GB {list(G.exprs)}"))
    print(f"--- {name}: Sigma(Q)={sorted(SigQ)}, n={n}, d={d} ---")
    if not found:
        print("    preservation locus: EMPTY (no outer R of this degree preserves rank)")
    for S, sol in found:
        print(f"    surviving classes {sorted(S)}: solutions {sol}")
    print(f"    expected: {expected}")
    return found

def verify_point(Qcoeffs, n, rvals, expect_q):
    m = pdeg(Qcoeffs)
    router = [0]*(n+1); router[n] = 1
    for i, v in rvals.items(): router[i] = v
    P = pcompose(router, Qcoeffs)
    q = q_deRham(P, rng=rng)
    S = support(P, 12*n*m)
    print(f"    numeric check R={router} over Q: q={q} Sigma={sorted(S)} (expected q={expect_q})")
    return q == expect_q

t0 = time.time(); ok = True

Q_quartic = poly_from_dict({4:1, 1:1})
Q_sq2     = poly_from_dict({6:1, 2:1})
Q_cub2    = poly_from_dict({6:1, 4:2, 2:3})
Q_sq3     = poly_from_dict({9:1, 3:1})
Q_D5      = dickson(5, 1)
Q_qo3     = poly_from_dict({6:1, 3:1})

f = extension_search("Q=x^4+x", Q_quartic, 2, "empty everywhere (no square of a quartic keeps rank 3)")
ok &= (len(f) == 0)
f = extension_search("Q=x^4+x", Q_quartic, 3, "single point r1=r2=0, surviving {1,7,10} (the collision)")
ok &= (len(f) == 1 and f[0][1] == [{sp.Symbol('r1'): 0, sp.Symbol('r2'): 0}])
ok &= verify_point(Q_quartic, 3, {}, 3)

f = extension_search("Q=x^6+x^2", Q_sq2, 2, "single point r1=0, surviving {1,5,9} (aligned square)")
ok &= (len(f) == 1 and list(f[0][1]) == [0])
ok &= verify_point(Q_sq2, 2, {}, 3)
f = extension_search("Q=x^6+x^2", Q_sq2, 3, "empty everywhere (no cube preserves)")
ok &= (len(f) == 0)

f = extension_search("Q=x^6+2x^4+3x^2 (generic cubicO)", Q_cub2, 2, "empty everywhere (alignment needs A=0)")
ok &= (len(f) == 0)
f = extension_search("Q=x^6+2x^4+3x^2 (generic cubicO)", Q_cub2, 3, "empty everywhere")
ok &= (len(f) == 0)

f = extension_search("Q=x^9+x^3", Q_sq3, 2, "single point r1=0, surviving {1,7,13}")
ok &= (len(f) == 1 and list(f[0][1]) == [0])
f = extension_search("Q=x^9+x^3", Q_sq3, 3, "empty everywhere")
ok &= (len(f) == 0)

f = extension_search("Q=D_5(x,1)", Q_D5, 2, "single point r1=0 (Dickson chain D_2)")
ok &= (len(f) == 1 and list(f[0][1]) == [0])
ok &= verify_point(Q_D5, 2, {}, 2)
f = extension_search("Q=D_5(x,1)", Q_D5, 3, "single point (r1,r2)=(-3,0): the chain D_3(y,1)=y^3-3y")
ok &= (len(f) == 1 and f[0][1] == [{sp.Symbol('r1'): -3, sp.Symbol('r2'): 0}])
ok &= verify_point(Q_D5, 3, {1: -3}, 2)

f = extension_search("Q=x^6+x^3 (quadO m=3)", Q_qo3, 2, "empty everywhere (Fermat rigidity 10.2)")
ok &= (len(f) == 0)

print("\n--- mutation records (numeric, for the table) ---")
for name, P, expq in [("(x^4+x+1)^3", pcompose(monoxp(3), poly_from_dict({4:1,1:1,0:1})), 9),
                      ("(x^6+x^2)^3", pcompose(monoxp(3), Q_sq2), None),
                      ("(x^6+x^3)^2", pcompose(monoxp(2), Q_qo3), None),
                      ("(x^6+2x^4+3x^2)^2", pcompose(monoxp(2), Q_cub2), 6)]:
    q = q_deRham(P, P61, rng=rng); S = support(P, 10*pdeg(centre(P, P61)), P61)
    print(f"    {name}: q={q} Sigma={sorted(S)}")
    if expq is not None: ok &= (q == expq)

print("\n--- loci sweeps: exact boundaries of the rank strata ---")
bad = 0
for _ in range(120):
    A = rng.randrange(1, P61-1); m = rng.choice([2,3])
    B = (A*A*pow(4,P61-2,P61)) % P61
    c = poly_from_dict({3*m:1, 2*m:A, m:B}, P61)
    q = q_deRham(c, P61, rng=rng)
    want = 2 if m == 2 else 3
    if q != want: bad += 1; print(f"  LOCUS FAIL m={m} A={A}: q={q} want {want}")
for _ in range(120):
    A = rng.randrange(1, P61-1); m = rng.choice([2,3])
    B = rng.randrange(1, P61-1)
    if B == (A*A*pow(4,P61-2,P61)) % P61: continue
    q = q_deRham(poly_from_dict({3*m:1, 2*m:A, m:B}, P61), P61, rng=rng)
    if q != 3: bad += 1; print(f"  LOCUS FAIL generic m={m}: q={q}")
for _ in range(60):
    A = rng.randrange(0, P61-1)
    q0 = q_deRham(poly_from_dict({4:1, 2:A}, P61), P61, rng=rng)
    q1 = q_deRham(poly_from_dict({4:1, 2:A, 1: rng.randrange(1, P61-1)}, P61), P61, rng=rng)
    if not ((q0 <= 2) and q1 == 3): bad += 1; print(f"  LOCUS FAIL quartic A={A}: q0={q0} q1={q1}")
print(f"    cubicO sublocus B=A^2/4: m=2 drops to rank 2, m=3 stays rank 3; quartic q=3 iff B!=0: "
      f"{'PASS' if bad == 0 else 'FAIL'} (300 random points)")
ok &= (bad == 0)

print(f"\nBATTERY 4D: {'PASS - extension loci are exactly the aligned points of Theorem 9.1' if ok else 'REVIEW REQUIRED'}  [{time.time()-t0:.1f}s]")
sys.exit(0 if ok else 1)
