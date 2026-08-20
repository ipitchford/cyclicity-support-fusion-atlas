"""Row-shuffled box-minors classifier (final form).

Excess in box[-M,N]  <=>  rank(full condition matrix on slots k != 0) < r*,
r* = (M+N) - min(M//m, N//n).  Excess locus  subset of  V(any set of r*-minors).
Row order is shuffled per sample point so successive minors draw on different
condition depths (fix for the shallow-pivot degeneration).  Ideal = (1) certifies
EMPTY for all parameters; otherwise the candidate variety is decided pointwise
(mod-p zero-excess at a point certifies the exact statement, since reduction can
only lower rank) or by polynomial restriction onto the candidate locus.
"""
import random, time
from fractions import Fraction
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ
from lcls import sym_branch_G, sym_smul, sym_sinv

rng = random.Random(424242)

def box_matrix_sym(m, cnames, cterms_fn, Mneg, Npos, E):
    R = ring(",".join(cnames), QQ)[0]
    cs = {nm: g for nm, g in zip(cnames, R.gens)}
    K = m*E + Mneg + 4
    G = sym_branch_G(cterms_fn(cs), m, K, R)
    zero, one = R.zero, R.one
    pw = {0: [one]+[zero]*K, 1: G}
    for k in range(2, Npos+1): pw[k] = sym_smul(pw[k-1], G, K, zero)
    Gi = sym_sinv(G, K, R); pw[-1] = Gi
    for k in range(2, Mneg+1): pw[-k] = sym_smul(pw[-(k-1)], Gi, K, zero)
    slots = [k for k in range(-Mneg, Npos+1) if k != 0]
    rows = [[sp.sympify(str(pw[k][m*e-k])) if 0 <= m*e-k <= K else sp.S(0)
             for k in slots] for e in range(1, E+1)]
    return rows, slots

def box_classify(title, m, n, cnames, cterms_fn, Mneg, Npos, npts=5, Epad=8):
    nslots = Mneg + Npos
    rstar = nslots - min(Mneg//m, Npos//n)
    rows, slots = box_matrix_sym(m, cnames, cterms_fn, Mneg, Npos, rstar + Epad)
    syms = [sp.Symbol(nm) for nm in cnames]
    dets = []
    for _ in range(npts):
        vals = {s: Fraction(rng.randrange(2, 60), rng.randrange(1, 5)) for s in syms}
        order = list(range(len(rows))); rng.shuffle(order)
        num = [[Fraction(sp.Rational(e.subs(vals))) for e in rows[i]] for i in order]
        rowsel, colsel, ridx, work, rw = [], [], order[:], [r[:] for r in num], 0
        for col in range(nslots):
            pr = next((i for i in range(rw, len(work)) if work[i][col] != 0), None)
            if pr is None: continue
            work[rw], work[pr] = work[pr], work[rw]
            ridx[rw], ridx[pr] = ridx[pr], ridx[rw]
            pv = work[rw][col]; work[rw] = [x/pv for x in work[rw]]
            for i in range(len(work)):
                if i != rw and work[i][col] != 0:
                    f = work[i][col]
                    work[i] = [x - f*y for x, y in zip(work[i], work[rw])]
            rowsel.append(ridx[rw]); colsel.append(col); rw += 1
            if rw == rstar: break
        if rw < rstar:
            print(f"  {title} box[-{Mneg},{Npos}]: GENERIC EXCESS (rank < r* at random point)")
            return "GENERIC"
        d = sp.expand(sp.Matrix([[rows[i][j] for j in colsel]
                                 for i in rowsel]).det(method='bareiss'))
        if d != 0:
            dets.append(d)
            if len(dets) >= 2 and syms:
                Gb = sp.groebner(dets, *syms, order='grevlex')
                if any(g == 1 for g in Gb.exprs):
                    print(f"  {title} box[-{Mneg},{Npos}] (r*={rstar}): EMPTY -- certified for all parameters")
                    return []
    if not syms:
        print(f"  {title}: {'EMPTY' if dets else '?'}")
        return [] if dets else None
    Gb = sp.groebner(dets, *syms, order='grevlex')
    if any(g == 1 for g in Gb.exprs):
        print(f"  {title} box[-{Mneg},{Npos}] (r*={rstar}): EMPTY -- certified")
        return []
    loc = [sp.factor(g) for g in Gb.exprs]
    print(f"  {title} box[-{Mneg},{Npos}] (r*={rstar}): locus V({loc})")
    return loc

if __name__ == "__main__":
    box_classify("(2,2)", 2, 2, ["a", "b"],
                 lambda cs: [(-1, cs["b"]), (1, cs["a"]), (2, cs["a"]**0)], 3, 3, npts=8)
