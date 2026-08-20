"""Demonstration of the dictionary q(P,dx) = order of the minimal ODE of I(s) = int e^{sP(x)}dx.

Pipeline per phase P:
  (1) PREDICT the order by series reversion: |Sigma(P)|  (milliseconds).
  (2) DERIVE the ODE symbolically: reduce [P^j dx] in H_P with s symbolic
      (substitution u = 1/s makes all entries polynomial in u), find the first
      Krylov dependence, solve for the coefficients, clear denominators.
  (3) VALIDATE against ground truth: I^{(j)}(s) = int P(x)^j e^{sP(x)} dx by
      high-precision quadrature (mpmath); report the relative residual of the ODE.
"""
import time
from fractions import Fraction
import sympy as sp
from mpmath import mp, quad, exp as mexp, mpf
from lib import centre, pdeg, ptrim, pcompose, poly_from_dict, monoxp, dickson, support

U = sp.Symbol('u')   # u = 1/s
S = sp.Symbol('s')

# ---- u-polynomial helpers (lists of Fractions, ascending in u) ----
def uadd(a, b):
    n = max(len(a), len(b)); c = [Fraction(0)]*n
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    return c
def uscal(a, k): return [x*k for x in a]
def ushift(a):   return [Fraction(0)] + list(a)          # multiply by u
def uiszero(a):  return all(x == 0 for x in a)

def reduce_sym(f, a, d):
    """f: list over x-degree of u-polys. Reduce mod (g' + sP'g) to x-degree <= d-2."""
    Pp = [Fraction(i)*a[i] for i in range(1, d+1)]        # P' ascending, rationals
    f = [list(c) for c in f]
    def xdeg(v):
        i = len(v)-1
        while i >= 0 and uiszero(v[i]): i -= 1
        return i
    N = xdeg(f)
    while N >= d-1:
        cN = f[N]; sh = N-d+1
        base = uscal(cN, Fraction(1, d))                  # cN/d
        # subtract sP'g = (cN/d) * P' * x^{sh}
        for i, pi in enumerate(Pp):
            if pi:
                f[sh+i] = uadd(f[sh+i], uscal(base, -pi))
        # subtract g' = sh*(cN/d)*u * x^{sh-1}
        if sh >= 1:
            f[sh-1] = uadd(f[sh-1], ushift(uscal(base, -Fraction(sh))))
        Nn = xdeg(f)
        assert Nn < N, "reduction failed"
        N = Nn
    out = f[:d-1] + [[Fraction(0)]]*(d-1-len(f))
    return [sp.Poly(list(reversed([sp.Rational(x.numerator, x.denominator) for x in c])) or [0], U).as_expr()
            for c in out[:d-1]]

def upoly(v, d):
    """embed integer x-poly as symbolic f (u-degree 0)."""
    return [[Fraction(v[i])] if i < len(v) else [Fraction(0)] for i in range(d*20)]

def derive_ode(coeffs, name, expect):
    a0 = centre(coeffs); d = pdeg(a0)
    a = [Fraction(x) for x in a0]
    t0 = time.time()
    Pj = [Fraction(1)]
    reds, q = [], None
    M = sp.zeros(d-1, 0)
    for j in range(0, d):
        f = [[Pj[i]] if i < len(Pj) else [Fraction(0)] for i in range(max(len(Pj), d))]
        col = sp.Matrix(reduce_sym(f, a, d))
        M2 = M.row_join(col)
        if M2.rank() > M.rank():
            M = M2
        else:
            q = j
            sol = M.solve(col)      # unique: M has full column rank q
            break
        # Pj *= P
        newP = [Fraction(0)]*(len(Pj)+d)
        for i, x in enumerate(Pj):
            if x:
                for k, y in enumerate(a):
                    if y: newP[i+k] += x*y
        Pj = newP
    # ODE: I^{(q)} = sum_j sol[j] * I^{(j)}, coefficients rational in u; substitute u = 1/s
    cs = [sp.together(sol[j].subs(U, 1/S)) for j in range(q)]
    den = sp.lcm([sp.denom(c) for c in cs] + [sp.Integer(1)])
    ode = [sp.expand(den)] + [sp.expand(-den*c) for c in reversed(cs)]   # coeff of D^q, D^{q-1}, ..., D^0
    g = sp.gcd(ode)
    ode = [sp.factor(sp.cancel(c/g)) for c in ode]
    terms = " + ".join(f"({sp.sstr(c)})*I{'^('+str(q-k)+')' if q-k>1 else (chr(39) if q-k==1 else '')}"
                       for k, c in enumerate(ode))
    ok = (q == expect)
    print(f"[{'OK ' if ok else '***'}] {name}: derived order {q} (predicted {expect})   [{time.time()-t0:.1f}s]")
    print(f"      L[I] = {terms} = 0")
    return q, ode

def validate(coeffs, ode, name, svals):
    """coeffs even-degree, positive lead: quadrature on R for s<0."""
    a = centre(coeffs); d = pdeg(a)
    mp.dps = 30
    q = len(ode)-1
    Pnum = lambda x: sum(mpf(str(a[i]))*x**i for i in range(d+1))
    worst = 0
    for sv in svals:
        Ij = []
        for j in range(q+1):
            f = lambda x, j=j: (Pnum(x)**j)*mexp(mpf(str(sv))*Pnum(x))
            Ij.append(quad(f, [-4, 0, 4]))
        terms = [complex(sp.N(ode[k].subs(S, sp.Rational(str(sv))), 25))*complex(Ij[q-k]) for k in range(q+1)]
        resid = abs(sum(terms))/max(abs(t) for t in terms)
        worst = max(worst, resid)
        print(f"      s={sv}: |L[I]| / max|term| = {resid:.2e}")
    print(f"[{'OK ' if worst < 1e-12 else '***'}] {name}: quadrature residuals (ground truth) at {len(svals)} points")

print("="*80)
print("STEP 1 - the order oracle: predicted minimal ODE order = |Sigma(P)| by reversion")
print("="*80)
cases = [
    ("x^7                       ", monoxp(7), None),
    ("D_5(x,1)  (Bessel class)  ", dickson(5,1), None),
    ("x^4+x^2+x  (Pearcey)      ", poly_from_dict({4:1,2:1,1:1}), None),
    ("x^4+x^2    (B=0 sublocus) ", poly_from_dict({4:1,2:1}), None),
    ("(x^6+x^2)^2 (aligned sq.) ", pcompose(monoxp(2), poly_from_dict({6:1,2:1})), None),
    ("(x^6+x^4+x^2)^2 (mutation)", pcompose(monoxp(2), poly_from_dict({6:1,4:1,2:1})), None),
    ("(x^4+x)^3  (exceptional)  ", pcompose(monoxp(3), poly_from_dict({4:1,1:1})), None),
    ("x^12+x^10+x^3  (generic)  ", poly_from_dict({12:1,10:1,3:1}), None),
]
pred = {}
for name, c, _ in cases:
    t0 = time.time()
    Sg = support(c, 10*pdeg(ptrim(c)))
    pred[name] = len(Sg)
    print(f"  {name} degree {pdeg(ptrim(c)):2d}  ->  predicted order {len(Sg)}  "
          f"(generic would be {pdeg(ptrim(c))-1})   [{1000*(time.time()-t0):.0f} ms]")

print()
print("="*80)
print("STEP 2 - derive the ODEs symbolically (twisted de Rham reduction, s symbolic)")
print("="*80)
_, ode_anchor = derive_ode(monoxp(4), "x^4 anchor (closed form: I = Gamma(1/4)/(2(-s)^{1/4}))", 1)
_, ode_pear = derive_ode(poly_from_dict({4:1,2:1,1:1}), "x^4+x^2+x (Pearcey class)", 3)
_, ode_sq   = derive_ode(pcompose(monoxp(2), poly_from_dict({6:1,2:1})), "(x^6+x^2)^2, degree 12", 3)
_, ode_exc  = derive_ode(pcompose(monoxp(3), poly_from_dict({4:1,1:1})), "(x^4+x)^3, degree 12 - THE EXCEPTIONAL OPERATOR", 3)

# generic degree-12 comparison: certify Krylov rank 11 at a rational point u0 (rank at a point <= generic rank <= d-1)
import random
from lib import q_deRham
rng = random.Random(5)
qgen = q_deRham(poly_from_dict({12:1,10:1,3:1}), None, s_values=[Fraction(3,7), Fraction(-5,2)], rng=rng)
print(f"[{'OK ' if qgen == 11 else '***'}] x^12+x^10+x^3 (generic comparison): exact Krylov rank = {qgen} = d-1;"
      f" same degree as the exceptional phase, ODE order 11 vs 3")

print()
print("="*80)
print("STEP 3 - validate against ground truth: high-precision quadrature of int P^j e^{sP} dx")
print("="*80)
validate(monoxp(4), ode_anchor, "x^4 anchor", [-1, -2])
validate(poly_from_dict({4:1,2:1,1:1}), ode_pear, "Pearcey class", [-1, Fraction(-1,2)])
validate(pcompose(monoxp(2), poly_from_dict({6:1,2:1})), ode_sq, "(x^6+x^2)^2", [-1])
validate(pcompose(monoxp(3), poly_from_dict({4:1,1:1})), ode_exc, "(x^4+x)^3 exceptional", [-1, Fraction(-3,4)])
print()
print("Done: prediction (combinatorial) -> derivation (exact symbolic) -> validation (numerical ground truth).")
