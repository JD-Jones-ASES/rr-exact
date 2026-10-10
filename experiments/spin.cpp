// Floating-point discovery only; never used by the exact certificate checkers.
// Compile: g++ -O3 -shared -fPIC experiments/spin.cpp -o experiments/spin.so
#include <vector>
#include <cmath>
#include <algorithm>

// Spin dimension d=2 represents real symmetric 2x2 matrices; d=3 represents
// complex Hermitian 2x2 matrices.  Each input is (scalar, vector coordinates).
// sign=-1/1 selects -lambda_min/lambda_max with mean-norm normalization.
// sign=-2/2 selects the same branch without normalization, for a constrained
// mean-I optimization.  grad is the analytic derivative where norms are smooth.
extern "C" double spin_eval(int n, int d, const double* aa, double* grad, int sign) {
    const bool normalized = std::abs(sign) == 1;
    sign = sign > 0 ? 1 : -1;
    const int q = d + 1, N = 1 << n;
    std::vector<double> a(n*q), s(N*q, 0), b(N*q, 0), g(n*q, 0), total(q, 0);
    for (int i=0; i<n; i++)
        for (int j=0; j<q; j++) total[j] += aa[i*q+j];
    double vn = 0;
    for (int j=1; j<q; j++) vn += total[j]*total[j];
    vn = std::sqrt(vn);
    const double m = normalized ? (total[0]+vn)/n : 1;
    for (int i=0; i<n*q; i++) a[i] = aa[i]/m;
    s[0] = 1;

    // S(U) = |U|^{-1} sum_i A_i Jordan S(U\i).
    for (int mask=1; mask<N; mask++) {
        const double inv = 1.0/__builtin_popcount((unsigned)mask);
        double* r = &s[mask*q];
        for (int z=mask; z; z&=z-1) {
            const int i = __builtin_ctz((unsigned)z), sub = mask^(1<<i);
            const double* u = &a[i*q];
            const double* v = &s[sub*q];
            double t = u[0]*v[0];
            for (int j=1; j<q; j++) t += u[j]*v[j];
            r[0] += t*inv;
            for (int j=1; j<q; j++) r[j] += (u[0]*v[j]+v[0]*u[j])*inv;
        }
    }
    const double* r = &s[(N-1)*q];
    double norm = 0;
    for (int j=1; j<q; j++) norm += r[j]*r[j];
    norm = std::sqrt(norm);
    const double value = sign*r[0]+norm;
    b[(N-1)*q] = sign;
    if (norm>1e-25)
        for (int j=1; j<q; j++) b[(N-1)*q+j] = r[j]/norm;
    if (!grad) return value;

    // Reverse derivatives of the subset recurrence.
    for (int mask=N-1; mask>=1; mask--) {
        const double* adj = &b[mask*q];
        const double inv = 1.0/__builtin_popcount((unsigned)mask);
        for (int z=mask; z; z&=z-1) {
            const int i = __builtin_ctz((unsigned)z), sub = mask^(1<<i);
            const double* u = &a[i*q];
            const double* v = &s[sub*q];
            double* bs = &b[sub*q];
            double* gi = &g[i*q];
            double t1 = adj[0]*u[0], t2 = adj[0]*v[0];
            for (int j=1; j<q; j++) {
                t1 += adj[j]*u[j];
                t2 += adj[j]*v[j];
            }
            bs[0] += inv*t1;
            gi[0] += inv*t2;
            for (int j=1; j<q; j++) {
                bs[j] += inv*(adj[0]*u[j]+u[0]*adj[j]);
                gi[j] += inv*(adj[0]*v[j]+v[0]*adj[j]);
            }
        }
    }
    for (int i=0; i<n; i++) {
        grad[i*q] = (g[i*q]-(normalized ? value : 0))/m;
        for (int j=1; j<q; j++)
            grad[i*q+j] = (g[i*q+j] -
                (normalized && vn>1e-18 ? value*total[j]/vn : 0))/m;
    }
    return value;
}
