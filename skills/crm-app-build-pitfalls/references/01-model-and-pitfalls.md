# crm-app-build-pitfalls §1 — Minimal model and its pitfalls

> Part 1 of `skills/crm-app-build-pitfalls`. Read it when a schema or a write path is designed. Mostly craft
> knowledge; points 1 and 5 carry facts from the Atomic CRM documentation (MIT), read 2026-10-20 and restated in
> our words (`references/origin.md`, source 1). Everything not marked as sourced is our own guidance. Each point
> gives the symptom, the check and the fix.

1. **Duplicates are stopped at write time.** Symptom: the same company and the same person exist several
   times, each with part of the history. Check: create the same contact twice, once with different case,
   spacing or a plus-tag in the email. Fix: store a normalised key beside the display value (lowercased and
   trimmed email, digits-only phone with country, a company key from website domain or registration number),
   put a unique index on the key within the tenant, and on collision offer "open existing" or "merge", never
   silently create. Treat a name match alone as a suggestion, not a key. Compute the key for every address and phone a contact
   holds, not only the first: the reference CRM stores several typed emails and phones per contact. The same
   documentation lists three usual causes of duplicates, which are the three paths to guard: overlapping CSV
   imports, mail that creates a contact for an unseen address, and manual entry without a lookup (source 1).
2. **Minimal model, each entity with one owner.** Account (a company or household), contact (a person, possibly
   linked to several accounts through a role record), deal (an opportunity on one account, with an amount, a
   currency, a pipeline and a stage), activity (a call, mail, meeting or note attached to contact, account or
   deal), task (a due, assignable follow-up), user, team. Give each record an owning user and a creating user.
   Symptom of skipping the role record: a contact who changes company is edited in place and the old company
   loses its history.
3. **Statuses are an enumeration with defined transitions.** Symptom: "Qualified" means three things to three
   people and a deal jumps to "Won" with no amount. Check: list stages and, for each, the entry condition, the
   exit condition and the allowed next stages. Fix: a stage table or enum owned by the pipeline, a transition
   check in one place (see `skills/laravel-recognise-state-machine-or-pipeline`), a required reason when a deal
   closes lost, a required amount and date when it closes won, and the stage history kept as rows, not
   overwritten. Do not let users add stages without a migration policy for open deals.
4. **Lifecycle of a lead is not a deal stage.** Symptom: a lead counted as pipeline value. Fix: keep person
   status (new, contacted, qualified, disqualified) separate from deal stage, and convert explicitly: the
   conversion creates or links an account, a contact and a deal in one transaction and records the source.
5. **Merge keeps history and leaves a redirect.** Symptom: after a merge the old record's emails, deals and
   tasks vanish, or an old link returns a 404. Check: merge two records that each have deals and notes. Fix: in
   one transaction repoint every child to the survivor, resolve field conflicts by a visible rule (survivor
   wins unless empty, or the user picks), keep the absorbed record as archived with a pointer to the survivor,
   and write a merge event listing who, when and what moved. Merge must also be reversible within a window or
   at least reconstructable from the event. The reference CRM is smaller than this: it moves the source contact's
   data to the target, keeps the target's value when both have one, and deletes the source (source 1). The
   conflict rule is confirmed as a common choice; the archive, redirect and event are our own guidance, because a
   deleted source leaves old links and history with no trace.
6. **The timeline is append-only.** Symptom: a salesperson edits or removes a logged call and a dispute cannot
   be resolved. Fix: activity rows and stage changes are inserted, never updated; a correction is a new entry
   referencing the old one; record the actor, the time the event happened and the time it was written
   (they differ for logged calls and synced mail). Field-level audit of sensitive fields (owner, amount, stage,
   consent) is a separate change log with old and new value.
7. **Consent and source are fields with a history.** Symptom: nobody can say why a person is mailed or who
   opted out. Fix: store the channel, the state, the date, and the evidence or source for each consent as rows,
   keep one suppression list that every sending path reads, and keep it when a contact is merged or archived.
   Method only; what counts as valid consent is a legal question, not legal advice here.
8. **Archive is the default, hard delete is a controlled job.** Symptom: deleting an account removes its deals,
   notes and reports, and totals change retroactively. Fix: an archived flag or timestamp hidden by default and
   restorable; foreign keys that restrict, not cascade (see `skills/laravel-no-cascade-delete`); a separate,
   audited erasure routine for a person's erasure request that removes or anonymises personal fields while
   keeping the non-personal deal record, run by a role and logged. Soft delete alone is not erasure: the data
   is still there, and unique indexes can collide with a "deleted" row, so decide whether the unique key
   includes the archive state. What law requires erasure and when is for the data-protection owner.
9. **Money has a currency and exact arithmetic.** Symptom: a pipeline total changes by cents or mixes
   currencies. Fix: integer minor units or exact decimal plus a currency code on every amount, a deal keeps its
   own currency, and any converted figure on a dashboard names the rate and its date (see
   `skills/money-arithmetic-and-rounding-pitfalls`). Weighted forecast is a calculation over stage
   probabilities that are policy, not stored truth.
10. **Custom fields are limited and typed.** Symptom: fifty free-text custom fields, half unused, no report can
    use them. Fix: typed fields (text, number, date, choice, reference), a per-entity cap, a choice list with
    stable ids so a renamed label does not rewrite history, a visible "last used" count, and promotion of a
    popular field into a real column. Never let a custom field carry a status that drives logic.
11. **Every row belongs to a tenant or team, from the first migration.** Symptom: a second customer or a second
    team needs the product and every query lacks a boundary. Fix: a tenant column (or a separate schema) on all
    tables including join tables, the boundary applied in one scope applied by default (see
    `skills/laravel-tenant-context-by-default` and `skills/laravel-scope-dont-check-after-fetch`), the key
    uniqueness defined within the tenant, and file storage and search indexes partitioned the same way.
12. **Time and identity are stored precisely.** Store timestamps in UTC with the user's zone applied at display,
    store a due date as a date when it has no time, and give every record a stable internal id that is never
    shown as the business key. Symptom of ignoring it: a task due "tomorrow" appears overdue for a user in
    another zone.
