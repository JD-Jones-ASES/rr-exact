module

public import RRExact.Defs
public import RRExact.Perms

/-!
Compared statements for the exact norm of De Sa's `n = 5` counterexample.
Definitions are shared with the development. These declarations are the contract;
the proofs are in `RRExact`, not here.
-/

@[expose] public section

namespace RRExact

/-- The five matrices are symmetric and positive semidefinite, sum to `5 I`,
and the kernel of each `Aₖ` is the line through `κₖ = 1 - 5 yₖ`. -/
theorem family_psd :
    (∀ k i j, A k i j = A k j i) ∧
      (∀ k v, 0 ≤ dot v (mv (A k) v)) ∧
      (∀ i j, sumA i j = (5 : Rat) * (if i = j then 1 else 0)) ∧
      (∀ k i, mv (A k) (kappa k) i = 0) ∧
      (∀ k v, dot v (mv (A k) v) = 0 → ∀ i, v i = (dot ones v / 5) * kappa k i) := by
  sorry

/-- `perms` is exactly `S₅`, and the average of the ordered products is
`(29/64) I - (21/64) J`. -/
theorem average_closed :
    perms.length = 120 ∧ perms.Nodup ∧ (∀ p ∈ perms, isPerm p = true) ∧
      (∀ p, isPerm p = true → p ∈ perms) ∧ reshuffle = closed := by
  sorry

/-- Every vector is expanded by at most `19/16` in Euclidean norm. -/
theorem operator_norm (v : Fin 5 → Rat) : sq (mv reshuffle v) * 256 ≤ 361 * sq v := by
  sorry

/-- The bound is attained on the all-ones vector. -/
theorem operator_norm_sharp :
    (mv reshuffle ones = fun _ => (-19 / 16 : Rat)) ∧
      (sq (mv reshuffle ones) * 256 = 361 * sq ones) ∧ sq ones = 5 ∧
      ((19 / 16 : Rat) ^ 2 = 361 / 256) := by
  sorry

/-- Terminal values through the first violation, the `n = 5` age table, and `a₁₀`. -/
theorem recurrence_bound :
    seq 2 2 = 0 ∧ seq 3 3 = -1 / 2 ∧ seq 4 4 = -8 / 9 ∧ seq 5 5 = -19 / 16 ∧
      seq 10 10 = -99712 / 59049 ∧
      seq 5 0 = 1 ∧ seq 5 1 = 1 ∧ seq 5 2 = 3 / 4 ∧ seq 5 3 = 1 / 4 ∧
      seq 5 4 = -7 / 16 ∧ seq 5 5 = -19 / 16 ∧
      seq 2 2 ≤ (1 : Rat) ∧ -(seq 2 2) ≤ 1 ∧
      seq 3 3 ≤ 1 ∧ -(seq 3 3) ≤ 1 ∧
      seq 4 4 ≤ 1 ∧ -(seq 4 4) ≤ 1 ∧
      1 < -(seq 5 5) := by
  sorry

end RRExact
