#!/usr/bin/env python3
"""Regression controls for cross-environment semantic receipt identity."""

from battery4a_fast import software_identity


def main():
    reviewed = software_identity((3, 14, 6), "1.14.0")
    runner = software_identity((3, 14, 7), "1.14.0")
    next_series = software_identity((3, 15, 0), "1.14.0")
    next_sympy = software_identity((3, 14, 7), "1.15.0")

    assert reviewed == runner, "Python patch releases must share receipt identity"
    assert reviewed != next_series, "Python minor-series changes must remain visible"
    assert reviewed != next_sympy, "SymPy version changes must remain visible"
    assert reviewed == {"python_series": "3.14", "sympy": "1.14.0"}
    print("receipt portability controls: PASS")


if __name__ == "__main__":
    main()
