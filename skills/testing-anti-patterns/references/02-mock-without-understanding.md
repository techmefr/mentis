# testing-anti-patterns §2 — Mock without understanding what you removed

> Section 2 of `skills/testing-anti-patterns`. Read it when a collaborator is replaced, or a double is built from memory of a payload. The other sections and the guardrails stay in `SKILL.md`.

1. **Before mocking, know the real method's side effects** and whether the test depends on them.
   Mocking away a call that the test silently relied on gives a pass that means nothing.
2. **An incomplete mock fails silently.** A double returning only the three fields you thought about
   passes, while the real payload has twelve and the code reads a fourth. Build mocks from the real
   response shape, not from the fields you remembered.
3. Corollary already learned the hard way on our own stack: a mocked engine missing a method the code
   calls produces a crash that looks like a real bug, and hours go into the wrong hypothesis.
4. **Run it against the real implementation once**, if you can, before deciding what to mock.
