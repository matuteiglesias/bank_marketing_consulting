# T03 — Reproducible Modeling

**Timebox:** minutes 50–85  
**Status:** CLOSED — validated local execution; see `memos/T03_modeling_closure.md`
**Unlocks:** T04

## Objective

Build the smallest defensible model comparison for ranking future customers.

## Required models

1. regularized logistic regression;
2. one flexible model, preferably a stable sklearn-native gradient boosting implementation.

Optional diagnostic only:

3. a leakage model including `duration`, clearly labeled invalid for deployment.

## Split

Use a temporal holdout.

Preferred design:

- earlier period: training;
- optional intermediate period: validation;
- latest period: untouched test.

If only an ordered row sequence is available, use an ordered split and document the approximation.

## Pipeline requirements

- preprocessing fitted on training data only;
- categorical handling inside a pipeline;
- numeric imputation inside a pipeline;
- deterministic random state;
- no prohibited production features;
- saved feature manifest;
- saved test predictions.

## Required metrics

General:

- ROC-AUC;
- PR-AUC;
- Brier score.

Ranking:

- top 10%, 20%, 30% conversion rate;
- recall at cut;
- lift at cut.

## Required artifacts

### `artifacts/modeling/model_comparison.csv`

Recommended columns:

- `model_id`
- `valid_for_deployment`
- `feature_set`
- `roc_auc`
- `pr_auc`
- `brier_score`
- `conversion_at_10pct`
- `lift_at_10pct`
- `conversion_at_20pct`
- `lift_at_20pct`
- `conversion_at_30pct`
- `lift_at_30pct`
- `notes`

### `artifacts/modeling/test_predictions.csv`

Required columns:

- stable row identifier;
- observed target;
- split;
- prediction from each valid candidate;
- optional invalid leakage prediction, clearly named.

### `artifacts/modeling/feature_manifest.json`

Must list:

- included features;
- excluded features;
- availability class;
- exclusion reason.

## Model selection rule

Select the flexible model only if its operational gain over logistic regression is material and stable enough to justify extra complexity.

Otherwise, recommend logistic regression.

## Exit criteria

T03 may close only if:

- both required models ran;
- test predictions are saved;
- all comparison metrics derive from the same test set;
- the leakage test passes;
- the selected candidate is named;
- T04 can reproduce gains from saved predictions alone.

## Closure memo

Write `memos/T03_modeling_closure.md`.
