#!/usr/bin/env python3
"""Emit RRExact/Perms.lean, the explicit list of S_5."""

from itertools import permutations
from pathlib import Path

rows = ",\n".join(
    f"  ({', '.join(str(i) for i in p)})" for p in permutations(range(5))
)
text = f"""module

public import RRExact.Defs

@[expose] public section

namespace RRExact

/-!
The 120 ordered tuples. `perms_spec_aux` checks that the list is duplicate-free and contains a
tuple if and only if that tuple is a permutation.
-/

def perms : List Perm5 := [
{rows}
]

def sumList : List Perm5 → Mat
  | [] => mzero
  | p :: ps => madd (prod5 p) (sumList ps)

def reshuffle : Mat :=
  fun i j => sumList perms i j / 120

end RRExact
"""
path = Path(__file__).resolve().parents[1] / "RRExact" / "Perms.lean"
path.write_text(text)
print(f"wrote {path}")
