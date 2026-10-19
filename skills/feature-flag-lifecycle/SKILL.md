---
name: feature-flag-lifecycle
description: "Use when adding, ramping, reviewing or removing a feature flag (toggle) in application code: classify it, give it an owner and an expiry at creation, prove the kill switch before any ramp, test both states, and delete it after a quiet period at full rollout."
---

# feature-flag-lifecycle

A flag is cheap to add and expensive to keep: every one is a branch to test, a state to explain and, once the
feature is settled, dead code. The block treats a flag as something with a life (create, ramp, remove) and a
price, not as an `if`. It owns no flag product and no provider choice (those change too fast to write down).
Related: `skills/deprecation-migration` (removing the code the flag protected), `skills/observability-instrumentation`
§4 (the alert that triggers a kill switch), `skills/slo-design` §3 (burn-rate signals as abort criteria).

## When
- A change is going to ship behind a flag, or someone proposes "just put it behind a flag".
- A ramp plan (a percentage, a cohort) is written or reviewed.
- A flag has been at full rollout for a while, or a review finds flags nobody owns.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Flag types, what a flag is not, the record written at creation (owner, expiry, off-switch), one decision point | a flag is about to be created | [`01-types-ownership-expiry.md`](./references/01-types-ownership-expiry.md) |
| 2 | Kill switch proven before the ramp, ramp stages with abort criteria, defaults | a flag is about to reach real users | [`02-kill-switch-and-ramp.md`](./references/02-kill-switch-and-ramp.md) |
| 3 | Testing both states, removal after a quiet period, flag debt and its audit | tests are written, a flag reaches full rollout, or flags are reviewed | [`03-testing-removal-debt.md`](./references/03-testing-removal-debt.md) |

## Output / checkpoint
No pipeline checkpoint. For each flag: the record (name, type, owner, creation and expiry dates, what the off
switch does, who may use it, the signal that triggers it), the ramp plan with an abort criterion per stage, the
test of the off state, and the removal task already on the backlog. A flag with no owner or no expiry is not
merged.

## Guardrails
- Never create a flag without an owner and an expiry date. "We will remember" is how flags outlive their team.
- Never ramp a flag whose off switch has not been exercised in a non-production environment first.
- Never use a flag as a permanent configuration or entitlement mechanism under a release flag's name.
- Never carry another project's numbers (quiet-period lengths, stage sizes, hold times): choose yours from
  your traffic and risk and write them in the ramp plan.
- Never remove a flag by deleting the flag definition alone: the dead branch and the tests of it go in the same
  change.

## Origin
Martin Fowler's article on feature toggles (read 2026-10-19) for the categories, inventory and carrying-cost,
expiry and test-both-states ideas, plus one MIT skill collection's flag workflow, rewritten. Provenance, what was
removed and not verified: [`references/origin.md`](./references/origin.md). 🟡: never run by us.
