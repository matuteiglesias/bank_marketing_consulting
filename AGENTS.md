# Execution Contract for Codex

## Mission

Build a compact, reproducible evidence pipeline that answers:

> Which eligible customers should the bank contact first, using only information available at the defined scoring time, to improve conversions per unit of telephone capacity?

## Non-negotiable constraints

1. **No leakage in the production candidate.**
   - `duration` is forbidden in production features.
   - Variables generated during the current campaign are forbidden for initial customer selection.
2. **Temporal evaluation is preferred.**
   - Preserve chronological ordering when the dataset supports it.
3. **Business metrics are mandatory.**
   - Report top-decile/top-20%/top-30% conversion rate, recall, lift, and incremental conversions.
4. **Keep the pipeline small.**
   - One baseline logistic model.
   - One flexible model, preferably histogram gradient boosting or another stable sklearn-native option.
5. **Do not optimize prematurely.**
   - No broad hyperparameter search.
   - No large model zoo.
6. **Every stage must close before the next begins.**
7. **Every claim must be traceable to an artifact.**
8. **Unknown categories are data, not automatically missing values.**
9. **Associations involving contact count are descriptive, not causal.**
10. **The human owns the final recommendation.**
    - Machine outputs may propose evidence-backed implications, but must not overstate causality or implementation certainty.

## Working style

- Prefer scripts and reusable functions over exploratory notebook-only logic.
- Keep notebooks optional and thin.
- Use deterministic seeds.
- Save intermediate outputs.
- Write tests for leakage rules, split integrity, and metric calculations.
- Fail loudly when required columns are missing.
- Avoid undocumented manual edits.

## Stage protocol

For each task:

1. read its task file;
2. inspect existing artifacts and closure memos;
3. execute only the stated scope;
4. write or update the required artifacts;
5. run the specified checks;
6. write the closure memo using `memos/TEMPLATE_stage_closure.md`;
7. mark the task `CLOSED`, `BLOCKED`, or `PARTIAL`;
8. only unlock the next task if all mandatory exit criteria pass.

## Definition of done

The bundle is done when:

- T01 through T04 are closed;
- the production feature set contains no prohibited fields;
- all reported model metrics use out-of-sample test predictions;
- the gains table is reproducible from saved predictions;
- all caveats are recorded;
- the human handoff checklist is complete.
