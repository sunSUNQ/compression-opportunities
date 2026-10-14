#!/usr/bin/env python3
"""Build deterministic event-level COC ledgers from frozen OSW/Qwen data."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import pyarrow as pa
import pyarrow.parquet as pq

from frozen_detector import detect_event_shapes, parse_events, session_shapes


ALL_SHAPES = [
    "E1_repeated_exact_command",
    "E2_repeated_similar_command",
    "E3_same_file_reread",
    "E4_overlapping_file_read",
    "E5_same_search",
    "E6_large_test_success",
    "E7_large_test_failure",
    "E8_large_lint_output",
    "E9_large_build_output",
    "E10_repeated_validation",
    "E11_unchanged_validation",
    "E12_large_diagnostic",
    "E13_large_output_near_terminal",
    "E14_output_followed_by_reread",
    "E15_output_followed_by_rederivation",
]
PRIMARY_EXCLUDED = {"E7_large_test_failure", "E9_large_build_output", "E12_large_diagnostic"}
LEGACY_EXCLUDED = {"E7_large_test_failure", "E12_large_diagnostic"}
SHIPPED = {"E5_same_search", "E8_large_lint_output", "E10_repeated_validation", "E11_unchanged_validation"}
PRIMARY_CANDIDATE = SHIPPED | {
    "E1_repeated_exact_command",
    "E2_repeated_similar_command",
    "E3_same_file_reread",
    "E14_output_followed_by_reread",
}
LEGACY_CANDIDATE = PRIMARY_CANDIDATE | {"E15_output_followed_by_rederivation"}

LEDGER_SCHEMA = pa.schema(
    [
        ("corpus", pa.string()),
        ("scaffold", pa.string()),
        ("session_id", pa.string()),
        ("event_id", pa.string()),
        ("event_index", pa.int32()),
        ("source_file", pa.string()),
        ("source_row_ordinal", pa.int64()),
        ("payload_chars", pa.int64()),
        ("payload_utf8_bytes", pa.int64()),
        ("shapes", pa.list_(pa.string())),
        ("qualified_shapes", pa.list_(pa.string())),
        ("shipped_supported_shapes", pa.list_(pa.string())),
        ("candidate_supported_shapes", pa.list_(pa.string())),
        ("ineligible_shapes", pa.list_(pa.string())),
        ("shape_count", pa.int16()),
        ("allocation_divisor", pa.int16()),
        ("multi_label", pa.bool_()),
        ("allocation_rule", pa.string()),
        ("qualified_allocated_bytes", pa.float64()),
        ("shipped_allocated_bytes", pa.float64()),
        ("candidate_allocated_bytes", pa.float64()),
        ("qualified_allocated_chars", pa.float64()),
        ("shipped_allocated_chars", pa.float64()),
        ("candidate_allocated_chars", pa.float64()),
        ("missing_reason", pa.string()),
        ("byte_measurement_status", pa.string()),
        ("evidence_provenance", pa.string()),
    ]
)

SESSION_SCHEMA = pa.schema(
    [
        ("corpus", pa.string()),
        ("scaffold", pa.string()),
        ("session_id", pa.string()),
        ("source_file", pa.string()),
        ("source_row_ordinal", pa.int64()),
        ("event_count", pa.int32()),
        ("labeled_event_count", pa.int32()),
        ("shape_count", pa.int16()),
        ("shapes", pa.list_(pa.string())),
        ("total_observation_chars", pa.int64()),
        ("total_observation_utf8_bytes", pa.int64()),
        ("qualified_allocated_bytes", pa.float64()),
        ("shipped_allocated_bytes", pa.float64()),
        ("candidate_allocated_bytes", pa.float64()),
    ]
)


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def fraction_value(value: Fraction) -> dict[str, Any]:
    return {
        "decimal": float(value),
        "exact_numerator": value.numerator,
        "exact_denominator": value.denominator,
    }


def ratio(numerator: Fraction, denominator: Fraction) -> float | None:
    return float(numerator / denominator) if denominator else None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


class LedgerWriter:
    def __init__(self, path: Path, schema: pa.Schema, batch_size: int = 5000) -> None:
        self.path = path
        self.schema = schema
        self.batch_size = batch_size
        self.rows: list[dict[str, Any]] = []
        self.writer = pq.ParquetWriter(path, schema, compression="zstd", use_dictionary=True)

    def add(self, row: dict[str, Any]) -> None:
        self.rows.append(row)
        if len(self.rows) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        if not self.rows:
            return
        self.writer.write_table(pa.Table.from_pylist(self.rows, schema=self.schema))
        self.rows.clear()

    def close(self) -> None:
        self.flush()
        self.writer.close()


class CorpusAccumulator:
    def __init__(self, corpus: str) -> None:
        self.corpus = corpus
        self.sessions = 0
        self.events = 0
        self.labeled_events = 0
        self.unlabeled_events = 0
        self.empty_labeled_events = 0
        self.multi_label_events = 0
        self.session_ids: set[str] = set()
        self.session_shape_counts: Counter[str] = Counter()
        self.event_shape_counts: Counter[str] = Counter()
        self.shape_bytes: defaultdict[str, Fraction] = defaultdict(Fraction)
        self.shape_chars: defaultdict[str, Fraction] = defaultdict(Fraction)
        self.primary_den_bytes = Fraction()
        self.primary_shipped_bytes = Fraction()
        self.primary_candidate_bytes = Fraction()
        self.primary_den_chars = Fraction()
        self.primary_shipped_chars = Fraction()
        self.primary_candidate_chars = Fraction()
        self.eligible_renorm_den = Fraction()
        self.eligible_renorm_shipped = Fraction()
        self.eligible_renorm_candidate = Fraction()
        self.optimistic_den = Fraction()
        self.optimistic_shipped = Fraction()
        self.optimistic_candidate = Fraction()
        self.conservative_den = Fraction()
        self.conservative_shipped = Fraction()
        self.conservative_candidate = Fraction()
        self.legacy_event_den = Fraction()
        self.legacy_event_shipped = Fraction()
        self.legacy_event_candidate = Fraction()
        self.historical_den = Fraction()
        self.historical_shipped = Fraction()
        self.historical_candidate = Fraction()
        self.historical_by_scaffold: defaultdict[str, list[Fraction]] = defaultdict(
            lambda: [Fraction(), Fraction(), Fraction()]
        )


def event_allocations(payload: int, shapes: list[str], excluded: set[str], supported: set[str]) -> tuple[Fraction, Fraction]:
    divisor = len(shapes)
    denominator = Fraction(payload * sum(shape not in excluded for shape in shapes), divisor)
    numerator = Fraction(payload * sum(shape not in excluded and shape in supported for shape in shapes), divisor)
    return denominator, numerator


def process_session(
    accumulator: CorpusAccumulator,
    ledger: LedgerWriter,
    sessions: LedgerWriter,
    *,
    scaffold: str,
    session_id: str,
    source_file: str,
    source_row_ordinal: int,
    messages: Any,
    adapter: str,
    provenance: str,
) -> None:
    if session_id in accumulator.session_ids:
        raise ValueError(f"duplicate session identity in {accumulator.corpus}: {session_id}")
    accumulator.session_ids.add(session_id)
    events = parse_events(messages, adapter)
    labels = detect_event_shapes(events)
    shapes_for_session = session_shapes(labels)
    accumulator.sessions += 1
    accumulator.events += len(events)
    for shape in shapes_for_session:
        accumulator.session_shape_counts[shape] += 1

    session_den = Fraction()
    session_shipped = Fraction()
    session_candidate = Fraction()
    labeled = 0
    for event, shapes in zip(events, labels):
        if not shapes:
            accumulator.unlabeled_events += 1
            continue
        labeled += 1
        accumulator.labeled_events += 1
        if len(shapes) > 1:
            accumulator.multi_label_events += 1
        payload_bytes = event["obs_utf8_bytes"]
        payload_chars = event["obs_chars"]
        if payload_bytes == 0:
            accumulator.empty_labeled_events += 1
        for shape in shapes:
            accumulator.event_shape_counts[shape] += 1
            accumulator.shape_bytes[shape] += Fraction(payload_bytes, len(shapes))
            accumulator.shape_chars[shape] += Fraction(payload_chars, len(shapes))

        den_b, shipped_b = event_allocations(payload_bytes, shapes, PRIMARY_EXCLUDED, SHIPPED)
        _, candidate_b = event_allocations(payload_bytes, shapes, PRIMARY_EXCLUDED, PRIMARY_CANDIDATE)
        den_c, shipped_c = event_allocations(payload_chars, shapes, PRIMARY_EXCLUDED, SHIPPED)
        _, candidate_c = event_allocations(payload_chars, shapes, PRIMARY_EXCLUDED, PRIMARY_CANDIDATE)
        accumulator.primary_den_bytes += den_b
        accumulator.primary_shipped_bytes += shipped_b
        accumulator.primary_candidate_bytes += candidate_b
        accumulator.primary_den_chars += den_c
        accumulator.primary_shipped_chars += shipped_c
        accumulator.primary_candidate_chars += candidate_c
        session_den += den_b
        session_shipped += shipped_b
        session_candidate += candidate_b

        qualified = [shape for shape in shapes if shape not in PRIMARY_EXCLUDED]
        shipped_shapes = [shape for shape in qualified if shape in SHIPPED]
        candidate_shapes = [shape for shape in qualified if shape in PRIMARY_CANDIDATE]
        ineligible = [shape for shape in shapes if shape in PRIMARY_EXCLUDED]

        if qualified:
            accumulator.eligible_renorm_den += payload_bytes
            accumulator.eligible_renorm_shipped += Fraction(payload_bytes * len(shipped_shapes), len(qualified))
            accumulator.eligible_renorm_candidate += Fraction(payload_bytes * len(candidate_shapes), len(qualified))
            accumulator.optimistic_den += payload_bytes
            accumulator.optimistic_shipped += payload_bytes if shipped_shapes else 0
            accumulator.optimistic_candidate += payload_bytes if candidate_shapes else 0
            accumulator.conservative_den += payload_bytes
            accumulator.conservative_shipped += payload_bytes if len(shipped_shapes) == len(qualified) else 0
            accumulator.conservative_candidate += payload_bytes if len(candidate_shapes) == len(qualified) else 0

        legacy_den, legacy_shipped = event_allocations(payload_bytes, shapes, LEGACY_EXCLUDED, SHIPPED)
        _, legacy_candidate = event_allocations(payload_bytes, shapes, LEGACY_EXCLUDED, LEGACY_CANDIDATE)
        accumulator.legacy_event_den += legacy_den
        accumulator.legacy_event_shipped += legacy_shipped
        accumulator.legacy_event_candidate += legacy_candidate

        missing_reason = ""
        if not qualified:
            missing_reason = "NO_QUALIFIED_SHAPE"
        elif payload_bytes == 0:
            missing_reason = "EMPTY_PAYLOAD"
        ledger.add(
            {
                "corpus": accumulator.corpus,
                "scaffold": scaffold,
                "session_id": session_id,
                "event_id": f"{session_id}:{event['event_index']}",
                "event_index": event["event_index"],
                "source_file": source_file,
                "source_row_ordinal": source_row_ordinal,
                "payload_chars": payload_chars,
                "payload_utf8_bytes": payload_bytes,
                "shapes": shapes,
                "qualified_shapes": qualified,
                "shipped_supported_shapes": shipped_shapes,
                "candidate_supported_shapes": candidate_shapes,
                "ineligible_shapes": ineligible,
                "shape_count": len(shapes),
                "allocation_divisor": len(shapes),
                "multi_label": len(shapes) > 1,
                "allocation_rule": "ALL_FIRED_SHAPES_EQUAL_SPLIT_THEN_FILTER",
                "qualified_allocated_bytes": float(den_b),
                "shipped_allocated_bytes": float(shipped_b),
                "candidate_allocated_bytes": float(candidate_b),
                "qualified_allocated_chars": float(den_c),
                "shipped_allocated_chars": float(shipped_c),
                "candidate_allocated_chars": float(candidate_c),
                "missing_reason": missing_reason,
                "byte_measurement_status": "UTF8_REENCODED_EVENT_PAYLOAD_PROXY",
                "evidence_provenance": provenance,
            }
        )

    # Exact historical proxies are intentionally session-level.
    legacy_session_shapes = [shape for shape in shapes_for_session if shape not in LEGACY_EXCLUDED]
    if legacy_session_shapes:
        if accumulator.corpus == "OSW_MINIMAX_20K":
            # Historical OSW divides each qualified share by all session shapes,
            # including unsafe shapes that are then omitted from the denominator.
            mass = Fraction(sum(event["obs_chars"] for event in events), len(shapes_for_session))
        else:
            mass = Fraction(1, len(legacy_session_shapes))
        den_mass = mass * len(legacy_session_shapes)
        shipped_mass = mass * sum(shape in SHIPPED for shape in legacy_session_shapes)
        candidate_mass = mass * sum(shape in LEGACY_CANDIDATE for shape in legacy_session_shapes)
        accumulator.historical_den += den_mass
        accumulator.historical_shipped += shipped_mass
        accumulator.historical_candidate += candidate_mass
        accumulator.historical_by_scaffold[scaffold][0] += den_mass
        accumulator.historical_by_scaffold[scaffold][1] += shipped_mass
        accumulator.historical_by_scaffold[scaffold][2] += candidate_mass

    sessions.add(
        {
            "corpus": accumulator.corpus,
            "scaffold": scaffold,
            "session_id": session_id,
            "source_file": source_file,
            "source_row_ordinal": source_row_ordinal,
            "event_count": len(events),
            "labeled_event_count": labeled,
            "shape_count": len(shapes_for_session),
            "shapes": shapes_for_session,
            "total_observation_chars": sum(event["obs_chars"] for event in events),
            "total_observation_utf8_bytes": sum(event["obs_utf8_bytes"] for event in events),
            "qualified_allocated_bytes": float(session_den),
            "shipped_allocated_bytes": float(session_shipped),
            "candidate_allocated_bytes": float(session_candidate),
        }
    )


def iter_rows(files: Iterable[Path]) -> Iterable[tuple[Path, int, dict[str, Any]]]:
    for source in sorted(files, key=lambda path: path.name):
        ordinal = 0
        parquet = pq.ParquetFile(source)
        for batch in parquet.iter_batches(batch_size=400, columns=["trajectory_id", "messages"]):
            for row in batch.to_pylist():
                yield source, ordinal, row
                ordinal += 1


def summarize(accumulator: CorpusAccumulator) -> dict[str, Any]:
    primary_candidate_coc = ratio(accumulator.primary_candidate_bytes, accumulator.primary_den_bytes)
    primary_shipped_coc = ratio(accumulator.primary_shipped_bytes, accumulator.primary_den_bytes)
    gap = None
    if primary_candidate_coc:
        gap = 1 - (primary_shipped_coc or 0) / primary_candidate_coc
    return {
        "corpus": accumulator.corpus,
        "sessions": accumulator.sessions,
        "events": accumulator.events,
        "labeled_events": accumulator.labeled_events,
        "unlabeled_events": accumulator.unlabeled_events,
        "multi_label_events": accumulator.multi_label_events,
        "empty_labeled_events": accumulator.empty_labeled_events,
        "primary": {
            "measurement_unit": "UTF8_REENCODED_EVENT_PAYLOAD_PROXY",
            "qualified_allocated_bytes": fraction_value(accumulator.primary_den_bytes),
            "shipped_allocated_bytes": fraction_value(accumulator.primary_shipped_bytes),
            "candidate_allocated_bytes": fraction_value(accumulator.primary_candidate_bytes),
            "shipped_coc": primary_shipped_coc,
            "candidate_coc": primary_candidate_coc,
            "relative_full_fit_coverage_gap": gap,
        },
        "sensitivities": {
            "codepoint_chars": {
                "shipped_coc": ratio(accumulator.primary_shipped_chars, accumulator.primary_den_chars),
                "candidate_coc": ratio(accumulator.primary_candidate_chars, accumulator.primary_den_chars),
            },
            "eligible_renormalized": {
                "shipped_coc": ratio(accumulator.eligible_renorm_shipped, accumulator.eligible_renorm_den),
                "candidate_coc": ratio(accumulator.eligible_renorm_candidate, accumulator.eligible_renorm_den),
            },
            "optimistic_any_supported_whole_event": {
                "shipped_coc": ratio(accumulator.optimistic_shipped, accumulator.optimistic_den),
                "candidate_coc": ratio(accumulator.optimistic_candidate, accumulator.optimistic_den),
            },
            "conservative_all_qualified_supported_whole_event": {
                "shipped_coc": ratio(accumulator.conservative_shipped, accumulator.conservative_den),
                "candidate_coc": ratio(accumulator.conservative_candidate, accumulator.conservative_den),
            },
            "legacy_mapping_event_allocation": {
                "shipped_coc": ratio(accumulator.legacy_event_shipped, accumulator.legacy_event_den),
                "candidate_coc": ratio(accumulator.legacy_event_candidate, accumulator.legacy_event_den),
            },
        },
        "historical_proxy_replay": {
            "shipped_coc": ratio(accumulator.historical_shipped, accumulator.historical_den),
            "candidate_coc": ratio(accumulator.historical_candidate, accumulator.historical_den),
            "unit": "WHOLE_TRAJECTORY_CHARS_PER_SESSION_SHAPE" if accumulator.corpus == "OSW_MINIMAX_20K" else "SESSION_SHAPE_EQUAL_WEIGHT",
            "by_scaffold": {
                scaffold: {
                    "shipped_coc": ratio(values[1], values[0]),
                    "candidate_coc": ratio(values[2], values[0]),
                }
                for scaffold, values in sorted(accumulator.historical_by_scaffold.items())
            },
        },
        "session_shape_counts": {shape: accumulator.session_shape_counts.get(shape, 0) for shape in ALL_SHAPES},
        "event_shape_counts": {shape: accumulator.event_shape_counts.get(shape, 0) for shape in ALL_SHAPES},
    }


def write_shape_csv(path: Path, accumulators: list[CorpusAccumulator]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "corpus",
                "shape",
                "session_occurrence",
                "event_occurrence",
                "allocated_utf8_bytes",
                "allocated_codepoint_chars",
                "primary_qualified",
                "shipped_full",
                "candidate_full",
            ]
        )
        for accumulator in accumulators:
            for shape in ALL_SHAPES:
                writer.writerow(
                    [
                        accumulator.corpus,
                        shape,
                        accumulator.session_shape_counts.get(shape, 0),
                        accumulator.event_shape_counts.get(shape, 0),
                        format(float(accumulator.shape_bytes.get(shape, Fraction())), ".12f"),
                        format(float(accumulator.shape_chars.get(shape, Fraction())), ".12f"),
                        str(shape not in PRIMARY_EXCLUDED).lower(),
                        str(shape in SHIPPED).lower(),
                        str(shape in PRIMARY_CANDIDATE).lower(),
                    ]
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    ledger_dir = output / "ledger"
    summary_dir = output / "summaries"
    ledger_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = args.repo / "evidence/V1/v011-d4a1-oswe-20k-manifest-v2.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    osw_ids = {row["trajectory_id"] for row in manifest["sample"]}

    osw_acc = CorpusAccumulator("OSW_MINIMAX_20K")
    qwen_acc = CorpusAccumulator("QWEN_35334")
    osw_ledger = LedgerWriter(ledger_dir / "osw-event-allocation-ledger.parquet", LEDGER_SCHEMA)
    qwen_ledger = LedgerWriter(ledger_dir / "qwen-event-allocation-ledger.parquet", LEDGER_SCHEMA)
    session_writer = LedgerWriter(ledger_dir / "session-allocation-summary.parquet", SESSION_SCHEMA)

    osw_files = list(args.raw_root.glob("*minimax_m25*.parquet"))
    qwen_files = list(args.raw_root.glob("*qwen35_122b*.parquet"))
    if len(osw_files) != 37:
        raise ValueError(f"expected 37 Minimax shards, found {len(osw_files)}")
    if len(qwen_files) != 15:
        raise ValueError(f"expected 15 Qwen shards, found {len(qwen_files)}")

    for source, ordinal, row in iter_rows(osw_files):
        session_id = row["trajectory_id"]
        if session_id not in osw_ids:
            continue
        scaffold = "openhands" if source.name.startswith("openhands_") else "sweagent"
        process_session(
            osw_acc,
            osw_ledger,
            session_writer,
            scaffold=scaffold,
            session_id=session_id,
            source_file=source.name,
            source_row_ordinal=ordinal,
            messages=row["messages"],
            adapter="osw",
            provenance="frozen OSW manifest-v2 + historical v011_d4a1 detector semantics",
        )

    for source, ordinal, row in iter_rows(qwen_files):
        scaffold = "openhands" if source.name.startswith("openhands_") else "sweagent"
        process_session(
            qwen_acc,
            qwen_ledger,
            session_writer,
            scaffold=scaffold,
            session_id=row["trajectory_id"],
            source_file=source.name,
            source_row_ordinal=ordinal,
            messages=row["messages"],
            adapter="qwen",
            provenance="all 15 frozen Qwen shards + historical a2_cross_model detector semantics",
        )

    osw_ledger.close()
    qwen_ledger.close()
    session_writer.close()

    if osw_acc.sessions != 20000 or osw_acc.session_ids != osw_ids:
        raise ValueError(f"OSW identity closure failed: replay={osw_acc.sessions}, manifest={len(osw_ids)}")
    if qwen_acc.sessions != 35334:
        raise ValueError(f"Qwen identity closure failed: {qwen_acc.sessions} != 35334")

    corpus_summaries = [summarize(osw_acc), summarize(qwen_acc)]
    result = {
        "schema_version": 1,
        "method_version": "COC-ALLOCATION-R1",
        "status_ceiling": "PARTIAL",
        "corpora": {item["corpus"]: item for item in corpus_summaries},
    }
    dump_json(summary_dir / "coc-recalculation-summary.json", result)
    write_shape_csv(summary_dir / "shape-allocation-summary.csv", [osw_acc, qwen_acc])

    artifacts = {}
    for path in sorted(output.rglob("*")):
        if path.is_file():
            artifacts[str(path.relative_to(output)).replace("\\", "/")] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    dump_json(summary_dir / "replay-artifact-sha.json", artifacts)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
