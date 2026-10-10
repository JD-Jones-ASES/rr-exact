# Verification

Two independent checks.

`scripts/check_certificate.py` is exact rational arithmetic. It does not call a floating-point eigensolver. Run it with `python3 scripts/check_certificate.py`. A nonzero exit is a failed identity.

What the script checks:

- For \(n=5\) and \(n=10\), the vectors are orthogonal to the all-ones vector, have squared length \(1/n\), have pairwise inner product \(-1/(n(n-1))\), and sum to zero.
- Each matrix equals \(I+\mathbf{1}y^{\mathsf T}+y\mathbf{1}^{\mathsf T}\), is symmetric, kills \(\mathbf{1}-ny\), and sums with the others to \(nI\).
- The quadratic identity and the completed-square gap, on the all-ones vector, on \(y\), and on \((1,2,\ldots,n)\).
- The age recurrence and the second-order recurrence agree for every \(n\) from \(2\) through \(40\), the age table at \(n=5\) is the one in PROOF.md, \(a_5=-19/16\), and \(a_{10}=-99712/59049\).
- The first \(n\) with \(|a_n|>1\) is \(5\).
- The average of all \(120\) ordered products at \(n=5\) equals \((29/64)I-(21/64)J\) entrywise, the all-ones eigenvalue of that matrix is \(-19/16\), and the complementary eigenvalue \(29/64\) is strictly smaller in absolute value.

The Lean development checks the \(n=5\) theorems named in `comparator.json`, including the kernel line for every rational vector, not only the sample vectors, and the operator-norm inequality for every rational vector. Build with

```sh
lake build RRExact RRExactChallenge RRExactSolution
```

`RRExactChallenge` is the contract and contains `sorry`. `RRExactSolution` imports the proofs and does not. The script `scripts/emit_certificate.py` regenerates the literal matrix multiplications in `RRExact/Cert*.lean`; those files are already checked into the repository.

What neither check claims:

- No dimension below \(5\).
- The positive-semidefinite square roots and the symmetric-product inequality.
- Any term \(a_n\) for \(n>40\), and no theorem that describes \(\{n:|a_n|>1\}\) past the computed range. The Lean proof records \(a_{10}\) and the values through \(a_5\), not the whole table to \(40\).
