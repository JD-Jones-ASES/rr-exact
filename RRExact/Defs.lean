module

import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

@[expose] public section

namespace RRExact

/-- Five-by-five rational matrices, as functions. -/
abbrev Mat := Fin 5 → Fin 5 → Rat

/-- The sum of the five values of `f`. -/
def sum5 (f : Fin 5 → Rat) : Rat :=
  f 0 + f 1 + f 2 + f 3 + f 4

/-- De Sa's vector at index `k`, for `n = 5`. The distinguished coordinate is `2/5`. -/
def y (k i : Fin 5) : Rat :=
  if i = k then (2 : Rat) / 5 else -1 / 10

/-- `Aₖ = I + 1 yₖᵀ + yₖ 1ᵀ`. -/
def A (k : Fin 5) : Mat :=
  fun i j => (if i = j then (1 : Rat) else 0) + y k j + y k i

/-- The all-ones vector. -/
def ones (_ : Fin 5) : Rat := 1

/-- The standard dot product, written as an explicit five-term sum. -/
def dot (v w : Fin 5 → Rat) : Rat :=
  sum5 fun i => v i * w i

/-- Squared Euclidean norm. -/
def sq (v : Fin 5 → Rat) : Rat :=
  dot v v

/-- Matrix-vector product. -/
def mv (M : Mat) (v : Fin 5 → Rat) : Fin 5 → Rat :=
  fun i => sum5 fun j => M i j * v j

/-- Matrix product. -/
def mmul (M N : Mat) : Mat :=
  fun i j => sum5 fun k => M i k * N k j

/-- Entrywise sum. `Mat` has no imported additive instance. -/
def madd (M N : Mat) : Mat :=
  fun i j => M i j + N i j

/-- The zero matrix. -/
def mzero : Mat :=
  fun _ _ => 0

/-- Entrywise sum of the five matrices. -/
def sumA : Mat :=
  madd (madd (madd (madd (A 0) (A 1)) (A 2)) (A 3)) (A 4)

/-- The kernel vector `1 - 5 yₖ` of `Aₖ`. -/
def kappa (k : Fin 5) : Fin 5 → Rat :=
  fun i => 1 - 5 * y k i

/-- The all-ones matrix. -/
def J : Mat := fun _ _ => 1

/-- `(29/64) I - (21/64) J`. -/
def closed : Mat :=
  fun i j => (29 / 64) * (if i = j then (1 : Rat) else 0) + (-21 / 64)

/-- An ordered 5-tuple, used as a word in `Fin 5`. -/
abbrev Perm5 := Fin 5 × Fin 5 × Fin 5 × Fin 5 × Fin 5

/-- Read a 5-tuple as a function on `Fin 5`. -/
def coords (p : Perm5) : Fin 5 → Fin 5
  | 0 => p.1
  | 1 => p.2.1
  | 2 => p.2.2.1
  | 3 => p.2.2.2.1
  | 4 => p.2.2.2.2

/-- The ordered product `A_{p₀} ⋯ A_{p₄}`. -/
def prod5 (p : Perm5) : Mat :=
  mmul (mmul (mmul (mmul (A (coords p 0)) (A (coords p 1))) (A (coords p 2))) (A (coords p 3)))
    (A (coords p 4))

/-- `p` is a permutation when its five coordinates are pairwise distinct. -/
def isPerm (p : Perm5) : Bool :=
  let a := coords p 0
  let b := coords p 1
  let c := coords p 2
  let d := coords p 3
  let e := coords p 4
  decide
    (a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ a ≠ e ∧ b ≠ c ∧ b ≠ d ∧ b ≠ e ∧ c ≠ d ∧ c ≠ e ∧ d ≠ e)

/-- The second-order sequence `a₀ = a₁ = 1`, `a_{t+2} = 2 a_{t+1} - (n/(n-1)) a_t`. -/
def seq (n : Nat) : Nat → Rat
  | Nat.zero => 1
  | Nat.succ Nat.zero => 1
  | Nat.succ (Nat.succ t) =>
    2 * seq n (Nat.succ t) - ((n : Rat) / (n - 1 : Nat)) * seq n t

theorem y_orth_test : ∀ k : Fin 5, dot ones (y k) = 0 := by
  intro k
  fin_cases k <;> simp [dot, sum5, ones, y] <;> norm_num

theorem ones_sq_test : sq ones = 5 := by
  simp [sq, dot, sum5, ones]
  norm_num

end RRExact
