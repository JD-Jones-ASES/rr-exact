#!/usr/bin/env python3
"""Emit the rational matrix certificate: literal factors, products, and the sum."""

from fractions import Fraction
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "RRExact"
N = 5


def fmt(q: Fraction) -> str:
    return f"({q.numerator} / {q.denominator})"


def factor(k: int):
    mat = []
    for i in range(N):
        row = []
        for j in range(N):
            yi = Fraction(2, 5) if i == k else Fraction(-1, 10)
            yj = Fraction(2, 5) if j == k else Fraction(-1, 10)
            row.append((1 if i == j else 0) + yj + yi)
        mat.append(row)
    return mat


def mm(a, b):
    return [
        [sum((a[i][t] * b[t][j] for t in range(N)), Fraction(0)) for j in range(N)]
        for i in range(N)
    ]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(N)] for i in range(N)]


def emit_mat(name: str, mat) -> str:
    lines = [f"def {name} : Mat"]
    for i in range(N):
        for j in range(N):
            lines.append(f"  | {i}, {j} => {fmt(mat[i][j])}")
    return "\n".join(lines)


HEADER = """module

import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

public import RRExact.Lits

@[expose] public section

namespace RRExact

set_option maxHeartbeats 0
"""


def main() -> None:
    lits = [factor(k) for k in range(N)]
    perms = list(permutations(range(N)))
    zero = [[Fraction(0) for _ in range(N)] for _ in range(N)]
    total = [row[:] for row in zero]
    products = []
    for perm in perms:
        cur = lits[perm[0]]
        steps = []
        acc_name = f"lit{perm[0]}"
        for step, idx in enumerate(perm[1:], start=1):
            cur = mm(cur, lits[idx])
            out = f"m{len(products)}_{step}"
            steps.append((out, acc_name, f"lit{idx}", cur))
            acc_name = out
        products.append((perm, steps, cur))
        total = madd(total, cur)

    closed = []
    for i in range(N):
        row = []
        for j in range(N):
            diag = Fraction(29, 64) if i == j else 0
            row.append(diag + Fraction(-21, 64))
        closed.append(row)
    for i in range(N):
        for j in range(N):
            if total[i][j] / 120 != closed[i][j]:
                raise SystemExit(f"average mismatch at {i},{j}: {total[i][j] / 120}")

    lit_body = [
        "module",
        "",
        "import Mathlib.Data.Fintype.Basic",
        "import Mathlib.Tactic.FinCases",
        "import Mathlib.Tactic.NormNum",
        "",
        "public import RRExact.Defs",
        "",
        "@[expose] public section",
        "",
        "namespace RRExact",
        "",
        "set_option maxHeartbeats 0",
        "",
    ]
    for k, mat in enumerate(lits):
        lit_body.append(emit_mat(f"lit{k}", mat))
        lit_body.append("")
        lit_body.append(
            f"theorem A_lit{k} : A {k} = lit{k} := by\n"
            f"  ext i j\n"
            f"  fin_cases i <;> fin_cases j <;> simp only [A, y, lit{k}] <;> norm_num\n"
        )
    lit_body.append("end RRExact\n")
    (ROOT / "Lits.lean").write_text("\n".join(lit_body))

    chunks = 8
    size = len(products) // chunks
    for c in range(chunks):
        block = products[c * size : (c + 1) * size]
        parts = [HEADER]
        for n, (perm, steps, _final) in enumerate(block, start=c * size):
            for out, left, right, mat in steps:
                parts.append(emit_mat(out, mat))
                parts.append("")
                parts.append(
                    f"theorem mul_{out} : mmul {left} {right} = {out} := by\n"
                    f"  ext i j\n"
                    f"  fin_cases i <;> fin_cases j <;>\n"
                    f"    simp only [mmul, sum5, {left}, {right}, {out}] <;> norm_num\n"
                )
            tup = ", ".join(str(i) for i in perm)
            rw_lits = ", ".join(f"A_lit{i}" for i in perm)
            rw_muls = ", ".join(f"mul_{out}" for out, *_ in steps)
            final = steps[-1][0]
            parts.append(
                f"theorem prod_{n} : prod5 ({tup}) = {final} := by\n"
                f"  simp only [prod5, coords]\n"
                f"  rw [{rw_lits}]\n"
                f"  rw [{rw_muls}]\n"
            )
        parts.append("end RRExact\n")
        (ROOT / f"Cert{c}.lean").write_text("\n".join(parts))
        print(f"wrote Cert{c}.lean ({len(block)} permutations)")

    # Grand total and the sum over the explicit list.
    sum_parts = [
        "module",
        "",
        "import Mathlib.Data.Fintype.Basic",
        "import Mathlib.Tactic.FinCases",
        "import Mathlib.Tactic.NormNum",
        "",
        "public import RRExact.Perms",
    ]
    for c in range(chunks):
        sum_parts.append(f"public import RRExact.Cert{c}")
    sum_parts += [
        "",
        "@[expose] public section",
        "",
        "namespace RRExact",
        "",
        "set_option maxHeartbeats 0",
        "",
        emit_mat("grand", total),
        "",
    ]
    # Ten-permutation blocks of the final matrices, summed by norm_num.
    block = 10
    chunk_names = []
    for b in range(0, len(products), block):
        names = [products[n][1][-1][0] for n in range(b, b + block)]
        cname = f"chunk{b // block}"
        chunk_names.append(cname)
        acc = zero
        for n in range(b, b + block):
            acc = madd(acc, products[n][2])
        sum_parts.append(emit_mat(cname, acc))
        sum_parts.append("")
        joined = ", ".join(names)
        simp_names = ", ".join(names + [cname])
        sum_parts.append(
            f"theorem {cname}_sum : madd {names[0]} (madd {names[1]} (madd {names[2]} "
            f"(madd {names[3]} (madd {names[4]} (madd {names[5]} (madd {names[6]} "
            f"(madd {names[7]} (madd {names[8]} {names[9]})))))))) = {cname} := by\n"
            f"  ext i j\n"
            f"  fin_cases i <;> fin_cases j <;> simp only [madd, {simp_names}] <;> norm_num\n"
        )
    # Sum of the twelve chunks.
    expr = chunk_names[-1]
    for name in reversed(chunk_names[:-1]):
        expr = f"madd {name} ({expr})"
    # That is madd c0 (madd c1 (... c11)). Build it nested the same way.
    nested = chunk_names[0]
    for name in chunk_names[1:]:
        nested = f"madd {nested} {name}"
    # nested is left-associated: madd (madd c0 c1) c2 ... which is NOT what I wrote.
    # Use right fold to match a simple recursive reading, and prove it equals grand directly.
    right = chunk_names[-1]
    for name in reversed(chunk_names[:-1]):
        right = f"madd {name} ({right})"
    simp_chunks = ", ".join(chunk_names)
    sum_parts.append(
        f"theorem chunks_sum : {right} = grand := by\n"
        f"  ext i j\n"
        f"  fin_cases i <;> fin_cases j <;> simp only [madd, {simp_chunks}, grand] <;> norm_num\n"
    )
    rw_prods = ", ".join(f"prod_{n}" for n in range(len(products)))
    finals = ", ".join(products[n][1][-1][0] for n in range(len(products)))
    # Right-associated `sumList` becomes the nested `madd` of the final matrices.
    # Adding those matrices entrywise is faster than rewriting the ten-matrix chunks.
    sum_parts.append(
        f"""
theorem sumList_perms : sumList perms = grand := by
  simp only [sumList, perms]
  rw [{rw_prods}]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp only [madd, mzero, grand, {finals}] <;> norm_num
"""
    )
    sum_parts.append(
        """
theorem reshuffle_eq : reshuffle = closed := by
  have hsum := sumList_perms
  ext i j
  fin_cases i <;> fin_cases j <;> simp only [reshuffle, hsum, grand, closed] <;> norm_num
"""
    )
    sum_parts.append("end RRExact\n")
    (ROOT / "Shuffle.lean").write_text("\n".join(sum_parts))
    print("wrote Lits.lean, Shuffle.lean, certificate chunks")
    print("grand 0 0", total[0][0], "average", total[0][0] / 120)


if __name__ == "__main__":
    main()
