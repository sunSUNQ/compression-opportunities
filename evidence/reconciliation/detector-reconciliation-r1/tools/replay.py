#!/usr/bin/env python3
"""Full TW/OSW replay using the reconciled A0 detector implementation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from adapters import parse_osw, parse_tw
from shared_detectors import FULL_NAMES, SHAPES, VERSION, detect

FROZEN_COMMIT = "5e57cf5e62a688cfd43b5762d83b1906e637283c"


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def osw_files(root: Path) -> list[Path]:
    files = []
    for prefix, count in (
        ("openhands_minimax_m25_swe-rebench-v2_train", 18),
        ("sweagent_minimax_m25_swe-rebench-v2_train", 19),
    ):
        for index in range(count):
            path = root / f"{prefix}-{index:05d}-of-{count:05d}.parquet"
            if not path.exists():
                raise FileNotFoundError(path)
            files.append(path)
    return files


class Metrics:
    def __init__(self, denominator: int) -> None:
        self.denominator = denominator
        self.rows = 0
        self.events = 0
        self.shape_rows: Counter[str] = Counter()
        self.shape_events: Counter[str] = Counter()
        self.adapter: Counter[str] = Counter()
        self.replay_digest = hashlib.sha256()
        self.deterministic = True

    def add(
        self,
        identity: str,
        events: list[dict[str, Any]],
        masks: list[set[str]],
        audit: dict[str, int],
    ) -> None:
        repeated = detect([dict(event) for event in events])
        if repeated != masks:
            self.deterministic = False
        self.rows += 1
        self.events += len(events)
        self.adapter.update(audit)
        row_shapes = set().union(*masks) if masks else set()
        self.shape_rows.update(row_shapes)
        for labels in masks:
            self.shape_events.update(labels)
        canonical = json.dumps(
            [identity, [sorted(labels) for labels in masks]],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        self.replay_digest.update(canonical.encode("utf-8"))

    def finish(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "denominator": self.denominator,
            "events": self.events,
            "deterministic_double_evaluation": self.deterministic,
            "label_stream_sha256": self.replay_digest.hexdigest(),
            "adapter_audit": dict(sorted(self.adapter.items())),
            "shape": {
                shape: {
                    "occurrence_rows": self.shape_rows[shape],
                    "occurrence_events": self.shape_events[shape],
                    "denominator": self.denominator,
                    "incidence": self.shape_rows[shape] / self.denominator,
                    "measurement_status": "MEASURABLE",
                }
                for shape in SHAPES
            },
        }


def replay_tw(path: Path) -> dict[str, Any]:
    metrics = Metrics(15000)
    parquet = pq.ParquetFile(path)
    ordinal = 0
    for batch in parquet.iter_batches(batch_size=250, columns=["session_id", "messages_json"]):
        for row in batch.to_pylist():
            try:
                messages = json.loads(row["messages_json"])
            except Exception:
                messages = []
            events, audit = parse_tw(messages)
            metrics.add(f"row:{ordinal}", events, detect(events), audit)
            ordinal += 1
    return metrics.finish()


def replay_osw(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected = {row["trajectory_id"] for row in manifest["sample"]}
    metrics = Metrics(len(selected))
    seen: set[str] = set()
    files = osw_files(root)
    for path in files:
        parquet = pq.ParquetFile(path)
        for batch in parquet.iter_batches(batch_size=300, columns=["trajectory_id", "messages"]):
            for row in batch.to_pylist():
                identity = row["trajectory_id"]
                if identity not in selected:
                    continue
                messages = json.loads(row["messages"]) if isinstance(row["messages"], str) else row["messages"]
                events, audit = parse_osw(messages)
                metrics.add(identity, events, detect(events), audit)
                seen.add(identity)
    result = metrics.finish()
    result["manifest_selected"] = len(selected)
    result["selected_seen"] = len(seen)
    result["missing_selected_ids"] = sorted(selected - seen)
    result["raw_shards"] = [str(path) for path in files]
    return result


def replication_status(tw_incidence: float, osw_incidence: float) -> tuple[float | None, str]:
    if tw_incidence == 0 and osw_incidence == 0:
        return None, "NOT_ESTIMABLE_ZERO_BASELINE"
    if tw_incidence == 0 or osw_incidence == 0:
        return None, "DATASET_SPECIFIC_ZERO"
    ratio = osw_incidence / tw_incidence
    if 0.5 <= ratio <= 2.0:
        return ratio, "REPLICATED"
    if 0.2 <= ratio < 0.5 or 2.0 < ratio <= 5.0:
        return ratio, "PARTIAL_REPLICATION"
    return ratio, "DATASET_SPECIFIC"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--tw", type=Path, required=True)
    parser.add_argument("--osw-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    args = parser.parse_args()

    manifest_path = args.repo / "evidence/V1/v011-d4a1-oswe-20k-manifest-v2.json"
    frozen_osw_path = args.repo / "evidence/V1/v011-d4a1-census-results.json"
    frozen_tw_path = args.repo / "evidence/V1/v011-d4a1r3-tw-trajectory-census.json"
    a0_path = args.repo / "evidence/V1/v011-d4a0-taxonomy-registry.json"

    tw = replay_tw(args.tw)
    osw = replay_osw(args.osw_root, manifest_path)
    frozen_osw = json.loads(frozen_osw_path.read_text(encoding="utf-8"))
    frozen_tw = json.loads(frozen_tw_path.read_text(encoding="utf-8"))

    matrix = []
    for shape in SHAPES:
        full_name = f"{shape}_{FULL_NAMES[shape]}"
        tw_new = tw["shape"][shape]
        osw_new = osw["shape"][shape]
        tw_old = frozen_tw["per_shape"][shape]["row_sessions"]
        osw_old_record = frozen_osw["shape_results"].get(full_name)
        osw_old = osw_old_record["event_sessions"] if osw_old_record else 0
        ratio, status = replication_status(tw_new["incidence"], osw_new["incidence"])
        matrix.append(
            {
                "shape": shape,
                "name": FULL_NAMES[shape],
                "tw": {
                    **tw_new,
                    "historical_occurrence_rows": tw_old,
                    "delta_rows": tw_new["occurrence_rows"] - tw_old,
                },
                "osw": {
                    **osw_new,
                    "historical_occurrence_rows": osw_old,
                    "historical_incidence": osw_old / 20000,
                    "delta_rows": osw_new["occurrence_rows"] - osw_old,
                    "delta_incidence": osw_new["incidence"] - osw_old / 20000,
                },
                "ratio_osw_over_tw": ratio,
                "replication_status": status,
            }
        )

    counts = Counter(row["replication_status"] for row in matrix)
    comparable = sum(status != "NOT_ESTIMABLE_ZERO_BASELINE" for status in counts.elements())
    replicated_or_partial = counts["REPLICATED"] + counts["PARTIAL_REPLICATION"]
    data_files = [args.tw, manifest_path, a0_path, frozen_tw_path, frozen_osw_path, *osw_files(args.osw_root)]
    result = {
        "schema_version": 1,
        "task": "PAPER-A-DETECTOR-CROSS-CORPUS-RECONCILIATION-R1",
        "detector_version": VERSION,
        "base_commit": FROZEN_COMMIT,
        "taxonomy_changed": False,
        "historical_evidence_overwritten": False,
        "tw": tw,
        "osw": osw,
        "shape_matrix": matrix,
        "replication_summary": {
            "status_counts": dict(sorted(counts.items())),
            "ratio_comparable_shapes": comparable,
            "replicated_or_partial": replicated_or_partial,
            "headline_candidate": f"{replicated_or_partial}/{comparable} ratio-comparable shapes replicate fully or partially",
        },
        "integrity": {
            "tw_rows_complete": tw["rows"] == 15000,
            "osw_rows_complete": osw["rows"] == 20000,
            "osw_manifest_complete": osw["selected_seen"] == osw["manifest_selected"] == 20000,
            "deterministic": tw["deterministic_double_evaluation"] and osw["deterministic_double_evaluation"],
            "input_sha256": [{"path": str(path), "sha256": hash_file(path), "bytes": path.stat().st_size} for path in data_files],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    with args.csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "shape", "name", "tw_occurrence", "tw_denominator", "tw_incidence",
                "osw_historical_occurrence", "osw_occurrence", "osw_delta", "osw_denominator",
                "osw_historical_incidence", "osw_incidence", "ratio_osw_over_tw", "replication_status",
            ],
        )
        writer.writeheader()
        for row in matrix:
            writer.writerow(
                {
                    "shape": row["shape"],
                    "name": row["name"],
                    "tw_occurrence": row["tw"]["occurrence_rows"],
                    "tw_denominator": row["tw"]["denominator"],
                    "tw_incidence": row["tw"]["incidence"],
                    "osw_historical_occurrence": row["osw"]["historical_occurrence_rows"],
                    "osw_occurrence": row["osw"]["occurrence_rows"],
                    "osw_delta": row["osw"]["delta_rows"],
                    "osw_denominator": row["osw"]["denominator"],
                    "osw_historical_incidence": row["osw"]["historical_incidence"],
                    "osw_incidence": row["osw"]["incidence"],
                    "ratio_osw_over_tw": row["ratio_osw_over_tw"],
                    "replication_status": row["replication_status"],
                }
            )
    print(json.dumps({"output": str(args.output), "csv": str(args.csv), "summary": result["replication_summary"], "integrity": {k: v for k, v in result["integrity"].items() if k != "input_sha256"}}, indent=2))


if __name__ == "__main__":
    main()
