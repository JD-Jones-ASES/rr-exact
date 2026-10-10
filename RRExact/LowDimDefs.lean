module

public import Mathlib.Analysis.CStarAlgebra.Matrix
public import Mathlib.Analysis.Complex.Order
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.LinearAlgebra.Matrix.Notation
public import Mathlib.NumberTheory.Zsqrtd.GaussianInt
public import RRExact.Perms

@[expose] public section

open scoped Matrix.Norms.L2Operator ComplexOrder
open Matrix

namespace RRExact.LowDim

noncomputable section

set_option maxHeartbeats 0
set_option maxRecDepth 100000

/-- The ordered product associated with a permutation tuple. -/
def word {n K : Type*} [Fintype n] [Semiring K]
    (A : Fin 5 → Matrix n n K) (p : Perm5) : Matrix n n K :=
  A (coords p 0) * A (coords p 1) * A (coords p 2) * A (coords p 3) * A (coords p 4)

/-- The sum over the certified complete list of the 120 permutations. -/
def total {n K : Type*} [Fintype n] [Semiring K]
    (A : Fin 5 → Matrix n n K) : Matrix n n K :=
  (perms.map (word A)).sum

/-- The full random-reshuffling average for five factors. -/
def average {n K : Type*} [Fintype n] [Field K]
    (A : Fin 5 → Matrix n n K) : Matrix n n K :=
  (1 / 120 : K) • total A

/-- The arithmetic mean of the five matrices. -/
def mean {n K : Type*} [Fintype n] [Field K]
    (A : Fin 5 → Matrix n n K) : Matrix n n K :=
  (1 / 5 : K) • ∑ k, A k

/-- Five explicit symmetric integer matrices in dimension three, regarded over the reals. -/
def realFamily : Fin 5 → Matrix (Fin 3) (Fin 3) ℝ
  | 0 => !![25, 20, 0; 20, 16, 0; 0, 0, 16]
  | 1 => !![25, -20, 0; -20, 16, 0; 0, 0, 16]
  | 2 => !![25, 0, 20; 0, 16, 0; 20, 0, 16]
  | 3 => !![25, 0, -20; 0, 16, 0; -20, 0, 16]
  | 4 => !![0, 0, 0; 0, 36, 0; 0, 0, 36]

/-- Integer Gram factors for the real family. -/
def realRoot : Fin 5 → Matrix (Fin 2) (Fin 3) ℝ
  | 0 => !![5, 4, 0; 0, 0, 4]
  | 1 => !![5, -4, 0; 0, 0, 4]
  | 2 => !![5, 0, 4; 0, 4, 0]
  | 3 => !![5, 0, -4; 0, 4, 0]
  | 4 => !![0, 6, 0; 0, 0, 6]

/-- The five Gaussian-integer column vectors for the complex rank-one family. -/
def complexVector : Fin 5 → Fin 2 → ℂ
  | 0 => ![5, 4]
  | 1 => ![5, -4]
  | 2 => ![5, 4 * Complex.I]
  | 3 => ![5, -4 * Complex.I]
  | 4 => ![0, 6]

/-- Five explicit Hermitian Gaussian-integer matrices in dimension two. -/
def complexFamily (k : Fin 5) : Matrix (Fin 2) (Fin 2) ℂ :=
  vecMulVec (complexVector k) (star (complexVector k))

/-- Integer arithmetic model of the real witness, for kernel reduction. -/
def realInt : Fin 5 → Matrix (Fin 3) (Fin 3) ℤ
  | 0 => !![25, 20, 0; 20, 16, 0; 0, 0, 16]
  | 1 => !![25, -20, 0; -20, 16, 0; 0, 0, 16]
  | 2 => !![25, 0, 20; 0, 16, 0; 20, 0, 16]
  | 3 => !![25, 0, -20; 0, 16, 0; -20, 0, 16]
  | 4 => !![0, 0, 0; 0, 36, 0; 0, 0, 36]

/-- Gaussian-integer arithmetic model of the complex witness. -/
def complexInt : Fin 5 → Matrix (Fin 2) (Fin 2) GaussianInt
  | 0 => !![25, 20; 20, 16]
  | 1 => !![25, -20; -20, 16]
  | 2 => !![25, ⟨0, -20⟩; ⟨0, 20⟩, 16]
  | 3 => !![25, ⟨0, 20⟩; ⟨0, -20⟩, 16]
  | 4 => !![0, 0; 0, 36]


end

end RRExact.LowDim
