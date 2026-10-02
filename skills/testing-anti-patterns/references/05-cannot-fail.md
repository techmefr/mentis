# testing-anti-patterns §5 — Tests that cannot fail, and defaults that pass for data

> Section 5 of `skills/testing-anti-patterns`. Read it when a negative test, a claim in a test title, a fallback value or a fixture is written. The other sections and the guardrails stay in `SKILL.md`.

1. **A negative test must be able to fail.** Before trusting "this input is rejected", feed it an input
   that should be accepted and confirm the test notices; an assertion on an error that the setup itself
   produces proves nothing about the rule.
2. **A positive test must exercise the quantity it claims to measure.** A test titled "retries three
   times" that stubs the retry loop, or "caches the result" that never reads twice, passes whatever the
   code does. Assert on the observable the title names.
3. **A default is not data.** Code that turns a failure into `[]`, `0` or `null` and a test that blesses
   it manufacture a result that nobody observed (`skills/gate` step 6). Test the failure path as a
   failure.
4. **A fixture uses values the world has reserved for examples, so a non-measurement is visible.** Use the
   example domains and the documentation address ranges that the standards set aside (RFC 2606 and 6761 for
   names, RFC 5737 and RFC 3849 for addresses) and the number ranges telephone regulators publish for
   fiction. Such a value cannot reach a real service or a real person, and it is unmistakable in an output:
   a result that still shows a reserved value was never fed real input, and a reserved value found in
   production data is a test that leaked. A fixture that looks like production data passes for a measurement
   nobody took.
