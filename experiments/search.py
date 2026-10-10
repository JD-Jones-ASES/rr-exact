#!/usr/bin/env python3
"""Optional floating-point search, with bounded relative traces.

This is discovery software, not a certificate or a global optimization proof.
See README.md for usage and the meaning of spin dimension.
"""
import argparse
import ctypes
import json
import os
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "results"
library_path = os.environ.get("RR_SPIN_LIBRARY", str(HERE / "spin.so"))
lib = ctypes.CDLL(library_path)
lib.spin_eval.argtypes = [
    ctypes.c_int, ctypes.c_int,
    np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
    np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
    ctypes.c_int,
]
lib.spin_eval.restype = ctypes.c_double


def evaluate(a, sign=-1):
    a = np.ascontiguousarray(a, dtype=np.float64)
    if a.ndim != 2 or a.shape[1] not in (3, 4) or not 1 <= len(a) <= 20:
        raise ValueError("Expected 1..20 spin vectors of dimension 2 or 3.")
    if sign not in (-2, -1, 1, 2):
        raise ValueError("sign must be -2, -1, 1, or 2.")
    if abs(sign) == 1 and a[:, 0].sum() + np.linalg.norm(a[:, 1:].sum(axis=0)) <= 0:
        raise ValueError("The normalization denominator must be positive.")
    gradient = np.zeros_like(a)
    value = lib.spin_eval(len(a), a.shape[1]-1, a, gradient, sign)
    return value, gradient


def unpack(x, n, d, rankone=False):
    x = x.reshape(n, -1)
    w, theta = np.exp(x[:, 0]), x[:, 1]
    radii = np.ones(n) if rankone else x[:, d]
    if d == 2:
        vectors = np.stack([np.cos(theta), np.sin(theta)], axis=1)
    else:
        phi = x[:, 2]
        vectors = np.stack([np.cos(theta)*np.cos(phi),
                            np.sin(theta)*np.cos(phi), np.sin(phi)], axis=1)
    a = np.column_stack([w, w[:, None]*radii[:, None]*vectors])
    return a, w, radii, vectors, x


def objective(x, n, d, rankone=False, sign=-1):
    a, w, radii, vectors, x = unpack(x, n, d, rankone)
    value, gradient = evaluate(a, sign)
    result = np.empty_like(x)
    result[:, 0] = np.sum(gradient*a, axis=1)
    if d == 2:
        tangent = np.stack([-vectors[:, 1], vectors[:, 0]], axis=1)
    else:
        theta, phi = x[:, 1], x[:, 2]
        tangent = np.stack([-np.sin(theta)*np.cos(phi),
                            np.cos(theta)*np.cos(phi), np.zeros(n)], axis=1)
        phi_tangent = np.stack([-np.cos(theta)*np.sin(phi),
                                -np.sin(theta)*np.sin(phi), np.cos(phi)], axis=1)
        result[:, 2] = w*radii*np.sum(gradient[:, 1:]*phi_tangent, axis=1)
    result[:, 1] = w*radii*np.sum(gradient[:, 1:]*tangent, axis=1)
    if not rankone:
        result[:, d] = w*np.sum(gradient[:, 1:]*vectors, axis=1)
    return -value, -result.ravel()


def start(n, d, rankone, rng):
    x = np.empty((n, d if rankone else d+1))
    x[:, 0] = rng.normal(0, .5, n)
    x[:, 1] = rng.uniform(-np.pi, np.pi, n)
    if d == 3:
        x[:, 2] = np.arcsin(rng.uniform(-1, 1, n))
    if not rankone:
        x[:, d] = rng.uniform(.6, 1, n)
    return x.ravel()


def run(ns, tries, d, rankone, seed=20261010, sign=-1, output_dir=DEFAULT_OUTPUT):
    rng = np.random.default_rng(seed)
    all_best, begun = {}, time.time()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for n in ns:
        if not 2 <= n <= 20:
            raise ValueError("Search supports 2 <= n <= 20.")
        bounds = ([(-3, 3)] + [(None, None)]*(d-1)
                  + ([] if rankone else [(0, 1)]))*n
        best = -100
        for trial in range(tries):
            initial = start(n, d, rankone, rng)
            result = minimize(
                objective, initial, args=(n, d, rankone, sign), jac=True,
                bounds=bounds, method="L-BFGS-B",
                options={"maxiter": 1000, "ftol": 1e-13,
                         "gtol": 1e-8, "maxls": 40},
            )
            value = -result.fun
            if value > best + 1e-8:
                best = value
                a, *_ = unpack(result.x, n, d, rankone)
                info = {
                    "n": n, "d_vector": d, "rankone": rankone,
                    "value": best, "trial": trial, "success": result.success,
                    "message": result.message, "matrices_spin": a.tolist(),
                    "x": result.x.tolist(), "time": time.time()-begun,
                }
                all_best[str(n)] = info
                suffix = "_positive" if sign > 0 else ""
                filename = "best_d{}_r{}_n{}{}.json".format(d, int(rankone), n, suffix)
                (output_dir / filename).write_text(json.dumps(info, indent=2)+"\n")
                print(n, trial, best, result.success, result.nit,
                      round(time.time()-begun, 2), flush=True)
            if best > 1.0000000001:
                print("NUMERICAL_CANDIDATE; exact verification required", flush=True)
                return all_best
        print("DONE", n, best, flush=True)
    return all_best


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dimension", type=int, choices=(2, 3), nargs="?", default=2)
    parser.add_argument("rankone", type=int, choices=(0, 1), nargs="?", default=0)
    parser.add_argument("starts", type=int, nargs="?", default=100)
    parser.add_argument("sizes", nargs="?", default="5,6,7,8,9,10,11,12")
    parser.add_argument("sign", type=int, choices=(-1, 1), nargs="?", default=-1)
    parser.add_argument("--seed", type=int, default=20261010)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    run(list(map(int, args.sizes.split(","))), args.starts, args.dimension,
        bool(args.rankone), args.seed, args.sign, args.output_dir)
