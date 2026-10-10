module

import Mathlib.Data.Fintype.Basic
import Init.Data.Rat.Lemmas
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

public import RRExact.Defs

@[expose] public section

namespace RRExact

lemma sum5_congr {f g : Fin 5 → Rat} (h : ∀ i, f i = g i) : sum5 f = sum5 g := by
  simp only [sum5, h]

lemma sum5_add (f g : Fin 5 → Rat) : sum5 (fun i => f i + g i) = sum5 f + sum5 g := by
  simp only [sum5]; ring

lemma sum5_add3 (f g h : Fin 5 → Rat) :
    sum5 (fun i => f i + g i + h i) = sum5 f + sum5 g + sum5 h := by
  simp only [sum5]; ring

lemma sum5_lin (f g h p q : Fin 5 → Rat) :
    sum5 (fun i => f i + g i - h i - p i - q i) =
      sum5 f + sum5 g - sum5 h - sum5 p - sum5 q := by
  simp only [sum5]; ring

lemma sum5_mul (c : Rat) (f : Fin 5 → Rat) : sum5 (fun i => c * f i) = c * sum5 f := by
  simp only [sum5]; ring

lemma sum5_const (c : Rat) : sum5 (fun _ : Fin 5 => c) = 5 * c := by
  simp only [sum5]; ring

theorem y_orth (k : Fin 5) : dot ones (y k) = 0 := by
  fin_cases k <;> simp [dot, sum5, ones, y] <;> norm_num

theorem y_sq (k : Fin 5) : sq (y k) = 1 / 5 := by
  fin_cases k <;> simp [sq, dot, sum5, y] <;> norm_num

theorem ones_sq : sq ones = 5 := by
  simp [sq, dot, sum5, ones]; norm_num

theorem A_symm (k i j : Fin 5) : A k i j = A k j i := by
  by_cases h : i = j
  · simp [A, h]
  · have h' : j ≠ i := fun e => h e.symm
    simp [A, h, h', add_comm]

/-- Entrywise form of `∑ Aₖ = 5 I`. -/
theorem sum_eq_five (i j : Fin 5) :
    sumA i j = (5 : Rat) * (if i = j then 1 else 0) := by
  fin_cases i <;> fin_cases j <;> simp [sumA, madd, A, y] <;> norm_num

theorem kappa_diag (k : Fin 5) : kappa k k = -1 := by
  fin_cases k <;> simp [kappa, y] <;> norm_num

theorem kernel_vec (k i : Fin 5) : mv (A k) (kappa k) i = 0 := by
  fin_cases k <;> fin_cases i <;> simp [mv, sum5, A, kappa, y] <;> norm_num

lemma mv_expand (k : Fin 5) (v : Fin 5 → Rat) (i : Fin 5) :
    mv (A k) v i = v i + dot (y k) v + y k i * dot ones v := by
  fin_cases i <;> simp [mv, A, dot, sum5, ones] <;> ring

lemma quad_formula (k : Fin 5) (v : Fin 5 → Rat) :
    dot v (mv (A k) v) = sq v + 2 * dot ones v * dot (y k) v := by
  simp only [dot, sq, sum5, ones, mv_expand]
  ring

/-- The orthogonal projection of `v` onto `span{1, yₖ}`. -/
def plane (k : Fin 5) (v : Fin 5 → Rat) : Fin 5 → Rat :=
  fun i => dot ones v / 5 + 5 * dot (y k) v * y k i

/-- The component of `v` orthogonal to that plane. -/
def residual (k : Fin 5) (v : Fin 5 → Rat) : Fin 5 → Rat :=
  fun i => v i - plane k v i

lemma dot_plane (k : Fin 5) (v : Fin 5 → Rat) :
    dot v (plane k v) = (dot ones v) ^ 2 / 5 + 5 * (dot (y k) v) ^ 2 := by
  have hs : sum5 v = dot ones v := by simp [dot, ones]
  have ht : sum5 (fun i => v i * y k i) = dot (y k) v := by simp [dot, mul_comm]
  have hfun : ∀ i,
      v i * (dot ones v / 5 + 5 * dot (y k) v * y k i) =
        (dot ones v / 5) * v i + (5 * dot (y k) v) * (v i * y k i) := by
    intro i; ring
  conv_lhs => rw [dot]
  simp only [plane]
  rw [sum5_congr hfun, sum5_add, sum5_mul, sum5_mul, hs, ht]
  ring

lemma sq_plane (k : Fin 5) (v : Fin 5 → Rat) :
    sq (plane k v) = (dot ones v) ^ 2 / 5 + 5 * (dot (y k) v) ^ 2 := by
  have hy0 : sum5 (y k) = 0 := by simpa [dot, ones] using y_orth k
  have hy2 : sum5 (fun i => (y k i) ^ 2) = 1 / 5 := by simpa [sq, dot, pow_two] using y_sq k
  have hfun : ∀ i,
      (dot ones v / 5 + 5 * dot (y k) v * y k i) *
          (dot ones v / 5 + 5 * dot (y k) v * y k i) =
        (dot ones v / 5) ^ 2 + (2 * dot ones v * dot (y k) v) * y k i +
          (25 * (dot (y k) v) ^ 2) * (y k i) ^ 2 := by
    intro i; ring
  conv_lhs => rw [sq, dot]
  simp only [plane]
  rw [sum5_congr hfun, sum5_add3, sum5_const, sum5_mul, sum5_mul, hy0, hy2]
  ring

lemma sq_nonneg (v : Fin 5 → Rat) : 0 ≤ sq v := by
  simp only [sq, dot, sum5]
  exact add_nonneg
    (add_nonneg (add_nonneg (add_nonneg (mul_self_nonneg _) (mul_self_nonneg _))
      (mul_self_nonneg _)) (mul_self_nonneg _))
    (mul_self_nonneg _)

lemma dot_residual_plane (k : Fin 5) (v : Fin 5 → Rat) : dot (residual k v) (plane k v) = 0 := by
  have hs : sum5 v = dot ones v := by simp [dot, ones]
  have ht : sum5 (fun i => v i * y k i) = dot (y k) v := by simp [dot, mul_comm]
  have hy0 : sum5 (y k) = 0 := by simpa [dot, ones] using y_orth k
  have hy2 : sum5 (fun i => (y k i) ^ 2) = 1 / 5 := by simpa [sq, dot, pow_two] using y_sq k
  have hfun : ∀ i,
      (v i - (dot ones v / 5 + 5 * dot (y k) v * y k i)) *
          (dot ones v / 5 + 5 * dot (y k) v * y k i) =
        (dot ones v / 5) * v i + (5 * dot (y k) v) * (v i * y k i) -
          (dot ones v / 5) ^ 2 - (2 * dot ones v * dot (y k) v) * y k i -
          (25 * (dot (y k) v) ^ 2) * (y k i) ^ 2 := by
    intro i; ring
  conv_lhs => rw [dot]
  simp only [residual, plane]
  rw [sum5_congr hfun, sum5_lin, sum5_mul, sum5_mul, sum5_const, sum5_mul, sum5_mul, hs, ht, hy0,
    hy2]
  ring

lemma sq_decompose (k : Fin 5) (v : Fin 5 → Rat) :
    sq v = sq (residual k v) + (dot ones v) ^ 2 / 5 + 5 * (dot (y k) v) ^ 2 := by
  have hsplit : ∀ i, v i = residual k v i + plane k v i := by
    intro i; simp [residual, sub_add_cancel]
  have hexpand :
      sq v = sq (residual k v) + sq (plane k v) + 2 * dot (residual k v) (plane k v) := by
    have hfun : ∀ i, v i * v i =
        residual k v i * residual k v i + plane k v i * plane k v i +
          2 * (residual k v i * plane k v i) := by
      intro i
      rw [hsplit i]
      ring
    conv_lhs => rw [sq, dot]
    rw [sum5_congr hfun, sum5_add3, sum5_mul]
    simp only [sq, dot]
  calc
    sq v = sq (residual k v) + sq (plane k v) + 2 * dot (residual k v) (plane k v) := hexpand
    _ = sq (residual k v) + ((dot ones v) ^ 2 / 5 + 5 * (dot (y k) v) ^ 2) + 2 * 0 := by
      rw [dot_residual_plane, sq_plane]
    _ = sq (residual k v) + (dot ones v) ^ 2 / 5 + 5 * (dot (y k) v) ^ 2 := by ring

lemma quad_sos (k : Fin 5) (v : Fin 5 → Rat) :
    dot v (mv (A k) v) =
      sq (residual k v) + (dot ones v + 5 * dot (y k) v) ^ 2 / 5 := by
  rw [quad_formula, sq_decompose]
  ring

lemma pow_two_nonneg (a : Rat) : 0 ≤ a ^ 2 := by
  rw [pow_two]
  exact mul_self_nonneg a

theorem posSemidef (k : Fin 5) (v : Fin 5 → Rat) : 0 ≤ dot v (mv (A k) v) := by
  rw [quad_sos]
  exact add_nonneg (sq_nonneg _) (div_nonneg (pow_two_nonneg _) (by norm_num))

lemma rat_mul_self_zero {a : Rat} (h : a * a = 0) : a = 0 :=
  (Rat.mul_eq_zero.mp h).elim id id

lemma sq_eq_zero {v : Fin 5 → Rat} (h : sq v = 0) : ∀ i, v i = 0 := by
  have h' : v 0 * v 0 + v 1 * v 1 + v 2 * v 2 + v 3 * v 3 + v 4 * v 4 = 0 := by
    simpa [sq, dot, sum5] using h
  have z0 : v 0 * v 0 = 0 := by
    linarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2),
      mul_self_nonneg (v 3), mul_self_nonneg (v 4)]
  have z1 : v 1 * v 1 = 0 := by
    linarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2),
      mul_self_nonneg (v 3), mul_self_nonneg (v 4)]
  have z2 : v 2 * v 2 = 0 := by
    linarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2),
      mul_self_nonneg (v 3), mul_self_nonneg (v 4)]
  have z3 : v 3 * v 3 = 0 := by
    linarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2),
      mul_self_nonneg (v 3), mul_self_nonneg (v 4)]
  have z4 : v 4 * v 4 = 0 := by
    linarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2),
      mul_self_nonneg (v 3), mul_self_nonneg (v 4)]
  intro i
  fin_cases i
  · exact rat_mul_self_zero z0
  · exact rat_mul_self_zero z1
  · exact rat_mul_self_zero z2
  · exact rat_mul_self_zero z3
  · exact rat_mul_self_zero z4

theorem kernel_line (k : Fin 5) (v : Fin 5 → Rat) (h : dot v (mv (A k) v) = 0) :
    ∀ i, v i = (dot ones v / 5) * kappa k i := by
  have hid := quad_sos k v
  rw [h] at hid
  have hsum : sq (residual k v) + (dot ones v + 5 * dot (y k) v) ^ 2 / 5 = 0 := hid.symm
  have hden : (0 : Rat) ≤ 5 := by norm_num
  have hres0 : sq (residual k v) = 0 := by
    linarith [hsum, sq_nonneg (residual k v),
      div_nonneg (pow_two_nonneg (dot ones v + 5 * dot (y k) v)) hden]
  have hcross0 : (dot ones v + 5 * dot (y k) v) ^ 2 / 5 = 0 := by
    linarith [hsum, sq_nonneg (residual k v),
      div_nonneg (pow_two_nonneg (dot ones v + 5 * dot (y k) v)) hden]
  have hsq0 : (dot ones v + 5 * dot (y k) v) ^ 2 = 0 := by
    have h5 : (5 : Rat) ≠ 0 := by norm_num
    rw [← Rat.div_mul_cancel (a := (dot ones v + 5 * dot (y k) v) ^ 2) h5, hcross0, Rat.zero_mul]
  have hlin : dot ones v + 5 * dot (y k) v = 0 :=
    rat_mul_self_zero (by simpa [pow_two] using hsq0)
  have ht : dot (y k) v = -(dot ones v) / 5 := by
    have h5 : (5 : Rat) ≠ 0 := by norm_num
    have hmul : (5 * dot (y k) v) / 5 = dot (y k) v := by
      rw [mul_comm]
      exact Rat.mul_div_cancel h5
    have h5t : 5 * dot (y k) v = -(dot ones v) := by linarith
    rw [← hmul, h5t]
  have hres : ∀ i, residual k v i = 0 := sq_eq_zero hres0
  intro i
  have hv : v i = dot ones v / 5 + 5 * dot (y k) v * y k i := by
    have hr : v i - (dot ones v / 5 + 5 * dot (y k) v * y k i) = 0 := by
      simpa [residual, plane] using hres i
    linarith
  rw [ht] at hv
  calc
    v i = dot ones v / 5 + 5 * (-(dot ones v) / 5) * y k i := hv
    _ = (dot ones v / 5) * (1 - 5 * y k i) := by ring
    _ = (dot ones v / 5) * kappa k i := by simp [kappa]

end RRExact
