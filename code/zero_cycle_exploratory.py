"""At-infinity tangential centre problem on zero-cycles: effective solution via the atlas.

Setting: f monic centred degree d; branches at infinity xi_j(tau) = xi(zeta^j tau), f(xi_j)=tau^d.
A zero-cycle at infinity: weights n=(n_j), sum n_j = 0. Tangential centre condition for g:
    sum_j n_j g(xi_j(tau)) == 0   (identically).

CRITERION (proved in the writeup): vanishing  <=>  the class-r part of g o xi vanishes
for every r in supp(n-hat), where n-hat(r) = sum_j n_j zeta^{jr}.

This script:
  A. verifies the criterion two ways on random cases (exact classes vs numerical branches);
  B. audits MECHANISM EXCESS for the certified degree-12 families: which support kills are
     NOT explained by deck symmetry (composition) or the dihedral (Dickson) mechanism;
  C. computes the centre-space Hilbert function for the rational cycle n_j = cos(2*pi*j/3)
     on f = (x^4+x)^3, decides the degree-7/10 existence questions exactly, and compares
     with the composition-mechanism prediction;
  D. numerically verifies the new identity  sum_j cos(2pi j/3) xi_j(tau) == 0  on actual roots.
"""
import time, random
from fractions import Fraction
from math import gcd
import sympy as sp
from mpmath import mp, mpf, mpc, polyroots, cos as mcos, pi as mpi, exp as mexpn
from lib import (centre, pdeg, ptrim, pcompose, poly_from_dict, monoxp, dickson,
                 inverse_series_F, support, P61, P2)

rng = random.Random(2026)

def match_labels(roots, tau, d, zeta):
    """Assign each root a distinct label j by globally greedy nearest matching."""
    pairs = sorted(((abs(rt - zeta**j*tau), j, idx) for idx, rt in enumerate(roots) for j in range(d)),
                   key=lambda t: t[0])
    lab, used_j, used_r = {}, set(), set()
    for dist, j, idx in pairs:
        if j in used_j or idx in used_r: continue
        lab[j] = roots[idx]; used_j.add(j); used_r.add(idx)
        if len(lab) == d: break
    return lab


def xi_power_class_coeff(F, k, e, d):
    """coefficient of tau^e in xi^k = tau^k F(1/tau)^k: index i = k - e in F^k."""
    return None  # placeholder (we precompute powers)

def build_condition_matrix(coeffs, classes, N, M, p):
    """Rows: (r, e) with e = r mod d, e in [k_min, N], e >= -M; cols: g-coeff g_0..g_N.
       Entry = [tau^e] xi^k = F^k_{k-e}. Returns matrix (list of rows) mod p."""
    a = centre(coeffs, p)
    d = pdeg(a)
    F = inverse_series_F(a, N + M, p)
    # powers of F up to N
    pows = [[1] + [0]*(N+M)]
    for k in range(1, N+1):
        prev = pows[-1]
        cur = [0]*(N+M+1)
        for i, x in enumerate(prev):
            if x:
                for jj, y in enumerate(F):
                    if y and i+jj <= N+M:
                        cur[i+jj] = (cur[i+jj] + x*y) % p
        pows.append(cur)
    rows = []
    for r in classes:
        e = r - d*((r + M)//d)  # smallest e >= -M with e = r mod d
        while e <= N:
            row = []
            for k in range(0, N+1):
                i = k - e
                row.append(pows[k][i] if 0 <= i <= N+M else 0)
            if any(row): rows.append([x % p for x in row])
            e += d
    return rows

def rank_mod(rows, p):
    rows = [r[:] for r in rows]; rank = 0; ncols = len(rows[0]) if rows else 0; piv = 0
    for c in range(ncols):
        pr = next((i for i in range(rank, len(rows)) if rows[i][c] % p), None)
        if pr is None: continue
        rows[rank], rows[pr] = rows[pr], rows[rank]
        inv = pow(rows[rank][c], p-2, p)
        rows[rank] = [(x*inv) % p for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(x - f*y) % p for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank

def centre_space_dims(coeffs, classes, Nmax, p, Mfac=12):
    d = pdeg(ptrim(coeffs))
    out = {}
    M = Mfac*d + Nmax
    rowsfull = build_condition_matrix(coeffs, classes, Nmax, M, p)
    for N in range(0, Nmax+1):
        sub = [r[:N+1] for r in rowsfull]
        sub = [r for r in sub if any(r)]
        out[N] = (N+1) - rank_mod(sub, p)
    return out

t0 = time.time()
print("== A. Criterion verification: class test vs direct numerical branch summation ==")
mp.dps = 30
ok = True
structured = [
    (poly_from_dict({8:1,4:3}), 3),                                   # quadO: Sigma={1,5}, class 3 killed
    (poly_from_dict({12:1,8:2,4:5}), 3),                              # cubicO: Sigma={1,5,9}, class 3 killed
    (pcompose(monoxp(3), poly_from_dict({4:1,1:1})), 4),              # exceptional: class 4 killed
    (dickson(8, 1), 5),                                               # Dickson: Sigma={1,7}, class 5 killed
]
for trial in range(10):
    if trial < len(structured):
        c, r0 = structured[trial]
        d = pdeg(ptrim(c)); a = centre(c)
    else:
        d = rng.choice([6, 8, 12])
        c = [0]*(d+1); c[d] = 1
        for i in rng.sample(range(0, d-1), rng.randrange(1, d-1)):
            c[i] = rng.randrange(-4, 5) or 2
        a = centre(c)
        r0 = rng.randrange(1, d)
    # cycle n_j = zeta^{-j r0}: vanishing for g=x  <=>  class r0 of xi is empty
    Sg = support(c, 14*d, P61)
    predict_vanish = (r0 not in Sg)
    tau = mpf("2.2")
    poly = [mpf(str(a[d-i])) for i in range(0, d+1)]
    poly[-1] -= tau**d
    roots = polyroots(poly, maxsteps=200, extraprec=80)
    zeta = mexpn(2j*mpi/d)
    lab = match_labels(roots, tau, d, zeta)
    ssum = sum(zeta**(-j*r0)*lab[j] for j in range(d))
    numeric_vanish = abs(ssum) < 1e-9
    tag = "OK " if numeric_vanish == predict_vanish else "***"
    ok &= numeric_vanish == predict_vanish
    print(f"  [{tag}] d={d} cycle r={r0}: class-{r0} in Sigma? {r0 in Sg};"
          f"  |sum_j zeta^(-jr) x_j(tau)| = {float(abs(ssum)):.2e}")

print("\n== B. Mechanism-excess audit, degree 12 (families certified by the atlas sweep) ==")
def deck_order(coeffs):
    a = [int(x) for x in ptrim(coeffs)]
    d = pdeg(a)
    g = 0
    for i in range(0, d):
        if a[i] != 0: g = gcd(g, d - i)
    return g if g else d
fams = [
  ("x^12 (power)",            monoxp(12), "deck Z/12"),
  ("D_12(x,1) (Dickson)",     dickson(12, 1), "dihedral (u + a/u)"),
  ("x^12+3x^6 (quadO m=6)",   poly_from_dict({12:1,6:3}), "deck Z/6"),
  ("x^12+2x^8+5x^4 (cubicO)", poly_from_dict({12:1,8:2,4:5}), "deck Z/4"),
  ("(x^6+2x^2)^2 (aligned)",  pcompose(monoxp(2), poly_from_dict({6:1,2:2})), "deck Z/4 (sublocus)"),
  ("(x^4+x)^3 (EXCEPTIONAL)", pcompose(monoxp(3), poly_from_dict({4:1,1:1})), "deck Z/3"),
  ("x^12+x^10+x^3 (generic)", poly_from_dict({12:1,10:3,3:2}), "none"),
]
for name, c, mech in fams:
    d = pdeg(ptrim(c)); Sg = support(c, 16*d, P61)
    m = deck_order(c)
    deck_pred = frozenset(r for r in range(1, d) if r % m == 1 % m) if m > 1 else frozenset(range(1, d))
    if "D_12" in name:
        mech_pred = frozenset({1, d-1})   # dihedral mechanism: xi = u + a/u
    else:
        mech_pred = deck_pred
    excess = mech_pred - Sg
    print(f"  {name:26s} Sigma={sorted(Sg)}; mechanism [{mech}] predicts <= {sorted(mech_pred)};"
          f"  UNEXPLAINED KILLS: {sorted(excess) if excess else 'none'}")

print("\n== C. Centre space of the rational cycle n_j = cos(2pi j/3) on f=(x^4+x)^3 ==")
E = pcompose(monoxp(3), poly_from_dict({4:1,1:1}))
Nmax = 26
dims1 = centre_space_dims(E, [4, 8], Nmax, P61)
dims2 = centre_space_dims(E, [4, 8], Nmax, P2)
assert dims1 == dims2, "prime disagreement"
comp = {N: (N//3 + 1) + len([k for k in range(1, N//12 + 1) if 12*(k-1)+1 <= N]) for N in range(Nmax+1)}
# composition mechanism C[x^3] plus the known exotic tower x*P^k (deg 12k+1)
comp = {N: (N//3 + 1) + len([k for k in range(0, Nmax) if 12*k+1 <= N]) for N in range(Nmax+1)}
print("  N:            ", "  ".join(f"{N:2d}" for N in range(0, Nmax+1, 2)))
print("  dim centre_N: ", "  ".join(f"{dims1[N]:2d}" for N in range(0, Nmax+1, 2)))
print("  C[x^3]+x*P^k: ", "  ".join(f"{comp[N]:2d}" for N in range(0, Nmax+1, 2)))
print("  (excess of computed dim over C[x^3] alone measures non-composition centres)")

# decide degree-7 and degree-10 existence exactly over Q
print("\n  Exact existence questions (over Q, conditions to depth 40d):")
a = centre(E); d = 12
F = inverse_series_F(a, 40*d + 12, None)
def exact_conditions(N, classes, M):
    pows = [[Fraction(1)] + [Fraction(0)]*M]
    for k in range(1, N+1):
        prev = pows[-1]; cur = [Fraction(0)]*(M+1)
        for i, x in enumerate(prev):
            if x:
                for jj in range(0, M+1-i):
                    if F[jj]: cur[i+jj] += x*F[jj]
        pows.append(cur)
    rows = []
    for r in classes:
        e = r - d*((r + (M - N))//d)
        while e <= N:
            row = [pows[k][k-e] if 0 <= k-e <= M else Fraction(0) for k in range(N+1)]
            if any(row): rows.append(row)
            e += d
    return rows
for N, want in [(7, "degree-7"), (10, "degree-10")]:
    rows = exact_conditions(N, [4, 8], 40*d)
    Msp = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in rows])
    ns = Msp.nullspace()
    # basis elements with top-degree N (not inherited from lower degree)
    tops = [v for v in ns if v[N] != 0]
    print(f"    {want} centre element with leading term x^{N}: "
          f"{'EXISTS' if tops else 'does NOT exist'}   (nullspace dim <= {N}: {len(ns)})")
    if tops:
        v = tops[0]/tops[0][N]
        gpoly = sp.expand(sum(v[k]*sp.Symbol('x')**k for k in range(N+1)))
        print(f"      g = {gpoly}")

print("\n== D. The new identity, numerically on actual roots of (x^4+x)^3 = tau^12 ==")
tau = mpf("1.3")
aE = centre(E)
poly = [mpf(str(aE[12-i])) for i in range(13)]; poly[-1] -= tau**12
roots = polyroots(poly, maxsteps=300, extraprec=120)
zeta = mexpn(2j*mpi/12)
lab = match_labels(roots, tau, 12, zeta)
w = [mcos(2*mpi*j/3) for j in range(12)]
sE = sum(w[j]*lab[j] for j in range(12))
G = poly_from_dict({12:1,10:3,3:2}); aG = centre(G)
polyG = [mpf(str(sp.Rational(str(aG[12-i])))) for i in range(13)]; polyG[-1] -= tau**12
rootsG = polyroots(polyG, maxsteps=300, extraprec=120)
labG = match_labels(rootsG, tau, 12, zeta)
sG = sum(w[j]*labG[j] for j in range(12))
print(f"  exceptional f: |sum_j cos(2pi j/3) x_j(tau)| = {float(abs(sE)):.2e}   (identity: exact zero)")
print(f"  generic f:     |sum_j cos(2pi j/3) x_j(tau)| = {float(abs(sG)):.2e}   (no identity)")
print(f"\n[{time.time()-t0:.1f}s]  criterion check: {'ALL CONSISTENT' if ok else 'REVIEW'}")
