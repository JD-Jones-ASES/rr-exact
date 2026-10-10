#!/usr/bin/env python3
"""Exact polynomial checks for the one-parameter Hermitian 2x2 family.

All 120 ordinary matrix products are enumerated over Gaussian polynomials
with rational coefficients.  This is independent of the numerical spin/Jordan
discovery code.  Only the standard library and the existing exact polynomial
helpers in check_low_dim.py are used.  Checks remain active under python -O.
"""
from fractions import Fraction as F

from check_low_dim import Poly, diag, ordered_sum, require, scale, sum_matrices


class GaussianPoly:
    """A pair of rational polynomials, representing real + i*imaginary."""

    def __init__(self, real=0, imaginary=0):
        if isinstance(real, GaussianPoly):
            self.real, self.imaginary = real.real, real.imaginary
        else:
            self.real, self.imaginary = Poly(real), Poly(imaginary)

    def __add__(self, other):
        other = GaussianPoly(other)
        return GaussianPoly(self.real+other.real, self.imaginary+other.imaginary)

    __radd__ = __add__

    def __neg__(self):
        return GaussianPoly(-self.real, -self.imaginary)

    def __sub__(self, other):
        return self + -GaussianPoly(other)

    def __rsub__(self, other):
        return GaussianPoly(other) + -self

    def __mul__(self, other):
        other = GaussianPoly(other)
        return GaussianPoly(self.real*other.real-self.imaginary*other.imaginary,
                            self.real*other.imaginary+self.imaginary*other.real)

    __rmul__ = __mul__

    def conjugate(self):
        return GaussianPoly(self.real, -self.imaginary)

    def __eq__(self, other):
        other = GaussianPoly(other)
        return self.real == other.real and self.imaginary == other.imaginary


def outer(vector):
    return [[GaussianPoly(x)*GaussianPoly(y).conjugate() for y in vector]
            for x in vector]


def derivative(poly):
    """Derivative in the first of the existing Poly class's five variables."""
    terms = {}
    for key, value in poly.terms.items():
        if key[0]:
            lower = (key[0]-1,) + key[1:]
            terms[lower] = key[0]*value
    return Poly(terms)


def norm_polynomial(x):
    return F(625, 768)*x*(1-x)*(3*x*x+2*x+3)


def crossing_polynomial(x):
    return 1875*x**4-625*x**3+625*x**2-1875*x+768


def optimum_polynomial(x):
    return 12*x**3-3*x**2+2*x-3


def check():
    r = Poly({(1, 0, 0, 0, 0): 1})
    real_r, imaginary_r = GaussianPoly(r), GaussianPoly(0, r)
    matrices = [
        scale(F(5, 4), [[1, real_r], [real_r, r*r]]),
        scale(F(5, 4), [[1, -real_r], [-real_r, r*r]]),
        scale(F(5, 4), [[1, imaginary_r], [-imaginary_r, r*r]]),
        scale(F(5, 4), [[1, -imaginary_r], [imaginary_r, r*r]]),
        diag([GaussianPoly(0), GaussianPoly(5*(1-r*r))]),
    ]
    matrices = [[[GaussianPoly(entry) for entry in row] for row in matrix]
                for matrix in matrices]
    vectors = [[1, real_r], [1, -real_r],
               [1, -imaginary_r], [1, imaginary_r]]
    for matrix, vector in zip(matrices[:4], vectors):
        require(matrix == scale(F(5, 4), outer(vector)), "symbolic rank-one Gram identity")
    require(sum_matrices(matrices) == diag([5, 5]), "symbolic sum = 5 I")

    q1 = F(625, 768)*(-3*r**2+r**4-r**6+3*r**8)
    q2 = F(625, 768)*(-2*r**2-r**4-9*r**6+27*r**8-15*r**10)
    require(ordered_sum(matrices) == scale(120, diag([GaussianPoly(q1), GaussianPoly(q2)])),
            "all coefficients of the exact complex family average")
    print("PASS: all coefficients of the 120-product Hermitian family formula.")

    x = r*r
    common = F(625, 768)*x*(1-x)
    require(-q1 == norm_polynomial(x), "first eigenvalue factorization")
    second_bracket = 2+3*x*(1-x)*(1+5*x)
    require(-q2 == common*second_bracket, "second eigenvalue nonpositive factorization")
    p = 15*x**3-9*x*x-x+1
    sos = 15*x*(x-F(1, 2))**2+6*(x-F(19, 48))**2+F(23, 384)
    require(p == sos, "rational sum-of-squares dominance certificate")
    require((3*x*x+2*x+3)-second_bracket == p, "eigenvalue magnitude comparison")
    print("PASS: exact factorizations and rational sum-of-squares norm dominance.")

    # Now use the same indeterminate directly as x, to check the calculus identities.
    x = r
    f = norm_polynomial(x)
    require(derivative(f) == -F(625, 768)*optimum_polynomial(x), "critical point cubic")
    require(derivative(derivative(f)) ==
            -F(625, 768)*(36*(x-F(1, 12))**2+F(7, 4)), "strict concavity identity")
    require(768*(1-f) == crossing_polynomial(x), "violation quartic")
    require(norm_polynomial(F(16, 25)) == F(10329, 10000), "canonical parameter")
    require(norm_polynomial(F(9, 16))-1 == F(272159, 16777216) > 0,
            "left rational subinterval endpoint")
    require(norm_polynomial(F(25, 36))-1 == F(3315179, 429981696) > 0,
            "right rational subinterval endpoint")

    denominator = 10**11
    lower = (F(53784488806, denominator), F(53784488807, denominator))
    upper = (F(70363085259, denominator), F(70363085260, denominator))
    maximum = (F(62436484355, denominator), F(62436484356, denominator))
    require(crossing_polynomial(lower[0]) > 0 > crossing_polynomial(lower[1]),
            "lower quartic root bracket")
    require(crossing_polynomial(upper[0]) < 0 < crossing_polynomial(upper[1]),
            "upper quartic root bracket")
    require(optimum_polynomial(maximum[0]) < 0 < optimum_polynomial(maximum[1]),
            "unique maximizer bracket")
    print("PASS: critical point, strict concavity, and exact rational root brackets.")
    print("All supplementary complex family polynomial checks passed.")


if __name__ == "__main__":
    check()
