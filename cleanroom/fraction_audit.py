#!/usr/bin/env python3
"""Clean-room exact audit for support/rank and low-rank Ritt claims.

Imports neither src/fusion_support.py nor a computer-algebra package.
Polynomial and matrix arithmetic use fractions.Fraction only.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import gcd
import hashlib
import json
import random
from pathlib import Path
from typing import Iterable, List, Dict, Tuple

Q = Fraction
Poly = List[Q]  # ascending coefficients


def trim(a: Poly) -> Poly:
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    out = [Q(0) for _ in range(n)]
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return trim(out)


def scale(a: Poly, c: Q) -> Poly:
    return trim([c * x for x in a])


def mul(a: Poly, b: Poly) -> Poly:
    out = [Q(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if y:
                out[i + j] += x * y
    return trim(out)


def pow_poly(a: Poly, n: int) -> Poly:
    out: Poly = [Q(1)]
    base = a
    while n:
        if n & 1:
            out = mul(out, base)
        n >>= 1
        if n:
            base = mul(base, base)
    return out


def derivative(a: Poly) -> Poly:
    return trim([Q(i) * a[i] for i in range(1, len(a))]) if len(a) > 1 else [Q(0)]


def compose(a: Poly, b: Poly) -> Poly:
    out: Poly = [Q(0)]
    for c in reversed(a):
        out = add(mul(out, b), [c])
    return trim(out)


def monic(a: Poly) -> Poly:
    a = trim(a)
    return scale(a, Q(1) / a[-1])


def sparse(items: Dict[int, int | Q]) -> Poly:
    out = [Q(0) for _ in range(max(items, default=0) + 1)]
    for k, v in items.items():
        out[k] = Q(v)
    return trim(out)


def chebyshev(n: int) -> Poly:
    x = [Q(0), Q(1)]
    if n == 0:
        return [Q(1)]
    if n == 1:
        return x
    t0, t1 = [Q(1)], x
    for _ in range(2, n + 1):
        t0, t1 = t1, add(scale(mul(x, t1), Q(2)), scale(t0, Q(-1)))
    return t1


def reduce_twisted(f: Poly, p: Poly, s: Q) -> Poly:
    """Reduce f modulo D_s(q)=q'+s p' q for monic p."""
    p = monic(p)
    d = len(p) - 1
    dp = derivative(p)
    f = trim(f)
    while len(f) - 1 >= d - 1:
        N = len(f) - 1
        c = f[N]
        k = N - d + 1
        factor = c / (s * d)
        if k > 0:
            while len(f) <= k - 1:
                f.append(Q(0))
            f[k - 1] -= factor * k
        for j, coeff in enumerate(dp):
            idx = k + j
            while len(f) <= idx:
                f.append(Q(0))
            f[idx] -= factor * s * coeff
        f = trim(f)
    f += [Q(0)] * max(0, d - 1 - len(f))
    return f[: d - 1]


def rank_matrix(rows: List[List[Q]]) -> int:
    if not rows:
        return 0
    a = [list(r) for r in rows]
    m, n = len(a), len(a[0])
    rank = col = 0
    while rank < m and col < n:
        pivot = next((i for i in range(rank, m) if a[i][col]), None)
        if pivot is None:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pv = a[rank][col]
        a[rank] = [x / pv for x in a[rank]]
        for i in range(m):
            if i != rank and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[rank])]
        rank += 1
        col += 1
    return rank


def cyclic_rank_at_s(p: Poly, s: Q) -> int:
    p = monic(p)
    d = len(p) - 1
    powers: List[Poly] = [[Q(1)]]
    for _ in range(1, d - 1):
        powers.append(mul(powers[-1], p))
    cols = [reduce_twisted(f, p, s) for f in powers]
    rows = [[cols[j][i] for j in range(d - 1)] for i in range(d - 1)]
    return rank_matrix(rows)


def sampled_cyclic_rank(p: Poly) -> Tuple[int, Dict[str, int]]:
    samples = [Q(1), Q(2), Q(3), Q(5)]
    ranks = {str(s): cyclic_rank_at_s(p, s) for s in samples}
    return max(ranks.values()), ranks


def series_mul(a: List[Q], b: List[Q], N: int) -> List[Q]:
    out = [Q(0) for _ in range(N + 1)]
    for i, x in enumerate(a[: N + 1]):
        if not x:
            continue
        for j, y in enumerate(b[: N - i + 1]):
            if y:
                out[i + j] += x * y
    return out


def series_pow(a: List[Q], n: int, N: int) -> List[Q]:
    out = [Q(0)] * (N + 1)
    out[0] = Q(1)
    base = list(a)
    while n:
        if n & 1:
            out = series_mul(out, base, N)
        n >>= 1
        if n:
            base = series_mul(base, base, N)
    return out


def inverse_coefficients(p: Poly, N: int) -> List[Q]:
    """c_n in xi=t*(1+sum c_n t^-n), through n=N."""
    p = monic(p)
    d = len(p) - 1
    if p[d - 1] != 0:
        raise ValueError("input must be centred")
    c = [Q(0)] * (N + 1)
    c[0] = Q(1)
    for n in range(1, N + 1):
        lhs = series_pow(c, d, n)[n]
        for j in range(d - 1):
            shift = d - j
            if shift <= n and p[j]:
                lhs += p[j] * series_pow(c, j, n - shift)[n - shift]
        c[n] = -lhs / d
    return c


def inverse_support(p: Poly, N_factor: int = 8) -> Tuple[List[int], Dict[int, Tuple[int, Q]]]:
    p = monic(p)
    d = len(p) - 1
    coeffs = inverse_coefficients(p, N_factor * d)
    witnesses: Dict[int, Tuple[int, Q]] = {1 % d: (0, Q(1))}
    for n, cn in enumerate(coeffs[1:], start=1):
        if cn:
            witnesses.setdefault((1 - n) % d, (n, cn))
    return sorted(witnesses), witnesses


def qproj(S: Iterable[int], m: int) -> int:
    return len({x % m for x in S})


def check_case(name: str, p: Poly, expected: int | None = None) -> Dict[str, object]:
    p = monic(p)
    d = len(p) - 1
    if p[d - 1] != 0:
        raise AssertionError(f"{name}: not centred")
    q, samples = sampled_cyclic_rank(p)
    support, witnesses = inverse_support(p)
    if q != len(support):
        raise AssertionError(f"{name}: sampled q={q}, support={support}")
    if expected is not None and q != expected:
        raise AssertionError(f"{name}: expected {expected}, got {q}")
    return {
        "name": name,
        "degree": d,
        "sampled_q": q,
        "sample_ranks": samples,
        "support": support,
        "support_witness_n": {str(r): witnesses[r][0] for r in support},
    }


def named_cases() -> List[Dict[str, object]]:
    x3px = sparse({3: 1, 1: 1})
    x4px = sparse({4: 1, 1: 1})
    cases = [
        ("power_7", sparse({7: 1}), 1),
        ("chebyshev_7", chebyshev(7), 2),
        ("quadratic_over_power", sparse({6: 1, 3: 1}), 2),
        ("cubic_over_power", sparse({9: 1, 6: 1, 3: 1}), 3),
        ("aligned_rank_two", pow_poly(x3px, 2), 2),
        ("quartic_cubic_ritt", pow_poly(x4px, 3), 3),
        ("canonical_partial_fusion", sparse({8: 1, 4: 1}), 2),
        ("rank_four_negative", add(pow_poly(x3px, 2), x3px), 4),
        ("generic_even_sextic_rank3", sparse({6: 1, 2: 1}), 3),
    ]
    return [check_case(*case) for case in cases]


def random_cases() -> List[Dict[str, object]]:
    rng = random.Random(20260819)
    out = []
    for d in range(3, 9):
        for k in range(2):
            p = [Q(rng.randint(-3, 3)) for _ in range(d + 1)]
            p[d] = Q(1)
            p[d - 1] = Q(0)
            if all(c == 0 for c in p[1:d - 1]):
                p[1] = Q(1)
            out.append(check_case(f"random_d{d}_{k}", p))
    return out


def composition_projection_cases() -> List[Dict[str, object]]:
    pairs = [
        (sparse({2: 1, 1: 1}), sparse({3: 1}), "(y2+y)o x3"),
        (sparse({3: 1}), sparse({4: 1, 1: 1}), "y3 o (x4+x)"),
        (sparse({2: 1}), sparse({3: 1, 1: 1}), "y2 o (x3+x)"),
        (sparse({3: 1, 1: 1}), sparse({2: 1}), "(y3+y)o x2"),
    ]
    out = []
    for r, qpoly, name in pairs:
        p = compose(r, qpoly)
        q_rank, _ = sampled_cyclic_rank(qpoly)
        p_rank, _ = sampled_cyclic_rank(p)
        p_support, _ = inverse_support(p)
        m = len(qpoly) - 1
        projected = sorted({x % m for x in p_support})
        if len(projected) != q_rank:
            raise AssertionError((name, p_support, projected, q_rank))
        out.append({
            "name": name,
            "degree_P": len(p) - 1,
            "degree_Q": m,
            "q_P": p_rank,
            "q_Q": q_rank,
            "support_P": p_support,
            "projected_support_mod_Q_degree": projected,
        })
    return out


def ritt_diamond_types() -> Dict[str, object]:
    observed = {}
    for a, b in [(2, 3), (2, 5), (3, 4), (3, 5)]:
        if gcd(a, b) != 1:
            continue
        for h in range(1, 4):
            N = a * b * h
            for size in range(1, 4):
                for S in combinations(range(N), size):
                    q0 = qproj(S, h)
                    qa = qproj(S, a * h)
                    qb = qproj(S, b * h)
                    q2 = size
                    key = (q2, q0, tuple(sorted((qa, qb))))
                    observed.setdefault(key, {"a": a, "b": b, "h": h, "S": list(S), "oriented": [qa, qb]})
                    # Exact CRT fibre-product check.
                    for c in {u % h for u in S}:
                        Sc = [u for u in S if u % h == c]
                        ac = len({u % (a * h) for u in Sc})
                        bc = len({u % (b * h) for u in Sc})
                        if len(Sc) > ac * bc:
                            raise AssertionError("Ritt fibre-product bound failed")
    expected = {
        (1, 1, (1, 1)),
        (2, 1, (1, 2)),
        (2, 1, (2, 2)),
        (2, 2, (2, 2)),
        (3, 1, (1, 3)),
        (3, 1, (2, 2)),
        (3, 1, (2, 3)),
        (3, 1, (3, 3)),
        (3, 2, (2, 3)),
        (3, 2, (3, 3)),
        (3, 3, (3, 3)),
    }
    if set(observed) != expected:
        raise AssertionError({"missing": sorted(expected - set(observed)), "extra": sorted(set(observed) - expected)})
    serial = []
    for key in sorted(observed):
        q2, q0, mids = key
        serial.append({"top": q2, "bottom": q0, "intermediate_unordered": list(mids), "example": observed[key]})
    return {"count": len(serial), "types": serial}


def main() -> None:
    report = {
        "schema": "cyclicity-cleanroom-fraction-audit-v1",
        "status": "pass",
        "independence": "No import from the production module and no computer-algebra library; exact Fraction arithmetic only.",
        "limitations": [
            "The cyclic rank is sampled at four rational nonzero s-values and the maximum is taken; this is a fault control, not a symbolic proof over Q(s).",
            "Inverse support is expanded through 8d coefficients; theorem proofs, not finite truncation, establish exhaustiveness.",
            "Random cases are deterministic and producer-run, not external reproduction.",
        ],
        "named_cases": named_cases(),
        "random_cases": random_cases(),
        "composition_projection_cases": composition_projection_cases(),
        "ritt_diamond": ritt_diamond_types(),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["report_sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    out = Path(__file__).with_name("fraction_audit_receipt.json")
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(report['named_cases'])} named, {len(report['random_cases'])} random, "
          f"{len(report['composition_projection_cases'])} composition cases; "
          f"{report['ritt_diamond']['count']} Ritt diamond types")
    print(out)


if __name__ == "__main__":
    main()
