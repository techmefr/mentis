---
name: crm-app-build-pitfalls
description: "Use when a CRM or customer-tracking application is designed or built: the minimal model of account, contact, deal, activity and owner, duplicate prevention at write time, pipeline statuses with defined transitions, merge that keeps history, immutable activity timeline, archive versus delete and erasure requests, per-user and per-team visibility, imports and sync with mail, calendar and forms, custom fields that rot, and what to split first and what gets regretted at v2. Method only; consent and privacy law is not legal advice."
---

# crm-app-build-pitfalls

A defensive block for building the application, not for running sales with it. A CRM built in a hurry fails in
familiar ways: the same company exists four times, a deal has a stage nobody can define, a merge destroys the
history of the record it absorbs, a salesperson sees every customer's data, an import doubles the database, and
custom fields multiply until no report can be trusted. The content is mostly craft knowledge; a few points are checked against open-source CRM documentation (see `references/origin.md`). Cleaning and reporting on the data of an existing CRM, stage evidence and
dedupe as a sales-ops practice, are in `business/outbound-sales-and-crm-hygiene-pitfalls`. Money fields are in
`skills/money-arithmetic-and-rounding-pitfalls`, tenant boundaries in `skills/laravel-tenant-context-by-default`,
role design in `skills/laravel-permissions-not-roles`, personal data duties in `business/data-protection`.

## When
- A new CRM, contact book, lead tracker or customer-success tool is specified or its schema is drafted.
- An existing internal tool grows deals, pipelines, reminders or a sales dashboard.
- A feature touches merge, import, sync with mail or calendar, deletion or visibility.

## Steps

**Read the part you need before the schema or the migration is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Minimal model and its pitfalls: duplicates, statuses, merge, timeline, archive versus delete, money, tenants | a schema or a write path is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Roles and visibility, imports, exports and integrations, what to split first, v2 regrets, framework pointers | permissions, an import, a sync or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the entity list with a unique key and an owner for each, the status list per pipeline with
entry and exit conditions and the allowed transitions, the merge and erasure behaviour written down, the
visibility matrix by role and team, and the import and sync keys. Evidence is a duplicate-creation test, a
merge test that keeps the absorbed record's timeline, and a test that a user of one team cannot read another
team's record through the list, the search and the export. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Consent, marketing opt-in, retention and erasure duties depend on the
  jurisdiction and the use; ask the data-protection owner and see `business/data-protection`.
- Never accept a contact or account write without a normalised duplicate check (§1, point 1). Do it at write
  time and in the import path, not only in a later cleanup.
- Never let a status be a free-text field, and never let a deal skip to a closed state with no recorded reason
  (§1, point 3).
- Never merge by deleting the loser: repoint its children, keep a redirect and write a merge event (§1, point 5).
- Never edit or delete a timeline entry; correct it with a new entry (§1, point 6).
- Never filter visibility in the screen only: enforce it in the query that feeds the list, the search index and
  the export (§2, point 1).
- Never cascade a delete from an account to its history (§1, point 8).
- Never store money as a float or without a currency (§1, point 9).

## Origin
Written from craft knowledge of building CRM-style applications; checked on 2026-10-20 against the Atomic CRM
documentation (MIT), credited in the origin file, and no text was taken. See [`references/origin.md`](./references/origin.md). 🟡: never
run by us.
