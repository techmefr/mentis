---
name: run-generated-tests
description: 'Use whenever a test is written or modified, in any stack — after generating or scaffolding it, execute it, read the output, and iterate until it passes for the right reason (or fails for the right reason, for a deliberately-failing test). Scope the run to what was generated — the new test, at widest the file or class it lives in. The project-wide suite is CI''s job, not the session''s, and never runs silently.'
---

# run-generated-tests

Step 5/6 of the pipeline (`WORKFLOW.md`) — a companion to `tdd` and `code`, and a review lens at
`review` (8). `tdd` says tests come first and start red; `testing-anti-patterns` says what makes a
written test worthless; this block says a generated test is not done until it has actually run, and
draws the line at *how much else* runs with it.

## When
After writing or modifying any automated test — unit, feature, integration, widget, end-to-end — in
any language or runner. Also when reviewing a diff that adds tests, to check the closing message
claimed a run rather than a guess.

## Steps

### 1. Run it, scoped to what you generated
Execute the new or changed test with the runner's own filter — a name, a path, a `-t`/`-run`/
`--filter` flag. Never launch the project's bare full-suite command (`pytest`, `go test ./...`,
`pnpm test`, `php artisan test` with no filter, `dotnet test` with no filter) as part of writing a
test — that command belongs to CI. At widest, when production code changed alongside the test, widen
one notch: the file or class whose behaviour changed, not the project.

### 2. Read the output, not the colour
A stack trace, a diff, or "expected X, got Y" is the signal — don't guess at the cause. **A skipped
test is not a passing test.** `3 passed, 1 skipped` is green, and the one you just wrote may be the
skipped one: read the counters and confirm your test's name is in the *passed* count, because an
environment guard the suite never satisfies (a driver check, an unset env var) leaves it dead inside
a run that still prints green.

### 3. Iterate on the right side
When it fails, decide whether the test's expectation is wrong or the code is: fix that side, never
the other one to force a match. Repeat until the result is green for a "should pass" test, or red for
the *expected* reason for a deliberately-failing one — a setup error earlier in the test is not the
same failure as the one the test claims to assert.

### 4. Stop at that scope; say so
Once the scoped run is green, the turn is done — widened one notch at most, per step 1. Don't launch
the broader suite "to be sure": it is slow, it buries the one output line that matters under hundreds
of unrelated ones, and most of what it turns up is not yours to fix (a pre-existing failure, a flaky
neighbour, a missing local service). State in the closing message that the scoped result is what you
verified and the full suite is what CI verifies — never let a scoped green be read as a claim about
the whole project.

### 5. The three cases where the full suite genuinely is yours to run
- **The user asks for it.** Run it, and report pre-existing failures separately from the one you own.
- **The project has no CI running tests.** Nothing else will ever run the suite; run it once and say
  why.
- **You changed shared test infrastructure** — a base test case, a global fixture/`conftest`, a
  factory or seed data half the suite boots through. A scoped run can't show that blast radius.
  Announce it before launching a long run, or push and let CI answer instead.

## Output / checkpoint
The generated test's own run, read and green (or red-for-the-expected-reason) — reported with the
scoped command used and the counters read. `tdd`'s `test-results.json` line for the matching
criterion flips from `{ passes: false }` only on this evidence. Diff-coverage or coverage-floor checks
(`tdd`'s target from `test-casebook`, where installed) are read the same way: scoped to the changed
files at the "I think I'm done" moment, not from a full-suite coverage run.

## Guardrails
- **Never report "tests added" without having run them.** If the environment genuinely can't execute
  them (no DB, no reachable external service, a destructive/side-effecting test), say so explicitly
  and name the command for the user to run — don't report completion.
- **Never weaken a test to make it pass**, and never delete or skip a failing test you just wrote —
  both are `testing-anti-patterns`' territory, restated here because they're exactly what "iterate
  until green" is not license to do.
- **Never launch the bare full-suite command as part of writing a test.** That's CI's command; typing
  it in the session is the anti-pattern this block exists to prevent.
- **Never silently fix a pre-existing failure a wider run surfaced.** Name it in the closing message
  and leave it — fixing it hides a regression nobody asked you to touch inside your diff.

## Origin
Mined from an org skill catalogue's `global` (cross-stack) plugin's `run-generated-tests` skill,
reworked 2026-09-17 to add the scoping half — de-identified and rewritten in the house voice. The
core "a test isn't done until it's run" obligation already matches this repo's own default-is-failure
guarantee (`WORKFLOW.md` §3) and `tdd`'s default-FAIL contract; what the source added and this block
keeps is the second half nothing here stated yet: the full local suite is the expensive, low-signal
half of verification, already automated end to end by CI, and re-running it in the session mostly
surfaces failures that aren't the task's to fix. The three carve-outs (user asks, no CI, shared test
infrastructure changed) are kept from the source almost as-is — they're a short, complete list, not
house-specific detail. Left out: the source's per-language command table (`php artisan test
--filter=`, `pytest ...::test_name`, `go test ./... -run`, …), which is `test-casebook`'s own
per-stack guides' job where that family is installed, and a generic restatement here would drift from
whichever runner a given stack actually uses. Written 2026-09-29.
