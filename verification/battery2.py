import random, sys, time
from fractions import Fraction
from lib import *

rng = random.Random(77)

def deep_support_family(name, build, params, allowed, d, N, p=P61):
    """build(param)->coeffs; assert support subset of allowed at depth N for many params.
       Returns True if all pass and the full allowed set is realised."""
    ok = True
    realised = set()
    for a in params:
        c = build(a)
        S, wit = support(c, N, p, want_witness=True)
        bad = S - allowed
        if bad:
            print(f"FAIL {name} param={a}: forbidden classes {sorted(bad)} witness exps "
                  f"{[wit[r] for r in bad]}")
            ok = False
        realised |= S
    tag = "PASS" if ok and realised == allowed else ("PASS(sub)" if ok else "FAIL")
    print(f"{tag}  {name:34s} depth N={N}  classes realised {sorted(realised)}  allowed {sorted(allowed)}  #params={len(params)}")
    return ok

t0 = time.time()
print("=== Exceptional collision (x^4+ax)^3, d=12: claimed Sigma={1,7,10}; class 4 must vanish identically ===")
params = [rng.randrange(1, P61-1) for _ in range(80)]
ok = deep_support_family("(x^4+ax)^3 mod P61", lambda a: pcompose(monoxp(3), poly_from_dict({4:1,1:a}, P61), P61),
                         params, frozenset({1,7,10}), 12, 240)
params2 = [rng.randrange(1, P2-1) for _ in range(10)]
ok &= deep_support_family("(x^4+ax)^3 mod P2", lambda a: pcompose(monoxp(3), poly_from_dict({4:1,1:a}, P2), P2),
                          params2, frozenset({1,7,10}), 12, 240, p=P2)
# exact rational, a=1, deep
S, wit = support(pcompose(monoxp(3), poly_from_dict({4:1,1:1})), 180, None, want_witness=True)
print(("PASS" if S == frozenset({1,7,10}) else "FAIL"),
      " (x^4+x)^3 exact Fractions to t^-179:", sorted(S))
ok &= S == frozenset({1,7,10})

print("\nNote: for this family a_k is a MONOMIAL in a (weight(a)=3, weight(a_k)=1-k),")
print("so vanishing at one generic parameter certifies vanishing for all a != 0, per coefficient.")

print("\n=== Other one-parameter families, deep order ===")
ok &= deep_support_family("D_11(x,a)", lambda a: dickson(11, a, P61), params[:40], frozenset({1,10}), 11, 220)
ok &= deep_support_family("(x^9+bx^3)^2", lambda b: pcompose(monoxp(2), poly_from_dict({9:1,3:b}, P61), P61),
                          params[:40], frozenset({1,7,13}), 18, 216)
ok &= deep_support_family("(x^6+bx^2)^2", lambda b: pcompose(monoxp(2), poly_from_dict({6:1,2:b}, P61), P61),
                          params[:40], frozenset({1,5,9}), 12, 240)
ok &= deep_support_family("(x^m+b)^3 m=4", lambda b: pcompose(monoxp(3), poly_from_dict({4:1,0:b}, P61), P61),
                          params[:40], frozenset({1,9,5}), 12, 240)

print("\n=== Two-parameter cubic-over-power, deep order, random (A,B) ===")
ok2 = True
for _ in range(40):
    A = rng.randrange(1, P61-1); B = rng.randrange(1, P61-1); m = rng.choice([2,3,4])
    c = poly_from_dict({3*m:1, 2*m:A, m:B}, P61)
    S = support(c, 60*m, P61)
    if not S <= frozenset({1, m+1, 2*m+1}):
        print("FAIL cubic-over-power", m, A, B, sorted(S)); ok2 = False
print("PASS  cubic-over-power 40 random (A,B), m in {2,3,4}, depth 20d" if ok2 else "FAIL")
ok &= ok2

print(f"\nBATTERY 2: {'ALL PASS' if ok else 'FAILURES'}   ({time.time()-t0:.1f}s)")
sys.exit(0 if ok else 1)
