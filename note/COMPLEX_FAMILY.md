# A rank-one complex Hermitian 2-by-2 family

This note gives an exact one-parameter family containing the complex Hermitian
counterexample. Its parameter analysis is supplementary mathematics; it is not a claim
of global optimality over all Hermitian tuples. The explicit fixed witness is checked
separately by [`check_complex_certificate.py`](../scripts/check_complex_certificate.py).

## Inputs and the exact average

For a real parameter `0 <= r <= 1`, set

```math
 A_\pm(r)=\frac54
 \begin{pmatrix}1&\pm r\\\pm r&r^2\end{pmatrix},\qquad
 B_\pm(r)=\frac54
 \begin{pmatrix}1&\pm ir\\\mp ir&r^2\end{pmatrix},\qquad
 C(r)=\begin{pmatrix}0&0\\0&5(1-r^2)\end{pmatrix}.
 \tag{C1}
```

The first four matrices are positive multiples of outer products of `(1,r)`, `(1,-r)`,
`(1,ir)`, and `(1,-ir)`. The last is a nonnegative multiple of the second coordinate
projection. Thus every input is Hermitian positive semidefinite. All five have rank one
for `0<=r<1`; at `r=1` the last matrix is zero. Their sum is `5I`.

Let `Q(r)` be the average of their 120 ordered products. It is diagonal, with

```math
 Q_{11}(r)=\frac{625}{768}
   (-3r^2+r^4-r^6+3r^8),
 \tag{C2}
```

```math
 Q_{22}(r)=\frac{625}{768}
   (-2r^2-r^4-9r^6+27r^8-15r^{10}).
 \tag{C3}
```

These identities can be checked as polynomial identities, without numerical sampling:
[`check_complex_family.py`](../scripts/check_complex_family.py) enumerates the 120
products in the ring of Gaussian polynomials with rational coefficients and compares
every coefficient. The coefficient formulas also follow by ordinary multiplication
followed by averaging. Conjugation by `diag(1,-1)` permutes the factors, explaining the
zero off-diagonal entries.

## Exact operator norm for every parameter

Put `x=r^2`. Equations (C2) and (C3) factor as

```math
 -Q_{11}=\frac{625}{768}x(1-x)(3x^2+2x+3)=:f(x),
 \tag{C4}
```

```math
 -Q_{22}=\frac{625}{768}x(1-x)
 \left[2+3x(1-x)(1+5x)\right].
 \tag{C5}
```

Both eigenvalues are nonpositive for `0<=x<=1`. Their negative magnitudes differ by the
common nonnegative factor `(625/768)x(1-x)` times

```math
 P(x)=15x^3-9x^2-x+1.
```

The exact rational sum-of-squares identity

```math
 P(x)=15x\left(x-\frac12\right)^2
       +6\left(x-\frac{19}{48}\right)^2+\frac{23}{384}
 \tag{C6}
```

shows that `P(x)>0` for all `x>=0`. Thus the first eigenvalue has at least the magnitude
of the second throughout the allowed parameter interval. This proves the full
operator-norm identity, including the absolute values:

```math
 \boxed{\|Q(r)\|_{\mathrm{op}}
 =f(r^2)=\frac{625}{768}r^2(1-r^2)(3r^4+2r^2+3).}
 \tag{C7}
```

The mean is `I`, so (C7) is also the exact ratio in the norm-of-average Recht–Ré
inequality at `n=k=5`.

## Exact violation interval

The family violates the conjectured bound exactly when `f(x)>1`, or

```math
 W(x):=1875x^4-625x^3+625x^2-1875x+768<0.
 \tag{C8}
```

There are exactly two roots of `W` in `(0,1)`. Denote them by `x_-<x_+`. They specify
the violation interval exactly: `x_-<r^2<x_+`. Numerically,

```math
 x_-\approx0.5378448880609344,\qquad
 x_+\approx0.7036308525929249,
```

or, in terms of `r`,

```math
 0.7333790889171401<r<0.838827069539917.
```

To justify the root description rather than merely estimate it, observe that

```math
 f''(x)=\frac{625}{768}(-2+6x-36x^2)
 =-\frac{625}{768}
 \left[36\left(x-\frac1{12}\right)^2+\frac74\right]<0.
```

Thus `f` is strictly concave, `f(0)=f(1)=0`, and a value above `1` gives exactly two
crossings of the level `1`. One such value is `f(16/25)=10329/10000`. The strict
superlevel set is exactly the interval between the two crossings. The symbolic checker
also certifies narrow rational brackets for the two roots using exact signs of `W`.

For an entirely rational subinterval, every `r` in `[3/4,5/6]` violates the bound. The
endpoint excesses are

```math
 f(9/16)-1=\frac{272159}{16777216}>0,\qquad
 f(25/36)-1=\frac{3315179}{429981696}>0.
```

Concavity in `x` proves the claim between these endpoints.

## The maximum within the family

The unique maximizer is the real root $x_{\ast}$ of

```math
 12x_{\ast}^3-3x_{\ast}^2+2x_{\ast}-3=0.
 \tag{C9}
```

Strict concavity gives uniqueness. Equivalently, the left side of (C9) has strictly
positive derivative `36x^2-6x+2`. Since `f'(0)>0` and `f'(1)<0`, the root lies in
`(0,1)`. Numerically,

```math
 x_{\ast}\approx0.6243648435583831,\qquad
 r_{\ast}=\sqrt{x_{\ast}}\approx0.790167604725974,
```

```math
 \max_{0\le r\le1}\|Q(r)\|_{\mathrm{op}}
 =f(x_{\ast})\approx1.0341426052836649.
```

This optimizes only the family (C1). It is not an asserted optimum for arbitrary complex
Hermitian 2-by-2 inputs, arbitrary numbers of inputs, or other averaging schemes.

The convenient rational choice `r=4/5` yields

```math
 A_\pm=\begin{pmatrix}5/4&\pm1\\\pm1&4/5\end{pmatrix},\quad
 B_\pm=\begin{pmatrix}5/4&\pm i\\\mp i&4/5\end{pmatrix},\quad
 C=\mathrm{diag}(0,9/5),
```

with average-product spectrum `-10329/10000, -22983/25000`. Multiplication by `20` gives
the Gaussian-integer matrices and outer-product factors of the fixed exact certificate.
Because the two imaginary matrices have nonreal entries, this family does not resolve
the real symmetric 2-by-2 problem.

The full parameter analysis in this note is not currently a Lean theorem of the project.
Its identities have an independent exact polynomial checker, and the inequalities follow
from the displayed factorization, sum of squares, and one-variable calculus.
