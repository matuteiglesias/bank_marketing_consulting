# Bank Marketing Consulting Sprint Bundle

This repository is an execution scaffold for a 120-minute consulting case based on the UCI Bank Marketing dataset.

The machine-assisted scope covers minutes 12–100:

1. data audit;
2. hypothesis-driven EDA;
3. reproducible modeling;
4. operational targeting policy.

The human retains ownership of minutes 100–120:

- executive recommendation;
- risks and assumptions;
- final integrity review;
- 60-second synthesis.

## Core principle

Do not maximize the amount of analysis. Produce the smallest coherent evidence chain that supports an actionable recommendation.

The workflow is stage-gated. Each stage must:

1. consume only declared inputs;
2. produce the required artifact;
3. record a closure memo;
4. pass its exit criteria;
5. unlock the next stage.

## Start here

1. Read `AGENTS.md`.
2. Read `docs/problem_statement.md`.
3. Read `plans/sprint_execution_plan.md`.
4. Execute `tasks/T01_data_audit.md`.
5. Do not begin a later task before the prior task is closed.

## Expected final machine-produced evidence

- `artifacts/quality/data_quality_table.csv`
- `artifacts/quality/feature_availability_matrix.csv`
- `artifacts/eda/eda_findings.md`
- `artifacts/modeling/model_comparison.csv`
- `artifacts/modeling/test_predictions.csv`
- `artifacts/policy/gains_table.csv`
- `artifacts/policy/policy_summary.md`
- one closure memo per stage in `memos/`

## Dataset

Expected source: UCI Bank Marketing, preferably `bank-additional-full.csv`.

The implementation must fail clearly if the expected file is absent. It must not silently fabricate or substitute data.
# bank_marketing_consulting
