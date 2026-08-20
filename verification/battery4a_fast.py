import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path
import random
import sys
import time
import sympy as sp
from sympy import QQ
from symconstr import build_constrained, conds_to_exprs, staircase_dim, allowed_low_indices
sys.path.insert(0, '.')
from lib import (inverse_series_F, pcompose, monoxp, poly_from_dict, dickson,
                 pdeg, ptrim, P61)

rng = random.Random(424242)


def expression_digest(expressions):
    """Digest a canonical textual representation of exact SymPy expressions."""
    payload = "\n".join(sp.srepr(sp.expand(expr)) for expr in expressions)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def failure_count(results):
    """Return the number of semantic failures in an atlas sweep."""
    return len(results["anomalies"]) + len(results["nocert"])

def fam_samplers(d):
    """Return dict famname -> (support frozenset, dim, sampler(rng)->coeff list mod P61)."""
    p = P61
    fams = {}
    fams['power'] = (frozenset({1}), 1,
        lambda: poly_from_dict({d:1, 0:rng.randrange(1,p)}, p))
    fams['dickson'] = (frozenset({1, d-1}), 2,
        lambda: [ (c + (rng.randrange(1,p) if i==0 else 0)) % p
                  for i, c in enumerate(dickson(d, rng.randrange(1,p), p)) ])
    if d % 2 == 0 and d >= 4:
        m = d//2
        fams['quadO'] = (frozenset({1, m+1}), 2,
            lambda m=m: poly_from_dict({d:1, m:rng.randrange(1,p), 0:rng.randrange(1,p)}, p))
    if d % 3 == 0 and d >= 6:
        m = d//3
        fams['cubicO'] = (frozenset({1, m+1, 2*m+1}), 3,
            lambda m=m: poly_from_dict({d:1, 2*m:rng.randrange(1,p), m:rng.randrange(1,p),
                                        0:rng.randrange(1,p)}, p))
    if d == 12:
        def exc():
            a = rng.randrange(1, p)
            c = pcompose(monoxp(3), poly_from_dict({4:1,1:a}, p), p)
            c[0] = rng.randrange(1, p)
            return c
        fams['exceptional'] = (frozenset({1,7,10}), 2, exc)
    if d == 4:
        fams['quartic'] = (frozenset({1,2,3}), 3,
            lambda: poly_from_dict({4:1, 2:rng.randrange(1,p), 1:rng.randrange(1,p),
                                    0:rng.randrange(1,p)}, p))
    return fams

def u_coords_mod_p(coeffs, d, S, p=P61):
    """F_i mod p at allowed indices for a family member (constant retained, centred in x)."""
    a = ptrim([c % p for c in coeffs])
    if not (pdeg(a) == d and a[d] == 1 and a[d-1] == 0):
        raise ValueError("family sampler did not return a monic centred polynomial")
    N = max(allowed_low_indices(d, S))
    F = inverse_series_F(a, N, p)
    return {i: F[i] % p for i in allowed_low_indices(d, S)}

def eval_gen_mod_p(gen_expr, syms, uvals, p=P61):
    pg = sp.Poly(gen_expr, *syms, domain='QQ')
    pg2, _den = pg.clear_denoms()
    tot = 0
    for mono, coeff in pg.terms():
        cnum, cden = sp.fraction(sp.Rational(coeff))
        c = (int(cnum) * pow(int(cden) % p, p-2, p)) % p
        term = c
        for e, s in zip(mono, syms):
            if e:
                term = (term * pow(uvals[s], e, p)) % p
        tot = (tot + term) % p
    return tot

def analyse(d, S, K1, K2, results):
    S = frozenset(S)
    case = {
        "degree": d,
        "support": sorted(S),
        "truncation": {"K1": K1, "K2": K2},
        "status": "started",
        "predicted_families": [],
        "predicted_dimension": None,
        "stability": None,
        "ideal_digest": None,
        "groebner_digest": None,
        "witness": None,
    }

    def finish(status, witness=None):
        case["status"] = status
        case["witness"] = witness
        results["records"].append(case)

    R, us, F, plist, conds = build_constrained(d, S, K2)
    # class-0 auto-check happens inside engine via assertion
    conds1 = [(n, g) for n, g in conds if n <= K1]
    condsH = [(n, g) for n, g in conds if n > K1]
    fams = fam_samplers(d)
    present = {name: v for name, v in fams.items() if v[0] <= S}
    pred_dim = max(v[1] for v in present.values())
    case["predicted_families"] = sorted(present)
    case["predicted_dimension"] = pred_dim
    nvars = len(S)
    idx_of_class = {(1-i) % d: i for i in allowed_low_indices(d, S)}
    status = []
    anomaly = False
    if not conds1 and not condsH:
        # vacuous: variety = full space
        if pred_dim == nvars:
            results['vacuous_ok'] += 1
            case["stability"] = True
            finish("vacuous-full-family", {"free_coordinates": nvars})
            return
        else:
            print(f"ANOMALY d={d} S={sorted(S)}: VACUOUS but predicted dim {pred_dim} < {nvars} "
                  f"-> variety larger than atlas!")
            results['anomalies'].append((d, sorted(S), 'vacuous-excess'))
            finish("anomaly", {"kind": "vacuous-excess", "free_coordinates": nvars})
            return
    exprs, syms = conds_to_exprs(conds1, R)
    case["ideal_digest"] = expression_digest(exprs)
    G = sp.groebner(exprs, *syms, order='lex', domain='QQ')
    case["groebner_digest"] = expression_digest(G.exprs)
    dim = staircase_dim(G, syms)
    # stability of high conditions
    stable = True
    for n, g in condsH:
        e = sp.Poly(g.as_expr(), *syms, domain='QQ')
        e = e.mul_ground(1/e.content()).as_expr()
        if sp.reduced(e, G)[1] != 0:
            stable = False
            print(f"NOTE d={d} S={sorted(S)}: condition at order {n} NOT in ideal of first {K1//d}d "
                  f"orders (variety shrinks with depth)")
            break
    if not stable:
        # recompute with all conditions
        exprs, syms = conds_to_exprs(conds, R)
        G = sp.groebner(exprs, *syms, order='lex', domain='QQ')
        case["ideal_digest"] = expression_digest(exprs)
        case["groebner_digest"] = expression_digest(G.exprs)
        dim = staircase_dim(G, syms)
    case["stability"] = stable
    case["computed_dimension"] = dim
    # dimension comparison
    if dim != pred_dim:
        print(f"ANOMALY d={d} S={sorted(S)}: GB dim {dim} != predicted {pred_dim}. GB="
              f"{[sp.factor(g) for g in G.exprs]}")
        results['anomalies'].append((d, sorted(S), f'dim {dim} vs {pred_dim}'))
        anomaly = True
    # containment sampling
    for name, (fsup, fdim, sampler) in present.items():
        for _ in range(3):
            c = sampler()
            uv = u_coords_mod_p(c, d, S)
            uvals = {sp.Symbol(f"u{i}"): v for i, v in uv.items()}
            for g in G.exprs:
                val = eval_gen_mod_p(g, syms, uvals)
                if val != 0:
                    print(f"ANOMALY d={d} S={sorted(S)}: family {name} member NOT in variety "
                          f"(gen value {val} mod p)")
                    results['anomalies'].append((d, sorted(S), f'containment {name}'))
                    anomaly = True
                    break
    # exactness certificate: variety subset of union of predicted components
    # component defining polys: plane families -> off-variable; exceptional -> quadric; power alone -> all non-ud vars
    witness = None
    if pred_dim == 1:
        # power only: every non-u_d variable must be in the radical
        cert = True
        powers = {}
        for i in allowed_low_indices(d, S):
            if i == d: continue
            v = sp.Symbol(f"u{i}")
            found = False
            for k in range(1, 25):
                if sp.reduced(v**k, G)[1] == 0:
                    found = True
                    powers[f"u{i}"] = k
                    break
            if not found:
                cert = False
                print(f"NO-CERT d={d} S={sorted(S)}: u{i} not shown nilpotent mod GB (k<=24). GB="
                      f"{[sp.factor(g) for g in G.exprs]}")
                results['nocert'].append((d, sorted(S), f'u{i}'))
        if cert:
            results['exact_poweronly'] += 1
            witness = {"kind": "power-only", "nilpotence_powers": powers}
    elif pred_dim == 2:
        prod = sp.Integer(1)
        for name, (fsup, fdim, sampler) in present.items():
            if fdim != 2: continue
            if name == 'exceptional':
                prod *= (sp.Symbol("u3")**2 + 2*sp.Symbol("u6"))
            else:
                off = S - fsup
                if len(off) != 1:
                    raise RuntimeError(
                        f"component {name} has {len(off)} off-support coordinates "
                        f"for d={d}, S={sorted(S)}"
                    )
                prod *= sp.Symbol(f"u{idx_of_class[next(iter(off))]}")
        found = False
        for k in range(1, 25):
            if sp.reduced(sp.expand(prod**k), G)[1] == 0:
                found = True; break
        if found:
            results['exact_union'] += 1
            witness = {"kind": "union", "product_power": k}
        else:
            print(f"NO-CERT d={d} S={sorted(S)}: product cert failed. GB="
                  f"{[sp.factor(g) for g in G.exprs]}")
            results['nocert'].append((d, sorted(S), 'union'))
    if not anomaly:
        results['ok'] += 1
    if anomaly:
        finish("anomaly", witness)
    elif any(item[0] == d and item[1] == sorted(S) for item in results['nocert']):
        finish("no-certificate", witness)
    else:
        finish("certified", witness)

def run(dmin, dmax):
    results = dict(ok=0, vacuous_ok=0, exact_poweronly=0, exact_union=0,
                   anomalies=[], nocert=[], records=[])
    t0 = time.time()
    for d in range(dmin, dmax+1):
        t1 = time.time()
        cases = 0
        classes = list(range(1, d))
        Ss = [frozenset({1})]
        Ss += [frozenset({1, r}) for r in classes if r != 1]
        Ss += [frozenset({1, r, s}) for r, s in itertools.combinations(classes, 2)
               if r != 1 and s != 1]
        for S in Ss:
            analyse(d, S, 4*d, 6*d, results)
            cases += 1
        print(f"degree {d}: {cases} support cases analysed in {time.time()-t1:.1f}s")
    print(f"\n=== SWEEP SUMMARY (degrees {dmin}..{dmax}, {time.time()-t0:.1f}s) ===")
    print(f"vacuous (variety = full space, matching saturating family): {results['vacuous_ok']}")
    print(f"exact power-only certificates: {results['exact_poweronly']}")
    print(f"exact union-of-predicted-components certificates: {results['exact_union']}")
    print(f"other OK: {results['ok'] - results['exact_poweronly'] - results['exact_union']}")
    print(f"anomalies: {len(results['anomalies'])}  {results['anomalies']}")
    print(f"no-certificate (needs manual review): {len(results['nocert'])}  {results['nocert']}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fail-closed exact atlas sweep")
    parser.add_argument("dmin", type=int, nargs="?", default=5)
    parser.add_argument("dmax", type=int, nargs="?", default=20)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument(
        "--self-test-failure",
        choices=("anomaly", "nocert"),
        help="inject a synthetic semantic failure and confirm a non-zero exit",
    )
    args = parser.parse_args()

    if args.self_test_failure:
        r = {"anomalies": [], "nocert": [], "records": [], "vacuous_ok": 0,
             "exact_poweronly": 0, "exact_union": 0}
        key = "anomalies" if args.self_test_failure == "anomaly" else "nocert"
        r[key].append((0, [], "synthetic-fail-closed-control"))
    else:
        r = run(args.dmin, args.dmax)
    bad = failure_count(r)
    receipt = {
        "schema": "cyclicity-atlas-case-records-v1",
        "range": [args.dmin, args.dmax],
        "software": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "summary": {
            "cases": len(r["records"]),
            "vacuous_full_family": r["vacuous_ok"],
            "exact_power_only": r["exact_poweronly"],
            "exact_union": r["exact_union"],
            "anomalies": len(r["anomalies"]),
            "no_certificate": len(r["nocert"]),
        },
        "records": r["records"],
    }
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        print(f"case_records={args.json_path}")
    print("\nBATTERY 4A:", "PASS" if bad == 0 else "REVIEW REQUIRED")
    raise SystemExit(0 if bad == 0 else 1)
