# Methodological Guardrails

## 1. Prediction is not causal impact

The dataset records customers who were contacted. A high predicted probability of subscription does not prove that calling caused the subscription.

The model supports prioritization among historically contacted customer profiles. It does not estimate individual treatment effects.

## 2. Leakage boundary

The feature matrix must explicitly classify every input by availability time.

Minimum rules:

- `duration`: post-contact, prohibited;
- `campaign`: current-campaign contact count, prohibited for initial selection unless a separately labeled dynamic-policy analysis is performed;
- calendar and channel fields: classify based on the declared scoring moment;
- prior-campaign variables such as `pdays`, `previous`, and `poutcome`: potentially valid if they refer strictly to earlier campaigns.

## 3. Time-aware validation

If records are chronologically ordered:

- use earlier observations for training;
- reserve later observations for testing;
- do not shuffle before splitting.

If exact dates cannot be reconstructed, document the approximation.

## 4. Baseline discipline

A model must beat useful baselines, not merely another algorithm.

Required:

- random ranking;
- overall prevalence;
- logistic regression.

Optional:

- simple rule based on prior campaign outcome or recency.

## 5. Business-facing metrics

Mandatory:

- ROC-AUC;
- PR-AUC;
- Brier score or calibration diagnostic;
- conversion rate at 10%, 20%, 30%;
- recall at 10%, 20%, 30%;
- lift at 10%, 20%, 30%;
- incremental conversions versus random selection.

## 6. EDA discipline

Every analysis must map to a stated hypothesis or data-integrity question.

Do not create broad chart inventories.

## 7. Modeling discipline

Use:

- one regularized logistic regression;
- one flexible model.

No extensive tuning unless all required artifacts are already complete.

## 8. Interpretability

Distinguish:

- predictive importance;
- direction of association;
- causal effect.

Do not turn feature importance into causal recommendations.

## 9. Operational policy

The final policy must be expressible as:

- a score;
- a ranked list;
- capacity cutoffs;
- expected conversions at each cutoff;
- explicit exclusions and caveats.
