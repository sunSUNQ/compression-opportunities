# Historical COC implementation audit

## OSW

`evidence/tools/v011_d4a1_census.py` labels its result byte-deduplicated, but the executed formula is session-grain:

1. Sum every parsed observation's Python code-point length into `ss['obs_chars']`.
2. Detect a set of shapes anywhere in the session.
3. Allocate the entire trajectory observation mass as `obs_chars / len(all_session_shapes)` to each session shape.
4. Exclude E7/E12 shares from the denominator.
5. Count full-fit supported shares in the numerator.

It does not allocate individual events and does not use UTF-8 bytes or byte spans.

## Qwen

`D:\tasco-temp\d3_hf_data\a2_cross_model.py` does not retain observation length for coverage. It assigns each qualified session total unit mass and splits that unit equally across qualified session shapes. Its coverage is therefore shape-weighted session coverage, not byte coverage.

The executable `QFILES` list reads 6 OpenHands shards and 15,000 trajectories. Although the artifact provenance mentions the 20,334 SWE-agent frame, the historical coverage calculation does not include it.

## Mapping drift

Historical coverage excludes only E7/E12 and counts E15 as a candidate full-fit shape. The frozen A0 registry records E9 as `NO_OPPORTUNITY` and E15 as partial-fit. R1's primary mapping therefore excludes E9 from the qualified denominator and E15 from the full-fit numerator. A legacy-mapping event-level sensitivity is provided to isolate this mapping effect; its numerical impact is negligible relative to the allocation-grain change.

## Terminology consequence

The historical values can be reproduced but cannot substantiate the paper's claimed event-level overlap allocation. R1 retains them as traceable legacy proxies and does not alter their frozen artifacts.
