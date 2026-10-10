# Intended Palomar cut

Not a submission. There is no Lean development in this repository. The statements below are the ones a later formalization would put in `Challenge.lean`, against Mathlib only, with `Solution.lean` proving them from the three standard axioms.

The mathematical account those statements have to match is PROOF.md. The finite half is the entrywise identity for the average of \(120\) products; the hand half is the completed-square bound and the age recurrence. A formalization that checks only the matrix identity, and cites the hand half as comments, would be proving less than the note.

Suggested declarations, over \(\mathbb{Q}\), with the five matrices written as the integer matrix in PROOF.md divided by \(10\) and its coordinate permutations:

1. Each \(A_k\) is symmetric positive semidefinite, and \(\sum_{k=1}^5 A_k=5I\).
2. The average \(R\) of the \(120\) ordered products equals \((29/64)I-(21/64)J\).
3. \(R\mathbf{1}=-(19/16)\mathbf{1}\), and the operator norm of \(R\) is \(19/16\). Equivalently, \(285/2\) is the operator norm of the un-normalized sum, which is strictly larger than \(120\).
4. The recurrence \(a_0=a_1=1\), \((n-1)a_{t+1}=2(n-1)a_t-n a_{t-1}\), satisfies \(|a_n|\leq 1\) for \(n\in\{2,3,4\}\) and \(a_5=-19/16\).

Optional, still rational, and not required for the norm: the same positive-semidefinite and sum statements at \(n=10\), together with \(a_{10}=-99712/59049\).

Do not state a minimal-dimension theorem. Do not state the symmetric-product inequality. Do not state that \(|a_n|>1\) for all \(n\geq 5\).

Classification, if a `formalization.yaml` is written later: `math.FA` or `math.OC`, and MSC `15A45`, `15A60`, `47A30`. The result is source-based (De Sa, NeurIPS 2020) with the exact norm and the recurrence proved in this note. Automation would be disclosed as an agent draft of the argument and the certificate, not as a checked Lean proof.
