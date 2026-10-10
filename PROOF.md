# De Sa benchmark: exact norm 19/16

This supporting benchmark formalizes De Sa's published dimension-five construction. The
real 3 × 3 and complex Hermitian 2 × 2 results are in
[note/LOW_DIMENSION.md](note/LOW_DIMENSION.md).

The family is De Sa's. The argument below does not use his trigonometric formula and
does not use floating point. The violating eigenvalue is computed by a five-step
recurrence. The operator norm, as opposed to that lower bound, is the one place a finite
expansion enters: one hundred twenty products of explicit $5\times 5$ rational matrices.

## Statement

For $n\geq 2$ and $k\in\{1,\ldots,n\}$, define $y_k\in\mathbb{R}^n$ by
```math
(y_k)_k=\frac{\sqrt{n-1}}{n},\qquad (y_k)_i=-\frac{1}{n\sqrt{n-1}}\quad(i\neq k),
```
and set
```math
A_k=I+\mathbf{1}y_k^{\mathsf T}+y_k\mathbf{1}^{\mathsf T},
```
where $\mathbf{1}$ is the all-ones vector. Write $J=\mathbf{1}\mathbf{1}^{\mathsf T}$
and
```math
\operatorname{rr}(A_1,\ldots,A_n)=\frac1{n!}\sum_{\sigma\in S_n}A_{\sigma(1)}\cdots A_{\sigma(n)}.
```
The Recht–Ré inequality, in the form disproved here, asserts that if $A_1,\ldots,A_n$
are positive semidefinite and $\sum_i A_i\preceq nI$, then
$\lVert\operatorname{rr}(A_1,\ldots,A_n)\rVert\leq 1$.

**Theorem.** Each $A_k$ is positive semidefinite of rank $n-1$, and $\sum_k A_k=nI$. The
scalar $a_n\in\mathbb{Q}$ defined by $a_0=a_1=1$ and
```math
(n-1)\,a_{t+1}=2(n-1)\,a_t-n\,a_{t-1}\qquad(t\geq 1)
```
satisfies $\operatorname{rr}(A_1,\ldots,A_n)\,\mathbf{1}=a_n\mathbf{1}$. In particular
```math
a_2=0,\quad a_3=-\frac12,\quad a_4=-\frac89,\quad a_5=-\frac{19}{16}.
```
Thus the inequality already fails at $n=5$, in dimension $5$, and $19/16$ is the first
absolute value of this sequence that exceeds $1$.

**Theorem (norm).** For $n=5$,
```math
\operatorname{rr}(A_1,\ldots,A_5)=\frac{29}{64}\,I-\frac{21}{64}\,J.
```
The eigenvalues are $-19/16$, once, and $29/64$, four times. The operator norm is
exactly $19/16$.

The same conclusion holds with the sum of the products in place of the average: that sum
has norm $120\cdot 19/16=285/2>120$.

## The vectors

The coordinates of $y_k$ sum to zero:
```math
\frac{\sqrt{n-1}}{n}+(n-1)\cdot\Bigl(-\frac{1}{n\sqrt{n-1}}\Bigr)=0.
```
Hence $\sum_k y_k=0$, because the sum is permutation-invariant and orthogonal to
$\mathbf{1}$, so it is zero; or by counting, each coordinate of the sum is
$\sqrt{n-1}/n+(n-1)\cdot(-1/(n\sqrt{n-1}))=0$. Also
```math
\lVert y_k\rVert^2=\frac{n-1}{n^2}+\frac{n-1}{n^2(n-1)}=\frac1n,
```
and for $i\neq k$,
```math
\begin{aligned}
y_i\cdot y_k
&=2\cdot\frac{\sqrt{n-1}}{n}\cdot\Bigl(-\frac{1}{n\sqrt{n-1}}\Bigr)+(n-2)\cdot\frac{1}{n^2(n-1)}\\
&=-\frac{2}{n^2}+\frac{n-2}{n^2(n-1)}
=-\frac{1}{n(n-1)}.
\end{aligned}
```
Write $\rho=-1/(n(n-1))$. In particular $\mathbf{1}\cdot y_k=0$.

When $n=m^2+1$, one has $\sqrt{n-1}=m\in\mathbb{Z}$, so every $y_k$ and every $A_k$ has
rational entries. The first two such $n$ at which $|a_n|>1$ are $n=5$ and $n=10$. For
$n=5$,
```math
(y_k)_k=\frac25,\qquad (y_k)_i=-\frac1{10}\quad(i\neq k),
```
and the matrix for $k=1$, with the distinguished index first, is
```math
A_1=\frac1{10}
\begin{pmatrix}
18&3&3&3&3\\
3&8&-2&-2&-2\\
3&-2&8&-2&-2\\
3&-2&-2&8&-2\\
3&-2&-2&-2&8
\end{pmatrix}.
```
The other four matrices are the coordinate permutations of this one. For $n=10$,
$(y_k)_k=3/10$ and $(y_k)_i=-1/30$.

## The sum and the positive-semidefinite bound

```math
\sum_k A_k=nI+\mathbf{1}\Bigl(\sum_k y_k\Bigr)^{\mathsf T}+\Bigl(\sum_k y_k\Bigr)\mathbf{1}^{\mathsf T}=nI.
```
So $\lVert n^{-1}\sum_k A_k\rVert=1$, and the conjectured upper bound is $1$.

For the quadratic form, $\mathbf{1}\perp y_k$ gives
```math
v^{\mathsf T}A_k v=\lVert v\rVert^2+2(\mathbf{1}\cdot v)(y_k\cdot v).
```
Pythagoras in the orthogonal decomposition
$\operatorname{span}\{\mathbf{1},y_k\}\oplus\operatorname{span}\{\mathbf{1},y_k\}^\perp$
gives
```math
\lVert v\rVert^2\geq\frac{s^2}{n}+n t^2,
```
where $s=\mathbf{1}\cdot v$ and $t=y_k\cdot v$, since $\lVert\mathbf{1}\rVert^2=n$ and
$\lVert y_k\rVert^2=1/n$. Therefore
```math
v^{\mathsf T}A_k v\geq\frac{s^2}{n}+nt^2+2st=\frac{(s+nt)^2}{n}\geq 0.
```
Equality holds if and only if $v\in\operatorname{span}\{\mathbf{1},y_k\}$ and $s+nt=0$,
i.e. on the line spanned by $\kappa_k=\mathbf{1}-n y_k$. Directly,
```math
A_k\kappa_k=(\mathbf{1}-ny_k)+(y_k\cdot\kappa_k)\mathbf{1}+(\mathbf{1}\cdot\kappa_k)y_k
=\mathbf{1}-ny_k-\mathbf{1}+ny_k=0,
```
using $y_k\cdot\kappa_k=-1$ and $\mathbf{1}\cdot\kappa_k=n$. The kernel is exactly that
line, so $A_k$ has rank $n-1$.

## The all-ones eigenvalue

Apply an ordered product of distinct factors to $\mathbf{1}$. The claim is that after
any $t$ distinct factors, the image has the form
```math
v=a\,\mathbf{1}+\sum c_{\mathrm{age}}\,y,
```
where the sum runs over the $t$ factors already used, each carrying a coefficient that
depends only on how early it was used, and the pair $(a,S)$ with $S$ the sum of those
coefficients obeys
```math
a\leftarrow a+\rho S,\qquad S\leftarrow S+na
```
(the second update uses the value of $a$ from before the first update). Starting from
$\mathbf{1}$ itself, which is $a=1$, $S=0$.

The inductive step: $A_m v=v+(y_m\cdot v)\mathbf{1}+(\mathbf{1}\cdot v)y_m$ for a fresh
index $m$. Freshness gives $y_m\cdot v=\rho S$, because $y_m$ meets $\mathbf{1}$ in $0$
and meets each already-used $y$ in $\rho$. Also $\mathbf{1}\cdot v=an$. The coefficient
of $\mathbf{1}$ therefore increases by $\rho S$, the old $y$-coefficients are unchanged,
and the new coefficient of $y_m$ is $na$. The pair $(a,S)$ updates as claimed, and the
update does not depend on which fresh index was chosen.

Every ordered product of all $n$ factors therefore sends $\mathbf{1}$ to $a_n\mathbf{1}$
plus a linear combination of $y_1,\ldots,y_n$ whose coefficients are a rearrangement of
one fixed list with sum $S$. Averaging over $S_n$, each index occupies each position in
that list equally often, so each $y_k$ receives the coefficient $S/n$. Those terms
cancel because $\sum_k y_k=0$. Hence
```math
\operatorname{rr}(A_1,\ldots,A_n)\,\mathbf{1}=a_n\mathbf{1},
```
where $a_n$ is the value of $a$ at step $n$.

Eliminating $S$ gives the second-order relation. From the updates,
$a_t-a_{t-1}=\rho S_{t-1}$ and $S_t=S_{t-1}+n a_{t-1}$, so for $t\geq 1$
```math
\begin{aligned}
a_{t+1}
&=a_t+\rho S_t
=a_t+\rho(S_{t-1}+na_{t-1})
=a_t+(a_t-a_{t-1})+n\rho\,a_{t-1}\\
&=2a_t-\frac{n}{n-1}a_{t-1},
\end{aligned}
```
since $n\rho=-1/(n-1)$. The initial values are $a_0=1$ and $a_1=1$. Clearing the
denominator gives the recurrence in the theorem. Both recurrences have rational
coefficients and rational initial data, so $a_n\in\mathbb{Q}$ for every integer
$n\geq 2$, whether or not the matrices themselves are rational.

For $n=5$, one has $\rho=-1/20$, and the age steps are

| $t$ | $a_t$ | $S_t$ |
| ---: | ---: | ---: |
| 0 | $1$ | $0$ |
| 1 | $1$ | $5$ |
| 2 | $3/4$ | $10$ |
| 3 | $1/4$ | $55/4$ |
| 4 | $-7/16$ | $15$ |
| 5 | $-19/16$ | $205/16$ |

The last line is the one that matters:
$\operatorname{rr}\,\mathbf{1}=-(19/16)\mathbf{1}$, so
```math
\lVert\operatorname{rr}(A_1,\ldots,A_5)\rVert\geq\frac{19}{16}>1.
```
The three preceding absolute values are $0$, $1/2$, $8/9$, all at most $1$. To conclude
that the whole operator norm is at most one, one also needs the complementary
eigenvalue. De Sa's Statement 1 gives it as $b_n=1+(a_n-1)/(n-1)$, which is respectively
$0$, $1/4$, and $10/27$ for $n=2,3,4$. Thus this family does not violate the inequality
for those parameters, and $n=5$ is its first violation. The general
complementary-eigenvalue formula is cited here; it is not a benchmark Lean theorem.

(The recurrence continues to produce rationals past $n=5$. It is not the case that
$|a_n|>1$ for every $n\geq 5$: the certificate computes the terms through $n=40$, and
$|a_n|\leq 1$ for $17\leq n\leq 28$. For those $n$ the all-ones vector is not a witness.
For $n=10=3^2+1$ the matrices are rational and $a_{10}=-99712/59049$, whose absolute
value is greater than $1$.)

## The operator norm at $n=5$

The all-ones computation gives the lower bound. The matching upper bound is the matrix
identity
```math
\operatorname{rr}(A_1,\ldots,A_5)=\frac{29}{64}\,I-\frac{21}{64}\,J.
```
A scalar matrix plus a multiple of $J$ acts by $\beta+n\gamma$ on
$\operatorname{span}\{\mathbf{1}\}$ and by $\beta$ on $\mathbf{1}^\perp$. Here
$\beta=29/64$ and $\gamma=-21/64$, so
```math
\beta+5\gamma=\frac{29}{64}-\frac{105}{64}=-\frac{76}{64}=-\frac{19}{16},
```
in agreement with the recurrence, and the spectrum is $-19/16$ once and $29/64$ four
times. Since $29/64<19/16$, the operator norm is $19/16$.

De Sa's displayed shape is the same matrix:
```math
\frac{29}{64}\Bigl(I-\frac{J}{5}\Bigr)-\frac{19}{16}\cdot\frac{J}{5}
=\frac{29}{64}\,I-\Bigl(\frac{29}{320}+\frac{19}{80}\Bigr)J
=\frac{29}{64}\,I-\frac{21}{64}\,J.
```

The identity itself is a finite calculation. There are $120$ ordered products of five
explicit matrices with entries in $\frac1{10}\mathbb{Z}$. Their average equals the
right-hand side entrywise. `scripts/check_certificate.py` performs that multiplication
in exact rational arithmetic, and also rechecks the quadratic-form bound, the sum $5I$,
the kernel vectors, the age table, and the agreement of the two recurrences through
$n=40$. The products are closed under transpose, because the reverse of a permutation is
a permutation, so the average is symmetric and the operator norm is the largest absolute
eigenvalue.

## What the trigonometric form is

The characteristic roots of $r^2-2r+n/(n-1)=0$ are $1\pm i/\sqrt{n-1}$, with modulus
$\sqrt{n/(n-1)}$ and argument $\theta=\arcsin(1/\sqrt{n})$. The solution of the
recurrence with $a_0=a_1=1$ is
```math
a_t=\Bigl(\frac{n}{n-1}\Bigr)^{t/2}\cos\bigl(t\arcsin(1/\sqrt{n})\bigr).
```
This is De Sa's factor $\lambda$. It is recorded so the rational value $-19/16$ can be
matched to his formula. No step of the violation uses it: $-19/16$ is the output of the
age table.

## What is not claimed

This benchmark alone does not address dimensions below five. De Sa's padding remark
gives counterexamples in every dimension $d\geq5$, for every full-epoch length
$n=k\geq5$, by adding diagonal $1$'s or extra copies of $I$. The low-dimensional note
supplies real dimension-three and complex dimension-two counterexamples; it leaves the
real dimension-two question unresolved.

The symmetric-product form, with positive-semidefinite square roots of the $A_k$, is De
Sa's second inequality. It is not reproved here. The square roots are real, but they are
not rational.

No closed description of $\{n:|a_n|>1\}$ is claimed beyond the terms the certificate
computes. For $n\neq5$, the benchmark Lean development does not determine the operator
norm. The all-ones factor gives a lower bound; De Sa's general Statement 1 also
specifies the complementary eigenvalue.

Zhong's abstract reports that the inequality holds for all positive-semidefinite tuples
once $n\geq 2\lceil m/2\rceil^2$, is the complementary regime. It is not used.

## Sources

The matrices, the exact averaged-product formula, and the exact eigenvalues at $n=5$ are
due to De Sa, *Random Reshuffling is Not Always Better*, NeurIPS 2020. His Statement 1
gives an analytic formula, and he also remarks that the five-factor case is easy to
check numerically. This note gives an elementary rational-recurrence presentation, a
completed-square PSD proof, exact replay, and Lean formalization of that existing
example. Neither the number $19/16$ nor the dimension-five counterexample is a new
mathematical result of this repository.

The inequality is Conjecture 1 of Recht and Ré, *Toward a Noncommutative
Arithmetic-geometric Mean Inequality*, COLT 2012. Lai and Lim, *Recht–Ré Noncommutative
Arithmetic-Geometric Mean Conjecture is False*, ICML 2020, give the dimension-free
disproof. Zhong, *When the noncommutative AM-GM inequality holds*, arXiv:2610.04874,
states a sufficient condition in the large-$n$ regime; its proof is not audited here.
