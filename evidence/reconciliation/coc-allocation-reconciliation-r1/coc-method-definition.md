# COC method definition — reconciliation R1

Status: **FROZEN FOR R1 REPLAY**. This definition was fixed before the R1 aggregate results were computed.

## Scope and invariant inputs

R1 changes one variable only: the coverage-opportunity (COC) allocation/accounting method. It preserves the historical frozen A0 taxonomy and the historical OSW/Qwen parser and detector semantics. In particular, R1 does not repair E4 or any other detector and does not use formal-annotation outputs.

The two replay frames are:

- OSW: the frozen 20,000-trajectory Minimax manifest v2.
- Qwen: all locally frozen 35,334 trajectories: 15,000 OpenHands and 20,334 SWE-agent. The historical Qwen coverage artifact used only the 15,000 OpenHands trajectories; R1 reports that historical frame separately and never treats it as a 35,334-trajectory result.

## Measurement unit

An event is one parsed tool observation paired with its preceding tool command by the frozen corpus adapter. The measurable payload is `len(observation.encode("utf-8"))`.

This is an **UTF-8 re-encoded event-payload proxy**. It is not the byte length of the original serialized message, transport frame, tokenizer output, or exact removable byte span. Code-point character length is retained only as a sensitivity measure.

## Opportunity and capability sets

The primary R1 denominator follows the frozen A0 registry:

- excluded as unsafe: E7, E12;
- excluded as `NO_OPPORTUNITY`: E9;
- qualified opportunity: every other detected shape, including partial-fit and gap-semantic shapes;
- shipped full-fit numerator: E5, E8, E10, E11;
- shipped-plus-candidate full-fit numerator: shipped plus E1, E2, E3, E14.

E15 is partial-fit in A0 and is therefore not included in a full-fit numerator. A separate legacy-mapping sensitivity retains the historical implementation's choices (E9 in the denominator and E15 in the candidate numerator).

## Primary overlap allocation

For an event with payload `B` and `k` fired frozen-detector shapes, each fired shape receives exactly `B/k` allocation units. Aggregation uses exact rational arithmetic; decimal values in the ledger are presentation fields only. Qualified, shipped, and candidate totals are sums of the relevant per-shape allocations.

This rule prevents double counting within a multi-label event: the sum of allocations across all fired shapes equals the event payload. Ineligible shares remain excluded rather than being reallocated. Repeated payloads in distinct events are not deduplicated because they are distinct trajectory events.

The primary corpus metric is:

`COC = supported qualified allocated UTF-8 bytes / all qualified allocated UTF-8 bytes`.

The reported relative full-fit coverage gap is `1 - shipped_COC / candidate_COC` when candidate COC is non-zero. It is not a deletion or savings rate.

## Missing and non-measurable states

- `NO_DETECTOR_SHAPE`: event has no frozen-detector label and does not enter the COC ledger denominator.
- `NO_QUALIFIED_SHAPE`: event fires shapes, but all are unsafe or `NO_OPPORTUNITY`.
- `EMPTY_PAYLOAD`: a labeled event has zero re-encoded bytes; it remains traceable but contributes zero mass.
- `NOT_MEASURABLE`: required observation content or event identity is absent.

Missing or non-measurable events are never treated as negative detector results.

## Sensitivity strategies

R1 also computes, without changing the primary definition:

1. eligible-renormalized equal split;
2. optimistic any-supported whole-event allocation;
3. conservative all-qualified-shapes-supported whole-event allocation;
4. code-point character length instead of UTF-8 bytes;
5. the historical eligibility/candidate mapping;
6. exact historical OSW whole-trajectory/session-shape and Qwen session-shape proxies.

If reasonable strategies change the qualitative conclusion, R1 must report that instability.

## Interpretation boundary and verdict rule

Because frozen detectors provide event membership but no byte spans, exact event-level byte-span union is not identifiable. Equal splitting is deterministic overlap-controlled bookkeeping, not proof that the assigned bytes are safely removable. Therefore the maximum possible final verdict for the requested reconciliation is **PARTIAL**, unless exact span provenance is independently present. R1 must not describe COC as online token savings, safe deletion, realized cost reduction, or task-level causal effect.
