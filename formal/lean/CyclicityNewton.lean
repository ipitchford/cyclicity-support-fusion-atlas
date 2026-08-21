import Mathlib

/-!
# Kernel checks for the Newton-descent boundary identities

This file formalises the polynomial identities and exceptional coefficient
obstructions used in Sections 4 and 5 of `ALL_DEGREE_NEWTON_DESCENT.md`.

It intentionally does not formalise the monodromy/scaling lemma, the
finite-pole argument, or the uniform coefficient-extraction argument.  A
successful kernel check therefore strengthens the local algebraic interface;
it is not a formal proof of the all-degree theorem.
-/

namespace CyclicityNewton

section RootMaps

variable {R : Type*} [CommRing R]

/-- Equation (4.3): a root of the trace-normalised cubic maps, on squaring,
to a root of the claimed powered-root polynomial. -/
theorem cubic_powered_root (x a e : R)
    (h : x ^ 3 + a * x + e = 0) :
    x ^ 2 * (x ^ 2 + a) ^ 2 - e ^ 2 = 0 := by
  calc
    x ^ 2 * (x ^ 2 + a) ^ 2 - e ^ 2 =
        (x ^ 3 + a * x - e) * (x ^ 3 + a * x + e) := by ring
    _ = 0 := by rw [h, mul_zero]

/-- Equation (5.4): after imposing `a = 0`, a root of the quartic maps, on
cubing, to a root of `Y (Y+c)^3 + e^3`. -/
theorem quartic_powered_root (x c e : R)
    (h : x ^ 4 + c * x + e = 0) :
    x ^ 3 * (x ^ 3 + c) ^ 3 + e ^ 3 = 0 := by
  have h' : x ^ 4 + c * x = -e := by
    linear_combination h
  calc
    x ^ 3 * (x ^ 3 + c) ^ 3 + e ^ 3 =
        (x ^ 4 + c * x) ^ 3 + e ^ 3 := by ring
    _ = 0 := by rw [h']; ring

end RootMaps

section Obstructions

/-! The following statements make “independent of `e`” exact: a displayed
derivative polynomial is assumed to vanish for every rational `e`.  The
conclusions reproduce the eliminations in equations (4.2) and (5.3). -/

/-- The cubic `m = 4` derivative `8*a*e` cannot vanish identically when
`a != 0`. -/
theorem cubic_m4_forces_power (a : ℚ)
    (h : ∀ e : ℚ, 8 * a * e = 0) : a = 0 := by
  have h1 := h 1
  norm_num at h1 ⊢
  exact h1

/-- The quartic `m = 2` derivative is the nonzero constant `2`. -/
theorem quartic_m2_obstruction : ¬(∀ _e : ℚ, (2 : ℚ) = 0) := by
  intro h
  have h0 := h 0
  norm_num at h0

/-- At quartic `m = 3`, constancy forces the exceptional locus `a = 0`. -/
theorem quartic_m3_forces_a_zero (a : ℚ)
    (h : ∀ _e : ℚ, -3 * a = 0) : a = 0 := by
  have h0 := h 0
  linarith

/-- At quartic `m = 5`, identically vanishing
`-5*(a^3 - 2*a*e - c^2)` forces `c = 0`, contradicting the primitive
quartic hypothesis. -/
theorem quartic_m5_forces_degenerate (a c : ℚ)
    (h : ∀ e : ℚ, -5 * (a ^ 3 - 2 * a * e - c ^ 2) = 0) : c = 0 := by
  have h0 := h 0
  have h1 := h 1
  norm_num at h0 h1
  have ha : a = 0 := by linarith
  rw [ha] at h0
  norm_num at h0
  exact h0

/-- The quartic `m = 6`, `a = 0` derivative `6*e^2` is not identically
zero. -/
theorem quartic_m6_obstruction : ¬(∀ e : ℚ, 6 * e ^ 2 = 0) := by
  intro h
  have h1 := h 1
  norm_num at h1

/-- The quartic `m = 9`, `a = 0` derivative `54*c^2*e^2` cannot vanish
identically unless the quartic degenerates (`c = 0`). -/
theorem quartic_m9_forces_degenerate (c : ℚ)
    (h : ∀ e : ℚ, 54 * c ^ 2 * e ^ 2 = 0) : c = 0 := by
  have h1 := h 1
  norm_num at h1
  exact h1

end Obstructions

section DisplayedCoefficientIdentities

/-- Cubic `m = 2`: the first two Newton elementary-symmetric expressions
reduce to `-2a` and `a^2`. -/
theorem cubic_m2_elementary (a : ℚ) :
    ((-2 * a : ℚ) ^ 2 - 2 * a ^ 2) / 2 = a ^ 2 := by
  ring

/-- Quartic `m = 3`, `a = 0`: the second displayed elementary-symmetric
expression reduces to `3c^2`. -/
theorem quartic_m3_second_elementary (c : ℚ) :
    ((-3 * c : ℚ) ^ 2 - 3 * c ^ 2) / 2 = 3 * c ^ 2 := by
  ring

/-- Quartic `m = 3`, `a = 0`: the third displayed elementary-symmetric
expression reduces to `-c^3`. -/
theorem quartic_m3_third_elementary (c : ℚ) :
    ((-3 * c : ℚ) ^ 3 - 3 * (-3 * c) * (3 * c ^ 2) +
      2 * (-3 * c ^ 3)) / 6 = -c ^ 3 := by
  ring

end DisplayedCoefficientIdentities

end CyclicityNewton
