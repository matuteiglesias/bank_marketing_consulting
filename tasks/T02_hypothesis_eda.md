# T02 — Hypothesis-Driven EDA

**Timebox:** minutes 30–50  
**Status:** CLOSED
**Unlocks:** T03

## Objective

Produce a small set of findings that determine whether predictive ranking is plausible and which relationships require modeling or caution.

## Hypotheses

- H1: conversion heterogeneity is large enough to support prioritization;
- H2: prior campaign outcome and recency are strong predictors;
- H3: relevant financial or macroeconomic variables add signal;
- H4: conversion patterns shift over time;
- H5: current-campaign contact count is associated with diminishing conversion;
- H6: `duration` produces misleadingly strong apparent performance because it is post-contact.

## Required analyses

1. global conversion;
2. conversion by `poutcome`;
3. conversion by recency:
   - handle sentinel values in `pdays`;
4. conversion by relevant financial variables;
5. temporal evolution of conversion;
6. relationship with `campaign`, labeled descriptive only;
7. comparison with `duration` to demonstrate leakage.

## Chart limit

Maximum recommended charts: 5.

Every chart or table must answer one named hypothesis.

## Required artifacts

### `artifacts/eda/eda_summary_metrics.csv`

Compact metrics supporting the findings.

### `artifacts/eda/eda_findings.md`

Must contain 3–5 findings. Each finding must include:

- claim;
- evidence;
- business implication;
- caveat;
- downstream modeling consequence.

## Prohibited behavior

- no exhaustive pair plots;
- no chart gallery;
- no causal language;
- no recommendation to use `duration`;
- no model training before EDA closure.

## Exit criteria

T02 may close only if:

- 3–5 findings are recorded;
- each finding has quantitative evidence;
- leakage demonstration is explicit;
- candidate model features are refined;
- the closure memo authorizes or blocks T03.

## Closure memo

Write `memos/T02_eda_closure.md`.
