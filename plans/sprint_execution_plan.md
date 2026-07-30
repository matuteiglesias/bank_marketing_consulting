# Sprint Execution Plan

## Overview

The machine-assisted sprint covers minutes 12–100 of the case.

| Stage | Timebox | Goal | Required artifact |
|---|---:|---|---|
| T01 | 12–30 min | Audit data and establish feature availability | quality and limitations tables |
| T02 | 30–50 min | Test a small set of business hypotheses | 3–5 findings |
| T03 | 50–85 min | Build and compare reproducible ranking models | model comparison table |
| T04 | 85–100 min | Convert scores into an operating policy | gains table and policy summary |
| Human handoff | 100–120 min | Recommendation, risks, final review | executive narrative |

## Dependency chain

`T01 -> T02 -> T03 -> T04 -> HUMAN`

No stage may use undeclared outputs from a future stage.

## Stage gates

### Gate G1 — Data is understood

Must establish:

- row and column counts;
- target prevalence;
- data types;
- duplicates;
- unknown-category prevalence;
- numeric ranges;
- temporal coverage;
- feature availability classification;
- repeated-customer limitation.

### Gate G2 — EDA has decision value

Must produce only evidence that informs:

- whether heterogeneity is exploitable;
- whether prior campaign history matters;
- whether recency matters;
- whether financial or macro variables matter;
- whether performance shifts over time;
- whether contact count is associated with diminishing conversion;
- how much `duration` inflates apparent predictability.

### Gate G3 — Models are valid

Must confirm:

- temporal split integrity;
- preprocessing fitted on training data only;
- no prohibited features in production candidates;
- saved out-of-sample predictions;
- baseline and flexible model comparison;
- deterministic execution.

### Gate G4 — Policy is actionable

Must report for top 10%, 20%, 30%:

- customers selected;
- observed positives;
- conversion rate;
- recall;
- lift;
- expected random positives;
- incremental positives.

## Human handoff packet

The final machine handoff must include:

1. one-paragraph evidence summary;
2. best valid model;
3. comparison to logistic baseline;
4. gains at 10%, 20%, 30%;
5. strongest 3–5 findings;
6. leakage statement;
7. key limitations;
8. open decisions the human must make.
