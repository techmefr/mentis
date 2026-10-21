---
name: field-and-row-permission-ui-api-pitfalls
description: "Use when a business application restricts what a person can see or change per record (row-level) or per attribute (field-level), or such rules are reviewed: deciding hide versus disable versus mask in the interface, enforcing the same rule in the API and the query layer (never in the client alone), mass assignment and write-side field filtering, lists, search, counts and exports that leak restricted rows or columns, permission-aware errors, caching and tenant scoping, and an audit trail of reads and changes. Framework-independent."
---

# field-and-row-permission-ui-api-pitfalls

A defensive block for the gap between "the button is hidden" and "the server refuses". Premise: **the interface
only expresses a permission; the server enforces it on every path that reads or writes the data, and the same
rule has to come out of one definition, not two**. Role versus permission naming in Laravel is
`skills/laravel-permissions-not-roles`; scoping a query instead of checking after fetch is
`skills/laravel-scope-dont-check-after-fetch`; tenant isolation is `skills/laravel-tenant-context-by-default`;
database row-level security for generated APIs is `skills/postgres-operations-and-exposed-api-pitfalls`; client
trust in backend-as-a-service rules is `skills/firebase-rules-and-client-trust-pitfalls`; authentication and
sessions are `skills/auth-session-conventions`. Export mechanics are `skills/csv-xlsx-import-export-pitfalls`; data
tables, filters and dashboards belong to their own blocks and are not repeated here.

## When
- A screen shows or edits a record where different people may see different rows or fields.
- A report says "someone saw or changed what they should not have", or a security review asks how restrictions are
  enforced.
- A new endpoint, list, search, export, notification or background job reads data that has restrictions.
- A permission model is added to an application that had only authentication.

## Steps

**Read only the section the task meets.** §2 is the entry point for any leak report.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Modelling: rule definition in one place, hide versus disable versus mask, how the interface learns what is allowed | permissions are designed or surfaced in the UI | [`01-model-and-interface.md`](./references/01-model-and-interface.md) |
| 2 | Enforcement in the API: reads, writes, mass assignment, lists, counts, search, exports, jobs, errors, caching | an endpoint or query touches restricted data | [`02-api-enforcement-and-leaks.md`](./references/02-api-enforcement-and-leaks.md) |
| 3 | Audit and verification: logging reads and changes, permission matrix tests, bulk actions, review checklist | a rule is shipped, reviewed or investigated | [`03-audit-and-verification.md`](./references/03-audit-and-verification.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed feature owes: the rules written once per resource, with row scope and field
lists (§1), a table of every path that reads or writes the resource and how each applies the rule (§2), a
permission-matrix test over roles, records and fields (§3), and the audit events emitted (§3).

## Guardrails
- Decide access on the server for every request, whatever the interface hides. Never rely on a hidden control, a
  disabled input or a client-held flag (§1, §2).
- Define each rule once and derive the interface flags from the same definition. Never keep a second copy of
  the rule in the front end (§1).
- Filter rows in the query and columns in the serializer, on the write side as on the read side. Never fetch
  everything and trim in the client or after the fact (§2).
- Allow-list the writable fields per role. Never pass a request body straight to a model (§2).
- Apply the same scope to lists, counts, search, exports, notifications and jobs. Never secure the detail view
  alone (§2).
- Answer a refused request without confirming that a hidden record exists. Never let error text or timing reveal
  what the person may not see (§2).
- Record reads of sensitive fields and every permission-relevant change. Never rely on application logs that
  rotate away (§3).
- Status-code points (§2.3.1) are checked against RFC 9110; the rest is craft knowledge. Unverified points are in
  [`references/origin.md`](./references/origin.md). No application was tested.

## Origin
Written from general practice in access control for business applications; the 401, 403 and 404 semantics were checked against RFC 9110, the shared-cache rules against RFC 9111, error-body leakage against RFC 9457, merge-patch nulls against RFC 7396, and the disabled-control facts against the HTML Standard and the ARIA Authoring Practices (facts only, credited). No other source was read, and no text was copied.
🟡: never run by us. Details in [`references/origin.md`](./references/origin.md).
