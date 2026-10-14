#!/usr/bin/env python3
"""Build the final SHA/provenance manifest for reconciliation R1."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import pyarrow


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, label: str) -> dict[str, object]:
    return {"path": label, "bytes": path.stat().st_size, "sha256": sha(path)}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    raw = args.raw_root.resolve()
    base = args.base.resolve()

    frozen_relatives = [
        "evidence/tools/v011_d4a1_census.py",
        "evidence/V1/v011-d4a0-taxonomy-registry.json",
        "evidence/V1/v011-d4a1-oswe-20k-manifest-v2.json",
        "evidence/V1/v011-d4a1-census-results.json",
        "evidence/V1/v011-d4a2-cross-model.json",
        "evidence/V1/v011-d4a2r1-full-factorial.json",
        "evidence/V1/paper/paper-draft-v1-icse.md",
        "evidence/V1/paper/paper-tables.json",
        "evidence/V1/paper/paper-figures-data/figures.json",
        "evidence/V1/paper/supplements/supplement-A-detectors.md",
        "evidence/V1/paper/supplements/supplement-C-census-factorial.md",
    ]
    frozen_inputs = [record(repo / relative, relative.replace("\\", "/")) for relative in frozen_relatives]
    external_script = Path("D:/tasco-temp/d3_hf_data/a2_cross_model.py")
    frozen_inputs.append(record(external_script, str(external_script)))

    raw_files = sorted(raw.glob("*minimax_m25*.parquet"), key=lambda path: path.name) + sorted(
        raw.glob("*qwen35_122b*.parquet"), key=lambda path: path.name
    )
    raw_inputs = [record(path, str(path)) for path in raw_files]

    outputs = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.name == "validation-execution-manifest.json" or "__pycache__" in path.parts:
            continue
        outputs.append(record(path, str(path.relative_to(base)).replace("\\", "/")))

    manifest = {
        "schema_version": 1,
        "task": "PAPER-A-COC-ALLOCATION-RECONCILIATION-R1",
        "execution_date": "2026-10-13",
        "status": "PARTIAL",
        "git": {
            "branch": git(repo, "branch", "--show-current"),
            "base_head": "5e57cf5e62a688cfd43b5762d83b1906e637283c",
            "current_head": git(repo, "rev-parse", "HEAD"),
            "worktree": str(repo),
        },
        "environment": {"python": platform.python_version(), "pyarrow": pyarrow.__version__},
        "scope": {
            "unique_variable": "COC allocation/accounting",
            "annotation_outputs_read": False,
            "paper_modified": False,
            "frozen_inputs_modified": False,
            "exact_byte_spans": "NOT_MEASURABLE",
        },
        "raw_input_count": len(raw_inputs),
        "frozen_inputs": frozen_inputs,
        "raw_inputs": raw_inputs,
        "outputs": outputs,
        "validation": {
            "component_regression": "PASS_5_OF_5",
            "historical_proxy_regression": "PASS",
            "identity_closure": "PASS_OSW_20000_QWEN_35334",
            "allocation_invariants": "PASS",
            "aggregate_rebuild": "PASS",
            "double_replay_determinism": "PASS_BYTE_IDENTICAL",
            "overall": "PARTIAL_EXACT_SPANS_NOT_MEASURABLE",
        },
    }
    destination = base / "validation-execution-manifest.json"
    destination.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(destination), "raw_inputs": len(raw_inputs), "outputs": len(outputs)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
