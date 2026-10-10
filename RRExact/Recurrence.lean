module

import Mathlib.Tactic.NormNum

public import RRExact.Defs

@[expose] public section

namespace RRExact

theorem terminal_values :
    seq 2 2 = 0 ∧ seq 3 3 = -1 / 2 ∧ seq 4 4 = -8 / 9 ∧ seq 5 5 = -19 / 16 ∧
      seq 10 10 = -99712 / 59049 := by
  simp only [seq]
  norm_num

theorem age_table :
    seq 5 0 = 1 ∧ seq 5 1 = 1 ∧ seq 5 2 = 3 / 4 ∧ seq 5 3 = 1 / 4 ∧
      seq 5 4 = -7 / 16 ∧ seq 5 5 = -19 / 16 := by
  simp only [seq]
  norm_num

theorem early_bound :
    seq 2 2 ≤ (1 : Rat) ∧ -(seq 2 2) ≤ 1 ∧
      seq 3 3 ≤ 1 ∧ -(seq 3 3) ≤ 1 ∧
      seq 4 4 ≤ 1 ∧ -(seq 4 4) ≤ 1 ∧
      1 < -(seq 5 5) := by
  simp only [seq]
  norm_num

end RRExact
