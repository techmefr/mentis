# admin-back-office-pitfalls §2 — Roles, support workflows and v2 regrets

> Part 2 of `skills/admin-back-office-pitfalls`. Read it when staff permissions, support tooling or the first
> release are planned. Craft knowledge, no external source read.

1. **Every staff member has a named account and least privilege.** Symptom: a shared admin login, nobody
   accountable, a departed employee still able to sign in. Fix: individual accounts with second factor,
   abilities rather than a single "admin" flag (see `skills/laravel-permissions-not-roles`), a small number of
   roles built from abilities (support read, support edit, finance, super admin), a review of who holds what on
   a schedule, and deactivation (never deletion) on departure so the audit rows keep their author. Break-glass
   access for emergencies is time-boxed, logged and reviewed afterwards.
2. **Support sees what it needs, not everything.** Symptom: first-line support can read payment details or full
   documents. Fix: field-level masking by ability (last digits only, redacted body) as in
   `skills/field-and-row-permission-ui-api-pitfalls`, an explicit "reveal" action that logs a read row, and
   tenant scoping that applies to staff too unless the role is global.
3. **Two-person rule for money and access changes.** Symptom: one person refunds, grants a role and approves
   their own request. Fix: an approval record for refunds above a policy threshold, role grants and data exports;
   the requester cannot approve; both are audited. The threshold is policy, set by the business.
4. **Support actions tell the customer.** Symptom: a staff member changes an email or closes an account and the
   customer finds out when they cannot sign in. Fix: send a notification for identity, security and billing
   changes made by staff, through the normal notification path (see `skills/laravel-mail-via-notifications`),
   with the staff action referenced but not the staff member's name unless policy says so.
5. **Internal notes are separate from customer-visible text.** Symptom: an internal remark appears in an email
   or an export. Fix: a distinct note type with its own visibility, never rendered in customer templates, and
   excluded from the customer's data export unless the data-protection owner decides otherwise.
6. **Admin search is fast, scoped and safe.** Symptom: support pastes an email and gets nothing because of
   case, or gets another tenant's user. Fix: normalised lookup keys (as in `skills/crm-app-build-pitfalls`
   §1, point 1), tenant-aware results, a result cap, and a jump from an audit row to the target record.
7. **Admin screens are accessible and consistent too.** Staff work in them all day. Keep the same table, form
   and error patterns as the customer app (see `skills/data-table-ui-pitfalls`), keyboard navigation, and no
   color-only status.
8. **Operational dashboards read dated numbers and say how fresh they are.** Symptom: two screens disagree.
   Fix: one query per metric reused by screen and export, a visible "as of" time, and a clear separation
   between live figures and nightly aggregates (see `skills/dashboard-ui-pitfalls`).
9. **What to split first.** Build in this order and keep each independent: staff accounts, second factor and
   abilities; the audit log and its catalogue; read-only record views with masking; reversible edits;
   dangerous actions with confirmation levels; bulk operations; impersonation; then flag screens, approvals
   and dashboards. Impersonation comes late on purpose: it needs the audit log, the banner and the forbidden
   list to exist first.
10. **What is regretted at v2.** One shared admin password; admin pages on the same session as the public app;
    audit written by hooks that bulk queries skip; mutable audit rows; impersonation without a banner or a
    forbidden list; "select all" that meant the whole table; hard-delete buttons next to edit buttons; flags
    that granted permissions; permissions hidden in the menu only; no retention rule so the log became the
    biggest table. Each is cheap at the first migration and expensive after the data and the habits exist.
11. **Laravel and Nuxt pointers, short.** In Laravel: a dedicated guard and route group for staff, policies and
    gates for abilities, an action class per admin operation that writes the audit row inside one database
    transaction, queued jobs with batches and a progress table for bulk work, and a separate database role for
    the audit table with insert and select only. In Nuxt: a separate layout or app for the admin, route
    middleware as convenience only, a persistent banner component driven by the session's effective-actor flag,
    and confirmation dialogs that require the typed target name before enabling the button.
