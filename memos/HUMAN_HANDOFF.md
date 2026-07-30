# Human Handoff

## Governing recommendation

Pilot a pre-campaign `logistic_regression` ranking and call the highest-ranked
20% of eligible customer-contact opportunities first. In the ordered holdout,
that cut selected 1,648 opportunities, captured 819 subscriptions, and converted
at 49.70% versus the contemporaneous random-selection baseline of 30.83%—a
1.6118x lift and 310.88 incremental conversions. Use the top 10% when capacity
is tighter. This is a pilot policy, not a universal or causal rule.

## Supporting evidence

- Evaluation uses the same untouched final 8,238 source-ordered rows for both
  candidates. The split is an approximate temporal validation, not exact
  chronology: dates, years, and a stable customer identifier are unavailable.
- Train prevalence was 6.37% (2,100/32,950); test prevalence was 30.83%
  (2,540/8,238). The full dataset's 11.27% is historical context, not the test
  baseline used for lift or incremental conversions.
- Logistic capacity results from saved test predictions are:

| Capacity | Selected | Conversions | Conversion | Recall | Lift | Incremental vs random |
|---:|---:|---:|---:|---:|---:|---:|
| 10% | 824 | 502 | 60.92% | 19.76% | 1.9759x | 247.94 |
| 20% | 1,648 | 819 | 49.70% | 32.24% | 1.6118x | 310.88 |
| 30% | 2,472 | 993 | 40.17% | 39.09% | 1.3028x | 230.82 |

- Descriptive EDA found strong response heterogeneity in prior-campaign outcome
  and recency, macroeconomic variation, and a rise from 3.14% to 30.84% across
  source-order quintiles. These associations motivate ranking and warn of drift;
  they do not establish causal effects.

## Why logistic regression was selected

| Model | ROC-AUC | PR-AUC | Brier | Top-10% conversion | Top-10% lift |
|---|---:|---:|---:|---:|---:|
| Logistic regression | 0.559286 | 0.418420 | 0.239939 | 60.92% | 1.9759x |
| Histogram gradient boosting | 0.588409 | 0.393809 | 0.251783 | 44.78% | 1.4524x |

Boosting has the higher ROC-AUC, which is acknowledged. Logistic was selected
for the operating decision because it has higher PR-AUC, lower Brier score, and
much stronger performance at the tightest capacity cut. Boosting also failed
the predeclared selection rule: at least 5% relative lift improvement at every
tested cut without lower PR-AUC. Overall discrimination remains modest; model
selection does not convert the evidence into a full-rollout recommendation.

## Implementation proposal

1. Apply bank-owned consent, suppression, legal, and eligibility rules and
   deduplicate with a real customer identifier before scoring.
2. Score once before current-campaign contact using only manifest-approved
   pre-campaign inputs; rank descending rather than treating raw scores as
   economic probabilities.
3. Allocate the pilot's capacity to the top 20%, or top 10% if capacity is more
   constrained. Refresh the rank and capacity cutoff for each eligible pool.
4. Log model/version, scoring time, eligibility, assignment, calls, outcomes,
   costs, deposit value, complaints, and opt-outs.
5. Monitor conversion per call, lift, calibration/drift, operational load, and
   customer-harm indicators before any expansion.

## Risks and assumptions

- Prediction is not causal uplift: outcomes exist only for historically
  contacted opportunities, and historical campaign selection may bias labels.
- A record is a contact opportunity, not necessarily a unique customer; the
  public data contains no stable customer ID.
- The ordered-row split only approximates time, and the 6.37%/30.83% regime
  shift creates material transportability and calibration risk.
- `duration` is post-contact leakage. `campaign`, `contact`, `month`, and
  `day_of_week` are outside the strict initial-selection boundary.
- Deposit margin, call cost, agent time, and deposit size are absent, so neither
  net value nor an economically optimal cutoff can be estimated.
- Fairness, consent, suppression, and operational eligibility require bank data
  and governance before deployment.

## Prospective experiment

Run a controlled prospective pilot under a single eligibility policy and fixed
capacity. Randomly assign eligible opportunities to model-ranked selection or
business-as-usual/random selection; where operationally useful, randomize near
the proposed cutoff. Predefine conversion per call as the primary outcome and
compare groups over the same campaign window. Also measure deposit balance and
margin, call cost and agent time, complaints and opt-outs, subgroup outcomes,
and score/calibration drift. Set sample size, stopping rules, guardrails, and
rollout criteria before launch. The human owner approves the design and final
decision.

## 60-second answer

The bank needs to decide whom to call first, before any current-campaign contact
information exists. I compared logistic regression with histogram gradient
boosting on the same final 8,238 rows, preserving source order as an approximate
time holdout and excluding `duration` plus current-campaign scheduling and
contact fields. Logistic has modest ROC-AUC, but it performs better where
capacity matters: its top 20% converted at 49.70% versus the test period's
30.83% random baseline, producing about 311 incremental subscriptions; its top
10% converted at 60.92%. Boosting's ROC-AUC was higher, but its PR-AUC, Brier
score, and top-10% result were worse. I recommend a controlled top-20% pilot,
with top 10% for tighter capacity—not immediate rollout—because prevalence
shifted sharply, the data cannot identify causal uplift, and margin and call
cost are missing. The next step is a randomized prospective test that captures
economics, customer impact, and drift.

## Likely interviewer objections and concise responses

### “The ROC-AUC is low. Why use the model?”

Overall discrimination is modest, so the model should not be fully deployed.
It still produced useful concentration at the tested capacity cuts: 49.70%
conversion in the top 20% against 30.83% contemporaneous prevalence. That is
enough evidence to justify a controlled pilot, not enough to guarantee rollout.

### “Why not use gradient boosting if its ROC-AUC is higher?”

The decision is capacity-constrained ranking, not maximizing ROC-AUC alone.
Boosting's ROC-AUC was higher (0.588409), but it had lower PR-AUC, worse Brier
score, and only 44.78% top-10% conversion versus logistic's 60.92%. It failed the
predeclared operational selection rule, so logistic is the stronger pilot.

### “Why did test conversion jump from 6.37% in train to 30.83%?”

The public rows span changing campaign and macro conditions, but lack exact
dates and years. Source-order EDA shows a large response shift, so the ordered
split exposes regime drift rather than hiding it with random shuffling. The data
cannot isolate the cause; the jump is a limitation requiring prospective
validation and monitoring.

### “Can you claim calling causes subscription?”

No. Every observed outcome comes from a contacted opportunity, with no uncalled
counterfactual. The model predicts subscription among historically contacted
profiles; only a randomized prospective design can estimate incremental impact
of the targeting policy.

### “Why is top 20% the recommendation?”

Among the three predeclared cuts, top 20% produced the largest observed
incremental count (310.88) while retaining 1.6118x lift. Top 10% is more
efficient when capacity is tight. Twenty percent is a practical pilot setting,
not a globally optimal cutoff.

### “Why exclude duration if it is highly predictive?”

Call duration is known only after the call, while the decision is whom to call
before contact. Including it would leak future information and create a ranking
that cannot be used at scoring time. Its strong association is retained only as
a leakage demonstration.

### “How would you turn this into an economic decision?”

Collect deposit value and margin, call and agent cost, retention/value horizon,
and customer-harm measures. Then estimate expected incremental net value under
the randomized policy and choose capacity where incremental margin exceeds
incremental cost and risk—not by applying a universal threshold to today's raw
scores.
