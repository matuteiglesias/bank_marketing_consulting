# T01 — Data Audit

**Timebox:** minutes 12–30  
**Status:** NOT_STARTED  
**Unlocks:** T02

## Objective

Determine whether the dataset supports a valid pre-contact prioritization analysis and create a traceable inventory of quality, timing, and limitations.

## Inputs

- raw Bank Marketing dataset;
- `docs/problem_statement.md`;
- `docs/methodological_guardrails.md`.

## Required analyses

1. dimensions;
2. target balance;
3. column types;
4. exact duplicate rows;
5. missing values;
6. prevalence of literal `unknown` categories;
7. numeric ranges and suspicious values;
8. temporal coverage and ordering;
9. feature classification:
   - pre-campaign;
   - pre-call;
   - during current campaign;
   - post-contact;
   - ambiguous;
10. possible repeated customers without stable identifiers.

## Required artifacts

### `artifacts/quality/data_quality_table.csv`

Recommended columns:

- `check_id`
- `category`
- `field`
- `metric`
- `value`
- `severity`
- `implication`
- `action`

### `artifacts/quality/feature_availability_matrix.csv`

Required columns:

- `feature`
- `description`
- `availability_class`
- `allowed_strict_model`
- `allowed_pre_call_model`
- `leakage_risk`
- `rationale`

## Mandatory checks

- `duration` must be classified post-contact and forbidden.
- `campaign` must not enter the strict initial-selection model.
- `pdays`, `previous`, `poutcome` require explicit interpretation.
- if no stable customer ID exists, record inability to guarantee customer-level independence.
- determine whether records appear chronologically ordered.

## Exit criteria

T01 may close only if:

- both required CSV files exist;
- every model candidate feature is classified;
- all high-severity data issues have a declared action;
- leakage risks are explicit;
- the closure memo states whether T02 can proceed.

## Closure memo

Write `memos/T01_data_audit_closure.md`.
