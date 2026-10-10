#!/usr/bin/env python3
"""Small source/manifest guards; the official verifier remains authoritative.

These checks catch accidental scope, import, axiom, and dependency-pin drift.
They do not replace Lean elaboration or Palomar's compiler-backed provenance
audit, theorem comparison, and independent kernel replay.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PRINCIPAL_THEOREMS = {"RRExact.real_counterexample", "RRExact.complex_counterexample"}
SUPPORTING_THEOREMS = {
    "RRExact.family_psd", "RRExact.average_closed", "RRExact.operator_norm",
    "RRExact.operator_norm_sharp", "RRExact.recurrence_bound",
    "RRExact.LowDim.real_counterexample", "RRExact.LowDim.complex_counterexample",
}
STANDARD_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def lean_code(source: str) -> str:
    """Erase nested comments and strings, retaining line boundaries."""
    out, index, depth = [], 0, 0
    while index < len(source):
        pair = source[index:index + 2]
        if pair == "/-":
            depth += 1
            out.append("  ")
            index += 2
        elif depth and pair == "-/":
            depth -= 1
            out.append("  ")
            index += 2
        elif depth:
            out.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif pair == "--":
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source[index] == '"':
            out.append(" ")
            index += 1
            while index < len(source) and source[index] != '"':
                if source[index] == "\\":
                    index += 1
                index += 1
            index += 1
        else:
            out.append(source[index])
            index += 1
    require(depth == 0, "Unterminated Lean block comment")
    return "".join(out)


def check_contract(root: Path = ROOT) -> None:
    config = json.loads((root / "comparator.json").read_text())
    require(set(config) == {"challenge_module", "solution_module", "theorem_names",
                            "permitted_axioms"}, "Unexpected comparator keys")
    require(config["challenge_module"] == "RRExactChallenge"
            and config["solution_module"] == "RRExactSolution", "Comparator module drift")
    require(len(config["theorem_names"]) == 2
            and set(config["theorem_names"]) == PRINCIPAL_THEOREMS,
            "Principal theorem contract changed")
    require(len(config["permitted_axioms"]) == 3
            and set(config["permitted_axioms"]) == STANDARD_AXIOMS,
            "Permitted axioms must be exactly the standard three")

    challenge = root / "RRExactChallenge.lean"
    sources = sorted(root.glob("*.lean")) + sorted((root / "RRExact").rglob("*.lean"))
    sources += sorted((root / "scripts").rglob("*.lean"))
    for path in sources:
        code = lean_code(path.read_text())
        require(re.match(r"\s*module\b", code) is not None,
                f"{path.relative_to(root)}: missing module header")
        require(not re.search(r"\b(?:native_decide|admit|axiom|unsafe)\b", code),
                f"{path.relative_to(root)}: forbidden proof mechanism")
        if path != challenge:
            require(not re.search(r"\b(?:sorry|sorryAx)\b", code),
                    f"{path.relative_to(root)}: proof hole")

    code = lean_code(challenge.read_text())
    imports = re.findall(r"^\s*(?:public\s+)?import\s+(\S+)", code, re.MULTILINE)
    require(bool(imports) and all(name.startswith("Mathlib.") for name in imports),
            "Challenge may import only Mathlib modules")
    require(not re.search(r"\b(?:opaque|abbrev|instance|macro|elab)\b", code),
            "Unexpected Challenge declaration")
    require(re.findall(r"\bdef\s+(\w+)", code) == ["arithmeticMean", "permutationAverage"],
            "Challenge mean definitions changed")
    require(set(re.findall(r"\btheorem\s+(\w+)", code))
            == {"real_counterexample", "complex_counterexample"}, "Challenge theorem drift")
    require(len(re.findall(r"\bsorry\b", code)) == 2, "Expected exactly two Challenge holes")

    audit = lean_code((root / "scripts/AxiomAudit.lean").read_text())
    audited = re.findall(r"#print\s+axioms\s+(\S+)", audit)
    require(len(audited) == 9 and set(audited) == PRINCIPAL_THEOREMS | SUPPORTING_THEOREMS,
            "Axiom audit must cover two principal and seven supporting theorems")

    lake = tomllib.loads((root / "lakefile.toml").read_text())
    manifest = json.loads((root / "lake-manifest.json").read_text())
    dependencies = {package["name"]: package for package in manifest["packages"]}
    for name, package in dependencies.items():
        require(package["type"] == "git" and re.fullmatch(r"[0-9a-f]{40}", package["rev"]),
                f"{name}: dependency must resolve to a full Git SHA")
        require(package["url"].startswith("https://github.com/"),
                f"{name}: dependency must use public GitHub source")
    for package in lake["require"]:
        require(re.fullmatch(r"[0-9a-f]{40}", package["rev"]) is not None,
                f"{package['name']}: direct dependency must use a full Git SHA")
        require(package["rev"] == dependencies[package["name"]]["rev"],
                f"{package['name']}: Lake/manifest revision mismatch")
    require(re.fullmatch(r"leanprover/lean4:v\d+\.\d+\.\d+(?:-rc\d+)?\n?",
                         (root / "lean-toolchain").read_text()) is not None,
            "Use an exact Lean release toolchain")
    print(f"Source contract passed: {len(sources)} Lean files; 2 principal / 7 supporting theorems.")


if __name__ == "__main__":
    check_contract()
