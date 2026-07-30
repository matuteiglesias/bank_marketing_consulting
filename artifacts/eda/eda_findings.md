# T02 Hypothesis-Driven EDA Findings

All rates below are descriptive contact-record associations from the full audited dataset. The reproducible evidence is in `eda_summary_metrics.csv`; no model was trained in this stage.

## 1. Historical response heterogeneity supports testing a ranking model (H1/H2)

- **Claim:** Prior-campaign outcome and recency identify sharply different conversion groups.
- **Evidence:** Overall conversion was 11.27% (4,640/41,188). Records with a prior success converted at 65.11% (894/1,373; 5.78x baseline), versus 8.83% (3,141/35,563; 0.78x) when prior outcome was nonexistent. Customers contacted in a prior campaign within 0–7 days converted at 65.76% (774/1,177; 5.84x), while the explicit `pdays=999` never-contacted group converted at 9.26% (3,673/39,673; 0.82x).
- **Business implication:** There is enough observed heterogeneity to evaluate a capacity-constrained ranking approach rather than random calling.
- **Caveat:** These are unadjusted associations, and the previously contacted groups are small; they do not establish that contact timing caused response.
- **Downstream modeling consequence:** Retain eligible historical fields `poutcome`, `pdays`, and `previous`; encode `pdays=999` as a meaningful never-contacted state rather than missing or ordinary elapsed time.

## 2. Macroeconomic context carries descriptive signal (H3)

- **Claim:** Conversion differs materially across the observed Euribor distribution.
- **Evidence:** The lowest `euribor3m` quartile (at or below 1.344) converted at 25.38% (2,676/10,543; 2.25x baseline), compared with 5.08% (475/9,342; 0.45x) in the third empirical quartile (above 4.857 and at or below 4.961).
- **Business implication:** Market context may help distinguish historically favorable response environments.
- **Caveat:** Euribor is correlated with time and other macro variables, so this contrast is not an isolated or causal rate effect and may not transport to a new regime.
- **Downstream modeling consequence:** Retain scoring-time macro variables, including `euribor3m`, and rely on ordered holdout performance to judge whether their signal generalizes.

## 3. Conversion shifts substantially over approximate time (H4)

- **Claim:** Response prevalence is not stable across source order.
- **Evidence:** Source-order quintile conversion rose from 3.14% (259/8,238; 0.28x overall baseline) in the first quintile to 30.84% (2,540/8,237; 2.74x) in the fifth.
- **Business implication:** A random split could mix distinct historical regimes and overstate deployment relevance.
- **Caveat:** Source order is only an approximate chronology: exact dates and years are unavailable, and the month audit found backward transitions.
- **Downstream modeling consequence:** Preserve row order for an ordered holdout, report its approximate nature, and do not use current-campaign `month` or source-row position as strict production features.

## 4. More current-campaign contacts coincide with lower conversion, descriptively only (H5)

- **Claim:** Higher current-campaign contact count is associated with lower observed conversion.
- **Evidence:** Records at contact count 1 converted at 13.04% (2,300/17,642), while records at 6+ contacts converted at 5.49% (186/3,385).
- **Business implication:** Repeated-call capacity deserves operational monitoring, but this table alone cannot determine an optimal cap.
- **Caveat:** This is **descriptive, not causal**: selection, customer difficulty, and campaign progression can jointly determine both contact count and response.
- **Downstream modeling consequence:** Exclude `campaign` from the strict initial-selection model; reserve it for descriptive monitoring or a separately governed in-campaign use case.

## 5. Call duration demonstrates severe post-contact leakage (H6)

- **Claim:** `duration` creates an exceptionally strong but unusable apparent separation because it is observed only after the call.
- **Evidence:** Calls lasting 0–60 seconds converted at 0.02% (1/4,286; 0.002x baseline), whereas calls lasting 601+ seconds converted at 48.61% (1,684/3,464; 4.32x baseline), a difference of 48.59 percentage points.
- **Business implication:** Using this field to choose whom to call would rely on information unavailable at selection time and produce misleading policy evidence.
- **Caveat:** The contrast reflects post-contact call evolution and is presented solely as a leakage demonstration, not as an actionable duration intervention.
- **Downstream modeling consequence:** Forbid `duration` from every production candidate, preprocessing pipeline, and scoring artifact; enforce the rule with a feature-manifest test.

## Refined production-candidate scope

The strict candidate set remains the audited pre-campaign set: customer profile/account fields (`age`, `job`, `marital`, `education`, `default`, `housing`, `loan`), prior-campaign history (`pdays`, `previous`, `poutcome`), and available macro context (`emp.var.rate`, `cons.price.idx`, `cons.conf.idx`, `euribor3m`, `nr.employed`). Literal `unknown` values remain categories. `duration` and `campaign` are excluded; current-campaign scheduling/contact fields (`contact`, `month`, `day_of_week`) are also excluded from the strict initial-selection candidate.
