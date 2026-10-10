# Palomar submission scope

**Title:** Low-dimensional exact counterexamples to the Recht–Ré inequality

## Contribution

Five real symmetric PSD 3 × 3 integer matrices and five complex Hermitian PSD 2 × 2
Gaussian-integer matrices violate the norm-of-averaged-product inequality at $n=k=5$.
Both have mean $20I$ and exact norm ratio $10329/10000$. Their averaged products are
diagonal, and integer or Gaussian-integer Gram factors certify positivity.

The real example reduces the dimension of De Sa's explicit dimension-five benchmark. The
complex example attains the smallest possible complex dimension. It does not resolve the
real symmetric dimension-two question.

## Formal contract

[RRExactChallenge.lean](../RRExactChallenge.lean) contains two existential contracts,
`RRExact.real_counterexample` and `RRExact.complex_counterexample`, using only Mathlib
imports. Each asserts a tuple of five PSD matrices, sum $100I$, the explicit diagonal
average, arithmetic-mean norm $20$, fifth-power norm $3200000$, permutation-average norm
$3305280$, strict violation, and ratio $10329/10000$. The ordered products are summed
over `Equiv.Perm (Fin 5)` and the norm is Mathlib's Euclidean operator norm.

[RRExactSolution.lean](../RRExactSolution.lean) supplies both proofs.
[comparator.json](../comparator.json) specifies the compared declarations. Only
`propext`, `Quot.sound`, and `Classical.choice` are permitted axioms. Verification
commands and evidence requirements are in [VERIFICATION.md](../VERIFICATION.md).

The concrete witness lemmas and De Sa's rational dimension-five benchmark remain
supporting library results. They are audited alongside the two main contracts. The
benchmark uses custom rational quadratic forms and squared norms; it is not a further
standard real operator-norm contract.

## Supplementary scope

[LOW_DIMENSION.md](LOW_DIMENSION.md), [COMPLEX_FAMILY.md](COMPLEX_FAMILY.md), and
[REAL_2X2_PROBE.md](REAL_2X2_PROBE.md) prove parameterized families, family-specific
optima, a stronger rational real example, positive definite perturbations, full-epoch
padding, and the optimization metric distinction. Exact Python scripts check the fixed
products and polynomial identities. These are not additional compared Lean statements.

Ranks follow from the displayed Gram factors. The complex dimension-one exclusion
follows from scalar AM–GM. Neither a global optimum over matrix tuples nor a real
dimension-two exclusion is claimed. The separate palindromic/second-moment inequality is
not disproved by these witnesses.

The low-dimensional contribution is qualified by the literature assessment in
[LOW_DIMENSION.md](LOW_DIMENSION.md). De Sa's dimension-five construction is attributed
as an existing mathematical result.

Classification: `math.OC`, `math.FA`; MSC `15A45`, `15A60`, `47A30`.
