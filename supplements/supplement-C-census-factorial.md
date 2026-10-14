# Supplement C — Full census and factorial results

Evidence freeze: 2026-09-24. Cleanup checkpoint: `057477902627f0007aad42dcc853c7b6d52698e2`. All numerical tables are transcriptions of frozen fields; no experiment, aggregation, significance test, or detector is run during preparation. Original fractions are retained without calculating additional statistics.

> **AMENDMENT (V0.11-D4-A1R2 klear recovery, 2026-10-09; PAPER-A-NUMBERS-UPDATE 2026-10-10):** the discovery-side census blocks below are transcriptions of the **pre-amendment frame** (old two-source parse; klear sessions contributed zero events). Display authority for TW discovery incidence and cross-corpus replication bands migrated to the A1R2 census in the section *“klear recovery amendment census (D4-A1R2)”* near the end of this supplement. The pre-amendment blocks are retained verbatim below as superseded provenance. OSW-side, model, scaffold, factorial, and coverage blocks are unaffected.

`REPLICATED` denotes the pre-specified descriptive replication criterion; the 0.5–2.0 incidence-ratio band is not a statistical equivalence interval. Scaffold contrasts are within-frame scaffold-associated differences. Session rows are observations, not independent tasks. Final cross-model/frame authority is the full-factorial artifact; acquisition snapshots and empty intermediate cells are not final evidence.

## Discovery census

> **SUPERSEDED-FOR-DISPLAY (pre-amendment frame):** the transcription below is the D3-E1 discovery census under the old two-source parse. For current display authority see the A1R2 amendment census section at the end of this supplement.

[evidence/V1/v011-d3e1-external-census.json](sources/evidence/V1/v011-d3e1-external-census.json) — field: `root`

```json
{
  "schema_version": 1,
  "stage": "V0.11-D3-E1 external dataset opportunity census (prereg 55494bce FROZEN before aggregation)",
  "date": "2026-09-23",
  "dataset": {
    "name": "thoughtworks/agentic-coding-trajectories",
    "sessions": 15000,
    "pin": "[local dataset pin omitted in review copy]",
    "bytes": 325563194
  },
  "context_proxy": {
    "whole_session_context_chars_sum": 1134133251,
    "mean_obs_chars_per_session": 75608.9
  },
  "shapes": {
    "E10_repeated_validation": {
      "sessions": 17,
      "session_incidence": 0.0011,
      "events": 58,
      "median_chars": 8440,
      "p75_chars": 15846,
      "median_tokens_est": 2110,
      "median_turn_index": 0.608,
      "median_turns_after": 28,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 2,
      "later_reread_rate": null,
      "success_session_rate": 0.471,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 4,
        "nebius-swe-rebench-openhands": 54
      }
    },
    "E11_unchanged_validation": {
      "sessions": 8,
      "session_incidence": 0.0005,
      "events": 24,
      "median_chars": 5946,
      "p75_chars": 9726,
      "median_tokens_est": 1486.5,
      "median_turn_index": 0.635,
      "median_turns_after": 18,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.5,
      "potential_compressible_chars_median": 4943,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 2,
        "nebius-swe-rebench-openhands": 22
      }
    },
    "E12_large_diagnostic": {
      "sessions": 9017,
      "session_incidence": 0.6011,
      "events": 30962,
      "median_chars": 8049.5,
      "p75_chars": 15620,
      "median_tokens_est": 2012.4,
      "median_turn_index": 0.344,
      "median_turns_after": 24,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.462,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 12728,
        "nebius-swe-rebench-openhands": 18234
      }
    },
    "E13_large_output_near_terminal": {
      "sessions": 7988,
      "session_incidence": 0.5325,
      "events": 11363,
      "median_chars": 5780,
      "p75_chars": 10285,
      "median_tokens_est": 1445,
      "median_turn_index": 0.988,
      "median_turns_after": 1,
      "trajectory_exposure": "LOW",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.465,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 6251,
        "nebius-swe-rebench-openhands": 5112
      }
    },
    "E14_output_followed_by_reread": {
      "sessions": 9230,
      "session_incidence": 0.6153,
      "events": 69122,
      "median_chars": 1193,
      "p75_chars": 2066,
      "median_tokens_est": 298.2,
      "median_turn_index": 0.45,
      "median_turns_after": 25,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.449,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 40903,
        "nebius-swe-rebench-openhands": 28219
      }
    },
    "E15_output_followed_by_rederivation": {
      "sessions": 7,
      "session_incidence": 0.0005,
      "events": 8,
      "median_chars": 10808.5,
      "p75_chars": 30047,
      "median_tokens_est": 2702.1,
      "median_turn_index": 0.207,
      "median_turns_after": 32,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.571,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 1,
        "nebius-swe-rebench-openhands": 7
      }
    },
    "E1_repeated_exact_command": {
      "sessions": 9872,
      "session_incidence": 0.6581,
      "events": 233334,
      "median_chars": 987,
      "p75_chars": 2018,
      "median_tokens_est": 246.8,
      "median_turn_index": 0.536,
      "median_turns_after": 26,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 8,
      "later_reread_rate": null,
      "success_session_rate": 0.463,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 48387,
        "nebius-swe-rebench-openhands": 184947
      }
    },
    "E2_repeated_similar_command": {
      "sessions": 9940,
      "session_incidence": 0.6627,
      "events": 257483,
      "median_chars": 1016,
      "p75_chars": 2064,
      "median_tokens_est": 254,
      "median_turn_index": 0.52,
      "median_turns_after": 26,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 7,
      "later_reread_rate": null,
      "success_session_rate": 0.462,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 71098,
        "nebius-swe-rebench-openhands": 186385
      }
    },
    "E3_same_file_reread": {
      "sessions": 9976,
      "session_incidence": 0.6651,
      "events": 149152,
      "median_chars": 1245,
      "p75_chars": 2280,
      "median_tokens_est": 311.2,
      "median_turn_index": 0.484,
      "median_turns_after": 25,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 7,
      "later_reread_rate": null,
      "success_session_rate": 0.462,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 68037,
        "nebius-swe-rebench-openhands": 81115
      }
    },
    "E4_overlapping_file_read": {
      "sessions": 4157,
      "session_incidence": 0.2771,
      "events": 37104,
      "median_chars": 1296,
      "p75_chars": 2278,
      "median_tokens_est": 324,
      "median_turn_index": 0.381,
      "median_turns_after": 39,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.463,
      "potential_compressible_chars_median": null,
      "by_source": {
        "nebius-swe-rebench-openhands": 37104
      }
    },
    "E5_same_search": {
      "sessions": 70,
      "session_incidence": 0.0047,
      "events": 213,
      "median_chars": 328,
      "p75_chars": 1250,
      "median_tokens_est": 82,
      "median_turn_index": 0.525,
      "median_turns_after": 27,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 2,
      "later_reread_rate": null,
      "success_session_rate": 0.243,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 195,
        "nebius-swe-rebench-openhands": 18
      }
    },
    "E6_large_test_success": {
      "sessions": 59,
      "session_incidence": 0.0039,
      "events": 105,
      "median_chars": 10425,
      "p75_chars": 21889,
      "median_tokens_est": 2606.2,
      "median_turn_index": 0.302,
      "median_turns_after": 32,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.508,
      "potential_compressible_chars_median": null,
      "by_source": {
        "nebius-swe-rebench-openhands": 105
      }
    },
    "E7_large_test_failure": {
      "sessions": 30,
      "session_incidence": 0.002,
      "events": 45,
      "median_chars": 14144,
      "p75_chars": 30047,
      "median_tokens_est": 3536,
      "median_turn_index": 0.2,
      "median_turns_after": 38,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.433,
      "potential_compressible_chars_median": null,
      "by_source": {
        "nebius-swe-rebench-openhands": 45
      }
    },
    "E9_large_build_output": {
      "sessions": 1,
      "session_incidence": 0.0001,
      "events": 1,
      "median_chars": 4398,
      "p75_chars": 4398,
      "median_tokens_est": 1099.5,
      "median_turn_index": 0.333,
      "median_turns_after": 64,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 1,
      "potential_compressible_chars_median": null,
      "by_source": {
        "nebius-swe-rebench-openhands": 1
      }
    }
  },
  "pool_gates": {
    "min_incidence": 0.2,
    "min_median_chars": 1000
  },
  "candidate_pool": [
    "E3_same_file_reread",
    "E2_repeated_similar_command",
    "E14_output_followed_by_reread",
    "E12_large_diagnostic",
    "E13_large_output_near_terminal",
    "E4_overlapping_file_read"
  ],
  "top3": [
    {
      "shape": "E3_same_file_reread",
      "session_incidence": 0.6651,
      "events": 149152,
      "median_chars": 1245,
      "p75_chars": 2280,
      "median_turns_after": 25,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 7,
      "success_session_rate": 0.462,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 68037,
        "nebius-swe-rebench-openhands": 81115
      }
    },
    {
      "shape": "E2_repeated_similar_command",
      "session_incidence": 0.6627,
      "events": 257483,
      "median_chars": 1016,
      "p75_chars": 2064,
      "median_turns_after": 26,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 7,
      "success_session_rate": 0.462,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 71098,
        "nebius-swe-rebench-openhands": 186385
      }
    },
    {
      "shape": "E14_output_followed_by_reread",
      "session_incidence": 0.6153,
      "events": 69122,
      "median_chars": 1193,
      "p75_chars": 2066,
      "median_turns_after": 25,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "success_session_rate": 0.449,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 40903,
        "nebius-swe-rebench-openhands": 28219
      }
    }
  ],
  "special_directions": {
    "E10_repeated_validation": {
      "sessions": 17,
      "session_incidence": 0.0011,
      "events": 58,
      "median_chars": 8440,
      "p75_chars": 15846,
      "median_tokens_est": 2110,
      "median_turn_index": 0.608,
      "median_turns_after": 28,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 2,
      "later_reread_rate": null,
      "success_session_rate": 0.471,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 4,
        "nebius-swe-rebench-openhands": 54
      }
    },
    "E11_unchanged_validation": {
      "sessions": 8,
      "session_incidence": 0.0005,
      "events": 24,
      "median_chars": 5946,
      "p75_chars": 9726,
      "median_tokens_est": 1486.5,
      "median_turn_index": 0.635,
      "median_turns_after": 18,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.5,
      "potential_compressible_chars_median": 4943,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 2,
        "nebius-swe-rebench-openhands": 22
      }
    },
    "E3_same_file_reread": {
      "sessions": 9976,
      "session_incidence": 0.6651,
      "events": 149152,
      "median_chars": 1245,
      "p75_chars": 2280,
      "median_tokens_est": 311.2,
      "median_turn_index": 0.484,
      "median_turns_after": 25,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 7,
      "later_reread_rate": null,
      "success_session_rate": 0.462,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 68037,
        "nebius-swe-rebench-openhands": 81115
      }
    },
    "E4_overlapping_file_read": {
      "sessions": 4157,
      "session_incidence": 0.2771,
      "events": 37104,
      "median_chars": 1296,
      "p75_chars": 2278,
      "median_tokens_est": 324,
      "median_turn_index": 0.381,
      "median_turns_after": 39,
      "trajectory_exposure": "HIGH",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.463,
      "potential_compressible_chars_median": null,
      "by_source": {
        "nebius-swe-rebench-openhands": 37104
      }
    },
    "E13_large_output_near_terminal": {
      "sessions": 7988,
      "session_incidence": 0.5325,
      "events": 11363,
      "median_chars": 5780,
      "p75_chars": 10285,
      "median_tokens_est": 1445,
      "median_turn_index": 0.988,
      "median_turns_after": 1,
      "trajectory_exposure": "LOW",
      "repeat_rate": 1,
      "later_reread_rate": null,
      "success_session_rate": 0.465,
      "potential_compressible_chars_median": null,
      "by_source": {
        "swe-smith-claude-3-7-sonnet": 6251,
        "nebius-swe-rebench-openhands": 5112
      }
    }
  },
  "verdict": "PASS — NATURAL_OPPORTUNITY_FOUND"
}
```

## External census, all shapes and reported strata

[evidence/V1/v011-d4a1-census-results.json](sources/evidence/V1/v011-d4a1-census-results.json) — field: `root`

```json
{
  "schema_version": 1,
  "stage": "V0.11-D4-A1 census — frozen-detector external validation (prereg d229a6a4 + amendment 76547f34; A0 freeze 1865a160)",
  "date": "2026-09-24",
  "provenance": {
    "manifest": "v011-d4a1-oswe-20k-manifest-v2.json",
    "manifest_sample_id_set_sha256": "601318a78fc86c84",
    "manifest_note": "file-level manifest_sha256 895a96c0 predates SUPERSEDED bookkeeping append on old manifest; v2 sample array verified 20000/20000 unique",
    "detector_freeze_commit": "1865a160 (A0 registry)",
    "dataset": "nvidia/Open-SWE-Traces v1.0 HF revision f8fb5b3d2c78 (Minimax-M2.5, OH+SA strata)"
  },
  "census_integrity": {
    "sessions_expected": 20000,
    "sessions_censused": 20000,
    "complete": true
  },
  "shape_results": {
    "E1_repeated_exact_command": {
      "measurable": true,
      "event_sessions": 19992,
      "session_incidence": 0.9996,
      "median_event_chars": 54827.5,
      "p75_event_chars": 82831,
      "thoughtworks_incidence": 0.6581,
      "replication_band": "REPLICATED",
      "abcde_class": "A"
    },
    "E2_repeated_similar_command": {
      "measurable": true,
      "event_sessions": 19995,
      "session_incidence": 0.9998,
      "median_event_chars": 58233,
      "p75_event_chars": 87304,
      "thoughtworks_incidence": 0.6627,
      "replication_band": "REPLICATED",
      "abcde_class": "A"
    },
    "E3_same_file_reread": {
      "measurable": true,
      "event_sessions": 19997,
      "session_incidence": 0.9999,
      "median_event_chars": 41806,
      "p75_event_chars": 62686,
      "thoughtworks_incidence": 0.6651,
      "replication_band": "REPLICATED",
      "abcde_class": "A"
    },
    "E4_overlapping_file_read": {
      "measurable": true,
      "event_sessions": 0,
      "session_incidence": 0,
      "median_event_chars": null,
      "p75_event_chars": null,
      "thoughtworks_incidence": 0.2771,
      "replication_band": "DATASET_SPECIFIC",
      "abcde_class": "A"
    },
    "E5_same_search": {
      "measurable": true,
      "event_sessions": 398,
      "session_incidence": 0.0199,
      "median_event_chars": 598,
      "p75_event_chars": 1382,
      "thoughtworks_incidence": 0.0047,
      "replication_band": "PARTIAL_REPLICATION",
      "abcde_class": "D"
    },
    "E6_large_test_success": {
      "measurable": true,
      "event_sessions": 15,
      "session_incidence": 0.0008,
      "median_event_chars": 6954,
      "p75_event_chars": 19706,
      "thoughtworks_incidence": 0.0039,
      "replication_band": "DATASET_SPECIFIC",
      "abcde_class": "D"
    },
    "E7_large_test_failure": {
      "measurable": true,
      "event_sessions": 13,
      "session_incidence": 0.0006,
      "median_event_chars": 7379,
      "p75_event_chars": 11182,
      "thoughtworks_incidence": 0.002,
      "replication_band": "PARTIAL_REPLICATION",
      "abcde_class": "C"
    },
    "E8_large_lint_output": {
      "measurable": true,
      "event_sessions": 0,
      "session_incidence": 0,
      "median_event_chars": null,
      "p75_event_chars": null,
      "thoughtworks_incidence": null,
      "replication_band": "NOT_MEASURABLE",
      "abcde_class": "A"
    },
    "E9_large_build_output": {
      "measurable": true,
      "event_sessions": 1,
      "session_incidence": 0.0001,
      "median_event_chars": 5496,
      "p75_event_chars": 5496,
      "thoughtworks_incidence": 0.0001,
      "replication_band": "REPLICATED",
      "abcde_class": "E"
    },
    "E10_repeated_validation": {
      "measurable": true,
      "event_sessions": 16,
      "session_incidence": 0.0008,
      "median_event_chars": 4579,
      "p75_event_chars": 10873,
      "thoughtworks_incidence": 0.0011,
      "replication_band": "REPLICATED",
      "abcde_class": "D"
    },
    "E11_unchanged_validation": {
      "measurable": true,
      "event_sessions": 8,
      "session_incidence": 0.0004,
      "median_event_chars": 2397.5,
      "p75_event_chars": 3477,
      "thoughtworks_incidence": 0.0005,
      "replication_band": "REPLICATED",
      "abcde_class": "D"
    },
    "E12_large_diagnostic": {
      "measurable": true,
      "event_sessions": 15900,
      "session_incidence": 0.795,
      "median_event_chars": 29889.5,
      "p75_event_chars": 50534,
      "thoughtworks_incidence": 0.6011,
      "replication_band": "REPLICATED",
      "abcde_class": "C"
    },
    "E13_large_output_near_terminal": {
      "measurable": true,
      "event_sessions": 9327,
      "session_incidence": 0.4663,
      "median_event_chars": 4764,
      "p75_event_chars": 8951,
      "thoughtworks_incidence": 0.5325,
      "replication_band": "REPLICATED",
      "abcde_class": "B"
    },
    "E14_output_followed_by_reread": {
      "measurable": true,
      "event_sessions": 18967,
      "session_incidence": 0.9484,
      "median_event_chars": 11345,
      "p75_event_chars": 21975,
      "thoughtworks_incidence": 0.6153,
      "replication_band": "REPLICATED",
      "abcde_class": "A"
    },
    "E15_output_followed_by_rederivation": {
      "measurable": true,
      "event_sessions": 7,
      "session_incidence": 0.0003,
      "median_event_chars": 1324,
      "p75_event_chars": 2919,
      "thoughtworks_incidence": 0.0005,
      "replication_band": "REPLICATED",
      "abcde_class": "D"
    }
  },
  "abcde_session_distribution": {
    "A": {
      "sessions": 20000,
      "session_share": 1
    },
    "B": {
      "sessions": 9327,
      "session_share": 0.4663
    },
    "C": {
      "sessions": 15900,
      "session_share": 0.795
    },
    "D": {
      "sessions": 418,
      "session_share": 0.0209
    },
    "E": {
      "sessions": 1,
      "session_share": 0.0001
    }
  },
  "coverage": {
    "shipped_only": {
      "SOC": 0.0207,
      "COC": 0.0039
    },
    "shipped_plus_candidate": {
      "SOC": 1,
      "COC": 0.9012
    },
    "capability_gap_rate": 0.9957,
    "definition_note": "COC byte numerator counts full-fit capability shape sessions (conservative; partial-fit not counted); unsafe shapes (E7/E12) excluded from qualified denominator"
  },
  "stratification": {
    "openhands": {
      "sessions": 10000,
      "incidence": {
        "E10": 0.0005,
        "E11": 0.0001,
        "E12": 0.7715,
        "E13": 0.6487,
        "E14": 0.9388,
        "E15": 0.0001,
        "E1": 0.9993,
        "E2": 0.9995,
        "E3": 0.9997,
        "E5": 0.0266,
        "E6": 0.0008,
        "E7": 0.0006
      }
    },
    "sweagent": {
      "sessions": 10000,
      "incidence": {
        "E10": 0.0011,
        "E11": 0.0007,
        "E12": 0.8185,
        "E13": 0.284,
        "E14": 0.9579,
        "E15": 0.0006,
        "E1": 0.9999,
        "E2": 1,
        "E3": 1,
        "E5": 0.0132,
        "E6": 0.0007,
        "E7": 0.0007,
        "E9": 0.0001
      }
    },
    "languages_by_sessions": {
      "python": 11861,
      "typescript": 8438,
      "go": 8426,
      "javascript": 6547,
      "rust": 4708,
      "java": 3184,
      "php": 2287,
      "c": 132,
      "cpp": 63
    },
    "resolved_by_sessions": {
      "0": {
        "A": 8534,
        "C": 6816,
        "B": 4244,
        "D": 187
      },
      "1": {
        "A": 6911,
        "B": 3197,
        "C": 5544,
        "D": 130,
        "E": 1
      },
      "-1": {
        "A": 4555,
        "B": 1886,
        "C": 3540,
        "D": 101
      }
    },
    "language_class_breakdown": {
      "python": {
        "A": 4739,
        "B": 2672,
        "C": 4350,
        "D": 100
      },
      "typescript": {
        "A": 3651,
        "B": 1661,
        "C": 3057,
        "D": 69
      },
      "go": {
        "A": 4215,
        "B": 1861,
        "C": 2275,
        "D": 75
      },
      "javascript": {
        "A": 2943,
        "B": 1213,
        "C": 2325,
        "D": 66
      },
      "rust": {
        "A": 2054,
        "B": 905,
        "C": 1728,
        "D": 21
      },
      "java": {
        "A": 1281,
        "C": 1212,
        "B": 625,
        "D": 65,
        "E": 1
      },
      "php": {
        "A": 1019,
        "C": 904,
        "B": 347,
        "D": 17
      },
      "c": {
        "A": 70,
        "D": 3,
        "C": 28,
        "B": 31
      },
      "cpp": {
        "A": 28,
        "C": 21,
        "B": 12,
        "D": 2
      }
    }
  },
  "scaffold_comparison_note": "compare oh/sa shape_incidence: persistent if both >0.5x overall; scaffold-sensitive if ratio >2x; near-absent if <0.1",
  "final_status": "EXTERNAL_VALIDATION_COMPLETE",
  "aggregates_sha256": "59d42edee1de76618f3427f4764ecc90bd12de34f47664d6fc7be3a790e7643c",
  "analyzer_fix_note": "abcde_session_distribution and stratum shape_incidence recomputed via verified mini-census logic after main-run implementation anomaly (per-session classes were dropped in first run); shape_results/coverage untouched"
}
```

## Final scaffold × model factorial

[evidence/V1/v011-d4a2r1-full-factorial.json](sources/evidence/V1/v011-d4a2r1-full-factorial.json) — field: `root`

```json
{
  "schema_version": 1,
  "stage": "V0.11-D4-A2R1 SAxQwen cross-cell closure — full factorial model x scaffold (prereg A2 frozen; detectors unchanged)",
  "date": "2026-09-24",
  "provenance": {
    "detector_freeze_commit": "1865a160",
    "dataset": "nvidia/Open-SWE-Traces v1.0 rev f8fb5b3d2c78",
    "sa_qwen_frame": "9/9 shards FULL (20334 trajectories), transactional recovery (never delete valid finals)"
  },
  "sa_qwen_sessions": 20334,
  "sa_qwen_incidence": {
    "E10": 0,
    "E11": 0,
    "E12": 0.8292,
    "E13": 0.2392,
    "E14": 0.9705,
    "E15": 0.0001,
    "E1": 1,
    "E2": 1,
    "E3": 0.9991,
    "E5": 0.3232,
    "E8": 0,
    "E9": 0.0001
  },
  "e13_full_factorial_2x2": {
    "incidence": {
      "OH_x_Minimax": 0.6487,
      "SA_x_Minimax": 0.284,
      "OH_x_Qwen": 0.4389,
      "SA_x_Qwen": 0.2392
    },
    "contrasts": {
      "scaffold_within_minimax": {
        "pp_diff": -0.3647,
        "ratio": 0.438
      },
      "scaffold_within_qwen": {
        "pp_diff": -0.1997,
        "ratio": 0.545
      },
      "model_within_openhands": {
        "pp_diff": -0.2098,
        "ratio": 0.677
      },
      "model_within_sweagent": {
        "pp_diff": -0.0448,
        "ratio": 0.842
      }
    },
    "scaffold_effect_consistent_across_models": true,
    "reading": "scaffold contrast direction consistent across models (Minimax -0.365, Qwen -0.200 pp; |effect| 0.365 vs 0.200); model contrast within SA +-0.045 pp"
  },
  "core_shape_model_contrast_on_SA": {
    "E1": {
      "minimax": 0.9999,
      "qwen": 1,
      "ratio": 1,
      "verdict": "MODEL_STABLE"
    },
    "E2": {
      "minimax": 1,
      "qwen": 1,
      "ratio": 1,
      "verdict": "MODEL_STABLE"
    },
    "E3": {
      "minimax": 1,
      "qwen": 0.9991,
      "ratio": 0.999,
      "verdict": "MODEL_STABLE"
    },
    "E12": {
      "minimax": 0.8185,
      "qwen": 0.8292,
      "ratio": 1.013,
      "verdict": "MODEL_STABLE"
    },
    "E13": {
      "minimax": 0.284,
      "qwen": 0.2392,
      "ratio": 0.842,
      "verdict": "MODEL_STABLE"
    },
    "E14": {
      "minimax": 0.9579,
      "qwen": 0.9705,
      "ratio": 1.013,
      "verdict": "MODEL_STABLE"
    }
  },
  "full_factorial_status": "COMPLETE (2x2 all four cells observed; OH/SA x Minimax/Qwen)",
  "verdict": "FULL_FACTORIAL_VALIDATION_COMPLETE",
  "aggregates_sha256": "3168804e0c8e69097deaf728f4dc2b407228040bf4fd97c82d0877f263f6d3ce"
}
```

## Historical frozen publication tables

For candidate Minimax COC, the historical 0.9013 paper-table entry is superseded as a display authority by census field 0.9012, displayed consistently as 90.12%. Legacy safety and power terminology in the raw JSON is provenance, not adopted terminology.

## Frozen publication tables

[evidence/V1/paper/paper-tables.json](sources/evidence/V1/paper/paper-tables.json) — field: `root`

```json
{
  "schema_version": 1,
  "freeze": "D4-P0 paper evidence freeze (74b3b6a7 lineage; all numbers from frozen artifacts, no recomputation)",
  "frozen_at": "2026-09-24",
  "tables": {
    "T1_opportunity_taxonomy_census": {
      "caption": "Compression opportunity shapes E1-E15: incidence, payload, exposure, mechanical compressibility across two corpora",
      "columns": [
        "shape",
        "TW15K_incidence",
        "OSW20K_incidence",
        "TW_median_chars",
        "TW_p75_chars",
        "exposure",
        "replication_band"
      ],
      "rows": [
        [
          "E1_repeated_exact_command",
          0.6581,
          0.9996,
          987,
          2018,
          "HIGH",
          "REPLICATED*"
        ],
        [
          "E2_repeated_similar_command",
          0.6627,
          0.9998,
          1016,
          2064,
          "HIGH",
          "REPLICATED*"
        ],
        [
          "E3_same_file_reread",
          0.6651,
          0.9999,
          1245,
          2280,
          "HIGH",
          "REPLICATED*"
        ],
        [
          "E4_overlapping_file_read",
          0.2771,
          "NOT_MEASURABLE",
          1296,
          2278,
          "HIGH",
          "NOT_MEASURABLE"
        ],
        [
          "E5_same_search",
          0.0047,
          0.0199,
          328,
          1250,
          "HIGH",
          "PARTIAL_REPLICATION"
        ],
        [
          "E6_large_test_success",
          0.0039,
          0.0008,
          10425,
          21889,
          "HIGH",
          "DATASET_SPECIFIC"
        ],
        [
          "E7_large_test_failure",
          0.002,
          0.0006,
          14144,
          30047,
          "HIGH",
          "PARTIAL_REPLICATION"
        ],
        [
          "E8_large_lint_output",
          null,
          0,
          null,
          null,
          "HIGH",
          "NOT_MEASURABLE"
        ],
        [
          "E9_large_build_output",
          0.0001,
          0.0001,
          4398,
          4398,
          "HIGH",
          "REPLICATED"
        ],
        [
          "E10_repeated_validation",
          0.0011,
          0.0008,
          8440,
          15846,
          "HIGH",
          "REPLICATED"
        ],
        [
          "E11_unchanged_validation",
          0.0005,
          0.0004,
          5946,
          9726,
          "HIGH",
          "REPLICATED"
        ],
        [
          "E12_large_diagnostic",
          0.6011,
          0.795,
          8049,
          15620,
          "HIGH",
          "REPLICATED"
        ],
        [
          "E13_large_output_near_terminal",
          0.5325,
          0.4663,
          5780,
          10285,
          "LOW",
          "REPLICATED"
        ],
        [
          "E14_output_followed_by_reread",
          0.6153,
          0.9484,
          1193,
          2066,
          "HIGH",
          "REPLICATED"
        ],
        [
          "E15_output_followed_by_rederivation",
          0.0005,
          0.0003,
          10808,
          30047,
          "HIGH",
          "REPLICATED"
        ]
      ],
      "note": "* E1/E2/E3/E14 OSW values use path-aware command normalization; TW values retain the original detector caliber (see limitations L6). Cross-corpus ratios are descriptive under this documented caliber difference and are not same-caliber estimates. E4 NOT_MEASURABLE in OSW (no range field) — not a negative result.",
      "sources": [
        "v011-d3e1-external-census.json",
        "v011-d4a1-census-results.json"
      ]
    },
    "T2_ae_class_distribution": {
      "caption": "A-E opportunity class distribution (session-level union), Thoughtworks vs Open-SWE",
      "columns": [
        "class",
        "TW15K_sessions",
        "TW15K_share",
        "OSW20K_sessions",
        "OSW20K_share"
      ],
      "rows": [
        [
          "A existing/candidate-covered",
          null,
          null,
          20000,
          1
        ],
        [
          "B semantic gap (E13)",
          null,
          0.4663,
          9327,
          0.4663
        ],
        [
          "C unsafe/high-exposure (E12+E7)",
          null,
          0.795,
          15900,
          0.795
        ],
        [
          "D low-value",
          null,
          0.0209,
          418,
          0.0209
        ],
        [
          "E no meaningful opportunity",
          null,
          0.0001,
          1,
          0.0001
        ]
      ],
      "note": "TW per-session class union not computed in D3-E1 (shape-level only); OSW full union computed. TW A-row left null (not back-filled post hoc).",
      "sources": [
        "v011-d4a1-census-results.json"
      ]
    },
    "T3_e13_full_factorial_2x2": {
      "caption": "E13 late-trajectory large-output incidence: model x scaffold full factorial",
      "columns": [
        "cell",
        "incidence"
      ],
      "rows": [
        [
          "OpenHands x Minimax",
          0.6487
        ],
        [
          "SWE-agent x Minimax",
          0.284
        ],
        [
          "OpenHands x Qwen3.5",
          0.4389
        ],
        [
          "SWE-agent x Qwen3.5",
          0.2392
        ]
      ],
      "contrasts_pp": {
        "scaffold_within_minimax": -0.3647,
        "scaffold_within_qwen": -0.1997,
        "model_within_openhands": -0.2098,
        "model_within_sweagent": -0.0448,
        "average_scaffold_contrast_abs_pp": 0.2822,
        "average_model_contrast_abs_pp": 0.1273,
        "difference_in_differences_interaction_pp": 0.165
      },
      "reading": "scaffold-associated variation (mean 28.2pp) > model-associated variation (mean 12.7pp); interaction 16.5pp — model modulates scaffold-effect magnitude without changing direction",
      "sources": [
        "v011-d4a2r1-full-factorial.json"
      ]
    },
    "T4_core_shape_model_stability": {
      "caption": "Core shapes: model contrast within each scaffold (A2 + A2R1)",
      "columns": [
        "shape",
        "OH_MM",
        "OH_QW",
        "OH_verdict",
        "SA_MM",
        "SA_QW",
        "SA_verdict"
      ],
      "rows": [
        [
          "E1_repeated_exact_command",
          0.9993,
          1,
          "MODEL_STABLE",
          0.9999,
          1,
          "MODEL_STABLE"
        ],
        [
          "E2_repeated_similar_command",
          0.9995,
          1,
          "MODEL_STABLE",
          1,
          1,
          "MODEL_STABLE"
        ],
        [
          "E3_same_file_reread",
          0.9997,
          1,
          "MODEL_STABLE",
          1,
          0.9991,
          "MODEL_STABLE"
        ],
        [
          "E12_large_diagnostic",
          0.7715,
          0.7417,
          "MODEL_STABLE",
          0.8185,
          0.8292,
          "MODEL_STABLE"
        ],
        [
          "E13_large_output_near_terminal",
          0.6487,
          0.4389,
          "MODEL_STABLE",
          0.284,
          0.2392,
          "MODEL_STABLE"
        ],
        [
          "E14_output_followed_by_reread",
          0.9388,
          0.9833,
          "MODEL_STABLE",
          0.9579,
          0.9705,
          "MODEL_STABLE"
        ]
      ],
      "sources": [
        "v011-d4a1-census-results.json",
        "v011-d4a2-cross-model.json",
        "v011-d4a2r1-full-factorial.json"
      ]
    },
    "T5_capability_coverage_dual_ledger": {
      "caption": "Capability coverage: production (shipped-only) vs research (shipped+RDS candidate), Minimax OH+SA 20K",
      "columns": [
        "ledger",
        "SOC",
        "COC",
        "note"
      ],
      "rows": [
        [
          "production_shipped_only",
          0.0207,
          0.0039,
          "shipped capabilities near-zero coverage of natural repeated-delivery opportunities"
        ],
        [
          "research_shipped_plus_candidate",
          1,
          0.9013,
          "RDS candidate fills ~90% of qualified-opportunity bytes"
        ],
        [
          "capability_gap_rate",
          null,
          0.9957,
          "qualified bytes without supported primitive / all qualified bytes"
        ]
      ],
      "qwen_cross_check": {
        "shipped_only": {
          "SOC": 0.0612,
          "COC_shape_weighted": 0.0114
        },
        "shipped_plus_candidate": {
          "SOC": 1,
          "COC_shape_weighted": 0.9127
        }
      },
      "sources": [
        "v011-d4a1-census-results.json",
        "v011-d4a2-cross-model.json"
      ]
    },
    "T6_online_qualification_feasibility": {
      "caption": "Why offline compressibility did not translate to online task-token qualification (C1/D2/D5/E7)",
      "rows": [
        {
          "experiment": "D3-E7 power design",
          "within_arm_noise_median_abs_relative": 0.2796,
          "bt_pair_delta_median_abs": 0.2379,
          "mechanism_exposure_median": 0.00011,
          "signal_to_noise": 0.0003,
          "power_3pct_best": 0.622,
          "power_5pct_best": 0.699,
          "power_10pct_best": 0.856,
          "permutation_p_observed_7_38pct": 0.1185
        },
        {
          "experiment": "D3-E5 RDS A/B",
          "pairs": 24,
          "oracle_pass": "24/24",
          "aggregate_relative_saving": 0.0738,
          "nonneg_pairs": "13/24",
          "g2": "FAIL"
        },
        {
          "experiment": "V0.11-D2 terminal-state",
          "pairs": 18,
          "opportunity_incidence": 0,
          "aggregate": -0.0805,
          "verdict": "NOT_QUALIFIED"
        }
      ],
      "reading": "within-task stochastic trajectory variance (median 27.96%) exceeds both B/T pair deltas (23.79%) and any hundred-token-scale mechanism exposure (0.011%) — online task-token qualification of such mechanisms is not cost-justifiable at practical sample sizes"
    }
  }
}
```

Absent stratifications are NOT_REPORTED; no new resolved/language cross-tabulations are calculated. Source-specific rounds and exclusions remain attached to each artifact.

## Same-caliber recalculation (D4-A1R1, E1/E2/E3/E14)

Prereg v011-d4a1r1-prereg.json (FROZEN before first aggregate). Motivation: the external (Open-SWE) census applies path-aware command normalization (tool path appended to view/open/edit command strings before cnorm/csim grouping) while the discovery (TW) census originally did not. This recalculation re-runs the A0-frozen E1/E2/E3/E14 detector rules, verbatim from v011_d4a1_census.py (A0 freeze 1865a160), on all 15,000 TW discovery sessions with that single normalization variable applied; the TW schema adapter (tool_calls_json loader, code-fence fallback, user-role OBSERVATION capture, from v011_d3e3_repeat_class_census.py) is a per-corpus property and not part of the caliber under test. Session incidence only; no removable-char ledger is recomputed.

[evidence/V1/v011-d4a1r1-tw-same-caliber.json](sources/evidence/V1/v011-d4a1r1-tw-same-caliber.json) — field: root

`json
{
 "schema_version": 1,
 "stage": "V0.11-D4-A1R1 Thoughtworks same-caliber recalculation E1/E2/E3/E14 (prereg 8303a572 FROZEN before first aggregate)",
 "date": "2026-10-09",
 "provenance": {
  "detector_source": "evidence/tools/v011_d4a1_census.py (A0 freeze 1865a160), rules verbatim",
  "schema_adapter_source": "evidence/tools/v011_d3e3_repeat_class_census.py loader (TW schema; user-observation fallback; code-fence fallback)",
  "single_variable": "path-aware command normalization (d4a1 rule applied to TW loader)",
  "input_pin": "D:/tasco-temp/d3_hf_data/sessions.parquet",
  "input_bytes": 325563194,
  "denominator": "all corpus rows (matches D3-E1 accounting)"
 },
 "census_integrity": {
  "sessions_expected": 15000,
  "sessions_censused": 15000,
  "complete": true
 },
 "shapes": {
  "E1_repeated_exact_command": {
   "sessions_with_shape": 9892,
   "tw_same_caliber_incidence": 0.6595,
   "tw_original_caliber_incidence": 0.6581,
   "caliber_shift_pp": 0.14,
   "osw_incidence": 0.9996,
   "band_osw_vs_tw_original": "REPLICATED",
   "band_osw_vs_tw_same_caliber": "REPLICATED",
   "ratio_osw_over_tw_same_caliber": 1.5157
  },
  "E2_repeated_similar_command": {
   "sessions_with_shape": 9952,
   "tw_same_caliber_incidence": 0.6635,
   "tw_original_caliber_incidence": 0.6627,
   "caliber_shift_pp": 0.08,
   "osw_incidence": 0.9998,
   "band_osw_vs_tw_original": "REPLICATED",
   "band_osw_vs_tw_same_caliber": "REPLICATED",
   "ratio_osw_over_tw_same_caliber": 1.5069
  },
  "E3_same_file_reread": {
   "sessions_with_shape": 9999,
   "tw_same_caliber_incidence": 0.6666,
   "tw_original_caliber_incidence": 0.6651,
   "caliber_shift_pp": 0.15,
   "osw_incidence": 0.9999,
   "band_osw_vs_tw_original": "REPLICATED",
   "band_osw_vs_tw_same_caliber": "REPLICATED",
   "ratio_osw_over_tw_same_caliber": 1.5
  },
  "E14_output_followed_by_reread": {
   "sessions_with_shape": 9790,
   "tw_same_caliber_incidence": 0.6527,
   "tw_original_caliber_incidence": 0.6153,
   "caliber_shift_pp": 3.74,
   "osw_incidence": 0.9484,
   "band_osw_vs_tw_original": "REPLICATED",
   "band_osw_vs_tw_same_caliber": "REPLICATED",
   "ratio_osw_over_tw_same_caliber": 1.453
  }
 },
 "interpretation_note": "bands use the frozen D4-A1 function; original TW incidences are the D3-E1 authority and remain unchanged",
 "naming_discipline": "session-incidence recalculation only; no removable-char ledger is recomputed",
 "verdict": "TW_SAME_CALIBER_RECALCULATION_COMPLETE",
 "aggregates_sha256": "9050d4a1e69799c950cfe64068feb5829608abe940481d3c52ab306eb55c30c5"
}
`

Reading: the path-aware caliber shifts TW incidence by at most +3.74pp (E14); E1/E2/E3 shift by <=0.15pp. All four OSW/TW replication bands are unchanged (REPLICATED; ratios 1.45–1.52). The TW–OSW incidence gap on these shapes is therefore a corpus property, not a normalization-caliber artifact. Original TW D3-E1 incidences remain the display authority for Fig. 3; this recalculation is a robustness audit, not a replacement census.

> **A1R2 NOTE (display-authority migration):** the sentence “Original TW D3-E1 incidences remain the display authority for Fig. 3” above is **superseded by the A1R2 klear recovery amendment below** — the A1R1 same-caliber shifts (+0.14/+0.08/+0.15/+3.74pp; ratios 1.45–1.52) are historical **pre-amendment-frame** results. Under the recovered full three-source parse the four repetition shapes are REPLICATED with full-precision ratios 1.17/1.16/1.29/1.35. Same-caliber normalization re-validation under the recovered frame remains future work.

## klear recovery amendment census (D4-A1R2)

Prereg [v011-d4a1r2-klear-amendment-prereg.json](sources/evidence/V1/v011-d4a1r2-klear-amendment-prereg.json) (sha256-16 `e98345d748ac7620`, FROZEN before recompute) froze the amendment scope: the TW discovery census parse gains the D3-E4-verified klear observation adapter on the user-role branch (schema-adapter only); E1–E15 predicates, thresholds, grouping semantics, class mappings, candidate gate, registry, and the OSW census are unchanged; the old d3e1 census is not overwritten.

Result [v011-d4a1r2-tw-klear-census.json](sources/evidence/V1/v011-d4a1r2-tw-klear-census.json) — sha256-16 `630dcfaae0bca521` (deterministic replay of the frozen script over the pinned parquet reproduces this file byte-for-byte; see reconciliation report PAPER-A-NUMBERS-UPDATE). The sha256-16 `d9f95a84cb157172` recorded in `v011-d4a1r2-affected-numbers.md` for this file is a stale provenance annotation (erratum); the authoritative hash is `630dcfaae0bca521`.

Gates (from the result file): non-klear 10,000-session regression equals the official d3e1 census per shape exactly (E8 zero-event consistent) and non-klear observation chars equal the official ctx sum 1,134,133,251 — **PASS**; klear parse recovery 5,000/5,000 sessions produce events, 127,985 events = 127,985 returncode-type messages (1:1), exit extracted 127,985 (100%), zero-event sessions = 0 — **verified**. A0 detector changes: none.

[evidence/V1/v011-d4a1r2-tw-klear-census.json](sources/evidence/V1/v011-d4a1r2-tw-klear-census.json) — field: `root` (key-fields snapshot)

```json
{
 "meta": {
  "stage": "V0.11-D4-A1R2 klear recovery discovery census amendment",
  "prereg_sha256_16": "e98345d748ac7620",
  "input_parquet_sha256_16": "3dd8ec3546cf771c",
  "script_sha256_16": "9d599d820038311d",
  "sessions": 15000,
  "events": 578283,
  "adapter": "D3-E4 user-role <returncode>/<output> branch (schema-adapter only)"
 },
 "regression_gate": {"pass": true},
 "klear_verification": {"sessions": 5000, "sessions_with_events": 5000, "events": 127985, "empty_obs_events": 25910, "exit_extracted": 127985, "zero_event_sessions": 0},
 "amended": {
  "per_shape_sessions": {"E1": 12832, "E2": 12945, "E3": 11592, "E4": 4157, "E5": 109, "E6": 293, "E7": 210, "E8": 0, "E9": 1, "E10": 297, "E11": 114, "E12": 10317, "E13": 8688, "E14": 10523, "E15": 116},
  "per_shape_events": {"E1": 269309, "E2": 305739, "E3": 159510, "E4": 29088, "E5": 300, "E6": 396, "E7": 363, "E8": 0, "E9": 1, "E10": 1169, "E11": 329, "E12": 33922, "E13": 12275, "E14": 71081, "E15": 176},
  "session_incidence": {"E1": 0.8555, "E2": 0.863, "E3": 0.7728, "E4": 0.2771, "E5": 0.0073, "E6": 0.0195, "E7": 0.014, "E8": 0.0, "E9": 0.0001, "E10": 0.0198, "E11": 0.0076, "E12": 0.6878, "E13": 0.5792, "E14": 0.7015, "E15": 0.0077},
  "total_obs_chars": 1239474486.0,
  "labeled_chars": 920214271.0,
  "qualified_chars": 703167334.5
 },
 "bands_full_precision": {
  "E1": {"osw_exact": 19992, "tw_old_exact": 9872, "tw_new_exact": 12832, "ratio_old_fullprec": 1.5188, "ratio_new_fullprec": 1.1685, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E2": {"osw_exact": 19995, "tw_old_exact": 9940, "tw_new_exact": 12945, "ratio_old_fullprec": 1.5087, "ratio_new_fullprec": 1.1585, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E3": {"osw_exact": 19997, "tw_old_exact": 9976, "tw_new_exact": 11592, "ratio_old_fullprec": 1.5034, "ratio_new_fullprec": 1.2938, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E4": {"osw_exact": 0, "tw_old_exact": 4157, "tw_new_exact": 4157, "ratio_old_fullprec": null, "ratio_new_fullprec": null, "band_old_fullprec": "MEASURABLE_ONLY", "band_new_fullprec": "MEASURABLE_ONLY", "band_stored_d4a1": "DATASET_SPECIFIC"},
  "E5": {"osw_exact": 398, "tw_old_exact": 70, "tw_new_exact": 109, "ratio_old_fullprec": 4.2643, "ratio_new_fullprec": 2.7385, "band_old_fullprec": "PARTIAL_REPLICATION", "band_new_fullprec": "PARTIAL_REPLICATION", "band_stored_d4a1": "PARTIAL_REPLICATION"},
  "E6": {"osw_exact": 15, "tw_old_exact": 59, "tw_new_exact": 293, "ratio_old_fullprec": 0.1907, "ratio_new_fullprec": 0.0384, "band_old_fullprec": "DATASET_SPECIFIC", "band_new_fullprec": "DATASET_SPECIFIC", "band_stored_d4a1": "DATASET_SPECIFIC"},
  "E7": {"osw_exact": 13, "tw_old_exact": 30, "tw_new_exact": 210, "ratio_old_fullprec": 0.325, "ratio_new_fullprec": 0.0464, "band_old_fullprec": "PARTIAL_REPLICATION", "band_new_fullprec": "DATASET_SPECIFIC", "band_stored_d4a1": "PARTIAL_REPLICATION"},
  "E8": {"osw_exact": 0, "tw_old_exact": 0, "tw_new_exact": 0, "ratio_old_fullprec": null, "ratio_new_fullprec": null, "band_old_fullprec": "NOT_MEASURABLE", "band_new_fullprec": "NOT_MEASURABLE", "band_stored_d4a1": "NOT_MEASURABLE"},
  "E9": {"osw_exact": 1, "tw_old_exact": 1, "tw_new_exact": 1, "ratio_old_fullprec": 0.75, "ratio_new_fullprec": 0.75, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E10": {"osw_exact": 16, "tw_old_exact": 17, "tw_new_exact": 297, "ratio_old_fullprec": 0.7059, "ratio_new_fullprec": 0.0404, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "DATASET_SPECIFIC", "band_stored_d4a1": "REPLICATED"},
  "E11": {"osw_exact": 8, "tw_old_exact": 8, "tw_new_exact": 114, "ratio_old_fullprec": 0.75, "ratio_new_fullprec": 0.0526, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "DATASET_SPECIFIC", "band_stored_d4a1": "REPLICATED"},
  "E12": {"osw_exact": 15900, "tw_old_exact": 9017, "tw_new_exact": 10317, "ratio_old_fullprec": 1.3225, "ratio_new_fullprec": 1.1559, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E13": {"osw_exact": 9327, "tw_old_exact": 7988, "tw_new_exact": 8688, "ratio_old_fullprec": 0.8757, "ratio_new_fullprec": 0.8052, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E14": {"osw_exact": 18967, "tw_old_exact": 9230, "tw_new_exact": 10523, "ratio_old_fullprec": 1.5412, "ratio_new_fullprec": 1.3518, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "REPLICATED", "band_stored_d4a1": "REPLICATED"},
  "E15": {"osw_exact": 7, "tw_old_exact": 7, "tw_new_exact": 116, "ratio_old_fullprec": 0.75, "ratio_new_fullprec": 0.0453, "band_old_fullprec": "REPLICATED", "band_new_fullprec": "DATASET_SPECIFIC", "band_stored_d4a1": "REPLICATED"}
 }
}
```

Reading: under the recovered full three-source parse (denominator 15,000 in both frames), **8 of 13 measurable shapes** satisfy the pre-specified bands — R7 (E1/E2/E3/E9/E12/E13/E14) + P1 (E5) — with NM2 (E4 MEASURABLE_ONLY on OSW schema; E8 NOT_MEASURABLE). All six core shapes (E1/E2/E3/E12/E13/E14) remain REPLICATED and their ratios tighten toward 1.0 (E1 1.52→1.17, E2 1.51→1.16, E3 1.50→1.29, E12 1.32→1.16, E13 0.88→0.81, E14 1.54→1.35). The five sparse shapes (E6, E7, E10, E11, E15) are **DATASET_SPECIFIC**: the recovery multiplied discovery-side validation events (e.g., E10 17→297) while the OSW side stayed sparse (16/13/8/7/15), collapsing the ratios — a corpus-composition effect consistent with the low-incidence-noise limitation; sparse-shape band assignments are corpus-composition-sensitive. E6's full-precision ratio 0.0384 removes the former 0.19/0.205 rounding boundary: E6 is unambiguously DATASET_SPECIFIC. Other full-corpus totals: total observation chars 1,134,133,251 → 1,239,474,486 (+105.3M, all from klear); labeled 920.2M; qualified (unsafe-excluded) 703.2M; events 450,298 → 578,283. Display authority for the TW discovery column of Fig. 3 and paper-tables T1 rests on this section; the taxonomy registry `discovery_metrics_15k` stays frozen (display-authority migration recorded in the reconciliation report, not in the registry).

> **A1R3 NOTE (session-semantics supersession):** the A1R2 session-level numbers above are **superseded for session semantics** by the trajectory-identity caliber below (A1R3). Event-level hits, observation characters, allocation accounting, and residual buckets remain A1R2-authoritative (verified equal by A1R3 gates).

## Session-identity amendment (D4-A1R3, trajectory caliber)

Prereg `v011-d4a1r3-session-identity-prereg.json` (FROZEN before recompute; at `evidence/V1/`). Motivation (`taxonomy-residual-v1-report.md` + `taxonomy-session-identity-v1-report.md`): the frozen TW input carries 15,000 recorded trajectories under only **13,053 unique session identifiers** — 1,947 identifiers each appear on exactly two recorded trajectories (multiplicity histogram {1: 11,106, 2: 1,947}); 1,946 collided pairs carry distinct messages and 1 pair (tids 317/318) is byte-identical. Trajectory identity := (frozen source file, row ordinal), content digest verification-only; replay stability proven (two-pass sequence SHA256 `8a74f744b1f79930`). Identifier collisions are a labeling property of the klear source, **not** evidence about run independence.

Result `v011-d4a1r3-tw-trajectory-census.json` (sha256-16 `ae954c032022ca79`). Gates ALL PASS: id-set recomputation equals the A1R2 frozen per-shape session counts exactly; event hits, observation characters (578,283 / 1,239,474,486), allocation accounting (Σ splits = labeled 920,214,271), and residual buckets (including orphan 15,011 / 70,819,544) equal A1R2 exactly.

Per-shape trajectory-level caliber (denominator 15,000 recorded trajectories; OSW exact fractions /20,000; band function unchanged):

| Shape | id-set n (A1R2) | trajectory n (A1R3) | Δn | A1R3 incidence | ratio | band (both calibers) |
|---|---|---|---|---|---|---|
| E1 | 12,832 | 14,578 | +1,746 | 0.971867 | 1.028536 | REPLICATED |
| E2 | 12,945 | 14,789 | +1,844 | 0.985933 | 1.014014 | REPLICATED |
| E3 | 11,592 | 12,302 | +710 | 0.820133 | 1.219131 | REPLICATED |
| E4 | 4,157 | 4,157 | 0 | 0.277133 | — | MEASURABLE_ONLY (OSW schema) |
| E5 | 109 | 112 | +3 | 0.007467 | 2.665179 | PARTIAL_REPLICATION |
| E6 | 293 | 333 | +40 | 0.022200 | 0.033784 | DATASET_SPECIFIC |
| E7 | 210 | 233 | +23 | 0.015533 | 0.041845 | DATASET_SPECIFIC |
| E8 | 0 | 0 | 0 | — | — | NOT_MEASURABLE |
| E9 | 1 | 1 | 0 | 0.000067 | 0.750000 | REPLICATED |
| E10 | 297 | 342 | +45 | 0.022800 | 0.035088 | DATASET_SPECIFIC |
| E11 | 114 | 122 | +8 | 0.008133 | 0.049180 | DATASET_SPECIFIC |
| E12 | 10,317 | 10,938 | +621 | 0.729200 | 1.090236 | REPLICATED |
| E13 | 8,688 | 8,808 | +120 | 0.587200 | 0.794193 | REPLICATED |
| E14 | 10,523 | 11,073 | +550 | 0.738200 | 1.284679 | REPLICATED |
| E15 | 116 | 126 | +10 | 0.008400 | 0.041667 | DATASET_SPECIFIC |

Reading: **all 15 replication bands are unchanged under either caliber**; 8 of 13 measurable shapes satisfy the criterion (R7 + P1) with the six core shapes' ratios tightening toward 1.0 (0.79–1.28). Δn per shape = number of collided pairs where both members carry the shape (E2 +1,844 largest). Byte-identical-pair exclusion sensitivity (denominator 14,999): zero band changes. Display authority for TW session-level incidence migrates to this section; the id-set caliber is retained as superseded provenance.
## A-E class distribution summary (PAPER-A-POSTFREEZE-EVIDENCE-AUGMENTATION-R1, 2026-10-13)

OSW-side class shares come from the frozen figures authority (`data/figures.json`, key `fig2_ae_class_distribution_osw`); TW-side cells come from `paper-tables.json` T2. Per T2: B and E are single-shape classes repaired from R1 incidence; TW A/C/D class unions remain UNRESOLVED (no frozen TW class-union artifact; no values inferred). Classes overlap: a session can belong to A and C simultaneously, so shares need not sum to 100%.

| Class | OSW20K share (figures.json) | TW15K sessions (T2) | TW15K share (T2) | Status |
|---|---|---|---|---|
| A existing/candidate-covered | 1.0000 | - | - | TW union UNRESOLVED |
| B semantic gap (E13) | 0.4663 | 8,808 | 0.5872 | repaired from R1 incidence |
| C unsafe/high-exposure (E12+E7) | 0.7950 | - | - | TW union UNRESOLVED |
| D low-value | 0.0209 | - | - | TW union UNRESOLVED |
| E no meaningful opportunity (E9) | 0.0001 | 1 | 0.0000667 | repaired from R1 incidence |

No new computation: all values verbatim from the two frozen artifacts.
