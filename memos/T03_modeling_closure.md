# Stage Closure Memo

## Stage

`T03 — Reproducible Modeling`

## Status

`CLOSED`

## Inputs consumed

- `tasks/T03_reproducible_modeling.md`
- `docs/methodological_guardrails.md`
- `artifacts/eda/eda_findings.md`
- `artifacts/quality/feature_availability_matrix.csv`
- `data/raw/bank-additional-full.csv`

## Work completed

- Executed the two predeclared sklearn pipelines with deterministic seed 1729.
- Used the first 32,950 source-ordered rows for training and held out the final
  8,238 rows untouched for comparison. This preserves source order as an
  approximate chronology; the data does not contain exact dates, years, or a
  stable customer identifier.
- Fitted all preprocessing on training data only and saved row-level test
  predictions, the comparison table, and the production feature manifest.
- Reproduced the gains table from the selected model's saved test predictions.

## Artifacts produced and validated

- `artifacts/modeling/feature_manifest.json`
- `artifacts/modeling/model_comparison.csv`
- `artifacts/modeling/test_predictions.csv`
- `artifacts/policy/gains_table.csv`
- `src/modeling.py`
- `tests/test_modeling.py`

All model metrics use the same 8,238-row untouched ordered holdout. The saved
predictions contain exactly those 8,238 unique source-row identifiers and both
candidate scores.

## Holdout composition

| Partition | Rows | Positives | Conversion |
|---|---:|---:|---:|
| Train | 32,950 | 2,100 | 6.37% |
| Test | 8,238 | 2,540 | 30.83% |

The large prevalence shift is material. Capacity gains are therefore compared
with contemporaneous random selection at the **30.83% test prevalence**, not
with the 11.27% full-sample historical conversion rate.

## Model results on the common test set

| Model | ROC-AUC | PR-AUC | Brier | Top-10% conversion | Top-10% lift |
|---|---:|---:|---:|---:|---:|
| Logistic regression | 0.559286 | 0.418420 | 0.239939 | 60.92% | 1.9759x |
| Histogram gradient boosting | 0.588409 | 0.393809 | 0.251783 | 44.78% | 1.4524x |

## Selected candidate and rationale

`logistic_regression` is selected for operational performance, not simplicity
alone. Histogram gradient boosting has the higher ROC-AUC (0.588409 versus
0.559286), but logistic regression has the higher PR-AUC, lower Brier score,
and substantially stronger top-10% conversion and lift. The flexible model also
fails the predeclared rule requiring at least 5% relative lift improvement at
all three capacity cuts with no PR-AUC loss.

## Integrity checks

- [x] Both required models executed.
- [x] Required artifacts exist.
- [x] All metrics use the same untouched 8,238-row test set.
- [x] Saved predictions contain only test rows and reconcile to the gains table.
- [x] `duration`, `campaign`, `contact`, `month`, and `day_of_week` are absent
  from both production candidates.
- [x] Tests cover leakage rules, ordered split integrity, preprocessing, metric
  calculations, manifest coverage, and end-to-end output structure.

## Limitations

- Source order is only approximate chronology; exact temporal validation is not
  possible from the public fields.
- No stable customer identifier exists, so customer-level independence across
  the split cannot be guaranteed.
- The prevalence shift and modest discrimination indicate temporal drift and
  limit transportability; monitoring and prospective validation are required.
- Ranking predicts subscription among historically contacted opportunities; it
  does not estimate causal uplift from calling.
- Raw predicted probabilities must not be interpreted as calibrated economic
  values, especially without deposit margin and contact-cost inputs.

## Deviations and execution context

The original Codex container could not install NumPy, pandas, SciPy, or
scikit-learn because both package proxies returned HTTP 403, so T03 was
correctly recorded as blocked at that time and no results were fabricated.
Analytical execution was subsequently completed and validated in a working
local environment; that verified execution is the governing current state.

## Decision

- `T04_UNLOCKED`

## Exact next action

- Translate the saved logistic-regression test scores into a capacity-dependent
  policy and close T04.
