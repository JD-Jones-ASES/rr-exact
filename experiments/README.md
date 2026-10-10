# Optional numerical probes

These floating-point programs explore real symmetric and complex Hermitian 2 × 2 tuples.
Their output is neither an exact certificate nor a proof of nonexistence or global
optimality. The certificate scripts in `scripts/` require none of these programs or
dependencies.

## Build and run

The probes require NumPy, SciPy, and a C++ compiler supporting the GCC/Clang
population-count builtins. From the repository root:

```sh
g++ -O3 -shared -fPIC experiments/spin.cpp -o experiments/spin.so
OPENBLAS_NUM_THREADS=1 python3 experiments/search.py 2 0 5 5 -1
```

The default library path is `experiments/spin.so`; `RR_SPIN_LIBRARY` can name an
absolute path to another build. Outputs are current-best JSON candidates in the ignored
`experiments/results/` directory. `--output-dir` selects another directory. The
mean-identity search reads initial candidates there, or from `--input-dir`. No compiled
binary is required in the repository.

The positional arguments to `search.py` are:

1. Spin-vector dimension: `2` for real symmetric matrices or `3` for complex Hermitian
   matrices. The matrix dimension is two in both cases.
2. Rank-one restriction: `0` allows radii in `[0,1]`; `1` fixes them at `1`.
3. Number of random starts for each requested tuple size.
4. Comma-separated numbers of matrices, always with product length `k=n`.
5. Spectral branch: `-1` maximizes `-lambda_min(Q)`; `1` maximizes `lambda_max(Q)`. The
   denominator is the actual mean norm to power `n`.

The default seed is `20261010`; `--seed` overrides it. A numerical value above the
candidate threshold stops the search early and must be independently reconstructed and
checked exactly.

For broader real symmetric probes, for example:

```sh
OPENBLAS_NUM_THREADS=1 python3 experiments/search.py 2 0 120 5,6,7,8,9,10,11,12 -1
OPENBLAS_NUM_THREADS=1 python3 experiments/search.py 2 0 120 5,6,7,8,9,10,11,12 1
OPENBLAS_NUM_THREADS=1 python3 experiments/isotropic.py 5 2 200
```

For complex Hermitian probes:

```sh
OPENBLAS_NUM_THREADS=1 python3 experiments/search.py 3 0 100 5 -1
OPENBLAS_NUM_THREADS=1 python3 experiments/isotropic.py 5 3 200
```

`isotropic.py` uses default seed `46`. If a matching negative-branch varying-mean JSON
candidate exists, it initializes the first start; otherwise that start is randomized.
Candidate availability, library versions, and platform can affect the trajectory. The
mean-identity constraint defines a subfamily; it is not a congruence reduction of
arbitrary tuples.

## Parameterization and computation

A real symmetric input is parameterized as

```math
 A_i=w_i\left[I+r_i\begin{pmatrix}
 \cos\theta_i&\sin\theta_i\\
 \sin\theta_i&-\cos\theta_i
 \end{pmatrix}\right],\qquad
 w_i=e^{s_i},\quad -3\le s_i\le3,\quad0\le r_i\le1.
```

The bounded log weights restrict relative traces. In the complex case the spin vector
has three components. A spin `(t,v)` represents `t I + v[0] sigma_z + v[1] sigma_x`,
with `v[2] sigma_y` in the complex case. Its Jordan product is

```math
 (t,v)\circ(u,w)=(tu+v\cdot w,tw+uv).
```

`spin.cpp` computes the average of all labeled ordered products by a subset recurrence,

```math
 S(\varnothing)=I,\qquad
 S(U)=\frac1{|U|}\sum_{i\in U} A_i\circ S(U\setminus\lbrace i\rbrace ).
```

Reversal pairs the ordered products, so their average is Hermitian and this Jordan
recurrence agrees with the fully symmetrized ordinary product. Reverse derivatives
support local optimization. When a vector part vanishes, the norm objective can be
nondifferentiable; the implementation selects a zero subgradient. This can affect
optimization near scalar means.

The wrapper accepts at most 20 factors because its time and memory grow exponentially
with the number of factors. SLSQP feasibility residuals are numerical tolerances, not
exact PSD certificates. These programs cannot settle unrestricted tuples, unsearched
trace ranges, or `k<n`.

The exact complex family is in [COMPLEX_FAMILY.md](../note/COMPLEX_FAMILY.md); a
restricted real family and its exact optimum are in
[REAL_2X2_PROBE.md](../note/REAL_2X2_PROBE.md).
