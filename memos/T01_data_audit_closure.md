# Stage Closure Memo

## Stage

`T01 — Data Audit`

## Status

`BLOCKED`

## Inputs consumed

- `docs/problem_statement.md`
- `docs/methodological_guardrails.md`
- UCI dataset retrieval was attempted, but the execution environment returned HTTP 403 and no raw dataset was present.

## Work completed

- Implemented a deterministic, standard-library audit entry point with strict schema and target validation.
- Declared availability and leakage rules for every expected candidate feature.
- Added checks for dimensions, target balance, duplicates, blanks, literal `unknown`, numeric ranges, temporal ordering, prior-campaign sentinel semantics, and the absent customer identifier.
- Added focused tests for loud input failure, schema/target validation, leakage rules, and deterministic metrics.

## Artifacts produced

- None. Evidence tables cannot be generated truthfully without the canonical raw records.

## Key findings

1. The repository and workspace contain no `bank-additional-full.csv` input.
2. `duration` is classified post-contact and forbidden; `campaign` is current-campaign and forbidden for strict initial selection.
3. `pdays`, `previous`, and `poutcome` are explicitly interpreted as prior-campaign history, with `pdays=999` treated as a meaningful sentinel.

## Integrity checks

- [ ] Required artifacts exist — blocked by absent input
- [ ] Metrics reconcile — no source metrics can be calculated
- [x] No prohibited feature entered a production model — no model was built
- [x] Claims are supported by saved evidence — blocker and rules are recorded in code/tests
- [x] Limitations are recorded

## Deviations from plan

- The expected UCI dataset was not supplied. Direct retrieval from the canonical archive was attempted but denied by the environment (HTTP 403). No alternate data were fabricated or silently substituted.

## Open issues

- Supply the canonical `bank-additional-full.csv` at `data/raw/bank-additional-full.csv`.
- Run the audit and review all high-severity issues before closure.

## Decision

- `NEXT_STAGE_BLOCKED`

## Exact next action

- Place the canonical file at `data/raw/bank-additional-full.csv`, run `python -m src.data_audit`, verify both quality artifacts, then update this memo to `CLOSED` only if every exit criterion passes.
