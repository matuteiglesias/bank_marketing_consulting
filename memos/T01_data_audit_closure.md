# Stage Closure Memo

## Stage

`T01 — Data Audit`

## Status

`CLOSED`

## Inputs consumed

- `docs/problem_statement.md`
- `docs/methodological_guardrails.md`
- Canonical `bank-additional-full.csv` supplied in the repository data bundle and staged at the declared raw-data path.

## Work completed

- Validated the 21-column schema and binary target across 41,188 contact records.
- Audited target balance, exact duplicates, blanks, literal `unknown` values, numeric ranges, prior-contact sentinel semantics, and approximate source ordering.
- Classified every candidate feature by scoring-time availability and production eligibility.
- Recorded the lack of a stable customer identifier and the resulting independence limitation.

## Artifacts produced

- `artifacts/quality/data_quality_table.csv`
- `artifacts/quality/feature_availability_matrix.csv`

## Key findings

1. The historical positive rate is 11.2654% (4,640 of 41,188), establishing the random-selection benchmark.
2. Twelve exact duplicate rows are retained because the unit is a contact opportunity and no customer identifier exists; customer-level independence cannot be guaranteed.
3. Source order is approximately chronological but exact dates and years cannot be reconstructed: the month sequence has two backward transitions.
4. `duration` is post-contact and forbidden, while current-campaign `campaign` is also forbidden for strict initial prioritization.
5. Prior-campaign fields are eligible with explicit semantics: `pdays=999` means never previously contacted and occurs in 39,673 records.

## Integrity checks

- [x] Required artifacts exist
- [x] Metrics reconcile
- [x] No prohibited feature entered a production model — no model was built in T01
- [x] Claims are supported by saved evidence
- [x] Limitations are recorded

## Deviations from plan

- None. The canonical file was available in the supplied repository bundle rather than initially at the declared `data/raw` path.

## Open issues

- Exact customer-level independence is unverifiable.
- Temporal evaluation must preserve source order and be labeled an approximation because year/date identifiers are absent.

## Decision

- `NEXT_STAGE_UNLOCKED`

## Exact next action

- Execute `tasks/T02_hypothesis_eda.md` using the audited raw file and availability rules.
