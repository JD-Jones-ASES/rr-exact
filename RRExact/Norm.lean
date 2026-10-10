module

import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

public import RRExact.PSD

@[expose] public section

namespace RRExact

lemma mv_closed (v : Fin 5 → Rat) (i : Fin 5) :
    mv closed v i = (29 / 64) * v i - (21 / 64) * sum5 v := by
  fin_cases i <;> simp [mv, closed, sum5] <;> ring

lemma variance (v : Fin 5 → Rat) :
    sum5 (fun i => sum5 (fun j => (v i - v j) ^ 2)) = 10 * sq v - 2 * (sum5 v) ^ 2 := by
  simp only [sum5, sq, dot]
  ring

lemma sum_sq_nonneg (v : Fin 5 → Rat) :
    0 ≤ sum5 (fun i => sum5 (fun j => (v i - v j) ^ 2)) := by
  simp only [sum5]
  positivity

lemma cauchy_ones (v : Fin 5 → Rat) : (sum5 v) ^ 2 ≤ 5 * sq v := by
  have hnonneg := sum_sq_nonneg v
  rw [variance] at hnonneg
  linarith

lemma closed_identity (v : Fin 5 → Rat) :
    (361 / 256) * sq v - sq (mv closed v) = (987 / 4096) * (5 * sq v - (sum5 v) ^ 2) := by
  have h := fun i => mv_closed v i
  simp only [sq, dot, sum5] at h ⊢
  simp_rw [h]
  ring

theorem closed_bound (v : Fin 5 → Rat) : sq (mv closed v) * 256 ≤ 361 * sq v := by
  have hid := closed_identity v
  have hc := cauchy_ones v
  have hcoef : (0 : Rat) ≤ 987 / 4096 := by norm_num
  have hgap : 0 ≤ (361 / 256) * sq v - sq (mv closed v) := by
    rw [hid]
    exact mul_nonneg hcoef (by linarith)
  linarith

theorem closed_attained :
    (mv closed ones = fun _ => (-19 / 16 : Rat)) ∧
      (sq (mv closed ones) * 256 = 361 * sq ones) ∧ sq ones = 5 ∧
      ((19 / 16 : Rat) ^ 2 = 361 / 256) := by
  refine ⟨?_, ?_, ones_sq, ?_⟩
  · ext i
    rw [mv_closed]
    simp [ones, sum5]
    norm_num
  · have h : mv closed ones = fun _ => (-19 / 16 : Rat) := by
      ext i
      rw [mv_closed]
      simp [ones, sum5]
      norm_num
    simp only [sq, dot, sum5, ones, h]
    norm_num
  · norm_num

end RRExact
