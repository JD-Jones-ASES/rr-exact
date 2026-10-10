#!/usr/bin/env python3
"""Independent exact finite controls for the restricted real 2x2 family.

Enumerate every labeled permutation at n=4,...,8 using ordinary multiplication.
Entries are integer pairs a+b*sqrt(D), with D=2(n-2). This is not the subset
or Jordan recurrence and uses no floating point or external package. The
general theorem is proved by counting in note/REAL_2X2_PROBE.md.
"""
from fractions import Fraction as F
from itertools import permutations
from math import factorial


def require(condition, explanation):
    if not condition:
        raise ArithmeticError(explanation)


def add(z, w):
    return (z[0]+w[0], z[1]+w[1])


def mul(z, w, d):
    return (z[0]*w[0]+d*z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def matrix_add(a, b):
    return tuple(add(z, w) for z, w in zip(a, b))


def matrix_mul(a, b, d):
    return tuple(add(mul(a[2*i], b[j], d), mul(a[2*i+1], b[2+j], d))
                 for i in range(2) for j in range(2))


ZERO = ((0, 0),)*4
IDENTITY = ((1, 0), (0, 0), (0, 0), (1, 0))


def check(n):
    m, d, scale = n-3, 2*(n-2), 4*(n-2)
    # These are the attaining matrices, multiplied by scale. All coefficients
    # are now integers in the quadratic algebra with generator sqrt(d).
    matrices = [
        ((n*(n-2), 0), (0, n), (0, n), (2*n, 0)),
        ((n*(n-2), 0), (0, -n), (0, -n), (2*n, 0)),
        ((2*n*(n-2), 0), (0, 0), (0, 0), (0, 0)),
    ] + [((0, 0), (0, 0), (0, 0), (4*n, 0))]*m
    require(len(matrices) == n, "number of labeled factors")
    for matrix in matrices:
        require(matrix[1] == matrix[2], "symmetry")
        require(matrix[0][1] == matrix[3][1] == 0, "rational diagonal")
        require(matrix[0][0] >= 0 and matrix[3][0] >= 0, "nonnegative diagonal")
        require(mul(matrix[0], matrix[3], d) == mul(matrix[1], matrix[2], d),
                "rank-one determinant identity")
        require(matrix != ZERO, "nonzero rank-one input")

    total = ZERO
    for matrix in matrices:
        total = matrix_add(total, matrix)
    require(total == ((n*scale, 0), (0, 0), (0, 0), (n*scale, 0)), "mean = scale I")

    product_sum, count = ZERO, 0
    for ordering in permutations(range(n)):
        product = IDENTITY
        for index in ordering:
            product = matrix_mul(product, matrices[index], d)
        product_sum = matrix_add(product_sum, product)
        count += 1
    require(count == factorial(n), "all labeled permutations counted")
    q1 = -F(n**(n-1), 4*(n-1)*(n-2)**(n-1))
    q2 = -F(n**(n-1), 8*(n-1)*(n-2)**(n-2))
    expected = ((q1*count*scale**n, 0), (0, 0),
                (0, 0), (q2*count*scale**n, 0))
    require(product_sum == expected, "independent exact product formula at n={}".format(n))
    require(0 < -q2 < 1 and abs(q1) <= -q2, "finite norm and nonviolation control")
    print("PASS: n={}, {} labeled products; exact norm {}.".format(n, count, -q2))


if __name__ == "__main__":
    for size in range(4, 9):
        check(size)
    print("All finite real 2x2 family controls passed; general proof is in the note.")
