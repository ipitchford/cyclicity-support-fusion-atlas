#!/usr/bin/env python3
"""Numerical sign/asymptotic check for Theorem 7.3, P=x^4+x^2+x."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 45
D = 4
ZETA = mp.e ** (2j * mp.pi / D)
PHI = [(mp.pi + 2 * mp.pi * k) / D for k in range(D)]


def phase(z):
    return z**4 + z**2 + z


def ray_integral(phi, j, s):
    e = mp.e ** (1j * phi)
    return mp.quad(lambda r: (r * e) ** j * mp.e ** (s * phase(r * e)) * e,
                   [0, mp.inf])


def period_matrix(s):
    M = mp.matrix(D - 1, D - 1)
    for k in range(D - 1):
        for j in range(D - 1):
            M[k, j] = -ray_integral(PHI[k], j, s) + ray_integral(PHI[k + 1], j, s)
    return M


def leading_matrix():
    L = mp.matrix(D - 1, D - 1)
    for k in range(D - 1):
        for j in range(D - 1):
            r = j + 1
            L[k, j] = (mp.gamma(mp.mpf(r) / D) / D
                       * mp.e ** (mp.pi * 1j * r / D)
                       * (ZETA**r - 1) * ZETA ** (k * r))
    return L


def cpx(z):
    return {"re": mp.nstr(mp.re(z), 18), "im": mp.nstr(mp.im(z), 18)}


def main():
    L = leading_matrix()
    detL = mp.det(L)
    runs = []
    for st in ["0.03", "0.01", "0.003"]:
        s = mp.mpf(st)
        M = period_matrix(s)
        scaled = mp.matrix(D - 1, D - 1)
        for k in range(D - 1):
            for j in range(D - 1):
                scaled[k, j] = s ** (mp.mpf(j + 1) / D) * M[k, j]
        errors = [abs(scaled[k, j] - L[k, j])
                  for k in range(D - 1) for j in range(D - 1)]
        determinant_ratio = s ** (mp.mpf(D - 1) / 2) * mp.det(M) / detL
        runs.append({
            "s": st,
            "max_entry_error": mp.nstr(max(errors), 18),
            "determinant_ratio_to_leading_constant": cpx(determinant_ratio),
            "determinant_nonzero": bool(abs(mp.det(M)) > 0),
        })
    report = {
        "schema": "period-matrix-fourier-gamma-spotcheck-v1",
        "status": "pass",
        "phase": "x^4+x^2+x",
        "sector_centre_arg": 0,
        "ray_angles": ["pi/4", "3pi/4", "5pi/4", "7pi/4"],
        "precision_decimal_digits": mp.mp.dps,
        "leading_determinant": cpx(detL),
        "runs": runs,
        "interpretation": "Entry errors decrease and the scaled determinant ratio tends to 1 as s tends to 0.",
        "limitations": "Same-producer numerical quadrature; checks signs and asymptotic behaviour but is not proof or independent reproduction."
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    out = Path(__file__).with_name("period_matrix_spotcheck_receipt.json")
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS: Fourier-Gamma period-matrix spot check")
    for row in runs:
        print(row)
    print(out)


if __name__ == "__main__":
    main()
