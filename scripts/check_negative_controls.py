#!/usr/bin/env python3
"""Ensure corrupted witnesses, incomplete enumeration, and source drift fail.

Controls patch module objects or isolated temporary source copies. Tracked files
are never modified. Run both normally and with Python -O.
"""
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from pathlib import Path
import shutil
import tempfile

import check_complex_certificate as complex_certificate
import check_low_dim as real_certificate
from check_contract import ROOT, check_contract


def rejected(label, operation, diagnostic):
    try:
        with redirect_stdout(StringIO()):
            operation()
    except (ArithmeticError, RuntimeError, ValueError) as error:
        if diagnostic not in str(error):
            raise RuntimeError(f"{label}: unexpected rejection: {error}") from error
        print(f"PASS: rejected {label} ({diagnostic})")
    else:
        raise RuntimeError(f"Negative control was accepted: {label}")


@contextmanager
def patched(module, name, value):
    original = getattr(module, name)
    setattr(module, name, value)
    try:
        yield
    finally:
        setattr(module, name, original)


def main():
    original_family = real_certificate.family

    def bad_family(*args):
        matrices = original_family(*args)
        matrices[0][0][0] += 1
        return matrices

    with patched(real_certificate, "family", bad_family):
        rejected("changed real matrix entry", real_certificate.check_canonical, "PSD Gram identity")

    matrices = original_family(25, 20, 16, 16, 36)
    original_permutations = real_certificate.permutations
    with patched(real_certificate, "permutations", lambda values: list(original_permutations(values))[:-1]):
        rejected("missing real permutation", lambda: real_certificate.ordered_sum(matrices),
                 "permutation count")

    original_ordered_sum = real_certificate.ordered_sum

    def bad_sum(*args, **kwargs):
        total = original_ordered_sum(*args, **kwargs)
        total[0][0] += 1
        return total

    with patched(real_certificate, "ordered_sum", bad_sum):
        rejected("corrupted real product sum", real_certificate.check_canonical,
                 "independent subset recurrence")

    changed = list(complex_certificate.MATRICES)
    changed[2] = (changed[2][0], (0, -19), changed[2][2], changed[2][3])
    with patched(complex_certificate, "MATRICES", tuple(changed)):
        rejected("changed Gaussian entry", complex_certificate.verify, "Gram factorization failed")

    original_permutations = complex_certificate.permutations
    with patched(complex_certificate, "permutations", lambda values: list(original_permutations(values))[:-1]):
        rejected("missing complex permutation", complex_certificate.verify,
                 "Exactly 120 ordered products")

    with tempfile.TemporaryDirectory(prefix="rr-exact-controls-") as temporary:
        fixture = Path(temporary)
        for path in ROOT.glob("*.lean"):
            shutil.copy2(path, fixture / path.name)
        for name in ("comparator.json", "lakefile.toml", "lake-manifest.json", "lean-toolchain"):
            shutil.copy2(ROOT / name, fixture / name)
        shutil.copytree(ROOT / "RRExact", fixture / "RRExact")
        (fixture / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/AxiomAudit.lean", fixture / "scripts/AxiomAudit.lean")
        mutations = [
            ("comparator.json", '"Classical.choice"', '"sorryAx"', "Permitted axioms"),
            ("RRExactSolution.lean", "module", "-- removed module", "missing module header"),
            ("RRExactSolution.lean", "public import RRExact.Canonical",
             "public import RRExact.Canonical\nexample : False := by sorry", "proof hole"),
            ("RRExactChallenge.lean", "public import Mathlib.Data.Fintype.Perm",
             "public import RRExact.LowDim", "only Mathlib modules"),
        ]
        for name, before, after, diagnostic in mutations:
            path = fixture / name
            original = path.read_text()
            if original.count(before) != 1:
                raise RuntimeError(f"Negative-control anchor changed: {name}: {before}")
            path.write_text(original.replace(before, after, 1))
            rejected(f"source mutation in {name}: {diagnostic}",
                     lambda: check_contract(fixture), diagnostic)
            path.write_text(original)
    print("All 9 negative controls were rejected for the expected reason.")


if __name__ == "__main__":
    main()
