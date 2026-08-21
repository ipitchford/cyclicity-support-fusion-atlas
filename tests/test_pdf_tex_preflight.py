#!/usr/bin/env python3
"""Regression tests for the release-blocking PDF raw-TeX detector."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pdf_tex_preflight import find_raw_tex  # noqa: E402


class PdfTexPreflightTests(unittest.TestCase):
    def test_rendered_mathematics_is_accepted(self) -> None:
        self.assertEqual(find_raw_tex("α γ = β δ = 0 and dim W = |Σ(P)|"), [])

    def test_fraction_and_tag_leak_is_rejected(self) -> None:
        findings = find_raw_tex(r"U=\frac1m\sum_j x_j. \tag{7.4}")
        self.assertEqual(len(findings), 1)
        self.assertIn(r"\frac", findings[0]["tokens"])
        self.assertIn(r"\sum", findings[0]["tokens"])
        self.assertIn(r"\tag", findings[0]["tokens"])

    def test_environment_and_proof_end_leak_is_rejected(self) -> None:
        findings = find_raw_tex(r"\begin{array} x & y \end{array} \square")
        self.assertEqual(len(findings), 1)
        self.assertIn(r"\begin", findings[0]["tokens"])
        self.assertIn(r"\end", findings[0]["tokens"])
        self.assertIn(r"\square", findings[0]["tokens"])

    def test_display_delimiters_are_rejected(self) -> None:
        self.assertEqual(len(find_raw_tex(r"\[x^2+y^2\]")), 1)


if __name__ == "__main__":
    unittest.main()
