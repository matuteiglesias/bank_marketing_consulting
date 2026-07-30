# Final Consulting Answer

## Problem definition

The bank must decide **which eligible customer-contact opportunities to call
first when telephone capacity is limited**. Scoring occurs before any contact in
the current campaign. The production ranking may therefore use only information
available at that moment; it predicts subscription among historically contacted
opportunities and does not estimate the causal effect of calling.

The formal decision boundary and success criteria are recorded in
`docs/problem_statement.md`; feature-timing rules are in
`artifacts/quality/feature_availability_matrix.csv`.

## Data and limitations

The audited data contains 41,188 contact records and 4,640 subscriptions (11.27%
full-sample conversion). A record is a contact opportunity, not necessarily a
unique customer: no stable customer identifier is available. Twelve exact
duplicates were retained, literal `unknown` values remain observed categories,
and `pdays=999` means no prior contact rather than missingness.

Exact dates and years are absent, so source order supports only approximate
chronology. The ordered split has 32,950 training rows with 2,100 positives
(6.37%) and 8,238 test rows with 2,540 positives (30.83%). This regime shift is
material. The 11.27% full-sample rate is historical context; all policy lift and
incremental-conversion calculations use the contemporaneous **30.83% test
prevalence**. Audit evidence is in `artifacts/quality/data_quality_table.csv` and
the split is declared in `artifacts/modeling/feature_manifest.json`.

## Hypotheses tested

Focused EDA found:

1. prior-campaign outcome and recency separate historically high- and
   low-conversion groups;
2. macroeconomic context, including Euribor, carries descriptive signal;
3. response prevalence changes sharply across source order, supporting ordered
   rather than shuffled evaluation while warning of temporal drift;
4. higher current-campaign contact counts coincide with lower conversion, but
   this association is descriptive and not causal; and
5. call `duration` creates severe apparent predictability but is observed only
   after contact and is therefore leakage.

Exact rates and caveats are in `artifacts/eda/eda_findings.md`, with reproducible
metrics in `artifacts/eda/eda_summary_metrics.csv`.

## Leakage boundary

The strict production set contains customer/account profile fields,
prior-campaign history, and scoring-time macro context. It excludes `duration`,
`campaign`, `contact`, `month`, and `day_of_week`. `duration` is post-contact;
the other excluded fields are current-campaign or scheduling/channel
information outside strict initial selection. The authoritative included and
excluded lists are in `artifacts/modeling/feature_manifest.json`, enforced by
`tests/test_modeling.py` and implemented in `src/modeling.py`.

## Model comparison

Both candidates used the same untouched 8,238-row ordered holdout and
training-only preprocessing.

| Model | ROC-AUC | PR-AUC | Brier | Top-10% conversion | Top-10% lift |
|---|---:|---:|---:|---:|---:|
| Logistic regression | 0.559286 | 0.418420 | 0.239939 | 60.92% | 1.9759x |
| Histogram gradient boosting | 0.588409 | 0.393809 | 0.251783 | 44.78% | 1.4524x |

Histogram gradient boosting has the higher ROC-AUC. Logistic regression is
selected because it has higher PR-AUC, lower Brier score, substantially better
top-10% performance, and the flexible model failed the predeclared operational
selection rule. Overall discrimination is modest, so this comparison supports a
controlled pilot rather than rollout. Exact results and row-level scores are in
`artifacts/modeling/model_comparison.csv` and
`artifacts/modeling/test_predictions.csv`.

## Targeting policy

Apply bank-owned consent, suppression, legal, deduplication, and eligibility
rules first. Score the remaining opportunities before campaign contact, rank
scores descending, and call until capacity is exhausted.

| Capacity | Score cutoff | Selected | Conversions | Conversion | Recall | Lift | Incremental vs random |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% | 0.292266 | 824 | 502 | 60.92% | 19.76% | 1.9759x | 247.94 |
| 20% | 0.157163 | 1,648 | 819 | 49.70% | 32.24% | 1.6118x | 310.88 |
| 30% | 0.132720 | 2,472 | 993 | 40.17% | 39.09% | 1.3028x | 230.82 |

These holdout cutoffs are capacity markers, not universal probability or
profitability thresholds. The exact reproducible table is
`artifacts/policy/gains_table.csv`; operating instructions are in
`artifacts/policy/policy_summary.md`.

## Recommendation

Run a controlled **top-20% pilot** because this cut produced the largest
observed incremental-conversion count among the three predeclared cuts. Use the
top 10% as the higher-efficiency alternative when capacity is tighter. This is
an evidence-backed pilot recommendation, not a claim that 20% is globally
optimal or that calling causes subscription. The governing executive handoff is
`memos/HUMAN_HANDOFF.md` and the five-slide presentation source is
`beamer/bank_marketing_consulting_beamer.tex`.

## Risks and assumptions

- source order is only an approximate temporal holdout;
- the 6.37%/30.83% prevalence shift creates transportability and calibration
  risk;
- historical selection may bias observed outcomes, and no uncalled
  counterfactual exists;
- no stable customer ID exists, so customer-independent evaluation and public
  data deduplication cannot be guaranteed;
- deposit margin, deposit value, call cost, and agent time are absent, so raw
  scores are not economic values and an optimal economic cutoff is unknown; and
- bank-owned fairness, consent, suppression, legal, and operational controls are
  required before use.

## Required next experiment

Under one eligibility policy and fixed capacity, prospectively randomize
eligible opportunities to model-ranked selection or business-as-usual/random
selection. Predefine conversion per call, sample size, stopping rules,
guardrails, and rollout criteria. Collect deposit balance and margin, call cost
and agent time, complaints and opt-outs, subgroup outcomes, stable customer IDs,
and score/calibration drift. The human owner makes the final authorization and
rollout decision.

## Artifact map

| Evidence | Canonical artifact |
|---|---|
| Decision and scoring moment | `docs/problem_statement.md` |
| Methodological rules | `docs/methodological_guardrails.md` |
| Data audit | `artifacts/quality/data_quality_table.csv` |
| Feature timing | `artifacts/quality/feature_availability_matrix.csv` |
| EDA evidence | `artifacts/eda/eda_findings.md`, `artifacts/eda/eda_summary_metrics.csv` |
| Production feature boundary | `artifacts/modeling/feature_manifest.json` |
| Model comparison | `artifacts/modeling/model_comparison.csv` |
| Out-of-sample scores | `artifacts/modeling/test_predictions.csv` |
| Capacity gains | `artifacts/policy/gains_table.csv` |
| Operating policy | `artifacts/policy/policy_summary.md` |
| Stage closure | `memos/T03_modeling_closure.md`, `memos/T04_policy_closure.md` |
| Executive handoff | `memos/HUMAN_HANDOFF.md` |
| Presentation | `beamer/bank_marketing_consulting_beamer.tex` |
