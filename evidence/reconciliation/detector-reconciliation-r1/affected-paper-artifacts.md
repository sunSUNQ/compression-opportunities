# Affected Paper Claims, Figures, and Tables

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
