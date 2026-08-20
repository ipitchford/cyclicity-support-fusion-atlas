#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json, hashlib
from pathlib import Path
import sympy as sp
from exact_rank import x, cyclic_rank

def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def check(name, expr, expected):
    rank=cyclic_rank(sp.expand(expr))
    if rank!=expected:
        raise RuntimeError(f'{name}: expected {expected}, got {rank}')
    return {'name':name,'phase':sp.sstr(sp.expand(expr)),'degree':int(sp.degree(expr,x)),'rank':int(rank)}

checks=[
    check('power_9',x**9,1),
    check('dickson_5',x**5-5*x**3+5*x,2),
    check('quadratic_over_power_m4',(x**4+1)**2,2),
    check('generic_cubic_over_power_m3',x**9+2*x**6+3*x**3,3),
    check('dickson_sextic_lower_locus',x**6-6*x**4+9*x**2,2),
    check('quartic_generic',x**4+x**2+x,3),
    check('quartic_collision',(x**4+x)**3,3),
    check('rank3_square_m2',(x**6+x**2)**2,3),
    check('rank3_square_m3',(x**9+x**3)**2,3),
    check('square_alignment_mutation',(x**6+x**4+x**2)**2,6),
    check('quartic_pullback_m2_generic',x**8+x**4+x**2,4),
    check('quartic_collision_extra_power',(x**8+x**2)**3,4),
]
receipt={'schema':'coefficient-atlas-exact-rank-v1','status':'pass','method':'exact twisted-de-Rham Krylov rank over Q(s)','checks':checks}
receipt['sha256']=sha(receipt)
parser=argparse.ArgumentParser(description='Exact low-rank atlas controls')
parser.add_argument('--output', type=Path)
args=parser.parse_args()
out=args.output or (Path(__file__).resolve().parents[1]/'receipts'/'exact_rank_receipt.json')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
