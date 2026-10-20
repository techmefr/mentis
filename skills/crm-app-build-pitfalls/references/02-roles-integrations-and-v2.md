# crm-app-build-pitfalls §2 — Roles, integrations and v2

> Part 2 of `skills/crm-app-build-pitfalls`. Read it when permissions, an import, a sync or the first release
> are planned. Mostly craft knowledge; points 2, 3 and 5 carry facts from the Atomic CRM documentation (MIT), read
> 2026-10-20 (`references/origin.md`, source 1). Everything not marked as sourced is our own guidance.

1. **Visibility is a rule on the query, by role and team.** Typical shape: an admin sees all, a manager sees
   their team, a rep sees what they own or what is shared with them, a read-only role sees a chosen set.
   Symptom: the list hides records but the search, the export, the dashboard totals, the API and an email
   notification still expose them. Check: log in as a rep and compare the count in list, search, export and
   dashboard. Fix: one scoping function used by every read path, permissions named as abilities (view, export,
   merge, reassign, delete, see-amount) rather than hard-coded role names (see
   `skills/laravel-permissions-not-roles`), and a test per ability and per path.
2. **Reassignment and departure are first-class.** Symptom: a rep leaves and their accounts are invisible or
   unowned. Fix: bulk reassign with a recorded event, a rule for unowned records (a queue), and deactivating a
   user instead of deleting them so history keeps its author. The reference CRM does the same: it offers no user
   deletion, only disabling an account, to avoid losing data (source 1).
3. **Imports are idempotent and staged.** Symptom: running a CSV twice doubles the database, a column shift
   writes phone numbers into names. Fix: upload to a staging table, map columns with a preview, normalise
   keys as in §1 point 1, show counts of create, update, skip and conflict before commit, commit in one
   transaction or resumable batches, store the import id on each created row so it can be undone, and keep the
   original file. Identifiers and dates in spreadsheets break in known ways (see
   `business/spreadsheet-data-cleaning-pitfalls`).
   State which key decides update versus create (external id first, then email, never name) and which fields an import may overwrite; an empty column must not blank a field unless the user chose that.
   Never map an unrecognised value to a default silently: the reference CRM sends a deal with an empty or unknown
   stage to the first stage, ignores unknown columns, and reuses or creates a company from its name (source 1).
   Each of those hides a bad row or creates a duplicate, so list them in the preview instead. Run a long import
   in the background with a progress count and a stop control, as that documentation describes.
4. **Exports respect the same visibility and are logged.** Symptom: a departing rep exports everything. Fix:
   an export ability, the same scope as the list, a row cap or an async job with a signed expiring link, and an
   audit entry of who exported what filter. Quote or prefix cells that begin with a formula character so the
   file cannot run a formula when opened.
5. **Mail and calendar sync are matched by address and by thread, and are never trusted blindly.** Symptom: a
   synced mail attaches to the wrong contact, or a private mail from a shared mailbox lands in the CRM. Fix:
   match on normalised address, store the provider message id to stay idempotent, let the user choose which
   mail is shared, treat sync tokens as secrets in a vault, and handle token revocation by marking the
   connection broken and telling the owner, not by retrying forever. The reference CRM's inbound mail flow shows
   the duplicate risk: it finds the contact by the recipient address and creates the company and contact when
   they do not exist (source 1), so route it through the same duplicate check as §1 point 1.
6. **Inbound forms and webhooks are untrusted.** Validate and length-limit fields, dedupe through the same
   write path as a human, rate-limit the endpoint, and keep the raw payload for a short period for debugging.
   An outbound webhook carries an event id and a version so a receiver can ignore replays.
7. **Reports read a defined, dated number.** A dashboard figure names the stage set, the date field (created,
   expected close, closed), the currency and the owner scope it uses. Symptom: two screens show different
   pipeline totals. Fix: one query per metric, reused by the screen and the export, and a snapshot table if a
   historical figure must not move when stages are edited.
8. **What to split first.** Build in this order and keep each independent: accounts and contacts with duplicate
   control and the audit trail; the pipeline with defined stages and stage history; activities and tasks;
   visibility and roles; import and export; then sync and automation. Ship the first three before any
   integration: they are the data every later feature depends on.
9. **What is regretted at v2.** No tenant column; free-text statuses; merge that deleted; no unique key so
   cleanup became a project; custom fields with logic attached; permissions written as role-name checks in
   screens; no actor and event time on activities; hard-deleted users; an import with no undo; reports that
   each recompute stage meaning. Each is cheap at the first migration and expensive after data exists.
10. **Laravel and Nuxt pointers, short.** In Laravel: a unique index on the normalised key plus a model
    mutator or an action class to compute it, a global tenant scope, policies for abilities, a queued job for
    imports with a staging table, and a database transaction around merge. In Nuxt: keep list filters in the
    URL, never rely on the front to hide data, show duplicate suggestions from a server endpoint, and treat
    exports as a download from the API, not a client-side dump.
