# flaky-test-triage-pitfalls §3 — Quarantine

Quarantine keeps a known-flaky test running without blocking the team. It is a state with a way out; without an
owner and an end date it becomes a place where tests are forgotten.

## 3.1 The lifecycle
1. **Detect**: a CI reporter or a manual triage identifies the test as flaky, and §1.1 gives it a class
   (qa-skills lifecycle, step 1).
2. **Tag with an owner and a date.** qa-skills tags the test and asks for a ticket link and a date. This repository
   has no tracker, so the entry carries three things in text: **who owns it, the date it was quarantined, and the date
   it expires** (own guidance, replacing the ticket link).
3. **Isolate**: the quarantined test runs in a separate project or job that does not block merges (qa-skills;
   Currents).
4. **Diagnose** with §1 and fix with the fix direction of the class.
5. **Verify with a long clean run**: qa-skills requires zero failures over 50 repeated runs before release; the
   count is the author's example, and the point is a run much longer than the failure rate you saw (§1.3).
6. **Release**: remove the tag and write down what the fix was (qa-skills).
7. **If the expiry date passes without a fix, fix it or delete it.** qa-skills says "permanent quarantine is permanent
   rot" and sets 14 days as its maximum; the number is that author's, so choose your own period and write the
   date at entry time (§3.3).

```ts
test('reconnects after a dropped socket', {
  tag: ['@quarantine'],
  annotation: {
    type: 'quarantine',
    description: 'owner: realtime team; since 2026-10-15; expires 2026-11-15; race in the reconnect handler',
  },
}, async ({ page }) => {
  await expect(page.getByRole('status')).toHaveText('connected');
});
```
The shape follows qa-skills (a tag and an annotation); the description text is ours.

## 3.2 Run it without blocking, and keep running it
1. **Two Playwright projects**: one that excludes the quarantined files or tag and one that includes only them.
   Currents separates them by file name (`*.flaky.spec.ts`) and qa-skills by tag; both give the quarantine project
   its own retry count (3 in both sources, an example).
2. **The blocking job runs the stable project only**; the quarantine job is allowed to fail (qa-skills names
   `continue-on-error: true`, a GitHub Actions key; other CI systems have their own switch). If the quarantine job
   blocks merges, it will be disabled the first week.
3. **The quarantine job keeps running.** A test that is excluded and never run is dead code; the run is what shows
   that a fix worked.
4. **Verify** by checking that the stable project excludes quarantined tests and the quarantine project runs only
   them (qa-skills verification).
5. **Annotating instead of isolating**: Currents also shows a flaky annotation or a conditional skip with a reason
   for the CI environment only. Prefer the project route above, because a skipped test is not running.

## 3.3 Review the list
1. **Review the quarantine every cycle** and escalate the entries that are close to expiry (qa-skills: weekly, each
   sprint).
2. **Watch the size.** qa-skills treats more than 5 percent of tests in quarantine as a sign of a process problem
   rather than a set of test fixes; the figure is one author's example. Track the count and the age of the oldest
   entry (qa-skills metrics).
3. **A skipped test with no owner is not a quarantine.** qa-skills calls `skip` with "flaky, will fix later" dead code
   unless it is tracked or deleted. For the lint side of reasons on skipped tests, see `playwright-e2e-pitfalls` §3.5,
   and for Jest and Vitest `jest-vitest-assertion-pitfalls` §2.2.
4. **Healing must be reviewable.** qa-skills also describes automatic locator repair with a confidence score; that
   mechanism is not adopted here, and its one transferable rule is that any automatic change to a test produces
   evidence a person can review.
5. **Own guidance:** put the expiry date where a script can read it (a fixed prefix in the annotation text) so a CI
   step can fail a run that contains an expired entry.
