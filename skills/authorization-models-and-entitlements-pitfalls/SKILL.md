---
name: authorization-models-and-entitlements-pitfalls
description: "Use when choosing or reviewing how an application decides who may do what, beyond a handful of roles: picking role, attribute or relationship-based models, putting the decision in one service and calling it from every entry point, listing what a person may see instead of checking row by row, keeping stored relationships in step with the source of truth, caching decisions after a revocation, and gating features by plan (entitlements) separately from permissions."
---

# authorization-models-and-entitlements-pitfalls

A defensive block for the design side of access control, once "a role column and a middleware" stops being
enough. Premise: **an authorization decision is a function of (who, what action, which resource, which facts),
the model that computes it has to be chosen and tested as data, and "may this person do it" and "does this
customer's plan include it" are two questions with two stores**. Enforcement on every read and write path
(hide versus refuse, lists, counts, exports, mass assignment) is `skills/field-and-row-permission-ui-api-pitfalls`;
the per-route declaration and default deny in the application are `skills/security-hardening` §3; role names versus
permissions in Laravel is `skills/laravel-permissions-not-roles`; authentication and sessions are
`skills/auth-session-conventions`; database row-level security is `skills/sql-conventions` §6.

## When
- A new product needs sharing, teams, folders, per-record owners or delegation, and roles no longer describe it.
- Several services or languages each re-implement the same access rule.
- A screen must list "everything this person can open", or a revocation seems to take effect late.
- A feature is sold per plan, tier, add-on or usage limit, and code asks whether a customer may use it.

## Steps

**Read only the section the task meets.** §2 is the entry point for "someone saw something after losing access".

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Choosing the model: roles, attributes, relationships, hierarchy, set operations, versioned model | a model is chosen, extended or found too coarse | [`01-model-choice.md`](./references/01-model-choice.md) |
| 2 | Decision point: one place, request shape, default deny, listing, sync with the source of truth, cache staleness, tests | decisions are centralised, listed, cached or reported late | [`02-decision-point-and-consistency.md`](./references/02-decision-point-and-consistency.md) |
| 3 | Entitlements: plan to feature, limits, downgrade, overrides, denial reasons | a feature depends on what the customer bought | [`03-entitlements-and-plan-gating.md`](./references/03-entitlements-and-plan-gating.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed design owes: the questions the product asks written as (principal, action,
resource) with the facts each needs (§1), the one place that answers them and what it does on missing input (§2),
a test table with allowed and refused cases including revocation (§2), and, where plans exist, a table of
feature, plan, limit and downgrade behaviour (§3).

## Guardrails
- Choose the smallest model that expresses the questions the product asks. Never adopt a relationship graph or a
  policy engine before a written question needs one (§1).
- Answer every question in one place and call it from every entry point. Never copy a rule into a second service
  or into the client (§2).
- Refuse when the decision cannot be computed (missing attribute, unknown resource, engine down). Never default to
  allow (§2).
- Ask "what may this person see" as one query. Never fetch everything and test each row afterwards (§2).
- Revoke through the same path that grants, and decide how late a revocation may take effect. Never cache a
  decision with no stated staleness window (§2).
- Keep plan entitlements apart from permissions: check that the customer has the feature and that the person may
  use it. Never encode a plan tier as a role (§3).
- This block restates documentation of two open-source authorization engines at idea level and adds marked own
  guidance; nothing was run. Defaults and limits are not given (see
  [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from the OpenFGA documentation (Apache-2.0) and the Cerbos documentation (Apache-2.0), read 2026-10-20,
with own guidance marked in the references. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
