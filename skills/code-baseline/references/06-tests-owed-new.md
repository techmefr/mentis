# code-baseline §6 — Tests owed by new code

> Section 6 of `skills/code-baseline`. Read it when new behaviour is added. The other sections and the guardrails stay in `SKILL.md`.

Stated here because it's language-agnostic; the doctrine of *how* to test lives in `skills/tdd` and in the
testing package it points at. What this section owns is the **debt**: what new code owes, and what does and
does not discharge it.
1. **New behaviour ships with a test** — a function, endpoint, controller, job, listener, command, model
   event, domain rule, composable, component or page. No exceptions by language.
2. **A test is done when it has been run and its output read**, not when it's written. What running catches
   that reading never does: a wrong import or missing fixture, a typoed matcher, a stale factory, a missing
   test-env variable or migration, an assertion that can never fail, and a test that passes for the wrong
   reason because nothing was actually exercised.
3. **A test that has never failed has not been shown to work.** Write it red, or break the behaviour once and
   watch it go red before trusting it. This is the same guarantee the pipeline applies to itself
   (`WORKFLOW.md` §3): a test asserting something already true is worse than no test, because it occupies
   the place where the real one would have been and reports success for ever — §8's asymmetry, arriving
   through the test suite.
4. **Fix the right side.** The test is wrong (matcher, setup, expectation) → fix the test. The code is wrong →
   the test just did its job; fix the code if scope allows, otherwise flag it. Both look right → re-read the
   test. **Never weaken the assertion to get green**: turning `toEqual(42)` into `toBeGreaterThan(0)` is a
   regression disguised as a fix.
5. **Verify an expected-failure test fails for the stated reason**, not for a setup error that happens to
   throw.
6. **Six ways to fake it, all refused**: claiming "tests added" without running them; weakening an assertion;
   skipping or deleting the failing test you just wrote; re-running until it passes by chance (an
   intermittent pass means broken, and the flake is the bug); silencing the runner (`2>/dev/null`,
   `|| true`); and asserting on a value the test itself just set (`create(['name' => 'Bob'])` then asserting
   the name is Bob tests the factory, not the code).
7. **If you genuinely can't run them** — no environment, no database, a sandbox that forbids it — **say so
   explicitly** in the closing message. An unrun test presented as passing is exactly what the pipeline's
   default-is-failure guarantee exists to catch (`WORKFLOW.md` §3, and `hooks/verify-gate.sh` refuses a
   `passes: true` claim with no read evidence).
8. **The refusal is part of the behaviour owed.** New code that can be reached by more than one kind of
   caller owes a test for the ones that must be turned away — the other tenant, the read-only role, the
   unauthenticated request, the invalid input. A change tested only as the person it was built for proves
   the feature works and says nothing about who can reach it, and that is the half that becomes an incident
   rather than a bug.
9. **A failure path is behaviour.** The named exception (§3), the error response, the rollback: each is a
   decision the code makes, so each is owed an assertion. Without one, the first refactor turns the throw
   into a returned error object and nothing anywhere goes red.
10. **A test of the implementation is not a test of the behaviour.** Asserting which collaborators were
    called, in what order, with what arguments, breaks on every refactor that changes nothing observable and
    passes when the observable result is wrong. It is the shape that makes a suite expensive enough to be
    abandoned. Assert what the caller can see.
11. **A test that reads the real clock or real randomness is not owed-satisfying**, because it will fail at
    midnight, on the first of the month, on a leap day or in the CI timezone — and a test that fails for
    reasons unrelated to the code gets muted, then deleted. Freeze both.
12. **Each test stands alone.** State left behind by another test makes the order matter, so the suite passes
    in the order it was written and fails in the order the runner chooses, which then reads as infrastructure
    trouble rather than as the coupling it is.
13. **A bugfix's test reproduces the bug first.** Written after the fix and never seen red, it asserts the
    behaviour of the code in front of it rather than the absence of the defect — so it cannot tell you
    whether the fix works, only that something now passes.
14. **The coverage bar is on the diff, not the project**: ≥80% of the lines added or changed exercised by a
    test in the same change. It works at 10% total coverage or at 100%, it can't be satisfied by tests written
    years ago, and it ratchets the total up on its own. It also gives a bugfix its regression test for free —
    the lines you touched to fix it are changed lines.
15. **Coverage is a smoke detector, not the target.** A line executed is not a line asserted, so a high
    number produced by tests that call code without checking outcomes is more dangerous than an honest lower
    one: it retires the question. Which is why point 16 exists as a list rather than as a threshold.
16. **What doesn't count as covering it**: coverage-ignore annotations added to make the number pass; an
    assertion-free test that only touches lines; snapshotting a whole rendered page to cover one helper;
    padding the change with tests for files you didn't touch; constructor-only tests of behaviourless DTOs;
    and lowering the project's CI threshold — that's a project decision, never a side effect of your change.
17. **A suite that is slow gets skipped, so its speed is part of the debt.** A test added to a change is
    added to every future change's feedback loop; one that takes a minute because it reaches a real network
    or a real sleep is a tax on everyone, and taxes get evaded locally by running a subset.
18. **Where the bar doesn't apply**: a pure refactor with no behaviour change (the existing tests should
    already cover it — if they don't, that's the finding); framework boilerplate and generated scaffolding;
    a behaviourless DTO or value object; an exception class that only carries a message; and the first commit
    in a brand-new repo, where the coverage tooling doesn't exist yet.
