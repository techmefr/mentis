---
name: admin-back-office-pitfalls
description: "Use when an admin or back-office application is designed or built: a separate admin surface and its own authentication, an append-only audit log of who did what to which record, impersonation (act-as) with consent, banner and limits, feature flags managed from the admin, dangerous actions with typed confirmation and dry run, bulk operations as previewed and resumable jobs, support-staff roles and what to split first. Method only; access-logging and privacy duties are not legal advice."
---

# admin-back-office-pitfalls

A defensive block for building the internal tool that staff use to see and change everything. A back office
built in a hurry fails in familiar ways: the admin screens share a session with the public app, a staff member
edits a record and nobody can say who or why, "login as user" leaves no trace and lets support do things the
customer never could, a bulk action runs on a filter that matched ten times more rows than expected, and one
mis-click on a delete button cannot be undone. The content is craft knowledge with no external source read
(see `references/origin.md`). Flag lifecycle (owner, expiry, removal) is in `skills/feature-flag-lifecycle`;
this block covers only flags as an admin screen. Field and row visibility is in
`skills/field-and-row-permission-ui-api-pitfalls`, role design in `skills/laravel-permissions-not-roles`,
tables in `skills/data-table-ui-pitfalls`, import and export files in `skills/csv-xlsx-import-export-pitfalls`,
background work in `skills/background-jobs-conventions`, personal data duties in `business/data-protection`.

## When
- A new admin panel, support console or internal tool is specified, or an existing one gets "login as",
  bulk edit, a delete or a flag screen.
- A feature touches who may do what to which customer's data, or needs a trail of staff actions.
- An incident review asks "who changed this" and the answer is a shrug.

## Steps

**Read the part you need before the admin routes or the audit table are written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Admin surface, audit log, impersonation, feature flags in admin, dangerous actions, bulk operations | a schema, a route group or an admin action is designed | [`01-audit-impersonation-and-dangerous-actions.md`](./references/01-audit-impersonation-and-dangerous-actions.md) |
| 2 | Staff roles, support workflows, notifications to the customer, v2 regrets, framework pointers | permissions, support tooling or the first release are planned | [`02-roles-support-and-v2.md`](./references/02-roles-support-and-v2.md) |

## Output / checkpoint
Before building: the list of admin abilities with the role that holds each, the audit event catalogue (actor,
action, target, before and after, reason), the impersonation rules (who, consent, banner, forbidden actions,
expiry), the list of dangerous actions with their confirmation level, and the bulk-operation contract (preview,
cap, resume, undo). Evidence is a test that every state-changing admin route writes an audit row, a test that an
impersonating session cannot change a password or an email, a test that a bulk action refuses a filter that
matches more than its cap, and a test that a user without the ability gets a refusal from the API, not only a
hidden button. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Logging of staff access to personal data, retention of audit rows and
  notification duties depend on the jurisdiction; ask the data-protection owner and see `business/data-protection`.
- Never write an admin action without an audit row in the same transaction (§1, point 2), and never let the
  audit table be updated or deleted by the application role (§1, point 3).
- Never run impersonation without a recorded actor, a visible banner and a forbidden-action list (§1, point 5).
- Never run a dangerous action on one click; require a typed confirmation or a second approver and offer a dry
  run (§1, point 8).
- Never run a bulk action on a filter without showing the matched count and a cap (§1, point 9).
- Never enforce admin permissions in the screen only; check them in the API and the job (§1, point 1).
- Never use a shared super-user account; give every staff member their own named, audited login (§2, point 1).

## Origin
Written from craft knowledge of building admin and support tools; no open-source admin framework documentation
was read, so no source is credited and no text was taken. See [`references/origin.md`](./references/origin.md).
🟡: never run by us.
