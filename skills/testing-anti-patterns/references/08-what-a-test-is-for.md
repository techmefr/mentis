# testing-anti-patterns §8 — What a test is for

> Section 8 of `skills/testing-anti-patterns`. Read it when a test is written or named, when a failing test
> is about to be edited, when a suite is being pruned, or when a test is skipped. The other sections and the
> guardrails stay in `SKILL.md`.

1. **Every test names the break it catches, and a regression test is proven by reverting the fix.** Both are
   the law in `skills/tdd` §1 (points 5 and 6); this section is the review lens on them. A test whose name
   cannot say what it would mean for it to turn red guards nothing and is a candidate for deletion, and a
   regression test that was never seen red on the old behaviour guards nothing either.
2. **A test that pins a decision says so.** When the assertion exists because of a choice (a limit, an
   ordering, a format), the name carries the choice. Then a failure prompts "do we still want this", and
   changing the test is a recorded decision, not a repair to make the run green.
3. **One reason to fail.** A test with two acts or an assertion per unrelated property fails with a message
   that does not say which behaviour broke, and passes if the first assertion fails and hides the second. Split
   by behaviour; group assertions only when they describe one outcome.
4. **A failing test is read before it is edited.** The failure is either a defect in the code (fix the code),
   a changed specification (change the test and say so in the commit), or a defect in the test (a timing
   guess, leaked state, a wrong fixture). Deciding which comes first; editing the expectation to match the
   output is the wrong first move (§6, point 9).
5. **Skipping is a decision with an owner and a date.** A skipped test states why, who will unskip it and by
   when, in the test's name or the tracker; otherwise it is dead code that reports a larger suite than runs.
   A test that cannot be repaired is deleted, with the reason in the commit, since the history keeps it.
6. **Tests describe behaviour a caller depends on, not the structure that produces it.** A private method, an
   intermediate class, the number of calls and the order of internal steps are implementation; they change
   in a refactor that preserves behaviour, and a test of them fails for no reason. The measure of a good suite
   is that a behaviour-preserving refactor leaves it green.
7. **The cheapest layer that can show the defect owns the test.** A rule about a rounding mode is a unit
   test; the same rule asserted through a browser journey is slower, flakier and fails for twenty unrelated
   reasons (`skills/frontend-testing` for the layer table on an interface). A defect no layer owns is
   reported as a hole and not covered by stacking another test on the nearest one.
