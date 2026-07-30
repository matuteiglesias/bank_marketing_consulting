# Problem Statement

## Client

Portuguese commercial bank.

## Situation

Telephone campaigns used to sell term deposits consume significant operational capacity and currently achieve a low conversion rate.

## Decision to support

Before launching or executing a future campaign, determine which eligible customers should be contacted first.

## Precise analytical problem

Develop a reproducible ranking policy that uses only information available at the declared scoring time to prioritize eligible customers by expected likelihood of subscribing to a term deposit.

The ranking must improve conversions obtained within a fixed calling capacity relative to:

1. random selection;
2. the historical population conversion rate;
3. a simple business-rule baseline where feasible.

## Unit of analysis

One campaign contact record representing a candidate customer-contact opportunity.

Important limitation: the public dataset does not provide a stable customer identifier. Therefore, repeated appearances of the same customer may be impossible to identify conclusively.

## Target

Binary term-deposit subscription outcome:

- positive: customer subscribed;
- negative: customer did not subscribe.

## Operational objective

For a fixed calling budget or capacity, maximize:

- conversions per call;
- lift over non-targeted selection;
- incremental conversions.

A later production version should optimize expected economic value:

`P(subscription | pre-contact information) × expected margin − contact cost`

The public dataset does not contain all monetary inputs required for that objective.

## Scoring moment

Primary scope:

> Initial campaign prioritization before the customer has been contacted in the current campaign.

Optional secondary scope, not required for this sprint:

> Dynamic next-best-action or recontact decisions after one or more current-campaign contacts.

## Feature availability rule

Every variable must be assigned to one of:

1. **pre-campaign** — known before the campaign begins;
2. **pre-call** — known before a specific call but possibly assigned during campaign planning;
3. **during-contact/current-campaign** — generated while the current campaign unfolds;
4. **post-contact** — known only after the call or outcome;
5. **ambiguous** — documentation or business process does not establish timing confidently.

Only approved pre-campaign variables may enter the strict production model.

## Known leakage concern

`duration` is known only after a call has occurred. It may be used only in a diagnostic leakage comparison and must never enter the production candidate.

## Primary success criteria

A candidate solution is successful if it:

1. produces a materially better top-k conversion rate and lift than the baselines;
2. is evaluated out of sample using a time-aware split where possible;
3. excludes prohibited variables;
4. is reproducible from raw input to final gains table;
5. yields a simple operational cutoff or ranked list;
6. documents uncertainty, limitations, and deployment assumptions.

## Required capacity cuts

Evaluate the top:

- 10%;
- 20%;
- 30%;

of ranked customers in the test period.

## Out of scope

- causal impact of calling versus not calling;
- script optimization;
- agent performance optimization;
- exact contact-cost or term-deposit margin estimation;
- multi-channel optimization;
- customer lifetime value;
- production deployment architecture;
- fairness certification;
- full hyperparameter tuning.
