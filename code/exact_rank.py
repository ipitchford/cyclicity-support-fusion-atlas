#!/usr/bin/env python3
"""Exact fixed-seed cyclic rank over Q(s) for trusted Q[x] input."""
from __future__ import annotations
import sympy as sp
x, s = sp.symbols('x s')
K = sp.QQ.frac_field(s)

def reduce_twisted(polynomial: sp.Poly, phase: sp.Poly) -> sp.Poly:
    phase_k = sp.Poly(phase.as_expr(), x, domain=K)
    derivative = phase_k.diff()
    d = phase.degree()
    leading = derivative.LC()
    lower = derivative - sp.Poly(leading*x**(d-1), x, domain=K)
    reduced = sp.Poly(polynomial.as_expr(), x, domain=K)
    while not reduced.is_zero and reduced.degree() >= d-1:
        degree = reduced.degree()
        coefficient = reduced.LC()
        shift = degree-(d-1)
        derivative_term = shift*x**(shift-1) if shift else sp.S.Zero
        tail = sp.Poly(derivative_term+s*x**shift*lower.as_expr(), x, domain=K)
        reduced = (reduced-sp.Poly(coefficient*x**degree,x,domain=K)
                   +tail.mul_ground(-coefficient/(s*leading)))
    return reduced

def column(poly: sp.Poly, phase: sp.Poly) -> sp.Matrix:
    d=phase.degree()
    r=reduce_twisted(poly,phase)
    return sp.Matrix([sp.cancel(r.nth(i)) for i in range(d-1)])

def cyclic_rank(expr: sp.Expr) -> int:
    phase=sp.Poly(sp.expand(expr),x,domain=sp.QQ)
    d=phase.degree()
    phase_k=sp.Poly(phase.as_expr(),x,domain=K)
    iterate=sp.Poly(1,x,domain=K)
    cols=[]
    for count in range(1,d):
        cols.append(column(iterate,phase))
        M=sp.Matrix.hstack(*cols)
        if M.rank()<count:
            return count-1
        iterate*=phase_k
    return d-1
