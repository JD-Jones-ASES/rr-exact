module

public import RRExact.LowDim
public import Mathlib.Data.Fintype.Perm
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

@[expose] public section

open scoped Matrix.Norms.L2Operator ComplexOrder
open Matrix

namespace RRExact

noncomputable section

/-- The arithmetic mean of five square matrices. -/
def arithmeticMean {n K : Type*} [Fintype n] [Field K]
    (A : Fin 5 → Matrix n n K) : Matrix n n K :=
  (1 / 5 : K) • ∑ k, A k

/-- The average of all 120 ordered products, indexed by genuine permutations. -/
def permutationAverage {n K : Type*} [Fintype n] [DecidableEq n] [Field K]
    (A : Fin 5 → Matrix n n K) : Matrix n n K :=
  (1 / 120 : K) • ∑ σ : Equiv.Perm (Fin 5),
    A (σ 0) * A (σ 1) * A (σ 2) * A (σ 3) * A (σ 4)

/-- Record the images of the five indices as an ordered tuple. -/
def permutationTuple (σ : Equiv.Perm (Fin 5)) : Perm5 :=
  (σ 0, σ 1, σ 2, σ 3, σ 4)

theorem coords_permutationTuple (σ : Equiv.Perm (Fin 5)) :
    coords (permutationTuple σ) = σ := by
  funext i
  fin_cases i <;> rfl

theorem permutationTuple_injective : Function.Injective permutationTuple := by
  intro σ τ h
  apply Equiv.ext
  intro i
  have hc := congrArg (fun p => coords p i) h
  simpa only [coords_permutationTuple] using hc

theorem permutationTuple_valid (σ : Equiv.Perm (Fin 5)) :
    isPerm (permutationTuple σ) = true := by
  simp [isPerm, coords_permutationTuple]

theorem coords_injective (p : Perm5) (hp : isPerm p = true) :
    Function.Injective (coords p) := by
  have hd : p.1 ≠ p.2.1 ∧ p.1 ≠ p.2.2.1 ∧ p.1 ≠ p.2.2.2.1 ∧
      p.1 ≠ p.2.2.2.2 ∧ p.2.1 ≠ p.2.2.1 ∧ p.2.1 ≠ p.2.2.2.1 ∧
      p.2.1 ≠ p.2.2.2.2 ∧ p.2.2.1 ≠ p.2.2.2.1 ∧
      p.2.2.1 ≠ p.2.2.2.2 ∧ p.2.2.2.1 ≠ p.2.2.2.2 := by
    exact of_decide_eq_true hp
  intro i j h
  fin_cases i <;> fin_cases j <;> simp_all [coords]

/-- Every tuple in the certified enumeration arises from a genuine permutation. -/
theorem permutationTuple_surjective (p : Perm5) (hp : p ∈ perms) :
    ∃ σ : Equiv.Perm (Fin 5), permutationTuple σ = p := by
  let σ : Equiv.Perm (Fin 5) := Equiv.ofBijective (coords p)
    (Finite.injective_iff_bijective.mp (coords_injective p (perms_valid p hp)))
  exact ⟨σ, rfl⟩

/-- The concrete certificate enumerates precisely the standard permutation sum. -/
theorem permutation_sum_eq_total {n K : Type*} [Fintype n] [DecidableEq n] [Semiring K]
    (A : Fin 5 → Matrix n n K) :
    (∑ σ : Equiv.Perm (Fin 5),
      A (σ 0) * A (σ 1) * A (σ 2) * A (σ 3) * A (σ 4)) = LowDim.total A := by
  classical
  rw [LowDim.total, ← List.sum_toFinset _ perms_nodup]
  apply Finset.sum_bij (fun σ _ => permutationTuple σ)
  · intro σ hσ
    exact List.mem_toFinset.mpr (perms_complete _ (permutationTuple_valid σ))
  · intro σ hσ τ hτ h
    exact permutationTuple_injective h
  · intro p hp
    obtain ⟨σ, hσ⟩ := permutationTuple_surjective p (List.mem_toFinset.mp hp)
    exact ⟨σ, Finset.mem_univ _, hσ⟩
  · intro σ hσ
    rfl

theorem permutationAverage_eq_average {n K : Type*} [Fintype n] [DecidableEq n] [Field K]
    (A : Fin 5 → Matrix n n K) : permutationAverage A = LowDim.average A := by
  rw [permutationAverage, permutation_sum_eq_total]
  rfl

/-- Five real PSD matrices in dimension 3 violate the norm-of-average
Recht–Ré inequality at `n = k = 5`, with exact ratio `10329/10000`.
Every matrix norm is the Euclidean operator norm. -/
theorem real_counterexample :
    ∃ A : Fin 5 → Matrix (Fin 3) (Fin 3) ℝ,
      (∀ k, (A k).PosSemidef) ∧
      (∑ k, A k = (100 : Matrix (Fin 3) (Fin 3) ℝ)) ∧
      (permutationAverage A = diagonal ![-3305280, -291264, -291264]) ∧
      ‖arithmeticMean A‖ = 20 ∧ ‖permutationAverage A‖ = 3305280 ∧
      ‖arithmeticMean A ^ 5‖ = 3200000 ∧
      ‖arithmeticMean A ^ 5‖ < ‖permutationAverage A‖ ∧
      ‖permutationAverage A‖ / ‖arithmeticMean A‖ ^ 5 = (10329 / 10000 : ℝ) := by
  refine ⟨LowDim.realFamily, ?_⟩
  simpa only [permutationAverage_eq_average, arithmeticMean, LowDim.mean] using
    LowDim.real_counterexample

/-- Five complex PSD matrices in dimension 2 violate the norm-of-average
Recht–Ré inequality at `n = k = 5`, with exact ratio `10329/10000`.
Every matrix norm is the Euclidean operator norm. -/
theorem complex_counterexample :
    ∃ A : Fin 5 → Matrix (Fin 2) (Fin 2) ℂ,
      (∀ k, (A k).PosSemidef) ∧
      (∑ k, A k = (100 : Matrix (Fin 2) (Fin 2) ℂ)) ∧
      (permutationAverage A = diagonal ![-3305280, -2941824]) ∧
      ‖arithmeticMean A‖ = 20 ∧ ‖permutationAverage A‖ = 3305280 ∧
      ‖arithmeticMean A ^ 5‖ = 3200000 ∧
      ‖arithmeticMean A ^ 5‖ < ‖permutationAverage A‖ ∧
      ‖permutationAverage A‖ / ‖arithmeticMean A‖ ^ 5 = (10329 / 10000 : ℝ) := by
  refine ⟨LowDim.complexFamily, ?_⟩
  simpa only [permutationAverage_eq_average, arithmeticMean, LowDim.mean] using
    LowDim.complex_counterexample

end

end RRExact
