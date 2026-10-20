# release-strategy-and-progressive-delivery-pitfalls §1 — Branching and the release path

> Part 1 of `skills/release-strategy-and-progressive-delivery-pitfalls`. Read it when a branching model or a
> merge-to-release path is chosen or reviewed. Own guidance from general craft knowledge, except point 9 and 10, which
> cite the GitHub Actions documentation on concurrency (CC BY 4.0, read 2026-10-20, restated in our words). Re-read
> before relying on any claim about a given tool.

1. **Keep the shared line releasable.** Symptom: the main line is red for a day, nobody ships, fixes pile up
   behind the break. Check: how long was it red last month, and who was blocked. Fix: a failing change is fixed
   or reverted first, and the gate that merged it is repaired.
2. **Short-lived branches, merged often.** Symptom: a branch is weeks old, its merge needs a meeting, its diff is
   unreviewable. Check: age of every open branch and size of its diff. Fix: slice the work so each slice merges
   alone, and hide unfinished behaviour behind a flag (`skills/feature-flag-lifecycle`) rather than behind a
   branch.
3. **Build once, promote the artefact.** Symptom: staging passed, production fails with the same commit.
   Check: is production built from a fresh build, or from the very artefact staging ran. Fix: one build, one
   identifier (digest or version), environment differences only in configuration supplied at deploy time.
4. **Configuration is not code that changes per environment.** Symptom: a hotfix edits a file differently in
   each environment. Fix: one configuration shape, values injected, and a diff of effective configuration
   between environments reviewed on every release.
5. **Release branches only when you support more than one version.** Symptom: a release branch exists for a
   service with one deployed version, and fixes are cherry-picked twice. Fix: release from the main line;
   keep a branch per supported version only when customers really run several, and port fixes deliberately.
6. **Name the path from merge to users in one sentence.** Symptom: nobody can say which step is manual or who
   approves it. Check: write it down. Fix: each step has an owner, a gate and an evidence trail; a manual
   approval gate states what the approver must look at, not only that they click.
7. **Environment parity is a list, not a hope.** Symptom: a bug appears only in production because of data
   volume, a missing job or a different dependency version. Fix: list the known differences, decide for each
   whether it matters, and add the check that would catch it before production.
8. **A hotfix uses the normal path, faster.** Symptom: urgent changes bypass tests and arrive broken. Fix: the
   same pipeline with a smaller scope, never a side door, and the fix lands on the main line the same day.
9. **A deploy job can cancel itself.** Symptom: a pipeline setting that cancels an in-progress run
   when a newer one starts is applied to the job that publishes, so a deploy that was half done is stopped and the
   live site is left on neither version. Check: read the concurrency setting of the publishing job, and ask what
   state the live site is in if that job is killed at any step. Fix: queue publishing runs instead of cancelling
   them, and keep cancellation for the test jobs, which are safe to stop. Where the platform serves the new version
   only once the whole artefact is uploaded, say so and treat the risk as low rather than skipping the check.
   Confirmed (GitHub Actions concurrency page): in one concurrency group only one run goes at a time, and the
   cancel-in-progress option lets a new run cancel the running one, which can leave an environment partly deployed;
   the symptom, check and fix are ours.
10. **A queued deploy can be replaced, so an intermediate release may never ship.** Symptom: two merges land
    minutes apart, the first never reaches production, and its changelog entry or migration step is missing from
    the live system. Cause: in the platform's default queue only one run may wait, and a newer waiting run
    replaces the older one (GitHub Actions concurrency page: one pending run per group, a newer pending run
    cancels the existing pending one; an option allows up to 100 waiting runs in order, and cannot be combined
    with cancelling the running one). Check: read the concurrency setting of the publishing job and ask what
    happens to the second of three quick merges. Fix: choose on purpose between keeping every release in order and
    shipping only the latest, write which one this project means, and make any step that must happen once per
    release (a migration, a notification) independent of whether its run was replaced.
