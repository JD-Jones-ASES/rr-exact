# Exact norm 19/16 for a PSD counterexample to Recht–Ré

Five rational positive-semidefinite \(5\times 5\) matrices \(A_1,\ldots,A_5\) with
\(\sum_k A_k=5I\), for which the average over \(S_5\) of the ordered products has
operator norm exactly \(19/16>1\).

The family is De Sa's (NeurIPS 2020). His paper records the \(n=5\) average and
says it is easily checked numerically. The Lean development replaces that check.

- Each \(A_k=I+\mathbf{1}y_k^{\mathsf T}+y_k\mathbf{1}^{\mathsf T}\) is symmetric and positive semidefinite, with kernel the line through \(\mathbf{1}-5y_k\), and the five matrices sum to \(5I\).
- The average sends the all-ones vector to \(a_n\) times itself. The scalar \(a_n\) is rational for every \(n\geq 2\), given by \(a_0=a_1=1\) and \((n-1)a_{t+1}=2(n-1)a_t-n a_{t-1}\).
- The terminal values begin \(a_2=0\), \(a_3=-1/2\), \(a_4=-8/9\), \(a_5=-19/16\). So \(n=5\) is the first violation of this family. The \(n=5\) age table is \(1,1,3/4,1/4,-7/16,-19/16\).
- At \(n=5\) the average of the \(120\) ordered products is exactly \((29/64)I-(21/64)J\). Its spectrum is \(-19/16\) once and \(29/64\) four times, so the operator norm is \(19/16\).

The matrices are rational precisely when \(n=m^2+1\). The same recurrence gives \(a_{10}=-99712/59049\).

Not claimed: the minimal dimension (open below \(5\)); the symmetric-product form; a closed set of those \(n\) with \(|a_n|>1\). On the range computed by the script, the absolute value drops back to at most \(1\) for \(17\leq n\leq 28\).

The compared Lean statements are `RRExact.family_psd`, `RRExact.average_closed`, `RRExact.operator_norm`, `RRExact.operator_norm_sharp`, and `RRExact.recurrence_bound`. [PROOF.md](PROOF.md) is the argument. [VERIFICATION.md](VERIFICATION.md) says what is checked. [DISCLOSURE.md](DISCLOSURE.md) is the assistance statement. [note/PALOMAR.md](note/PALOMAR.md) is the submission cut.

```sh
python3 scripts/check_certificate.py
lake build RRExact RRExactChallenge RRExactSolution
```

Lean `v4.35.0-rc3`, Mathlib `a98628e16c11f5167f16124105ddce53efa9bfe5`. The permitted axioms are `propext`, `Quot.sound`, and `Classical.choice`.

License: [MIT](LICENSE).
