import sys, time, random
from lib import (P61, P2, centre, pdeg, ptrim, pcompose, poly_from_dict, monoxp,
                 dickson, support, q_deRham, _reduce_dR, _rank_update, pmulpoly)

rng = random.Random(999331)

def screen_q_le3(coeffs, p, s0):
    """Fast screen: True if the first four Krylov vectors have rank <= 3 at s=s0."""
    a = centre(coeffs, p)
    d = pdeg(a)
    basis = []; Pj = [1]; rank = 0
    for j in range(4):
        v = _reduce_dR(Pj, a, d, s0, p)
        if _rank_update(basis, v, p):
            rank += 1
            if rank == 4: return False
        else:
            return True
        Pj = pmulpoly(Pj, a, p)
    return rank <= 3

def classify(coeffs):
    """Match centred integer poly against atlas shapes. Returns tag or 'UNKNOWN'."""
    a = [int(x) for x in ptrim(coeffs)]
    d = pdeg(a)
    nz = {i for i in range(1, d-1) if a[i] != 0}
    if not nz: return "power"
    if d % 2 == 0 and nz <= {d//2}: return f"quadO(m={d//2})"
    if d % 3 == 0:
        m = d//3
        if nz <= {2*m, m}:
            A, B = a[2*m], a[m]
            tag = f"cubicO(m={m})"
            if 4*B == A*A: tag += "[aligned-square locus]"
            return tag
    if d == 12 and nz <= {9, 6, 3}:
        A9 = a[9]
        if A9 != 0 and 3*a[6] == A9*A9 and 27*a[3] == A9**3:
            return "exceptional"
    if a[d-2] % d == 0:
        aa = -a[d-2]//d
        if aa != 0 and dickson(d, aa) == a:
            return f"Dickson(a={aa})"
    return "UNKNOWN"

t0 = time.time()
hits = []; screened = 0
s0 = rng.randrange(2, P61-2)

print("=== binomials x^d + a x^j, a in [-9..9]\\0, degrees 15..24 ===")
for d in range(15, 25):
    for j in range(1, d-1):
        for av in range(-9, 10):
            if av == 0: continue
            c = poly_from_dict({d:1, j:av})
            screened += 1
            if screen_q_le3(c, P61, s0):
                hits.append(("bino", d, {j:av}, c))
print(f"binomials screened: {screened}  ({time.time()-t0:.0f}s)")

t1 = time.time(); screened2 = 0
print("=== trinomials x^d + a x^j + b x^i, a,b in [-3..3]\\0 ===")
for d in range(15, 25):
    for j in range(2, d-1):
        for i in range(1, j):
            for av in (-3,-2,-1,1,2,3):
                for bv in (-3,-2,-1,1,2,3):
                    c = poly_from_dict({d:1, j:av, i:bv})
                    screened2 += 1
                    if screen_q_le3(c, P61, s0):
                        hits.append(("tri", d, {j:av, i:bv}, c))
print(f"trinomials screened: {screened2}  ({time.time()-t1:.0f}s)")

print(f"\n=== confirming {len(hits)} screen hits ===")
anom = 0
seen = {}
for kind, d, dic, c in hits:
    q1 = q_deRham(c, P61, rng=rng)
    q2 = q_deRham(c, P2, rng=rng)
    S  = support(c, 8*d, P61)
    S2 = support(c, 8*d, P2)
    ok = (q1 == q2 == len(S)) and (S == S2) and q1 <= 3
    tag = classify(c)
    key = (d, tag.split('(')[0])
    seen[key] = seen.get(key, 0) + 1
    if not ok or tag == "UNKNOWN":
        anom += 1
        print(f"  ANOMALY {kind} d={d} {dic}: q={q1}/{q2} Sigma={sorted(S)} tag={tag}")
print("hit census (degree, family):", dict(sorted(seen.items())))
print(f"anomalies among hits: {anom}")

print("\n=== impostor composites (must NOT be rank 3) ===")
imp_ok = True
perturb1 = pcompose(monoxp(3), poly_from_dict({4:1,1:2}))
perturb1[3] += 1
perturb2 = pcompose(monoxp(2), poly_from_dict({6:1,2:1}))
perturb2[4] += 1
for name, P in [("(x^4+x)^6", pcompose(monoxp(6), poly_from_dict({4:1,1:1}))),
                ("(x^4+x^2)^3", pcompose(monoxp(3), poly_from_dict({4:1,2:1}))),
                ("(x^12+x^3)^3", pcompose(monoxp(3), poly_from_dict({12:1,3:1}))),
                ("(x^4+2x)^3 + x^3", perturb1),
                ("(x^6+x^2)^2 + x^4", perturb2)]:
    q = q_deRham(P, P61, rng=rng)
    S = support(P, 8*pdeg(ptrim(P)), P61)
    flag = (q == len(S))
    ok3 = (q != 3) or (classify(P) != "UNKNOWN")
    print(f"  {name}: q={q} Sigma={sorted(S)}  identity {'OK' if flag else 'FAIL'}"
          f"{'' if ok3 else '  *** UNCLASSIFIED RANK 3 ***'}")
    imp_ok &= flag and ok3

print(f"\nBATTERY 4C: {'PASS' if anom == 0 and imp_ok else 'REVIEW REQUIRED'}  total {time.time()-t0:.0f}s")
sys.exit(0 if anom == 0 and imp_ok else 1)
