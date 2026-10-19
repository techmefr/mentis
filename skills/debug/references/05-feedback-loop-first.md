# debug §5 — The feedback loop comes before any hypothesis

> Section 5 of `skills/debug`, continuing its inline sections 1 to 4. Read it when a bug, a failure or a
> slowdown shows up and nothing yet runs red on it, when a repro is long or flaky, and when debug logs are about
> to be added. 🟡: rewritten from documentation, not yet run on a real bug.

**How this fits the single-hypothesis rule.** `SKILL.md` §1 says: reproduce, then state one hypothesis and
verify it before changing anything. This section is the strong form of "reproduce" and a precondition of that
rule, not a competing method. Hypotheses, instrumentation and the fix all consume the loop's verdict; without
it each of them is a guess you cannot score. The one-hypothesis-per-fix-attempt rule and the stop after three
failed attempts are unchanged.

## Build the loop first

1. **A loop is one command that goes red on this bug.** A pass/fail signal you can run on demand, tight enough
   that you run it many times. Spend more effort here than anywhere else: if the loop is good, locating the
   cause is mostly mechanical; if there is none, reading code will not substitute for it.
2. **The completion criterion, all four.** Phase one ends when you can name one command that you have already
   run at least once, and that is: **red-capable** (it drives the real code path and asserts the symptom the
   report describes, so it can fail on this bug and pass when fixed; "runs without crashing" is not that),
   **deterministic** (same verdict each run), **fast** (seconds), and **runnable without a person**.
3. **No hypothesis before that command exists.** If you catch yourself reading code to build a theory first, stop
   and go back to the loop. A theory built without a signal to test it against is the failure this section
   prevents.
4. **Ways to build one, in roughly this order of preference.** A failing test at whatever seam reaches the bug
   (unit, integration, end to end); a scripted HTTP call against a running dev server; a command-line run on a
   fixture input, diffing the output against a known-good one; a headless-browser script asserting on DOM,
   console or network; a replay of a captured request, payload or event log through the code path alone; a
   throwaway harness booting the smallest slice of the system around one function call; a property or fuzz loop
   for "sometimes wrong output"; a bisection harness when the bug appeared between two known states, so the
   state-check can be automated and run unattended; a differential run of the same input through two versions
   or configs; and last, a script that drives a person through the manual steps and captures their answers, so
   the loop is still structured. Take the first rung that reaches the bug.
5. **Tighten the loop once you have one.** Faster (cache setup, skip unrelated initialisation, narrow the
   scope), sharper (assert on the exact symptom, not on "did not crash"), more deterministic (pin the clock, seed
   the random source, isolate the filesystem, freeze the network). A thirty-second flaky loop is barely better
   than none; a two-second deterministic one is the working tool.
6. **A non-deterministic bug needs a higher reproduction rate, not a clean repro.** Run the trigger a hundred
   times, in parallel, under stress, with the timing window narrowed. A bug that fails half the time can be
   debugged; one that fails one time in a hundred cannot, so keep raising the rate until it can.
7. **When no loop can be built, say so and stop.** List what you tried and ask for one of: access to an
   environment where it reproduces, a captured artefact with secrets redacted (a request log, a dump, a
   recording with timestamps), or permission to add temporary instrumentation where it happens. Do not carry on to
   hypotheses without a loop.
8. **Redact before you show anything.** A command, its output or a captured artefact can carry a credential or an
   auth header: replace every secret with a visible placeholder and quote only the lines that carry the signal.
   Build the loop against environment variables so the credential never enters what is shown. If the redacted
   output is too thin to diagnose from, say that and ask.

## Reproduce, then minimise

9. **Confirm the loop shows the reported failure, not a neighbour of it.** Same symptom as the report, across
   several runs (or at the stated rate for a flaky bug), with the exact message, wrong value or timing captured so
   the fix can be checked against it later. A loop that goes red on a different failure produces a fix for the
   wrong bug.
10. **Shrink the repro to the smallest scenario that still goes red.** Remove inputs, callers, configuration,
    data and steps one at a time, re-run the loop after each removal, and keep only what the failure depends on.
    It is finished when taking out any single remaining element turns the loop green. A minimal repro leaves less
    to suspect and becomes the regression test.

## When more than one cause is plausible

11. **Rank candidates only when the failure is ambiguous or intermittent, and test them one at a time.** If the
    loop leaves several plausible causes, write them down ranked, each as a falsifiable prediction ("if X is the
    cause, changing Y makes it disappear"). A candidate whose prediction you cannot state is a hunch: sharpen it
    or drop it. Then test them **one per attempt**, changing one variable, which keeps §1's single-hypothesis
    discipline and the three-attempts stop. Ranking does not license changing several things at once. For an
    ordinary bug with a clear first suspect, skip it. (The ranked-list step comes from one source and the single
    hypothesis from another; keeping both under the one-variable rule is our reconciliation, recorded in
    `origin.md`.)

## Instrument, fix, clean up

12. **Every temporary debug log carries one unique tag**, for example a prefix `[DEBUG-a4f2]` chosen for this
    session. Removal then is a single search for the tag; an untagged log survives into the commit. Prefer a
    debugger or REPL inspection to logs where the environment allows ("one breakpoint beats ten logs"), place
    logs at the boundaries that tell your candidates apart, and never "log everything and search it". This adds
    to `SKILL.md` §2.5, which still governs how to capture the call chain.
13. **A performance problem starts from a baseline, not from logs.** Measure first (a timing harness, a profiler,
    a query plan), then bisect. Logs distort timing and rarely tell regressions apart.
14. **Write the regression test before the fix only where there is a correct seam.** A correct seam exercises
    the real bug pattern as it happens at the call site. A test at too shallow a seam (a single-caller test for a
    bug that needs several callers) passes for the wrong reason and gives false confidence. If no correct seam
    exists, that is itself a finding: the structure of the code prevents locking the bug down, so record it
    rather than writing a weaker test. This narrows `SKILL.md` §3.4, which still requires the test at the origin.
15. **If you forced the red by editing code or a fixture, prove the edit landed.** Compare against a pristine
    copy before trusting the failure; then apply the fix, watch the test pass, and run the original loop against
    the full, un-minimised scenario.
16. **Cleanup is part of done.** The original repro no longer reproduces (the loop re-run); the regression test
    passes, or the missing seam is written down; a search for the debug tag finds nothing; throwaway harnesses are
    deleted or kept in a place marked as temporary; and the commit or the merge request message states which
    hypothesis turned out to be right, so the next person debugging this area learns from it.
