#!/usr/bin/env python3
"""Exact certificate for five rank-one Hermitian 2-by-2 counterexample matrices.

The input matrices have Gaussian-integer entries.  Each is checked against an
explicit outer product v v*, which certifies positive semidefiniteness and rank
one.  All 120 ordered products are enumerated independently of the Lean proof.

Only Python's standard library is used.  Every verification uses integer or
Fraction arithmetic.  Checks remain active under ``python3 -O``.
"""

from fractions import Fraction
from itertools import permutations


def require(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)


# A Gaussian integer is (real part, imaginary part); matrices are row-major.
def gaussian_add(z, w):
    return (z[0] + w[0], z[1] + w[1])


def gaussian_mul(z, w):
    return (z[0] * w[0] - z[1] * w[1],
            z[0] * w[1] + z[1] * w[0])


def gaussian_conj(z):
    return (z[0], -z[1])


def matrix_add(a, b):
    return tuple(gaussian_add(z, w) for z, w in zip(a, b))


def matrix_mul(a, b):
    return tuple(
        gaussian_add(gaussian_mul(a[2 * i], b[j]),
                     gaussian_mul(a[2 * i + 1], b[2 + j]))
        for i in range(2) for j in range(2)
    )


def outer_product(v):
    return tuple(gaussian_mul(v[i], gaussian_conj(v[j]))
                 for i in range(2) for j in range(2))


ZERO = ((0, 0),) * 4
IDENTITY = ((1, 0), (0, 0), (0, 0), (1, 0))

MATRICES = (
    ((25, 0), (20, 0), (20, 0), (16, 0)),
    ((25, 0), (-20, 0), (-20, 0), (16, 0)),
    ((25, 0), (0, -20), (0, 20), (16, 0)),
    ((25, 0), (0, 20), (0, -20), (16, 0)),
    ((0, 0), (0, 0), (0, 0), (36, 0)),
)

GRAM_VECTORS = (
    ((5, 0), (4, 0)),
    ((5, 0), (-4, 0)),
    ((5, 0), (0, 4)),
    ((5, 0), (0, -4)),
    ((0, 0), (6, 0)),
)


def verify():
    require(len(MATRICES) == len(GRAM_VECTORS) == 5,
            "The certificate must contain five matrices and five factors.")
    for index, (matrix, vector) in enumerate(zip(MATRICES, GRAM_VECTORS), 1):
        require(any(z != (0, 0) for z in vector),
                "Gram vector {} must be nonzero.".format(index))
        require(matrix == outer_product(vector),
                "Gram factorization failed for matrix {}.".format(index))
        require(matrix[0][1] == matrix[3][1] == 0
                and matrix[1] == gaussian_conj(matrix[2]),
                "Matrix {} is not Hermitian.".format(index))

    total = ZERO
    for matrix in MATRICES:
        total = matrix_add(total, matrix)
    require(total == ((100, 0), (0, 0), (0, 0), (100, 0)),
            "The sum must be exactly 100 I.")

    product_sum = ZERO
    count = 0
    for permutation in permutations(range(5)):
        product = IDENTITY
        for index in permutation:
            product = matrix_mul(product, MATRICES[index])
        product_sum = matrix_add(product_sum, product)
        count += 1
    require(count == 120, "Exactly 120 ordered products must be enumerated.")
    require(product_sum == ((-396633600, 0), (0, 0),
                            (0, 0), (-353018880, 0)),
            "The exact ordered-product sum differs from the certificate.")

    average = tuple((Fraction(z[0], count), Fraction(z[1], count))
                    for z in product_sum)
    require(average == ((-3305280, 0), (0, 0), (0, 0), (-2941824, 0)),
            "The exact average differs from the claimed diagonal matrix.")
    average_norm = max(abs(average[0][0]), abs(average[3][0]))
    mean_norm = Fraction(total[0][0], 5)
    require(mean_norm == 20, "The mean matrix must have norm 20.")
    ratio = average_norm / mean_norm ** 5
    require(ratio == Fraction(10329, 10000),
            "The exact operator-norm ratio is incorrect.")
    require(ratio > 1, "The operator-norm inequality must be strictly violated.")
    require(average[0][0] / mean_norm ** 5 == Fraction(-10329, 10000),
            "The first normalized eigenvalue is incorrect.")
    require(average[3][0] / mean_norm ** 5 == Fraction(-22983, 25000),
            "The second normalized eigenvalue is incorrect.")

    print("PASS: all five explicit nonzero rank-one Gram factors verified.")
    print("PASS: each input is Hermitian positive semidefinite; sum = 100 I.")
    print("PASS: 120 Gaussian-integer ordered products enumerated exactly.")
    print("Exact product sum: diag(-396633600, -353018880).")
    print("Exact average: diag(-3305280, -2941824).")
    print("Normalized spectrum: -10329/10000, -22983/25000.")
    print("Exact operator-norm ratio: {} > 1.".format(ratio))
    print("Field: complex Hermitian 2-by-2 matrices.")


if __name__ == "__main__":
    verify()
