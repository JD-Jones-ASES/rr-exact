#!/usr/bin/env python3
"""Optional search within the mean-I subfamily; no general reduction is claimed."""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

import search


def unpack(x, n, d):
    a = x.reshape(n-1, d+1)
    return np.vstack([a, np.r_[n-np.sum(a[:, 0]), -a[:, 1:].sum(axis=0)]])


def objective(x, n, d):
    a = unpack(x, n, d)
    value, gradient = search.evaluate(a, -2)
    return -value, -(gradient[:-1]-gradient[-1]).ravel()


def constraints(x, n, d):
    a = unpack(x, n, d)
    return a[:, 0]**2 - np.sum(a[:, 1:]**2, axis=1)


def jacobian(x, n, d):
    a = unpack(x, n, d)
    q, signs = d+1, np.r_[1, -np.ones(d)]
    result = np.zeros((n, (n-1)*q))
    for i in range(n-1):
        result[i, i*q:(i+1)*q] = 2*a[i]*signs
    result[-1] = np.tile(-2*a[-1]*signs, n-1)
    return result


def run(n, d, tries, seed=46, output_dir=search.DEFAULT_OUTPUT, input_dir=None):
    if not 2 <= n <= 20:
        raise ValueError("Search supports 2 <= n <= 20.")
    output_dir = Path(output_dir)
    input_dir = output_dir if input_dir is None else Path(input_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rng, best, begun = np.random.default_rng(seed), -1, time.time()
    for trial in range(tries):
        initial = None
        if trial == 0:
            previous = input_dir / "best_d{}_r0_n{}.json".format(d, n)
            if previous.exists():
                a = np.array(json.loads(previous.read_text())["matrices_spin"])
                a *= n/a[:, 0].sum()
                initial = a[:-1].ravel()
        if initial is None:
            a = rng.normal(size=(n, d+1))
            a[:, 1:] -= a[:, 1:].mean(axis=0)
            a[:, 0] = np.linalg.norm(a[:, 1:], axis=1) + rng.uniform(0, .5, n)
            a *= n/a[:, 0].sum()
            initial = a[:-1].ravel()
        bounds = ([(0, n)]+[(-n, n)]*d)*(n-1)
        result = minimize(
            objective, initial, args=(n, d), jac=True, method="SLSQP", bounds=bounds,
            constraints=[
                {"type": "ineq", "fun": constraints, "jac": jacobian, "args": (n, d)},
                {"type": "ineq", "fun": lambda x: unpack(x, n, d)[-1, 0]},
            ],
            options={"maxiter": 1500, "ftol": 2e-13},
        )
        value = -result.fun
        minimum_determinant = float(constraints(result.x, n, d).min())
        feasible = minimum_determinant > -1e-7
        if feasible and value > best + 1e-9:
            best = value
            info = {
                "n": n, "d_vector": d, "value": best, "trial": trial,
                "success": result.success, "message": result.message,
                "matrices_spin": unpack(result.x, n, d).tolist(),
                "x": result.x.tolist(), "time": time.time()-begun,
                "min_det": minimum_determinant,
            }
            (output_dir / "iso_d{}_n{}.json".format(d, n)).write_text(
                json.dumps(info, indent=2)+"\n")
            print(n, d, trial, best, result.success, result.nit,
                  round(time.time()-begun, 2), flush=True)
    print("DONE", n, d, best, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("dimension", type=int, choices=(2, 3))
    parser.add_argument("starts", type=int)
    parser.add_argument("--seed", type=int, default=46)
    parser.add_argument("--output-dir", type=Path, default=search.DEFAULT_OUTPUT)
    parser.add_argument("--input-dir", type=Path)
    args = parser.parse_args()
    run(args.n, args.dimension, args.starts, args.seed, args.output_dir, args.input_dir)
