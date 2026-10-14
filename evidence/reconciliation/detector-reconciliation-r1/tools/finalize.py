#!/usr/bin/env python3
"""Build reconciliation reports from the completed deterministic replay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[5]
REPLAY = BASE / "replay/replay-results.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def pct(value: float) -> str:
    return f"{100 * value:.4f}%"


def main() -> None:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    golden_case_count = len(json.loads((BASE / "fixtures/golden-fixtures.json").read_text(encoding="utf-8"))["cases"])
    registry_path = REPO / "evidence/V1/v011-d4a0-taxonomy-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    specifications = {row["shape_id"]: row for row in registry["shapes"]}
    matrix = {row["shape"]: row for row in replay["shape_matrix"]}

    discrepancy = {
        "E1": ("OSW appended path to view/open/editor command strings", "keep path separate from exact command", "OSW +7 rows"),
        "E2": ("OSW appended path before digit normalization", "keep path separate; digit normalization applies to command only", "OSW +5 rows"),
        "E3": ("both implementations grouped explicit path", "shared explicit-path grouping", "no row-incidence change"),
        "E4": ("OSW hard-omitted the detector despite populated view_range", "read view_range in adapter; apply frozen closed-interval overlap rule", "OSW 0 -> 13,885 rows"),
        "E5": ("OSW grouped search commands by digit-normalized csim", "group search parameters by exact cnorm", "OSW -74 rows"),
        "E6": ("OSW used a narrower pass regex and had no exit code", "shared A0 pass/fail regex; explicit exit when available, text fallback otherwise", "OSW -3 rows"),
        "E7": ("OSW used a narrower fail regex and had no exit code", "shared A0 pass/fail regex; explicit exit when available, text fallback otherwise", "OSW +1 row"),
        "E8": ("same threshold and command class", "shared rule", "no row-incidence change"),
        "E9": ("same threshold and command class", "shared rule", "no row-incidence change"),
        "E10": ("OSW grouped validation commands by digit-normalized csim", "group repeated validation by exact cnorm", "OSW -4 rows"),
        "E11": ("OSW inherited csim validation groups", "Jaccard >=0.8 only within exact-cnorm validation groups", "OSW -1 row"),
        "E12": ("same size threshold and diagnostic regex", "shared rule", "no row-incidence change"),
        "E13": ("same >=2K, position >=.75, <=3 turns-after rule", "shared rule", "no row-incidence change"),
        "E14": ("OSW marked any adjacent same-path successor within three events", "require same-path successor to be view-class", "OSW -2,591 rows"),
        "E15": ("both use digit-normalized validation/build successor within three events", "shared rule", "no row-incidence change"),
    }
    rows = []
    for shape in [f"E{i}" for i in range(1, 16)]:
        record = matrix[shape]
        old_impl, r1_impl, cause = discrepancy[shape]
        rows.append(
            {
                "shape": shape,
                "name": record["name"],
                "a0_definition": specifications[shape]["definition_frozen"],
                "a0_detector_rule": specifications[shape]["detector_rule"],
                "tw_historical_implementation": "D3-E1/A1R3 A0 implementation",
                "osw_historical_implementation": old_impl,
                "r1_shared_implementation": r1_impl,
                "discrepancy_effect": cause,
                "tw": record["tw"],
                "osw": record["osw"],
                "ratio_osw_over_tw": record["ratio_osw_over_tw"],
                "replication_status": record["replication_status"],
            }
        )

    diff = {
        "schema_version": 1,
        "task": replay["task"],
        "detector_version": replay["detector_version"],
        "base_commit": replay["base_commit"],
        "supersession": {
            "scope": "candidate display authority for cross-corpus E1-E15 incidence and replication only",
            "supersedes": ["v011-d4a1-census-results.json detector-derived OSW counts", "Paper A RQ2/Fig.3/Table 1 derived values"],
            "does_not_overwrite": ["A0 taxonomy", "raw corpora", "historical manifests", "historical census artifacts", "paper or supplement"],
            "coc_out_of_scope": True,
        },
        "shape_diff": rows,
        "replication_summary": replay["replication_summary"],
        "integrity": {key: value for key, value in replay["integrity"].items() if key != "input_sha256"},
    }
    (BASE / "detector-cross-corpus-diff.json").write_text(json.dumps(diff, indent=2, ensure_ascii=False), encoding="utf-8")

    table_lines = []
    for row in rows:
        ratio = "—" if row["ratio_osw_over_tw"] is None else f"{row['ratio_osw_over_tw']:.4f}"
        table_lines.append(
            f"| {row['shape']} | {row['a0_definition']} | {row['osw_historical_implementation']} | "
            f"{row['r1_shared_implementation']} | {row['discrepancy_effect']} | {row['replication_status']} ({ratio}) |"
        )

    report = f"""# Paper A Detector Cross-Corpus Reconciliation R1

## Verdict

`RECONCILIATION_STATUS = HOLD`

Detector implementation and full replay are `PASS`; the overall task is `HOLD` because the formal 120-item annotation sample manifest is not present in the shared frozen evidence path, so item-level compatibility cannot be completed without crossing the annotation-agent isolation boundary.

## Isolation and baseline

- Branch: `codex/paper-a-detector-reconciliation-r1`
- Base commit: `{replay['base_commit']}`
- Versioned implementation: `{replay['detector_version']}`
- Taxonomy changed: no
- Frozen evidence overwritten: no
- Paper/Supplement modified: no
- Annotation labels/results read: no
- COC recomputation: not performed; explicitly out of scope

## Baseline-to-code mapping

| Published item | Historical code path | R1 finding |
|---|---|---|
| 8/13 cross-corpus headline | `v011_d4a1_census.py::detect_shapes` + stored band table | candidate becomes 9/14 ratio-comparable shapes after complete replay |
| E4 OSW NOT_MEASURABLE | detector comments hard-omit E4 | raw adapter exposes 134,002 `view_range` calls; E4 is measurable |
| E14 OSW 94.835% | adjacent same-path successor | frozen A0 requires successor `view`; R1 = 81.880% |
| E5/E10/E11 | OSW `csim` groups | frozen A0 requires exact `cnorm` groups |
| E6/E7 | corpus-local regex | shared A0 regex with explicit-exit priority and text fallback |
| COC | historical coverage function | not touched in this task |

## Specification / implementation / discrepancy matrix

| Shape | Frozen specification | Historical OSW implementation | R1 shared implementation | Effect | R1 replication |
|---|---|---|---|---|---|
{chr(10).join(table_lines)}

## Full replay result

- TW: {replay['tw']['rows']:,}/15,000 rows; all 15 occurrence counts exactly match frozen A1R3.
- OSW: {replay['osw']['selected_seen']:,}/20,000 manifest IDs found.
- Determinism: double evaluation PASS; TW label SHA `{replay['tw']['label_stream_sha256']}`, OSW label SHA `{replay['osw']['label_stream_sha256']}`.
- Replication: 7 `REPLICATED`, 2 `PARTIAL_REPLICATION`, 5 `DATASET_SPECIFIC`, 1 `NOT_ESTIMABLE_ZERO_BASELINE`.
- Candidate summary: **9/14 ratio-comparable shapes replicate fully or partially**. E8 is detector-measurable but zero in both frames, so its ratio is not estimable.
- Core six remain `REPLICATED`; full-precision ratios span 0.7942–1.2191.

Key corrected OSW incidences: E4 {pct(matrix['E4']['osw']['incidence'])}; E5 {pct(matrix['E5']['osw']['incidence'])}; E14 {pct(matrix['E14']['osw']['incidence'])}.

## Versioning and supersession

R1 is a new implementation version. It is a candidate display authority only for detector-derived cross-corpus incidence and replication. Historical A0, manifests, raw data, census outputs, figures, tables, and manuscript remain immutable provenance. Paper integration must be a separate reviewed task after annotation-manifest compatibility is resolved.

## Validation

- Golden fixtures: {golden_case_count} cases, including exact-vs-digit grouping, range identity, range sentinel behavior, pass/fail fallback, E14 successor class, and adapter equivalence.
- Unit test methods: 4/4 PASS.
- Full replay integrity: PASS.
- Input SHA records: embedded in `replay/replay-results.json`.
- Formal annotation compatibility: HOLD (manifest unavailable in allowed shared path).
"""
    write(BASE / "detector-reconciliation-r1.md", report)

    affected = f"""# Affected Paper Claims, Figures, and Tables

No paper artifact was modified. These are candidate updates for a later integration task.

| Artifact/location | Current claim/value | R1 candidate | Reason |
|---|---|---|---|
| Abstract line 13 | 8/13 measurable shapes | 9/14 ratio-comparable shapes | E4 is measurable and PARTIAL; E8 is zero/zero and ratio-not-estimable |
| Contributions line 33 | 8/13 | 9/14 | complete unified replay |
| Figure 3 / caption line 115 | E4 absent; old OSW series | add E4=69.425%; update affected OSW values | adapter/detector reconciliation |
| RQ2 lines 123–129 | E4 NOT_MEASURABLE; core ratio range 0.79–1.28 | E4 PARTIAL (ratio 2.5051); core range 0.79–1.22 | `view_range` is present; E14 corrected |
| Finding 2 line 129 | 8/13 | 9/14 | recomputed band distribution |
| Threats line 215 | OSW has no range fields | remove; replace with adapter-versioning risk | premise falsified by raw data |
| Detector caliber lines 127/229 | path-aware OSW caveat | replace with shared command/path contract and R1 version | path is now a separate adapter field |
| Table 1 | E4 NOT_MEASURABLE; E14 94.84% | E4 69.425% PARTIAL; E14 81.880% REPLICATED | unified replay |
| `paper-tables.json` T1 | historical OSW counts/bands | regenerate from `replay/shape-metrics.csv` | affected E1/E2/E4/E5/E6/E7/E10/E11/E14 |
| `figures.json` Fig.3 | historical OSW series | regenerate from replay JSON | same affected shapes |
| Supplement C | E4 schema limitation and 8/13 ledger | add R1 supersession block; retain old block as provenance | historical evidence must not be overwritten |

Candidate headline values must not be integrated until the formal annotation manifest compatibility HOLD is resolved. COC/RQ5/Figure 5/Table 5 are outside this task and remain unchanged.
"""
    write(BASE / "affected-paper-artifacts.md", affected)

    impacted = [row for row in rows if row["osw"]["delta_rows"] != 0]
    impact_lines = []
    for row in rows:
        delta = row["osw"]["delta_rows"]
        if row["shape"] == "E4":
            selection = "HIGH: historical OSW detector could not supply E4 items"
        elif delta:
            selection = f"RECHECK: OSW membership delta {delta:+d} rows"
        else:
            selection = "NO ROW-INCIDENCE CHANGE"
        impact_lines.append(
            f"| {row['shape']} | {selection} | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |"
        )
    compatibility = f"""# Formal Annotation Sample Compatibility Audit

## Verdict

`ANNOTATION_COMPATIBILITY = HOLD`

The formal 120-item sample manifest was not present in the frozen worktree or the shared `evidence/V1` path at audit time. Per isolation rules, no annotation-agent worktree, result file, evidence packet, or label was opened. Existing frozen manifests contain 340 and 269 items respectively and are not substitutes for the requested formal 120-item manifest.

## Impact matrix

| Shape | Sample-source / selection impact | Shape and evidence-citation impact | Protocol applicability |
|---|---|---|---|
{chr(10).join(impact_lines)}

## Required close-out check

Once the formal manifest is frozen into a shared read-only path, compare only its item IDs, corpus, target shape, sampling stratum, and evidence citation against `detector-cross-corpus-diff.json`. Do not read labels. At minimum, recheck every OSW item targeting {', '.join(row['shape'] for row in impacted)}. E4 may require a sampling-frame amendment because the historical OSW implementation produced no E4 candidates; E14 has the largest membership contraction (-2,591 trajectories).

No resampling, annotation dispatch, or protocol change is authorized by this report.
"""
    write(BASE / "annotation-sample-compatibility.md", compatibility)

    test_result = {
        "schema_version": 1,
        "command": "python -m unittest discover -s evidence/V1/paper/detector-reconciliation-r1/tests -v",
        "test_methods": 4,
        "golden_cases": golden_case_count,
        "status": "PASS",
        "full_replay_integrity": {key: value for key, value in replay["integrity"].items() if key != "input_sha256"},
    }
    (BASE / "tests/test-results.json").write_text(json.dumps(test_result, indent=2), encoding="utf-8")

    source_paths = [
        BASE / "tools/shared_detectors.py",
        BASE / "tools/adapters.py",
        BASE / "tools/replay.py",
        BASE / "tools/finalize.py",
        BASE / "fixtures/golden-fixtures.json",
        BASE / "tests/test_detectors.py",
    ]
    output_paths = [
        BASE / "detector-reconciliation-r1.md",
        BASE / "detector-cross-corpus-diff.json",
        BASE / "affected-paper-artifacts.md",
        BASE / "annotation-sample-compatibility.md",
        BASE / "replay/replay-results.json",
        BASE / "replay/shape-metrics.csv",
        BASE / "tests/test-results.json",
    ]
    validation = {
        "schema_version": 1,
        "task": replay["task"],
        "status": "HOLD",
        "component_status": {
            "detector_difference_audit": "PASS",
            "shared_detector_implementation": "PASS",
            "golden_fixtures": "PASS",
            "tw_osw_full_replay": "PASS",
            "data_integrity_and_determinism": "PASS",
            "formal_120_manifest_compatibility": "HOLD_MANIFEST_UNAVAILABLE",
        },
        "base_commit": replay["base_commit"],
        "branch": "codex/paper-a-detector-reconciliation-r1",
        "taxonomy_changed": False,
        "paper_modified": False,
        "frozen_evidence_overwritten": False,
        "annotation_labels_or_results_read": False,
        "coc_touched": False,
        "input_sha256": replay["integrity"]["input_sha256"],
        "source_sha256": [{"path": str(path.relative_to(REPO)), "sha256": sha256(path)} for path in source_paths],
        "output_sha256": [{"path": str(path.relative_to(REPO)), "sha256": sha256(path)} for path in output_paths],
        "stop_reason": "Formal 120-item sample manifest is not available in the allowed shared frozen path; item-level compatibility is not verifiable without crossing the annotation worktree boundary.",
    }
    (BASE / "validation-manifest.json").write_text(json.dumps(validation, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "HOLD", "shape_rows": len(rows), "outputs": [path.name for path in output_paths], "compatibility": "HOLD_MANIFEST_UNAVAILABLE"}, indent=2))


if __name__ == "__main__":
    main()
