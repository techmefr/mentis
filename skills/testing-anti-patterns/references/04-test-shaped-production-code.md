# testing-anti-patterns §4 — Test-shaped code in production

> Section 4 of `skills/testing-anti-patterns`. Read it when a reset helper, a test hook or an internal getter is added to a production class. The other sections and the guardrails stay in `SKILL.md`.

1. **A method that exists only for tests doesn't belong in the production class.** Reset helpers,
   internal-state getters, test hooks: move them into test utilities. Otherwise something eventually
   calls them for real.
2. Red flag: a public method whose only callers are in test files.
