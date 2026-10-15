# flaky-test-triage-pitfalls §2 — Retries

A retry re-runs a failed test. It is useful as a detector, because a pass after a failure is evidence of a flake,
and harmful as a fix, because the failure it hid will come back on the day all the attempts fail.

## 2.1 A retry is a smoke alarm
1. **Retries are off by default in Playwright**, and a test that failed and then passed is reported as "flaky",
   not "passed" (Playwright retries page): "passed" means it passed on the first run, "flaky" failed first and
   passed on retry, "failed" failed every attempt.
2. **A test that needs a retry to pass is not passing.** Track the retry count and fix the cause (TestDino;
   Currents: retrying until a pass hides systemic problems, and retries are for diagnosis).
3. **qa-skills puts it sharply**: retries are a detection mechanism, and a test that passes on two of three attempts
   will eventually fail all three. The sentence is its author's reasoning, and it is consistent with the count above.
4. **Retry locally zero times and on CI a small number.** The Playwright example sets 0 locally and 2 on CI, and
   TestDino gives 0 locally and 1 to 2 on CI; the zero makes flakes visible to the person who caused them. The
   counts are examples (`playwright-e2e-pitfalls` §3.1).
5. **Raising a timeout is not a retry policy.** Currents lists increasing the global timeout to "fix" a flake as an
   anti-pattern: it hides the cause and slows every test. The same holds for `testing-anti-patterns` §3, which says
   never to raise a sleep.

## 2.2 What a retry does in Playwright
1. **A failed test discards the worker process and its browser, and a new worker continues**; with retries on, the
   new worker begins with the failed test (Playwright retries page). `beforeAll` and `afterAll` run again in the
   new worker.
2. **Own inference, worth checking in a reproduction:** because the retry starts in a fresh worker, it does not run
   after the tests that ran before it in the first worker. A failure caused by state left by those earlier tests can
   therefore pass on retry and look like a pure timing flake. Compare with `--workers=1` and repeated runs (§1.3).
3. **A test can detect that it is a retry** through `testInfo.retry`, to clear server-side state before the
   attempt (Playwright retries page). Using that to make a retry pass silently defeats the detector; use it for
   cleanup, and log that it ran.
4. **Serial mode retries a whole group together** and the page says it is usually better to make tests isolated so
   they run and retry independently (Playwright retries page; `playwright-e2e-pitfalls` §2.1).
5. **Count retried-and-passed tests**: a hook that reads `testInfo.retry` and `testInfo.status` after each test can
   log "passed on retry" for a dashboard (Currents shows such a hook; the logging target is yours to choose).

## 2.3 Retries in Python with pytest-retry
1. **Retries are per failed test**: `--retries N` globally, or a `flaky` mark per test with its own retries and
   delay; the mark overrides command-line options and global filter hooks (`pytest-retry` README, version 1.7.0).
2. **Limit retries to infrastructure failures.** The `only_on` argument retries only the listed exception types, and
   `exclude` retries everything except the listed ones; only one of the two may be used. Globally the same is set
   with a filtered-exceptions or excluded-exceptions hook in `conftest.py`, and the two hooks cannot both be defined.
   Excluding `AssertionError` means an assertion failure is never retried (README example).
3. **If a later attempt fails with an exception that no longer matches the filter, retrying stops and the test
   fails at once** (README).
4. **Fixtures are not retried.** A failing fixture is not retried, and a failure during teardown halts further
   attempts so it can be fixed; a retry runs teardown as if the test had passed, including class and module
   fixtures, so that the next attempt starts clean. Keep teardown reliable when using the plugin (README).
5. **Skipped, xfailed and xpassed tests are never retried**, and a delay between attempts is only useful when the
   failures come from an environment that clears after a few seconds (README).
6. **The README calls flaky tests unsustainable and the plugin a short-term measure** while a permanent fix is
   implemented; use its report of retried tests, which lists each failed attempt's exception, to find the cause.
7. **Reporting**: retried tests are counted both as retried and as passed or failed; stash keys expose attempts,
   outcome and duration to your own hooks; `--retry-outcome` renames the outcome string for a reporter that needs a
   different one (README).

## 2.4 What to track
1. **The flaky rate is the share of tests that passed only on retry**, published where the team sees it
   (qa-skills "done when"). Its guidance on health bands (below about 2 percent healthy, 2 to 5 needs attention, above
   5 erodes trust) is one author's, as an example.
2. **A retried test with no owner is a deferred failure.** Own guidance: the report of retried tests goes to a person
   each week, and each entry becomes a quarantine entry (§3.1) or a fix.
