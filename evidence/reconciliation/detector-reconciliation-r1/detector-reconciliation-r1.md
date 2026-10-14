# Paper A Detector Cross-Corpus Reconciliation R1

## Verdict

`RECONCILIATION_STATUS = HOLD`

Detector implementation and full replay are `PASS`; the overall task is `HOLD` because the formal 120-item annotation sample manifest is not present in the shared frozen evidence path, so item-level compatibility cannot be completed without crossing the annotation-agent isolation boundary.

## Isolation and baseline

- Branch: `codex/paper-a-detector-reconciliation-r1`
- Base commit: `5e57cf5e62a688cfd43b5762d83b1906e637283c`
- Versioned implementation: `A0-XCORPUS-R1.0.0`
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
| E1 | identical normalized command appears >=2 times | OSW appended path to view/open/editor command strings | keep path separate from exact command | OSW +7 rows | REPLICATED (1.0289) |
| E2 | digit-normalized command repeats >=2 times | OSW appended path before digit normalization | keep path separate; digit normalization applies to command only | OSW +5 rows | REPLICATED (1.0143) |
| E3 | non-shell same path >=2 times | both implementations grouped explicit path | shared explicit-path grouping | no row-incidence change | REPLICATED (1.2191) |
| E4 | same path with overlapping view ranges >=2 times | OSW hard-omitted the detector despite populated view_range | read view_range in adapter; apply frozen closed-interval overlap rule | OSW 0 -> 13,885 rows | PARTIAL_REPLICATION (2.5051) |
| E5 | search-class command with same query params >=2 times | OSW grouped search commands by digit-normalized csim | group search parameters by exact cnorm | OSW -74 rows | PARTIAL_REPLICATION (2.1696) |
| E6 | test command, observation >=3000 chars, explicit pass | OSW used a narrower pass regex and had no exit code | shared A0 pass/fail regex; explicit exit when available, text fallback otherwise | OSW -3 rows | DATASET_SPECIFIC (0.0270) |
| E7 | test command, observation >=3000 chars, explicit fail | OSW used a narrower fail regex and had no exit code | shared A0 pass/fail regex; explicit exit when available, text fallback otherwise | OSW +1 row | DATASET_SPECIFIC (0.0451) |
| E8 | lint/typecheck command, observation >=3000 chars | same threshold and command class | shared rule | no row-incidence change | NOT_ESTIMABLE_ZERO_BASELINE (—) |
| E9 | build command, observation >=3000 chars | same threshold and command class | shared rule | no row-incidence change | REPLICATED (0.7500) |
| E10 | test/lint command repeats >=2 times | OSW grouped validation commands by digit-normalized csim | group repeated validation by exact cnorm | OSW -4 rows | DATASET_SPECIFIC (0.0263) |
| E11 | repeated validation with line-set Jaccard >=0.8 | OSW inherited csim validation groups | Jaccard >=0.8 only within exact-cnorm validation groups | OSW -1 row | DATASET_SPECIFIC (0.0430) |
| E12 | observation >=3000 chars containing Traceback/Exception/ERROR patterns | same size threshold and diagnostic regex | shared rule | no row-incidence change | REPLICATED (1.0902) |
| E13 | observation >=2000 chars in last 25% of trajectory with <=3 subsequent observations | same >=2K, position >=.75, <=3 turns-after rule | shared rule | no row-incidence change | REPLICATED (0.7942) |
| E14 | non-shell observation followed by same-path read within <=3 assistant turns | OSW marked any adjacent same-path successor within three events | require same-path successor to be view-class | OSW -2,591 rows | REPLICATED (1.1092) |
| E15 | same normalized command re-executed within <=3 assistant turns | both use digit-normalized validation/build successor within three events | shared rule | no row-incidence change | DATASET_SPECIFIC (0.0417) |

## Full replay result

- TW: 15,000/15,000 rows; all 15 occurrence counts exactly match frozen A1R3.
- OSW: 20,000/20,000 manifest IDs found.
- Determinism: double evaluation PASS; TW label SHA `eca542a321d791f68380c5cd17bd53479777b01c75bf9bdb20381c93682f2f86`, OSW label SHA `c22946594c47f17ca19ee28e1e3da535392fc5c381997a502417d23ee9548dbf`.
- Replication: 7 `REPLICATED`, 2 `PARTIAL_REPLICATION`, 5 `DATASET_SPECIFIC`, 1 `NOT_ESTIMABLE_ZERO_BASELINE`.
- Candidate summary: **9/14 ratio-comparable shapes replicate fully or partially**. E8 is detector-measurable but zero in both frames, so its ratio is not estimable.
- Core six remain `REPLICATED`; full-precision ratios span 0.7942–1.2191.

Key corrected OSW incidences: E4 69.4250%; E5 1.6200%; E14 81.8800%.

## Versioning and supersession

R1 is a new implementation version. It is a candidate display authority only for detector-derived cross-corpus incidence and replication. Historical A0, manifests, raw data, census outputs, figures, tables, and manuscript remain immutable provenance. Paper integration must be a separate reviewed task after annotation-manifest compatibility is resolved.

## Validation

- Golden fixtures: 10 cases, including exact-vs-digit grouping, range identity, range sentinel behavior, pass/fail fallback, E14 successor class, and adapter equivalence.
- Unit test methods: 4/4 PASS.
- Full replay integrity: PASS.
- Input SHA records: embedded in `replay/replay-results.json`.
- Formal annotation compatibility: HOLD (manifest unavailable in allowed shared path).
