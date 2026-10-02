# testing-anti-patterns §7 — Isolation, order dependence and finding the polluter

> Section 7 of `skills/testing-anti-patterns`. Read it when a test passes alone and fails in the suite (or
> the reverse), when a run leaves a file, a row, a setting or a process behind, when tests share a port, a
> database or a directory, or before parallelism or random ordering is switched on. The other sections and
> the guardrails stay in `SKILL.md`.

1. **A test that depends on another test's leftovers is a bug in one of the two.** The signs: it passes
   alone and fails in the suite, it fails only when run after a particular file, it passes only because an
   earlier test created the row it reads, or a stray artefact (a file in the working directory, a row, a
   lock, an environment value) appears after a run. Order dependence is state shared through something the
   tests do not own.
2. **State that leaks is a short list.** Files and directories created outside the runner's temporary space;
   environment variables and the working directory; global and static state, singletons and module-level
   caches; database rows, sequences and open transactions; timers and pending promises; a mock or spy left
   installed; the locale, the time zone and the fake clock; listeners registered on shared objects; ports and
   sockets left open. Read this list against the failing test before reading anything else.
3. **Finding the polluter is a bisection, and the procedure is written once** in `skills/bug-triage` §6,
   point 9 (run the files one at a time or in halves, checking for the stray state after each). What this
   section adds is the reproduction: print the order and the seed of a failing run, put the victim last when
   halving the tests before it, and keep the failing order in the bug report.
4. **Fix the source, not the victim.** The polluter cleans up what it created in a teardown that runs even
   when the test fails (so the cleanup is not the last line of the test body). A victim that defends itself
   by deleting leftovers before it runs hides the next polluter and leaves it for a different victim.
   Temporary files go in the runner's temporary directory under unique names, the environment and the globals
   a test changes are restored after it (restored, not merely cleared), and spies and mocks are restored,
   not only reset.
5. **Random order exposes what a fixed order hides.** Run the suite in a random order regularly (in CI at
   least), with the seed printed in the output, so that an order-dependent failure is discovered when it is
   introduced and can be reproduced with the same seed. A suite that has only ever run in one order has
   never been tested for independence.
6. **Parallel workers share nothing implicitly.** Two workers using the same port, the same database, the same
   cache prefix or the same temporary path produce failures that appear on a busy machine and disappear on a
   quiet one. Each worker gets its own database or schema, its own port range and its own directory, derived
   from the worker's index. A resource that cannot be split is a serial test, declared as such.
7. **A shared fixture is read-only or rebuilt.** Expensive setup (a container, a seeded database) shared
   across tests is either never modified by them or restored to a known state between them, by rolling back a
   transaction, truncating, or recreating. "The tests happen not to touch each other's rows" is a coincidence
   with an expiry date.
8. **Time and randomness are inputs.** The test supplies the clock and the seed; tests that read the system
   clock fail at midnight, at month end and around a daylight-saving change, and a random value that is not
   seeded makes a failure unrepeatable. The seed is printed on failure.
9. **A flaky test is classified before it is fixed.** Run it alone many times: if it fails alone, the cause
   is inside it (a race, a timing guess, an unseeded random value); if it passes alone and fails in the suite,
   the cause is pollution (this section). Retrying until green is not a classification and teaches nothing.
