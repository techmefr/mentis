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
9. **Client caches keep the bad version after a rollback.** Own guidance. Symptom: the fix or revert is live, and
   returning visitors still see the broken page, because a service worker, a browser cache or a CDN edge serves
   the old shell first and updates in the background, or only on a second load or a restart of the tab. Check:
   list every layer that can hold a copy (service worker and its update rule, cache headers on pages and on
   hashed assets, CDN time to live, a stale-while-revalidate rule) and for each, how long a visitor can stay on a
   version after it is replaced. Fix: keep the HTML and the worker script short-lived or revalidated, let the
   worker take over at once when a new version is installed (MDN service worker guide, read 2026-10-20: a new
   worker waits while pages controlled by the old one stay open and activates only when none is left, unless it
   asks to skip waiting, and it may then claim the open pages; old caches are removed in the activation step), give the worker a way to be disabled by a new
   release, and put the purge or the expiry time of the CDN in the release record.
10. **Say how the rollback and the forward fix reach users, in one line.** Own guidance. Symptom: a one-person
    project with no written rule, so the choice is made under stress. Check: the release record says whether the
    default is revert-and-redeploy or fix-forward, how long that takes through the pipeline end to end, and who
    decides. Fix: when the pipeline is slow, add a shorter documented path (re-run an older successful run, or
    redeploy a stored artefact), and rehearse it once (§3.1).
11. **The minimum for one environment with no data.** Own guidance. Where the project has one exposure unit, the
    release strategy reduces to four lines in the release record: the artefact is built once and published from
    that build (§1.3), the live address is checked after publishing (§2.10), the rollback or forward-fix rule is
    written (§3.4, §3.10), and the client caches that hold the old version are listed with their expiry (§3.9).
    Everything else in this block is not applicable until a second environment, tenant or data store exists.
