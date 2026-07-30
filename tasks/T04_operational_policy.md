# T04 — Operational Policy

**Timebox:** minutes 85–100  
**Status:** CLOSED
**Unlocks:** HUMAN HANDOFF

## Objective

Translate valid out-of-sample scores into a simple campaign prioritization policy.

## Required capacity cuts

- top 10%;
- top 20%;
- top 30%.

## Required gains table

Create `artifacts/policy/gains_table.csv` with:

- `model_id`
- `capacity_fraction`
- `customers_selected`
- `observed_conversions`
- `conversion_rate`
- `recall`
- `population_conversion_rate`
- `lift`
- `expected_random_conversions`
- `incremental_conversions`
- `score_cutoff`

## Policy summary

Create `artifacts/policy/policy_summary.md` containing:

1. chosen model;
2. recommended ranking procedure;
3. performance at 10%, 20%, 30%;
4. suggested initial operating cutoff;
5. segments overrepresented near the top, if descriptively useful;
6. exclusions:
   - prohibited variables;
   - ambiguous records;
   - operational or legal exclusions not represented in the dataset;
7. cautions:
   - prediction is not causal uplift;
   - historical campaign selection may bias observed outcomes;
   - public data lacks margin and contact-cost fields;
   - prospective validation is required.

## Cutoff rule

The policy must be framed as capacity-dependent.

Do not claim a universal probability threshold unless business economics support it.

## Exit criteria

T04 may close only if:

- gains are computed from saved test predictions;
- the three required cuts are present;
- the baseline comparison is explicit;
- no causal claim is made;
- the human handoff memo is populated.

## Closure memo

Write `memos/T04_policy_closure.md`.
