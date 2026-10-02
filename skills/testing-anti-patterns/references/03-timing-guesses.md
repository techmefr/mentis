# testing-anti-patterns §3 — Timing guesses: the flaky-test engine

> Section 3 of `skills/testing-anti-patterns`. Read it when a test waits, polls, sleeps or advances a clock. The other sections and the guardrails stay in `SKILL.md`.

1. **Never wait for a duration; wait for the condition.** `sleep(50)` then assert is a bet on machine
   speed: it passes locally and fails in CI under load, which is the definition of flaky.
2. The correct shape is polling the thing you actually care about, with a **timeout** so a genuine
   failure fails instead of hanging, and a **sane interval** (10ms, not 1ms).
3. **Read the state fresh inside the loop.** Capturing it before the wait and re-asserting on the
   stale copy is the same bug with extra steps.
4. **A deliberate delay is only legitimate when the timing itself is the thing under test**, and then
   the test's name says so (`two_rapid_calls_keep_the_later_result`) and the delay lives in a helper named for
   its purpose — otherwise the next person deletes it or, worse, copies it. The code carries no comment
   either way.
5. Never "fix" a flaky test by increasing the sleep. That converts an intermittent failure into a slow
   suite that still fails, occasionally, for the same reason.
6. **Don't flag a virtual-clock advance as a duration wait.** `tester.pump(Duration(...))` /
   `FakeAsync` (Flutter), `vi.advanceTimersByTime` / `jest.advanceTimersByTime` (JS), and similar
   fake-timer APIs move a simulated clock inside a deterministic test zone — they don't sleep on the
   wall clock and can't flake under CI load. The anti-pattern is a *real* wall-clock wait
   (`Future.delayed`, `sleep`, `setTimeout` with no fake timer installed) used to outguess a timer or
   debounce in production code; that one still gets rewritten as a poll on observable state (e.g.
   listening for the next `notifyListeners`/state-change event) with a timeout, per point 2 above.
