# Formal Annotation Sample Compatibility Audit

## Verdict

`ANNOTATION_COMPATIBILITY = HOLD`

The formal 120-item sample manifest was not present in the frozen worktree or the shared `evidence/V1` path at audit time. Per isolation rules, no annotation-agent worktree, result file, evidence packet, or label was opened. Existing frozen manifests contain 340 and 269 items respectively and are not substitutes for the requested formal 120-item manifest.

## Impact matrix

| Shape | Sample-source / selection impact | Shape and evidence-citation impact | Protocol applicability |
|---|---|---|---|
| E1 | RECHECK: OSW membership delta +7 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E2 | RECHECK: OSW membership delta +5 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E3 | NO ROW-INCIDENCE CHANGE | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E4 | HIGH: historical OSW detector could not supply E4 items | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E5 | RECHECK: OSW membership delta -74 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E6 | RECHECK: OSW membership delta -3 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E7 | RECHECK: OSW membership delta +1 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E8 | NO ROW-INCIDENCE CHANGE | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E9 | NO ROW-INCIDENCE CHANGE | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E10 | RECHECK: OSW membership delta -4 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E11 | RECHECK: OSW membership delta -1 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E12 | NO ROW-INCIDENCE CHANGE | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E13 | NO ROW-INCIDENCE CHANGE | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E14 | RECHECK: OSW membership delta -2591 rows | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |
| E15 | NO ROW-INCIDENCE CHANGE | raw evidence remains citable; target-shape membership must be checked for selected OSW items | protocol remains conceptually applicable; item-level verdict pending manifest |

## Required close-out check

Once the formal manifest is frozen into a shared read-only path, compare only its item IDs, corpus, target shape, sampling stratum, and evidence citation against `detector-cross-corpus-diff.json`. Do not read labels. At minimum, recheck every OSW item targeting E1, E2, E4, E5, E6, E7, E10, E11, E14. E4 may require a sampling-frame amendment because the historical OSW implementation produced no E4 candidates; E14 has the largest membership contraction (-2,591 trajectories).

No resampling, annotation dispatch, or protocol change is authorized by this report.
