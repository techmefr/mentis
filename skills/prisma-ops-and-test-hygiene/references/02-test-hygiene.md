# prisma-ops-and-test-hygiene §2 — Test hygiene for Node services

A test is worth what it would catch. This section adds Node-specific hygiene to `testing-anti-patterns`
(which covers the general mistakes); it does not repeat them.

## 2.1 Assert the five outcomes
For a handler or use case, the outcomes that can change are: **the response**, **new public state** (what a
later read returns), **calls to external systems**, **messages on queues or events**, and **observability**
(an error logged, a metric moved). A test that checks only the response misses the other four. Pick the
ones the behaviour is for; for each effect, assert the state or the message actually produced, not that a
mock was called. Then check the test is real: break the implementation on purpose (remove the write, drop
the publish) and watch the test fail.

## 2.2 Servers on port 0
1. **Listen on port 0** in tests: the operating system assigns an unused port, which you read from the
   server's address after the listening event. Fixed ports collide when suites run in parallel or when a
   developer's service is up.
2. **Close the server in teardown** and wait for it; an open handle keeps the runner alive or leaks into the
   next file.
3. **In-process request injection** (a framework's inject method, or the supertest-style helper) avoids a
   port altogether for most handler tests; use a real listening server when the test is about the network
   (timeouts, keep-alive, streaming). In Nest, build the testing module and `app.init()` without `listen`.

## 2.3 Event emitters
1. **Listeners run synchronously, in registration order**, and an `emit` returns after the last one ran. A
   test that asserts "after emit" needs no wait; one that asserts something asynchronous must await the
   promise the listener returns or the event it emits.
2. **An `'error'` event with no listener throws** and takes the process down. Test the error path by
   attaching a listener (or by asserting the throw), not by hoping it is rare.
3. **Order is part of behaviour** when two listeners touch the same state; test with both registered in
   both orders if the order is not meant to matter.
4. **Remove listeners in teardown**; a leaked listener fires in the next test and fails it for no visible
   reason.

## 2.4 Never sleep
A sleep makes the test slow when it passes and flaky when the machine is busy. Wait for the condition:
await the promise, wait for the event, poll a predicate with a deadline, or use fake timers for code that
uses timers. If the code under test hides its completion (fire-and-forget), expose a handle that resolves
when it is done, or assert through an observable effect with a polling deadline. A test that needs a fixed
delay is a design signal.

## 2.5 Realistic data
1. **Build data that looks like production**: names with accents and apostrophes, long strings, empty
   collections, boundary numbers, time zones and daylight-saving edges. A test using `"foo"` and `1`
   passes against code that breaks on a real name.
2. **Use factories** with overrides, and keep each test's relevant values visible in the test, so a reader
   sees why it passes.
3. **Do not share mutable data between tests**; build per test or reset in teardown.

## 2.6 Test behaviour, not internals
Assert what a caller can observe. A test that reads private fields, stubs the module's own helpers, or
asserts the order of internal calls breaks when you refactor and still passes when behaviour is wrong.
Mock only the boundary you do not own (the network, the clock, the broker); let the rest run.

## 2.7 Verification
- Each new test failed against a deliberately broken implementation.
- The suite passes with tests run in random order and in parallel.
- No test contains a fixed sleep.
- No server in tests listens on a fixed port.

## 2.8 Nest mapping
Use the testing module to build the app, override only boundary providers, and prefer injection over a
listening server for handler tests; see `testing-anti-patterns` for mocking policy.
