import random, sys, itertools, cmath
import numpy as np
from lib import *

rng = random.Random(3141)

def num_rank(M, tol=1e-8):
    if M.size == 0: return 0, float('inf')
    sv = np.linalg.svd(M, compute_uv=False)
    smax = sv[0] if len(sv) else 0.0
    if smax == 0: return 0, float('inf')
    r = int(np.sum(sv > tol*smax))
    gap = (sv[r-1]/sv[r]) if r < len(sv) and sv[r] > 0 else float('inf')
    return r, gap

def branch_matrix(coeffs, rows, N):
    """Rows: branch indices j; columns i=0..N; entry F_i * zeta_d^{j(1-i)} (exact F via QQ->float)."""
    a = centre(coeffs)
    d = pdeg(a)
    F = inverse_series_F(a, N)
    zeta = cmath.exp(2j*cmath.pi/d)
    M = np.zeros((len(rows), N+1), dtype=complex)
    for ri, j in enumerate(rows):
        for i in range(N+1):
            if F[i] != 0:
                M[ri, i] = float(F[i]) * zeta**((j*(1-i)) % d)
    return M

def fusion_check(name, Rout, Qin, subsets='all'):
    P = pcompose(Rout, Qin)
    a = centre(P); d = pdeg(a)
    m = pdeg(ptrim(Qin)); n = pdeg(ptrim(Rout))
    if d != m*n:
        print(f"FAIL {name}: degree {d} != {m}*{n}")
        return False
    Sig = support(P, 12*d, P61)
    SigQ = support(Qin, 12*m, P61) if m >= 2 else frozenset({1} if m==1 else set())
    # heredity (8.12)
    proj = frozenset(r % m for r in Sig) if m >= 2 else None
    her = (proj == SigQ) if m >= 2 else True
    # L_c sets
    Ls = {}
    for r in Sig:
        c = r % m
        l = ((r - c)//m) % n if (r - c) % m == 0 else None
        # compute l properly: r = c + m*l mod d
        l = ((r - c) * pow(m, -1, n)) % n if False else ((r - c)//m) % n
        Ls.setdefault(c, set()).add(l)
    zeta_n = cmath.exp(2j*cmath.pi/n)
    N = 10*d
    ok = her
    if not her:
        print(f"FAIL heredity {name}: pi_m(Sigma(P))={sorted(proj)} vs Sigma(Q)={sorted(SigQ)}")
    subs = [tuple(A) for k in range(1, n+1) for A in itertools.combinations(range(n), k)] if subsets=='all' \
           else subsets
    worst_gap = float('inf')
    for A in subs:
        rows = [ (aa + n*b) % d for aa in A for b in range(m) ]
        lhs, gap = num_rank(branch_matrix(P, rows, N))
        worst_gap = min(worst_gap, gap)
        rhs = 0
        for c, L in Ls.items():
            Msub = np.array([[zeta_n**((aa*l) % n) for l in sorted(L)] for aa in A], dtype=complex)
            r_c, g = num_rank(Msub)
            worst_gap = min(worst_gap, g)
            rhs += r_c
        if lhs != rhs:
            print(f"FAIL 8.10 {name} A={A}: LHS(numeric)={lhs} RHS(Fourier)={rhs}")
            ok = False
    # Cor 8.4 pairwise intersections via inclusion-exclusion + direct formula
    for aa, bb in itertools.combinations(range(n), 2):
        rows_a = [ (aa + n*b) % d for b in range(m) ]
        rows_b = [ (bb + n*b) % d for b in range(m) ]
        da, _ = num_rank(branch_matrix(P, rows_a, N))
        db, _ = num_rank(branch_matrix(P, rows_b, N))
        dab, _ = num_rank(branch_matrix(P, rows_a+rows_b, N))
        inter_numeric = da + db - dab
        inter_formula = sum(1 for c, L in Ls.items()
                            if all(((aa-bb)*(l1-l2)) % n == 0 for l1 in L for l2 in L))
        if inter_numeric != inter_formula:
            print(f"FAIL 8.13 {name} ({aa},{bb}): numeric {inter_numeric} formula {inter_formula}")
            ok = False
    # Cor 8.6 / 8.7
    qP, qQ = len(Sig), len(SigQ)
    inj = len(proj) == len(Sig)
    full_fusion_pred = all(len(L) == 1 for L in Ls.values())
    if (qP == qQ) != inj or inj != full_fusion_pred:
        print(f"FAIL 8.6 {name}: qP={qP} qQ={qQ} injective={inj} allsingleton={full_fusion_pred}")
        ok = False
    nofusion_pred = all(len(L) == n for L in Ls.values())
    if nofusion_pred != (qP == n*qQ):
        print(f"FAIL 8.7 {name}: qP={qP} n*qQ={n*qQ} nofusion={nofusion_pred}")
        ok = False
    print(f"{'PASS' if ok else 'FAIL'}  {name:36s} d={d:2d} q(P)={qP} q(Q)={qQ} "
          f"L={{{', '.join(str(c)+':'+str(sorted(L)) for c,L in sorted(Ls.items()))}}} min_gap={worst_gap:.1e}")
    return ok

allok = True
print("=== Structured fusion cases: formula 8.10, 8.12, 8.13, 8.6, 8.7 ===")
allok &= fusion_check("(x^4+x)^3  full fusion", monoxp(3), poly_from_dict({4:1,1:1}))
allok &= fusion_check("D_15 = D_3(D_5(x,1),1)", dickson(3,1), dickson(5,1))
allok &= fusion_check("(x^6+x^2)^2 aligned square", monoxp(2), poly_from_dict({6:1,2:1}))
allok &= fusion_check("(x^6+x^4+x^2)^2 no-fusion mutation", monoxp(2), poly_from_dict({6:1,4:1,2:1}))
allok &= fusion_check("(x^8+x^2)^3 mutation", monoxp(3), poly_from_dict({8:1,2:1}))
allok &= fusion_check("(x^3+x)^2", monoxp(2), poly_from_dict({3:1,1:1}))
allok &= fusion_check("(x^3+x)^2+ (x^3+x) partial", poly_from_dict({2:1,1:1}), poly_from_dict({3:1,1:1}))
allok &= fusion_check("(x^3+x)^3+(x^3+x)^2", poly_from_dict({3:1,2:1}), poly_from_dict({3:1,1:1}))
allok &= fusion_check("(x^4+x)^2", monoxp(2), poly_from_dict({4:1,1:1}))
allok &= fusion_check("random R3 o Q4", poly_from_dict({3:1,2:2,1:-1}), poly_from_dict({4:1,2:1,1:3}))

print("\n=== Heredity 8.12 on 200 random pairs (exact, mod two primes) ===")
bad = 0
for _ in range(200):
    m = rng.choice([2,3,4,5]); n = rng.choice([2,3,4])
    Q = [0]*(m+1); Q[m] = 1
    for i in range(0, m-1): Q[i] = rng.randrange(-6,7)
    R = [0]*(n+1); R[n] = 1
    for i in range(0, n): R[i] = rng.randrange(-6,7)
    P = pcompose(R, Q)
    for pp in (P61, P2):
        Sig = support(P, 12*m*n, pp)
        SigQ = support(Q, 12*m, pp) if m >= 2 else frozenset()
        if m >= 2 and frozenset(r % m for r in Sig) != SigQ:
            print("HEREDITY FAIL", R, Q, sorted(Sig), sorted(SigQ)); bad += 1
print(f"heredity: 200 pairs x 2 primes, {bad} failures")
allok &= bad == 0

print("\nBATTERY 3:", "ALL PASS" if allok else "FAILURES PRESENT")
sys.exit(0 if allok else 1)
