"""Pivot-guided minors classification + number-field pointwise decision.

Per shape: (1) exact numeric elimination at random rational parameter points finds
the generic rank of [A|b] and, when it is u+1, the pivot ROW SET; (2) the symbolic
determinants of those pivot rows (from >= 2 independent points) generate an ideal
I with solvable-locus subset V(I); (3) if I = (1): EMPTY; else solve I: for
zero-dimensional candidates, verify each point EXACTLY over its number field via
the generic NF class; refuted points certify emptiness, verified points are
genuine excess solutions (exotic if the bidegree is mechanism-free).
"""
import itertools, random, time
from fractions import Fraction
import sympy as sp
from laurent_cls2 import shape_rows

rng = random.Random(99)

# ---------- generic number field Q[x]/(f), f monic with Fraction coeffs ----------
def poly_divmod(a, b):
    a = a[:]; q = [Fraction(0)]*(max(len(a)-len(b)+1, 1))
    while len(a) >= len(b) and any(a):
        if a[-1] == 0: a.pop(); continue
        c = a[-1]/b[-1]; d = len(a)-len(b)
        q[d] = c
        for i in range(len(b)): a[d+i] -= c*b[i]
        a.pop()
    return q, a

def poly_xgcd(a, b):
    r0, r1 = a[:], b[:]
    s0, s1 = [Fraction(1)], [Fraction(0)]
    while any(r1):
        q, r = poly_divmod(r0, r1)
        r0, r1 = r1, r
        # s0 - q*s1
        prod = [Fraction(0)]*(len(q)+len(s1)-1 if s1 else 1)
        for i, qi in enumerate(q):
            for j, sj in enumerate(s1):
                prod[i+j] += qi*sj
        ns = [Fraction(0)]*max(len(s0), len(prod))
        for i in range(len(s0)): ns[i] += s0[i]
        for i in range(len(prod)): ns[i] -= prod[i]
        while len(ns) > 1 and ns[-1] == 0: ns.pop()
        s0, s1 = s1, ns
    return r0, s0

class NF:
    """element of Q[x]/(f); f list of Fractions ascending, monic."""
    def __init__(self, f, vec):
        self.f = f
        d = len(f)-1
        v = [Fraction(x) for x in vec] + [Fraction(0)]*d
        self.v = self._red(v[:])
    def _red(self, v):
        f, d = self.f, len(self.f)-1
        while len(v) > d:
            c = v.pop()
            if c:
                for i in range(d):
                    v[len(v)-d+i] -= c*f[i]
        while len(v) < d: v.append(Fraction(0))
        return v
    def _mk(self, vec): return NF(self.f, vec)
    def __add__(s, o):
        o = o if isinstance(o, NF) else NF(s.f, [o])
        return s._mk([a+b for a, b in zip(s.v, o.v)])
    __radd__ = __add__
    def __neg__(s): return s._mk([-a for a in s.v])
    def __sub__(s, o): return s + (-(o if isinstance(o, NF) else NF(s.f, [o])))
    def __rsub__(s, o): return NF(s.f, [o]) - s
    def __mul__(s, o):
        o = o if isinstance(o, NF) else NF(s.f, [o])
        prod = [Fraction(0)]*(len(s.v)+len(o.v)-1)
        for i, a in enumerate(s.v):
            if a:
                for j, b in enumerate(o.v):
                    if b: prod[i+j] += a*b
        return s._mk(prod)
    __rmul__ = __mul__
    def inv(s):
        g, u = poly_xgcd(s.f, s.v + [Fraction(0)])
        assert len(g) == 1 and g[0] != 0, "not invertible"
        return s._mk([x/g[0] for x in u])
    def __truediv__(s, o):
        o = o if isinstance(o, NF) else NF(s.f, [o])
        return s * o.inv()
    def __rtruediv__(s, o): return NF(s.f, [o]) * s.inv()
    def __eq__(s, o):
        o = o if isinstance(o, NF) else NF(s.f, [o])
        return s.v == o.v
    def __ne__(s, o): return not s.__eq__(o)
    def __repr__(s): return "NF" + str([str(x) for x in s.v])

def nf_solve_shape(m, cterm_vals, shape, E, field_f):
    """cterm_vals: [(i, NF value)] with c_{-m}=1 implicit. Returns (solvable, sol or n_resid)."""
    one = NF(field_f, [1]); zero = NF(field_f, [0])
    unknowns = sorted(k for k, v in shape.items() if v == 'u')
    monic = next(k for k, v in shape.items() if v == 1)
    Mneg = max(0, -min(shape.keys())); Npos = max(0, max(shape.keys()))
    K = m*E + Mneg + 4
    def smulF(A, B):
        C = [zero]*(K+1)
        for i, x in enumerate(A):
            if x != zero:
                for j in range(min(len(B), K+1-i)):
                    if B[j] != zero: C[i+j] = C[i+j] + x*B[j]
        return C
    def sinvF(A):
        B = [zero]*(K+1); B[0] = A[0].inv()
        for k in range(1, K+1):
            acc = zero
            for i in range(1, min(k, len(A)-1)+1):
                if A[i] != zero: acc = acc + A[i]*B[k-i]
            B[k] = zero - B[0]*acc
        return B
    G = [zero]*(K+1); G[0] = one
    maxpow = max([m]+[i+m for i, _ in cterm_vals])
    for _ in range(60):
        pw = [[one]+[zero]*K]
        for _ in range(maxpow): pw.append(smulF(pw[-1], G))
        F = pw[m][:]; F[0] = F[0] - one
        for i, c in cterm_vals:
            sh = i+m; src = pw[i+m]
            for jj in range(0, K+1-sh):
                if src[jj] != zero: F[sh+jj] = F[sh+jj] - c*src[jj]
        if all(x == zero for x in F): break
        Fp = [x*m for x in pw[m-1]]
        for i, c in cterm_vals:
            sh = i+m; src = pw[i+m-1]
            for jj in range(0, K+1-sh):
                if src[jj] != zero: Fp[sh+jj] = Fp[sh+jj] - c*src[jj]*(i+m)
        corr = smulF(F, sinvF(Fp))
        G = [G[t]-corr[t] for t in range(K+1)]
    pw = {0: [one]+[zero]*K, 1: G}
    for k in range(2, Npos+1): pw[k] = smulF(pw[k-1], G)
    if Mneg:
        Gi = sinvF(G); pw[-1] = Gi
        for k in range(2, Mneg+1): pw[-k] = smulF(pw[-(k-1)], Gi)
    A, b = [], []
    for e in range(1, E+1):
        row = []
        for k in unknowns:
            idx = m*e - k
            row.append(pw[k][idx] if 0 <= idx <= K else zero)
        idxm = m*e - monic
        b.append(zero - (pw[monic][idxm] if 0 <= idxm <= K else zero))
        A.append(row)
    rw = 0
    for col in range(len(unknowns)):
        pr = next((i for i in range(rw, len(A)) if A[i][col] != zero), None)
        if pr is None: continue
        A[rw], A[pr] = A[pr], A[rw]; b[rw], b[pr] = b[pr], b[rw]
        pv = A[rw][col]
        A[rw] = [x/pv for x in A[rw]]; b[rw] = b[rw]/pv
        for i in range(len(A)):
            if i != rw and A[i][col] != zero:
                f = A[i][col]
                A[i] = [x - f*y for x, y in zip(A[i], A[rw])]
                b[i] = b[i] - f*b[rw]
        rw += 1
    resid = sum(1 for i in range(len(A)) if all(x == zero for x in A[i]) and b[i] != zero)
    if resid: return (False, resid)
    return (True, b[:len(unknowns)])

# ---------- pivot-guided shape decision ----------
def decide_shape(m, cnames, cterms_fn, shape, E, npts=3):
    A_rows, b_col, unknowns = shape_rows(m, cnames, cterms_fn, shape, E)
    u = len(unknowns)
    syms = [sp.Symbol(nm) for nm in cnames]
    aug = [[sp.sympify(str(x)) for x in row] + [sp.sympify(str(b))]
           for row, b in zip(A_rows, b_col)]
    dets = []
    for _ in range(npts):
        vals = {s: Fraction(rng.randrange(2, 40), rng.randrange(1, 4)) for s in syms}
        num = [[Fraction(sp.Rational(e.subs(vals))) for e in row] for row in aug]
        rows_i = list(range(len(num)))
        pivots, rw = [], 0
        work = [r[:] for r in num]
        for col in range(u+1):
            pr = next((i for i in range(rw, len(work)) if work[i][col] != 0), None)
            if pr is None: continue
            work[rw], work[pr] = work[pr], work[rw]
            rows_i[rw], rows_i[pr] = rows_i[pr], rows_i[rw]
            pv = work[rw][col]
            work[rw] = [x/pv for x in work[rw]]
            for i in range(len(work)):
                if i != rw and work[i][col] != 0:
                    f = work[i][col]
                    work[i] = [x - f*y for x, y in zip(work[i], work[rw])]
            pivots.append(rows_i[rw]); rw += 1
        if rw < u + 1:
            return ("SOLVABLE-GENERICALLY (rank <= u at random point)", None)
        Msub = sp.Matrix([aug[i] for i in sorted(pivots[:u+1])])
        try:
            d = sp.expand(Msub.det(method='bareiss'))
        except Exception:
            d = sp.expand(Msub.det(method='berkowitz'))
        if d != 0:
            dets.append(d)
            if len(dets) >= 2 and syms:
                Gb = sp.groebner(dets, *syms, order='grevlex')
                if any(g == 1 for g in Gb.exprs):
                    return ("EMPTY", None)
    if not syms:
        return ("EMPTY" if dets else "CANDIDATE", None)
    if not dets:
        return ("SOLVABLE-GENERICALLY?", None)
    Gb = sp.groebner(dets, *syms, order='grevlex')
    if any(g == 1 for g in Gb.exprs):
        return ("EMPTY", None)
    return ("CANDIDATE V(I)", [sp.factor(g) for g in Gb.exprs])
