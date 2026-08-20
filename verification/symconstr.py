"""Support-constrained symbolic reversion (corrected engine).

Primal object: F(y) = 1 + sum_{i>=2} F_i y^i with xi(t) = t F(1/t), P(xi(t)) = t^d.
Master equation at order n >= 2:
    [F^d]_n + sum_{j=0}^{d-2} p_j [F^j]_{n-(d-j)} = 0.
Orders 2..d define p_{d-n} triangularly from the low F's.
Orders n > d define F_n recursively.

Mode A (build_constrained): low F's on allowed classes are ring variables u_i,
forbidden low F's are zero; conditions = F_n for forbidden n in (d, K].
Mode B (reversion_given_p): p's given as ring elements; compute all F_n.

Incremental power maintenance with the corrected tilde recursion:
    tilde[j]_n = sum_{i=0}^{n-1} [F^{j-1}]_i F_{n-i}  +  tilde[j-1]_n,
    [F^j]_n = tilde[j]_n + j * F_n.
"""
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ

def s_mul(A, B, N, zero):
    C = [zero]*(N+1)
    for i in range(min(len(A), N+1)):
        ai = A[i]
        if ai == zero: continue
        for j in range(min(len(B), N+1-i)):
            bj = B[j]
            if bj == zero: continue
            C[i+j] = C[i+j] + ai*bj
    return C

def allowed_low_indices(d, S):
    return [i for i in range(2, d+1) if (1-i) % d in S]

def _extend(F, Tpows, plist, d, n_from, n_to, R, S=None, conditions=None, nzF=None):
    """Extend F (exact to n_from-1) up to n_to using the master equation.
       Tpows[j] exact to n_from-1 (length n_from). Collect conditions if S given."""
    zero = R.zero
    inv_d = QQ(1, d)
    if nzF is None:
        nzF = [k for k in range(1, n_from) if F[k] != zero]
    for n in range(n_from, n_to+1):
        tilde = [zero]*(d+1)
        for j in range(1, d+1):
            A = Tpows[j-1]
            s = zero
            for k in nzF:
                if k <= n-1:
                    a = A[n-k]
                    if a != zero:
                        fk = F[k]
                        s = s + a*fk
            tilde[j] = s + tilde[j-1]
        acc = tilde[d]
        for j in range(0, d-1):
            idx = n-(d-j)
            if 0 <= idx <= n-1:
                pj = plist.get(j, zero)
                if pj != zero:
                    a = Tpows[j][idx]
                    if a != zero:
                        acc = acc + pj*a
        Fn = (-acc).mul_ground(inv_d) if acc != zero else zero
        F[n] = Fn
        if Fn != zero:
            nzF.append(n)
        for j in range(0, d+1):
            Tpows[j].append(tilde[j] + (j*Fn if Fn != zero else zero))
        if S is not None and (1-n) % d not in S:
            if (1-n) % d == 0:
                if Fn != zero:
                    raise RuntimeError(
                        f"class-0 coefficient nonzero at n={n}: engine/theorem violation"
                    )
            elif Fn != zero:
                conditions.append((n, Fn))
    return F, Tpows, nzF

def build_constrained(d, S, K):
    idxs = allowed_low_indices(d, S)
    names = [f"u{i}" for i in idxs]
    R = ring(",".join(names), QQ)[0] if names else ring("udummy", QQ)[0]
    gens = R.gens
    zero, one = R.zero, R.one
    us = {i: gens[k] for k, i in enumerate(idxs)}
    F = [zero]*(K+1); F[0] = one
    for i in idxs:
        F[i] = us[i]
    # low powers to order d for p-extraction
    Ftr = F[:d+1]
    pows = [[one] + [zero]*d]
    for j in range(1, d+1):
        pows.append(s_mul(pows[-1], Ftr, d, zero))
    plist = {}
    for n in range(2, d+1):
        acc = pows[d][n]
        for j in range(d-n+1, d-1):
            if plist.get(j, zero) != zero and pows[j][n-(d-j)] != zero:
                acc = acc + plist[j]*pows[j][n-(d-j)]
        plist[d-n] = -acc
    # init Tpows exact to order d
    Tpows = [p[:d+1] for p in pows]
    conditions = []
    F, Tpows, _ = _extend(F, Tpows, plist, d, d+1, K, R, S=S, conditions=conditions)
    return R, us, F, plist, conditions

def reversion_given_p(d, plist, K, R, S=None):
    """plist: dict j -> ring element (j=0..d-2, p_{d-1}=0 assumed). Returns F, conditions."""
    zero, one = R.zero, R.one
    F = [zero]*(K+1); F[0] = one
    Tpows = [[one, zero]] + [[one, zero] for _ in range(d)]
    for j in range(0, d+1):
        Tpows[j] = [one, zero]
        Tpows[0] = [one, zero]
    Tpows[0][0] = one
    # [F^0] = 1,0,...  [F^j]_0 = 1, [F^j]_1 = j*F1 = 0
    conditions = []
    F, Tpows, _ = _extend(F, Tpows, plist, d, 2, K, R, S=S, conditions=conditions)
    return F, conditions

def compose_ring(outer_list, inner_list, R):
    """outer, inner: ascending lists of ring elements. Horner."""
    zero = R.zero
    res = [zero]
    def mul(a, b):
        c = [zero]*(len(a)+len(b)-1)
        for i, x in enumerate(a):
            if x == zero: continue
            for j, y in enumerate(b):
                if y == zero: continue
                c[i+j] = c[i+j] + x*y
        return c
    for c in reversed(outer_list):
        res = mul(res, inner_list)
        if not res: res = [zero]
        res[0] = res[0] + c
    return res

# ---------- Groebner helpers ----------

def conds_to_exprs(conditions, R):
    syms = [sp.Symbol(str(g)) for g in R.gens]
    out = []
    seen = set()
    for _, g in conditions:
        e = g.as_expr()
        pe = sp.Poly(e, *syms, domain='QQ')
        pe = pe.mul_ground(1/pe.content()) if pe.content() != 0 else pe
        key = pe.rep
        if key in seen: continue
        seen.add(key)
        out.append(pe.as_expr())
    return out, syms

def staircase_dim(G, syms):
    """Krull dimension of ideal from Groebner leading monomials."""
    lms = [sp.Poly(g, *syms).LM(order=G.order) for g in G.polys] if hasattr(G, 'polys') else []
    lms = [sp.Poly(g, *syms, domain='QQ').monoms()[0] for g in
           [p.as_expr() for p in G.polys]] if not lms else None
    # simpler: recompute leading monomials wrt the GB order
    import itertools
    lt = []
    for g in G.exprs:
        pg = sp.Poly(g, *syms, domain='QQ')
        mons = pg.monoms(order=G.order)
        lt.append(mons[0])
    nv = len(syms)
    best = -1
    for r in range(nv, -1, -1):
        for T in itertools.combinations(range(nv), r):
            Tset = set(T)
            ok = True
            for m in lt:
                if all((m[i] == 0 or i in Tset) for i in range(nv)):
                    ok = False; break
            if ok:
                return r
    return 0

def reduces_to_zero(expr, G):
    return sp.reduced(expr, G)[1] == 0

if __name__ == "__main__":
    import time
    t0 = time.time()
    # Control 1: vacuity for Dickson pair d=5, S={1,4}
    R, us, F, plist, conds = build_constrained(5, {1,4}, 40)
    print("d=5 S={1,4}: #conditions =", len(conds), "(expect 0)")
    if len(conds) != 0:
        raise RuntimeError("Dickson-pair vacuity control failed")
    # Control 2: vacuity for cubic-over-power d=6, S={1,3,5}
    R, us, F, plist, conds = build_constrained(6, {1,3,5}, 48)
    print("d=6 S={1,3,5}: #conditions =", len(conds), "(expect 0)")
    if len(conds) != 0:
        raise RuntimeError("cubic-over-power vacuity control failed")
    # Control 3: quadratic-over-power pair d=8, S={1,5}
    R, us, F, plist, conds = build_constrained(8, {1,5}, 56)
    print("d=8 S={1,5}: #conditions =", len(conds), "(expect 0)")
    if len(conds) != 0:
        raise RuntimeError("quadratic-over-power vacuity control failed")
    # Control 4: p-extraction correctness: d=12 curve point vs (x^4+ax)^3
    a = QQ(3)
    R, us, F, plist, conds = build_constrained(12, {1,7,10}, 24)
    # substitute u3=-a/4, u6=-a^2/32, u12=t (solve t so that p9 matches 3a? p-extraction full check)
    # direct check: expand (x^4+3x)^3 = x^12+9x^9+27x^6+27x^3, centred, constant 0
    # find u12 value by requiring p0 pattern: instead reverse: compute F numerically via lib and compare
    import sys
    sys.path.insert(0, '.')
    from lib import inverse_series_F as num_rev, pcompose, monoxp, poly_from_dict
    from fractions import Fraction
    Pnum = pcompose(monoxp(3), poly_from_dict({4:1,1:3}))
    Fn = num_rev(Pnum, 24)
    subs = [(R.gens[0], QQ(Fraction(Fn[3]).numerator, Fraction(Fn[3]).denominator)),
            (R.gens[1], QQ(Fraction(Fn[6]).numerator, Fraction(Fn[6]).denominator)),
            (R.gens[2], QQ(Fraction(Fn[12]).numerator, Fraction(Fn[12]).denominator))]
    for j, el in plist.items():
        v = el.evaluate(subs) if el != R.zero else QQ(0)
        expect = QQ(Fraction(Pnum[j]).numerator, Fraction(Pnum[j]).denominator) if j != 0 else None
        if j == 0:
            continue  # constant differs by target translation convention
        if v != expect:
            raise RuntimeError(f"p-extraction mismatch at coefficient {j}: {v} != {expect}")
    print("d=12 p-extraction matches (x^4+3x)^3 on all non-constant coefficients")
    # Control 5: the S={1,7,10} variety at d=12
    R, us, F, plist, conds = build_constrained(12, {1,7,10}, 72)
    exprs, syms = conds_to_exprs(conds, R)
    print(f"d=12 S={{1,7,10}}: #distinct conditions = {len(exprs)}")
    G = sp.groebner(exprs, *syms, order='lex', domain='QQ')
    print("GB:", [sp.factor(g) for g in G.exprs])
    print("dim =", staircase_dim(G, syms), "(expect 2)")
    print(f"[{time.time()-t0:.1f}s]")
