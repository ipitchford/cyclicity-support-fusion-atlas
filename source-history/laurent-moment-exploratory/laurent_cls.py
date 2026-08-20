"""Classification of the excess locus for the Laurent moment problem, small bidegrees.

For each bidegree, coefficients are symbolic; a shape-enumerated Q (normalised
modulo C[L] and monic at its extreme exponent) is imposed to satisfy the moment
conditions [tau^{me}](Q o phi) = 0, e = 1..E. Groebner elimination of the
Q-unknowns yields the exact locus of coefficients where excess solutions exist.

Bidegrees:
  (1,2): L = z^{-1} + a z + z^2  (c0=0, c_{-1}=c_2=1).  No composition or z^d
         mechanism exists here, so ANY nonempty locus is exotic.
  (2,2): L = z^{-2} + b z^{-1} + a z + z^2.  Mechanisms predict the locus b = +-a
         (L = A(z + w0 -+ 1/z)) containing the point a=b=0 (L = A(z^2)).
  (1,3): L = z^{-1} + a1 z + a2 z^2 + z^3.  Again mechanism-free: exotic hunt.
"""
import time
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ

def sym_smul(A, B, K, zero):
    C = [zero]*(K+1)
    for i in range(min(len(A), K+1)):
        ai = A[i]
        if ai == zero: continue
        for j in range(min(len(B), K+1-i)):
            bj = B[j]
            if bj == zero: continue
            C[i+j] = C[i+j] + ai*bj
    return C

def sym_sinv(A, K, R):
    zero, one = R.zero, R.one
    B = [zero]*(K+1)
    # assumes A[0] is a nonzero rational constant times one
    a0 = A[0]
    # extract constant
    c0 = a0.coeff(1) if hasattr(a0, 'coeff') else a0
    B[0] = one*QQ(1,1)/QQ(c0) if not isinstance(c0, int) else one*QQ(1, c0)
    for k in range(1, K+1):
        acc = zero
        for i in range(1, min(k, len(A)-1)+1):
            if A[i] != zero:
                acc = acc + A[i]*B[k-i]
        B[k] = -(B[0]*acc)
    return B

def sym_branch_G(cterms, m, K, R):
    """cterms: list of (i, ring elem c_i) for i > -m; c_{-m}=1. Newton for G."""
    zero, one = R.zero, R.one
    G = [zero]*(K+1); G[0] = one
    maxpow = max([m] + [i+m for i, _ in cterms]) if cterms else m
    for _ in range(60):
        pw = [[one] + [zero]*K]
        for _ in range(maxpow):
            pw.append(sym_smul(pw[-1], G, K, zero))
        F = pw[m][:]
        F[0] = F[0] - one
        for i, c in cterms:
            sh = i + m
            src = pw[i+m]
            for jj in range(0, K+1-sh):
                if src[jj] != zero:
                    F[sh+jj] = F[sh+jj] - c*src[jj]
        if all(x == zero for x in F):
            return G
        Fp = [x*m for x in pw[m-1]]
        for i, c in cterms:
            sh = i + m
            src = pw[i+m-1]
            for jj in range(0, K+1-sh):
                if src[jj] != zero:
                    Fp[sh+jj] = Fp[sh+jj] - c*src[jj]*(i+m)
        corr = sym_smul(F, sym_sinv(Fp, K, R), K, zero)
        G = [G[t] - corr[t] for t in range(K+1)]
    raise RuntimeError("symbolic Newton failed")

def classify(name, m, n, cnames, cterms_fn, shapes, E, K_extra=4):
    """cnames: parameter names. shapes: list of dicts {exponent: 'unknown'|value}
       with exactly one exponent set to 1 (monic) and 0 excluded (constants trivial)."""
    t0 = time.time()
    print(f"--- {name} ---")
    results = {}
    for shp_id, shape in enumerate(shapes):
        unknowns = sorted([k for k, v in shape.items() if v == 'u'])
        qnames = [f"q{('m' if k<0 else '')}{abs(k)}" for k in unknowns]
        R = ring(",".join(cnames + qnames), QQ)[0]
        gens = R.gens
        cs = {nm: gens[i] for i, nm in enumerate(cnames)}
        qs = {k: gens[len(cnames)+i] for i, k in enumerate(unknowns)}
        cterms = cterms_fn(cs)
        Mneg = -min(shape.keys()); Npos = max(shape.keys())
        Mneg = max(Mneg, 0); Npos = max(Npos, 0)
        K = m*E + Mneg + K_extra
        G = sym_branch_G(cterms, m, K, R)
        # powers of G for k in [min shape .. max shape]
        zero, one = R.zero, R.one
        pw = {0: [one] + [zero]*K}
        for k in range(1, Npos+1):
            pw[k] = sym_smul(pw[k-1], G, K, zero)
        if Mneg > 0:
            Gi = sym_sinv(G, K, R)
            for k in range(1, Mneg+1):
                pw[-k] = sym_smul(pw[-(k-1)], Gi, K, zero)
        conds = []
        for e in range(1, E+1):
            acc = zero
            for k, v in shape.items():
                idx = m*e - k
                if 0 <= idx <= K and pw[k][idx] != zero:
                    coef = one if v == 1 else qs[k]
                    acc = acc + coef*pw[k][idx]
            if acc != zero:
                conds.append(acc)
        exprs = [sp.sympify(str(g)) for g in conds]
        syms_c = [sp.Symbol(nm) for nm in cnames]
        syms_q = [sp.Symbol(nm) for nm in qnames]
        if not exprs:
            results[shp_id] = ("ALL", shape)
            print(f"  shape {shape}: NO conditions -> solutions for all parameters (!)")
            continue
        G2 = sp.groebner(exprs, *(syms_q + syms_c), order='lex')
        elim = [g for g in G2.exprs if not any(s in g.free_symbols for s in syms_q)]
        if any(g == 1 for g in G2.exprs):
            results[shp_id] = ("EMPTY", shape)
            print(f"  shape {shape}: EMPTY (no parameters admit this solution shape)")
        elif not elim:
            results[shp_id] = ("ALLC", shape)
            print(f"  shape {shape}: solvable for ALL parameter values (locus = everything)")
        else:
            fac = [sp.factor(g) for g in elim]
            results[shp_id] = (fac, shape)
            print(f"  shape {shape}: locus V({fac})")
    print(f"[{time.time()-t0:.1f}s]")
    return results

# ============ (1,2):  L = z^{-1} + a z + z^2,  parameter a ============
shapes12 = []
# top-monic odd tops (mod C[L] normal forms), q0 excluded (constants trivial)
for top, bot in [(1,1),(1,2),(1,3),(1,4),(3,1),(3,2),(3,3),(3,4)]:
    sh = {top: 1}
    for k in range(-bot, top):
        if k != 0 and k != top: sh[k] = 'u'
    if top == 3: sh.pop(2, None)  # z^2 removable by subtracting multiples of L
    shapes12.append(sh)
# pure-nonpositive, bottom-monic
for bot in [1,2,3,4]:
    sh = {-bot: 1}
    for k in range(-bot+1, 0): sh[k] = 'u'
    shapes12.append(sh)
res12 = classify("(1,2): L = 1/z + a z + z^2", 1, 2, ["a"],
                 lambda cs: [(1, cs["a"]), (2, cs["a"]**0)], shapes12, E=12)

# ============ (2,2):  L = z^{-2} + b/z + a z + z^2 ============
shapes22 = []
for top, bot in [(1,1),(1,2),(1,3),(3,1),(3,2),(3,3)]:
    sh = {top: 1}
    for k in range(-bot, top):
        if k != 0 and k != top: sh[k] = 'u'
    shapes22.append(sh)
for bot in [1,2,3]:
    sh = {-bot: 1}
    for k in range(-bot+1, 0): sh[k] = 'u'
    shapes22.append(sh)
res22 = classify("(2,2): L = z^-2 + b/z + a z + z^2", 2, 2, ["a","b"],
                 lambda cs: [(-1, cs["b"]), (1, cs["a"]), (2, cs["a"]**0)], shapes22, E=10)

# ============ (1,3):  L = 1/z + a1 z + a2 z^2 + z^3 ============
shapes13 = []
for top, bot in [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3)]:
    sh = {top: 1}
    for k in range(-bot, top):
        if k != 0 and k != top: sh[k] = 'u'
    shapes13.append(sh)
for bot in [1,2,3]:
    sh = {-bot: 1}
    for k in range(-bot+1, 0): sh[k] = 'u'
    shapes13.append(sh)
res13 = classify("(1,3): L = 1/z + a1 z + a2 z^2 + z^3", 1, 3, ["a1","a2"],
                 lambda cs: [(1, cs["a1"]), (2, cs["a2"]), (3, cs["a1"]**0)], shapes13, E=12)
