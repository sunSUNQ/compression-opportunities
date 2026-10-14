# Supplement A — Frozen E1–E15 detector specifications

Evidence freeze: 2026-09-24. Cleanup checkpoint: `057477902627f0007aad42dcc853c7b6d52698e2`. All numerical tables are transcriptions of frozen fields; no experiment, aggregation, significance test, or detector is run during preparation. Original fractions are retained without calculating additional statistics.

Deterministic operational assignments define the census instrument. They do not imply safe deletion, semantic equivalence, or online savings. Thoughtworks retains original normalization; Open-SWE E1/E2/E3/E14 use path-aware normalization. Exact cross-corpus ratios are descriptive under this difference.

[evidence/V1/v011-d4a0-taxonomy-registry.json](sources/evidence/V1/v011-d4a0-taxonomy-registry.json) — field: `shapes`

| Shape | Name | Frozen predicate | Exposure | Source rule |
| --- | --- | --- | --- | --- |
| E1 | repeated_exact_command | identical normalized command appears >=2 times | HIGH | D3-E1 census rule (csim exact) |
| E2 | repeated_similar_command | digit-normalized command repeats >=2 times | HIGH | D3-E1 census rule |
| E3 | same_file_reread | non-shell same path >=2 times | HIGH | D3-E1 census rule |
| E4 | overlapping_file_read | same path with overlapping view ranges >=2 times | HIGH | D3-E1 census rule |
| E5 | same_search | search-class command with same query params >=2 times | HIGH | D3-E1 census rule |
| E6 | large_test_success | test command, observation >=3000 chars, explicit pass | HIGH | D3-E1 census rule |
| E7 | large_test_failure | test command, observation >=3000 chars, explicit fail | HIGH | D3-E1 census rule |
| E8 | large_lint_output | lint/typecheck command, observation >=3000 chars | HIGH | D3-E1 census rule |
| E9 | large_build_output | build command, observation >=3000 chars | HIGH | D3-E1 census rule |
| E10 | repeated_validation | test/lint command repeats >=2 times | HIGH | D3-E1 census rule |
| E11 | unchanged_validation | repeated validation with line-set Jaccard >=0.8 | HIGH | D3-E1 census rule |
| E12 | large_diagnostic | observation >=3000 chars containing Traceback/Exception/ERROR patterns | HIGH | D3-E1 census rule |
| E13 | large_output_near_terminal | observation >=2000 chars in last 25% of trajectory with <=3 subsequent observations | LOW | D3-E1 census rule |
| E14 | output_followed_by_reread | non-shell observation followed by same-path read within <=3 assistant turns | HIGH | D3-E1 census rule |
| E15 | output_followed_by_rederivation | same normalized command re-executed within <=3 assistant turns | HIGH | D3-E1 census rule |

The executable implementation and schema adapters are bundled in `sources/evidence/tools/v011_d4a1_census.py`; the registry predicates above are authoritative shape definitions. E4 is not measurable on the external corpus where read-range fields are absent. Null/missing metrics are not zero or negative findings. Exact normalization/classification code is preserved rather than rewritten.

[evidence/V1/v011-d4a0-taxonomy-registry.json](sources/evidence/V1/v011-d4a0-taxonomy-registry.json) — field: `dataset_independence_contract`

```json
"shape definitions and mechanical detectors are frozen from D3-E1 (prereg 55494bce) and MUST be applied unchanged to any external validation dataset; shapes discovered later are labeled post-hoc-discovered and validated only on the NEXT dataset"
```

## Shape relations and multi-label semantics (PAPER-A-TAXONOMY-RELATIONS-AMENDMENT, 2026-10-10)

Shapes are concurrent morphology labels, not exclusive classes and not a tree: an observation event carries every shape whose frozen predicate fires. Per-shape counts are therefore never summed across shapes. This subsection is a transcription of `taxonomy-relations-v1-report.md` (relations audit); no detector, threshold, or census value is changed.

**Construct-level inclusions (LOGICAL_IMPLIES; exhaustive counterexample search over every parsed event: zero violations — TW 450,298 events pre-amendment frame / OSW 1,296,519 events).**

| Inclusion | Why it holds by construction | Counterexample search |
| --- | --- | --- |
| E1 ⊆ E2 | E1 groups by normalized command; E2 by digit-normalized command. Equal normalized keys imply equal digit-normalized keys, so the E2 group of an E1 event contains its E1 group (≥2 members) and fires on the same event | 0 violations (TW 233,334 E1 events; OSW 600,181); session containment 1.0 (TW 9,872/9,872; OSW 19,992/19,992) |
| E14 ⊆ E3 | E14 marks the later member of a same-path pair (within the window); any such pair places both events in a same-path group of ≥2, which fires E3 on the same event | 0 violations (TW 66,081; OSW 154,643 E14 events); session containment 1.0 |
| E4 ⊆ E3 | Overlapping-range reads require the same path at least twice ⇒ same-path group ≥2 | TW 29,088/29,088 = 1.0; OSW: E4 structurally not measurable (no range fields) |
| E11 ⊆ E10 | E11 is marked only inside repeated-validation (test/lint, ≥2) groups, on members of those groups | 0 violations (TW 22; OSW 11 E11 events); session containment 1.0 |

**Key-caliber dependent relations (ADAPTER_DEPENDENT / EMPIRICAL_SUBSET).** E5 ⊆ E2 and E15 ⊆ E2 hold by construction (both are witnessed on digit-normalized keys); E5 ⊆ E1 is exact on TW (213/213) but only 0.803 on OSW (digit-differing repeated searches exist); E10's grouping key is exact-normalized on TW (E10 ⊆ E1 empirically 1.0) but digit-normalized on OSW (E10 ⊆ E1 only 0.6735); E15 ⊆ E1 is empirical (TW 8/8 at n=8; OSW 0.875). The first event of a path group can never be E14 (successor marking), so E3∖E14 is non-empty by construction.

**Cross-family intersections (INTERSECTION; observed, not logical).** E12∩E13 "terminal failure report": 3,930 events / 7,249 sessions (TW) and 1,648 / 7,531 (OSW). E12∩E1/E2 "repeated failing command produces repeated diagnostics": 28,381–29,995 events (OSW), 13,357–14,612 (TW). E12∩E14 "post-diagnosis reread": 5,248 (OSW) / 2,598 (TW). E13∩E1/E2: 5,502–5,800 (OSW) / 2,281–2,363 (TW). Sparse-family crossings (E6/E7/E9/E10/E11/E15 with anything) have too few events for interpretation and are reported only in the relations audit.

**Multi-label accounting (A1R2 authoritative frame; read-only recount consistent with the frozen census: unique events 578,283 and per-shape event hits match `v011-d4a1r2-tw-klear-census.json` exactly; census sha256-16 `630dcfaae0bca521`, parquet pin sha256-16 `3dd8ec3546cf771c`).** Events with ≥2 labels: 319,843 of 578,283 = 55.31% (event-level denominator: all parsed events). Sessions containing ≥1 multi-label event: 14,825 of 15,000 = 98.83% (session-level denominator: all corpus sessions). Shape assignments total 883,658 (multi-label events counted once per fired shape). Four denominators are distinct and never mixed: session incidence (all corpus sessions), event hits (per-shape; not additive across shapes), character allocation (each event's observation length split equally across its fired shapes — per-shape shares sum exactly to labeled characters in both corpora and both frames), and session-level COC (OSW-only; allocation-based byte accounting with overlap control; unsafe shapes E7/E12 excluded from qualified denominators; full-fit supported shapes only in the numerator). All of these are coverage-accounting quantities: they are not safe-compression rates, not deletable-character volumes, and not token savings.

**Real-event illustrations (frozen data; full excerpts and provenance in `taxonomy-relations-v1-report.md` §5).** Session-level counts quoted in the relations audit use the V1-scan id-set caliber; the paper's session-level statistics now use trajectory (row) identity (A1R3: 15,000 recorded trajectories, 13,053 unique session identifiers) — the relation lattice and inclusions are caliber-independent.

| Relation | Corpus | Session | Event | Shapes |
| --- | --- | --- | --- | --- |
| E1∧E2∧E3 | TW | nebius-swe-rebench-openhands::chatcmpl-8d0a85520f21e36b9f51b0d416dac5a | 48 | E1,E2,E3 |
| E1∧E2∧E3∧E4 | TW | nebius-swe-rebench-openhands::chatcmpl-92208a1fc35ba3791f8d3ab81b25afd | 15 | E1,E2,E3,E4 |
| E14∧E3 (view successor, not command repeat) | TW | swe-smith-claude-3-7-sonnet::davidhalter__parso.338a5760.combine_file_ | 8 | E14,E3 |
| E12∧E13 (submit report) | TW | swe-smith-claude-3-7-sonnet::encode__starlette.db5063c2.combine_module | 24 | E12,E13 |
| E2∖E1 (digit-differing repeat) | OSW | 6f0f9455-d972-4a90-b48d-2a465f13fa45 | 56 | E2 |
| E10∧E11 (unchanged validation) | TW | kwai-klear-swe-smith-mini::mahmoud__boltons.3bfcfdd0.combine_file__zbreonqj | 6 | E1,E2,E10,E11 |
| E10∧E11 | TW | kwai-klear-swe-smith-mini::mahmoud__boltons.3bfcfdd0.combine_file__zbreonqj | 10 | E1,E2,E10,E11 |
| E10∖E11 (changed validation) | TW | kwai-klear-swe-smith-mini::oauthlib__oauthlib.1fd52536.lm_rewrite__c7uizw13 | 8 | E1,E2,E10 |
| E10∖E11 | TW | kwai-klear-swe-smith-mini::oauthlib__oauthlib.1fd52536.lm_rewrite__c7uizw13 | 13 | E1,E2,E10 |
| E3∖E14 (first-of-group reread) | TW | swe-smith-claude-3-7-sonnet::conan-io__conan.86f29e13.pr_14164.1zmen2ge | 0 | E2,E3 |
| E2∖E1 then E2∧E3∧E14 (view-range digits differ) | TW | swe-smith-claude-3-7-sonnet::conan-io__conan.86f29e13.pr_14164.1zmen2ge | 0,1 | E2,E3 / E2,E3,E14 |
| E12∧E13 (submit report) | TW | swe-smith-claude-3-7-sonnet::facelessuser__soupsieve.a8080d97.func_pm_ctrl_shuffle__blbbmdgj.3qdud4nz | 10 | E12,E13 |
| E4∧E1∧E2∧E3 | TW | nebius-swe-rebench-openhands::chatcmpl-6b80470647e80e9c69cc5d0dadcfa1ea | 4 | E1,E2,E3,E4,E12 |
| E4∧E1∧E2∧E3∧E14 | TW | nebius-swe-rebench-openhands::chatcmpl-280c9130f0914d5256662645a39a08e0 | 18 | E1,E2,E3,E4,E14 |

Provenance: invariants and pair matrices from `v1-taxonomy-scan-tw.json` (sha256-16 `407db29b24447c7b`) and `v1-taxonomy-scan-osw.json` (`447c684196acf4b5`) produced by `v1_taxonomy_validation.py` (`a9a9e0e825ba08bb`; verbatim frozen detectors; prereg `6b012b4d33465b8c`), matrix CSV `19593816ac71802f`; A1R2-frame multi-label recount executed read-only against the pinned parquet with the frozen A1R2 detection block (byte-sliced, no transcription); relation examples mined read-only from the same pin. Relation audit: `taxonomy-relations-v1-report.md` (PASS). E8 has zero events in both public corpora; its specification example is synthetic and marked as such in the V1 examples document.


## Residual accounting and coverage boundary (PAPER-A-TAXONOMY-RESIDUAL-AMENDMENT, 2026-10-10)

Authoritative caliber: A1R3 trajectory-identity frame (`v011-d4a1r3-tw-trajectory-census.json`, sha256-16 `ae954c032022ca79`; gates ALL PASS). The event/character residual buckets are identical between A1R2 and A1R3 (verified bucket-by-bucket in the A1R3 census gates); they are event-level quantities outside the trajectory-identity change, cited here under the current authority. This section is a transcription of `taxonomy-residual-v1-report.md` (PASS); no detector, threshold, or census value is changed.

### Seven-bucket accounting (events / observation characters)

| Bucket | TW events | TW chars | OSW events | OSW chars |
| --- | --- | --- | --- | --- |
| detected (>=1 shape) | 357,394 | 920,214,271 | 695,780 | 1,782,349,136 |
| -- detected-unsafe-only (mask subset of {E7,E12}) | 10,354 | 132,791,414 | 25,105 | 309,512,393 |
| small-no-repeat (<2,000 chars) | 190,850 | 95,553,363 | 490,349 | 255,130,515 |
| large-uncovered-other (>=2,000 chars, no hit) | 29,925 | 223,431,268 | 110,359 | 719,563,215 |
| below-large-threshold (test/lint/build 2,000-3,000) | 114 | 275,584 | 24 | 60,455 |
| large-classed-ambiguous-features (test >=3,000, no pass/fail feature) | 0 | 0 | 7 | 63,973 |
| schema-missing-view-range (OSW E4) | — | — | 0 | 0 |
| orphan-observation (message-level diagnostic, outside the event universe) | 15,011 | 70,819,544 | 0 | 0 |
| **uncovered total (no shape hit)** | **220,889** | **319,260,215** | **600,739** | **974,818,158** |
| **totals** | **578,283** | **1,239,474,486** | **1,296,519** | **2,757,167,294** |

Conservation: detected + four uncovered buckets = totals exactly; the sum of per-shape allocation splits equals labeled characters (920,214,271 TW; 1,782,349,136 OSW). Detection coverage: TW 61.8% of events / 74.2% of characters; OSW 53.7% / 64.6%.

### large-uncovered-other (LUO) composition

LUO holds 70.0% of uncovered characters on TW (18.0% of all event characters; 5.2% of events) and 73.8% on OSW (26.1%; 8.5%). Composition — TW: other-class 21,970, view 4,789, search 3,166; length bands <3K 9,792 / 3-10K 14,225 / 10-50K 5,888 / >=50K 20; position mid(<0.5) 14,205 / 0.5-0.75 5,866 / terminal(>=0.75) 9,854; source: OpenHands-stratum 20,291, swe-smith 5,606, klear 4,028. OSW: other-class 57,765, view 48,866, search 3,728; bands <3K 41,227 / 3-10K 52,073 / 10-50K 16,292 / >=50K 798; scaffold OpenHands 58,681 / SWE-agent 51,709.

Structural characterization: by construction of the E2/E3 predicates, every LUO event is within-session csim-unique (no exact/similar command repeat) and outside any same-path group — i.e., a single-delivery large output without a within-session mechanical anchor. LUO is nonetheless a residual mixture (the five sample families below differ structurally) and is not asserted to be homogeneous.

### Detector boundaries (observable, not speculative)

| Boundary | Evidence |
| --- | --- |
| Command classification | compound commands (`cd X && cat > f << EOF ... && go test`) are classified by the first token (other); their test-run-shaped outputs land in LUO (OSW samples) |
| Size thresholds | 2,000 (LUO floor) and 3,000 (E12/E6-E9) leave a 2-3K in-class band (TW below-large 114 events; e.g., `mvn -q test ... | head -30` at 2,669 chars, SWE-agent, with [ERROR] content) |
| E13 window | terminal-band LUO (pos >= 0.75): TW 9,854 / OSW 17,766 — late but with >3 subsequent observations or position <0.75 |
| Repetition predicates | LUO events are within-session csim-unique and path-group-free by construction; cross-trajectory parameterized near-repeats (klear `nl -ba F | sed -n 'A,Bp'` family across sessions) are invisible to within-session predicates |
| Schema | E4 not measurable on OSW (no range fields); E8 zero lint in both public corpora (5 TW sub-threshold lint events archived as illustrations) |

### Real-event illustrations (frozen data; corpus / session / event)

| Family | Corpus | Session | Event | Command (abridged) | Chars | Reading |
| --- | --- | --- | --- | --- | --- | --- |
| directory tree dump | TW | swe-smith-claude-3-7-sonnet (view /testbed) | — | `str_replace_editor view /testbed` | 2,509 / 3,671 | information-unique listing, single delivery |
| file content dump | TW | kwai-klear-swe-smith-mini::safety (cat ./safety/scan/finder/handlers.py) | — | `cat ./safety/scan/finder/handlers.py` | 4,085 | single large view, no reread |
| parameterized near-repeat across sessions | TW | kwai-klear-swe-smith-mini::bottlepy__bottle.a8dfef30.{func_basic__mzx9j8vd, func_basic__3o4hv5ws, func_pm_op_change_const__vw9bgvbf} | — | `nl -ba bottle.py | sed -n '2243,2300p'` (ranges vary) | 2,012-2,391 | same pattern, different sessions/ranges — invisible within-session |
| single search result set | TW | kwai-klear-swe-smith-mini::bottlepy__bottle.a8dfef30.func_pm_ctrl_shuffle__h6g621us | 2 | `grep -n -A 20 "def auth" bottle.py` | 2,108 | E5 requires a same-query repeat |
| env-setup noise | TW | kwai-klear-swe-smith-mini (pip install requests && python test_auth_bug.py) | — | compound install+run | 2,032 | no dedicated shape |
| recursive search dump | TW | kwai-klear-swe-smith-mini::PyCQA__flake8.cf1542ce.func_basic__zg6dlaxx | 2 | `grep -r "statistics" src/ --include="*.py"` | 3,704 | single-shot |
| directory tree dump | OSW | openhands 0f0c4923-59d3-4230-898c-07ca42ee7c50 | 0 | `view /workspace/influxdata__telegraf-operator__1.0` | 2,620 | information-unique |
| compound-command test-shaped output | OSW | openhands (bridges/otelzap session) | — | `cd ... && cat > /tmp/test_*.go << 'EOF'` | 9,095-10,259 | `=== RUN ...` / `go: downloading` outputs classified other — command-classification boundary |
| threshold boundary | OSW | sweagent (mvn -q test ... | head -30) | — | `mvn -q test -pl amoro-common ...` | 2,669 | [ERROR] content, 331 chars below the 3,000 gate → below-large bucket |
| heredoc write echo | OSW | openhands 0f8dc6f5-cd8f-4100-ba43-3ff7a7e5e9b3 | 150 | `cat > /tmp/patch.txt << 'EOF'` | 27,781 | write-operation echo, no dedicated shape |

TW directory-dump/file-dump rows come from the residual-v1 stratified mining pass (session prefixes shown; full IDs and observation excerpts in `taxonomy-residual-v1-report.md` §4); OSW rows with UUIDs are from the V1 example pools (`v1-taxonomy-scan-osw.json`, sha256-16 `447c684196acf4b5`).

### Boundary versus speculative opportunity

Observable detector boundaries (above) are transcriptions of frozen-predicate behavior. The residual pool motivates **post-hoc hypotheses** — e.g., a single-delivery structured-dump family or cross-trajectory parameterized repetition — to be validated on the NEXT dataset under the dataset-independence contract before any shape is proposed; no E16 is added here, nothing in the residual is asserted to be safely compressible, and unmatched does not mean incompressible (detection and safety are separate properties; see the non-exclusive-semantics subsection).
