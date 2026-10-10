# Low-dimensional exact counterexamples to the Recht–Ré inequality

Five real symmetric positive-semidefinite **3 × 3 integer matrices** and five complex
Hermitian positive-semidefinite **2 × 2 Gaussian-integer matrices** each satisfy

```math
\frac{\left\Vert\frac1{120}\sum_{\sigma\in S_5}
 A_{\sigma(0)}A_{\sigma(1)}A_{\sigma(2)}A_{\sigma(3)}A_{\sigma(4)}\right\Vert_{\mathrm{op}}}
 {\left\Vert\frac15\sum_{i=0}^4 A_i\right\Vert_{\mathrm{op}}^5}
=\frac{10329}{10000}>1.
```

The norm is the Euclidean operator norm. Both tuples sum to $100I$; their averaged
products are respectively

```math
\mathrm{diag}(-3305280,-291264,-291264),\qquad
\mathrm{diag}(-3305280,-2941824).
```

Integer and Gaussian-integer Gram factors certify positivity. Exact arithmetic certifies
every product. The real matrices have rank two and the complex matrices rank one.
Complex dimension two is minimal, by scalar AM–GM in dimension one. The unrestricted
real symmetric 2 × 2 question remains unresolved here.

## Formal result

The Palomar contracts `RRExact.real_counterexample` and `RRExact.complex_counterexample`
in [RRExactChallenge.lean](RRExactChallenge.lean) assert the existence of real 3 × 3 and
complex 2 × 2 PSD tuples violating the inequality. Their statements use Mathlib
matrices, positive semidefiniteness, Euclidean operator norms, and the sum over
`Equiv.Perm (Fin 5)`; they do not import project definitions.
[RRExactSolution.lean](RRExactSolution.lean) provides the proofs through
[RRExact/Canonical.lean](RRExact/Canonical.lean).

[VERIFICATION.md](VERIFICATION.md) specifies the exact formal scope, reproduction
commands, and release checks. The permitted axioms are `propext`, `Quot.sound`, and
`Classical.choice`.

## Mathematics

[LOW_DIMENSION.md](note/LOW_DIMENSION.md) contains the explicit witnesses and
supplementary proofs:

- A real family with a polynomial product formula, a stronger integer witness of ratio
  $8701875/8388608$, and the algebraic optimum of its central branch.
- A complex rank-one family with an exact norm formula and violation interval.
- Positive definite integer examples and padding to every full-epoch length $n=k\ge5$
  and every larger matrix dimension.
- A quadratic-optimization example distinguishing the norm of expected error from
  expected squared error.

These supplementary results are distinct from the two compared Lean contracts. The
restricted real 2 × 2 family in [REAL_2X2_PROBE.md](note/REAL_2X2_PROBE.md) has exact
maximal norm $n^{n-1}/[8(n-1)(n-2)^{n-2}]<1$; this gives no bound for arbitrary real 2 ×
2 tuples.

[PROOF.md](PROOF.md) presents De Sa's published dimension-five counterexample, with
exact norm $19/16$. Its rational Lean certificates remain a supporting benchmark; the
matrices, spectrum, and ratio are attributed to De Sa.

## Context

Recht–Ré posed the inequality in 2012. Lai–Lim disproved its universal form in 2020, and
De Sa gave an explicit real dimension-five construction that year. The real example here
reduces the dimension of that explicit benchmark to three. The source assessment in
[LOW_DIMENSION.md](note/LOW_DIMENSION.md) identifies no earlier published real 3 × 3 or
complex Hermitian 2 × 2 witness. This assessment is qualified by its coverage, including
abstract-only sources; it is not an exhaustive priority claim.

See [DISCLOSURE.md](DISCLOSURE.md) for assistance and attribution, and
[note/PALOMAR.md](note/PALOMAR.md) for submission scope. License: [MIT](LICENSE).
