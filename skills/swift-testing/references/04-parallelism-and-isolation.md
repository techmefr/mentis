# swift-testing §4 — Parallelism and isolation

The Apple documentation pages "Parallelization" and "Migrating a test from XCTest", read 2026-10-08, with one
MIT-licensed iOS testing skill for the leak-check and main-actor advice. The parallel default applies to every
Swift Testing release; the toolchain-specific parts are in §1.

## 4.1 Parallel by default, in one process
1. **Swift Testing runs tests in parallel with respect to each other, using task groups, generally in one process.**
   The number running at once is up to the Swift runtime. The default in XCTest is the opposite: the tests of a
   suite run one after another. Code that "worked" under XCTest because of that sequence can fail intermittently
   after migration.
2. **Shared state is the usual cause:** global variables, a `static var` in a test file, a shared database file, a
   singleton, user defaults, a keychain item. Give each test its own instance: construct the subject in the suite's
   `init`, inject a fresh store, use a temporary location per test.
3. **Reproduce with parallelism on, repeated, in random order,** not once in file order; a flake that appears once
   in twenty runs is shared state.

## 4.2 `.serialized` is a stopgap
1. **Disable parallelism for a suite with the serialized trait,** which makes the suite's tests and sub-suites run
   one after another. The page says it is applied recursively: sub-suites and the tests in them are serialised too.
2. **It only orders the tests inside that suite.** It does not change how the suite runs relative to unrelated
   tests, and it has no effect if parallelism is globally disabled (for example with `--no-parallel`). Applied to a
   single non-parameterised test function it has no effect; on a parameterised test it makes the cases run one
   after another.
3. **Treat it as temporary.** The MIT skill's advice, which fits the page: use it to make a legacy suite stable
   and record a task to remove the shared state, because serialising hides the dependency and slows the suite.

## 4.3 Main actor and suite shape
1. **XCTest runs a synchronous test method on the main actor; Swift Testing runs a test function on an arbitrary
   task.** A test of a main-actor model must be isolated explicitly: `@MainActor` on the function, or on the
   suite type so every test inherits it, or run the thread-sensitive part inside the main-actor run helper the
   page names. Annotating the suite does not serialise it; tests still run in parallel.
2. **`confirmation()` and `withKnownIssue()` accept an isolation parameter,** to run their closure on a specific
   actor.
3. **Prefer a struct or an actor for a suite.** The compiler can then check concurrency safety. Use a class (or an
   actor) only when teardown needs `deinit`.
4. **`init` replaces `setUp` and `deinit` replaces `tearDown`;** keep each doing one thing, so a failure in setup
   names its cause.

## 4.4 Leaks and test doubles
1. **Check that the subject is released.** Hold the subject weakly in a teardown step and assert it is `nil`. In
   XCTest, `addTeardownBlock` does this and the check belongs in the factory that builds the subject, so every
   test gets it. Swift Testing has no `addTeardownBlock`, so the MIT skill uses a class suite with `deinit` or a
   helper that records the weak reference and checks it at the end.
2. **Keep doubles small and protocol-shaped.** A double that has grown past a hundred lines usually means the
   protocol it implements does too much (the MIT skill's rule of thumb); split the protocol rather than the
   double.
3. **Never reach the real network, disk or keychain from a unit test.** Replace the boundary with an injected
   double, and keep the real thing for a separate, small integration layer.
