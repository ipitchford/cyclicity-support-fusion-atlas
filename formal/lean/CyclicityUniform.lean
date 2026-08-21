import Mathlib

/-!
# Structural kernel checks for the all-degree Newton descent

This additive successor checks two previously unformalised interfaces:

1. the projective-permutation argument that removes root-dependent radical
   scalings; and
2. the modular witness construction behind the uniform cubic and quartic
   coefficient-extraction proof.

The file does not formalise polynomial monodromy itself or the analytic
finite-pole descent.  Its scaling theorems take full symmetric projective
invariance as a hypothesis, exactly exposing that remaining interface.
-/

namespace CyclicityUniform

set_option maxHeartbeats 1000000

section Scaling

variable {ι K : Type*} [DecidableEq ι] [Field K]

/-- If a projective line is stable under a transposition and a third nonzero
coordinate is fixed, the two transposed coordinates are equal. -/
theorem projective_swap_equal (L : ι → K) (i j k : ι)
    (hki : k ≠ i) (hkj : k ≠ j) (hk : L k ≠ 0)
    (hproj : ∃ μ : K, ∀ r, L ((Equiv.swap i j) r) = μ * L r) :
    L i = L j := by
  rcases hproj with ⟨μ, hμ⟩
  have hfixed : L k = μ * L k := by
    simpa [Equiv.swap_apply_of_ne_of_ne hki hkj] using hμ k
  have hμone : μ = 1 := by
    apply (mul_right_cancel₀ hk)
    simpa using hfixed.symm
  have hi := hμ i
  simpa [Equiv.swap_apply_left, hμone] using hi.symm

/-- Taking `m`-th powers removes the rootwise roots of unity in a lifted
monodromy transformation. -/
theorem lifted_relation_power_projective {n : ℕ} (m : ℕ)
    (lam zeta : Fin n → K) (σ : Equiv.Perm (Fin n)) (μ : K)
    (hzeta : ∀ i, zeta i ^ m = 1)
    (hlift : ∀ j, lam (σ.symm j) * zeta (σ.symm j) = μ * lam j) :
    ∀ j, lam (σ.symm j) ^ m = μ ^ m * lam j ^ m := by
  intro j
  calc
    lam (σ.symm j) ^ m = lam (σ.symm j) ^ m * 1 := by simp
    _ = lam (σ.symm j) ^ m * zeta (σ.symm j) ^ m := by rw [hzeta]
    _ = (lam (σ.symm j) * zeta (σ.symm j)) ^ m := by rw [mul_pow]
    _ = (μ * lam j) ^ m := by rw [hlift]
    _ = μ ^ m * lam j ^ m := by rw [mul_pow]

/-- The natural permutation representation of `S₃` has no nonconstant
projectively invariant line with nonzero coordinates. -/
theorem projective_s3_constant (L : Fin 3 → K) (hL : ∀ i, L i ≠ 0)
    (hproj : ∀ σ : Equiv.Perm (Fin 3), ∃ μ : K, ∀ r, L (σ r) = μ * L r) :
    ∀ i j, L i = L j := by
  have h01 : L 0 = L 1 := by
    apply projective_swap_equal L 0 1 2 (by decide) (by decide) (hL 2)
    exact hproj (Equiv.swap 0 1)
  have h02 : L 0 = L 2 := by
    apply projective_swap_equal L 0 2 1 (by decide) (by decide) (hL 1)
    exact hproj (Equiv.swap 0 2)
  intro i j
  fin_cases i <;> fin_cases j <;> simp_all

/-- The analogous statement for the natural permutation representation of
`S₄`. -/
theorem projective_s4_constant (L : Fin 4 → K) (hL : ∀ i, L i ≠ 0)
    (hproj : ∀ σ : Equiv.Perm (Fin 4), ∃ μ : K, ∀ r, L (σ r) = μ * L r) :
    ∀ i j, L i = L j := by
  have h01 : L 0 = L 1 := by
    apply projective_swap_equal L 0 1 2 (by decide) (by decide) (hL 2)
    exact hproj (Equiv.swap 0 1)
  have h02 : L 0 = L 2 := by
    apply projective_swap_equal L 0 2 1 (by decide) (by decide) (hL 1)
    exact hproj (Equiv.swap 0 2)
  have h03 : L 0 = L 3 := by
    apply projective_swap_equal L 0 3 1 (by decide) (by decide) (hL 1)
    exact hproj (Equiv.swap 0 3)
  intro i j
  fin_cases i <;> fin_cases j <;> simp_all

theorem scaling_powers_equal_s3 (m : ℕ) (lam : Fin 3 → K)
    (hlam : ∀ i, lam i ≠ 0)
    (hproj : ∀ σ : Equiv.Perm (Fin 3), ∃ μ : K,
      ∀ r, lam (σ r) ^ m = μ * lam r ^ m) :
    ∀ i j, lam i ^ m = lam j ^ m := by
  apply projective_s3_constant (fun i ↦ lam i ^ m)
  · intro i
    exact pow_ne_zero m (hlam i)
  · exact hproj

theorem scaling_powers_equal_s4 (m : ℕ) (lam : Fin 4 → K)
    (hlam : ∀ i, lam i ≠ 0)
    (hproj : ∀ σ : Equiv.Perm (Fin 4), ∃ μ : K,
      ∀ r, lam (σ r) ^ m = μ * lam r ^ m) :
    ∀ i j, lam i ^ m = lam j ^ m := by
  apply projective_s4_constant (fun i ↦ lam i ^ m)
  · intro i
    exact pow_ne_zero m (hlam i)
  · exact hproj

/-- Over an algebraically closed field, equal nonzero `m`-th powers can be
made equal to one by one common rescaling. -/
theorem common_rescale_of_equal_powers {n : ℕ} [IsAlgClosed K]
    (m : ℕ) (hm : 0 < m) (lam : Fin (n + 1) → K)
    (hlam : ∀ i, lam i ≠ 0)
    (hequal : ∀ i j, lam i ^ m = lam j ^ m) :
    ∃ s : K, ∀ i, (s * lam i) ^ m = 1 := by
  obtain ⟨s, hs⟩ := IsAlgClosed.exists_pow_nat_eq (lam 0 ^ m)⁻¹ hm
  refine ⟨s, fun i ↦ ?_⟩
  rw [mul_pow, hs, hequal i 0, inv_mul_cancel₀ (pow_ne_zero m (hlam 0))]

end Scaling

section CoefficientFormulae

open Finset

/-- Coefficient of `t^r` in the negative-binomial expansion of
`(1 + a*t^2)^(-k-1)`. -/
def cubicInvCoeff (k r : ℕ) (a : ℚ) : ℚ :=
  ∑ j ∈ range (r + 1),
    if 2 * j = r then
      (-1 : ℚ) ^ j * (Nat.choose (k + j) j : ℚ) * a ^ j
    else 0

/-- Coefficient of `t^r` in the negative-binomial expansion of
`(1 + a*t^2 + c*t^3)^(-k-1)`. -/
def quarticInvCoeff (k r : ℕ) (a c : ℚ) : ℚ :=
  ∑ u ∈ range (r + 1), ∑ v ∈ range (r + 1),
    if 2 * u + 3 * v = r then
      (-1 : ℚ) ^ (u + v) *
        (Nat.choose (k + u + v) (u + v) : ℚ) *
        (Nat.choose (u + v) u : ℚ) * a ^ u * c ^ v
    else 0

theorem cubic_coeff_zero (k : ℕ) (a : ℚ) :
    cubicInvCoeff k 0 a = 1 := by
  norm_num [cubicInvCoeff, Finset.sum_range_succ]

theorem cubic_coeff_two (k : ℕ) (a : ℚ) :
    cubicInvCoeff k 2 a = -(k + 1 : ℕ) * a := by
  norm_num [cubicInvCoeff, Finset.sum_range_succ, Nat.choose_one_right]

theorem cubic_coeff_four (k : ℕ) (a : ℚ) :
    cubicInvCoeff k 4 a = (Nat.choose (k + 2) 2 : ℚ) * a ^ 2 := by
  norm_num [cubicInvCoeff, Finset.sum_range_succ]

theorem quartic_coeff_zero (k : ℕ) (a c : ℚ) :
    quarticInvCoeff k 0 a c = 1 := by
  norm_num [quarticInvCoeff, Finset.sum_range_succ]

theorem quartic_coeff_two (k : ℕ) (a c : ℚ) :
    quarticInvCoeff k 2 a c = -(k + 1 : ℕ) * a := by
  norm_num [quarticInvCoeff, Finset.sum_range_succ, Nat.choose_one_right]

theorem quartic_coeff_three (k : ℕ) (a c : ℚ) :
    quarticInvCoeff k 3 a c = -(k + 1 : ℕ) * c := by
  norm_num [quarticInvCoeff, Finset.sum_range_succ, Nat.choose_one_right]

theorem quartic_coeff_five (k : ℕ) (a c : ℚ) :
    quarticInvCoeff k 5 a c = 2 * (Nat.choose (k + 2) 2 : ℚ) * a * c := by
  norm_num [quarticInvCoeff, Finset.sum_range_succ]
  exact Or.inl (Or.inl (by ring))

theorem quarticInvCoeff_a_zero (k r : ℕ) (c : ℚ) :
    quarticInvCoeff k r 0 c =
      ∑ v ∈ Finset.range (r + 1),
        if 3 * v = r then
          (-1 : ℚ) ^ v * (Nat.choose (k + v) v : ℚ) * c ^ v
        else 0 := by
  classical
  unfold quarticInvCoeff
  rw [Finset.sum_eq_single 0]
  · simp
  · intro u hu hu0
    have hupos : 0 < u := Nat.pos_of_ne_zero hu0
    simp [zero_pow hupos.ne']
  · simp

theorem quartic_coeff_six_at_a_zero (k : ℕ) (c : ℚ) :
    quarticInvCoeff k 6 0 c = (Nat.choose (k + 2) 2 : ℚ) * c ^ 2 := by
  norm_num [quarticInvCoeff, Finset.sum_range_succ]

theorem quartic_coeff_nine_at_a_zero (k : ℕ) (c : ℚ) :
    quarticInvCoeff k 9 0 c =
      -(Nat.choose (k + 3) 3 : ℚ) * c ^ 3 := by
  rw [quarticInvCoeff_a_zero]
  norm_num [Finset.sum_range_succ]

end CoefficientFormulae

section UniformWitnesses

/-- For every cubic exponent beyond the sole boundary `m=4`, modular
arithmetic produces one of the nonzero residual coefficients `0,2,4`. -/
theorem cubic_uniform_residual_witness (m : ℕ) (hm : 5 ≤ m) :
    ∃ k r : ℕ, m = 3 + 3 * k + r ∧ (r = 0 ∨ r = 2 ∨ r = 4) := by
  have hmod : m % 3 < 3 := Nat.mod_lt m (by omega)
  interval_cases h : m % 3
  · refine ⟨(m - 3) / 3, 0, ?_, Or.inl rfl⟩
    omega
  · refine ⟨(m - 7) / 3, 4, ?_, Or.inr (Or.inr rfl)⟩
    omega
  · refine ⟨(m - 5) / 3, 2, ?_, Or.inr (Or.inl rfl)⟩
    omega

/-- If `a != 0`, every quartic exponent `m >= 4` except `m=5` has a
nonzero residual witness among `0,2,3,5`. -/
theorem quartic_uniform_residual_witness_a_ne_zero (m : ℕ) (hm : 4 ≤ m)
    (hm5 : m ≠ 5) :
    ∃ k r : ℕ, m = 4 + 4 * k + r ∧ (r = 0 ∨ r = 2 ∨ r = 3 ∨ r = 5) := by
  have hmod : m % 4 < 4 := Nat.mod_lt m (by omega)
  interval_cases h : m % 4
  · refine ⟨(m - 4) / 4, 0, ?_, Or.inl rfl⟩
    omega
  · refine ⟨(m - 9) / 4, 5, ?_, Or.inr (Or.inr (Or.inr rfl))⟩
    omega
  · refine ⟨(m - 6) / 4, 2, ?_, Or.inr (Or.inl rfl)⟩
    omega
  · refine ⟨(m - 7) / 4, 3, ?_, Or.inr (Or.inr (Or.inl rfl))⟩
    omega

/-- On the locus `a=0`, the only quartic exponents not immediately exposed
by residuals `0,3,6,9` are the boundary values `5,6,9`. -/
theorem quartic_uniform_residual_witness_a_zero (m : ℕ) (hm : 4 ≤ m)
    (hm5 : m ≠ 5) (hm6 : m ≠ 6) (hm9 : m ≠ 9) :
    ∃ k r : ℕ, m = 4 + 4 * k + r ∧ (r = 0 ∨ r = 3 ∨ r = 6 ∨ r = 9) := by
  have hmod : m % 4 < 4 := Nat.mod_lt m (by omega)
  interval_cases h : m % 4
  · refine ⟨(m - 4) / 4, 0, ?_, Or.inl rfl⟩
    omega
  · refine ⟨(m - 13) / 4, 9, ?_, Or.inr (Or.inr (Or.inr rfl))⟩
    omega
  · refine ⟨(m - 10) / 4, 6, ?_, Or.inr (Or.inr (Or.inl rfl))⟩
    omega
  · refine ⟨(m - 7) / 4, 3, ?_, Or.inr (Or.inl rfl)⟩
    omega

/-- The cubic modular witness always selects a genuinely nonzero coefficient
when `a != 0`. -/
theorem cubic_uniform_coefficient_nonzero (m : ℕ) (hm : 5 ≤ m)
    (a : ℚ) (ha : a ≠ 0) :
    ∃ k r : ℕ, m = 3 + 3 * k + r ∧ cubicInvCoeff k r a ≠ 0 := by
  rcases cubic_uniform_residual_witness m hm with ⟨k, r, hmr, hr⟩
  rcases hr with rfl | rfl | rfl
  · refine ⟨k, 0, hmr, ?_⟩
    rw [cubic_coeff_zero]
    norm_num
  · refine ⟨k, 2, hmr, ?_⟩
    rw [cubic_coeff_two]
    have hk : ((k + 1 : ℕ) : ℚ) ≠ 0 := by positivity
    exact mul_ne_zero (neg_ne_zero.mpr hk) ha
  · refine ⟨k, 4, hmr, ?_⟩
    rw [cubic_coeff_four]
    have hchooseNat : 0 < Nat.choose (k + 2) 2 := Nat.choose_pos (by omega)
    have hchoose : (Nat.choose (k + 2) 2 : ℚ) ≠ 0 := by exact_mod_cast hchooseNat.ne'
    exact mul_ne_zero hchoose (pow_ne_zero 2 ha)

/-- In the quartic branch `a != 0`, every `m >= 4` except `m=5` has a
nonzero coefficient witness. -/
theorem quartic_uniform_coefficient_nonzero_a_ne_zero (m : ℕ) (hm : 4 ≤ m)
    (hm5 : m ≠ 5) (a c : ℚ) (ha : a ≠ 0) (hc : c ≠ 0) :
    ∃ k r : ℕ, m = 4 + 4 * k + r ∧ quarticInvCoeff k r a c ≠ 0 := by
  rcases quartic_uniform_residual_witness_a_ne_zero m hm hm5 with ⟨k, r, hmr, hr⟩
  rcases hr with rfl | rfl | rfl | rfl
  · refine ⟨k, 0, hmr, ?_⟩
    rw [quartic_coeff_zero]
    norm_num
  · refine ⟨k, 2, hmr, ?_⟩
    rw [quartic_coeff_two]
    have hk : ((k + 1 : ℕ) : ℚ) ≠ 0 := by positivity
    exact mul_ne_zero (neg_ne_zero.mpr hk) ha
  · refine ⟨k, 3, hmr, ?_⟩
    rw [quartic_coeff_three]
    have hk : ((k + 1 : ℕ) : ℚ) ≠ 0 := by positivity
    exact mul_ne_zero (neg_ne_zero.mpr hk) hc
  · refine ⟨k, 5, hmr, ?_⟩
    rw [quartic_coeff_five]
    have hchooseNat : 0 < Nat.choose (k + 2) 2 := Nat.choose_pos (by omega)
    have hchoose : (Nat.choose (k + 2) 2 : ℚ) ≠ 0 := by exact_mod_cast hchooseNat.ne'
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hchoose) ha) hc

/-- On `a=0`, every quartic exponent outside `5,6,9` has a nonzero
coefficient witness when `c != 0`. -/
theorem quartic_uniform_coefficient_nonzero_a_zero (m : ℕ) (hm : 4 ≤ m)
    (hm5 : m ≠ 5) (hm6 : m ≠ 6) (hm9 : m ≠ 9) (c : ℚ) (hc : c ≠ 0) :
    ∃ k r : ℕ, m = 4 + 4 * k + r ∧ quarticInvCoeff k r 0 c ≠ 0 := by
  rcases quartic_uniform_residual_witness_a_zero m hm hm5 hm6 hm9 with
    ⟨k, r, hmr, hr⟩
  rcases hr with rfl | rfl | rfl | rfl
  · refine ⟨k, 0, hmr, ?_⟩
    rw [quartic_coeff_zero]
    norm_num
  · refine ⟨k, 3, hmr, ?_⟩
    rw [quartic_coeff_three]
    have hk : ((k + 1 : ℕ) : ℚ) ≠ 0 := by positivity
    exact mul_ne_zero (neg_ne_zero.mpr hk) hc
  · refine ⟨k, 6, hmr, ?_⟩
    rw [quartic_coeff_six_at_a_zero]
    have hchooseNat : 0 < Nat.choose (k + 2) 2 := Nat.choose_pos (by omega)
    have hchoose : (Nat.choose (k + 2) 2 : ℚ) ≠ 0 := by exact_mod_cast hchooseNat.ne'
    exact mul_ne_zero hchoose (pow_ne_zero 2 hc)
  · refine ⟨k, 9, hmr, ?_⟩
    rw [quartic_coeff_nine_at_a_zero]
    have hchooseNat : 0 < Nat.choose (k + 3) 3 := Nat.choose_pos (by omega)
    have hchoose : (Nat.choose (k + 3) 3 : ℚ) ≠ 0 := by exact_mod_cast hchooseNat.ne'
    exact mul_ne_zero (neg_ne_zero.mpr hchoose) (pow_ne_zero 3 hc)

/-- Uniform cubic conclusion from the coefficient formula: simultaneous
vanishing leaves only `m=2` and the secondary boundary `m=4`. -/
theorem cubic_uniform_boundary (m : ℕ) (hm : 2 ≤ m) (a : ℚ) (ha : a ≠ 0)
    (hvanish : ∀ k r : ℕ, m = 3 + 3 * k + r → cubicInvCoeff k r a = 0) :
    m = 2 ∨ m = 4 := by
  by_cases hm2 : m = 2
  · exact Or.inl hm2
  by_cases hm4 : m = 4
  · exact Or.inr hm4
  have hm3or5 : m = 3 ∨ 5 ≤ m := by omega
  rcases hm3or5 with hm3 | hm5
  · have hz := hvanish 0 0 (by omega)
    rw [cubic_coeff_zero] at hz
    norm_num at hz
  · rcases cubic_uniform_coefficient_nonzero m hm5 a ha with ⟨k, r, hmr, hn⟩
    exact (hn (hvanish k r hmr)).elim

/-- Uniform quartic conclusion from the coefficient formula.  These are
exactly the boundary values subsequently eliminated by `E₂`, except for
`m=3,a=0`. -/
theorem quartic_uniform_boundary (m : ℕ) (hm : 2 ≤ m) (a c : ℚ) (hc : c ≠ 0)
    (hvanish : ∀ k r : ℕ, m = 4 + 4 * k + r → quarticInvCoeff k r a c = 0) :
    m = 2 ∨ m = 3 ∨ m = 5 ∨ (m = 6 ∧ a = 0) ∨ (m = 9 ∧ a = 0) := by
  by_cases hm2 : m = 2
  · exact Or.inl hm2
  by_cases hm3 : m = 3
  · exact Or.inr (Or.inl hm3)
  have hm4 : 4 ≤ m := by omega
  by_cases ha0 : a = 0
  · subst a
    by_cases hm5 : m = 5
    · exact Or.inr (Or.inr (Or.inl hm5))
    by_cases hm6 : m = 6
    · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨hm6, rfl⟩)))
    by_cases hm9 : m = 9
    · exact Or.inr (Or.inr (Or.inr (Or.inr ⟨hm9, rfl⟩)))
    rcases quartic_uniform_coefficient_nonzero_a_zero m hm4 hm5 hm6 hm9 c hc with
      ⟨k, r, hmr, hn⟩
    exact (hn (hvanish k r hmr)).elim
  · by_cases hm5 : m = 5
    · exact Or.inr (Or.inr (Or.inl hm5))
    rcases quartic_uniform_coefficient_nonzero_a_ne_zero m hm4 hm5 a c ha0 hc with
      ⟨k, r, hmr, hn⟩
    exact (hn (hvanish k r hmr)).elim

end UniformWitnesses

end CyclicityUniform
