---
name: flaky-test-triage-pitfalls
description: "Use when a test passes and fails without a code change, or a suite uses retries or a quarantine: classifying the flake before fixing it (timing, data, order, environment, time sensitivity, visual, external service), reproducing it (repeat runs, one worker, CI-like conditions, a replayable random seed in pytest), what a retry means and how to track retried tests (Playwright, pytest-retry exception filters), and the quarantine lifecycle with an owner and an expiry date instead of a ticket."
---

# flaky-test-triage-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), and the step that reads a red or intermittent CI run. The three sections
share one premise: **a flake has a cause in one of a few classes, each with a different fix, and a retry or a
longer sleep treats none of them**. The rule against fixed waits is in `testing-anti-patterns` §3, and Node test
hygiene (random order, realistic data) in `prisma-ops-and-test-hygiene` §2; neither is repeated. The
tool-specific traps are in `playwright-e2e-pitfalls`, `testing-library-query-pitfalls` and
`jest-vitest-assertion-pitfalls`. The text is stack-neutral; Playwright and pytest are the worked examples.

## When
- A test fails intermittently, only in CI, only in parallel, or only at certain times.
- Deciding whether a suite may retry, how to report retried tests, or whether to quarantine a test.
- A quarantine or a list of skipped tests has grown and nobody owns it.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Classes of flake, the questions that tell them apart, reproducing, a replayable seed, environment checks | a test is intermittent and the cause is unknown | [`01-classify-and-reproduce.md`](./references/01-classify-and-reproduce.md) |
| 2 | What a retry is, how Playwright and pytest-retry treat it, tracking retried tests | retries are configured or a test needs them | [`02-retries.md`](./references/02-retries.md) |
| 3 | Quarantine lifecycle, owner and expiry, non-blocking runs, size signals | a flaky test is isolated or a quarantine is reviewed | [`03-quarantine.md`](./references/03-quarantine.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the flaky test was run many times before any change and failed at
least once (§1.3), the class was written in the fix's message and the fix matched it (§1.1), the same test passed
every run of a repeat batch after the fix (§3.1), and each quarantined test had an owner and a date (§3.1). A
flake that "stopped happening" without a reproduction is not fixed.

## Guardrails
- Never fix a flake before naming its class (§1.1).
- Never trust a fix that was not preceded by a reproduction and followed by a long clean run (§1.3).
- Never let a retry be the only response to a failure; a test that needed one is reported and tracked (§2.1).
- Never retry an assertion failure by default; limit retries to named infrastructure failures (§2.3).
- Never quarantine a test without an owner and an expiry date (§3.1).
- Never let the quarantine run block merges, and never stop running it (§3.2).
- This block states what the sources describe at the repository commits in
  [`references/origin.md`](./references/origin.md). The thresholds in it (percentages, days, run counts) are one
  author's or one page's examples, not measurements for your suite. Nothing was run while writing it.

## Origin
Rewritten from the qa-skills `test-reliability` skill (MIT), the Playwright retries page (Apache-2.0), the
Currents flaky-tests page (MIT), the `pytest-randomly` and `pytest-retry` READMEs (MIT) and the TestDino
common-pitfalls page (MIT), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
