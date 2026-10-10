# A restricted real symmetric 2 × 2 family

The family below has an exact norm maximum strictly below one. This is a family-specific
result. It neither proves the Recht–Ré inequality for all real symmetric 2 × 2 tuples
nor rules out a counterexample in that dimension. The complex Hermitian witness uses
nonreal entries and does not answer this real question.

Optional numerical search programs and their parameterization are documented in
[experiments/README.md](../experiments/README.md). Their outputs require independent
exact reconstruction; optimizer termination is not a proof.

## Exact result for a restricted real 2-by-2 family

The following is an analytical result, separate from the numerical search. It concerns
only the explicitly defined family below. No global optimality over real symmetric
2-by-2 matrices is claimed.

Let `n >= 4` and `m = n - 3`. Take the following `n` labeled factors:

```math
 A_+=\begin{pmatrix}a&b\\b&t\end{pmatrix},\qquad
 A_-=\begin{pmatrix}a&-b\\-b&t\end{pmatrix},\qquad
 C=\begin{pmatrix}c&0\\0&0\end{pmatrix},
```

together with `m` copies of

```math
 B=\begin{pmatrix}0&0\\0&d\end{pmatrix}.
```

Assume

```math
 a,t,c,d\ge0,\quad b^2\le at,\quad
 2a+c=n,\quad 2t+md=n.
```

These conditions give positive semidefinite inputs and mean `I`.

### Product formula by counting coordinate paths

For this family, the symmetrized product is diagonal:

```math
 Q_n=-\operatorname{diag}\!\left(
 \frac{4b^2cd^m}{n(n-1)(n-2)},\;
 \frac{2b^2cd^m}{n(n-1)}
 \right).
 \tag{R1}
```

First, conjugation by `diag(1,-1)` interchanges `A_+` and `A_-`, fixes all other
factors, and hence fixes their symmetrized product. Its off-diagonal entries must
therefore vanish.

For a nonzero contribution to a diagonal entry of a word, the factor `C` forces
coordinate `1`, while every `B` forces coordinate `2`. Only `A_+` and `A_-` can change
coordinates. Both must use their off-diagonal entries, and their combined contribution
is `-b^2`. The remaining contribution is `c d^m`.

For the `(1,1)` entry, all `B` factors must lie between the two `A` factors, and `C`
must lie outside them. There are two orders of the `A` factors, two choices for the side
containing `C`, and `m!` orders of the labeled `B` factors: `4m!` nonzero contributions.
Dividing by `n!` gives the first entry of (R1).

For the `(2,2)` entry, `C` must lie between the two `A` factors, and all `B` factors lie
outside them. The `m` labeled `B` factors can be ordered in `m!` ways and split at any
of `m+1` positions between the two outer blocks. With two orders of the `A` factors, the
count is `2(m+1)m!`. Dividing by `n!` gives the second entry of (R1). This counts
labeled permutations even though the `B` matrices coincide.

Since `n >= 4`, the magnitude of the second entry is at least that of the first.
Therefore

```math
 \|Q_n\|_{\mathrm{op}}=
 \frac{2b^2cd^m}{n(n-1)}.
 \tag{R2}
```

### Exact optimum within this family

Using `b^2 <= at`, the numerator in (R2) is bounded by `2atcd^m`. The two mean
constraints separate this product into two maximization problems:

```math
 ac=a(n-2a)\le\frac{n^2}{8},
```

with equality at `a=n/4`, `c=n/2`, and

```math
 td^m=t\left(\frac{n-2t}{m}\right)^m
 \le \frac{n^{m+1}}{2(m+1)^{m+1}},
```

with equality at `t=n/[2(m+1)]`, `d=n/(m+1)`. The latter bound is ordinary AM-GM applied
to the `m+1` nonnegative numbers `2t,d,...,d`, whose sum is `n`. Setting `b^2=at`
achieves both bounds simultaneously. Thus the exact family maximum is

```math
 \boxed{R_n=\frac{n^{n-1}}{8(n-1)(n-2)^{n-2}}.}
 \tag{R3}
```

An attaining tuple consists of

```math
 A_\pm=
 \begin{pmatrix}
 n/4&\displaystyle\pm n/\sqrt{8(n-2)}\\[2mm]
 \displaystyle\pm n/\sqrt{8(n-2)}&n/[2(n-2)]
 \end{pmatrix},\qquad
 C=\operatorname{diag}(n/2,0),
```

and `n-3` copies of `B=diag(0,n/(n-2))`. Every input in this attaining tuple has rank
one. Its exact spectral values are

```math
 -\frac{n^{n-1}}{4(n-1)(n-2)^{n-1}},\qquad
 -\frac{n^{n-1}}{8(n-1)(n-2)^{n-2}}.
```

For example, `R_5=625/864` and `R_6=243/320`. These values are attained within the
displayed family only.

### The family never violates the conjectured bound

The sequence `R_n` is strictly increasing and converges to `e^2/8 < 1`. For a direct
proof, set `y=n-1` and extend the logarithm continuously:

```math
 L(y)=\log(8R_{y+1})
 =y\log(y+1)-(y-1)\log(y-1)-\log y.
```

For `y>1`,

```math
 L'(y)=\log\frac{y+1}{y-1}-\frac1y-\frac1{y+1}>0.
```

Indeed, strict convexity of `1/u` on the interval `[y-1,y+1]` gives
`log((y+1)/(y-1))>2/y`, so `L'(y)>1/y-1/(y+1)>0`. The alternative expression

```math
 L(y)=(y-1)\log\left(1+\frac2{y-1}\right)
       +\log\left(1+\frac1y\right)
```

has limit `2`. Hence `R_n < e^2/8` for every finite `n>=4`. For completeness, the
elementary exponential series gives `e<11/4`, and therefore `e^2/8<121/128<1`.

The ordinary multiplication audit
[`scripts/check_real_2x2_family.py`](../scripts/check_real_2x2_family.py) independently
enumerates every labeled permutation at `n=4,5,6,7,8`. It uses integer arithmetic in the
quadratic algebra generated by the one required square root. These finite checks support
the formulas; the general proof is the counting and optimization argument above. This
supplementary family theorem is not currently a Lean theorem of the project.
