# admin-back-office-pitfalls §1 — Audit, impersonation and dangerous actions

> Part 1 of `skills/admin-back-office-pitfalls`. Read it when an admin schema, route group or action is
> designed. Craft knowledge, no external source read. Each point gives the symptom, the check and the fix.

1. **The admin surface is separate and re-checks on the server.** Symptom: a customer who guesses an admin URL
   gets a page, or a hidden button still works when called by hand. Check: call each admin endpoint with a
   customer token, with no token and with a staff token lacking the ability. Fix: a distinct route group and
   guard (and ideally a distinct host), staff accounts in their own table or flagged role, stronger sign-in
   (second factor, short session, optional network restriction), and an ability check in the API and the
   queued job, never only in the menu. The front hides; the server decides.
2. **Every state-changing admin action writes an audit row in the same transaction.** Symptom: a price changed
   and nobody knows by whom. Check: perform each admin action and look for exactly one row. Fix: one action
   class per operation that does the change and the audit write together (not a model hook that can be skipped
   by a bulk query, see `skills/laravel-no-observers`), and a test per route. Reads of sensitive records
   (personal data, secrets) are logged too, in a lighter row, because "who looked" is a real question.
3. **The audit log is append-only and shaped for questions.** Symptom: rows edited after the fact, or a log so
   free-form nobody can filter it. Fix: columns for actor, effective actor (differs when impersonating),
   action key from a catalogue, target type and id, tenant, before and after values of the changed fields,
   reason text, request id, source (screen, API, job) and event time. Revoke update and delete from the
   application database role; correct a mistake with a new row. Never store secrets or full documents in the
   before and after columns: store field names and redacted or hashed values.
4. **The log has a retention rule and a reader.** Symptom: the table grows without bound, or nobody can read it
   without SQL. Fix: decide retention by policy (not by us), archive to cheaper storage on schedule, give
   support a filterable view (by actor, target, action, date) and an export that is itself logged. Personal
   data inside audit rows follows the same erasure routine as elsewhere; ask the data-protection owner.
5. **Impersonation is consented, visible, scoped and limited.** Symptom: support logs in as a customer, changes
   something, and the customer is blamed. Fix: a staff ability to impersonate, a reason and ticket reference
   required, customer consent or a documented exception, a permanent banner with a one-click exit, a short
   expiry, and the audit row recording both identities for every action taken (the effective actor is the
   customer, the real actor is the staff member). Forbid inside an impersonated session: changing the password,
   email or second factor, accepting terms, payments, deleting the account, exporting all data, and starting a
   nested impersonation. Notify the customer after the session when policy says so.
6. **Impersonation never reuses the customer's credentials.** Symptom: support knows or resets the customer's
   password. Fix: mint a separate session carrying the real actor id, revoke it on exit or expiry, keep it out
   of "remember me", and never show customer secrets (tokens, API keys) in the impersonated view.
7. **Feature flags in admin are a thin screen over the lifecycle.** Symptom: a staff member flips a flag for all
   tenants at 17:00 and it is not in any log. Fix: a flag screen that lists owner, expiry, current rule and last
   change, writes an audit row per change, supports tenant or user targeting and a kill switch, requires a
   reason for a production change, and shows stale flags past expiry. Flag design, ramp and removal are in
   `skills/feature-flag-lifecycle`; do not duplicate them here. A flag must never grant a permission: access
   is an ability, rollout is a flag.
8. **Dangerous actions have friction proportional to the damage.** Symptom: delete tenant sits beside edit
   tenant with the same button. Fix: classify actions (reversible, costly, irreversible). Reversible ones need a
   toast with undo. Costly ones need a confirm dialog naming the target and the count. Irreversible ones need a
   typed confirmation of the target's name, a second approver or a delay window, a dry run that reports what
   would change, and an archive-first default (see `skills/laravel-no-cascade-delete`). Place them away from
   routine actions, and name the button for the effect ("Delete 214 invoices"), not "OK".
9. **Bulk operations are previewed, capped, resumable and undoable.** Symptom: "select all" plus "archive"
   hits 40 000 rows when the user meant one page, the request times out halfway and the state is unknown.
   Check: run a bulk action on a filter matching more than the cap, kill the worker mid-run and run it twice.
   Fix: freeze the selection as a set of ids or a filter snapshot at submit, show the matched count and a
   sample before confirming, refuse above a cap unless a higher ability is held, run as a queued job processed
   in batches with a progress record (see `skills/laravel-idempotent-jobs`), record per-row outcome (done,
   skipped, failed with reason), make a rerun skip finished rows, and write one parent audit row linked to
   child rows. Offer undo when the change is reversible by storing the previous values.
10. **Select-all means the filter, not the page, and the user is told which.** Symptom: the header checkbox
    selects 25 rows but the action applies to 25 000, or the reverse. Fix: show "25 selected on this page,
    select all 25 000 matching" as an explicit second step, send the filter plus an exclusion list to the
    server, and re-evaluate permissions per row there (see `skills/data-table-ui-pitfalls`).
11. **Admin edits go through the same validation as customer edits.** Symptom: a staff form writes a state the
    public app would refuse, and later code breaks on it. Fix: one domain action per operation called by both
    surfaces; where staff may legitimately override a rule, make it an explicit, audited override with a reason,
    not a skipped validation.
12. **Admin lists are queries on production, treated as such.** Symptom: an unbounded search in the console
    takes the database down. Fix: pagination with a cap, indexed filters only, no free `LIKE '%x%'` on large
    tables (see `skills/filters-search-and-saved-views-pitfalls`), read replicas where available, and a
    statement timeout for admin queries.
