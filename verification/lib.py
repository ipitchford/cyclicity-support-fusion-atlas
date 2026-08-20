"""Independent verification library for the cyclicity bundle.

Two independent computations:
  (A) Sigma(P): residue support of the normalised inverse xi(t), P(xi(t)) = t^d,
      via Newton iteration on F^d + sum_j p_j y^(d-j) F^j = 1  (y = 1/t, xi = t F(y)).
  (B) q(P,dx): Krylov dimension of span_K{[P^j dx]} in H_P = K[x]dx / (f' + sP'f)dx,
      basis [x^0..x^(d-2)], with s specialised to random rationals / random F_p points.

Backends: exact Fraction ('QQ') and mod-p ('Fp', p = 2^61-1 Mersenne prime by default).
Polynomials are ascending coefficient lists.
"""
from fractions import Fraction
import random

P61 = (1 << 61) - 1  # Mersenne prime
P2 = (1 << 61) - 31  # second large prime 2305843009213693921
# verify primality of P2 quickly below in selftest

# ---------- polynomial helpers (ascending coeff lists) ----------

def pdeg(a):
    i = len(a) - 1
    while i >= 0 and a[i] == 0:
        i -= 1
    return i

def ptrim(a):
    d = pdeg(a)
    return a[:d+1] if d >= 0 else [0]

def padd(a, b, p=None):
    n = max(len(a), len(b))
    c = [0]*n
    for i, x in enumerate(a): c[i] = x
    for i, x in enumerate(b):
        c[i] = (c[i] + x) % p if p else c[i] + x
    return c

def pscal(a, k, p=None):
    return [ (x*k) % p if p else x*k for x in a ]

def pmulpoly(a, b, p=None):
    if pdeg(a) < 0 or pdeg(b) < 0: return [0]
    c = [0]*(pdeg(a)+pdeg(b)+2)
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if y == 0: continue
            c[i+j] = (c[i+j] + x*y) % p if p else c[i+j] + x*y
    return c

def pcompose(outer, inner, p=None):
    """outer(inner(x)) by Horner."""
    res = [0]
    for c in reversed(outer):
        res = pmulpoly(res, inner, p)
        res = padd(res, [c], p)
    return res

def pshift_x(a, c, p=None):
    """a(x + c)"""
    return pcompose(a, [c % p if p else c, 1], p)

# ---------- centring ----------

def centre(a, p=None):
    """Make monic centred: divide by lead, shift x by -p_{d-1}/d, drop constant.
    Returns coefficient list with a[d]=1, a[d-1]=0, a[0]=0."""
    a = ptrim(list(a))
    d = pdeg(a)
    lead = a[d]
    if p:
        il = pow(lead, p-2, p)
        a = [ (x*il) % p for x in a ]
        shift = (-a[d-1] * pow(d, p-2, p)) % p
    else:
        a = [ Fraction(x, 1) / lead for x in a ]
        shift = Fraction(-a[d-1], d)
    a = pshift_x(a, shift, p)
    a[0] = 0
    a = [x % p for x in a] if p else a
    return ptrim(a)

# ---------- truncated power series (lists, index = power of y) ----------

def smul(A, B, N, p=None):
    C = [0]*(N+1)
    for i in range(min(len(A), N+1)):
        ai = A[i]
        if ai == 0: continue
        lim = min(len(B), N+1-i)
        if p:
            for j in range(lim):
                bj = B[j]
                if bj: C[i+j] = (C[i+j] + ai*bj) % p
        else:
            for j in range(lim):
                bj = B[j]
                if bj: C[i+j] += ai*bj
    return C

def sinv(A, N, p=None):
    B = [0]*(N+1)
    a0 = A[0]
    B[0] = pow(a0, p-2, p) if p else Fraction(1,1)/a0
    for n in range(1, N+1):
        acc = 0
        for i in range(1, min(n, len(A)-1)+1):
            if A[i]:
                acc = (acc + A[i]*B[n-i]) % p if p else acc + A[i]*B[n-i]
        B[n] = (-B[0]*acc) % p if p else -B[0]*acc
    return B

def inverse_series_F(coeffs, N, p=None):
    """coeffs: centred monic ascending, degree d. Solve
       F^d + sum_j p_j y^(d-j) F^j = 1 (mod y^(N+1)), F(0)=1, by Newton.
       Returns F list length N+1."""
    a = ptrim(list(coeffs))
    d = pdeg(a)
    if not ((a[d] == 1) and (a[d-1] % p == 0 if p else a[d-1] == 0)):
        raise ValueError("inverse_series_F requires a monic centred polynomial")
    one = Fraction(1,1) if not p else 1
    F = [0]*(N+1); F[0] = one
    ymon = {}
    for j in range(0, d-1):
        if a[j] != 0:
            ymon[j] = a[j]  # coefficient of y^{d-j} F^j
    it = 0
    while True:
        it += 1
        # G(F) = F^d + sum_j a_j y^{d-j} F^j - 1 via Horner in F:
        # T = 1 (coeff of F^d); for j=d-1..0: T = T*F + a_j y^{d-j}
        T = [0]*(N+1); T[0] = one
        for j in range(d-1, -1, -1):
            T = smul(T, F, N, p)
            aj = a[j] if j <= d-2 else 0
            if j == d-1: aj = 0
            if aj != 0 and d-j <= N:
                T[d-j] = (T[d-j] + aj) % p if p else T[d-j] + aj
        G = T[:]
        G[0] = (G[0] - one) % p if p else G[0] - one
        if all(x == 0 for x in G):
            break
        # G'(F) = d F^{d-1} + sum_j j a_j y^{d-j} F^{j-1}, Horner:
        # S = d; for j = d-1..1: S = S*F + j*a_j*y^{d-j}
        S = [0]*(N+1); S[0] = d % p if p else Fraction(d,1)
        for j in range(d-1, 0, -1):
            S = smul(S, F, N, p)
            aj = a[j] if j <= d-2 else 0
            if j == d-1: aj = 0
            if aj != 0 and d-j <= N:
                v = (j*aj) % p if p else j*aj
                S[d-j] = (S[d-j] + v) % p if p else S[d-j] + v
        corr = smul(G, sinv(S, N, p), N, p)
        F = [ (F[i] - corr[i]) % p if p else F[i] - corr[i] for i in range(N+1) ]
        if it > 80:
            raise RuntimeError("Newton failed to converge")
    return F

def support(coeffs, N, p=None, want_witness=False):
    """Sigma(P) as a frozenset of residues mod d, from xi = t F(1/t):
       coefficient F_i multiplies t^(1-i); residue class (1-i) mod d.
       Includes built-in sanity check: class 0 must be empty (centred trace)."""
    a = centre(coeffs, p)
    d = pdeg(a)
    F = inverse_series_F(a, N, p)
    seen = {}
    for i in range(0, N+1):
        if F[i] != 0:
            r = (1 - i) % d
            if r not in seen:
                seen[r] = 1 - i
    if 0 in seen:
        raise RuntimeError(
            "class-0 coefficient nonzero: violates centred-trace theorem "
            f"(3.8): {seen.get(0)}"
        )
    S = frozenset(seen.keys())
    return (S, seen) if want_witness else S

# ---------- twisted de Rham Krylov rank ----------

def _reduce_dR(f, a, d, s0, p=None):
    """Reduce [f dx] modulo D_P(g) = g' + s0 P' g to degree <= d-2.
       a = centred monic coeffs of P; returns vector length d-1."""
    Pp = [ ((i)*a[i]) % p if p else i*a[i] for i in range(1, d+1) ]  # P' ascending, deg d-1
    f = list(f)
    while pdeg(f) >= d-1:
        Nn = pdeg(f)
        cN = f[Nn]
        sh = Nn - (d-1)
        # g = cN/(s0*d) x^sh ;  subtract g' + s0 P' g
        if p:
            gc = (cN * pow((s0*d) % p, p-2, p)) % p
        else:
            gc = Fraction(cN,1) / (s0*d)
        # g' term:
        if sh >= 1:
            gp = [0]*sh; gp[sh-1] = (sh*gc) % p if p else sh*gc
        else:
            gp = [0]
        term = padd(gp, pscal([0]*sh + Pp, (s0*gc) % p if p else s0*gc, p), p)
        f = padd(f, pscal(term, -1 % p if p else -1, p), p)
        f = ptrim(f)
        if pdeg(f) >= Nn:
            raise RuntimeError("twisted de Rham reduction failed to lower degree")
    v = [0]*(d-1)
    for i in range(min(len(f), d-1)):
        v[i] = f[i]
    return v

def _rank_update(basis, v, p=None):
    """Gaussian elimination; basis: list of (pivot_index, row). Returns True if v added."""
    v = list(v)
    for piv, row in basis:
        if v[piv] != 0:
            if p:
                c = (v[piv] * pow(row[piv], p-2, p)) % p
                v = [ (v[i] - c*row[i]) % p for i in range(len(v)) ]
            else:
                c = v[piv] / row[piv]
                v = [ v[i] - c*row[i] for i in range(len(v)) ]
    for i, x in enumerate(v):
        if x != 0:
            basis.append((i, v))
            return True
    return False

def q_deRham(coeffs, p=None, s_values=None, rng=None):
    """q(P,dx) via Krylov of [P^j dx]; s specialised. Returns max rank over s_values."""
    rng = rng or random
    a = centre(coeffs, p)
    d = pdeg(a)
    if s_values is None:
        if p: s_values = [rng.randrange(2, p-2), rng.randrange(2, p-2)]
        else: s_values = [Fraction(rng.randrange(2, 50), rng.randrange(1, 30)) for _ in range(2)]
    best = 0
    for s0 in s_values:
        basis = []
        Pj = [1] if p else [Fraction(1,1)]
        rank = 0
        for j in range(0, d):
            v = _reduce_dR(Pj, a, d, s0, p)
            if _rank_update(basis, v, p):
                rank += 1
            else:
                break
            Pj = pmulpoly(Pj, a, p)
        best = max(best, rank)
    return best

# ---------- families ----------

def dickson(n, aa, p=None):
    """D_n(x, a) ascending coeffs."""
    D0 = [2]; D1 = [0, 1]
    if n == 0: return D0
    if n == 1: return D1
    for _ in range(2, n+1):
        Dn = padd(pmulpoly([0,1], D1, p), pscal(D0, (-aa) % p if p else -aa, p), p)
        D0, D1 = D1, Dn
    return D1

def monoxp(d):
    a = [0]*(d+1); a[d] = 1
    return a

def poly_from_dict(dd, p=None):
    n = max(dd)
    a = [0]*(n+1)
    for k, v in dd.items():
        a[k] = v % p if p else v
    return a

def selftest():
    # P2 primality (Miller-Rabin deterministic bases for < 3.3e24)
    def is_prime(n):
        for q in [2,3,5,7,11,13,17,19,23,29,31,37]:
            if n % q == 0: return n == q
        dd = n-1; r = 0
        while dd % 2 == 0: dd//=2; r+=1
        for q in [2,3,5,7,11,13,17,19,23,29,31,37]:
            x = pow(q, dd, n)
            if x in (1, n-1): continue
            for _ in range(r-1):
                x = x*x % n
                if x == n-1: break
            else: return False
        return True
    if not (is_prime(P61) and is_prime(P2)):
        raise RuntimeError("prime backends broken")
    # reversion sanity: P = x^3 - 3x (Dickson a=1): support {1,2} mod 3
    S = support([0,-3,0,1], 40)
    if S != frozenset({1,2}):
        raise RuntimeError(f"Dickson cubic support self-test failed: {S}")
    # closed form check: P=(x^2+5)^2 -> xi = t(1-5 t^-2)^{1/2}
    S = support(pcompose([0,0,1],[5,0,1]), 60)
    if S != frozenset({1,3}):
        raise RuntimeError(f"quadratic-over-power support self-test failed: {S}")
    # de Rham: x^5 -> 1 ; Dickson5 -> 2 ; generic quartic -> 3
    if q_deRham(monoxp(5)) != 1:
        raise RuntimeError("power rank self-test failed")
    if q_deRham(dickson(5,1)) != 2:
        raise RuntimeError("Dickson rank self-test failed")
    if q_deRham([0,1,1,0,1]) != 3:
        raise RuntimeError("quartic rank self-test failed")
    print("selftest OK  (P2 =", P2, "prime)")

if __name__ == "__main__":
    selftest()
