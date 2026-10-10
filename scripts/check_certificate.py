#!/usr/bin/env python3
"""Exact rational certificate for the De Sa family at n = 5.

Checks, over the rationals, that the five matrices below are symmetric,
have the displayed kernel vectors, sum to 5 I, and that the average over S_5 of their
ordered products is exactly (29/64) I - (21/64) 11^T. The eigenvalues of that
matrix are -19/16 (multiplicity 1) and 29/64 (multiplicity 4), so its operator
norm is 19/16.

The quadratic-form checks use three selected vectors; they are regression
controls, not a proof of positive semidefiniteness for every vector. The PSD
proof is in RRExact/PSD.lean and the mathematical argument in PROOF.md.

Also checks the age recurrence that sends the all-ones vector to a_n times
itself, for every n from 2 through 40, against the second-order recurrence.
"""

from fractions import Fraction
from itertools import permutations
import sys

def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def matvec(A, v):
    return [dot(row, v) for row in A]

def zeros(n):
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]

def eye(n):
    A = zeros(n)
    for i in range(n):
        A[i][i] = Fraction(1)
    return A

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def scale(c, A):
    n = len(A)
    return [[c * A[i][j] for j in range(n)] for i in range(n)]

def mul(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            aik = A[i][k]
            row = B[k]
            crow = C[i]
            for j in range(n):
                crow[j] += aik * row[j]
    return C

def y_vectors(n):
    """Rational De Sa vectors. Requires sqrt(n - 1) to be an integer."""
    s = n - 1
    root = int(s ** 0.5)
    if root * root != s:
        fail(f"sqrt({s}) is not an integer")
    ys = []
    for k in range(n):
        y = [Fraction(-1, n * root) for _ in range(n)]
        y[k] = Fraction(root, n)
        ys.append(y)
    return ys

def matrices_from(ys):
    n = len(ys)
    ones_row = [Fraction(1) for _ in range(n)]
    As = []
    for y in ys:
        A = eye(n)
        # A = I + 1 y^T + y 1^T
        for i in range(n):
            for j in range(n):
                A[i][j] += y[j] + y[i]
        As.append(A)
    return As

def age_factor(n):
    """a_n from the age recurrence. Returns (a_0..a_n, S_0..S_n)."""
    rho = Fraction(-1, n * (n - 1))
    a = Fraction(1)
    S = Fraction(0)
    out_a = [a]
    out_S = [S]
    for _ in range(n):
        a_prev = a
        a = a_prev + rho * S
        S = S + n * a_prev
        out_a.append(a)
        out_S.append(S)
    return out_a, out_S

def second_order(n):
    """a_n from (n-1) a_{t+1} = 2(n-1) a_t - n a_{t-1}, a_0 = a_1 = 1."""
    c = Fraction(n, n - 1)
    seq = [Fraction(1), Fraction(1)]
    for _ in range(1, n):
        seq.append(2 * seq[-1] - c * seq[-2])
    return seq[-1]

def check_family(n):
    ys = y_vectors(n)
    ones = [Fraction(1) for _ in range(n)]
    # sum y = 0, common squared length 1/n, common distinct inner product
    for y in ys:
        if dot(y, ones) != 0:
            fail(f"n={n}: y not orthogonal to 1")
        if dot(y, y) != Fraction(1, n):
            fail(f"n={n}: ||y||^2 != 1/n")
    total_y = [Fraction(0) for _ in range(n)]
    for y in ys:
        total_y = [total_y[i] + y[i] for i in range(n)]
    if any(c != 0 for c in total_y):
        fail(f"n={n}: sum y != 0")
    rho = dot(ys[0], ys[1])
    if rho != Fraction(-1, n * (n - 1)):
        fail(f"n={n}: pairwise inner product {rho}")

    As = matrices_from(ys)
    # symmetry, kernel, sum, quadratic-form identity
    S = zeros(n)
    for k, A in enumerate(As):
        for i in range(n):
            for j in range(n):
                if A[i][j] != A[j][i]:
                    fail(f"n={n}: A_{k} not symmetric")
        kappa = [ones[i] - n * ys[k][i] for i in range(n)]
        if any(c != 0 for c in matvec(A, kappa)):
            fail(f"n={n}: kernel vector is not a kernel vector")
        # v^T A v = ||v||^2 + 2 (1·v)(y·v), and that is (1/n)(1·v + n y·v)^2
        # plus a sum of squares. Check the algebraic identity on the basis
        # and on kappa (already zero) and on ones.
        y = ys[k]
        for v in (ones, y, [Fraction(i + 1) for i in range(n)]):
            Av = matvec(A, v)
            quad = dot(v, Av)
            s = dot(ones, v)
            t = dot(y, v)
            claimed = dot(v, v) + 2 * s * t
            if quad != claimed:
                fail(f"n={n}: quadratic expansion")
            # nonnegativity: claimed - (s + n t)^2 / n = ||v||^2 - s^2/n - n t^2
            gap = claimed - (s + n * t) ** 2 / n
            if gap < 0:
                fail(f"n={n}: quadratic form negative")
            # gap must equal the squared distance to span{1, y}
            # ||v||^2 - s^2/||1||^2 - t^2/||y||^2 = ||v||^2 - s^2/n - n t^2
            if gap != dot(v, v) - s ** 2 / n - n * t * t:
                fail(f"n={n}: gap identity")
        S = add(S, A)
    if S != scale(n, eye(n)):
        fail(f"n={n}: sum of matrices is not {n} I")
    return ys, As

def check_n5_products(As):
    n = 5
    total = zeros(n)
    count = 0
    for perm in permutations(range(n)):
        P = eye(n)
        for k in perm:
            P = mul(P, As[k])
        total = add(total, P)
        count += 1
    if count != 120:
        fail("permutation count")
    rr = scale(Fraction(1, 120), total)
    J = [[Fraction(1) for _ in range(n)] for _ in range(n)]
    expected = add(scale(Fraction(29, 64), eye(n)), scale(Fraction(-21, 64), J))
    if rr != expected:
        fail("reshuffled mean is not (29/64) I - (21/64) J")
    # spectrum of beta I + gamma J
    beta = Fraction(29, 64)
    gamma = Fraction(-21, 64)
    on_ones = beta + n * gamma
    if on_ones != Fraction(-19, 16):
        fail("all-ones eigenvalue")
    if abs(on_ones) != Fraction(19, 16) or abs(beta) >= Fraction(19, 16):
        fail("operator norm is not 19/16")
    # direct action on the all-ones vector
    ones = [Fraction(1)] * n
    image = matvec(rr, ones)
    if image != [Fraction(-19, 16)] * n:
        fail("rr 1 != (-19/16) 1")
    print("n=5 matrix identity: rr_5 = (29/64) I - (21/64) 11^T")
    print("spectrum: -19/16 (once), 29/64 (four times)")
    print("operator norm: 19/16")

def main():
    for n in (5, 10):
        ys, As = check_family(n)
        a, S = age_factor(n)
        if a[-1] != second_order(n):
            fail(f"n={n}: recurrences disagree")
        print(f"n={n}: symmetry, kernel, sum = {n} I, selected-vector controls; a_n = {a[-1]}")
        if n == 5:
            if a[-1] != Fraction(-19, 16):
                fail("a_5")
            # age table printed in PROOF.md
            expected_a = [
                Fraction(1),
                Fraction(1),
                Fraction(3, 4),
                Fraction(1, 4),
                Fraction(-7, 16),
                Fraction(-19, 16),
            ]
            expected_S = [
                Fraction(0),
                Fraction(5),
                Fraction(10),
                Fraction(55, 4),
                Fraction(15),
                Fraction(205, 16),
            ]
            if a != expected_a or S != expected_S:
                fail(f"age steps a={a} S={S}")
            check_n5_products(As)
        if n == 10 and a[-1] != Fraction(-99712, 59049):
            fail("a_10")

    print("a_n for 2 <= n <= 40 (mark |a_n| > 1):")
    first = None
    for n in range(2, 41):
        val = second_order(n)
        if val != age_factor(n)[0][-1]:
            fail(f"recurrence mismatch at {n}")
        flag = abs(val) > 1
        if flag and first is None:
            first = n
        mark = ">" if flag else " "
        print(f"  {n:2d} {mark} {val}")
    if first != 5:
        fail("first violation is not n=5")
    print("first n with |a_n| > 1 is 5")
    print("certificate ok")

if __name__ == "__main__":
    main()
