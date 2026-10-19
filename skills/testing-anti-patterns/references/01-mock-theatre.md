# testing-anti-patterns §1 — Mock theatre: testing the double instead of the code

> Section 1 of `skills/testing-anti-patterns`. Read it when a double is introduced, or a test asserts that something was called. The other sections and the guardrails stay in `SKILL.md`.

1. **Never assert on a mock's existence or on the mock having been called** as the point of the test.
   That confirms your mock works. Assert on what the code *does*: the value returned, the state
   changed, what the caller observes.
2. **Red flag, mechanical**: if removing the mock makes the test fail for a reason other than a
   missing dependency, or if the mock setup is more than half the test, the test is about the mock.
3. **Mock at the lowest useful level**, usually the external boundary (network, clock, filesystem),
   not a high-level method of your own code. Mocking your own method mocks away the thing under test.
