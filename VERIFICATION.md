# Verification

The two primary contracts concern full Euclidean operator-norm counterexamples over the
real and complex fields. Exact Python checks provide a separate arithmetic replay.
Numerical optimization is not a proof dependency.

## Exact arithmetic

All certificate scripts use the Python standard library:

```sh
python3 scripts/check_certificate.py
python3 scripts/check_low_dim.py
python3 scripts/check_complex_certificate.py
python3 scripts/check_complex_family.py
python3 scripts/check_real_2x2_family.py
python3 scripts/check_negative_controls.py
```

| Checker | Scope |
|---|---|
| `check_certificate.py` | De Sa's dimension-five exact average and norm, rational vector identities at $n=5,10$, and finite recurrence values through $n=40$. |
| `check_low_dim.py` | Real 3 × 3 Gram factors, 120 direct products, independent subset recurrence, canonical and stronger witnesses, general family and identity-shift polynomial identities, positive definite witness, $n=6$ padding control, and second-moment matrices. |
| `check_complex_certificate.py` | Nonzero rank-one Gaussian-integer Gram factors, Hermitian symmetry, all 120 ordered products, both eigenvalues, and exact ratio. |
| `check_complex_family.py` | Gaussian-polynomial product identity, sum-of-squares norm comparison, rational violation interval, and algebraic root brackets. |
| `check_real_2x2_family.py` | Exact labeled-product checks for the restricted real family at $n=4,5,6,7,8$. |

The polynomial checks compare all coefficients. Finite padding and restricted family
controls support the general written proofs; they do not establish universal claims by
sampling. The low-dimensional checkers use explicit failures that remain active under
`python3 -O`.

The nine negative controls reject altered real and Gaussian entries, omitted
permutations, a corrupted product sum, forbidden axioms, a solution proof hole,
a missing module header, and a project import in the Challenge. CI runs the
arithmetic scripts and these controls both normally and with `python3 -O`.

## Lean and independent kernel checks

The project pins Lean `v4.35.0-rc3` and Mathlib
`a98628e16c11f5167f16124105ddce53efa9bfe5` in the toolchain and Lake files. After
installing the pinned toolchain and fetching dependencies and cache:

```sh
lake exe cache get
python3 scripts/check_contract.py
bash scripts/build_lean.sh
python3 scripts/check_axioms.py
```

The build helper compiles the large dimension-five certificate modules sequentially
before the library, challenge, and solution. The challenge contains intentional proof
stubs; the solution does not import those stubs. Finite arithmetic uses ordinary kernel
`decide`, not `native_decide`.

The authoritative release check is Linux CI for the exact repository commit, using the
Palomar verifier pinned at `d4e41c1d5b0d114c4859e6e5831dc6d3ad1d0d44`: Comparator must
accept both challenge/solution contracts and only the permitted axioms `propext`,
`Quot.sound`, and `Classical.choice`; Lean, NanoDa, and `con-ron` replay must succeed. A
build or a dated report for another working tree is not evidence for a changed release
commit. CI status and the verified commit must be checked together before describing a
release as ready.

The [verification workflow](.github/workflows/verify.yml) runs this official
mechanical preflight and a separate fresh Linux build of the full library,
including all nine principal and supporting axiom audits. Its
[GitHub Actions runs](https://github.com/JD-Jones-ASES/rr-exact/actions/workflows/verify.yml)
identify the exact tested commits. The preflight does not submit or register
the project with Palomar.

## The compared statements

The contracts `RRExact.real_counterexample` and `RRExact.complex_counterexample` in
[RRExactChallenge.lean](RRExactChallenge.lean) use only Mathlib imports. They assert the
existence of five real PSD 3 × 3 matrices and five complex Hermitian PSD 2 × 2 matrices,
respectively, with:

1. Sum $100I$ and arithmetic-mean norm $20$.
2. Exact diagonal permutation averages, as displayed in the README.
3. Fifth-power arithmetic-mean norm $3200000$ and permutation-average norm $3305280$.
4. Strict failure of the inequality and exact ratio $10329/10000$.

The averages sum over `Equiv.Perm (Fin 5)` and divide by $120$.
`Matrix.Norms.L2Operator` selects the Euclidean operator norm.
[RRExact/Canonical.lean](RRExact/Canonical.lean) connects this standard permutation sum
to the complete explicit enumeration used by the witnesses.

The concrete witness proofs establish positivity over all real or complex vectors, exact
scalar sums and diagonal averages, and both full operator norms. Their integer and
Gaussian-integer calculations are transported to $\mathbb R$ and $\mathbb C$ by ring
homomorphisms. The supporting permutation list is certified complete, valid, and
duplicate-free.

The axiom audit covers both main contracts and seven supporting witness and benchmark
declarations. The dimension-five benchmark statements use rational vectors and custom
quadratic-form and squared-norm definitions. Its recurrence theorem gives specified
scalar evaluations; it does not prove the general-dimensional matrix recurrence
connection.

## Supplementary mathematics

The stronger real witness, parameterized families and optima, rank claims, positive
definite perturbations, arbitrary identity padding, complex minimal-dimension argument,
and quadratic-optimization application have written elementary proofs. They are not
additional compared Lean contracts. Their exact arithmetic checks have the scope
specified above.

The optional numerical programs in [experiments/](experiments/README.md) cannot
establish global optimality or exclude unrestricted real 2 × 2 counterexamples. No
separate palindromic/second-moment disproof is claimed.
