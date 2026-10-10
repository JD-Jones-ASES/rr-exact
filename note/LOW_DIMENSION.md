# Exact real 3 × 3 and complex 2 × 2 counterexamples to the Recht–Ré inequality

JD Jones

## 1. Statement and scope

For PSD matrices over $\mathbb F=\mathbb R$ or $\mathbb C$, write

```math
 M(A)=\frac1n\sum_{i=1}^n A_i,\qquad
 R_k(A)=\frac1{(n)_k}\sum_{\substack{i_1,\ldots,i_k\\\text{all distinct}}}
 A_{i_1}\cdots A_{i_k},\qquad (n)_k=\frac{n!}{(n-k)!}.
```

The norm is the Euclidean operator norm. The inequality under consideration is

```math
 \VertR_k(A)\Vert_{\mathrm{op}}\le \VertM(A)^k\Vert_{\mathrm{op}}
 =\VertM(A)\Vert_{\mathrm{op}}^k. \qquad\text{(1)}
```

This is the norm of an averaged product. It is not an average of product norms or the
separate palindromic/second-moment conjecture. Our primary examples have $n=k=5$.

**Theorem 1 (real dimension three).** Five explicit symmetric integer matrices of rank
two have sum $100I_3$, averaged product $\mathrm{diag}(-3305280,-291264,-291264)$,
and ratio $10329/10000>1$ in (1).

**Theorem 2 (complex dimension two).** Five explicit Hermitian Gaussian-integer matrices
of rank one have sum $100I_2$, averaged product
$\mathrm{diag}(-3305280,-2941824)$, and the same ratio.

The complex dimension is minimal: in dimension one the matrices are nonnegative real
numbers and the scalar AM–GM inequality applies. No minimality theorem in the real case
is claimed. In particular the real symmetric 2 × 2 question is not settled by using
imaginary entries in a Hermitian 2 × 2 matrix.

Sections 2–3 prove the primary examples. Sections 4–7 give algebraic families,
robustness, padding, and an optimization application. The supplementary family and
application results have elementary proofs and exact Python checks; the Lean comparison
contract proves two existential counterexamples using the fixed examples. De Sa's
dimension-five benchmark remains a supporting library result; see
[VERIFICATION.md](../VERIFICATION.md).

## 2. Five real integer matrices

Set

```math
A_1=\begin{pmatrix}25&20&0\\20&16&0\\0&0&16\end{pmatrix},\quad
A_2=\begin{pmatrix}25&-20&0\\-20&16&0\\0&0&16\end{pmatrix},
```
```math
A_3=\begin{pmatrix}25&0&20\\0&16&0\\20&0&16\end{pmatrix},\quad
A_4=\begin{pmatrix}25&0&-20\\0&16&0\\-20&0&16\end{pmatrix},\quad
A_5=\begin{pmatrix}0&0&0\\0&36&0\\0&0&36\end{pmatrix}.
```

Their quadratic forms are

```math
 (5x\pm4y)^2+16z^2,\qquad
 (5x\pm4z)^2+16y^2,\qquad36y^2+36z^2.
```

Each is the sum of squares of two independent linear forms, so each matrix is PSD of
rank two. Their sum is $100I_3$, hence $M=20I_3$ and $\VertM^5\Vert=20^5=3200000$.

The exact product identity is

```math
 \sum_{\sigma\in S_5}A_{\sigma(1)}\cdots A_{\sigma(5)}
 =\mathrm{diag}(-396633600,-34951680,-34951680). \qquad\text{(2)}
```

Dividing by 120 gives the average in Theorem 1. Its largest absolute eigenvalue is
$3305280$, attained on $e_1=(1,0,0)^T$, and

```math
 \frac{3305280}{3200000}=\frac{10329}{10000}=1.0329.
```

Equation (2) specializes the polynomial identity proved in Section 4. It is also checked
by direct enumeration of all 120 labeled permutations, an independent subset recurrence,
and the Lean fixed-instance development. The strict gap is $105280$, so the result does
not depend on numerical rounding.

## 3. Five complex rank-one matrices

Let

```math
 v_1=(5,4)^T,\quad v_2=(5,-4)^T,\quad
 v_3=(5,4i)^T,\quad v_4=(5,-4i)^T,\quad v_5=(0,6)^T,
 \qquad H_j=v_jv_j^*.
```

Thus the collection consists of

```math
 \begin{pmatrix}25&\pm20\\\pm20&16\end{pmatrix},\qquad
 \begin{pmatrix}25&\pm20i\\\mp20i&16\end{pmatrix},\qquad
 \begin{pmatrix}0&0\\0&36\end{pmatrix}.
```

The sign order in the imaginary pair only relabels the matrices. Every $H_j$ is
Hermitian PSD of rank one because $z^*H_jz=|v_j^*z|^2$ and $v_j\ne0$. Their sum is
$100I_2$.

Gaussian-integer multiplication gives

```math
 \sum_{\sigma\in S_5}H_{\sigma(1)}\cdots H_{\sigma(5)}
 =\mathrm{diag}(-396633600,-353018880). \qquad\text{(3)}
```

Consequently

```math
 R_5(H)=\mathrm{diag}(-3305280,-2941824),\qquad
 \VertR_5(H)\Vert=3305280>20^5.
```

The real and imaginary parts of every arithmetic operation in the independent checker
are integers or rational numbers. No floating-point complex arithmetic is used. An
operator-norm certificate is immediate from the diagonal form.

These witnesses cannot be simultaneously unitarily conjugated to real symmetric 2 × 2
matrices. Indeed, they span the four-dimensional real vector space of Hermitian 2 × 2
matrices, whereas real symmetric 2 × 2 matrices span only three real dimensions. Their
usual realification has dimension four. Calling (3) a solution of the real dimension-two
case would therefore be incorrect.

## 4. A real family and its exact product formula

For real parameters $a,b,t,d,c$, define

```math
 X_\pm=\begin{pmatrix}a&\pm b&0\\\pm b&t&0\\0&0&d\end{pmatrix},\quad
 Y_\pm=\begin{pmatrix}a&0&\pm b\\0&d&0\\\pm b&0&t\end{pmatrix},\quad
 Z=\mathrm{diag}(0,c,c).
```

Their average full product is exactly

```math
 R_5(X_+,X_-,Y_+,Y_-,Z)=\mathrm{diag}(q_0,q_1,q_1), \qquad\text{(4)}
```
where

```math
 q_0=-\frac{b^2c}{15}(3a^2+4ad-2b^2+3d^2), \qquad\text{(5)}
```
```math
 q_1=\frac{c}{30}
 \left(-2a^2b^2-6ab^2d+3b^4-12b^2d^2+30d^2t^2\right). \qquad\text{(6)}
```

**Proof of the identity.** Conjugating by either coordinate sign change in the last two
coordinates permutes the five matrices. The symmetrized product is invariant under these
conjugations, so its off-diagonal entries vanish. Swapping the last two coordinates also
permutes the collection; the last two diagonal entries therefore agree.

For the remaining entries, expand each product by closed index paths. The nonzero
coefficients in the sums of 120 products are as follows:

| Entry | Monomial | Coefficient |
|---|---|---:|
| $(1,1)$ | $a^2b^2c$ | $-24$ |
| $(1,1)$ | $ab^2cd$ | $-32$ |
| $(1,1)$ | $b^4c$ | $16$ |
| $(1,1)$ | $b^2cd^2$ | $-24$ |
| $(2,2)$, $(3,3)$ | $a^2b^2c$ | $-8$ |
| $(2,2)$, $(3,3)$ | $ab^2cd$ | $-24$ |
| $(2,2)$, $(3,3)$ | $b^4c$ | $12$ |
| $(2,2)$, $(3,3)$ | $b^2cd^2$ | $-48$ |
| $(2,2)$, $(3,3)$ | $cd^2t^2$ | $120$ |

Dividing by 120 proves (5)–(6). The coefficient table is independently checked by the
standard-library sparse-polynomial verifier in `scripts/check_low_dim.py`; it enumerates
products symbolically rather than testing selected parameter values.

### Positivity and scalar mean

Assume

```math
 a>0,\qquad t=\frac{b^2}{a},\qquad d\ge0,\qquad
 c=4a-2t-2d\ge0. \qquad\text{(7)}
```

Then all five matrices are PSD and their sum is $4aI_3$. For example,

```math
 (x,y,z)X_\pm(x,y,z)^T
 =a\left(x\pm\frac ba y\right)^2+dz^2.
```

Writing $x=t/a=b^2/a^2$ and $y=d/a$, the parameter domain is $x\ge0,y\ge0,x+y\le2$. The
central negative-eigenvalue ratio becomes

```math
 \mathcal R(x,y)=\frac{-q_0}{(4a/5)^5}
 =\frac{625}{1536}\,x(2-x-y)(3+4y+3y^2-2x). \qquad\text{(8)}
```

Every point with $\mathcal R(x,y)>1$ proves a violation. This is a sufficient condition
even if the other eigenvalue has larger absolute value.

### A stronger small integer example

The values $(a,b,t,d,c)=(16,12,9,11,24)$ give five integer matrices with largest
absolute entry 24 and mean $(64/5)I_3$. Formula (4) gives

```math
 R_5=\mathrm{diag}
 \left(-\frac{1782144}{5},-\frac{314568}{5},-\frac{314568}{5}\right),
```

so the exact operator-norm ratio is

```math
 \frac{8701875}{8388608}=1.03734433650970458984375.
```

This is a supplementary rational certificate; the two compared Lean contracts use
witnesses with the common ratio $10329/10000$.

### Exact optimum of the central branch

Let $y_{\ast}$ be the unique positive root of $36y^3+39y^2-18y-17=0$, and put

```math
 x_{\ast} = \frac{(1-y_{\ast})(9y_{\ast}+5)}{2(3y_{\ast}+1)}.
```

Then $\mathcal R$ has its unique global maximum on the parameter triangle at
$(x_{\ast},y_{\ast})$. Numerically,

```math
 y_{\ast}\approx0.678666120985539,\quad x_{\ast}\approx0.587842074213783,\quad
 \mathcal R(x_{\ast},y_{\ast})\approx1.038773776705983.
```

**Proof.** Remove the positive constant $625/1536$ and call the remaining polynomial
$F$. On the edges $x=0$ and $x+y=2$, $F=0$. On $y=0$, its maximum is
$(35+13\sqrt{13})/54<2$, whereas $F(1/2,1/2)=19/8>2$. A global maximizer is therefore
interior. The equation $F_y=0$ gives

```math
 x=\frac{(1-y)(9y+5)}{2(3y+1)}.
```

Interior feasibility implies $3y^2+6y-1>0$. Substituting into $F_x$ gives

```math
 \frac{(3y^2+6y-1)(36y^3+39y^2-18y-17)}{2(3y+1)^2}.
```

The cubic has exactly one positive root by Descartes' sign rule, and its values at $2/3$
and $7/10$ have opposite signs. It gives a feasible interior point. Thus there is
exactly one interior stationary point that could be the global maximum, proving the
claim.

This optimizes a particular eigenvalue in the displayed two-parameter family. It does
not claim the largest possible norm ratio among all five real 3 × 3 PSD matrices or an
optimal dimension-independent constant.

## 5. A one-parameter complex rank-one family

For $0\le r\le1$, take the four matrices

```math
 \frac54\begin{pmatrix}1&\pm r\\\pm r&r^2\end{pmatrix},\qquad
 \frac54\begin{pmatrix}1&\pm ir\\\mp ir&r^2\end{pmatrix},
```

together with $\mathrm{diag}(0,5(1-r^2))$. All are PSD, and their sum is $5I_2$.
For $r<1$, all five have rank one; at $r=1$ the fifth is zero. Their average full
product is diagonal, with entries

```math
 \lambda_0=\frac{625}{768}(-3r^2+r^4-r^6+3r^8), \qquad\text{(9)}
```
```math
 \lambda_1=\frac{625}{768}(-2r^2-r^4-9r^6+27r^8-15r^{10}). \qquad\text{(10)}
```

The case $r=4/5$, scaled by 20, is Theorem 2. Putting $s=r^2$, the exact operator norm
of this family is

```math
 g(s)=\frac{625}{768}s(1-s)(3+2s+3s^2),\qquad0\le s\le1.
```

To verify the choice of eigenvalue, both $\lambda_0$ and $\lambda_1$ are nonpositive,
since

```math
 -\lambda_1=\frac{625}{768}s(1-s)
   [2+3s(1-s)(1+5s)]\ge0.
```

The difference $(-\lambda_0)-(-\lambda_1)$ is the nonnegative factor $(625/768)s(1-s)$
times the strictly positive polynomial

```math
 15s^3-9s^2-s+1
 =15s(s-1/2)^2+6(s-19/48)^2+23/384.
```

Thus $|\lambda_0|$ determines the norm throughout the family.

The same function $g$ occurs on the slice $y=x=s$ of (8), and

```math
 g''(s)=\frac{625}{768}(-2+6s-36s^2)<0.
```

Its strict concavity gives an exact violation interval: $g(s)>1$ precisely between the
two roots in $(0,1)$ of

```math
 1875s^4-625s^3+625s^2-1875s+768=0.
```

These roots are approximately $0.5378448881$ and $0.7036308526$. In particular every
$r\in[3/4,5/6]$ gives a counterexample: the two endpoint excesses are exactly
$272159/16777216$ and $3315179/429981696$. Every rational $r$ in this interval gives
rational real and imaginary matrix entries.

The unique maximum of $g$ occurs at the root in $(0,1)$ of $12s^3-3s^2+2s-3=0$, and
equals approximately $1.034142605283665$. This is the exact norm optimum within the
displayed one-parameter family, not a global optimum over all complex PSD tuples. See
[COMPLEX_FAMILY.md](COMPLEX_FAMILY.md) for further proof and verification details.

## 6. Positive definiteness and larger full epochs

### An explicit positive definite real example

Let $A_i$ be the matrices of Section 2 and set $A_i(\delta)=A_i+\delta I_3$. Their mean
is $(20+\delta)I_3$. The central entry of their symmetrized product is

```math
 q_0(\delta)=\delta^5+100\delta^4+2950\delta^3+17700\delta^2
 -\frac{1021325}{3}\delta-3305280.
```

The strict-violation margin is

```math
\begin{aligned}
 -q_0(\delta)-(20+\delta)^5
 ={}&105280-\frac{1378675}{3}\delta-97700\delta^2\\
 &-6950\delta^3-200\delta^4-2\delta^5.
\end{aligned} \qquad\text{(11)}
```

All nonconstant coefficients are negative. At $\delta=1/5$ the right side is
$88166369/9375>0$, so it is positive on $[0,1/5]$. For every $0<\delta\le1/5$, all five
matrices are positive definite and violate (1). In particular **$N_i=10A_i+I_3$** are
positive definite integer matrices with mean $201I_3$, and

```math
 R_5(N)=\mathrm{diag}\left(
 -\frac{1001743261997}{3},-\frac{81674724997}{3},-\frac{81674724997}{3}\right).
```

Their exact norm ratio is $1001743261997/984241203003\approx1.0177822864$. The product
polynomial and the strict rational endpoint check are included in the exact script.
Strictness and continuity likewise yield positive definite perturbations of the complex
example. Positive definiteness alone is not claimed as a previously unavailable feature
in the literature.

### Identity padding

Normalize either primary family to mean $I$. For any $n\ge5$, adjoin $n-5$ labeled
copies of $I$. The mean remains $I$. In a uniform permutation of the enlarged
collection, the relative order of the five nonidentity labeled matrices is uniform on
$S_5$. Removing the identity factors therefore leaves the original averaged product, so
the ratio $10329/10000$ is unchanged at **$k=n$**.

The same argument applies to the normalized positive definite tuple. Direct sums with
identity blocks extend the examples to every higher dimension. Hence for every $n=k\ge5$
there are real examples in each dimension $d\ge3$ and complex examples in each dimension
$d\ge2$.

This is a full-epoch extension. It does not say that a *length-five* violation persists
after adding arbitrarily many identities. It therefore does not contradict a theorem
fixing $k=5$ and taking large $n$.

## 7. A precise optimization application and a metric distinction

For the real matrices in Section 2, set

```math
 B_i=A_i/42,\qquad Q_i=I_3-B_i,\qquad
 f_i(x)=\tfrac12x^TQ_ix.
```

The eigenvalues of $A_1,\ldots,A_4$ are $0,16,41$, and those of $A_5$ are $0,36,36$.
Thus $\frac1{42}I\preceq Q_i\preceq I$: every component is a strongly convex quadratic
with common minimizer zero. A component-gradient step of size one is exactly
$x\mapsto B_ix$.

Starting at $e_1$, independent with-replacement sampling for five steps has mean iterate

```math
 \mathbb E[x_5]_{\mathrm{wr}}=(20/42)^5e_1.
```

A uniformly reshuffled full epoch has mean iterate

```math
 \mathbb E[x_5]_{\mathrm{rr}}
 =-\frac{10329}{10000}(20/42)^5e_1.
```

For $m$ independent full epochs, the ratio of the norms of these expected iterates is
exactly $(10329/10000)^m$. Both schemes converge; the mean iterate under reshuffling has
the slower exponential decay in this direction.

**Expected squared error is different.** For unscaled $A_i$, write
$P_\sigma=A_{\sigma(1)}\cdots A_{\sigma(5)}$. Exact enumeration and the independent
replacement recurrence $T(X)=\frac15\sum_iA_iXA_i$ give

```math
\begin{aligned}
 \mathbb E_{\mathrm{rr}}[P_\sigma^TP_\sigma]
 &=\mathrm{diag}(52137052427520,26248489865856,26248489865856),\\
 T^5(I)
 &=\mathrm{diag}(222683810001920,145806819139584,145806819139584).
\end{aligned}
```

Every diagonal entry in the first matrix is strictly smaller. Dividing both matrices by
$42^{10}$ gives the second-moment comparison for the gradient steps. At the first epoch,
reshuffling therefore gives **smaller expected squared error for every nonzero starting
vector**, despite the larger norm of expected error in the displayed direction.

This exact separation is the application claimed here. It does not establish slower
expected-risk convergence for random reshuffling, and it does not refute the separate
palindromic inequality with these same matrices.

## 8. The real dimension-two boundary

The complex Hermitian witness does not settle the real symmetric 2 × 2 question. The
exact scripts verify fixed matrices and symbolic identities; optional numerical probes
in [experiments/](../experiments/README.md) do not supply nonexistence or global
optimality certificates.

A restricted real 2 × 2 family has the exact maximum

```math
 \frac{n^{n-1}}{8(n-1)(n-2)^{n-2}}\nearrow\frac{e^2}{8}<1,
 \qquad n\ge4.
```

[REAL_2X2_PROBE.md](REAL_2X2_PROBE.md) gives its counting proof and exact optimization.
This excludes violations only inside that explicitly defined family. The unrestricted
real dimension-two question remains unresolved here.

## 9. Literature and attribution

1. **Benjamin Recht and Christopher Ré**, *Toward a Noncommutative Arithmetic-geometric
   Mean Inequality: Conjectures, Case-studies, and Consequences*, COLT 2012, Conjecture
   1, formulas (8)–(9).
   [Proceedings PDF](https://proceedings.mlr.press/v23/recht12/recht12.pdf). Formula (8)
   is the operator comparison treated here; formula (9) is the separate second-moment
   comparison.

2. **Zehua Lai and Lek-Heng Lim**, *Recht–Ré Noncommutative Arithmetic-Geometric Mean
   Conjecture is False*, ICML 2020.
   [Proceedings](https://proceedings.mlr.press/v119/lai20a.html),
   [corrected arXiv manuscript](https://arxiv.org/pdf/2006.01510). This gives a
   nonconstructive disproof at five factors and establishes the two- and three-factor
   cases. The authors distinguish the lack of explicit witness matrices and the unknown
   smallest dimension. Lai's
   [author page](https://laizehua.github.io/publications/2020-11-21-noncommutative-am-gm/)
   warns of a printing error in the proceedings conjecture; use the original Recht–Ré or
   corrected arXiv statement.

3. **Christopher De Sa**, *Random Reshuffling is Not Always Better*, NeurIPS 2020,
   Section 2.1 and Statement 1.
   [Full paper](https://proceedings.neurips.cc/paper_files/paper/2020/file/42299f06ee419aa5d9d07798b56779e2-Paper.pdf).
   This gives explicit real dimension-five matrices, the exact $-19/16$ and $29/64$
   eigenvalues, and identity-padding extensions. The supporting `RRExact` benchmark
   formalizes this existing construction. It does not discover $19/16$ or replace a
   result known only numerically.

4. **Chulhee Yun, Suvrit Sra, and Ali Jadbabaie**, *Open Problem: Can Single-Shuffle SGD
   be Better than Reshuffling SGD and GD?*, COLT 2021.
   [Paper](https://proceedings.mlr.press/v134/yun21a/yun21a.pdf). This concerns a
   distinct multi-epoch ordering. Its two-dimensional examples are not counterexamples
   to (1).

5. **Binghui Peng**, *A Resolution of the SS–RS–GD Inequalities*, arXiv:2607.22620,
   2026. [Canonical record](https://arxiv.org/abs/2607.22620). This disproves the SS–RS
   ordering near the identity and proves an RS–GD comparison under a sufficiently strong
   near-identity condition. Those claims do not resolve the real dimension-two question
   considered here.

6. **Yimin Zhong**, *When the noncommutative AM-GM inequality holds*, arXiv:2610.04874,
   submitted October 4, 2026. [Canonical record](https://arxiv.org/abs/2610.04874). The
   abstract states the sufficient condition $n\ge2\lceil k/2\rceil^2$, so at $k=5$ it
   applies for $n\ge18$. This is complementary to $n=k=5$. This reference is used at
   abstract level; its full proof is not audited here.

7. **Anonymous**, *Exact Low-Length Recht–Ré Inequalities*, public unrefereed candidate
   package, version `v1.1.1-candidate`.
   [Versioned manuscript source](https://github.com/ipitchford/exact-low-length-recht-re-inequalities/blob/v1.1.1-candidate/paper/exact_low_length_recht_re.tex).
   It claims exact low-length inequalities, including all four-factor cases and a
   five-factor lower bound for $n\ge6$. The cited manuscript is not independently
   certified here. It is acknowledged as related candidate work, not treated as a
   refereed theorem or a source of the low-dimensional witnesses above.

8. **Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner**,
   *Mathematical exploration and discovery at scale*, arXiv:2511.02864, version 3,
   Section 6.28 / Problem 6.47. [Manuscript](https://arxiv.org/html/2511.02864v3),
   [original experimental notebook](https://github.com/google-deepmind/alphaevolve_repository_of_problems/blob/main/experiments/matrix_multiplication_amgm/matrix_multiplication_amgm.ipynb).
   The relevant experiments concern the average-of-norms variant associated with Duchi,
   not (1). The authors report no improving construction in that experiment. The
   manuscript and notebook do not supply a prior low-dimensional counterexample to the
   norm-of-mean inequality treated here.

This source assessment identifies no earlier published real 3 × 3 or complex Hermitian 2
× 2 witness to (1). Its coverage is limited, including the abstract-only reference noted
above, and does not establish exhaustive priority. The real construction reduces the
dimension of De Sa's explicit benchmark. No endorsement by the cited authors is claimed.
