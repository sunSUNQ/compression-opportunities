# Paper Claim Trace — Full Draft v1 (D4-P3)

每条 substantive claim → RQ/Finding → exact metric → frozen artifact → frame → detector version → limitation。正文修订时若任一行失效，draft 不得提交。

| # | 位置 | Claim | Metric | Frozen artifact | Frame | Detector | Limitation |
|---|---|---|---|---|---|---|---|
| C01 | Abstract | 35,334 trajectories, two corpora, two scaffolds, two models | corpus composition | v011-d4a1-oswe-20k-manifest-v2.json + D3-E1 census | TW 15K + OSW Minimax 20K + Qwen 35K | A0 1865a160 | L5 |
| C02 | Abstract | 15-shape taxonomy, frozen detectors | taxonomy definition | v011-d4a0-taxonomy-registry.json + V0.11-D3 preregs (49482bbf internal morphology census; 55494bce E1–E15 frozen before aggregation) | dataset-independent | A0 1865a160 | L1 |
| C03 | Abstract | 8/13 measurable shapes replicate (all six core REPLICATED, full-precision ratios 0.79–1.28; five sparse E6/E7/E10/E11/E15 DATASET_SPECIFIC) | replication band | v011-d4a1r3-tw-trajectory-census.json bands_full_precision (TW, trajectory identity) + v011-d4a1-census-results.json shape_results (OSW) | TW vs OSW | A0 1865a160 | L3/L6 + low-incidence corpus-composition |
| C04 | Abstract | Large diagnostics 72.9%→79.5% | trajectory-level incidence | v011-d4a1r3-tw-trajectory-census.json per_shape + v011-d4a1-census-results.json | TW/OSW | A0 | — |
| C05 | Abstract | Late large outputs 58.7%→46.6% | trajectory-level incidence | same | TW/OSW | A0 | — |
| C06 | Abstract | Core shapes model-stable, ratios 0.68–1.013 | same-scaffold cross-model ratio | v011-d4a2r1-full-factorial.json core_verification + v011-d4a2-cross-model.json | OH/SA × MM/QW | A0 | L2 (sparse excluded) |
| C07 | Abstract | Scaffold variation 28.2pp > model 12.7pp, interaction 16.5pp | E13 2x2 contrasts | v011-d4a2r1-full-factorial.json | controlled frame | A0 | L1 |
| C08 | Abstract | Shipped SOC 2.07% / COC 0.39%; candidate SOC 100% / COC 90.13%; Gap 99.57% | dual coverage ledger | v011-d4a1-census-results.json coverage | OSW Minimax 20K | A0 | L4 |
| C09 | §1 | Repeated info re-enters context in near-original form | qualitative (motivation) | narrative | — | — | — |
| C10 | §2 | Opportunity definition (conservative; detection ≠ safe deletion) | definition | — | — | — | — |
| C11 | §3 | Frozen-before-external-validation discipline | process | A0 freeze commit 1865a160 | — | — | — |
| C12 | §4 | Sessions are observations within a frame, not independent tasks | framing | — | — | — | — |
| C13 | §5 | E12 72.9%/79.5%, median 8.0K (median from pre-amendment frozen ledger) | trajectory-level incidence + median | T1 / A1R3 census + both census JSONs | TW/OSW | A0 | — |
| C14 | §5 | E13 58.7%/46.6%, median 5.8K p75 10.3K (medians pre-amendment) | incidence + median/p75 | same | TW/OSW | A0 | — |
| C15 | §5 | E3 82.0%/~100%; E2 98.6%/~100% | trajectory-level incidence | same | TW/OSW | A0 | — |
| C16 | §5 | Unchanged validation 0.81%; build 0.01% | trajectory-level incidence | same | TW/OSW | A0 | L2 |
| C17 | §6 | 8/13 REPLICATED/PARTIAL (R7+P1; DS5 E6/E7/E10/E11/E15 corpus-composition-sensitive; NM2 E4/E8) | band distribution | v011-d4a1r3-tw-trajectory-census.json bands_full_precision (trajectory identity; bands unchanged under id-set caliber) | TW vs OSW | A0 | L3/L6 + low-incidence corpus-composition |
| C18 | §6 | E4 NOT_MEASURABLE (no range fields) — schema limitation | detector applicability | same + A0 registry | OSW | A0 | L3 |
| C19 | §6 | E1/E2/E3/E14 caliber caveat (path-aware on OSW side; A1R1 same-caliber shifts +0.14/+0.08/+0.15/+3.74pp are historical pre-amendment-frame results; A1R3 trajectory-identity frame ratios 1.03/1.01/1.22/1.28) | normalization scope | v011-d4a1r1-tw-same-caliber.json + v011-d4a1r3-tw-trajectory-census.json | cross-corpus | A0 | L6 |
| C20 | §7 Table3 | Six core shapes all MODEL_STABLE (max ratio shift E13 0.68 OH) | cross-model ratios | v011-d4a2r1-full-factorial.json core_verification | OH/SA × MM/QW | A0 | L2 |
| C21 | §7 | Sparse shapes excluded from core narrative | scoping | v011-d4a1-census-results.json | — | A0 | L2 |
| C22 | §8 | E13 2x2 four cells 0.6487/0.284/0.4389/0.2392 | factorial incidence | v011-d4a2r1-full-factorial.json | OH/SA × MM/QW | A0 | L1 |
| C23 | §8 | Contrasts −36.5/−20.0/−21.0/−4.5pp; mean 28.2/12.7; DiD 16.5pp | E13 contrasts | same | controlled frame | A0 | L1 |
| C24 | §8 | Mechanism interpretation: OH view stream vs SA command flow (interpretation only) | qualitative reading | narrative + A0 shape semantics | controlled frame | A0 | L1 |
| C25 | §9 | Shipped near-zero coverage of repeated-delivery band | mapping | A0 registry mapping | OSW 20K | A0 | L4 |
| C26 | §9 | E12 partial coverage by capability with negative task-level history | coverage + history | A0 registry + D2-E7 frozen record | OSW 20K | A0 | — |
| C27 | §9 | Qwen-side same structure (6.12%/1.14% vs 100%/91.27%) | dual ledger on Qwen | v011-d4a2-cross-model.json coverage_qwen | OH Qwen 15K | A0 | — |
| C28 | §10 F1 | RDS offline: 218M chars removed; 90.1% byte-coverage; 289,822 events; 0 failures; exact 1.0; capture 0.8098 | replay ledger | v011-d3e4-rds-prototype-replay.json | 15K offline replay | A0 | — |
| C29 | §10 F1 | A/B correctness-clean 24/24; zero attributable failures; no backlash | pair oracle | v011-d5-rds-online-ab.json | OSW 24 pairs | A0 | — |
| C30 | §10 F1 | +7.38% NON-QUALIFYING; permutation p=0.1185; nonneg 54% | pair-level aggregate + permutation | same | 24 pairs | A0 | L4 |
| C31 | §10 F1 | Within-arm replicate swing median 27.96% > B/T delta 23.79% | within-arm replicate deltas | v011-d3e7-power-design.json | D5 24 pairs | A0 | L7 |
| C32 | §10 F1 | Mechanism exposure median 0.011%; signal:noise 0.0003 | exposure rate | same | D5 24 pairs | A0 | L7 |
| C33 | §10 F1 | Power <0.80 for 3%/5% at ≤10 reps (0.622/0.699 best) | power simulation | same | D5-derived noise | A0 | L7 |
| C34 | §11 D1-D3 | Opportunity-aware / scaffold-in-benchmark / semantic frontier implications | qualitative (design implications) | narrative | — | — | — |
| C35 | §12 | L1-L7 threats embodied | threats mapping | limitations.md | — | — | — |
| C36 | §13 | Related work positioned as measurement layer (citations pending) | positioning | [CITATION NEEDED] ×3 groups | — | — | — |
| C37 | §14 | Conclusion three-sentence summary | qualitative (consistent with Abstract/Intro) | narrative | — | — | — |

## Coverage summary

- Quantitative claims: C01–C08, C13–C33 (30 traced; zero untraced)
- Qualitative/motivation claims: C09/C10/C12/C24/C34/C37 (6)
- [EVIDENCE NEEDED]: 0
- [CITATION NEEDED]: 3 (Related Work groups §13)
- Frozen-number drift: none (all values quoted from frozen artifacts)

| C38 | §3.5 LLM Audit | Heterogeneous-LLM audit: overall Q1 raw agreement 52.65%, κ=0.2665 (locked recomputation, annotation-statistics-amendment.json; published 0.1531 superseded as unreproducible); E13 Q1 raw agreement 96.4% (κ=0.9146, the only high interpretable shape-level κ) | construct-validity/model-audit/model-audit-reconciled.json + annotation-statistics-amendment.json (de30138fa71414a0) | stratified 340-item interpretation audit | A0 1865a160 | Not human ground truth; E13 result cannot be reported without the overall result |
| C39 | §3.5 LLM Audit | Overall Q2 raw agreement 49.41%, κ=0.2284 (locked recomputation; published 0.0003 superseded as unreproducible; large share of Q2 disagreement = differing evaluator scale usage, an observable response-style difference); E13 Q2 raw agreement 78.6% | construct-validity/model-audit/model-audit-reconciled.json + annotation-statistics-amendment.json (de30138fa71414a0) | stratified 340-item interpretation audit | A0 1865a160 | Interpretation-sensitivity diagnostic, not detector precision |
| C40 | §12 Threats | Construct validity probed via heterogeneous-LLM audit, not human annotation | construct-validity/model-audit/model-audit-reconciled.json + manuscript §3.5 | stratified 340-item interpretation audit | A0 1865a160 | L1; no human ground-truth claim |
| C41 | §3 Overlap | Shapes are non-exclusive multi-label labels (not a tree); construct-level inclusions E1⊆E2, E14⊆E3, E4⊆E3, E11⊆E10 with zero counterexamples over all parsed events (both corpora); four distinct accounting denominators; allocation split sums exactly to labeled characters; coverage shares ≠ safe-compression/deletable-chars/token savings | predicate-level invariant search + allocation conservation | v1-taxonomy-scan-tw.json + v1-taxonomy-scan-osw.json invariants (a9a9e0e825ba08bb) + taxonomy-v1-overlap-matrix.csv + v011-d4a1r2-tw-klear-census.json conservation + taxonomy-relations-v1-report.md | TW + OSW | A0 1865a160 | wording discipline: coverage-accounting shares only |

## P3R6 amendment: C38-C40 added (heterogeneous-LLM audit integration); C36 updated to 3-group structure with 19 citations; zero frozen-number drift.

## PAPER-A-NUMBERS-UPDATE amendment (2026-10-10): C03/C04/C05/C13/C14/C15/C16/C17/C19 updated to the V0.11-D4-A1R2 klear recovery census (v011-d4a1r2-tw-klear-census.json, sha256-16 630dcfaae0bca521; prereg e98345d748ac7620; regression gate PASS; A0 detectors zero changes). Discovery-side numbers migrated to the recovered full three-source parse: 8/13 measurable shapes satisfy the bands (R7+P1), all six core shapes REPLICATED (ratios 0.81–1.35), five sparse shapes E6/E7/E10/E11/E15 DATASET_SPECIFIC. OSW-side, model, scaffold, factorial, and coverage claims (C06–C08, C20–C28, C33) unchanged. Pre-amendment numbers retained as superseded provenance (paper-tables.pre-a1r2.json; git history).

## PAPER-A-TAXONOMY-CONSTRUCTION-AMENDMENT (2026-10-10): C02 artifact reference extended to the two frozen D3 preregs (49482bbf internal morphology census 158 realized sessions; 55494bce E1–E15 frozen before aggregation). §3.1 Construction rewritten to the two-stage preregistered origin (internal 158-session morphology census S1–S8+S7b → D3-E1 prereg extension E1–E15 → definition-level freeze → TW 15K first census → D4-A0 registry freeze → OSW 20K external replay); three evidenced definitional splits described (S2→E1/E2, S3→E10/E11, S1→E12/E13); corrected: "derived from 15K by scanning", "iteratively consolidating", "E-numbers reflect discovery order" (→ prereg enumeration order), "recorded at freeze time" (→ registry freeze preceding external use). No candidate-merge / human-consensus / rejected-candidate-list claims introduced. All quantitative claims (C01–C40) unchanged.

## PAPER-A-TAXONOMY-RELATIONS-AMENDMENT (2026-10-10): C41 added (non-exclusive shape semantics, construct-level inclusions with zero counterexample violations, four accounting denominators, allocation conservation, coverage-shares-only wording). Source: taxonomy-relations-v1-report.md (PASS) + A1R2-frame read-only multi-label recount (55.31% of events / 98.83% of sessions; denominators and hash recorded in Supplement A). Body §3 stays qualitative (no percentages); Supplement A carries the full lattice, adapter preconditions, intersections, and 14 real-event rows. Quantitative claims C01–C40 unchanged.

## PAPER-A-TAXONOMY-RELATIONS-AMENDMENT (2026-10-10): C41 added (non-exclusive shape semantics, construct-level inclusions with zero counterexample violations, four accounting denominators, allocation conservation, coverage-shares-only wording). Source: taxonomy-relations-v1-report.md (PASS) + A1R2-frame read-only multi-label recount (55.31% of events / 98.83% of sessions; denominators and hash recorded in Supplement A). Body §3 stays qualitative (no percentages); Supplement A carries the full lattice, adapter preconditions, intersections, and 14 real-event rows. Quantitative claims C01–C40 unchanged.

## PAPER-A-SESSION-IDENTITY-AMENDMENT (2026-10-10): C03/C04/C05/C13/C14/C15/C16/C17/C19 updated to the V0.11-D4-A1R3 trajectory-identity caliber (prereg v011-d4a1r3-session-identity-prereg.json; census v011-d4a1r3-tw-trajectory-census.json sha256-16 ae954c032022ca79; gates ALL PASS — id-set/event/char/residual recomputation equals A1R2 exactly). TW session-level counts now use recorded-trajectory (row) identity: 15,000 recorded trajectories under 13,053 unique session identifiers (1,947 collided id pairs; 1,946 distinct-content, 1 identical-content; identifier collisions are a labeling property, not run-independence evidence). Per-shape band assignment unchanged under both calibers; 8/13 retained; R-band ratios tighten (core six 0.79–1.28). Event-level, character-level, allocation, and residual ledgers remain A1R2-authoritative. Byte-identical-pair exclusion sensitivity: zero band changes. Affected rows: C03/C04/C05/C13/C14/C15/C16/C17/C19; C41 relations and all other claims unchanged.
