# Stage Closure Memo

## Stage

`T02 — Hypothesis-Driven EDA`

## Status

`CLOSED`

## Inputs consumed

- `data/raw/bank-additional-full.csv`
- `artifacts/quality/data_quality_table.csv`
- `artifacts/quality/feature_availability_matrix.csv`
- `memos/T01_data_audit_closure.md`

## Work completed

- Implemented reusable, deterministic descriptive aggregation for H1–H6 without training a model.
- Quantified global, prior-outcome, sentinel-aware recency, Euribor, approximate-time, campaign-count, and post-contact duration conversion patterns.
- Recorded five structured findings and refined the strict production candidate scope.
- Added focused tests for sentinel handling, aggregate reconciliation, hypothesis coverage, and explicit nonproduction labels.

## Artifacts produced

- `artifacts/eda/eda_summary_metrics.csv`
- `artifacts/eda/eda_findings.md`
- `src/hypothesis_eda.py`
- `tests/test_hypothesis_eda.py`

## Key findings

1. Prior success and recent prior contact groups converted above 65%, versus the 11.27% overall rate, supporting evaluation of predictive ranking while not implying causality.
2. Conversion varied from 3.14% to 30.84% across source-order quintiles, requiring an approximate ordered evaluation.
3. Current-campaign contact count is descriptively associated with declining conversion but is forbidden for strict initial selection.
4. Duration segments range from 0.02% to 48.61% conversion, explicitly demonstrating severe post-contact leakage.

## Integrity checks

- [x] Required artifacts exist
- [x] Metrics reconcile
- [x] No prohibited feature entered a production model — no model was built in T02
- [x] Claims are supported by saved evidence
- [x] Limitations are recorded

## Deviations from plan

- No charts were produced; compact tables directly answer every named hypothesis and remain below the five-chart limit.

## Open issues

- Exact chronology and customer-level independence remain unavailable.
- Macro associations may proxy historical regime rather than transportable customer-level signal.

## Decision

- `NEXT_STAGE_UNLOCKED`

## Exact next action

- Execute `tasks/T03_reproducible_modeling.md` with an approximate source-order holdout and the refined strict feature set.
