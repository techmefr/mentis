# release-strategy-and-progressive-delivery-pitfalls §3 — Rollback and data

> Part 3 of `skills/release-strategy-and-progressive-delivery-pitfalls`. Read it when a release carries a schema
> or contract change, or rollback is claimed. The source asks whether the deployment strategy supports rollback
> and who triggers it (Azure Architecture Center, tenant updates, CC BY 4.0, read 2026-10-20). Everything else
> is own guidance and rests on no source read.

1. **Rollback is a feature, so it needs a test.** The source lists the ability to return to a previous version as
   a question to decide, not a given. Symptom: the incident starts, the documented rollback fails on a step
   nobody ran. Check: when did the procedure last run on a copy. Fix: rehearse it, date it in the release
   record, and re-run after the pipeline changes.
2. **Make data changes in steps that tolerate both versions.** Own guidance: add the new thing first (a column,
   a field, an endpoint) while old code ignores it; deploy code that writes both and reads the new; backfill;
   switch reads; only later remove the old. Symptom: a rollback finds the old code cannot read what the new
   code wrote. Fix: each step is a release of its own, and removal waits until the previous code can no longer
   be returned to.
3. **A destructive step is a one-way door.** Own guidance: dropping a column, deleting data or rewriting in
   place cannot be rolled back by redeploying code. Fix: take a restorable copy first
   (`skills/backup-restore-drill-pitfalls`), schedule the destructive step apart from the feature, and say so
   in the release record.
4. **Forward fix versus rollback is decided in advance.** Symptom: twenty minutes of argument during an incident.
   Fix: a rule such as "roll back when the cause is not understood and rollback is safe; fix forward when the
   change is small and rollback is not safe", with the person who decides named.
5. **Contracts have consumers you do not control.** Own guidance: a changed message, event or public API breaks
   consumers that cannot roll back with you. Fix: the compatible-step approach of point 2 applies to the
   contract, plus the versioning rules of `skills/api-design` and `skills/api-change-classification-pitfalls`.
6. **Queued work crosses versions.** Symptom: a job enqueued by the new version fails under the old after
   rollback. Fix: payloads stay readable by the previous version for the whole rollback window.
7. **Roll back the configuration with the code.** Symptom: code is back, a changed setting or flag state still
   expects the new version. Fix: the release record lists every setting and flag changed with the release, and
   the rollback procedure reverts them.
8. **Record the outcome.** Fix: after any rollback or halted rollout, a short note of the signal that fired, the
   time to decision and what the rule missed, feeding the stop rule (`skills/blameless-incident-review-pitfalls`).
