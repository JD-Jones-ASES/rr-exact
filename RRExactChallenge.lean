module

public import Mathlib.Analysis.CStarAlgebra.Matrix
public import Mathlib.Analysis.Complex.Order
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.LinearAlgebra.Matrix.Notation
public import Mathlib.Data.Fintype.Perm

/-!
Two exact low-dimensional counterexamples to the norm-of-averaged-product
Recht–Ré inequality. The means and permutation averages below have their
standard meanings; the only dependencies of this contract are Mathlib and its
pinned dependencies. Positive semidefiniteness and the Euclidean operator norm
are Mathlib's analytic definitions over the displayed scalar fields.
-/

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
  sorry

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
  sorry

end

end RRExact
