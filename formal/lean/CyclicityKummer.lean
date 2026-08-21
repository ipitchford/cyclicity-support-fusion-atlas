import Mathlib

/-!
# Algebraic checks for the all-m Kummer-line normalizer lemma

This file checks the characteristic-polynomial coefficient identities and the
two spectral obstructions used in the standalone proof.  It does not formalise
Kummer theory, divisor valuations, line imprimitivity, or the S4 normalizer.
-/

namespace CyclicityKummer

section CharacteristicPolynomials

variable {K : Type*} [Field K]

/-- Characteristic polynomial of a monomial transposition block. -/
theorem transposition_characteristic_identity (X a q : K) :
    (X - a) * (X ^ 2 - q) =
      X ^ 3 - a * X ^ 2 - q * X + a * q := by
  ring

/-- Characteristic polynomial of the target spectrum zeta, 1, 1. -/
theorem kummer_reflection_characteristic_identity (X z : K) :
    (X - z) * (X - 1) ^ 2 =
      X ^ 3 - (z + 2) * X ^ 2 + (2 * z + 1) * X - z := by
  ring

variable [CharZero K]

/-- Matching a transposition monomial spectrum to (zeta,1,1) forces zeta=-1. -/
theorem transposition_coefficients_force_neg_one (z a q : K)
    (ha : a = z + 2) (hq : -q = 2 * z + 1) (hc : a * q = -z) :
    z = -1 := by
  have hq' : q = -(2 * z + 1) := by
    linear_combination -hq
  rw [ha, hq'] at hc
  have hs : (2 : K) * (z + 1) ^ 2 = 0 := by
    linear_combination -hc
  have htwo : (2 : K) ≠ 0 := by norm_num
  have hzsq : (z + 1) ^ 2 = 0 := (mul_eq_zero.mp hs).resolve_left htwo
  have hz : z + 1 = 0 := by
    by_contra hne
    exact (pow_ne_zero 2 hne) hzsq
  exact eq_neg_of_add_eq_zero_left hz

/-- A three-cycle monomial cannot have target spectrum (zeta,1,1). -/
theorem three_cycle_coefficients_impossible (z : K)
    (hquad : z + 2 = 0) (hlinear : 2 * z + 1 = 0) :
    False := by
  have hthree : (3 : K) = 0 := by
    linear_combination 2 * hquad - hlinear
  norm_num at hthree

/-- Thus a non-minus-one Kummer reflection cannot permute a competing
three-line system by a nontrivial permutation. -/
theorem nontrivial_line_permutation_obstructed (z : K) (hz : z ≠ -1) :
    (∀ a q : K, ¬ (a = z + 2 ∧ -q = 2 * z + 1 ∧ a * q = -z)) ∧
      ¬ (z + 2 = 0 ∧ 2 * z + 1 = 0) := by
  constructor
  . intro a q h
    exact hz (transposition_coefficients_force_neg_one z a q h.1 h.2.1 h.2.2)
  . intro h
    exact three_cycle_coefficients_impossible z h.1 h.2

end CharacteristicPolynomials

end CyclicityKummer
