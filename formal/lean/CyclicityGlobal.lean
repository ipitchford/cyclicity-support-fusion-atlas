import Mathlib

/-!
# Kernel checks for the global low-rank completion

This additive file formalises the elementary algebra used at four interfaces:

* an infinity-order bound below one forces polynomial constancy;
* an endomorphism fixing a spanning family is the identity;
* the scalar equations in the cubic and quartic extension cases have exactly
  the asserted solutions; and
* the two exceptional primitive character restrictions have multiplicity zero.

It does not formalise Laurent-series inversion, algebraic function fields,
polynomial monodromy, the classification of primitive polynomial groups, or
the finite-subgroup classifications of `PGL₂` and `PGL₃`.  Those remain
explicit imported hypotheses in the accompanying proof and source audit.
-/

namespace CyclicityGlobal

set_option maxHeartbeats 1000000

section PoleOrder

/-- The integer part of a proper nonnegative fraction is zero.  This is the
arithmetic step turning an infinity bound `k/n < 1` into constancy. -/
theorem lower_coefficient_floor_zero (k n : ℕ) (hkn : k < n) :
    k / n = 0 := by
  exact Nat.div_eq_of_lt hkn

/-- The top elementary coefficient is allowed degree one at infinity. -/
theorem top_coefficient_floor_one (n : ℕ) (hn : 0 < n) :
    n / n = 1 := by
  exact Nat.div_self hn

/-- A polynomial whose natural degree is strictly below one is constant. -/
theorem polynomial_constant_of_natDegree_lt_one {K : Type*} [Semiring K]
    (p : Polynomial K) (h : p.natDegree < 1) :
    p = Polynomial.C (p.coeff 0) := by
  apply Polynomial.eq_C_of_natDegree_eq_zero
  omega

end PoleOrder

section FullBlockKernel

variable {K V ι : Type*} [Semiring K] [AddCommMonoid V] [Module K V]

/-- Fixing a spanning family pointwise forces a linear endomorphism to be the
identity.  This is the linear-algebraic core of the full-block kernel lemma. -/
theorem fixed_spanning_family_is_identity (T : V →ₗ[K] V) (v : ι → V)
    (hspan : Submodule.span K (Set.range v) = ⊤)
    (hfix : ∀ i, T (v i) = v i) :
    T = LinearMap.id := by
  apply LinearMap.ext_on_range hspan
  intro i
  simpa using hfix i

/-- A purported nonidentity block-kernel element cannot fix a full-span
block pointwise. -/
theorem partial_support_kernel_impossible (T : V →ₗ[K] V) (v : ι → V)
    (hspan : Submodule.span K (Set.range v) = ⊤)
    (hfix : ∀ i, T (v i) = v i) (hne : T ≠ LinearMap.id) :
    False := by
  exact hne (fixed_spanning_family_is_identity T v hspan hfix)

end FullBlockKernel

section ScalarExtensions

variable {K : Type*} [Field K]

/-- If the quadratic coefficient of the cubic is nonzero, its scalar fibre
symmetry is trivial. -/
theorem cubic_scalar_trivial_of_A_ne_zero (A c : K) (hA : A ≠ 0)
    (hcA : c * A = A) :
    c = 1 := by
  apply (mul_right_cancel₀ hA)
  simpa using hcA

/-- On the odd-centred cubic locus, the only scalar fibre symmetries are
`1` and `-1`. -/
theorem cubic_scalar_one_or_neg_one (B c : K) (hB : B ≠ 0)
    (hcB : c ^ 2 * B = B) :
    c = 1 ∨ c = -1 := by
  have hc2 : c ^ 2 = 1 := by
    apply (mul_right_cancel₀ hB)
    simpa using hcB
  have hfactor : (c - 1) * (c + 1) = 0 := by
    calc
      (c - 1) * (c + 1) = c ^ 2 - 1 := by ring
      _ = 0 := by rw [hc2]; ring
  rcases mul_eq_zero.mp hfactor with h | h
  · exact Or.inl (sub_eq_zero.mp h)
  · exact Or.inr (eq_neg_of_add_eq_zero_left h)

/-- A nonzero quadratic coefficient prevents the odd cubic involution from
reappearing after the aligned-square extension. -/
theorem aligned_square_cubic_no_repeat (b c : K) (hb : b ≠ 0)
    (hcoeff : c * (2 * b) = 2 * b) (hchar : (2 : K) ≠ 0) :
    c = 1 := by
  apply cubic_scalar_trivial_of_A_ne_zero (2 * b) c (mul_ne_zero hchar hb)
  exact hcoeff

/-- A nonzero quartic linear coefficient converts scalar semiequivariance
into the cubic root-of-unity condition. -/
theorem quartic_scalar_cube_one (B c : K) (hB : B ≠ 0)
    (hcB : c ^ 3 * B = B) :
    c ^ 3 = 1 := by
  apply (mul_right_cancel₀ hB)
  simpa using hcB

/-- If both the quadratic and linear coefficients of the quartic are
nonzero, the simultaneous square/cube scalar conditions are trivial. -/
theorem quartic_scalar_trivial_of_A_ne_zero (A B c : K)
    (hA : A ≠ 0) (hB : B ≠ 0)
    (hcA : c ^ 2 * A = A) (hcB : c ^ 3 * B = B) :
    c = 1 := by
  have hc2 : c ^ 2 = 1 := by
    apply (mul_right_cancel₀ hA)
    simpa using hcA
  have hc3 : c ^ 3 = 1 := quartic_scalar_cube_one B c hB hcB
  calc
    c = c ^ 3 / c ^ 2 := by
      field_simp
    _ = 1 := by rw [hc2, hc3]; simp

/-- Equality of the degree-12 collision multipliers at exponents twelve and
nine already forces the deck condition `c³ = 1`. -/
theorem collision_equal_multipliers_force_cube_one (c : K) (hc : c ≠ 0)
    (h : c ^ 12 = c ^ 9) :
    c ^ 3 = 1 := by
  have hc9 : c ^ 9 ≠ 0 := pow_ne_zero 9 hc
  apply (mul_right_cancel₀ hc9)
  calc
    c ^ 3 * c ^ 9 = c ^ 12 := by ring
    _ = c ^ 9 := h
    _ = 1 * c ^ 9 := by simp

/-- Once `c³ = 1`, every nonzero exponent in the collision polynomial has
multiplier one. -/
theorem collision_deck_multiplier_one (c : K) (hc3 : c ^ 3 = 1) :
    c ^ 12 = 1 ∧ c ^ 9 = 1 ∧ c ^ 6 = 1 ∧ c ^ 3 = 1 := by
  constructor
  · calc c ^ 12 = (c ^ 3) ^ 4 := by ring
         _ = 1 := by rw [hc3]; simp
  constructor
  · calc c ^ 9 = (c ^ 3) ^ 3 := by ring
         _ = 1 := by rw [hc3]; simp
  constructor
  · calc c ^ 6 = (c ^ 3) ^ 2 := by ring
         _ = 1 := by rw [hc3]; simp
  · exact hc3

end ScalarExtensions

section PrimitiveCharacters

/-- Restriction of the three-dimensional `A₅` character to the point
stabiliser `A₄` has no trivial constituent. -/
theorem a5_a4_trivial_multiplicity_numerator_zero :
    (3 + 3 * (-1) + 8 * 0 : ℤ) = 0 := by
  norm_num

/-- The two nontrivial linear characters of `A₄` give the same numerator
because the three-cycle character value is zero. -/
theorem a5_a4_nontrivial_linear_numerator_zero :
    (3 + 3 * (-1) + 8 * 0 : ℤ) = 0 := by
  norm_num

/-- Restriction of the Klein three-dimensional `PSL₃(2)` character to its
point stabiliser `S₄` has no trivial constituent. -/
theorem psl3_2_s4_trivial_multiplicity_numerator_zero :
    (3 + 9 * (-1) + 8 * 0 + 6 * 1 : ℤ) = 0 := by
  norm_num

/-- The sign-twisted point-stabiliser multiplicity also vanishes. -/
theorem psl3_2_s4_sign_multiplicity_numerator_zero :
    (3 + 6 - 3 - 6 : ℤ) = 0 := by
  norm_num

end PrimitiveCharacters

end CyclicityGlobal
