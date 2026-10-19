---
name: testing-anti-patterns
description: "Use when writing or reviewing tests, the specific ways a test suite reports safety it doesn't have: mock theatre, timing guesses, tests that cannot fail, state leaking between tests, regressions typical of code written by an agent. Complements tdd (which says write tests first) by covering what makes a written test worthless."
---

# testing-anti-patterns

Step 5 of the pipeline (`WORKFLOW.md`), and a review lens at step 8. `tdd` says tests come first;
`skills/run-generated-tests` says a written test has to actually run, scoped; this block is about
the tests that exist, run, pass, and prove nothing.

Every pattern here has the same shape: **the suite is green and the safety is imaginary**. That's
worse than having no tests, because nobody checks manually anymore.

## When
While writing tests, and when reviewing a diff that adds them. Also when a bug reaches production
through code that had coverage: one of these is usually why. And after any fix: §6 and §8 say where the
regression test goes and how to show it can fail.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; a section read is a section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Mock theatre: testing the double instead of the code | a double is introduced, or a test asserts that something was called | [`01-mock-theatre.md`](./references/01-mock-theatre.md) |
| 2 | Mock without understanding what you removed | a collaborator is replaced, or a double is built from memory of a payload | [`02-mock-without-understanding.md`](./references/02-mock-without-understanding.md) |
| 3 | Timing guesses: the flaky-test engine | a test waits, polls, sleeps or advances a clock | [`03-timing-guesses.md`](./references/03-timing-guesses.md) |
| 4 | Test-shaped code in production | a reset helper, a test hook or an internal getter is added to a production class | [`04-test-shaped-production-code.md`](./references/04-test-shaped-production-code.md) |
| 5 | Tests that cannot fail, and defaults that pass for data | a negative test, a claim in a test title, a fallback value or a fixture is written | [`05-cannot-fail.md`](./references/05-cannot-fail.md) |
| 6 | Regressions typical of code written by an agent | a bug is fixed, a diff written in one pass is reviewed, or the author is the only reviewer | [`06-regressions-in-agent-written-code.md`](./references/06-regressions-in-agent-written-code.md) |
| 7 | Isolation, order dependence, finding the polluter | a test passes alone and fails in the suite, a run leaves state behind, or parallelism and random order are switched on | [`07-isolation-and-pollution.md`](./references/07-isolation-and-pollution.md) |
| 8 | What a test is for | a test is written, named, edited after a failure, skipped or pruned | [`08-what-a-test-is-for.md`](./references/08-what-a-test-is-for.md) |

## Output / checkpoint
For the tests added: no assertion whose subject is a mock, no bare duration wait, mocks justified
against the real shape, no test-only method left in production code, no test that leaves state behind,
every test able to name the break it catches. If a test can't fail, it isn't finished (see `dozer`, which
owns this while writing).

## Guardrails
- **Never weaken a test to make it pass.** Loosening an assertion, widening a matcher or deleting a
  case converts a real signal into a green tick.
- Never mock "just to be safe": each double is a piece of reality removed, and it has to be justified.
- A flaky test is a **bug report**, not noise to be retried. Retrying it hides either a race in the
  test or a race in the code, and you can't tell which without looking.
- A coverage percentage is a map of what no test touched, never a goal; this block sets none.

## Origin
Rewrite of `testing/testing-anti-patterns` and `testing/condition-based-waiting` from a market skills
repository, plus, since 2026-10-02, the sections on regressions typical of agent-written code, on
isolation and on the purpose of a test, from a read of two further public repositories. The full
provenance, the dogfooding record and the refresh log are in [`references/origin.md`](./references/origin.md).
Read it when checking whether a rule is still current, not when applying one.
