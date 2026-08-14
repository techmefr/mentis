# code-baseline §6 — Tests owed by new code

> Section 6 of `skills/code-baseline`. Read it when new behaviour is added. The other sections and the guardrails stay in `SKILL.md`.

Stated here because it's language-agnostic; the doctrine of *how* to test lives in `skills/tdd` and in the
testing package it points at.
1. **New behaviour ships with a test** — a function, endpoint, controller, job, listener, command, model
   event, domain rule, composable, component or page. No exceptions by language.
2. **A test is done when it has been run and its output read**, not when it's written. What running catches
   that reading never does: a wrong import or missing fixture, a typoed matcher, a stale factory, a missing
   test-env variable or migration, an assertion that can never fail, and a test that passes for the wrong
   reason because nothing was actually exercised.
3. **Fix the right side.** The test is wrong (matcher, setup, expectation) → fix the test. The code is wrong →
   the test just did its job; fix the code if scope allows, otherwise flag it. Both look right → re-read the
   test. **Never weaken the assertion to get green**: turning `toEqual(42)` into `toBeGreaterThan(0)` is a
   regression disguised as a fix.
4. **Verify an expected-failure test fails for the stated reason**, not for a setup error that happens to
   throw.
5. **Six ways to fake it, all refused**: claiming "tests added" without running them; weakening an assertion;
   skipping or deleting the failing test you just wrote; re-running until it passes by chance (an
   intermittent pass means broken, and the flake is the bug); silencing the runner (`2>/dev/null`,
   `|| true`); and asserting on a value the test itself just set (`create(['name' => 'Bob'])` then asserting
   the name is Bob tests the factory, not the code).
6. **If you genuinely can't run them** — no environment, no database, a sandbox that forbids it — **say so
   explicitly** in the closing message. An unrun test presented as passing is exactly what the pipeline's
   default-is-failure guarantee exists to catch (`WORKFLOW.md` §3, and `hooks/verify-gate.sh` refuses a
   `passes: true` claim with no read evidence).
7. **The coverage bar is on the diff, not the project**: ≥80% of the lines added or changed exercised by a
   test in the same change. It works at 10% total coverage or at 100%, it can't be satisfied by tests written
   years ago, and it ratchets the total up on its own. It also gives a bugfix its regression test for free —
   the lines you touched to fix it are changed lines.
8. **What doesn't count as covering it**: coverage-ignore annotations added to make the number pass; an
   assertion-free test that only touches lines; snapshotting a whole rendered page to cover one helper;
   padding the change with tests for files you didn't touch; constructor-only tests of behaviourless DTOs;
   and lowering the project's CI threshold — that's a project decision, never a side effect of your change.
9. **Where the bar doesn't apply**: a pure refactor with no behaviour change (the existing tests should
   already cover it — if they don't, that's the finding); framework boilerplate and generated scaffolding;
   a behaviourless DTO or value object; an exception class that only carries a message; and the first commit
   in a brand-new repo, where the coverage tooling doesn't exist yet.
