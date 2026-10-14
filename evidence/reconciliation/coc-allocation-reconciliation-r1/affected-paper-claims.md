# Affected Paper A claims

This file is an update candidate list only. R1 does not edit the paper, tables, figures, or supplements.

| Location | Current claim | R1 assessment | Candidate action |
|---|---|---|---|
| Abstract, `paper-draft-v1-icse.md:13` | shipped 0.39%, candidate 90.12%, gap 99.57% of qualified opportunity bytes | Historical proxy, not event-level allocation | Replace COC with OSW event-proxy 0.02% / 95.96% and ratio gap 99.98%; call the unit allocated UTF-8 re-encoded event-payload proxy, not bytes generally |
| Metrics, line 97 | “For each session” observation-character mass is allocated across detected shapes | Describes historical session proxy, inconsistent with event-level method language | Specify per-event payload allocation, UTF-8 re-encoding, event-label divisor, E7/E9/E12 exclusion, and full-fit mapping; disclose no byte spans |
| Metrics, line 97 | Gap ratio “no ratio is recalculated” | Incompatible with a reconciled implementation | Recalculate from the selected authoritative COC pair and version the result |
| RQ5, lines 179–181 | 0.39% / 90.12% / 99.57% | Reproducible only under old whole-trajectory proxy | Supersede with 0.018496% / 95.957692% / 99.980725%, displayed consistently (suggested 0.02% / 95.96% / 99.98%) |
| RQ5, line 183 | Qwen 1.14% / 91.27%; “gap is cross-model stable” | Historical Qwen calculation used session weights, no bytes, and only OpenHands 15K | Same-frame OH15 event proxy is 0.053476% / 96.829525%; full Qwen 35,334 is 0.273375% / 97.673127%. State both scope and method before any cross-model comparison |
| Finding 5, line 185 | 0.39% / 90.12% qualified opportunity bytes | Numerical and construct update required | Use R1 values and allocation-proxy wording; do not imply safe removability |
| Table 5 source, `paper-tables.json:81–87` | OSW 0.0039/0.9012 and Qwen 0.0114/0.9127 | Historical display authority conflicts with R1 method | Version the table; preserve old values as historical proxy provenance, not current event-level result |
| Figure 5 source, `figures.json:43–45` | 0.0039/0.9012, gap 99.57% | Historical session proxy | Regenerate only during later paper integration from R1 summary; do not overwrite in this task |
| Supplement A, line 52 | Says event character allocation but labels COC session-level/OSW-only | Internally mixes two allocation grains | Separate event-shape ledger from historical session proxy; add UTF-8 versus characters and no-span limitation |
| Supplement C, lines 654–661, 899, 1232–1262 | Treats 0.9012 as canonical allocation-based byte result | Canonical only for historical implementation | Add R1 supersession record and link exact method/version; retain frozen snapshots unchanged |

## Values for later integration

| Frame | Shipped | Shipped + candidate | Relative gap | Scope note |
|---|---:|---:|---:|---|
| OSW Minimax 20K primary | 0.0001849571 | 0.9595769206 | 0.9998072514 | Same 20K manifest; event-level UTF-8 allocation proxy |
| Qwen OpenHands 15K | 0.0005347615 | 0.9682952547 | 0.9994477272 | Apples-to-apples scope with historical Qwen artifact |
| Qwen full 35,334 | 0.0027337532 | 0.9767312725 | 0.9972011205 | 15K OpenHands + 20,334 SWE-agent |

SOC is outside the R1 allocation-variable change. Do not mechanically combine these COC candidates with revised detector/SOC results until the detector reconciliation and annotation workstreams are formally integrated.
