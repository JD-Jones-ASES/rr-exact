#!/usr/bin/env python3
"""Dependency-free exact checks for the real 3 x 3 counterexamples.

This is a rational/polynomial certificate, not the Lean kernel check.  All
comparisons remain active under python -O.  The symbolic identity is checked
coefficient by coefficient by enumerating the 120 products; the numerical
discovery software and floating point are not used.
"""

from fractions import Fraction as F
from itertools import permutations
from math import factorial


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def zero(n):
    return [[0 for _ in range(n)] for _ in range(n)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def mul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def outer(v):
    return [[x * y for y in v] for x in v]


def diag(values):
    return [[values[i] if i == j else 0 for j in range(len(values))]
            for i in range(len(values))]


def ordered_sum(matrices, second_moment=False):
    """Enumerate labeled permutations, including when some factors coincide."""
    n, d = len(matrices), len(matrices[0])
    out = zero(d)
    count = 0
    for order in permutations(range(n)):
        p = eye(d)
        for i in order:
            p = mul(p, matrices[i])
        out = add(out, mul(transpose(p), p) if second_moment else p)
        count += 1
    require(count == factorial(n), "permutation count")
    return out


def subset_sum(matrices):
    """Independent recurrence: append the last labeled factor to each word."""
    n, d = len(matrices), len(matrices[0])
    memo = [eye(d)]
    for mask in range(1, 1 << n):
        total = zero(d)
        for i in range(n):
            if mask & (1 << i):
                total = add(total, mul(memo[mask ^ (1 << i)], matrices[i]))
        memo.append(total)
    return memo[-1]


def family(a, b, t, d, c):
    return [
        [[a, b, 0], [b, t, 0], [0, 0, d]],
        [[a, -b, 0], [-b, t, 0], [0, 0, d]],
        [[a, 0, b], [0, d, 0], [b, 0, t]],
        [[a, 0, -b], [0, d, 0], [-b, 0, t]],
        diag([0, c, c]),
    ]


class Poly:
    """Sparse polynomials over Q in (a,b,t,d,c), for exact coefficient checks."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {k: F(v) for k, v in value.items() if v}
        else:
            self.terms = {(0, 0, 0, 0, 0): F(value)} if value else {}

    def __add__(self, other):
        terms = self.terms.copy()
        for key, value in Poly(other).terms.items():
            terms[key] = terms.get(key, 0) + value
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        terms = {}
        for k, v in self.terms.items():
            for l, w in Poly(other).terms.items():
                key = tuple(x + y for x, y in zip(k, l))
                terms[key] = terms.get(key, 0) + v * w
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(isinstance(power, int) and power >= 0, "polynomial power")
        result = Poly(1)
        for _ in range(power):
            result = result * self
        return result

    def __eq__(self, other):
        return self.terms == Poly(other).terms


def check_symbolic_family():
    a, b, t, d, c = [Poly({tuple(int(i == j) for i in range(5)): 1})
                     for j in range(5)]
    total = ordered_sum(family(a, b, t, d, c))
    q0 = -8 * b**2 * c * (3*a**2 + 4*a*d - 2*b**2 + 3*d**2)
    q1 = 4 * c * (-2*a**2*b**2 - 6*a*b**2*d + 3*b**4
                  - 12*b**2*d**2 + 30*d**2*t**2)
    require(total == diag([q0, q1, q1]), "symbolic five-parameter formula")
    print("PASS: general five-parameter product formula, all coefficients")

    z = a
    shifted = [add(matrix, scale(z, eye(3)))
               for matrix in family(25, 20, 16, 16, 36)]
    shifted_total = ordered_sum(shifted)
    central = (z**5 + 100*z**4 + 2950*z**3 + 17700*z**2
               - F(1021325, 3)*z - 3305280)
    transverse = (z**5 + 100*z**4 + 3440*z**3 + 46880*z**2
                  + F(556280, 3)*z - 291264)
    require(shifted_total == scale(120, diag([central, transverse, transverse])),
            "symbolic identity-shift formula")
    print("PASS: identity-shift product formula, all coefficients")


def check_canonical():
    matrices = family(25, 20, 16, 16, 36)
    gram_vectors = [
        [(5, 4, 0), (0, 0, 4)], [(5, -4, 0), (0, 0, 4)],
        [(5, 0, 4), (0, 4, 0)], [(5, 0, -4), (0, 4, 0)],
        [(0, 6, 0), (0, 0, 6)],
    ]
    for matrix, vectors in zip(matrices, gram_vectors):
        gram = add(outer(vectors[0]), outer(vectors[1]))
        require(matrix == gram, "PSD Gram identity")
        require(matrix == transpose(matrix), "symmetry")
        # The displayed vectors are orthogonal and nonzero: the rank is two.
        require(sum(x*y for x, y in zip(*vectors)) == 0, "Gram orthogonality")
        require(all(sum(x*x for x in v) > 0 for v in vectors), "Gram ranks")
    require(sum_matrices(matrices) == scale(100, eye(3)), "sum = 100 I")
    total = ordered_sum(matrices)
    require(total == subset_sum(matrices), "independent subset recurrence")
    average = scale(F(1, 120), total)
    require(average == diag([-3305280, -291264, -291264]), "canonical average")
    require(max(abs(average[i][i]) for i in range(3)) == 3305280, "norm")
    require(F(3305280, 20**5) == F(10329, 10000) > 1, "strict ratio")
    print("PASS: real 3 x 3 rank-two PSD; mean 20 I; ratio 10329/10000")

    shifted = [add(scale(10, a), eye(3)) for a in matrices]
    require(sum_matrices(shifted) == scale(1005, eye(3)), "shifted mean 201 I")
    shifted_average = scale(F(1, 120), ordered_sum(shifted))
    # Each shifted quadratic form is ten times a Gram form plus ||v||^2.
    require(-shifted_average[0][0] > 201**5, "positive definite violation")
    require(-shifted_average[0][0] - 201**5 == F(17502058994, 3),
            "positive definite margin")
    print("PASS: positive definite integer matrices 10 A_i + I")

    # A symbolic scalar certificate for every identity shift 0 <= z <= 1/5.
    margin_coefficients = [F(105280), -F(1378675, 3), -F(97700),
                           -F(6950), -F(200), -F(2)]
    require(all(c < 0 for c in margin_coefficients[1:]), "monotone margin")
    margin_at_endpoint = sum(c * F(1, 5)**i for i, c in enumerate(margin_coefficients))
    require(margin_at_endpoint > 0, "shift interval endpoint")

    # Labeled identity padding: a finite independent control for n=6.
    padded = matrices + [scale(20, eye(3))]
    require(scale(F(1, 720), ordered_sum(padded)) == scale(20, average),
            "identity padding at n=6")
    print("PASS: labeled identity-padding control at n=k=6")
    return matrices


def sum_matrices(matrices):
    out = zero(len(matrices[0]))
    for matrix in matrices:
        out = add(out, matrix)
    return out


def check_stronger_rational():
    matrices = family(16, 12, 9, 11, 24)
    require(sum_matrices(matrices) == scale(64, eye(3)), "alternate sum")
    require(16*9 == 12**2 and 11 > 0 and 24 > 0, "alternate PSD")
    average = scale(F(1, 120), ordered_sum(matrices))
    require(average == diag([-F(1782144, 5), -F(314568, 5), -F(314568, 5)]),
            "alternate average")
    ratio = -average[0][0] / F(64, 5)**5
    require(ratio == F(8701875, 8388608) > F(10329, 10000), "alternate ratio")
    print("PASS: stronger real rational ratio 8701875/8388608")


def check_second_moments(matrices):
    without = scale(F(1, 120), ordered_sum(matrices, second_moment=True))
    with_replacement = eye(3)
    for _ in range(5):
        with_replacement = scale(F(1, 5), sum_matrices(
            [mul(mul(a, with_replacement), a) for a in matrices]))
    require(without == diag([52137052427520, 26248489865856, 26248489865856]),
            "without-replacement second moment")
    require(with_replacement == diag([222683810001920, 145806819139584,
                                     145806819139584]), "replacement second moment")
    require(all(0 < without[i][i] < with_replacement[i][i] for i in range(3)),
            "second-moment inequality goes in the opposite direction")
    print("PASS: squared-error comparison distinguished from norm of mean")


if __name__ == "__main__":
    check_symbolic_family()
    matrices = check_canonical()
    check_stronger_rational()
    check_second_moments(matrices)
    print("All low-dimensional real certificates passed.")
