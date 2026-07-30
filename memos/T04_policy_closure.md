# Stage Closure Memo

## Stage

`T04 — Operational Policy`

## Status

`CLOSED`

## Inputs consumed

- `tasks/T04_operational_policy.md`
- `artifacts/modeling/model_comparison.csv`
- `artifacts/modeling/test_predictions.csv`
- `artifacts/modeling/feature_manifest.json`
- `artifacts/policy/gains_table.csv`

## Work completed

- Reproduced the policy gains from saved out-of-sample logistic-regression test
  predictions alone.
- Documented capacity-dependent procedures, exclusions, limitations, and the
  prospective experiment required before rollout.

## Policy evidence

The contemporaneous random baseline is the 30.83% conversion prevalence of the
8,238-row test period.

| Capacity | Score cutoff | Customers | Conversions | Conversion | Recall | Lift | Incremental vs random |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% | 0.292266 | 824 | 502 | 60.92% | 19.76% | 1.9759x | 247.94 |
| 20% | 0.157163 | 1,648 | 819 | 49.70% | 32.24% | 1.6118x | 310.88 |
| 30% | 0.132720 | 2,472 | 993 | 40.17% | 39.09% | 1.3028x | 230.82 |

## Recommendation

Pilot the top 20% because it maximizes observed incremental conversions among
the three tested capacity cuts. If capacity is tighter, the top 10% is the
higher-efficiency alternative, with the highest observed conversion and lift.
The 20% cut and its score cutoff are not globally optimal: deposit margin and
call-cost data are absent, and cutoffs can drift with campaign conditions.

## Integrity checks

- [x] Gains derive from `artifacts/modeling/test_predictions.csv`.
- [x] The 10%, 20%, and 30% cuts reconcile exactly with the committed gains
  artifact.
- [x] The baseline is contemporaneous test prevalence, not 11.27% full-sample
  prevalence.
- [x] No causal-uplift or universal-threshold claim is made.
- [x] Limitations and the next experiment are specified.

## Limitations and next experiment

Ranking performance is modest overall and observed under approximate chronology
with a large prevalence shift. There is no stable customer ID, no causal
counterfactual, and no complete campaign economics. Historical selection can
bias labels. Before rollout, run a controlled prospective pilot against random
or business-as-usual selection under identical capacity and eligibility rules;
capture conversions, deposit margin, call cost/time, complaints, opt-outs, and
stable identifiers.

## Presentation validation

The five-slide Beamer source was updated to the final evidence and policy.
`pdflatex`, `latexmk`, and `tectonic` are unavailable in the closure container,
so the source could not be compiled here and the committed PDF was not
fabricated or replaced. Compile the `.tex` in a LaTeX-enabled environment before
external delivery.

## Decision

- `HUMAN_HANDOFF_UNLOCKED`

## Exact next action

- The human owner reviews the evidence, chooses pilot capacity and risk
  acceptance, and authorizes (or rejects) the prospective experiment.
