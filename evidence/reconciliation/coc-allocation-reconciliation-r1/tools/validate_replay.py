#!/usr/bin/env python3
"""Independently validate R1 ledgers and produce machine-readable gates."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq


CORE = [
    "ledger/osw-event-allocation-ledger.parquet",
    "ledger/qwen-event-allocation-ledger.parquet",
    "ledger/session-allocation-summary.parquet",
    "summaries/coc-recalculation-summary.json",
    "summaries/shape-allocation-summary.csv",
]


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def dump(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def close(actual: float, expected: float, tolerance: float = 1e-8) -> bool:
    return abs(actual - expected) <= tolerance * max(1.0, abs(expected))


def validate_ledger(path: Path) -> dict[str, Any]:
    rows = 0
    violations = CounterLike()
    sums: defaultdict[str, list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
    columns = [
        "scaffold",
        "payload_utf8_bytes",
        "shape_count",
        "allocation_divisor",
        "qualified_allocated_bytes",
        "shipped_allocated_bytes",
        "candidate_allocated_bytes",
    ]
    for batch in pq.ParquetFile(path).iter_batches(batch_size=10000, columns=columns):
        for row in batch.to_pylist():
            rows += 1
            payload = row["payload_utf8_bytes"]
            den = row["qualified_allocated_bytes"]
            shipped = row["shipped_allocated_bytes"]
            candidate = row["candidate_allocated_bytes"]
            if row["shape_count"] != row["allocation_divisor"] or row["shape_count"] <= 0:
                violations.add("invalid_divisor")
            if den < -1e-9 or den > payload + 1e-7:
                violations.add("qualified_exceeds_event")
            if shipped < -1e-9 or shipped > den + 1e-7:
                violations.add("shipped_exceeds_qualified")
            if candidate < -1e-9 or candidate > den + 1e-7:
                violations.add("candidate_exceeds_qualified")
            values = sums[row["scaffold"]]
            values[0] += den
            values[1] += shipped
            values[2] += candidate
    return {
        "rows": rows,
        "violations": violations.value,
        "aggregates_by_scaffold": {
            scaffold: {
                "qualified_allocated_bytes": values[0],
                "shipped_allocated_bytes": values[1],
                "candidate_allocated_bytes": values[2],
                "shipped_coc": values[1] / values[0],
                "candidate_coc": values[2] / values[0],
            }
            for scaffold, values in sorted(sums.items())
        },
        "aggregate": {
            "qualified_allocated_bytes": sum(values[0] for values in sums.values()),
            "shipped_allocated_bytes": sum(values[1] for values in sums.values()),
            "candidate_allocated_bytes": sum(values[2] for values in sums.values()),
        },
    }


class CounterLike:
    def __init__(self) -> None:
        self.value: dict[str, int] = {}

    def add(self, key: str) -> None:
        self.value[key] = self.value.get(key, 0) + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    args = parser.parse_args()
    base = args.base.resolve()
    run2 = base / "run2"
    summary = json.loads((base / "summaries/coc-recalculation-summary.json").read_text(encoding="utf-8"))

    deterministic = {}
    for relative in CORE:
        left = sha256(base / relative)
        right = sha256(run2 / relative)
        deterministic[relative] = {"run1_sha256": left, "run2_sha256": right, "identical": left == right}

    osw = validate_ledger(base / "ledger/osw-event-allocation-ledger.parquet")
    qwen = validate_ledger(base / "ledger/qwen-event-allocation-ledger.parquet")
    ledgers = {"OSW_MINIMAX_20K": osw, "QWEN_35334": qwen}
    aggregate_checks = {}
    for corpus, result in ledgers.items():
        expected = summary["corpora"][corpus]["primary"]
        aggregate_checks[corpus] = {
            "qualified_matches": close(result["aggregate"]["qualified_allocated_bytes"], expected["qualified_allocated_bytes"]["decimal"]),
            "shipped_matches": close(result["aggregate"]["shipped_allocated_bytes"], expected["shipped_allocated_bytes"]["decimal"]),
            "candidate_matches": close(result["aggregate"]["candidate_allocated_bytes"], expected["candidate_allocated_bytes"]["decimal"]),
        }

    session_rows = pq.ParquetFile(base / "ledger/session-allocation-summary.parquet").metadata.num_rows
    historical_gates = {
        "osw_shipped_round4": round(summary["corpora"]["OSW_MINIMAX_20K"]["historical_proxy_replay"]["shipped_coc"], 4) == 0.0039,
        "osw_candidate_round4": round(summary["corpora"]["OSW_MINIMAX_20K"]["historical_proxy_replay"]["candidate_coc"], 4) == 0.9012,
        "qwen_oh15_shipped_round4": round(summary["corpora"]["QWEN_35334"]["historical_proxy_replay"]["by_scaffold"]["openhands"]["shipped_coc"], 4) == 0.0114,
        "qwen_oh15_candidate_round4": round(summary["corpora"]["QWEN_35334"]["historical_proxy_replay"]["by_scaffold"]["openhands"]["candidate_coc"], 4) == 0.9127,
    }
    all_pass = (
        all(item["identical"] for item in deterministic.values())
        and not osw["violations"]
        and not qwen["violations"]
        and all(all(checks.values()) for checks in aggregate_checks.values())
        and session_rows == 55334
        and all(historical_gates.values())
    )
    validation = {
        "schema_version": 1,
        "gate": "PASS" if all_pass else "FAIL",
        "determinism": deterministic,
        "ledger_checks": ledgers,
        "aggregate_checks": aggregate_checks,
        "session_summary_rows": session_rows,
        "expected_session_summary_rows": 55334,
        "historical_regression_gates": historical_gates,
    }
    dump(base / "summaries/replay-validation.json", validation)

    old_osw = summary["corpora"]["OSW_MINIMAX_20K"]["historical_proxy_replay"]
    new_osw = summary["corpora"]["OSW_MINIMAX_20K"]["primary"]
    old_qwen = summary["corpora"]["QWEN_35334"]["historical_proxy_replay"]["by_scaffold"]["openhands"]
    new_qwen_oh = qwen["aggregates_by_scaffold"]["openhands"]

    def comparison(old: float, new: float) -> dict[str, float]:
        return {
            "historical": old,
            "recomputed": new,
            "absolute_difference": new - old,
            "relative_difference": (new - old) / old if old else float("inf"),
        }

    diff = {
        "schema_version": 1,
        "OSW_MINIMAX_20K_same_frame": {
            "shipped_coc": comparison(old_osw["shipped_coc"], new_osw["shipped_coc"]),
            "candidate_coc": comparison(old_osw["candidate_coc"], new_osw["candidate_coc"]),
        },
        "QWEN_OPENHANDS_15000_same_frame": {
            "shipped_coc": comparison(old_qwen["shipped_coc"], new_qwen_oh["shipped_coc"]),
            "candidate_coc": comparison(old_qwen["candidate_coc"], new_qwen_oh["candidate_coc"]),
        },
        "QWEN_35334_primary": summary["corpora"]["QWEN_35334"]["primary"],
        "scope_note": "Historical Qwen paper values are OpenHands 15K only; the 35,334 primary result is not a same-frame difference.",
    }
    dump(base / "summaries/historical-vs-recomputed-diff.json", diff)
    dump(base / "summaries/subgroup-recalculation-summary.json", qwen["aggregates_by_scaffold"])
    print(json.dumps({"gate": validation["gate"], "diff": diff}, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
