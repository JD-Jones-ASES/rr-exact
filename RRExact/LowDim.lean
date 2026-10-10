module

public import RRExact.LowDimDefs
public import RRExact.Spec
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

@[expose] public section

open scoped Matrix.Norms.L2Operator ComplexOrder
open Matrix

namespace RRExact.LowDim

noncomputable section
set_option maxHeartbeats 0
set_option maxRecDepth 100000

/-- The real matrices are Gram matrices, so their positivity is over all real vectors. -/
theorem real_gram (k : Fin 5) : realFamily k = (realRoot k)ᴴ * realRoot k := by
  ext i j
  fin_cases k <;> fin_cases i <;> fin_cases j <;>
    norm_num [realFamily, realRoot, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Fin.sum_univ_succ]

/-- Standard Mathlib positive semidefiniteness of every member of the real family. -/
theorem real_psd (k : Fin 5) : (realFamily k).PosSemidef := by
  rw [real_gram]
  exact Matrix.posSemidef_conjTranspose_mul_self _

/-- Standard Mathlib positive semidefiniteness of every member of the complex family. -/
theorem complex_psd (k : Fin 5) : (complexFamily k).PosSemidef :=
  Matrix.posSemidef_vecMulVec_self_star _

/-- The five real matrices sum to `100 I`. -/
theorem real_sum : ∑ k, realFamily k = (100 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [realFamily, Fin.sum_univ_succ, Matrix.ofNat_apply]

/-- The five complex matrices sum to `100 I`. -/
theorem complex_sum : ∑ k, complexFamily k = (100 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [complexFamily, complexVector, Matrix.vecMulVec, Fin.sum_univ_succ,
      Matrix.ofNat_apply, Complex.ext_iff]

/-- Applying a coefficient ring homomorphism commutes with the permutation sum. -/
theorem total_map {n K L : Type*} [Fintype n] [DecidableEq n] [Semiring K] [Semiring L]
    (f : K →+* L) (A : Fin 5 → Matrix n n K) :
    total (fun k => (A k).map f) = (total A).map f := by
  change total (fun k => f.mapMatrix (A k)) = f.mapMatrix (total A)
  simp only [total, map_list_sum, List.map_map, Function.comp_def, word, map_mul]
  rfl

/-- The real matrices are precisely the entrywise casts of the integer certificate. -/
theorem real_cast (k : Fin 5) : realFamily k = (realInt k).map (Int.castRingHom ℝ) := by
  ext i j
  fin_cases k <;> fin_cases i <;> fin_cases j <;>
    norm_num [realFamily, realInt]

/-- The complex matrices are precisely the casts of the Gaussian-integer certificate. -/
theorem complex_cast (k : Fin 5) :
    complexFamily k = (complexInt k).map GaussianInt.toComplex := by
  ext i j
  fin_cases k <;> fin_cases i <;> fin_cases j <;>
    norm_num [complexFamily, complexVector, complexInt, Matrix.vecMulVec,
      GaussianInt.toComplex_def, GaussianInt.toComplex_def', Complex.ext_iff]

/-- Exact integer identity, reduced and checked by the Lean kernel. -/
theorem real_total_int : total realInt = diagonal ![-396633600, -34951680, -34951680] := by
  decide

/-- Exact Gaussian-integer identity, reduced and checked by the Lean kernel. -/
theorem complex_total_int : total complexInt = diagonal ![-396633600, -353018880] := by
  decide

/-- Exact real permutation sum, transported from the integer calculation. -/
theorem real_total : total realFamily = diagonal ![-396633600, -34951680, -34951680] := by
  have hcast : realFamily = fun k => (realInt k).map (Int.castRingHom ℝ) := funext real_cast
  rw [hcast, total_map, real_total_int]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply]

/-- Exact complex permutation sum, transported from the Gaussian-integer calculation. -/
theorem complex_total : total complexFamily = diagonal ![-396633600, -353018880] := by
  have hcast : complexFamily = fun k => (complexInt k).map GaussianInt.toComplex := funext complex_cast
  rw [hcast, total_map, complex_total_int]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, GaussianInt.toComplex_def]

/-- The full real reshuffling average is diagonal. -/
theorem real_average : average realFamily = diagonal ![-3305280, -291264, -291264] := by
  rw [average, real_total]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply]

/-- The full complex reshuffling average is diagonal. -/
theorem complex_average : average complexFamily = diagonal ![-3305280, -2941824] := by
  rw [average, complex_total]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply]

/-- The arithmetic mean of the real witness is `20 I`. -/
theorem real_mean : mean realFamily = diagonal (fun _ => 20) := by
  rw [mean, real_sum]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, Matrix.ofNat_apply]

/-- The arithmetic mean of the complex witness is `20 I`. -/
theorem complex_mean : mean complexFamily = diagonal (fun _ => 20) := by
  rw [mean, complex_sum]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, Matrix.ofNat_apply]

/-- Standard Euclidean operator norm of the real arithmetic mean. -/
theorem real_mean_norm : ‖mean realFamily‖ = 20 := by
  rw [real_mean, Matrix.l2_opNorm_diagonal]
  norm_num

/-- Standard Euclidean operator norm of the complex arithmetic mean. -/
theorem complex_mean_norm : ‖mean complexFamily‖ = 20 := by
  rw [complex_mean, Matrix.l2_opNorm_diagonal]
  norm_num

/-- Operator norm of the with-replacement average, namely the fifth power of the mean. -/
theorem real_mean_power_norm : ‖mean realFamily ^ 5‖ = 3200000 := by
  rw [real_mean, Matrix.diagonal_pow, Matrix.l2_opNorm_diagonal]
  change ‖fun _ : Fin 3 => (20 : ℝ) ^ 5‖ = 3200000
  norm_num

/-- Operator norm of the complex with-replacement average. -/
theorem complex_mean_power_norm : ‖mean complexFamily ^ 5‖ = 3200000 := by
  rw [complex_mean, Matrix.diagonal_pow, Matrix.l2_opNorm_diagonal]
  change ‖fun _ : Fin 2 => (20 : ℂ) ^ 5‖ = 3200000
  norm_num

/-- Exact standard Euclidean operator norm of the real reshuffling average. -/
theorem real_average_norm : ‖average realFamily‖ = 3305280 := by
  rw [real_average, Matrix.l2_opNorm_diagonal]
  apply le_antisymm
  · apply (pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 3305280)).mpr
    intro i
    fin_cases i <;> norm_num
  · have h := norm_le_pi_norm (![-3305280, -291264, -291264] : Fin 3 → ℝ) 0
    norm_num at h ⊢
    exact h

/-- Exact standard Euclidean operator norm of the complex reshuffling average. -/
theorem complex_average_norm : ‖average complexFamily‖ = 3305280 := by
  rw [complex_average, Matrix.l2_opNorm_diagonal]
  apply le_antisymm
  · apply (pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 3305280)).mpr
    intro i
    fin_cases i <;> norm_num
  · have h := norm_le_pi_norm (![-3305280, -2941824] : Fin 2 → ℂ) 0
    norm_num at h ⊢
    exact h

/-- Five real positive-semidefinite `3 × 3` matrices violate Recht–Ré at `k = n = 5`.
Both norms here are Mathlib's Euclidean operator norms. -/
theorem real_counterexample :
    (∀ k, (realFamily k).PosSemidef) ∧
    (∑ k, realFamily k = (100 : Matrix (Fin 3) (Fin 3) ℝ)) ∧
    (average realFamily = diagonal ![-3305280, -291264, -291264]) ∧
    ‖mean realFamily‖ = 20 ∧ ‖average realFamily‖ = 3305280 ∧
    ‖mean realFamily ^ 5‖ = 3200000 ∧
    ‖mean realFamily ^ 5‖ < ‖average realFamily‖ ∧
    ‖average realFamily‖ / ‖mean realFamily‖ ^ 5 = (10329 / 10000 : ℝ) := by
  refine ⟨real_psd, real_sum, real_average, real_mean_norm, real_average_norm, real_mean_power_norm, ?_, ?_⟩
  · rw [real_mean_power_norm, real_average_norm]
    norm_num
  · rw [real_mean_norm, real_average_norm]
    norm_num

/-- Five complex Hermitian positive-semidefinite `2 × 2` matrices violate Recht–Ré
at `k = n = 5`, with the same exact ratio as the real `3 × 3` witness. -/
theorem complex_counterexample :
    (∀ k, (complexFamily k).PosSemidef) ∧
    (∑ k, complexFamily k = (100 : Matrix (Fin 2) (Fin 2) ℂ)) ∧
    (average complexFamily = diagonal ![-3305280, -2941824]) ∧
    ‖mean complexFamily‖ = 20 ∧ ‖average complexFamily‖ = 3305280 ∧
    ‖mean complexFamily ^ 5‖ = 3200000 ∧
    ‖mean complexFamily ^ 5‖ < ‖average complexFamily‖ ∧
    ‖average complexFamily‖ / ‖mean complexFamily‖ ^ 5 = (10329 / 10000 : ℝ) := by
  refine ⟨complex_psd, complex_sum, complex_average, complex_mean_norm, complex_average_norm, complex_mean_power_norm, ?_, ?_⟩
  · rw [complex_mean_power_norm, complex_average_norm]
    norm_num
  · rw [complex_mean_norm, complex_average_norm]
    norm_num

end

end RRExact.LowDim
