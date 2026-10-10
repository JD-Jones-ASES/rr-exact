module

public import RRExact.Norm
public import RRExact.Recurrence
public import RRExact.Shuffle
public import RRExact.Spec

@[expose] public section

namespace RRExact

/-- The five matrices are symmetric and positive semidefinite, sum to `5 I`,
and the kernel of each `Aₖ` is the line through `κₖ = 1 - 5 yₖ`. -/
theorem family_psd :
    (∀ k i j, A k i j = A k j i) ∧
      (∀ k v, 0 ≤ dot v (mv (A k) v)) ∧
      (∀ i j, sumA i j = (5 : Rat) * (if i = j then 1 else 0)) ∧
      (∀ k i, mv (A k) (kappa k) i = 0) ∧
      (∀ k v, dot v (mv (A k) v) = 0 → ∀ i, v i = (dot ones v / 5) * kappa k i) :=
  ⟨A_symm, posSemidef, sum_eq_five, kernel_vec, kernel_line⟩

/-- `perms` is exactly `S₅`, and the average of the ordered products is
`(29/64) I - (21/64) J`. -/
theorem average_closed :
    perms.length = 120 ∧ perms.Nodup ∧ (∀ p ∈ perms, isPerm p = true) ∧
      (∀ p, isPerm p = true → p ∈ perms) ∧ reshuffle = closed :=
  ⟨perms_length, perms_nodup, perms_valid, perms_complete, reshuffle_eq⟩

/-- Every vector is expanded by at most `19/16` in Euclidean norm. -/
theorem operator_norm (v : Fin 5 → Rat) : sq (mv reshuffle v) * 256 ≤ 361 * sq v := by
  simpa [reshuffle_eq] using closed_bound v

/-- The bound is attained on the all-ones vector. -/
theorem operator_norm_sharp :
    (mv reshuffle ones = fun _ => (-19 / 16 : Rat)) ∧
      (sq (mv reshuffle ones) * 256 = 361 * sq ones) ∧ sq ones = 5 ∧
      ((19 / 16 : Rat) ^ 2 = 361 / 256) := by
  simpa [reshuffle_eq] using closed_attained

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
  rcases terminal_values with ⟨h22, h33, h44, h55, h10⟩
  rcases age_table with ⟨a0, a1, a2, a3, a4, a5⟩
  rcases early_bound with ⟨b0, b1, b2, b3, b4, b5, b6⟩
  exact ⟨h22, h33, h44, h55, h10, a0, a1, a2, a3, a4, a5, b0, b1, b2, b3, b4, b5, b6⟩

end RRExact
