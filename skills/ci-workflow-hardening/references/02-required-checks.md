# ci-workflow-hardening §2 — Required checks

A required check protects the branch only if it can neither be skipped nor be orphaned. Both failures are
silent: the merge button turns green, or never does, and nothing says why.

## 2.1 One aggregator job is the required check
1. **A job skipped by a condition reports success.** The GitHub documentation's handling table says a job
   skipped by a conditional reports "Success", and a required check counts as met. A dependency that failed
   upstream can therefore make a downstream required job skip and the merge allowed.
2. **Add a final job that depends on every job that matters and runs even when they fail.** It needs
   `if: always()`: without it, a failed dependency makes the aggregator itself skip, which reads as success.
   Its one step fails when any needed result is `failure` or `cancelled`, and also `skipped` unless a job is
   skipped on purpose (a path filter), in which case that exception is written next to the condition.
3. **Keep its name stable and make it the only required check.** Renaming it means updating the branch rule
   in the same change, or nothing merges.
4. **Prove it trips.** Fail one job on a scratch branch and confirm the aggregator is red; skip one and
   confirm it is not green.

## 2.2 Do not require matrix legs
1. **A required check is bound to a context name such as a job plus its matrix values.** Adding or
   dropping a version, or renaming a job, removes names the rule still expects, and every pull request
   waits for a status that will never be reported.
2. **Job names are unique across workflow files.** Two jobs with the same name make the context ambiguous
   for the rule.
3. **A check can only be selected after it has run once.** Run the workflow on a branch before wiring the
   rule, and spell the context exactly: a misspelt required context blocks every merge.

## 2.3 Merge queue
1. **A workflow that provides required checks must also trigger on `merge_group`.** The GitHub
   documentation says the event is separate from `pull_request` and `push` and that the workflows need it
   added as a trigger; without it the check never reports for the queued commit and the pull request waits.
2. **A path filter that skips a workflow leaves its check pending** for the queue or the pull request,
   which is why a path-filtered pipeline needs the aggregator to decide whether "nothing relevant changed"
   is a pass (§2.1.2), not a skipped required job.

## 2.4 The matrix itself
1. **Quote the versions.** An unquoted `3.10` is read as the number 3.1 by YAML and the leg runs the wrong
   interpreter; quote every version string.
2. **Decide `fail-fast` on purpose.** The sources read state that it defaults to true, which cancels the
   other legs on the first failure. Turn it off when the cross-version picture is the point, leave it on
   when you want the first red quickly.
3. **Install tools from the lockfile, not the latest.** A formatter or linter installed unpinned in a
   workflow step makes an unrelated release a red build; the project's lockfile install command, in its
   "fail if the lockfile is stale" mode, keeps CI and the laptop on the same versions (uv: `uv sync --locked`,
   which raises instead of rewriting the lockfile).
4. **Gate coverage once, not per leg.** A leg that skips a version-specific branch fails a threshold the
   combined run meets; each leg uploads its data, one job combines them and applies the threshold
   (the settings are in `python-testing-strictness` §2).

## 2.5 Events created by a workflow
1. **An event created with the default workflow token does not start another workflow run**, with the
   exception of `workflow_dispatch` and `repository_dispatch`; a pull request created or updated that way
   starts runs that need approval. A tag pushed by one workflow with that token will therefore not trigger
   the release workflow listening for tags.
2. **Chain on purpose:** trigger the next workflow explicitly with `workflow_dispatch`, or use a separate
   app credential for the push. Do not widen the default token to make it work.

## Verification
- A scratch pull request with one job failed shows the aggregator red; with one job skipped it is not green.
- Adding a version to the matrix leaves existing pull requests mergeable.
- If a merge queue is enabled, one pull request went through it end to end.
