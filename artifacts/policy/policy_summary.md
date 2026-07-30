# Operational Policy Summary

## Recommendation

Before a future campaign contact, score each **eligible customer-contact
opportunity** with the selected `logistic_regression` pipeline, sort scores from
highest to lowest, and call in that order until the campaign's capacity is
exhausted. The public data has no stable customer identifier, so records cannot
be assumed to represent unique customers; the bank must apply its own consent,
suppression, deduplication, legal, and operational eligibility rules first.

Pilot the **top 20%** capacity cut initially. On the ordered test holdout this
cut produced the largest observed incremental-conversion count among the three
tested cuts. It is a practical pilot choice, not a globally optimal threshold.
When capacity is tighter, use the **top 10%** as the higher-efficiency option.

## Holdout evidence

All figures below are reproduced from `artifacts/modeling/test_predictions.csv`.
The baseline is random selection within the same 8,238-row test period, whose
conversion rate was 30.83% (2,540 conversions), not the full dataset's 11.27%.

| Capacity | Score cutoff | Selected | Observed conversions | Conversion | Recall | Lift | Random expected | Incremental |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% | 0.292266 | 824 | 502 | 60.92% | 19.76% | 1.9759x | 254.06 | 247.94 |
| 20% | 0.157163 | 1,648 | 819 | 49.70% | 32.24% | 1.6118x | 508.12 | 310.88 |
| 30% | 0.132720 | 2,472 | 993 | 40.17% | 39.09% | 1.3028x | 762.18 | 230.82 |

The score cutoffs describe this holdout ranking only. They are not universal
probability or profitability thresholds and should be refreshed for each
eligible campaign pool and available capacity.

## Feature and use restrictions

- Use only the pre-campaign fields in
  `artifacts/modeling/feature_manifest.json`.
- Never use `duration`, which is observed after contact.
- Do not use current-campaign `campaign` or scheduling/channel fields
  `contact`, `month`, and `day_of_week` in the strict initial-selection model.
- Preserve literal `unknown` values as observed categories.
- Treat the ranking as prediction, not causal uplift. Contact-count patterns and
  other historical associations do not establish effects of intervention.

## Economics and validation

The data omits deposit margin and call cost, so net value and an economically
optimal cutoff cannot be calculated. Historical campaign selection may also
bias observed labels, the source-order holdout is only approximately temporal,
and train/test prevalence differs sharply.

Run a prospective controlled pilot before rollout: compare model-ranked
selection with business-as-usual or random selection under the same eligibility
and capacity rules. Predefine conversion per call as the primary outcome and
also collect deposit value/margin, contact cost and agent time, complaints and
opt-outs, customer identifiers for deduplication, and score/calibration drift.
