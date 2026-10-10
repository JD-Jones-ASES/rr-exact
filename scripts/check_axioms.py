#!/usr/bin/env python3
"""Validate the axiom sets of the two principal and seven supporting theorems.

Run after scripts/build_lean.sh, with the pinned `lake` available on PATH.
The Lean audit contains explicit theorem names; this script checks that they
cover comparator.json and the supporting audit, with only standard axioms.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

from check_contract import PRINCIPAL_THEOREMS, SUPPORTING_THEOREMS, STANDARD_AXIOMS


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    contract = json.loads((ROOT / "comparator.json").read_text(encoding="utf-8"))
    principal = set(contract["theorem_names"])
    if principal != PRINCIPAL_THEOREMS:
        raise SystemExit("The principal theorem contract changed")
    expected = principal | SUPPORTING_THEOREMS
    permitted = set(contract["permitted_axioms"])
    if permitted != STANDARD_AXIOMS:
        raise SystemExit("The permitted axiom contract changed")
    result = subprocess.run(
        ["lake", "env", "lean", str(ROOT / "scripts" / "AxiomAudit.lean")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode

    seen: dict[str, set[str]] = {}
    pattern = re.compile(r"^'([^']+)' depends on axioms: \[([^\]]*)\]$")
    no_axioms = re.compile(r"^'([^']+)' does not depend on any axioms$")
    for line in result.stdout.splitlines():
        match = pattern.fullmatch(line.strip())
        empty = no_axioms.fullmatch(line.strip())
        if match:
            name = match.group(1)
            axioms = {s.strip() for s in match.group(2).split(",") if s.strip()}
        elif empty:
            name, axioms = empty.group(1), set()
        else:
            continue
        if name in seen:
            raise SystemExit(f"Duplicate axiom report for {name}")
        seen[name] = axioms
        forbidden = axioms - permitted
        if forbidden:
            raise SystemExit(f"Forbidden axioms for {name}: {sorted(forbidden)}")
    missing = expected - seen.keys()
    extra = seen.keys() - expected
    if missing or extra:
        raise SystemExit(f"Axiom-audit theorem mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    if not expected:
        raise SystemExit("The comparator lists no theorems")
    sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    print(f"Axiom audit passed: {len(principal)} principal and "
          f"{len(SUPPORTING_THEOREMS)} supporting theorems; all axioms permitted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
