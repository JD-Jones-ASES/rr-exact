# Palomar cut

The compared statements are the five theorems in `RRExactChallenge.lean`, proved in `RRExact/Main.lean` and re-exported by `RRExactSolution.lean`.

1. Each \(A_k\) is symmetric and positive semidefinite, \(\sum_k A_k=5I\), and the kernel of \(A_k\) is the line through \(\kappa_k=\mathbf{1}-5y_k\).
2. `perms` is exactly \(S_5\), and the average of the \(120\) ordered products equals \((29/64)I-(21/64)J\).
3. That average sends \(\mathbf{1}\) to \(-(19/16)\mathbf{1}\), and its Euclidean operator norm is \(19/16\).
4. The recurrence \(a_0=a_1=1\), \((n-1)a_{t+1}=2(n-1)a_t-n a_{t-1}\), satisfies \(|a_n|\leq 1\) for \(n\in\{2,3,4\}\) and \(a_5=-19/16\). The \(n=5\) age table and \(a_{10}=-99712/59049\) are included.

Not stated: a minimal-dimension theorem, the symmetric-product inequality, or \(|a_n|>1\) for every \(n\geq 5\).

Classification in `formalization.yaml`: `math.FA` and `math.OC`, MSC `15A45`, `15A60`, `47A30`.
