# Codex Launch Prompt

You are executing a time-boxed consulting-case analysis.

Read, in order:

1. `AGENTS.md`
2. `docs/problem_statement.md`
3. `docs/methodological_guardrails.md`
4. `plans/sprint_execution_plan.md`
5. `tasks/TASK_INDEX.md`

Then begin only `tasks/T01_data_audit.md`.

Operate stage by stage. Do not begin a later task until the prior closure memo marks it CLOSED and explicitly unlocks the next stage.

For every stage:

- produce the required artifacts;
- run integrity checks;
- write the closure memo;
- preserve reproducibility;
- record blockers rather than silently improvising;
- prefer a complete small analysis over an incomplete complex one.

The strict production use case is initial customer prioritization before current-campaign contact. `duration` is forbidden. Variables generated during the current campaign are forbidden unless analyzed separately and labeled non-production.

At the end of T04, populate `memos/HUMAN_HANDOFF.md` from the template and stop. Do not write the final executive recommendation as though it were validated beyond the evidence.
