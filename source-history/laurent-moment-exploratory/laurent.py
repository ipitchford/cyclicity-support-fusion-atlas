"""Laurent polynomial moment problem: two-puncture support engine.

L(z) = sum_{i=-m}^{n} c_i z^i, c_{-m} = 1 (normalised), c_n != 0.
Moment problem: find Laurent polynomials q with Res_0(L^k q) = 0 for all k >= 0.

THEOREM (reduction): q solves  <=>  Res(q) = 0 and, writing Q for the Laurent
primitive of q, the branch composition Q(phi(tau)) has ZERO coefficient at
tau^{m e} for every e >= 1, where phi(tau) = tau*G(tau) is the local branch of
L at z=0 with L(phi(tau)) = tau^{-m}, G(0)=1.

Solution module M(L) := { Q : all class-0 positive tau-coefficients of Q o phi vanish }.
Always contains C[L]  (L o phi = tau^{-m}). It is a C[L]-module.
Composition mechanism: L = A o W (A polynomial, W Laurent)  =>  C[W] subset M(L).

This engine computes dim( M(L) ∩ box[-M..N] ) exactly (two primes / exact Q),
the excess over C[L], and exact solution exhibits.
"""
from fractions import Fraction
import random
from lib import P61, P2

rng = random.Random(31415)

# ---- series helpers over Fraction or F_p (lists ascending in tau) ----
def smul(A, B, K, p=None):
    C = [0]*(K+1)
    for i in range(min(len(A), K+1)):
        ai = A[i]
        if ai == 0: continue
        for j in range(min(len(B), K+1-i)):
            bj = B[j]
            if bj == 0: continue
            C[i+j] = (C[i+j] + ai*bj) % p if p else C[i+j] + ai*bj
    return C

def sinv(A, K, p=None):
    B = [0]*(K+1)
    a0 = A[0]
    B[0] = pow(a0, p-2, p) if p else Fraction(1,1)/a0
    for k in range(1, K+1):
        acc = 0
        for i in range(1, min(k, len(A)-1)+1):
            if A[i]:
                acc = (acc + A[i]*B[k-i]) % p if p else acc + A[i]*B[k-i]
        B[k] = (-B[0]*acc) % p if p else -B[0]*acc
    return B

def branch_G(cdict, m, K, p=None):
    """Solve G^m = 1 + sum_{i>-m} c_i tau^{i+m} G^{i+m}  (Newton), G(0)=1.
       cdict: {i: c_i}, must have c_{-m} = 1."""
    one = 1 if p else Fraction(1)
    assert cdict.get(-m, 0) == 1, "normalise c_{-m}=1"
    G = [0]*(K+1); G[0] = one
    terms = [(i, c) for i, c in cdict.items() if i > -m and c != 0]
    for _ in range(80):
        # F(G) = G^m - 1 - sum c_i tau^{i+m} G^{i+m}
        # compute powers of G up to max needed exponent
        maxpow = max([m] + [i+m for i, _ in terms])
        pw = [[one] + [0]*K]
        for _ in range(maxpow):
            pw.append(smul(pw[-1], G, K, p))
        F = pw[m][:]
        F[0] = (F[0] - one) % p if p else F[0] - one
        for i, c in terms:
            sh = i + m
            src = pw[i+m]
            for jj in range(0, K+1-sh):
                if src[jj]:
                    v = (c*src[jj]) % p if p else c*src[jj]
                    F[sh+jj] = (F[sh+jj] - v) % p if p else F[sh+jj] - v
        if all(x == 0 for x in F):
            return G
        # F'(G) = m G^{m-1} - sum c_i (i+m) tau^{i+m} G^{i+m-1}
        Fp = [ (m*x) % p if p else m*x for x in pw[m-1] ]
        for i, c in terms:
            sh = i + m
            src = pw[i+m-1]
            for jj in range(0, K+1-sh):
                if src[jj]:
                    v = (c*(i+m)*src[jj]) % p if p else c*(i+m)*src[jj]
                    Fp[sh+jj] = (Fp[sh+jj] - v) % p if p else Fp[sh+jj] - v
        corr = smul(F, sinv(Fp, K, p), K, p)
        G = [ (G[t] - corr[t]) % p if p else G[t] - corr[t] for t in range(K+1) ]
    raise RuntimeError("Newton failed")

def gpowers(G, kmin, kmax, K, p=None):
    """dict k -> series of G^k, k in [kmin, kmax]."""
    one = 1 if p else Fraction(1)
    out = {0: [one] + [0]*K}
    for k in range(1, kmax+1):
        out[k] = smul(out[k-1], G, K, p)
    if kmin < 0:
        Gi = sinv(G, K, p)
        for k in range(1, -kmin+1):
            out[-k] = smul(out[-(k-1)], Gi, K, p)
    return out

def condition_matrix(cdict, m, Mneg, Npos, E, p=None):
    """Rows e=1..E; columns k=-Mneg..Npos; entry [tau^{me-k}] G^k. Returns rows, kcols."""
    K = m*E + Mneg + 2
    G = branch_G(cdict, m, K, p)
    pw = gpowers(G, -Mneg, Npos, K, p)
    kcols = list(range(-Mneg, Npos+1))
    rows = []
    for e in range(1, E+1):
        row = []
        for k in kcols:
            idx = m*e - k
            row.append(pw[k][idx] if 0 <= idx <= K else 0)
        rows.append([x % p for x in row] if p else row)
    return rows, kcols

def rank_mod(rows, p):
    rows = [r[:] for r in rows]; rank = 0
    ncols = len(rows[0]) if rows else 0
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

def rank_exact(rows):
    rows = [r[:] for r in rows]; rank = 0
    ncols = len(rows[0]) if rows else 0
    for c in range(ncols):
        pr = next((i for i in range(rank, len(rows)) if rows[i][c] != 0), None)
        if pr is None: continue
        rows[rank], rows[pr] = rows[pr], rows[rank]
        pv = rows[rank][c]
        rows[rank] = [x/pv for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [x - f*y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank

def module_dim(cdict, m, n, Mneg, Npos, p=P61, E=None):
    if E is None: E = 2*(Npos + Mneg) + 8
    rows, _ = condition_matrix(cdict, m, Mneg, Npos, E, p)
    r = rank_mod(rows, p) if p else rank_exact(rows)
    dim = (Npos + Mneg + 1) - r
    powers = min(Mneg//m, Npos//n) + 1
    return dim, dim - powers

def selftests():
    print("== engine controls ==")
    # 1. L = z + 1/z  (m=n=1): expect M(L) = C[L]: dim = min(M,N)+1, excess 0
    L = {-1:1, 1:1}
    for (M,N) in [(3,3),(4,6),(6,4),(5,5)]:
        d1, e1 = module_dim(L, 1, 1, M, N, P61)
        d2, e2 = module_dim(L, 1, 1, M, N, P2)
        assert (d1,e1)==(d2,e2)
        print(f"  z+1/z  box[-{M},{N}]: dim={d1} excess={e1}  (expect excess 0)")
    # 2. L = z^2 + z^{-2} = W^2-2, W=z+1/z: expect C[W]: dim=min(M,N)+1
    L = {-2:1, 2:1}
    for (M,N) in [(3,3),(4,4),(5,5),(6,6),(4,6)]:
        d1, e1 = module_dim(L, 2, 2, M, N, P61)
        d2, e2 = module_dim(L, 2, 2, M, N, P2)
        assert (d1,e1)==(d2,e2)
        exp = min(M,N)+1 - (min(M//2,N//2)+1)
        print(f"  z^2+z^-2 box[-{M},{N}]: dim={d1} excess={e1}  (composition C[W] predicts excess {exp})")
    # 3. generic (1,2): expect excess 0
    L = {-1:1, 1:3, 2:1}
    for (M,N) in [(4,6),(6,8)]:
        d1, e1 = module_dim(L, 1, 2, M, N, P61)
        print(f"  generic (1,2) c1=3: box[-{M},{N}]: dim={d1} excess={e1}  (expect 0)")
    # 4. decomposable (2,2): L = A(W), W = z - 1/z + 0, A = y^2 + 5y: L = z^2 -2 +z^-2 +5z -5/z
    #    normalised c_{-2}=1: L = z^2 + 5z - 5 z^{-1} + z^{-2} (constant dropped: c0 := 0 shift ok)
    L = {-2:1, -1:-5, 1:5, 2:1}
    for (M,N) in [(4,4),(5,5),(6,6)]:
        d1, e1 = module_dim(L, 2, 2, M, N, P61)
        exp = min(M,N)+1 - (min(M//2,N//2)+1)
        print(f"  A(z-1/z) (2,2): box[-{M},{N}]: dim={d1} excess={e1}  (C[W] predicts excess {exp})")
    # 5. cubic composition (3,3): L = W^3 - 3W (W=z+1/z) = z^3 + z^-3
    L = {-3:1, 3:1}
    for (M,N) in [(4,4),(6,6)]:
        d1, e1 = module_dim(L, 3, 3, M, N, P61)
        exp = min(M,N)+1 - (min(M//3,N//3)+1)
        print(f"  z^3+z^-3 (3,3): box[-{M},{N}]: dim={d1} excess={e1}  (C[W] predicts excess {exp})")
    # 6. generic-rank certificates for a spread of bidegrees (random rational coefficients)
    print("== generic-rank certificates (semicontinuity: one exact point per (m,n)) ==")
    for (m,n) in [(1,1),(1,2),(1,3),(1,4),(2,2),(2,3),(3,3),(2,4),(3,4)]:
        c = {-m:1, n: rng.randrange(1,7)}
        for i in range(-m+1, n):
            if i != 0: c[i] = rng.randrange(-5,6)
        c = {i:v for i,v in c.items() if v != 0}; c[-m]=1
        M, N = 2*m+2, 2*n+2
        d1, e1 = module_dim(c, m, n, M, N, P61)
        d2, e2 = module_dim(c, m, n, M, N, P2)
        assert (d1,e1)==(d2,e2)
        print(f"  (m,n)=({m},{n}) random L: box[-{M},{N}] dim={d1} excess={e1}"
              f"  -> generic excess {'0 CERTIFIED' if e1==0 else 'NONZERO (!)'}")

if __name__ == "__main__":
    selftests()
