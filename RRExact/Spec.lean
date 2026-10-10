module

import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Prod

public import RRExact.Perms

@[expose] public section

namespace RRExact

set_option maxHeartbeats 0
set_option maxRecDepth 100000

theorem perms_length : perms.length = 120 := by
  simp only [perms]
  rfl

theorem perms_nodup : perms.Nodup := by
  unfold perms
  decide

theorem perms_valid : ∀ p ∈ perms, isPerm p = true := by
  intro p hp
  simp only [perms, List.mem_cons, List.mem_nil_iff, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  <;> simp [isPerm, coords]

theorem perms_complete (p : Perm5) (hp : isPerm p = true) : p ∈ perms := by
  revert p hp
  decide

end RRExact
