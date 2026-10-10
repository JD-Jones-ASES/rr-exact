# Exact norm 19/16 for a PSD counterexample to Recht–Ré

Five rational positive-semidefinite \(5\times 5\) matrices \(A_1,\ldots,A_5\) with
\(\sum_k A_k=5I\), for which the average over \(S_5\) of the ordered products has
operator norm exactly \(19/16>1\).

The family is De Sa's (NeurIPS 2020). His paper records the \(n=5\) average and
says it is easily checked numerically. This note replaces that check.

- Each \(A_k=I+\mathbf{1}y_k^{\mathsf T}+y_k\mathbf{1}^{\mathsf T}\) is positive semidefinite of rank \(n-1\), by completing the square, and the sum is \(nI\).
- The average sends the all-ones vector to \(a_n\) times itself. The scalar \(a_n\) is rational for every \(n\geq 2\), given by \(a_0=a_1=1\) and \((n-1)a_{t+1}=2(n-1)a_t-n a_{t-1}\). The coefficient depends on \(n\), so each \(n\) has its own sequence.
- The terminal values begin \(a_2=0\), \(a_3=-1/2\), \(a_4=-8/9\), \(a_5=-19/16\). So \(n=5\) is the first violation of this family, and the lower bound there is exactly \(19/16\). The \(n=5\) age table itself is \(1,1,3/4,1/4,-7/16,-19/16\).
- At \(n=5\) the average is exactly \((29/64)I-(21/64)J\). Its spectrum is \(-19/16\) once and \(29/64\) four times, so the operator norm is \(19/16\), not a larger number hiding on the orthogonal complement.

The matrices are rational precisely when \(n=m^2+1\). The first two such violations are \(n=5\), with norm \(19/16\), and \(n=10\), with all-ones factor \(-99712/59049\).

Not claimed: the minimal dimension (open below \(5\); De Sa's padding gives every \(d\geq 5\)); the symmetric-product form; a closed set of those \(n\) with \(|a_n|>1\). The certificate computes \(a_n\) through \(n=40\). On that range the absolute value drops back to at most \(1\) for \(17\leq n\leq 28\).

[PROOF.md](PROOF.md) is the argument. [VERIFICATION.md](VERIFICATION.md) says what the script checks and what it does not. [DISCLOSURE.md](DISCLOSURE.md) is the assistance statement. [note/PALOMAR.md](note/PALOMAR.md) is the cut a Lean formalization would have to make; this repository does not contain one.

```sh
python3 scripts/check_certificate.py
```

The script uses only the Python standard library. License: [MIT](LICENSE) for the script; the note [PROOF.md](PROOF.md) and [note/PALOMAR.md](note/PALOMAR.md) are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
